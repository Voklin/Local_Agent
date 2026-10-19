"""Bounded conversation context helpers.

The complete transcript remains stored on disk for the user. Only a compact tail of
recent turns is sent to the model, avoiding repeated replay of the entire chat forever.
"""
from __future__ import annotations
import json

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
    """Build a request from recent bounded context plus the new user message."""
    messages = select_recent_history(history)
    messages.append({"role": "user", "content": prompt})
    return messages
