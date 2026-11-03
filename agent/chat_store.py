"""Transactional chat history for Neutral.

Chats are stored outside projects under the user's application data directory.
Only conversation metadata and model messages are stored; project files are not copied.
"""
from __future__ import annotations
import json, os, tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "LocalCodingAgent"
CHAT_DIR = APP_DIR / "chats"
INDEX_FILE = CHAT_DIR / "index.json"
STORE_LOCK = threading.RLock()


def _valid_id(chat_id):
    return isinstance(chat_id, str) and len(chat_id) == 32 and all(c in '0123456789abcdef' for c in chat_id)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.stem + "_", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _database():
    """Use the current chat-directory profile, including isolated test profiles."""
    from .storage import Storage
    return Storage(CHAT_DIR.parent).ready()


def list_chats():
    return read_chat_catalog()['chats']


def read_chat_catalog(**scope):
    """Read indexed metadata; legacy files are visited only by the first migration."""
    return _database().catalog(**scope)


def search_chats(query, **scope):
    """Search persisted title/user/assistant text without loading transcripts."""
    return _database().search(query, **scope)


def create_chat(project_root: str = "", model: str = "", title: str = "Новый чат", mode=None) -> dict[str, Any]:
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
        "mode": mode or ("ide" if project_root else "chat"),
    }
    with STORE_LOCK:
        database = _database()
        with database.transaction() as connection:
            database.write_chat(connection, record)
    return record


def load_chat(chat_id: str) -> dict[str, Any] | None:
    if not _valid_id(chat_id):
        return None
    return _database().load_chat(chat_id)


def save_chat(chat: dict[str, Any], *, checkpoint=True) -> str | None:
    """Atomically save history/index and an explicitly updated checkpoint."""
    chat = dict(chat)
    if not _valid_id(chat.get('id')):
        raise ValueError('Некорректный идентификатор чата')
    chat['updated_at'] = _now()
    with STORE_LOCK:
        database = _database()
        with database.transaction() as connection:
            database.write_chat(connection, chat, checkpoint=checkpoint)
    return None


def delete_chat(chat_id: str) -> bool:
    """Delete canonical history, checkpoints and receipts in a single transaction.

    Legacy migration sources are retained as backups and are never reimported.
    Immutable artifact bytes are retained for backups; no automatic garbage collection.
    """
    if not _valid_id(chat_id):
        return False
    with STORE_LOCK:
        database = _database()
        with database.transaction() as connection:
            connection.execute('DELETE FROM chats WHERE id=?', (chat_id,))
            connection.execute('DELETE FROM tasks WHERE chat_id=?', (chat_id,))
            connection.execute('DELETE FROM tasks WHERE chat_id IN (SELECT id FROM runs WHERE chat_id=? AND parent_id IS NOT NULL)',(chat_id,))
            connection.execute('DELETE FROM journal_events WHERE chat_id IN (SELECT id FROM runs WHERE chat_id=? AND parent_id IS NOT NULL)',(chat_id,))
            connection.execute('DELETE FROM inference_attempts WHERE run_id IN (SELECT id FROM runs WHERE chat_id=?)',(chat_id,))
            connection.execute('DELETE FROM runs WHERE chat_id=?',(chat_id,))
            connection.execute('DELETE FROM workspace_snapshots WHERE chat_id=?', (chat_id,))
            connection.execute('DELETE FROM journal_events WHERE chat_id=?', (chat_id,))
            connection.execute('INSERT OR IGNORE INTO chat_tombstones VALUES(?)', (chat_id,))
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
