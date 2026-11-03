"""Real multipart STT request and cancellation without accessing a microphone."""
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import queue
import threading
import time
import unittest
import wave

from core.python.transcription_service import TranscriptionService


class TranscriptionHandler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass

    def do_POST(self):
        self.server.body=self.rfile.read(int(self.headers['Content-Length']))
        self.server.arrived.set()
        if self.server.stalled:self.server.release.wait(5)
        try:
            self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
            self.wfile.write(json.dumps({'text':'Распознанный текст'}).encode())
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.server=ThreadingHTTPServer(('127.0.0.1',0),TranscriptionHandler)
        self.server.arrived=threading.Event();self.server.release=threading.Event();self.server.stalled=False
        self.server_thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.server_thread.start()
        self.service=TranscriptionService();self.results=queue.Queue()
        output=io.BytesIO()
        with wave.open(output,'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(16000);wav.writeframes(b'\0\0'*1600)
        self.audio=base64.b64encode(output.getvalue()).decode()
        self.profile={'stt_url':f'http://127.0.0.1:{self.server.server_port}/inference','stt_model':'fixture','stt_language':'ru'}

    def tearDown(self):
        self.service.shutdown();self.server.release.set();self.server.shutdown();self.server.server_close();self.server_thread.join(2)

    def test_real_multipart_returns_editable_text(self):
        self.service.start({'audio':self.audio},self.profile,self.results.put)
        result=self.results.get(timeout=10)
        self.assertTrue(result['ok'],result);self.assertEqual(result['text'],'Распознанный текст')
        self.assertIn(b'RIFF',self.server.body);self.assertIn(b'WAVE',self.server.body)
        self.assertIn(b'name="language"',self.server.body)
        self.assertIn(b'name="temperature"\r\n\r\n0',self.server.body)

    def test_cancel_closes_stalled_request_promptly(self):
        self.server.stalled=True
        self.service.start({'audio':self.audio},self.profile,self.results.put)
        self.assertTrue(self.server.arrived.wait(10))
        started=time.monotonic();self.service.stop();self.service.thread.join(2)
        self.assertFalse(self.service.thread.is_alive());self.assertLess(time.monotonic()-started,2)
        self.assertFalse(self.results.get(timeout=1)['ok'])


if __name__=='__main__':unittest.main()
