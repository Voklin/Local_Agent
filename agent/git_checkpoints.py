"""Private Git checkpoints of confirmed snapshot bytes; never touches the project's index/branch."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from .managed_worktrees import git_path
from .optional_process import process_env,run_bounded
from .workspace_access import WorkspaceAccessPolicy
from .storage import encode
from .chat_store import _atomic_write


class GitCheckpoints:
    """Back up known before/after bytes; restoration still uses SnapshotStore's conflict gate."""
    def __init__(self, store):
        self.store=store
        identity=str(store.root).casefold() if os.name=='nt' else str(store.root)
        key=hashlib.sha256(identity.encode()).hexdigest()[:24]
        self.directory=store.database.directory/'git-checkpoints'/key
        self.repository=self.directory/'objects.git'

    def info(self, group_id):
        """Return only bounded metadata belonging to this private repository and snapshot group."""
        if not isinstance(group_id,str) or not re.fullmatch('[a-f0-9]{32}',group_id):return None
        path=self.directory/(group_id+'.json')
        if not path.exists() or path.stat().st_size>20000 or not self.repository.is_dir():return None
        try:
            value=json.loads(path.read_text(encoding='utf8'))
            if value.get('group_id')!=group_id or value.get('repository')!=str(self.repository) or not re.fullmatch('[a-f0-9]{40}|[a-f0-9]{64}',str(value.get('commit',''))):return None
            return value
        except (OSError,ValueError,AttributeError):return None

    def create(self, group_id, context):
        """Write immutable content-addressed refs in a private bare repository after explicit UI action."""
        if not isinstance(group_id,str) or not re.fullmatch('[a-f0-9]{32}',group_id):raise ValueError('Неверный ID снимка')
        with self.store.database.transaction() as connection:
            rows=self.store._rows(connection,group_id)
            if any(row['status'] not in ('applied','failed') for row in rows):raise ValueError('Сохраняются только завершённые подтверждённые правки')
            before,after=self.store._aggregate(rows)
        if not before:raise ValueError('Нет подтверждённых файлов для Git-снимка')
        self.directory.mkdir(parents=True,exist_ok=True)
        env=process_env();env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0',
            GIT_AUTHOR_NAME='Neutral',GIT_AUTHOR_EMAIL='neutral@localhost',GIT_COMMITTER_NAME='Neutral',GIT_COMMITTER_EMAIL='neutral@localhost')
        def git(args):
            command=[git_path(),'-c','core.hooksPath='+str(self.directory/'disabled-hooks'),'-c','core.fsmonitor=false','-c','core.longpaths=true',*args]
            result=run_bounded(command,self.directory,context,env=env)
            if not result['ok'] or result.get('truncated'):raise ValueError('Git checkpoint: '+str(result.get('error') or result['output'])[:400])
            return result['output'].strip()
        if not self.repository.exists():git(['init','--bare','--template=',str(self.repository)])
        prefix=['--git-dir='+str(self.repository)]
        with tempfile.TemporaryDirectory(prefix='checkpoint-',dir=self.directory) as temporary:
            folder=Path(temporary);env['GIT_INDEX_FILE']=str(folder/'index')
            manifest={'version':1,'root':str(self.store.root),'chat_id':self.store.chat_id,'group_id':group_id,'before':{},'after':{}}
            counter=0
            for stage,values in [('before',before),('after',after)]:
                for relative,saved in sorted(values.items()):
                    WorkspaceAccessPolicy(self.store.root).require(relative)
                    record={k:v for k,v in saved.items() if k in ('kind','sha256','mode')}
                    if saved['kind']=='file':
                        raw=self.store._original_bytes(saved);file=folder/('blob-'+str(counter));file.write_bytes(raw)
                        oid=git([*prefix,'hash-object','-w','--no-filters','--',str(file)])
                        location=stage+'/'+str(counter);git([*prefix,'update-index','--add','--cacheinfo','100644,'+oid+','+location])
                        record.update(blob=oid,entry=location);counter+=1
                    manifest[stage][relative]=record
            raw=encode(manifest).encode('utf8');signature=hashlib.sha256(raw).hexdigest();ref='refs/neutral/'+group_id+'/'+signature
            meta=folder/'manifest.json';meta.write_bytes(raw);oid=git([*prefix,'hash-object','-w','--no-filters','--',str(meta)])
            git([*prefix,'update-index','--add','--cacheinfo','100644,'+oid+',manifest.json'])
            tree=git([*prefix,'write-tree']);commit=git([*prefix,'commit-tree',tree,'-m','Neutral checkpoint '+group_id])
            # No project Git refs/index/hooks participate. Publishing this ref is the commit point.
            git([*prefix,'update-ref',ref,commit])
            result={'commit':commit,'ref':ref,'repository':str(self.repository),'paths':sorted(before),'group_id':group_id,'source':'neutral-private-git'}
            _atomic_write(self.directory/(group_id+'.json'),result)
            return {'checkpoint':result,'committed':True}
