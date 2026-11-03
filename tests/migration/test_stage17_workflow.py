"""Actual checks-only LSP approvals and a real Core private checkpoint API."""
from pathlib import Path
import shutil
import sys
import unittest
from tests.migration import test_run_control as fixture
import test_bridge_process as bridge_fixture

LSP=Path(__file__).parents[1]/'fixtures/lsp_diagnostics.py'


class Stage17HttpTests(unittest.TestCase):
    setUp=fixture.RunControlHttpTests.setUp
    stop_server=fixture.RunControlHttpTests.stop_server
    event=fixture.RunControlHttpTests.event

    def run_lsp(self, clean):
        (self.root/'main.py').write_text('VALUE = 1\n')
        self.service.extensions.configure({'kind':'groups','id':'commands','enabled':True})
        self.service.optional.settings['lsp']={'enabled':True,'program':sys.executable,'arguments':[str(LSP),'--pull']+(['--clean'] if clean else []),'language':'python','seconds':5}
        options={'checks_only':True,'criteria':['Полная LSP проверка без ошибок'],'criteria_links':{'0':['lsp']},'checks':[{'id':'lsp','kind':'diagnostics','purpose':'LSP main.py','program':'lsp','arguments':['main.py'],'cwd':'.','timeout':5,'evidence_scope':{'kind':'files','files':['main.py'],'dependencies':[]}}]}
        self.service.start(self.root,{'mode':'ide','task_options':options})
        while True:
            event=self.events.get(timeout=10)
            if event['event']=='task_end':self.fail(str(self.service.chat.get('task_checkpoint')))
            if event['event']=='failed':self.fail(event.get('text','failed'))
            if event['event']=='approval':break
        self.assertIn('main.py',event['diff']);self.assertIn('lsp_diagnostics.py',event['diff'])
        self.service.resolve_approval({**event,'decision':'apply'});self.event('task_end');self.service.thread.join(5)
        self.assertEqual(self.server.requests,[])
        return self.service.chat['task_checkpoint']

    def test_complete_lsp_check_and_criterion_pass_without_model_http(self):
        task=self.run_lsp(True)
        self.assertEqual(task['run_state'],'completed');self.assertEqual(task['verification']['status'],'scoped_passed')
        self.assertEqual(task['acceptance_evidence'][0]['status'],'scoped_checks_passed')
        self.service.optional.settings['lsp']['language']='typescript'
        task,_=self.service._recover_chat();self.assertEqual(task['verification']['status'],'stale')

    def test_lsp_error_keeps_task_paused_and_does_not_satisfy_criterion(self):
        task=self.run_lsp(False)
        self.assertEqual(task['run_state'],'paused');self.assertEqual(task['verification']['status'],'failed')
        self.assertEqual(task['acceptance_evidence'][0]['status'],'failed')


class Stage17BridgeTests(unittest.TestCase):
    setUp=bridge_fixture.BridgeProcessTests.setUp
    tearDown=bridge_fixture.BridgeProcessTests.tearDown
    start_process=bridge_fixture.BridgeProcessTests.start_process
    read_output=bridge_fixture.BridgeProcessTests.read_output
    call=bridge_fixture.BridgeProcessTests.call
    until=bridge_fixture.BridgeProcessTests.until
    start_crash_scenario=bridge_fixture.BridgeProcessTests.start_crash_scenario
    stop_process=bridge_fixture.BridgeProcessTests.stop_process

    def test_checkpoint_api_saves_confirmed_write_and_keeps_core_responsive(self):
        if not shutil.which('git'):self.skipTest('Git unavailable')
        chat_id=self.start_crash_scenario(bridge_fixture.ModelHandler)
        approval=self.until(lambda r:r.get('event')=='approval')
        self.assertTrue(self.call('resolve_approval',run_id=approval['run_id'],approval_id=approval['approval_id'],decision='apply')['ok'])
        self.until(lambda r:r.get('event')=='task_end')
        groups=self.call('snapshot_list',chat_id=chat_id);group=groups['snapshots'][0]['id']
        self.counter+=1;request_id=self.counter
        self.process.stdin.write(__import__('json').dumps({'id':request_id,'method':'snapshot_checkpoint','params':{'chat_id':chat_id,'group_id':group}})+'\n');self.process.stdin.flush()
        self.assertTrue(self.call('health')['ok'])
        result=self.until(lambda r:r.get('id')==request_id)
        self.assertTrue(result['ok'],result);self.assertEqual(result['checkpoint']['source'],'neutral-private-git')
        self.assertEqual(self.call('snapshot_list',chat_id=chat_id)['snapshots'][0]['git_checkpoint']['commit'],result['checkpoint']['commit'])
        self.assertEqual((self.root/'new.txt').read_text(),'approved content')
        self.assertTrue(self.call('health')['ok'])
