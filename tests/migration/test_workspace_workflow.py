"""A real HTTP agent creates folders, patches, renames and deletes with approvals."""
import json
import queue
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from agent import chat_store,task_store,model_preferences
from agent.engine import AgentEngine
from core.python.task_service import TaskService


class WorkspaceHandler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass

    def do_POST(self):
        request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request);self.send_response(200)
        if not request.get('stream'):
            self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(json.dumps({'id':'check','object':'chat.completion','model':'fixture',
                'choices':[{'index':0,'message':{'role':'assistant','content':'{"complete":true}'},'finish_reason':'stop'}]}).encode());return
        receipts=[m for m in request['messages'] if m.get('role')=='tool']
        if receipts and receipts[-1]['tool_call_id']==f'step-{self.server.step}' and json.loads(receipts[-1]['content']).get('ok'):
            self.server.step+=1
        operations=[('create_directory',{'path':'web/js'}),
            ('write_file',{'path':'web/js/game.js','content':'export const answer = 1;\n','overwrite':False}),
            ('read_range',{'path':'web/js/game.js','start_line':1,'end_line':1}),
            ('patch_file',{'path':'web/js/game.js','old_text':'answer = 1','new_text':'answer = 42'}),
            ('rename_file',{'path':'web/js/game.js','destination':'web/js/snake.js'}),
            ('delete_file',{'path':'obsolete.txt'})]
        step=self.server.step
        if step<len(operations):
            name,args=operations[step]
            delta={'tool_calls':[{'index':0,'id':f'step-{step}','type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}
        else:delta={'content':'Готово. Структура создана, функция исправлена, файл перемещён.'}
        self.send_header('Content-Type','text/event-stream');self.end_headers()
        event={'id':'workspace','object':'chat.completion.chunk','model':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if delta.get('tool_calls') else 'stop'}]}
        self.wfile.write(('data: '+json.dumps(event)+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()


class WorkspaceWorkflowTests(unittest.TestCase):
    def test_agent_creates_and_changes_nested_project_through_fresh_approvals(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);project=root/'project';project.mkdir();(project/'web').mkdir()
            (project/'AGENTS.md').write_text('Keep the requested task and file boundaries.',encoding='utf-8')
            (project/'web/AGENTS.md').write_text('Scoped JS policy: use ES modules.',encoding='utf-8')
            (project/'obsolete.txt').write_text('remove this source',encoding='utf-8')
            server=ThreadingHTTPServer(('127.0.0.1',0),WorkspaceHandler);server.requests=[];server.step=0
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                with patch.object(chat_store,'CHAT_DIR',root/'chats'),patch.object(chat_store,'INDEX_FILE',root/'chats/index.json'),patch.object(task_store,'TASK_DIR',root/'tasks'),patch.object(model_preferences,'PREFERENCES_FILE',root/'model.json'):
                    events=queue.Queue();service=TaskService(events.put,engine_factory=lambda **kw:AgentEngine(**{**kw,'auto_memory':False}))
                    try:
                        service.configure({'base_url':f'http://127.0.0.1:{server.server_port}/v1','model':'fixture'})
                        service.start(project,{'mode':'ide','prompt':'Создай вложенный проект, исправь функцию, перемести и удали старый файл'})
                        approvals=[]
                        while True:
                            event=events.get(timeout=20)
                            self.assertNotEqual(event['event'],'failed',event)
                            if event['event']=='approval':
                                approvals.append(event['kind'])
                                if event['kind']=='directory':self.assertFalse((project/'web/js').exists())
                                if event['kind']=='patch':self.assertIn('answer = 1',(project/'web/js/game.js').read_text())
                                if event['kind']=='rename':self.assertFalse((project/'web/js/snake.js').exists())
                                if event['kind']=='delete':self.assertTrue((project/'obsolete.txt').exists())
                                service.resolve_approval({**event,'decision':'apply'})
                            if event['event']=='task_end':break
                        service.thread.join(2)
                        self.assertEqual(approvals,['directory','write','patch','rename','delete'])
                        self.assertEqual((project/'web/js/snake.js').read_bytes(),b'export const answer = 42;\n')
                        self.assertFalse((project/'web/js/game.js').exists());self.assertFalse((project/'obsolete.txt').exists())
                        task=service.chat['task_checkpoint'];self.assertEqual(task['status'],'completed')
                        self.assertEqual(len(task['workspace_changes']),5)
                        self.assertTrue(any('Scoped JS policy' in request['messages'][0]['content'] for request in server.requests if request.get('stream')))
                        receipts=[json.loads(m['content']) for m in service.chat['messages'] if m.get('role')=='tool']
                        self.assertTrue(any(r.get('code')=='PROJECT_INSTRUCTIONS_REQUIRED' for r in receipts))
                    finally:service.shutdown()
            finally:server.shutdown();server.server_close();thread.join(2)
