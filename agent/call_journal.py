"""Durable tool-call receipts and conservative canonical-history recovery.

The task checkpoint contains UI metadata; this separate append-only journal owns
the complete calls and receipts needed after a process interruption. An effect
must never start before its ``started`` event has been durably appended.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import threading
from pathlib import Path

from . import task_store


MAX_RECORD_BYTES = 4 * 1024 * 1024
_PHASES = {"prepared": 0, "awaiting_approval": 1, "started": 2}
_RECOVERY_CODES = {"NOT_EXECUTED", "TOOL_INTERRUPTED", "OUTCOME_UNKNOWN"}
_JOURNAL_LOCKS = {}
_LOCKS_GUARD = threading.Lock()


def _unknown(result):
    return isinstance(result, dict) and (
        result.get("code") == "OUTCOME_UNKNOWN" or result.get("outcome_unknown") is True
    )


def _placeholder(result):
    return (isinstance(result, dict) and result.get("recovery") is True and
            isinstance(result.get("code"), str) and result["code"] in _RECOVERY_CODES)


def _replaceable(result):
    return result is None or _unknown(result) or _placeholder(result)


def _index(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("Journal message_index must be a non-negative integer")
    return value


def _canonical_calls(calls):
    if not isinstance(calls, list) or not calls:
        raise ValueError("Journal batch must contain at least one tool call")
    normalized, seen = [], set()
    for call in calls:
        if not isinstance(call, dict):
            raise ValueError("Journal tool call must be an object")
        call_id, function = call.get("id"), call.get("function")
        if not isinstance(call_id, str) or not call_id or call_id in seen:
            raise ValueError("Journal tool-call ids must be non-empty and unique")
        if call.get("type", "function") != "function" or not isinstance(function, dict):
            raise ValueError("Journal tool call must use the canonical function shape")
        name, arguments = function.get("name"), function.get("arguments")
        if not isinstance(name, str) or not name or not isinstance(arguments, str):
            raise ValueError("Journal tool call requires a function name and JSON argument string")
        # Invalid JSON arguments are still persisted: validation can produce a
        # real failed receipt later, without ever executing the invalid call.
        normalized.append({"id": call_id, "type": "function", "function": {"name": name, "arguments": arguments}})
        seen.add(call_id)
    return normalized


def _resolution_result(resolution):
    if resolution == "completed":
        return {"ok": True, "code": "USER_CONFIRMED_EFFECT", "user_confirmed": True, "result_unavailable": True}
    return {"ok": False, "code": "USER_CONFIRMED_NOT_EXECUTED", "user_confirmed": True}


class LegacyCallJournal:
    """One fsynced JSONL file for one chat/task epoch.

    ``message_index`` always addresses the persisted canonical history, without
    the transient system message added when constructing an API request.
    """

    def __init__(self, chat_id, journal_id, directory=None):
        self.chat_id, self.journal_id = str(chat_id), str(journal_id)
        if not self.chat_id or not self.journal_id:
            raise ValueError("Journal chat_id and journal_id must be non-empty")
        directory = Path(directory) if directory is not None else Path(task_store.TASK_DIR) / "journals"
        identity = json.dumps([self.chat_id, self.journal_id], ensure_ascii=False).encode("utf-8")
        self.path = directory / (hashlib.sha256(identity).hexdigest() + ".jsonl")
        # UI recovery and execution may construct separate instances for the
        # same epoch. Serialize their read/validate/append transactions too.
        lock_key = os.path.normcase(str(self.path.resolve()))
        with _LOCKS_GUARD:
            self._lock = _JOURNAL_LOCKS.setdefault(lock_key, threading.RLock())

    def _read(self):
        """Return validated events plus the byte boundary before a torn tail."""
        events, valid_end, torn, unterminated = [], 0, False, False
        try:
            stream = self.path.open("rb")
        except FileNotFoundError:
            return events, valid_end, torn, unterminated
        with stream:
            while True:
                row = stream.readline(MAX_RECORD_BYTES + 1)
                if not row:
                    break
                if len(row) > MAX_RECORD_BYTES:
                    raise ValueError("Journal row exceeds the durable record size limit")
                complete = row.endswith(b"\n")
                try:
                    event = json.loads(row.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    if not complete and not stream.read(1):
                        torn = True
                        break
                    raise ValueError("Journal contains a corrupt complete row; recovery stopped") from exc
                if not isinstance(event, dict) or event.get("version") != 1:
                    raise ValueError("Journal contains an invalid event/version")
                if event.get("chat_id") != self.chat_id or event.get("journal_id") != self.journal_id:
                    raise ValueError("Journal identity mismatch")
                events.append(event)
                valid_end = stream.tell()
                unterminated = not complete
        return events, valid_end, torn, unterminated

    def _state(self):
        events, valid_end, torn, unterminated = self._read()
        batches = {}
        for event in events:
            try:
                index = _index(event.get("message_index"))
                kind = event.get("event")
                if kind == "batch":
                    calls = _canonical_calls(event.get("calls"))
                    content = event.get("assistant_content")
                    if content is not None and not isinstance(content, str):
                        raise ValueError("Invalid journal assistant content")
                    if index in batches:
                        raise ValueError("Journal contains a colliding batch/call id")
                    if any(not (index > anchor + len(batch["calls"]) or
                                anchor > index + len(calls)) for anchor, batch in batches.items()):
                        raise ValueError("Journal contains overlapping assistant batch anchors")
                    states = {}
                    for call in calls:
                        states[call["id"]] = {"phase": "prepared", "effectful": True, "result": None, "resolution": None}
                    batches[index] = {"calls": calls, "assistant_content": content, "states": states}
                    continue
                state = self._call_state(batches, index, event.get("call_id"))
                if kind == "phase":
                    phase, effectful = event.get("phase"), event.get("effectful")
                    if phase not in _PHASES or not isinstance(effectful, bool):
                        raise ValueError("Invalid journal phase/effect classification")
                    if state["result"] is not None or _PHASES[phase] < _PHASES[state["phase"]]:
                        raise ValueError("Journal contains an invalid phase transition")
                    if state["phase"] == "started" and effectful != state["effectful"]:
                        raise ValueError("Journal changes effect classification after execution started")
                    state.update(phase=phase, effectful=effectful)
                elif kind == "result":
                    result = event.get("result")
                    if not isinstance(result, dict) or type(result.get('ok')) is not bool or state["resolution"] is not None:
                        raise ValueError("Invalid journal result")
                    if state["result"] is not None and not _replaceable(state["result"]):
                        raise ValueError("Journal attempts to replace a real saved receipt")
                    state["result"] = result
                elif kind == "resolution":
                    resolution = event.get("resolution")
                    if resolution not in ("completed", "not_executed") or not self._unresolved_state(state):
                        raise ValueError("Journal resolution does not refer to an unresolved effect")
                    state.update(resolution=resolution, result=_resolution_result(resolution))
                else:
                    raise ValueError("Unknown journal event")
            except (KeyError, TypeError) as exc:
                raise ValueError("Journal contains an invalid event") from exc
        return batches, valid_end, torn, unterminated

    @staticmethod
    def _call_state(batches, message_index, call_id):
        try:
            return batches[message_index]["states"][call_id]
        except (KeyError, TypeError) as exc:
            raise ValueError("Journal call identity does not match its recorded message anchor") from exc

    @staticmethod
    def _unresolved_state(state):
        return state["resolution"] is None and (
            _unknown(state["result"]) or
            (state["phase"] == "started" and state["effectful"] and state["result"] is None)
        )

    def _append(self, event, state_info):
        event = {"version": 1, "chat_id": self.chat_id, "journal_id": self.journal_id, **event}
        try:
            encoded = json.dumps(event, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8") + b"\n"
        except (TypeError, ValueError) as exc:
            raise ValueError("Journal event must contain finite JSON values") from exc
        if len(encoded) > MAX_RECORD_BYTES:
            raise ValueError("Journal row exceeds the durable record size limit")
        _, valid_end, torn, unterminated = state_info
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("r+b" if self.path.exists() else "w+b") as stream:
            if torn:
                stream.truncate(valid_end)
            stream.seek(0, os.SEEK_END)
            if unterminated:
                stream.write(b"\n")
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())

    def prepare_batch(self, calls, message_index, assistant_content=None):
        message_index, calls = _index(message_index), _canonical_calls(calls)
        if assistant_content is not None and not isinstance(assistant_content, str):
            raise ValueError("Journal assistant_content must be text or None")
        with self._lock:
            info = self._state()
            batches = info[0]
            if message_index in batches:
                batch = batches[message_index]
                if batch["calls"] == calls and batch["assistant_content"] == assistant_content:
                    return
                raise ValueError("Journal batch identity mismatch at recorded message anchor")
            if any(not (message_index > anchor + len(batch["calls"]) or
                        anchor > message_index + len(calls)) for anchor, batch in batches.items()):
                raise ValueError("Journal assistant batch anchors overlap")
            self._append({"event": "batch", "message_index": message_index, "calls": calls,
                          "assistant_content": assistant_content}, info)

    def set_phase(self, message_index, call_id, phase, *, effectful=True):
        message_index = _index(message_index)
        if not isinstance(phase, str) or phase not in _PHASES or not isinstance(effectful, bool):
            raise ValueError("Journal phase/effect classification is invalid")
        with self._lock:
            info = self._state()
            state = self._call_state(info[0], message_index, call_id)
            if state["phase"] == phase and state["effectful"] == effectful:
                return
            if state["result"] is not None or _PHASES[phase] < _PHASES[state["phase"]]:
                raise ValueError("Journal phase cannot move backwards or change after a receipt")
            if state["phase"] == "started" and effectful != state["effectful"]:
                raise ValueError("Journal effect classification cannot change after execution started")
            self._append({"event": "phase", "message_index": message_index, "call_id": call_id,
                          "phase": phase, "effectful": effectful}, info)

    def record_result(self, message_index, call_id, result):
        message_index = _index(message_index)
        if not isinstance(result, dict) or type(result.get('ok')) is not bool:
            raise ValueError("Journal result must contain a boolean ok")
        with self._lock:
            info = self._state()
            state = self._call_state(info[0], message_index, call_id)
            if state["result"] == result:
                return
            if state["resolution"] is not None or not _replaceable(state["result"]):
                raise ValueError("Journal cannot replace a real saved receipt")
            self._append({"event": "result", "message_index": message_index, "call_id": call_id,
                          "result": result}, info)

    def entries(self):
        with self._lock:
            batches = self._state()[0]
            entries = []
            for index, batch in sorted(batches.items()):
                for call in batch["calls"]:
                    entries.append({"message_index": index, "call_id": call["id"], "name": call["function"]["name"],
                                    "arguments": call["function"]["arguments"], "call": copy.deepcopy(call),
                                    **copy.deepcopy(batch["states"][call["id"]])})
            return entries

    calls = entries

    @staticmethod
    def delete_chat(chat_id):
        """Delete only journals whose recorded chat identity and filename match."""
        directory=Path(task_store.TASK_DIR)/'journals'
        for path in directory.glob('*.jsonl'):
            with path.open('rb') as stream:row=stream.readline(MAX_RECORD_BYTES+1)
            try:identity=json.loads(row)
            except (ValueError,UnicodeDecodeError):continue
            if isinstance(identity,dict) and identity.get('chat_id')==str(chat_id) and identity.get('journal_id'):
                journal=LegacyCallJournal(chat_id,identity['journal_id'])
                if journal.path==path:
                    with journal._lock:path.unlink(missing_ok=True)

    def unresolved(self):
        return [entry for entry in self.entries() if self._unresolved_state(entry)]

    def resolve(self, message_index, call_id, resolution):
        message_index = _index(message_index)
        if resolution not in ("completed", "not_executed"):
            raise ValueError("Journal resolution must be completed or not_executed")
        with self._lock:
            info = self._state()
            state = self._call_state(info[0], message_index, call_id)
            if not self._unresolved_state(state):
                raise ValueError("Only unresolved effects can be resolved by the user")
            self._append({"event": "resolution", "message_index": message_index, "call_id": call_id,
                          "resolution": resolution}, info)

    @staticmethod
    def _missing_result(state):
        if state["phase"] != "started":
            code, error = "NOT_EXECUTED", "Tool call did not start before interruption."
        elif state["effectful"]:
            code, error = "OUTCOME_UNKNOWN", "Tool execution started; its effect is unknown. User review is required before retrying."
        else:
            code, error = "TOOL_INTERRUPTED", "Read-only tool execution was interrupted before its result was saved."
        return {"ok": False, "code": code, "error": error, "recovery": True}

    def recover(self, messages):
        """Repair a matching history, validating every anchor before mutating it.

        A missing tail may be restored at its exact next index. An occupied
        anchor with different call ids/names/arguments is a different transcript
        and is rejected. Real receipts are never replaced by unknown outcomes.
        """
        if not isinstance(messages, list):
            raise ValueError("Canonical history must be a list")
        with self._lock:
            batches, _, torn, _ = self._state()
            candidate, adoptions = copy.deepcopy(messages), []
            warnings = ["Journal has an incomplete trailing row; it was ignored."] if torn else []
            for index, batch in sorted(batches.items()):
                if index > len(candidate):
                    raise ValueError("Journal anchor is beyond the canonical history; transcript identity cannot be established")
                if index == len(candidate):
                    candidate.append({"role": "assistant", "content": batch["assistant_content"],
                                      "tool_calls": copy.deepcopy(batch["calls"])})
                assistant = candidate[index]
                if not isinstance(assistant, dict) or assistant.get("role") != "assistant":
                    raise ValueError("Journal assistant anchor does not match canonical history")
                try:
                    actual_calls = _canonical_calls(assistant.get("tool_calls"))
                except ValueError as exc:
                    raise ValueError("Journal assistant call identity does not match canonical history") from exc
                if actual_calls != batch["calls"]:
                    raise ValueError("Journal call ids/names/arguments mismatch at canonical history anchor")
                if assistant.get("content") is None and batch["assistant_content"] is not None:
                    assistant["content"] = batch["assistant_content"]
                end, existing = index + 1, {}
                while end < len(candidate) and isinstance(candidate[end], dict) and candidate[end].get("role") == "tool":
                    message = candidate[end]
                    call_id = message.get("tool_call_id")
                    if call_id not in batch["states"] or call_id in existing:
                        raise ValueError("Canonical tool result has an unmatched or duplicate call id")
                    try:
                        result = json.loads(message.get("content", ""))
                    except (TypeError, json.JSONDecodeError) as exc:
                        raise ValueError("Canonical tool result is not a valid JSON receipt") from exc
                    if not isinstance(result, dict) or type(result.get('ok')) is not bool:
                        raise ValueError("Canonical tool result must be an object receipt with boolean ok")
                    existing[call_id] = (message, result)
                    end += 1
                repaired = []
                for call in batch["calls"]:
                    call_id, state = call["id"], batch["states"][call["id"]]
                    recorded = state["result"]
                    saved = existing.get(call_id)
                    if saved is not None and not _replaceable(saved[1]):
                        if not _replaceable(recorded) and recorded != saved[1]:
                            raise ValueError("Canonical receipt conflicts with a real saved journal receipt")
                        if recorded != saved[1]:
                            adoptions.append((index, call_id, saved[1]))
                        repaired.append(saved[0])
                        continue
                    result = copy.deepcopy(recorded) if recorded is not None else self._missing_result(state)
                    if saved is not None and saved[1] == result:
                        repaired.append(saved[0])
                    else:
                        repaired.append({"role": "tool", "tool_call_id": call_id,
                                         "content": json.dumps(result, ensure_ascii=False)})
                candidate[index + 1:end] = repaired
            # Identity mismatches above leave both files and caller history
            # untouched. Adopt already-saved real receipts before clearing any
            # unresolved gate or publishing repaired history.
            for index, call_id, result in adoptions:
                self.record_result(index, call_id, result)
            changed = candidate != messages
            if changed:
                messages[:] = candidate
            return {"changed": changed, "unresolved": self.unresolved(), "warnings": warnings}


class JournalTransaction:
    """Serialize state validation and append across both threads and processes."""

    def __init__(self, lock, database):
        self.lock = lock
        self.database = database
        self.local = threading.local()

    def __enter__(self):
        self.lock.acquire()
        transaction = self.database.transaction()
        try:
            transaction.__enter__()
        except BaseException:
            self.lock.release()
            raise
        stack = getattr(self.local, 'stack', [])
        stack.append(transaction)
        self.local.stack = stack
        return self

    def __exit__(self, *error):
        try:
            return self.local.stack.pop().__exit__(*error)
        finally:
            self.lock.release()


class CallJournal(LegacyCallJournal):
    """Canonical SQLite call journal; the JSONL reader is retained for migration."""

    def __init__(self, chat_id, journal_id, directory=None):
        super().__init__(chat_id, journal_id, directory)
        from .storage import Storage
        self.legacy_path = self.path
        profile = Path(directory) if directory is not None else Path(task_store.TASK_DIR).parent
        self.database = Storage(profile).ready()
        self.path = self.database.path
        self._lock = JournalTransaction(self._lock, self.database)

    def _stored_event(self, event):
        """Externalize only the receipt payload, keeping lifecycle anchors in SQLite."""
        from .storage import encode
        event = dict(event)
        if event.get('event') == 'result':
            event['result'] = self.database.pack(encode(event['result']))
            if isinstance(event['result'], str):
                event['result'] = json.loads(event['result'])
        return event

    def _read(self):
        """Import a validated legacy epoch once and return its transactional events."""
        from .storage import encode
        with self.database.transaction() as connection:
            if connection.execute('SELECT 1 FROM chat_tombstones WHERE id=?', (self.chat_id,)).fetchone():
                return [], 0, False, False
            migrated = connection.execute('SELECT warning FROM journal_imports WHERE chat_id=? AND journal_id=?', (self.chat_id,self.journal_id)).fetchone()
            if migrated is None:
                legacy = LegacyCallJournal(self.chat_id, self.journal_id, self.legacy_path.parent)
                legacy._state()  # Validate every transition before any event is copied.
                events, _, torn, _ = legacy._read()
                for event in events:
                    connection.execute('INSERT INTO journal_events(chat_id,journal_id,data) VALUES(?,?,?)', (self.chat_id,self.journal_id,encode(self._stored_event(event))))
                digest = hashlib.sha256(self.legacy_path.read_bytes()).hexdigest() if self.legacy_path.exists() else None
                warning = 'Journal has an incomplete trailing row; original JSONL was preserved.' if torn else None
                count = connection.execute('SELECT count(*) FROM journal_events WHERE chat_id=? AND journal_id=?',(self.chat_id,self.journal_id)).fetchone()[0]
                if count != len(events):
                    raise ValueError('Journal migration count mismatch')
                connection.execute('INSERT INTO journal_imports VALUES(?,?,?,?,?)',(self.chat_id,self.journal_id,digest,count,warning))
                migrated = {'warning': warning}
            events = []
            for row in connection.execute('SELECT data FROM journal_events WHERE chat_id=? AND journal_id=? ORDER BY sequence', (self.chat_id,self.journal_id)):
                event = json.loads(row['data'])
                if event.get('event') == 'result':
                    result = self.database.unpack(event['result'])
                    event['result'] = json.loads(result) if isinstance(result,str) else result
                events.append(event)
            return events, 0, bool(migrated['warning']), False

    def _append(self, event, state_info):
        """Commit the receipt before returning to the effect boundary or UI callback."""
        from .storage import encode
        event = {'version': 1, 'chat_id': self.chat_id, 'journal_id': self.journal_id, **event}
        run_id=(event.get('result') or {}).get('_run_id') if event.get('event')=='result' else None
        if isinstance(run_id,str):event['run_id']=run_id
        encoded = encode(self._stored_event(event))
        if len(encoded.encode('utf-8')) > MAX_RECORD_BYTES:
            raise ValueError('Journal row exceeds the durable record size limit')
        with self.database.transaction() as connection:
            if connection.execute('SELECT 1 FROM chat_tombstones WHERE id=?',(self.chat_id,)).fetchone():
                raise ValueError('Cannot append to a deleted chat')
            counted=connection.execute("SELECT 1 FROM journal_events WHERE chat_id=? AND journal_id=? AND json_extract(data,'$.run_id')=? AND json_extract(data,'$.message_index')=? AND json_extract(data,'$.call_id')=? LIMIT 1",(self.chat_id,self.journal_id,run_id,event.get('message_index'),event.get('call_id'))).fetchone() if run_id else None
            connection.execute('INSERT INTO journal_events(chat_id,journal_id,data) VALUES(?,?,?)', (self.chat_id,self.journal_id,encoded))
            if run_id and not counted:
                row=connection.execute('SELECT data FROM runs WHERE id=? AND json_extract(data,\'$.journal_id\')=? AND (chat_id=? OR (parent_id IS NOT NULL AND id=?))',(run_id,self.journal_id,self.chat_id,self.chat_id)).fetchone()
                if row:
                    value=json.loads(row[0]);value['tool_calls']=value.get('tool_calls',0)+1
                    connection.execute('UPDATE runs SET data=? WHERE id=?',(encode(value),run_id))

    @staticmethod
    def delete_chat(chat_id):
        """Delete all epochs transactionally while retaining migration tombstones."""
        from .storage import Storage
        database = Storage(Path(task_store.TASK_DIR).parent).ready()
        with database.transaction() as connection:
            connection.execute('DELETE FROM journal_events WHERE chat_id=?', (str(chat_id),))
            connection.execute('INSERT OR IGNORE INTO chat_tombstones VALUES(?)', (str(chat_id),))
