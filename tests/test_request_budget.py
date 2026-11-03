"""Full payload limits, lazy schemas, stable result references and reported usage."""
import copy
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from agent import task_store, model_preferences
from agent.context_manager import ContextManager
from agent.context_tools import find_mcp_tools, read_saved_result
from agent.engine import AgentEngine
from agent.model_client import ModelClient
from agent.request_budget import RequestBudget, BudgetExceededError, prepare_model_request


def definition(name='mcp_test', width=1):
    return {'type':'function','function':{'name':name,'description':'Add numbers сумма сложение',
        'parameters':{'type':'object','properties':{f'arg_{i}':{'type':'string','description':'value'*20} for i in range(width)}}}}


class UsageHandler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass

    def do_POST(self):
        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(payload)
        if self.server.reject_usage and 'stream_options' in payload:
            self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(b'{"error":{"message":"Unsupported parameter stream_options","type":"invalid_request_error"}}');return
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        chunks=[{'choices':[{'index':0,'delta':{'content':'42'},'finish_reason':'stop'}],
            'usage':{'prompt_tokens':90,'completion_tokens':1,'total_tokens':91}},
            {'choices':[],'usage':{'prompt_tokens':90,'completion_tokens':2,'total_tokens':92}}]
        for chunk in chunks:
            chunk.update(id='usage-fixture',object='chat.completion.chunk',model='fixture')
            self.wfile.write(('data: '+json.dumps(chunk)+'\n\n').encode())
        self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()


class RequestBudgetTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        context=patch.object(task_store,'TASK_DIR',self.root/'tasks');context.start();self.addCleanup(context.stop)

    def test_4k_8k_32k_windows_fit_complete_native_and_json_payloads(self):
        history=[{'role':'system','content':'Помощник.'}]
        for i in range(35):history.extend([{'role':'user','content':f'Вопрос {i}'},{'role':'assistant','content':'Подробный ответ о проекте. '*80}])
        history.append({'role':'user','content':'Объясни последнее решение.'})
        for window in (4096,8192,32768):
            for protocol in ('native','json'):
                with self.subTest(window=window,protocol=protocol):
                    original={'model':'fixture','messages':copy.deepcopy(history),'tools':[definition(width=2)],'max_tokens':512,'stream':True}
                    before=copy.deepcopy(original);budget=RequestBudget(window,256)
                    fitted,stats=budget.fit(original,tool_protocol=protocol,protected_text=history[-1]['content'])
                    budget.check(prepare_model_request(fitted,protocol),fitted['tools'])
                    self.assertGreaterEqual(stats['remaining_tokens'],0)
                    self.assertEqual(sum(stats['components'].values()),stats['input_tokens_estimate'])
                    self.assertEqual(fitted['messages'][-1]['content'],history[-1]['content'])
                    self.assertEqual(original,before);self.assertTrue(stats['compressed'])

    def test_subagent_tools_remain_discoverable_and_preferred_when_requested(self):
        """A Russian capability question can discover the enabled child tools after schema pruning."""
        from agent.child_executor import CHILD_TOOL
        from agent.subagent_profiles import CREATE_TOOL
        definitions=[CHILD_TOOL,CREATE_TOOL]
        catalog={d['function']['name']:{'definition':d,'label':d['function']['name']} for d in definitions}
        self.assertEqual(set(find_mcp_tools(catalog,'субагент')),{'delegate_readonly','create_subagent_profile'})
        engine=AgentEngine('http://127.0.0.1:1234/v1','','fixture',str(self.root),'Можешь создать субагента?',
            tool_definitions=definitions,auto_memory=False,context_builder=False)
        self.assertEqual(engine.budget.preferred_tools,{'delegate_readonly','create_subagent_profile'})
        disabled=AgentEngine('http://127.0.0.1:1234/v1','','fixture','','Можешь создать субагента?',
            tool_definitions=[],auto_memory=False)
        self.assertEqual(disabled.budget.preferred_tools,set())

    def test_large_russian_current_request_is_rejected_without_clipping(self):
        text='Измени конкретную функцию и сохрани интерфейс. '*500
        params={'model':'fixture','messages':[{'role':'system','content':'rules'},{'role':'user','content':text}],'max_tokens':512,'stream':True}
        before=copy.deepcopy(params)
        with self.assertRaises(BudgetExceededError):RequestBudget(4096,256).fit(params,protected_text=text)
        self.assertEqual(params,before)

    def test_schemas_and_json_protocol_overhead_are_included(self):
        params={'model':'fixture','messages':[{'role':'system','content':'rules'},{'role':'user','content':'hi'}],
            'tools':[definition(width=100)],'max_tokens':512,'stream':True}
        for protocol in ('native','json'):
            budget=RequestBudget(4096,256)
            with self.assertRaises(BudgetExceededError):budget.fit(params,tool_protocol=protocol)
            self.assertGreater(budget.last_stats['components']['tools'],4096)
            self.assertEqual(budget.last_stats['status'],'blocked')

    def test_responses_encrypted_items_count_and_remain_intact(self):
        call={'id':'c','type':'function','function':{'name':'mcp_test','arguments':'{}'}}
        cache={'c':[{'type':'reasoning','encrypted_content':'encrypted'*1000},
            {'type':'function_call','call_id':'c','name':'mcp_test','arguments':'{}'}]}
        params={'model':'fixture','messages':[{'role':'user','content':'hi'},{'role':'assistant','tool_calls':[call]},
            {'role':'tool','tool_call_id':'c','content':'{"ok":true}'}],'stream':True,'max_tokens':512}
        before=copy.deepcopy(cache)
        with self.assertRaises(BudgetExceededError):RequestBudget(4096,256).fit(params,api_protocol='responses',cache=cache)
        self.assertEqual(cache,before)
        fitted,_=RequestBudget(32768,256).fit(params,api_protocol='responses',cache=cache)
        self.assertIn(cache['c'][0],prepare_model_request(fitted,api_protocol='responses',cache=cache)['input'])

    def test_write_arguments_are_preserved_or_rejected(self):
        arguments=json.dumps({'path':'a.py','content':'print("Привет")\n'*1000})
        params={'model':'fixture','messages':[{'role':'user','content':'Создай файл'},
            {'role':'assistant','tool_calls':[{'id':'write','type':'function','function':{'name':'write_file','arguments':arguments}}]},
            {'role':'tool','tool_call_id':'write','content':'{"ok":true}'}],'stream':True,'max_tokens':512}
        with self.assertRaises(BudgetExceededError):RequestBudget(4096,256).fit(params,protected_text='Создай файл')
        self.assertEqual(params['messages'][1]['tool_calls'][0]['function']['arguments'],arguments)

    def test_result_reader_anchors_survive_two_compaction_passes(self):
        messages=[{'role':'system','content':'Rules'}]
        for i in range(15):messages.extend([{'role':'user','content':str(i)},{'role':'assistant','content':'answer '*100}])
        messages.append({'role':'user','content':'Проверь результат'})
        messages.append({'role':'assistant','tool_calls':[{'id':'cmd','type':'function','function':{'name':'run_project_command','arguments':'{}'}}]})
        source_index=len(messages)-1  # index of following tool in history without system
        full=json.dumps({'ok':False,'exit_code':7,'output':'progress\n'*2000+'FAILED last test'})
        messages.append({'role':'tool','tool_call_id':'cmd','content':full})
        first=ContextManager(12000).build(messages,request_index=31)
        fitted,_=RequestBudget(4096,256).fit({'model':'fixture','messages':first,'max_tokens':512,'stream':True},protected_text='Проверь результат')
        raw=next(m['content'] for m in fitted['messages'] if m.get('role')=='tool')
        reference=json.loads(raw)
        self.assertEqual(reference['source_message_index'],source_index)
        result=read_saved_result(messages[1:],{'message_index':source_index,'call_id':'cmd','offset':0,'limit':6000})
        self.assertEqual(result['content'],full[:6000]);self.assertTrue(result['truncated'])
        wire=prepare_model_request(fitted)
        self.assertNotIn('_source_message_index',json.dumps(wire))

    def test_reader_checks_identity_and_reassembles_character_ranges(self):
        text=json.dumps({'ok':True,'content':'Привет! '*1000},ensure_ascii=False)
        history=[{'role':'tool','tool_call_id':'same','content':'old'},
            {'role':'tool','tool_call_id':'same','content':text}]
        pieces=[];offset=0
        while True:
            part=read_saved_result(history,{'message_index':1,'call_id':'same','offset':offset,'limit':1000})
            pieces.append(part['content'])
            if part['next_offset'] is None:break
            offset=part['next_offset']
        self.assertEqual(''.join(pieces),text)
        self.assertFalse(read_saved_result(history,{'message_index':1,'call_id':'wrong'})['ok'])
        self.assertFalse(read_saved_result(history,{'message_index':20,'call_id':'same'})['ok'])

    def test_deferred_tools_require_discovery_and_are_bounded(self):
        catalog={f'mcp_{i}':{'definition':definition(f'mcp_{i}'),'label':'math add'} for i in range(15)}
        engine=AgentEngine('http://unused.invalid','','fixture','','Объясни',allow_tools=True,tool_definitions=[],deferred_tools=catalog,auto_memory=False)
        self.assertFalse(any(t['function']['name'].startswith('mcp_') for t in engine.tool_definitions))
        self.assertNotIn('mcp_1',engine.executor.policy.definitions)
        rejected=engine.executor.execute({'id':'not-loaded','type':'function','function':{'name':'mcp_1','arguments':'{}'}})
        self.assertEqual(rejected['code'],'INVALID_TOOL_ARGUMENTS')
        found=engine._dispatch_tool('discover_mcp_tools',{'query':'math','limit':3})
        names=[t['name'] for t in found['tools']]
        self.assertEqual(len(names),3);self.assertTrue(all(n in engine.executor.policy.definitions for n in names))
        self.assertNotIn('parameters',json.dumps(found))
        self.assertEqual(find_mcp_tools(catalog,'no-match'),[])

    def test_mcp_only_profile_still_exposes_discovery_without_full_schemas(self):
        from agent import chat_store
        from core.python.task_service import TaskService
        with patch.object(chat_store,'CHAT_DIR',self.root/'chats'),patch.object(chat_store,'INDEX_FILE',self.root/'chats/index.json'):
            service=TaskService(lambda *_:None);self.addCleanup(service.shutdown);service.config['model']='fixture'
            spec=definition('mcp_only')
            snapshot={'definitions':[spec],'external':{'mcp_only':{'server':{'name':'math','confirm':True},'tool':{'name':'add'}}},'hint':''}
            with patch.object(service.extensions,'snapshot',return_value=snapshot),patch.object(AgentEngine,'run'):
                service.start('',{'mode':'chat','prompt':'Посчитай'});service.thread.join(2)
            self.assertTrue(service.engine.allow_tools)
            names={t['function']['name'] for t in service.engine.tool_definitions}
            self.assertIn('discover_mcp_tools',names);self.assertNotIn('mcp_only',names)

    def test_memory_update_defaults_skip_read_only_tasks(self):
        engine=AgentEngine('http://unused.invalid','','fixture','','Объясни',auto_memory=True)
        self.assertFalse(engine._should_update_memory())
        engine._memory_tool_events=[{'tool':'read_file','ok':True}];self.assertFalse(engine._should_update_memory())
        engine._memory_tool_events.append({'tool':'write_file','ok':True});self.assertTrue(engine._should_update_memory())
        engine.settings['memory_updates']='off';self.assertFalse(engine._should_update_memory())
        engine.settings['memory_updates']='always';self.assertTrue(engine._should_update_memory())

    def test_legacy_large_reply_does_not_reset_endpoint_and_new_invalid_window_is_rejected(self):
        with patch.object(model_preferences,'PREFERENCES_FILE',self.root/'prefs.json'):
            model_preferences.PREFERENCES_FILE.write_text(json.dumps({'base_url':'http://127.0.0.1:1234/v1','model':'saved-model','settings':{'max_tokens':32768}}))
            self.assertEqual(model_preferences.load_preferences()['model'],'saved-model')
        with self.assertRaises(ValueError):model_preferences.validate_settings({'budget_mode':'manual','max_tokens':4096,'context_window':4096})


class BudgetTransportTests(unittest.TestCase):
    def setUp(self):
        self.server=ThreadingHTTPServer(('127.0.0.1',0),UsageHandler);self.server.requests=[];self.server.reject_usage=False
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.server.server_close);self.addCleanup(self.server.shutdown)
        self.client=ModelClient(f'http://127.0.0.1:{self.server.server_port}/v1','',threading.Event());self.addCleanup(self.client.close)

    def test_real_transport_rejects_oversized_schemas_before_http(self):
        self.client.budget=RequestBudget(4096,256)
        with self.assertRaises(BudgetExceededError):self.client.create(model='fixture',messages=[{'role':'user','content':'hi'}],tools=[definition(width=100)],max_tokens=512,stream=True)
        self.assertEqual(self.server.requests,[]);self.assertEqual(self.client.request_count,0)

    def test_reported_stream_usage_is_counted_once_per_response(self):
        chunks=list(self.client.create(model='fixture',messages=[{'role':'user','content':'hi'}],max_tokens=512,stream=True))
        self.assertTrue(chunks)
        self.assertEqual(self.client.usage_totals,{'input_tokens':90,'output_tokens':2,'requests_reported':1})
        self.assertTrue(self.server.requests[0]['stream_options']['include_usage'])

    def test_optional_usage_rejection_falls_back_before_stream_only(self):
        self.server.reject_usage=True
        list(self.client.create(model='fixture',messages=[{'role':'user','content':'hi'}],max_tokens=512,stream=True))
        self.assertEqual(len(self.server.requests),2)
        self.assertNotIn('stream_options',self.server.requests[1]);self.assertEqual(self.client.usage_totals['requests_reported'],1)

    def test_engine_budget_pause_preserves_request_and_sends_no_http(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(task_store,'TASK_DIR',Path(directory)/'tasks'):
            prompt='Сохрани весь этот запрос без потерь. '*500
            engine=AgentEngine(str(self.client.client.base_url),'','fixture','',prompt,allow_tools=False,
                task_id='over-budget',auto_memory=False,settings={'budget_mode':'manual','context_window':4096,'max_tokens':512,'context_reserve_tokens':256})
            engine.run();task=engine.task_snapshot()
            self.assertEqual(task['run_state'],'paused');self.assertEqual(task['budget']['status'],'blocked')
            self.assertEqual(engine._messages[-1]['content'],prompt);self.assertEqual(self.server.requests,[])

    def test_read_only_answer_skips_memory_request_and_exposes_reported_usage(self):
        with tempfile.TemporaryDirectory() as directory,patch.object(task_store,'TASK_DIR',Path(directory)/'tasks'):
            engine=AgentEngine(str(self.client.client.base_url),'','fixture',directory,'Объясни ответ',
                allow_tools=False,task_id='memory-economy',auto_memory=True)
            engine.run();task=engine.task_snapshot()
            self.assertEqual(task['status'],'completed');self.assertEqual(len(self.server.requests),1)
            self.assertEqual(task['usage']['input_tokens'],90);self.assertEqual(task['usage']['output_tokens'],2)
            self.assertTrue(task['usage']['reported'])


if __name__=='__main__':unittest.main()
