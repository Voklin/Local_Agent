"""Acceptance evidence, read-only enforcement and revision-safe workspace rollback."""
from copy import deepcopy
import json
from pathlib import Path
import queue
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import uuid
import zipfile

from agent import chat_store, task_store
from agent.engine import AgentEngine
from agent.project_command import COMMAND_TOOL
from agent.run_state import RunState
from agent.storage import Storage
from agent.task_contract import validate_options, install_contract, set_plan, acceptance_summary
from agent.tool_executor import ToolExecutor
from agent.tool_recovery import recover_task, task_journal
from agent.tools import TOOL_DEFINITIONS
from agent.verifier import StageVerifier
from agent.verification_evidence import capture_witness,make_receipt,now
from agent.workspace_revision import WorkspaceRevisionService
from agent.workspace_snapshots import SnapshotStore
from core.python.task_service import TaskService


class IdeVerificationTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.profile=Path(temp.name)/'profile';self.root=Path(temp.name)/'project';self.root.mkdir()
        for module,name,value in ((task_store,'TASK_DIR',self.profile/'tasks'),(chat_store,'CHAT_DIR',self.profile/'chats')):
            context=patch.object(module,name,value);context.start();self.addCleanup(context.stop)
        self.task=task_store.new_task('ide-fixture',str(self.root),'Изменить проект')
        install_contract(self.task,validate_options({}))
        self.store=SnapshotStore(self.root,self.task['chat_id'],self.task['journal_id'])
        self.journal=task_journal(self.task);self.history=[]

    def executor(self,**options):
        return ToolExecutor(str(self.root),TOOL_DEFINITIONS+[COMMAND_TOOL,{'type':'function','function':{'name':'external_effect'}}],None,{},threading.Event(),task=self.task,
            journal=self.journal,state=RunState(self.task),checkpoint=lambda *_:None,approve_write=lambda *_:'apply',change=lambda *_:None,**options)

    def apply(self,name,args,executor=None):
        executor=executor or self.executor();identity=uuid.uuid4().hex
        call={'id':identity,'type':'function','function':{'name':name,'arguments':json.dumps(args)}}
        executor.prepare_batch([call],len(self.history))
        self.history.append({'role':'assistant','content':None,'tool_calls':[call]})
        result=executor.execute(call)
        self.history.append({'role':'tool','tool_call_id':identity,'content':json.dumps(result)})
        self.assertTrue(result['ok'],result)
        return result

    def test_roundtrip_nested_create_patch_rename_delete_preserves_original_bytes(self):
        (self.root/'original.txt').write_bytes(b'original\r\n')
        self.apply('create_directory',{'path':'web/src'})
        self.apply('write_file',{'path':'web/src/main.js','content':'const x = 1;\n','overwrite':False})
        self.apply('patch_file',{'path':'web/src/main.js','old_text':'x = 1','new_text':'x = 2'})
        self.apply('rename_file',{'path':'web/src/main.js','destination':'web/src/game.js'})
        self.apply('delete_file',{'path':'original.txt'})
        groups=self.store.list();self.assertEqual(len(groups),1)
        preview=self.store.preview(groups[0]['id'])
        self.assertIn('original',preview['diff']);self.assertIn('game.js',preview['diff'])
        result=self.store.restore(groups[0]['id'],preview['fingerprint'])
        self.assertTrue(result['ok'],result)
        self.assertEqual((self.root/'original.txt').read_bytes(),b'original\r\n')
        self.assertFalse((self.root/'web').exists())
        self.assertEqual(self.store.list()[0]['status'],'rolled_back')

    def test_manual_edit_after_preview_blocks_entire_rollback(self):
        for name in ('a.txt','b.txt'):
            (self.root/name).write_text('before')
            self.apply('write_file',{'path':name,'content':'after','overwrite':True})
        group=self.store.list()[0]['id'];preview=self.store.preview(group)
        (self.root/'b.txt').write_text('manual')
        with self.assertRaisesRegex(ValueError,'ручные'):
            self.store.restore(group,preview['fingerprint'])
        self.assertEqual((self.root/'a.txt').read_text(),'after')
        self.assertEqual((self.root/'b.txt').read_text(),'manual')

    def test_untracked_file_in_created_directory_is_never_removed(self):
        self.apply('create_directory',{'path':'new'})
        (self.root/'new/manual.txt').write_text('keep')
        with self.assertRaisesRegex(ValueError,'новые файлы'):
            self.store.preview(self.store.list()[0]['id'])
        self.assertEqual((self.root/'new/manual.txt').read_text(),'keep')

    def test_intervening_manual_revision_starts_a_separate_undo_segment(self):
        path=self.root/'a.txt';path.write_text('A')
        self.apply('write_file',{'path':'a.txt','content':'B','overwrite':True})
        first=self.store.list()[0]['id'];path.write_text('manual C')
        self.apply('write_file',{'path':'a.txt','content':'D','overwrite':True})
        latest=self.store.list()[0]['id'];self.assertNotEqual(first,latest)
        preview=self.store.preview(latest);self.assertTrue(self.store.restore(latest,preview['fingerprint'])['ok'])
        self.assertEqual(path.read_text(),'manual C')
        with self.assertRaises(ValueError):self.store.preview(first)

    def test_binary_rename_undo_is_byte_exact(self):
        raw=bytes(range(256))*20;(self.root/'before.bin').write_bytes(raw)
        self.apply('rename_file',{'path':'before.bin','destination':'after.bin'})
        group=self.store.list()[0]['id'];preview=self.store.preview(group)
        self.assertIn('Бинарный файл',preview['diff'])
        self.assertTrue(self.store.restore(group,preview['fingerprint'])['ok'])
        self.assertEqual((self.root/'before.bin').read_bytes(),raw);self.assertFalse((self.root/'after.bin').exists())

    def test_snapshot_failure_prevents_file_dispatch(self):
        executor=self.executor();call={'id':'write','type':'function','function':{'name':'write_file','arguments':json.dumps({'path':'new.txt','content':'new','overwrite':False})}}
        executor.prepare_batch([call],0)
        with patch.object(SnapshotStore,'prepare',side_effect=OSError('disk full')):
            result=executor.execute(call)
        self.assertEqual(result['code'],'SNAPSHOT_FAILED');self.assertFalse((self.root/'new.txt').exists())
        self.assertEqual(self.journal.entries()[0]['phase'],'awaiting_approval')

    def test_read_only_blocks_files_commands_and_unknown_external_tools(self):
        self.task['options']['read_only']=True
        executor=self.executor()
        for index,name in enumerate(('write_file','run_project_command','external_effect')):
            call={'id':name,'type':'function','function':{'name':name,'arguments':'{}'}}
            executor.prepare_batch([call],index*2)
            result=executor.execute(call)
            self.assertEqual(result['code'],'READ_ONLY')
        self.assertTrue(all(entry['phase']=='prepared' for entry in self.journal.entries()))
        self.assertEqual(list(self.root.iterdir()),[])

    def test_model_plan_cannot_erase_user_criteria_or_invent_evidence(self):
        options=validate_options({'criteria':['Сохранить ручные правки']})
        install_contract(self.task,options)
        result=set_plan(self.task,{'steps':['Изучить файл','Внести правку'],'criteria':[{'description':'Не сломать синтаксис','check_ids':[]}]})
        self.assertTrue(result['ok']);self.assertEqual(len(self.task['acceptance']),2)
        self.assertTrue(all(item['status']=='unverified' for item in acceptance_summary(self.task)))
        self.assertFalse(set_plan(self.task,{'steps':['Готово'],'criteria':[{'description':'Всё готово','check_ids':['invented']} ]})['ok'])

    def test_checks_are_exactly_linked_and_invalidated_by_further_edits(self):
        check={'id':'syntax','purpose':'Синтаксис','program':'node','arguments':['--check','a.js'],'cwd':'.'}
        options=validate_options({'criteria':['Код корректен'],'criteria_links':{'0':['syntax']},'checks':[check]})
        install_contract(self.task,options);verifier=StageVerifier()
        verifier.record_command(self.task,{**check,'check_id':'syntax','arguments':['other.js']},{'ok':True,'exit_code':0,'workspace_generation':0})
        self.assertEqual(acceptance_summary(self.task)[0]['status'],'unverified')
        args={**check,'check_id':'syntax'};result={'ok':True,'exit_code':0,'workspace_generation':0};witness=capture_witness(self.root,{'kind':'workspace'})
        verifier.record_command(self.task,args,{**result,'verification_receipt':make_receipt(args,{'kind':'workspace'},witness,witness,result,started_at=now())})
        verifier.refresh(self.task)
        self.assertEqual(acceptance_summary(self.task)[0]['status'],'checks_passed')
        self.apply('write_file',{'path':'a.js','content':'broken','overwrite':False})
        self.assertEqual(acceptance_summary(self.task)[0]['status'],'stale')
        self.assertEqual(verifier.command_summary(self.task)['status'],'stale')

    def test_rollback_invalidates_receipts_even_after_projection_loss(self):
        self.apply('write_file',{'path':'a.txt','content':'new','overwrite':False})
        verifier=StageVerifier();verifier.record_command(self.task,{'program':'node','arguments':[]},{'ok':True,'exit_code':0,'workspace_generation':1})
        group=self.store.list()[0]['id'];preview=self.store.preview(group)
        self.assertTrue(self.store.restore(group,preview['fingerprint'])['ok'])
        recover_task(self.task,self.history)
        self.assertGreater(self.task['workspace_generation'],1);self.assertTrue(self.task['workspace_reverted'])
        self.assertTrue(any('отменил файловые правки' in (m.get('content') or '') for m in self.history))
        history_size=len(self.history)
        before=self.task['workspace_generation'];recover_task(self.task,self.history)
        self.assertEqual(len(self.history),history_size)
        self.assertEqual(self.task['workspace_generation'],before)
        self.assertEqual(verifier.command_summary(self.task)['status'],'stale')

    def test_partial_rollback_is_durable_and_never_replayed_implicitly(self):
        for name in ('a.txt','b.txt'):
            (self.root/name).write_text('before');self.apply('write_file',{'path':name,'content':'after','overwrite':True})
        group=self.store.list()[0]['id'];preview=self.store.preview(group)
        original=self.store._restore_file
        def fail_second(path,*args):
            if path=='b.txt':raise OSError('fixture failure')
            return original(path,*args)
        with patch.object(self.store,'_restore_file',side_effect=fail_second):result=self.store.restore(group,preview['fingerprint'])
        self.assertFalse(result['ok']);self.assertEqual(result['status'],'rollback_unknown')
        reopened=SnapshotStore(self.root,self.task['chat_id']);self.assertTrue(reopened.attention())
        self.assertEqual((self.root/'a.txt').read_text(),'before');self.assertEqual((self.root/'b.txt').read_text(),'after')
        with self.assertRaises(ValueError):reopened.preview(group)
        reopened.review(group);self.assertEqual(reopened.attention(),[])
        recover_task(self.task,self.history)
        self.assertFalse(self.task['workspace_reverted']);self.assertTrue(self.task['workspace_reviewed'])
        self.assertEqual((self.root/'b.txt').read_text(),'after')

    def test_prepared_snapshot_is_not_automatically_adopted_after_crash(self):
        self.apply('write_file',{'path':'a.txt','content':'new','overwrite':False})
        with self.store.database.transaction() as connection:connection.execute("UPDATE workspace_snapshots SET status='prepared'")
        recover_task(self.task,self.history)
        self.assertEqual(self.store.list()[0]['status'],'unknown')
        with self.assertRaises(ValueError):self.store.preview(self.store.list()[0]['id'])

    def test_snapshot_backup_can_restore_originals_in_a_fresh_profile(self):
        self.apply('write_file',{'path':'new.txt','content':'hello','overwrite':False})
        (self.root/'existing.txt').write_text('original')
        self.apply('write_file',{'path':'existing.txt','content':'changed','overwrite':True})
        archive=self.profile.parent/'backup.zip';self.store.database.backup(archive)
        restored=self.profile.parent/'restored'
        with zipfile.ZipFile(archive) as bundle:
            self.assertTrue(any(name.startswith('artifacts/workspace-snapshots/') for name in bundle.namelist()))
            bundle.extractall(restored)
        with patch.object(task_store,'TASK_DIR',restored/'tasks'):
            reopened=SnapshotStore(self.root,self.task['chat_id']);group=reopened.list()[0]['id'];preview=reopened.preview(group)
            self.assertTrue(reopened.restore(group,preview['fingerprint'])['ok'])
        self.assertEqual((self.root/'existing.txt').read_text(),'original')

    def test_schema_one_upgrade_preserves_canonical_history(self):
        database=Storage(self.profile).ready()
        chat=chat_store.create_chat(str(self.root),'fixture')
        with database.transaction() as connection:
            connection.execute('DROP TABLE inference_attempts');connection.execute('DROP TABLE runs')
            connection.execute('DROP TABLE workspace_snapshots');connection.execute('PRAGMA user_version=1')
        upgraded=Storage(self.profile).ready()
        self.assertEqual(upgraded.report()['version'],3)
        self.assertEqual(upgraded.load_chat(chat['id'])['messages'],[])

    def test_user_checks_use_real_approval_without_model_or_extra_capabilities(self):
        events=queue.Queue();service=TaskService(events.put)
        self.addCleanup(service.shutdown)
        check={'id':'syntax','purpose':'Проверить окружение Python','program':sys.executable,'arguments':['-c','print("passed")'],'cwd':'.','timeout':10}
        with patch('agent.engine.ModelClient',side_effect=AssertionError('no model request')):
            with self.assertRaisesRegex(ValueError,'расширение'):
                service.start(self.root,{'mode':'ide','task_options':{'checks_only':True,'checks':[check]}})
            service.extensions.state['groups']['commands']=True
            service.start(self.root,{'mode':'ide','task_options':{'checks_only':True,'checks':[check]}})
            approval=None
            while True:
                event=events.get(timeout=15)
                self.assertNotEqual(event['event'],'failed',event)
                if event['event']=='approval':
                    approval=event;self.assertIn(check['purpose'],event['diff'])
                    service.resolve_approval({**event,'decision':'apply'})
                if event['event']=='task_end':break
            service.thread.join(2)
        self.assertIsNotNone(approval)
        task=service.chat['task_checkpoint'];self.assertEqual(task['test_results'][0]['exit_code'],0)
        self.assertEqual(task['test_results'][0]['check_id'],'syntax')

    def test_invalid_options_do_not_start_commands_or_replace_task(self):
        for value in ({'read_only':'yes'},{'criteria':['']},{'checks_only':True},{'read_only':True,'auto_checks':True}):
            with self.assertRaises(ValueError):validate_options(value)

    def test_real_process_exit_during_rollback_requires_manual_review(self):
        for name in ('a.txt','b.txt'):
            (self.root/name).write_text('before');self.apply('write_file',{'path':name,'content':'after','overwrite':True})
        group=self.store.list()[0]['id']
        script="""
import os,sys
from pathlib import Path
from agent import task_store
from agent.workspace_snapshots import SnapshotStore
task_store.TASK_DIR=Path(sys.argv[1])/'tasks'
store=SnapshotStore(sys.argv[2],'ide-fixture');group=sys.argv[3]
original=store._restore_file
def exit_after_effect(path,*args):
    original(path,*args)
    os._exit(73)
store._restore_file=exit_after_effect
store.restore(group,store.preview(group)['fingerprint'])
"""
        process=subprocess.run([sys.executable,'-c',script,str(self.profile),str(self.root),group],capture_output=True,timeout=20)
        self.assertEqual(process.returncode,73,process.stderr)
        self.assertTrue(self.store.attention())
        self.assertEqual((self.root/'a.txt').read_text(),'before');self.assertEqual((self.root/'b.txt').read_text(),'after')
        recover_task(self.task,self.history)
        self.assertTrue(self.task['snapshot_attention'])
        self.assertFalse(StageVerifier().verify('finish',task=self.task,final_text='done')['ok'])

    def test_manual_change_during_partial_restore_is_preserved(self):
        for name in ('a.txt','b.txt'):
            (self.root/name).write_text('before');self.apply('write_file',{'path':name,'content':'after','overwrite':True})
        group=self.store.list()[0]['id'];preview=self.store.preview(group);original=self.store._restore_file
        def concurrent_edit(path,*args):
            original(path,*args)
            (self.root/'b.txt').write_text('manual during rollback')
        with patch.object(self.store,'_restore_file',side_effect=concurrent_edit):result=self.store.restore(group,preview['fingerprint'])
        self.assertEqual(result['status'],'rollback_unknown')
        self.assertEqual((self.root/'b.txt').read_text(),'manual during rollback')
