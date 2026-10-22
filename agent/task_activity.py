"""Bounded tool metadata for task progress; canonical results stay in chat history."""
from datetime import datetime, timezone
import json
from .planner import PlanStage
from .task_store import set_stage

MAX_ACTIVITY = 100
ACTIVE_STATUSES = {'running', 'awaiting_approval', 'applying'}


def begin_tool(task, tool, args, call_id, message_index):
    if not task:
        return None
    stage = 'implementation' if tool == 'write_file' else 'research'
    if stage == 'implementation' and not any(s['id'] == stage for s in task['stages']):
        index = next((i for i, s in enumerate(task['stages']) if s['id'] == 'verification'), len(task['stages']))
        task['stages'].insert(index, PlanStage(stage, 'Реализация', 'Изменения файлов после подтверждения.').to_dict())
    set_stage(task, stage)
    task['activity_sequence'] = int(task.get('activity_sequence', 0)) + 1
    entry = {'id': task['activity_sequence'], 'tool': str(tool)[:80], 'call_id': str(call_id),
             'message_index': message_index, 'path': str(args.get('path', '.'))[:500] if isinstance(args, dict) else '',
             'stage': stage, 'status': 'running', 'summary': 'Инструмент выполняется',
             'started_at': datetime.now(timezone.utc).isoformat()}
    entries = task.setdefault('tool_activity', [])
    entries.append(entry)
    if len(entries) > MAX_ACTIVITY:
        task['activity_omitted'] = int(task.get('activity_omitted', 0)) + len(entries) - MAX_ACTIVITY
        del entries[:-MAX_ACTIVITY]
    return entry['id']


def update_tool(task, activity_id, status, summary):
    if not task or activity_id is None:
        return
    for entry in task.get('tool_activity', []):
        if entry.get('id') == activity_id:
            entry['status'] = status
            entry['summary'] = str(summary)[:500]
            if status not in ACTIVE_STATUSES:
                entry['finished_at'] = datetime.now(timezone.utc).isoformat()
            return


def finish_tool(task, activity_id, tool, result):
    if result.get('ok'):
        status = 'succeeded'
        if tool == 'read_file':
            summary = f"Прочитано символов: {len(result.get('content', ''))}"
        elif tool == 'list_files':
            summary = f"Найдено элементов: {len(result.get('entries', []))}"
        elif tool == 'search_text':
            summary = f"Найдено совпадений: {len(result.get('matches', []))}"
        else:
            summary = 'Файл записан' if tool == 'write_file' else 'Инструмент завершён'
        if result.get('truncated'):
            summary += ' · достигнут лимит выдачи'
    else:
        status = {'USER_DENIED': 'rejected', 'USER_CANCELLED': 'cancelled'}.get(result.get('code'), 'failed')
        summary = {'rejected': 'Изменение отклонено пользователем', 'cancelled': 'Изменение отменено пользователем'}.get(status, str(result.get('error', 'Ошибка инструмента')))
    update_tool(task, activity_id, status, summary)


def recover_tools(task, messages):
    """Resolve in-flight metadata using only its anchored canonical tool block."""
    changed = False
    for entry in task.get('tool_activity', []):
        if entry.get('status') not in ACTIVE_STATUSES:
            continue
        result = None
        index = entry.get('message_index')
        if isinstance(index, int) and 0 <= index < len(messages):
            anchor = messages[index]
            if anchor.get('role') == 'assistant' and any(c.get('id') == entry.get('call_id') for c in anchor.get('tool_calls', []) if isinstance(c, dict)):
                for message in messages[index + 1:]:
                    if message.get('role') != 'tool':
                        break
                    if message.get('tool_call_id') == entry.get('call_id'):
                        try:
                            value = json.loads(message.get('content', ''))
                            if isinstance(value, dict) and isinstance(value.get('ok'), bool):
                                result = value
                        except (TypeError, ValueError):
                            pass
                        break
        if result is not None:
            finish_tool(task, entry['id'], entry['tool'], result)
        elif entry.get('status') == 'applying':
            update_tool(task, entry['id'], 'unknown', 'Запись могла завершиться до сбоя. Проверьте файл; прежнее согласие сброшено.')
        else:
            update_tool(task, entry['id'], 'interrupted', 'Выполнение прервано; результат не сохранён. Для записи потребуется новое согласие.')
        changed = True
    return changed
