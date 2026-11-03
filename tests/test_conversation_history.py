"""Conversation history regression tests. Run: python -m unittest discover -s tests -v"""
import unittest
import json
from copy import deepcopy
from agent.context_manager import ContextManager
from agent.conversation import build_messages, select_recent_history, compact_live_messages


class ConversationHistoryTests(unittest.TestCase):
    def test_archive_builder_keeps_all_turns_and_copies_nested_calls(self):
        history = [{'role': 'user', 'content': str(i)} for i in range(30)]
        history.append({'role': 'assistant', 'tool_calls': [{'id': 'one', 'function': {'arguments': '{}'}}]})
        messages = build_messages(history, 'new request')
        self.assertEqual(messages[:-1], history)
        messages[-2]['tool_calls'][0]['function']['arguments'] = 'changed'
        self.assertEqual(history[-1]['tool_calls'][0]['function']['arguments'], '{}')

    def test_model_context_preserves_partial_batch_and_omits_orphans(self):
        messages = [
            {'role': 'system', 'content': 'system'},
            {'role': 'user', 'content': 'old'},
            {'role': 'assistant', 'tool_calls': [{'id': 'a'}, {'id': 'b'}]},
            {'role': 'tool', 'tool_call_id': 'a', 'content': 'partial'},
            {'role': 'user', 'content': 'current'},
            {'role': 'tool', 'tool_call_id': 'orphan', 'content': 'orphan'},
            {'role': 'assistant', 'tool_calls': [{'id': 'c'}, {'id': 'd'}]},
            {'role': 'tool', 'tool_call_id': 'c', 'content': 'one'},
            {'role': 'tool', 'tool_call_id': 'd', 'content': 'two'},
        ]
        original = deepcopy(messages)
        context = ContextManager().build(messages)
        self.assertEqual([m['tool_call_id'] for m in context if m['role'] == 'tool'], ['a', 'b', 'c', 'd'])
        self.assertEqual(next(m['content'] for m in context if m.get('tool_call_id')=='a'),'partial')
        missing=json.loads(next(m['content'] for m in context if m.get('tool_call_id')=='b'))
        self.assertEqual(missing['code'],'OUTCOME_UNKNOWN');self.assertFalse(missing['ok'])
        self.assertEqual(messages, original)

    def test_serialized_context_budget_keeps_current_request_and_tool_pairs(self):
        messages = [{'role': 'system', 'content': 'system'}, {'role': 'user', 'content': 'current request'}]
        messages += [{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'one', 'function': {'name': 'read_file', 'arguments': '{}'}}]},
                     {'role': 'tool', 'tool_call_id': 'one', 'content': '\"\nПривет' * 4000}]
        original = deepcopy(messages)
        context = ContextManager(max_chars=1200).build(messages)
        self.assertLessEqual(len(json.dumps(context, ensure_ascii=False)), 1200)
        self.assertEqual(context[1], messages[1])
        self.assertEqual(context[-2]['tool_calls'][0]['id'], context[-1]['tool_call_id'])
        self.assertEqual(messages, original)

    def test_oversized_mandatory_instructions_fail_without_truncation(self):
        messages = [{'role': 'system', 'content': 'system' * 1000}, {'role': 'user', 'content': 'task'}]
        with self.assertRaises(ValueError):
            ContextManager(max_chars=500).build(messages)
        self.assertEqual(len(messages[0]['content']), 6000)

    def test_current_run_request_survives_internal_continuation(self):
        messages = [{'role': 'system', 'content': 'system'}, {'role': 'user', 'content': 'old chat'},
                    {'role': 'user', 'content': 'current task'}]
        messages += [{'role': 'assistant', 'content': 'step'} for _ in range(20)]
        messages += [{'role': 'user', 'content': 'internal continuation'}]
        result = compact_live_messages(messages, keep_recent_rounds=2, request_index=2)
        self.assertEqual([m['content'] for m in result if m['role'] == 'user'], ['current task', 'internal continuation'])

    def test_followup_keeps_previous_user_and_assistant_messages(self):
        history = [
            {"role": "user", "content": "Предложи изменение функции greet."},
            {"role": "assistant", "content": "Могу изменить greet. Подтвердить?"},
        ]
        messages = build_messages(history, "Да, подтверждаю.")
        self.assertEqual(messages[0], history[0])
        self.assertEqual(messages[1], history[1])
        self.assertEqual(messages[2], {"role": "user", "content": "Да, подтверждаю."})
        self.assertEqual(len(history), 2, "The input history must not be mutated")

    def test_tool_call_and_tool_result_are_preserved(self):
        tool_assistant = {
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": "call_1", "type": "function", "function": {"name": "read_file", "arguments": '{"path":"hello.py"}'}}],
        }
        tool_result = {"role": "tool", "tool_call_id": "call_1", "content": '{"ok":true,"content":"print(1)"}'}
        messages = build_messages([tool_assistant, tool_result], "Теперь измени функцию.")
        self.assertEqual(messages[:2], [tool_assistant, tool_result])
        self.assertEqual(messages[-1]["content"], "Теперь измени функцию.")

    def test_empty_history_starts_cleanly(self):
        self.assertEqual(build_messages([], "Привет"), [{"role": "user", "content": "Привет"}])


    def test_old_turns_are_trimmed_but_recent_confirmation_context_remains(self):
        history = []
        for i in range(12):
            history.extend([
                {"role": "user", "content": f"Задача {i}"},
                {"role": "assistant", "content": f"Ответ {i}"},
            ])
        history.extend([
            {"role": "user", "content": "Измени файл?"},
            {"role": "assistant", "content": "Предлагаю diff. Подтвердить?"},
        ])
        original_count = len(history)
        selected = select_recent_history(history, max_chars=10000, max_turns=5)
        self.assertLess(len(selected), len(history))
        self.assertEqual(selected[-1]["content"], "Предлагаю diff. Подтвердить?")
        self.assertEqual(len(history), original_count)

    def test_live_compaction_preserves_system_original_request_and_recent_tool_pair(self):
        history = [{"role": "system", "content": "system"}, {"role": "user", "content": "Original task"}]
        for i in range(15):
            call_id = f"c{i}"
            history.extend([
                {"role": "assistant", "content": f"step {i}", "tool_calls": [{"id": call_id, "type": "function", "function": {"name": "read_file", "arguments": '{"path":"x.py"}'}}]},
                {"role": "tool", "tool_call_id": call_id, "content": f"result {i}"},
            ])
        compacted = compact_live_messages(history, max_chars=12000, keep_recent_rounds=4)
        self.assertEqual(compacted[0]["role"], "system")
        self.assertTrue(any(m.get("role") == "user" and m.get("content") == "Original task" for m in compacted))
        assistant_calls = [tc["id"] for m in compacted if m.get("role") == "assistant" for tc in m.get("tool_calls", [])]
        tool_results = [m["tool_call_id"] for m in compacted if m.get("role") == "tool"]
        self.assertEqual(assistant_calls, tool_results)
        self.assertLess(len(compacted), len(history))

    def test_tool_results_are_bounded_without_dropping_tool_call_pair(self):
        history = [
            {"role": "user", "content": "Прочитай файл"},
            {"role": "assistant", "content": None, "tool_calls": [{"id": "c1", "type": "function", "function": {"name": "read_file", "arguments": '{"path":"main.py"}'}}]},
            {"role": "tool", "tool_call_id": "c1", "content": "x" * 12000},
            {"role": "assistant", "content": "Файл прочитан"},
        ]
        selected = select_recent_history(history)
        self.assertEqual(selected[1]["tool_calls"][0]["id"], "c1")
        self.assertEqual(selected[2]["tool_call_id"], "c1")
        self.assertLess(len(selected[2]["content"]), 7000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
