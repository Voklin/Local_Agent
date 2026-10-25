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
    'request_timeout': (180, 5, 600, True),
    'max_agent_turns': (200, 1, 500, True),
    'max_runtime_minutes': (180, 1, 1440, True),
}
DEFAULTS = {'api_protocol':'chat','tool_protocol':'native', 'base_url': 'http://127.0.0.1:1234/v1', 'model': '',
            'settings': {key: rule[0] for key, rule in SETTING_LIMITS.items()}}


def validate_settings(settings):
    if not isinstance(settings, dict):
        raise ValueError('Параметры генерации должны быть объектом')
    result = {}
    for key, (default, minimum, maximum, integer) in SETTING_LIMITS.items():
        value = settings.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value, float) and not math.isfinite(value)):
            raise ValueError(f'{key}: укажите конечное число от {minimum} до {maximum}')
        if not minimum <= value <= maximum or (integer and value != int(value)):
            raise ValueError(f'{key}: допустимо {"целое " if integer else ""}число от {minimum} до {maximum}')
        result[key] = int(value) if integer else float(value)
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
