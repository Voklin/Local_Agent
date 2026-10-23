"""Optional loopback Qwen3-TTS VoiceDesign server; run in its own environment."""
import argparse
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading

MODEL_ID='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign'
DEFAULT_STYLE='A young adult female anime assistant. Bright, gentle, slightly high-pitched voice, playful expressive intonation, warm and caring. Speak natural Russian clearly, without whispering or shouting.'


def synthesize(model, text, style):
    import soundfile as sf
    import torch
    torch.manual_seed(42)
    with torch.inference_mode():
        wavs,rate=model.generate_voice_design(text=text,language='Russian',instruct=style,max_new_tokens=1536)
    if not 0<len(wavs[0])<=rate*120:raise ValueError('Audio duration limit exceeded')
    output=io.BytesIO();sf.write(output,wavs[0],rate,format='WAV',subtype='PCM_16')
    return output.getvalue()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/health':self.send_error(404);return
        self.reply(200,json.dumps({'ok':True,'model':MODEL_ID}).encode(),'application/json')

    def do_POST(self):
        self.connection.settimeout(10)
        if self.path!='/v1/audio/speech':self.send_error(404);return
        if self.headers.get('Origin') or self.headers.get_content_type()!='application/json':self.send_error(403);return
        if not self.server.generation.acquire(blocking=False):self.send_error(429);return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=16000:raise ValueError('Request limit')
            data=json.loads(self.rfile.read(size));text=data.get('input','');style=data.get('instructions',DEFAULT_STYLE)
            if not isinstance(text,str) or not 1<=len(text.strip())<=1200 or '\x00' in text:raise ValueError('Text limit')
            if not isinstance(style,str) or not 1<=len(style)<=1500:raise ValueError('Style limit')
            audio=synthesize(self.server.model,text,style)
            self.reply(200,audio,'audio/wav')
        except (BrokenPipeError,ConnectionResetError):pass
        except Exception as exc:self.reply(400,json.dumps({'error':type(exc).__name__}).encode(),'application/json')
        finally:self.server.generation.release()

    def reply(self, code, body, content_type):
        self.send_response(code);self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=9080)
    parser.add_argument('--device',choices=('cpu','cuda','auto'),default='cpu')
    args=parser.parse_args()
    import torch
    from qwen_tts import Qwen3TTSModel
    torch.set_num_threads(4)
    device='cuda:0' if args.device=='cuda' or (args.device=='auto' and torch.cuda.is_available()) else 'cpu'
    print('Loading Qwen3-TTS VoiceDesign; first launch downloads model weights (several GB).',flush=True)
    model=Qwen3TTSModel.from_pretrained(MODEL_ID,device_map=device,
        dtype=torch.float32 if device=='cpu' else torch.float16,attn_implementation='sdpa')
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.daemon_threads=True
    server.model=model;server.generation=threading.Lock()
    print(f'Ready: http://127.0.0.1:{args.port}/v1/audio/speech ({device})',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
