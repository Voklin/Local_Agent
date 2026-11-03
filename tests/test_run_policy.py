"""Opt-in monetary planning across children/resume without adding local-auto caps."""
import tempfile
import unittest
from pathlib import Path
from agent.run_policy import validate_spending,SpendingLimitError,capacity_failure
from agent.run_registry import RunRegistry


class RunPolicyTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.registry=RunRegistry(Path(temp.name))
        self.policy={'enabled':True,'amount':.0003,'input_per_million':1,'output_per_million':1,'currency':'USD'}

    def begin(self,**kwargs):
        return self.registry.begin(**{'kind':'ide','model':'fixture','base_url':'https://example.invalid/v1','chat_id':'a'*32,'journal_id':'logical-task','spending_policy':self.policy,**kwargs})

    def test_children_and_resume_share_reported_and_unknown_cost(self):
        parent=self.begin();child=self.begin(parent=parent)
        attempt=self.registry.attempt(child.id,'agent',{'input_tokens_estimate':100,'output_tokens_reserved':100})
        self.registry.update_attempt(attempt,http_attempts=1,state='failed')
        self.assertAlmostEqual(parent.snapshot()['spending']['estimated_spent'],.0002)
        self.assertEqual(parent.snapshot()['spending']['unknown_attempts'],1)
        with self.assertRaises(SpendingLimitError):self.registry.attempt(parent.id,'agent',{'output_tokens_reserved':200})
        child.finish('failed');parent.finish('paused');resumed=self.begin()
        with self.assertRaises(SpendingLimitError):self.registry.attempt(resumed.id,'agent',{'output_tokens_reserved':200})
        self.assertEqual(resumed.snapshot()['ledger']['http_attempts'],0)

    def test_cancel_before_http_releases_money_and_exact_usage_is_idempotent(self):
        run=self.begin();attempt=self.registry.attempt(run.id,'agent',{'output_tokens_reserved':200})
        self.assertAlmostEqual(run.snapshot()['spending']['reserved'],.0002)
        self.registry.update_attempt(attempt,state='interrupted')
        self.assertEqual(run.snapshot()['spending']['estimated_spent'],0)
        attempt=self.registry.attempt(run.id,'agent',{'output_tokens_reserved':200})
        for _ in range(2):self.registry.update_attempt(attempt,state='finished',http_attempts=1,usage={'input_tokens':10,'output_tokens':20})
        self.assertAlmostEqual(run.snapshot()['spending']['estimated_spent'],.00003)

    def test_local_auto_ignores_paid_budget_and_unfinished_children_block_completion(self):
        run=self.begin(base_url='http://127.0.0.1:1234/v1');child=self.begin(base_url=run.base_url,parent=run)
        self.registry.attempt(run.id,'agent',{'output_tokens_reserved':1_000_000})
        self.assertNotIn('spending',run.snapshot())
        with self.assertRaises(ValueError):run.finish()
        self.registry.cancel(run.id);self.assertTrue(child.operation.is_set());child.finish('paused');run.finish('paused')

    def test_invalid_prices_and_capacity_error_classification(self):
        for value in ({'enabled':True}, {**self.policy,'amount':float('nan')},{**self.policy,'input_per_million':-1}):
            with self.assertRaises(ValueError):validate_spending(value)
        self.assertTrue(capacity_failure(Exception('CUDA out of memory')))
        self.assertFalse(capacity_failure(Exception('HTTP 500 temporary')))

    def test_durable_receipt_and_epoch_tool_counter_commit_together(self):
        from unittest.mock import patch
        from agent import task_store
        from agent.call_journal import CallJournal
        run=self.begin()
        with patch.object(task_store,'TASK_DIR',Path(self.registry.directory)/'tasks'):
            journal=CallJournal('a'*32,'logical-task')
            call={'id':'receipt','type':'function','function':{'name':'read_file','arguments':'{"path":"a.py"}'}}
            journal.prepare_batch([call],0)
            result={'ok':True,'content':'large evidence '*10000,'_run_id':run.id}
            journal.record_result(0,'receipt',result)
            # No engine.record_tool or subsequent checkpoint is necessary.
            self.assertEqual(run.snapshot()['tool_calls'],1)
            journal.record_result(0,'receipt',result)
            self.assertEqual(run.snapshot()['tool_calls'],1)
