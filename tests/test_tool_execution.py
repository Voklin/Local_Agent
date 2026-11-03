"""Execution boundaries, process loss and explicit recovery, without a real model."""
import copy
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from agent import task_store, chat_store
from agent.call_journal import CallJournal
from agent.run_state import RunState
from agent.tool_executor import ToolExecutor
from agent.tool_recovery import recover_task, task_journal
from agent.verifier import StageVerifier
from agent.tools import TOOL_DEFINITIONS
from core.python.task_service import TaskService
from tests.test_call_journal import call, assistant, receipt


# Each child really exits between durable boundaries; no exception unwinding or
# engine finally block can conceal a missing receipt in this test.
CRASH_WORKER = r'''
import json,os,sys,threading
from pathlib import Path
from agent import task_store
from agent.call_journal import CallJournal
from agent.run_state import RunState
from agent.tool_executor import ToolExecutor
from tests.test_call_journal import call,assistant
root=Path(sys.argv[1]);boundary=sys.argv[2];task_store.TASK_DIR=root/'tasks'
task=task_store.new_task('crash-chat','', 'fixture')
(root/'task.json').write_text(json.dumps(task))
calls=[call('saved','read_file','{"path":"a"}'),call('effect','fixture_effect','{}'),call('later','read_file','{"path":"b"}')]
journal=CallJournal(task['chat_id'],task['journal_id'])
def checkpoint(*_):
    entry=journal.entries()[1]
    if boundary=='before_effect' and entry['phase']=='started':os._exit(73)
    if boundary=='after_receipt' and entry['result'] is not None:os._exit(73)
def handler(name,args):
    if name=='read_file':return {'ok':True,'content':'preserved first result'}
    with (root/'effects.txt').open('a') as f:f.write('effect\n');f.flush();os.fsync(f.fileno())
    if boundary=='after_effect':os._exit(73)
    return {'ok':True,'value':17}
executor=ToolExecutor('',[{'type':'function','function':{'name':n}} for n in ('read_file','fixture_effect')],handler,{},threading.Event(),task=task,journal=journal,state=RunState(task),checkpoint=checkpoint,approve_write=lambda *_:'reject',change=lambda *_:None)
executor.prepare_batch(calls,1)
history=[{'role':'user','content':'fixture'},assistant(calls)]
result=executor.execute(calls[0]);history.append({'role':'tool','tool_call_id':'saved','content':json.dumps(result)})
(root/'history.json').write_text(json.dumps(history))
if boundary=='prepared':os._exit(73)
result=executor.execute(calls[1]);history.append({'role':'tool','tool_call_id':'effect','content':json.dumps(result)})
(root/'history.json').write_text(json.dumps(history))
os._exit(73)
'''


class ToolExecutionTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        for module,name,value in ((task_store,'TASK_DIR',self.root/'tasks'),
            (chat_store,'CHAT_DIR',self.root/'chats'),(chat_store,'INDEX_FILE',self.root/'chats/index.json')):
            context=patch.object(module,name,value);context.start();self.addCleanup(context.stop)
        self.task=task_store.new_task('fixture-chat',str(self.root),'fixture')
        self.journal=task_journal(self.task)

    def executor(self, handler=None, **options):
        definitions=options.pop('definitions',TOOL_DEFINITIONS+[{'type':'function','function':{'name':'fixture_effect'}}])
        return ToolExecutor(str(self.root),definitions,handler,{},threading.Event(),task=self.task,
            journal=self.journal,state=RunState(self.task),checkpoint=options.pop('checkpoint',lambda *_:None),
            approve_write=options.pop('approve_write',lambda *_:'apply'),change=lambda *_:None,**options)

    def test_invalid_arguments_never_start_or_dispatch(self):
        handler=Mock();executor=self.executor(handler)
        tool=call('bad','read_file','{"path":null}');executor.prepare_batch([tool],0)
        self.assertEqual(executor.execute(tool)['code'],'INVALID_TOOL_ARGUMENTS')
        handler.assert_not_called();self.assertEqual(self.journal.entries()[0]['phase'],'prepared')

    def test_prepared_record_failure_prevents_dispatch(self):
        handler=Mock();executor=self.executor(handler)
        with patch.object(self.journal,'_append',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):executor.prepare_batch([call()],0)
        handler.assert_not_called()

    def test_started_record_failure_prevents_effect(self):
        handler=Mock();executor=self.executor(handler);tool=call('effect','fixture_effect','{}')
        executor.prepare_batch([tool],0)
        with patch.object(self.journal,'set_phase',side_effect=OSError('disk full')):
            with self.assertRaises(OSError):executor.execute(tool)
        handler.assert_not_called();self.assertEqual(self.journal.entries()[0]['phase'],'prepared')

    def test_effect_exception_is_unknown_but_read_exception_is_retryable(self):
        handler=Mock(side_effect=RuntimeError('after effect'))
        executor=self.executor(handler);calls=[call('effect','fixture_effect','{}'),call('read','read_file','{"path":"x"}')]
        executor.prepare_batch(calls,0)
        self.assertEqual(executor.execute(calls[0])['code'],'OUTCOME_UNKNOWN')
        self.assertEqual(executor.execute(calls[1])['code'],'TOOL_ERROR')
        history=[assistant(calls)];recover_task(self.task,history)
        self.assertEqual([e['call_id'] for e in self.task['recovery_items']],['effect'])

    def test_denied_write_never_starts_and_keeps_file_unchanged(self):
        (self.root/'a.txt').write_text('old')
        executor=self.executor(approve_write=lambda *_:'reject')
        tool=call(arguments='{"path":"a.txt","content":"new","overwrite":true}')
        executor.prepare_batch([tool],0)
        self.assertEqual(executor.execute(tool)['code'],'USER_DENIED')
        self.assertEqual((self.root/'a.txt').read_text(),'old')
        self.assertEqual(self.journal.entries()[0]['phase'],'awaiting_approval')
        self.assertEqual(self.journal.unresolved(),[])

    def test_external_approval_durably_starts_only_after_agreement(self):
        phases=[]
        def handler(*_):
            executor.before_external_approval();phases.append(self.journal.entries()[0]['phase'])
            executor.after_external_approval(True);phases.append(self.journal.entries()[0]['phase'])
            return {'ok':True}
        executor=self.executor(handler,approval_tools=['fixture_effect']);tool=call('e','fixture_effect','{}')
        executor.prepare_batch([tool],0);self.assertTrue(executor.execute(tool)['ok'])
        self.assertEqual(phases,['awaiting_approval','started'])

    def test_external_denial_never_marks_effect_started(self):
        def handler(*_):
            executor.before_external_approval();executor.after_external_approval(False)
            return {'ok':False,'error':'denied'}
        executor=self.executor(handler,approval_tools=['fixture_effect']);tool=call('e','fixture_effect','{}')
        executor.prepare_batch([tool],0);self.assertEqual(executor.execute(tool)['code'],'USER_DENIED')
        self.assertEqual(self.journal.entries()[0]['phase'],'awaiting_approval')
        self.assertEqual(self.journal.unresolved(),[])

    def test_saved_receipt_survives_checkpoint_failure(self):
        def checkpoint(*_):
            if self.journal.entries()[0]['result'] is not None:raise OSError('chat unavailable')
        executor=self.executor(lambda *_:{'ok':True,'value':7},checkpoint=checkpoint)
        tool=call('e','fixture_effect','{}');executor.prepare_batch([tool],0)
        with self.assertRaises(OSError):executor.execute(tool)
        history=[];recover_task(self.task,history)
        self.assertEqual(json.loads(history[1]['content']),{'ok':True,'value':7,'_receipt':{'message_index':0,'call_id':'e'}})
        self.assertEqual(self.task['recovery_items'],[])

    def test_reused_call_ids_are_bound_to_their_batch(self):
        first=call('same','read_file','{"path":"a"}')
        second=call('same','fixture_effect','{}')
        self.journal.prepare_batch([first],0);self.journal.record_result(0,'same',{'ok':True,'content':'first'})
        self.journal.prepare_batch([second],2);self.journal.set_phase(2,'same','started')
        history=[];self.journal.recover(history)
        self.assertEqual(json.loads(history[1]['content'])['content'],'first')
        self.assertEqual(json.loads(history[3]['content'])['code'],'OUTCOME_UNKNOWN')
        self.assertEqual(self.journal.unresolved()[0]['message_index'],2)

    def test_real_process_exit_at_five_execution_boundaries(self):
        for boundary in ('prepared','before_effect','after_effect','after_receipt','after_history'):
            with self.subTest(boundary=boundary):
                directory=self.root/boundary;directory.mkdir()
                process=subprocess.run([sys.executable,'-c',CRASH_WORKER,str(directory),boundary],
                    cwd=Path(__file__).resolve().parents[1],capture_output=True,timeout=20)
                self.assertEqual(process.returncode,73,process.stderr.decode(errors='replace'))
                task=json.loads((directory/'task.json').read_text());history=json.loads((directory/'history.json').read_text())
                with patch.object(task_store,'TASK_DIR',directory/'tasks'):
                    recover_task(task,history)
                    journal=task_journal(task)
                    unknown=boundary in ('before_effect','after_effect')
                    self.assertEqual(bool(task['recovery_items']),unknown)
                    results={m['tool_call_id']:json.loads(m['content']) for m in history if m['role']=='tool'}
                    self.assertEqual(results['saved']['content'],'preserved first result')
                    self.assertEqual(results['later']['code'],'NOT_EXECUTED')
                    if boundary in ('after_receipt','after_history'):self.assertEqual(results['effect']['value'],17)
                    elif unknown:self.assertEqual(results['effect']['code'],'OUTCOME_UNKNOWN')
                    else:self.assertEqual(results['effect']['code'],'NOT_EXECUTED')
                    if unknown:
                        journal.resolve(1,'effect','completed' if boundary=='after_effect' else 'not_executed')
                        recover_task(task,history)
                        self.assertEqual(task['recovery_items'],[])
                    before=copy.deepcopy(history);recover_task(task,history);self.assertEqual(history,before)
                effects=(directory/'effects.txt').read_text().splitlines() if (directory/'effects.txt').exists() else []
                self.assertEqual(len(effects),int(boundary in ('after_effect','after_receipt','after_history')))

    def test_recovery_metadata_is_bounded_and_idempotent(self):
        for index in range(105):
            self.journal.prepare_batch([call(str(index),'read_file','{"path":"a"}')],index*2)
            self.journal.record_result(index*2,str(index),{'ok':True,'content':'x'})
        history=[];recover_task(self.task,history);before=copy.deepcopy(self.task)
        recover_task(self.task,history)
        self.assertEqual(self.task,before);self.assertEqual(len(self.task['tool_activity']),100)

    def test_verification_recovers_failed_commands_from_receipts(self):
        tool=call('check','run_project_command','{"program":"test","arguments":[]}')
        self.journal.prepare_batch([tool],0);self.journal.record_result(0,'check',{'ok':False,'exit_code':7})
        history=[];recover_task(self.task,history)
        verdict=StageVerifier().verify('finish',task=self.task,final_text='Everything is done')
        self.assertFalse(verdict['ok']);self.assertEqual(self.task['test_results'][0]['exit_code'],7)
        self.assertEqual(self.task['verification']['status'],'failed')

    def test_unknown_effect_blocks_new_prompt_resume_and_fork_until_review(self):
        service=TaskService(lambda *_:None);self.addCleanup(service.shutdown)
        service.config['model']='fixture'
        chat=service.select_chat(self.root)['chat'];task=task_store.new_task(chat['id'],str(self.root),'fixture')
        journal=task_journal(task);tool=call('effect','fixture_effect','{}')
        journal.prepare_batch([tool],1);journal.set_phase(1,'effect','started')
        chat['messages']=[{'role':'user','content':'fixture'},assistant([tool])];chat['task_checkpoint']=task
        chat_store.save_chat(chat)
        recovered=service.select_chat(self.root,chat['id'])['task']
        with patch.object(service,'engine_factory') as factory:
            for params in ({'resume':True},{'prompt':'try again'}):
                with self.assertRaises(ValueError):service.start(self.root,params)
            factory.assert_not_called()
        with self.assertRaises(ValueError):service.conversations.fork(self.root,{'chat_id':chat['id'],'mode':'ide'})
        request={'chat_id':chat['id'],'journal_id':recovered['journal_id'],'message_index':1,'call_id':'effect','resolution':'completed'}
        for invalid in ({'journal_id':'old'},{'chat_id':'other'},{'message_index':True},{'call_id':'other'}):
            with self.assertRaises(ValueError):service.resolve_tool_recovery({**request,**invalid})
        result=service.resolve_tool_recovery(request)
        self.assertEqual(result['task']['run_state'],'paused');self.assertEqual(result['task']['recovery_items'],[])
        self.assertEqual(json.loads(result['chat']['messages'][2]['content'])['code'],'USER_CONFIRMED_EFFECT')
        with self.assertRaises(ValueError):service.resolve_tool_recovery(request)
        reopened=service.select_chat(self.root,chat['id']);self.assertEqual(reopened['task']['recovery_items'],[])

    def test_deleting_chat_removes_only_its_journals(self):
        self.journal.prepare_batch([call()],0)
        other=CallJournal('other','epoch');other.prepare_batch([call()],0)
        CallJournal.delete_chat(self.task['chat_id'])
        self.assertEqual(self.journal.entries(),[]);self.assertEqual(len(other.entries()),1)

    def test_unknown_flag_never_appears_as_success(self):
        executor=self.executor(lambda *_:{'ok':True,'outcome_unknown':True})
        tool=call('effect','fixture_effect','{}');executor.prepare_batch([tool],0)
        result=executor.execute(tool)
        self.assertFalse(result['ok']);self.assertEqual(result['code'],'OUTCOME_UNKNOWN')
        self.assertEqual(self.task['tool_activity'][0]['status'],'unknown')

    def test_receipt_without_boolean_outcome_is_rejected_before_adoption(self):
        tool=call();self.journal.prepare_batch([tool],0)
        for result in ({'ok':'true'},{'ok':None},{'message':'done'}):
            with self.assertRaises(ValueError):self.journal.record_result(0,tool['id'],result)
            history=[assistant([tool]),receipt(tool['id'],result)];original=copy.deepcopy(history)
            with self.assertRaises(ValueError):self.journal.recover(history)
            self.assertEqual(history,original)


if __name__=='__main__':unittest.main()
