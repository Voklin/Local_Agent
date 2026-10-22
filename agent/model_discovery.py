"""Bounded, cancellable discovery of OpenAI-compatible model IDs."""
from __future__ import annotations
import asyncio
import json
import threading

import httpx


async def _request_models(config, max_bytes):
    """Read a bounded response and validate its models-list shape."""
    headers = {'Authorization': 'Bearer ' + (config.get('api_key') or 'no-key')}
    async with httpx.AsyncClient(timeout=5.0, follow_redirects=False) as client:
        async with client.stream('GET', config['base_url'] + '/models', headers=headers) as response:
            response.raise_for_status()
            raw = bytearray()
            async for chunk in response.aiter_bytes():
                raw.extend(chunk)
                if len(raw) > max_bytes:
                    raise ValueError('Слишком большой ответ списка моделей')
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ValueError('Сервер вернул некорректный JSON списка моделей') from exc
    if not isinstance(data, dict) or not isinstance(data.get('data'), list):
        raise ValueError('Сервер должен вернуть объект с массивом data')
    return {'ok': True, 'models': [item['id'][:300] for item in data['data'][:500]
                                  if isinstance(item, dict) and isinstance(item.get('id'), str) and item['id'].strip()]}


async def _wait_cancelled(cancelled):
    """Observe cross-thread cancellation without blocking the asyncio loop."""
    while not cancelled.is_set():
        await asyncio.sleep(0.05)


async def _discover(config, timeout, max_bytes, cancelled):
    """Enforce one overall deadline, including headers and a trickling body."""
    request = asyncio.create_task(_request_models(config, max_bytes))
    cancel = asyncio.create_task(_wait_cancelled(cancelled))
    try:
        done, _ = await asyncio.wait({request, cancel}, timeout=timeout,
                                     return_when=asyncio.FIRST_COMPLETED)
        if cancelled.is_set():
            raise ValueError('Загрузка списка моделей отменена')
        if request in done:
            return await request
        raise ValueError('Время ожидания списка моделей истекло')
    finally:
        request.cancel()
        cancel.cancel()
        await asyncio.gather(request, cancel, return_exceptions=True)


def discover_models(config, *, timeout=5.0, max_bytes=1_000_000, cancelled=None):
    """Synchronous worker entry point; close the request on cancellation/deadline."""
    cancelled = cancelled or threading.Event()
    if cancelled.is_set():
        raise ValueError('Загрузка списка моделей отменена')
    return asyncio.run(_discover(dict(config), timeout, max_bytes, cancelled))
