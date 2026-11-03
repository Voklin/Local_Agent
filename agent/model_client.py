"""Cancellable async HTTP requests exposed to the synchronous agent loop."""
from __future__ import annotations
import asyncio
import concurrent.futures
import queue
import threading
import time
from copy import deepcopy
from .request_budget import RequestBudget, prepare_model_request


class ModelCancelled(Exception):
    pass


class SourceContextApprovalError(ValueError):
    """Pause without transmitting unapproved or changed selected source data."""


class ScheduledStream:
    """Keep the inference lease until the SDK response stream has actually closed."""
    def __init__(self,source,attempt):
        self.source=source;self.attempt=attempt;self.closed=False;self.cleanup=None

    async def __aenter__(self):
        try:await self.source.__aenter__()
        except BaseException as exc:
            await self.close(exc);raise
        return self

    def __aiter__(self):
        return self.source.__aiter__()

    async def __aexit__(self,kind,error,traceback):
        await self.close(error)

    async def close(self,error=None):
        """Finish telemetry only after response cleanup; errors still release the scheduler."""
        if self.closed:return
        self.closed=True
        cancelled=None;failure=None
        self.cleanup=asyncio.create_task(self.source.close())
        try:
            while not self.cleanup.done():
                try:await asyncio.shield(self.cleanup)
                except asyncio.CancelledError as exc:cancelled=exc
            self.cleanup.result()
        except BaseException as exc:failure=exc;raise
        finally:
            outcome=error or failure or cancelled
            self.attempt.finish('interrupted' if isinstance(outcome,asyncio.CancelledError) else 'failed' if outcome else 'finished',type(outcome).__name__ if outcome else None,release=failure is None)
        if cancelled and not error:raise cancelled


class ModelStream:
    def __init__(self, owner, params, original=None,purpose=None):
        self.owner = owner
        self.purpose=purpose or getattr(owner,'request_purpose','agent')
        self.chunks = queue.Queue(maxsize=64)
        self.future = owner.submit(self._produce(params,original))

    async def _produce(self, params,original=None):
        from .responses_adapter import ResponseEvents
        responses = self.owner.api_protocol == 'responses'
        request = params
        endpoint = self.owner.client.responses if responses else self.owner.client.chat.completions
        stream = await self.owner.request(endpoint,request,original,purpose=self.purpose)
        last_usage=None
        try:
            adapter = ResponseEvents(self.owner.response_cache) if responses else None
            async with stream:
                async for chunk in stream:
                    usage=getattr(getattr(chunk,'response',None),'usage',None) if responses else getattr(chunk,'usage',None)
                    if usage:last_usage=usage
                    stream.attempt.observe(usage)
                    if adapter:
                        chunk=adapter.translate(chunk)
                        if chunk is None:continue
                    terminal=next((c.finish_reason for c in getattr(chunk,'choices',[]) if c.finish_reason),None)
                    stream.attempt.observe(terminal=terminal)
                    while self.chunks.full():
                        await asyncio.sleep(0.01)
                    self.chunks.put_nowait(chunk)
        finally:
            try:self.owner.record_usage(last_usage)
            finally:await stream.close()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            self.owner.check_cancelled()
            try:
                return self.chunks.get(timeout=0.05)
            except queue.Empty:
                if self.future.done():
                    self.owner.result(self.future)
                    raise StopIteration

    def close(self):
        self.future.cancel()


class ModelClient:
    def __init__(self, base_url, api_key, interrupted, timeout=180, tool_protocol='native',api_protocol='chat'):
        self.tool_protocol = tool_protocol
        self.api_protocol = api_protocol
        self.response_cache = {}
        self.budget=RequestBudget()
        self.usage_totals={'input_tokens':0,'output_tokens':0,'requests_reported':0}
        self.request_count=0
        self.json_repair_count=0
        self.context_root=None
        self.source_approval=None
        self.run_context=getattr(interrupted,'run_context',None);self.request_purpose='agent';self._attempt=None
        self.base_url=base_url;self.api_key=api_key;self.tokenizer=None;self.budget_prepared=False
        self.profile_resolved=False;self.budget_refresh_at=0
        from openai import AsyncOpenAI,DefaultAsyncHttpxClient
        from .context_builder import local_context_endpoint
        self.interrupted = interrupted
        self.loop = asyncio.new_event_loop()
        # Approval binds the configured recipient; redirects/proxies cannot change that recipient.
        transport={'http_client':DefaultAsyncHttpxClient(trust_env=False,follow_redirects=False,timeout=timeout)}
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key or 'no-key', timeout=timeout, max_retries=0,**transport)
        self.client._client.event_hooks.setdefault('request',[]).append(self._http_attempt)
        self.lock = threading.Lock()
        self.pending = set()
        self.workers=set()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True, name='model-http')
        self.thread.start()

    def check_cancelled(self):
        if self.interrupted.is_set():
            raise ModelCancelled('Остановлено пользователем.')

    async def _http_attempt(self,request):
        """Count real inference transport attempts, including explicit retry and JSON repair."""
        if self._attempt:await self._attempt.on_http(request)

    def prepare_budget(self,settings,model,budget):
        """Resolve the loaded local context once per task without loading or reconfiguring a model."""
        self.budget=budget
        if budget.mode!='auto':return
        if self.budget_prepared and (self.profile_resolved or not self.request_count or time.monotonic()-self.budget_refresh_at<2):return
        from .auto_budget import discover_profile,LoadedTokenizer,INITIAL_WINDOW
        profile=self.result(self.submit(discover_profile(self.base_url,model,self.api_key,force=self.budget_prepared)))
        self.budget_refresh_at=time.monotonic()
        self.profile_resolved=bool(profile.get('instances') or 'загруженн' in profile.get('source','') or profile.get('provider')=='remote')
        if not profile.get('window'):
            profile={**profile,'window':INITIAL_WINDOW,'source':profile.get('source','Сервер')+' · временный автопрофиль'}
        if profile.get('provider')=='lmstudio' and not self.api_key and not self.tokenizer:
            self.tokenizer=LoadedTokenizer.connect(self.base_url,profile.get('instances',[]),self.interrupted)
        budget.configure(profile,self.tokenizer.count if self.tokenizer else None)
        self.budget_prepared=True

    def submit(self, coroutine):
        with self.lock:
            future = asyncio.run_coroutine_threadsafe(self._tracked(coroutine), self.loop)
            self.pending.add(future)
            if self.interrupted.is_set():
                future.cancel()
        future.add_done_callback(self._forget)
        return future

    async def _tracked(self,coroutine):
        """Track owners separately from SDK cleanup tasks so shutdown cannot cancel close halfway through."""
        task=asyncio.current_task();self.workers.add(task)
        try:return await coroutine
        finally:self.workers.discard(task)

    def _forget(self, future):
        with self.lock:
            self.pending.discard(future)

    def result(self, future):
        while True:
            self.check_cancelled()
            try:
                return future.result(timeout=0.05)
            except concurrent.futures.TimeoutError:
                continue
            except concurrent.futures.CancelledError as exc:
                raise ModelCancelled('Остановлено пользователем.') from exc

    def create(self, **params):
        self.check_cancelled()
        from .inference_scheduler import validate_model
        validate_model(self.interrupted,self.base_url,params.get('model'),self.api_protocol)
        from .context_builder import PACK_MARKER,local_context_endpoint,pack_summary
        if not local_context_endpoint(self.base_url) and not self.source_approval and params.get('messages'):
            params={**params,'messages':[m for m in params['messages'] if PACK_MARKER not in m]}
        if params.get('stream'):
            self.context_pack_summary=pack_summary(params.get('messages',[]))
            if not local_context_endpoint(self.base_url) and not self.source_approval:self.context_pack_summary['status']='remote_disabled'
        request=prepare_model_request(params,self.tool_protocol,self.api_protocol,self.response_cache)
        self.budget.check(request,params.get('tools',()))
        self.request_count+=1
        if params.get('stream'):
            if self.tool_protocol == 'json' and params.get('tools'):
                from .json_tools import JsonToolStream
                allowed={tool['function']['name'] for tool in params['tools']}
                choice=params.get('tool_choice','auto')
                return JsonToolStream(ModelStream(self, request,params), allowed, choice,
                    repair=lambda text,error,attempt:self._repair_json(params,text,error,attempt),canonical=True)
            return ModelStream(self, request,params)
        async def complete():
            if self.api_protocol=='responses':
                from .responses_adapter import response_completion
                response=await self.request(self.client.responses,request,params)
                self.record_usage(getattr(response,'usage',None))
                return response_completion(response)
            response=await self.request(self.client.chat.completions,request,params)
            self.record_usage(getattr(response,'usage',None))
            return response
        return self.result(self.submit(complete()))

    def _repair_json(self, original, rejected, error, attempt):
        """Regenerate an unexecuted malformed reply, fitted through the normal budget gate."""
        self.check_cancelled()
        params=deepcopy(original)
        params['messages']+=[{'role':'assistant','content':rejected[:4000]},
            {'role':'user','content':('Protocol correction '+str(attempt)+'/2. The previous response was rejected; '
                'NO tool from that response was executed. Regenerate your next action for the original task. '
                'Return ONE neutral.action.v1 tool or final JSON object, with no text outside it. '
                'Do not quote/extract examples as commands. Error: '+error)}]
        fitted,_=self.budget.fit(params,tool_protocol=self.tool_protocol,api_protocol=self.api_protocol,cache=self.response_cache)
        request=prepare_model_request(fitted,self.tool_protocol,self.api_protocol,self.response_cache)
        self.budget.check(request,fitted.get('tools',()))
        self.check_cancelled()
        self.request_count+=1;self.json_repair_count+=1
        return ModelStream(self,request,fitted,purpose='json_repair')

    def record_usage(self, usage):
        if usage is None:return
        values=usage if isinstance(usage,dict) else usage.model_dump()
        self.budget.observe_usage(values)
        incoming=values.get('input_tokens',values.get('prompt_tokens'))
        outgoing=values.get('output_tokens',values.get('completion_tokens'))
        if any(type(value) is not int or value<0 for value in (incoming,outgoing)):return
        self.usage_totals['input_tokens']+=incoming
        self.usage_totals['output_tokens']+=outgoing
        self.usage_totals['requests_reported']+=1

    async def request(self,endpoint,params,original=None,purpose=None):
        """Retry only before a response is received; never replay partial streams."""
        from openai import APIConnectionError,APIStatusError
        from .context_builder import PACK_MARKER,local_context_endpoint,pack_summary,validate_context
        transport_original=original;omit_stream_options=False
        for attempt in range(3):
            try:
                if transport_original and self.context_root:
                    from .project_knowledge import has_memory_projection,validate_memory_projection
                    if has_memory_projection(transport_original.get('messages',[])):
                        messages=await asyncio.to_thread(validate_memory_projection,transport_original['messages'],self.context_root)
                        transport_original={**transport_original,'messages':messages}
                        params=prepare_model_request(transport_original,self.tool_protocol,self.api_protocol,self.response_cache)
                        if omit_stream_options:params.pop('stream_options',None)
                        self.budget.check(params,transport_original.get('tools',()))
                if transport_original and any(PACK_MARKER in m for m in transport_original.get('messages',[])):
                    messages=transport_original['messages'];before=pack_summary(messages)
                    if (local_context_endpoint(self.base_url) or self.source_approval) and self.context_root:
                        messages=await asyncio.to_thread(validate_context,messages,self.context_root,self.check_cancelled,self.interrupted)
                    else:messages=[m for m in messages if PACK_MARKER not in m]
                    transport_original={**transport_original,'messages':messages}
                    params=prepare_model_request(transport_original,self.tool_protocol,self.api_protocol,self.response_cache)
                    if omit_stream_options:params.pop('stream_options',None)
                    self.budget.check(params,transport_original.get('tools',()))
                    self.context_pack_summary=pack_summary(messages)
                    self.context_pack_summary['omitted']+=max(0,len(before['sources'])-len(self.context_pack_summary['sources']))
                    if not local_context_endpoint(self.base_url) and any(PACK_MARKER in m for m in messages):
                        from .context_builder import source_proposal
                        recipient=self.base_url
                        proposal=source_proposal(recipient,self.api_protocol,transport_original)
                        self.context_pack_summary['status']='waiting_approval'
                        allowed=await asyncio.to_thread(self.source_approval,proposal)
                        self.check_cancelled()
                        if not allowed:
                            self.context_pack_summary['status']='rejected'
                            raise SourceContextApprovalError('Передача выбранных исходников отклонена. Запрос модели не отправлен.')
                        checked=await asyncio.to_thread(validate_context,messages,self.context_root,self.check_cancelled,self.interrupted)
                        if recipient!=self.base_url or source_proposal(self.base_url,self.api_protocol,{**transport_original,'messages':checked})!=proposal:
                            self.context_pack_summary=pack_summary(checked,status='changed')
                            raise SourceContextApprovalError('Источники или получатель изменились после предпросмотра. Продолжите задачу для нового подтверждения.')
                        self.context_pack_summary['status']='approved'
                self.check_cancelled()
                from .inference_scheduler import InferenceAttempt
                lease=await InferenceAttempt(self.interrupted,purpose or self.request_purpose,self.budget.last_stats).acquire()
                try:
                    from .inference_scheduler import validate_model
                    validate_model(self.interrupted,self.base_url,params.get('model'),self.api_protocol)
                    # Queueing may outlive file permissions or the approved source snapshot.
                    if transport_original and any(PACK_MARKER in m for m in transport_original.get('messages',[])):
                        from .context_builder import source_proposal
                        before_queue=source_proposal(self.base_url,self.api_protocol,transport_original)
                        checked=await asyncio.to_thread(validate_context,transport_original['messages'],self.context_root,self.check_cancelled,self.interrupted)
                        after_queue={**transport_original,'messages':checked}
                        if not local_context_endpoint(self.base_url) and source_proposal(self.base_url,self.api_protocol,after_queue)!=before_queue:
                            raise SourceContextApprovalError('Источники изменились во время ожидания модели. Продолжите для нового подтверждения.')
                        transport_original=after_queue;params=prepare_model_request(after_queue,self.tool_protocol,self.api_protocol,self.response_cache)
                        if omit_stream_options:params.pop('stream_options',None)
                        self.budget.check(params,after_queue.get('tools',()))
                        self.context_pack_summary=pack_summary(checked)
                    if transport_original and self.context_root:
                        from .project_knowledge import has_memory_projection,validate_memory_projection
                        if has_memory_projection(transport_original.get('messages',[])):
                            messages=await asyncio.to_thread(validate_memory_projection,transport_original['messages'],self.context_root)
                            transport_original={**transport_original,'messages':messages}
                            params=prepare_model_request(transport_original,self.tool_protocol,self.api_protocol,self.response_cache)
                            if omit_stream_options:params.pop('stream_options',None)
                            self.budget.check(params,transport_original.get('tools',()))
                    self.check_cancelled();self._attempt=lease
                    response=await endpoint.create(**params)
                    if params.get('stream'):return ScheduledStream(response,lease)
                    choices=getattr(response,'choices',[])
                    lease.observe(getattr(response,'usage',None),getattr(choices[0],'finish_reason',None) if choices else getattr(response,'status',None))
                    lease.finish();return response
                except BaseException as error:
                    lease.finish('interrupted' if isinstance(error,asyncio.CancelledError) else 'failed',type(error).__name__)
                    raise
            except (APIConnectionError,APIStatusError) as exc:
                from .run_policy import capacity_failure,ModelCapacityError
                if capacity_failure(exc):raise ModelCapacityError('Сервер модели сообщил нехватку памяти. Повтор запроса остановлен; освободите память или уменьшите загрузку модели на сервере и продолжите задачу. Neutral не управляет резидентными моделями внешнего сервера.') from None
                from .auto_budget import context_rejection
                window=context_rejection(exc)
                if window and self.budget.mode=='auto' and original is not None and attempt<2:
                    self.profile_resolved=True
                    self.budget.learn_rejection(window)
                    fitted,_=self.budget.fit(transport_original or original,tool_protocol=self.tool_protocol,api_protocol=self.api_protocol,cache=self.response_cache)
                    transport_original=fitted
                    params=prepare_model_request(fitted,self.tool_protocol,self.api_protocol,self.response_cache)
                    continue
                if attempt<2 and isinstance(exc,APIStatusError) and getattr(exc,'status_code',0) in (400,422) and 'stream_options' in params and 'stream_options' in str(exc).lower():
                    # Compatibility fallback is allowed only before a response
                    # stream exists, and only for this optional telemetry field.
                    params={k:v for k,v in params.items() if k!='stream_options'}
                    omit_stream_options=True
                    continue
                retry=isinstance(exc,APIConnectionError) or getattr(exc,'status_code',0) in (429,500,502,503,504)
                if not retry or attempt==2:raise
                await asyncio.sleep(.4*(2**attempt))

    def cancel(self):
        with self.lock:
            pending = tuple(self.pending)
        for future in pending:
            future.cancel()

    def close(self):
        if self.tokenizer:
            try:self.tokenizer.close()
            except Exception:pass
            self.tokenizer=None
        async def shutdown():
            tasks = [task for task in self.workers if task is not asyncio.current_task()]
            for task in tasks:
                if not task.cancelling():task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.client.close()
            if self._attempt and self._attempt.ticket:self._attempt.scheduler.release(self._attempt.ticket)
        self.cancel()
        future = asyncio.run_coroutine_threadsafe(shutdown(), self.loop)
        try:
            future.result(timeout=3)
        finally:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join(timeout=1)
            if not self.thread.is_alive():
                self.loop.close()
