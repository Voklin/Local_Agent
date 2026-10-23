import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from core.python.speech_service import SpeechService, speech_command


class SpeechServiceTests(unittest.TestCase):
    def setUp(self):
        self.service=SpeechService()
        self.service.voices=[{'id':'fixture-voice','culture':'ru-RU'}]

    def tearDown(self):
        self.service.shutdown()

    def test_invalid_text_voice_and_numeric_options_never_start_audio(self):
        for params in ({'text':''},{'text':'x'*6001},{'text':'hello','voice':'missing'},
                       {'text':'hello','rate':True},{'text':'hello','volume':101}):
            with self.assertRaises(ValueError):self.service.speak({'voice':'fixture-voice',**params})
        self.assertIsNone(self.service.thread)

    def test_catalog_runs_outside_bridge_and_returns_installed_choices(self):
        command=[sys.executable,'-u','-c',"import json,sys,time;json.loads(sys.stdin.buffer.read().decode('utf-8'));time.sleep(.2);print(json.dumps({'ok':True,'voices':[{'id':'fixture','culture':'ru-RU'}],'recognizers':[]}))"]
        with patch('core.python.speech_service.speech_command',return_value=command):
            result=self.service.refresh();self.assertEqual(result['state'],'loading')
            with self.assertRaises(ValueError):self.service.refresh()
            self.service.thread.join(3)
        self.assertEqual(self.service.status()['voices'][0]['id'],'fixture')
        self.assertEqual(self.service.state,'idle')

    def test_json_text_is_data_and_stop_cleans_owned_worker(self):
        with tempfile.TemporaryDirectory() as temp:
            capture=Path(temp)/'request.json'
            command=[sys.executable,'-u','-c',"import json,sys,time;from pathlib import Path;payload=json.loads(sys.stdin.buffer.read().decode('utf-8'));Path(sys.argv[1]).write_text(json.dumps(payload),encoding='utf-8');time.sleep(20)",str(capture)]
            text='Русский текст "кавычки"; $HOME; $(literal) <tag>😀'
            with patch('core.python.speech_service.speech_command',return_value=command):
                self.service.speak({'text':text,'voice':'fixture-voice'})
                deadline=time.monotonic()+3
                while not capture.exists() and time.monotonic()<deadline:time.sleep(.02)
                self.assertEqual(json.loads(capture.read_text(encoding='utf-8'))['text'],text)
                start=time.monotonic();self.service.stop();self.service.thread.join(3)
            self.assertFalse(self.service.thread.is_alive())
            self.assertLess(time.monotonic()-start,2)
            self.assertEqual(self.service.state,'idle')

    def test_timeout_is_visible_and_worker_can_be_reused(self):
        command=[sys.executable,'-u','-c',"import json,sys,time;json.loads(sys.stdin.buffer.read().decode('utf-8'));time.sleep(10)"]
        with patch('core.python.speech_service.speech_command',return_value=command):
            self.service._start({'action':'catalog'},'loading',.02);self.service.thread.join(3)
        self.assertEqual(self.service.state,'error');self.assertIn('истекло',self.service.error)
        self.assertFalse(self.service.thread.is_alive())
        recovered=[sys.executable,'-c',"import json,sys;json.loads(sys.stdin.buffer.read().decode('utf-8'));print('{\"ok\":true,\"voices\":[],\"recognizers\":[]}')"]
        with patch('core.python.speech_service.speech_command',return_value=recovered):
            self.service.refresh();self.service.thread.join(3)
        self.assertEqual(self.service.state,'idle');self.assertEqual(self.service.error,'')

    @unittest.skipUnless(os.name=='nt','Windows System.Speech only')
    def test_real_system_voice_renders_wave_without_speakers_or_microphone(self):
        command=speech_command()
        catalog=subprocess.run(command,input=b'{"action":"catalog"}',stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
        result=json.loads(catalog.stdout.decode('utf-8-sig'))
        if not result.get('ok') or not result.get('voices'):
            self.skipTest('No installed System.Speech voices')
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'voice.wav'
            payload={'action':'render','voice':result['voices'][0]['id'],'rate':1,'volume':70,
                     'text':'Проверка голоса. Quotes, $HOME and Unicode.','output':str(output)}
            rendered=subprocess.run(command,input=json.dumps(payload,ensure_ascii=False).encode('utf-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
            self.assertEqual(rendered.returncode,0,rendered.stdout)
            with wave.open(str(output),'rb') as stream:
                self.assertGreater(stream.getnframes(),100)
                self.assertGreater(stream.getframerate(),8000)
