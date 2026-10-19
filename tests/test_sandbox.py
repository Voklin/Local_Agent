"""Run from project root: python -m unittest discover -s tests -v"""
import unittest
from agent.tools import run_sandbox_self_test

class SandboxIntegrationTest(unittest.TestCase):
    def test_sandbox_self_test_suite(self):
        result = run_sandbox_self_test()
        self.assertTrue(result["ok"], result["details"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
