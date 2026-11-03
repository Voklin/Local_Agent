"""Actual localhost HTTP attempts/repair/usage and approval-time inference ownership."""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import queue
import tempfile
import threading
import unittest
from unittest.mock import patch
from agent import chat_store,task_store,model_preferences,project_memory
from core.python.task_service import TaskService


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        self.wfile.write(b'{"data":[{"id":"fixture"}]}')

    def do_POST(self):
        payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(payload)
        index=len(self.server.requests)
        if self.server.mode=='repair' and index==1:
            self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(b'{"error":{"message":"unsupported stream_options","type":"invalid_request_error"}}');return
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        delta={'content': 'bad json' if self.server.mode=='repair' and index==2 else json.dumps({'protocol':'neutral.action.v1','kind':'final','text':'Проверка завершена'})}
        if self.server.mode=='approval':
            delta={'tool_calls':[{'index':0,'id':'write','type':'function','function':{'name':'write_file','arguments':'{"path":"new.txt","content":"approved","overwrite":false}'}}]}
        values=[{'id':'fixture','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if self.server.mode=='approval' else 'stop'}]},
            {'id':'fixture','choices':[],'usage':{'prompt_tokens':10,'completion_tokens':3,'total_tokens':13}}]
        self.wfile.write((''.join('data: '+json.dumps(value)+'\n\n' for value in values)+'data: [DONE]\n\n').encode());self.wfile.flush()


class RunControlHttpTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)/'project';self.root.mkdir();profile=Path(temp.name)/'profile'
        for target,name,value in ((task_store,'TASK_DIR',profile/'tasks'),(chat_store,'CHAT_DIR',profile/'chats'),(chat_store,'INDEX_FILE',profile/'chats/index.json'),
            (model_preferences,'PREFERENCES_FILE',profile/'preferences.json'),(project_memory,'MEMORY_DIR',profile/'memory')):
            scope=patch.object(target,name,value);scope.start();self.addCleanup(scope.stop)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);self.server.requests=[];self.server.mode='repair'
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.addCleanup(self.stop_server)
        from core.python import extension_service
        scope=patch.object(extension_service,'APP_DIR',profile);scope.start();self.addCleanup(scope.stop)
        self.events=queue.Queue();self.service=TaskService(self.events.put);self.addCleanup(self.service.shutdown)
        self.service.configure({'base_url':f'http://127.0.0.1:{self.server.server_port}/v1','model':'fixture','tool_protocol':'json','settings':{'memory_updates':'off'}})

    def stop_server(self):
        self.server.shutdown();self.server.server_close();self.thread.join(2)

    def event(self,name):
        while True:
            value=self.events.get(timeout=15)
            if value['event']=='failed':self.fail(value['text'])
            if value['event']==name:return value

    def test_physical_attempts_include_optional_field_retry_and_json_repair_once(self):
        self.service.start(self.root,{'prompt':'Привет','mode':'ide'});self.event('task_end')
        row=self.service.registry.history(self.service.chat['id'])[0];ledger=row['ledger']
        self.assertEqual(len(self.server.requests),3);self.assertEqual(ledger['http_attempts'],3)
        self.assertEqual(ledger['requests_reported'],2);self.assertEqual(ledger['input_tokens'],20);self.assertEqual(ledger['output_tokens'],6)
        self.assertEqual(ledger['active_reserved_tokens'],0);self.assertEqual(row['state'],'completed')
        database=self.service.registry.ready()
        with database.transaction() as c:attempts=[json.loads(r[0]) for r in c.execute('SELECT data FROM inference_attempts')]
        self.assertEqual(sum(a['purpose']=='json_repair' for a in attempts),1)
        self.assertFalse(self.service.scheduler.status()['busy'])

    def test_waiting_write_approval_has_no_generation_lease_and_cancel_preserves_file(self):
        self.server.mode='approval';self.service.config['tool_protocol']='native'
        self.service.start(self.root,{'prompt':'Создай новый файл','mode':'ide'});self.event('approval')
        self.assertEqual(self.service.engine.state.phase,'waiting_approval')
        self.assertFalse(self.service.scheduler.status()['busy'])
        self.service.cancel();self.event('task_end')
        row=self.service.registry.history(self.service.chat['id'])[0]
        self.assertEqual(row['state'],'paused');self.assertEqual(row['ledger']['http_attempts'],1)
        self.assertFalse((self.root/'new.txt').exists());self.assertFalse(self.service.scheduler.status()['busy'])

