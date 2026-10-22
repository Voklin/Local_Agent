import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from agent import task_store
from agent.task_store import new_task, save_task, load_task, clear_task, set_stage, finish_task

class TaskStoreTests(unittest.TestCase):
    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(task_store, 'TASK_DIR', Path(tmp) / 'tasks'):
            task = new_task("chat-1", tmp, "сделать задачу")
            set_stage(task, "research", "active", "читаю проект")
            saved = save_task(task)
            loaded = load_task("chat-1")
            self.assertEqual(loaded["stage"], "research")
            self.assertEqual(loaded["status"], "running")
            self.assertEqual(loaded["last_event"], "читаю проект")
            finish_task(loaded, "completed")
            loaded = load_task("chat-1")
            self.assertEqual(loaded["status"], "completed")
            self.assertEqual(next(s['status'] for s in loaded['stages'] if s['id'] == 'research'), 'done')
            self.assertEqual(next(s['status'] for s in loaded['stages'] if s['id'] == 'verification'), 'skipped')
            self.assertTrue(all(x["status"] in ('done', 'skipped') for x in loaded["stages"]))
            clear_task("chat-1")
            self.assertIsNone(load_task("chat-1"))

if __name__ == "__main__":
    unittest.main()
