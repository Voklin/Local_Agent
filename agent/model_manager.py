"""Local GGUF model discovery and llama.cpp runtime management for v5.8.

The agent core talks to every model through an OpenAI-compatible endpoint.  This
module owns only local-model lifecycle; it does not know anything about tools,
sandbox permissions or task execution.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import threading
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from .process_job import ProcessJob


APP_DIR = Path(os.getenv("LOCALAPPDATA", Path.home() / ".local")) / "LocalCodingAgent"
DEFAULT_MODELS_DIR = APP_DIR / "models"
DEFAULT_RUNTIME_DIR = APP_DIR / "runtime"


@dataclass
class LocalModel:
    path: str
    name: str
    size_bytes: int
    quantization: str = "unknown"
    architecture: str = "unknown"

    @property
    def size_gb(self) -> float:
        return self.size_bytes / (1024 ** 3)

    def to_dict(self):
        data = asdict(self)
        data["size_gb"] = round(self.size_gb, 2)
        return data


class ModelManager:
    def __init__(self, models_dir: str | Path | None = None):
        self.models_dir = Path(models_dir or DEFAULT_MODELS_DIR).expanduser()
        self.models_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _quantization(name: str) -> str:
        match = re.search(r"(?:^|[-_.])(Q[0-9](?:_[A-Z0-9]+)?(?:_[A-Z0-9]+)?)(?:[-_.]|$)", name.upper())
        return match.group(1) if match else "unknown"

    def scan(self) -> list[LocalModel]:
        result: list[LocalModel] = []
        for path in sorted(self.models_dir.rglob("*.gguf"), key=lambda p: p.name.lower()):
            try:
                result.append(LocalModel(str(path), path.stem, path.stat().st_size, self._quantization(path.name)))
            except OSError:
                continue
        return result

    def import_model(self, source: str | Path, *, copy=True) -> LocalModel:
        source = Path(source).expanduser().resolve()
        if source.suffix.lower() != ".gguf" or not source.is_file():
            raise ValueError("Выберите существующий файл GGUF.")
        destination = self.models_dir / source.name
        if source != destination:
            if copy:
                shutil.copy2(source, destination)
            else:
                destination = source
        return LocalModel(str(destination), destination.stem, destination.stat().st_size, self._quantization(destination.name))


class LocalRuntime:
    """Starts llama-server and exposes its OpenAI-compatible endpoint."""
    def __init__(self, *, runtime_path: str | Path | None = None):
        self.runtime_path = str(runtime_path or "")
        self.process: subprocess.Popen | None = None
        self.port: int | None = None
        self.model: LocalModel | None = None
        self.logs: list[str] = []
        self.log_reader = None
        self.process_job = None
        self.process_lock = threading.RLock()

    @staticmethod
    def find_executable(explicit: str = "") -> str | None:
        candidates = []
        if explicit:
            candidates.append(Path(explicit))
        candidates.extend([
            DEFAULT_RUNTIME_DIR / "llama-server.exe",
            DEFAULT_RUNTIME_DIR / "llama-server",
            Path("llama-server.exe"),
            Path("llama-server"),
        ])
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
        return shutil.which("llama-server") or shutil.which("llama-server.exe")

    @staticmethod
    def free_port(host="127.0.0.1") -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, 0))
            return int(sock.getsockname()[1])

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/v1" if self.port else ""

    def start(self, model: LocalModel, *, ctx_size=32768, gpu_layers=-1, port=None, extra_args=None, cancelled=None, timeout=120):
        if self.running:
            raise RuntimeError("Сначала остановите собственный сервер")
        executable = self.find_executable(self.runtime_path)
        if not executable:
            raise FileNotFoundError("llama-server не найден. Выберите установленный llama-server.exe.")
        cancelled = cancelled or threading.Event()
        if cancelled.is_set():
            raise InterruptedError("Запуск отменён")
        self.port = int(port or self.free_port())
        args = [executable, "--model", model.path, "--host", "127.0.0.1", "--port", str(self.port),
                "--ctx-size", str(int(ctx_size)), "--n-gpu-layers", str(int(gpu_layers)), "--jinja"]
        if extra_args:
            args.extend(extra_args)
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
        with self.process_lock:
            self.logs.clear()
            process = self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=creationflags)
            try:
                self.process_job = ProcessJob(process)
            except Exception:
                process.kill()
                process.wait(timeout=3)
                if process.stdout:
                    process.stdout.close()
                self.process = None
                self.port = None
                raise
            self.model = model
        self.log_reader = threading.Thread(target=self._drain_output, args=(process,), daemon=True, name='llama-output')
        self.log_reader.start()
        ready = False
        try:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if cancelled.is_set():
                    raise InterruptedError("Запуск отменён")
                if process.poll() is not None:
                    self.log_reader.join(timeout=1)
                    raise RuntimeError(f"llama-server завершился с кодом {process.returncode}.\n{''.join(self.logs)[-4000:]}")
                if self._healthy() and process.poll() is None and not cancelled.is_set():
                    ready = True
                    return self.base_url
                cancelled.wait(0.2)
            raise TimeoutError(f"API llama-server не стал доступен за {timeout} секунд")
        finally:
            if not ready:
                self.stop()

    def _drain_output(self, process):
        try:
            while process.stdout:
                chunk = process.stdout.read(1024)
                if not chunk:
                    break
                with self.process_lock:
                    self.logs.append(chunk.decode('utf-8', errors='replace'))
                    del self.logs[:-100]
        except (OSError, ValueError):
            pass

    def _healthy(self) -> bool:
        if not self.base_url:
            return False
        try:
            with urllib.request.urlopen(self.base_url.removesuffix("/v1") + "/health", timeout=0.5) as response:
                return 200 <= response.status < 300
        except (OSError, urllib.error.URLError):
            return False

    def stop(self):
        with self.process_lock:
            process, self.process = self.process, None
        if process is not None:
            try:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=3)
            finally:
                if self.process_job:
                    self.process_job.close()
                    self.process_job = None
                if self.log_reader and self.log_reader is not threading.current_thread():
                    self.log_reader.join(timeout=1)
                if process.stdout:
                    process.stdout.close()
        self.port = None
        self.model = None

    def status(self) -> dict:
        with self.process_lock:
            return {
                "running": self.running,
                "pid": self.process.pid if self.running else None,
                "port": self.port,
                "base_url": self.base_url,
                "model": self.model.to_dict() if self.model else None,
            }

    def __del__(self):
        try:
            self.stop()
        except Exception:
            pass
