"""IDE adapters retain the canonical approval/journal/snapshot execution boundary."""
import json
import unittest
from unittest.mock import Mock
from tests import test_tool_execution as fixture
from tests.test_call_journal import call
from core.python.ide_sessions import IdeWorkspaceAdapter
from agent.tools import preview_file_change


class IdeExecutionTests(unittest.TestCase):
    setUp=fixture.ToolExecutionTests.setUp
    executor=fixture.ToolExecutionTests.executor

    def write_call(self):
        (self.root/'a.txt').write_text('old',encoding='utf8')
        return call('editor','write_file',json.dumps({'path':'a.txt','content':'new','overwrite':True}))

    def test_dirty_editor_rejects_before_approval_and_never_uses_python_writer(self):
        tool=self.write_call();runner=Mock();approval=Mock();executor=self.executor(runner=runner,approve_write=approval)
        executor.workspace_adapter=Mock();executor.workspace_adapter.prepare.return_value={'ok':False,'code':'DIRTY_BUFFER','error':'Save first'}
        executor.prepare_batch([tool],0);result=executor.execute(tool)
        self.assertEqual(result['code'],'DIRTY_BUFFER');runner.assert_not_called();approval.assert_not_called()
        executor.workspace_adapter.execute.assert_not_called();self.assertEqual((self.root/'a.txt').read_text(),'old')

    def test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation(self):
        tool=self.write_call();runner=Mock();executor=self.executor(runner=runner);adapter=executor.workspace_adapter=Mock()
        adapter.prepare.return_value={'ok':True,'editor_state':[{'version':3}]}
        def effect(*_):
            (self.root/'a.txt').write_text('new',encoding='utf8');return {'ok':True,'path':'a.txt','editor':True}
        adapter.execute.side_effect=effect;executor.prepare_batch([tool],0);result=executor.execute(tool)
        self.assertTrue(result['ok']);self.assertTrue(result['editor']);self.assertEqual(result['workspace_generation'],1)
        runner.assert_not_called();adapter.execute.assert_called_once();self.assertEqual(self.journal.unresolved(),[])
        self.assertTrue(self.task.get('snapshot_group_id'))

    def test_unknown_editor_effect_is_not_replayed_or_sent_to_python_writer(self):
        tool=self.write_call();runner=Mock();executor=self.executor(runner=runner);adapter=executor.workspace_adapter=Mock()
        adapter.prepare.return_value={'ok':True,'editor_state':[]};adapter.execute.return_value={'ok':False,'code':'OUTCOME_UNKNOWN','error':'Lost editor receipt'}
        executor.prepare_batch([tool],0);result=executor.execute(tool)
        self.assertEqual(result['code'],'OUTCOME_UNKNOWN');runner.assert_not_called();self.assertTrue(self.journal.unresolved())

    def test_stale_disk_never_reaches_external_editor_apply(self):
        self.write_call();owner=Mock();owner.views={'scope':{'root':self.root}};adapter=IdeWorkspaceAdapter(owner,'scope')
        args={'path':'a.txt','content':'new','overwrite':True};preview=preview_file_change(self.root,'a.txt','new')
        (self.root/'a.txt').write_text('external',encoding='utf8')
        result=adapter.execute('write_file',args,preview,Mock())
        self.assertEqual(result['code'],'FILE_CHANGED');owner.request.assert_not_called()
