"""One bounded background maintenance job; bridge dispatch never waits for its work."""
import threading
from agent.operation_context import OperationContext


class BackgroundJob:
    def __init__(self):
        self.lock=threading.Lock();self.thread=None;self.context=None;self.closed=False

    def start(self, work, respond, timeout=240):
        """Reject duplicate work and correlate completion through the supplied RPC callback."""
        with self.lock:
            if self.closed or (self.thread and self.thread.is_alive()):raise ValueError('Фоновая операция уже выполняется или приложение закрывается')
            context=OperationContext(timeout);self.context=context
            def run():
                try:
                    result=work(context)
                    if context.is_set() and result.get('committed') is not True:raise ValueError('Фоновая операция отменена или достигнут лимит')
                    response={'ok':True,**result}
                except Exception as exc:response={'ok':False,'error':str(exc)[:500]}
                finally:
                    with self.lock:
                        if self.context is context:self.context=None
                respond(response)
            self.thread=threading.Thread(target=run,daemon=True,name='storage-maintenance');self.thread.start()

    def cancel(self):
        """Request cancellation; the slot stays occupied until the worker exits."""
        with self.lock:
            if self.context:self.context.set()
        return {'ok':True}

    def shutdown(self):
        """Close admission, cancel and wait briefly without blocking process shutdown forever."""
        with self.lock:self.closed=True
        self.cancel()
        if self.thread:self.thread.join(2)
