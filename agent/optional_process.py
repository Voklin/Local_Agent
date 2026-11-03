"""Bounded child lifetime shared by opt-in IDE adapters; never uses a shell."""
import os
import signal
import subprocess
import threading
import time
from .process_job import ProcessJob


def process_env():
    names={'PATH','PATHEXT','SYSTEMROOT','WINDIR','TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','LANG'}
    return {**{k:v for k,v in os.environ.items() if k.upper() in names},'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'}


def stop_process(process,job):
    job.close()
    if os.name!='nt':
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    if process.poll() is None:process.kill()
    try:process.wait(3)
    except subprocess.TimeoutExpired:pass


def run_bounded(command,cwd,context,*,limit=64000,env=None):
    if context.is_set():return {'ok':False,'error':'Операция отменена','code':'CANCELLED','output':'','exit_code':None}
    process=subprocess.Popen(command,cwd=cwd,env=env or process_env(),stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False,
        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),start_new_session=os.name!='nt')
    try:job=ProcessJob(process)
    except Exception:
        process.kill();process.wait(3);process.stdout.close();raise
    raw=bytearray();total=[0];started=time.monotonic();reason=''
    def read():
        try:
            while chunk:=process.stdout.read(4096):
                total[0]+=len(chunk);raw.extend(chunk[:max(0,limit-len(raw))])
        except (OSError,ValueError):pass
    reader=threading.Thread(target=read,daemon=True);reader.start()
    try:
        while process.poll() is None:
            if context.wait(.025):reason='Операция отменена или достигнут предел времени';break
    finally:
        stop_process(process,job);reader.join(2);process.stdout.close()
    return {'ok':process.returncode==0 and not reason,'exit_code':process.returncode,
        'output':raw.decode('utf-8',errors='replace'),'truncated':total[0]>len(raw),
        'elapsed_ms':round((time.monotonic()-started)*1000),**({'error':reason,'code':'CANCELLED'} if reason else {})}
