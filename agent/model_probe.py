"""A bounded, cancellable draft-configuration test without files or chat history."""
import asyncio
import json
import threading
import time

import httpx

from .model_discovery import _wait_cancelled


async def _request_probe(config, max_bytes):
    settings = config['settings']
    payload = {'model': config['model'], 'messages': [
        {'role': 'system', 'content': 'Ты полезный собеседник. Дай краткий итоговый ответ.'},
        {'role': 'user', 'content': 'Сколько будет 17 + 25? Ответь только числом.'}],
        'temperature': settings['temperature'], 'top_p': settings['top_p'],
        'max_tokens': settings['max_tokens'], 'stream': False}
    async with httpx.AsyncClient(timeout=min(settings['request_timeout'], 30), follow_redirects=False) as client:
        async with client.stream('POST', config['base_url'] + '/chat/completions',
                headers={'Authorization': 'Bearer ' + (config.get('api_key') or 'no-key')}, json=payload) as response:
            response.raise_for_status()
            raw = bytearray()
            async for chunk in response.aiter_bytes():
                raw.extend(chunk)
                if len(raw) > max_bytes:
                    raise ValueError('Слишком большой ответ проверки модели')
    try:
        data = json.loads(raw)
        text = data['choices'][0]['message']['content']
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise ValueError('Сервер не вернул корректный ответ Chat Completions') from exc
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Сервер доступен, но модель не вернула текст в лимите теста. Для reasoning-модели увеличьте бюджет ответа или ограничьте рассуждения на сервере.')
    return {'ok': True, 'text': text.strip()[:1000]}


async def _probe(config, cancelled, timeout, max_bytes):
    request = asyncio.create_task(_request_probe(config, max_bytes))
    cancel = asyncio.create_task(_wait_cancelled(cancelled))
    try:
        done, _ = await asyncio.wait({request, cancel}, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        if cancelled.is_set():
            raise ValueError('Проверка модели отменена')
        if request in done:
            return await request
        raise ValueError(f'Проверка не завершилась за {timeout:g} с. Модель может загружаться или рассуждать; попробуйте обычный Chat.')
    finally:
        request.cancel()
        cancel.cancel()
        await asyncio.gather(request, cancel, return_exceptions=True)


def probe_model(config, *, cancelled=None, timeout=30, max_bytes=100_000):
    if not config['model'].strip():
        raise ValueError('Выберите модель перед проверкой ответа')
    started = time.monotonic()
    result = asyncio.run(_probe(config, cancelled or threading.Event(), timeout, max_bytes))
    return {**result, 'elapsed_ms': round((time.monotonic() - started) * 1000)}
