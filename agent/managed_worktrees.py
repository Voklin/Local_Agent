"""Explicit Git worktrees created from committed HEAD, with ownership receipts."""
import hashlib
import json
import os
import re
import shutil
import uuid
from pathlib import Path
from .chat_store import _atomic_write
from .security import canonical_root
from .operation_context import OperationContext
from .optional_process import run_bounded,process_env


def git_path():
    value=os.environ.get('LCA_GIT') or shutil.which('git')
    if not value:raise ValueError('Git не найден; установите Git или укажите LCA_GIT')
    return value


class ManagedWorktrees:
    def __init__(self,directory):
        self.directory=Path(directory).resolve();self.file=self.directory/'worktrees.json'

    def _records(self):
        if not self.file.exists():return []
        value=json.loads(self.file.read_text(encoding='utf-8'))
        if not isinstance(value,list):raise ValueError('Повреждён реестр worktrees')
        return value

    def _git(self,root,args,context):
        hooks=self.directory/'disabled-hooks';hooks.mkdir(parents=True,exist_ok=True)
        env=process_env();env.update(GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1')
        result=run_bounded([git_path(),'-c','core.hooksPath='+str(hooks),'-c','core.longpaths=true','-c','core.fsmonitor=false','-c','submodule.recurse=false',*args],root,context,env=env)
        if not result['ok']:raise ValueError('Git: '+str(result.get('error') or result['output'])[:700])
        if result.get('truncated'):raise ValueError('Вывод Git превышает предел; операция требует ручной проверки')
        return result['output']

    def repository(self,root,context):
        base=canonical_root(root)
        top=Path(self._git(base,['rev-parse','--show-toplevel'],context).strip()).resolve(strict=True)
        if base!=top:raise ValueError('Откройте корень Git-репозитория для управления worktrees')
        for row in self._records():
            if self._target(row)!=base:continue
            owner=canonical_root(row['root'])
            common=['rev-parse','--path-format=absolute','--git-common-dir']
            if self._git(owner,common,context).strip()!=self._git(base,common,context).strip():raise ValueError('Управляемая копия больше не принадлежит исходному репозиторию')
            return owner
        return base

    def list(self,root,context):
        base=self.repository(root,context);rows=[]
        actual=self._git(base,['worktree','list','--porcelain','-z'],context)
        registered={Path(line[9:]).resolve() for line in actual.split('\x00') if line.startswith('worktree ')}
        for row in self._records():
            if row.get('root')!=str(base):continue
            target=self._target(row)
            rows.append({**row,'exists':target.is_dir(),'registered':target in registered})
        return {'ok':True,'worktrees':rows}

    def _target(self,row):
        target=Path(row['path']).resolve()
        target.relative_to(self.directory)
        if target==self.directory or not re.fullmatch(r'[a-f0-9]{32}',row.get('id','')) or target.name!=row['id']:raise ValueError('Недопустимая запись worktree')
        return target

    def create(self,root,label,context):
        base=self.repository(root,context)
        if not isinstance(label,str) or not 1<=len(label.strip())<=80:raise ValueError('Название копии: 1–80 символов')
        rows=self._records()
        if sum(r.get('root')==str(base) for r in rows)>=8:raise ValueError('Предел: 8 управляемых копий на репозиторий')
        commit=self._git(base,['rev-parse','--verify','HEAD^{commit}'],context).strip()
        if not re.fullmatch('[0-9a-f]{40,64}',commit):raise ValueError('Нужен существующий commit')
        identity=uuid.uuid4().hex;parent=self.directory/hashlib.sha256(str(base).encode()).hexdigest()[:20]
        parent.mkdir(parents=True,exist_ok=True);target=parent/identity;target.resolve().relative_to(self.directory)
        row={'id':identity,'root':str(base),'path':str(target),'name':label.strip(),'commit':commit,'status':'creating'}
        # Receipt survives a crash between Git and response; never blindly retry effects.
        rows.append(row);_atomic_write(self.file,rows)
        try:self._git(base,['worktree','add','--detach','--',str(target),commit],context)
        except Exception:
            row['status']='needs_review';_atomic_write(self.file,rows);raise
        row['status']='ready';_atomic_write(self.file,rows)
        return {'ok':True,'worktree':row,'notice':'Создано из commit HEAD. Незакоммиченные изменения не копируются.'}

    def get(self,root,identity,context):
        base=self.repository(root,context)
        row=next((r for r in self._records() if r.get('id')==identity and r.get('root')==str(base)),None)
        if not row:raise ValueError('Это не управляемая копия выбранного проекта')
        target=self._target(row)
        registered=self._git(base,['worktree','list','--porcelain','-z'],context)
        if not any(line.startswith('worktree ') and Path(line[9:]).resolve()==target for line in registered.split('\x00')):raise ValueError('Git не подтверждает зарегистрированную копию; проверьте её вручную')
        # Ensure an existing path was not replaced by a different repository.
        common=self._git(base,['rev-parse','--path-format=absolute','--git-common-dir'],context).strip()
        if self._git(target,['rev-parse','--path-format=absolute','--git-common-dir'],context).strip()!=common:raise ValueError('Worktree больше не принадлежит этому репозиторию')
        return row,target

    def diff(self,root,identity,context):
        row,target=self.get(root,identity,context)
        changes=self._git(target,['status','--porcelain','--untracked-files=all'],context)
        diff=self._git(target,['diff','--no-ext-diff','--no-textconv','HEAD','--'],context)
        return {'ok':True,'worktree':row,'status':changes,'diff':diff,'notice':'Diff показывает отслеживаемые файлы; новые файлы перечислены в status.'}

    def remove(self,root,identity,context):
        row,target=self.get(root,identity,context)
        if target==canonical_root(root):raise ValueError('Нельзя удалить открытую копию; сначала вернитесь в исходную папку')
        if row['status']!='ready':raise ValueError('Незавершённую копию нужно проверить вручную')
        if self._git(target,['status','--porcelain','--untracked-files=all'],context).strip():raise ValueError('В копии есть изменения или новые файлы; удаление отклонено')
        if self._git(target,['ls-files','--others','--directory','-z'],context):raise ValueError('В копии есть неотслеживаемые или ignored файлы; сохраните их вручную')
        if self._git(target,['rev-parse','HEAD'],context).strip()!=row['commit']:raise ValueError('В копии появились commits; сохраните их вручную')
        # Git refuses ignored files, submodules and locked checkouts without --force.
        self._git(root,['worktree','remove','--',str(target)],context)
        _atomic_write(self.file,[r for r in self._records() if r.get('id')!=identity])
        return {'ok':True}
