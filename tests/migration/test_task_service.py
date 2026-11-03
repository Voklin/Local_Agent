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
        has_result=False
        for message in payload['messages']:
            if message.get('role')!='tool':continue
            try:result=json.loads(message['content'])
            except (ValueError,TypeError):result=None  # Legacy/compacted text is valid context too.
            if not isinstance(result,dict) or result.get('code')!='NOT_EXECUTED':
                has_result=True;break
        if has_result:
            delta = {'content': 'Готово'}
        else:
            delta = {'tool_calls':[{'index':0, 'id':'call-1', 'type':'function', 'function':{
                'name':'write_file', 'arguments':json.dumps({'path':'new.txt','content':'approved content','overwrite':False})}}]}
            if getattr(self.server, 'multiple_tools', False):
                delta['tool_calls'][0]['index'] = 1
                delta['tool_calls'].insert(0, {'index': 0, 'id': 'read-first', 'type': 'function',
                    'function': {'name': 'read_file', 'arguments': '{"path":"source.txt"}'}})
        empty = getattr(self.server, 'empty_mode', '')
        if empty and (not empty.startswith('after-tool') or any(m.get('role') == 'tool' for m in payload['messages'])):
            delta = {'reasoning_content': 'private reasoning'}
            if empty in ('recover', 'after-tool-recover') and payload.get('tool_choice') == 'none':
                delta = {'content': 'Восстановленный ответ'}
        elif not any(t['function']['name']=='write_file' for t in payload.get('tools',[])) and not getattr(self.server, 'unexpected_tool', False):
            delta = {'content': 'Ответ без папки'}
        chunk = {'id':'test', 'object':'chat.completion.chunk', 'created':0, 'model':'test-model',
                 'choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if delta.get('tool_calls') else 'stop'}]}
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

    def test_voice_persona_uses_chat_scope_without_file_tools(self):
        self.service.companion_config={**self.service.companion_config,**self.service.config}
        self.service.start('',{'prompt':'Привет','mode':'voice'})
        self.event('task_end')
        request=self.server.requests[-1]
        self.assertEqual({tool['function']['name'] for tool in request['tools']},{'get_local_time','calculate','save_note','list_notes','set_timer','list_timers','cancel_timer','skills_list','skill_view','create_skill','read_tool_result','discover_tools'})
        self.assertEqual(self.service.chat['mode'],'voice')
        self.assertIn('Лола',request['messages'][0]['content'])
        self.assertEqual(self.service.chat['project_root'],'')
        self.assertFalse(self.service.engine.auto_memory)

    def test_source_context_approval_reject_and_changed_preview_send_no_http(self):
        """Treat the local fixture as external: approval blocks HTTP and changes invalidate consent."""
        from agent import context_builder
        for changed in (False,True):
            with self.subTest(changed=changed),patch.object(context_builder,'local_context_endpoint',return_value=False):
                self.server.requests.clear()
                source=Path(self.root)/'source.txt';source.write_text('before preview',encoding='utf-8')
                self.service.start(self.root,{'prompt':'Объясни source.txt','mode':'ide'})
                approval=self.event('approval')
                self.assertEqual(approval['kind'],'context')
                self.assertEqual(self.service.engine.state.phase,'waiting_approval')
                self.assertIn('before preview',json.loads(approval['diff'])['sources'][0]['content'])
                self.assertEqual(self.server.requests,[])
                if changed:source.write_text('changed after preview',encoding='utf-8')
                self.service.resolve_approval({'run_id':approval['run_id'],'approval_id':approval['approval_id'],'decision':'apply' if changed else 'reject'})
                while self.events.get(timeout=10)['event']!='task_end':pass
                self.assertEqual(self.server.requests,[])
                self.assertEqual(self.service.engine.task_snapshot()['run_state'],'paused')

    def test_source_context_confirmed_http_preserves_write_approval(self):
        """Approved source data reaches only the local fixture; write consent remains separate."""
        from agent import context_builder
        source=Path(self.root)/'source.txt';source.write_text('approved source bytes',encoding='utf-8')
        with patch.object(context_builder,'local_context_endpoint',return_value=False):
            self.service.start(self.root,{'prompt':'Объясни source.txt','mode':'ide'})
            approval=self.event('approval');self.assertEqual(approval['kind'],'context')
            self.service.resolve_approval({'run_id':approval['run_id'],'approval_id':approval['approval_id'],'decision':'apply'})
            write=self.event('approval');self.assertEqual(write['kind'],'write')
            self.assertIn('approved source bytes',json.dumps(self.server.requests))
            self.assertFalse((Path(self.root)/'new.txt').exists())
            self.service.cancel()
            while self.events.get(timeout=10)['event']!='task_end':pass
            self.assertEqual(self.service.engine.task_snapshot()['run_state'],'paused')
            with self.assertRaises(ValueError):self.service.resolve_approval({'run_id':approval['run_id'],'approval_id':approval['approval_id'],'decision':'apply'})

    def test_rename_preserves_messages_and_scope_and_active_title(self):
        chat=self.service.select_chat('')['chat']
        result=self.service.rename('',{'chat_id':chat['id'],'title':'Личный разговор'})
        self.assertTrue(result['ok'])
        self.assertEqual(self.service.chat['title'],'Личный разговор')
        self.assertEqual(chat_store.load_chat(chat['id'])['messages'],chat['messages'])
        with self.assertRaises(ValueError):self.service.rename(self.root,{'chat_id':chat['id'],'title':'Wrong scope'})
        for title in ('', 'x'*121, '\x00'):
            with self.assertRaises(ValueError):self.service.rename('',{'chat_id':chat['id'],'title':title})

    def test_rename_rejected_during_active_task(self):
        self.start()
        with self.assertRaises(ValueError):self.service.rename(self.root,{'chat_id':self.service.chat['id'],'title':'Busy'})

    def start(self):
        result = self.service.start(self.root, {'prompt':'hello'})
        approval = self.event('approval')
        self.assertEqual(result['run_id'], approval['run_id'])
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertIn('+approved content', approval['diff'])
        return approval

    def resolve(self, approval, decision):
        return self.service.resolve_approval({**approval, 'decision':decision})

    def test_draft_probe_uses_generation_without_saving_configuration(self):
        before = self.service.preferences()
        draft = {**self.service.config, 'model':'draft-model', 'api_key':'probe-secret',
                 'settings':{**self.service.config['settings'], 'temperature':0.7, 'top_p':0.9, 'max_tokens':2048}}
        result = queue.Queue()
        self.service.start_model_probe(draft, result.put)
        response = result.get(timeout=5)
        self.assertTrue(response['ok'], response)
        self.service.probe_thread.join(2)
        self.assertEqual(self.service.preferences(), before)
        self.assertNotIn('probe-secret', model_preferences.PREFERENCES_FILE.read_text())
        request = self.server.requests[-1]
        self.assertEqual(request['model'], 'draft-model')
        self.assertEqual(request['temperature'], 0.7)
        self.assertEqual(request['top_p'], 0.9)
        self.assertEqual(request['max_tokens'], 2048)
        self.assertNotIn('tools',request)
        self.assertEqual(len(request['messages']), 2)

    def test_saved_generation_is_used_by_engine(self):
        self.service.configure({**self.service.config, 'settings':{'budget_mode':'manual','temperature':0.65,'top_p':0.85,'max_tokens':1024,'request_timeout':12}})
        self.service.select_chat('')
        before = len(self.server.requests)
        self.service.start('', {'prompt':'hello'})
        self.event('task_end')
        self.service.thread.join(2)
        request = self.server.requests[before]
        self.assertEqual((request['temperature'],request['top_p'],request['max_tokens']), (0.65,0.85,1024))
        self.assertEqual(self.service.engine.settings['request_timeout'],12)
        restarted = TaskService(self.events.put)
        self.assertEqual(restarted.preferences()['settings'],self.service.preferences()['settings'])
        restarted.shutdown()

    def test_empty_after_tool_recovers_without_repeating_write(self):
        before = len(self.server.requests)
        with patch.object(self.server, 'empty_mode', 'after-tool-recover', create=True):
            approval = self.start()
            self.resolve(approval, 'apply')
            self.event('task_end')
            self.service.thread.join(2)
        saved = chat_store.load_chat(self.service.chat['id'])
        self.assertEqual(saved['messages'][-1]['content'], 'Восстановленный ответ')
        self.assertEqual(sum(m['role'] == 'tool' for m in saved['messages']), 1)
        self.assertEqual(sum(m['role'] == 'user' for m in saved['messages']), 1)
        requests = [r for r in self.server.requests[before:] if r.get('stream')]
        self.assertEqual(len(requests), 3)
        self.assertEqual(requests[-1]['tool_choice'], 'none')
        self.assertEqual(saved['task_checkpoint']['status'], 'completed')

    def test_permanently_empty_model_pauses_after_two_retries(self):
        before = len(self.server.requests)
        with patch.object(self.server, 'empty_mode', 'after-tool-permanent', create=True):
            approval = self.start()
            self.resolve(approval, 'apply')
            seen = []
            while True:
                event = self.events.get(timeout=10)
                seen.append(event)
                if event['event'] == 'task_end':
                    break
            self.service.thread.join(2)
        self.assertTrue(any(e['event'] == 'failed' and 'двух повторных' in e['text'] for e in seen))
        saved = chat_store.load_chat(self.service.chat['id'])
        self.assertEqual(saved['task_checkpoint']['status'], 'paused')
        self.assertEqual(sum(m['role'] == 'tool' for m in saved['messages']), 1)
        self.assertEqual(len([r for r in self.server.requests[before:] if r.get('stream')]), 4)
        self.assertEqual((self.root / 'new.txt').read_text(), 'approved content')

    def test_chat_without_project_has_only_extension_tools_and_separate_history(self):
        project_chat = self.service.select_chat(self.root)['chat']
        self.service.select_chat('')
        before = len(self.server.requests)
        self.service.start('', {'prompt': 'hello'})
        self.event('task_end')
        self.service.thread.join(2)
        request = self.server.requests[before]
        self.assertEqual({t['function']['name'] for t in request.get('tools',[])},{'skills_list','skill_view','create_skill','read_tool_result','discover_tools'})
        saved = chat_store.load_chat(self.service.chat['id'])
        self.assertEqual(saved['project_root'], '')
        self.assertEqual(saved['messages'][-1]['content'], 'Ответ без папки')
        self.assertNotIn(project_chat['id'], [c['id'] for c in self.service.chats('')['chats']])
        self.assertFalse((self.root / 'new.txt').exists())

    def test_task_end_allows_immediate_configuration_before_thread_returns(self):
        original_emit = self.service.emit
        errors = []
        observed = []
        def observe(event):
            if event['event'] == 'task_end':
                observed.append(self.service.thread.is_alive())
                try:
                    self.service.configure(dict(self.service.config))
                except Exception as exc:
                    errors.append(str(exc))
            original_emit(event)
        self.service.emit = observe
        self.service.select_chat('')
        self.service.start('', {'prompt': 'hello'})
        self.event('task_end')
        self.service.thread.join(2)
        self.assertEqual(observed, [True])
        self.assertEqual(errors, [])
        self.assertFalse(self.service.task_running)

    def test_chat_refuses_unsolicited_tool(self):
        self.service.select_chat('')
        with patch.object(self.server, 'unexpected_tool', True, create=True):
            self.service.start('', {'prompt': 'hello'})
            seen = []
            while True:
                event = self.events.get(timeout=10)
                seen.append(event)
                if event['event'] == 'task_end':
                    break
            self.service.thread.join(2)
        results=[json.loads(m['content']) for m in self.service.chat['messages'] if m.get('role')=='tool']
        self.assertTrue(results);self.assertTrue(all(not r['ok'] for r in results))
        self.assertFalse((self.root/'new.txt').exists())
        self.assertFalse(any(e['event'] == 'approval' for e in seen))
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'completed')

    def test_apply_only_after_matching_approval_and_persist_history(self):
        approval = self.start()
        pending = chat_store.load_chat(self.service.chat['id'])['task_checkpoint']
        self.assertEqual(pending['stage'], 'implementation')
        self.assertEqual(pending['tool_activity'][-1]['status'], 'awaiting_approval')
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
        self.assertEqual(saved['task_checkpoint']['tool_activity'][-1]['status'], 'succeeded')
        self.assertEqual(self.service.select_chat(self.root, saved['id'])['task']['tool_activity'], saved['task_checkpoint']['tool_activity'])
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

    def test_multiple_tools_keep_same_archive_anchor_for_write_recovery(self):
        (self.root / 'source.txt').write_text('source', encoding='utf-8')
        with patch.object(self.server, 'multiple_tools', True, create=True):
            approval = self.start()
            pending = json.loads(json.dumps(self.service.chat['task_checkpoint']))
            self.assertEqual(pending['pending_write']['message_index'], 1)
            self.assertEqual([entry['message_index'] for entry in pending['tool_activity']], [1, 1])
            self.resolve(approval, 'apply')
            self.event('task_end')
            self.service.thread.join(2)
        # Simulate a crash after both canonical results, before the final journal checkpoint.
        pending['pending_write']['status'] = 'applying'
        pending['tool_activity'][-1]['status'] = 'applying'
        self.service.chat['task_checkpoint'] = pending
        chat_store.save_chat(self.service.chat)
        recovered = self.service.select_chat(self.root, self.service.chat['id'])['task']
        self.assertEqual([entry['status'] for entry in recovered['tool_activity']], ['succeeded', 'succeeded'])
        self.assertEqual(recovered['modified_files'], ['new.txt'])
        self.assertNotIn('recovery_warning', recovered)

    def test_reject_does_not_write(self):
        approval = self.start()
        self.resolve(approval, 'reject')
        self.event('task_end')
        self.service.thread.join(2)
        self.assertFalse((self.root / 'new.txt').exists())
        self.assertEqual(task_store.load_task(self.service.chat['id'])['modified_files'], [])
        self.assertEqual(self.service.chat['task_checkpoint']['tool_activity'][-1]['status'], 'rejected')

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
        self.assertEqual(saved['task_checkpoint']['tool_activity'][-1]['status'], 'failed')
        self.assertEqual(task_store.load_task(saved['id'])['modified_files'], [])
        with self.assertRaises(ValueError):
            self.resolve(approval, 'apply')

    def test_checkpoint_survives_absent_legacy_task_file(self):
        approval = self.start()
        self.resolve(approval, 'apply')
        self.event('task_end')
        self.service.thread.join(2)
        saved = chat_store.load_chat(self.service.chat['id'])
        self.assertEqual(saved['task_checkpoint']['status'], 'completed')
        task_store.task_path(saved['id']).unlink(missing_ok=True)
        reopened = self.service.select_chat(self.root, saved['id'])
        self.assertEqual(reopened['task']['status'], 'completed')
        self.assertEqual(task_store.load_task(saved['id'])['status'], 'completed')
        self.assertEqual(reopened['chat']['messages'], saved['messages'])

    def test_recovery_does_not_confuse_reused_tool_ids_with_old_success(self):
        chat = self.service.select_chat(self.root)['chat']
        call = {'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'same-id','type':'function','function':{'name':'write_file','arguments':'{"path":"uncertain.txt","content":"x"}'}}]}
        chat['messages'] = [call, {'role': 'tool', 'tool_call_id': 'same-id', 'content': '{"ok":true}'},
                            {'role': 'user', 'content': 'new task'}, call]
        task = task_store.new_task(chat['id'], str(self.root), 'hello')
        task['pending_write'] = {'path': 'uncertain.txt', 'call_id': 'same-id', 'message_index': 3, 'status': 'applying'}
        chat['task_checkpoint'] = task
        (self.root / 'uncertain.txt').write_text('external or applied', encoding='utf-8')
        chat_store.save_chat(chat)
        recovered = self.service.select_chat(self.root, chat['id'])
        self.assertEqual(recovered['task']['status'], 'paused')
        self.assertEqual(recovered['task']['run_state'],'needs_attention')
        self.assertEqual(len(recovered['task']['recovery_items']),1)
        self.assertEqual(recovered['task']['modified_files'], [])
        self.assertEqual((self.root / 'uncertain.txt').read_text(), 'external or applied')
        self.assertNotIn('pending_write', recovered['task'])
        with self.assertRaises(ValueError):
            self.service.resolve_approval({'run_id': 'old', 'approval_id': 'old', 'decision': 'apply'})
        with self.assertRaises(ValueError):self.service.start(self.root, {'resume':True})
        self.service.resolve_tool_recovery({'chat_id':chat['id'],'journal_id':recovered['task']['journal_id'], 'message_index':3,'call_id':'same-id','resolution':'completed'})
        with patch.object(AgentEngine, 'run', side_effect=RuntimeError('stop after resume')):
            self.service.start(self.root, {'resume': True})
            self.service.thread.join(2)
        resumed = self.service.engine.task_snapshot()
        self.assertNotIn('recovery_warning', resumed)
        self.assertEqual(resumed['recovery_items'],[])

    def test_recovery_recognizes_saved_tool_result_before_task_checkpoint(self):
        chat = self.service.select_chat(self.root)['chat']
        chat['messages'] = [{'role': 'user', 'content': 'new task'},
                            {'role': 'assistant', 'tool_calls': [{'id': 'saved'}]},
                            {'role': 'tool', 'tool_call_id': 'saved', 'content': '{"ok":true}'}]
        task = task_store.new_task(chat['id'], str(self.root), 'hello')
        task['pending_write'] = {'path': 'done.txt', 'call_id': 'saved', 'message_index': 1, 'status': 'applying'}
        chat['task_checkpoint'] = task
        chat_store.save_chat(chat)
        recovered = self.service.select_chat(self.root, chat['id'])
        self.assertEqual(recovered['task']['modified_files'], ['done.txt'])
        self.assertNotIn('recovery_warning', recovered['task'])

    def test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately(self):
        chat = self.service.select_chat(self.root)['chat']
        chat['messages'] = [{'role': 'user', 'content': 'hello'}]
        chat['active_run_id'] = 'current-run'
        chat['stream_draft'] = {'run_id': 'current-run', 'turn': 0, 'text': 'saved partial'}
        chat['task_checkpoint'] = task_store.new_task(chat['id'], str(self.root), 'hello')
        chat_store.save_chat(chat)
        recovered = self.service.select_chat(self.root, chat['id'])
        self.assertEqual(recovered['chat']['messages'][-1]['content'], 'saved partial')
        self.assertEqual(recovered['task']['status'], 'paused')
        self.assertEqual(len(self.service.select_chat(self.root, chat['id'])['chat']['messages']), 2)
        chat = self.service.chat
        chat['stream_draft'] = {'run_id': 'old-run', 'turn': 0, 'text': 'unrelated draft'}
        chat_store.save_chat(chat)
        recovered = self.service.select_chat(self.root, chat['id'])
        self.assertEqual(len(recovered['chat']['messages']), 2)
        self.assertEqual(recovered['chat']['recovery_fragments'][-1]['text'], 'unrelated draft')

    def test_unexpected_engine_exception_still_persists_pause_and_task_end(self):
        with patch.object(AgentEngine, 'run', side_effect=RuntimeError('fixture failure')):
            self.service.start(self.root, {'prompt': 'hello'})
            self.service.thread.join(2)
        self.assertFalse(self.service.thread.is_alive())
        events = list(self.events.queue)
        self.assertTrue(any(e['event'] == 'failed' for e in events))
        self.assertTrue(any(e['event'] == 'task_end' for e in events))
        self.assertEqual(chat_store.load_chat(self.service.chat['id'])['task_checkpoint']['status'], 'paused')

    def test_legacy_index_is_not_used_during_agent_execution(self):
        with patch.object(chat_store, '_atomic_write', side_effect=AssertionError('Legacy JSON writes are forbidden')):
            approval = self.start()
            self.resolve(approval, 'apply')
            self.event('task_end')
            self.service.thread.join(2)
            saved = chat_store.load_chat(self.service.chat['id'])
            self.assertEqual(saved['task_checkpoint']['status'], 'completed')
            self.assertTrue(any(m.get('content') == 'Готово' for m in saved['messages']))
        self.assertEqual(len(self.service.chats(self.root)['chats']), 1)
        self.assertEqual(self.service.chats(self.root)['warnings'], [])

    def test_persistence_failure_before_apply_never_writes_and_still_ends_task(self):
        approval = self.start()
        with patch('core.python.task_execution.save_chat', side_effect=OSError('fixture storage failure')):
            self.resolve(approval, 'apply')
            self.service.thread.join(3)
            self.assertFalse(self.service.thread.is_alive())
        self.assertFalse((self.root / 'new.txt').exists())
        events = list(self.events.queue)
        self.assertTrue(any(e['event'] == 'failed' for e in events))
        self.assertTrue(any(e['event'] == 'task_end' for e in events))
        recovered = self.service.select_chat(self.root, self.service.chat['id'])
        self.assertEqual(recovered['task']['status'], 'paused')

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

    def test_busy_task_allows_selection_but_rejects_configuration_and_same_workspace_run(self):
        self.start()
        original=self.service.chat['id']
        self.assertNotEqual(self.service.select_chat(self.root)['chat']['id'],original)
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
