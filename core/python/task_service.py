"""Threaded agent service. Only the main bridge thread accepts UI commands."""
from __future__ import annotations
from copy import deepcopy
import json
import threading
import time
import uuid
from pathlib import Path

from agent.engine import AgentEngine
from agent.chat_store import create_chat, read_chat_catalog, load_chat, save_chat, STORE_LOCK
from agent.project_memory import load_project_memory
from agent.task_store import clear_task, load_task, save_task
from agent.model_preferences import load_preferences, save_preferences, validate_preferences
from agent.model_discovery import discover_models
from agent.model_probe import probe_model
from agent.task_activity import recover_tools


class TaskService:
    def __init__(self, emit, engine_factory=AgentEngine):
        self.emit = emit
        self.engine_factory = engine_factory
        self.lock = threading.RLock()
        self.thread = None
        self.task_running = False
        self.engine = None
        self.approval = None
        self.chat = None
        self.run_id = None
        self.config = {**load_preferences(), 'api_key': ''}
        self.stream_turn = None
        self.stream_buffer = ''
        self.last_stream_emit = 0
        self.stream_timer = None
        self.probe_thread = None
        self.probe_cancel = threading.Event()
        self.discovery_thread = None
        self.discovery_cancel = threading.Event()
        self.stream_text = ''
        self.stream_persist_at = 0
        self.draft_timer = None

    def idle(self):
        with self.lock:
            if self.task_running:
                raise ValueError('Сначала остановите текущую задачу и дождитесь завершения')

    def configure(self, params):
        self.idle()
        preferences = save_preferences(params)
        self.config = {**preferences,
                       'api_key': str(params.get('api_key', ''))[:4000]}
        # Keys stay in process memory, never in bridge responses or persisted chats.
        return {'ok': True, **preferences}

    def preferences(self):
        return {'ok': True, 'base_url': self.config['base_url'], 'model': self.config['model'],
                'settings': deepcopy(self.config['settings'])}

    def models(self, config=None, cancelled=None):
        return discover_models(dict(config if config is not None else self.config), cancelled=cancelled)

    def diagnostic_config(self, params=None):
        if params is None:
            return deepcopy(self.config)
        return {**validate_preferences(params), 'api_key': str(params.get('api_key', ''))[:4000]}

    def start_model_probe(self, params, respond):
        self.idle()
        with self.lock:
            if self.probe_thread and self.probe_thread.is_alive():
                raise ValueError('Проверка модели уже выполняется')
            config = self.diagnostic_config(params)
            self.probe_cancel = cancelled = threading.Event()
            def run_probe():
                try:
                    response = probe_model(config, cancelled=cancelled)
                except Exception as exc:
                    response = {'ok': False, 'error': str(exc)[:500]}
                respond(response)
            self.probe_thread = threading.Thread(target=run_probe, daemon=True, name='model-probe')
            self.probe_thread.start()

    def cancel_model_setup(self):
        self.discovery_cancel.set()
        self.probe_cancel.set()
        return {'ok': True}

    def start_model_discovery(self, respond, params=None):
        with self.lock:
            if self.discovery_thread and self.discovery_thread.is_alive():
                raise ValueError('Загрузка списка моделей уже выполняется')
            config = self.diagnostic_config(params)
            self.discovery_cancel = cancelled = threading.Event()

            def run_discovery():
                try:
                    response = self.models(config, cancelled)
                except Exception as exc:
                    response = {'ok': False, 'error': str(exc)[:500]}
                respond(response)

            self.discovery_thread = threading.Thread(target=run_discovery, daemon=True, name='model-discovery')
            self.discovery_thread.start()

    def chats(self, root):
        catalog = read_chat_catalog()
        return {'ok': True, 'chats': [c for c in catalog['chats'] if c.get('project_root') == str(root)],
                'warnings': catalog['warnings']}

    def rename(self, root, params):
        self.idle()
        title=params.get('title')
        if not isinstance(title,str) or not title.strip() or len(title)>120 or '\x00' in title:
            raise ValueError('Название чата: от 1 до 120 символов без NUL')
        with self.lock, STORE_LOCK:
            chat=load_chat(params.get('chat_id'))
            if not chat or chat.get('project_root')!=str(root):
                raise ValueError('Чат не принадлежит выбранной области')
            chat['title']=' '.join(title.split())
            warning=save_chat(chat)
            if self.chat and self.chat['id']==chat['id']:
                self.chat['title']=chat['title']
            return {'ok':True,'title':chat['title'],'warnings':[warning] if warning else []}

    def select_chat(self, root, chat_id=None):
        self.idle()
        if chat_id:
            if not isinstance(chat_id, str) or len(chat_id) != 32 or any(c not in '0123456789abcdef' for c in chat_id):
                raise ValueError('Некорректный идентификатор чата')
            chat = load_chat(chat_id)
            if not chat or chat.get('project_root') != str(root):
                raise ValueError('Чат не принадлежит выбранному проекту')
        else:
            chat = create_chat(str(root), self.config['model'])
        self.chat = chat
        warnings = [chat.pop('storage_warning')] if chat.get('storage_warning') else []
        task, recovered = self._recover_chat()
        return {'ok': True, 'chat': chat, 'task': task, 'warnings': warnings + recovered}

    def _recover_chat(self):
        embedded = self.chat.get('task_checkpoint')
        task = deepcopy(embedded) if isinstance(embedded, dict) else load_task(self.chat['id'])
        if task and (task.get('chat_id') != self.chat['id'] or task.get('project_root') != self.chat['project_root']):
            raise ValueError('Контрольная точка не соответствует чату и проекту; исходные данные сохранены')
        warnings = []
        draft = self.chat.pop('stream_draft', None)
        dirty = draft is not None or (task is not None and embedded is None)
        if isinstance(draft, dict) and isinstance(draft.get('text'), str) and draft['text']:
            if draft.get('run_id') == self.chat.get('active_run_id'):
                message = {'role': 'assistant', 'content': draft['text']}
                if not self.chat['messages'] or self.chat['messages'][-1] != message:
                    self.chat['messages'].append(message)
                warnings.append('Восстановлен последний сохранённый фрагмент ответа после прерывания процесса.')
            else:
                self.chat.setdefault('recovery_fragments', []).append(draft)
                warnings.append('Фрагмент другого запуска сохранён в recovery_fragments; он не добавлен к текущему диалогу автоматически.')
        elif draft is not None:
            self.chat.setdefault('recovery_fragments', []).append(draft)
            warnings.append('Не удалось автоматически восстановить фрагмент потока; исходные данные сохранены в recovery_fragments.')
        if task and (task.get('status') == 'running' or task.get('pending_write')):
            task['status'] = 'paused'
            task['last_event'] = 'Предыдущий процесс завершился; задачу можно продолжить'
            pending = task.pop('pending_write', None)
            if isinstance(pending, dict):
                result = None
                index = pending.get('message_index')
                messages = self.chat['messages']
                if isinstance(index, int) and 0 <= index < len(messages):
                    anchor = messages[index]
                    if anchor.get('role') == 'assistant' and any(c.get('id') == pending.get('call_id') for c in anchor.get('tool_calls', []) if isinstance(c, dict)):
                        for message in messages[index + 1:]:
                            if message.get('role') != 'tool':
                                break
                            if message.get('tool_call_id') == pending.get('call_id'):
                                result = message
                                break
                if result:
                    try:
                        value = json.loads(result['content'])
                        if value.get('ok') and pending.get('path') not in task.setdefault('modified_files', []):
                            task['modified_files'].append(pending['path'])
                    except (ValueError, KeyError, TypeError, AttributeError):
                        result = None
                if not result and pending.get('status') == 'applying':
                    task['recovery_warning'] = f"Последняя запись {pending.get('path', '')} могла быть применена до сбоя. Проверьте файл перед продолжением; старое согласие сброшено."
                    task.setdefault('resume_state', {})['next_action'] = task['recovery_warning']
                elif not result:
                    warnings.append('Прерванное подтверждение сброшено; новые изменения потребуют нового diff и согласия.')
            if task.get('recovery_warning'):
                task['last_event'] = task['recovery_warning']
            dirty = True
        if task and task.get('recovery_warning'):
            warnings.append(task['recovery_warning'])
        if task and recover_tools(task, self.chat['messages']):
            dirty = True
        if task:
            self.chat['task_checkpoint'] = deepcopy(task)
        if dirty:
            warning = save_chat(self.chat)
            if warning:
                warnings.append(warning)
        if task:
            try:
                save_task(task)
            except OSError:
                warnings.append('Контрольная точка сохранена в чате, но её отдельная копия недоступна; проверьте доступ к каталогу данных.')
        return task, warnings

    def _persist_chat(self):
        warning = save_chat(self.chat)
        if warning:
            self._event('warning', text=warning)

    def _task_event(self, task):
        with self.lock:
            self.chat['task_checkpoint'] = deepcopy(task)
            self._persist_chat()
            self._event('task', task=task)

    def _event(self, kind, **data):
        self.emit({'event': kind, 'run_id': self.run_id, 'chat_id': self.chat['id'], **data})

    def _flush_text(self):
        if self.stream_timer:
            self.stream_timer.cancel()
            self.stream_timer = None
        if self.stream_buffer:
            self._event('text_delta', message_id=f'{self.run_id}:{self.stream_turn}', text=self.stream_buffer)
            self.stream_buffer = ''
            self.last_stream_emit = time.monotonic()

    def _flush_scheduled(self, run_id):
        with self.lock:
            if self.run_id == run_id:
                self._flush_text()

    def _persist_draft(self):
        self.chat['stream_draft'] = {'run_id': self.run_id, 'turn': self.stream_turn, 'text': self.stream_text}
        self._persist_chat()
        self.stream_persist_at = time.monotonic()

    def _persist_draft_scheduled(self, run_id, turn):
        with self.lock:
            if self.run_id != run_id or self.stream_turn != turn or not self.stream_text:
                return
            self.draft_timer = None
            try:
                self._persist_draft()
            except Exception as exc:
                self._event('failed', text=f'Не удалось сохранить потоковый ответ: {type(exc).__name__}: {exc}')
                self.cancel()

    def _text_delta(self, turn, text):
        with self.lock:
            if self.stream_turn != turn:
                self._flush_text()
                if self.draft_timer:
                    self.draft_timer.cancel()
                    self.draft_timer = None
                self.stream_turn = turn
                self.stream_text = ''
                self.stream_persist_at = 0
            self.stream_buffer += text
            self.stream_text += text
            if time.monotonic() - self.stream_persist_at >= 1:
                if self.draft_timer:
                    self.draft_timer.cancel()
                    self.draft_timer = None
                self._persist_draft()
            elif self.draft_timer is None:
                self.draft_timer = threading.Timer(max(0.01, 1 - (time.monotonic() - self.stream_persist_at)),
                                                  self._persist_draft_scheduled, (self.run_id, turn))
                self.draft_timer.daemon = True
                self.draft_timer.start()
            elapsed = time.monotonic() - self.last_stream_emit
            if len(self.stream_buffer) >= 2000 or elapsed >= 0.04:
                self._flush_text()
            elif self.stream_timer is None:
                self.stream_timer = threading.Timer(0.04 - elapsed, self._flush_scheduled, (self.run_id,))
                self.stream_timer.daemon = True
                self.stream_timer.start()

    def _chat_event(self, role, text):
        with self.lock:
            self._flush_text()
            message_id = f'{self.run_id}:{self.stream_turn}' if role == 'assistant' and self.stream_turn is not None else None
            self._event('chat', role=role, text=text, message_id=message_id)
            if role == 'assistant':
                self.stream_turn = None

    def _request_approval(self, path, diff, exists):
        with self.lock:
            if self.engine.isInterruptionRequested():
                self.engine.resolve_write_approval('cancel')
                return
            self.approval = uuid.uuid4().hex
            self._event('approval', approval_id=self.approval, path=path, diff=diff, exists=exists)

    def resolve_approval(self, params):
        with self.lock:
            if not self.engine or not self.approval or params.get('approval_id') != self.approval or params.get('run_id') != self.run_id:
                raise ValueError('Подтверждение устарело или задача завершена')
            decision = params.get('decision')
            if decision not in ('apply', 'reject', 'cancel'):
                raise ValueError('Допустимы только apply, reject, cancel')
            self.approval = None
            self.engine.resolve_write_approval(decision)
        return {'ok': True}

    def cancel(self):
        with self.lock:
            self.discovery_cancel.set()
            if self.engine:
                self.engine.requestInterruption()
                self.engine.resolve_write_approval('cancel')
            self.approval = None
        return {'ok': True}

    def start(self, root: Path, params):
        self.idle()
        if not self.config['model']:
            raise ValueError('Выберите модель в настройках')
        prompt = str(params.get('prompt', '')).strip()
        if params.get('resume'):
            task = (self.chat.get('task_checkpoint') or load_task(self.chat['id'])) if self.chat else None
            if not task or task.get('status') != 'paused':
                raise ValueError('Нет приостановленной задачи')
            if task.get('recovery_warning'):
                task.setdefault('resume_state', {})['recovery_note'] = task.pop('recovery_warning')
            save_task(task)
            prompt = task['prompt']
        if not prompt or len(prompt) > 50000:
            raise ValueError('Введите задачу длиной от 1 до 50000 символов')
        if not self.chat:
            self.select_chat(root)
        elif self.chat.get('stream_draft'):
            self._recover_chat()
        if self.chat['project_root'] != str(root):
            raise ValueError('Чат принадлежит другому проекту')
        if not params.get('resume'):
            clear_task(self.chat['id'])
        history = list(self.chat.get('messages', []))
        self.engine = self.engine_factory(**self.config, project_root=str(root), prompt=prompt,
            history=history, memory=load_project_memory(str(root)) if root else {},
            auto_memory=bool(root), allow_tools=bool(root), task_id=self.chat['id'])
        self.run_id = uuid.uuid4().hex
        self.stream_turn = None
        self.stream_buffer = ''
        self.stream_text = ''
        self.stream_persist_at = 0
        self.last_stream_emit = 0
        self.chat['model'] = self.config['model']
        self.chat['active_run_id'] = self.run_id
        self.chat['messages'] = history + [{'role': 'user', 'content': prompt}]
        self.chat['task_checkpoint'] = self.engine.task_snapshot()
        if self.chat.get('title') == 'Новый чат':
            self.chat['title'] = ' '.join(prompt.split())[:80]
        self._persist_chat()
        self.engine.chat.connect(self._chat_event)
        self.engine.text_delta.connect(self._text_delta)
        self.engine.log.connect(lambda text: self._event('log', text=text[:12000]))
        self.engine.progress.connect(lambda count, maximum: self._event('progress', count=count, maximum=maximum))
        self.engine.task_updated.connect(self._task_event)
        self.engine.change_event.connect(lambda change: self._event('change', change=change))
        self.engine.write_approval_requested.connect(self._request_approval)
        self.engine.conversation_updated.connect(self._save_messages)
        self.engine.finished_text.connect(lambda text: self._event('result', text=text))
        self.engine.failed.connect(lambda text: self._event('failed', text=text))
        self.thread = threading.Thread(target=self._run, daemon=True, name='agent-task')
        self.task_running = True
        self.thread.start()
        return {'ok': True, 'run_id': self.run_id, 'chat_id': self.chat['id']}

    def _save_messages(self, messages):
        with self.lock:
            self._flush_text()
            if self.draft_timer:
                self.draft_timer.cancel()
                self.draft_timer = None
            self.stream_turn = None
            self.stream_text = ''
            self.chat['messages'] = messages
            self.chat.pop('stream_draft', None)
            self._persist_chat()

    def _run(self):
        try:
            self.engine.run()
        except Exception as exc:
            self._event('failed', text=f'{type(exc).__name__}: {exc}')
        finally:
            with self.lock:
                self._flush_text()
                if self.draft_timer:
                    self.draft_timer.cancel()
                    self.draft_timer = None
                self.approval = None
                try:
                    task = self.engine.task_snapshot()
                    activity_changed = recover_tools(task, self.chat['messages']) if task else False
                    if task and task.get('status') == 'running':
                        task['status'] = 'paused'
                        task['last_event'] = 'Исполнение прервано; проверьте сообщения об ошибках и продолжите задачу'
                    saved_status = (self.chat.get('task_checkpoint') or {}).get('status')
                    if task and (saved_status != task.get('status') or activity_changed):
                        self._task_event(task)
                except Exception as exc:
                    self._event('failed', text=f'Не удалось сохранить состояние задачи: {type(exc).__name__}: {exc}')
                finally:
                    # All state is finalized before clients are told they may start again.
                    self.task_running = False
                    self._event('task_end')

    def shutdown(self):
        self.cancel_model_setup()
        self.cancel()
        if self.thread:
            self.thread.join(timeout=2)
        if self.discovery_thread:
            self.discovery_thread.join(timeout=1)
        if self.probe_thread:
            self.probe_thread.join(timeout=1)
