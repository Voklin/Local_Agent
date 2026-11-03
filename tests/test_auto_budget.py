"""Automatic local context sizing, read-only discovery and pre-stream recovery."""
import asyncio
from copy import deepcopy
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import threading
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock,patch,AsyncMock
import httpx
from openai import BadRequestError
from agent.auto_budget import loaded_profile,discover_profile,context_rejection,LoadedTokenizer,local_endpoint
from agent.request_budget import RequestBudget,BudgetExceededError,prepare_model_request
from agent.model_client import ModelClient
from agent.model_preferences import validate_settings
from agent.tools import TOOL_DEFINITIONS
from agent.context_tools import TOOL_CATALOG


class BudgetHandler(BaseHTTPRequestHandler):
    """Expose loaded metadata and reject exactly one request before SSE starts."""
    def log_message(self,*_args):pass

    def do_GET(self):
        """Only the native loaded-model endpoint succeeds."""
        self.server.gets.append(self.path)
        if self.path!='/api/v1/models':self.send_error(404);return
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        self.wfile.write(json.dumps({'models':[{'type':'llm','key':'fixture','max_context_length':262144,
            'loaded_instances':[{'id':'fixture','config':{'context_length':8192}}]}]}).encode())

    def do_POST(self):
        """The first admitted transport request is rejected; the retry must fit the true slot."""
        body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.posts.append(body)
        if len(self.server.posts)==1:
            self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(b'{"error":{"message":"Model loaded with context length of only 4096 tokens","n_ctx":4096}}');return
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        self.wfile.write(('data: '+json.dumps({'choices':[{'index':0,'delta':{'content':'done'},'finish_reason':'stop'}]})+'\n\ndata: [DONE]\n\n').encode())


class AutoBudgetTests(unittest.TestCase):
    """Keep user prompts intact and never load a real LLM."""
    def server(self):
        """Start a disposable loopback metadata/completion fixture."""
        server=ThreadingHTTPServer(('127.0.0.1',0),BudgetHandler);server.gets=[];server.posts=[]
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        self.addCleanup(worker.join,2);self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        return server,f'http://127.0.0.1:{server.server_port}/v1'

    def test_loaded_context_is_not_training_maximum_or_another_instance(self):
        """Select the actual requested slot, including a custom API instance identifier."""
        data={'models':[{'type':'llm','key':'downloaded','max_context_length':262144,'loaded_instances':[
            {'id':'my-api-id','config':{'context_length':4096}},{'id':'another','config':{'context_length':16384}}]}]}
        self.assertEqual(loaded_profile(data,'my-api-id','lmstudio')['window'],4096)
        self.assertNotIn('window',loaded_profile(data,'unloaded','lmstudio'))
        self.assertTrue(local_endpoint('http://127.0.0.1:1234/v1'));self.assertFalse(local_endpoint('https://api.openai.com/v1'))

    def test_discovery_is_cached_metadata_only(self):
        """Repeated detection uses no generation or model-management endpoint."""
        server,url=self.server();first=asyncio.run(discover_profile(url,'fixture'));count=len(server.gets)
        second=asyncio.run(discover_profile(url,'fixture'))
        self.assertEqual(first['window'],8192);self.assertEqual(first,second)
        self.assertEqual(len(server.gets),count);self.assertEqual(server.posts,[])

    def test_russian_prompt_fits_without_byte_equals_token_false_block(self):
        """A full Russian prompt survives fitting although its UTF-8 bytes exceed the window."""
        prompt='Проверь код функции. '*280
        params={'model':'fixture','messages':[{'role':'user','content':prompt}],'max_tokens':8000,'stream':True}
        before=deepcopy(params);fitted,stats=RequestBudget(8192,512,mode='auto').fit(params,protected_text=prompt)
        self.assertEqual(params,before);self.assertEqual(fitted['messages'][0]['content'],prompt)
        self.assertGreater(stats['wire_bytes'],stats['input_tokens_estimate']);self.assertGreaterEqual(stats['remaining_tokens'],0)
        self.assertLess(fitted['max_tokens'],8000)

    def test_auto_normalizes_irrelevant_manual_settings(self):
        """Bad dormant manual controls cannot prevent saving an automatic profile."""
        settings=validate_settings({'budget_mode':'auto','max_tokens':None,'context_window':1,'max_runtime_minutes':False})
        self.assertEqual(settings['budget_mode'],'auto');self.assertGreater(settings['max_tokens'],64)
        with self.assertRaises(ValueError):validate_settings({'budget_mode':'manual','context_window':4096,'max_tokens':8192})

    def test_auto_provisional_window_does_not_inherit_old_manual_cap(self):
        """Unknown server metadata must not turn a dormant manual 4K field into an auto limit."""
        client=ModelClient('http://unused.invalid/v1','',threading.Event());self.addCleanup(client.close)
        settings={'context_window':4096};budget=RequestBudget(4096,256,mode='auto')
        with patch('agent.auto_budget.discover_profile',new=AsyncMock(return_value={'provider':'unknown','source':'fixture'})):
            client.prepare_budget(settings,'fixture',budget)
        self.assertEqual(budget.window_tokens,32768);self.assertEqual(settings['context_window'],4096)
        self.assertIn('временный',budget.profile['source'])

    def test_schema_catalog_preserves_selected_tool_and_human_request(self):
        """Defer optional schemas rather than trimming the current task or required tool."""
        def tool(name):
            """Build a bulky but valid synthetic schema."""
            return {'type':'function','function':{'name':name,'description':'explanation '*600,'parameters':{'type':'object','properties':{}}}}
        params={'model':'fixture','messages':[{'role':'user','content':'Keep this request'}],
            'tools':[tool(name) for name in ['discover_tools','selected',*[f'extra_{i}' for i in range(15)]]],
            'tool_choice':{'type':'function','function':{'name':'selected'}},'max_tokens':4000}
        budget=RequestBudget(8192,256,mode='auto')
        fitted,stats=budget.fit(params,protected_text='Keep this request')
        self.assertIn('selected',[t['function']['name'] for t in fitted['tools']]);self.assertGreater(stats['tools_deferred'],0)
        self.assertEqual(fitted['messages'][0]['content'],'Keep this request')

    def test_mandatory_prompt_never_disappears_to_claim_fit(self):
        """A physically impossible prompt remains saved and reports a plain error."""
        params={'messages':[{'role':'user','content':'Большой обязательный запрос. '*3000}],'max_tokens':8192}
        original=deepcopy(params)
        with self.assertRaises(BudgetExceededError):RequestBudget(4096,256,mode='auto').fit(params,protected_text=params['messages'][0]['content'])
        self.assertEqual(params,original)

    def test_rejected_pre_stream_request_is_adapted_once_without_replaying_effects(self):
        """A real HTTP context rejection triggers a smaller complete request, not a failed task."""
        server,url=self.server();client=ModelClient(url,'',threading.Event());self.addCleanup(client.close)
        client.budget=RequestBudget(8192,256,mode='auto')
        chunks=list(client.create(model='fixture',messages=[{'role':'user','content':'Preserve me'}],max_tokens=4096,stream=True))
        self.assertEqual(chunks[-1].choices[0].finish_reason,'stop');self.assertEqual(len(server.posts),2)
        self.assertEqual(server.posts[1]['messages'][0]['content'],'Preserve me')
        self.assertLess(server.posts[1]['max_tokens'],server.posts[0]['max_tokens']);self.assertEqual(client.budget.window_tokens,4096)

    def test_error_parser_does_not_treat_unrelated_numbers_as_context(self):
        """Only explicit bounded context metadata permits recovery."""
        response=httpx.Response(400,request=httpx.Request('POST','http://fixture/v1/chat/completions'))
        self.assertEqual(context_rejection(BadRequestError('context length of only 4096 tokens',response=response,body={})),4096)
        self.assertIsNone(context_rejection(BadRequestError('bad temperature 4096',response=response,body={})))

    def test_sdk_uses_only_loaded_handles_and_token_count_is_cached(self):
        """The tokenizer adapter never calls SDK model/load methods."""
        handle=NS(identifier='existing',count_tokens=Mock(return_value=50));client=NS(llm=NS(list_loaded=lambda:[handle],model=Mock(side_effect=AssertionError('must not load'))),close=Mock())
        module=NS(Client=lambda **_:client,set_sync_api_timeout=Mock())
        with patch.dict('sys.modules',{'lmstudio':module}):
            tokenizer=LoadedTokenizer.connect('http://127.0.0.1:1234/v1',['existing'],threading.Event())
        self.assertIsNotNone(tokenizer)
        budget=RequestBudget(8192,mode='auto');budget.configure({'window':8192,'source':'fixture'},tokenizer.count)
        payload=prepare_model_request({'messages':[{'role':'user','content':'hello'}],'max_tokens':1000})
        budget.measure(payload);budget.measure(payload)
        self.assertEqual(handle.count_tokens.call_count,1);client.llm.model.assert_not_called();tokenizer.close();client.close.assert_called_once()

    def test_completed_large_write_is_projected_but_pending_code_is_never_trimmed(self):
        """A 40KB executed code write no longer blocks the next request in a 4K slot."""
        code='const answer = 42;\n'*2500
        call={'id':'written','type':'function','function':{'name':'write_file','arguments':json.dumps({'path':'game.js','content':code,'overwrite':False})}}
        prompt='Создай игру и проверь результат'
        params={'messages':[{'role':'user','content':prompt},{'role':'assistant','tool_calls':[call]},
            {'role':'tool','tool_call_id':'written','content':'{"ok":true,"path":"game.js","bytes_written":47500}'}],'max_tokens':8192}
        original=deepcopy(params);fitted,stats=RequestBudget(4096,256,mode='auto').fit(params,protected_text=prompt)
        self.assertEqual(params,original);self.assertEqual(fitted['messages'][0]['content'],prompt)
        archive=fitted['messages'][1]['content'];self.assertIn('completed_tool_exchange_context_projection',archive)
        self.assertIn('game.js',archive);self.assertIn('bytes_written',archive);self.assertIn('source_tool_call_id',archive)
        self.assertNotIn(code,archive);self.assertEqual(stats['compacted_calls'],1)
        pending={**original,'messages':original['messages'][:-1]}
        with self.assertRaises(BudgetExceededError):RequestBudget(4096,256,mode='auto').fit(pending,protected_text=prompt)
        self.assertEqual(pending['messages'][1]['tool_calls'][0]['function']['arguments'],call['function']['arguments'])

    def test_small_slot_keeps_instructions_and_uses_minimal_tool_catalog(self):
        """A 4K IDE window can defer even core schemas instead of blocking ordinary coding."""
        instructions='Правила проекта обязательны. '*120
        params={'messages':[{'role':'system','content':instructions},{'role':'user','content':'Проверь проект'}],
            'tools':[*deepcopy(TOOL_DEFINITIONS),deepcopy(TOOL_CATALOG)],'max_tokens':8192,'stream':True}
        fitted,stats=RequestBudget(4096,256,mode='auto').fit(params,protected_text='Проверь проект')
        names=[t['function']['name'] for t in fitted['tools']]
        self.assertEqual(fitted['messages'][0]['content'],instructions)
        self.assertIn('discover_tools',names);self.assertLessEqual(len(names),5)
        self.assertGreaterEqual(fitted['max_tokens'],512);self.assertGreater(stats['tools_deferred'],0)


if __name__=='__main__':unittest.main()
