"""Offline Windows System.Speech adapter; JSON is data, never PowerShell source."""
import base64
import json
import os
import subprocess
import threading
import time
from pathlib import Path

from agent.process_job import ProcessJob

SPEECH_SCRIPT = r'''
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
[Console]::InputEncoding=[System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$synth=$null
try {
  Add-Type -AssemblyName System.Speech
  $request=[Console]::In.ReadToEnd() | ConvertFrom-Json
  $synth=[System.Speech.Synthesis.SpeechSynthesizer]::new()
  if($request.action -eq 'catalog') {
    @{ok=$true;voices=@($synth.GetInstalledVoices() | Where-Object Enabled | Select-Object -First 100 | ForEach-Object {@{id=$_.VoiceInfo.Name;culture=$_.VoiceInfo.Culture.Name}});recognizers=@([System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers() | Select-Object -First 100 | ForEach-Object {@{id=$_.Id;culture=$_.Culture.Name}})} | ConvertTo-Json -Compress -Depth 5
  } elseif($request.action -in @('speak','render')) {
    $synth.SelectVoice([string]$request.voice)
    $synth.Rate=[int]$request.rate
    $synth.Volume=[int]$request.volume
    if($request.action -eq 'render') {$synth.SetOutputToWaveFile([string]$request.output)}
    else {$synth.SetOutputToDefaultAudioDevice()}
    $synth.Speak([string]$request.text)
    @{ok=$true} | ConvertTo-Json -Compress
  } else {throw 'Unknown speech action'}
} catch {
  @{ok=$false;error=$_.Exception.Message} | ConvertTo-Json -Compress
  exit 1
} finally {if($null -ne $synth){$synth.Dispose()}}
'''


def speech_command():
    if os.name != 'nt':
        raise RuntimeError('Windows System.Speech доступен только в Windows; выберите другой TTS provider')
    executable=Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
    if not executable.is_file():
        raise FileNotFoundError('Windows PowerShell не найден')
    encoded=base64.b64encode(SPEECH_SCRIPT.encode('utf-16le')).decode('ascii')
    return [str(executable),'-NoProfile','-NonInteractive','-EncodedCommand',encoded]


class SpeechService:
    def __init__(self):
        self.lock=threading.RLock()
        self.state='idle'
        self.error=''
        self.voices=[]
        self.recognizers=[]
        self.thread=None
        self.cancelled=threading.Event()
        self.sequence=0

    def status(self):
        with self.lock:
            return {'ok':True,'state':self.state,'error':self.error,'voices':list(self.voices),
                    'recognizers':list(self.recognizers),'sequence':self.sequence,'provider':'windows-system-speech'}

    def refresh(self):
        return self._start({'action':'catalog'},'loading',15)

    def speak(self, params):
        text=params.get('text')
        voice=params.get('voice')
        rate=params.get('rate',0)
        volume=params.get('volume',70)
        if not isinstance(text,str) or not text.strip() or len(text)>6000 or '\x00' in text:
            raise ValueError('Для озвучки нужен текст 1–6000 символов без NUL')
        with self.lock:
            if voice not in [v['id'] for v in self.voices]:
                raise ValueError('Выберите установленный голос после обновления списка')
        for value,minimum,maximum in ((rate,-5,5),(volume,0,100)):
            if isinstance(value,bool) or not isinstance(value,int) or not minimum<=value<=maximum:
                raise ValueError('Темп: -5–5, громкость: 0–100, целые числа')
        return self._start({'action':'speak','text':text,'voice':voice,'rate':rate,'volume':volume},'speaking',180)

    def _start(self, payload, state, timeout):
        with self.lock:
            if self.thread and self.thread.is_alive():
                raise ValueError('Дождитесь завершения или остановите текущую голосовую операцию')
            command=speech_command()
            self.cancelled=cancelled=threading.Event()
            self.state,self.error=state,''
            self.sequence+=1

            def run():
                process=None
                job=None
                try:
                    if cancelled.is_set():
                        return
                    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                    job=ProcessJob(process)
                    # communicate has a short timeout so cancellation stays responsive. The fixed
                    # script emits only one bounded catalog/result, never the input text.
                    raw_input=json.dumps(payload,ensure_ascii=False).encode('utf-8')
                    deadline=time.monotonic()+timeout
                    first=True
                    while True:
                        if cancelled.is_set():
                            return
                        if time.monotonic()>=deadline:
                            raise TimeoutError('Время голосовой операции истекло')
                        try:
                            output,_=process.communicate(input=raw_input if first else None,timeout=.1)
                            break
                        except subprocess.TimeoutExpired:
                            first=False
                    if len(output)>100_000:
                        raise ValueError('Слишком большой ответ системного голоса')
                    result=json.loads(output.decode('utf-8-sig'))
                    if not result.get('ok') or process.returncode:
                        raise RuntimeError(str(result.get('error','Системный голос завершился с ошибкой'))[:1000])
                    with self.lock:
                        if payload['action']=='catalog':
                            self.voices=result.get('voices',[])[:100]
                            self.recognizers=result.get('recognizers',[])[:100]
                except Exception as exc:
                    if not cancelled.is_set():
                        with self.lock:
                            self.error=str(exc)[:1000]
                finally:
                    try:
                        if job:
                            job.close()
                        if process:
                            if process.poll() is None:
                                process.kill()
                            process.communicate(timeout=3)
                    except Exception as exc:
                        with self.lock:
                            if not cancelled.is_set():self.error=str(exc)[:1000]
                    finally:
                        with self.lock:
                            self.state='error' if self.error and not cancelled.is_set() else 'idle'
                            if cancelled.is_set():
                                self.error=''

            self.thread=threading.Thread(target=run,daemon=True,name='system-speech')
            self.thread.start()
        return self.status()

    def stop(self):
        with self.lock:
            self.cancelled.set()
            if self.thread and self.thread.is_alive():
                self.state='stopping'
        return self.status()

    def shutdown(self):
        self.stop()
        if self.thread:
            self.thread.join(timeout=4)
