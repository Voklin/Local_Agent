"""Short-lived real LSP stdio diagnostics; ignores edits and executable requests."""
import json
import os
import queue
import shutil
import subprocess
import threading
import time
import hashlib
from .security import canonical_root,resolve_allowed_path
from .process_job import ProcessJob
from .optional_process import process_env,stop_process


def read_frame(stream):
    total=0;length=None
    while True:
        line=stream.readline(8193);total+=len(line)
        if not line or total>8192:raise ValueError('Некорректный заголовок LSP')
        if line==b'\r\n':break
        key,_,value=line.partition(b':')
        if key.lower()==b'content-length':length=int(value)
    if length is None or not 0<length<=1_000_000:raise ValueError('Размер LSP frame вне лимита')
    raw=stream.read(length)
    if len(raw)!=length:raise ValueError('Неполный LSP frame')
    value=json.loads(raw)
    if not isinstance(value,dict):raise ValueError('Ожидается JSON-RPC объект')
    return value


def write_frame(stream,value):
    raw=json.dumps({'jsonrpc':'2.0',**value},ensure_ascii=False).encode('utf-8')
    stream.write(b'Content-Length: '+str(len(raw)).encode()+b'\r\n\r\n'+raw);stream.flush()


def normalize_diagnostics(values):
    """Reject malformed evidence instead of turning it into an empty clean report."""
    if not isinstance(values,list):raise ValueError('Некорректный список LSP diagnostics')
    result=[]
    for item in values[:200]:
        if not isinstance(item,dict):raise ValueError('Некорректная LSP diagnostic')
        position=item.get('range',{}).get('start',{})
        if any(type(position.get(k)) is not int or position[k]<0 for k in ('line','character')):
            raise ValueError('Некорректная позиция LSP diagnostic')
        severity=item.get('severity',1)
        if type(severity) is not int or severity not in (1,2,3,4):raise ValueError('Некорректная severity LSP diagnostic')
        result.append({'line':position['line']+1,'column':position['character']+1,
            'severity':severity,'message':str(item.get('message',''))[:2000],'source':str(item.get('source',''))[:100]})
    return result


def diagnose(root,path,settings,context):
    base=canonical_root(root);target=resolve_allowed_path(base,path,must_exist=True)
    if not target.is_file() or target.stat().st_size>256000:raise ValueError('Для диагностики нужен сохранённый UTF-8 файл до 256 КБ')
    before=target.stat();identity=(before.st_ino,before.st_size,before.st_mtime_ns)
    raw=target.read_bytes()
    if len(raw)>256000 or b'\x00' in raw:raise ValueError('Файл слишком большой или бинарный')
    text=raw.decode('utf-8');bundled=os.environ.get('NEUTRAL_NODE_PATH') if settings['program'].lower() in ('node','node.exe') else None
    program=bundled or shutil.which(settings['program']);env=process_env()
    if bundled:env['ELECTRON_RUN_AS_NODE']='1'
    if not program or program.lower().endswith(('.cmd','.bat','.ps1')):raise ValueError('Укажите исполняемый LSP сервер. Для npm-сервера используйте node и путь к его JS CLI.')
    process=subprocess.Popen([program,*settings['arguments']],cwd=base,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
        shell=False,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),start_new_session=os.name!='nt')
    try:job=ProcessJob(process)
    except Exception:
        process.kill();process.wait(3);process.stdin.close();process.stdout.close();raise
    incoming=queue.Queue(maxsize=128);outgoing=queue.Queue(maxsize=16);started=time.monotonic()
    def read():
        try:
            while process.poll() is None:incoming.put(read_frame(process.stdout),timeout=1)
        except Exception:
            try:incoming.put_nowait({'transport_closed':True})
            except queue.Full:pass
    def write():
        try:
            while True:
                message=outgoing.get()
                if message is None:return
                write_frame(process.stdin,message)
        except (BrokenPipeError,OSError,ValueError):pass
    def send(value):
        try:outgoing.put_nowait(value)
        except queue.Full:raise ValueError('Слишком много LSP сообщений')
    reader=threading.Thread(target=read,daemon=True);writer=threading.Thread(target=write,daemon=True)
    reader.start();writer.start();uri=target.as_uri();phase='initialize';diagnostics=None
    pull=False;last_update=0;opened=0;values=[]
    try:
        send({'id':1,'method':'initialize','params':{'processId':None,'rootUri':base.as_uri(),'capabilities':{'textDocument':{'diagnostic':{'relatedDocumentSupport':False},'publishDiagnostics':{'versionSupport':True}}},'workspaceFolders':[{'uri':base.as_uri(),'name':base.name}]}})
        while not context.is_set():
            try:message=incoming.get(timeout=.025)
            except queue.Empty:
                if not pull and diagnostics is not None and time.monotonic()-opened>=1.25 and time.monotonic()-last_update>=.75:break
                continue
            if message.get('transport_closed'):raise ValueError('LSP сервер закрыл соединение до получения диагностики')
            if 'method' in message and 'id' in message:
                # Never service workspace/applyEdit or workspace/executeCommand.
                send({'id':message['id'],'error':{'code':-32601,'message':'Readonly diagnostics client'}});continue
            if message.get('id')==1 and phase=='initialize':
                if 'error' in message:raise ValueError('LSP initialize отклонён сервером')
                send({'method':'initialized','params':{}})
                send({'method':'textDocument/didOpen','params':{'textDocument':{'uri':uri,'languageId':settings['language'],'version':1,'text':text}}});phase='diagnostics';opened=time.monotonic()
                provider=(message.get('result') or {}).get('capabilities',{}).get('diagnosticProvider')
                pull=isinstance(provider,dict)
                if pull:
                    params={'textDocument':{'uri':uri}}
                    if provider.get('identifier'):params['identifier']=provider['identifier']
                    send({'id':3,'method':'textDocument/diagnostic','params':params})
            if phase=='diagnostics' and pull and message.get('id')==3:
                if message.get('error',{}).get('code')==-32601:
                    pull=False;continue
                report=message.get('result') or {}
                if 'error' in message or report.get('kind')!='full':raise ValueError('Не получен полный LSP diagnostic report')
                values=report.get('items');diagnostics=normalize_diagnostics(values);break
            if phase=='diagnostics' and message.get('method')=='textDocument/publishDiagnostics':
                params=message.get('params') or {}
                if params.get('uri')!=uri or params.get('version',1)!=1:continue
                values=params.get('diagnostics')
                diagnostics=normalize_diagnostics(values);last_update=time.monotonic()
        if context.is_set():raise ValueError('Диагностика отменена или достигнут предел ожидания; завершение анализа не подтверждено')
        if diagnostics is None:raise ValueError('Нет publishDiagnostics до отмены/лимита; это не подтверждение отсутствия ошибок')
        after=target.stat();stale=identity!=(after.st_ino,after.st_size,after.st_mtime_ns)
        with target.open('rb') as source:current=source.read(256001)
        stale=stale or hashlib.sha256(raw).digest()!=hashlib.sha256(current).digest()
        return {'ok':True,'path':target.relative_to(base).as_posix(),'diagnostics':diagnostics,'stale':stale,'complete':pull and not stale,
            'notice':'Получен полный ответ сервера для сохранённого файла.' if pull else 'Получен стабилизировавшийся список push-диагностик. Завершение всех анализаторов этим не подтверждается.',
            'truncated':len(values)>200,'elapsed_ms':round((time.monotonic()-started)*1000)}
    finally:
        try:
            send({'method':'textDocument/didClose','params':{'textDocument':{'uri':uri}}})
            send({'id':2,'method':'shutdown','params':None})
            send({'method':'exit'});outgoing.put_nowait(None)
        except (ValueError,queue.Full):pass
        writer.join(.1)
        stop_process(process,job);reader.join(2);writer.join(2);process.stdin.close();process.stdout.close()
