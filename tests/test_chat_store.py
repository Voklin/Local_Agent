import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent import chat_store
from agent.storage import Storage


class ChatRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, value in (('CHAT_DIR', self.root/'chats'), ('INDEX_FILE', self.root/'chats/index.json')):
            context = patch.object(chat_store, name, value)
            context.start()
            self.addCleanup(context.stop)

    def test_catalog_ignores_legacy_cache_after_migration(self):
        first = chat_store.create_chat('', 'test')
        second = chat_store.create_chat('', 'test')
        chat_store.CHAT_DIR.mkdir()
        chat_store.INDEX_FILE.write_text('broken legacy cache')
        with patch.object(Path, 'iterdir', side_effect=AssertionError('corpus scan')):
            self.assertEqual({c['id'] for c in chat_store.list_chats()}, {first['id'],second['id']})
        self.assertEqual(chat_store.INDEX_FILE.read_text(), 'broken legacy cache')

    def test_index_failure_rolls_back_transcript_and_metadata(self):
        chat = chat_store.create_chat('', 'test')
        previous = chat_store.load_chat(chat['id'])
        chat.update(title='unsaved', messages=[{'role':'user','content':'unsaved'}])
        with patch.object(Storage, '_search_entry', side_effect=OSError('index fixture')):
            with self.assertRaises(OSError):
                chat_store.save_chat(chat)
        self.assertEqual(chat_store.load_chat(chat['id']), previous)
        self.assertEqual(chat_store.list_chats()[0]['title'], previous['title'])

    def test_corrupted_legacy_chat_is_reported_without_modifying_source(self):
        chat_store.CHAT_DIR.mkdir()
        bad_id = '0'*32
        path = chat_store.CHAT_DIR/(bad_id+'.json')
        path.write_bytes(b'{broken source')
        catalog = chat_store.read_chat_catalog()
        self.assertEqual(catalog['chats'], [])
        self.assertIn(bad_id, catalog['warnings'][0])
        with self.assertRaises(ValueError):
            chat_store.load_chat(bad_id)
        self.assertEqual(path.read_bytes(), b'{broken source')

    def test_store_rejects_path_like_chat_ids(self):
        self.assertIsNone(chat_store.load_chat('../outside'))
        self.assertFalse(chat_store.delete_chat('../outside'))
        with self.assertRaises(ValueError):
            chat_store.save_chat({'id':'../outside','messages':[]})

    def test_unreadable_legacy_directory_is_not_an_empty_catalog(self):
        chat_store.CHAT_DIR.mkdir()
        with patch.object(Path, 'iterdir', side_effect=PermissionError('inaccessible')):
            with self.assertRaises(PermissionError):
                chat_store.read_chat_catalog()
        self.assertEqual(Storage(self.root).ready().catalog()['chats'], [])

    def test_corrupt_database_never_falls_back_to_old_json(self):
        chat_store.create_chat('', 'test')
        path = self.root/'neutral.sqlite3'
        path.write_bytes(b'corrupt database')
        with self.assertRaises(sqlite3.DatabaseError):
            chat_store.list_chats()
        self.assertEqual(path.read_bytes(), b'corrupt database')


class ChatStoreTest(unittest.TestCase):
    def test_create_save_load_rename_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(chat_store,'CHAT_DIR',root/'chats'):
                chat = chat_store.create_chat('', 'test-model')
                chat['messages'] = [{'role':'user','content':'Сделай тест'}]
                chat_store.save_chat(chat)
                self.assertEqual(chat_store.load_chat(chat['id'])['messages'], chat['messages'])
                chat_store.rename_chat(chat['id'], 'Мой тест')
                self.assertEqual(chat_store.load_chat(chat['id'])['title'], 'Мой тест')
                self.assertTrue(chat_store.delete_chat(chat['id']))
                self.assertIsNone(chat_store.load_chat(chat['id']))
