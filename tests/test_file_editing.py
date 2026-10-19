"""File-editing tool tests. Run: python -m unittest discover -s tests -v"""
import tempfile
import unittest
from pathlib import Path
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
        result = write_file(self.root, "new.py", 'print("hello")\n', approved=True)
        self.assertTrue(result["ok"], result)
        self.assertEqual((self.root / "new.py").read_text(encoding="utf-8"), 'print("hello")\n')

    def test_existing_file_requires_overwrite_flag(self):
        result = write_file(self.root, "existing.py", "new content", approved=True)
        self.assertFalse(result["ok"])
        self.assertEqual((self.root / "existing.py").read_text(encoding="utf-8"), 'print("old")\n')

    def test_overwrite_existing_file(self):
        result = write_file(self.root, "existing.py", "new content", overwrite=True, approved=True)
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
        allowed = execute_tool("write_file", args, self.root, approved=True)
        self.assertTrue(allowed["ok"], allowed)
        self.assertEqual((self.root / "dispatch.txt").read_text(encoding="utf-8"), "through dispatcher")


if __name__ == "__main__":
    unittest.main(verbosity=2)
