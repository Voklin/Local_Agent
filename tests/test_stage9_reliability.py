"""Regression scenarios for the five post-stage-eight audit findings and maintenance jobs."""
import json
import os
import queue
import subprocess
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from agent import task_store
from agent.json_tools import JsonToolStream, parse_tool_json
from agent.workspace_access import WorkspaceAccessPolicy,filter_model_history
from agent.workspace_read import read_range
from agent.workspace_search import search_project
from agent.workspace_revision import WorkspaceRevisionService
from agent.tools import read_file,list_files
from agent.verifier import StageVerifier
from agent.verification_evidence import capture_witness,make_receipt,now
from agent.language_diagnostics import diagnose
from agent.operation_context import OperationContext
from agent.storage import Storage
from core.python.background_job import BackgroundJob
from core.python.editor_service import EditorService


class Stage9Tests(unittest.TestCase):
    """Use disposable workspaces; never read user files or call a model."""
    def setUp(self):
        """Separate source files and permission metadata for each scenario."""
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)/'project';self.root.mkdir()
        self.source=self.root/'main.py';self.source.write_text('print(1)\n',encoding='utf-8')
        context=patch.object(task_store,'TASK_DIR',Path(temp.name)/'profile/tasks');context.start();self.addCleanup(context.stop)

    def test_json_rejects_suffix_second_object_duplicate_keys_and_nan(self):
        """Ambiguous input cannot become an effectful call."""
        envelope='{"tool_calls":[{"name":"read_file","arguments":{"path":"main.py"}}]}'
        for text in (envelope+' example',envelope+' {}','{"tool":"read_file","arguments":{"path":"a","path":"b"}}','{"tool":"read_file","arguments":{"value":NaN}}'):
            with self.subTest(text=text),self.assertRaises(ValueError):parse_tool_json(text,{'read_file'})
        self.assertEqual(parse_tool_json('Example: '+envelope,{'read_file'}),[])
        self.assertEqual(len(parse_tool_json('```json\n'+envelope+'\n```',{'read_file'})),1)

    def test_versioned_json_and_incomplete_stream_share_terminal_contract(self):
        """Versioned final text is visible, while missing stop evidence yields no calls."""
        tool=json.dumps({'protocol':'neutral.action.v1','kind':'tool','name':'read_file','arguments':{'path':'main.py'}})
        self.assertEqual(len(parse_tool_json(tool,{'read_file'})),1)
        chunks=[NS(choices=[NS(delta=NS(content=tool),finish_reason=None)])]
        result=list(JsonToolStream(chunks,{'read_file'},'auto'))[0].choices[0]
        self.assertEqual(result.delta.tool_calls,[]);self.assertEqual(result.finish_reason,'unknown')
        final=json.dumps({'protocol':'neutral.action.v1','kind':'final','text':'Готово'})
        chunks=[NS(choices=[NS(delta=NS(content=final),finish_reason='stop')])]
        self.assertEqual(list(JsonToolStream(chunks,set(),'auto'))[0].choices[0].delta.content,'Готово')

    def test_editor_and_external_changes_invalidate_content_evidence(self):
        """Manual editor saves and same-size backdated writes invalidate successful checks."""
        task={'project_root':str(self.root),'test_results':[]};verifier=StageVerifier()
        args={'program':'fixture'};result={'ok':True,'exit_code':0};witness=capture_witness(self.root,{'kind':'workspace'})
        verifier.record_command(task,args,{**result,'verification_receipt':make_receipt(args,{'kind':'workspace'},witness,witness,result,started_at=now())})
        self.assertEqual(verifier.command_summary(task)['status'],'commands_passed')
        editor=EditorService();current=editor.read(self.root,'main.py')
        proposal=editor.preview(self.root,{'path':'main.py','content':'print(2)\n','revision':current['revision']})
        self.assertTrue(editor.resolve(self.root,{'proposal_id':proposal['proposal_id'],'decision':'apply'})['applied'])
        self.assertEqual(verifier.command_summary(task)['status'],'stale')
        witness=capture_witness(self.root,{'kind':'workspace'})
        verifier.record_command(task,args,{**result,'verification_receipt':make_receipt(args,{'kind':'workspace'},witness,witness,result,started_at=now())})
        old=self.source.stat();self.source.write_text('print(3)\n',encoding='utf-8');os.utime(self.source,ns=(old.st_atime_ns,old.st_mtime_ns))
        self.assertEqual(verifier.command_summary(task)['status'],'stale')

    def test_legacy_and_over_budget_revisions_cannot_certify_checks(self):
        """Missing coverage never gets silently promoted to current evidence."""
        task={'project_root':str(self.root),'test_results':[]};verifier=StageVerifier()
        verifier.record_command(task,{'program':'fixture'},{'ok':True,'exit_code':0})
        self.assertEqual(verifier.command_summary(task)['status'],'stale')
        self.assertFalse(WorkspaceRevisionService.capture(self.root,max_bytes=1)['complete'])

    def test_shared_access_policy_requires_exact_user_exception(self):
        """All automatic readers obey the same rules; the manual editor remains usable."""
        (self.root/'.env').write_text('SYNTHETIC_SECRET=fixture',encoding='utf-8')
        (self.root/'private.txt').write_text('SYNTHETIC_SECRET=second',encoding='utf-8')
        (self.root/'.neutralignore').write_text('private.txt\n',encoding='utf-8')
        for reader in (lambda:read_file(self.root,'.env'),lambda:read_range(self.root,'private.txt')):
            with self.assertRaises(PermissionError):reader()
        self.assertNotIn('.env',[e['path'] for e in list_files(self.root)['entries']])
        self.assertEqual(search_project(self.root,{'mode':'text','query':'SYNTHETIC_SECRET'})['matches'],[])
        self.assertIn('SYNTHETIC_SECRET',EditorService().read(self.root,'.env')['content'])
        policy=WorkspaceAccessPolicy(self.root)
        with self.assertRaises(ValueError):policy.configure(['.env'],False)
        with self.assertRaises(ValueError):policy.configure(['.'],True)
        policy.configure(['.env'],True)
        self.assertIn('SYNTHETIC_SECRET',read_range(self.root,'.env')['content'])
        with self.assertRaises(PermissionError):read_file(self.root,'private.txt')
        policy.configure([],True)
        with self.assertRaises(PermissionError):read_file(self.root,'.env')

    def test_delayed_lsp_replaces_initial_empty_and_pull_is_preferred(self):
        """A real stdio server's delayed result must not be lost after an empty publish."""
        fixture=Path(__file__).parent/'fixtures/lsp_diagnostics.py'
        for mode in ('--late','--pull'):
            settings={'program':sys.executable,'arguments':['-u',str(fixture),mode],'language':'python'}
            result=diagnose(self.root,'main.py',settings,OperationContext(5))
            self.assertEqual(result['diagnostics'][0]['message'],'Delayed fixture error')
            self.assertEqual(result['complete'],mode=='--pull')

    def test_policy_metadata_cannot_be_granted_or_changed_as_a_project_file(self):
        """A workspace containing the profile cannot let the model rewrite its own grants."""
        with patch.object(task_store,'TASK_DIR',self.root/'runtime/tasks'):
            policy=WorkspaceAccessPolicy(self.root);policy.configure([],True)
            with self.assertRaises(PermissionError):policy.require('runtime/workspace-access.json',mutation=True)
            with self.assertRaises(ValueError):policy.configure(['runtime/workspace-access.json'],True)

    def test_revocation_filters_known_saved_results_without_deleting_chat(self):
        """Revoked file content and its artifact-reader copy do not enter a new model request."""
        (self.root/'.env').write_text('SYNTHETIC_SECRET=fixture',encoding='utf-8')
        history=[{'role':'assistant','tool_calls':[{'id':'read','function':{'name':'read_file','arguments':'{"path":".env"}'}}]},
            {'role':'tool','tool_call_id':'read','content':json.dumps({'path':'.env','content':'SYNTHETIC_SECRET'})},
            {'role':'assistant','tool_calls':[{'id':'again','function':{'name':'read_tool_result','arguments':'{"message_index":1,"call_id":"read"}'}}]},
            {'role':'tool','tool_call_id':'again','content':'SYNTHETIC_SECRET'}]
        policy=WorkspaceAccessPolicy(self.root);policy.configure(['.env'],True)
        self.assertIn('SYNTHETIC_SECRET',filter_model_history(history,self.root)[1]['content'])
        policy.configure([],True)
        projected=filter_model_history(history,self.root)
        self.assertNotIn('SYNTHETIC_SECRET',projected[1]['content']);self.assertNotIn('SYNTHETIC_SECRET',projected[3]['content'])
        self.assertNotIn('SYNTHETIC_SECRET',filter_model_history(history[2:],self.root)[1]['content'])
        self.assertIn('SYNTHETIC_SECRET',history[1]['content'])

    def test_background_job_cancel_and_duplicate_are_bounded(self):
        """Cancellation keeps the worker slot occupied until completion is delivered."""
        job=BackgroundJob();self.addCleanup(job.shutdown);started=threading.Event();finished=threading.Event();results=[]
        def work(context):
            """Wait cooperatively without blocking the caller thread."""
            started.set();context.wait(5);return {'value':1}
        def respond(value):
            """Capture the correlated result and wake the test."""
            results.append(value);finished.set()
        job.start(work,respond);self.assertTrue(started.wait(1))
        with self.assertRaises(ValueError):job.start(work,respond)
        job.cancel();self.assertTrue(finished.wait(2));self.assertFalse(results[0]['ok'])

    def test_cancelled_backup_preserves_existing_destination(self):
        """A cancellation cannot replace the user's existing archive."""
        target=self.root.parent/'backup.zip';target.write_bytes(b'original archive')
        context=OperationContext();context.set()
        database=Storage(task_store.TASK_DIR.parent).ready()
        with self.assertRaises(ValueError):database.backup(target,cancelled=context)
        self.assertEqual(target.read_bytes(),b'original archive')

    def test_backup_commit_is_not_relabelled_cancelled_after_replace(self):
        """Cancellation arriving after atomic commit must report the archive that was saved."""
        target=self.root.parent/'committed.zip';database=Storage(task_store.TASK_DIR.parent).ready()
        job=BackgroundJob();self.addCleanup(job.shutdown);finished=threading.Event();results=[]
        replace=os.replace
        def commit(source,destination):
            """Request a late cancellation immediately after the real atomic replacement."""
            replace(source,destination);job.cancel()
        def work(context):
            """Build a real archive while cancellation occurs exactly at its commit boundary."""
            with patch('agent.storage.os.replace',side_effect=commit):return database.backup(target,cancelled=context)
        def respond(value):
            """Capture the final maintenance result after the late cancel signal."""
            results.append(value);finished.set()
        job.start(work,respond);self.assertTrue(finished.wait(5));self.assertTrue(results[0]['ok']);self.assertTrue(target.is_file())

    def test_real_bridge_health_and_cancel_respond_during_backup(self):
        """Real JSON-lines dispatch stays responsive while a background backup is blocked."""
        code=('from core.python import bridge as b\nfrom agent.storage import Storage\n'
              'def slow(self,destination,*,cancelled=None):\n'
              ' b.emit({"event":"fixture_backup_started"})\n'
              ' cancelled.wait(10)\n'
              ' raise ValueError("fixture cancellation")\n'
              'Storage.backup=slow\nb.main()\n')
        process=subprocess.Popen([sys.executable,'-u','-c',code],cwd=Path(__file__).resolve().parents[1],
            env={**os.environ,'LOCALAPPDATA':str(self.root.parent/'bridge-profile'),'PYTHONIOENCODING':'utf-8'},
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8')
        messages=queue.Queue()
        def read():
            """Collect actual bridge replies without blocking the test's request thread."""
            for line in process.stdout:messages.put(json.loads(line))
        reader=threading.Thread(target=read,daemon=True);reader.start()
        def send(identity,method,params=None):
            """Write one framed test request to the child bridge."""
            process.stdin.write(json.dumps({'id':identity,'method':method,'params':params or {}})+'\n');process.stdin.flush()
        try:
            send(1,'storage_backup',{'path':str(self.root.parent/'fixture.zip')})
            self.assertEqual(messages.get(timeout=10).get('event'),'fixture_backup_started')
            send(2,'health');reply=messages.get(timeout=2)
            self.assertEqual(reply['id'],2);self.assertTrue(reply['ok'])
            send(3,'storage_cancel');replies=[messages.get(timeout=3),messages.get(timeout=3)]
            self.assertTrue(next(r for r in replies if r['id']==3)['ok'])
            self.assertFalse(next(r for r in replies if r['id']==1)['ok'])
        finally:
            process.stdin.close()
            try:process.wait(5)
            except subprocess.TimeoutExpired:process.kill();process.wait(3)
            reader.join(1);process.stdout.close()


if __name__=='__main__':unittest.main()
