import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
