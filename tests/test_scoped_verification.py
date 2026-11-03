"""Real command execution and explicit file-scoped evidence in large saved workspaces."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from agent import task_store
from agent.project_command import COMMAND_TOOL,run_project_command
from agent.run_state import RunState
from agent.task_contract import validate_options,install_contract
from agent.tool_executor import ToolExecutor
from agent.tool_recovery import task_journal,recover_task
from agent.verifier import StageVerifier
from agent.verification_evidence import command_scope,normalize_scope
from agent.workspace_revision import WorkspaceRevisionService


class ScopedVerificationTests(unittest.TestCase):
    """Use disposable sources; never execute model-generated code or touch user projects."""
    def setUp(self):
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.base=Path(temporary.name);self.root=self.base/'project';self.root.mkdir()
        (self.root/'main.py').write_text('value = 1\n',encoding='utf-8')
        (self.root/'config.json').write_text('{"rate":1}',encoding='utf-8')
        context=patch.object(task_store,'TASK_DIR',self.base/'profile/tasks');context.start();self.addCleanup(context.stop)
        self.task=task_store.new_task('scoped-fixture',str(self.root),'Проверить файл')
        self.check={'id':'syntax','purpose':'Синтаксис одного файла','program':sys.executable,
            'arguments':['-c','import ast,pathlib; ast.parse(pathlib.Path("main.py").read_text())'],'cwd':'.','timeout':10,
            'evidence_scope':{'kind':'files','files':['main.py'],'dependencies':['config.json']}}
        self.install();self.history=[];self.journal=task_journal(self.task);self.verifier=StageVerifier()

    def install(self):
        """Install only user-owned command scope and a linked acceptance criterion."""
        install_contract(self.task,validate_options({'checks':[self.check],'criteria':['Синтаксис корректен'],'criteria_links':{'0':['syntax']}}))

    def run_check(self,arguments=None,handler=None):
        """Exercise the normal journal, real process, approval and source witnesses."""
        args=arguments or {**{k:self.check[k] for k in ('program','arguments','cwd','timeout')},'check_id':self.check['id']}
        interrupted=threading.Event();notes=[]
        def approve(*_args):
            executor.before_external_approval();notes.append(executor.command_approval_note());executor.after_external_approval(True);return True
        def dispatch(_name,values):
            return handler(values,approve) if handler else run_project_command(self.root,values,interrupted,approve)
        executor=ToolExecutor(str(self.root),[COMMAND_TOOL],dispatch,{},interrupted,task=self.task,journal=self.journal,
            state=RunState(self.task),checkpoint=lambda *_:None,approve_write=lambda *_:'apply',change=lambda *_:None,
            approval_tools=['run_project_command'])
        call={'id':'command_'+str(len(self.history)),'type':'function','function':{'name':'run_project_command','arguments':json.dumps(args)}}
        executor.prepare_batch([call],len(self.history));self.history.append({'role':'assistant','tool_calls':[call],'content':None})
        result=executor.execute(call);self.history.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result)})
        self.verifier.record_command(self.task,args,result);return result,notes

    def test_large_unrelated_file_does_not_block_explicit_scope(self):
        """An actual exit=0 certifies selected files without certifying the large whole tree."""
        (self.root/'large.bin').write_bytes(b'x'*8_000_001)
        with patch.object(WorkspaceRevisionService,'capture',side_effect=AssertionError('full scan is forbidden for this scope')):
            result,notes=self.run_check();summary=self.verifier.refresh(self.task)
            self.assertTrue(result['ok'],result);self.assertEqual(result['exit_code'],0)
            self.assertEqual(summary['status'],'scoped_passed');self.assertEqual(summary['execution_status'],'passed')
            self.assertFalse(summary['project_complete']);self.assertIn('только выбранные файлы',notes[0])
            self.assertEqual(self.task['acceptance_evidence'][0]['status'],'scoped_checks_passed')
            self.assertTrue(self.verifier.verify('finish',task=self.task,final_text='Выбранные файлы проверены')['ok'])

    def test_default_workspace_remains_unverified_when_tree_is_incomplete(self):
        """An unknown/model-selected command cannot convert incomplete full coverage into success."""
        (self.root/'large.bin').write_bytes(b'x'*8_000_001)
        result,_=self.run_check({k:self.check[k] for k in ('program','arguments','cwd','timeout')})
        summary=self.verifier.refresh(self.task)
        self.assertEqual(result['exit_code'],0);self.assertEqual(summary['execution_status'],'passed')
        self.assertEqual(summary['status'],'stale');self.assertFalse(summary['project_complete'])
        self.assertEqual(self.task['test_results'][0]['evidence_status'],'unverified')

    def test_dependency_change_invalidates_but_unrelated_edit_does_not(self):
        """Content hashes detect backdated same-size edits while unrelated tool generations do not poison a scope."""
        self.run_check();self.assertEqual(self.verifier.refresh(self.task)['status'],'scoped_passed')
        (self.root/'unrelated.txt').write_text('new');self.task['workspace_generation']+=1
        self.assertEqual(self.verifier.refresh(self.task)['status'],'scoped_passed')
        target=self.root/'config.json';old=target.stat();target.write_text('{"rate":2}',encoding='utf-8')
        os.utime(target,ns=(old.st_atime_ns,old.st_mtime_ns))
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')

    def test_command_mutation_cannot_certify_post_execution_snapshot(self):
        """A command that modifies its covered input is exit=0 but has no stable tested snapshot."""
        self.check['arguments']=['-c','from pathlib import Path; Path("main.py").write_text("value = 2\\n")'];self.install()
        result,_=self.run_check();summary=self.verifier.refresh(self.task)
        self.assertEqual(result['exit_code'],0);self.assertEqual(summary['status'],'stale')
        self.assertIn('во время',summary['summary'])

    def test_nonzero_command_is_a_failed_criterion_not_just_stale(self):
        """Separate command failure from unknown source freshness in the linked criterion."""
        self.check['arguments']=['-c','raise SystemExit(7)'];self.install();result,_=self.run_check()
        self.assertEqual(result['exit_code'],7);self.assertEqual(self.verifier.refresh(self.task)['status'],'failed')
        self.assertEqual(self.task['acceptance_evidence'][0]['status'],'failed')

    def test_check_config_and_rollback_invalidate_receipt(self):
        """A saved receipt cannot follow a changed dependency list or rollback epoch."""
        self.run_check();self.task['observed_rollback_revision']+=1
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')
        self.task['observed_rollback_revision']-=1
        self.task['options']['checks'][0]['evidence_scope']['dependencies']=[]
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')

    def test_policy_revocation_and_missing_dependency_block_cached_evidence(self):
        """A former exact witness cannot bypass a newly denied path or removed dependency."""
        self.run_check();(self.root/'.neutralignore').write_text('config.json\n',encoding='utf-8')
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')
        (self.root/'.neutralignore').unlink();(self.root/'config.json').unlink()
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')

    def test_models_cannot_choose_scope_or_reuse_another_command(self):
        """Only exact command/check_id/timeout inherit a UI declaration; arbitrary scope args fail the tool schema."""
        args={**self.check,'check_id':'syntax'}
        self.assertEqual(command_scope(self.task,args)['kind'],'files')
        for change in ({'check_id':'unknown'},{'arguments':['other.py']},{'timeout':9}):
            self.assertEqual(command_scope(self.task,{**args,**change}),{'kind':'workspace'})
        supplied={k:self.check[k] for k in ('program','arguments','cwd','timeout')};supplied['evidence_scope']=self.check['evidence_scope']
        result,_=self.run_check(supplied);self.assertEqual(result['code'],'INVALID_TOOL_ARGUMENTS')

    def test_scope_validation_rejects_globs_escape_and_ambiguous_paths(self):
        """The UI scope is a list of exact relative saved files, never a folder grant or pattern."""
        for path in ('../main.py','/main.py','C:/main.py','*.py','a//b.py','.','main.py:secret','a\x00b'):
            with self.subTest(path=path),self.assertRaises(ValueError):normalize_scope({'kind':'files','files':[path]})
        self.assertEqual(normalize_scope({'kind':'files','files':['src\\main.py'],'dependencies':[]})['files'],['src/main.py'])

    def test_receipt_cannot_be_transplanted_to_another_workspace(self):
        """Identical file bytes in a different canonical workspace are not the recorded source snapshot."""
        self.run_check();other=self.base/'other';other.mkdir()
        for name in ('main.py','config.json'):(other/name).write_bytes((self.root/name).read_bytes())
        self.task['project_root']=str(other)
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')

    def test_malformed_or_incomplete_witness_is_never_success(self):
        """A valid exit code cannot repair absent, moving or ill-shaped source evidence."""
        self.run_check();entry=self.task['test_results'][0];original=deepcopy(entry['verification_receipt'])
        for replacement in ({'before':[],'after':{}},{'before':{'complete':False},'after':{}},['invalid']):
            entry['verification_receipt']={**original,'witness':replacement}
            self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')
            self.assertFalse(self.task['verification']['project_complete'])
        entry['verification_receipt']='invalid'
        self.assertEqual(self.verifier.refresh(self.task)['status'],'stale')

    def test_legacy_checkpoint_is_unverified_without_losing_exit_or_history(self):
        """A version-one fingerprint cannot regain success by loading a checkpoint or replaying its journal."""
        legacy={'kind':'command','id':'old','exit_code':0,'ok':True,'workspace_revision':WorkspaceRevisionService.capture(self.root)}
        self.task['test_results']=[legacy];self.task['verification']={'status':'commands_passed','summary':'old success'}
        task_store.save_task(self.task);loaded=task_store.load_task(self.task['chat_id'])
        self.assertEqual(loaded['test_results'][0]['exit_code'],0)
        self.assertEqual(loaded['test_results'][0]['evidence_status'],'unverified')
        self.assertEqual(loaded['verification']['status'],'stale')
        self.assertEqual(self.verifier.refresh(loaded)['status'],'stale')

    def test_receipt_survives_restart_without_reexecuting_command(self):
        """Recovery restores the actual v2 journal receipt and checks freshness without another process."""
        self.run_check();task_store.save_task(self.task);loaded=task_store.load_task(self.task['chat_id'])
        with patch('agent.project_command.subprocess.Popen',side_effect=AssertionError('must not rerun')):
            recover_task(loaded,deepcopy(self.history))
            self.assertEqual(loaded['verification']['status'],'scoped_passed')
        receipt=loaded['test_results'][0]['verification_receipt']
        self.assertEqual(receipt['version'],2);self.assertEqual(receipt,self.journal.entries()[0]['result']['verification_receipt'])


if __name__=='__main__':unittest.main()
