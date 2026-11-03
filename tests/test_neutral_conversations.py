import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from agent import chat_store,task_store
from agent.projects import ProjectStore
from agent.connection_profiles import ConnectionProfiles
from core.python.conversation_service import ConversationService


class NeutralConversationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        for target,value in [(patch.object(chat_store,'CHAT_DIR',self.root/'chats'),None),(patch.object(chat_store,'INDEX_FILE',self.root/'chats/index.json'),None),(patch.object(task_store,'TASK_DIR',self.root/'tasks'),None)]:
            target.start();self.addCleanup(target.stop)
        self.projects=ProjectStore(self.root)
        self.tasks=SimpleNamespace(project_id='',projects=self.projects,chat=None,lock=__import__('threading').RLock(),idle=lambda:None)
        self.tasks.chats=lambda root,mode:{'ok':True,'chats':[c for c in chat_store.read_chat_catalog()['chats'] if c.get('project_id','')==self.tasks.project_id and c.get('mode')==mode and c.get('project_root','')==str(root)]}
        self.service=ConversationService(self.tasks)
        self.chat=chat_store.create_chat('','test','Разговор',mode='chat')
        self.chat['messages']=[{'role':'user','content':'Проверка экспорта'},{'role':'assistant','content':'Ответ сохранён.'}]
        chat_store.save_chat(self.chat);self.params={'mode':'chat','chat_id':self.chat['id']}

    def test_project_instructions_and_chat_move_preserve_canonical_messages(self):
        project=self.projects.save({'name':'Сайт','instructions':'Ответы на русском','root':str(self.root)})
        self.service.update('',{**self.params,'project_id':project['id']})
        self.assertEqual(chat_store.load_chat(self.chat['id'])['messages'],self.chat['messages'])
        self.assertEqual(self.service.search('',{'mode':'chat'})['chats'],[])
        self.tasks.project_id=project['id']
        self.assertEqual(len(self.service.search('',{'mode':'chat','query':'экспорта'})['chats']),1)
        with self.assertRaises(ValueError):self.service.delete('',{**self.params,'mode':'voice','confirmed':True})
        self.assertIsNotNone(chat_store.load_chat(self.chat['id']))

    def test_pin_archive_delete_and_explicit_confirmation(self):
        self.service.update('',{**self.params,'pinned':True})
        self.assertTrue(self.service.search('',{'mode':'chat'})['chats'][0]['pinned'])
        self.service.update('',{**self.params,'archived':True})
        self.assertFalse(self.service.search('',{'mode':'chat'})['chats'])
        self.assertEqual(len(self.service.search('',{'mode':'chat','archived':True})['chats']),1)
        with self.assertRaises(ValueError):self.service.delete('',self.params)
        self.service.delete('',{**self.params,'confirmed':True})
        self.assertIsNone(chat_store.load_chat(self.chat['id']))

    def test_fork_and_retry_never_reuse_checkpoint_or_change_original(self):
        task_store.save_task({'chat_id':self.chat['id'],'status':'paused'})
        result=self.service.fork('',{**self.params,'retry':True})
        self.assertNotEqual(result['chat']['id'],self.chat['id']);self.assertEqual(result['chat']['messages'],[])
        self.assertEqual(result['prompt'],'Проверка экспорта')
        self.assertIsNone(task_store.load_task(result['chat']['id']))
        self.assertEqual(chat_store.load_chat(self.chat['id'])['messages'],self.chat['messages'])

    def test_exports_and_search_keep_modes_isolated(self):
        voice=chat_store.create_chat('','lola','Лола',mode='voice');voice['messages']=[{'role':'user','content':'Секретный разговор Лолы'}];chat_store.save_chat(voice)
        self.assertFalse(self.service.search('',{'mode':'chat','query':'Секретный'})['chats'])
        exported=self.service.export('',{**self.params,'format':'json'})
        self.assertEqual(json.loads(exported['content'])['messages'],self.chat['messages'])
        self.assertIn('## Ассистент',self.service.export('',self.params)['content'])
        with self.assertRaises(ValueError):self.service.export('',{**self.params,'format':'html'})

    def test_profiles_strip_secrets_and_validate_protocol(self):
        profiles=ConnectionProfiles(self.root)
        saved=profiles.save({'name':'OpenAI','api_protocol':'responses','base_url':'https://api.openai.com/v1','model':'test','api_key':'DO-NOT-PERSIST'})
        self.assertNotIn('DO-NOT-PERSIST',profiles.file.read_text());self.assertEqual(saved['api_protocol'],'responses')
        with self.assertRaises(ValueError):profiles.save({'name':'bad','base_url':'https://user:secret@example.com','api_protocol':'chat'})
        profiles.remove(saved['id']);self.assertFalse(profiles.list())
