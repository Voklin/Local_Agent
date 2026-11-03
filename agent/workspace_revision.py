"""Bounded content revisions shared by editor, command evidence and recovery."""
import hashlib
import json
import os
import time
from .security import canonical_root

REVISION_EXCLUDES = frozenset({'.git','node_modules','venv','__pycache__','.pytest_cache',
    '.mypy_cache','.ruff_cache','dist','build','artifacts','.test-data','coverage'})


class WorkspaceRevisionService:
    """Capture reproducible content evidence without retaining source file contents."""
    @staticmethod
    def capture(root, *, max_files=10000, max_bytes=96_000_000, timeout=2):
        """Hash source-tree contents; an unreadable, moving or over-budget tree is unverified."""
        rows=[];total=0;deadline=time.monotonic()+timeout
        try:
            if not root:raise ValueError('Корень проверки не задан')
            base=canonical_root(root)
            stack=[base]
            while stack:
                directory=stack.pop()
                with os.scandir(directory) as entries:
                    for entry in entries:
                        if time.monotonic()>deadline:raise ValueError('Лимит времени fingerprint')
                        if entry.name in REVISION_EXCLUDES or entry.name.startswith('.venv'):continue
                        relative=os.path.relpath(entry.path,base).replace('\\','/')
                        if len(rows)>=max_files:raise ValueError('Лимит файлов fingerprint')
                        if entry.is_symlink() or getattr(os.path,'isjunction',lambda _path:False)(entry.path):
                            rows.append((relative,'link',os.readlink(entry.path)));continue
                        if entry.is_dir(follow_symlinks=False):
                            rows.append((relative,'directory'));stack.append(entry.path);continue
                        if not entry.is_file(follow_symlinks=False):raise ValueError('Нестандартный файл fingerprint')
                        before=entry.stat(follow_symlinks=False);digest=hashlib.sha256()
                        if before.st_size>8_000_000:raise ValueError(relative+': файл превышает предел сверки 8 МБ')
                        with open(entry.path,'rb') as stream:
                            while True:
                                block=stream.read(65536)
                                if not block:break
                                total+=len(block)
                                if total>max_bytes or time.monotonic()>deadline:raise ValueError('Лимит чтения fingerprint')
                                digest.update(block)
                        after=entry.stat(follow_symlinks=False)
                        if (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):
                            raise ValueError('Файл изменился во время fingerprint')
                        rows.append((relative,digest.hexdigest()))
            digest=hashlib.sha256(json.dumps(sorted(rows),ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            return {'version':1,'scope':'source-tree-v1','complete':True,'digest':digest,'entries':len(rows)}
        except (OSError,ValueError,RuntimeError) as exc:
            return {'version':1,'scope':'source-tree-v1','complete':False,'digest':None,'error':str(exc)[:200]}

    @staticmethod
    def capture_files(root,paths,*,max_bytes=96_000_000,timeout=2):
        """Hash declared saved files under the access policy; no traversal of unrelated directories."""
        from .workspace_access import WorkspaceAccessPolicy
        rows=[];total=0;deadline=time.monotonic()+timeout
        try:
            if not isinstance(paths,list) or not 1<=len(paths)<=256:raise ValueError('Нужны конкретные файлы проверки')
            policy=WorkspaceAccessPolicy(root);base=policy.root
            policy_hash=hashlib.sha256(json.dumps({'patterns':policy.patterns,'exceptions':policy.exceptions},sort_keys=True).encode()).hexdigest()
            for relative in sorted(set(paths)):
                target=policy.require(relative)
                raw=base/relative
                if any(p.is_symlink() or getattr(os.path,'isjunction',lambda _p:False)(p) for p in (raw,*raw.parents) if p!=base and base in p.parents):
                    raise ValueError('Ссылки не входят в область проверки')
                if not target.is_file():raise ValueError('Файл проверки отсутствует или не является обычным файлом')
                before=target.stat();digest=hashlib.sha256()
                if before.st_size>8_000_000:raise ValueError('Файл области превышает предел сверки 8 МБ')
                with target.open('rb') as source:
                    while True:
                        block=source.read(65536)
                        if not block:break
                        total+=len(block)
                        if total>max_bytes or time.monotonic()>deadline:raise ValueError('Лимит сверки выбранных файлов')
                        digest.update(block)
                after=target.stat()
                if (before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):raise ValueError('Файл изменился во время сверки')
                policy.require(relative);rows.append((relative,digest.hexdigest()))
            fresh=WorkspaceAccessPolicy(root)
            fresh_hash=hashlib.sha256(json.dumps({'patterns':fresh.patterns,'exceptions':fresh.exceptions},sort_keys=True).encode()).hexdigest()
            if fresh_hash!=policy_hash:raise ValueError('Правила доступа изменились во время сверки')
            for relative in paths:fresh.require(relative)
            digest=hashlib.sha256(json.dumps({'files':rows,'policy':policy_hash},sort_keys=True,separators=(',',':')).encode()).hexdigest()
            return {'version':2,'scope':'declared-files-v1','complete':True,'digest':digest,'entries':len(rows)}
        except (OSError,ValueError,RuntimeError) as exc:
            return {'version':2,'scope':'declared-files-v1','complete':False,'digest':None,'error':str(exc)[:200]}


def evidence_matches(task, entry):
    """Old receipts are unverified; new evidence must match its declared witness and current sources."""
    from .verification_evidence import assess_evidence
    return assess_evidence(task,entry,task.get('workspace_revision'))['status']=='current'
