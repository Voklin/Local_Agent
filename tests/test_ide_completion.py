import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from core.python.ide_completion import complete

class CompletionTests(unittest.TestCase):
    def test_remote_does_not_construct_client(self):
        with patch('core.python.ide_completion.ModelClient') as client:
            with self.assertRaises(ValueError):complete(Path.cwd(),{'base_url':'https://api.openai.com/v1'}, {},None)
            client.assert_not_called()

    def test_outside_root_rejected(self):
        with patch('core.python.ide_completion.ModelClient') as client:
            with self.assertRaises(ValueError):complete(Path.cwd(),{'base_url':'http://127.0.0.1:1234/v1'},{'path':'../outside.py'},None)
            client.assert_not_called()

    def test_small_request_no_tools_and_cleanup(self):
        with patch('core.python.ide_completion.ModelClient') as factory:
            client=factory.return_value
            client.create.return_value=SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='return value'))])
            self.assertEqual(complete(Path.cwd(),{'base_url':'http://127.0.0.1:1234/v1','model':'test'},{'path':'main.py','prefix':'def test():','suffix':''},None),{'text':'return value'})
            self.assertNotIn('tools',client.create.call_args.kwargs)
            self.assertEqual(client.create.call_args.kwargs['max_tokens'],160)
            client.close.assert_called_once()

    def test_large_context_rejected_before_http(self):
        with patch('core.python.ide_completion.ModelClient') as factory:
            with self.assertRaises(ValueError):complete(Path.cwd(),{'base_url':'http://127.0.0.1:1234/v1'}, {'path':'main.py','prefix':'x'*6001},None)
            factory.assert_not_called()
