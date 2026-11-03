"""Real HTTP PCM validation, playback acknowledgement and bounded cancellation."""
import io
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import threading
import time
import unittest
import wave

from agent.companion_preferences import validate_profile,DEFAULT_PROFILE
from core.python.neural_speech import NeuralSpeech


class NeuralSpeechTests(unittest.TestCase):
    def test_http_busy_and_deadline_have_actionable_messages(self):
        for code,expected in ((429,'занят'),(504,'короткую фразу')):
            with self.subTest(code=code):
                class Handler(BaseHTTPRequestHandler):
                    def do_POST(self):
                        self.send_response(code);self.end_headers()
                    def log_message(self,*args):pass
                server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
                thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
                events=[];service=NeuralSpeech(events.append)
                try:
                    profile={**DEFAULT_PROFILE,'tts_url':f'http://127.0.0.1:{server.server_port}/v1/audio/speech'}
                    service.speak({'text':'Привет'},profile);service.thread.join(3)
                    self.assertEqual(service.state,'error');self.assertIn(expected,service.error)
                    self.assertNotIn('HTTPStatusError',service.error);self.assertEqual(events,[])
                finally:service.shutdown();server.shutdown();server.server_close();thread.join(2)

    def test_http_audio_and_exact_playback_sequence(self):
        output=io.BytesIO()
        with wave.open(output,'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000);wav.writeframes(b'\0\0'*2400)
        requests=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(200);self.end_headers();self.wfile.write(output.getvalue())
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        events=[];audio=threading.Event()
        def emit(event):
            events.append(event)
            if event['event']=='voice_audio':audio.set()
        service=NeuralSpeech(emit)
        try:
            profile=validate_profile({**DEFAULT_PROFILE,'tts_provider':'qwen3','tts_url':f'http://127.0.0.1:{server.server_port}/v1/audio/speech'})
            service.speak({'text':'Привет, я Лола!'},profile)
            self.assertTrue(audio.wait(5));self.assertEqual(requests[0]['language'],'Russian')
            self.assertIn('anime',requests[0]['instructions'])
            self.assertFalse(service.playback({'sequence':0})['ok'])
            self.assertTrue(service.playback({'sequence':1})['ok']);service.thread.join(2)
            self.assertEqual(service.status()['state'],'idle')
            self.assertTrue(events[0]['audio'].startswith('UklGR'))
            with self.assertRaises(ValueError):service.speak({'text':'x'*1201},profile)
        finally:service.shutdown();server.shutdown();server.server_close();thread.join(2)

    def test_cancel_closes_stalled_synthesis(self):
        entered=threading.Event();release=threading.Event()
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):entered.set();release.wait(5)
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        service=NeuralSpeech(lambda event:None)
        try:
            profile=validate_profile({**DEFAULT_PROFILE,'tts_url':f'http://127.0.0.1:{server.server_port}/v1/audio/speech'})
            service.speak({'text':'Привет'},profile);self.assertTrue(entered.wait(3))
            start=time.monotonic();service.stop();service.thread.join(2)
            self.assertFalse(service.thread.is_alive());self.assertLess(time.monotonic()-start,2)
            self.assertEqual(service.state,'idle')
            self.assertFalse(service.playback({'sequence':1})['ok'])
        finally:release.set();service.shutdown();server.shutdown();server.server_close();thread.join(2)
