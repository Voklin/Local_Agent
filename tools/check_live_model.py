"""Opt-in live Chat/IDE/companion check in disposable projects; never approves writes."""
import argparse
import hashlib
import json
import os
import queue
import sys
import tempfile
import time
from pathlib import Path


def fingerprint(root):
    """Хеширует только искусственные исходники, чтобы обнаружить неожиданную запись модели."""
    return {path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob('*') if path.is_file()}


def scenario(service, events, mode, root, timeout):
    """Запускает реальный task flow; все write approvals отклоняет, результат проверяет по событиям/истории."""
    scope=str(root) if mode=='ide' else ''
    prompt=('Прочитай README.md и calculator.py, затем кратко опиши назначение каждого файла. '
            'Ничего не создавай и не изменяй. Обязательно прочитай содержимое обоих файлов инструментом read_file.'
            if mode=='ide' else 'Ответь одной короткой фразой по-русски: сколько будет 6 умножить на 7?')
    before=fingerprint(root)
    if mode=='voice':service.companion_config={**service.companion_config,**service.config}
    service.select_chat(scope,mode=mode)
    service.start(scope,{'mode':mode,'prompt':prompt})
    deadline=time.monotonic()+timeout
    seen=[]
    while time.monotonic()<deadline:
        try:event=events.get(timeout=.2)
        except queue.Empty:continue
        seen.append(event)
        if event['event']=='approval':
            service.resolve_approval({'run_id':event['run_id'],'approval_id':event['approval_id'],'decision':'reject'})
        if event['event']=='task_end':break
    else:
        service.cancel()
        if service.thread:service.thread.join(5)
        raise TimeoutError(f'{mode}: task не завершился за {timeout} секунд')
    task=service.chat.get('task_checkpoint') or {}
    answers=[m['content'] for m in service.chat['messages'] if m.get('role')=='assistant' and isinstance(m.get('content'),str) and m['content'].strip()]
    tools=[m for m in service.chat['messages'] if m.get('role')=='tool']
    calls=[call for m in service.chat['messages'] for call in m.get('tool_calls',[])]
    reads=[]
    for call in calls:
        if call.get('function',{}).get('name')=='read_file':
            try:reads.append(json.loads(call['function']['arguments']).get('path'))
            except (ValueError,KeyError):pass
    unchanged=fingerprint(root)==before
    complete=task.get('status')=='completed' and bool(answers) and unchanged
    if mode=='ide':complete=complete and {'README.md','calculator.py'}.issubset(set(reads))
    else:complete=complete and not calls and not tools
    complete=complete and not any(e['event']=='approval' for e in seen)
    return {'mode':mode,'passed':complete,'status':task.get('status'),'answer':answers[-1] if answers else '',
            'read_paths':reads,'tool_results':len(tools),'source_unchanged':unchanged,
            'errors':[e['text'] for e in seen if e['event']=='failed']}


def main():
    """Изолирует AppData до импорта Core, проверяет выбранную модель без загрузок и записывает JSON-отчёт."""
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:1234/v1')
    parser.add_argument('--model',required=True,help='ID уже загруженной модели; не используйте большой unloaded model')
    parser.add_argument('--scenario',choices=['all','chat','ide','voice'],default='all')
    parser.add_argument('--timeout',type=int,default=120)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    with tempfile.TemporaryDirectory(prefix='localagent-live-') as temporary:
        os.environ['LOCALAPPDATA']=temporary
        from core.python.task_service import TaskService
        root=Path(temporary)/'project';root.mkdir()
        (root/'README.md').write_text('# SmokeCalc\nA small demonstration calculator.\n',encoding='utf-8')
        (root/'calculator.py').write_text('def add(a, b):\n    return a + b\n',encoding='utf-8')
        events=queue.Queue()
        service=TaskService(events.put)
        results=[]
        started=time.monotonic()
        try:
            service.configure({'base_url':args.url,'model':args.model,'settings':{
                'max_tokens':2048,'max_agent_turns':8,'max_runtime_minutes':2,'request_timeout':45,'max_context_chars':16000}})
            for mode in (['chat','ide','voice'] if args.scenario=='all' else [args.scenario]):
                result=scenario(service,events,mode,root.resolve(),args.timeout)
                results.append(result)
                print(json.dumps(result,ensure_ascii=False),flush=True)
        finally:service.shutdown()
        report={'model':args.model,'base_url':args.url,'elapsed_seconds':round(time.monotonic()-started,2),'results':results}
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        if not results or not all(result['passed'] for result in results):raise SystemExit(1)


if __name__=='__main__':
    main()
