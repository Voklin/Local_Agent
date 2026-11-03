"""Read-only process lifetime evidence; uncertainty never proves an owner exited."""
import os
from pathlib import Path
import sys


def inspect_process(pid):
    """Return (alive/dead/unknown, lifetime token); never send a Windows signal."""
    if type(pid) is not int or not 0<pid<=0xffffffff:return 'unknown',None
    if os.name=='nt':return _windows_process(pid)
    if sys.platform.startswith('linux'):return _linux_process(pid)
    try:os.kill(pid,0)
    except ProcessLookupError:return 'dead',None
    except (PermissionError,OSError):return 'unknown',None
    return 'alive',None


def _windows_process(pid):
    """Keep one query-only handle while reading creation FILETIME and exit status."""
    import ctypes
    from ctypes import wintypes
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
    kernel.GetProcessTimes.argtypes=[wintypes.HANDLE]+[ctypes.POINTER(wintypes.FILETIME)]*4;kernel.GetProcessTimes.restype=wintypes.BOOL
    kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)];kernel.GetExitCodeProcess.restype=wintypes.BOOL
    kernel.CloseHandle.argtypes=[wintypes.HANDLE];kernel.CloseHandle.restype=wintypes.BOOL
    handle=kernel.OpenProcess(0x1000,False,pid)
    if not handle:return ('dead' if ctypes.get_last_error()==87 else 'unknown'),None
    try:
        created,exited,kernel_time,user_time=(wintypes.FILETIME() for _ in range(4))
        timed=kernel.GetProcessTimes(handle,ctypes.byref(created),ctypes.byref(exited),ctypes.byref(kernel_time),ctypes.byref(user_time))
        code=wintypes.DWORD()
        if not kernel.GetExitCodeProcess(handle,ctypes.byref(code)):return 'unknown',None
        if code.value!=259:return 'dead',None
        token=f'win-filetime:{(created.dwHighDateTime<<32)|created.dwLowDateTime}' if timed else None
        return 'alive',token
    finally:kernel.CloseHandle(handle)


def _linux_process(pid):
    """Combine boot ID and /proc start ticks; comm may contain spaces and parentheses."""
    try:
        fields=(Path('/proc')/str(pid)/'stat').read_text().rsplit(')',1)[1].split()
        if fields[0] in ('Z','X'):return 'dead',None
        started=int(fields[19])
        boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        if not boot:return 'alive',None
        return 'alive',f'linux-start:{boot}:{started}'
    except FileNotFoundError:
        # A restricted /proc may hide an existing PID; confirm disappearance.
        try:os.kill(pid,0)
        except ProcessLookupError:return 'dead',None
        except (PermissionError,OSError):return 'unknown',None
        return 'alive',None
    except (OSError,ValueError,IndexError):return 'unknown',None


def owner_alive(pid):
    """Compatibility boolean: inaccessible owners remain protected from recovery."""
    return inspect_process(pid)[0]!='dead'


def owner_ended(pid,expected_token,inspect=inspect_process):
    """A dead PID or a different comparable lifetime proves the recorded owner ended."""
    state,actual=inspect(pid)
    if state=='dead':return 'owner_exited'
    if state=='alive' and isinstance(expected_token,str) and isinstance(actual,str):
        expected_scheme=expected_token.partition(':')[0]
        if expected_scheme in ('win-filetime','linux-start') and actual.partition(':')[0]==expected_scheme and actual!=expected_token:
            return 'owner_replaced'
    return None
