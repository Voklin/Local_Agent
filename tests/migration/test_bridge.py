import importlib.util
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

BRIDGE = Path(__file__).resolve().parents[2] / 'core' / 'python' / 'bridge.py'
spec = importlib.util.spec_from_file_location('lca_bridge', BRIDGE)
bridge = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(bridge)

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'hello.py').write_text('print("hi")', encoding='utf-8')
        bridge.project_root = self.root.resolve()
    def tearDown(self):
        self.temp.cleanup()
        bridge.project_root = None
    def test_chat_scope_does_not_require_selected_folder(self):
        bridge.project_root = None
        with patch.object(bridge.tasks, 'chats', return_value={'ok': True}) as chats:
            self.assertTrue(bridge.handle('list_chats', {'mode': 'chat'})['ok'])
            chats.assert_called_once_with('')
        with self.assertRaises(ValueError):
            bridge.handle('list_chats', {'mode': 'ide'})

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            bridge.handle('new_chat', {'mode': 'voice'})

    def test_health(self):
        self.assertTrue(bridge.handle('health', {})['ok'])
    def test_list_and_read(self):
        self.assertEqual(bridge.handle('list_files', {})['items'][0]['name'], 'hello.py')
        self.assertEqual(bridge.handle('read_file', {'path':'hello.py'})['content'], 'print("hi")')
    def test_parent_traversal_rejected(self):
        with self.assertRaises(PermissionError): bridge.handle('read_file', {'path':'../outside.txt'})
    def test_write_is_not_exposed(self):
        with self.assertRaises(ValueError): bridge.handle('write_file', {'path':'new.py','content':'x'})

if __name__ == '__main__': unittest.main()
