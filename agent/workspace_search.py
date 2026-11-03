"""Shared bounded project search for the agent and desktop navigation."""
import fnmatch
import os
import threading
import time
from pathlib import Path
from functools import lru_cache
from .security import canonical_root, resolve_allowed_path

EXCLUDED={'.git','.venv','venv','__pycache__','node_modules','.idea','.vscode','.venv-test','.test-data','.test-tmp','dist','dist-electron','artifacts','build'}


def glob_matches(path,pattern):
    if not pattern:return True
    parts=path.casefold().split('/');patterns=pattern.casefold().replace('\\','/').split('/')
    if len(patterns)==1:return fnmatch.fnmatchcase(parts[-1],patterns[0])
    @lru_cache(maxsize=None)
    def match(i,j):
        if j==len(patterns):return i==len(parts)
        if patterns[j]=='**':return match(i,j+1) or (i<len(parts) and match(i+1,j))
        return i<len(parts) and fnmatch.fnmatchcase(parts[i],patterns[j]) and match(i+1,j+1)
    return match(0,0)


def search_project(root, params, cancelled=None, *, timeout=3, max_files=15000, max_bytes=10_000_000, use_index=True):
    """Use an activated index; incomplete/unavailable caches retain the original bounded search."""
    if use_index:
        import sqlite3
        from .project_index import get_index
        index=get_index(root)
        if index:
            try:
                result=index.query(params,cancelled)
                if result is not None:return result
            except (OSError,ValueError,sqlite3.Error) as exc:index.uncertain('Поиск по кешу недоступен: '+type(exc).__name__)
            fallback={**params,'mode':'text' if params.get('mode') in ('symbols','outline') else params.get('mode','text')}
            if not fallback.get('query') and fallback['mode']=='text':return {'ok':False,'code':'INDEX_NOT_READY','error':'Индекс не готов; используйте поиск текста или read_range','matches':[],'index':index.status()}
            result=search_project(root,fallback,cancelled,timeout=timeout,max_files=max_files,max_bytes=max_bytes,use_index=False)
            return {**result,'backend':'linear-fallback','precision':'text','index':index.status()}
    base = canonical_root(root)
    mode = params.get('mode', 'text')
    query = params.get('query', '')
    pattern = params.get('pattern', '')
    case_sensitive = params.get('case_sensitive', False)
    if mode not in ('text', 'files') or not isinstance(query, str) or len(query) > 200:
        raise ValueError('Выберите text/files и запрос не длиннее 200 символов')
    if mode == 'text' and not query.strip():
        raise ValueError('Введите текст поиска')
    if not isinstance(pattern, str) or len(pattern) > 120 or not isinstance(case_sensitive, bool):
        raise ValueError('Некорректная маска файлов или регистр поиска')
    requested_limit = params.get('limit', 200 if mode == 'text' else 1000)
    if isinstance(requested_limit, bool) or not isinstance(requested_limit, int) or not 1 <= requested_limit <= 2000:
        raise ValueError('Лимит результатов: целое число 1–2000')
    limit = min(requested_limit, 200 if mode == 'text' else 2000)
    cancelled = cancelled or threading.Event()
    deadline = time.monotonic() + timeout
    needle = query if case_sensitive else query.casefold()
    result = {'ok': True, 'matches': [], 'truncated': False, 'reason': '', 'scanned_files': 0, 'skipped_files': 0}
    entries = 0
    bytes_read = 0
    target=resolve_allowed_path(base,params.get('path','.'),must_exist=True)
    max_depth=params.get('max_depth',30)
    if type(max_depth) is not int or not 0<=max_depth<=30:raise ValueError('Глубина поиска: 0–30')
    stack = [(target if target.is_dir() else target.parent, 0)]
    from .workspace_access import WorkspaceAccessPolicy
    policy=WorkspaceAccessPolicy(base)
    visited = set()

    def stop():
        if cancelled.is_set():
            result.update(ok=False, code='SEARCH_CANCELLED', error='Поиск отменён', reason='cancelled')
            return True
        if time.monotonic() >= deadline:
            result.update(truncated=True, reason='time')
            return True
        return False

    while stack:
        if stop():
            return result
        directory, depth = stack.pop()
        if directory in visited:
            continue
        visited.add(directory)
        try:
            iterator = os.scandir(directory)
        except OSError:
            result['skipped_files'] += 1
            continue
        with iterator:
            for entry in iterator:
                entries += 1
                if stop():
                    return result
                if entries > 30000 or result['scanned_files'] >= max_files:
                    return {**result, 'truncated': True, 'reason': 'files'}
                try:
                    if entry.is_symlink() or getattr(Path(entry.path),'is_junction',lambda:False)():
                        continue
                    path = resolve_allowed_path(base, entry.path, must_exist=True)
                    if not policy.allows(path):continue
                    if target.is_file() and path!=target:continue
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name not in EXCLUDED:
                            if depth < max_depth:
                                stack.append((path, depth + 1))
                            else:
                                result.update(truncated=True, reason='depth')
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    result['scanned_files'] += 1
                    relative = path.relative_to(base).as_posix()
                    if len(relative) > 1000 or (pattern and not glob_matches(relative,pattern)):
                        continue
                    if mode == 'files':
                        haystack = relative if case_sensitive else relative.casefold()
                        if needle in haystack:
                            result['matches'].append({'path':relative, 'line':1, 'text':'', 'size_bytes':path.stat().st_size})
                    else:
                        size = path.stat().st_size
                        if size > 1_000_000:
                            result['skipped_files'] += 1
                            continue
                        if bytes_read + size > max_bytes:
                            return {**result, 'truncated': True, 'reason': 'bytes'}
                        with path.open('rb') as stream:
                            raw = stream.read(min(1_000_001, max_bytes - bytes_read + 1))
                        bytes_read += len(raw)
                        if len(raw) > 1_000_000 or bytes_read > max_bytes:
                            return {**result, 'truncated': True, 'reason': 'bytes'}
                        if b'\x00' in raw:
                            result['skipped_files'] += 1
                            continue
                        text = raw.decode('utf-8')
                        for number, line in enumerate(text.splitlines(), 1):
                            if number % 64 == 0 and stop():
                                return result
                            haystack = line if case_sensitive else line.casefold()
                            if needle in haystack:
                                result['matches'].append({'path':relative, 'line':number, 'text':line[:300]})
                                if len(result['matches']) >= limit:
                                    return {**result, 'truncated': True, 'reason': 'results'}
                    if len(result['matches']) >= limit:
                        return {**result, 'truncated': True, 'reason': 'results'}
                except (OSError, ValueError, UnicodeError):
                    result['skipped_files'] += 1
    return result

