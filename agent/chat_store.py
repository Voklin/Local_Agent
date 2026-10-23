"""Persistent chat history for Local Coding Agent.

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


def _load_index() -> list[dict[str, Any]]:
    if not INDEX_FILE.exists():
        return []
    try:
        data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return [x for x in data if isinstance(x, dict) and _valid_id(x.get('id'))] if isinstance(data, list) else []
    except (OSError, ValueError, UnicodeError):
        return []


def list_chats() -> list[dict[str, Any]]:
    return read_chat_catalog()['chats']


def _metadata(chat):
    return {**{k: str(chat.get(k, '')) for k in ('id', 'title', 'created_at', 'updated_at', 'project_root', 'model')}, 'mode': chat.get('mode', 'ide' if chat.get('project_root') else 'chat')}


def _cache_chat(chat=None, deleted_id=None):
    """Update the derived index; a cache failure must not undo a saved transcript."""
    try:
        key = chat['id'] if chat else deleted_id
        index = [x for x in _load_index() if x.get('id') != key]
        if chat:
            index.append(_metadata(chat))
        _atomic_write(INDEX_FILE, index)
    except OSError as exc:
        return f'Чат сохранён, но индекс не обновлён: {type(exc).__name__}. Список будет восстановлен из файлов чатов.'
    return None


def read_chat_catalog():
    """Rebuild disposable metadata from canonical chat files; preserve corrupt files."""
    with STORE_LOCK:
        records, warnings = [], []
        try:
            paths = sorted(CHAT_DIR.iterdir())
        except FileNotFoundError:
            paths = []
        for path in paths:
            if path.suffix != '.json' or not _valid_id(path.stem):
                continue
            try:
                chat = load_chat(path.stem)
                if chat:
                    records.append(_metadata(chat))
            except (OSError, ValueError) as exc:
                warnings.append(f'Чат {path.stem} не прочитан ({type(exc).__name__}); исходный файл сохранён.')
        if sorted(_load_index(), key=lambda x: x['id']) != sorted(records, key=lambda x: x['id']):
            try:
                _atomic_write(INDEX_FILE, records)
            except OSError as exc:
                warnings.append(f'Индекс чатов не восстановлен ({type(exc).__name__}); показаны данные исходных файлов.')
        return {'chats': sorted(records, key=lambda x: x['updated_at'], reverse=True), 'warnings': warnings}


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
        _atomic_write(CHAT_DIR / f"{chat_id}.json", record)
        warning = _cache_chat(record)
    if warning:
        record['storage_warning'] = warning
    return record


def load_chat(chat_id: str) -> dict[str, Any] | None:
    if not _valid_id(chat_id):
        return None
    path = CHAT_DIR / f"{chat_id}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get('id') != chat_id or not isinstance(data.get('messages'), list) or not all(isinstance(m, dict) for m in data['messages']):
            raise ValueError('Некорректная структура чата; исходный файл сохранён')
        return data
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError('Данные чата повреждены; исходный файл сохранён для восстановления') from exc


def save_chat(chat: dict[str, Any]) -> str | None:
    chat = dict(chat)
    if not _valid_id(chat.get('id')):
        raise ValueError('Некорректный идентификатор чата')
    chat["updated_at"] = _now()
    chat.pop('storage_warning', None)
    with STORE_LOCK:
        _atomic_write(CHAT_DIR / f"{chat['id']}.json", chat)
        return _cache_chat(chat)


def delete_chat(chat_id: str) -> bool:
    if not _valid_id(chat_id):
        return False
    path = CHAT_DIR / f"{chat_id}.json"
    try:
        with STORE_LOCK:
            path.unlink(missing_ok=True)
            _cache_chat(deleted_id=chat_id)
    except OSError:
        return False
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
