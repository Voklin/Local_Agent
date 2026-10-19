"""Persistent task/checkpoint state for Local Coding Agent.

Task state is stored outside project folders. It is deliberately compact: no raw
file contents or tool output are persisted here. A task can therefore survive an
agent interruption and be resumed from the chat UI.
"""
from __future__ import annotations
import hashlib, json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "LocalCodingAgent"
TASK_DIR = APP_DIR / "tasks"

def _now():
    return datetime.now(timezone.utc).isoformat()

def _key(chat_id: str) -> str:
    return hashlib.sha256(str(chat_id).encode("utf-8", errors="replace")).hexdigest()[:32]

def task_path(chat_id: str) -> Path:
    return TASK_DIR / (_key(chat_id) + ".json")

def default_stages():
    return [
        {"id":"analysis","title":"Анализ задачи","status":"pending"},
        {"id":"research","title":"Исследование проекта","status":"pending"},
        {"id":"implementation","title":"Реализация изменений","status":"pending"},
        {"id":"verification","title":"Проверка и тесты","status":"pending"},
        {"id":"finish","title":"Завершение","status":"pending"},
    ]

def new_task(chat_id, project_root, prompt):
    return {
        "version": 1, "chat_id": str(chat_id), "project_root": str(project_root),
        "prompt": str(prompt)[:10000], "status": "running",
        "stage": "analysis", "turn": 0, "tool_calls": 0,
        "started_at": _now(), "updated_at": _now(), "stages": default_stages(),
        "last_event": "Задача запущена", "stop_reason": "",
    }

def save_task(task):
    task = dict(task)
    task["updated_at"] = _now()
    path = task_path(task.get("chat_id",""))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="task_",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(task,f,ensure_ascii=False,indent=2)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    return task

def load_task(chat_id):
    try:
        data=json.loads(task_path(chat_id).read_text(encoding="utf-8"))
        return data if isinstance(data,dict) else None
    except (OSError,json.JSONDecodeError):
        return None

def clear_task(chat_id):
    try: task_path(chat_id).unlink(missing_ok=True)
    except OSError: pass

def set_stage(task, stage_id, status="active", event=""):
    order=[s["id"] for s in task.get("stages",[])]
    if stage_id in order:
        idx=order.index(stage_id)
        for i,s in enumerate(task["stages"]):
            if i<idx and s.get("status")!="done": s["status"]="done"
            if i==idx: s["status"]=status
        task["stage"]=stage_id
    if event: task["last_event"]=str(event)[:500]
    return task

def finish_task(task, status="completed", reason=""):
    for s in task.get("stages",[]):
        s["status"]="done"
    task["status"]=status
    task["stage"]="finish"
    task["stop_reason"]=str(reason)[:500]
    task["last_event"]="Задача завершена" if status=="completed" else str(reason)[:500]
    return save_task(task)
