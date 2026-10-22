import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from agent import model_preferences as preferences


class ModelPreferencesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'settings/model.json'
        self.patch = patch.object(preferences, 'PREFERENCES_FILE', self.path)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_roundtrip_whitelists_nonsecret_fields(self):
        saved = preferences.save_preferences({'base_url':'http://localhost:1234/v1/', 'model':' Qwen ', 'api_key':'secret', 'other':'private'})
        self.assertEqual(saved, {'base_url':'http://localhost:1234/v1','model':'Qwen'})
        self.assertEqual(preferences.load_preferences(), saved)
        self.assertEqual(json.loads(self.path.read_text()), saved)
        self.assertNotIn('secret', self.path.read_text())

    def test_missing_corrupted_or_wrong_shape_uses_defaults(self):
        self.assertEqual(preferences.load_preferences(), preferences.DEFAULTS)
        self.path.parent.mkdir()
        for content in ('{broken', '[]', '{"base_url":"file:///outside"}'):
            self.path.write_text(content)
            self.assertEqual(preferences.load_preferences(), preferences.DEFAULTS)

    def test_credentials_or_invalid_ports_do_not_replace_saved_preferences(self):
        saved = preferences.save_preferences({'base_url':'http://localhost:1234/v1','model':'model'})
        for url in ('http://key:secret@localhost/v1', 'http://localhost/v1?key=secret', 'http://localhost:invalid/v1', 'http://localhost:99999/v1'):
            with self.assertRaises(ValueError):
                preferences.save_preferences({'base_url':url,'model':'bad'})
            self.assertEqual(preferences.load_preferences(), saved)
