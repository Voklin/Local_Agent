"""Verify the actual JSON-lines process, including cancellation during approval."""
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from test_task_service import ModelHandler

BRIDGE = Path(__file__).resolve().parents[2] / 'core/python/bridge.py'


class BridgeProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.messages = queue.Queue()
        self.buffer = []
        self.counter = 0
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
        self.temp.cleanup()

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
