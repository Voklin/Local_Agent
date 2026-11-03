"""User-owned IDE constraints and evidence-linked acceptance plans."""
from copy import deepcopy
import hashlib
import json


PLAN_TOOL={'type':'function','function':{'name':'set_task_plan','description':'Сохранить план задачи и дополнительные критерии готовности. Не отмечает их выполненными. check_ids могут ссылаться только на проверки, уже заданные пользователем. Пользовательские критерии сохраняются.',
    'parameters':{'type':'object','properties':{'steps':{'type':'array','minItems':1,'maxItems':12,'items':{'type':'string','minLength':1,'maxLength':300}},
        'criteria':{'type':'array','maxItems':12,'items':{'type':'object','properties':{'description':{'type':'string','minLength':1,'maxLength':500},'check_ids':{'type':'array','maxItems':8,'items':{'type':'string','maxLength':80}}},'required':['description'],'additionalProperties':False}}},'required':['steps','criteria'],'additionalProperties':False}}}


def validate_options(value):
    """Validate before discarding any previous task or starting model/command work."""
    if value is None:value={}
    if not isinstance(value,dict):raise ValueError('Некорректные параметры задачи')
    result={key:value.get(key,False) for key in ('read_only','auto_checks','checks_only')}
    if any(type(flag) is not bool for flag in result.values()):raise ValueError('Флаги задачи должны быть логическими')
    criteria=value.get('criteria',[]);checks=value.get('checks',[])
    if not isinstance(criteria,list) or len(criteria)>12 or any(not isinstance(c,str) or not 1<=len(c.strip())<=500 or '\x00' in c for c in criteria):
        raise ValueError('Критерии: до 12 строк по 500 символов')
    if not isinstance(checks,list) or len(checks)>8:raise ValueError('Допускается до 8 проверок')
    result['criteria']=[c.strip() for c in criteria];result['checks']=[]
    for check in checks:
        if not isinstance(check,dict):raise ValueError('Некорректная проверка')
        identity=check.get('id');purpose=check.get('purpose');program=check.get('program');args=check.get('arguments',[]);cwd=check.get('cwd','.')
        if not isinstance(identity,str) or not 1<=len(identity)<=80 or not all(c.isalnum() or c in '_-' for c in identity):raise ValueError('Некорректный ID проверки')
        if not isinstance(purpose,str) or not 1<=len(purpose.strip())<=300 or '\x00' in purpose:raise ValueError('Укажите назначение проверки: до 300 символов')
        if not isinstance(program,str) or not 1<=len(program.strip())<=2000 or '\x00' in program:raise ValueError('Укажите программу проверки')
        if not isinstance(args,list) or len(args)>100 or any(not isinstance(a,str) or len(a)>8000 or '\x00' in a for a in args):raise ValueError('Аргументы проверки: массив до 100 строк')
        if not isinstance(cwd,str) or not cwd or len(cwd)>1000 or '\x00' in cwd:raise ValueError('Укажите относительную папку проверки')
        timeout=check.get('timeout',60)
        if type(timeout) is not int or not 1<=timeout<=120:raise ValueError('Время проверки: 1–120 секунд')
        from .verification_evidence import normalize_scope
        scope=normalize_scope(check.get('evidence_scope'))
        from .verification_plan import KINDS
        kind=check.get('kind','custom');patterns=check.get('applies_to',[])
        if kind not in KINDS:raise ValueError('Неизвестный тип проверки')
        if not isinstance(patterns,list) or len(patterns)>12 or any(not isinstance(p,str) or len(p)>240 or chr(0) in p for p in patterns):raise ValueError('Укажите шаблоны путей до 240 символов')
        patterns=[p.strip().replace(chr(92),'/') for p in patterns if p.strip()]
        if kind=='diagnostics' and len(args)==1:args=[args[0].strip().replace(chr(92),'/')]
        if not isinstance(patterns,list) or len(patterns)>12 or any(not isinstance(p,str) or not p or len(p)>240 or p.startswith(('/',chr(92))) or ':' in p or '..' in p.replace(chr(92),'/').split('/') for p in patterns):raise ValueError('Укажите относительные шаблоны файлов проверки')
        if kind=='diagnostics' and (program!='lsp' or len(args)!=1 or scope['kind']!='files' or args[0] not in scope['files']):raise ValueError('LSP проверка: программа lsp, один файл и явная файловая область')
        result['checks'].append({'id':identity,'purpose':purpose.strip(),'program':program.strip(),'arguments':args,'cwd':cwd,'timeout':timeout,'evidence_scope':scope})
        if 'kind' in check:result['checks'][-1]['kind']=kind
        if patterns:result['checks'][-1]['applies_to']=patterns
    if len({c['id'] for c in result['checks']})!=len(checks):raise ValueError('ID проверок должны быть уникальны')
    links=value.get('criteria_links',{})
    if not isinstance(links,dict) or any(not isinstance(k,str) or not k.isdigit() or int(k)>=len(criteria) or not isinstance(v,list) or any(identity not in {c['id'] for c in result['checks']} for identity in v) for k,v in links.items()):raise ValueError('Критерий ссылается на неизвестную проверку')
    result['criteria_links']=deepcopy(links)
    if result['read_only'] and (result['auto_checks'] or result['checks_only']):raise ValueError('В режиме только чтения запуск программ отключён')
    if result['checks_only'] and not checks:raise ValueError('Сначала добавьте хотя бы одну проверку')
    return result


def install_contract(task, options):
    """Keep user requirements distinct from model-authored supplementary criteria."""
    task['options']=deepcopy(options)
    task['acceptance']=[{'id':'user_'+str(i),'description':text,'source':'user','check_ids':options.get('criteria_links',{}).get(str(i),[])} for i,text in enumerate(options['criteria'])]
    task['plan_steps']=[]
    task['workspace_generation']=0
    from pathlib import Path
    if task.get('project_root') and Path(task['project_root']).is_dir():
        from .workspace_snapshots import SnapshotStore
        task['observed_rollback_revision']=SnapshotStore(task['project_root'],task['chat_id']).revision()


def set_plan(task,args,source='model'):
    """A model can propose steps and evidence links, never assert success."""
    if source=='model' and task.get('plan_source')=='user':return {'ok':False,'error':'План закреплён пользователем; предложите изменение в ответе или обновляйте состояния шагов'}
    from .task_graph import prepare_steps
    try:nodes=prepare_steps(task,args['steps'],source)
    except (ValueError,KeyError,TypeError) as exc:return {'ok':False,'error':str(exc)[:300]}
    known={c['id'] for c in task.get('options',{}).get('checks',[])}
    if any(identity not in known for c in args['criteria'] for identity in c.get('check_ids',[])):
        return {'ok':False,'error':'check_ids могут ссылаться только на пользовательские проверки'}
    user=[c for c in task.get('acceptance',[]) if c.get('source')=='user']
    previous=task.get('plan_steps',[])
    if source=='model' and any(isinstance(n,dict) and not n.get('advisory') for n in previous) and nodes!=previous and not args.get('reason'):
        return {'ok':False,'error':'Для перепланирования структурированного плана укажите reason'}
    if nodes!=previous:
        task['plan_revision']=task.get('plan_revision',0)+1
        task['plan_changes']=(task.get('plan_changes',[])+[{'revision':task['plan_revision'],'source':source,'reason':args.get('reason','Изменение пользователем' if source=='user' else 'Первый план')[:500],'ids':[n['id'] for n in nodes]}])[-8:]
    task['plan_steps']=nodes;task['plan_schema']=2;task['plan_source']=source
    if source=='user':task.pop('progress_watchdog',None)
    model=[{'id':'model_'+str(i),'description':c['description'],'source':'model','check_ids':c.get('check_ids',[])} for i,c in enumerate(args['criteria'])]
    task['acceptance']=user+model
    return {'ok':True,'steps':task['plan_steps'],'criteria':len(user)+len(model),'note':'Критерии сохранены без отметки выполнения. Их подтверждают проверки или пользователь.'}


def command_key(arguments):
    """Command identity excludes labels but includes exact argv and working folder."""
    value={k:arguments.get(k,'.' if k=='cwd' else None) for k in ('program','arguments','cwd')}
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode('utf8')).hexdigest()


def acceptance_summary(task):
    """Separate uncovered, failed, stale and command-covered criteria without guessing."""
    from .workspace_revision import evidence_matches
    checks=task.get('test_results',[])
    result=[]
    for criterion in task.get('acceptance',[]):
        ids=criterion.get('check_ids',[])
        linked=[next((c for c in reversed(checks) if c.get('check_id')==identity),None) for identity in ids]
        status='unverified'
        if linked and all(c is not None for c in linked):
            if any(not c.get('ok') for c in linked):status='failed'
            elif any(not evidence_matches(task,c) for c in linked):status='stale'
            else:
                scoped=any((c.get('verification_receipt') or {}).get('scope',{}).get('kind')=='files' for c in linked)
                status='scoped_checks_passed' if scoped else 'checks_passed'
        result.append({**criterion,'status':status})
    return result

# Legacy strings remain advisory; structured nodes opt into evidence-linked execution.
from .task_graph import NODE_SCHEMA
PLAN_TOOL['function']['parameters']['properties']['steps']['items']={'oneOf':[{'type':'string','minLength':1,'maxLength':300},NODE_SCHEMA]}
PLAN_TOOL['function']['description']+=' Для исполняемого графа передай steps как объекты id/title/kind/depends_on/affected_files/check_ids; строки остаются предложением без подтверждённого выполнения. Состояния меняет update_task_step по _receipt инструментов.'

PLAN_TOOL['function']['parameters']['properties']['reason']={'type':'string','maxLength':500}
