"""Sandboxed text-file operations used by the built-in editor."""
from pathlib import Path
from .security import AccessDenied, resolve_allowed_path

MAX_EDITOR_FILE_BYTES = 2 * 1024 * 1024


def read_project_text(project_root: str | Path, requested: str | Path, *, max_bytes: int = MAX_EDITOR_FILE_BYTES) -> tuple[Path, str]:
    path = resolve_allowed_path(project_root, requested, must_exist=True)
    if not path.is_file():
        raise ValueError("Path is not a file.")
    if path.stat().st_size > max_bytes:
        raise ValueError(f"File exceeds editor limit ({max_bytes} bytes).")
    return path, path.read_text(encoding="utf-8")


def save_project_text(project_root: str | Path, requested: str | Path, text: str) -> Path:
    path = resolve_allowed_path(project_root, requested, must_exist=True)
    if not path.is_file():
        raise ValueError("Path is not an existing file.")
    # Re-resolve immediately before writing so a replaced symlink cannot redirect the save.
    path = resolve_allowed_path(project_root, path, must_exist=True)
    path.write_text(text, encoding="utf-8", newline="")
    return path
