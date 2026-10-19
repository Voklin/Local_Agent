import tempfile
import unittest
from pathlib import Path
from agent.editor_io import read_project_text, save_project_text
from agent.security import AccessDenied


class EditorIOTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.file = self.root / "main.py"
        self.file.write_text("print('hello')\n", encoding="utf-8")
        self.outside = Path(self.temp.name) / "outside.txt"
        self.outside.write_text("secret", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_read_and_save_inside_project(self):
        path, text = read_project_text(self.root, "main.py")
        self.assertEqual(path, self.file.resolve())
        self.assertEqual(text, "print('hello')\n")
        save_project_text(self.root, path, "print('updated')\n")
        self.assertEqual(self.file.read_text(encoding="utf-8"), "print('updated')\n")

    def test_outside_file_is_denied_for_read_and_write(self):
        with self.assertRaises(AccessDenied):
            read_project_text(self.root, self.outside)
        with self.assertRaises(AccessDenied):
            save_project_text(self.root, self.outside, "changed")
        self.assertEqual(self.outside.read_text(encoding="utf-8"), "secret")

    def test_oversized_file_is_rejected(self):
        with self.assertRaises(ValueError):
            read_project_text(self.root, "main.py", max_bytes=2)

    def test_nonexistent_file_cannot_be_saved(self):
        with self.assertRaises((FileNotFoundError, AccessDenied)):
            save_project_text(self.root, "new.py", "x=1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
