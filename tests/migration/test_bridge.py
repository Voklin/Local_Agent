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
        bridge.editor.clear()
    def tearDown(self):
        self.temp.cleanup()
        bridge.project_root = None
        bridge.editor.clear()
    def test_chat_scope_does_not_require_selected_folder(self):
        bridge.project_root = None
        with patch.object(bridge.tasks, 'chats', return_value={'ok': True}) as chats:
            self.assertTrue(bridge.handle('list_chats', {'mode': 'chat'})['ok'])
            chats.assert_called_once_with('')
        with self.assertRaises(ValueError):
            bridge.handle('list_chats', {'mode': 'ide'})

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            bridge.handle('new_chat', {'mode': 'unsupported-mode'})

    def test_editor_preview_blocks_task_and_project_switch_invalidates_approval(self):
        document = bridge.handle('editor_read', {'path':'hello.py'})
        proposal = bridge.handle('editor_preview', {'path':'hello.py','content':'changed','revision':document['revision']})
        self.assertTrue(proposal['ok'])
        with self.assertRaises(ValueError):
            bridge.handle('start_task', {'prompt':'hello'})
        bridge.handle('set_project', {'root':str(self.root)})
        with self.assertRaises(ValueError):
            bridge.handle('editor_resolve', {'proposal_id':proposal['proposal_id'],'decision':'apply'})
        self.assertEqual((self.root/'hello.py').read_text(),'print("hi")')

    def test_editor_writes_are_rejected_while_agent_is_running(self):
        document = bridge.handle('editor_read', {'path':'hello.py'})
        with patch.object(bridge.tasks,'idle',side_effect=ValueError('busy')):
            with self.assertRaises(ValueError):
                bridge.handle('editor_preview', {'path':'hello.py','content':'changed','revision':document['revision']})
        self.assertEqual((self.root/'hello.py').read_text(),'print("hi")')

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
