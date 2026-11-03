"""User-initiated optional IDE jobs with explicit settings, budgets and cancellation."""
from copy import deepcopy
import json
import threading
from pathlib import Path
from agent.chat_store import APP_DIR,_atomic_write
from agent.operation_context import OperationContext
from agent.readonly_research import research
from agent.language_diagnostics import diagnose
from agent.managed_worktrees import ManagedWorktrees
from agent.container_runner import container_status,run_container
from agent.security import canonical_root

DEFAULTS={'research':{'enabled':False,'seconds':60,'max_tokens':1024},
    'lsp':{'enabled':False,'program':'','arguments':[],'language':'python','seconds':20},
    'worktrees':{'enabled':False},'container':{'enabled':False,'image':'node:22-alpine','memory_mb':512}}


def validate_settings(value):
    if not isinstance(value,dict) or set(value)!=set(DEFAULTS):raise ValueError('Ожидаются настройки четырёх дополнительных возможностей')
    result=deepcopy(DEFAULTS)
    for name,default in DEFAULTS.items():
        item=value[name]
        if not isinstance(item,dict) or set(item)!=set(default) or type(item.get('enabled')) is not bool:raise ValueError('Некорректные настройки '+name)
        result[name]=deepcopy(item)
    for group,key,minimum,maximum in [('research','seconds',10,120),('research','max_tokens',256,2048),('lsp','seconds',2,60),('container','memory_mb',128,2048)]:
        number=result[group][key]
        if type(number) is not int or not minimum<=number<=maximum:raise ValueError(f'{group}.{key}: {minimum}–{maximum}')
    for group,key,limit in [('lsp','program',2000),('lsp','language',80),('container','image',200)]:
        text=result[group][key]
        if not isinstance(text,str) or len(text)>limit or '\x00' in text or (group!='lsp' or key!='program') and not text.strip():raise ValueError('Некорректное поле '+key)
    args=result['lsp']['arguments']
    if not isinstance(args,list) or len(args)>40 or any(not isinstance(a,str) or len(a)>2000 or '\x00' in a for a in args):raise ValueError('Аргументы LSP: до 40 строк по 2000 символов')
    if result['lsp']['enabled'] and not result['lsp']['program'].strip():raise ValueError('Укажите программу LSP до включения диагностики')
    # Validate image independently of runtime availability.
    import re
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/:@-]{0,199}',result['container']['image']):raise ValueError('Неверное имя Docker image')
    return result


class OptionalIdeService:
    def __init__(self,tasks,directory=None):
        self.tasks=tasks;self.directory=Path(directory) if directory else APP_DIR/'optional-ide'
        self.file=self.directory/'settings.json';self.settings=deepcopy(DEFAULTS);self.warning=''
        if self.file.exists():
            try:self.settings=validate_settings(json.loads(self.file.read_text(encoding='utf-8')))
            except (ValueError,OSError):self.warning='Не удалось прочитать дополнительные настройки; возможности выключены. Исправьте и сохраните настройки.'
        self.worktrees=ManagedWorktrees(self.directory.parent/'wt');self.context=None;self.thread=None;self.running=False;self.closed=False

    def catalog(self):
        return {'ok':True,'settings':deepcopy(self.settings),'running':self.running,'warning':self.warning,'inference':self.tasks.scheduler.status()}

    def configure(self,value):
        self.tasks.idle();settings=validate_settings(value);_atomic_write(self.file,settings);self.settings=settings;self.warning=''
        return self.catalog()

    def start(self,root,params,respond):
        with self.tasks.lock:
            self.tasks.idle()
            if self.closed:raise ValueError('Служба дополнительных возможностей закрыта')
            base=canonical_root(root);action=params.get('action');settings=deepcopy(self.settings);lease=None
            groups={'research':'research','diagnostics':'lsp','worktree_list':'worktrees','worktree_create':'worktrees','worktree_diff':'worktrees','worktree_remove':'worktrees','worktree_open':'worktrees','container_status':'container'}
            if action not in groups:raise ValueError('Неизвестная дополнительная операция')
            group=groups[action]
            if action!='container_status' and not settings[group]['enabled']:raise ValueError('Сначала включите эту возможность в панели IDE')
            if action in {'worktree_create','worktree_remove'} and params.get('confirmed') is not True:raise ValueError('Подтвердите действие с рабочей копией')
            seconds=settings[group].get('seconds',30)
            if action=='research':lease=self.tasks.inference.begin('исследователь',seconds)
            self.context=lease.context if lease else OperationContext(seconds);self.running=True
            config=deepcopy(self.tasks.config);context=self.context
            run_context=None
            if action=='research':
                try:run_context=self.tasks.registry.begin(kind='research',model=config['model'],base_url=config['base_url'],api_protocol=config.get('api_protocol','chat'),operation=context,spending_policy=config['settings'].get('paid_budget'))
                except BaseException:
                    self.tasks.inference.end(lease.id);self.running=False;self.context=None
                    raise
            def run():
                try:
                    if action=='research':result=research(base,params.get('query'),config,context,settings['research']['max_tokens'])
                    elif action=='diagnostics':result=diagnose(base,params.get('path',''),settings['lsp'],context)
                    elif action=='container_status':result=container_status(base,context)
                    elif action=='worktree_list':result=self.worktrees.list(base,context)
                    elif action=='worktree_create':result=self.worktrees.create(base,params.get('name'),context)
                    elif action=='worktree_diff':result=self.worktrees.diff(base,params.get('id'),context)
                    elif action=='worktree_remove':result=self.worktrees.remove(base,params.get('id'),context)
                    else:
                        row,path=self.worktrees.get(base,params.get('id'),context);result={'ok':True,'path':str(path),'name':row['name']}
                except Exception as exc:
                    # HTTP exception strings may contain authentication URLs; never forward them.
                    from httpx import HTTPError
                    result={'ok':False,'error':('Сервер модели: '+type(exc).__name__) if isinstance(exc,HTTPError) else str(exc)[:700]}
                finally:
                    with self.tasks.lock:
                        if run_context:run_context.finish('paused' if context.is_set() else 'completed' if result.get('ok') else 'failed')
                        if lease:self.tasks.inference.end(lease.id)
                        self.running=False;self.context=None
                respond({**result,'root':str(base)})
            self.thread=threading.Thread(target=run,daemon=True,name='optional-ide')
            try:self.thread.start()
            except Exception:
                self.running=False;self.context=None
                if lease:self.tasks.inference.end(lease.id)
                raise

    def cancel(self):
        with self.tasks.lock:
            if self.context:self.context.set()
        return {'ok':True}

    def command(self,root,args,context,approve):
        return run_container(root,args,self.settings['container'],context,approve)

    def shutdown(self):
        self.closed=True;self.cancel()
        if self.thread:self.thread.join(3)
