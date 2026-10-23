"""Cancellable local Qwen3 voice design HTTP synthesis with renderer playback."""
import asyncio
import base64
import io
import json
import threading
import wave

import httpx


class NeuralSpeech:
    def __init__(self, emit):
        self.emit=emit;self.lock=threading.RLock();self.thread=None
        self.cancelled=threading.Event();self.played=threading.Event()
        self.sequence=0;self.state='idle';self.error=''

    def status(self):
        with self.lock:
            return {'ok':True,'state':self.state,'error':self.error,'sequence':self.sequence,
                    'provider':'qwen3','voices':[{'id':'miya-anime-ru','culture':'ru-RU'}],'recognizers':[]}

    def speak(self, params, profile):
        text=params.get('text','');volume=params.get('volume',70);rate=params.get('rate',0)
        if not isinstance(text,str) or not text.strip() or len(text)>1200 or '\x00' in text:
            raise ValueError('Нейроозвучка: от 1 до 1200 символов')
        if type(volume)!=int or not 0<=volume<=100 or type(rate)!=int or not -5<=rate<=5:
            raise ValueError('Некорректные громкость или темп')
        with self.lock:
            if self.thread and self.thread.is_alive():raise ValueError('Сначала остановите текущую озвучку')
            self.sequence+=1;sequence=self.sequence
            self.cancelled=cancelled=threading.Event();self.played=threading.Event()
            self.state='synthesizing';self.error=''
            def run():
                try:
                    audio=asyncio.run(self.fetch(text,profile,cancelled))
                    with self.lock:
                        if cancelled.is_set():return
                        self.state='speaking'
                        self.emit({'event':'voice_audio','sequence':sequence,'audio':base64.b64encode(audio).decode(),
                                   'volume':volume/100,'rate':2**(rate/10)})
                    for _ in range(2000):
                        if cancelled.is_set() or self.played.wait(.1):break
                    else:raise TimeoutError('Плеер не завершил озвучку')
                except Exception as exc:
                    if not cancelled.is_set():self.error='Нейроозвучка: '+type(exc).__name__+'; проверьте локальный TTS сервер'
                finally:
                    with self.lock:self.state='error' if self.error and not cancelled.is_set() else 'idle'
            self.thread=threading.Thread(target=run,daemon=True,name='neural-speech');self.thread.start()
        return self.status()

    async def fetch(self, text, profile, cancelled):
        async def request():
            async with httpx.AsyncClient(timeout=180,trust_env=False,follow_redirects=False) as client:
                async with client.stream('POST',profile['tts_url'],json={'input':text,'voice':'miya-anime-ru',
                    'instructions':profile['tts_style'],'language':'Russian','response_format':'wav'}) as response:
                    response.raise_for_status();data=bytearray()
                    async for chunk in response.aiter_bytes():
                        data.extend(chunk)
                        if len(data)>15_000_000:raise ValueError('Слишком большой звук')
                with wave.open(io.BytesIO(data),'rb') as wav:
                    if wav.getnchannels()!=1 or wav.getsampwidth()!=2 or not 8000<=wav.getframerate()<=48000 or not 0<wav.getnframes()<=wav.getframerate()*120:
                        raise ValueError('Ожидается PCM16 mono WAV до 120 секунд')
                return bytes(data)
        async def cancellation():
            while not cancelled.is_set():await asyncio.sleep(.05)
        worker=asyncio.create_task(request());stop=asyncio.create_task(cancellation())
        try:
            done,_=await asyncio.wait({worker,stop},timeout=180,return_when=asyncio.FIRST_COMPLETED)
            if cancelled.is_set():raise ValueError('Отменено')
            if worker not in done:raise TimeoutError('TTS timeout')
            return await worker
        finally:
            worker.cancel();stop.cancel();await asyncio.gather(worker,stop,return_exceptions=True)

    def playback(self, params):
        with self.lock:
            if params.get('sequence')!=self.sequence or self.cancelled.is_set():return {'ok':False,'error':'Устаревшая озвучка'}
            if params.get('error'):self.error='Не удалось воспроизвести звук; нажмите «Озвучить» ещё раз'
            self.played.set()
        return {'ok':True}

    def stop(self):
        with self.lock:
            self.cancelled.set();self.played.set();self.error=''
            self.emit({'event':'voice_audio_stop','sequence':self.sequence})
            if self.thread and self.thread.is_alive():self.state='stopping'
        return self.status()

    def shutdown(self):
        self.stop()
        if self.thread:self.thread.join(timeout=3)
