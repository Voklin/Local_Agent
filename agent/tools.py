from __future__ import annotations

from pathlib import Path
from typing import Any


MAX_READ_BYTES = 120_000
MAX_SEARCH_RESULTS = 100
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".idea", ".vscode"}


def _safe_path(root: Path, relative_path: str) -> Path:
    root = root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError("Access denied: path is outside the selected project directory.")
    return candidate


def list_files(root: Path, path: str = ".", recursive: bool = False) -> dict[str, Any]:
    target = _safe_path(root, path)
    if not target.exists():
        return {"error": f"Path does not exist: {path}"}
    if not target.is_dir():
        return {"error": f"Not a directory: {path}"}

    results: list[dict[str, str]] = []
    iterator = target.rglob("*") if recursive else target.iterdir()
    for item in iterator:
        try:
            rel = item.relative_to(root).as_posix()
            if any(part in IGNORED_DIRS for part in Path(rel).parts):
                continue
            results.append({"path": rel, "type": "directory" if item.is_dir() else "file"})
            if len(results) >= 300:
                break
        except (OSError, PermissionError):
            continue
    return {"root": str(root), "path": path, "items": results, "truncated": len(results) >= 300}


def read_file(root: Path, path: str) -> dict[str, Any]:
    target = _safe_path(root, path)
    if not target.exists():
        return {"error": f"File does not exist: {path}"}
    if not target.is_file():
        return {"error": f"Not a file: {path}"}
    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        return {"error": f"File is {size} bytes; limit is {MAX_READ_BYTES} bytes. Search or inspect a smaller file."}
    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"error": str(exc)}
    return {"path": target.relative_to(root.resolve()).as_posix(), "bytes": size, "content": content}


def search_text(root: Path, query: str, path: str = ".", case_sensitive: bool = False) -> dict[str, Any]:
    target = _safe_path(root, path)
    if not target.exists():
        return {"error": f"Path does not exist: {path}"}
    candidates = target.rglob("*") if target.is_dir() else [target]
    matches: list[dict[str, Any]] = []
    needle = query if case_sensitive else query.casefold()
    for file in candidates:
        if not file.is_file():
            continue
        try:
            rel_parts = file.relative_to(root.resolve()).parts
            if any(part in IGNORED_DIRS for part in rel_parts):
                continue
            if file.stat().st_size > MAX_READ_BYTES:
                continue
            content = file.read_text(encoding="utf-8", errors="replace")
        except (OSError, PermissionError, ValueError):
            continue
        for line_no, line in enumerate(content.splitlines(), start=1):
            haystack = line if case_sensitive else line.casefold()
            if needle in haystack:
                matches.append({"path": file.relative_to(root.resolve()).as_posix(), "line": line_no, "text": line[:400]})
                if len(matches) >= MAX_SEARCH_RESULTS:
                    return {"query": query, "matches": matches, "truncated": True}
    return {"query": query, "matches": matches, "truncated": False}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories inside the selected project. Use path='.' for project root. recursive=true searches subdirectories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path inside the project, default '.'"},
                    "recursive": {"type": "boolean", "description": "Whether to include descendants"}
                },
                "required": ["path", "recursive"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file inside the selected project. Only use a relative path.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_text",
            "description": "Search for a text string in files inside the selected project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "path": {"type": "string", "description": "Relative file or directory path, default '.'"},
                    "case_sensitive": {"type": "boolean"}
                },
                "required": ["query", "path", "case_sensitive"],
                "additionalProperties": False
            }
        }
    }
]


def execute_tool(root: Path, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "list_files":
        return list_files(root, **arguments)
    if name == "read_file":
        return read_file(root, **arguments)
    if name == "search_text":
        return search_text(root, **arguments)
    return {"error": f"Unknown tool: {name}"}
