"""Threaded agent service. Only the main bridge thread accepts UI commands."""
from __future__ import annotations
from copy import deepcopy
from contextvars import ContextVar
from pathlib import Path
import threading
import os

from agent.engine import AgentEngine
from agent.chat_store import save_chat, STORE_LOCK
from agent.task_store import save_task
from agent.model_preferences import load_preferences, save_preferences, validate_preferences, connection_key
from agent.model_discovery import discover_models
from agent.model_probe import probe_model
from agent.run_state import RunState
from agent.tool_recovery import recover_task, task_journal
from agent.companion_preferences import load_profile, save_profile
from core.python.assistant_service import AssistantService
from agent.projects import ProjectStore
from core.python.conversation_service import ConversationService
from core.python.extension_service import ExtensionService
from agent.connection_profiles import ConnectionProfiles
from core.python.workspace_review import WorkspaceReview
from core.python.session_service import SessionService
from agent.operation_context import InferenceGate
from core.python.optional_ide_service import OptionalIdeService


class TaskService:
    def __init__(self, emit, engine_factory=AgentEngine):
        self.emit = emit
        self.engine_factory = engine_factory
        self.lock = threading.RLock()
        self.runs = {}
        self.closed = False
        self.config = {**load_preferences(), 'api_key': ''}
        self.companion_config = {**load_profile(), 'api_key':'', 'stt_api_key':''}
        self.probe_thread = None
        self.probe_cancel = threading.Event()
        self.discovery_thread = None
        self.discovery_cancel = threading.Event()
        self.desktop = None
        self.handoff_pending = None
        self.delegation_origin = None
        self.assistant = AssistantService(self.emit)
        self.connections = ConnectionProfiles()
        self.projects = ProjectStore()
        self.view_session=ContextVar('neutral_view_session',default=None)
        self.view_adapter=ContextVar('neutral_view_adapter',default=None)
        self.workspace_adapters={}
        self.native_ide_required=os.environ.get('NEUTRAL_NATIVE_IDE')=='1'
        self.sessions=SessionService(self.lock,self.idle,lambda mode:self.companion_config['model'] if mode=='voice' else self.config['model'])
        # Setup admission is separate from per-run execution and GPU tickets.
        self.inference=InferenceGate()
        from agent.run_registry import RunRegistry
        from agent.inference_scheduler import SCHEDULER
        self.registry=RunRegistry();self.scheduler=SCHEDULER
        self.conversations = ConversationService(self)
        self.extensions = ExtensionService()
        self.workspace_review=WorkspaceReview(self)
        self.optional=OptionalIdeService(self)

    @property
    def sessions(self):
        return self.view_session.get() or self.main_sessions

    @sessions.setter
    def sessions(self,value):
        self.main_sessions=value

    @property
    def workspace_adapter(self):
        adapter=self.view_adapter.get()
        if adapter:return adapter
        chat=getattr(self.sessions,'chat',None)
        return self.workspace_adapters.get(chat.get('project_root')) if chat and chat.get('mode')=='ide' else None

    @property
    def task_running(self):
        return any(run.task_running for run in self.runs.values())

    @property
    def engine(self):
        run=self.selected_run() if hasattr(self,'sessions') else None
        return run.engine if run else getattr(self,'_engine',None)

    @engine.setter
    def engine(self,value):
        self._engine=value

    @property
    def thread(self):
        run=self.selected_run() if hasattr(self,'sessions') else None
        return run.thread if run else getattr(self,'_thread',None)

    @thread.setter
    def thread(self,value):
        self._thread=value

    @property
    def run_id(self):
        run=self.selected_run() if hasattr(self,'sessions') else None
        return run.run_id if run else getattr(self,'_run_id',None)

    @run_id.setter
    def run_id(self,value):
        self._run_id=value

    @property
    def approval(self):
        run=self.selected_run() if hasattr(self,'sessions') else None
        return run.approval if run else getattr(self,'_approval',None)

    @approval.setter
    def approval(self,value):
        self._approval=value

    @property
    def handoff_pending(self):
        run=self.selected_run() if hasattr(self,'sessions') else None
        return run.handoff_pending if run else getattr(self,'_handoff_pending',None)

    @handoff_pending.setter
    def handoff_pending(self,value):
        self._handoff_pending=value
        run=self.selected_run() if hasattr(self,"sessions") else None
        if run:run.handoff_pending=value

    def idle(self):
        with self.lock:
            if self.task_running or (getattr(self,"optional",None) and self.optional.running) or (getattr(self,'workspace_review',None) and self.workspace_review.checkpoint_job.thread and self.workspace_review.checkpoint_job.thread.is_alive()):
                raise ValueError('Сначала остановите текущую задачу и дождитесь завершения')

    def configure(self, params):
        if self.task_running:
            preferences=validate_preferences(params)
            candidate={**preferences,'api_key':connection_key(self.config,preferences,params)}
            if candidate==self.config:return {'ok':True,**preferences}
        self.idle()
        preferences = save_preferences(params)
        self.config = {**preferences, 'api_key': connection_key(self.config, preferences, params)}
        # Keys stay in process memory, never in bridge responses or persisted chats.
        return {'ok': True, **preferences}

    def preferences(self):
        return {'ok': True, 'api_protocol':self.config.get('api_protocol','chat'), 'tool_protocol':self.config.get('tool_protocol','native'), 'base_url': self.config['base_url'], 'model': self.config['model'],
                'settings': deepcopy(self.config['settings'])}


    def prepare_handoff(self, root, params):
        self.idle()
        pending=self.handoff_pending
        if not pending or pending['id']!=params.get('id'):
            raise ValueError('Передача задачи устарела')
        if pending['target']!='chat':raise ValueError('Лола не связана с IDE. Отмените старую передачу; доступна только передача в Chat.')
        scope=''
        result=self.select_chat(scope,mode=pending['target'])
        self.handoff_pending=None
        self.delegation_origin={**pending,'target_chat':result['chat']['id']}
        self.emit({'event':'handoff_started','source_chat':pending['source_chat'],'target_chat':result['chat']['id']})
        return {**result,'handoff':pending}

    def discard_handoff(self, params):
        self.idle()
        if not self.handoff_pending or self.handoff_pending['id']!=params.get('id'):
            raise ValueError('Передача задачи устарела')
        self.handoff_pending=None
        return {'ok':True}

    def companion_preferences(self):
        return {'ok':True, **{k:v for k,v in self.companion_config.items() if k not in ('api_key','stt_api_key')}}

    def configure_companion(self, params):
        self.idle()
        public=save_profile(params)
        self.companion_config={**public,
            'api_key':connection_key(self.companion_config,public,params),
            'stt_api_key':connection_key(self.companion_config,public,params,'stt_api_key','stt_url')}
        return self.companion_preferences()

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
            lease=self.inference.begin('проверка модели',35)
            try:run=self.registry.begin(kind='probe',model=config['model'],base_url=config['base_url'],api_protocol=config.get('api_protocol','chat'),operation=lease.context,spending_policy=config['settings'].get('paid_budget'))
            except BaseException:
                self.inference.end(lease.id);raise
            self.probe_cancel = cancelled = lease.context
            def run_probe():
                try:
                    response = probe_model(config, cancelled=cancelled)
                except Exception as exc:
                    response = {'ok': False, 'error': str(exc)[:500]}
                finally:
                    run.finish('paused' if cancelled.is_set() else 'completed' if response.get('ok') else 'failed')
                    self.inference.end(lease.id)
                respond(response)
            self.probe_thread = threading.Thread(target=run_probe, daemon=True, name='model-probe')
            try:self.probe_thread.start()
            except BaseException:
                run.finish('failed')
                self.inference.end(lease.id)
                raise

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

    @property
    def chat(self):
        return self.sessions.chat

    @chat.setter
    def chat(self,value):
        self.sessions.chat=value

    @property
    def project_id(self):
        return self.sessions.project_id

    @project_id.setter
    def project_id(self,value):
        self.sessions.project_id=value

    def move_chat(self,params):
        return self.sessions.move_chat(params)

    def chats(self,root,mode=None):
        return self.sessions.chats(root,mode)

    def rename(self,root,params):
        return self.sessions.rename(root,params)

    def select_chat(self,root,chat_id=None,mode=None):
        with self.lock:
            self._prune_runs()
            run=self.runs.get(chat_id)
            if run and run.task_running:
                chat=run.chat
                if chat.get('project_root')!=str(root) or chat.get('mode')!=(mode or ('ide' if root else 'chat')) or chat.get('project_id','')!=self.project_id:
                    raise ValueError('Чат не принадлежит выбранному проекту')
                self.chat=chat
                return {'ok':True,**run.view(),'active_runs':self.active_runs(),'warnings':[]}
            # Selection must not invoke crash recovery for a live background owner.
            result=self.sessions.select_chat(root,chat_id,mode,allow_busy=True)
            if self._refresh_run_ledger(result['task']):
                self.chat['task_checkpoint']=deepcopy(result['task'])
                warning=save_chat(self.chat,checkpoint=True)
                if warning:result['warnings'].append(warning)
            result['active_runs']=self.active_runs()
            if run:result['event_seq']=run.event_seq
            return result

    def _recover_chat(self):
        run=self.selected_run()
        if run and run.task_running:return deepcopy(run.chat.get('task_checkpoint')),[]
        task,warnings=self.sessions.recover()
        if task:
            task['diagnostics_config']=deepcopy(self.optional.settings['lsp'])
            if any(r.get('kind')=='diagnostics' for r in task.get('test_results',[])):
                from agent.verifier import StageVerifier
                StageVerifier().refresh(task)
        self._refresh_run_ledger(task)
        return task,warnings

    def _refresh_run_ledger(self,task):
        if not task or not task.get('run_id'):return False
        try:record=self.registry.snapshot(task['run_id'])
        except ValueError:return False
        if record.get('chat_id')!=task.get('chat_id'):return False
        ledger={**record['ledger'],'elapsed_ms':record['elapsed_ms'],'approval_ms':record['approval_ms']}
        changed=task.get('run_ledger')!=ledger
        for child in task.get('children',[]):
            try:child_run=self.registry.snapshot(child['id'])
            except ValueError:continue
            if child_run.get('parent_id')!=record['id'] or child_run.get('chat_id')!=task.get('chat_id'):continue
            state=child_run['state'];event=child_run.get('reason',child.get('event',''))[:240]
            if child.get('state')!=state or child.get('event')!=event:child.update(state=state,event=event);changed=True
        task['run_ledger']=ledger
        return changed

    def workspace_changed(self, root):
        """Publish fresh evidence after a user editor save without altering task lifecycle."""
        if not (self.selected_run() and self.selected_run().task_running) and self.chat and self.chat.get('project_root')==str(root):
            task,_=self._recover_chat()
            if task:
                from agent.verifier import StageVerifier
                StageVerifier().refresh(task)
                task=save_task(task);self.chat['task_checkpoint']=deepcopy(task)
                self._persist_chat(checkpoint=True)
                self._event('workspace_evidence',root=str(root),task=task)
                return task


    def resolve_tool_recovery(self, params):
        """Persist a person's observation; never replay the action being reviewed."""
        self.idle()
        with self.lock, STORE_LOCK:
            if not self.chat or params.get('chat_id')!=self.chat['id'] or self.chat.get('project_id','')!=self.project_id:
                raise ValueError('Выберите чат с восстанавливаемой задачей')
            task,warnings=self._recover_chat()
            if not task or not task.get('journal_id') or params.get('journal_id')!=task['journal_id']:
                raise ValueError('Карточка восстановления устарела')
            if task.get('recovery_error'):raise ValueError(task['recovery_error'])
            journal=task_journal(task)
            journal.resolve(params.get('message_index'),params.get('call_id'),params.get('resolution'))
            recovery=recover_task(task,self.chat['messages'])
            if not task.get('recovery_items'):
                RunState(task).transition('paused','Результаты действий проверены пользователем. Можно продолжить задачу.')
            self.chat['task_checkpoint']=deepcopy(task)
            warning=save_chat(self.chat, checkpoint=True)
            return {'ok':True,'task':task,'chat':self.chat,'warnings':warnings+recovery['warnings']+([warning] if warning else [])}


    def start(self,root,params):
        from core.python.run_session import RunSession
        with self.lock:
            self._prune_runs()
            if self.closed:raise ValueError('Служба задач закрыта')
            if self.optional.running:raise ValueError('Дождитесь дополнительной операции IDE')
            if self.workspace_review.checkpoint_job.thread and self.workspace_review.checkpoint_job.thread.is_alive():raise ValueError('Дождитесь сохранения Git-снимка или отмените его')
            if self.inference.status()['busy']:raise ValueError('Уже выполняется проверка модели')
            if not self.chat:self.select_chat(root,mode=params.get('mode'))
            if root and self.native_ide_required and self.workspace_adapter is None:raise ValueError('Сначала откройте этот проект в Neutral IDE: файловые операции выполняет редактор.')
            if self.selected_run() and self.selected_run().task_running:raise ValueError('В этом чате уже выполняется задача')
            live=[r for r in self.runs.values() if r.task_running]
            if any(r.delegation_origin and r.delegation_origin['source_chat']==self.chat['id'] for r in live):
                raise ValueError('Лола ждёт результат переданной задачи; откройте её основной чат')
            base=Path(root).resolve() if root else None
            roots=[Path(r.chat['project_root']).resolve() for r in live if r.chat.get('project_root')]
            if base and any(base.is_relative_to(other) or other.is_relative_to(base) for other in roots):
                raise ValueError('В этой папке уже работает агент. Дождитесь завершения или остановите его.')
            config=self.companion_config if params.get('mode')=='voice' else self.config
            binding=(config['base_url'],config['model'],config.get('api_protocol','chat'))
            for other in live:
                active=other.companion_config if other.chat.get('mode')=='voice' else other.config
                if binding!=(active['base_url'],active['model'],active.get('api_protocol','chat')):
                    raise ValueError('Фоновые чаты используют одно подключение и модель. Дождитесь завершения другой модели.')
            run=RunSession(self,self.chat)
            self.runs[self.chat['id']]=run
            try:
                result=run.begin(root,params)
                if run.delegation_origin:self.delegation_origin=None
                return result
            except BaseException:
                self.runs.pop(self.chat['id'],None)
                raise

    def update_plan(self,params):
        self.idle()
        if not self.chat or params.get('chat_id')!=self.chat['id']:raise ValueError('Выберите чат плана')
        task,warnings=self._recover_chat()
        if not task or not task.get('project_root'):raise ValueError('План доступен для IDE задачи')
        from agent.task_contract import PLAN_TOOL,set_plan
        from agent.tools import validate_tool_arguments
        args={'steps':params.get('steps'),'criteria':[]}
        validate_tool_arguments(PLAN_TOOL,args)
        result=set_plan(task,args,source='user')
        if not result['ok']:raise ValueError(result['error'])
        task['options']['checks_only']=False
        from agent.verifier import StageVerifier
        StageVerifier().refresh(task)
        if any(not n.get('advisory') and n.get('status')!='done' for n in task.get('plan_steps',[])):RunState(task).revise_plan()
        self.chat['task_checkpoint']=task
        warning=save_chat(self.chat,checkpoint=True)
        return {'ok':True,'task':task,'warnings':warnings+([warning] if warning else [])}

    def _persist_chat(self,*,checkpoint=False):
        warning=save_chat(self.chat,checkpoint=checkpoint)
        if warning:self._event('warning',text=warning)

    def _event(self,event_type,**data):
        self.emit({'event':event_type,'chat_id':self.chat['id'],'run_id':self.run_id,**data})

    def _prune_runs(self):
        selected=self.chat['id'] if self.chat else None
        for identity,run in list(self.runs.items()):
            if identity!=selected and not run.task_running and (not run.thread or not run.thread.is_alive()):
                self.runs.pop(identity)

    def selected_run(self):
        return self.runs.get(self.chat['id']) if self.chat else None

    def active_runs(self):
        return [{'chat_id':r.chat['id'],'run_id':r.run_id,'title':r.chat.get('title','Разговор'),
            'mode':r.chat.get('mode','chat'),'approval':bool(r.approval),
            'state':(r.chat.get('task_checkpoint') or {}).get('run_state','running')}
            for r in self.runs.values() if r.task_running]

    def resolve_approval(self,params):
        with self.lock:
            run=self.selected_run()
            if not run:raise ValueError('Выберите чат с ожидающим подтверждением')
            return run.resolve_approval(params)

    def cancel(self,params=None):
        with self.lock:
            self.discovery_cancel.set()
            run=self.selected_run()
            if params and params.get('run_id') and (not run or params['run_id']!=run.run_id):
                raise ValueError('Запуск изменился; остановка устарела')
            if run:return run.cancel()
            return {'ok':True}


    def shutdown(self):
        self.workspace_review.shutdown()
        with self.lock:
            self.closed=True
            self.inference.cancel()
            self.cancel_model_setup()
            runs=list(self.runs.values())
            for run in runs:run.cancel()
        for run in runs:
            if run.thread:run.thread.join(timeout=2)
        self.optional.shutdown()
        self.extensions.shutdown()
        self.assistant.shutdown()
        self.cancel_model_setup()
        self.cancel()
        if self.thread:
            self.thread.join(timeout=2)
        if self.discovery_thread:
            self.discovery_thread.join(timeout=1)
        if self.probe_thread:
            self.probe_thread.join(timeout=1)
