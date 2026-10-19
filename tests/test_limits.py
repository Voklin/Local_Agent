"""Tests for configurable tool limits. Run with: python -m unittest discover -s tests -v"""
import tempfile
import unittest
from pathlib import Path
from agent.tools import list_files, search_text


class ConfigurableLimitsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="local_agent_limits_test_")
        self.root = Path(self.temp.name)
        (self.root / "a.txt").write_text("needle at root", encoding="utf-8")
        (self.root / "b.txt").write_text("second file", encoding="utf-8")
        (self.root / "one").mkdir()
        (self.root / "one" / "c.txt").write_text("needle one level down", encoding="utf-8")
        (self.root / "one" / "two").mkdir()
        (self.root / "one" / "two" / "d.txt").write_text("needle two levels down", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_list_files_obeys_entry_limit(self):
        result = list_files(self.root, ".", recursive=True, max_entries=2, max_depth=5)
        self.assertTrue(result["ok"])
        self.assertLessEqual(len(result["entries"]), 2)
        self.assertTrue(result["truncated"])

    def test_recursive_search_obeys_depth_limit(self):
        result = search_text(self.root, "needle", ".", max_depth=1)
        paths = {item["path"] for item in result["matches"]}
        self.assertIn("a.txt", paths)
        self.assertIn("one/c.txt", paths)
        self.assertNotIn("one/two/d.txt", paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)
