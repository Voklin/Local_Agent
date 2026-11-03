"""One automatic file-access policy; exact exceptions come only from the trusted UI."""
import fnmatch
import hashlib
import json
import os
from pathlib import Path
from .security import AccessDenied, canonical_root, resolve_allowed_path


class WorkspaceAccessPolicy:
    def __init__(self, root):
        self.root=canonical_root(root)
        from .task_store import TASK_DIR
        self.file=TASK_DIR.parent/'workspace-access.json'
        identity=str(self.root).casefold() if os.name=='nt' else str(self.root)
        self.key=hashlib.sha256(identity.encode()).hexdigest()
        try:
            with self.file.open('rb') as source:raw=source.read(128001)
            if len(raw)>128000:raise ValueError('Размер файла разрешений')
            self.records=json.loads(raw)
            if not isinstance(self.records,dict):raise ValueError('Формат разрешений')
        except FileNotFoundError:self.records={}
        except (ValueError,OSError) as exc:raise AccessDenied('Настройки доступа повреждены; проверьте разрешения в Neutral') from exc
        self.exceptions=self.records.get(self.key,[])
        if not isinstance(self.exceptions,list) or len(self.exceptions)>64 or any(not isinstance(p,str) for p in self.exceptions):
            raise AccessDenied('Некорректные разрешения проекта')
        self.patterns=[]
        ignore=resolve_allowed_path(self.root,'.neutralignore')
        self.ignore_path=ignore
        if ignore.exists():
            with ignore.open('rb') as source:raw=source.read(16385)
            if len(raw)>16384:raise AccessDenied('.neutralignore превышает 16 КБ')
            try:lines=raw.decode('utf-8-sig').splitlines()
            except UnicodeError as exc:raise AccessDenied('.neutralignore должен быть UTF-8') from exc
            self.patterns=[line.strip().replace('\\','/').casefold().lstrip('/') for line in lines if line.strip() and not line.lstrip().startswith('#')]
            if len(self.patterns)>128 or any(len(p)>256 or p.startswith('!') or '..' in p.split('/') for p in self.patterns):
                raise AccessDenied('.neutralignore: до 128 glob-правил; исключения задаются в интерфейсе')

    def allows(self, path):
        """Check canonical targets, including aliases, against defaults and user exclusions."""
        target=resolve_allowed_path(self.root,path)
        if target==self.file.resolve():return False
        relative=target.relative_to(self.root).as_posix()
        # Exact UI exceptions cannot be expanded into folder or glob grants by a model.
        if relative in self.exceptions:return True
        parts=relative.casefold().split('/')
        sensitive={'.git','.ssh','.aws','.azure','.gcp','credentials','secrets','id_rsa','id_ed25519','id_ecdsa'}
        if any(p in sensitive or p.endswith(('.pem','.key','.pfx','.p12','.jks','.keystore','.kdbx')) or
               (p=='.env' or p.startswith('.env.') and p not in {'.env.example','.env.sample','.env.template'}) for p in parts):return False
        ancestors=['/'.join(parts[:i]) for i in range(1,len(parts)+1)]
        for pattern in self.patterns:
            pattern=pattern.rstrip('/')
            if any(fnmatch.fnmatchcase(p,pattern) or ('/' not in pattern and fnmatch.fnmatchcase(p.split('/')[-1],pattern)) for p in ancestors):return False
        return True

    def require(self,path, *, mutation=False):
        """Reject automatic reads/changes; manual editor access remains independent."""
        target=resolve_allowed_path(self.root,path)
        if mutation and target==self.ignore_path:raise AccessDenied('Правила доступа меняются пользователем в редакторе')
        if not self.allows(target):raise AccessDenied('Файл закрыт для автоматического доступа. Разрешите конкретный файл в возможностях IDE → Доступ модели.')
        return target

    def catalog(self):
        """Return policy metadata without reading or revealing protected file contents."""
        return {'ok':True,'root':str(self.root),'exceptions':self.exceptions,'ignore_patterns':self.patterns}

    def configure(self,paths,confirmed=False):
        """Persist exact existing-file exceptions outside the workspace after explicit UI consent."""
        if confirmed is not True or not isinstance(paths,list) or len(paths)>64:raise ValueError('Подтвердите точные разрешения файлов')
        entries=[]
        for path in paths:
            if not isinstance(path,str) or not path or len(path)>1000 or '\x00' in path:raise ValueError('Некорректный путь разрешения')
            target=resolve_allowed_path(self.root,path,must_exist=True)
            if target==self.file.resolve():raise ValueError('Разрешения Neutral меняются только через интерфейс')
            if not target.is_file():raise ValueError('Разрешение задаётся для существующего файла, не папки')
            relative=target.relative_to(self.root).as_posix()
            if relative not in entries:entries.append(relative)
        from .chat_store import _atomic_write
        self.records[self.key]=entries
        _atomic_write(self.file,self.records)
        self.exceptions=entries
        return self.catalog()


def filter_model_history(messages,root):
    """Re-check known file-result provenance on every projection, without changing the saved chat."""
    policy=WorkspaceAccessPolicy(root);calls={};blocked=set();projected=[]
    offset=1 if messages and messages[0].get('role')=='system' else 0
    file_tools={'read_file','read_range','search_text','search_files','search_symbols','project_outline','glob_files','list_files','get_project_instructions',
                'write_file','patch_file','rename_file','delete_file','run_project_diagnostics'}
    def denied(path):
        """An invalid or escaped path is not suitable for automatic context either."""
        try:return not policy.allows(path)
        except (OSError,ValueError):return True
    for index,message in enumerate(messages):
        if message.get('role')=='assistant':
            for call in message.get('tool_calls') or []:
                function=call.get('function') or {}
                try:arguments=json.loads(function.get('arguments') or '{}')
                except (ValueError,TypeError):arguments={}
                calls[call.get('id')]=(function.get('name'),arguments if isinstance(arguments,dict) else {})
        if message.get('role')=='tool':
            name,args=calls.get(message.get('tool_call_id'),(None,{}));hide=False
            if name in file_tools:
                hide=any(denied(args[key]) for key in ('path','destination') if isinstance(args.get(key),str))
                try:value=json.loads(message.get('content') or '{}')
                except (ValueError,TypeError):value={}
                if isinstance(value,dict):
                    if isinstance(value.get('path'),str):hide=hide or denied(value['path'])
                    if name=='run_project_diagnostics':
                        scope=(value.get('verification_receipt') or {}).get('scope',{})
                        hide=hide or any(denied(p) for p in scope.get('files',[])+scope.get('dependencies',[]))
                    for key in ('matches','entries','instructions'):
                        entries=value.get(key)
                        if isinstance(entries,list):hide=hide or any(isinstance(item,dict) and isinstance(item.get('path'),str) and denied(item['path']) for item in entries)
            if name in ('search_project_memory','remember_project_note'):
                # A saved answer is not authority to disclose a revoked or stale memory source.
                try:
                    value=json.loads(message.get('content') or '{}')
                    records=value.get('records',[value['record']] if isinstance(value.get('record'),dict) else [])
                    ids={item['id'] for item in records if isinstance(item,dict) and isinstance(item.get('id'),str)}
                    from .project_knowledge import ProjectKnowledge
                    old={item['id']:item for item in records if isinstance(item,dict) and 'id' in item}
                    current=[item for item in ProjectKnowledge(root).listing(model=True,identities=ids) if all(item.get(k)==old[item['id']].get(k) for k in ('text','kind','sources','origin','created_at','updated_at','provenance','policy'))]
                    message={**message,'content':json.dumps({'ok':True,'records':current,'_receipt':value.get('_receipt'),'note':'Память повторно сверена; отсутствующие записи устарели, удалены или закрыты.'},ensure_ascii=False)}
                    blocked.add(index-offset) # Full artifact reader must not bypass this fresh projection.
                except (ValueError,OSError,RuntimeError,TypeError):hide=True
            if name=='read_tool_result':
                origin=args.get('message_index')
                source_index=origin+offset if type(origin) is int else -1
                source=messages[source_index] if 0<=source_index<len(messages) else {}
                if (type(origin) is not int or origin in blocked or source_index>=index or
                    source.get('role')!='tool' or source.get('tool_call_id')!=args.get('call_id')):hide=True
            if hide:
                blocked.add(index-offset)
                message={**message,'content':json.dumps({'ok':False,'code':'ACCESS_REVOKED','error':'Сохранённый файловый результат закрыт текущими правилами доступа.'},ensure_ascii=False)}
        projected.append(message)
    return projected
