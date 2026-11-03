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
from core.python.protocol import PROTOCOL_VERSION, validate_request
from agent.capability_profiles import MODE_GROUPS
from agent.companion_policy import clean_speech_text
from core.python.editor_service import EditorService
from core.python.project_search import ProjectSearchService
from core.python.runtime_service import RuntimeService
from core.python.memory_service import read_memory, write_memory, memory_action
from core.python.speech_service import SpeechService
from core.python.neural_speech import NeuralSpeech
from core.python.telegram_service import TelegramService
from core.python.desktop_service import DesktopService
from core.python.transcription_service import TranscriptionService
from core.python.background_job import BackgroundJob
from core.python.ide_sessions import IdeSessions,IDE_ROOT
from agent.project_index import get_index,close_indexes

output_lock = threading.Lock()

def emit(message):
    message={**message,'protocol_version':PROTOCOL_VERSION}
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
storage_jobs=BackgroundJob()
completion_jobs=BackgroundJob()

MAX_READ_BYTES = 1_000_000
MAX_ENTRIES = 1000
project_root: Path | None = None
ide_sessions=IdeSessions(tasks,emit)

def current_root():
    return IDE_ROOT.get() or project_root

def resolve_inside(relative: str) -> Path:
    project_root=current_root()
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
    workspace_root=current_root()
    if method=='ide_workspace_changed':
        return {'ok':True,'task':tasks.workspace_changed(workspace_root)}
    if method=='project_index':
        if workspace_root is None:raise ValueError('Сначала выберите папку проекта')
        index=get_index(workspace_root,create=True);action=params.get('action','status')
        if action not in ('status','rebuild','cancel'):raise ValueError('Неизвестная операция индекса')
        return getattr(index,action)()
    if method in ('workspace_access','workspace_access_configure'):
        if workspace_root is None:raise ValueError('Сначала выберите папку проекта')
        from agent.workspace_access import WorkspaceAccessPolicy
        policy=WorkspaceAccessPolicy(workspace_root)
        if method=='workspace_access':return policy.catalog()
        tasks.idle()
        result=policy.configure(params.get('paths'),params.get('confirmed'))
        index=get_index(workspace_root)
        if index:index.cancel_build.set();index.uncertain('Разрешения модели изменились; пересоберите индекс',purge=True)
        return result
    if method=='optional_settings':return tasks.optional.catalog()
    if method=='optional_configure':return tasks.optional.configure(params.get('settings'))
    if method=='optional_cancel':return tasks.optional.cancel()
    if method=='session_status':return {'ok':True,'inference':tasks.scheduler.status(),'mcp':tasks.extensions.mcp.pool.status(),'profiles':MODE_GROUPS}
    if method=='update_task_plan':return tasks.update_plan(params)
    if method=='active_runs':return {'ok':True,'runs':[r for r in tasks.active_runs() if IDE_ROOT.get() is None or (tasks.runs.get(r['chat_id']) and tasks.runs[r['chat_id']].chat.get('project_root')==str(workspace_root))]}
    if method=='run_history':
        chat=tasks.chat
        if not chat or params.get('chat_id')!=chat['id']:raise ValueError('Выберите чат для истории запусков')
        return {'ok':True,'runs':tasks.registry.history(chat['id'])}
    if method in ('snapshot_list','snapshot_preview','snapshot_apply','snapshot_review'):
        return getattr(tasks.workspace_review,method.removeprefix('snapshot_'))(workspace_root,params)
    if method=='storage_cancel':return storage_jobs.cancel()
    if method=='storage_status':
        from agent import chat_store
        tasks.idle()
        database=chat_store._database()
        return {'ok':True,'report':database.report()}
    if method == 'connections_list':
        return {'ok':True,'profiles':tasks.connections.list()}
    if method == 'connections_save':
        tasks.idle()
        return {'ok':True,'profile':tasks.connections.save(params)}
    if method == 'connections_delete':
        tasks.idle();tasks.connections.remove(params.get('id'))
        return {'ok':True}
    if method == 'extensions_list':
        return tasks.extensions.catalog()
    if method == 'extensions_configure':
        tasks.idle()
        return tasks.extensions.configure(params)
    if method == 'extensions_import':
        tasks.idle()
        return tasks.extensions.import_plugin(params.get('manifest'))
    if method == 'mcp_discover':
        return tasks.extensions.discover_server(str(params.get('id','')))
    if method == 'mcp_cancel_discovery':
        return tasks.extensions.cancel_discovery(str(params['id']) if params.get('id') else None)
    if method == 'workspace_list':
        return {'ok':True,'projects':tasks.projects.list(),'selected':tasks.project_id}
    if method == 'workspace_save':
        tasks.idle()
        return {'ok':True,'project':tasks.projects.save(params)}
    if method == 'workspace_select':
        tasks.idle()
        project=tasks.projects.get(params.get('id',''))
        root=Path(project['root']).resolve(strict=True) if project.get('root') else None
        if root and not root.is_dir():raise ValueError('Папка проекта недоступна')
        project_search.cancel();editor.clear();tasks.chat=None;tasks.project_id=project['id'];project_root=root
        close_indexes()
        if root:get_index(root,create=True)
        return {'ok':True,'project':project,'root':str(root) if root else '', 'name':project['name']}
    if method == 'workspace_delete':
        tasks.idle()
        if params.get('confirmed') is not True:raise ValueError('Подтвердите удаление проекта из списка')
        identity=params.get('id');tasks.projects.get(identity)
        tasks.projects.remove(identity)
        if tasks.project_id==identity:tasks.project_id='';tasks.chat=None
        return {'ok':True}
    if method in ('chat_update','chat_delete','chat_fork','chat_export','chat_search'):
        mode=params.get('mode','chat')
        if mode not in ('chat','ide','voice'):raise ValueError('Неизвестный режим')
        scope=workspace_root if mode=='ide' else ''
        if scope is None:raise ValueError('Сначала откройте папку')
        action={'chat_update':'update','chat_delete':'delete','chat_fork':'fork','chat_export':'export','chat_search':'search'}[method]
        return getattr(tasks.conversations,action)(scope,params)
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
        return tasks.prepare_handoff(workspace_root,params)
    if method == 'get_companion_settings':
        return tasks.companion_preferences()
    if method == 'configure_companion':
        return tasks.configure_companion(params)
    if method == 'cancel_transcription':
        return transcription.stop()
    if method == 'voice_status':
        return neural_speech.status(tasks.companion_config['tts_provider']) if tasks.companion_config['tts_provider'] in ('qwen3','piper') else speech.status()
    if method == 'voice_refresh':
        return neural_speech.status(tasks.companion_config['tts_provider']) if tasks.companion_config['tts_provider'] in ('qwen3','piper') else speech.refresh()
    if method == 'voice_speak':
        params={**params,'text':clean_speech_text(params.get('text',''))}
        return neural_speech.speak(params,tasks.companion_config) if tasks.companion_config['tts_provider'] in ('qwen3','piper') else speech.speak(params)
    if method == 'voice_playback':
        return neural_speech.playback(params)
    if method == 'voice_stop':
        neural_speech.stop()
        speech.stop()
        return neural_speech.status(tasks.companion_config['tts_provider']) if tasks.companion_config['tts_provider'] in ('qwen3','piper') else speech.status()
    if method in ('runtime_start', 'runtime_stop'):
        tasks.idle()
        return runtime.start(params) if method == 'runtime_start' else runtime.stop()
    if method == 'runtime_status':
        return runtime.status()
    if method == 'health':
        return {'ok': True, 'service': 'python-core-bridge', 'protocol': 1, 'project': str(workspace_root) if workspace_root else None,**({'chat_id':(tasks.chat or {}).get('id'),'project_id':tasks.project_id} if IDE_ROOT.get() else {})}
    if method == 'set_project':
        tasks.idle()
        root = Path(str(params.get('root', ''))).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Выбранный путь не является папкой')
        project_search.cancel()
        project_root = root
        close_indexes();get_index(root,create=True)
        editor.clear()
        tasks.chat = None
        return {'ok': True, 'root': str(root), 'name': root.name}
    if method in ('editor_read', 'editor_preview', 'editor_resolve'):
        if workspace_root is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'editor_read':
            return editor.read(workspace_root, str(params.get('path', '')))
        tasks.idle()
        if method == 'editor_preview':
            return editor.preview(workspace_root, params)
        result=editor.resolve(workspace_root, params)
        if result.get('applied'):result={**result,'task':tasks.workspace_changed(workspace_root)}
        return result
    if method in ('get_project_memory','save_project_memory','project_memory_action'):
        if workspace_root is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'get_project_memory':
            return read_memory(workspace_root)
        tasks.idle()
        if method=='project_memory_action':return memory_action(workspace_root,params)
        return write_memory(workspace_root,params)
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
        scope = '' if mode in ('chat','voice') else workspace_root
        if scope is None:
            raise ValueError('Сначала выберите папку проекта')
        if method == 'rename_chat':
            return tasks.rename(scope,params)
        if method == 'list_chats':
            return tasks.chats(scope, mode)
        if method in ('new_chat', 'load_chat'):
            result=tasks.select_chat(scope, params.get('chat_id') if method == 'load_chat' else None, mode)
            if IDE_ROOT.get():result['active_runs']=[r for r in result.get('active_runs',[]) if tasks.runs.get(r['chat_id']) and tasks.runs[r['chat_id']].chat.get('project_root')==str(scope)]
            return result
        if editor.pending:
            raise ValueError('Сначала завершите подтверждение изменения в редакторе')
        return tasks.start(scope, params)
    if method == 'cancel_project_search':
        return project_search.cancel()
    if method == 'cancel_task':
        return tasks.cancel(params)
    if method == 'resolve_approval':
        return tasks.resolve_approval(params)
    if method == 'resolve_tool_recovery':
        return tasks.resolve_tool_recovery(params)
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
                safe.relative_to(workspace_root)
            except (ValueError, OSError):
                continue
            if p.name in {'.git', '__pycache__', 'node_modules', '.venv'}:
                continue
            items.append({'name': p.name, 'path': p.relative_to(workspace_root).as_posix(), 'kind': 'directory' if p.is_dir() else 'file'})
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
        return {'ok': True, 'content': content, 'path': target.relative_to(workspace_root).as_posix()}
    # No direct write or shell API: writes go through the engine approval protocol.
    raise ValueError(f'Неизвестный или пока не подключённый метод: {method}')

telegram = TelegramService(tasks, current_root, emit, lambda params:handle('start_task',params),ide_sessions.control)

def main() -> None:
    for line in sys.stdin:
        req_id = None
        ide_context=None
        try:
            req = json.loads(line)
            req_id = req.get('id') if isinstance(req,dict) else None
            method,params=validate_request(req)
            if method=='ide_attach':
                emit({'id':req_id,**ide_sessions.attach(params.get('root',''))});continue
            if method=='ide_detach':
                emit({'id':req_id,**ide_sessions.detach(params.get('session_id'))});continue
            if method=='ide_editor_result':
                emit({'id':req_id,**ide_sessions.complete(params)});continue
            if method=='ide_call':
                method,params=validate_request({'method':params.get('method'),'params':params.get('params',{})})
                if params.get('mode','ide')!='ide':raise ValueError('IDE не может обращаться к Chat или Лоле')
                ide_context=ide_sessions.scope(req['params'].get('session_id'),method)
                ide_context.__enter__()
                req={**req,'method':method,'params':params}
            request_root=current_root()
            if method=='ide_complete':
                if request_root is None:raise ValueError('Откройте папку в IDE')
                from core.python.ide_completion import complete
                config=tasks.diagnostic_config()
                completion_jobs.start(lambda ctx,root=request_root,cfg=config,args=dict(params):complete(root,cfg,args,ctx),lambda result,request_id=req_id:emit({'id':request_id,**result}),timeout=30)
                continue
            if method in ('storage_backup','storage_status'):
                with tasks.lock:tasks.idle()
                def maintain(context,operation=method,arguments=dict(params)):
                    from agent import chat_store
                    database=chat_store._database()
                    return database.backup(arguments.get('path',''),cancelled=context) if operation=='storage_backup' else {'report':database.report()}
                storage_jobs.start(maintain,lambda result,request_id=req_id:emit({'id':request_id,**result}))
                continue
            if method=='snapshot_checkpoint':
                if request_root is None:raise ValueError('Выберите проект')
                tasks.workspace_review.start_checkpoint(request_root,params,lambda result,request_id=req_id:emit({'id':request_id,**result}))
                continue
            if method=='snapshot_checkpoint_cancel':
                emit({'id':req_id,**tasks.workspace_review.checkpoint_job.cancel()});continue
            if method == 'optional_run':
                if request_root is None:raise ValueError('Сначала выберите папку проекта')
                tasks.optional.start(request_root,params,lambda result,request_id=req_id:emit({'id':request_id,**result}))
                continue
            if method == 'mcp_discover':
                tasks.extensions.start_discovery(str((req.get('params') or {}).get('id','')),
                    lambda result,request_id=req_id:emit({'id':request_id,**result}))
                continue
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
                if request_root is None:
                    raise ValueError('Сначала выберите папку проекта')
                project_search.start(request_root, req.get('params') or {}, lambda result, request_id=req_id: emit({'id': request_id, **result}))
                continue
            result = handle(method, req.get('params') or {})
            response = {'id': req_id, **result}
        except Exception as exc:
            response = {'id': req_id, 'ok': False, 'error': str(exc)[:500]}
        finally:
            if ide_context:ide_context.__exit__(None,None,None)
        emit(response)
    completion_jobs.shutdown()
    storage_jobs.shutdown()
    telegram.shutdown()
    tasks.workspace_review.shutdown()
    tasks.extensions.shutdown()
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
    close_indexes()

if __name__ == '__main__':
    main()
