import json
import threading
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from agent.model_client import ModelClient
from agent.responses_adapter import response_request
from agent.model_probe import probe_model
from agent.model_preferences import validate_preferences


class ResponsesHandler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass

    def do_POST(self):
        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append((self.path,payload))
        if self.server.retry:
            self.server.retry=False;self.send_response(503);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"error":{"message":"temporary","type":"server_error"}}');return
        response={'id':'resp_fixture','object':'response','created_at':0,'status':'completed','model':'fixture','output':[]}
        if not payload.get('stream'):
            response['output']=[{'type':'message','id':'msg_1','role':'assistant','status':'completed','content':[{'type':'output_text','text':'42','annotations':[]}]}]
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps(response).encode());return
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        def event(data):self.wfile.write(('data: '+json.dumps(data)+'\n\n').encode());self.wfile.flush()
        if payload.get('tools') and not any(i.get('type')=='function_call_output' for i in payload['input']):
            item={'type':'function_call','id':'fc_1','call_id':'call_1','name':'calculate','arguments':'','status':'in_progress'}
            event({'type':'response.output_item.added','sequence_number':0,'output_index':1,'item':item})
            event({'type':'response.function_call_arguments.delta','sequence_number':1,'output_index':1,'item_id':'fc_1','delta':'{"expression":"6*7"}'})
            item={**item,'arguments':'{"expression":"6*7"}','status':'completed'}
            event({'type':'response.output_item.done','sequence_number':2,'output_index':1,'item':item})
            response['output']=[{'type':'reasoning','id':'rs_1','summary':[],'encrypted_content':'fixture-encrypted'},item]
        else:
            event({'type':'response.output_text.delta','sequence_number':0,'output_index':0,'content_index':0,'item_id':'msg_1','delta':'42'})
        event({'type':'response.completed','sequence_number':3,'response':response})


class ResponsesAdapterTests(unittest.TestCase):
    def setUp(self):
        self.server=ThreadingHTTPServer(('127.0.0.1',0),ResponsesHandler);self.server.requests=[];self.server.retry=False
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.server.server_close);self.addCleanup(self.server.shutdown)
        self.url=f'http://127.0.0.1:{self.server.server_port}/v1'
        self.client=ModelClient(self.url,'fixture-secret',threading.Event(),api_protocol='responses');self.addCleanup(self.client.close)

    def test_streaming_tools_and_reasoning_are_carried_between_calls(self):
        messages=[{'role':'system','content':'Помощник'},{'role':'user','content':'6*7'}]
        tool={'type':'function','function':{'name':'calculate','description':'Math','parameters':{'type':'object','properties':{'expression':{'type':'string'}},'required':['expression']}}}
        chunks=list(self.client.create(model='fixture',messages=messages,tools=[tool],max_tokens=512,temperature=.2,top_p=1,stream=True))
        calls=[c for chunk in chunks for c in chunk.choices[0].delta.tool_calls]
        self.assertEqual(calls[0].id,'call_1');self.assertEqual(calls[0].function.name,'calculate')
        self.assertEqual(''.join(c.function.arguments or '' for c in calls),'{"expression":"6*7"}')
        messages.extend([{'role':'assistant','content':None,'tool_calls':[{'id':'call_1','type':'function','function':{'name':'calculate','arguments':'{"expression":"6*7"}'}}]},{'role':'tool','tool_call_id':'call_1','content':'{"ok":true,"value":42}'}])
        result=list(self.client.create(model='fixture',messages=messages,tools=[tool],max_tokens=512,stream=True))
        self.assertEqual(''.join(c.choices[0].delta.content or '' for c in result),'42')
        path,request=self.server.requests[-1];self.assertEqual(path,'/v1/responses');self.assertFalse(request['store'])
        self.assertNotIn('temperature',request);self.assertNotIn('messages',request)
        self.assertTrue(any(i.get('encrypted_content')=='fixture-encrypted' for i in request['input']))
        self.assertTrue(any(i.get('type')=='function_call_output' for i in request['input']))

    def test_nonstream_probe_uses_responses_and_retry_is_before_stream(self):
        self.server.retry=True
        chunks=list(self.client.create(model='fixture',messages=[{'role':'user','content':'Hi'}],stream=True))
        self.assertEqual(''.join(c.choices[0].delta.content or '' for c in chunks),'42')
        self.assertEqual(len(self.server.requests),2)
        config=validate_preferences({'base_url':self.url,'api_protocol':'responses','model':'fixture'})
        self.assertEqual(probe_model(config)['text'],'42')
        result=self.client.create(model='fixture',messages=[{'role':'user','content':'Hi'}],stream=False)
        self.assertEqual(result.choices[0].message.content,'42')

    def test_transcript_conversion_does_not_send_unknown_chat_metadata(self):
        request=response_request({'model':'fixture','messages':[{'role':'assistant','content':'Ответ','private_note':'do not send'},{'role':'tool','tool_call_id':'x','content':'result'}]})
        self.assertNotIn('private_note',json.dumps(request));self.assertEqual(request['input'][1]['type'],'function_call_output')

    def test_lola_uses_her_own_responses_protocol_and_tools(self):
        from agent import chat_store,task_store
        from core.python.task_service import TaskService
        from core.python.extension_service import ExtensionService
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(chat_store,'CHAT_DIR',root/'chats'),patch.object(chat_store,'INDEX_FILE',root/'chats/index.json'),patch.object(task_store,'TASK_DIR',root/'tasks'):
                service=TaskService(lambda _:None);self.addCleanup(service.shutdown)
                service.extensions=ExtensionService(root/'extensions')
                service.companion_config={**service.companion_config,**validate_preferences({'base_url':self.url,'model':'fixture','api_protocol':'responses'}),'api_key':'fixture-only'}
                service.start('',{'mode':'voice','prompt':'Сколько будет 6 умножить на 7?'})
                service.thread.join(8)
                self.assertFalse(service.thread.is_alive())
                self.assertEqual(service.chat['messages'][-1]['content'],'42')
                self.assertTrue(all(path=='/v1/responses' for path,_ in self.server.requests))
                self.assertTrue(any(i.get('type')=='function_call_output' for _,r in self.server.requests for i in r['input']))
