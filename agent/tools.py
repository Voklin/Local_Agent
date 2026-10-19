from pathlib import Path
import os
from .security import AccessDenied, resolve_allowed_path

MAX_READ_BYTES = 120_000
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".idea", ".vscode"}


def list_files(root, path=".", recursive=False):
    target = resolve_allowed_path(root, path, must_exist=True)
    if not target.is_dir():
        return {"ok": False, "error": "Path is not a directory"}
    results = []
    iterator = target.rglob("*") if recursive else target.iterdir()
    for item in iterator:
        try:
            safe = resolve_allowed_path(root, item, must_exist=True)
        except (AccessDenied, OSError):
            continue  # do not follow symlinks/junctions that escape the root
        if any(part in IGNORED_DIRS for part in safe.relative_to(resolve_allowed_path(root)).parts):
            continue
        rel = safe.relative_to(resolve_allowed_path(root)).as_posix()
        results.append({"path": rel, "type": "directory" if safe.is_dir() else "file"})
        if len(results) >= 2000:
            break
    return {"ok": True, "root": str(resolve_allowed_path(root)), "path": str(target.relative_to(resolve_allowed_path(root)) or "."), "entries": results}


def read_file(root, path):
    target = resolve_allowed_path(root, path, must_exist=True)
    if not target.is_file():
        return {"ok": False, "error": "Path is not a file"}
    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        return {"ok": False, "error": f"File is too large ({size} bytes; limit {MAX_READ_BYTES})"}
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"ok": False, "error": "File is not UTF-8 text"}
    return {"ok": True, "path": target.relative_to(resolve_allowed_path(root)).as_posix(), "content": content}


def search_text(root, query, path=".", case_sensitive=False):
    if not query:
        return {"ok": False, "error": "query must not be empty"}
    target = resolve_allowed_path(root, path, must_exist=True)
    if not target.is_dir() and not target.is_file():
        return {"ok": False, "error": "Path is not a file or directory"}
    files = [target] if target.is_file() else target.rglob("*")
    needle = query if case_sensitive else query.casefold()
    matches = []
    for file in files:
        if not file.is_file():
            continue
        try:
            safe = resolve_allowed_path(root, file, must_exist=True)
        except (AccessDenied, OSError):
            continue
        if any(part in IGNORED_DIRS for part in safe.relative_to(resolve_allowed_path(root)).parts):
            continue
        try:
            if safe.stat().st_size > MAX_READ_BYTES:
                continue
            lines = safe.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(lines, 1):
            haystack = line if case_sensitive else line.casefold()
            if needle in haystack:
                matches.append({"path": safe.relative_to(resolve_allowed_path(root)).as_posix(), "line": number, "text": line[:500]})
                if len(matches) >= 200:
                    return {"ok": True, "matches": matches, "truncated": True}
    return {"ok": True, "matches": matches, "truncated": False}


TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "list_files", "description": "List files/directories inside the selected project only.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Relative project path; default ."}, "recursive": {"type": "boolean"}}, "required": []}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a UTF-8 text file inside the selected project only.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "search_text", "description": "Search text in files inside the selected project only.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "path": {"type": "string"}, "case_sensitive": {"type": "boolean"}}, "required": ["query"]}}},
]


def execute_tool(name, arguments, project_root):
    """Single dispatch point: every file tool must enforce the selected root."""
    try:
        if name == "list_files":
            return list_files(project_root, arguments.get("path", "."), bool(arguments.get("recursive", False)))
        if name == "read_file":
            return read_file(project_root, arguments["path"])
        if name == "search_text":
            return search_text(project_root, arguments["query"], arguments.get("path", "."), bool(arguments.get("case_sensitive", False)))
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
