"""Explicitly authorized owner-only Telegram results, diffs and remote control."""
import queue
import re
import threading

import httpx


class TelegramService:
    def __init__(self, tasks, root, emit, start_task):
        self.tasks,self.root,self.emit,self.start_task=tasks,root,emit,start_task
        self.lock=threading.RLock();self.stop_event=threading.Event();self.thread=None
        self.state='disconnected';self.error='';self.username='';self.owner=0
        self.client=None;self.token='';self.notifications=queue.Queue(maxsize=100)
        self.remote_chat=None;self.approval=None

    def status(self):
        """Expose connection state without token or token-bearing URLs."""
        with self.lock:
            return {'ok':True,'state':self.state,'error':self.error,'username':self.username,'owner_id':self.owner}

    def start(self, params):
        """Connect a BotFather token and a positive private-chat owner ID."""
        with self.lock:
            if self.thread and self.thread.is_alive():raise ValueError('Сначала отключите текущего бота')
            token=params.get('token','');owner=str(params.get('owner_id',''))
            if not isinstance(token,str) or not re.fullmatch(r'[0-9]{5,20}:[A-Za-z0-9_-]{20,120}',token):
                raise ValueError('Укажите токен бота от BotFather')
            if not owner.isdigit() or not 0<int(owner)<2**53:
                raise ValueError('Укажите свой числовой Telegram user ID')
            self.token,self.owner=token,int(owner);self.error='';self.state='connecting'
            self.username='';self.remote_chat=None;self.approval=None
            self.stop_event=threading.Event();self.notifications=queue.Queue(maxsize=100)
            self.thread=threading.Thread(target=self.poll,daemon=True,name='telegram-control');self.thread.start()
        return self.status()

    def api(self, method, params=None):
        """Call only Telegram via TLS; callers never expose raw HTTP exceptions."""
        response=self.client.post('https://api.telegram.org/bot'+self.token+'/'+method,json=params or {})
        response.raise_for_status();data=response.json()
        if not data.get('ok'):raise ValueError('Telegram API отклонил запрос')
        return data.get('result')

    def send(self, text):
        """Send bounded plain text exclusively to the configured owner."""
        for offset in range(0,min(len(text),21000),3500):
            if self.stop_event.is_set():return
            self.api('sendMessage',{'chat_id':self.owner,'text':text[offset:offset+3500],'link_preview_options':{'is_disabled':True}})

    def observe(self, event):
        """Queue remote results and current approval metadata without blocking Core."""
        if self.state!='connected':return
        if event.get('event')=='handoff_started' and event.get('source_chat')==self.remote_chat:
            self.remote_chat=event.get('target_chat');return
        if event.get('event')=='approval':self.approval=dict(event)
        if event.get('event') not in ('result','failed','approval','task_end'):return
        if event.get('chat_id')!=self.remote_chat and event.get('event')!='approval':return
        try:self.notifications.put_nowait(dict(event))
        except queue.Full:pass

    def command(self, message):
        """Ignore groups, strangers and forwarded commands; serialize owner actions."""
        if message.get('from',{}).get('id')!=self.owner or message.get('chat',{}).get('id')!=self.owner or message.get('chat',{}).get('type')!='private':return
        if message.get('forward_origin') or message.get('via_bot'):return
        text=message.get('text','')
        if not isinstance(text,str) or len(text)>10000:return
        name,_,argument=text.strip().partition(' ');name=name.split('@')[0].lower();argument=argument.strip()
        with self.tasks.lock:
            result=self.dispatch(name,argument)
        self.send(result)

    def dispatch(self, name, argument):
        """Execute a bounded command under the shared TaskService control lock."""
        if name in ('/start','/help'):
            return '/status — состояние\n/result — последний ответ\n/resume — продолжить паузу\n/stop — остановить\n/chat текст — основная модель\n/ide текст — выбранный проект\n/miya текст — Мия\n/approval — текущий diff\n/approve ID или /reject ID — решение по точному ID\nПапки для инструментов ПК укажите в двойных кавычках.'
        if name=='/status':
            snapshot=self.tasks.engine.task_snapshot() if self.tasks.engine else None
            return 'Задача: '+str((snapshot or {}).get('status','idle'))+'\nМодель: '+self.tasks.config.get('model','')+'\nПроект: '+str(self.root() or 'не выбран')
        if name=='/resume':
            self.tasks.idle();chat=self.tasks.chat
            if not chat:raise ValueError('Нет выбранной задачи для продолжения')
            mode=chat.get('mode','ide' if chat.get('project_root') else 'chat');self.remote_chat=chat['id']
            self.emit({'event':'remote_task','mode':mode,'chat':chat,'prompt':'Продолжить приостановленную задачу','resume':True})
            try:self.start_task({'mode':mode,'resume':True})
            except Exception:
                self.emit({'event':'remote_error','text':'Не удалось продолжить задачу'})
                raise
            return 'Продолжение запрошено'
        if name=='/result':
            messages=(self.tasks.chat or {}).get('messages',[])
            answers=[m.get('content') for m in messages if m.get('role')=='assistant' and isinstance(m.get('content'),str) and m.get('content').strip()]
            return 'Последний сохранённый ответ:\n'+answers[-1][-20000:] if answers else 'Сохранённого ответа пока нет'
        if name=='/stop':
            self.tasks.cancel();return 'Запрошена остановка задачи'
        if name=='/approval':
            if not self.tasks.approval or not self.approval:return 'Нет ожидающего подтверждения'
            return 'Подтверждение '+self.tasks.approval+'\n'+self.approval.get('path','')+'\n'+self.approval.get('diff','')[:10000]+'\n/approve '+self.tasks.approval+'\n/reject '+self.tasks.approval
        if name in ('/approve','/reject'):
            self.tasks.resolve_approval({'run_id':self.tasks.run_id,'approval_id':argument,'decision':'apply' if name=='/approve' else 'reject'})
            return 'Решение принято'
        if name in ('/chat','/ide','/miya'):
            if not argument:raise ValueError('После команды нужен текст задачи')
            self.tasks.idle();mode={'/chat':'chat','/ide':'ide','/miya':'voice'}[name]
            root=self.root() if mode=='ide' else ''
            if root is None:raise ValueError('Для IDE сначала выберите папку на ПК')
            selected=self.tasks.select_chat(root,mode=mode);self.remote_chat=selected['chat']['id']
            self.emit({'event':'remote_task','mode':mode,'chat':selected['chat'],'prompt':argument})
            try:self.start_task({'mode':mode,'prompt':argument})
            except Exception:
                self.emit({'event':'remote_error','text':'Удалённая задача не запущена; проверьте настройки и pending diff'})
                raise
            return 'Задача запущена: '+mode
        return 'Неизвестная команда. /help'

    def poll(self):
        """Drop stale backlog at connection, then use owner filtering and retries."""
        try:
            with httpx.Client(timeout=httpx.Timeout(30,connect=5),follow_redirects=False,trust_env=False) as client:
                self.client=client
                me=self.api('getMe');self.username=me.get('username','')
                backlog=self.api('getUpdates',{'offset':-1,'timeout':0,'allowed_updates':['message']})
                offset=max((item['update_id']+1 for item in backlog),default=0)
                self.state='connected'
                while not self.stop_event.is_set():
                    try:
                        while not self.notifications.empty():
                            event=self.notifications.get_nowait();kind=event.get('event')
                            if kind in ('result','failed'):self.send(event.get('text','') or kind)
                            elif kind=='approval':self.send('Ожидается подтверждение изменения '+event.get('path','')+'\n/approval')
                            elif kind=='task_end':self.send('Обработка задачи завершилась; /status')
                        updates=self.api('getUpdates',{'offset':offset,'timeout':10,'allowed_updates':['message']})
                        for update in updates:
                            offset=max(offset,update['update_id']+1)
                            try:self.command(update.get('message',{}))
                            except Exception as exc:
                                self.send('Команда не выполнена: '+(str(exc)[:300] if isinstance(exc,ValueError) else type(exc).__name__))
                        self.error=''
                    except Exception as exc:
                        if self.stop_event.is_set():break
                        self.error='Telegram: '+type(exc).__name__+'; повтор подключения'
                        self.stop_event.wait(3)
        except Exception as exc:
            self.error='Telegram: '+type(exc).__name__+'; проверьте токен, сеть и отсутствие webhook'
        finally:
            self.client=None;self.token='';self.state='disconnected'

    def stop(self):
        """Disconnect without keeping the bot token on disk or in status."""
        self.stop_event.set()
        if self.state!='disconnected':self.state='disconnecting'
        if self.client:self.client.close()
        return self.status()

    def shutdown(self):
        self.stop()
        if self.thread:self.thread.join(timeout=3)
