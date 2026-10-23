"""Explicit, nonblocking lifecycle for the application's own llama-server only."""
import threading
import os
import json
from pathlib import Path

from agent.chat_store import APP_DIR, _atomic_write
from agent.model_manager import LocalModel, LocalRuntime


class RuntimeService:
    def __init__(self):
        self.runtime = LocalRuntime()
        self.lock = threading.RLock()
        self.cancelled = threading.Event()
        self.thread = None
        self.preferences_file=APP_DIR/'runtime-preferences.json'
        try:data=json.loads(self.preferences_file.read_text('utf-8'))
        except (OSError,ValueError):data={}
        if not isinstance(data,dict):data={}
        self.cache_types={key:data.get(key) if data.get(key) in ('f16','q8_0','q4_0') else 'f16' for key in ('cache_type_k','cache_type_v')}
        self.options={'threads':max(1,min(4,(os.cpu_count() or 4)//2)),'ctx_size':4096,'gpu_layers':0}
        for key,minimum,maximum in (('threads',1,128),('ctx_size',512,32768),('gpu_layers',-1,256)):
            value=data.get(key)
            if type(value) is int and minimum<=value<=maximum:self.options[key]=value
        self.state = 'stopped'
        self.error = ''

    def start(self, params):
        with self.lock:
            if self.state in ('starting', 'running', 'stopping') or (self.thread and self.thread.is_alive()):
                raise ValueError('Сначала остановите текущий локальный сервер')
            executable = Path(str(params.get('runtime_path', ''))).resolve(strict=True)
            model = Path(str(params.get('model_path', ''))).resolve(strict=True)
            if not executable.is_file() or executable.name.lower() not in ('llama-server.exe', 'llama-server'):
                raise ValueError('Выберите установленный llama-server, а не произвольную программу')
            if not model.is_file() or model.suffix.lower() != '.gguf':
                raise ValueError('Выберите существующий GGUF')
            with model.open('rb') as stream:
                if stream.read(4) != b'GGUF':
                    raise ValueError('Файл не содержит заголовок GGUF')
            cache = {key: params.get(key, self.cache_types[key]) for key in ('cache_type_k','cache_type_v')}
            if any(value not in ('f16','q8_0','q4_0') for value in cache.values()):
                raise ValueError('Тип KV-кеша: f16, q8_0 или q4_0')
            threads=params.get('threads',self.options['threads'])
            if isinstance(threads,bool) or not isinstance(threads,int) or not 1<=threads<=128:
                raise ValueError('Потоки CPU: от 1 до 128')
            extra = ['--threads',str(threads),'--parallel','1','--cache-type-k',cache['cache_type_k'],'--cache-type-v',cache['cache_type_v'], '--flash-attn','on' if cache['cache_type_v'] != 'f16' else 'auto']
            ctx = params.get('ctx_size', self.options['ctx_size'])
            gpu = params.get('gpu_layers', self.options['gpu_layers'])
            for value, minimum, maximum in ((ctx,512,32768),(gpu,-1,256)):
                if isinstance(value,bool) or not isinstance(value,int) or not minimum <= value <= maximum:
                    raise ValueError('Контекст: 512–32768; GPU-слои: -1–256 (0 = CPU)')
            self.cache_types=cache
            self.options={'threads':threads,'ctx_size':ctx,'gpu_layers':gpu}
            _atomic_write(self.preferences_file,{**self.cache_types,**self.options})
            self.cancelled = cancelled = threading.Event()
            self.state, self.error = 'starting', ''
            self.runtime.runtime_path = str(executable)
            local_model = LocalModel(str(model),model.stem,model.stat().st_size)

            def launch():
                try:
                    self.runtime.start(local_model,ctx_size=ctx,gpu_layers=gpu,cancelled=cancelled,extra_args=extra)
                    with self.lock:
                        self.state = 'running' if not cancelled.is_set() else 'stopping'
                    if cancelled.is_set():
                        self.runtime.stop()
                        with self.lock:
                            self.state = 'stopped'
                except Exception as exc:
                    self.runtime.stop()
                    with self.lock:
                        self.state = 'stopped' if cancelled.is_set() else 'error'
                        self.error = '' if cancelled.is_set() else str(exc)[-4000:]

            self.thread = threading.Thread(target=launch,daemon=True,name='local-runtime')
            self.thread.start()
        return self.status()

    def status(self):
        with self.lock:
            if self.state == 'running' and not self.runtime.running:
                self.state, self.error = 'error', 'Локальный сервер завершился'
            return {'ok':True,'state':self.state,'error':self.error,**self.runtime.status(),
                    'logs':''.join(self.runtime.logs)[-4000:],**self.cache_types,**self.options}

    def stop(self):
        with self.lock:
            self.cancelled.set()
            if self.state in ('starting', 'stopping'):
                self.state = 'stopping'
            elif self.state == 'running' or self.runtime.running:
                self.state = 'stopping'

                def terminate():
                    try:
                        self.runtime.stop()
                    finally:
                        with self.lock:
                            self.state = 'stopped'

                self.thread = threading.Thread(target=terminate,daemon=True,name='local-runtime-stop')
                self.thread.start()
            elif not (self.thread and self.thread.is_alive()):
                self.state = 'stopped'
        return self.status()

    def shutdown(self):
        self.stop()
        if self.thread:
            self.thread.join(timeout=8)
        if self.runtime.running:
            self.runtime.stop()
