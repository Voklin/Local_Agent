import unittest
from agent.model_gateway import ModelGateway
from agent.model_manager import LocalRuntime


class ModelGatewayTests(unittest.TestCase):
    def test_remote_endpoint(self):
        gateway = ModelGateway(LocalRuntime())
        endpoint = gateway.use_provider("http://127.0.0.1:1234/v1", "qwen", "key", provider="LM Studio")
        self.assertEqual(endpoint.provider, "LM Studio")
        self.assertFalse(endpoint.local)
        self.assertEqual(endpoint.base_url, "http://127.0.0.1:1234/v1")


if __name__ == "__main__":
    unittest.main()
