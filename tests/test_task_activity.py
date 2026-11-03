import json
import unittest
from agent.task_store import new_task, set_stage
from agent.task_activity import begin_tool, update_tool, finish_tool, recover_tools, MAX_ACTIVITY


class TaskActivityTests(unittest.TestCase):
    def test_activity_is_bounded_metadata_with_monotonic_ids(self):
        task = new_task('test', '.', 'hello')
        for number in range(MAX_ACTIVITY + 3):
            activity = begin_tool(task, 'write_file', {'path': 'file.txt', 'content': 'PRIVATE_CONTENT'}, str(number), 0)
            finish_tool(task, activity, 'write_file', {'ok': True, 'content': 'PRIVATE_CONTENT'})
        self.assertEqual(len(task['tool_activity']), MAX_ACTIVITY)
        self.assertEqual(task['activity_omitted'], 3)
        self.assertEqual(task['tool_activity'][-1]['id'], MAX_ACTIVITY + 3)
        self.assertNotIn('PRIVATE_CONTENT', json.dumps(task))
        self.assertEqual(task['stage'], 'implementation')
        self.assertEqual(len([s for s in task['stages'] if s['id'] == 'implementation']), 1)

    def test_tool_outcomes_distinguish_denial_cancel_failure_and_truncation(self):
        task = new_task('test', '.', 'hello')
        for result, status in [({'ok': False, 'code': 'USER_DENIED'}, 'rejected'),
                               ({'ok': False, 'code': 'USER_CANCELLED'}, 'cancelled'),
                               ({'ok': False, 'error': 'conflict'}, 'failed')]:
            activity = begin_tool(task, 'write_file', {}, 'same', 0)
            finish_tool(task, activity, 'write_file', result)
            self.assertEqual(task['tool_activity'][-1]['status'], status)
        activity = begin_tool(task, 'search_text', {}, 'search', 0)
        finish_tool(task, activity, 'search_text', {'ok': True, 'matches': [1, 2], 'truncated': True})
        self.assertIn('2', task['tool_activity'][-1]['summary'])
        self.assertIn('лимит', task['tool_activity'][-1]['summary'])

    def test_activity_recovery_uses_anchored_result_and_is_idempotent(self):
        task = new_task('test', '.', 'hello')
        call = {'role': 'assistant', 'tool_calls': [{'id': 'same'}]}
        messages = [call, {'role': 'tool', 'tool_call_id': 'same', 'content': '{"ok":true}'},
                    {'role': 'user', 'content': 'next'}, call]
        activity = begin_tool(task, 'write_file', {'path': 'file.txt'}, 'same', 3)
        update_tool(task, activity, 'applying', 'writing')
        self.assertTrue(recover_tools(task, messages))
        self.assertEqual(task['tool_activity'][-1]['status'], 'unknown')
        self.assertFalse(recover_tools(task, messages))
        activity = begin_tool(task, 'read_file', {'path': 'file.txt'}, 'same', 3)
        messages.append({'role': 'tool', 'tool_call_id': 'same', 'content': '{"ok":true,"content":"abc"}'})
        self.assertTrue(recover_tools(task, messages))
        self.assertEqual(task['tool_activity'][-1]['status'], 'succeeded')
        self.assertIn('3', task['tool_activity'][-1]['summary'])
        self.assertNotIn('abc', json.dumps(task))

    def test_recovery_interrupts_waiting_without_replaying_approval(self):
        task = new_task('test', '.', 'hello')
        activity = begin_tool(task, 'write_file', {}, 'call', 0)
        update_tool(task, activity, 'awaiting_approval', 'waiting')
        self.assertTrue(recover_tools(task, []))
        self.assertEqual(task['tool_activity'][-1]['status'], 'interrupted')
        self.assertFalse(recover_tools(task, []))

    def test_stage_transitions_skip_unvisited_and_keep_only_one_active(self):
        task = new_task('test', '.', 'измени файл')
        set_stage(task, 'analysis')
        begin_tool(task, 'write_file', {}, 'write', 0)
        self.assertEqual(next(s['status'] for s in task['stages'] if s['id'] == 'research'), 'skipped')
        begin_tool(task, 'read_file', {}, 'read', 0)
        self.assertEqual([s['id'] for s in task['stages'] if s['status'] == 'active'], ['research'])
        self.assertEqual(next(s['status'] for s in task['stages'] if s['id'] == 'implementation'), 'done')
