"""Read-only lifetime probes and conservative recovery when a PID is reused."""
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock,patch

from agent.process_identity import inspect_process,owner_ended,_linux_process
from agent.run_registry import RunRegistry
from tests import test_run_registry as fixture


class ProcessIdentityTests(unittest.TestCase):
    def test_real_process_lifetime_is_stable_then_dead_without_signalling_probe(self):
        state,token=inspect_process(os.getpid())
        self.assertEqual(state,'alive')
        if os.name=='nt' or sys.platform.startswith('linux'):self.assertIsInstance(token,str)
        self.assertEqual(inspect_process(os.getpid()),(state,token))
        process=subprocess.Popen([sys.executable,'-u','-c','import sys;print("ready",flush=True);sys.stdin.read()'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        try:
            self.assertEqual(process.stdout.readline().strip(),b'ready')
            state,child_token=inspect_process(process.pid);self.assertEqual(state,'alive')
            if token:self.assertNotEqual(child_token,token)
            process.stdin.close();process.wait(5)
            self.assertEqual(owner_ended(process.pid,child_token),'owner_exited')
        finally:
            if process.poll() is None:process.kill();process.wait(5)
            process.stdout.close()

    @unittest.skipUnless(os.name=='nt','Windows query-only process handles')
    def test_windows_probe_never_uses_os_kill(self):
        with patch('os.kill',side_effect=AssertionError('Windows signals are forbidden')):
            self.assertEqual(inspect_process(os.getpid())[0],'alive')

    def test_uncertain_or_incomparable_identity_never_proves_owner_ended(self):
        for state,actual,expected in [('unknown',None,'win-filetime:1'),('alive',None,'win-filetime:1'),
            ('alive','linux-start:new:1','win-filetime:1'),('alive','win-filetime:1',None),('alive','win-filetime:1','win-filetime:1')]:
            with self.subTest(state=state,actual=actual,expected=expected):
                self.assertIsNone(owner_ended(100,expected,lambda _: (state,actual)))
        self.assertEqual(owner_ended(100,'win-filetime:1',lambda _:('alive','win-filetime:2')),'owner_replaced')
        for pid in (0,-1,True,None,'123',2**40):self.assertEqual(inspect_process(pid),('unknown',None))

    def test_linux_start_ticks_parse_complex_process_name(self):
        stat='123 (name with ) parentheses) R '+' '.join(['0']*18+['77'])
        def read(path,*args,**kwargs):
            return stat if path.name=='stat' else 'boot-id'
        with patch.object(Path,'read_text',read):
            self.assertEqual(_linux_process(123),('alive','linux-start:boot-id:77'))


class OwnerRecoveryTests(unittest.TestCase):
    setUp=fixture.RunRegistryTests.setUp
    run_context=fixture.RunRegistryTests.run_context

    def test_reused_pid_recovers_whole_tree_once_preserving_terminal_state(self):
        parent=self.run_context();children=[self.run_context(parent=parent) for _ in range(2)]
        for index,run in enumerate([parent,*children]):
            self.registry.update(run.id,owner_token='win-filetime:old')
            attempt=self.registry.attempt(run.id,'agent',{'output_tokens_reserved':100})
            if index==0:self.registry.update_attempt(attempt,http_attempts=1)
        parent.observe({'run_state':'paused'});children[1].observe({'run_state':'failed'})
        inspect=Mock(return_value=('alive','win-filetime:new'))
        recovered=RunRegistry(self.root,inspect_owner=inspect)
        rows=[recovered.snapshot(run.id) for run in [parent,*children]]
        self.assertEqual([r['state'] for r in rows],['paused','paused','failed'])
        self.assertEqual(inspect.call_count,1)
        for row in rows:
            self.assertEqual(row['recovery_cause'],'owner_replaced');self.assertTrue(row['recovered_at'])
            self.assertEqual(row['ledger']['active_reserved_tokens'],0);self.assertEqual(row['ledger']['interrupted'],1)
        self.assertEqual(rows[0]['ledger']['http_attempts'],1)
        self.assertEqual(rows[1]['parent_id'],parent.id)
        self.assertEqual(recovered.snapshot(parent.id)['ledger'],rows[0]['ledger'])
        self.assertFalse(recovered.handles)

    def test_legacy_or_unreadable_live_owner_keeps_reservations(self):
        run=self.run_context();self.registry.attempt(run.id,'agent',{'output_tokens_reserved':123})
        for token,state,actual in [(None,'alive','win-filetime:new'),('win-filetime:old','unknown',None),('win-filetime:old','alive','win-filetime:old')]:
            self.registry.update(run.id,owner_token=token)
            row=RunRegistry(self.root,inspect_owner=lambda _: (state,actual)).snapshot(run.id)
            self.assertEqual(row['state'],'running');self.assertNotIn('recovered',row)
            self.assertEqual(row['ledger']['active_reserved_tokens'],123)
