"""Real sockets verify cancellation before headers, during SSE and during memory calls."""
import json
import queue
import socket
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from agent.engine import AgentEngine
from agent import task_store, model_preferences, chat_store, project_memory
from core.python.task_service import TaskService


class SlowHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def chunk(self, text):
        data = {'id':'slow','object':'chat.completion.chunk','created':0,'model':'test-model',
                'choices':[{'index':0,'delta':{'content':text},'finish_reason':None}]}
        self.wfile.write(('data: ' + json.dumps(data) + '\n\n').encode())
        self.wfile.flush()

    def wait_for_disconnect(self):
        self.server.waiting.set()
        self.connection.settimeout(5)
        try:
            if self.connection.recv(1) == b'':
                self.server.disconnected.set()
        except (ConnectionResetError, ConnectionAbortedError):
            self.server.disconnected.set()
        except socket.timeout:
            pass

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if not data.get('stream') and self.server.mode != 'memory':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'id':'memory','object':'chat.completion','created':0,'model':'test-model',
                'choices':[{'index':0,'message':{'role':'assistant','content':'{}'},'finish_reason':'stop'}]}).encode())
            return
        if self.server.mode == 'before_headers' or not data.get('stream'):
            self.wait_for_disconnect()
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        self.chunk('Начало ')
        if self.server.mode == 'batch':
            self.chunk('потока ')
        if self.server.mode == 'mid_stream':
            self.wait_for_disconnect()
            return
        if self.server.mode in ('normal', 'batch'):
            self.server.release.wait(5)
        self.chunk('ответа')
        self.wfile.write(b'data: [DONE]\n\n')
        self.wfile.flush()


class StreamingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patches = [patch.object(task_store, 'TASK_DIR', self.root / 'tasks'),
                        patch.object(model_preferences, 'PREFERENCES_FILE', self.root / 'model.json'),
                        patch.object(chat_store, 'CHAT_DIR', self.root / 'chats'),
                        patch.object(chat_store, 'INDEX_FILE', self.root / 'chats/index.json'),
                        patch.object(project_memory, 'MEMORY_DIR', self.root / 'memory')]
        for item in self.patches:
            item.start()
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), SlowHandler)
        self.server.mode = 'normal'
        self.server.waiting = threading.Event()
        self.server.disconnected = threading.Event()
        self.server.release = threading.Event()
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        self.engine = None
        self.thread = None
        self.deltas = queue.Queue()
        self.messages = []
        self.failures = []

    def tearDown(self):
        if self.engine:
            self.engine.requestInterruption()
        self.server.release.set()
        if self.thread:
            self.thread.join(5)
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join(2)
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def start(self, mode, auto_memory=False):
        self.server.mode = mode
        self.engine = AgentEngine(f'http://127.0.0.1:{self.server.server_port}/v1', '', 'test-model',
            str(self.root), 'hello', task_id='stream-test', auto_memory=auto_memory)
        self.engine.text_delta.connect(lambda turn, text: self.deltas.put((turn, text)))
        self.engine.conversation_updated.connect(lambda messages: self.messages.extend(messages))
        self.engine.failed.connect(self.failures.append)
        self.thread = threading.Thread(target=self.engine.run, daemon=True)
        self.thread.start()

    def stop_and_assert(self):
        started = time.monotonic()
        self.engine.requestInterruption()
        self.thread.join(3)
        self.assertFalse(self.thread.is_alive(), 'Cancellation should not wait for the 180-second network timeout')
        self.assertLess(time.monotonic() - started, 3)
        self.assertTrue(self.server.disconnected.wait(2), 'Cancellation should close the actual HTTP connection')
        self.assertEqual(self.failures, [])
        self.assertEqual(task_store.load_task('stream-test')['status'], 'paused')

    def test_cancel_before_server_returns_headers(self):
        self.start('before_headers')
        self.assertTrue(self.server.waiting.wait(5))
        self.stop_and_assert()

    def test_cancel_during_stalled_sse_preserves_displayed_text(self):
        self.start('mid_stream')
        self.assertEqual(self.deltas.get(timeout=5), (0, 'Начало '))
        self.assertTrue(self.server.waiting.wait(5))
        self.stop_and_assert()
        self.assertTrue(any(m.get('role') == 'assistant' and m.get('content') == 'Начало' for m in self.messages))

    def test_text_arrives_before_response_finishes(self):
        self.start('normal')
        self.assertEqual(self.deltas.get(timeout=5), (0, 'Начало '))
        self.assertTrue(self.thread.is_alive())
        self.server.release.set()
        self.thread.join(5)
        self.assertFalse(self.thread.is_alive())
        self.assertEqual(self.failures, [])
        self.assertEqual(self.deltas.get(timeout=1), (0, 'ответа'))
        self.assertEqual([m['content'] for m in self.messages if m.get('role') == 'assistant'], ['Начало ответа'])
        self.assertEqual(task_store.load_task('stream-test')['status'], 'completed')

    def test_cancel_memory_request_does_not_mark_task_completed(self):
        self.start('memory', auto_memory=True)
        self.assertTrue(self.server.waiting.wait(5))
        self.stop_and_assert()

    def test_preferences_reload_does_not_restore_api_key(self):
        service = TaskService(lambda _: None)
        saved = service.configure({'base_url':'http://localhost:1234/v1','model':'Qwen','api_key':'temporary-secret'})
        restarted = TaskService(lambda _: None)
        self.assertEqual(restarted.preferences(), saved)
        self.assertEqual(restarted.config['api_key'], '')
        self.assertNotIn('temporary-secret', (self.root / 'model.json').read_text())

    def test_service_flushes_buffer_during_pause_and_final_uses_same_message_id(self):
        self.server.mode = 'batch'
        events = queue.Queue()
        service = TaskService(events.put)
        service.configure({'base_url':f'http://127.0.0.1:{self.server.server_port}/v1','model':'test-model'})
        service.start(self.root, {'prompt':'hello'})
        chunks = []
        try:
            while ''.join(e['text'] for e in chunks) != 'Начало потока ':
                event = events.get(timeout=2)
                self.assertNotEqual(event['event'], 'failed', event)
                if event['event'] == 'text_delta':
                    chunks.append(event)
            self.assertTrue(service.thread.is_alive())
            self.server.release.set()
            final = None
            while True:
                event = events.get(timeout=5)
                self.assertNotEqual(event['event'], 'failed', event)
                if event['event'] == 'chat' and event['role'] == 'assistant':
                    final = event
                if event['event'] == 'task_end':
                    break
            self.assertEqual(final['text'], 'Начало потока ответа')
            self.assertTrue(all(e['message_id'] == final['message_id'] for e in chunks))
        finally:
            service.shutdown()
