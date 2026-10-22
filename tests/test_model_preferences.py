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
        self.assertEqual(saved, {'base_url':'http://localhost:1234/v1','model':'Qwen','settings':preferences.DEFAULTS['settings']})
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

    def test_old_preferences_gain_generation_defaults(self):
        self.path.parent.mkdir()
        self.path.write_text('{"base_url":"http://localhost:1234/v1","model":"old"}')
        self.assertEqual(preferences.load_preferences()['settings'], preferences.DEFAULTS['settings'])

    def test_generation_roundtrip_and_invalid_values_do_not_replace_file(self):
        config = {'base_url': 'http://localhost:1234/v1', 'model':'model',
                  'settings': {'temperature':0.7, 'top_p':0.9, 'max_tokens':2048}}
        saved = preferences.save_preferences(config)
        self.assertEqual(preferences.load_preferences(), saved)
        for key, value in [('temperature',float('nan')), ('top_p',0), ('max_tokens',1),
                           ('max_tokens',3.5), ('max_tokens',10**400), ('request_timeout',True), ('max_context_chars',100),
                           ('max_agent_turns',501), ('max_runtime_minutes',0)]:
            with self.subTest(key=key,value=value), self.assertRaises(ValueError):
                preferences.save_preferences({**config,'settings':{key:value}})
            self.assertEqual(preferences.load_preferences(), saved)
