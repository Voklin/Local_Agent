"""Windows kill-on-close job for a process explicitly created by this application."""
import ctypes
import os
from ctypes import wintypes


class ProcessJob:
    def __init__(self, process):
        self.handle = None
        if os.name != 'nt':
            return
        size = ctypes.c_size_t

        class BasicLimits(ctypes.Structure):
            _fields_ = [('process_time',ctypes.c_int64),('job_time',ctypes.c_int64),('flags',wintypes.DWORD),
                        ('min_working_set',size),('max_working_set',size),('active_processes',wintypes.DWORD),
                        ('affinity',size),('priority',wintypes.DWORD),('scheduling',wintypes.DWORD)]

        class IoCounters(ctypes.Structure):
            _fields_ = [(name,ctypes.c_uint64) for name in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [('basic',BasicLimits),('io',IoCounters),('process_memory',size),('job_memory',size),
                        ('peak_process_memory',size),('peak_job_memory',size)]

        self.kernel = ctypes.WinDLL('kernel32',use_last_error=True)
        self.kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p,wintypes.LPCWSTR]
        self.kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self.kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD]
        self.kernel.SetInformationJobObject.restype = wintypes.BOOL
        self.kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE,wintypes.HANDLE]
        self.kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.kernel.CloseHandle.restype = wintypes.BOOL
        handle = self.kernel.CreateJobObjectW(None,None)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.kernel.SetInformationJobObject(handle,9,ctypes.byref(limits),ctypes.sizeof(limits)) or not self.kernel.AssignProcessToJobObject(handle,wintypes.HANDLE(int(process._handle))):
            error = ctypes.get_last_error()
            self.kernel.CloseHandle(handle)
            raise ctypes.WinError(error)
        self.handle = handle

    def close(self):
        if self.handle:
            self.kernel.CloseHandle(self.handle)
            self.handle = None
