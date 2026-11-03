"""Exercise real cache/AST/Tree-sitter/watcher behavior without any LLM or user source files."""
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from agent import task_store
from agent.project_index import ProjectIndex,get_index,close_indexes
from agent.project_symbols import extract_symbols
from agent.workspace_access import WorkspaceAccessPolicy
from agent.workspace_search import search_project
from core.python.editor_service import EditorService


class ProjectIndexTests(unittest.TestCase):
    """Use one isolated cache/observer per test; wait for facts rather than fixed timing."""
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.base=Path(temp.name);self.root=self.base/'project';self.root.mkdir()
        scope=patch.object(task_store,'TASK_DIR',self.base/'profile/tasks');scope.start();self.addCleanup(scope.stop);self.addCleanup(close_indexes)
        (self.root/'app').mkdir()
        (self.root/'app/main.py').write_text('import os\n\nclass Hello:\n    def greet(self):\n        return "Привет"\n',encoding='utf-8')
        (self.root/'app/main.ts').write_text('import { x } from "./x";\nexport class Example {\n run(): number { return 1; }\n}\nexport const greet = () => 2;\n',encoding='utf-8')
        (self.root/'.env').write_text('SYNTHETIC_HIDDEN=marker',encoding='utf-8')
        self.index=get_index(self.root,create=True);self.wait(lambda:self.index.state=='ready')

    def wait(self,predicate,seconds=15):
        """Bound test waiting and expose index status if an expected source fact never arrives."""
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if predicate():return
            time.sleep(.025)
        self.fail('Index did not reach expected state: '+str(self.index.status()))

    def hits(self,query,mode='symbols',**params):
        """Read only currently available index results; an updating cache has no claimed result."""
        result=self.index.query({'mode':mode,'query':query,**params})
        return result['matches'] if result else []

    def test_python_typescript_symbols_have_exact_ranges_and_provenance(self):
        for name,path,line,kind in (('greet','app/main.py',4,'method'),('Example','app/main.ts',2,'class'),('run','app/main.ts',3,'method')):
            hit=next(h for h in self.hits(name) if h['path']==path)
            self.assertEqual(hit['start_line'],line);self.assertEqual(hit['kind'],kind)
            self.assertGreaterEqual(hit['end_line'],hit['start_line']);self.assertEqual(len(hit['sha256']),64)
            self.assertEqual(hit['source_kind'],'saved-file');self.assertEqual(hit['freshness'],'hash-verified')
            self.assertEqual(hit['precision'],'syntax');self.assertEqual(hit['workspace_id'],self.index.workspace_id)

    def test_text_files_and_short_query_work_without_fts(self):
        self.index.fts=False
        self.assertTrue(self.hits('Привет','text'));self.assertTrue(self.hits('os','text'))
        self.assertEqual(self.hits('MAIN.TS','files')[0]['path'],'app/main.ts')
        result=search_project(self.root,{'query':'greet'});self.assertEqual(result['backend'],'project-index')

    def test_case_sensitive_symbols_and_file_paths_respect_request(self):
        """The case checkbox applies consistently to text, source definitions and file paths."""
        self.assertFalse(self.hits('hello',case_sensitive=True));self.assertTrue(self.hits('Hello',case_sensitive=True))
        self.assertFalse(self.hits('MAIN.TS','files',case_sensitive=True));self.assertTrue(self.hits('main.ts','files',case_sensitive=True))

    def test_transient_writer_sharing_error_does_not_disable_index(self):
        """A short Windows read-sharing race during atomic replace gets bounded read-only recovery."""
        original=self.index._read_once;calls=[]
        def transient(*args,**kwargs):
            calls.append(args[0])
            if len(calls)==1:raise PermissionError('temporary sharing conflict')
            return original(*args,**kwargs)
        with patch.object(self.index,'_read_once',side_effect=transient):self.assertTrue(self.hits('Hello'))
        self.assertGreaterEqual(len(calls),2);self.assertNotEqual(self.index.state,'needs_rebuild')

    def test_updating_cache_returns_verified_partial_hits(self):
        """An active delta update does not turn a known, current definition into a false missing result."""
        with patch.object(self.index,'state','updating'):
            result=self.index.query({'mode':'symbols','query':'greet'})
            self.assertTrue(result['matches']);self.assertTrue(result['truncated']);self.assertEqual(result['reason'],'updating')

    def test_queue_overflow_requires_recovery_without_unbounded_backlog(self):
        """A bounded durable queue cannot silently drop paths and still claim a ready index."""
        self.index.uncertain('hold worker')
        with patch('agent.project_index.MAX_PENDING',2):
            self.index.enqueue(['one.py','two.py','three.py'])
            self.assertEqual(self.index.state,'needs_rebuild');self.assertTrue(self.index.cancel_build.is_set())
            with self.index.database() as db:
                self.assertLessEqual(db.execute('SELECT count(*) FROM pending').fetchone()[0],2)
                self.assertEqual(db.execute("SELECT count(*) FROM pending WHERE path IN ('one.py','two.py','three.py')").fetchone()[0],0)

    def test_cancel_interrupts_flat_directory_before_reading_remaining_files(self):
        """Cancel is checked between files even inside one wide directory, not just between directories."""
        for number in range(40):(self.root/f'flat{number}.py').write_text('x = 1\n')
        original=self.index._read;started=threading.Event();release=threading.Event();calls=[]
        def paused_read(*args,**kwargs):
            calls.append(args[0])
            if not started.is_set() and self.index.state=='building':started.set();release.wait(3)
            return original(*args,**kwargs)
        with patch.object(self.index,'_read',side_effect=paused_read):
            self.index.rebuild();self.assertTrue(started.wait(4));before=len(calls)
            self.index.cancel();release.set();self.index.close()
            self.assertLessEqual(len(calls)-before,1)
            self.assertFalse(self.index.worker.is_alive())

    def test_symlink_targets_are_never_indexed_through_aliases(self):
        """Both escaped and inside-root aliases are excluded while ordinary source remains searchable."""
        outside=self.base/'outside.py';outside.write_text('def outside_only(): pass\n')
        try:
            (self.root/'escape.py').symlink_to(outside)
            (self.root/'alias.py').symlink_to(self.root/'app/main.py')
        except OSError:self.skipTest('Windows symbolic link creation is unavailable')
        self.index.enqueue(['escape.py','alias.py']);self.wait(lambda:self.index.state=='ready')
        self.assertFalse(self.hits('outside_only'));self.assertFalse(self.hits('alias.py','files'))

    def test_editor_save_external_rename_delete_are_incremental(self):
        scans=self.index.scan_count;editor=EditorService();current=editor.read(self.root,'app/main.py')
        proposal=editor.preview(self.root,{'path':'app/main.py','content':current['content'].replace('greet','welcome'),'revision':current['revision']})
        self.assertTrue(editor.resolve(self.root,{'proposal_id':proposal['proposal_id'],'decision':'apply'})['applied'])
        self.wait(lambda:bool(self.hits('welcome')))
        (self.root/'app/main.py').rename(self.root/'app/renamed.py')
        self.wait(lambda:any(h['path']=='app/renamed.py' for h in self.hits('welcome')))
        (self.root/'app/renamed.py').unlink()
        self.wait(lambda:self.index.state=='ready' and not self.hits('welcome'))
        self.assertEqual(self.index.scan_count,scans)

    def test_delete_during_subtree_read_is_incremental_absence(self):
        original=self.index._read_once;scans=self.index.scan_count;deleted=[]
        def disappearing(relative,policy,**kwargs):
            if relative=='app/main.py' and not deleted:
                (self.root/relative).unlink();deleted.append(relative)
            return original(relative,policy,**kwargs)
        with patch.object(self.index,'_read_once',side_effect=disappearing):
            self.index.enqueue(['app'])
            self.wait(lambda:bool(deleted) and self.index.state=='ready')
        self.assertFalse(any(hit['path']=='app/main.py' for hit in self.hits('greet')));self.assertEqual(self.index.scan_count,scans)

    def test_stale_backdated_bytes_are_never_returned(self):
        source=self.root/'app/main.py';old=source.stat();source.write_text(source.read_text(encoding='utf-8').replace('greet','other'),encoding='utf-8')
        os.utime(source,ns=(old.st_atime_ns,old.st_mtime_ns))
        self.assertFalse(any(h['path']=='app/main.py' for h in self.hits('greet')))
        self.wait(lambda:any(h['path']=='app/main.py' for h in self.hits('other')))

    def test_root_nested_gitignore_and_policy_revoke_old_cache(self):
        (self.root/'app/.gitignore').write_text('main.ts\n',encoding='utf-8')
        self.wait(lambda:self.index.state=='needs_rebuild');self.wait(lambda:self.index.file_count==0)
        self.index.rebuild();self.wait(lambda:self.index.state=='ready')
        self.assertFalse(self.hits('Example'))
        (self.root/'.neutralignore').write_text('app/main.py\n',encoding='utf-8')
        self.assertFalse(self.hits('Hello'));self.wait(lambda:self.index.state=='needs_rebuild')
        self.wait(lambda:self.index.file_count==0)

    def test_exact_grant_revocation_is_checked_even_without_workspace_event(self):
        policy=WorkspaceAccessPolicy(self.root);policy.configure(['.env'],True)
        self.assertIsNone(self.index.query({'query':'SYNTHETIC_HIDDEN'}))
        self.index.rebuild();self.wait(lambda:self.index.state=='ready')
        self.assertEqual(self.hits('SYNTHETIC_HIDDEN','text')[0]['path'],'.env')
        policy.configure([],True)
        result=search_project(self.root,{'query':'SYNTHETIC_HIDDEN'})
        self.assertEqual(result['matches'],[]);self.wait(lambda:self.index.file_count==0)

    def test_ignored_parent_cannot_be_restored_by_child_negation(self):
        (self.root/'ignored').mkdir();(self.root/'ignored/visible.py').write_text('def hidden(): pass\n')
        (self.root/'.gitignore').write_text('ignored/\n!ignored/visible.py\n',encoding='utf-8')
        self.wait(lambda:self.index.state=='needs_rebuild');self.index.rebuild();self.wait(lambda:self.index.state=='ready')
        self.assertFalse(self.hits('hidden'))

    def test_parser_failure_and_non_utf8_leave_text_search_available(self):
        symbols,status=extract_symbols('bad.py','def invalid(:\n');self.assertEqual(symbols,[]);self.assertIn('error',status)
        with patch.dict('sys.modules',{'tree_sitter':None}):self.assertEqual(extract_symbols('x.js','function f() {}')[0],[])
        (self.root/'bad.py').write_text('def invalid(:\n')
        (self.root/'binary.dat').write_bytes(b'\xff\xfe\xfd')
        self.wait(lambda:bool(self.hits('invalid','text')))
        self.assertFalse(self.hits('binary.dat','files'))
        self.wait(lambda:self.index.state=='ready')
        result=self.index.query({'mode':'symbols','query':'invalid'})
        self.assertTrue(result['truncated']);self.assertEqual(result['reason'],'parser')

    def test_durable_queue_coalesces_and_restart_recovers_offline_edit(self):
        self.index.uncertain('offline fixture');self.index.enqueue(['app/main.py']);self.index.enqueue(['app/main.py'])
        with self.index.database() as db:self.assertEqual(db.execute('SELECT count(*) FROM pending WHERE path=?',('app/main.py',)).fetchone()[0],1)
        close_indexes();(self.root/'app/main.py').write_text('def offline(): pass\n')
        self.index=get_index(self.root,create=True);self.wait(lambda:self.index.state=='ready')
        self.assertTrue(self.hits('offline'));self.assertFalse(self.hits('Hello'))

    def test_overflow_cancel_and_explicit_rebuild_never_claim_ready(self):
        self.index.uncertain('overflow fixture');self.assertIsNone(self.index.query({'query':'greet'}))
        self.assertEqual(search_project(self.root,{'query':'greet'})['backend'],'linear-fallback')
        self.index.cancel();self.assertEqual(self.index.state,'needs_rebuild')
        self.index.rebuild();self.wait(lambda:self.index.state=='ready');self.assertTrue(self.hits('greet'))

    def test_corrupt_derived_cache_requires_explicit_rebuild(self):
        path=self.index.path;close_indexes();path.write_bytes(b'not sqlite')
        self.index=get_index(self.root,create=True);self.assertEqual(self.index.state,'degraded')
        self.assertEqual(search_project(self.root,{'query':'greet'})['backend'],'linear-fallback')
        self.index.rebuild();self.wait(lambda:self.index.state=='ready');self.assertTrue(self.hits('greet'))
        self.assertTrue(list(self.index.directory.glob('*.broken')))

    def test_scoped_outline_and_cancellation_do_not_return_other_sources(self):
        hits=self.hits('',mode='outline',path='app/main.ts');self.assertTrue(hits)
        self.assertEqual({h['path'] for h in hits},{'app/main.ts'})
        cancelled=threading.Event();cancelled.set()
        self.assertEqual(self.index.query({'query':'greet'},cancelled)['code'],'SEARCH_CANCELLED')


if __name__=='__main__':unittest.main()
