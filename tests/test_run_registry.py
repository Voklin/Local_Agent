"""Durable ledger, orphan recovery, bounded child identities and actual FIFO/stream ownership."""
import asyncio
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
import httpx
from agent.run_registry import RunRegistry,owner_alive
from agent.inference_scheduler import InferenceScheduler,InferenceAttempt
from agent.model_client import ScheduledStream,ModelClient
from agent.operation_context import OperationContext
from agent.storage import Storage,encode


class RunRegistryTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.registry=RunRegistry(self.root)

    def run_context(self,**kwargs):
        """Use only a synthetic connection/model, with caller overrides for negative tests."""
        return self.registry.begin(**{'kind':'ide','model':'fixture','base_url':'https://example.invalid/v1','chat_id':'a'*32,**kwargs})

    def test_resume_epochs_are_independent_and_duplicate_ids_are_rejected(self):
        first=self.run_context(journal_id='same-journal');first.finish('paused')
        second=self.run_context(journal_id='same-journal')
        second.observe({'tool_calls':100,'run_state':'running'});second.record_tool()
        self.assertEqual(second.snapshot()['tool_calls'],1);self.assertEqual(first.snapshot()['tool_calls'],0)
        self.assertNotEqual(first.id,second.id);self.assertEqual(len(self.registry.history('a'*32)),2)
        with self.assertRaises(ValueError):self.run_context(run_id=first.id)

    def test_child_inheritance_bounds_and_cascade_cancel(self):
        parent=self.run_context();child=self.run_context(parent=parent)
        with self.assertRaises(ValueError):self.run_context(parent=parent,model='another')
        with self.assertRaises(ValueError):self.run_context(parent=child)
        self.run_context(parent=parent);self.run_context(parent=parent)
        with self.assertRaises(ValueError):self.run_context(parent=parent)
        self.registry.cancel(parent.id)
        self.assertTrue(child.operation.is_set());self.assertTrue(parent.operation.is_set())
        self.assertTrue(child.snapshot()['cancel_requested'])

    def test_ledger_idempotent_usage_and_reservations_are_not_charges(self):
        run=self.run_context();identity=self.registry.attempt(run.id,'agent',{'input_tokens_estimate':100,'output_tokens_reserved':200})
        ledger=run.snapshot()['ledger'];self.assertEqual(ledger['http_attempts'],0);self.assertEqual(ledger['active_reserved_tokens'],300)
        for _ in range(2):self.registry.update_attempt(identity,http_attempts=1,state='finished',usage={'input_tokens':10,'output_tokens':3})
        ledger=run.snapshot()['ledger'];self.assertEqual(ledger['requests_reported'],1);self.assertEqual(ledger['input_tokens'],10);self.assertEqual(ledger['active_reserved_tokens'],0)
        self.assertEqual(ledger['reservations'],1)

    def test_orphan_recovery_releases_estimates_and_never_replays_http(self):
        for phase in ('running','paused'):
            with self.subTest(phase=phase):
                run=self.run_context();identity=self.registry.attempt(run.id,'agent',{'output_tokens_reserved':100})
                self.registry.update_attempt(identity,http_attempts=1)
                run.observe({'run_state':phase})
                restarted=RunRegistry(self.root,alive=lambda _pid:False)
                row=restarted.snapshot(run.id)
                self.assertEqual(row['state'],'paused');self.assertTrue(row['recovered'])
                self.assertEqual(row['ledger']['active_reserved_tokens'],0);self.assertEqual(row['ledger']['interrupted'],1)
                self.assertEqual(row['ledger']['http_attempts'],1);self.assertEqual(row['ledger']['requests_reported'],0)
                self.assertFalse(restarted.handles)

    def test_live_owner_is_preserved_and_pid_check_does_not_signal_it(self):
        self.assertTrue(owner_alive(os.getpid()))
        run=self.run_context();row=RunRegistry(self.root).snapshot(run.id)
        self.assertEqual(row['state'],'running');self.assertNotIn('recovered',row)

    def test_approval_time_is_separate_from_elapsed_and_model_queue(self):
        run=self.run_context();run.observe({'run_state':'waiting_approval'});time.sleep(.04)
        run.record_tool();run.record_tool();run.observe({'run_state':'running','tool_calls':2});run.finish()
        value=run.snapshot();self.assertGreaterEqual(value['approval_ms'],25)
        self.assertLessEqual(value['approval_ms'],value['elapsed_ms']);self.assertEqual(value['ledger']['queue_ms'],0)
        self.assertEqual(value['tool_calls'],2)

    def test_schema_two_upgrade_preserves_existing_task_and_backup_contains_runs(self):
        database=Storage(self.root).ready()
        with database.transaction() as c:
            c.execute('DROP TABLE inference_attempts');c.execute('DROP TABLE runs');c.execute('PRAGMA user_version=2')
            c.execute('INSERT INTO tasks VALUES(?,?)',('fixture',encode({'status':'paused','journal_id':'keep'})))
        run=self.run_context();run.finish()
        with database.transaction() as c:
            self.assertEqual(c.execute('PRAGMA user_version').fetchone()[0],3)
            self.assertEqual(json.loads(c.execute('SELECT data FROM tasks WHERE chat_id=?',('fixture',)).fetchone()[0])['journal_id'],'keep')
        import zipfile
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        archive=Path(temporary.name)/'snapshot.zip';database.backup(archive)
        restored=self.root/'restored';restored.mkdir()
        with zipfile.ZipFile(archive) as source:source.extract('neutral.sqlite3',restored)
        self.assertEqual(RunRegistry(restored).snapshot(run.id)['state'],'completed')

    def test_delete_chat_also_deletes_its_run_metadata(self):
        from unittest.mock import patch
        from agent import chat_store
        run=self.run_context();run.finish()
        with patch.object(chat_store,'_database',return_value=self.registry.ready()):chat_store.delete_chat('a'*32)
        self.assertEqual(self.registry.history('a'*32),[])

    def test_model_binding_rejects_child_or_parent_configuration_drift(self):
        run=self.run_context();client=ModelClient(run.base_url,'',run.operation);self.addCleanup(client.close)
        with self.assertRaises(ValueError):client.create(model='another',messages=[],stream=False)
        self.assertEqual(run.snapshot()['ledger']['http_attempts'],0)


class SchedulerTests(unittest.IsolatedAsyncioTestCase):
    async def test_fifo_waiter_cancel_and_stale_release(self):
        scheduler=InferenceScheduler();first=await scheduler.acquire(OperationContext(),'parent')
        cancelled=OperationContext();waiting=asyncio.create_task(scheduler.acquire(cancelled,'cancelled'))
        child=asyncio.create_task(scheduler.acquire(OperationContext(),'child'))
        await asyncio.sleep(.05);self.assertEqual(scheduler.status()['waiting'],2)
        cancelled.set()
        with self.assertRaises(asyncio.CancelledError):await waiting
        self.assertEqual(scheduler.status()['waiting'],1);scheduler.release(first)
        second=await asyncio.wait_for(child,1);self.assertEqual(second['run_id'],'child')
        scheduler.release(first);self.assertTrue(scheduler.status()['busy']);scheduler.release(second)
        self.assertFalse(scheduler.status()['busy'])

    async def test_parent_waits_for_child_without_holding_generation_lease(self):
        scheduler=InferenceScheduler();parent=await scheduler.acquire(OperationContext(),'parent');scheduler.release(parent)
        child=await asyncio.wait_for(scheduler.acquire(OperationContext(),'child'),1);scheduler.release(child)
        continued=await asyncio.wait_for(scheduler.acquire(OperationContext(),'parent'),1);scheduler.release(continued)
        self.assertFalse(scheduler.status()['busy'])

    async def test_stream_close_holds_lease_until_sdk_cleanup_finishes(self):
        scheduler=InferenceScheduler();attempt=await InferenceAttempt(OperationContext(),'agent',scheduler=scheduler).acquire()
        entered=asyncio.Event();release=asyncio.Event()
        class Response:
            async def close(self):entered.set();await release.wait()
        stream=ScheduledStream(Response(),attempt);closing=asyncio.create_task(stream.close(asyncio.CancelledError()))
        await entered.wait();next_request=asyncio.create_task(scheduler.acquire(OperationContext(),'next'));await asyncio.sleep(.05)
        closing.cancel();await asyncio.sleep(.02);closing.cancel();await asyncio.sleep(.02)
        self.assertTrue(scheduler.status()['busy']);self.assertFalse(next_request.done())
        release.set();await closing;ticket=await asyncio.wait_for(next_request,1);scheduler.release(ticket)

    async def test_cancelled_queued_reservation_has_no_http_or_token_charge(self):
        with tempfile.TemporaryDirectory() as directory:
            registry=RunRegistry(directory);run=registry.begin(kind='chat',model='fixture',base_url='https://example.invalid/v1')
            scheduler=InferenceScheduler();first=await scheduler.acquire(OperationContext())
            task=asyncio.create_task(InferenceAttempt(run.operation,'agent',{'output_tokens_reserved':500},scheduler).acquire())
            await asyncio.sleep(.04);run.operation.set()
            with self.assertRaises(asyncio.CancelledError):await task
            ledger=run.snapshot()['ledger'];self.assertEqual(ledger['http_attempts'],0);self.assertEqual(ledger['active_reserved_tokens'],0)
            self.assertEqual(ledger['requests_reported'],0);self.assertTrue(scheduler.status()['busy']);scheduler.release(first)

    async def test_failed_close_blocks_reuse_until_owning_client_cleanup(self):
        scheduler=InferenceScheduler();attempt=await InferenceAttempt(OperationContext(),'agent',scheduler=scheduler).acquire()
        class Response:
            async def close(self):raise OSError('synthetic close failure')
        with self.assertRaises(OSError):await ScheduledStream(Response(),attempt).close()
        self.assertTrue(scheduler.status()['needs_attention'])
        with self.assertRaises(ValueError):await scheduler.acquire(OperationContext(),'next')
        self.assertEqual(scheduler.status()['waiting'],0)
        scheduler.release(attempt.ticket)
        ticket=await scheduler.acquire(OperationContext(),'after-owner-cleanup');scheduler.release(ticket)
