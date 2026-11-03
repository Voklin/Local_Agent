"""Real JSON-lines Core isolates IDE views and waits for authenticated editor receipts."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
import unittest
import test_bridge_process as fixture
from test_task_service import ModelHandler


class IdeScopeBridgeTests(unittest.TestCase):
    setUp=fixture.BridgeProcessTests.setUp
    tearDown=fixture.BridgeProcessTests.tearDown
    start_process=fixture.BridgeProcessTests.start_process
    stop_process=fixture.BridgeProcessTests.stop_process
    read_output=fixture.BridgeProcessTests.read_output
    until=fixture.BridgeProcessTests.until
    call=fixture.BridgeProcessTests.call

    def scoped(self,scope,operation,**params):
        self.counter+=1;identity=self.counter
        self.process.stdin.write(json.dumps({'id':identity,'method':'ide_call','params':{'session_id':scope,'method':operation,'params':params}})+'\n');self.process.stdin.flush()
        return self.until(lambda result:result.get('id')==identity)

    def test_ide_root_and_selection_do_not_mutate_desktop_or_other_view(self):
        other=self.root.parent/'other';other.mkdir();(other/'only.txt').write_text('other')
        self.call('set_project',root=str(self.root));main=self.call('new_chat',mode='chat')['chat']['id']
        scope=self.call('ide_attach',root=str(other))['session_id'];ide=self.scoped(scope,'new_chat',mode='ide')['chat']['id']
        self.assertNotEqual(main,ide);self.assertEqual(self.call('health')['project'],str(self.root))
        self.assertTrue(self.call('run_history',chat_id=main)['ok'])
        self.assertEqual([row['name'] for row in self.scoped(scope,'list_files')['items']],['only.txt'])
        self.assertFalse(self.scoped(scope,'load_chat',chat_id=main,mode='chat')['ok'])
        self.assertFalse(self.scoped(scope,'set_project',root=str(self.root))['ok'])
        self.assertFalse(self.scoped(scope,'ide_attach',root=str(self.root))['ok'])
        self.assertFalse(self.scoped(scope,'read_file',path='../project/nope')['ok'])
        self.assertEqual(self.call('health')['project'],str(self.root))

    def test_editor_prepare_apply_receipts_are_scoped_and_python_never_writes(self):
        server=self.scenario_server=ThreadingHTTPServer(('127.0.0.1',0),ModelHandler);server.requests=[];server.release=threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.call('configure_model',base_url=f'http://127.0.0.1:{server.server_port}/v1',model='test-model')
        scope=self.call('ide_attach',root=str(self.root))['session_id'];self.scoped(scope,'new_chat',mode='ide')
        started=self.scoped(scope,'start_task',mode='ide',prompt='write');self.assertTrue(started['ok'],started)
        prepared=self.until(lambda r:r.get('event')=='ide_editor' and r.get('phase')=='prepare')
        self.assertFalse(self.call('ide_editor_result',session_id='foreign',operation_id=prepared['operation_id'],result={'ok':True})['ok'])
        self.assertTrue(self.call('ide_editor_result',session_id=scope,operation_id=prepared['operation_id'],result={'ok':True,'editor_state':[]})['ok'])
        approval=self.until(lambda r:r.get('event')=='approval')
        self.assertTrue(self.scoped(scope,'resolve_approval',run_id=approval['run_id'],approval_id=approval['approval_id'],decision='apply')['ok'])
        apply=self.until(lambda r:r.get('event')=='ide_editor' and r.get('phase')=='apply')
        self.assertFalse((self.root/'new.txt').exists(),'Python wrote before editor acknowledgement')
        self.assertTrue(self.call('health')['ok'])
        (self.root/'new.txt').write_text(apply['args']['content'],encoding='utf8')
        self.assertTrue(self.call('ide_editor_result',session_id=scope,operation_id=apply['operation_id'],result={'ok':True,'path':'new.txt','editor':True})['ok'])
        self.until(lambda r:r.get('event')=='task_end')
        self.assertEqual((self.root/'new.txt').read_text(),'approved content')
        self.assertFalse(self.call('ide_editor_result',session_id=scope,operation_id=apply['operation_id'],result={'ok':True})['ok'])

    def test_closed_ide_cancels_only_its_run_before_file_effect(self):
        server=self.scenario_server=ThreadingHTTPServer(('127.0.0.1',0),ModelHandler);server.requests=[];server.release=threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.call('configure_model',base_url=f'http://127.0.0.1:{server.server_port}/v1',model='test-model')
        scope=self.call('ide_attach',root=str(self.root))['session_id'];self.scoped(scope,'new_chat',mode='ide')
        self.assertTrue(self.scoped(scope,'start_task',mode='ide',prompt='write')['ok'])
        self.until(lambda r:r.get('event')=='ide_editor')
        self.assertTrue(self.call('ide_detach',session_id=scope)['ok']);self.until(lambda r:r.get('event')=='task_end')
        self.assertFalse((self.root/'new.txt').exists());self.assertTrue(self.call('health')['ok'])
