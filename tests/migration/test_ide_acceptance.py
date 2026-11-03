"""Real model HTTP, approved commands, acceptance evidence and guarded undo."""
import json
from pathlib import Path
import queue
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

from agent import chat_store,task_store,model_preferences
from agent.engine import AgentEngine
from core.python.task_service import TaskService


class AcceptanceHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_POST(self):
        request=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        if not request.get('stream'):
            value={'choices':[{'message':{'content':'{"complete":true}'}}]}
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps(value).encode());return
        results=[m for m in request['messages'] if m.get('role')=='tool']
        if self.server.read_only:
            action=None if results else ('write_file',{'path':'forbidden.txt','content':'unsafe','overwrite':False})
        elif not results:action=('set_task_plan',{'steps':['Создать файл','Проверить содержимое'],'criteria':[{'description':'Новый файл содержит код','check_ids':['content']} ]})
        elif not any(m.get('tool_call_id')=='file' for m in results):action=('write_file',{'path':'main.js','content':'const answer = 42;\n','overwrite':False})
        else:action=None
        if action:
            name,args=action
            delta={'tool_calls':[{'index':0,'id':'file' if name=='write_file' else 'plan','type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}
        else:delta={'content':'Результат подготовлен.'}
        chunk={'id':'acceptance','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if delta.get('tool_calls') else 'stop'}]}
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        self.wfile.write(('data: '+json.dumps(chunk)+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()


class IdeAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory();self.addCleanup(self.temporary.cleanup)
        self.base=Path(self.temporary.name);self.root=self.base/'project';self.root.mkdir()
        for module,name,value in ((chat_store,'CHAT_DIR',self.base/'chats'),(task_store,'TASK_DIR',self.base/'tasks'),(model_preferences,'PREFERENCES_FILE',self.base/'models.json')):
            context=patch.object(module,name,value);context.start();self.addCleanup(context.stop)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),AcceptanceHandler);self.server.requests=[];self.server.read_only=False
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.server.server_close);self.addCleanup(self.server.shutdown)
        self.events=queue.Queue();self.service=TaskService(self.events.put,engine_factory=lambda **kwargs:AgentEngine(**{**kwargs,'auto_memory':False}))
        self.addCleanup(self.service.shutdown)
        self.service.configure({'base_url':f'http://127.0.0.1:{self.server.server_port}/v1','model':'fixture'})

    def finish(self):
        approvals=[]
        while True:
            event=self.events.get(timeout=20)
            self.assertNotEqual(event['event'],'failed',event)
            if event['event']=='approval':
                approvals.append(event);self.service.resolve_approval({**event,'decision':'apply'})
            if event['event']=='task_end':break
        self.service.thread.join(2)
        return approvals

    def test_http_plan_auto_check_rollback_and_failed_recheck(self):
        self.service.extensions.state['groups']['commands']=True
        check={'id':'content','purpose':'Проверить код нового файла','program':sys.executable,
            'arguments':['-c',"from pathlib import Path;assert '42' in Path('main.js').read_text()"],'cwd':'.','timeout':10}
        options={'auto_checks':True,'criteria':['Содержимое файла проверено'],'checks':[check],'criteria_links':{'0':['content']}}
        self.service.start(self.root,{'mode':'ide','prompt':'Создай main.js','task_options':options})
        approvals=self.finish();self.assertEqual([p['kind'] for p in approvals],['write','command'])
        self.assertIn(check['purpose'],approvals[-1]['diff'])
        task=self.service.chat['task_checkpoint'];self.assertEqual(task['verification']['status'],'commands_passed')
        self.assertTrue(all(c['status']=='checks_passed' for c in task['acceptance_evidence']))
        params={'chat_id':self.service.chat['id']};groups=self.service.workspace_review.list(self.root,params)['snapshots']
        proposal=self.service.workspace_review.preview(self.root,{**params,'group_id':groups[0]['id']})['proposal']
        result=self.service.workspace_review.apply(self.root,{**params,'proposal_id':proposal['id'],'confirmed':True})
        self.assertTrue(result['ok'],result);self.assertFalse((self.root/'main.js').exists())
        self.assertEqual(result['task']['verification']['status'],'stale')
        self.assertTrue(all(c['status']=='stale' for c in result['task']['acceptance_evidence']))
        requests=len(self.server.requests)
        self.service.start(self.root,{'mode':'ide','task_options':{**options,'checks_only':True}})
        self.assertEqual([p['kind'] for p in self.finish()],['command'])
        self.assertEqual(len(self.server.requests),requests,'Checks must not invoke a model')
        task=self.service.chat['task_checkpoint'];self.assertEqual(task['verification']['status'],'failed')
        self.assertEqual(task['test_results'][0]['exit_code'],1)

    def test_read_only_http_malicious_call_is_not_dispatched(self):
        self.server.read_only=True
        self.service.start(self.root,{'mode':'ide','prompt':'Изучи проект','task_options':{'read_only':True}})
        self.assertEqual(self.finish(),[]);self.assertFalse((self.root/'forbidden.txt').exists())
        receipts=[json.loads(m['content']) for m in self.service.chat['messages'] if m.get('role')=='tool']
        self.assertEqual(receipts[0]['code'],'READ_ONLY')
        for request in self.server.requests:
            names={t['function']['name'] for t in request.get('tools',[])}
            self.assertNotIn('write_file',names);self.assertNotIn('run_project_command',names)

    def test_scoped_check_runs_on_large_project_and_reloads_without_model(self):
        """The real Core/approval flow reports selected-file success, not whole-project coverage."""
        self.service.extensions.state['groups']['commands']=True
        (self.root/'main.py').write_text('print(1)\n',encoding='utf-8')
        (self.root/'large.bin').write_bytes(b'x'*8_000_001)
        check={'id':'syntax','purpose':'Проверка файла','program':sys.executable,
            'arguments':['-c','import ast,pathlib; ast.parse(pathlib.Path("main.py").read_text())'],'cwd':'.','timeout':10,
            'evidence_scope':{'kind':'files','files':['main.py'],'dependencies':[]}}
        self.service.start(self.root,{'mode':'ide','task_options':{'checks_only':True,'checks':[check]}})
        approvals=self.finish();self.assertEqual(len(approvals),1)
        self.assertIn('только выбранные файлы',approvals[0]['diff']);self.assertEqual(self.server.requests,[])
        task=self.service.chat['task_checkpoint'];self.assertEqual(task['verification']['status'],'scoped_passed')
        self.assertFalse(any(stage['status']=='active' for stage in task['stages']))
        self.assertFalse(task['verification']['project_complete'])
        self.assertEqual(task['test_results'][0]['verification_receipt']['version'],2)
        reloaded=self.service.select_chat(self.root,self.service.chat['id'])
        self.assertEqual(reloaded['task']['verification']['status'],'scoped_passed')
