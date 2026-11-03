"""Versioned command evidence: execution, declared coverage and source freshness are distinct."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import PurePosixPath


def now():
    """Return the UTC boundary of command execution, outside user approval wait."""
    return datetime.now(timezone.utc).isoformat()


def normalize_scope(value=None):
    """Accept only workspace or an explicit bounded list of files and dependencies from the UI."""
    if value is None:return {'kind':'workspace'}
    if not isinstance(value,dict):raise ValueError('Некорректная область проверки')
    if value=={'kind':'workspace'}:return dict(value)
    if value.get('kind')!='files' or set(value)-{'kind','files','dependencies'}:raise ValueError('Выберите весь проект или конкретные файлы')
    result={'kind':'files'};seen=set()
    for field in ('files','dependencies'):
        items=value.get(field,[])
        if not isinstance(items,list) or len(items)>128 or (field=='files' and not items):raise ValueError('Укажите от 1 до 128 файлов проверки; зависимостей — до 128')
        result[field]=[]
        for item in items:
            if not isinstance(item,str) or not 1<=len(item)<=1000:raise ValueError('Некорректный путь области проверки')
            path=item.strip().replace('\\','/')
            if not path or path.startswith('/') or any(c in path for c in ':*?<>|"\x00\r\n') or any(p in ('','..','.') for p in path.split('/')):
                raise ValueError('Для проверки нужны относительные пути файлов без масок и переходов ..')
            path=PurePosixPath(path).as_posix()
            key=path.casefold() if os.name=='nt' else path
            if key not in seen:result[field].append(path);seen.add(key)
        result[field].sort()
    return result


def configured_check(task,arguments):
    """Only an exact user-defined command can inherit the user's selected evidence scope."""
    from .task_contract import command_key
    return next((c for c in task.get('options',{}).get('checks',[])
        if c.get('kind')!='diagnostics' and c['id']==arguments.get('check_id') and command_key(c)==command_key(arguments)
        and c.get('timeout',60)==arguments.get('timeout',60)),None)


def command_scope(task,arguments):
    """Model-created commands remain workspace-scoped; models cannot downgrade coverage."""
    check=configured_check(task or {},arguments)
    return normalize_scope(check.get('evidence_scope') if check else None)


def command_digest(arguments,scope):
    """Bind evidence to argv, cwd, timeout and the exact user-declared dependency set."""
    value={key:arguments.get(key,default) for key,default in (('program',None),('arguments',[]),('cwd','.'),('timeout',60))}
    value['scope']=scope
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def capture_witness(root,scope):
    """Capture either the existing full revision or exactly the declared files, never a guessed subset."""
    from .workspace_revision import WorkspaceRevisionService
    from .security import canonical_root
    try:
        identity=str(canonical_root(root));identity=identity.casefold() if os.name=='nt' else identity
        revision=(WorkspaceRevisionService.capture_files(root,scope['files']+scope['dependencies'])
            if scope['kind']=='files' else WorkspaceRevisionService.capture(root))
        return {**revision,'root_id':hashlib.sha256(identity.encode()).hexdigest()}
    except (OSError,ValueError,RuntimeError) as exc:
        return {'complete':False,'digest':None,'error':str(exc)[:200]}


def make_receipt(arguments,scope,before,after,result,*,started_at,rollback_revision=0,generation=0):
    """Store immutable execution facts and both witnesses in the durable tool result."""
    passed=result.get('ok') is True and type(result.get('exit_code')) is int and result['exit_code']==0
    return {'version':2,'command_hash':command_digest(arguments,scope),'scope':deepcopy(scope),
        'execution':{'outcome':'passed' if passed else 'failed' if type(result.get('exit_code')) is int else 'unknown',
            'exit_code':result.get('exit_code'),'started_at':started_at,'finished_at':now(),'elapsed_ms':result.get('elapsed_ms')},
        'witness':{'before':deepcopy(before),'after':deepcopy(after)},
        'rollback_revision':rollback_revision,'generation':generation}


def assess_evidence(task,entry,current_workspace=None):
    """Revalidate coverage/config/content; legacy receipts and incomplete witnesses cannot certify success."""
    if entry.get('kind')=='diagnostics':
        from .diagnostics_evidence import assess_diagnostics
        return assess_diagnostics(task,entry)
    receipt=entry.get('verification_receipt') or {}
    coverage={'kind':'unknown','project_complete':False}
    def verdict(status,summary):return {'status':status,'summary':summary,'coverage':coverage}
    if not isinstance(receipt,dict) or receipt.get('version')!=2:
        return verdict('unverified','Старый результат без versioned witness; повторите проверку.')
    arguments=entry.get('command',{})
    if not isinstance(arguments,dict):return verdict('unverified','Не сохранены параметры команды проверки.')
    try:scope=command_scope(task,arguments)
    except (ValueError,TypeError,KeyError):return verdict('unverified','Область проверки повреждена.')
    coverage={'kind':scope['kind'],'project_complete':False,'files':scope.get('files',[]),'dependencies':scope.get('dependencies',[])}
    if receipt.get('scope')!=scope or receipt.get('command_hash')!=command_digest(arguments,scope):
        return verdict('stale','Параметры или область проверки изменились.')
    witness=receipt.get('witness');execution=receipt.get('execution')
    if not isinstance(witness,dict) or not isinstance(execution,dict):return verdict('unverified','Квитанция проверки повреждена.')
    before=witness.get('before');after=witness.get('after')
    if not isinstance(before,dict) or not isinstance(after,dict):return verdict('unverified','Снимки проверки отсутствуют.')
    if before.get('complete') is not True or after.get('complete') is not True:
        return verdict('unverified','Неполный снимок проверки: '+str(before.get('error') or after.get('error') or 'не удалось сверить файлы'))
    if any(before.get(k)!=after.get(k) for k in ('digest','root_id','scope','version')):
        return verdict('stale','Исходники изменились во время проверки; повторите её.')
    if receipt.get('rollback_revision')!=task.get('observed_rollback_revision',0):
        return verdict('stale','После проверки выполнялся откат; повторите её.')
    if scope['kind']=='workspace' and receipt.get('generation')!=task.get('workspace_generation',0):
        return verdict('stale','После проверки изменялись исходники проекта.')
    current=current_workspace if current_workspace is not None and scope['kind']=='workspace' else capture_witness(task.get('project_root',''),scope)
    if not current.get('complete'):
        return verdict('unverified','Актуальность снимка не подтверждена: '+str(current.get('error','неполная сверка')))
    if any(current.get(k)!=before.get(k) for k in ('digest','root_id','scope','version')):
        return verdict('stale','Файлы проверки или её зависимости изменились.')
    if execution.get('outcome')!='passed' or type(execution.get('exit_code')) is not int or execution['exit_code']!=0:
        return verdict('failed','Команда не завершилась успешно.')
    coverage['project_complete']=scope['kind']=='workspace'
    return verdict('current','Снимок проекта актуален.' if scope['kind']=='workspace' else 'Выбранные файлы и объявленные зависимости актуальны; остальной проект не сверялся.')


def migrate_evidence(task):
    """Lazily mark old checkpoint projections unverified without rewriting journal receipts/history."""
    if not isinstance(task,dict) or 'test_results' not in task:return task
    task['verification_schema']=2
    legacy=False
    for entry in task.get('test_results',[]):
        receipt=entry.get('verification_receipt')
        if entry.get('kind')=='command' and (not isinstance(receipt,dict) or receipt.get('version')!=2):
            entry.update(evidence_status='unverified',evidence_summary='Старый результат без witness; повторите проверку.')
            legacy=True
    if legacy:
        task['verification']={'status':'stale','summary':'Сохранены старые результаты команд без witness. Повторите проверки; история и коды выхода сохранены.'}
        for criterion in task.get('acceptance_evidence',[]):criterion['status']='unverified'
    return task
