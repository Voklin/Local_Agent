import os
import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import patch
from agent import chat_store


class ChatRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patches = [patch.object(chat_store, 'CHAT_DIR', self.root / 'chats'),
                        patch.object(chat_store, 'INDEX_FILE', self.root / 'chats/index.json')]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def test_missing_corrupt_and_stale_index_is_rebuilt_from_chat_files(self):
        first = chat_store.create_chat(str(self.root), 'test')
        second = chat_store.create_chat(str(self.root), 'test')
        for raw in (b'not json', b'\xff', b'[null, 1, {}]', b'[]'):
            chat_store.INDEX_FILE.write_bytes(raw)
            catalog = chat_store.read_chat_catalog()
            self.assertEqual({c['id'] for c in catalog['chats']}, {first['id'], second['id']})
            self.assertEqual(catalog['warnings'], [])
        chat_store.INDEX_FILE.unlink()
        self.assertEqual(len(chat_store.list_chats()), 2)
        first['title'] = 'updated outside cache'
        (chat_store.CHAT_DIR / (first['id'] + '.json')).write_text(json.dumps(first), encoding='utf-8')
        self.assertEqual(next(c for c in chat_store.list_chats() if c['id'] == first['id'])['title'], first['title'])

    def test_index_failure_does_not_lose_saved_transcript(self):
        original = chat_store._atomic_write
        def write_with_failed_index(path, data):
            if path == chat_store.INDEX_FILE:
                raise OSError('fixture index failure')
            return original(path, data)
        with patch.object(chat_store, '_atomic_write', side_effect=write_with_failed_index):
            chat = chat_store.create_chat(str(self.root), 'test')
            self.assertIn('storage_warning', chat)
            chat['messages'] = [{'role': 'user', 'content': 'persisted'}]
            self.assertIsInstance(chat_store.save_chat(chat), str)
            self.assertEqual(chat_store.load_chat(chat['id'])['messages'], chat['messages'])
            catalog = chat_store.read_chat_catalog()
            self.assertEqual(len(catalog['chats']), 1)
            self.assertTrue(catalog['warnings'])
        self.assertEqual(chat_store.read_chat_catalog()['warnings'], [])
        self.assertEqual(json.loads(chat_store.INDEX_FILE.read_text(encoding='utf-8'))[0]['id'], chat['id'])

    def test_corrupted_chat_is_reported_without_modifying_source(self):
        good = chat_store.create_chat(str(self.root), 'test')
        bad_id = '0' * 32
        path = chat_store.CHAT_DIR / (bad_id + '.json')
        path.write_bytes(b'{broken source')
        catalog = chat_store.read_chat_catalog()
        self.assertEqual([c['id'] for c in catalog['chats']], [good['id']])
        self.assertIn(bad_id, catalog['warnings'][0])
        with self.assertRaises(ValueError):
            chat_store.load_chat(bad_id)
        self.assertEqual(path.read_bytes(), b'{broken source')

    def test_store_rejects_path_like_chat_ids(self):
        outside = self.root / 'outside.json'
        outside.write_text('keep', encoding='utf-8')
        self.assertIsNone(chat_store.load_chat('../outside'))
        self.assertFalse(chat_store.delete_chat('../outside'))
        with self.assertRaises(ValueError):
            chat_store.save_chat({'id': '../outside', 'messages': []})
        self.assertEqual(outside.read_text(), 'keep')

    def test_unreadable_directory_is_not_reported_as_empty_catalog(self):
        with patch.object(Path, 'iterdir', side_effect=PermissionError('fixture inaccessible directory')):
            with self.assertRaises(PermissionError):
                chat_store.read_chat_catalog()

    def test_fsync_failure_leaves_previous_chat_and_cleans_temporary_file(self):
        chat = chat_store.create_chat(str(self.root), 'test')
        path = chat_store.CHAT_DIR / (chat['id'] + '.json')
        previous = path.read_bytes()
        chat['messages'].append({'role': 'user', 'content': 'unsaved'})
        with patch('agent.chat_store.os.fsync', side_effect=OSError('fixture fsync failure')):
            with self.assertRaises(OSError):
                chat_store.save_chat(chat)
        self.assertEqual(path.read_bytes(), previous)
        self.assertEqual(list(chat_store.CHAT_DIR.glob('*.tmp')), [])

class ChatStoreTest(unittest.TestCase):
    def test_create_save_load_rename_delete(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with patch("agent.chat_store.CHAT_DIR", root / "chats"), patch("agent.chat_store.INDEX_FILE", root / "chats" / "index.json"):
                from agent.chat_store import create_chat, save_chat, load_chat, list_chats, rename_chat, delete_chat
                chat = create_chat(str(root), "test-model")
                chat["messages"] = [{"role": "user", "content": "Сделай тест"}]
                save_chat(chat)
                loaded = load_chat(chat["id"])
                self.assertEqual(loaded["messages"][0]["content"], "Сделай тест")
                self.assertEqual(len(list_chats()), 1)
                rename_chat(chat["id"], "Мой тест")
                self.assertEqual(load_chat(chat["id"])["title"], "Мой тест")
                self.assertTrue(delete_chat(chat["id"]))
                self.assertIsNone(load_chat(chat["id"]))

if __name__ == "__main__": unittest.main()
