import tempfile
import unittest
from pathlib import Path
from agent.model_manager import ModelManager, LocalModel, LocalRuntime


class ModelManagerTests(unittest.TestCase):
    def test_scan_gguf_and_quantization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Qwen2.5-Coder-7B-Q4_K_M.gguf").write_bytes(b"gguf")
            (root / "ignore.txt").write_text("x", encoding="utf-8")
            models = ModelManager(root).scan()
            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].quantization, "Q4_K_M")
            self.assertEqual(models[0].name, "Qwen2.5-Coder-7B-Q4_K_M")

    def test_free_port_is_valid(self):
        port = LocalRuntime.free_port()
        self.assertGreater(port, 0)
        self.assertLessEqual(port, 65535)

    def test_status_stopped(self):
        runtime = LocalRuntime(runtime_path="missing-llama-server")
        status = runtime.status()
        self.assertFalse(status["running"])
        self.assertEqual(status["base_url"], "")


if __name__ == "__main__":
    unittest.main()
