"""Evidence-linked evolution of canonical plan_steps, not a second task plan."""
from copy import deepcopy
import hashlib
import json
import time
from .task_store import _now
from .verification_evidence import normalize_scope
from .workspace_access import WorkspaceAccessPolicy
from .project_index_policy import IndexPolicy

NODE_SCHEMA={'type':'object','properties':{'id':{'type':'string','pattern':'^[A-Za-z0-9_-]{1,60}$'},'title':{'type':'string','minLength':1,'maxLength':300},
    'kind':{'type':'string','enum':['analysis','change','verification']},'depends_on':{'type':'array','maxItems':12,'items':{'type':'string','maxLength':60}},
    'affected_files':{'type':'array','maxItems':24,'items':{'type':'string','maxLength':1000}},'check_ids':{'type':'array','maxItems':8,'items':{'type':'string','maxLength':80}}},
    'required':['id','title','kind'],'additionalProperties':False}
STEP_TOOL={'type':'function','function':{'name':'update_task_step','description':'Активировать/заблокировать шаг или подтвердить его реальными journal receipts. Завершение без evidence запрещено. Ссылки на receipts указаны в tool result _receipt.',
    'parameters':{'type':'object','properties':{'id':{'type':'string','maxLength':60},'status':{'type':'string','enum':['active','blocked','done']},'note':{'type':'string','maxLength':500},
        'evidence':{'type':'array','maxItems':24,'items':{'type':'object','properties':{'message_index':{'type':'integer','minimum':0},'call_id':{'type':'string','maxLength':200}},'required':['message_index','call_id'],'additionalProperties':False}}},'required':['id','status','evidence'],'additionalProperties':False}}}


def migrate_plan(task):
    if not task:return
    task['plan_steps']=[{'id':f'step_{i+1}','title':s,'kind':'analysis','depends_on':[],'affected_files':[],'check_ids':[],
        'status':'proposed','advisory':True,'source':'legacy','evidence':[]} if isinstance(s,str) else s for i,s in enumerate(task.get('plan_steps',[]))]
    task['plan_schema']=2


def prepare_steps(task,steps,source):
    from .tools import validate_tool_arguments
    nodes=[];known={c['id'] for c in task.get('options',{}).get('checks',[])}
    old={n['id']:n for n in task.get('plan_steps',[]) if isinstance(n,dict)}
    for index,item in enumerate(steps):
        advisory=isinstance(item,str)
        value={'id':f'step_{index+1}','title':item,'kind':'analysis'} if advisory else item
        validate_tool_arguments({'function':{'parameters':NODE_SCHEMA}},value)
        node={**deepcopy(value),'depends_on':list(value.get('depends_on',[])),'affected_files':list(value.get('affected_files',[])),'check_ids':list(value.get('check_ids',[]))}
        if any(c not in known for c in node['check_ids']):raise ValueError('Шаг ссылается на неизвестную проверку пользователя')
        if node['affected_files']:node['affected_files']=normalize_scope({'kind':'files','files':node['affected_files']})['files']
        if task.get('options',{}).get('read_only') and node['kind']!='analysis':raise ValueError('В режиме только чтения доступны только шаги исследования')
        if node['kind']=='change' and not node['affected_files']:raise ValueError('Для изменения укажите затронутые файлы')
        if node['kind']=='verification' and not node['check_ids']:raise ValueError('Для проверки выберите check_ids пользователя')
        node.update(status='proposed' if advisory else 'pending',advisory=advisory,source=source,evidence=[])
        previous=old.get(node['id'])
        fields=('id','title','kind','depends_on','affected_files','check_ids','advisory')
        if previous and all(previous.get(k)==node.get(k) for k in fields):node={**previous,'source':source}
        nodes.append(node)
    ids={n['id'] for n in nodes}
    if len(ids)!=len(nodes):raise ValueError('ID шагов должны быть уникальны')
    done=set()
    for _ in nodes:
        ready={n['id'] for n in nodes if n['id'] not in done and set(n['depends_on'])<=done}
        if not ready:break
        done|=ready
    if done!=ids:raise ValueError('План содержит цикл, неизвестную зависимость или ссылку на себя')
    return nodes


def witness(root,paths):
    policy=WorkspaceAccessPolicy(root);version=IndexPolicy(root).version;states={};size=0;started=time.monotonic()
    for path in sorted(set(paths)):
        target=policy.require(path)
        if not target.exists():states[path]={'kind':'missing'};continue
        if target.is_dir():states[path]={'kind':'directory'};continue
        before=target.stat();digest=hashlib.sha256()
        with target.open('rb') as stream:
            while True:
                chunk=stream.read(65536)
                if not chunk:break
                size+=len(chunk)
                if size>96_000_000 or time.monotonic()-started>2:raise ValueError('Сверка шагов слишком широка; сузьте affected_files')
                digest.update(chunk)
        after=target.stat()
        if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):raise ValueError('Файл изменился во время сверки')
        policy.require(path);states[path]={'kind':'file','sha256':digest.hexdigest()}
    if version!=IndexPolicy(root).version:raise ValueError('Права изменились во время сверки')
    return {'policy':version,'files':states}


def refresh_steps(task):
    migrate_plan(task)
    nodes={n['id']:n for n in task.get('plan_steps',[])}
    for node in nodes.values():
        if node.get('status')!='done':continue
        from .workspace_revision import evidence_matches
        for check in node.get('check_ids',[]):
            results=[r for r in task.get('test_results',[]) if r.get('check_id')==check]
            if not results or not results[-1].get('ok') or not evidence_matches(task,results[-1]):node['status']='stale'
        try:
            if node.get('witness')!=witness(task['project_root'],node.get('witness',{}).get('files',{})):node['status']='stale'
        except (ValueError,OSError):node['status']='stale'
    for _ in nodes:
        changed=False
        for node in nodes.values():
            if node.get('status')=='done' and any(nodes[d]['status']!='done' for d in node['depends_on']):node['status']='stale';changed=True
        if not changed:break


def update_step(task,args):
    migrate_plan(task);refresh_steps(task)
    nodes={n['id']:n for n in task.get('plan_steps',[])};node=nodes.get(args['id'])
    if not node:return {'ok':False,'error':'Шаг не найден'}
    if any(nodes[d]['status']!='done' for d in node['depends_on']):return {'ok':False,'error':'Сначала завершите зависимости с evidence'}
    if args['status']!='done':
        node.update(status=args['status'],advisory=False,note=args.get('note','')[:500],updated_at=_now());return {'ok':True,'step':deepcopy(node)}
    from .tool_recovery import task_journal
    entries={(r['message_index'],r['call_id']):r for r in task_journal(task).entries()}
    selected=[entries.get((e['message_index'],e['call_id'])) for e in args['evidence']]
    if not selected or any(not r or not(r.get('result') or {}).get('ok') or r['result'].get('user_confirmed') for r in selected):
        return {'ok':False,'error':'Нужны успешные неизменяемые квитанции текущего журнала'}
    allowed={'read_range','read_file','list_files','search_text','search_symbols','project_outline','delegate_readonly'} if node['kind']=='analysis' else {'write_file','patch_file','create_directory','delete_file','rename_file'} if node['kind']=='change' else {'run_project_command','run_project_diagnostics'}
    if any(r['name'] not in allowed for r in selected):return {'ok':False,'error':'Тип квитанции не соответствует шагу'}
    from .workspace_revision import evidence_matches
    for check in node['check_ids']:
        results=[r for r in task.get('test_results',[]) if r.get('check_id')==check]
        if not results or not results[-1].get('ok') or not evidence_matches(task,results[-1]):return {'ok':False,'error':'Нужна актуальная успешная проверка '+check+'. При run_project_command передайте check_id и точные параметры пользовательской проверки'}
    paths=set(node['affected_files']);covered=set();proof={}
    for entry in selected:
        result=entry['result'];arguments=json.loads(entry['arguments'])
        if node['kind']=='change':
            from .storage import Storage
            from .task_store import TASK_DIR
            with Storage(TASK_DIR.parent).ready().transaction() as c:
                rows=c.execute("SELECT data FROM workspace_snapshots WHERE group_id=? AND chat_id=? AND journal_id=? AND status='applied' ORDER BY sequence",(result.get('snapshot_group_id'),task['chat_id'],task['journal_id'])).fetchall()
            for row in rows:proof.update(json.loads(row[0]).get('after',{}))
            covered.update(proof)
        elif entry['name'] in ('run_project_command','run_project_diagnostics'):
            scope=(result.get('verification_receipt') or {}).get('scope',{})
            covered.update(paths if scope.get('kind')=='workspace' else scope.get('files',[]))
        elif entry['name']=='delegate_readonly':
            for source in result.get('sources',[]):covered.add(source['path']);proof[source['path']]={'kind':'file','sha256':source['sha256']}
        elif arguments.get('path') and arguments['path']!='.':
            path=result.get('path',arguments['path']);covered.add(path)
            if result.get('sha256'):proof[path]={'kind':'file','sha256':result['sha256']}
    if paths-covered:return {'ok':False,'error':'Квитанции не покрывают affected_files шага'}
    try:
        snapshot=witness(task['project_root'],paths or covered)
        for path,expected in proof.items():
            if path in snapshot['files'] and any(snapshot['files'][path].get(k)!=expected.get(k) for k in ('kind','sha256') if k in expected):raise ValueError('Файл уже не соответствует результату инструмента')
    except (ValueError,OSError) as exc:return {'ok':False,'error':str(exc)[:300]}
    node.update(status='done',advisory=False,evidence=deepcopy(args['evidence']),witness=snapshot,note=args.get('note','')[:500],updated_at=_now())
    return {'ok':True,'step':deepcopy(node),'note':'Квитанции и текущие файлы подтверждены; семантику пользовательских требований проверяют отдельно.'}
