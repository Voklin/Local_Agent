from copy import deepcopy
import unittest

from agent.run_state import InvalidRunStateTransition, RunState


class RunStateTests(unittest.TestCase):
    def test_approval_execution_verification_and_completion_share_legacy_status(self):
        stages = [{'id': 'implementation', 'status': 'active'}]
        task = {'status': 'running', 'stage': 'implementation', 'stages': stages}
        state = RunState(task)
        for phase in ('waiting_approval', 'executing', 'verifying'):
            self.assertEqual(state.transition(phase, f'event: {phase}'), phase)
            self.assertEqual(state.phase, phase)
            self.assertEqual(task['run_state'], phase)
            self.assertEqual(task['status'], 'running')
            self.assertEqual(task['last_event'], f'event: {phase}')
            self.assertEqual(task['stop_reason'], '')
        state.transition('completed')
        self.assertEqual(task['status'], 'completed')
        self.assertEqual(task['last_event'], 'Задача завершена')
        self.assertEqual(task['stage'], 'implementation')
        self.assertIs(task['stages'], stages)
        self.assertEqual(stages, [{'id': 'implementation', 'status': 'active'}])

    def test_unknown_effect_pause_and_failure_can_resume_with_reason_cleared(self):
        for phase in ('needs_attention', 'paused', 'failed'):
            with self.subTest(phase=phase):
                task = {'status': 'running'}
                state = RunState(task)
                state.transition('executing')
                state.transition(phase, 'Execution interrupted')
                self.assertEqual(task['status'], 'paused')
                self.assertEqual(task['stop_reason'], 'Execution interrupted')
                self.assertEqual(task['last_event'], 'Execution interrupted')
                state.transition('running', 'Resumed by user')
                self.assertEqual(task['run_state'], 'running')
                self.assertEqual(task['status'], 'running')
                self.assertEqual(task['stop_reason'], '')
                self.assertEqual(task['last_event'], 'Resumed by user')

    def test_recovery_can_reclassify_stopped_run_without_executing_it(self):
        task = {'status': 'paused', 'run_state': 'failed'}
        state = RunState(task)
        state.transition('needs_attention', 'Effect could not be confirmed')
        state.transition('paused', 'Waiting for user')
        self.assertEqual(task['status'], 'paused')
        self.assertEqual(task['stop_reason'], 'Waiting for user')
        before = deepcopy(task)
        with self.assertRaises(InvalidRunStateTransition):
            state.transition('executing')
        self.assertEqual(task, before)

    def test_completed_run_cannot_reopen_or_change_terminal_outcome(self):
        task = {'status': 'completed'}
        state = RunState(task)
        before = deepcopy(task)
        for phase in ('running', 'executing', 'paused', 'failed', 'needs_attention'):
            with self.subTest(phase=phase), self.assertRaises(InvalidRunStateTransition):
                state.transition(phase, 'Reopen')
            self.assertEqual(task, before)
        state.transition('completed')
        self.assertEqual(task, before)

    def test_finishing_without_tools_and_during_execution_is_permitted(self):
        for phase in ('running', 'executing', 'verifying'):
            with self.subTest(phase=phase):
                task = {'run_state': phase, 'status': 'running'}
                RunState(task).transition('completed')
                self.assertEqual(task['status'], 'completed')
                self.assertEqual(task['stop_reason'], '')

    def test_approval_wait_cannot_be_marked_completed(self):
        task = {'status': 'running'}
        state = RunState(task)
        state.transition('waiting_approval')
        before = deepcopy(task)
        with self.assertRaises(InvalidRunStateTransition):
            state.transition('completed')
        self.assertEqual(task, before)
        state.transition('running')
        state.transition('completed')

    def test_legacy_tasks_migrate_without_losing_event_or_plan(self):
        for status in ('running', 'paused', 'completed'):
            with self.subTest(status=status):
                task = {'status': status, 'stage': 'analysis', 'stages': [],
                        'stop_reason': 'Previous reason', 'last_event': 'Previous event'}
                state = RunState(task)
                self.assertEqual(state.phase, status)
                self.assertEqual(task['run_state'], status)
                self.assertEqual(task['last_event'], 'Previous event')
                self.assertEqual(task['stop_reason'], 'Previous reason')
                self.assertEqual(task['stage'], 'analysis')

    def test_unrecognized_legacy_status_requires_attention(self):
        task = {'status': 'interrupted'}
        self.assertEqual(RunState(task).phase, 'needs_attention')
        self.assertEqual(task['status'], 'paused')

    def test_existing_run_phase_takes_precedence_and_is_shared(self):
        task = {'status': 'running', 'run_state': 'paused'}
        first = RunState(task)
        second = RunState(task)
        self.assertEqual(task['status'], 'paused')
        second.transition('running')
        self.assertEqual(first.phase, 'running')
        first.transition('executing')
        self.assertEqual(second.phase, 'executing')

    def test_repeated_transition_preserves_event_and_reason(self):
        task = {'status': 'running'}
        state = RunState(task)
        state.transition('needs_attention', 'Unknown file write outcome')
        before = deepcopy(task)
        state.transition('needs_attention')
        self.assertEqual(task, before)
        state.transition('needs_attention', 'Recovery still uncertain')
        self.assertEqual(task['stop_reason'], 'Recovery still uncertain')
        self.assertEqual(task['last_event'], 'Recovery still uncertain')

    def test_unknown_phase_is_rejected_without_changing_task(self):
        task = {'status': 'running'}
        state = RunState(task)
        before = deepcopy(task)
        for phase in ('unknown', '', None, [], {}):
            with self.subTest(phase=phase), self.assertRaises(InvalidRunStateTransition):
                state.transition(phase)
            self.assertEqual(task, before)
        bad_task = {'status': 'running', 'run_state': 'unknown'}
        with self.assertRaises(InvalidRunStateTransition):
            RunState(bad_task)
        self.assertEqual(bad_task, {'status': 'running', 'run_state': 'unknown'})

    def test_optional_task_obeys_same_transitions(self):
        state = RunState(None)
        self.assertIsNone(state.task)
        self.assertEqual(state.phase, 'running')
        state.transition('executing')
        state.transition('failed')
        state.transition('running')
        state.transition('completed')
        with self.assertRaises(InvalidRunStateTransition):
            state.transition('running')

    def test_reasons_are_bounded_and_nonempty_for_failures(self):
        task = {'status': 'running'}
        state = RunState(task)
        state.transition('failed', 'x' * 600)
        self.assertEqual(len(task['stop_reason']), 500)
        self.assertEqual(task['last_event'], task['stop_reason'])
        state.transition('running')
        state.transition('failed')
        self.assertTrue(task['stop_reason'])
        self.assertEqual(task['last_event'], task['stop_reason'])


if __name__ == '__main__':
    unittest.main()
