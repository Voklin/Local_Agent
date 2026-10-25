import sys
import tempfile
import threading
import time
import unittest
import socket
import subprocess
from pathlib import Path
from core.python.extension_service import ExtensionService
from agent.tools import TOOL_DEFINITIONS
from agent.mcp_client import validate_server
from agent.progress_guard import ProgressGuard


class NeutralExtensionsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.service=ExtensionService(self.temp.name)

    def test_disabled_tools_and_groups_are_enforced_and_snapshot_is_frozen(self):
        before=self.service.snapshot([('project',TOOL_DEFINITIONS)])
        self.service.configure({'kind':'tools','id':'read_file','enabled':False})
        after=self.service.snapshot([('project',TOOL_DEFINITIONS)])
        self.assertIn('read_file',before['allowed']);self.assertNotIn('read_file',after['allowed'])
        self.assertFalse(self.service.execute(after,'read_file',{},threading.Event(),lambda *_:True)['ok'])
        self.service.configure({'kind':'groups','id':'project','enabled':False})
        self.assertNotIn('write_file',self.service.snapshot([('project',TOOL_DEFINITIONS)])['allowed'])

    def test_generated_skill_is_reviewable_draft_and_lazy_loaded_after_enable(self):
        snapshot=self.service.snapshot([])
        result=self.service.execute(snapshot,'create_skill',{'title':'Проверка сайта','summary':'Проверка формы','content':'Проверьте форму, затем проверьте успешный ответ сервера.'},threading.Event(),lambda *_:True)
        self.assertEqual(result['status'],'draft')
        self.assertNotIn(result['id'],{s['id'] for s in self.service.snapshot([])['skills']})
        self.service.configure({'kind':'skills','id':result['id'],'enabled':True})
        enabled=self.service.snapshot([])
        self.assertNotIn('успешный ответ сервера',enabled['hint'])
        self.assertIn('успешный ответ сервера',self.service.execute(enabled,'skill_view',{'id':result['id']},threading.Event(),lambda *_:True)['content'])
        persisted=ExtensionService(self.temp.name)
        self.assertTrue(next(s for s in persisted.skills() if s['id']==result['id'])['enabled'])

    def test_learning_toggle_and_plugin_validation(self):
        self.service.configure({'kind':'learn','enabled':False})
        self.assertNotIn('create_skill',self.service.snapshot([])['allowed'])
        with self.assertRaises(ValueError):self.service.import_plugin({'version':1,'name':'bad','tools':['run_arbitrary_shell']})
        result=self.service.import_plugin({'version':1,'name':'Проверка','skills':[{'title':'Проверка','summary':'Поиск ошибки','content':'Сначала воспроизведите ошибку и сохраните результат.'}]})
        plugin=result['plugins'][0];self.assertFalse(plugin['enabled'])
        self.service.configure({'kind':'plugin_toggle','id':plugin['id'],'enabled':True})
        self.assertIn(plugin['skills'][0],{s['id'] for s in self.service.snapshot([])['skills']})

    def test_mcp_stdio_discovery_call_confirmation_and_cancellation(self):
        fixture=str(Path(__file__).parent/'fixtures/mcp_echo.py')
        self.service.configure({'kind':'server_save','server':{'id':'echo','command':sys.executable,'args':[fixture],'enabled':True,'timeout':10}})
        discovered=self.service.discover_server('echo');self.assertTrue(discovered['ok'],discovered)
        snapshot=self.service.snapshot([])
        alias=next(t['id'] for t in discovered['tools'] if t['name']=='add')
        self.assertFalse(self.service.execute(snapshot,alias,{'a':3,'b':4},threading.Event(),lambda *_:False)['ok'])
        self.assertFalse(self.service.execute(snapshot,alias,{'a':'bad','b':4},threading.Event(),lambda *_:True)['ok'])
        result=self.service.execute(snapshot,alias,{'a':3,'b':4},threading.Event(),lambda *_:True)
        self.assertTrue(result['ok'],result);self.assertIn('7',str(result['content']))
        alias=next(t['id'] for t in discovered['tools'] if t['name']=='wait_seconds')
        stop=threading.Event();timer=threading.Timer(.7,stop.set);timer.start();self.addCleanup(timer.cancel)
        started=time.monotonic();result=self.service.execute(snapshot,alias,{'seconds':20},stop,lambda *_:True)
        self.assertFalse(result['ok']);self.assertLess(time.monotonic()-started,4)

    def test_server_url_does_not_store_credentials_and_change_invalidates_tools(self):
        with self.assertRaises(ValueError):validate_server({'id':'x','transport':'http','url':'https://user:secret@example.com/mcp'})
        self.service.configure({'kind':'server_save','server':{'id':'x','transport':'http','url':'http://localhost:9999/mcp'},'token':'test-secret'})
        self.assertNotIn('test-secret',self.service.file.read_text())
        self.service.configure({'kind':'server_save','server':{'id':'x','transport':'http','url':'http://localhost:9998/mcp'}})
        self.assertNotIn('x',self.service.tokens)

    def test_mcp_streamable_http_discovers_and_calls_real_server(self):
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        fixture=str(Path(__file__).parent/'fixtures/mcp_echo.py')
        process=subprocess.Popen([sys.executable,fixture,str(port)],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        self.addCleanup(lambda:process.poll() is None and process.kill())
        started=time.monotonic()
        while time.monotonic()-started<10:
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.2):break
            except OSError:time.sleep(.05)
        self.service.configure({'kind':'server_save','server':{'id':'web','transport':'http','url':f'http://127.0.0.1:{port}/mcp','enabled':True}})
        result=self.service.discover_server('web');self.assertTrue(result['ok'],result)
        snapshot=self.service.snapshot([]);alias=next(t['id'] for t in result['tools'] if t['name']=='add')
        result=self.service.execute(snapshot,alias,{'a':10,'b':20},threading.Event(),lambda *_:True)
        self.assertTrue(result['ok'],result);self.assertIn('30',str(result['content']))
        process.terminate();process.wait(3)

    def test_progress_guard_detects_alternation_but_allows_changing_results(self):
        guard=ProgressGuard()
        for _ in range(3):
            self.assertFalse(guard.observe('read',{'path':'a'},{'ok':True,'text':'a'}))
            self.assertFalse(guard.observe('read',{'path':'b'},{'ok':True,'text':'b'}))
        self.assertTrue(guard.observe('read',{'path':'a'},{'ok':True,'text':'a'}))
        self.assertFalse(guard.observe('read',{'path':'a'},{'ok':True,'text':'updated'}))
