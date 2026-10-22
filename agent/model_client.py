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
        stream = await self.owner.client.chat.completions.create(**params)
        async with stream:
            async for chunk in stream:
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
    def __init__(self, base_url, api_key, interrupted, timeout=180):
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
            return ModelStream(self, params)
        return self.result(self.submit(self.client.chat.completions.create(**params)))

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
