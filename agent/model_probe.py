"""A bounded, cancellable draft-configuration test without files or chat history."""
import asyncio
import json
import threading
import time

import httpx

from .model_discovery import _wait_cancelled


async def _request_probe(config, max_bytes,context=None):
    from .inference_scheduler import validate_model
    validate_model(context,config['base_url'],config['model'],config.get('api_protocol','chat'))
    settings = config['settings']
    payload = {'model': config['model'], 'messages': [
        {'role': 'system', 'content': 'Ты полезный собеседник. Дай краткий итоговый ответ.'},
        {'role': 'user', 'content': 'Сколько будет 17 + 25? Ответь только числом.'}],
        'temperature': settings['temperature'], 'top_p': settings['top_p'],
        'max_tokens': settings['max_tokens'], 'stream': False}
    from .request_budget import RequestBudget
    from .auto_budget import discover_profile,INITIAL_WINDOW
    budget=RequestBudget(settings.get('context_window',32768),settings.get('context_reserve_tokens',512),mode=settings.get('budget_mode','auto'))
    if budget.mode=='auto':
        profile=await discover_profile(config['base_url'],config['model'],config.get('api_key',''))
        if not profile.get('window'):profile={**profile,'window':INITIAL_WINDOW,'source':profile.get('source','Сервер')+' · временный автопрофиль'}
        budget.configure(profile)
    responses=config.get('api_protocol')=='responses'
    payload,_=budget.fit(payload,api_protocol='responses' if responses else 'chat')
    from .request_budget import prepare_model_request
    payload=prepare_model_request(payload,api_protocol='responses' if responses else 'chat')
    from .inference_scheduler import scheduled_request
    async with scheduled_request(context,'probe',budget.last_stats) as attempt:
        async with httpx.AsyncClient(timeout=min(settings['request_timeout'], 30), follow_redirects=False,event_hooks={'request':[attempt.on_http]}) as client:
            async with client.stream('POST', config['base_url'] + ('/responses' if responses else '/chat/completions'),
                    headers={'Authorization': 'Bearer ' + (config.get('api_key') or 'no-key')}, json=payload) as response:
                response.raise_for_status()
                raw = bytearray()
                async for chunk in response.aiter_bytes():
                    raw.extend(chunk)
                    if len(raw) > max_bytes:
                        raise ValueError('Слишком большой ответ проверки модели')
        try:
            data = json.loads(raw)
            text = ''.join(part.get('text','') for item in data.get('output',[]) if item.get('type')=='message' for part in item.get('content',[]) if part.get('type')=='output_text') if responses else data['choices'][0]['message']['content']
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise ValueError('Сервер не вернул корректный ответ Chat Completions') from exc
        attempt.observe(data.get('usage'),data.get('status') if responses else data['choices'][0].get('finish_reason'))
        if not isinstance(text, str) or not text.strip():
            raise ValueError('Сервер доступен, но модель не вернула текст в лимите теста. Для reasoning-модели увеличьте бюджет ответа или ограничьте рассуждения на сервере.')
        return {'ok': True, 'text': text.strip()[:1000]}


async def _probe(config, cancelled, timeout, max_bytes):
    request = asyncio.create_task(_request_probe(config, max_bytes,cancelled))
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
