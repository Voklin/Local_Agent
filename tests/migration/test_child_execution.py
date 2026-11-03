"""Real parent-child-parent HTTP sequence, cancellation and stale source handback."""
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler
from tests.migration import test_run_control as fixture


class ChildHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"data":[{"id":"fixture"}]}')

    def do_POST(self):
        p=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(p)
        if getattr(self.server,'oom',False):
            self.send_response(500);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"error":{"message":"CUDA out of memory","type":"server_error"}}');return
        user=next(m['content'] for m in reversed(p['messages']) if m['role']=='user' and isinstance(m.get('content'),str) and m['content'] in ('parent','child'))
        if user=='child' and getattr(self.server,'fail_child',False):
            self.send_response(500);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(b'{"error":{"message":"fixture unavailable","type":"server_error"}}');return
        replied=any(m['role']=='tool' for m in p['messages'])
        if not replied:
            name,args=('delegate_readonly',{'task':'child',**({'profile_id':self.server.profile_id} if getattr(self.server,'profile_id',None) else {})}) if user=='parent' else ('read_range',{'path':'main.py','start_line':1,'end_line':3})
            if user=='parent' and getattr(self.server,'draft_profile',False):name,args='create_subagent_profile',{'title':'Архитектор','summary':'Исследовать устройство проекта','instructions':'Читай нужные файлы и объясняй связи между компонентами.','tools':['read_range']}
            if user=='child' and getattr(self.server,'malicious_child',False):name,args='write_file',{'path':'forbidden.txt','content':'not allowed','overwrite':False}
            delta={'tool_calls':[{'index':0,'id':'call','type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}
        else:delta={'content':'child answer' if user=='child' else 'parent answer'}
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        self.wfile.write(('data: '+json.dumps({'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if 'tool_calls' in delta else 'stop'}]})+'\n\n').encode());self.wfile.flush()
        if user=='child' and self.server.hold:
            self.server.waiting.set();self.server.release.wait(10)
        try:self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()
        except OSError:pass


class ChildExecutionTests(unittest.TestCase):
    setUp=fixture.RunControlHttpTests.setUp
    stop_server=fixture.RunControlHttpTests.stop_server
    event=fixture.RunControlHttpTests.event

    def start(self,hold=False,options=None):
        self.server.RequestHandlerClass=ChildHandler;self.server.hold=hold;self.server.waiting=threading.Event();self.server.release=threading.Event();self.addCleanup(self.server.release.set)
        (self.root/'main.py').write_text('value = 1\n')
        self.service.config['tool_protocol']='native'
        self.service.start(self.root,{'mode':'ide','prompt':'parent','task_options':options or {}})

    def test_parent_child_handoff_joins_and_ledger_matches_real_http(self):
        self.start();self.event('task_end')
        self.assertEqual(len(self.server.requests),4)
        runs=self.service.registry.history(self.service.chat['id']);parent=next(r for r in runs if not r['parent_id']);child=next(r for r in runs if r['parent_id'])
        self.assertEqual(child['parent_id'],parent['id']);self.assertEqual(child['state'],'completed')
        self.assertEqual(sum(r['ledger']['http_attempts'] for r in runs),4)
        self.assertTrue(all(r['ledger']['active_reserved_tokens']==0 for r in runs))
        child_request=self.server.requests[1]
        self.assertFalse({'write_file','delegate_readonly','run_project_command'}&{t['function']['name'] for t in child_request['tools']})
        result=json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))
        self.assertTrue(result['ok']);self.assertEqual(result['text'],'child answer');self.assertEqual(result['sources'][0]['path'],'main.py')
        self.assertEqual(self.service.chat['task_checkpoint']['children'][0]['state'],'completed')
        self.assertTrue(self.service.chat['task_checkpoint']['children'][0]['activity'])

    def test_parent_cancel_cascades_and_closes_child_transport(self):
        self.start(hold=True);self.assertTrue(self.server.waiting.wait(5));self.service.cancel();self.server.release.set();self.service.thread.join(5)
        self.assertFalse(self.service.task_running);self.assertFalse(self.service.scheduler.status()['busy'])
        runs=self.service.registry.history(self.service.chat['id'])
        self.assertTrue(all(r['state']=='paused' for r in runs));self.assertEqual(len(self.server.requests),2)

    def test_child_transport_failure_returns_control_to_parent(self):
        """A bounded child inference failure is data for the parent, not a fatal parent exception."""
        self.server.fail_child=True;self.start();self.event('task_end')
        result=json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))
        self.assertFalse(result['ok']);self.assertEqual(result['state'],'failed')
        self.assertEqual(self.service.chat['task_checkpoint']['status'],'completed')
        self.assertEqual(self.service.chat['messages'][-1]['content'],'parent answer')
        self.assertEqual(len(self.server.requests),5)
        self.assertFalse(self.service.scheduler.status()['busy'])

    def test_changed_source_discards_entire_child_answer(self):
        self.start(hold=True);self.assertTrue(self.server.waiting.wait(5))
        # First child request is still held before its read. Let that complete,
        # then hold the final child response after the tool has read its source.
        self.server.hold=False
        # Deterministically alter the source in the child completion callback.
        owner=self.service.selected_run()
        original=owner.engine._checkpoint
        def checkpoint(*args,**kwargs):
            children=owner.engine._task.get('children',[])
            if children and children[-1]['state']=='completed':(self.root/'main.py').write_text('value = 2\n')
            return original(*args,**kwargs)
        owner.engine._checkpoint=checkpoint
        self.server.release.set()
        self.event('task_end')
        result=json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))
        self.assertEqual(result['code'],'STALE_CHILD_RESULT');self.assertNotIn('text',result)

    def test_memory_exhaustion_pauses_without_retry(self):
        self.server.oom=True;self.start()
        while self.events.get(timeout=10)['event']!='task_end':pass
        self.assertEqual(len(self.server.requests),1)
        self.assertEqual(self.service.chat['task_checkpoint']['run_state'],'paused')
        self.assertIn('нехватку памяти',self.service.chat['task_checkpoint']['stop_reason'])

    def test_child_cannot_gain_write_permission_from_model_output(self):
        self.server.malicious_child=True;self.start()
        self.event('task_end')
        self.assertFalse((self.root/'forbidden.txt').exists())
        self.assertFalse(any(e['event']=='approval' for e in list(self.events.queue)))

    def test_explicit_external_budget_blocks_before_physical_http(self):
        from unittest.mock import patch
        policy={'enabled':True,'amount':.000000001,'input_per_million':1,'output_per_million':1,'currency':'USD'}
        self.service.config['settings']['paid_budget']=policy
        with patch('agent.auto_budget.local_endpoint',return_value=False):
            self.start()
            while self.events.get(timeout=10)['event']!='task_end':pass
        self.assertEqual(self.server.requests,[])
        self.assertEqual(self.service.chat['task_checkpoint']['run_state'],'paused')


    def test_user_profile_narrows_child_tools_and_persists_exact_version(self):
        profile=self.service.extensions.subagents.configure({'title':'Точный читатель','summary':'Только диапазоны','instructions':'Читай только нужные строки; верни факты с путями.','tools':['read_range'],'enabled':True})
        self.server.profile_id=profile['id'];self.start();self.event('task_end')
        child=self.server.requests[1]
        names={t['function']['name'] for t in child['tools']}
        self.assertIn('read_range',names);self.assertNotIn('read_file',names);self.assertNotIn('list_files',names)
        self.assertNotIn('create_subagent_profile',names);self.assertNotIn('delegate_readonly',names)
        result=json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))
        self.assertTrue(result['ok']);self.assertEqual(result['profile']['id'],profile['id'])
        from agent.task_store import load_task
        self.assertEqual(load_task(result['run_id'])['subagent_profile'],profile)

    def test_disabled_profile_does_not_create_child_or_inference(self):
        profile=self.service.extensions.subagents.configure({'title':'Черновик','summary':'Не запускать','instructions':'Читай файлы только по задаче родителя.','tools':['read_range']},generated=True)
        self.server.profile_id=profile['id'];self.start();self.event('task_end')
        self.assertEqual(len(self.server.requests),2)
        self.assertFalse(any(r['parent_id'] for r in self.service.registry.history(self.service.chat['id'])))
        result=json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))
        self.assertEqual(result['code'],'ACCESS_DENIED')

    def test_disabling_subagents_preserves_single_agent_without_child_tools(self):
        self.service.extensions.subagents.configure({'kind':'subagents_toggle','enabled':False})
        self.start();self.event('task_end')
        names={t['function']['name'] for t in self.server.requests[0]['tools']}
        self.assertFalse({'delegate_readonly','create_subagent_profile'} & names)
        self.assertIn('read_range',names)

    def test_chat_explains_subagent_mode_without_exposing_project_tools(self):
        self.server.RequestHandlerClass=ChildHandler
        self.service.config['tool_protocol']='native'
        self.service.start('',{'mode':'chat','prompt':'parent'})
        self.event('task_end')
        request=self.server.requests[0]
        names={t['function']['name'] for t in request['tools']}
        self.assertFalse({'delegate_readonly','create_subagent_profile','read_range'} & names)
        self.assertIn('режиме IDE',request['messages'][0]['content'])
        self.assertIn('не подключены',request['messages'][0]['content'])
        self.assertFalse(any(r['parent_id'] for r in self.service.registry.history(self.service.chat['id'])))

    def test_readonly_parent_hint_matches_child_capabilities(self):
        self.start(options={'read_only':True});self.event('task_end')
        request=self.server.requests[0]
        self.assertIn('delegate_readonly',request['messages'][0]['content'])
        self.assertNotIn('create_subagent_profile',request['messages'][0]['content'])
        self.assertNotIn('create_subagent_profile',{t['function']['name'] for t in request['tools']})
        self.assertEqual(self.service.chat['task_checkpoint']['children'][0]['state'],'completed')


    def test_model_creates_only_disabled_draft_via_real_tool_dispatch(self):
        self.server.draft_profile=True;self.start();self.event('task_end')
        self.assertEqual(len(self.server.requests),2)
        drafts=[p for p in self.service.extensions.subagents.catalog()['profiles'] if p['source']=='model']
        self.assertEqual(len(drafts),1);self.assertFalse(drafts[0]['enabled'])
        self.assertFalse(any(r['parent_id'] for r in self.service.registry.history(self.service.chat['id'])))
        self.assertIn('Выключенный черновик',json.loads(next(m['content'] for m in self.service.chat['messages'] if m['role']=='tool'))['note'])
