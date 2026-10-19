import tempfile
import unittest
from pathlib import Path
from agent.planner import build_plan
from agent.runtime import AgentRuntime
from agent.skills import SkillManager
from agent.context_manager import ContextManager
from agent.verifier import StageVerifier

class RuntimeArchitectureTests(unittest.TestCase):
    def test_plan_has_stages(self):
        stages = build_plan("добавь функцию и проверь тестами")
        self.assertEqual(stages[0]["id"], "analysis")
        self.assertIn("implementation", [x["id"] for x in stages])
        self.assertIn("verification", [x["id"] for x in stages])

    def test_runtime_prepares_skills_without_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            task={"version":2,"prompt":"исправь python код","stage":"analysis","status":"running","stages":build_plan("исправь python код")}
            rt=AgentRuntime(task, skills_root=Path(__file__).parents[1]/"skills")
            selected=rt.prepare()
            self.assertTrue(task["runtime_version"] == "5.7")
            self.assertIsInstance(selected,list)

    def test_context_is_bounded(self):
        ctx=ContextManager(max_chars=500)
        msgs=[{"role":"system","content":"system"}]+[{"role":"user","content":"x"*300} for _ in range(10)]
        self.assertLessEqual(len(str(ctx.build(msgs))), 900)

    def test_verifier_rejects_stopped_stage(self):
        result=StageVerifier().verify("verification", final_text="ok", stop_reason="stopped")
        self.assertFalse(result["ok"])

if __name__ == "__main__": unittest.main()
