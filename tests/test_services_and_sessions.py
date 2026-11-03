"""Shared deadline/gate, protocol validation and real persistent MCP transports."""
import asyncio
from pathlib import Path
import queue
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from agent.capability_profiles import mode_groups
from agent.mcp_client import MCPClient
from agent.operation_context import OperationContext,InferenceGate
from core.python.protocol import validate_request
from core.python.session_service import SessionService
from core.python.task_service import TaskService


class ServiceBoundaryTests(unittest.TestCase):
    def setUp(self):
        """Keep durable run telemetry in an isolated profile, including mocked probe operations."""
        from agent import task_store
        directory=tempfile.TemporaryDirectory();self.addCleanup(directory.cleanup)
        scope=patch.object(task_store,'TASK_DIR',Path(directory.name)/'tasks');scope.start();self.addCleanup(scope.stop)

    def test_child_deadline_is_bounded_and_parent_cancel_is_immediate(self):
        parent=OperationContext(.08);child=parent.child(10)
        self.assertLessEqual(child.remaining(),.081)
        self.assertTrue(child.wait(.3));self.assertTrue(parent.is_set())
        parent=OperationContext();child=parent.child(10);parent.set()
        self.assertTrue(child.wait(.1))

    def test_stale_gate_owner_cannot_release_a_new_inference(self):
        gate=InferenceGate();first=gate.begin('first')
        with self.assertRaises(ValueError):gate.begin('second')
        gate.end(first.id);second=gate.begin('second');gate.end(first.id)
        self.assertTrue(gate.status()['busy']);gate.cancel();self.assertTrue(second.context.is_set())
        gate.end(second.id);self.assertFalse(gate.status()['busy'])

    def test_approval_wait_freezes_nested_deadlines_but_not_cancellation(self):
        """Human think time cannot expire parent/child budgets; Stop still propagates."""
        with patch('agent.operation_context.time.monotonic',return_value=10) as clock:
            parent=OperationContext(20);child=parent.child(10)
            clock.return_value=12
            with child.approval_wait():
                clock.return_value=1000
                self.assertEqual(child.remaining(),8)
                self.assertEqual(parent.remaining(),18)
                with child.approval_wait():
                    clock.return_value=2000
                    self.assertFalse(child.is_set())
                self.assertEqual(child.remaining(),8)
            self.assertEqual(child.remaining(),8)
            clock.return_value=2007
            self.assertEqual(child.remaining(),1)
            with child.approval_wait():
                parent.set()
                self.assertTrue(child.is_set())

    def test_approval_exception_restores_deadline_once(self):
        """An approval callback failure must not leave the operation permanently suspended."""
        with patch('agent.operation_context.time.monotonic',return_value=10) as clock:
            operation=OperationContext(5)
            with self.assertRaises(ValueError):
                with operation.approval_wait():
                    clock.return_value=100
                    raise ValueError('fixture approval failed')
            self.assertEqual(operation.remaining(),5)
            clock.return_value=106
            self.assertTrue(operation.is_set())

    def test_protocol_rejects_wrong_version_ids_and_non_boolean_approval(self):
        with self.assertRaises(ValueError):validate_request({'protocol_version':2,'method':'start_task','params':{}})
        with self.assertRaises(ValueError):validate_request({'method':'snapshot_apply','params':{'chat_id':'chat','proposal_id':'id','confirmed':'yes'}})
        with self.assertRaises(ValueError):validate_request({'method':'start_task','params':{'run_id':'not-an-id'}})
        self.assertEqual(validate_request({'method':'cancel_task','params':{}})[0],'cancel_task')

    def test_mode_profiles_cannot_enable_project_tools_in_chat_or_voice(self):
        definitions=[('project',['write']),('commands',['run']),('desktop',['open'])]
        self.assertEqual(dict(mode_groups('voice','root',definitions))['project'],[])
        self.assertEqual(dict(mode_groups('chat','root',definitions))['commands'],[])
        self.assertEqual(dict(mode_groups('ide','',definitions))['project'],[])

    def test_probe_and_task_share_one_heavy_inference_gate(self):
        service=TaskService(lambda _:None);started=threading.Event();answers=queue.Queue()
        def probe(*args,cancelled=None,**kwargs):
            started.set();cancelled.wait(2);return {'ok':False,'canceled':True}
        try:
            with patch('core.python.task_service.probe_model',side_effect=probe):
                service.start_model_probe({'base_url':'http://127.0.0.1:1234/v1','model':'fixture'},answers.put)
                self.assertTrue(started.wait(1))
                with self.assertRaisesRegex(ValueError,'Уже выполняется'):service.start('',{'mode':'chat','prompt':'hello'})
                service.cancel_model_setup();self.assertTrue(answers.get(timeout=2)['canceled'])
                service.probe_thread.join(1)
                self.assertFalse(service.inference.status()['busy'])
        finally:service.shutdown();service.extensions.shutdown()

    def test_mcp_reuses_process_and_invalidates_without_replaying_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            client=MCPClient(Path(directory));fixture=Path(__file__).parent/'fixtures/mcp_echo.py'
            server={'id':'sessions','transport':'stdio','command':sys.executable,'args':[str(fixture)],'timeout':10}
            try:
                first=client.operation(server,'session_identity')
                second=client.operation({**server,'name':'Updated label','tools':[{'name':'discovered'}]},'session_identity')
                self.assertTrue(first['ok'],first);self.assertEqual(first['content'],second['content'])
                self.assertEqual(client.pool.status()['active'],1)
                self.assertEqual(client.pool.status()['sessions'][0]['calls'],2)
                client.pool.invalidate('sessions')
                deadline=time.monotonic()+3
                while client.pool.status()['active'] and time.monotonic()<deadline:time.sleep(.025)
                third=client.operation(server,'session_identity');self.assertTrue(third['ok'],third)
                self.assertNotEqual(first['content'],third['content'])
            finally:client.shutdown()
            self.assertEqual(client.pool.status()['active'],0)

    def test_mcp_cancellation_during_connect_is_prompt(self):
        from contextlib import asynccontextmanager
        from agent.mcp_sessions import MCPSessionPool
        @asynccontextmanager
        async def connect(*args):
            await asyncio.sleep(20)
            yield object()
        async def exchange(*args):return {'ok':True}
        pool=MCPSessionPool(connect,exchange);cancel=threading.Event()
        timer=threading.Timer(.15,cancel.set);timer.start()
        try:
            started=time.monotonic();result=pool.operation({'id':'slow','timeout':10},'effect',{},cancel,'')
            self.assertEqual(result['code'],'OUTCOME_UNKNOWN');self.assertLess(time.monotonic()-started,2)
        finally:timer.cancel();pool.shutdown()
