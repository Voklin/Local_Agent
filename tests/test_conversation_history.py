"""Conversation history regression tests. Run: python -m unittest discover -s tests -v"""
import unittest
from agent.conversation import build_messages


class ConversationHistoryTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
