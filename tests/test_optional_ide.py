"""Opt-in boundaries, real LSP/Git and single-request model research contracts."""
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from agent.operation_context import InferenceGate,OperationContext
from agent.language_diagnostics import diagnose,read_frame,write_frame
from agent.managed_worktrees import ManagedWorktrees,git_path
from agent.container_runner import container_command,run_container
from agent.optional_process import process_env,run_bounded
from agent.readonly_research import research,collect_sources
from core.python.optional_ide_service import DEFAULTS,OptionalIdeService,validate_settings

FIXTURE=Path(__file__).parent/'fixtures/lsp_diagnostics.py'


class ResearchHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.server.requests.append(data)
        if self.server.hold:self.server.release.wait(5)
        payload={'choices':[{'message':{'content':'main.py:1 — найдена точка входа'},'finish_reason':'stop'}],'usage':{'prompt_tokens':60,'completion_tokens':12}}
        raw=json.dumps(payload).encode();self.send_response(200);self.end_headers()
        try:self.wfile.write(raw)
        except (ConnectionError,OSError):pass


class OptionalIdeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name);self.root=self.base/'project';self.root.mkdir()
        (self.root/'main.py').write_text('def main():\n    print("hello")\n',encoding='utf-8')

    def model(self,hold=False):
        server=ThreadingHTTPServer(('127.0.0.1',0),ResearchHandler);server.requests=[];server.hold=hold;server.release=threading.Event()
        threading.Thread(target=server.serve_forever,daemon=True).start();self.addCleanup(server.server_close);self.addCleanup(server.shutdown);self.addCleanup(server.release.set)
        return server,{'base_url':f'http://127.0.0.1:{server.server_port}/v1','api_key':'fixture-only','model':'fixture','settings':{'context_window':32768,'context_reserve_tokens':512}}

    def service(self,config=None):
        from agent.run_registry import RunRegistry
        from agent.inference_scheduler import SCHEDULER
        tasks=SimpleNamespace(lock=threading.RLock(),inference=InferenceGate(),config=config or {},registry=RunRegistry(self.base/'profile'),scheduler=SCHEDULER)
        def idle():
            if tasks.optional.running:raise ValueError('busy')
        tasks.idle=idle;service=OptionalIdeService(tasks,self.base/'optional');tasks.optional=service;self.addCleanup(service.shutdown)
        return service

    def git(self,*args,cwd=None):
        result=subprocess.run([git_path(),*args],cwd=cwd or self.root,capture_output=True,text=True,encoding='utf-8')
        if result.returncode:raise RuntimeError(result.stderr)
        return result.stdout.strip()

    def repository(self):
        self.git('init');self.git('add','.');self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Initial')
        return ManagedWorktrees(self.base/'managed')

    def test_optional_features_default_off_and_require_exact_confirmation(self):
        service=self.service()
        self.assertTrue(all(not v['enabled'] for v in service.catalog()['settings'].values()))
        with self.assertRaises(ValueError):service.start(self.root,{'action':'research','query':'main'},lambda _:None)
        settings=deepcopy(DEFAULTS);settings['worktrees']['enabled']=True;service.configure(settings)
        with self.assertRaises(ValueError):service.start(self.root,{'action':'worktree_create','name':'test','confirmed':'true'},lambda _:None)
        self.assertFalse(service.running)

    def test_optional_settings_reject_shell_fields_and_unbounded_budgets(self):
        settings=deepcopy(DEFAULTS);settings['research']['seconds']=10000
        with self.assertRaises(ValueError):validate_settings(settings)
        settings=deepcopy(DEFAULTS);settings['container']['image']='--privileged'
        with self.assertRaises(ValueError):validate_settings(settings)
        settings=deepcopy(DEFAULTS);settings['lsp']['enabled']=True
        with self.assertRaises(ValueError):validate_settings(settings)
        settings=deepcopy(DEFAULTS);settings['container']['mounts']=['C:/']
        with self.assertRaises(ValueError):validate_settings(settings)

    def test_research_one_request_bounded_sources_no_tools_and_no_secret_excerpt(self):
        server,config=self.model();(self.root/'.env').write_text('main=fixture-secret',encoding='utf-8')
        result=research(self.root,'main',config,OperationContext(5),512)
        self.assertEqual(result['requests'],1);self.assertTrue(result['complete']);self.assertEqual(len(server.requests),1)
        self.assertNotIn('tools',server.requests[0]);self.assertNotIn('fixture-secret',json.dumps(server.requests))
        self.assertLessEqual(result['source_chars'],12000);self.assertLessEqual(len(result['sources']),6)
        self.assertEqual((self.root/'main.py').read_text(),'def main():\n    print("hello")\n')

    def test_research_offline_budget_refuses_before_http(self):
        server,config=self.model();config['settings'].update(context_window=700,budget_mode='manual')
        with self.assertRaises(ValueError):research(self.root,'main',config,OperationContext(5),512)
        self.assertEqual(server.requests,[])

    def test_research_holds_shared_gate_until_cancelled_worker_exits(self):
        server,config=self.model(True);service=self.service(config);settings=deepcopy(DEFAULTS);settings['research']['enabled']=True;service.configure(settings)
        responses=[];service.start(self.root,{'action':'research','query':'main'},responses.append)
        deadline=time.monotonic()+3
        while not server.requests and time.monotonic()<deadline:time.sleep(.01)
        self.assertTrue(server.requests)
        with self.assertRaises(ValueError):service.tasks.inference.begin('task')
        service.cancel();service.thread.join(2)
        self.assertFalse(service.running);self.assertFalse(service.tasks.inference.status()['busy']);self.assertFalse(responses[0]['ok'])

    def test_lsp_real_frames_reports_location_and_refuses_server_edit(self):
        settings={**DEFAULTS['lsp'],'program':sys.executable,'arguments':['-u',str(FIXTURE)],'enabled':True}
        result=diagnose(self.root,'main.py',settings,OperationContext(5))
        self.assertEqual(result['diagnostics'][0]['line'],2);self.assertEqual(result['diagnostics'][0]['column'],3)
        self.assertEqual(result['diagnostics'][0]['message'],'Fixture warning');self.assertFalse(result['stale'])
        self.assertNotIn('UNAUTHORIZED',(self.root/'main.py').read_text())

    def test_lsp_deadline_interrupts_server_that_never_reads_stdin(self):
        settings={**DEFAULTS['lsp'],'program':sys.executable,'arguments':['-u',str(FIXTURE),'--stall']}
        (self.root/'main.py').write_text('x'*200000);started=time.monotonic()
        with self.assertRaises(ValueError):diagnose(self.root,'main.py',settings,OperationContext(.3))
        self.assertLess(time.monotonic()-started,3)

    def test_lsp_frame_limits_and_foreign_paths_are_rejected(self):
        with self.assertRaises(ValueError):read_frame(io.BytesIO(b'Content-Length: 1000001\r\n\r\n'))
        with self.assertRaises(ValueError):read_frame(io.BytesIO(b'Content-Length: 12\r\n\r\n{}'))
        settings={**DEFAULTS['lsp'],'program':sys.executable}
        with self.assertRaises(PermissionError):diagnose(self.root,'../outside.py',settings,OperationContext(1))

    def test_worktree_create_diff_remove_keeps_primary_checkout_unchanged(self):
        manager=self.repository();head=self.git('rev-parse','HEAD');(self.root/'main.py').write_text('manual edit')
        row=manager.create(self.root,'Trial',OperationContext(10))['worktree'];target=Path(row['path'])
        self.assertNotEqual((target/'main.py').read_text(),'manual edit');self.assertEqual(self.git('rev-parse','HEAD'),head)
        self.assertEqual(manager.list(self.root,OperationContext(3))['worktrees'][0]['id'],row['id'])
        self.assertEqual(manager.list(target,OperationContext(3))['worktrees'][0]['id'],row['id'])
        with self.assertRaises(ValueError):manager.remove(target,row['id'],OperationContext(3))
        self.assertEqual(manager.diff(self.root,row['id'],OperationContext(3))['status'],'')
        manager.remove(self.root,row['id'],OperationContext(3));self.assertFalse(target.exists());self.assertEqual((self.root/'main.py').read_text(),'manual edit')

    def test_worktree_refuses_unknown_id_dirty_untracked_and_new_commits(self):
        manager=self.repository();row=manager.create(self.root,'Trial',OperationContext(10))['worktree'];target=Path(row['path'])
        with self.assertRaises(ValueError):manager.get(self.root,'0'*32,OperationContext(3))
        (target/'untracked.txt').write_text('keep')
        with self.assertRaises(ValueError):manager.remove(self.root,row['id'],OperationContext(3))
        (target/'untracked.txt').unlink();(target/'main.py').write_text('new commit')
        self.assertIn('+new commit',manager.diff(self.root,row['id'],OperationContext(3))['diff'])
        self.git('add','.',cwd=target);self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Save',cwd=target)
        with self.assertRaises(ValueError):manager.remove(self.root,row['id'],OperationContext(3))
        self.assertTrue(target.exists())

    def test_worktree_owned_path_cannot_escape_managed_directory(self):
        manager=self.repository();row=manager.create(self.root,'Trial',OperationContext(10))['worktree']
        row['path']=str(self.root)
        with self.assertRaises(ValueError):manager._target(row)

    def test_container_argv_fixed_boundaries_no_network_no_host_write(self):
        command=container_command(self.root,{'program':'node','arguments':['--check','main.js']},DEFAULTS['container'],'fixture')
        for flag in ('--network=none','--read-only','--cap-drop=ALL','--pull=never','--cpus=1','--user=65534:65534'):self.assertIn(flag,command)
        self.assertTrue(command[command.index('--mount')+1].endswith(',readonly'));self.assertNotIn('--privileged',command)
        with self.assertRaises(PermissionError):container_command(self.root,{'program':'node','cwd':'..'},DEFAULTS['container'],'fixture')

    def test_container_denial_never_contacts_docker_and_cancel_cleans_daemon_container(self):
        with patch('agent.container_runner.shutil.which',return_value='docker'),patch('agent.container_runner.run_bounded') as run:
            result=run_container(self.root,{'program':'node'},DEFAULTS['container'],OperationContext(2),lambda *_:False)
            self.assertFalse(result['ok']);run.assert_not_called()
        calls=[]
        def execute(command,*args,**kwargs):
            calls.append(command)
            if command[1]=='info':return {'ok':True,'output':'linux'}
            if command[1]=='image':return {'ok':True,'output':'sha256:fixture'}
            if command[1]=='run':return {'ok':False,'output':'','code':'CANCELLED','error':'cancelled','exit_code':-1}
            return {'ok':True,'output':''}
        with patch('agent.container_runner.shutil.which',return_value='docker'),patch('agent.container_runner.run_bounded',side_effect=execute):
            result=run_container(self.root,{'program':'node'},DEFAULTS['container'],OperationContext(2),lambda *_:True)
        self.assertEqual(result['code'],'CANCELLED');self.assertEqual(calls[-1][1:3],['rm','--force'])
        self.assertEqual(calls[-1][-1],calls[-2][calls[-2].index('--name')+1])

    def test_bounded_process_deadline_kills_child_and_filters_environment(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'fixture-secret','TELEGRAM_BOT_TOKEN':'fixture-secret'}):
            self.assertNotIn('OPENAI_API_KEY',process_env());self.assertNotIn('TELEGRAM_BOT_TOKEN',process_env())
        started=time.monotonic();result=run_bounded([sys.executable,'-c','import time;time.sleep(30)'],self.root,OperationContext(.2))
        self.assertFalse(result['ok']);self.assertLess(time.monotonic()-started,3)
