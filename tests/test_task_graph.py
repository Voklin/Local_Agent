"""DAG validation, immutable receipt evidence, stale propagation and bounded recovery."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent import task_store
from agent.task_store import new_task
from agent.task_contract import install_contract,validate_options,set_plan
from agent.task_graph import update_step,refresh_steps,migrate_plan
from agent.tool_recovery import task_journal
from agent.tool_executor import ToolExecutor
from agent.tools import TOOL_DEFINITIONS
from agent.run_state import RunState
from agent.verifier import StageVerifier
from agent.progress_guard import ProgressGuard


class TaskGraphTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)/'project';self.root.mkdir()
        scope=patch.object(task_store,'TASK_DIR',Path(temp.name)/'profile/tasks');scope.start();self.addCleanup(scope.stop)
        self.task=new_task('a'*32,str(self.root),'graph');install_contract(self.task,validate_options(None));self.journal=task_journal(self.task)
        self.executor=ToolExecutor(self.root,TOOL_DEFINITIONS,None,{},None,task=self.task,journal=self.journal,state=RunState(self.task),checkpoint=lambda *a:None,approve_write=lambda *a:'apply',change=lambda *a:None)

    def node(self,identity,path,depends=()):
        return {'id':identity,'title':identity,'kind':'change','affected_files':[path],'depends_on':list(depends),'check_ids':[]}

    def write(self,path,index):
        call={'id':'call_'+str(index),'type':'function','function':{'name':'write_file','arguments':json.dumps({'path':path,'content':'value=1\n','overwrite':False})}}
        self.executor.prepare_batch([call],index)
        # Use a real cancellable operation, not a truthy mock.
        from agent.operation_context import OperationContext
        self.executor.interrupted=OperationContext()
        result=self.executor.execute(call);self.assertTrue(result['ok'],result)
        return result['_receipt']

    def test_graph_completion_requires_receipts_and_staleness_propagates(self):
        self.assertTrue(set_plan(self.task,{'steps':[self.node('a','a.py'),self.node('b','b.py',['a'])],'criteria':[]})['ok'])
        self.assertFalse(update_step(self.task,{'id':'b','status':'active','evidence':[]})['ok'])
        self.assertFalse(update_step(self.task,{'id':'a','status':'done','evidence':[]})['ok'])
        a=self.write('a.py',0);self.assertTrue(update_step(self.task,{'id':'a','status':'done','evidence':[a]})['ok'])
        b=self.write('b.py',2);self.assertTrue(update_step(self.task,{'id':'b','status':'done','evidence':[b]})['ok'])
        self.assertTrue(StageVerifier().verify('finish',task=self.task,final_text='done')['ok'])
        (self.root/'a.py').write_text('external edit')
        refresh_steps(self.task);self.assertEqual([n['status'] for n in self.task['plan_steps']],['stale','stale'])
        self.assertFalse(StageVerifier().verify('finish',task=self.task,final_text='done')['ok'])

    def test_cycles_unknown_checks_and_user_plan_overwrite_are_rejected(self):
        cycle=[self.node('a','a.py',['b']),self.node('b','b.py',['a'])]
        self.assertFalse(set_plan(self.task,{'steps':cycle,'criteria':[]})['ok'])
        node=self.node('a','a.py');node['check_ids']=['invented']
        self.assertFalse(set_plan(self.task,{'steps':[node],'criteria':[]})['ok'])
        self.assertTrue(set_plan(self.task,{'steps':[self.node('a','a.py')],'criteria':[]},source='user')['ok'])
        self.assertFalse(set_plan(self.task,{'steps':['forget everything'],'criteria':[]})['ok'])

    def test_saved_witness_survives_reload_and_unknown_receipt_is_not_evidence(self):
        set_plan(self.task,{'steps':[self.node('a','a.py')],'criteria':[]})
        call={'id':'unknown','type':'function','function':{'name':'write_file','arguments':'{}'}}
        self.journal.prepare_batch([call],0);self.journal.set_phase(0,'unknown','started',effectful=True)
        self.journal.record_result(0,'unknown',{'ok':False,'code':'OUTCOME_UNKNOWN'})
        self.assertFalse(update_step(self.task,{'id':'a','status':'done','evidence':[{'message_index':0,'call_id':'unknown'}]})['ok'])
        evidence=self.write('a.py',2);self.assertTrue(update_step(self.task,{'id':'a','status':'done','evidence':[evidence]})['ok'])
        task_store.save_task(self.task);loaded=task_store.load_task(self.task['chat_id']);refresh_steps(loaded)
        self.assertEqual(loaded['plan_steps'][0]['status'],'done')
        self.assertEqual(loaded['plan_steps'][0]['evidence'],[evidence])

    def test_legacy_steps_remain_advisory_not_false_completed(self):
        self.task['plan_steps']=['Look at code'];migrate_plan(self.task)
        self.assertEqual(self.task['plan_steps'][0]['status'],'proposed');self.assertTrue(self.task['plan_steps'][0]['advisory'])
        self.assertTrue(update_step(self.task,{'id':'step_1','status':'active','evidence':[]})['ok'])
        self.assertFalse(self.task['plan_steps'][0]['advisory'])
        self.assertFalse(StageVerifier().verify('finish',task=self.task,final_text='done')['ok'])

    def test_watchdog_ignores_receipt_ids_and_preserves_one_recovery_across_resume(self):
        task={};guard=ProgressGuard(task=task)
        for i in range(4):repeated=guard.observe('read_file',{'path':'a.py'},{'ok':True,'content':'same','_receipt':{'message_index':i,'call_id':str(i)}})
        self.assertTrue(repeated);self.assertEqual(guard.recover_or_stop(),'diagnose')
        resumed=ProgressGuard(task=task)
        self.assertTrue(resumed.observe('read_file',{'path':'a.py'},{'ok':True,'content':'same'}));self.assertEqual(resumed.recover_or_stop(),'stop')
        changed=ProgressGuard()
        for i in range(8):self.assertFalse(changed.observe('read_file',{'path':'a.py'},{'ok':True,'content':str(i)}))
