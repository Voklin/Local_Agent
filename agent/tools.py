from pathlib import Path
import os
import difflib
import tempfile
import hashlib
from .security import AccessDenied, resolve_allowed_path
from .workspace_access import WorkspaceAccessPolicy

MAX_READ_BYTES = 120_000
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".idea", ".vscode"}


def validate_tool_arguments(definition, arguments):
    """Validate before dispatch, without putting submitted argument values in errors."""
    from jsonschema import Draft202012Validator
    if not isinstance(arguments, dict):
        raise ValueError('Аргументы инструмента должны быть JSON-объектом')
    schema = definition['function'].get('parameters', {'type': 'object'})
    error = next(Draft202012Validator(schema).iter_errors(arguments), None)
    if error is not None:
        field = '.'.join(str(part) for part in error.absolute_path)[:160] or 'arguments'
        detail = str(error.validator_value)[:200] if error.validator in ('required', 'type', 'enum', 'minimum', 'maximum') else str(error.validator)
        raise ValueError(f'{field}: схема {error.validator}, ожидается {detail}')


def list_files(root, path=".", recursive=False, max_entries=200, max_depth=5):
    policy=WorkspaceAccessPolicy(root)
    target = policy.require(path)
    if not target.is_dir():
        return {"ok": False, "error": "Path is not a directory"}
    results = []
    base = resolve_allowed_path(root)
    # Walk one level at a time so recursive listings can enforce a depth cap.
    if recursive:
        for current, dirs, files in os.walk(target, topdown=True, followlinks=False):
            current_path = Path(current)
            try:
                safe_current = resolve_allowed_path(root, current_path, must_exist=True)
                policy.require(safe_current)
            except (AccessDenied, OSError):
                dirs[:] = []
                continue
            depth = len(safe_current.relative_to(base).parts) - len(target.relative_to(base).parts)
            dirs[:] = [name for name in dirs if name not in IGNORED_DIRS and depth < max_depth]
            names = list(dirs) + list(files)
            for name in names:
                item = current_path / name
                try:
                    safe = resolve_allowed_path(root, item, must_exist=True)
                except (AccessDenied, OSError):
                    continue  # do not follow symlinks/junctions that escape the root
                if any(part in IGNORED_DIRS for part in safe.relative_to(base).parts):
                    continue
                if not policy.allows(safe):continue
                rel = safe.relative_to(base).as_posix()
                results.append({"path": rel, "type": "directory" if safe.is_dir() else "file"})
                if len(results) >= max_entries:
                    return {"ok": True, "root": str(base), "path": safe_relative(target, base), "entries": results, "truncated": True, "limit": max_entries}
    else:
        for item in target.iterdir():
            try:
                safe = resolve_allowed_path(root, item, must_exist=True)
            except (AccessDenied, OSError):
                continue
            if any(part in IGNORED_DIRS for part in safe.relative_to(base).parts):
                continue
            if not policy.allows(safe):continue
            results.append({"path": safe.relative_to(base).as_posix(), "type": "directory" if safe.is_dir() else "file"})
            if len(results) >= max_entries:
                return {"ok": True, "root": str(base), "path": safe_relative(target, base), "entries": results, "truncated": True, "limit": max_entries}
    return {"ok": True, "root": str(base), "path": safe_relative(target, base), "entries": results, "truncated": False, "limit": max_entries}


def safe_relative(target, base):
    rel = target.relative_to(base).as_posix()
    return rel if rel != "." else "."


def read_file(root, path):
    target = WorkspaceAccessPolicy(root).require(path)
    if not target.is_file():
        return {"ok": False, "error": "Path is not a file"}
    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        return {"ok": False, "error": f"File is too large ({size} bytes; limit {MAX_READ_BYTES})"}
    try:
        before=target.stat()
        with target.open('rb') as stream:raw=stream.read(MAX_READ_BYTES+1)
        after=target.stat()
        if len(raw)>MAX_READ_BYTES or (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):
            return {'ok':False,'code':'FILE_CHANGED','error':'Файл изменился во время чтения'}
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        return {"ok": False, "error": "File is not UTF-8 text"}
    return {"ok": True, "path": target.relative_to(resolve_allowed_path(root)).as_posix(), "content": content,"sha256":hashlib.sha256(raw).hexdigest()}


def search_text(root, query, path=".", case_sensitive=False, max_depth=5, cancelled=None, pattern="", limit=200):
    from .workspace_search import search_project
    return search_project(root,{'query':query,'path':path,'case_sensitive':case_sensitive,
        'max_depth':max_depth,'pattern':pattern,'limit':limit},cancelled)


def preview_file_change(root, path, content, *, max_existing_bytes=MAX_READ_BYTES):
    """Validate a proposed text edit and return a unified diff without writing anything."""
    if not isinstance(content, str):
        return {"ok": False, "error": "content must be a string"}
    if len(content.encode("utf-8")) > 1_000_000:
        return {"ok": False, "error": "Proposed file exceeds 1 MB limit"}
    base = resolve_allowed_path(root)
    target = resolve_allowed_path(root, path, must_exist=False)
    if target == base:
        return {"ok": False, "error": "Cannot write to the project root itself"}
    if not target.parent.exists() or not target.parent.is_dir():
        return {"ok": False, "error": "Parent directory must already exist; directory creation is disabled"}
    # Resolve the parent separately to block links/junctions that lead outside the root.
    safe_parent = resolve_allowed_path(root, target.parent, must_exist=True)
    target = safe_parent / target.name
    exists = target.exists()
    if exists and not target.is_file():
        return {"ok": False, "error": "Target exists but is not a regular file"}
    old = ""
    original_bytes = b''
    if exists:
        if target.stat().st_size > max_existing_bytes:
            return {"ok": False, "error": f"Existing file is too large to safely preview (limit {max_existing_bytes} bytes)"}
        try:
            with target.open('rb') as source:
                original_bytes = source.read(max_existing_bytes + 1)
            if len(original_bytes) > max_existing_bytes:
                return {"ok": False, "error": "Existing file grew beyond the preview limit"}
            old = original_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return {"ok": False, "error": "Existing file is not UTF-8 text; refusing to replace it"}
    diff = "".join(difflib.unified_diff(
        old.splitlines(keepends=True), content.splitlines(keepends=True),
        fromfile=f"a/{target.relative_to(base).as_posix()}" if exists else "/dev/null",
        tofile=f"b/{target.relative_to(base).as_posix()}",
    ))
    relative = target.relative_to(base).as_posix()
    snapshot = {'path': relative, 'exists': exists,
                'sha256': hashlib.sha256(original_bytes).hexdigest() if exists else None,
                'proposed_sha256': hashlib.sha256(content.encode('utf-8')).hexdigest()}
    return {"ok": True, "path": relative, "exists": exists, "diff": diff or "(No textual changes)",
            'snapshot': snapshot}


def write_file(root, path, content, overwrite=False, *, approved=False, expected_snapshot=None, max_existing_bytes=MAX_READ_BYTES):
    """Write UTF-8 text atomically; deny by default unless the GUI explicitly approved."""
    if not approved:
        return {"ok": False, "error": "User approval is required before writing a file", "code": "APPROVAL_REQUIRED"}
    if not isinstance(expected_snapshot, dict):
        return {"ok": False, "error": "A matching preview snapshot is required", "code": "APPROVAL_SNAPSHOT_REQUIRED"}
    preview = preview_file_change(root, path, content, max_existing_bytes=max_existing_bytes)
    if not preview.get("ok"):
        return preview
    if preview['snapshot'] != expected_snapshot:
        return {'ok': False, 'code': 'FILE_CHANGED',
                'error': 'Файл или предложение изменились после показа diff. Запись отменена; запросите новый diff и подтвердите его заново.'}
    if preview["exists"] and not overwrite:
        return {"ok": False, "error": "File already exists; set overwrite=true and obtain user approval before replacing it"}
    base = resolve_allowed_path(root)
    target = resolve_allowed_path(root, path, must_exist=False)
    parent = resolve_allowed_path(root, target.parent, must_exist=True)
    target = parent / target.name
    # Re-check destination just before writing.
    if target.exists() and not overwrite:
        return {"ok": False, "error": "File already exists; overwrite was not authorized"}
    data = content.encode("utf-8")
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=str(parent), prefix=".local-agent-tmp-", delete=False) as temp:
            temp_name = temp.name
            temp.write(data)
            temp.flush()
            os.fsync(temp.fileno())
        # Resolve once more immediately before replace, guarding against path redirection.
        current = preview_file_change(root, path, content, max_existing_bytes=max_existing_bytes)
        if not current.get('ok') or current.get('snapshot') != expected_snapshot or resolve_allowed_path(root, path, must_exist=False) != target:
            return {'ok': False, 'code': 'FILE_CHANGED',
                    'error': 'Файл изменился перед записью. Обновите diff и подтвердите изменение заново.'}
        if target.exists() and not overwrite:
            return {"ok": False, "error": "File appeared during write; refusing to overwrite"}
        if expected_snapshot['exists']:
            for attempt in range(5):
                try:
                    os.replace(temp_name, target)
                    break
                except PermissionError as exc:
                    if os.name!='nt' or getattr(exc,'winerror',None) not in (5,32) or attempt==4:raise
                    import time
                    time.sleep(.01*(2**attempt))
                    fresh=preview_file_change(root,path,content,max_existing_bytes=max_existing_bytes)
                    if not fresh.get('ok') or fresh.get('snapshot')!=expected_snapshot or resolve_allowed_path(root,path,must_exist=False)!=target:
                        return {'ok':False,'code':'FILE_CHANGED','error':'Файл изменился во время ожидания Windows file lock; требуется новый diff'}
            temp_name = None
        else:
            # Atomic create-only operation: never overwrite a file created after recheck.
            try:
                if os.name == 'nt':
                    # Windows rename refuses an existing destination, unlike POSIX rename.
                    os.rename(temp_name, target)
                    temp_name = None
                else:
                    os.link(temp_name, target)
            except FileExistsError:
                return {'ok': False, 'code': 'FILE_CHANGED', 'error': 'Файл появился перед записью; требуется новый diff.'}
    finally:
        if temp_name and os.path.exists(temp_name):
            try: os.unlink(temp_name)
            except OSError: pass
    from .project_index import notify_paths
    notify_paths(base,[target.relative_to(base).as_posix()])
    return {"ok": True, "path": target.relative_to(base).as_posix(), "bytes_written": len(data), "overwrote_existing_file": preview["exists"]}


TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "list_files", "description": "List files/directories inside the selected project only.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Relative project path; default ."}, "recursive": {"type": "boolean"}}, "required": []}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a UTF-8 text file inside the selected project only.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "search_text", "description": "Search text in files inside the selected project only.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "path": {"type": "string"}, "case_sensitive": {"type": "boolean"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Propose writing UTF-8 text to a file inside the selected project. The application will show a diff and ask the user for approval before writing. Parent directories must already exist.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Path relative to the project root"}, "content": {"type": "string"}, "overwrite": {"type": "boolean", "description": "Set true only when replacing an existing file is intended"}}, "required": ["path", "content", "overwrite"]}}},
]


def workspace_tool(name,description,properties,required):
    return {'type':'function','function':{'name':name,'description':description,'parameters':
        {'type':'object','properties':properties,'required':required,'additionalProperties':False}}}


_PATH={'type':'string','minLength':1,'maxLength':1000}
_HASH={'type':'string','pattern':'^[a-fA-F0-9]{64}$'}
TOOL_DEFINITIONS[2]=workspace_tool('search_text','Литеральный поиск текста в проекте с маской файлов, лимитом результатов и возможностью остановки.',
    {'query':{'type':'string','minLength':1,'maxLength':200},'path':_PATH,'pattern':{'type':'string','maxLength':120},
     'case_sensitive':{'type':'boolean'},'limit':{'type':'integer','minimum':1,'maximum':200},
     'max_depth':{'type':'integer','minimum':0,'maximum':30}},['query'])
TOOL_DEFINITIONS.extend([
    workspace_tool('search_files','Найти сохранённые файлы по части пути через индекс проекта; при его недоступности используется ограниченный обычный поиск.',{'query':{'type':'string','maxLength':200},'path':_PATH,'limit':{'type':'integer','minimum':1,'maximum':200}},['query']),
    workspace_tool('search_symbols','Найти определения функций, классов, методов, импортов/экспортов Python/JS/TS. Возвращает точный диапазон и SHA256; это синтаксический индекс, не семантические references.',{'query':{'type':'string','minLength':1,'maxLength':200},'path':_PATH,'limit':{'type':'integer','minimum':1,'maximum':200}},['query']),
    workspace_tool('project_outline','Карта определений сохранённого проекта или выбранной папки/файла. При неполном индексе не утверждай, что определений нет.',{'path':_PATH,'limit':{'type':'integer','minimum':1,'maximum':200}},[]),
    workspace_tool('glob_files','Найти файлы по маске проекта: *.py, src/**/*.ts. Без чтения содержимого; поиск можно остановить.',
        {'pattern':{'type':'string','minLength':1,'maxLength':120},'path':_PATH,'limit':{'type':'integer','minimum':1,'maximum':2000},'max_depth':{'type':'integer','minimum':0,'maximum':30}},['pattern']),
    workspace_tool('read_range','Прочитать точный диапазон UTF-8 файла без обрезания строк. Возвращает SHA256 всей ревизии и next_line.',
        {'path':_PATH,'start_line':{'type':'integer','minimum':1},'end_line':{'type':'integer','minimum':1}},['path']),
    workspace_tool('patch_file','Точечно заменить один уникальный old_text на new_text. Сначала прочитай нужный диапазон; для ревизии передай sha256. Перед записью будет diff и согласие.',
        {'path':_PATH,'old_text':{'type':'string','minLength':1,'maxLength':1000000},'new_text':{'type':'string','maxLength':1000000},'expected_sha256':_HASH},['path','old_text','new_text']),
    workspace_tool('create_directory','Создать вложенные каталоги проекта с предварительным просмотром и подтверждением. Уже существующий каталог не меняется.',{'path':_PATH},['path']),
    workspace_tool('rename_file','Переместить обычный файл внутри проекта с preview и подтверждением. Не заменяет существующий файл; каталог назначения должен существовать.',
        {'path':_PATH,'destination':_PATH,'expected_sha256':_HASH},['path','destination']),
    workspace_tool('delete_file','Удалить один UTF-8 файл проекта после просмотра diff и отдельного подтверждения. Каталоги рекурсивно не удаляются.',
        {'path':_PATH,'expected_sha256':_HASH},['path']),
    workspace_tool('get_project_instructions','Прочитать применимые AGENTS.md от корня до выбранного пути. Они не расширяют доступ инструментов.',{'path':_PATH},[]),
])


def execute_tool(name, arguments, project_root, settings=None, *, approved=False, expected_snapshot=None, cancelled=None):
    """Single dispatch point: every file tool must enforce the selected root."""
    settings = settings or {}
    max_entries = int(settings.get("max_entries", 200))
    max_search_depth = int(settings.get("max_search_depth", 5))
    try:
        if name == "list_files":
            return list_files(project_root, arguments.get("path", "."), bool(arguments.get("recursive", False)), max_entries, max_search_depth)
        if name == "read_file":
            return read_file(project_root, arguments["path"])
        if name == "search_text":
            return search_text(project_root, arguments["query"], arguments.get("path", "."), bool(arguments.get("case_sensitive", False)), arguments.get('max_depth',max_search_depth), cancelled, arguments.get("pattern",""), arguments.get("limit",200))
        if name == 'glob_files':
            from .workspace_search import search_project
            return search_project(project_root,{'mode':'files','query':'','pattern':arguments['pattern'],
                'path':arguments.get('path','.'),'limit':arguments.get('limit',1000),'max_depth':arguments.get('max_depth',max_search_depth)},cancelled)
        if name == 'read_range':
            from .workspace_read import read_range
            return read_range(project_root,arguments['path'],arguments.get('start_line',1),arguments.get('end_line'),cancelled)
        if name in ('search_files','search_symbols','project_outline'):
            from .workspace_search import search_project
            mode={'search_files':'files','search_symbols':'symbols','project_outline':'outline'}[name]
            from .project_index import get_index
            index=get_index(project_root,create=True)
            return search_project(project_root,{**arguments,'query':arguments.get('query',''),'mode':mode},cancelled)
        if name in ('patch_file','create_directory','rename_file','delete_file'):
            from .workspace_edits import apply_mutation
            result=apply_mutation(project_root,name,arguments,approved=approved,expected_snapshot=expected_snapshot,cancelled=cancelled)
            if result.get('ok'):
                from .project_index import notify_paths
                notify_paths(project_root,[p for p in (arguments.get('path'),arguments.get('destination')) if p])
            return result
        if name == "write_file":
            if not approved:
                return {"ok": False, "error": "User approval is required before writing a file", "code": "APPROVAL_REQUIRED"}
            return write_file(project_root, arguments["path"], arguments["content"], bool(arguments.get("overwrite", False)),
                              approved=approved, expected_snapshot=expected_snapshot)
        return {"ok": False, "error": f"Unknown tool: {name}"}
    except AccessDenied as exc:
        return {"ok": False, "error": str(exc), "code": "ACCESS_DENIED"}
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError, PermissionError, OSError, KeyError, ValueError) as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def run_sandbox_self_test():
    """Run isolated security checks using temporary folders; never touches user files."""
    import tempfile
    import unittest

    class SandboxTests(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.TemporaryDirectory(prefix="local_agent_sandbox_test_")
            self.base = Path(self.temp.name) / "project"
            self.outside = Path(self.temp.name) / "outside"
            self.base.mkdir(); self.outside.mkdir()
            (self.base / "inside.txt").write_text("sandbox test marker", encoding="utf-8")
            (self.outside / "outside.txt").write_text("must not be read", encoding="utf-8")
        def tearDown(self): self.temp.cleanup()
        def test_read_inside_allowed(self): self.assertTrue(read_file(self.base, "inside.txt")["ok"])
        def test_parent_traversal_denied(self):
            with self.assertRaises(AccessDenied): resolve_allowed_path(self.base, "../outside/outside.txt", must_exist=True)
        def test_absolute_outside_denied(self):
            with self.assertRaises(AccessDenied): resolve_allowed_path(self.base, self.outside / "outside.txt", must_exist=True)
        def test_list_outside_denied(self):
            result = execute_tool("list_files", {"path": str(self.outside)}, self.base)
            self.assertFalse(result["ok"]); self.assertEqual(result.get("code"), "ACCESS_DENIED")
        def test_search_outside_denied(self):
            result = execute_tool("search_text", {"query": "must not", "path": str(self.outside)}, self.base)
            self.assertFalse(result["ok"]); self.assertEqual(result.get("code"), "ACCESS_DENIED")
        def test_symlink_escape_denied(self):
            link = self.base / "escape_link"
            try: link.symlink_to(self.outside, target_is_directory=True)
            except (OSError, NotImplementedError): self.skipTest("Symlink creation not permitted on this Windows setup")
            with self.assertRaises(AccessDenied): resolve_allowed_path(self.base, "escape_link/outside.txt", must_exist=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SandboxTests)
    stream = __import__("io").StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {"ok": result.wasSuccessful(), "passed": result.testsRun - len(result.failures) - len(result.errors), "failed": len(result.failures) + len(result.errors), "skipped": len(result.skipped), "details": stream.getvalue()}
