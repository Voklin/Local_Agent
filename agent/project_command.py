"""Explicitly approved project commands with bounded output, time and child lifetime."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import threading
import time
from .process_job import ProcessJob

COMMAND_TOOL={'type':'function','function':{'name':'run_project_command','description':'Запустить проверку, тест или сборку в проекте. Нужны включённые команды и отдельное подтверждение пользователя. program — исполняемый файл, arguments — массив; без shell. Для JavaScript доступен встроенный node. Не запрашивай команду, если пользователь уже отклонил её.',
    'parameters':{'type':'object','properties':{'program':{'type':'string'},'arguments':{'type':'array','items':{'type':'string'}},'cwd':{'type':'string','description':'Папка относительно корня проекта, по умолчанию .'},'timeout':{'type':'integer','minimum':1,'maximum':120}},'required':['program','arguments'],'additionalProperties':False}}}


def run_project_command(root,args,interrupted,approve):
    program=args.get('program');arguments=args.get('arguments',[]);timeout=args.get('timeout',60)
    if not isinstance(program,str) or not 1<=len(program)<=2000 or not isinstance(arguments,list) or len(arguments)>100 or any(not isinstance(a,str) or len(a)>8000 or '\x00' in a for a in arguments):raise ValueError('Укажите программу и массив аргументов; максимум 100 аргументов по 8000 символов')
    if type(timeout) is not int or not 1<=timeout<=120:raise ValueError('Время команды: 1–120 секунд')
    if not root:raise ValueError('Для команды сначала выберите папку проекта в IDE')
    base=Path(root).resolve(strict=True);relative=args.get('cwd','.')
    if not isinstance(relative,str):raise ValueError('Папка команды должна быть строкой')
    cwd=(base/relative).resolve()
    try:cwd.relative_to(base)
    except ValueError:raise ValueError('Рабочая папка команды должна находиться внутри проекта')
    if not cwd.is_dir():raise ValueError('Рабочая папка не найдена')
    bundled_node=os.environ.get('NEUTRAL_NODE_PATH') if program.lower() in ('node','node.exe') else None
    resolved=bundled_node or shutil.which(program)
    if not resolved:raise ValueError('Программа не найдена. Node встроен в Neutral; остальные среды разработки нужно установить или указать полным путём.')
    if Path(resolved).suffix.lower() in ('.cmd','.bat','.ps1','.vbs','.js') or Path(resolved).stem.lower() in ('cmd','powershell','pwsh','wscript','cscript','mshta'):
        raise ValueError('Команды выполняются без shell. Для npm используйте node и путь npm-cli.js; скрипты запускайте через соответствующую программу.')
    proposal=json.dumps({'program':resolved,'arguments':arguments,'cwd':str(cwd),'timeout_seconds':timeout},ensure_ascii=False,indent=2)
    if interrupted.is_set() or not approve('Запуск программы в проекте',proposal,'command'):return {'ok':False,'error':'Запуск отклонён пользователем'}
    if interrupted.is_set():return {'ok':False,'error':'Остановлено пользователем'}
    names=('PATH','PATHEXT','SystemRoot','WINDIR','COMSPEC','TEMP','TMP','USERPROFILE','APPDATA','LOCALAPPDATA','HOME','LANG')
    env={k:v for k,v in os.environ.items() if k.upper() in {n.upper() for n in names}}
    env['PYTHONIOENCODING']='utf-8';env['PYTHONUTF8']='1'
    if bundled_node:env['ELECTRON_RUN_AS_NODE']='1'
    process=subprocess.Popen([resolved,*arguments],cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,shell=False,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),start_new_session=os.name!='nt')
    try:job=ProcessJob(process)
    except Exception:
        process.kill();process.wait(3);process.stdout.close();raise
    output=bytearray();total=[0]
    def read():
        try:
            while True:
                chunk=process.stdout.read(4096)
                if not chunk:break
                total[0]+=len(chunk)
                output.extend(chunk[:max(0,64000-len(output))])
        except (OSError,ValueError):pass
    reader=threading.Thread(target=read,daemon=True,name='project-command-output');reader.start()
    started=time.monotonic();reason=''
    try:
        while process.poll() is None:
            if interrupted.wait(.05):reason='Остановлено пользователем';break
            if time.monotonic()-started>=timeout:reason='Достигнут лимит времени команды';break
        if process.poll() is None:process.kill()
        process.wait(3)
    finally:
        job.close()
        if os.name!='nt':
            import signal
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        reader.join(2);process.stdout.close()
    return {'ok':process.returncode==0 and not reason,'exit_code':process.returncode,'output':output.decode('utf-8',errors='replace'),'truncated':total[0]>len(output),'elapsed_ms':round((time.monotonic()-started)*1000),**({'error':reason} if reason else {})}
