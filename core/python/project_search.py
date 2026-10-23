"""Bounded project navigation, independent of the language model and agent tools."""
import fnmatch
import os
import threading
import time

from agent.security import canonical_root, resolve_allowed_path
from agent.tools import IGNORED_DIRS

EXCLUDED = IGNORED_DIRS | {'.venv-test', '.test-data', '.test-tmp', 'dist', 'dist-electron', 'artifacts', 'build'}


def search_project(root, params, cancelled=None, *, timeout=3, max_files=15000, max_bytes=10_000_000):
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
    stack = [(base, 0)]
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
                    if entry.is_symlink():
                        continue
                    path = resolve_allowed_path(base, entry.path, must_exist=True)
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name not in EXCLUDED:
                            if depth < 30:
                                stack.append((path, depth + 1))
                            else:
                                result.update(truncated=True, reason='depth')
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    result['scanned_files'] += 1
                    relative = path.relative_to(base).as_posix()
                    if len(relative) > 1000 or (pattern and not fnmatch.fnmatchcase(relative.casefold(), pattern.casefold())):
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


class ProjectSearchService:
    def __init__(self):
        self.thread = None
        self.cancelled = threading.Event()
        self.lock = threading.RLock()
        self.running = False

    def start(self, root, params, respond):
        with self.lock:
            if self.running:
                raise ValueError('Предыдущий поиск ещё завершается')
            snapshot_root = canonical_root(root)
            snapshot_params = dict(params)
            self.running = True
            self.cancelled = cancelled = threading.Event()

            def run_search():
                try:
                    response = search_project(snapshot_root, snapshot_params, cancelled)
                except Exception as exc:
                    response = {'ok':False, 'error':str(exc)[:500]}
                with self.lock:
                    self.running = False
                respond(response)

            self.thread = threading.Thread(target=run_search, daemon=True, name='project-search')
            self.thread.start()

    def cancel(self):
        self.cancelled.set()
        return {'ok':True}

    def shutdown(self):
        self.cancel()
        if self.thread:
            self.thread.join(timeout=1)
