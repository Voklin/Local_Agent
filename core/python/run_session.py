"""An execution owner whose chat and callbacks never follow UI selection."""
from copy import deepcopy
import threading

from agent.operation_context import InferenceGate
from core.python.session_service import SessionService
from core.python.task_execution import TaskExecution


class RunSession(TaskExecution):
    def __init__(self, owner, chat):
        self.lock=owner.lock
        self.emit=lambda event:owner.emit(event)
        self.engine_factory=owner.engine_factory
        self.workspace_adapter=owner.workspace_adapter
        self.config=deepcopy(owner.config)
        self.companion_config=deepcopy(owner.companion_config)
        self.project_id=owner.project_id
        self.sessions=SessionService(self.lock,self.idle,lambda mode:self.config['model'])
        self.sessions.project_id=self.project_id
        self.sessions.chat=chat
        self.inference=InferenceGate();self.inference_lease=None
        self.registry=owner.registry
        self.projects=owner.projects;self.extensions=owner.extensions
        self.assistant=owner.assistant;self.desktop=owner.desktop;self.optional=owner.optional
        self.thread=None;self.engine=None;self.run_context=None;self.run_id=None
        self.task_running=False;self.approval=None;self.approval_event=None;self.external_pending=None
        self.event_seq=0
        self.discovery_cancel=threading.Event()
        self.handoff_pending=None;self.delegation_origin=deepcopy(owner.delegation_origin) if owner.delegation_origin and owner.delegation_origin.get('target_chat')==chat['id'] else None
        self.stream_turn=None;self.stream_buffer='';self.stream_text=''
        self.last_stream_emit=0;self.stream_persist_at=0;self.stream_timer=None;self.draft_timer=None

    @property
    def chat(self):
        return self.sessions.chat

    def idle(self):
        if self.task_running:raise ValueError('В этом чате уже выполняется задача')

    def _recover_chat(self):
        return self.sessions.recover()

    def select_chat(self,*args,**kwargs):
        raise ValueError('Запуск должен получить выбранный чат до начала исполнения')

    def begin(self,root,params):
        self.inference_lease=self.inference.begin('задача')
        try:return self._start(root,params)
        except BaseException:
            if self.run_context and not self.run_context.closed:self.run_context.finish('failed')
            self.inference.end(self.inference_lease.id);self.inference_lease=None
            self.task_running=False
            if self.stream_timer:self.stream_timer.cancel()
            if self.draft_timer:self.draft_timer.cancel()
            raise

    def view(self):
        """The bridge lock serializes this snapshot with callbacks and finalization."""
        chat=deepcopy(self.chat)
        if self.stream_text and self.stream_turn is not None:
            chat['messages'].append({'role':'assistant','content':self.stream_text,
                'message_id':f'{self.run_id}:{self.stream_turn}','streaming':True})
        return {'chat':chat,'task':deepcopy(self.chat.get('task_checkpoint')),
            'active_run':{'run_id':self.run_id,'chat_id':self.chat['id']},
            'approval':deepcopy(self.approval_event) if self.approval else None,'event_seq':self.event_seq}
