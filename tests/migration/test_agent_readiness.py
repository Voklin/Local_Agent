"""Agent readiness: actual HTTP, executor, approvals, disk edits and subprocess tests.

The provider is deterministic; this suite validates orchestration, not LLM quality.
Every case owns a disposable workspace and profile.
"""
import json
import sys
import unittest
from http.server import BaseHTTPRequestHandler

from tests.migration import test_run_control as run_fixture


class ReadinessHandler(BaseHTTPRequestHandler):
    """Serve scripted decisions over the real OpenAI-compatible HTTP boundary."""

    def log_message(self, *_args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"data":[{"id":"fixture"}]}')

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(payload)
        self.send_response(200)
        if not payload.get('stream'):
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'choices': [{'message': {
                'content': '{"complete":true,"reason":"fixture advisory"}'},
                'finish_reason': 'stop'}]}).encode())
            return
        index = self.server.step
        self.server.step += 1
        action = self.server.decide(index, payload)
        if isinstance(action, tuple):
            name, arguments = action
            if self.server.protocol == 'json':
                delta = {'content': json.dumps({'protocol': 'neutral.action.v1',
                    'kind': 'tool', 'name': name, 'arguments': arguments})}
                finish = 'stop'
            else:
                delta = {'tool_calls': [{'index': 0, 'id': f'readiness-{index}',
                    'type': 'function', 'function': {'name': name,
                    'arguments': json.dumps(arguments)}}]}
                finish = 'tool_calls'
        else:
            delta = {'content': json.dumps({'protocol': 'neutral.action.v1',
                'kind': 'final', 'text': action}) if self.server.protocol == 'json' else action}
            finish = 'stop'
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        chunk = {'id': 'readiness', 'choices': [{'index': 0, 'delta': delta,
            'finish_reason': finish}]}
        self.wfile.write(('data: ' + json.dumps(chunk) + '\n\ndata: [DONE]\n\n').encode())
        self.wfile.flush()


class AgentReadinessTests(unittest.TestCase):
    """Repeatable vertical workflows with explicit expected disk and task outcomes."""
    setUp = run_fixture.RunControlHttpTests.setUp
    stop_server = run_fixture.RunControlHttpTests.stop_server

    def start(self, actions, *, options=None, protocol='native', history=None):
        self.server.RequestHandlerClass = ReadinessHandler
        self.server.protocol = protocol
        self.server.step = 0
        self.server.decide = actions if callable(actions) else lambda index, _payload: actions[min(index, len(actions)-1)]
        self.service.config['tool_protocol'] = protocol
        self.service.extensions.state['groups']['commands'] = True
        if history:
            self.service.select_chat(self.root, mode='ide')
            self.service.chat['messages'] = history
        return self.service.start(self.root, {'mode': 'ide',
            'prompt': 'Inspect the project, fix the requested behavior and verify the result.',
            'task_options': options or {}})

    def finish(self, decision='apply'):
        """Use the public approval API and retain evidence from real task events."""
        events = []
        while True:
            event = self.events.get(timeout=20)
            events.append(event)
            self.assertNotEqual(event['event'], 'failed', event)
            if event['event'] == 'approval':
                self.assertEqual(self.service.engine.state.phase, 'waiting_approval')
                self.assertFalse(self.service.scheduler.status()['busy'])
                self.service.resolve_approval({**event, 'decision': decision})
            if event['event'] == 'task_end':
                break
        self.service.thread.join(2)
        self.assertFalse(self.service.task_running)
        self.assertFalse(self.service.scheduler.status()['busy'])
        return events

    def check(self):
        """Run the fixture's assertions in a real interpreter, without cache writes."""
        return {'id': 'behavior', 'purpose': 'Verify fixture behavior',
            'program': sys.executable, 'arguments': ['-B', 'verify.py'],
            'cwd': '.', 'timeout': 10}

    def fixture(self):
        (self.root/'calc.py').write_text('def total():\n    return 1\n', encoding='utf-8')
        (self.root/'verify.py').write_text('from calc import total\nassert total() == 3, total()\nprint("behavior passed")\n', encoding='utf-8')

    def receipts(self):
        return [json.loads(m['content']) for m in self.service.chat['messages'] if m['role']=='tool']

    def test_a_exploration_returns_current_source_references(self):
        self.fixture()
        self.start([('read_range', {'path':'calc.py', 'start_line':1, 'end_line':2}),
            'calc.py:1 defines total; verify.py checks its result.'], options={'read_only':True})
        self.finish()
        self.assertIn('return 1', self.receipts()[0]['content'])
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'completed')
        self.assertIn('calc.py:1', self.service.chat['messages'][-1]['content'])

    def test_b_simple_edit_and_real_test(self):
        self.fixture()
        self.start([('read_range', {'path':'calc.py', 'start_line':1, 'end_line':2}),
            ('patch_file', {'path':'calc.py','old_text':'return 1','new_text':'return 3'}),
            ('run_project_command', {k:v for k,v in self.check().items() if k!='id'}), 'Changed calc.py:2; behavior passed.'])
        events = self.finish()
        self.assertEqual([e['kind'] for e in events if e['event']=='approval'], ['patch','command'])
        self.assertIn('return 3', (self.root/'calc.py').read_text())
        self.assertEqual(self.service.chat['task_checkpoint']['verification']['status'], 'commands_passed')

    def test_c_multi_file_json_edit_and_test(self):
        self.fixture()
        self.start([('patch_file', {'path':'calc.py','old_text':'total','new_text':'answer'}),
            ('patch_file', {'path':'verify.py','old_text':'from calc import total','new_text':'from calc import answer as total'}),
            ('patch_file', {'path':'calc.py','old_text':'return 1','new_text':'return 3'}),
            ('run_project_command', {k:v for k,v in self.check().items() if k!='id'}), 'Renamed both references and verified behavior.'], protocol='json')
        self.finish()
        self.assertIn('def answer', (self.root/'calc.py').read_text())
        self.assertIn('answer as total', (self.root/'verify.py').read_text())
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'completed')
        self.assertEqual(len([r for r in self.receipts() if r.get('operation')=='patch_file']), 3)

    def test_d_failed_auto_check_returns_to_model_and_recovers(self):
        self.fixture()
        self.start([('patch_file', {'path':'calc.py','old_text':'return 1','new_text':'return 2'}),
            'The edit is ready.',
            ('patch_file', {'path':'calc.py','old_text':'return 2','new_text':'return 3'}),
            'Corrected calc.py:2; verification now passes.'],
            options={'auto_checks':True, 'checks':[self.check()]})
        self.finish()
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'completed')
        self.assertIn('return 3', (self.root/'calc.py').read_text())
        commands = [r for r in self.receipts() if 'exit_code' in r]
        self.assertEqual([r['exit_code'] for r in commands], [1,0])
        self.assertTrue(any('AssertionError' in json.dumps(r['messages']) for r in self.server.requests[2:]))

    def test_d_auto_checks_run_even_without_file_edits(self):
        self.fixture()
        (self.root/'calc.py').write_text('def total():\n    return 3\n')
        self.start(['Existing behavior is correct.'], options={'auto_checks':True, 'checks':[self.check()]})
        self.finish()
        self.assertEqual(self.service.chat['task_checkpoint']['verification']['status'], 'commands_passed')
        self.assertEqual(len([r for r in self.receipts() if 'exit_code' in r]), 1)

    def test_g_denied_auto_check_is_not_automatically_replayed(self):
        self.fixture()
        self.start(['Verification requested.'], options={'auto_checks':True, 'checks':[self.check()]})
        events = self.finish('reject')
        self.assertEqual(len([e for e in events if e['event']=='approval']), 1)
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'paused')
        self.assertFalse(any(r.get('exit_code')==0 for r in self.receipts()))

    def test_g_rejected_edit_is_returned_to_model(self):
        self.fixture()
        self.start([('patch_file', {'path':'calc.py','old_text':'return 1','new_text':'return 3'}),
            'The user rejected the edit; calc.py is unchanged.'])
        events = self.finish('reject')
        self.assertEqual(len([e for e in events if e['event']=='approval']), 1)
        self.assertEqual(self.receipts()[0]['code'], 'USER_DENIED')
        self.assertIn('return 1', (self.root/'calc.py').read_text())
        self.assertIn('USER_DENIED', json.dumps(self.server.requests[1]['messages']))

    def test_g_repeated_denied_command_does_not_prompt_again(self):
        """Changing a purpose or check ID cannot repeat an already rejected command."""
        self.fixture()
        command={k:v for k,v in self.check().items() if k!='id'}
        self.start([('run_project_command',command),
            ('run_project_command',{**command,'purpose':'A different label','check_id':'retry'}),
            'The command was denied; execution is unverified.'])
        events=self.finish('reject')
        self.assertEqual(len([e for e in events if e['event']=='approval']),1)
        self.assertTrue(all(r.get('code')=='USER_DENIED' for r in self.receipts()))
        self.assertEqual(self.service.chat['task_checkpoint']['status'],'paused')

    def test_e_h_long_task_retains_goal_and_uses_full_canonical_history(self):
        self.fixture()
        for i in range(24):
            (self.root/f'part_{i}.py').write_text(f'part = {i}\n' + '# contextual source\n'*300)
        def decide(index, payload):
            self.assertIn('fix the requested behavior', json.dumps(payload['messages']))
            return ('read_range', {'path':f'part_{index}.py','start_line':1,'end_line':300}) if index<24 else 'Inspected 24 distinct sources; no edits requested for them.'
        self.service.config['settings'].update(budget_mode='manual',context_window=16384,max_tokens=1024,max_context_chars=12000)
        self.start(decide, options={'read_only':True})
        self.finish()
        task = self.service.chat['task_checkpoint']
        self.assertEqual(task['status'], 'completed')
        self.assertEqual(len(self.receipts()), 24)
        self.assertTrue(task['context']['compressed'])
        self.assertEqual(len({r['path'] for r in self.receipts()}), 24)

    def test_i_cancel_approval_then_resume_without_duplicate_effect(self):
        self.fixture()
        self.start([('patch_file', {'path':'calc.py','old_text':'return 1','new_text':'return 3'}),
            'Previous proposal was cancelled; no changes applied.'])
        while self.events.get(timeout=15)['event'] != 'approval':
            pass
        self.service.cancel()
        self.finish()
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'paused')
        self.assertIn('return 1', (self.root/'calc.py').read_text())
        self.service.start(self.root, {'mode':'ide','resume':True})
        self.finish()
        self.assertIn('return 1', (self.root/'calc.py').read_text())
        self.assertEqual(self.service.chat['task_checkpoint']['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
