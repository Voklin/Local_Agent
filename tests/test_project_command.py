import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from agent.project_command import run_project_command


class ProjectCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def test_rejected_command_never_executes_and_scope_cannot_escape(self):
        args={'program':sys.executable,'arguments':['-c',"open('proof.txt','w').write('ran')"]}
        result=run_project_command(self.root,args,threading.Event(),lambda *_:False)
        self.assertFalse(result['ok']);self.assertFalse((self.root/'proof.txt').exists())
        with self.assertRaises(ValueError):run_project_command(self.root,{**args,'cwd':'..'},threading.Event(),lambda *_:True)

    def test_success_and_nonzero_exit_are_observable(self):
        proposals=[]
        def approve(*args):proposals.append(args);return True
        result=run_project_command(self.root,{'program':sys.executable,'arguments':['-c',"print('Проверка прошла')"]},threading.Event(),approve)
        self.assertTrue(result['ok'],result);self.assertIn('Проверка прошла',result['output']);self.assertEqual(proposals[0][2],'command')
        result=run_project_command(self.root,{'program':sys.executable,'arguments':['-c','import sys;print("failed");sys.exit(7)']},threading.Event(),approve)
        self.assertFalse(result['ok']);self.assertEqual(result['exit_code'],7)

    def test_replaced_working_directory_after_approval_is_not_executed(self):
        """The approved cwd identity is checked again before a process can start."""
        folder=self.root/'cwd';folder.mkdir()
        def replace(*_args):
            folder.rename(self.root/'original')
            folder.mkdir()
            return True
        result=run_project_command(self.root,{'program':sys.executable,'cwd':'cwd',
            'arguments':['-c',"open('proof.txt','w').write('ran')"]},threading.Event(),replace)
        self.assertFalse(result['ok']);self.assertEqual(result['code'],'WORKSPACE_CHANGED')
        self.assertFalse((folder/'proof.txt').exists())
        self.assertFalse((self.root/'original/proof.txt').exists())

    def test_output_is_bounded_and_cancellation_stops_child(self):
        result=run_project_command(self.root,{'program':sys.executable,'arguments':['-c','print("x"*200000)']},threading.Event(),lambda *_:True)
        self.assertTrue(result['ok']);self.assertTrue(result['truncated']);self.assertLessEqual(len(result['output']),64000)
        stop=threading.Event();timer=threading.Timer(.4,stop.set);timer.start();self.addCleanup(timer.cancel)
        started=time.monotonic();result=run_project_command(self.root,{'program':sys.executable,'arguments':['-c','import time;time.sleep(20)']},stop,lambda *_:True)
        self.assertFalse(result['ok']);self.assertLess(time.monotonic()-started,3)
