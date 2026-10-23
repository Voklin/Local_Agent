"""Verify the actual JSON-lines process, including cancellation during approval."""
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from test_task_service import ModelHandler
from test_model_discovery import DiscoveryHandler
from test_model_probe import ProbeHandler
from test_streaming import SlowHandler

BRIDGE = Path(__file__).resolve().parents[2] / 'core/python/bridge.py'


class BridgeProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.messages = queue.Queue()
        self.buffer = []
        self.counter = 0
        self.discovery_server = None
        self.scenario_server = None
        self.start_process()

    def start_process(self):
        frozen = os.environ.get('LCA_TEST_CORE')
        command = [str(Path(frozen).resolve(strict=True))] if frozen else [sys.executable, '-u', str(BRIDGE)]
        env = {**os.environ, 'LOCALAPPDATA': self.temp.name, 'PYTHONIOENCODING': 'utf-8'}
        if frozen:
            env['PATH'] = str(Path(os.environ['SystemRoot']) / 'System32')
            env.pop('PYTHONHOME', None)
            env.pop('PYTHONPATH', None)
        self.process = subprocess.Popen(command, cwd=self.root,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', env=env)
        self.reader = threading.Thread(target=self.read_output, daemon=True)
        self.reader.start()

    def read_output(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except json.JSONDecodeError:
                self.messages.put({'invalid_output':line})

    def stop_process(self, kill=False):
        if kill and self.process.poll() is None:
            self.process.kill()
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(5)
        self.reader.join(2)
        self.process.stdout.close()
        self.process.stderr.close()

    def tearDown(self):
        self.stop_process()
        if self.discovery_server:
            self.discovery_server.release.set()
            self.discovery_server.shutdown()
            self.discovery_server.server_close()
        if self.scenario_server:
            self.scenario_server.release.set()
            self.scenario_server.shutdown()
            self.scenario_server.server_close()
        self.temp.cleanup()

    def start_crash_scenario(self, handler, mode=None):
        server = self.scenario_server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        server.mode = mode
        server.requests = []
        server.waiting = threading.Event()
        server.disconnected = threading.Event()
        server.release = threading.Event()
        server.disconnect_timeout = 20
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.assertTrue(self.call('set_project', root=str(self.root))['ok'])
        self.assertTrue(self.call('configure_model', base_url=f'http://127.0.0.1:{server.server_port}/v1', model='test-model')['ok'])
        return self.call('start_task', prompt='hello')['chat_id']

    def reopen_after_kill(self, chat_id):
        self.stop_process(kill=True)
        self.messages = queue.Queue()
        self.buffer = []
        self.start_process()
        self.assertTrue(self.call('set_project', root=str(self.root))['ok'])
        result = self.call('load_chat', chat_id=chat_id)
        self.assertTrue(result['ok'], result)
        return result

    def test_project_search_requires_root_and_does_not_block_bridge(self):
        self.assertFalse(self.call('search_project',query='needle')['ok'])
        (self.root/'search.txt').write_text('first\nneedle here\n',encoding='utf-8')
        self.assertTrue(self.call('set_project',root=str(self.root))['ok'])
        result=self.call('search_project',query='needle')
        self.assertTrue(result['ok'],result)
        self.assertEqual(result['matches'][0]['line'],2)
        self.assertTrue(self.call('health')['ok'])
        self.assertTrue(self.call('cancel_project_search')['ok'])

    def test_process_kill_before_headers_recovers_user_request_and_paused_task(self):
        chat_id = self.start_crash_scenario(SlowHandler, 'before_headers')
        self.assertTrue(self.scenario_server.waiting.wait(10))
        recovered = self.reopen_after_kill(chat_id)
        self.assertEqual(recovered['task']['status'], 'paused')
        self.assertEqual(recovered['chat']['messages'], [{'role': 'user', 'content': 'hello'}])

    def test_approved_write_and_preferences_survive_process_restart(self):
        chat_id = self.start_crash_scenario(ModelHandler)
        proposal = self.until(lambda r: r.get('event') == 'approval')
        self.assertTrue(self.call('resolve_approval', run_id=proposal['run_id'], approval_id=proposal['approval_id'], decision='apply')['ok'])
        self.until(lambda r: r.get('event') == 'task_end')
        self.assertEqual((self.root / 'new.txt').read_text(encoding='utf-8'), 'approved content')
        self.assertTrue(self.call('configure_model', base_url=f'http://127.0.0.1:{self.scenario_server.server_port}/v1', model='test-model', api_key='packaging-test-secret')['ok'])
        recovered = self.reopen_after_kill(chat_id)
        self.assertEqual(recovered['task']['status'], 'completed')
        self.assertIn('new.txt', recovered['task']['modified_files'])
        self.assertEqual(self.call('get_model_settings')['model'], 'test-model')
        for file in Path(self.temp.name).rglob('*.json'):
            self.assertNotIn('packaging-test-secret', file.read_text(encoding='utf-8'))

    def test_process_kill_during_stream_recovers_partial_once(self):
        chat_id = self.start_crash_scenario(SlowHandler, 'crash_stream')
        expected = 'Начало потока '
        received = ''
        while received != expected:
            received += self.until(lambda r: r.get('event') == 'text_delta')['text']
            self.assertTrue(expected.startswith(received))
        # Wait for persistence, not an assumed scheduler/fsync duration. The
        # fixture sends no further tokens; the expected draft must reach disk before kill.
        archive = Path(self.temp.name) / 'LocalCodingAgent/chats' / (chat_id + '.json')
        deadline = time.monotonic() + 10
        while True:
            saved = json.loads(archive.read_text(encoding='utf-8'))
            if saved.get('stream_draft', {}).get('text') == expected:
                break
            self.assertLess(time.monotonic(), deadline, 'Periodic stream draft was not saved while the server was idle')
            time.sleep(0.05)
        recovered = self.reopen_after_kill(chat_id)
        self.assertEqual(recovered['task']['status'], 'paused')
        self.assertEqual([m['content'] for m in recovered['chat']['messages'] if m.get('role') == 'assistant'], ['Начало потока '])
        repeated = self.call('load_chat', chat_id=chat_id)
        self.assertEqual(repeated['chat']['messages'], recovered['chat']['messages'])

    def test_process_kill_during_approval_never_replays_permission(self):
        chat_id = self.start_crash_scenario(ModelHandler)
        proposal = self.until(lambda r: r.get('event') == 'approval')
        recovered = self.reopen_after_kill(chat_id)
        self.assertEqual(recovered['task']['status'], 'paused')
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertEqual(recovered['task']['tool_activity'][-1]['status'], 'interrupted')
        self.assertFalse(self.call('resolve_approval', run_id=proposal['run_id'], approval_id=proposal['approval_id'], decision='apply')['ok'])
        self.assertTrue(self.call('start_task', resume=True)['ok'])
        fresh = self.until(lambda r: r.get('event') == 'approval')
        self.assertNotEqual(fresh['run_id'], proposal['run_id'])
        self.assertNotEqual(fresh['approval_id'], proposal['approval_id'])
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertTrue(self.call('cancel_task')['ok'])
        self.until(lambda r: r.get('event') == 'task_end')

    def start_discovery_server(self, mode):
        server = self.discovery_server = ThreadingHTTPServer(('127.0.0.1', 0), DiscoveryHandler)
        server.mode = mode
        server.waiting = threading.Event()
        server.release = threading.Event()
        server.disconnected = threading.Event()
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.assertTrue(self.call('configure_model', base_url=f'http://127.0.0.1:{server.server_port}/v1', model='first')['ok'])
        self.counter += 1
        request_id = self.counter
        self.process.stdin.write(json.dumps({'id': request_id, 'method': 'list_models'}) + '\n')
        self.process.stdin.flush()
        self.assertTrue(server.waiting.wait(3))
        return request_id

    def test_bridge_models_discovery_keeps_commands_responsive_and_pins_config(self):
        request_id = self.start_discovery_server('hold')
        started = time.monotonic()
        self.assertTrue(self.call('health')['ok'])
        self.assertLess(time.monotonic() - started, 1)
        self.assertFalse(self.call('list_models')['ok'], 'A second discovery must not spawn another worker')
        self.assertTrue(self.call('configure_model', base_url='http://127.0.0.1:1/v1', model='second')['ok'])
        self.discovery_server.release.set()
        self.assertEqual(self.until(lambda item: item.get('id') == request_id)['models'], ['original-model'])

    def test_draft_probe_keeps_bridge_responsive_and_can_be_cancelled(self):
        server = self.scenario_server = ThreadingHTTPServer(('127.0.0.1',0), ProbeHandler)
        server.mode = 'stall'
        server.waiting = threading.Event()
        server.release = threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.counter += 1
        request_id = self.counter
        draft = {'base_url':f'http://127.0.0.1:{server.server_port}/v1','model':'draft-model'}
        self.process.stdin.write(json.dumps({'id':request_id,'method':'test_model','params':draft})+'\n')
        self.process.stdin.flush()
        self.assertTrue(server.waiting.wait(5))
        started = time.monotonic()
        self.assertTrue(self.call('health')['ok'])
        self.assertLess(time.monotonic()-started,1)
        self.assertTrue(self.call('cancel_model_setup')['ok'])
        response = self.until(lambda item:item.get('id')==request_id)
        self.assertFalse(response['ok'])
        self.assertIn('отменена',response['error'])
        self.assertEqual(self.call('get_model_settings')['model'],'')

    def test_bridge_cancel_closes_discovery_socket(self):
        request_id = self.start_discovery_server('stall')
        self.assertTrue(self.call('cancel_task')['ok'])
        result = self.until(lambda item: item.get('id') == request_id)
        self.assertFalse(result['ok'])
        self.assertIn('отменена', result['error'])
        self.assertTrue(self.discovery_server.disconnected.wait(2))

    def until(self, predicate):
        for i, item in enumerate(self.buffer):
            if predicate(item):
                return self.buffer.pop(i)
        while True:
            item = self.messages.get(timeout=10)
            self.assertNotIn('invalid_output', item)
            if predicate(item):
                return item
            self.buffer.append(item)

    def call(self, method, **params):
        self.counter += 1
        request_id = self.counter
        self.process.stdin.write(json.dumps({'id':request_id,'method':method,'params':params}) + '\n')
        self.process.stdin.flush()
        return self.until(lambda r: r.get('id') == request_id)

    def test_malformed_input_does_not_reuse_previous_request_id(self):
        self.assertTrue(self.call('health')['ok'])
        for raw in ('{invalid json}', '[]', '{"params":[]}'):
            self.process.stdin.write(raw + '\n')
            self.process.stdin.flush()
            result = self.until(lambda r: r.get('id') is None and 'ok' in r)
            self.assertFalse(result['ok'])
        self.assertTrue(self.call('health')['ok'])

    def test_bridge_remains_responsive_during_write_approval(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), ModelHandler)
        server.requests = []
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            self.assertTrue(self.call('set_project', root=str(self.root))['ok'])
            self.assertTrue(self.call('configure_model', base_url=f'http://127.0.0.1:{server.server_port}/v1', model='test-model')['ok'])
            result = self.call('start_task', prompt='hello')
            self.assertTrue(result['ok'])
            proposal = self.until(lambda r: r.get('event') == 'approval')
            self.assertIn('+approved content', proposal['diff'])
            self.assertTrue(self.call('health')['ok'])
            self.assertFalse(self.call('set_project', root=str(self.root))['ok'])
            self.assertFalse(self.call('write_file', path='bypass.txt', content='bad')['ok'])
            self.assertFalse((self.root / 'new.txt').exists())
            self.assertTrue(self.call('cancel_task')['ok'])
            self.until(lambda r: r.get('event') == 'task_end')
            self.assertFalse((self.root / 'new.txt').exists())
            self.assertFalse((self.root / 'bypass.txt').exists())
        finally:
            server.shutdown()
            server.server_close()
            thread.join(2)
