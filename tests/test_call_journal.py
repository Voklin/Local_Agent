import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent import task_store
from agent.call_journal import LegacyCallJournal as CallJournal, MAX_RECORD_BYTES
# Keep byte-level JSONL fault tests for the retained migration reader.
# Canonical SQLite lifecycle/crash tests live in test_tool_execution/test_storage.


def call(call_id="call-1", name="write_file", arguments='{"path":"a.txt","content":"hello"}'):
    return {"id": call_id, "type": "function", "function": {"name": name, "arguments": arguments}}


def assistant(calls, content=None):
    return {"role": "assistant", "content": content, "tool_calls": copy.deepcopy(calls)}


def receipt(call_id, result):
    return {"role": "tool", "tool_call_id": call_id, "content": json.dumps(result, ensure_ascii=False)}


class CallJournalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.journal = CallJournal("chat", "epoch-1", self.directory)

    def result(self, messages, index=1):
        return json.loads(messages[index]["content"])

    def test_default_directory_uses_current_task_dir_and_chat_epoch_are_isolated(self):
        with patch.object(task_store, "TASK_DIR", self.directory / "tasks"):
            journal = CallJournal("chat", "epoch")
            journal.prepare_batch([call()], 0)
            self.assertEqual(journal.path.parent, self.directory / "tasks" / "journals")
            self.assertNotEqual(journal.path, CallJournal("other-chat", "epoch").path)
            self.assertNotEqual(journal.path, CallJournal("chat", "other-epoch").path)

    def test_prepare_and_started_are_fsynced_before_return(self):
        with patch("agent.call_journal.os.fsync", wraps=__import__("os").fsync) as sync:
            self.journal.prepare_batch([call()], 0, "Выполняю запись")
            self.assertEqual(sync.call_count, 1)
            self.journal.set_phase(0, "call-1", "started")
            self.assertEqual(sync.call_count, 2)
        entry = CallJournal("chat", "epoch-1", self.directory).entries()[0]
        self.assertEqual(entry["call"], call())
        self.assertEqual(entry["phase"], "started")

    def test_prepared_batch_and_awaiting_approval_are_never_executed(self):
        calls = [call(), call("call-2")]
        self.journal.prepare_batch(calls, 1, "План записи")
        self.journal.set_phase(1, "call-2", "awaiting_approval")
        messages = [{"role": "user", "content": "write"}]
        details = self.journal.recover(messages)
        self.assertTrue(details["changed"])
        self.assertEqual(messages[1], assistant(calls, "План записи"))
        self.assertEqual(self.result(messages, 2)["code"], "NOT_EXECUTED")
        self.assertEqual(self.result(messages, 3)["code"], "NOT_EXECUTED")
        self.assertEqual(details["unresolved"], [])

    def test_started_read_only_and_effectful_calls_are_classified_conservatively(self):
        self.journal.prepare_batch([call("read", "read_file"), call("write")], 0)
        self.journal.set_phase(0, "read", "started", effectful=False)
        self.journal.set_phase(0, "write", "started", effectful=True)
        messages = []
        details = self.journal.recover(messages)
        self.assertEqual(self.result(messages)["code"], "TOOL_INTERRUPTED")
        self.assertEqual(self.result(messages, 2)["code"], "OUTCOME_UNKNOWN")
        self.assertEqual([entry["call_id"] for entry in details["unresolved"]], ["write"])
        self.assertFalse(self.result(messages, 2)["ok"])
        self.assertTrue(self.result(messages, 2)["recovery"])

    def test_saved_receipt_restores_missing_chat_tail(self):
        result = {"ok": True, "text": "полный сохранённый результат", "details": {"count": 3}}
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        self.journal.record_result(0, "call-1", result)
        for initial in ([], [assistant([call()])]):
            with self.subTest(initial=initial):
                messages = copy.deepcopy(initial)
                self.assertTrue(self.journal.recover(messages)["changed"])
                self.assertEqual(self.result(messages), result)
                self.assertFalse(self.journal.recover(messages)["changed"])
                self.assertEqual(len(messages), 2)
        self.assertEqual(self.journal.unresolved(), [])

    def test_partial_batch_preserves_receipt_and_pairs_every_call(self):
        calls = [call("done"), call("unknown"), call("pending")]
        result = {"ok": False, "code": "PERMISSION_DENIED", "error": "denied"}
        self.journal.prepare_batch(calls, 0)
        self.journal.set_phase(0, "done", "started")
        self.journal.record_result(0, "done", result)
        self.journal.set_phase(0, "unknown", "started")
        messages = [assistant(calls), receipt("done", result)]
        self.journal.recover(messages)
        self.assertEqual([message["tool_call_id"] for message in messages[1:]], ["done", "unknown", "pending"])
        self.assertEqual(self.result(messages), result)
        self.assertEqual(self.result(messages, 2)["code"], "OUTCOME_UNKNOWN")
        self.assertEqual(self.result(messages, 3)["code"], "NOT_EXECUTED")
        self.assertFalse(self.journal.recover(messages)["changed"])

    def test_real_canonical_receipt_replaces_placeholder_and_clears_gate(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        self.journal.record_result(0, "call-1", {"ok": False, "code": "OUTCOME_UNKNOWN", "outcome_unknown": True})
        result = {"ok": True, "path": "a.txt", "bytes": 5}
        messages = [assistant([call()]), receipt("call-1", result)]
        original = copy.deepcopy(messages)
        self.assertFalse(self.journal.recover(messages)["changed"])
        self.assertEqual(messages, original)
        self.assertEqual(self.journal.unresolved(), [])
        self.assertEqual(self.journal.entries()[0]["result"], result)

    def test_stored_real_receipt_replaces_canonical_unknown(self):
        self.journal.prepare_batch([call()], 0)
        result = {"ok": False, "error": "Target exists", "code": "EXISTS"}
        self.journal.record_result(0, "call-1", result)
        messages = [assistant([call()]), receipt("call-1", {"ok": False, "code": "OUTCOME_UNKNOWN", "recovery": True})]
        self.journal.recover(messages)
        self.assertEqual(self.result(messages), result)

    def test_resolutions_are_durable_explicit_and_replace_only_unknowns(self):
        for resolution, code, ok in (("completed", "USER_CONFIRMED_EFFECT", True),
                                     ("not_executed", "USER_CONFIRMED_NOT_EXECUTED", False)):
            with self.subTest(resolution=resolution):
                journal = CallJournal("chat", resolution, self.directory)
                journal.prepare_batch([call()], 0)
                journal.set_phase(0, "call-1", "started")
                journal.record_result(0, "call-1", {"ok": False, "code": "OUTCOME_UNKNOWN"})
                messages = []
                journal.recover(messages)
                journal.resolve(0, "call-1", resolution)
                reopened = CallJournal("chat", resolution, self.directory)
                self.assertEqual(reopened.unresolved(), [])
                reopened.recover(messages)
                result = self.result(messages)
                self.assertEqual(result["code"], code)
                self.assertEqual(result["ok"], ok)
                self.assertTrue(result["user_confirmed"])
                if ok:
                    self.assertTrue(result["result_unavailable"])
                self.assertFalse(reopened.recover(messages)["changed"])
                with self.assertRaises(ValueError):
                    reopened.resolve(0, "call-1", resolution)

    def test_never_started_and_real_receipts_cannot_be_resolved(self):
        self.journal.prepare_batch([call()], 0)
        with self.assertRaises(ValueError):
            self.journal.resolve(0, "call-1", "completed")
        self.journal.record_result(0, "call-1", {"ok": True, "receipt": "saved"})
        before = self.journal.path.read_bytes()
        with self.assertRaises(ValueError):
            self.journal.resolve(0, "call-1", "not_executed")
        with self.assertRaises(ValueError):
            self.journal.record_result(0, "call-1", {"ok": True, "receipt": "different"})
        self.assertEqual(self.journal.path.read_bytes(), before)

    def test_field_only_unknown_result_is_unresolved_and_can_be_resolved(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        self.journal.record_result(0, "call-1", {"ok": False, "code": "TRANSPORT_ERROR", "outcome_unknown": True})
        self.assertEqual(len(self.journal.unresolved()), 1)
        self.journal.resolve(0, "call-1", "not_executed")
        self.assertEqual(self.journal.unresolved(), [])

    def test_started_effect_can_be_resolved_when_no_receipt_was_written(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        self.journal.resolve(0, "call-1", "completed")
        messages = []
        self.journal.recover(messages)
        self.assertEqual(self.result(messages)["code"], "USER_CONFIRMED_EFFECT")

    def test_torn_final_row_is_ignored_and_repaired_before_append(self):
        self.journal.prepare_batch([call()], 0)
        with self.journal.path.open("ab") as stream:
            stream.write(b'{"event":"phase","broken":"\xd0')
        before = self.journal.path.read_bytes()
        messages = []
        self.assertTrue(self.journal.recover(messages)["warnings"])
        self.assertEqual(self.result(messages)["code"], "NOT_EXECUTED")
        self.assertEqual(self.journal.path.read_bytes(), before)
        self.journal.set_phase(0, "call-1", "started")
        self.assertEqual(self.journal.entries()[0]["phase"], "started")
        self.assertEqual(len(self.journal.path.read_bytes().splitlines()), 2)

    def test_valid_unterminated_final_event_is_kept_when_appending(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.path.write_bytes(self.journal.path.read_bytes().rstrip(b"\n"))
        self.journal.set_phase(0, "call-1", "started")
        self.assertEqual(self.journal.entries()[0]["phase"], "started")
        self.assertEqual(len(self.journal.path.read_bytes().splitlines()), 2)

    def test_complete_corrupt_row_is_not_silently_skipped(self):
        self.journal.prepare_batch([call()], 0)
        with self.journal.path.open("ab") as stream:
            stream.write(b'{"broken":\n')
            stream.write(b'{"another":"row"}\n')
        before = self.journal.path.read_bytes()
        messages = []
        for action in (self.journal.entries, lambda: self.journal.recover(messages),
                       lambda: self.journal.set_phase(0, "call-1", "started")):
            with self.assertRaisesRegex(ValueError, "corrupt"):
                action()
        self.assertEqual(self.journal.path.read_bytes(), before)
        self.assertEqual(messages, [])

    def test_identity_mismatches_leave_history_and_file_untouched(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        before = self.journal.path.read_bytes()
        mismatches = [
            [{"role": "user", "content": "different transcript"}],
            [assistant([call("different-id")])],
            [assistant([call(name="different_name")])],
            [assistant([call(arguments='{"path":"different.txt"}')])],
            [assistant([call()]), receipt("unknown-id", {"ok": True})],
            [assistant([call()]), receipt("call-1", {"ok": True}), receipt("call-1", {"ok": True})],
        ]
        for messages in mismatches:
            with self.subTest(messages=messages):
                original = copy.deepcopy(messages)
                with self.assertRaises(ValueError):
                    self.journal.recover(messages)
                self.assertEqual(messages, original)
                self.assertEqual(self.journal.path.read_bytes(), before)

    def test_all_anchors_validate_before_adopting_any_canonical_receipt(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started")
        self.journal.prepare_batch([call("call-2")], 3)
        messages = [assistant([call()]), receipt("call-1", {"ok": True}),
                    {"role": "user", "content": "continue"}, assistant([call("wrong")])]
        original, before = copy.deepcopy(messages), self.journal.path.read_bytes()
        with self.assertRaises(ValueError):
            self.journal.recover(messages)
        self.assertEqual(self.journal.path.read_bytes(), before)
        self.assertEqual(messages, original)
        self.assertEqual(len(self.journal.unresolved()), 1)

    def test_multiple_missing_tail_batches_restore_at_their_exact_anchors(self):
        self.journal.prepare_batch([call()], 1)
        self.journal.record_result(1, "call-1", {"ok": True, "bytes": 5})
        self.journal.prepare_batch([call("call-2", "read_file")], 3)
        self.journal.set_phase(3, "call-2", "started", effectful=False)
        messages = [{"role": "user", "content": "do it"}]
        self.journal.recover(messages)
        self.assertEqual(len(messages), 5)
        self.assertEqual(messages[3]["tool_calls"][0]["id"], "call-2")
        self.assertFalse(self.journal.recover(messages)["changed"])

    def test_anchor_beyond_history_is_not_blindly_appended(self):
        self.journal.prepare_batch([call()], 4)
        messages = [{"role": "user", "content": "unrelated"}]
        with self.assertRaisesRegex(ValueError, "beyond"):
            self.journal.recover(messages)
        self.assertEqual(len(messages), 1)

    def test_conflicting_real_receipts_fail_without_overwriting_either_copy(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.record_result(0, "call-1", {"ok": True, "bytes": 5})
        messages = [assistant([call()]), receipt("call-1", {"ok": True, "bytes": 6})]
        original, before = copy.deepcopy(messages), self.journal.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.journal.recover(messages)
        self.assertEqual(messages, original)
        self.assertEqual(self.journal.path.read_bytes(), before)

    def test_batch_and_call_collisions_are_rejected_before_append(self):
        self.journal.prepare_batch([call()], 0)
        before = self.journal.path.read_bytes()
        self.journal.prepare_batch([call()], 0)
        self.assertEqual(self.journal.path.read_bytes(), before)
        for calls, index in (([call("different")], 0), ([call("x"), call("x")], 3),
                             ([call("overlap")], 1)):
            with self.assertRaises(ValueError):
                self.journal.prepare_batch(calls, index)
        self.assertEqual(self.journal.path.read_bytes(), before)

    def test_row_limit_and_invalid_json_values_preserve_the_existing_file(self):
        self.journal.prepare_batch([call()], 0)
        before = self.journal.path.read_bytes()
        for result in ({"ok": True, "text": "x" * MAX_RECORD_BYTES}, {"ok": True, "value": float("nan")}):
            with self.assertRaises(ValueError):
                self.journal.record_result(0, "call-1", result)
        self.assertEqual(self.journal.path.read_bytes(), before)

    def test_phases_cannot_move_backwards_or_reclassify_started_effects(self):
        self.journal.prepare_batch([call()], 0)
        self.journal.set_phase(0, "call-1", "started", effectful=True)
        for phase, effectful in (("prepared", True), ("awaiting_approval", True), ("started", False)):
            with self.assertRaises(ValueError):
                self.journal.set_phase(0, "call-1", phase, effectful=effectful)

    def test_recovery_restores_missing_assistant_content(self):
        self.journal.prepare_batch([call()], 0, "Working on the requested file")
        messages = [assistant([call()])]
        self.journal.recover(messages)
        self.assertEqual(messages[0]["content"], "Working on the requested file")

    def test_separate_instances_share_the_same_transaction_lock(self):
        other = CallJournal("chat", "epoch-1", self.directory)
        self.assertIs(other._lock, self.journal._lock)


if __name__ == "__main__":
    unittest.main()
