import unittest
from agent.companion_policy import clean_speech_text, is_coding_request


class CompanionPolicyTests(unittest.TestCase):
    def test_only_coding_requests_can_delegate(self):
        for prompt in ('Сделай сайт игру змейка', 'Напиши код калькулятора', 'Исправь баг в Python', 'Объясни функцию на JavaScript', 'Refactor this component', 'Ошибка TypeError'):
            with self.subTest(prompt=prompt):self.assertTrue(is_coding_request(prompt))
        for prompt in ('Найди музыку', 'Напиши письмо', 'Сложный вопрос о вселенной', 'Открой VS Code', 'Найди код двери', 'Расскажи про Код да Винчи', 'Сделай заметку о покупках', 'Напиши программу праздника', 'Объясни функции холодильника'):
            with self.subTest(prompt=prompt):self.assertFalse(is_coding_request(prompt))

    def test_speech_removes_markdown_preserving_words_and_math(self):
        text = '## **Привет!**\n- Вот [ответ](https://example.com).\n2 * 3 = 6. `hello_world`\n```python\nprint(1)\n```'
        result=clean_speech_text(text)
        self.assertIn('Привет!',result);self.assertIn('2 умножить на 3 = 6.',result)
        self.assertIn('hello world',result);self.assertNotIn('print(1)',result)
        for mark in ('*','`','#','https://'):self.assertNotIn(mark,result)

    def test_internal_reasoning_is_not_spoken(self):
        self.assertEqual(clean_speech_text('<think>private</think>**Готово** &amp; ясно'), 'Готово & ясно')


class LolaIdeIsolationTests(unittest.TestCase):
    def test_lola_delegate_schema_and_runtime_exclude_ide(self):
        from agent.delegation import DELEGATE_TOOL
        from core.python.task_execution import TaskExecution
        from types import SimpleNamespace
        from unittest.mock import Mock
        self.assertEqual(DELEGATE_TOOL['function']['parameters']['properties']['target']['enum'],['chat'])
        receiver=SimpleNamespace(engine=SimpleNamespace(prompt='Напиши код Python'),_event=Mock())
        result=TaskExecution.request_delegation(receiver,'delegate_task',{'target':'ide','prompt':'Напиши код'})
        self.assertFalse(result['ok']);receiver._event.assert_not_called()

    def test_old_pending_lola_ide_handoff_cannot_start_ide(self):
        from core.python.task_service import TaskService
        from types import SimpleNamespace
        from unittest.mock import Mock
        receiver=SimpleNamespace(idle=Mock(),handoff_pending={'id':'legacy','target':'ide'},select_chat=Mock())
        with self.assertRaisesRegex(ValueError,'не связана с IDE'):TaskService.prepare_handoff(receiver,'project',{'id':'legacy'})
        receiver.select_chat.assert_not_called()
