"""Real HTTP/SSE, approvals and serial model lifecycle for IDE roles."""
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from agent import task_store, chat_store, project_memory, model_preferences, ide_workflow, ide_coordinator
from agent.ide_workflow import DEFAULT_WORKFLOW, ROLES, resolve_roles, validate_workflow
from agent.model_lifecycle import ModelLifecycle
from core.python.task_service import TaskService


class WorkflowHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def reply(self,data):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path=='/api/tags':self.reply({'models':[{'name':role+':latest'} for role in ROLES]});return
        if self.path=='/api/ps':self.reply({'models':[{'name':role+':latest'} for role in self.server.loaded]});return
        self.reply({'models':[{'type':'llm','key':role,'loaded_instances':[{'id':role+'-instance'}] if role in self.server.loaded else []} for role in (*ROLES,'unrelated')]})

    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.path.endswith('/load') and self.server.stall_load:
            self.server.load_arrived.set();self.connection.settimeout(3)
            try:self.connection.recv(1)
            except (OSError,ConnectionError):pass
            return
        if self.path=='/api/generate':
            model=data['model'].removesuffix(':latest');action='unload' if data.get('keep_alive')==0 else 'load'
            if action=='unload':self.server.loaded.discard(model)
            else:self.server.loaded.add(model)
            self.server.events.append((action,model));self.server.peak=max(self.server.peak,len(self.server.loaded));self.reply({'done':True});return
        if self.path.endswith('/unload'):
            model=data['instance_id'].removesuffix('-instance');self.server.loaded.discard(model);self.server.events.append(('unload',model));self.reply({'instance_id':data['instance_id']});return
        if self.path.endswith('/load'):
            self.server.loaded.add(data['model']);self.server.peak=max(self.server.peak,len(self.server.loaded));self.server.events.append(('load',data['model']))
            self.server.loads.append(data);self.reply({'status':'loaded','instance_id':data['model']+'-instance'});return
        role=data['model'].removesuffix('-instance').removesuffix(':latest');self.server.requests.append(data)
        tools={item['function']['name'] for item in data.get('tools',[])}
        if ('write_file' in tools)!=(role=='builder'):self.server.bad_permissions=True
        completed=any(message['role']=='tool' for message in data['messages'])
        if role=='conductor':delta={'content':'План: сохранить дизайн, создать app.py и проверить его.'}
        elif role=='coder':
            self.server.authors+=1
            target='../escape.py' if self.server.escape else 'app.py'
            delta={'content':json.dumps({'files':[{'path':target,'content':f'print({self.server.authors})\n'}],'notes':'Сохранён дизайн'})}
        elif role=='builder' and not completed:
            delta={'tool_calls':[{'index':0,'id':'write','type':'function','function':{'name':'write_file','arguments':json.dumps({'path':'app.py','content':f'print({self.server.authors})\n','overwrite':True})}}]}
        elif role=='builder':delta={'content':'app.py записан через подтверждение.'}
        elif role=='reviewer' and not completed and not self.server.skip_read:
            delta={'tool_calls':[{'index':0,'id':'read','type':'function','function':{'name':'read_file','arguments':'{"path":"app.py"}'}}]}
        else:
            self.server.reviews+=1
            if self.server.invalid_review:delta={'content':'Всё проверено'}
            else:delta={'content':json.dumps({'verdict':'revise' if self.server.revise_once and self.server.reviews==1 else 'pass','summary':'Проверено чтением и AST','issues':['Исправить код'] if self.server.revise_once and self.server.reviews==1 else []})}
        self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
        chunk={'id':'fixture','object':'chat.completion.chunk','created':0,'model':data['model'],'choices':[{'index':0,'delta':delta,'finish_reason':None}]}
        self.wfile.write(('data: '+json.dumps(chunk)+'\n\ndata: [DONE]\n\n').encode());self.wfile.flush()


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.root=Path(self.directory.name)/'project';self.root.mkdir()
        data=Path(self.directory.name)/'data';data.mkdir()
        self.patches=[patch.object(task_store,'TASK_DIR',data/'tasks'),patch.object(chat_store,'CHAT_DIR',data/'chats'),
            patch.object(project_memory,'MEMORY_DIR',data/'memory'),patch.object(model_preferences,'PREFERENCES_FILE',data/'model.json'),
            patch.object(ide_workflow,'WORKFLOW_FILE',data/'workflow.json'),patch.object(ide_coordinator,'STATE_DIR',data/'handoffs')]
        for item in self.patches:item.start()
        self.server=ThreadingHTTPServer(('127.0.0.1',0),WorkflowHandler)
        self.server.daemon_threads=True;self.server.stall_load=False;self.server.load_arrived=threading.Event()
        for key,value in {'loaded':set(),'events':[],'loads':[],'requests':[],'peak':0,'authors':0,'reviews':0,'bad_permissions':False,'escape':False,'skip_read':False,'revise_once':False,'invalid_review':False}.items():setattr(self.server,key,value)
        self.server_thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.server_thread.start()
        self.events=[];self.approve=True;self.service=TaskService(self.emit)
        self.url=f'http://127.0.0.1:{self.server.server_port}/v1'
        self.service.configure({'base_url':self.url,'model':'conductor','settings':{'max_agent_turns':40}})
        options=deepcopy(DEFAULT_WORKFLOW);options['enabled']=True
        for role in ROLES:options['roles'][role].update(base_url=self.url,model=role)
        self.service.configure_workflow(options);self.service.select_chat(self.root,mode='ide')

    def emit(self,event):
        self.events.append(event)
        if event['event']=='approval':self.service.resolve_approval({'approval_id':event['approval_id'],'run_id':event['run_id'],'decision':'apply' if self.approve else 'reject'})

    def tearDown(self):
        self.service.shutdown();self.server.shutdown();self.server.server_close();self.server_thread.join(2)
        for item in reversed(self.patches):item.stop()
        self.directory.cleanup()

    def run_workflow(self,resume=False):
        self.service.start(self.root,{'mode':'ide','prompt':'Добавь app.py, сохрани заданный дизайн','resume':resume})
        self.service.thread.join(20);self.assertFalse(self.service.thread.is_alive(),'Workflow must finish')
        return self.service.engine.task_snapshot()

    def test_pipeline_real_sse_diff_and_one_resident_model(self):
        result=self.run_workflow()
        self.assertEqual(result['status'],'completed',result.get('stop_reason'))
        self.assertEqual((self.root/'app.py').read_text(),'print(1)\n')
        self.assertEqual(self.server.peak,1);self.assertFalse(self.server.loaded);self.assertFalse(self.server.bad_permissions)
        self.assertEqual(self.server.events,[(action,role) for role in ROLES for action in ('load','unload')])
        self.assertEqual([e['event'] for e in self.events].count('approval'),1)
        self.assertTrue(all(load['context_length']==4096 and load['eval_batch_size']==128 and load['offload_kv_cache_to_gpu'] is False for load in self.server.loads))
        self.assertTrue(any('files' in request['messages'][-1].get('content','') for request in self.server.requests if request['model']=='builder-instance'))
        self.assertTrue(any(test['check']=='Python AST' and test['status']=='passed' for test in result['test_results']))

    def test_rejected_write_does_not_reach_reviewer(self):
        self.approve=False;result=self.run_workflow()
        self.assertEqual(result['status'],'paused');self.assertFalse((self.root/'app.py').exists())
        self.assertNotIn(('load','reviewer'),self.server.events);self.assertFalse(self.server.loaded)

    def test_reviewer_revision_has_bounded_repair_cycle(self):
        self.server.revise_once=True;result=self.run_workflow()
        self.assertEqual(result['status'],'completed',result.get('stop_reason'))
        self.assertEqual(self.server.authors,2);self.assertEqual(self.server.reviews,2)
        self.assertEqual((self.root/'app.py').read_text(),'print(2)\n');self.assertEqual(self.server.peak,1)

    def test_verdict_without_reading_changed_file_cannot_pass(self):
        self.server.skip_read=True;self.service.workflow['repair_passes']=0
        result=self.run_workflow();self.assertEqual(result['status'],'paused')
        self.assertIn('не прочитал',result['stop_reason']);self.assertFalse(self.server.loaded)

    def test_standalone_review_requires_file_evidence(self):
        self.server.skip_read=True;self.service.workflow['mode']='reviewer'
        result=self.run_workflow();self.assertEqual(result['status'],'paused')
        self.assertIn('ни одного файла',result['stop_reason'])

    def test_resume_repeats_only_unfinished_review(self):
        self.server.invalid_review=True;first=self.run_workflow()
        self.assertEqual(first['status'],'paused');self.assertEqual(self.server.authors,1)
        self.server.invalid_review=False;second=self.run_workflow(resume=True)
        self.assertEqual(second['status'],'completed',second.get('stop_reason'));self.assertEqual(self.server.authors,1)
        self.assertEqual([event['event'] for event in self.events].count('approval'),1)

    def test_resume_cannot_silently_switch_workflow_to_single_model(self):
        self.server.invalid_review=True;self.run_workflow();self.service.workflow['enabled']=False
        with self.assertRaisesRegex(ValueError,'Режим IDE изменился'):
            self.service.start(self.root,{'mode':'ide','resume':True})

    def test_author_path_escape_stops_before_builder(self):
        self.server.escape=True;result=self.run_workflow()
        self.assertEqual(result['status'],'paused');self.assertFalse((self.root.parent/'escape.py').exists())
        self.assertNotIn(('load','builder'),self.server.events)

    def test_unrelated_loaded_model_is_not_evicted(self):
        self.server.loaded.add('unrelated');result=self.run_workflow()
        self.assertEqual(result['status'],'paused');self.assertEqual(self.server.loaded,{'unrelated'})
        self.assertEqual(self.server.events,[])

    def test_same_model_is_reused_until_release(self):
        roles=resolve_roles(self.service.workflow,self.service.config)
        lifecycle=ModelLifecycle(roles,threading.Event())
        first=lifecycle.acquire(roles['conductor']);second=lifecycle.acquire(roles['conductor']);self.assertEqual(first,second)
        lifecycle.release();self.assertEqual(self.server.events,[('load','conductor'),('unload','conductor')])

    def test_ollama_pipeline_loads_and_unloads_serially(self):
        for role in ROLES:self.service.workflow['roles'][role]['provider']='ollama'
        result=self.run_workflow();self.assertEqual(result['status'],'completed',result.get('stop_reason'))
        self.assertEqual(self.server.peak,1);self.assertFalse(self.server.loaded)

    def test_cancel_interrupts_stalled_model_load(self):
        self.server.stall_load=True;cancelled=threading.Event();errors=[]
        roles=resolve_roles(self.service.workflow,self.service.config);lifecycle=ModelLifecycle(roles,cancelled)
        def acquire():
            try:lifecycle.acquire(roles['coder'])
            except Exception as exc:errors.append(exc)
        worker=threading.Thread(target=acquire,daemon=True);worker.start();self.assertTrue(self.server.load_arrived.wait(5))
        started=time.monotonic();cancelled.set();worker.join(2)
        self.assertFalse(worker.is_alive());self.assertLess(time.monotonic()-started,2)
        self.assertTrue(errors)

    def test_role_secrets_never_persist_or_leak_to_different_endpoint(self):
        options=deepcopy(self.service.workflow);options['roles']['builder']['api_key']='ROLE_SECRET'
        self.service.configure_workflow(options)
        self.assertNotIn('ROLE_SECRET',ide_workflow.WORKFLOW_FILE.read_text())
        self.assertNotIn('ROLE_SECRET',json.dumps(self.service.workflow_preferences()))
        roles=resolve_roles(self.service.workflow,{**self.service.config,'api_key':'MAIN_SECRET'})
        self.assertEqual(roles['conductor']['api_key'],'MAIN_SECRET')
        options['roles']['builder']['base_url']='http://127.0.0.1:9/v1'
        self.assertEqual(resolve_roles(validate_workflow(options),{**self.service.config,'api_key':'MAIN_SECRET'})['builder']['api_key'],'')

    def test_invalid_configuration_does_not_mutate_saved_roles(self):
        before=ide_workflow.WORKFLOW_FILE.read_bytes();options=deepcopy(self.service.workflow)
        options['roles']['coder']['api_key']=[]
        with self.assertRaises(ValueError):self.service.configure_workflow(options)
        self.assertEqual(ide_workflow.WORKFLOW_FILE.read_bytes(),before)

    def test_chat_mode_never_uses_role_coordinator(self):
        self.service.select_chat('',mode='chat');self.service.start('',{'mode':'chat','prompt':'Привет'})
        self.service.thread.join(10)
        self.assertNotIsInstance(self.service.engine,ide_coordinator.IDECoordinator)
        self.assertEqual(self.server.events,[])


if __name__=='__main__':unittest.main()
