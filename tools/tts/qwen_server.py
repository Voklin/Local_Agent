"""Optional loopback Qwen3-TTS server; run in its own environment."""
import argparse
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import select
import socket
import time

MODEL_ID='Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign'
CUSTOM_MODEL_ID='Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice'
DEFAULT_STYLE='A young adult female anime assistant. Bright, gentle, slightly high-pitched voice, playful expressive intonation, warm and caring. Speak natural Russian clearly, without whispering or shouting.'
GENERATION_TIMEOUT=150


def synthesize(model, text, style):
    import soundfile as sf
    import torch
    torch.manual_seed(42)
    with torch.inference_mode():
        speaker=getattr(model,'localagent_speaker',None)
        if speaker:
            wavs,rate=model.generate_custom_voice(text=text,language='Russian',speaker=speaker,max_new_tokens=1536)
        else:
            wavs,rate=model.generate_voice_design(text=text,language='Russian',instruct=style,max_new_tokens=1536)
    if not 0<len(wavs[0])<=rate*120:raise ValueError('Audio duration limit exceeded')
    output=io.BytesIO();sf.write(output,wavs[0],rate,format='WAV',subtype='PCM_16')
    return output.getvalue()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/health':self.send_error(404);return
        self.reply(200,json.dumps({'ok':True,'model':getattr(self.server,'model_id',MODEL_ID),
                                  'speaker':getattr(self.server.model,'localagent_speaker',None),'busy':self.server.generation.locked(),
                                  'device':getattr(self.server,'device','unknown')}).encode(),'application/json')

    def do_POST(self):
        self.connection.settimeout(10)
        if self.path!='/v1/audio/speech':self.send_error(404);return
        if self.headers.get('Origin') or self.headers.get_content_type()!='application/json':self.send_error(403);return
        if not self.server.generation.acquire(blocking=False):
            self.reply(429,b'{"error":"busy"}','application/json');return
        hook=None
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=16000:raise ValueError('Request limit')
            data=json.loads(self.rfile.read(size));text=data.get('input','');style=data.get('instructions',DEFAULT_STYLE)
            if not isinstance(text,str) or not 1<=len(text.strip())<=1200 or '\x00' in text:raise ValueError('Text limit')
            if not isinstance(style,str) or not 1<=len(style)<=1500:raise ValueError('Style limit')
            deadline=time.monotonic()+GENERATION_TIMEOUT
            def guard(module, args):
                if time.monotonic()>=deadline:raise TimeoutError('Generation deadline')
                if select.select([self.connection],[],[],0)[0] and not self.connection.recv(1,socket.MSG_PEEK):
                    raise ConnectionAbortedError('Client disconnected')
            # Qwen3-TTS 0.1.1 discards stopping_criteria in its outer generate().
            # A public PyTorch hook checks before every talker forward instead.
            guard(None,None)
            backend=getattr(self.server,'synthesize',None)
            if backend is None:
                hook=self.server.model.model.talker.register_forward_pre_hook(guard)
                audio=synthesize(self.server.model,text,style)
            else:
                audio=backend(text,guard)
            guard(None,None)
            self.reply(200,audio,'audio/wav')
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):
            print('TTS cancelled: client disconnected',flush=True)
        except Exception as exc:
            code=504 if isinstance(exc,TimeoutError) else 400 if isinstance(exc,(ValueError,TypeError)) else 500
            print(f'TTS request failed: HTTP {code}, {type(exc).__name__}',flush=True)
            self.reply(code,json.dumps({'error':type(exc).__name__}).encode(),'application/json')
        finally:
            if hook is not None:hook.remove()
            self.server.generation.release()

    def reply(self, code, body, content_type):
        self.send_response(code);self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=9080)
    parser.add_argument('--device',choices=('cpu','cuda','auto'),default='cpu')
    parser.add_argument('--dtype',choices=('auto','float32','bfloat16'),default='auto')
    parser.add_argument('--model',choices=('voicedesign-1.7b','custom-0.6b'),default='voicedesign-1.7b')
    parser.add_argument('--speaker',choices=('Ono_Anna','Serena','Vivian','Sohee','Ryan','Aiden','Uncle_Fu','Dylan','Eric'),default='Ono_Anna')
    args=parser.parse_args()
    model_id=CUSTOM_MODEL_ID if args.model=='custom-0.6b' else MODEL_ID
    import torch
    from qwen_tts import Qwen3TTSModel
    from huggingface_hub import snapshot_download
    torch.set_num_threads(4)
    device='cuda:0' if args.device=='cuda' or (args.device=='auto' and torch.cuda.is_available()) else 'cpu'
    dtype=(torch.bfloat16 if args.dtype=='bfloat16' else torch.float32 if args.dtype=='float32'
           else torch.float32 if device=='cpu' else torch.bfloat16)
    if device.startswith('cuda'):
        if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable; run start-tts.ps1 -Device cuda to install CUDA PyTorch.')
        free,_=torch.cuda.mem_get_info()
        minimum=3 if args.model=='custom-0.6b' else 6
        if free<minimum*1024**3:raise RuntimeError(f'TTS needs at least {minimum} GiB free VRAM. Unload the large LM Studio model or use CPU.')
        torch.ones(1,device=device).add_(1).cpu()  # Verify GPU architecture before loading weights.
    print(f'Loading {model_id}; first launch downloads model weights (several GB).',flush=True)
    model_path=snapshot_download(model_id,allow_patterns=['*.json','*.safetensors','*.txt','*.model'])
    model=Qwen3TTSModel.from_pretrained(model_path,device_map=device,
        dtype=dtype,attn_implementation='sdpa')
    if args.model=='custom-0.6b':model.localagent_speaker=args.speaker
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.daemon_threads=True
    server.model=model;server.model_id=model_id;server.device=device;server.generation=threading.Lock()
    print(f'Ready: http://127.0.0.1:{args.port}/v1/audio/speech ({device})',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
