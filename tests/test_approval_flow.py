import unittest
try:
    from agent.worker import AgentWorker
except ModuleNotFoundError as exc:
    if exc.name == "PySide6":
        AgentWorker = None
    else:
        raise

@unittest.skipIf(AgentWorker is None, "PySide6 is not installed in the test environment")
class ApprovalFlowTest(unittest.TestCase):
    def test_approval_decisions_are_explicit(self):
        worker = AgentWorker(
            "http://127.0.0.1:8080/v1", "no-key", "test-model",
            ".", "test"
        )
        for decision in ("apply", "reject", "cancel"):
            worker.resolve_write_approval(decision)
            self.assertEqual(worker._approval_result, decision)

if __name__ == "__main__":
    unittest.main()
