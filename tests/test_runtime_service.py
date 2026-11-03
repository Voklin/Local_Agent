import io
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.model_manager import LocalModel, LocalRuntime
from agent.process_job import ProcessJob
from core.python.runtime_service import RuntimeService


class RuntimeServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.exe = root/'llama-server.exe';self.exe.write_bytes(b'fixture')
        self.model = root/'model.gguf';self.model.write_bytes(b'GGUFfixture')
        self.params={'runtime_path':str(self.exe),'model_path':str(self.model),'ctx_size':512,'gpu_layers':0}
        self.service=RuntimeService()

    def tearDown(self):
        self.service.shutdown();self.temp.cleanup()

    def test_validation_does_not_launch_arbitrary_files(self):
        for params in ({**self.params,'runtime_path':str(self.model)}, {**self.params,'ctx_size':True}, {**self.params,'gpu_layers':300}):
            with self.assertRaises(ValueError): self.service.start(params)
        self.model.write_bytes(b'not gguf')
        with self.assertRaises(ValueError): self.service.start(self.params)
        self.assertEqual(self.service.state,'stopped')

    def test_start_cancel_is_nonblocking_and_cannot_restart_until_worker_finishes(self):
        entered=threading.Event();release=threading.Event()
        def launching(model,**kwargs):
            entered.set();release.wait(2)
            if kwargs['cancelled'].is_set():raise InterruptedError('cancelled')
        with patch.object(self.service.runtime,'start',side_effect=launching):
            result=self.service.start(self.params)
            self.assertEqual(result['state'],'starting');self.assertTrue(entered.wait(1))
            self.assertEqual(self.service.stop()['state'],'stopping')
            self.service.stop()
            with self.assertRaises(ValueError):self.service.start(self.params)
            release.set();self.service.thread.join(2)
            self.assertEqual(self.service.status()['state'],'stopped')

    def test_start_failure_is_visible_without_busy_deadlock(self):
        with patch.object(self.service.runtime,'start',side_effect=RuntimeError('fixture failure')):
            self.service.start(self.params);self.service.thread.join(2)
        result=self.service.status()
        self.assertEqual(result['state'],'error');self.assertIn('fixture failure',result['error'])

    def test_output_drain_is_bounded_even_without_newlines(self):
        class Output:
            stdout=io.BytesIO(b'x'*500_000)
        runtime=LocalRuntime();runtime._drain_output(Output())
        self.assertLessEqual(len(runtime.logs),100)
        self.assertLessEqual(sum(map(len,runtime.logs)),102400)

    def test_readiness_timeout_cleans_only_owned_process(self):
        process=subprocess.Popen([sys.executable,'-c','import time;time.sleep(20)'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        runtime=LocalRuntime(runtime_path=str(self.exe))
        with patch('agent.model_manager.subprocess.Popen',return_value=process),patch.object(runtime,'_healthy',return_value=False):
            with self.assertRaises(TimeoutError):runtime.start(LocalModel(str(self.model),'fixture',8),timeout=0.02)
        self.assertIsNotNone(process.poll());self.assertFalse(runtime.running)
        self.assertIsNone(runtime.process_job)

    @unittest.skipUnless(sys.platform=='win32','Windows job only')
    def test_parent_crash_closes_job_and_terminates_child(self):
        import ctypes
        from ctypes import wintypes
        code="from agent.process_job import ProcessJob;import subprocess,sys,time;p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);job=ProcessJob(p);print(p.pid,flush=True);time.sleep(30)"
        parent=subprocess.Popen([sys.executable,'-u','-c',code],stdout=subprocess.PIPE,text=True)
        parent_job=ProcessJob(parent)
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD];kernel.WaitForSingleObject.restype=wintypes.DWORD
        kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        handle=None
        try:
            child_pid=int(parent.stdout.readline())
            handle=kernel.OpenProcess(0x100000,False,child_pid)
            self.assertTrue(handle)
            parent_job.close();parent.wait(timeout=3)
            self.assertEqual(kernel.WaitForSingleObject(handle,3000),0)
        finally:
            parent_job.close()
            if parent.poll() is None:parent.kill();parent.wait(3)
            parent.stdout.close()
            if handle:kernel.CloseHandle(handle)

    @unittest.skipUnless(sys.platform=='win32','Windows job only')
    def test_windows_job_close_terminates_owned_child(self):
        process=subprocess.Popen([sys.executable,'-c','import time;time.sleep(20)'])
        try:
            job=ProcessJob(process);job.close();process.wait(timeout=3)
            self.assertIsNotNone(process.returncode)
        finally:
            if process.poll() is None:process.kill();process.wait(3)
