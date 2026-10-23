"""JSON-lines bridge for the Electron shell. File access is confined to the selected project."""
from __future__ import annotations
import json
import os
import sys
import threading
from pathlib import Path

for stream in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8')

if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core.python.task_service import TaskService
from core.python.editor_service import EditorService
from core.python.project_search import ProjectSearchService
from core.python.runtime_service import RuntimeService
from core.python.memory_service import read_memory, write_memory
from core.python.speech_service import SpeechService
from core.python.neural_speech import NeuralSpeech
from core.python.telegram_service import TelegramService
from core.python.desktop_service import DesktopService
from core.python.transcription_service import TranscriptionService

output_lock = threading.Lock()

def emit(message):
    with output_lock:
        sys.stdout.write(json.dumps(message, ensure_ascii=False) + '\n')
        sys.stdout.flush()
    observer=globals().get('telegram')
    if observer:observer.observe(message)

tasks = TaskService(emit)
editor = EditorService()
project_search = ProjectSearchService()
runtime = RuntimeService()
speech = SpeechService()
neural_speech = NeuralSpeech(emit)
transcription = TranscriptionService()
desktop = DesktopService(emit)
tasks.desktop = desktop

MAX_READ_BYTES = 1_000_000
MAX_ENTRIES = 1000
project_root: Path | None = None

def resolve_inside(relative: str) -> Path:
    if project_root is None:
        raise ValueError('Сначала выберите папку проекта')
    candidate = (project_root / relative).resolve()
    try:
        candidate.relative_to(project_root)
    except ValueError:
        raise PermissionError('Доступ за пределами выбранного проекта запрещён')
    return candidate

def handle(method: str, params: dict) -> dict:
    with tasks.lock:
        return _handle(method,params)

def _handle(method: str, params: dict) -> dict:
    global project_root
    if method == 'telegram_status':
        return telegram.status()
    if method == 'telegram_start':
        return telegram.start(params)
    if method == 'telegram_stop':
        return telegram.stop()
    if method == 'desktop_result':
        return desktop.respond(params)
    if method == 'desktop_settings':
        return {'ok':True,'enabled':desktop.enabled}
    if method == 'configure_desktop':
        tasks.idle()
        return desktop.configure(params)
    if method == 'move_chat_mode':
        return tasks.move_chat(params)
    if method == 'discard_handoff':
        return tasks.discard_handoff(params)
    if method == 'prepare_handoff':
        return tasks.prepare_handoff(project_root,params)
    if method == 'get_companion_settings':
        return tasks.companion_preferences()
    if method == 'configure_companion':
        return tasks.configure_companion(params)
    if method == 'cancel_transcription':
        return transcription.stop()
    if method == 'voice_status':
        return neural_speech.status() if tasks.companion_config['tts_provider']=='qwen3' else speech.status()
    if method == 'voice_refresh':
        return neural_speech.status() if tasks.companion_config['tts_provider']=='qwen3' else speech.refresh()
    if method == 'voice_speak':
        return neural_speech.speak(params,tasks.companion_config) if tasks.companion_config['tts_provider']=='qwen3' else speech.speak(params)
    if method == 'voice_playback':
        return neural_speech.playback(params)
    if method == 'voice_stop':
        neural_speech.stop()
        speech.stop()
        return neural_speech.status() if tasks.companion_config['tts_provider']=='qwen3' else speech.status()
    if method in ('runtime_start', 'runtime_stop'):
        tasks.idle()
        return runtime.start(params) if method == 'runtime_start' else runtime.stop()
    if method == 'runtime_status':
        return runtime.status()
    if method == 'health':
        return {'ok': True, 'service': 'python-core-bridge', 'protocol': 1, 'project': str(project_root) if project_root else None}
    if method == 'set_project':
        tasks.idle()
        root = Path(str(params.get('root', ''))).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Выбранный путь не является папкой')
        project_search.cancel()
        project_root = root
        editor.clear()
        tasks.chat = None
        return {'ok': True, 'root': str(root), 'name': root.name}
    if method in ('editor_read', 'editor_preview', 'editor_resolve'):
        if project_root is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'editor_read':
            return editor.read(project_root, str(params.get('path', '')))
        tasks.idle()
        if method == 'editor_preview':
            return editor.preview(project_root, params)
        return editor.resolve(project_root, params)
    if method in ('get_project_memory','save_project_memory'):
        if project_root is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'get_project_memory':
            return read_memory(project_root)
        tasks.idle()
        return write_memory(project_root,params)
    if method == 'configure_model':
        return tasks.configure(params)
    if method == 'get_model_settings':
        return tasks.preferences()
    if method == 'list_models':
        return tasks.models(tasks.diagnostic_config(params or None))
    if method == 'cancel_model_setup':
        return tasks.cancel_model_setup()
    if method in ('list_chats', 'new_chat', 'load_chat', 'rename_chat', 'start_task'):
        mode = params.get('mode', 'ide')
        if mode not in ('chat', 'ide', 'voice'):
            raise ValueError('Неизвестный режим работы')
        scope = '' if mode in ('chat','voice') else project_root
        if scope is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'rename_chat':
            return tasks.rename(scope,params)
        if method == 'list_chats':
            return tasks.chats(scope, mode)
        if method in ('new_chat', 'load_chat'):
            return tasks.select_chat(scope, params.get('chat_id') if method == 'load_chat' else None, mode)
        if editor.pending:
            raise ValueError('Сначала завершите подтверждение изменения в редакторе')
        return tasks.start(scope, params)
    if method == 'cancel_project_search':
        return project_search.cancel()
    if method == 'cancel_task':
        return tasks.cancel()
    if method == 'resolve_approval':
        return tasks.resolve_approval(params)
    if method == 'list_files':
        rel = str(params.get('path', '.'))
        target = resolve_inside(rel)
        if not target.is_dir():
            raise ValueError('Путь не является папкой')
        items = []
        for p in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name.casefold()))[:MAX_ENTRIES]:
            # Resolve each entry as well: do not expose symlinks that escape the project root.
            try:
                safe = p.resolve()
                safe.relative_to(project_root)
            except (ValueError, OSError):
                continue
            if p.name in {'.git', '__pycache__', 'node_modules', '.venv'}:
                continue
            items.append({'name': p.name, 'path': str(p.relative_to(project_root)), 'kind': 'directory' if p.is_dir() else 'file'})
        return {'ok': True, 'items': items, 'truncated': len(items) >= MAX_ENTRIES}
    if method == 'read_file':
        target = resolve_inside(str(params.get('path', '')))
        if not target.is_file():
            raise ValueError('Файл не найден')
        if target.stat().st_size > MAX_READ_BYTES:
            raise ValueError(f'Файл превышает лимит {MAX_READ_BYTES} байт')
        try:
            content = target.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = target.read_text(encoding='utf-8', errors='replace')
        return {'ok': True, 'content': content, 'path': str(target.relative_to(project_root))}
    # No direct write or shell API: writes go through the engine approval protocol.
    raise ValueError(f'Неизвестный или пока не подключённый метод: {method}')

telegram = TelegramService(tasks, lambda:project_root, emit, lambda params:handle('start_task',params))

def main() -> None:
    for line in sys.stdin:
        req_id = None
        try:
            req = json.loads(line)
            if not isinstance(req, dict) or not isinstance(req.get('params', {}), dict):
                raise ValueError('Ожидается JSON-объект запроса и параметров')
            req_id = req.get('id')
            method = str(req.get('method', ''))
            if method == 'transcribe':
                transcription.start(req.get('params') or {}, dict(tasks.companion_config), lambda result, request_id=req_id: emit({'id':request_id, **result}))
                continue
            if method == 'list_models':
                tasks.start_model_discovery(lambda result, request_id=req_id: emit({'id': request_id, **result}), req.get('params') or None)
                continue
            if method == 'test_model':
                tasks.start_model_probe(req.get('params') or None, lambda result, request_id=req_id: emit({'id': request_id, **result}))
                continue
            if method == 'search_project':
                if project_root is None:
                    raise ValueError('Сначала выберите папку проекта')
                project_search.start(project_root, req.get('params') or {}, lambda result, request_id=req_id: emit({'id': request_id, **result}))
                continue
            result = handle(method, req.get('params') or {})
            response = {'id': req_id, **result}
        except Exception as exc:
            response = {'id': req_id, 'ok': False, 'error': str(exc)[:500]}
        emit(response)
    telegram.shutdown()
    project_search.cancel()
    speech.stop()
    runtime.stop()
    tasks.cancel()
    project_search.shutdown()
    transcription.shutdown()
    speech.shutdown()
    neural_speech.shutdown()
    runtime.shutdown()
    tasks.shutdown()

if __name__ == '__main__':
    main()
