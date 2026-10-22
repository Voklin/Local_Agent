"""Network discovery regressions: bounded bodies, deadlines and socket cancellation."""
import json
import queue
import threading
import time
import unittest
import httpx
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent.model_discovery import discover_models


class DiscoveryHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        mode = self.server.mode
        if mode == 'hold':
            self.server.waiting.set()
            self.server.release.wait(4)
        self.send_response(500 if mode == 'http_error' else 200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.server.waiting.set()
        try:
            if mode == 'stall':
                self.wfile.write(b'{"data":[')
                self.wfile.flush()
                self.connection.settimeout(3)
                if self.connection.recv(1) == b'':
                    self.server.disconnected.set()
                return
            if mode == 'trickle':
                for _ in range(30):
                    self.wfile.write(b' ')
                    self.wfile.flush()
                    time.sleep(0.05)
                return
            payload = {'data': [{'id': 'original-model'}, {'id': None}, {'id': ''}]}
            if mode == 'bad_shape':
                payload = {'data': {}}
            if mode == 'huge':
                payload = {'data': [{'id': 'x' * 10000}]}
            raw = b'not json' if mode == 'bad_json' else json.dumps(payload).encode()
            self.wfile.write(raw)
        except OSError:
            self.server.disconnected.set()


class ModelDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), DiscoveryHandler)
        self.server.mode = 'normal'
        self.server.waiting = threading.Event()
        self.server.release = threading.Event()
        self.server.disconnected = threading.Event()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.config = {'base_url': f'http://127.0.0.1:{self.server.server_port}/v1', 'api_key': ''}

    def tearDown(self):
        self.server.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)

    def test_valid_discovery_filters_invalid_ids(self):
        self.assertEqual(discover_models(self.config), {'ok': True, 'models': ['original-model']})

    def test_invalid_json_shape_status_and_size_are_rejected(self):
        for mode in ('bad_shape', 'bad_json', 'http_error', 'huge'):
            with self.subTest(mode=mode):
                self.server.mode = mode
                with self.assertRaises(httpx.HTTPStatusError if mode == 'http_error' else ValueError):
                    discover_models(self.config, max_bytes=1000)

    def test_total_deadline_stops_slow_trickle(self):
        self.server.mode = 'trickle'
        started = time.monotonic()
        with self.assertRaisesRegex(ValueError, 'истекло'):
            discover_models(self.config, timeout=0.5)
        self.assertLess(time.monotonic() - started, 2)
        self.assertTrue(self.server.disconnected.wait(2))

    def test_cancellation_closes_stalled_socket(self):
        self.server.mode = 'stall'
        cancelled = threading.Event()
        results = queue.Queue()
        def run():
            try:
                results.put(discover_models(self.config, cancelled=cancelled))
            except Exception as exc:
                results.put(exc)
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(self.server.waiting.wait(3))
        cancelled.set()
        result = results.get(timeout=2)
        thread.join(2)
        self.assertIsInstance(result, ValueError)
        self.assertIn('отменена', str(result))
        self.assertTrue(self.server.disconnected.wait(2))
