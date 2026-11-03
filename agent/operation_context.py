"""A shared deadline/cancellation contract, compatible with Event-based adapters."""
import threading
import time
import uuid
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass


class OperationContext:
    def __init__(self, timeout=None, parent=None):
        self.event=threading.Event();self.parent=parent;self.deadline=None
        self.lock=threading.RLock();self.pause_depth=0;self.pause_started=None
        self.set_deadline(timeout)

    def set_deadline(self,timeout):
        if timeout is not None:
            with self.lock:
                deadline=(self.pause_started if self.pause_depth else time.monotonic())+max(0,float(timeout))
                self.deadline=min(self.deadline,deadline) if self.deadline is not None else deadline

    @contextmanager
    def approval_wait(self):
        """Freeze execution deadlines during a human decision; cancellation remains immediate."""
        parent_wait=self.parent.approval_wait() if hasattr(self.parent,'approval_wait') else nullcontext()
        with parent_wait:
            with self.lock:
                if not self.pause_depth:self.pause_started=time.monotonic()
                self.pause_depth+=1
            try:
                yield
            finally:
                with self.lock:
                    self.pause_depth-=1
                    if not self.pause_depth:
                        if self.deadline is not None:self.deadline+=time.monotonic()-self.pause_started
                        self.pause_started=None

    def remaining(self,default=None):
        values=[]
        with self.lock:
            if self.deadline is not None:
                values.append(max(0,self.deadline-(self.pause_started if self.pause_depth else time.monotonic())))
        if hasattr(self.parent,'remaining'):
            remaining=self.parent.remaining()
            if remaining is not None:values.append(remaining)
        return min(values) if values else default

    def is_set(self):
        return self.event.is_set() or bool(self.parent and self.parent.is_set()) or self.remaining(1)<=0

    def set(self):
        self.event.set()

    def wait(self,timeout=None):
        end=time.monotonic()+timeout if timeout is not None else None
        while not self.is_set():
            remaining=(end-time.monotonic()) if end is not None else .05
            if remaining<=0:return False
            self.event.wait(min(.05,remaining,self.remaining(.05)))
        return True

    def child(self,timeout=None):
        return OperationContext(timeout,self)


@dataclass
class InferenceLease:
    id:str
    kind:str
    context:OperationContext


class InferenceGate:
    """One actual model operation; stale completion cannot release a newer owner."""
    def __init__(self):
        self.lock=threading.Lock();self.active=None

    def begin(self,kind,timeout=None):
        with self.lock:
            if self.active:raise ValueError('Уже выполняется запрос модели: '+self.active.kind+'. Дождитесь завершения или остановите его.')
            self.active=InferenceLease(uuid.uuid4().hex,kind,OperationContext(timeout))
            return self.active

    def end(self,identity):
        with self.lock:
            if self.active and self.active.id==identity:self.active=None

    def cancel(self):
        with self.lock:
            if self.active:self.active.context.set()

    def status(self):
        with self.lock:
            return {'busy':self.active is not None,'kind':self.active.kind if self.active else '', 'limit':1}
