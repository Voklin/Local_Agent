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


def compact_live_messages(messages, max_chars=80000, keep_recent_rounds=10):
    """Bound a live agent run's context while preserving the original request and valid tool pairs.

    Unlike the persisted chat transcript, this is a model-facing working context. Old completed
    tool rounds can be summarized as metadata and removed when the budget is exceeded.
    """
    if not messages:
        return []
    system = [dict(messages[0])] if messages[0].get("role") == "system" else []
    body = [dict(m) for m in messages[1:] if isinstance(m, dict)] if system else [dict(m) for m in messages if isinstance(m, dict)]
    first_user = next((dict(m) for m in body if m.get("role") == "user"), None)
    # Group assistant tool-call messages with their tool results as indivisible units.
    units = []
    i = 0
    while i < len(body):
        msg = body[i]
        unit = [msg]
        i += 1
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            expected = {tc.get("id") for tc in msg.get("tool_calls", []) if tc.get("id")}
            while i < len(body) and body[i].get("role") == "tool" and body[i].get("tool_call_id") in expected:
                unit.append(body[i]); expected.discard(body[i].get("tool_call_id")); i += 1
                if not expected:
                    break
        units.append(unit)
    # Always keep initial request and recent units. Tool outputs are shortened before pruning.
    for unit in units:
        for msg in unit:
            if msg.get("role") == "tool" and isinstance(msg.get("content"), str):
                content = msg["content"]
                if len(content) > 10000:
                    msg["content"] = content[:10000] + f"\n[… результат сокращён в рабочем контексте; полная история сохранена, длина {len(content)} символов …]"
    def flatten(items):
        return system + [m for unit in items for m in unit]
    recent = units[-max(1, int(keep_recent_rounds)):]
    # Ensure the original request remains available even when older units are discarded.
    def total(items):
        return sum(_message_size(m) for m in flatten(items))
    while len(recent) > 1 and total(recent) > max(12000, int(max_chars)):
        recent.pop(0)
    result = flatten(recent)
    if first_user and not any(m is first_user or (m.get("role") == "user" and m.get("content") == first_user.get("content")) for m in result):
        result.insert(len(system), first_user)
    # If the original prompt plus latest round still exceeds budget, keep the latest complete
    # tool round and a clipped copy of the initial request rather than sending unbounded history.
    if total(recent) > max(12000, int(max_chars)) and first_user:
        for m in result:
            if m.get("role") == "user" and m.get("content") == first_user.get("content"):
                content = str(m.get("content", ""))
                m["content"] = content[:6000] + ("\n[… исходный запрос сокращён только в контексте модели …]" if len(content) > 6000 else "")
                break
    return result
