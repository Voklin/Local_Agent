import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.project_memory import (empty_memory, validate_memory, format_memory_context,
    merge_memory_update, save_project_memory, load_project_memory, clear_project_memory)

class ProjectMemoryTests(unittest.TestCase):
    def test_round_trip_is_project_scoped(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            project_a, project_b = base / "a", base / "b"
            project_a.mkdir(); project_b.mkdir()
            with patch("agent.project_memory.MEMORY_DIR", base / "memory"):
                save_project_memory(str(project_a), {"project_summary": "Проект А", "decisions": ["PySide6"]})
                self.assertEqual(load_project_memory(str(project_a))["project_summary"], "Проект А")
                self.assertEqual(load_project_memory(str(project_b))["project_summary"], "")

    def test_validation_limits_and_deduplicates(self):
        memory = validate_memory({"project_summary": "x" * 5000, "decisions": ["a", "a", 42]}, "/tmp/project")
        self.assertLessEqual(len(memory["project_summary"]), 1200)
        self.assertEqual(memory["decisions"], ["a"])

    def test_context_is_compact_and_marked_as_reference(self):
        memory = empty_memory("/tmp/project")
        memory["constraints"] = ["Не менять sandbox"]
        context = format_memory_context(memory)
        self.assertIn("справочные заметки", context)
        self.assertIn("Не менять sandbox", context)

    def test_merge_preserves_missing_fields(self):
        current = empty_memory("/tmp/project")
        current["decisions"] = ["Не использовать shell"]
        updated = merge_memory_update(current, {"current_focus": "Тесты"}, "/tmp/project")
        self.assertEqual(updated["decisions"], ["Не использовать shell"])
        self.assertEqual(updated["current_focus"], "Тесты")

    def test_clear_only_clears_memory_file(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"; project.mkdir()
            with patch("agent.project_memory.MEMORY_DIR", Path(td) / "memory"):
                save_project_memory(str(project), {"project_summary": "test"})
                clear_project_memory(str(project))
                self.assertEqual(load_project_memory(str(project))["project_summary"], "")

if __name__ == "__main__": unittest.main()
