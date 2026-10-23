"""Cancellable, bounded WAV transcription via whisper.cpp/OpenAI-compatible API."""
import base64
import asyncio
import json
import io
import threading
import wave

import httpx


class TranscriptionService:
    def __init__(self):
        self.lock=threading.RLock()
        self.cancelled=threading.Event()
        self.thread=None
        self.client=None

    def start(self, params, profile, respond):
        """Validate <=60 seconds of mono PCM WAV before starting a network worker."""
        with self.lock:
            if self.thread and self.thread.is_alive():
                raise ValueError('Распознавание уже выполняется')
            encoded=params.get('audio','')
            if not isinstance(encoded,str) or len(encoded)>2_600_000:
                raise ValueError('Запись должна быть короче 60 секунд')
            audio=base64.b64decode(encoded,validate=True)
            with wave.open(io.BytesIO(audio),'rb') as wav:
                if wav.getnchannels()!=1 or wav.getsampwidth()!=2 or wav.getframerate()!=16000 or not 0<wav.getnframes()<=960000:
                    raise ValueError('Ожидается WAV PCM16 mono 16 kHz, до 60 секунд')
            self.cancelled=cancelled=threading.Event()

            def transcribe():
                response={'ok':False,'error':'Распознавание отменено'}
                try:
                    text=asyncio.run(self.request_audio(audio,profile,cancelled))
                    response={'ok':True,'text':text.strip()}
                except Exception as exc:
                    response={'ok':False,'error':'STT: '+type(exc).__name__+'; проверьте адрес и запущенный сервер'}
                finally:
                    respond({'ok':False,'error':'Распознавание отменено'} if cancelled.is_set() else response)

            self.thread=threading.Thread(target=transcribe,daemon=True,name='transcription')
            self.thread.start()

    async def request_audio(self, audio, profile, cancelled):
        async def request():
            async with httpx.AsyncClient(timeout=90,follow_redirects=False,trust_env=False) as client:
                headers={'Authorization':'Bearer '+profile['stt_api_key']} if profile.get('stt_api_key') else {}
                async with client.stream('POST',profile['stt_url'],headers=headers,
                        files={'file':('recording.wav',audio,'audio/wav')},
                        data={'model':profile['stt_model'],'language':profile['stt_language'],'response_format':'json'}) as result:
                    result.raise_for_status();raw=bytearray()
                    async for chunk in result.aiter_bytes():
                        raw.extend(chunk)
                        if len(raw)>1_000_000:raise ValueError('STT ответ слишком велик')
                text=json.loads(raw).get('text')
                if not isinstance(text,str) or len(text)>50000:raise ValueError('STT не вернул допустимый текст')
                return text
        async def cancellation():
            while not cancelled.is_set():await asyncio.sleep(.05)
        worker=asyncio.create_task(request());stop=asyncio.create_task(cancellation())
        try:
            done,_=await asyncio.wait({worker,stop},timeout=90,return_when=asyncio.FIRST_COMPLETED)
            if cancelled.is_set():raise ValueError('Распознавание отменено')
            if worker in done:return await worker
            raise TimeoutError('Истекло время STT')
        finally:
            worker.cancel();stop.cancel();await asyncio.gather(worker,stop,return_exceptions=True)

    def stop(self):
        """Cancel via the event; async worker closes the actual HTTP socket."""
        self.cancelled.set()
        return {'ok':True}

    def shutdown(self):
        self.stop()
        if self.thread:
            self.thread.join(timeout=3)
