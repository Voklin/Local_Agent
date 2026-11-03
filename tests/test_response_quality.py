"""Strict semantic-check output and bounded incomplete-answer recovery."""
import json
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from agent.response_outcome import parse_completion_assessment
from agent import engine as module
from tests import test_core_reliability as fixture


class ResponseQualityTests(unittest.TestCase):
    setUp=fixture.CoreReliabilityTests.setUp

    def test_completion_assessment_rejects_truthy_strings_missing_and_ambiguous_json(self):
        for raw in ('{"complete":"false"}','{"complete":1}','{}','{"complete":null}',
                    '{"complete":true,"complete":false}','prefix {"complete":true}', '{"complete":true,"reason":[]}'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):parse_completion_assessment(raw)
        self.assertEqual(parse_completion_assessment('```json\n{"complete":false,"reason":"Нет изменений"}\n```'),(False,'Нет изменений'))

    def test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success(self):
        requests=[]
        class Client:
            def __init__(self,*args,**kwargs):pass
            def create(self,**kwargs):
                requests.append(kwargs)
                if kwargs.get('stream'):return fixture.Stream([fixture.delta('Сейчас исправлю код.')])
                return NS(choices=[NS(message=NS(content=json.dumps({'complete':False,'reason':'Нет выполненных действий'})),finish_reason='stop')])
            def close(self):pass
            def cancel(self):pass
        engine=module.AgentEngine('http://unused.invalid','','fixture',str(self.root),'Исправь ошибку',auto_memory=False,task_id=__import__('uuid').uuid4().hex)
        with patch.object(module,'ModelClient',Client):engine.run()
        self.assertEqual(engine.task_snapshot()['run_state'],'paused',str(engine.task_snapshot().get('completion_assessment'))+' requests='+str(len(requests)))
        self.assertEqual(engine.task_snapshot()['completion_assessment']['status'],'incomplete')
        self.assertEqual(sum(bool(r.get('stream')) for r in requests),3)
        self.assertEqual(len(requests),6)
        self.assertIn('двух попыток',engine.task_snapshot()['stop_reason'])

    def test_informational_answer_has_no_verification_model_overhead(self):
        engine,messages,_=fixture.CoreReliabilityTests.run_engine(self,[[fixture.delta('Объяснение без доступа к файлам.')]],prompt='Что такое рекурсия?',allow_tools=False)
        self.assertEqual(engine.task_snapshot()['run_state'],'completed')
        self.assertNotIn('completion_assessment',engine.task_snapshot())


    def test_empty_terminal_answer_gets_bounded_text_recovery(self):
        engine,messages,_=fixture.CoreReliabilityTests.run_engine(self,[[fixture.delta(None)],[fixture.delta('Содержательный ответ.')]],prompt='Объясни рекурсию',allow_tools=False)
        self.assertEqual(engine.task_snapshot()['run_state'],'completed')
        self.assertEqual(engine.task_snapshot()['answer_retries'],1)
        self.assertEqual(messages[-1]['content'],'Содержательный ответ.')


    def test_explicit_source_location_format_repairs_without_replaying_tools(self):
        engine,messages,_=fixture.CoreReliabilityTests.run_engine(self,[[fixture.delta('src/main.py:def run():')],[fixture.delta('src/main.py:7')]],prompt='Ответь в формате путь:строка.',allow_tools=False)
        self.assertEqual(engine.task_snapshot()['run_state'],'completed')
        self.assertEqual(engine.task_snapshot()['answer_quality']['repairs'],1)
        self.assertEqual(messages[-1]['content'],'src/main.py:7')

    def test_format_guard_does_not_apply_to_freeform_questions(self):
        from agent.response_outcome import answer_format_issue
        self.assertEqual(answer_format_issue('Объясни формат путь:строка','Обычное объяснение'), '')
        self.assertEqual(answer_format_issue('Answer in format path:line','src/main.py:7'), '')
        self.assertTrue(answer_format_issue('Ответь в формате путь:строка','src/main.py:0'))
