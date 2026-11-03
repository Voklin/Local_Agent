"""Regression scenarios from the Neutral core audit, using no external model."""
import json
import tempfile
import threading
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from agent import engine as module, task_store, model_preferences, companion_preferences
from agent.json_tools import JsonToolStream
from agent.responses_adapter import ResponseEvents
from agent.tools import TOOL_DEFINITIONS
from core.python.task_service import TaskService


def delta(text=None, calls=(), finish='stop', refusal=None):
    return NS(choices=[NS(delta=NS(content=text,tool_calls=list(calls),refusal=refusal),finish_reason=finish)])


def call(name, arguments, identity='test_call'):
    return NS(index=0,id=identity,function=NS(name=name,arguments=json.dumps(arguments)))


class Stream:
    def __init__(self, chunks):self.chunks=chunks
    def __iter__(self):return iter(self.chunks)
    def close(self):pass


class CoreReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'project';self.root.mkdir()
        self.patch=patch.object(task_store,'TASK_DIR',Path(self.temp.name)/'profile/tasks');self.patch.start();self.addCleanup(self.patch.stop)

    def run_engine(self, replies, handler=None, **options):
        class Client:
            def __init__(self,*_,**__):self.replies=iter(replies)
            def create(self,**request):
                if request.get('stream'):return Stream(next(self.replies))
                return NS(choices=[NS(message=NS(content='{"complete":true}'))])
            def close(self):pass
            def cancel(self):pass
        engine=module.AgentEngine(options.pop('endpoint','http://unused.invalid'),'','fixture',str(self.root),
            options.pop('prompt','Исправь код и проверь тесты'),task_id=uuid.uuid4().hex,
            auto_memory=False,tool_handler=handler,**options)
        errors=[];messages=[];chats=[]
        engine.failed.connect(errors.append)
        engine.conversation_updated.connect(lambda history:messages.append(history))
        engine.chat.connect(lambda role,text:chats.append((role,text)))
        with patch.object(module,'ModelClient',Client):engine.run()
        self.assertEqual(errors,[])
        return engine,messages[-1],chats

    def test_truncated_answer_is_saved_and_paused(self):
        engine,messages,_=self.run_engine([[delta('Частичный ответ',finish='length')]],allow_tools=False)
        self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertEqual(engine.task_snapshot()['finish_reason'],'length')
        self.assertEqual(messages[-1]['content'],'Частичный ответ')

    def test_truncated_native_tool_is_never_executed(self):
        executed=[]
        engine,messages,_=self.run_engine([[delta(calls=[call('read_file',{'path':'a.txt'})],finish='length')]],handler=lambda *args:executed.append(args))
        self.assertEqual(executed,[]);self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertFalse(any(m.get('tool_calls') for m in messages))

    def test_eof_without_terminal_reason_preserves_partial_and_pauses(self):
        """EOF cannot certify a partial answer as completed."""
        engine,messages,_=self.run_engine([[delta('Часть ответа',finish=None)]],allow_tools=False)
        self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertEqual(engine.task_snapshot()['response_outcome']['status'],'incomplete')
        self.assertEqual(messages[-1]['content'],'Часть ответа')

    def test_eof_without_terminal_reason_never_executes_native_call(self):
        """Even complete-looking call arguments cannot compensate for missing termination."""
        executed=[]
        engine,messages,_=self.run_engine([[delta(calls=[call('read_file',{'path':'a.txt'})],finish=None)]],handler=lambda *args:executed.append(args))
        self.assertEqual(executed,[]);self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertFalse(any(m.get('tool_calls') for m in messages))

    def test_access_policy_is_rechecked_after_file_approval(self):
        """A changed ignore policy during approval blocks the impending write."""
        def approve(*_args):
            """Simulate an external user policy edit while the diff was open."""
            (self.root/'.neutralignore').write_text('late.txt\n',encoding='utf-8');return 'apply'
        with patch.object(module.AgentEngine,'_ask_write_approval',side_effect=approve):
            _,messages,_=self.run_engine([[delta(calls=[call('write_file',{'path':'late.txt','content':'x','overwrite':False})])],[delta('Правило доступа изменилось.')]])
        result=next(json.loads(m['content']) for m in messages if m.get('role')=='tool')
        self.assertEqual(result['code'],'ACCESS_DENIED');self.assertFalse((self.root/'late.txt').exists())

    def test_auto_local_continues_text_without_duplicate_canonical_fragments(self):
        """An output-length boundary is resumed with one combined saved assistant answer."""
        engine,messages,_=self.run_engine([[delta('Первая ',finish='length')],[delta('вторая')]],allow_tools=False,
            endpoint='http://127.0.0.1:1234/v1',settings={'budget_mode':'auto','max_agent_turns':1,'max_runtime_minutes':1})
        self.assertEqual(engine.task_snapshot()['status'],'completed')
        self.assertEqual([m['content'] for m in messages if m['role']=='assistant'],['Первая вторая'])
        self.assertIsNone(engine._runtime_timer)

    def test_auto_local_retries_truncated_call_without_executing_its_fragment(self):
        """Only the complete regenerated call reaches the handler, despite tiny old cumulative caps."""
        executed=[]
        engine,messages,_=self.run_engine([[delta(calls=[call('read_file',{'path':'discard.txt'})],finish='length')],
            [delta(calls=[call('read_file',{'path':'actual.txt'})])],[delta('Готово')]],
            handler=lambda name,args:(executed.append(args) or {'ok':True,'content':'fixture'}),
            endpoint='http://127.0.0.1:1234/v1',settings={'budget_mode':'auto','max_tool_calls':1,'max_agent_turns':1})
        self.assertEqual(executed,[{'path':'actual.txt'}]);self.assertEqual(engine.task_snapshot()['status'],'completed')

    def test_native_refusal_is_visible_and_not_completed(self):
        engine,messages,_=self.run_engine([[delta(refusal='Не могу выполнить запрос')]],allow_tools=False)
        self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertEqual(messages[-1]['content'],'Не могу выполнить запрос')

    def test_malformed_write_returns_error_and_allows_model_repair(self):
        engine,messages,_=self.run_engine([[delta(calls=[call('write_file',{'path':None,'content':'x','overwrite':False})])],[delta('Путь нужно уточнить')]])
        results=[json.loads(m['content']) for m in messages if m.get('role')=='tool']
        self.assertFalse(results[0]['ok']);self.assertIn('path',results[0]['error'])
        self.assertEqual(engine.task_snapshot()['status'],'completed')
        self.assertFalse((self.root/'x').exists())

    def test_preview_io_error_is_a_tool_result_not_a_failed_run(self):
        with patch.object(module,'preview_file_change',side_effect=OSError('fixture disk unavailable')):
            _,messages,_=self.run_engine([[delta(calls=[call('write_file',{'path':'a.txt','content':'x','overwrite':False})])],[delta('Не удалось подготовить изменение')]])
        result=next(json.loads(m['content']) for m in messages if m.get('role')=='tool')
        self.assertFalse(result['ok']);self.assertIn('diff',result['error'])

    def test_cancel_with_assistant_commentary_is_paused(self):
        with patch.object(module.AgentEngine,'_ask_write_approval',return_value='cancel'):
            engine,_,_=self.run_engine([[delta('Сейчас создам файл',calls=[call('write_file',{'path':'cancelled.txt','content':'x','overwrite':False})])]])
        self.assertEqual(engine.task_snapshot()['run_state'],'paused')
        self.assertFalse((self.root/'cancelled.txt').exists())

    def test_failed_command_cannot_be_overruled_by_final_answer(self):
        definition={'type':'function','function':{'name':'run_project_command'}}
        engine,_,chats=self.run_engine([[delta(calls=[call('run_project_command',{'program':'test','arguments':[]})])]]+[[delta('Готово, всё работает')]]*3,
            handler=lambda *_:{'ok':False,'exit_code':7,'output':'1 test failed'},tool_definitions=[definition])
        task=engine.task_snapshot()
        self.assertEqual(task['status'],'paused');self.assertEqual(task['verification']['status'],'failed')
        self.assertEqual(task['test_results'][0]['exit_code'],7)
        self.assertTrue(any(role=='system' and 'Проверка не прошла' in text for role,text in chats))

    def test_successful_retry_of_same_command_resolves_failed_evidence(self):
        result=iter([{'ok':False,'exit_code':7},{'ok':True,'exit_code':0}])
        definition={'type':'function','function':{'name':'run_project_command'}}
        args={'program':'test','arguments':[]}
        engine,_,_=self.run_engine([[delta(calls=[call('run_project_command',args,'one')])],
            [delta(calls=[call('run_project_command',args,'two')])],[delta('Проверки прошли')]],
            handler=lambda *_:next(result),tool_definitions=[definition])
        task=engine.task_snapshot();self.assertEqual(task['status'],'completed')
        self.assertEqual(task['verification']['status'],'commands_passed');self.assertEqual(len(task['test_results']),1)

    def test_unrelated_success_does_not_erase_failed_command(self):
        result=iter([{'ok':False,'exit_code':7},{'ok':True,'exit_code':0}])
        definition={'type':'function','function':{'name':'run_project_command'}}
        engine,_,_=self.run_engine([[delta(calls=[call('run_project_command',{'program':'test','arguments':[]},'one')])],
            [delta(calls=[call('run_project_command',{'program':'lint','arguments':[]},'two')])]]+[[delta('Готово')]]*3,
            handler=lambda *_:next(result),tool_definitions=[definition])
        self.assertEqual(engine.task_snapshot()['status'],'paused')

    def test_answer_without_commands_is_explicitly_unverified(self):
        engine,_,_=self.run_engine([[delta('Результат описан')]])
        self.assertEqual(engine.task_snapshot()['verification']['status'],'not_run')
        self.assertIn('не подтверждена',engine.task_snapshot()['last_event'])

    def test_runtime_uses_one_minute_and_timer_is_always_cancelled(self):
        with patch.object(module.threading,'Timer') as timer:
            engine,_,_=self.run_engine([[delta('Ответ')]],settings={'max_runtime_minutes':1})
        self.assertEqual(timer.call_args.args[0],60)
        timer.return_value.cancel.assert_called_once()
        engine._expire_runtime();self.assertTrue(engine.isInterruptionRequested())
        self.assertIn('лимит времени',engine.interruption_reason())

    def test_runtime_expiry_interrupts_an_outstanding_approval(self):
        original=module.AgentEngine._ask_write_approval
        def expire_at_approval(engine,path,diff,exists):
            engine.write_approval_requested.connect(lambda *_:engine._expire_runtime())
            return original(engine,path,diff,exists)
        with patch.object(module.AgentEngine,'_ask_write_approval',expire_at_approval):
            engine,_,_=self.run_engine([[delta(calls=[call('write_file',{'path':'unwritten.txt','content':'x','overwrite':False})])]])
        self.assertEqual(engine.task_snapshot()['status'],'paused')
        self.assertIn('лимит времени',engine.task_snapshot()['stop_reason'])
        self.assertFalse((self.root/'unwritten.txt').exists())

    def test_json_truncation_does_not_parse_or_execute_complete_prefix(self):
        text='{"tool_calls":[{"name":"read_file","arguments":{"path":"a.txt"}}]} extra'
        for choice in ('auto','required'):
            chunks=list(JsonToolStream(Stream([delta(text,finish='length')]),{'read_file'},choice))
            self.assertEqual(chunks[0].choices[0].finish_reason,'length')
            self.assertEqual(chunks[0].choices[0].delta.tool_calls,[])

    def test_responses_incomplete_and_refusal_are_not_cached_as_success(self):
        cache={};adapter=ResponseEvents(cache)
        terminal=adapter.translate(NS(type='response.incomplete',response=NS(incomplete_details=NS(reason='max_output_tokens'))))
        self.assertEqual(terminal.choices[0].finish_reason,'length');self.assertEqual(cache,{})
        adapter.translate(NS(type='response.refusal.delta',delta='Refusal'))
        terminal=adapter.translate(NS(type='response.completed',response=NS(output=[])))
        self.assertEqual(terminal.choices[0].finish_reason,'refusal')

    def test_endpoint_change_clears_omitted_or_stale_model_and_stt_keys(self):
        for explicit in (False,True):
            service=TaskService.__new__(TaskService);service.lock=threading.RLock();service.runs={}
            service.companion_config={**companion_preferences.DEFAULT_PROFILE,'api_key':'fixture-model','stt_api_key':'fixture-stt'}
            params={'base_url':'https://new.invalid/v1','stt_url':'https://new.invalid/stt'}
            if explicit:params.update(api_key='fixture-model',stt_api_key='fixture-stt')
            with patch.object(companion_preferences,'PROFILE_FILE',self.root/'profile.json'):
                public=service.configure_companion(params)
            self.assertEqual(service.companion_config['api_key'],'');self.assertEqual(service.companion_config['stt_api_key'],'')
            self.assertNotIn('api_key',public)
            self.assertNotIn('fixture-model',(self.root/'profile.json').read_text())

    def test_key_is_retained_for_same_endpoint_and_fresh_key_for_new_endpoint(self):
        previous={'base_url':'https://one.invalid/v1','api_key':'old'}
        self.assertEqual(model_preferences.connection_key(previous,previous,{}),'old')
        self.assertEqual(model_preferences.connection_key(previous,{'base_url':'https://two.invalid/v1'},{'api_key':'fresh'}),'fresh')


if __name__=='__main__':unittest.main()
