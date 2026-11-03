"""Stage 17 gates: selected tests, real LSP, private Git and conflict-aware rollback."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch
from tests import test_ide_verification as fixture
from agent.task_contract import validate_options,install_contract
from agent.verification_plan import required_checks
from agent.diagnostics_evidence import run_diagnostics
from agent.verifier import StageVerifier
from agent.operation_context import OperationContext
from agent.git_checkpoints import GitCheckpoints

LSP=Path(__file__).parent/'fixtures/lsp_diagnostics.py'


class Stage17Tests(unittest.TestCase):
    setUp=fixture.IdeVerificationTests.setUp
    executor=fixture.IdeVerificationTests.executor
    apply=fixture.IdeVerificationTests.apply

    def lsp_task(self,*flags):
        (self.root/'main.py').write_text('VALUE = 1\n')
        options=validate_options({'checks':[{'id':'lsp','kind':'diagnostics','purpose':'Проверка сохранённого файла','program':'lsp','arguments':['main.py'],'cwd':'.','timeout':5,'evidence_scope':{'kind':'files','files':['main.py'],'dependencies':[]}}]})
        install_contract(self.task,options)
        settings={'enabled':True,'program':sys.executable,'arguments':[str(LSP),'--pull',*flags],'language':'python','seconds':5}
        self.task['diagnostics_config']=deepcopy(settings)
        result=run_diagnostics(self.root,self.task,{'check_id':'lsp'},settings,OperationContext(10),lambda *_:True)
        StageVerifier().record_diagnostics(self.task,{'check_id':'lsp'},result)
        return result

    def test_full_lsp_clean_is_scoped_and_file_or_server_change_invalidates(self):
        self.assertTrue(self.lsp_task('--clean')['ok'])
        self.assertEqual(StageVerifier().refresh(self.task)['status'],'scoped_passed')
        self.assertIsNone(self.task['test_results'][0]['exit_code'])
        self.task['diagnostics_config']['language']='typescript'
        self.assertEqual(StageVerifier().refresh(self.task)['status'],'stale')
        self.lsp_task('--clean');(self.root/'main.py').write_text('VALUE = 2\n')
        self.assertEqual(StageVerifier().refresh(self.task)['status'],'stale')

    def test_lsp_errors_and_incomplete_push_never_pass(self):
        self.assertFalse(self.lsp_task()['ok'])
        self.assertEqual(StageVerifier().refresh(self.task)['status'],'failed')
        self.assertFalse(StageVerifier().verify('finish',task=self.task,final_text='Всё исправлено')['ok'])
        self.lsp_task('--clean')
        settings=self.task['diagnostics_config'];settings['arguments']=[str(LSP)]
        result=run_diagnostics(self.root,self.task,{'check_id':'lsp'},settings,OperationContext(10),lambda *_:True)
        self.assertFalse(result['ok']);self.assertEqual(result['code'],'LSP_INCOMPLETE')

    def test_user_selectors_skip_unrelated_checks_but_not_acceptance_requirements(self):
        checks=[{'id':'py','purpose':'Python tests','program':'python','arguments':['-m','unittest'],'applies_to':['src/*.py']},
            {'id':'js','purpose':'JS types','program':'node','arguments':['--check','web/main.js'],'kind':'types','applies_to':['web/*.js']}]
        install_contract(self.task,validate_options({'checks':checks}));self.task['modified_files']=['src/main.py']
        self.assertEqual([c['id'] for c in required_checks(self.task)],['py'])
        self.task['acceptance']=[{'description':'JS должен пройти','check_ids':['js']}]
        self.assertEqual([c['id'] for c in required_checks(self.task)],['py','js'])
        self.task['acceptance']=[];self.task['options']['checks_only']=True
        self.assertEqual(len(required_checks(self.task)),2)

    def test_git_snapshot_uses_confirmed_bytes_and_never_changes_project_index_or_head(self):
        if not shutil.which('git'):self.skipTest('Git unavailable')
        subprocess.run(['git','init','--quiet',str(self.root)],check=True)
        (self.root/'main.py').write_text('VALUE = 1\n')
        original_bytes=(self.root/'main.py').read_bytes()
        self.apply('write_file',{'path':'main.py','content':'VALUE = 2\n','overwrite':True})
        group=self.store.list()[0]['id'];head=(self.root/'.git/HEAD').read_bytes();index=self.root/'.git/index';old_index=index.read_bytes() if index.exists() else None
        result=GitCheckpoints(self.store).create(group,OperationContext(30))['checkpoint']
        self.assertEqual(GitCheckpoints(self.store).info(group)['commit'],result['commit'])
        self.assertEqual((self.root/'.git/HEAD').read_bytes(),head);self.assertEqual(index.read_bytes() if index.exists() else None,old_index)
        self.assertEqual((self.root/'main.py').read_text(),'VALUE = 2\n')
        manifest=json.loads(subprocess.check_output(['git','--git-dir='+result['repository'],'show',result['commit']+':manifest.json']))
        for version,expected in [('before',original_bytes),('after',b'VALUE = 2\n')]:
            entry=manifest[version]['main.py']['entry']
            self.assertEqual(subprocess.check_output(['git','--git-dir='+result['repository'],'show',result['commit']+':'+entry]),expected)

    def test_external_edit_during_multi_file_rollback_is_preserved_and_requires_review(self):
        for name in ('a.py','b.py'):
            (self.root/name).write_text('original\n');self.apply('write_file',{'path':name,'content':'agent\n','overwrite':True})
        group=self.store.list()[0]['id'];preview=self.store.preview(group);original=self.store._restore_file
        def restore(path,saved,expected):
            original(path,saved,expected)
            if path=='a.py':(self.root/'b.py').write_text('user edit\n')
        with patch.object(self.store,'_restore_file',side_effect=restore):result=self.store.restore(group,preview['fingerprint'])
        self.assertFalse(result['ok']);self.assertEqual(result['status'],'rollback_unknown')
        self.assertEqual((self.root/'a.py').read_text(),'original\n');self.assertEqual((self.root/'b.py').read_text(),'user edit\n')
        with self.assertRaises(ValueError):self.store.preview(group)


    def test_command_receipt_cannot_impersonate_lsp_check(self):
        self.lsp_task('--clean')
        from agent.verification_evidence import configured_check
        check=self.task['options']['checks'][0]
        self.assertIsNone(configured_check(self.task,{**check,'check_id':'lsp'}))
        from agent.language_diagnostics import normalize_diagnostics
        with self.assertRaises(ValueError):normalize_diagnostics([{'range':{'start':{'line':0,'character':0}},'severity':'error'}])


    def test_revoked_lsp_source_is_hidden_from_future_model_history(self):
        from agent.workspace_access import filter_model_history
        result=self.lsp_task('--clean')
        result['diagnostics']=[{'line':1,'column':1,'message':'PRIVATE_DIAGNOSTIC'}]
        messages=[{'role':'assistant','content':None,'tool_calls':[{'id':'lsp','function':{'name':'run_project_diagnostics','arguments':'{"check_id":"lsp"}'}}]},
            {'role':'tool','tool_call_id':'lsp','content':json.dumps(result)}]
        (self.root/'.neutralignore').write_text('main.py\n')
        self.assertNotIn('PRIVATE_DIAGNOSTIC',filter_model_history(messages,self.root)[1]['content'])
        self.assertIn('PRIVATE_DIAGNOSTIC',messages[1]['content'])
