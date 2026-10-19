"""Persistent chat history for Local Coding Agent.

Chats are stored outside projects under the user's application data directory.
Only conversation metadata and model messages are stored; project files are not copied.
"""
from __future__ import annotations
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "LocalCodingAgent"
CHAT_DIR = APP_DIR / "chats"
INDEX_FILE = CHAT_DIR / "index.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.stem + "_", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _load_index() -> list[dict[str, Any]]:
    if not INDEX_FILE.exists():
        return []
    try:
        data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def list_chats() -> list[dict[str, Any]]:
    return sorted(_load_index(), key=lambda x: x.get("updated_at", ""), reverse=True)


def create_chat(project_root: str = "", model: str = "", title: str = "Новый чат") -> dict[str, Any]:
    import uuid
    chat_id = uuid.uuid4().hex
    now = _now()
    record = {
        "id": chat_id,
        "title": title or "Новый чат",
        "created_at": now,
        "updated_at": now,
        "project_root": str(project_root),
        "model": str(model),
        "messages": [],
    }
    _atomic_write(CHAT_DIR / f"{chat_id}.json", record)
    index = _load_index()
    index.append({k: record[k] for k in ("id", "title", "created_at", "updated_at", "project_root", "model")})
    _atomic_write(INDEX_FILE, index)
    return record


def load_chat(chat_id: str) -> dict[str, Any] | None:
    path = CHAT_DIR / f"{chat_id}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def save_chat(chat: dict[str, Any]) -> None:
    chat = dict(chat)
    chat["updated_at"] = _now()
    _atomic_write(CHAT_DIR / f"{chat['id']}.json", chat)
    index = [x for x in _load_index() if x.get("id") != chat["id"]]
    index.append({k: chat.get(k, "") for k in ("id", "title", "created_at", "updated_at", "project_root", "model")})
    _atomic_write(INDEX_FILE, index)


def delete_chat(chat_id: str) -> bool:
    path = CHAT_DIR / f"{chat_id}.json"
    try:
        path.unlink(missing_ok=True)
    except OSError:
        return False
    _atomic_write(INDEX_FILE, [x for x in _load_index() if x.get("id") != chat_id])
    return True


def rename_chat(chat_id: str, title: str) -> dict[str, Any] | None:
    chat = load_chat(chat_id)
    if not chat: return None
    chat["title"] = (title or "Новый чат").strip()[:120] or "Новый чат"
    save_chat(chat)
    return chat


def title_from_messages(messages: list[dict[str, Any]]) -> str:
    for msg in messages:
        if msg.get("role") == "user" and isinstance(msg.get("content"), str):
            text = " ".join(msg["content"].split())
            if text:
                return text[:80] + ("…" if len(text) > 80 else "")
    return "Новый чат"
