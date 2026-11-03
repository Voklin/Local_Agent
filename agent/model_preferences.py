"""Validate and atomically persist non-secret endpoint and generation settings."""
import json
import math
from copy import deepcopy
import os
import tempfile
from pathlib import Path
from urllib.parse import urlparse

PREFERENCES_FILE = Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData/Local') / 'LocalCodingAgent/model-preferences.json'
SETTING_LIMITS = {
    'temperature': (0.2, 0, 2, False),
    'top_p': (1.0, 0.01, 1, False),
    'max_tokens': (8192, 64, 32768, True),
    'max_context_chars': (80000, 12000, 500000, True),
    'context_window': (32768, 512, 1048576, True),
    'context_reserve_tokens': (512, 128, 8192, True),
    'request_timeout': (180, 5, 600, True),
    'max_agent_turns': (200, 1, 500, True),
    'max_runtime_minutes': (180, 1, 1440, True),
}
DEFAULTS = {'api_protocol':'chat','tool_protocol':'native', 'base_url': 'http://127.0.0.1:1234/v1', 'model': '',
            'settings': {**{key: rule[0] for key, rule in SETTING_LIMITS.items()},'memory_updates':'on_change','budget_mode':'auto','paid_budget':{'enabled':False,'amount':1.0,'input_per_million':0.0,'output_per_million':0.0,'currency':'USD'}}}


def validate_settings(settings):
    if not isinstance(settings, dict):
        raise ValueError('Параметры генерации должны быть объектом')
    result = {}
    budget_mode=settings.get('budget_mode','auto')
    if budget_mode not in ('auto','manual'):raise ValueError('Управление контекстом: auto или manual')
    for key, (default, minimum, maximum, integer) in SETTING_LIMITS.items():
        value = settings.get(key, default)
        if budget_mode=='auto' and key not in ('temperature','top_p'):
            if isinstance(value,bool) or not isinstance(value,(int,float)) or (isinstance(value,float) and not math.isfinite(value)) or not minimum<=value<=maximum or (integer and value!=int(value)):
                value=default
        if isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value, float) and not math.isfinite(value)):
            raise ValueError(f'{key}: укажите конечное число от {minimum} до {maximum}')
        if not minimum <= value <= maximum or (integer and value != int(value)):
            raise ValueError(f'{key}: допустимо {"целое " if integer else ""}число от {minimum} до {maximum}')
        result[key] = int(value) if integer else float(value)
    mode=settings.get('memory_updates','on_change')
    if mode not in ('off','on_change','always'):raise ValueError('Обновление памяти: off, on_change или always')
    result['memory_updates']=mode
    result['budget_mode']=budget_mode
    from .run_policy import validate_spending
    result['paid_budget']=validate_spending(settings.get('paid_budget'))
    if budget_mode=='manual' and 'context_window' in settings and result['max_tokens']+result['context_reserve_tokens']>=result['context_window']:
        raise ValueError('Ответ и запас должны быть меньше окна контекста модели')
    return result


def validate_preferences(params):
    base_url = str(params.get('base_url', '')).strip().rstrip('/')
    parsed = urlparse(base_url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Укажите HTTP(S) URL сервера, например http://127.0.0.1:1234/v1')
    if len(base_url) > 2000:
        raise ValueError('Слишком длинный URL сервера')
    parsed.port  # Validate port syntax/range before persisting it.
    protocol = params.get('tool_protocol', 'native')
    if protocol not in ('native','json'):
        raise ValueError('Протокол инструментов: native или json')
    api_protocol=params.get('api_protocol','chat')
    if api_protocol not in ('chat','responses'):raise ValueError('API: Chat Completions или Responses')
    return {'api_protocol':api_protocol,'tool_protocol':protocol, 'base_url': base_url, 'model': str(params.get('model', '')).strip()[:300],
            'settings': validate_settings(params.get('settings', {}))}


def connection_key(previous, public, params, key='api_key', endpoint='base_url'):
    """Never reuse a prior endpoint's secret, including a stale form's explicit copy."""
    old = str(previous.get(key, ''))[:4000]
    incoming = str(params.get(key, old))[:4000]
    changed = previous.get(endpoint) != public.get(endpoint)
    # A different fresh key may be entered after changing the address. An identical
    # old key requires a separate save at the new endpoint, making consent explicit.
    return '' if changed and incoming == old else incoming


def load_preferences():
    try:
        data = json.loads(PREFERENCES_FILE.read_text(encoding='utf-8'))
        return validate_preferences(data) if isinstance(data, dict) else deepcopy(DEFAULTS)
    except (OSError, ValueError, TypeError):
        return deepcopy(DEFAULTS)


def save_preferences(params):
    preferences = validate_preferences(params)
    PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='model-', suffix='.tmp', dir=PREFERENCES_FILE.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(preferences, stream, ensure_ascii=False, indent=2)
        os.replace(temporary, PREFERENCES_FILE)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return preferences
