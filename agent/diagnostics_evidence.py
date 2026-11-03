"""LSP evidence bound to the exact user check, saved file and configured server."""
from copy import deepcopy
import hashlib
import json
from .operation_context import OperationContext
from .verification_evidence import capture_witness

DIAGNOSTICS_TOOL={'type':'function','function':{'name':'run_project_diagnostics','description':'Выполнить только заданную пользователем LSP проверку по check_id. Перед запуском покажет точный сервер и файл. Не заменяет тесты или проверку всего проекта.',
    'parameters':{'type':'object','properties':{'check_id':{'type':'string','maxLength':80}},'required':['check_id'],'additionalProperties':False}}}


def config_digest(settings):
    """Bind evidence to enabled server, argv and language, without trusting model metadata."""
    return hashlib.sha256(json.dumps(settings,sort_keys=True).encode()).hexdigest()


def run_diagnostics(root, task, args, settings, operation, approve):
    """Approve exact server/file, then run existing LSP client and capture before/after witnesses."""
    from .language_diagnostics import diagnose
    check=next((c for c in task['options']['checks'] if c['id']==args.get('check_id') and c.get('kind')=='diagnostics'),None)
    if not check:return {'ok':False,'code':'UNKNOWN_CHECK','error':'Выберите заданную пользователем LSP проверку'}
    if not settings.get('enabled'):return {'ok':False,'code':'LSP_DISABLED','error':'Включите и настройте LSP в дополнительных возможностях IDE'}
    from .workspace_access import WorkspaceAccessPolicy
    WorkspaceAccessPolicy(root).require(check['arguments'][0])
    proposal=json.dumps({'purpose':check['purpose'],'server':settings,'file':check['arguments'][0],'permissions':'Сервер запускается с правами пользователя. Область подтверждения не является ограничением доступа программы.','scope':check['evidence_scope']},ensure_ascii=False,indent=2)
    if not approve('Проверка LSP',proposal,'command'):return {'ok':False,'code':'USER_DENIED','error':'Запуск LSP отклонён'}
    WorkspaceAccessPolicy(root).require(check['arguments'][0])
    scope=check['evidence_scope'];before=capture_witness(root,scope);signature=config_digest(settings)
    if not before.get('complete'):return {'ok':False,'code':'UNVERIFIED_SCOPE','error':'Не удалось подтвердить снимок выбранных файлов'}
    context=OperationContext(min(check['timeout'],settings.get('seconds',check['timeout'])),parent=operation)
    result=diagnose(root,check['arguments'][0],settings,context)
    for path in scope['files']+scope.get('dependencies',[]):WorkspaceAccessPolicy(root).require(path)
    after=capture_witness(root,scope)
    errors=sum(1 for d in result.get('diagnostics',[]) if d.get('severity',1)==1)
    stable=after.get('complete') and before.get('digest')==after.get('digest') and not result.get('stale')
    complete=result.get('complete') is True and not result.get('truncated')
    receipt={'version':2,'kind':'diagnostics','check':deepcopy(check),'config':signature,'scope':scope,'witness':{'before':before,'after':after},
        'rollback_revision':task.get('observed_rollback_revision',0),'complete':complete,'errors':errors}
    return {**result,'ok':bool(stable and complete and not errors),'check_id':check['id'],'verification_receipt':receipt,
        'code':'LSP_ERRORS' if errors else 'LSP_INCOMPLETE' if not complete else 'LSP_STALE' if not stable else 'LSP_CLEAN'}


def assess_diagnostics(task, entry):
    """Fresh hashes and server/check identity are mandatory; push-only quiet is not a clean bill."""
    receipt=entry.get('verification_receipt') or {};scope=receipt.get('scope',{})
    coverage={'kind':'files','project_complete':False,'files':scope.get('files',[]),'dependencies':scope.get('dependencies',[])}
    def verdict(status,summary):return {'status':status,'summary':summary,'coverage':coverage}
    check=next((c for c in task.get('options',{}).get('checks',[]) if c['id']==entry.get('check_id')),None)
    if receipt.get('kind')!='diagnostics' or not check or receipt.get('check')!=check:return verdict('unverified','Нет точного свидетельства заданной LSP проверки.')
    if receipt.get('config')!=config_digest(task.get('diagnostics_config',{})):return verdict('stale','Настройки LSP изменились; повторите диагностику.')
    if receipt.get('rollback_revision')!=task.get('observed_rollback_revision',0):return verdict('stale','После отката диагностику нужно повторить.')
    if not receipt.get('complete'):return verdict('unverified','Сервер не подтвердил полноту диагностики; отсутствие ошибок не доказано.')
    if receipt.get('errors'):return verdict('failed','LSP сообщил ошибки в выбранном файле.')
    before=receipt.get('witness',{}).get('before',{});after=receipt.get('witness',{}).get('after',{})
    from .workspace_access import WorkspaceAccessPolicy
    try:
        for path in scope.get('files',[])+scope.get('dependencies',[]):WorkspaceAccessPolicy(task['project_root']).require(path)
    except (OSError,ValueError):return verdict('stale','Доступ к источнику диагностики отозван.')
    current=capture_witness(task['project_root'],scope)
    if not all(v.get('complete') for v in (before,after,current)) or len({v.get('digest') for v in (before,after,current)})!=1:return verdict('stale','Исходники или зависимости LSP проверки изменились.')
    return verdict('current','Полная диагностика сохранённого файла без ошибок; весь проект не проверялся.')
