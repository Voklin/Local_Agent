"""Explicit, nonblocking lifecycle for the application's own llama-server only."""
import threading
from pathlib import Path

from agent.model_manager import LocalModel, LocalRuntime


class RuntimeService:
    def __init__(self):
        self.runtime = LocalRuntime()
        self.lock = threading.RLock()
        self.cancelled = threading.Event()
        self.thread = None
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
            ctx = params.get('ctx_size', 4096)
            gpu = params.get('gpu_layers', 0)
            for value, minimum, maximum in ((ctx,512,32768),(gpu,-1,256)):
                if isinstance(value,bool) or not isinstance(value,int) or not minimum <= value <= maximum:
                    raise ValueError('Контекст: 512–32768; GPU-слои: -1–256 (0 = CPU)')
            self.cancelled = cancelled = threading.Event()
            self.state, self.error = 'starting', ''
            self.runtime.runtime_path = str(executable)
            local_model = LocalModel(str(model),model.stem,model.stat().st_size)

            def launch():
                try:
                    self.runtime.start(local_model,ctx_size=ctx,gpu_layers=gpu,cancelled=cancelled)
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
                    'logs':''.join(self.runtime.logs)[-4000:]}

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
