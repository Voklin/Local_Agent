"""Miya delegates to a different model and receives the result in her own history."""
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


class DelegationHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_POST(self):
        request=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.models.append(request['model'])
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        if request['model']=='miya-fixture' and not any(m.get('role')=='tool' for m in request['messages']):
            delta={'tool_calls':[{'index':0,'id':'delegate-fixture','type':'function','function':{'name':'delegate_task','arguments':json.dumps({'target':'chat','prompt':'Ответь основной моделью'})}}]}
        else:delta={'content':'Передала задачу.' if request['model']=='miya-fixture' else 'MAIN_MODEL_RESULT'}
        chunk={'id':'fixture','object':'chat.completion.chunk','model':request['model'],'choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if delta.get('tool_calls') else 'stop'}]}
        self.wfile.write(('data: '+json.dumps(chunk)+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()


class DelegationTests(unittest.TestCase):
    def test_independent_model_delegates_and_returns_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);server=ThreadingHTTPServer(('127.0.0.1',0),DelegationHandler);server.models=[]
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                with patch.object(chat_store,'CHAT_DIR',root/'chats'),patch.object(chat_store,'INDEX_FILE',root/'chats/index.json'),patch.object(task_store,'TASK_DIR',root/'tasks'),patch.object(model_preferences,'PREFERENCES_FILE',root/'model.json'):
                    events=queue.Queue();service=TaskService(events.put,engine_factory=lambda **kw:AgentEngine(**{**kw,'auto_memory':False}))
                    try:
                        url=f'http://127.0.0.1:{server.server_port}/v1'
                        service.configure({'base_url':url,'model':'main-fixture'})
                        service.companion_config={**service.companion_config,'base_url':url,'model':'miya-fixture'}
                        service.start('',{'mode':'voice','prompt':'Объясни код Python и исправь ошибку'})
                        source=service.chat['id'];pending=None
                        while True:
                            event=events.get(timeout=15);self.assertNotEqual(event['event'],'failed',event)
                            if event['event']=='handoff':pending=event['handoff']
                            if event['event']=='task_end':break
                        self.assertIsNotNone(pending);self.assertEqual(service.config['model'],'main-fixture')
                        selected=service.prepare_handoff(None,{'id':pending['id']})
                        service.start('',{'mode':'chat','prompt':selected['handoff']['prompt']})
                        while True:
                            event=events.get(timeout=15);self.assertNotEqual(event['event'],'failed',event)
                            if event['event']=='task_end':break
                        original=chat_store.load_chat(source)
                        self.assertEqual(original['mode'],'voice');self.assertIn('MAIN MODEL RESULT',original['messages'][-1]['content'])
                        self.assertEqual(server.models,['miya-fixture','miya-fixture','main-fixture'])
                        self.assertNotEqual(service.chat['id'],source)
                    finally:service.shutdown()
            finally:server.shutdown();server.server_close();thread.join(2)


if __name__=='__main__':unittest.main()
