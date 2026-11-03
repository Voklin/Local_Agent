"""Exercise cancellation and deadline over real HTTP without neural weights."""
from http.server import ThreadingHTTPServer
import io
import json
import socket
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import wave

import httpx

from tools.tts import qwen_server
from tools.tts import piper_server


class FakeTalker:
    def register_forward_pre_hook(self, hook):
        self.guard=hook
        return self

    def remove(self):
        self.guard=None


class TtsServerTests(unittest.TestCase):
    def setUp(self):
        self.server=ThreadingHTTPServer(('127.0.0.1',0),qwen_server.Handler)
        self.server.daemon_threads=True;self.server.generation=threading.Lock()
        self.talker=FakeTalker();self.server.model=SimpleNamespace(model=SimpleNamespace(talker=self.talker))
        self.entered=threading.Event();self.blocked=True
        self.patch=patch.object(qwen_server,'synthesize',self.generate);self.patch.start()
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.url=f'http://127.0.0.1:{self.server.server_port}'

    def generate(self, model, text, style):
        self.entered.set()
        while self.blocked:
            model.model.talker.guard(None,None);time.sleep(.01)
        result=io.BytesIO()
        with wave.open(result,'wb') as audio:
            audio.setnchannels(1);audio.setsampwidth(2);audio.setframerate(24000);audio.writeframes(bytes(480))
        return result.getvalue()

    def tearDown(self):
        self.blocked=False;self.server.shutdown();self.server.server_close();self.thread.join(2);self.patch.stop()

    def test_disconnect_releases_busy_server_and_allows_retry(self):
        client=socket.create_connection(self.server.server_address,timeout=3)
        try:
            body=json.dumps({'input':'Привет'}).encode()
            client.sendall(f'POST /v1/audio/speech HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n'.encode()+body)
            self.assertTrue(self.entered.wait(3))
            busy=httpx.post(self.url+'/v1/audio/speech',json={'input':'Ещё'},trust_env=False)
            self.assertEqual(busy.status_code,429)
            self.assertTrue(httpx.get(self.url+'/health',trust_env=False).json()['busy'])
        finally:client.close()
        deadline=time.monotonic()+3
        while self.server.generation.locked() and time.monotonic()<deadline:time.sleep(.01)
        self.assertFalse(self.server.generation.locked());self.assertIsNone(self.talker.guard)
        self.blocked=False
        retry=httpx.post(self.url+'/v1/audio/speech',json={'input':'Привет'},trust_env=False)
        self.assertEqual(retry.status_code,200);self.assertTrue(retry.content.startswith(b'RIFF'))

    def test_deadline_returns_504_and_removes_hook(self):
        with patch.object(qwen_server,'GENERATION_TIMEOUT',.05):
            result=httpx.post(self.url+'/v1/audio/speech',json={'input':'Привет'},trust_env=False)
        self.assertEqual(result.status_code,504)
        self.assertFalse(self.server.generation.locked());self.assertIsNone(self.talker.guard)

    def test_piper_backend_wav_and_disconnect_guard(self):
        chunk=SimpleNamespace(sample_channels=1,sample_width=2,sample_rate=22050,audio_int16_bytes=bytes(440))
        voice=SimpleNamespace(synthesize=lambda text:iter([chunk,chunk]))
        self.server.synthesize=lambda text,guard:piper_server.synthesize(voice,text,guard)
        result=httpx.post(self.url+'/v1/audio/speech',json={'input':'Привет'},trust_env=False)
        self.assertEqual(result.status_code,200)
        with wave.open(io.BytesIO(result.content),'rb') as wav:
            self.assertEqual(wav.getnframes(),440)
            self.assertEqual(wav.getframerate(),22050)
            self.assertEqual((wav.getnchannels(),wav.getsampwidth()),(1,2))
        self.assertFalse(self.server.generation.locked())
        with self.assertRaises(ConnectionAbortedError):
            piper_server.synthesize(voice,'Привет',lambda *args:(_ for _ in ()).throw(ConnectionAbortedError()))
