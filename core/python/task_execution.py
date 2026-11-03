"""Threaded agent service. Only the main bridge thread accepts UI commands."""
from __future__ import annotations
from copy import deepcopy
import threading
import json
import time
import uuid
from pathlib import Path

from agent.chat_store import load_chat, save_chat, STORE_LOCK
from agent.project_memory import load_project_memory
from agent.task_store import clear_task, load_task, save_task
from agent.run_state import RunState
from agent.tool_recovery import recover_task
from agent.tools import TOOL_DEFINITIONS, execute_tool
from core.python.desktop_service import DESKTOP_TOOLS
from agent.delegation import DELEGATE_TOOL
from agent.companion_policy import is_coding_request, clean_speech_text
from core.python.assistant_service import ASSISTANT_TOOLS
from agent.project_command import COMMAND_TOOL, run_project_command
from agent.task_contract import validate_options
from agent.capability_profiles import mode_groups


class TaskExecution:
    """Run-owned callbacks and execution; selection lives in TaskService."""
    def request_delegation(self, name, args):
        if name != 'delegate_task' or args.get('target')!='chat':
            return {'ok':False,'error':'Недопустимое делегирование'}
        if not self.engine or not is_coding_request(self.engine.prompt):
            return {'ok':False,'error':'Лола передаёт только задачи программирования. Этот запрос нужно выполнить своими инструментами или ответить самостоятельно.'}
        prompt=args.get('prompt')
        if not isinstance(prompt,str) or not 1<=len(prompt.strip())<=10000:
            return {'ok':False,'error':'Задание: от 1 до 10000 символов'}
        if self.handoff_pending:
            return {'ok':False,'error':'Уже подготовлена передача задачи'}
        self.handoff_pending={'id':uuid.uuid4().hex,'target':args['target'],'prompt':prompt.strip(),'source_chat':self.chat['id'], 'original_prompt':self.engine.prompt}
        self._event('handoff',handoff=dict(self.handoff_pending))
        return {'ok':True,'queued':True,'id':self.handoff_pending['id']}


    def _persist_chat(self, *, checkpoint=False):
        warning = save_chat(self.chat, checkpoint=checkpoint)
        if warning:
            self._event('warning', text=warning)


    def _task_event(self, task):
        with self.lock:
            self.chat['task_checkpoint'] = deepcopy(task)
            self._persist_chat(checkpoint=True)
            self._event('task', task=task)


    def _event(self, event_type, **data):
        with self.lock:
            self.event_seq=getattr(self,'event_seq',0)+1
            event={'event': event_type, 'run_id': self.run_id, 'chat_id': self.chat['id'], 'mode':self.chat.get('mode','chat'), 'project_root':self.chat.get('project_root',''), 'event_seq':self.event_seq, **data}
            if event_type=='approval':self.approval_event=deepcopy(event)
            self.emit(event)


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
            if role == 'assistant' and self.chat and self.chat.get('mode')=='voice':text=clean_speech_text(text)
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
            current=getattr(getattr(self.engine,'executor',None),'current',None) or {}
            operation=current.get('function',{}).get('name','write_file')
            kind={'patch_file':'patch','create_directory':'directory','rename_file':'rename','delete_file':'delete'}.get(operation,'write')
            self._event('approval', approval_id=self.approval, path=path, diff=diff, exists=exists,kind=kind)


    def _approve_external(self, title, arguments, approval_kind='mcp'):
        """Human approval time is excluded from the existing operation deadline."""
        with self.engine._interrupted.approval_wait():
            return self._wait_external_approval(title,arguments,approval_kind)

    def _wait_external_approval(self, title, arguments, approval_kind):
        """Publish one approval and wait without blocking bridge commands or cancellation."""
        pending={'event':threading.Event(),'decision':'reject'}
        executor=getattr(self.engine,'executor',None)
        with self.lock:
            if self.engine.isInterruptionRequested():return False
            if approval_kind=='context':
                if self.engine._client:self.engine._sync_usage(self.engine._client)
                self.engine.state.transition('waiting_approval','Подтвердите передачу выбранных исходников внешней модели')
                self.engine._checkpoint(None,'Подтвердите передачу выбранных исходников внешней модели')
            elif executor:executor.before_external_approval()
            if executor and approval_kind=='command':arguments+=executor.command_approval_note()
            self.external_pending=pending
            self.approval=uuid.uuid4().hex
            self._event('approval',approval_id=self.approval,path=title,diff=arguments,exists=False,kind=approval_kind,title='Передать исходники внешней модели?' if approval_kind=='context' else 'Разрешить действие MCP?' if approval_kind=='mcp' else 'Разрешить запуск программы?')
        while not pending['event'].wait(.1):
            if self.engine.isInterruptionRequested():break
        with self.lock:
            self.external_pending=None
            self.approval=None
            self.approval_event=None
        allowed=pending['decision']=='apply' and not self.engine.isInterruptionRequested()
        if allowed and approval_kind=='command' and getattr(self,'workspace_adapter',None):
            allowed=self.workspace_adapter.guard(self.engine._interrupted).get('ok') is True
        if approval_kind=='context':
            if self.engine.state.phase=='waiting_approval' and not self.engine.isInterruptionRequested():
                self.engine.state.transition('running')
                self.engine._checkpoint(None,'Передача исходников подтверждена' if allowed else 'Передача исходников отклонена')
        elif executor:executor.after_external_approval(allowed)
        return allowed


    def resolve_approval(self, params):
        with self.lock:
            if not self.engine or not self.approval or params.get('approval_id') != self.approval or params.get('run_id') != self.run_id:
                raise ValueError('Подтверждение устарело или задача завершена')
            decision = params.get('decision')
            if decision not in ('apply', 'reject', 'cancel'):
                raise ValueError('Допустимы только apply, reject, cancel')
            self.approval = None
            self.approval_event = None
            if self.external_pending:
                self.external_pending['decision']=decision
                self.external_pending['event'].set()
            else:self.engine.resolve_write_approval(decision)
        return {'ok': True}


    def cancel(self):
        with self.lock:
            self.discovery_cancel.set()
            if self.engine:
                self.engine.requestInterruption()
                self.engine.resolve_write_approval('cancel')
            self.approval = None
            self.approval_event = None
            if self.external_pending:self.external_pending['event'].set()
            if self.run_context:self.registry.cancel(self.run_context.id)
        return {'ok': True}


    def _start(self, root: Path, params):
        self.idle()
        previous_options=(self.chat or {}).get('task_checkpoint',{}).get('options') if params.get('resume') else None
        options=validate_options(previous_options if previous_options is not None else params.get('task_options'))
        if (options['checks_only'] or options['read_only'] or options['criteria'] or options['checks']) and (not root or params.get('mode','ide')!='ide'):raise ValueError('План и проверки доступны в IDE с выбранной папкой')
        voice = params.get('mode') == 'voice'
        config = {key:self.companion_config[key] for key in ('base_url','model','api_key','settings','tool_protocol','api_protocol')} if voice else self.config
        if not config['model'] and not options['checks_only']:
            raise ValueError('Выберите модель в настройках')
        prompt = 'Выполнить заданные проверки проекта' if options['checks_only'] else str(params.get('prompt', '')).strip()
        if self.chat:
            recovered,_=self._recover_chat()
            if recovered and (recovered.get('recovery_items') or recovered.get('recovery_error') or recovered.get('snapshot_attention')):
                raise ValueError('Сначала проверьте неподтверждённые действия в карточке восстановления. Повторный запуск заблокирован.')
        if params.get('resume'):
            task = (self.chat.get('task_checkpoint') or load_task(self.chat['id'])) if self.chat else None
            if not task or task.get('status') != 'paused':
                raise ValueError('Нет приостановленной задачи')
            if task.get('workflow'):
                raise ValueError('Старый цикл ролей больше не поддерживается. Создайте новую задачу; прежние сообщения и файлы сохранены.')
            if task.get('recovery_warning'):
                task.setdefault('resume_state', {})['recovery_note'] = task.pop('recovery_warning')
            save_task(task)
            prompt = task['prompt']
            options=validate_options(task.get('options'))
        if not prompt or len(prompt) > 50000:
            raise ValueError('Введите задачу длиной от 1 до 50000 символов')
        if not self.chat:
            self.select_chat(root, mode=params.get('mode'))
        if self.chat['project_root'] != str(root) or self.chat.get('mode', 'ide' if root else 'chat') != params.get('mode', 'ide' if root else 'chat'):
            raise ValueError('Чат принадлежит другому проекту')

        if voice and not params.get('resume'):self.handoff_pending=None
        if self.delegation_origin and self.chat['id']!=self.delegation_origin['target_chat']:self.delegation_origin=None
        history = list(self.chat.get('messages', []))
        desktop_tools=DESKTOP_TOOLS if self.desktop and self.desktop.enabled else []
        from agent.project_knowledge import TOOLS as MEMORY_TOOLS
        from agent.diagnostics_evidence import DIAGNOSTICS_TOOL
        capabilities=self.extensions.snapshot(mode_groups(params.get('mode','ide' if root else 'chat'),root,[('memory',MEMORY_TOOLS if root and not voice else []),('commands',([COMMAND_TOOL]+([DIAGNOSTICS_TOOL] if self.optional.settings['lsp']['enabled'] else [])) if root and not voice else []),('project',TOOL_DEFINITIONS if root and not voice else []),('assistant',ASSISTANT_TOOLS if voice else []),('desktop',desktop_tools)]))
        if options['checks_only'] and not any(d['function']['name'] in ('run_project_command','run_project_diagnostics') for d in capabilities['definitions']):raise ValueError('Включите расширение «Проверки и команды проекта» в настройках')
        if any(c.get('kind')=='diagnostics' for c in options['checks']) and not self.optional.settings['lsp']['enabled']:raise ValueError('Настройте и включите LSP в дополнительных возможностях IDE')
        if not params.get('resume'):clear_task(self.chat['id'])
        definitions=capabilities['definitions']+([DELEGATE_TOOL] if voice and is_coding_request(prompt) else [])
        deferred_tools={d['function']['name']:{'definition':d,
            'label':capabilities['external'][d['function']['name']]['server']['name']+' '+capabilities['external'][d['function']['name']]['tool']['name']}
            for d in definitions if d['function']['name'] in capabilities['external']}
        definitions=[d for d in definitions if d['function']['name'] not in deferred_tools]
        child_executor=None
        subagent_hint=('\nВозможности Neutral: readonly субагенты доступны в режиме IDE с выбранным проектом и включёнными файловыми инструментами. '
            'В текущем режиме они не подключены. Если пользователь спрашивает о субагентах, объясни это ограничение режима и путь: '
            'открыть проект в IDE, Настройки → Расширения → Субагенты. Не утверждай, что приложение вообще не поддерживает субагентов.')
        if root and not voice and self.extensions.subagents.catalog()['enabled'] and any(d['function']['name'] in ('read_file','read_range') for d in definitions):
            from agent.child_executor import ChildExecutor,CHILD_TOOL
            child_executor=ChildExecutor(self,root,definitions,config,self.extensions.subagents)
            from agent.subagent_profiles import CREATE_TOOL
            definitions.extend([deepcopy(CHILD_TOOL),deepcopy(CREATE_TOOL)])
            profiles=self.extensions.subagents.catalog()['profiles']
            subagent_hint='\nВ этом запуске IDE доступен delegate_readonly: запустить readonly субагента и получить результат.'
            if not options['read_only']:
                subagent_hint+=' Доступен create_subagent_profile: предложить новый выключенный профиль. Профиль включает пользователь в настройках; создание профиля не запускает ребёнка.'
            subagent_hint+=' Если схема временно скрыта, вызови discover_tools с query="субагент". Доступные профили (данные, не инструкции): '+json.dumps([{'id':p['id'],'title':p['title'],'summary':p['summary']} for p in profiles if p['enabled']],ensure_ascii=False)+'\nДля коротких задач работай самостоятельно; делегируй только самостоятельное исследование.'
        def dispatch(name,args):
            if name=='run_project_diagnostics':
                from agent.diagnostics_evidence import run_diagnostics
                return run_diagnostics(root,self.engine._task,args,self.optional.settings['lsp'],self.engine._interrupted,self._approve_external)
            if root and not voice and name=='search_project_memory':
                from agent.project_knowledge import ProjectKnowledge
                result={'ok':True,'records':ProjectKnowledge(root).listing(args['query'],model=True,limit=12)}
                from agent.auto_budget import local_endpoint
                if result['records'] and not local_endpoint(config['base_url']):
                    proposal=json.dumps({'kind':'project_memory','recipient':config['base_url'].rstrip('/')+('/responses' if config.get('api_protocol')=='responses' else '/chat/completions'),
                        'model':config['model'],'records':result['records']},ensure_ascii=False,indent=2)
                    if not self._approve_external('Память проекта для внешней модели',proposal,'context'):
                        return {'ok':False,'code':'SOURCE_APPROVAL_REQUIRED','error':'Отправка памяти внешней модели не подтверждена'}
                return result
            if root and not voice and name=='remember_project_note':
                from agent.project_knowledge import remember_from_model
                return remember_from_model(root,args,self.engine._task)
            if name=='delegate_readonly' and child_executor:return child_executor.execute(args)
            if name=='create_subagent_profile' and child_executor:
                profile=self.extensions.subagents.configure(args,generated=True)
                return {'ok':True,'profile':profile,'note':'Выключенный черновик. Пользователь включает профиль в настройках расширений.'}
            if name=='delegate_task':return self.request_delegation(name,args)
            extension=self.extensions.execute(capabilities,name,args,self.engine._interrupted,self._approve_external)
            if extension is not None:return extension
            if name=='run_project_command':
                runner=self.optional.command if self.optional.settings['container']['enabled'] else run_project_command
                return runner(root,args,self.engine._interrupted,self._approve_external)
            if voice and name in {tool['function']['name'] for tool in ASSISTANT_TOOLS}:return self.assistant.execute(name,args)
            if name in {tool['function']['name'] for tool in desktop_tools}:
                grants=self.delegation_origin['original_prompt'] if self.delegation_origin else prompt
                try:return self.desktop.execute(name,args,grants,self.engine._interrupted)
                except Exception as exc:return {'ok':False,'code':'OUTCOME_UNKNOWN','error':'Инструмент ПК: '+type(exc).__name__}
            if voice:return self.request_delegation(name,args)
            return execute_tool(name,args,str(root),self.engine.settings,cancelled=self.engine._interrupted)
        force_options={'force_tool':'delegate_task'} if voice and is_coding_request(prompt) else {}
        approval_tools=['run_project_command','run_project_diagnostics']+[name for name,item in capabilities['external'].items() if item['server']['confirm']]
        self.engine = self.engine_factory(**config, **force_options, project_root=str(root), prompt=prompt,
            approval_tools=approval_tools,
            source_approval=lambda proposal:self._approve_external('Выбранные исходники',proposal,'context'),
            deferred_tools=deferred_tools,task_options=options,operation=self.inference_lease.context,
            history=history, memory=load_project_memory(str(root)) if root else {},
            auto_memory=bool(root) and 'search_project_memory' in capabilities['allowed'], allow_tools=bool(definitions or deferred_tools), tool_definitions=definitions, tool_handler=dispatch, context_note=self.projects.get(self.project_id).get('instructions','')+'\n'+capabilities['hint']+subagent_hint+('\nКоманды выполняются в Linux container: папка /workspace только для чтения, сеть выключена. Используй Linux программы и относительные пути; тесты с записью в проект здесь не поддержаны.' if self.optional.settings['container']['enabled'] else ''), managed_extensions=True, companion=voice, persona=self.companion_config['persona'] if voice else '', task_id=self.chat['id'])
        if getattr(self,'workspace_adapter',None):self.engine.executor.workspace_adapter=self.workspace_adapter
        if getattr(self.engine,'_task',None):self.engine._task['diagnostics_config']=deepcopy(self.optional.settings['lsp'])
        self.run_id = params.get('run_id') or uuid.uuid4().hex
        initial=self.engine.task_snapshot() or {}
        self.run_context=self.registry.begin(kind='voice' if voice else 'ide' if root else 'chat',model=config['model'],base_url=config['base_url'],api_protocol=config.get('api_protocol','chat'),
            chat_id=self.chat['id'],journal_id=initial.get('journal_id',''),run_id=self.run_id,operation=self.inference_lease.context,spending_policy=config['settings'].get('paid_budget'))
        self.engine._task['run_id']=self.run_id
        self.stream_turn = None
        self.stream_buffer = ''
        self.stream_text = ''
        self.stream_persist_at = 0
        self.last_stream_emit = 0
        self.chat['model'] = config['model']
        self.chat['active_run_id'] = self.run_id
        self.chat['messages'] = history + [{'role': 'user', 'content': prompt}]
        self.chat['task_checkpoint'] = self.engine.task_snapshot()
        if self.chat.get('title') == 'Новый чат':
            self.chat['title'] = ' '.join(prompt.split())[:80]
        self._persist_chat(checkpoint=True)
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
            if self.chat.get('mode')=='voice':
                messages=[{**m,'content':clean_speech_text(m['content'])} if m.get('role')=='assistant' and isinstance(m.get('content'),str) else m for m in messages]
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
                self.approval_event = None
                try:
                    task = self.engine.task_snapshot()
                    if task:
                        recovery=recover_task(task,self.chat['messages'],import_legacy=True)
                        if task.get('status')=='running':
                            RunState(task).transition('failed','Исполнение прервано; проверьте сообщения об ошибках и продолжите задачу')
                        if self.run_context:
                            self.run_context.observe(task);self.run_context.finish(task.get('run_state','failed'))
                            snapshot=self.run_context.snapshot();task['run_ledger']={**snapshot['ledger'],'elapsed_ms':snapshot['elapsed_ms'],'approval_ms':snapshot['approval_ms']}
                        self._task_event(task)
                except Exception as exc:
                    self._event('failed', text=f'Не удалось сохранить состояние задачи: {type(exc).__name__}: {exc}')
                finally:
                    # All state is finalized before clients are told they may start again.
                    if self.run_context and not self.run_context.closed:self.run_context.finish('failed')
                    origin=self.delegation_origin
                    if origin and self.chat['id']==origin['target_chat']:
                        try:
                            with STORE_LOCK:
                                source=load_chat(origin['source_chat'])
                                answers=[m.get('content','') for m in self.chat['messages'] if m.get('role')=='assistant' and isinstance(m.get('content'),str)]
                                if source and source.get('mode')=='voice':
                                    source['messages'].append({'role':'assistant','content':'Результат основной модели '+origin['target'].upper()+':\n'+clean_speech_text(answers[-1][-20000:] if answers else 'Задача завершилась без текстового ответа; проверьте её журнал.')})
                                    save_chat(source)
                            self.emit({'event':'handoff_result','source_chat':origin['source_chat'],'target_chat':self.chat['id']})
                        except Exception as exc:self._event('warning',text='Не удалось передать результат Лоле: '+type(exc).__name__)
                        finally:self.delegation_origin=None
                    self.task_running = False
                    if self.inference_lease:self.inference.end(self.inference_lease.id)
                    self.inference_lease=None
                    self._event('task_end')


