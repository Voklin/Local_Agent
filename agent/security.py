"""Path security for the local coding agent.

All file tools must resolve paths through resolve_allowed_path before accessing them.
This is an application-level sandbox, not an OS security boundary: do not expose a
shell tool without separate command controls or run the app with elevated privileges.
"""
from pathlib import Path

class AccessDenied(PermissionError):
    pass


def canonical_root(root: str | Path) -> Path:
    p = Path(root).expanduser().resolve(strict=True)
    if not p.is_dir():
        raise NotADirectoryError(f"Project root is not a directory: {p}")
    return p


def resolve_allowed_path(root: str | Path, requested: str | Path = ".", *, must_exist: bool = False) -> Path:
    base = canonical_root(root)
    raw = Path(requested).expanduser()
    # Relative paths are rooted inside the selected project. Absolute paths are accepted
    # only when their resolved destination remains within the project root.
    candidate = raw if raw.is_absolute() else base / raw
    try:
        resolved = candidate.resolve(strict=must_exist)
    except (OSError, RuntimeError) as exc:
        raise AccessDenied(f"Cannot safely resolve path: {requested}") from exc
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise AccessDenied(f"Access denied: path is outside the selected project directory: {requested}") from exc
    return resolved
