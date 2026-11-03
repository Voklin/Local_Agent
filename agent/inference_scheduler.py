"""FIFO inference leases held until response close; ledger telemetry never stops local auto work."""
import asyncio
from contextlib import asynccontextmanager
import threading
import time
import uuid
from .run_registry import safe_usage,now


class InferenceScheduler:
    """One heavy generation per process, with cancellation-safe FIFO tickets and stale-owner protection."""
    def __init__(self):
        self.lock=threading.Lock();self.queue=[];self.active=None

    async def acquire(self,context,run_id='',purpose='agent'):
        """Wait without occupying the resource; cancellation removes the exact queued ticket."""
        ticket={'id':uuid.uuid4().hex,'run_id':run_id,'purpose':purpose,'at':time.monotonic()}
        with self.lock:self.queue.append(ticket)
        try:
            while True:
                if context and context.is_set():raise asyncio.CancelledError()
                with self.lock:
                    if self.active and self.active.get('needs_attention'):raise ValueError('Не подтверждено закрытие потока модели. Дождитесь закрытия соединения или перезапустите Neutral.')
                    if self.active is None and self.queue and self.queue[0] is ticket:
                        self.queue.pop(0);self.active=ticket
                        return ticket
                await asyncio.sleep(.025)
        except BaseException:
            self.release(ticket)
            raise

    def release(self,ticket):
        """Only the exact owner can release a lease; removing a cancelled waiter does not affect the owner."""
        with self.lock:
            self.queue=[item for item in self.queue if item is not ticket]
            if self.active is ticket:self.active=None

    def quarantine(self,ticket):
        """Block unsafe reuse after a failed SDK close until its owning HTTP client closes."""
        with self.lock:
            if self.active is ticket:self.active['needs_attention']=True

    def status(self):
        """Publish only queue/owner metadata, never request content or a claim about model residency."""
        with self.lock:return {'busy':self.active is not None,'kind':self.active['purpose'] if self.active else '',
            'run_id':self.active['run_id'] if self.active else '', 'waiting':len(self.queue),'resource_group':'shared-inference','managed_residency':False,'model_policy':'inherited-connection','limit':1,'needs_attention':bool(self.active and self.active.get('needs_attention'))}


SCHEDULER=InferenceScheduler()


def validate_model(context,base_url,model,api_protocol='chat'):
    """Apply the same fixed connection contract to SDK, probe and raw research paths."""
    run=getattr(context,'run_context',None)
    if run and (model,base_url.rstrip('/'),api_protocol)!=(run.model,run.base_url,run.api_protocol):
        raise ValueError('Run использует зафиксированные модель и подключение; смените их в новом запуске')


class InferenceAttempt:
    """A single scheduled SDK/HTTP attempt; physical HTTP is counted only by the transport hook."""
    def __init__(self,context,purpose,reservation=None,scheduler=None):
        self.context=context;self.run=getattr(context,'run_context',None);self.purpose=purpose
        self.scheduler=scheduler or SCHEDULER;self.ticket=None;self.id=None;self.http_attempts=0
        self.usage=None;self.outcome='unconfirmed';self.closed=False;self.reservation=reservation or {};self.started=time.monotonic()

    async def acquire(self):
        """Reserve a ledger row, then queue fairly; even cancelled waiters release their reservation."""
        if self.run:self.id=self.run.registry.attempt(self.run.id,self.purpose,self.reservation)
        try:
            self.ticket=await self.scheduler.acquire(self.context,self.run.id if self.run else '',self.purpose)
            if self.id:self.run.registry.update_attempt(self.id,phase='generating',queue_ms=round((time.monotonic()-self.started)*1000))
        except BaseException:
            self.finish('interrupted','cancelled_before_http')
            raise
        return self

    async def on_http(self,request):
        """HTTPX request hook counts only an inference POST, not discovery or a reservation."""
        if request.method!='POST' or not request.url.path.endswith(('/chat/completions','/responses')):return
        self.http_attempts+=1
        if self.id:self.run.registry.update_attempt(self.id,http_attempts=self.http_attempts,started_at=now())

    def observe(self,usage=None,terminal=None):
        """Retain the last cumulative usage frame once; missing usage remains unknown."""
        reported=safe_usage(usage)
        if reported is not None:self.usage=reported
        if terminal:self.outcome=str(terminal)[:50]

    def finish(self,state='finished',outcome=None,release=True):
        """Release after close, even on telemetry failure; never turn an unconfirmed stream into success."""
        if self.closed:return
        self.closed=True
        try:
            if self.id:self.run.registry.update_attempt(self.id,state=state,phase='closed',outcome=outcome or self.outcome,usage=self.usage,
                ended_at=now(),elapsed_ms=round((time.monotonic()-self.started)*1000))
        finally:
            if self.ticket:
                if release:self.scheduler.release(self.ticket)
                else:self.scheduler.quarantine(self.ticket)


@asynccontextmanager
async def scheduled_request(context,purpose,reservation=None):
    """Shared lease/telemetry contract for raw HTTP probe and readonly research callers."""
    attempt=await InferenceAttempt(context,purpose,reservation).acquire()
    try:yield attempt
    except BaseException as exc:
        attempt.finish('interrupted' if isinstance(exc,asyncio.CancelledError) else 'failed',type(exc).__name__)
        raise
    else:attempt.finish()
