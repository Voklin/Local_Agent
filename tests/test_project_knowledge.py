"""Freshness, provenance, project scope, CAS and bounded prompt memory."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent import project_memory, task_store
from agent.project_knowledge import ProjectKnowledge, remember_from_model
from agent.workspace_access import filter_model_history
from core.python.memory_service import read_memory, memory_action, write_memory


class ProjectKnowledgeTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.base=Path(temp.name);self.root=self.base/'repo';self.root.mkdir()
        (self.root/'main.py').write_text('VALUE = 1\n')
        for module,key,value in [(project_memory,'MEMORY_DIR',self.base/'memory'),(task_store,'TASK_DIR',self.base/'profile/tasks')]:
            scoped=patch.object(module,key,value);scoped.start();self.addCleanup(scoped.stop)
        self.knowledge=ProjectKnowledge(self.root)

    def put(self,**extra):
        return self.knowledge.put({'kind':'decision','text':'Используем VALUE для расчётов','paths':['main.py'],**extra})

    def test_new_instance_finds_decision_and_timestamp_does_not_change_on_reads(self):
        item=self.put();fresh=ProjectKnowledge(self.root);results=fresh.listing('VALUE',model=True)
        self.assertEqual(results[0]['id'],item['id']);self.assertEqual(results[0]['state'],'source_current')
        self.assertEqual(fresh.listing()[0]['created_at'],item['created_at'])
        other=self.base/'other';other.mkdir();self.assertEqual(ProjectKnowledge(other).listing(),[])

    def test_file_changes_deletion_and_revocation_remove_entire_model_note(self):
        item=self.put();(self.root/'main.py').write_text('VALUE = 2\n')
        self.assertEqual(self.knowledge.listing()[0]['state'],'stale');self.assertEqual(self.knowledge.context('VALUE'),'')
        self.put(id=item['id']);(self.root/'.neutralignore').write_text('main.py\n')
        self.assertEqual(self.knowledge.listing()[0]['state'],'revoked');self.assertEqual(self.knowledge.listing(model=True),[])
        (self.root/'.neutralignore').unlink();(self.root/'main.py').unlink()
        self.assertEqual(self.knowledge.listing()[0]['state'],'missing')

    def test_policy_change_invalidates_sourceless_decision_and_gitignore_source(self):
        self.put(paths=[]);(self.root/'.neutralignore').write_text('other.py\n')
        self.assertEqual(self.knowledge.listing(model=True),[])
        (self.root/'.neutralignore').unlink();self.put();(self.root/'.gitignore').write_text('main.py\n')
        self.assertFalse(any(r['sources'] for r in self.knowledge.listing(model=True)))

    def test_ui_cas_preserves_external_edits_and_rejects_root_switch(self):
        initial=read_memory(str(self.root));self.put()
        with self.assertRaisesRegex(ValueError,'MEMORY_CHANGED'):memory_action(self.root,{'root':str(self.root),'revision':initial['revision'],'action':'delete','id':'fake'})
        current=read_memory(str(self.root));fields={**current['memory'],'project_summary':'Мои заметки'}
        write_memory(self.root,{'memory':fields,'revision':current['revision'],'root':str(self.root)})
        with self.assertRaises(ValueError):memory_action(self.root,{'root':str(self.base),'action':'search'})
        self.assertIn('Мои заметки',project_memory.current_user_notes(self.root))
        (self.root/'.neutralignore').write_text('main.py\n')
        self.assertEqual(project_memory.current_user_notes(self.root),'')

    def test_model_proposal_cannot_promote_or_anchor_unread_sources(self):
        task={'chat_id':'a'*32,'journal_id':'b'*32}
        with self.assertRaises(ValueError):remember_from_model(self.root,{'text':'Неподтверждённый вывод','paths':['main.py']},task)
        record=self.knowledge.put({'kind':'fact','text':'Неподтверждённый вывод','paths':['main.py']},origin='model',provenance={'source':'model'})
        self.assertEqual(record['kind'],'hypothesis');self.assertEqual(self.knowledge.listing()[0]['state'],'hypothesis')
        with self.assertRaises(ValueError):self.put(paths=['../other.py'])

    def test_old_tool_memory_is_reprojected_after_revocation_without_changing_history(self):
        item=self.put(text='PRIVATE_MEMORY_DATA')
        messages=[{'role':'assistant','content':None,'tool_calls':[{'id':'memory','function':{'name':'search_project_memory','arguments':'{"query":"VALUE"}'}}]},
            {'role':'tool','tool_call_id':'memory','content':json.dumps({'ok':True,'records':[item]})}]
        self.assertIn('PRIVATE_MEMORY_DATA',filter_model_history(messages,self.root)[1]['content'])
        (self.root/'.neutralignore').write_text('main.py\n')
        projected=filter_model_history(messages,self.root)
        self.assertNotIn('PRIVATE_MEMORY_DATA',projected[1]['content']);self.assertIn('PRIVATE_MEMORY_DATA',messages[1]['content'])

    def test_legacy_and_model_notes_are_not_automatically_presented_as_current(self):
        path=project_memory.memory_path(str(self.root));path.parent.mkdir(parents=True);path.write_text(json.dumps({'project_summary':'Старые выводы'}))
        self.assertEqual(project_memory.current_user_notes(self.root),'')
        project_memory.save_project_memory(str(self.root),{'project_summary':'Предположение модели'},origin='model')
        self.assertEqual(project_memory.current_user_notes(self.root),'')
        self.assertEqual(read_memory(self.root)['memory']['project_summary'],'Предположение модели')

    def test_context_is_bounded_and_no_semantic_verification_is_invented(self):
        for n in range(15):self.put(text='VALUE решение '+str(n)+' '+'x'*450,paths=[])
        text=self.knowledge.context('VALUE',max_chars=1800)
        self.assertLessEqual(len(text),1800);self.assertIn('не доказанность вывода',text)
        self.assertLessEqual(len(self.knowledge.listing('VALUE',model=True,limit=3)),3)


    def test_fitted_memory_is_removed_after_change_and_metadata_never_reaches_api(self):
        from agent.project_knowledge import memory_projection,validate_memory_projection,MEMORY_MARKER
        from agent.request_budget import prepare_model_request
        self.put(text='PRIVATE_MEMORY_DATA')
        message=memory_projection(self.root,'PRIVATE_MEMORY_DATA');self.assertIsNotNone(message)
        prepared=prepare_model_request({'messages':[message]})
        self.assertNotIn(MEMORY_MARKER,prepared['messages'][0])
        (self.root/'main.py').write_text('VALUE = 2\n')
        self.assertEqual(validate_memory_projection([message],self.root),[])


    def test_http_retry_rechecks_fitted_memory_before_second_post(self):
        import threading
        from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
        from agent.model_client import ModelClient
        from agent.project_knowledge import memory_projection
        captured=[];root=self.root
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                captured.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                retry=len(captured)==1
                if retry:(root/'main.py').write_text('VALUE = 2\n')
                self.send_response(500 if retry else 200);self.send_header('Content-Type','application/json');self.end_headers()
                payload={'error':{'message':'temporary'}} if retry else {'choices':[{'message':{'content':'OK'},'finish_reason':'stop'}]}
                self.wfile.write(json.dumps(payload).encode())
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.put(text='PRIVATE_MEMORY_DATA');client=ModelClient(f'http://127.0.0.1:{server.server_port}/v1','',threading.Event());client.context_root=str(self.root)
        try:client.create(model='fixture',messages=[{'role':'system','content':'rules'},memory_projection(self.root,'PRIVATE_MEMORY_DATA'),{'role':'user','content':'question'}],max_tokens=100,stream=False)
        finally:client.close();server.shutdown();server.server_close();thread.join(2)
        self.assertEqual(len(captured),2);self.assertIn('PRIVATE_MEMORY_DATA',json.dumps(captured[0]));self.assertNotIn('PRIVATE_MEMORY_DATA',json.dumps(captured[1]))


    def test_corrupt_record_catalog_is_reported_without_rewriting_it(self):
        self.put();raw=self.knowledge.path.read_bytes();data=json.loads(raw);data['records'][0].pop('created_at');self.knowledge.path.write_text(json.dumps(data))
        before=self.knowledge.path.read_bytes()
        with self.assertRaises(ValueError):self.knowledge.listing()
        self.assertEqual(before,self.knowledge.path.read_bytes())
