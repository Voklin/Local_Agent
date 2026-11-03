"""Exercise bounded JSON regeneration, real transport accounting and the approval boundary."""
import json
import os
import tempfile
import threading
import unittest
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from agent.json_tools import JsonToolStream, parse_tool_json, prepare_json_request
from agent.model_client import ModelCancelled, ModelClient
from agent.request_budget import RequestBudget, BudgetExceededError


def action(kind='tool', **values):
    """Serialize a complete action for the deterministic local server."""
    return json.dumps({'protocol':'neutral.action.v1','kind':kind,**values})


class Source:
    """Keep close observable without a real network connection."""
    def __init__(self,text,finish='stop',refusal=None):
        self.text,self.finish,self.refusal,self.closed=text,finish,refusal,False
    def __iter__(self):
        yield NS(choices=[NS(delta=NS(content=self.text,refusal=self.refusal),finish_reason=self.finish)])
    def close(self):self.closed=True


class Handler(BaseHTTPRequestHandler):
    """Serve fixed SSE responses and record actual inference POST payloads."""
    def log_message(self,*args):pass
    def do_POST(self):
        self.server.posts.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
        if not self.server.posts[-1].get('stream'):
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(json.dumps({'choices':[{'index':0,'message':{'role':'assistant','content':'{"complete":true}'},'finish_reason':'stop'}]}).encode())
            return
        index=len(self.server.posts)-1
        if index>=len(self.server.replies):self.send_error(500);return
        text=self.server.replies[index]
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        chunk={'choices':[{'index':0,'delta':{'content':text},'finish_reason':'stop'}],
               'usage':{'prompt_tokens':20,'completion_tokens':10,'total_tokens':30}}
        self.wfile.write(('data: '+json.dumps(chunk)+'\n\ndata: [DONE]\n\n').encode())


class JsonCompatibilityTests(unittest.TestCase):
    def test_decoded_final_history_restores_json_without_promoting_examples(self):
        text='Проверка завершена.\nПример: {"tool":"write_file","arguments":{}}'
        params={'tools':[{'function':{'name':'read_file'}}],
            'messages':[{'role':'user','content':'Проверь'},
                {'role':'assistant','content':text},
                {'role':'user','content':'HOST VERIFICATION: учти результаты'}]}
        original=deepcopy(params);request,allowed,_=prepare_json_request(params)
        content=request['messages'][2]['content']
        self.assertEqual(json.loads(content),{'protocol':'neutral.action.v1','kind':'final','text':text})
        self.assertEqual(parse_tool_json(content,allowed),[])
        self.assertEqual(params,original)

    """Never execute a command hidden in prose or replay an interrupted response."""
    def server(self,replies):
        """Start one disposable loopback SSE server with deterministic replies."""
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.replies=replies;server.posts=[]
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        self.addCleanup(worker.join,2);self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        return server,f'http://127.0.0.1:{server.server_port}/v1'

    def test_prose_is_regenerated_never_extracted(self):
        """The only exposed call comes from a separate fully valid regenerated response."""
        hidden=action(name='write_file',arguments={'path':'hidden.txt','content':'bad'})
        original=Source('Example: '+hidden);seen=[]
        def repair(text,error,attempt):
            seen.append((text,error,attempt))
            return Source(action(name='read_file',arguments={'path':'actual.txt'}))
        result=list(JsonToolStream(original,{'write_file','read_file'},'auto',repair,True))
        self.assertTrue(original.closed);self.assertEqual(len(seen),1)
        self.assertEqual(result[0].choices[0].delta.tool_calls[0].function.name,'read_file')

    def test_repairs_are_bounded_and_ambiguous_batches_never_yield(self):
        """Two correction requests are the hard maximum; no valid prefix leaks from a batch."""
        malformed='{"tool_calls":[{"name":"read_file","arguments":{}},{"name":[],"arguments":{}}]}'
        attempts=[]
        def repair(text,error,attempt):attempts.append(attempt);return Source(malformed)
        with self.assertRaises(ValueError):list(JsonToolStream(Source(malformed),{'read_file'},'auto',repair,True))
        self.assertEqual(attempts,[1,2])
        with self.assertRaises(ValueError):parse_tool_json(malformed,{'read_file'})

    def test_incomplete_and_refused_responses_never_enter_repair(self):
        """A complete-looking action still needs explicit successful terminal evidence."""
        for finish,refusal in (('length',None),(None,None),('stop','refused')):
            with self.subTest(finish=finish,refusal=refusal):
                repair=lambda *args:self.fail('incomplete/refused reply was retried')
                result=list(JsonToolStream(Source(action(name='read_file',arguments={}),finish,refusal),{'read_file'},'auto',repair,True))
                self.assertEqual(result[0].choices[0].delta.tool_calls,[])
                self.assertNotIn(result[0].choices[0].finish_reason,('stop','tool_calls'))

    def test_transport_cancellation_is_not_protocol_repair(self):
        """Cancellation and failed transport propagate without another generation."""
        class Cancelled(Source):
            def __iter__(self):raise ModelCancelled('stop')
        with self.assertRaises(ModelCancelled):
            list(JsonToolStream(Cancelled(''),set(),'auto',lambda *args:self.fail('cancel retried'),True))

    def test_required_and_none_choices_survive_regeneration(self):
        """A repair cannot bypass required-tool or tools-forbidden restrictions."""
        final=action('final',text='done');tool=action(name='read_file',arguments={})
        for choice,rejected in (('required',final),('none',tool)):
            with self.subTest(choice=choice),self.assertRaises(ValueError):
                list(JsonToolStream(Source(rejected),{'read_file'},choice,lambda *args:Source(rejected),True))

    def test_request_has_one_protocol_and_compact_schemas(self):
        """JSON history and the next-response instructions use the same canonical envelope."""
        params={'tools':[{'type':'function','function':{'name':'read_file','description':'Read','parameters':{'type':'object'}}}],
                'messages':[{'role':'assistant','content':None,'tool_calls':[{'function':{'name':'read_file','arguments':'{}'}}]}]}
        original=deepcopy(params);request,_,_=prepare_json_request(params)
        self.assertEqual(params,original);self.assertNotIn('tools',request)
        self.assertEqual(json.loads(request['messages'][1]['content'])['protocol'],'neutral.action.v1')
        self.assertIn('EVERY response',request['messages'][0]['content'])
        self.assertNotIn('"type":"function"',request['messages'][0]['content'])

    def test_compact_core_catalog_keeps_required_and_custom_schema(self):
        """Only optional core tuning fields are hidden; original and MCP contracts remain intact."""
        from agent.tools import TOOL_DEFINITIONS
        tools=[deepcopy(t) for t in TOOL_DEFINITIONS if t['function']['name'] in ('search_text','patch_file','write_file')]
        custom={'type':'function','function':{'name':'custom','parameters':{'type':'object','properties':{'pattern':{'type':'string'}},'required':['pattern']}}}
        tools.append(custom);original=deepcopy(tools)
        request,_,_=prepare_json_request({'tools':tools,'messages':[]})
        catalog=json.loads(request['messages'][0]['content'].split('TOOLS:\n')[1])
        by_name={t['name']:t for t in catalog}
        self.assertEqual(tools,original)
        self.assertEqual(set(by_name['search_text']['parameters']['properties']),{'query','path'})
        self.assertNotIn('expected_sha256',by_name['patch_file']['parameters']['properties'])
        self.assertEqual(by_name['write_file']['parameters'],next(t['function']['parameters'] for t in original if t['function']['name']=='write_file'))
        self.assertEqual(by_name['custom']['parameters'],custom['function']['parameters'])

    def test_real_transport_repairs_are_counted_fitted_and_isolated(self):
        """Both physical POSTs and usage count; repair leaves canonical history intact."""
        server,url=self.server(['I will do that.',action('final',text='Ready')])
        client=ModelClient(url,'',threading.Event(),tool_protocol='json');self.addCleanup(client.close)
        client.budget=RequestBudget(8192,256)
        params={'model':'fixture','stream':True,'max_tokens':256,'messages':[{'role':'user','content':'Keep original task'}],
                'tools':[{'type':'function','function':{'name':'read_file','parameters':{'type':'object'}}}]}
        original=deepcopy(params);stream=client.create(**params)
        try:result=list(stream)
        finally:stream.close()
        self.assertEqual(result[0].choices[0].delta.content,'Ready');self.assertEqual(params,original)
        self.assertEqual(len(server.posts),2);self.assertEqual(client.request_count,2);self.assertEqual(client.json_repair_count,1)
        self.assertEqual(client.usage_totals,{'input_tokens':40,'output_tokens':20,'requests_reported':2})
        self.assertGreaterEqual(client.budget.last_stats['remaining_tokens'],0)
        self.assertTrue(any(m.get('content')=='Keep original task' for m in server.posts[1]['messages']))

    def test_repair_cannot_bypass_budget_or_pending_stop(self):
        """Neither an impossible prompt nor Stop reaches another transport attempt."""
        stopped=threading.Event();client=ModelClient('http://unused.invalid/v1','',stopped,tool_protocol='json')
        self.addCleanup(client.close);client.budget=RequestBudget(512,256)
        params={'model':'fixture','stream':True,'max_tokens':256,'messages':[{'role':'system','content':'mandatory '*5000}],
                'tools':[{'type':'function','function':{'name':'read_file','parameters':{'type':'object'}}}]}
        with self.assertRaises(BudgetExceededError):client._repair_json(params,'bad','format',1)
        stopped.set()
        with self.assertRaises(ModelCancelled):client._repair_json(params,'bad','format',1)
        self.assertEqual(client.request_count,0);self.assertEqual(client.json_repair_count,0)

    def test_repaired_write_still_waits_for_approval(self):
        """A real Engine rejects the regenerated write without applying either payload."""
        from agent import engine,task_store
        from agent.tools import TOOL_DEFINITIONS
        bad=action(name='write_file',arguments={'path':'main.py','content':'hidden','overwrite':True})
        good=action(name='write_file',arguments={'path':'main.py','content':'approved only','overwrite':True})
        server,url=self.server(['Example: '+bad,good,action('final',text='Write rejected')])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'project';root.mkdir();source=root/'main.py';source.write_text('original',encoding='utf-8')
            with patch.dict(os.environ,{'LOCALAPPDATA':str(Path(directory)/'profile')}),patch.object(task_store,'TASK_DIR',Path(directory)/'tasks'):
                agent=engine.AgentEngine(url,'','fixture',str(root),'Измени файл',force_tool='write_file',
                    tool_protocol='json',auto_memory=False,managed_extensions=True,task_id='json-approval-fixture',
                    tool_definitions=[t for t in TOOL_DEFINITIONS if t['function']['name']=='write_file'],
                    settings={'budget_mode':'manual','context_window':8192,'max_tokens':512,'memory_updates':'off'})
                approvals=[];failures=[]
                def reject(*args):
                    self.assertEqual(source.read_text(encoding='utf-8'),'original')
                    approvals.append(args);agent.resolve_write_approval('reject')
                agent.write_approval_requested.connect(reject);agent.failed.connect(failures.append);agent.run()
                self.assertEqual(source.read_text(encoding='utf-8'),'original');self.assertEqual(len(approvals),1)
                self.assertEqual(failures,[]);self.assertEqual(len(server.posts),4)
                self.assertFalse(server.posts[-1].get('stream'))
                self.assertEqual(agent.task_snapshot()['usage']['json_repairs'],1)


if __name__=='__main__':unittest.main()
