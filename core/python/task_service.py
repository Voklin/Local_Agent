"""Threaded agent service. Only the main bridge thread accepts UI commands."""
from __future__ import annotations
import json
import threading
import uuid
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from agent.engine import AgentEngine
from agent.chat_store import create_chat, list_chats, load_chat, save_chat
from agent.project_memory import load_project_memory
from agent.task_store import clear_task, load_task, save_task


class TaskService:
    def __init__(self, emit, engine_factory=AgentEngine):
        self.emit = emit
        self.engine_factory = engine_factory
        self.lock = threading.RLock()
        self.thread = None
        self.engine = None
        self.approval = None
        self.chat = None
        self.run_id = None
        self.config = {'base_url': 'http://127.0.0.1:1234/v1', 'model': '', 'api_key': ''}

    def idle(self):
        if self.thread and self.thread.is_alive():
            raise ValueError('Сначала остановите текущую задачу и дождитесь завершения')

    def configure(self, params):
        self.idle()
        base_url = str(params.get('base_url', '')).strip().rstrip('/')
        parsed = urlparse(base_url)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError('Укажите HTTP(S) URL сервера, например http://127.0.0.1:1234/v1')
        self.config = {'base_url': base_url, 'model': str(params.get('model', '')).strip()[:300],
                       'api_key': str(params.get('api_key', ''))[:4000]}
        # Keys stay in process memory, never in bridge responses or persisted chats.
        return {'ok': True, 'base_url': base_url, 'model': self.config['model']}

    def models(self):
        req = Request(self.config['base_url'] + '/models', headers={
            'Authorization': 'Bearer ' + (self.config['api_key'] or 'no-key')})
        with urlopen(req, timeout=5) as response:
            raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError('Слишком большой ответ списка моделей')
        data = json.loads(raw)
        return {'ok': True, 'models': [str(m['id'])[:300] for m in data.get('data', [])[:500]
                                      if isinstance(m, dict) and isinstance(m.get('id'), str)]}

    def chats(self, root):
        return {'ok': True, 'chats': [c for c in list_chats() if c.get('project_root') == str(root)]}

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
        task = load_task(chat['id'])
        if task and task.get('status') == 'running':
            task['status'] = 'paused'
            task['last_event'] = 'Предыдущий процесс завершился; задачу можно продолжить'
            task = save_task(task)
        return {'ok': True, 'chat': chat, 'task': task}

    def _event(self, kind, **data):
        self.emit({'event': kind, 'run_id': self.run_id, 'chat_id': self.chat['id'], **data})

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
            task = load_task(self.chat['id']) if self.chat else None
            if not task or task.get('status') != 'paused':
                raise ValueError('Нет приостановленной задачи')
            prompt = task['prompt']
        if not prompt or len(prompt) > 50000:
            raise ValueError('Введите задачу длиной от 1 до 50000 символов')
        if not self.chat:
            self.select_chat(root)
        if self.chat['project_root'] != str(root):
            raise ValueError('Чат принадлежит другому проекту')
        if not params.get('resume'):
            clear_task(self.chat['id'])
        history = list(self.chat.get('messages', []))
        self.engine = self.engine_factory(**self.config, project_root=str(root), prompt=prompt,
            history=history, memory=load_project_memory(str(root)), task_id=self.chat['id'])
        self.run_id = uuid.uuid4().hex
        self.chat['model'] = self.config['model']
        self.chat['messages'] = history + [{'role': 'user', 'content': prompt}]
        if self.chat.get('title') == 'Новый чат':
            self.chat['title'] = ' '.join(prompt.split())[:80]
        save_chat(self.chat)
        self.engine.chat.connect(lambda role, text: self._event('chat', role=role, text=text))
        self.engine.log.connect(lambda text: self._event('log', text=text[:12000]))
        self.engine.progress.connect(lambda count, maximum: self._event('progress', count=count, maximum=maximum))
        self.engine.task_updated.connect(lambda task: self._event('task', task=task))
        self.engine.change_event.connect(lambda change: self._event('change', change=change))
        self.engine.write_approval_requested.connect(self._request_approval)
        self.engine.conversation_updated.connect(self._save_messages)
        self.engine.finished_text.connect(lambda text: self._event('result', text=text))
        self.engine.failed.connect(lambda text: self._event('failed', text=text))
        self.thread = threading.Thread(target=self._run, daemon=True, name='agent-task')
        self.thread.start()
        return {'ok': True, 'run_id': self.run_id, 'chat_id': self.chat['id']}

    def _save_messages(self, messages):
        self.chat['messages'] = messages
        save_chat(self.chat)

    def _run(self):
        try:
            self.engine.run()
        except Exception as exc:
            self._event('failed', text=f'{type(exc).__name__}: {exc}')
        finally:
            with self.lock:
                self.approval = None
                self._event('task_end')

    def shutdown(self):
        self.cancel()
        if self.thread:
            self.thread.join(timeout=2)
