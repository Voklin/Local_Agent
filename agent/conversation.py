"""Bounded conversation context helpers.

The complete transcript remains stored on disk for the user. Only a compact tail of
recent turns is sent to the model, avoiding repeated replay of the entire chat forever.
"""
from __future__ import annotations
import json
from copy import deepcopy

MAX_CONTEXT_CHARS = 30000
MAX_CONTEXT_TURNS = 8
MAX_TOOL_RESULT_CHARS = 2600
MAX_LAST_TOOL_RESULT_CHARS = 6000


def _message_size(message):
    try:
        return len(json.dumps(message, ensure_ascii=False))
    except (TypeError, ValueError):
        return len(str(message))


def _bounded_turn(turn):
    """Copy a turn and bound bulky tool payloads without breaking tool-call pairing."""
    result = []
    tool_indexes = [i for i, msg in enumerate(turn) if msg.get("role") == "tool"]
    last_tool = tool_indexes[-1] if tool_indexes else -1
    for index, original in enumerate(turn):
        msg = dict(original)
        if msg.get("role") == "tool" and isinstance(msg.get("content"), str):
            limit = MAX_LAST_TOOL_RESULT_CHARS if index == last_tool else MAX_TOOL_RESULT_CHARS
            content = msg["content"]
            if len(content) > limit:
                msg["content"] = content[:limit] + f"\n[… вывод инструмента сокращён для контекста; полная версия остаётся в истории чата, исходная длина {len(content)} символов …]"
        result.append(msg)
    return result


def select_recent_history(history, max_chars=MAX_CONTEXT_CHARS, max_turns=MAX_CONTEXT_TURNS):
    """Keep the newest complete user-turn groups within a bounded context budget."""
    messages = [dict(m) for m in (history or []) if isinstance(m, dict)]
    turns = []
    current = []
    preamble = []
    saw_user = False
    for message in messages:
        role = message.get("role")
        if role == "user":
            if current:
                turns.append(current)
            current = (preamble + [message]) if not saw_user else [message]
            preamble = []
            saw_user = True
        elif current:
            current.append(message)
        else:
            # Some imported/legacy histories can begin with an assistant tool-call pair.
            # Preserve it as a standalone context segment instead of silently dropping it.
            preamble.append(message)
    if current:
        turns.append(current)
    elif preamble:
        turns.append(preamble)
    if not turns:
        return []

    selected = []
    used = 0
    for turn in reversed(turns[-max(1, max_turns):]):
        bounded = _bounded_turn(turn)
        size = sum(_message_size(m) for m in bounded)
        if selected and used + size > max_chars:
            break
        selected.append(bounded)
        used += size
    selected.reverse()
    # Keep only whole turns; if the latest turn itself is large, tool payloads have already
    # been capped above and it remains available so confirmations retain their context.
    return [message for turn in selected for message in turn]


def build_messages(history, prompt):
    """Copy the full transcript and append the new request; compact only before HTTP."""
    messages = deepcopy([m for m in (history or []) if isinstance(m, dict)])
    messages.append({"role": "user", "content": prompt})
    return messages


def _complete_units(messages):
    """Copy complete tool exchanges; omit orphaned/unfinished exchanges from model context."""
    units = []
    index = 0
    while index < len(messages):
        start = index
        message = deepcopy(messages[index])
        index += 1
        role = message.get("role")
        if role not in ("user", "assistant"):
            continue
        unit = [message]
        calls = message.get("tool_calls") if role == "assistant" else None
        if calls:
            ids = [call.get("id") for call in calls if isinstance(call, dict)]
            valid = len(ids) == len(calls) and all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids)
            expected = set(ids) if valid else set()
            seen = set()
            while index < len(messages) and messages[index].get("role") == "tool":
                result = deepcopy(messages[index])
                index += 1
                call_id = result.get("tool_call_id")
                if not isinstance(call_id, str) or call_id not in expected or call_id in seen:
                    valid = False
                if isinstance(call_id, str):
                    seen.add(call_id)
                unit.append(result)
            if not valid or seen != expected:
                continue
        units.append((start, unit))
    return units


def compact_live_messages(messages, max_chars=80000, keep_recent_rounds=10, request_index=None):
    """Build a bounded JSON message list without mutating the complete transcript.

    Preserve system instructions, the current request and newest user message. Tool calls
    and results are indivisible. If mandatory instructions/arguments alone exceed the
    budget, raise before HTTP rather than sending an invalid or silently changed request.
    """
    if not messages:
        return []
    limit = max(256, int(max_chars))
    system = [deepcopy(messages[0])] if messages[0].get("role") == "system" else []
    units = _complete_units(messages)
    user_indexes = [start for start, unit in units if unit[0].get("role") == "user"]
    latest_user = user_indexes[-1] if user_indexes else None
    if request_index not in user_indexes:
        request_index = latest_user
    protected = {i for i in (request_index, latest_user) if i is not None}
    if units:
        protected.add(units[-1][0])
    recent = {start for start, _ in units[-max(1, int(keep_recent_rounds)):]}
    selected = [item for item in units if item[0] in protected or item[0] in recent]

    def flatten():
        return system + [message for _, unit in selected for message in unit]

    def size():
        return len(json.dumps(flatten(), ensure_ascii=False))

    # Bound individual tool outputs in the projection, never in the persisted transcript.
    for _, unit in selected:
        for message in unit:
            if message.get("role") == "tool" and isinstance(message.get("content"), str):
                if len(message["content"]) > 10000:
                    message["content"] = message["content"][:10000] + "\n[Вывод сокращён для модели]"
    while size() > limit:
        removable = next((i for i, (start, _) in enumerate(selected) if start not in protected), None)
        if removable is None:
            break
        selected.pop(removable)
    # JSON escaping and message metadata count towards the limit. Binary search a prefix
    # instead of assuming that one character of content equals one serialized character.
    candidates = [m for _, unit in selected for m in unit
                  if m.get("role") in ("tool", "assistant") and isinstance(m.get("content"), str)]
    for message in sorted(candidates, key=lambda m: len(m["content"]), reverse=True):
        if size() <= limit:
            break
        original = message["content"]
        marker = "[Сокращено для модели]"
        message["content"] = marker
        if size() > limit:
            continue
        low, high = 0, len(original)
        while low < high:
            middle = (low + high + 1) // 2
            message["content"] = original[:middle] + marker
            if size() <= limit:
                low = middle
            else:
                high = middle - 1
        message["content"] = original[:low] + marker
    if size() > limit:
        raise ValueError("Контекст обязательных инструкций, запроса или аргументов инструментов превышает лимит. Увеличьте max_context_chars или сократите запрос.")
    return flatten()
