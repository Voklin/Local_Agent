"""CPU Piper adapter for the existing local speech HTTP contract."""
import argparse
import io
from pathlib import Path
import threading
import wave
from http.server import ThreadingHTTPServer

try:
    from .qwen_server import Handler
except ImportError:
    from qwen_server import Handler


def synthesize(voice, text, guard):
    """Collect sentence chunks as bounded PCM16 mono WAV, checking cancellation."""
    output=io.BytesIO();pcm=io.BytesIO()
    frames=0
    rate=None
    for chunk in voice.synthesize(text):
        guard(None,None)
        if chunk.sample_channels!=1 or chunk.sample_width!=2 or not 8000<=chunk.sample_rate<=48000:
            raise ValueError('Unsupported audio format')
        if rate is None:rate=chunk.sample_rate
        elif rate!=chunk.sample_rate:raise ValueError('Sample rate changed')
        frames+=len(chunk.audio_int16_bytes)//2
        if frames>rate*120 or pcm.tell()+len(chunk.audio_int16_bytes)>15*1024**2:
            raise ValueError('Audio duration limit exceeded')
        pcm.write(chunk.audio_int16_bytes)
    if not frames:raise ValueError('No speech generated')
    with wave.open(output,'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
        wav.writeframes(pcm.getvalue())
    return output.getvalue()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',type=Path,required=True)
    parser.add_argument('--port',type=int,default=9080)
    args=parser.parse_args()
    from piper import PiperVoice
    voice=PiperVoice.load(str(args.model),use_cuda=False)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.daemon_threads=True;server.model=voice;server.model_id='Piper/'+args.model.stem
    server.device='cpu';server.generation=threading.Lock()
    server.synthesize=lambda text,guard:synthesize(voice,text,guard)
    print(f'Ready: http://127.0.0.1:{args.port}/v1/audio/speech ({server.model_id}, CPU)',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
