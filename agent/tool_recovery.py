"""Reconcile durable receipts with chat history and bounded UI metadata."""
import json
import uuid

from .call_journal import CallJournal
from .run_state import RunState
from .task_activity import begin_tool, finish_tool, MAX_ACTIVITY
from .tool_executor import ToolPolicy
from .verifier import StageVerifier
from .workspace_edits import record_workspace_change


def task_journal(task):
    task.setdefault('journal_id',uuid.uuid4().hex)
    return CallJournal(task['chat_id'],task['journal_id'])


def _import_legacy(task, messages, journal):
    """Only import incomplete legacy blocks; existing successful histories stay intact."""
    if journal.entries():return
    index=0
    while index<len(messages):
        message=messages[index];calls=message.get('tool_calls') if message.get('role')=='assistant' else None
        if not calls:index+=1;continue
        end=index+1;results={}
        while end<len(messages) and messages[end].get('role')=='tool':
            results[messages[end].get('tool_call_id')]=messages[end];end+=1
        ids=[c.get('id') for c in calls if isinstance(c,dict)]
        if len(ids)!=len(calls) or not all(isinstance(i,str) and i for i in ids) or len(set(ids))!=len(ids):
            index=end;continue
        if set(results)==set(ids):index=end;continue
        journal.prepare_batch(calls,index,message.get('content'))
        for call in calls:
            identity=call['id'];name=call['function']['name']
            if identity in results:
                try:value=json.loads(results[identity]['content'])
                except (ValueError,TypeError):raise ValueError('Прерванный старый tool block содержит нечитаемый результат; исходная история сохранена')
                journal.record_result(index,identity,value)
                continue
            activity=next((e for e in task.get('tool_activity',[]) if e.get('call_id')==identity and e.get('message_index')==index),None)
            pending=task.get('pending_write') or {}
            if not activity and pending.get('call_id')==identity and pending.get('message_index')==index:
                activity=pending
            never_started=activity and (activity.get('status') in ('awaiting_approval','prepared','rejected','cancelled') or
                (name=='write_file' and activity.get('status')=='running'))
            if not never_started:journal.set_phase(index,identity,'started',effectful=ToolPolicy.effectful(name))
        # Repair immediately so later legacy anchor positions include inserted results.
        journal.recover(messages)
        index+=1+len(calls)


def recover_task(task, messages, *, import_legacy=False):
    before=json.dumps(task,sort_keys=True,ensure_ascii=False)
    journal=task_journal(task)
    if import_legacy:_import_legacy(task,messages,journal)
    recovery=journal.recover(messages)
    # Older versions could persist a successful canonical write before saving
    # modified_files, without enough call metadata to build a new journal.
    pending=task.get('pending_write') or {}
    anchor=pending.get('message_index')
    if isinstance(anchor,int) and 0<=anchor<len(messages):
        calls=messages[anchor].get('tool_calls',[])
        if any(c.get('id')==pending.get('call_id') for c in calls):
            for message in messages[anchor+1:]:
                if message.get('role')!='tool':break
                if message.get('tool_call_id')==pending.get('call_id'):
                    try:receipt=json.loads(message.get('content',''))
                    except (ValueError,TypeError):break
                    if isinstance(receipt,dict) and receipt.get('ok') and pending.get('path'):
                        paths=task.setdefault('modified_files',[])
                        if pending['path'] not in paths:paths.append(pending['path'])
                    break
    verifier=StageVerifier()
    entries=journal.entries()
    for position,item in enumerate(entries):
        entry=next((e for e in task.get('tool_activity',[]) if e.get('call_id')==item['call_id'] and e.get('message_index')==item['message_index']),None)
        try:args=json.loads(item['arguments'])
        except (TypeError,ValueError):args={}
        if not entry and position >= len(entries)-MAX_ACTIVITY:
            identity=begin_tool(task,item['name'],args,item['call_id'],item['message_index'])
            entry=next(e for e in task['tool_activity'] if e['id']==identity)
        result=item['result']
        if result is None:
            for message in messages[item['message_index']+1:]:
                if message.get('role')!='tool':break
                if message.get('tool_call_id')==item['call_id']:
                    result=json.loads(message['content']);break
        if result is not None:
            record_workspace_change(task,item['name'],result,item['call_id'],item['message_index'])
            if entry and entry.get('status') in ('running','awaiting_approval','applying','unknown','interrupted','not_executed'):
                finish_tool(task,entry['id'],item['name'],result)
            if item['name']=='run_project_command':verifier.record_command(task,args,result)
            if item['name']=='write_file' and result.get('ok') and isinstance(args,dict):
                paths=task.setdefault('modified_files',[])
                if args.get('path') not in paths:paths.append(args.get('path'))
    from pathlib import Path
    if task.get('project_root') and Path(task['project_root']).is_dir():
        from .workspace_snapshots import SnapshotStore
        store=SnapshotStore(task['project_root'],task['chat_id'],task['journal_id'])
        store.reconcile(entries)
        revision=store.revision()
        if revision>task.get('observed_rollback_revision',revision):
            task['workspace_generation']=task.get('workspace_generation',0)+1
            event=store.rollback_event()
            status=(event or {}).get('status')
            task['workspace_reverted']=status=='rolled_back'
            task['workspace_reviewed']=status=='abandoned'
            note=('Пользователь отменил файловые правки выбранного набора. Предыдущие проверки устарели.' if status=='rolled_back' else 'Пользователь вручную проверил последствия прерванного отката. Автоматический откат этого набора отключён.' if status=='abandoned' else 'Откат файлов был прерван; часть изменений могла отмениться. Требуется ручная проверка, автоматический повтор запрещён.')
            messages.append({'role':'user','content':'[Действие в интерфейсе] '+note+' Для следующих решений проверьте текущее состояние файлов.'})
            task['last_event']=note
        task['observed_rollback_revision']=revision
        task['snapshot_attention']=store.attention()
        verifier.refresh(task)
    task['recovery_items']=[]
    for item in recovery['unresolved']:
        try:args=json.loads(item['arguments'])
        except (TypeError,ValueError):args={}
        task['recovery_items'].append({'message_index':item['message_index'],'call_id':item['call_id'],
            'tool':item['name'],'path':str(args.get('path',''))[:500] if isinstance(args,dict) else '',
            'summary':'Действие могло выполниться. Проверьте файл или внешний сервис и укажите результат.'})
    if recovery['unresolved']:
        RunState(task).transition('needs_attention','Результат действия неизвестен. Проверьте пункты восстановления перед продолжением.')
    task.pop('pending_write',None)
    if not task['recovery_items']:task.pop('recovery_warning',None)
    task.pop('recovery_error',None)
    recovery['changed']=recovery['changed'] or json.dumps(task,sort_keys=True,ensure_ascii=False)!=before
    return recovery
