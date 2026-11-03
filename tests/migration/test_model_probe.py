"""Bounded real HTTP checks for the model-settings diagnostic request."""
import json
import threading
import unittest
import httpx
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent.model_preferences import validate_preferences
from agent.model_probe import probe_model


class ProbeHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_POST(self):
        self.server.payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.server.mode == 'stall':
            self.server.waiting.set()
            self.server.release.wait(10)
            return
        self.send_response(401 if self.server.mode == 'unauthorized' else 200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        raw = {'choices':[{'message':{'content':'' if self.server.mode == 'empty' else 'Готово'}}]}
        if self.server.mode == 'invalid':
            raw = {'unexpected': 'shape'}
        data = json.dumps(raw).encode()
        if self.server.mode == 'large':
            data = b'x' * 200_000
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass


class ModelProbeTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), ProbeHandler)
        self.server.mode = 'ok'
        self.server.waiting = threading.Event()
        self.server.release = threading.Event()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.config = {**validate_preferences({'base_url':f'http://127.0.0.1:{self.server.server_port}/v1', 'model':'probe'}), 'api_key':''}

    def tearDown(self):
        self.server.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)

    def test_probe_requires_real_text_and_bounds_bad_responses(self):
        result = probe_model(self.config)
        self.assertEqual(result['text'], 'Готово')
        self.assertNotIn('tools', self.server.payload)
        for mode in ('empty','invalid','large','unauthorized'):
            with self.subTest(mode=mode):
                self.server.mode = mode
                with self.assertRaises((ValueError, httpx.HTTPStatusError)):
                    probe_model(self.config)

    def test_probe_deadline_and_cancellation_are_bounded(self):
        self.server.mode = 'stall'
        with self.assertRaisesRegex(ValueError, 'Проверка не завершилась'):
            probe_model(self.config, timeout=0.15)
        cancelled = threading.Event()
        cancelled.set()
        with self.assertRaisesRegex(ValueError, 'отменена'):
            probe_model(self.config, cancelled=cancelled)
