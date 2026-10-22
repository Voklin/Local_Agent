"""Exercise the real agent loop against a local OpenAI-compatible test server."""
import json
import queue
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from core.python.task_service import TaskService
from agent.engine import AgentEngine
from agent import chat_store, project_memory, task_store, model_preferences


class ModelHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"data":[{"id":"test-model"}]}')

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(payload)
        self.send_response(200)
        if not payload.get('stream'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'id':'test', 'object':'chat.completion', 'created':0, 'model':'test-model',
                'choices':[{'index':0,'message':{'role':'assistant','content':'{}'},'finish_reason':'stop'}]}).encode())
            return
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        # A single write proposal, then a normal answer after the tool result.
        if any(m.get('role') == 'tool' for m in payload['messages']):
            delta = {'content': 'Готово'}
        else:
            delta = {'tool_calls':[{'index':0, 'id':'call-1', 'type':'function', 'function':{
                'name':'write_file', 'arguments':json.dumps({'path':'new.txt','content':'approved content','overwrite':False})}}]}
        chunk = {'id':'test', 'object':'chat.completion.chunk', 'created':0, 'model':'test-model',
                 'choices':[{'index':0,'delta':delta,'finish_reason':None}]}
        self.wfile.write(('data: ' + json.dumps(chunk) + '\n\ndata: [DONE]\n\n').encode())
        self.wfile.flush()


class TaskServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), ModelHandler)
        cls.server.requests = []
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join(2)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        store = Path(self.temp.name) / 'data'
        self.patches = [patch.object(chat_store, 'CHAT_DIR', store / 'chats'),
            patch.object(chat_store, 'INDEX_FILE', store / 'chats/index.json'),
            patch.object(task_store, 'TASK_DIR', store / 'tasks'),
            patch.object(project_memory, 'MEMORY_DIR', store / 'memory'),
            patch.object(model_preferences, 'PREFERENCES_FILE', store / 'model-preferences.json')]
        for p in self.patches:
            p.start()
        self.events = queue.Queue()
        self.service = TaskService(self.events.put)
        self.service.configure({'base_url': f'http://127.0.0.1:{self.server.server_port}/v1', 'model':'test-model'})

    def tearDown(self):
        self.service.shutdown()
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def event(self, name):
        while True:
            event = self.events.get(timeout=10)
            if event['event'] == 'failed':
                self.fail(event['text'])
            if event['event'] == name:
                return event

    def start(self):
        result = self.service.start(self.root, {'prompt':'hello'})
        approval = self.event('approval')
        self.assertEqual(result['run_id'], approval['run_id'])
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertIn('+approved content', approval['diff'])
        return approval

    def resolve(self, approval, decision):
        return self.service.resolve_approval({**approval, 'decision':decision})

    def test_apply_only_after_matching_approval_and_persist_history(self):
        approval = self.start()
        with self.assertRaises(ValueError):
            self.service.resolve_approval({**approval, 'approval_id':'stale', 'decision':'apply'})
        with self.assertRaises(ValueError):
            self.service.resolve_approval({**approval, 'run_id':'stale', 'decision':'apply'})
        self.assertFalse((self.root / 'new.txt').exists())
        self.resolve(approval, 'apply')
        self.event('task_end')
        self.service.thread.join(2)
        self.assertEqual((self.root / 'new.txt').read_text(), 'approved content')
        saved = chat_store.load_chat(self.service.chat['id'])
        self.assertTrue(any(m.get('role') == 'tool' for m in saved['messages']))
        self.assertEqual(task_store.load_task(saved['id'])['status'], 'completed')
        self.assertEqual(task_store.load_task(saved['id'])['modified_files'], ['new.txt'])
        self.assertEqual(self.service.select_chat(self.root, saved['id'])['chat']['messages'], saved['messages'])

    def test_long_archive_survives_model_compaction_and_service_restart(self):
        chat = self.service.select_chat(self.root)['chat']
        history = []
        for i in range(20):
            history.extend([{'role': 'user', 'content': f'old-{i}'},
                            {'role': 'assistant', 'content': 'answer-' + str(i) + 'x' * 5000}])
        history.extend([
            {'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'old-tool', 'type': 'function',
                'function': {'name': 'read_file', 'arguments': '{"path":"example.txt"}'}}]},
            {'role': 'tool', 'tool_call_id': 'old-tool', 'content': 'full output ' + 'x' * 30000}])
        chat['messages'] = history
        chat_store.save_chat(chat)
        before = len(self.server.requests)
        self.service.start(self.root, {'prompt': 'hello followup'})
        self.event('task_end')
        self.service.thread.join(2)
        saved = chat_store.load_chat(chat['id'])
        self.assertEqual(saved['messages'][:len(history)], history)
        self.assertEqual(saved['messages'][len(history)], {'role': 'user', 'content': 'hello followup'})
        request = next(r for r in self.server.requests[before:] if r.get('stream'))
        self.assertLess(len(request['messages']), len(saved['messages']))
        self.assertLessEqual(len(json.dumps(request['messages'], ensure_ascii=False)), 80000)
        self.service.shutdown()
        self.service = TaskService(self.events.put)
        reopened = self.service.select_chat(self.root, chat['id'])['chat']
        self.assertEqual(reopened['messages'], saved['messages'])

    def test_forced_tool_uses_single_definition_then_restores_auto(self):
        before = len(self.server.requests)
        self.service.engine_factory = lambda **kwargs: AgentEngine(force_tool='write_file', **kwargs)
        approval = self.start()
        self.resolve(approval, 'apply')
        self.event('task_end')
        self.service.thread.join(2)
        requests = [r for r in self.server.requests[before:] if r.get('stream')]
        self.assertEqual(requests[0]['tool_choice'], 'required')
        self.assertEqual([t['function']['name'] for t in requests[0]['tools']], ['write_file'])
        self.assertEqual(requests[1]['tool_choice'], 'auto')
        self.assertGreater(len(requests[1]['tools']), 1)

    def test_reject_does_not_write(self):
        approval = self.start()
        self.resolve(approval, 'reject')
        self.event('task_end')
        self.service.thread.join(2)
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertEqual(task_store.load_task(self.service.chat['id'])['modified_files'], [])

    def test_matching_approval_refuses_new_external_file(self):
        approval = self.start()
        (self.root / 'new.txt').write_text('external edit', encoding='utf-8')
        self.resolve(approval, 'apply')
        self.event('task_end')
        self.service.thread.join(2)
        self.assertEqual((self.root / 'new.txt').read_text(), 'external edit')
        saved = chat_store.load_chat(self.service.chat['id'])
        results = [json.loads(m['content']) for m in saved['messages'] if m.get('role') == 'tool']
        self.assertEqual(results[-1]['code'], 'FILE_CHANGED')
        self.assertEqual(task_store.load_task(saved['id'])['modified_files'], [])
        with self.assertRaises(ValueError):
            self.resolve(approval, 'apply')

    def test_resume_preserves_task_and_recovery_marks_interrupted_task_paused(self):
        self.start()
        self.service.cancel()
        self.event('task_end')
        self.service.thread.join(2)
        task = task_store.load_task(self.service.chat['id'])
        task['status'] = 'running'  # Simulate process loss before the final checkpoint.
        task_store.save_task(task)
        recovered = self.service.select_chat(self.root, self.service.chat['id'])
        self.assertEqual(recovered['task']['status'], 'paused')
        self.service.start(self.root, {'resume': True})
        self.event('task_end')
        self.service.thread.join(2)
        resumed = task_store.load_task(self.service.chat['id'])
        self.assertEqual(resumed['resume_state']['attempt'], 1)
        self.assertEqual(resumed['status'], 'completed')

    def test_new_prompt_after_pause_creates_new_task(self):
        self.start()
        self.service.cancel()
        self.event('task_end')
        self.service.thread.join(2)
        self.service.start(self.root, {'prompt':'new request'})
        self.event('task_end')
        self.service.thread.join(2)
        task = task_store.load_task(self.service.chat['id'])
        self.assertEqual(task['prompt'], 'new request')
        self.assertEqual(task['resume_state']['attempt'], 0)

    def test_cancel_while_waiting_pauses_task_and_unblocks_worker(self):
        self.start()
        self.service.cancel()
        self.event('task_end')
        self.service.thread.join(2)
        self.assertFalse(self.service.thread.is_alive())
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertEqual(task_store.load_task(self.service.chat['id'])['status'], 'paused')

    def test_busy_task_rejects_chat_and_configuration_changes(self):
        self.start()
        with self.assertRaises(ValueError):
            self.service.select_chat(self.root)
        with self.assertRaises(ValueError):
            self.service.configure({'base_url':'http://127.0.0.1/v1'})
        with self.assertRaises(ValueError):
            self.service.start(self.root, {'prompt':'another'})

    def test_chats_are_scoped_to_project_and_ids_cannot_escape_store(self):
        chat = self.service.select_chat(self.root)['chat']
        with self.assertRaises(ValueError):
            self.service.select_chat(self.root, '../outside')
        with self.assertRaises(ValueError):
            self.service.select_chat(self.root / 'other', chat['id'])
        self.assertEqual(self.service.chats(self.root / 'other')['chats'], [])

    def test_models_and_configuration_do_not_return_key(self):
        result = self.service.configure({'base_url': f'http://127.0.0.1:{self.server.server_port}/v1', 'model':'test-model', 'api_key':'test-secret'})
        self.assertNotIn('api_key', result)
        self.assertEqual(self.service.models()['models'], ['test-model'])

    def test_missing_model_and_bad_url_are_rejected(self):
        for url in ('file:///tmp', 'http://user:password@localhost/v1', 'https://localhost/v1?key=secret'):
            with self.assertRaises(ValueError):
                self.service.configure({'base_url': url})
        self.service.config['model'] = ''
        with self.assertRaises(ValueError):
            self.service.start(self.root, {'prompt':'hello'})
