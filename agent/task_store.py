"""Persistent task/checkpoint state for Local Coding Agent.

Task state is stored in the profile SQLite database outside project folders.
It contains compact UI metadata; full durable receipts live in the call journal.
The legacy task_path helper is retained for migration and recovery diagnostics.
"""
from __future__ import annotations
import hashlib, os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .planner import build_plan

APP_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "LocalCodingAgent"
TASK_DIR = APP_DIR / "tasks"

def _now():
    return datetime.now(timezone.utc).isoformat()

def _key(chat_id: str) -> str:
    return hashlib.sha256(str(chat_id).encode("utf-8", errors="replace")).hexdigest()[:32]

def task_path(chat_id: str) -> Path:
    return TASK_DIR / (_key(chat_id) + ".json")

def default_stages(prompt=""):
    return build_plan(prompt)

def new_task(chat_id, project_root, prompt):
    return {
        "version": 2, "verification_schema":2, "runtime_version": "5.7", "chat_id": str(chat_id), "project_root": str(project_root),
        "journal_id": uuid.uuid4().hex, "run_state": "running", "recovery_items": [],
        "prompt": str(prompt)[:50000], "status": "running",
        "stage": "analysis", "turn": 0, "tool_calls": 0,
        "started_at": _now(), "updated_at": _now(), "stages": default_stages(prompt),
        "selected_skills": [], "decisions": [], "discovered_files": [], "modified_files": [],
        "test_results": [], "resume_state": {"next_action": "Начать текущий этап", "attempt": 0},
        "last_event": "Задача запущена", "stop_reason": "",
        "tool_activity": [], "activity_sequence": 0, "activity_omitted": 0,
    }

def _database():
    """Resolve the current task profile without sharing test or user connections."""
    from .storage import Storage
    return Storage(TASK_DIR.parent).ready()


def save_task(task):
    """Commit the canonical checkpoint; return the timestamped saved snapshot."""
    task = dict(task)
    task['updated_at'] = _now()
    identity = str(task.get('chat_id', ''))
    if not identity:
        raise ValueError('Checkpoint requires chat_id')
    from .storage import encode
    database = _database()
    with database.transaction() as connection:
        connection.execute('INSERT INTO tasks VALUES(?,?) ON CONFLICT(chat_id) DO UPDATE SET data=excluded.data', (identity, encode(task)))
    return task


def load_task(chat_id):
    database = _database()
    with database.transaction() as connection:
        return database.checkpoint(connection, chat_id)


def clear_task(chat_id):
    database = _database()
    with database.transaction() as connection:
        connection.execute('DELETE FROM tasks WHERE chat_id=?', (str(chat_id),))


def set_stage(task, stage_id, status="active", event=""):
    order=[s["id"] for s in task.get("stages",[])]
    if stage_id in order:
        idx=order.index(stage_id)
        for i,s in enumerate(task["stages"]):
            if s.get("status") == "active" and i != idx: s["status"]="done"
            if i<idx and s.get("status")=="pending": s["status"]="skipped"
            if i==idx: s["status"]=status
        task["stage"]=stage_id
    if event: task["last_event"]=str(event)[:500]
    return task

def finish_task(task, status="completed", reason=""):
    for s in task.get("stages",[]):
        if s.get('status') == 'active' or s.get('id') == 'finish': s['status']='done'
        elif s.get('status') == 'pending': s['status']='skipped'
    task["status"]=status
    task["stage"]="finish"
    task["stop_reason"]=str(reason)[:500]
    task["last_event"]="Задача завершена" if status=="completed" else str(reason)[:500]
    if status == 'completed' and task.get('verification', {}).get('status') == 'not_run':
        task['last_event'] = 'Ответ получен; проверка результата не подтверждена'
    return save_task(task)
