"""File-editing tool tests. Run: python -m unittest discover -s tests -v"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent.tools import preview_file_change, write_file, execute_tool
from agent.security import AccessDenied


class FileEditingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="local_agent_write_test_")
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        (self.root / "existing.py").write_text('print("old")\n', encoding="utf-8")
        self.outside = Path(self.temp.name) / "outside.txt"
        self.outside.write_text("keep me", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_does_not_write(self):
        result = preview_file_change(self.root, "existing.py", 'print("new")\n')
        self.assertTrue(result["ok"])
        self.assertIn("-print(\"old\")", result["diff"])
        self.assertEqual((self.root / "existing.py").read_text(encoding="utf-8"), 'print("old")\n')

    def test_write_file_denies_without_explicit_approval(self):
        result = write_file(self.root, "blocked.txt", "must not be written")
        self.assertFalse(result["ok"])
        self.assertEqual(result.get("code"), "APPROVAL_REQUIRED")
        self.assertFalse((self.root / "blocked.txt").exists())

    def test_create_new_file(self):
        result = write_file(self.root, "new.py", 'print("hello")\n', approved=True,
                            expected_snapshot=preview_file_change(self.root, 'new.py', 'print("hello")\n')['snapshot'])
        self.assertTrue(result["ok"], result)
        self.assertEqual((self.root / "new.py").read_text(encoding="utf-8"), 'print("hello")\n')

    def test_existing_file_requires_overwrite_flag(self):
        result = write_file(self.root, "existing.py", "new content", approved=True,
                            expected_snapshot=preview_file_change(self.root, 'existing.py', 'new content')['snapshot'])
        self.assertFalse(result["ok"])
        self.assertEqual((self.root / "existing.py").read_text(encoding="utf-8"), 'print("old")\n')

    def test_overwrite_existing_file(self):
        result = write_file(self.root, "existing.py", "new content", overwrite=True, approved=True,
                            expected_snapshot=preview_file_change(self.root, 'existing.py', 'new content')['snapshot'])
        self.assertTrue(result["ok"], result)
        self.assertEqual((self.root / "existing.py").read_text(encoding="utf-8"), "new content")

    def test_outside_path_denied(self):
        with self.assertRaises(AccessDenied):
            preview_file_change(self.root, str(self.outside), "overwrite")

    def test_dispatch_write_requires_approval(self):
        args = {"path": "dispatch.txt", "content": "through dispatcher", "overwrite": False}
        denied = execute_tool("write_file", args, self.root)
        self.assertFalse(denied["ok"])
        self.assertEqual(denied.get("code"), "APPROVAL_REQUIRED")
        self.assertFalse((self.root / "dispatch.txt").exists())
        allowed = execute_tool("write_file", args, self.root, approved=True,
                               expected_snapshot=preview_file_change(self.root, args['path'], args['content'])['snapshot'])
        self.assertTrue(allowed["ok"], allowed)
        self.assertEqual((self.root / "dispatch.txt").read_text(encoding="utf-8"), "through dispatcher")

    def test_snapshot_is_required_and_model_cannot_supply_it(self):
        args = {'path': 'blocked.txt', 'content': 'new', 'overwrite': True,
                'expected_snapshot': preview_file_change(self.root, 'blocked.txt', 'new')['snapshot']}
        result = execute_tool('write_file', args, self.root, approved=True)
        self.assertEqual(result['code'], 'APPROVAL_SNAPSHOT_REQUIRED')
        self.assertFalse((self.root / 'blocked.txt').exists())

    def test_external_edit_after_preview_is_not_overwritten(self):
        snapshot = preview_file_change(self.root, 'existing.py', 'replacement')['snapshot']
        (self.root / 'existing.py').write_text('external edit', encoding='utf-8')
        result = write_file(self.root, 'existing.py', 'replacement', overwrite=True, approved=True, expected_snapshot=snapshot)
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual((self.root / 'existing.py').read_text(), 'external edit')

    def test_deleted_existing_file_requires_new_approval(self):
        snapshot = preview_file_change(self.root, 'existing.py', 'replacement')['snapshot']
        (self.root / 'existing.py').unlink()
        result = write_file(self.root, 'existing.py', 'replacement', overwrite=True, approved=True, expected_snapshot=snapshot)
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertFalse((self.root / 'existing.py').exists())

    def test_snapshot_binds_path_and_proposed_content(self):
        snapshot = preview_file_change(self.root, 'one.txt', 'shown')['snapshot']
        for path, content in [('two.txt', 'shown'), ('one.txt', 'different')]:
            result = write_file(self.root, path, content, approved=True, expected_snapshot=snapshot)
            self.assertEqual(result['code'], 'FILE_CHANGED')
            self.assertFalse((self.root / path).exists())

    def test_byte_level_line_ending_change_invalidates_preview(self):
        target = self.root / 'existing.py'
        target.write_bytes(b'original\r\n')
        snapshot = preview_file_change(self.root, 'existing.py', 'replacement')['snapshot']
        target.write_bytes(b'original\n')
        result = write_file(self.root, 'existing.py', 'replacement', overwrite=True, approved=True, expected_snapshot=snapshot)
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual(target.read_bytes(), b'original\n')

    def test_second_snapshot_check_catches_edit_during_temp_write(self):
        target = self.root / 'existing.py'
        snapshot = preview_file_change(self.root, 'existing.py', 'replacement')['snapshot']
        with patch('agent.tools.os.fsync', side_effect=lambda _: target.write_text('late edit', encoding='utf-8')):
            result = write_file(self.root, 'existing.py', 'replacement', overwrite=True, approved=True, expected_snapshot=snapshot)
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual(target.read_text(), 'late edit')
        self.assertEqual(list(self.root.glob('.local-agent-tmp-*')), [])

    def test_atomic_create_refuses_file_that_appears_after_final_check(self):
        import os
        target = self.root / 'new.txt'
        snapshot = preview_file_change(self.root, 'new.txt', 'proposed')['snapshot']
        operation = 'rename' if os.name == 'nt' else 'link'
        original_create = getattr(os, operation)
        def late_create(source, destination):
            target.write_text('external', encoding='utf-8')
            return original_create(source, destination)
        with patch('agent.tools.os.' + operation, side_effect=late_create):
            result = write_file(self.root, 'new.txt', 'proposed', overwrite=True, approved=True, expected_snapshot=snapshot)
        self.assertEqual(result['code'], 'FILE_CHANGED')
        self.assertEqual(target.read_text(), 'external')
        self.assertEqual(list(self.root.glob('.local-agent-tmp-*')), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
