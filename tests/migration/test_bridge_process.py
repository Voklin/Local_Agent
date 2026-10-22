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
        self.process = subprocess.Popen([sys.executable, '-u', str(BRIDGE)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', env={**os.environ, 'LOCALAPPDATA': self.temp.name, 'PYTHONIOENCODING':'utf-8'})
        self.reader = threading.Thread(target=self.read_output, daemon=True)
        self.reader.start()

    def read_output(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except json.JSONDecodeError:
                self.messages.put({'invalid_output':line})

    def tearDown(self):
        self.process.stdin.close()
        try:
            self.process.wait(5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(5)
        self.reader.join(2)
        self.process.stdout.close()
        self.process.stderr.close()
        if self.discovery_server:
            self.discovery_server.release.set()
            self.discovery_server.shutdown()
            self.discovery_server.server_close()
        self.temp.cleanup()

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
