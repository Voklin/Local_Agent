"""Conversation selection and recovery, independent from inference workers and UI events."""
from copy import deepcopy
import threading
from agent.chat_store import create_chat,read_chat_catalog,load_chat,save_chat,STORE_LOCK
from agent.task_store import load_task
from agent.tool_recovery import recover_task
from agent.run_state import RunState


class SessionService:
    def __init__(self,lock,idle,model_for_mode):
        self.lock=lock;self.idle=idle;self.model_for_mode=model_for_mode
        self.chat=None;self.project_id=''

    def move_chat(self, params):
        self.idle()
        target=params.get('target');source=params.get('mode')
        if target not in ('chat','voice') or source not in ('chat','voice'):
            raise ValueError('Перенос доступен между Chat и Лолой')
        with self.lock, STORE_LOCK:
            chat=load_chat(params.get('chat_id'))
            if not chat or chat.get('project_root') or chat.get('mode','chat')!=source or chat.get('project_id','')!=self.project_id:
                raise ValueError('Чат не принадлежит исходной области')
            chat['mode']=target
            save_chat(chat)
            if self.chat and self.chat['id']==chat['id']:self.chat=None
        return {'ok':True}

    def chats(self, root, mode=None):
        mode = mode or ('ide' if root else 'chat')
        catalog = read_chat_catalog(root=str(root), mode=mode, project_id=self.project_id)
        return {'ok': True, 'chats': catalog['chats'],
                'warnings': catalog['warnings']}

    def rename(self, root, params):
        mode = params.get('mode', 'ide' if root else 'chat')
        self.idle()
        title=params.get('title')
        if not isinstance(title,str) or not title.strip() or len(title)>120 or '\x00' in title:
            raise ValueError('Название чата: от 1 до 120 символов без NUL')
        with self.lock, STORE_LOCK:
            chat=load_chat(params.get('chat_id'))
            if not chat or chat.get('project_root')!=str(root) or chat.get('mode', 'ide' if root else 'chat')!=mode or chat.get('project_id','')!=self.project_id:
                raise ValueError('Чат не принадлежит выбранной области')
            chat['title']=' '.join(title.split())
            warning=save_chat(chat)
            if self.chat and self.chat['id']==chat['id']:
                self.chat['title']=chat['title']
            return {'ok':True,'title':chat['title'],'warnings':[warning] if warning else []}

    def select_chat(self, root, chat_id=None, mode=None, *, allow_busy=False):
        mode = mode or ('ide' if root else 'chat')
        if not allow_busy:self.idle()
        if chat_id:
            if not isinstance(chat_id, str) or len(chat_id) != 32 or any(c not in '0123456789abcdef' for c in chat_id):
                raise ValueError('Некорректный идентификатор чата')
            chat = load_chat(chat_id)
            if not chat or chat.get('project_root') != str(root) or chat.get('mode', 'ide' if root else 'chat') != mode or chat.get('project_id','')!=self.project_id:
                raise ValueError('Чат не принадлежит выбранному проекту')
        else:
            chat = create_chat(str(root), self.model_for_mode(mode), mode=mode)
            chat['project_id']=self.project_id
            save_chat(chat)
        self.chat = chat
        warnings = [chat.pop('storage_warning')] if chat.get('storage_warning') else []
        task, recovered = self.recover()
        return {'ok': True, 'chat': chat, 'task': task, 'warnings': warnings + recovered}

    def recover(self):
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
        if task:
            from agent.task_graph import migrate_plan
            dirty=dirty or task.get('plan_schema')!=2
            migrate_plan(task)
            was_running=task.get('status')=='running'
            try:
                # Receipt durability precedes task/chat projections. Never use a
                # stale task snapshot to repeat an effect recorded in the journal.
                recovery=recover_task(task,self.chat['messages'],import_legacy=True)
                warnings.extend(recovery['warnings'])
                dirty=dirty or recovery['changed']
                if was_running and not task.get('recovery_items'):
                    RunState(task).transition('paused','Предыдущий процесс завершился; задачу можно продолжить')
                    dirty=True
            except (ValueError,OSError) as exc:
                task['recovery_error']='Не удалось восстановить журнал действий. Исходные данные сохранены: '+str(exc)[:400]
                if task.get('run_state')!='completed':
                    RunState(task).transition('needs_attention',task['recovery_error'])
                warnings.append(task['recovery_error'])
                dirty=True
        if task:
            if task.get('context_pack'):
                from agent.context_builder import visible_summary
                task['context_pack']=visible_summary(task['context_pack'],task['project_root'])
            self.chat['task_checkpoint'] = deepcopy(task)
        if dirty:
            warning = save_chat(self.chat, checkpoint=True)
            if warning:
                warnings.append(warning)
        return task, warnings

