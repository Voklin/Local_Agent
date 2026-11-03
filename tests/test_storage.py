"""Migration, process-exit, index, artifact and backup contracts for real SQLite."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from agent import chat_store, task_store
from agent.call_journal import CallJournal, LegacyCallJournal
from agent.context_tools import read_saved_result
from agent.projects import ProjectStore
from agent.storage import Storage, encode


def conversation(identity='1'*32, mode='chat', messages=None):
    return {'id':identity,'title':'Разговор '+mode,'mode':mode,'project_id':'project',
        'project_root':'','model':'fixture','created_at':'2026-01-01','updated_at':'2026-01-02',
        'messages':messages or [{'role':'user','content':'Привет, Лола!'}]}


def tool_call():
    return {'id':'effect','type':'function','function':{'name':'write_file','arguments':'{"path":"a.txt","content":"ok"}'}}


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)/'profile'
        self.root.mkdir()
        self.database = Storage(self.root)
        for module, name, value in ((chat_store,'CHAT_DIR',self.root/'chats'),(task_store,'TASK_DIR',self.root/'tasks')):
            context = patch.object(module,name,value)
            context.start()
            self.addCleanup(context.stop)

    def legacy(self, value):
        path = self.root/'chats'/(value['id']+'.json')
        path.parent.mkdir(exist_ok=True)
        path.write_text(encode(value),encoding='utf-8')
        return path

    def test_migration_preserves_modes_projects_checkpoints_and_original_bytes(self):
        values = [conversation(str(i)*32, mode) for i,mode in enumerate(('chat','ide','voice'),1)]
        checkpoint = {'chat_id':values[1]['id'],'project_root':'','status':'paused','journal_id':'epoch'}
        values[1]['task_checkpoint'] = checkpoint
        paths = [self.legacy(value) for value in values]
        (self.root/'tasks').mkdir()
        path = task_store.task_path(values[1]['id'])
        path.write_text(encode({**checkpoint,'status':'running'}),encoding='utf-8')
        project = {'id':'project','name':'Сайт','root':'','instructions':'Русский','created_at':'2026','updated_at':'2026'}
        (self.root/'projects.json').write_text(encode([project]),encoding='utf-8')
        paths += [path,self.root/'projects.json']
        before = {path:path.read_bytes() for path in paths}
        report = self.database.ready().report()
        self.assertEqual(report['migration'],{'version':1,'chats':3,'messages':3})
        self.assertEqual(report['integrity'],'ok')
        self.assertTrue(all(source['status']=='verified' for source in report['sources']))
        for value in values:
            self.assertEqual(self.database.load_chat(value['id']),value)
        self.assertEqual(task_store.load_task(values[1]['id']),checkpoint)
        self.assertEqual(ProjectStore(self.root).list(),[project])
        self.assertEqual(before,{path:path.read_bytes() for path in paths})
        with patch.object(Path,'iterdir',side_effect=AssertionError('second migration')):
            self.assertEqual(len(Storage(self.root).ready().catalog()['chats']),3)

    def test_interrupted_migration_is_rolled_back_and_can_retry(self):
        value = conversation()
        path = self.legacy(value)
        with patch.object(Storage,'_source',side_effect=OSError('power loss fixture')):
            with self.assertRaises(OSError):
                self.database.ready()
        connection = sqlite3.connect(self.database.path)
        try:
            self.assertEqual(connection.execute('PRAGMA user_version').fetchone()[0],0)
        finally:
            connection.close()
        self.assertEqual(self.database.ready().load_chat(value['id']),value)
        self.assertEqual(json.loads(path.read_text(encoding='utf-8')),value)

    def test_malformed_project_catalog_stops_migration_without_losing_chats(self):
        value = conversation()
        self.legacy(value)
        projects = self.root/'projects.json'
        projects.write_bytes(b'{broken')
        with self.assertRaisesRegex(ValueError,'проектов'):
            self.database.ready()
        self.assertEqual(projects.read_bytes(),b'{broken')
        projects.write_text('[]')
        self.assertEqual(self.database.ready().load_chat(value['id']),value)

    def test_future_schema_is_not_downgraded(self):
        self.database.ready()
        with self.database.transaction() as connection:
            connection.execute('PRAGMA user_version=999')
        with self.assertRaisesRegex(ValueError,'новой версией'):
            Storage(self.root).ready()

    def test_corrupt_checkpoint_cannot_be_treated_as_a_new_chat(self):
        value=conversation()
        self.legacy(value)
        path=task_store.task_path(value['id'])
        path.parent.mkdir()
        path.write_bytes(b'{broken')
        self.database.ready()
        with self.assertRaisesRegex(ValueError,'точка'):
            self.database.load_chat(value['id'])
        with self.assertRaisesRegex(ValueError,'точка'):
            task_store.load_task(value['id'])
        self.assertEqual(path.read_bytes(),b'{broken')

    def test_readonly_catalog_and_search_never_open_full_chats_or_legacy_files(self):
        self.database.ready()
        for index in range(40):
            value = conversation(f'{index:032x}', 'voice' if index%2 else 'chat')
            value['messages']=[{'role':'user','content':f'Змейка номер {index}'}]
            chat_store.save_chat(value)
        with patch.object(Storage,'load_chat',side_effect=AssertionError('full load')), patch.object(Path,'read_text',side_effect=AssertionError('JSON scan')):
            result=chat_store.search_chats('ЗМЕЙКА номер 12', root='',mode='chat',project_id='project')
            self.assertEqual([c['id'] for c in result['chats']],[f'{12:032x}'])
            self.assertIn('Змейка',result['chats'][0]['snippet'])
            self.assertEqual(len(chat_store.read_chat_catalog(mode='voice')['chats']),20)
        self.assertEqual(self.database.search('номер 13',root='',mode='chat',project_id='project')['chats'],[])
        self.assertEqual(len(self.database.search('12',root='',mode='chat',project_id='project')['chats']),1)
        self.assertEqual(self.database.search('номер 12',root='',mode='chat',project_id='other')['chats'],[])

    def test_sql_fallback_preserves_substring_search(self):
        chat_store.save_chat(conversation())
        with self.database.transaction() as connection:
            connection.execute("UPDATE meta SET value='substring' WHERE key='search_backend'")
        self.assertEqual(len(self.database.search('ВЕТ, ло',root='',mode='chat',project_id='project')['chats']),1)

    def test_task_and_history_commit_together_without_stale_draft_overwrite(self):
        value = conversation()
        value['task_checkpoint']={'chat_id':value['id'],'status':'paused','turn':1}
        chat_store.save_chat(value)
        fresh = {**value['task_checkpoint'],'turn':2}
        task_store.save_task(fresh)
        value['stream_draft']={'text':'draft','run_id':'run'}
        chat_store.save_chat(value, checkpoint=False)
        self.assertEqual(chat_store.load_chat(value['id'])['task_checkpoint']['turn'],2)
        value['task_checkpoint']=fresh
        value['messages'].append({'role':'assistant','content':'ready'})
        with patch.object(Storage,'_search_entry',side_effect=OSError('index failed')):
            with self.assertRaises(OSError):
                chat_store.save_chat(value)
        saved = chat_store.load_chat(value['id'])
        self.assertEqual(len(saved['messages']),1)
        self.assertEqual(saved['task_checkpoint']['turn'],2)

    def test_real_process_exit_before_and_after_chat_commit(self):
        value = conversation()
        value['task_checkpoint']={'chat_id':value['id'],'turn':0}
        chat_store.save_chat(value)
        script = """
import os,sys
from pathlib import Path
from agent.storage import Storage
database=Storage(Path(sys.argv[1])).ready()
value=database.load_chat(sys.argv[2]);value['title']=sys.argv[3]
value['messages'].append({'role':'assistant','content':sys.argv[3]})
value['task_checkpoint']['turn']=1
with database.transaction() as connection:
    database.write_chat(connection,value,checkpoint=True)
    if sys.argv[3]=='before': os._exit(81)
os._exit(82)
"""
        for boundary,code in (('before',81),('after',82)):
            result = subprocess.run([sys.executable,'-c',script,str(self.root),value['id'],boundary],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,code,result.stderr)
            loaded=Storage(self.root).ready().load_chat(value['id'])
            self.assertEqual(len(loaded['messages']),1 if boundary=='before' else 2)
            self.assertEqual(loaded['task_checkpoint']['turn'],0 if boundary=='before' else 1)
        self.assertEqual(self.database.report()['integrity'],'ok')

    def test_large_outputs_are_referenced_and_hydrated_without_reexecution(self):
        text=encode({'ok':True,'stdout':'Привет! '*8000})
        value=conversation(messages=[{'role':'assistant','content':None,'tool_calls':[tool_call()]},
            {'role':'tool','tool_call_id':'effect','content':text}])
        chat_store.save_chat(value)
        with self.database.transaction() as connection:
            raw=connection.execute('SELECT data FROM messages WHERE position=1').fetchone()[0]
        self.assertLess(len(raw),500)
        self.assertIn('_neutral_artifact_v1',raw)
        loaded=chat_store.load_chat(value['id'])
        self.assertEqual(loaded['messages'],value['messages'])
        result=read_saved_result(loaded['messages'],{'message_index':1,'call_id':'effect','offset':1000,'limit':300})
        self.assertEqual(result['content'],text[1000:1300])
        self.assertEqual(result['sha256'],hashlib.sha256(text.encode()).hexdigest())
        journal=CallJournal(value['id'],'large')
        journal.prepare_batch([tool_call()],0)
        journal.record_result(0,'effect',json.loads(text))
        self.assertEqual(journal.entries()[0]['result'],json.loads(text))
        with self.database.transaction() as connection:
            row=connection.execute("SELECT data FROM journal_events ORDER BY sequence DESC LIMIT 1").fetchone()[0]
        self.assertLess(len(row),600)
        self.assertEqual(len(list(self.database.artifacts.directory.glob('*/*.utf8'))),1)

    def test_missing_or_corrupt_artifact_fails_without_mutating_history(self):
        text='output'*10000
        value=conversation(messages=[{'role':'tool','tool_call_id':'effect','content':text}])
        chat_store.save_chat(value)
        path=next(self.database.artifacts.directory.glob('*/*.utf8'))
        path.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'сумма'):
            chat_store.load_chat(value['id'])
        self.assertEqual(path.read_bytes(),b'changed')
        path.unlink()
        with self.assertRaisesRegex(ValueError,'отсутствует'):
            chat_store.load_chat(value['id'])

    def test_legacy_receipts_migrate_once_and_torn_tail_is_retained(self):
        journal=LegacyCallJournal('chat','epoch',self.root/'tasks'/'journals')
        journal.prepare_batch([tool_call()],0)
        journal.set_phase(0,'effect','started')
        journal.record_result(0,'effect',{'ok':True,'bytes':2})
        with journal.path.open('ab') as stream:
            stream.write(b'{torn')
        before=journal.path.read_bytes()
        canonical=CallJournal('chat','epoch')
        messages=[]
        result=canonical.recover(messages)
        self.assertTrue(result['warnings'])
        self.assertEqual(json.loads(messages[1]['content']),{'ok':True,'bytes':2})
        self.assertEqual(journal.path.read_bytes(),before)
        self.assertEqual(len(CallJournal('chat','epoch').entries()),1)

    def test_corrupt_complete_journal_blocks_import_and_keeps_source(self):
        journal=LegacyCallJournal('chat','epoch',self.root/'tasks'/'journals')
        journal.prepare_batch([tool_call()],0)
        with journal.path.open('ab') as stream:
            stream.write(b'{broken}\n')
        before=journal.path.read_bytes()
        with self.assertRaisesRegex(ValueError,'corrupt'):
            CallJournal('chat','epoch').entries()
        self.assertEqual(journal.path.read_bytes(),before)

    def test_two_processes_share_atomic_call_validation(self):
        self.database.ready()
        script="""
import sys
from pathlib import Path
from agent import task_store
from agent.call_journal import CallJournal
task_store.TASK_DIR=Path(sys.argv[1])/'tasks'
call={'id':'same','type':'function','function':{'name':'read_file','arguments':'{}'}}
journal=CallJournal('chat','parallel');journal.prepare_batch([call],0)
journal.set_phase(0,'same','started',effectful=False)
"""
        processes=[subprocess.Popen([sys.executable,'-c',script,str(self.root)],stdout=subprocess.PIPE,stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            _,error=process.communicate(timeout=20)
            self.assertEqual(process.returncode,0,error)
        journal=CallJournal('chat','parallel')
        self.assertEqual(journal.entries()[0]['phase'],'started')
        with self.database.transaction() as connection:
            self.assertEqual(connection.execute('SELECT count(*) FROM journal_events').fetchone()[0],2)

    def test_deletion_is_atomic_and_cannot_resurrect_legacy_data(self):
        value=conversation()
        self.legacy(value)
        old=LegacyCallJournal(value['id'],'epoch',self.root/'tasks'/'journals')
        old.prepare_batch([tool_call()],0)
        journal=CallJournal(value['id'],'epoch')
        self.assertEqual(len(journal.entries()),1)
        task_store.save_task({'chat_id':value['id'],'status':'paused'})
        chat_store.delete_chat(value['id'])
        self.assertIsNone(chat_store.load_chat(value['id']))
        self.assertIsNone(task_store.load_task(value['id']))
        self.assertEqual(CallJournal(value['id'],'epoch').entries(),[])
        self.assertTrue(old.path.exists())
        self.assertTrue((self.root/'chats'/(value['id']+'.json')).exists())

    def test_project_removal_detaches_all_chat_modes_in_one_transaction(self):
        projects=ProjectStore(self.root)
        project=projects.save({'name':'Сайт'})
        for index,mode in enumerate(('chat','ide','voice'),1):
            value=conversation(str(index)*32,mode)
            value['project_id']=project['id']
            chat_store.save_chat(value)
        projects.remove(project['id'])
        self.assertEqual(projects.list(),[])
        self.assertEqual(len(self.database.catalog(project_id='')['chats']),3)
        self.assertTrue(all(chat_store.load_chat(str(i)*32)['project_id']=='' for i in range(1,4)))

    def test_verified_backup_restores_database_receipts_and_full_outputs(self):
        value=conversation(messages=[{'role':'tool','tool_call_id':'effect','content':'output'*5000}])
        original=self.legacy(value)
        self.database.ready()
        inactive=LegacyCallJournal('inactive','epoch',self.root/'tasks'/'journals')
        inactive.prepare_batch([tool_call()],0)
        inactive.set_phase(0,'effect','started')
        journal=CallJournal(value['id'],'epoch')
        journal.prepare_batch([tool_call()],0)
        journal.record_result(0,'effect',{'ok':True,'stdout':'receipt'*5000})
        archive=self.root.parent/'backup.zip'
        self.database.backup(archive)
        restored=self.root.parent/'restored'
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertIn('legacy/chats/'+value['id']+'.json',bundle.namelist())
            bundle.extractall(restored)
        self.assertEqual(Storage(restored).ready().load_chat(value['id']),value)
        with patch.object(task_store,'TASK_DIR',restored/'tasks'):
            self.assertEqual(CallJournal(value['id'],'epoch').entries()[0]['result']['stdout'],'receipt'*5000)
            self.assertEqual(len(CallJournal('inactive','epoch').unresolved()),1)
        self.assertEqual(json.loads(original.read_text(encoding='utf-8')),value)
        with self.assertRaises(ValueError):
            self.database.backup(self.root/'bad.zip')
