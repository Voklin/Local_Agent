"""Cancellable async HTTP requests exposed to the synchronous agent loop."""
from __future__ import annotations
import asyncio
import concurrent.futures
import queue
import threading


class ModelCancelled(Exception):
    pass


class ModelStream:
    def __init__(self, owner, params):
        self.owner = owner
        self.chunks = queue.Queue(maxsize=64)
        self.future = owner.submit(self._produce(params))

    async def _produce(self, params):
        from .responses_adapter import response_request, ResponseEvents
        responses = self.owner.api_protocol == 'responses'
        request = response_request(params,self.owner.response_cache) if responses else params
        endpoint = self.owner.client.responses if responses else self.owner.client.chat.completions
        stream = await self.owner.request(endpoint,request)
        adapter = ResponseEvents(self.owner.response_cache) if responses else None
        async with stream:
            async for chunk in stream:
                if adapter:
                    chunk=adapter.translate(chunk)
                    if chunk is None:continue
                while self.chunks.full():
                    await asyncio.sleep(0.01)
                self.chunks.put_nowait(chunk)

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
        from openai import AsyncOpenAI
        self.interrupted = interrupted
        self.loop = asyncio.new_event_loop()
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key or 'no-key', timeout=timeout, max_retries=0)
        self.lock = threading.Lock()
        self.pending = set()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True, name='model-http')
        self.thread.start()

    def check_cancelled(self):
        if self.interrupted.is_set():
            raise ModelCancelled('Остановлено пользователем.')

    def submit(self, coroutine):
        with self.lock:
            future = asyncio.run_coroutine_threadsafe(coroutine, self.loop)
            self.pending.add(future)
            if self.interrupted.is_set():
                future.cancel()
        future.add_done_callback(self._forget)
        return future

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
        if params.get('stream'):
            if self.tool_protocol == 'json' and params.get('tools'):
                from .json_tools import prepare_json_request, JsonToolStream
                request, allowed, choice = prepare_json_request(params)
                return JsonToolStream(ModelStream(self, request), allowed, choice)
            return ModelStream(self, params)
        async def complete():
            if self.api_protocol=='responses':
                from .responses_adapter import response_request,response_completion
                return response_completion(await self.request(self.client.responses,response_request(params,self.response_cache)))
            return await self.request(self.client.chat.completions,params)
        return self.result(self.submit(complete()))

    async def request(self,endpoint,params):
        """Retry only before a response is received; never replay partial streams."""
        from openai import APIConnectionError,APIStatusError
        for attempt in range(3):
            try:return await endpoint.create(**params)
            except (APIConnectionError,APIStatusError) as exc:
                retry=isinstance(exc,APIConnectionError) or getattr(exc,'status_code',0) in (429,500,502,503,504)
                if not retry or attempt==2:raise
                await asyncio.sleep(.4*(2**attempt))

    def cancel(self):
        with self.lock:
            pending = tuple(self.pending)
        for future in pending:
            future.cancel()

    def close(self):
        async def shutdown():
            tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.client.close()
        self.cancel()
        future = asyncio.run_coroutine_threadsafe(shutdown(), self.loop)
        try:
            future.result(timeout=3)
        finally:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join(timeout=1)
            if not self.thread.is_alive():
                self.loop.close()
