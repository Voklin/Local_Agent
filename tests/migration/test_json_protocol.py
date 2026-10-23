"""Exercise JSON-only model calls through real HTTP, file tools and diff approval."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import queue
import tempfile
import threading
import unittest
from unittest.mock import patch

from agent import chat_store, task_store, model_preferences
from agent.engine import AgentEngine
from core.python.task_service import TaskService


class JsonOnlyHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_POST(self):
        request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        if 'tools' in request or any(message.get('role')=='tool' for message in request['messages']):
            self.send_error(400,'Native tools unsupported');return
        if not request.get('stream'):
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(json.dumps({'id':'fixture','object':'chat.completion','model':'coder','choices':[{'index':0,'message':{'role':'assistant','content':'{"complete":true}'},'finish_reason':'stop'}]}).encode());return
        stage=self.server.stage;self.server.stage+=1
        content=[json.dumps({'tool_calls':[{'name':'read_file','arguments':{'path':'source.txt'}}]}),
                 json.dumps({'tool_calls':[{'name':'write_file','arguments':{'path':'result.txt','content':'tested','overwrite':False}}]}),
                 'Готово. Результат инструмента учтён.'][min(stage,2)]
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        for offset in range(0,len(content),13):
            chunk={'id':'fixture','object':'chat.completion.chunk','model':'coder','choices':[{'index':0,'delta':{'content':content[offset:offset+13]},'finish_reason':None}]}
            self.wfile.write(('data: '+json.dumps(chunk)+'\n\n').encode())
        self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()


class JsonProtocolTests(unittest.TestCase):
    def test_json_only_model_uses_same_write_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);project=root/'project';project.mkdir();(project/'source.txt').write_text('input',encoding='utf-8')
            server=ThreadingHTTPServer(('127.0.0.1',0),JsonOnlyHandler);server.requests=[];server.stage=0
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                with patch.object(chat_store,'CHAT_DIR',root/'chats'),patch.object(chat_store,'INDEX_FILE',root/'chats/index.json'),patch.object(task_store,'TASK_DIR',root/'tasks'),patch.object(model_preferences,'PREFERENCES_FILE',root/'preferences.json'):
                    events=queue.Queue();service=TaskService(events.put,engine_factory=lambda **kw:AgentEngine(**{**kw,'auto_memory':False}))
                    try:
                        service.configure({'base_url':f'http://127.0.0.1:{server.server_port}/v1','model':'coder','tool_protocol':'json'})
                        service.start(project,{'prompt':'Прочитай source.txt и запиши result.txt'})
                        while True:
                            event=events.get(timeout=20)
                            self.assertNotEqual(event['event'],'failed',event)
                            if event['event']=='approval':break
                        self.assertFalse((project/'result.txt').exists());self.assertIn('+tested',event['diff'])
                        service.resolve_approval({**event,'decision':'apply'})
                        while True:
                            event=events.get(timeout=20)
                            self.assertNotEqual(event['event'],'failed',event)
                            if event['event']=='task_end':break
                        self.assertEqual((project/'result.txt').read_text(),'tested')
                        self.assertTrue(all('tools' not in request for request in server.requests))
                        self.assertEqual([m['role'] for m in service.chat['messages']].count('tool'),2)
                    finally:service.shutdown()
            finally:server.shutdown();server.server_close();worker.join(2)


if __name__=='__main__':unittest.main()
