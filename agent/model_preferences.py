"""Persist only the non-secret model endpoint and selected model."""
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import urlparse

PREFERENCES_FILE = Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData/Local') / 'LocalCodingAgent/model-preferences.json'
DEFAULTS = {'base_url': 'http://127.0.0.1:1234/v1', 'model': ''}


def validate_preferences(params):
    base_url = str(params.get('base_url', '')).strip().rstrip('/')
    parsed = urlparse(base_url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Укажите HTTP(S) URL сервера, например http://127.0.0.1:1234/v1')
    if len(base_url) > 2000:
        raise ValueError('Слишком длинный URL сервера')
    parsed.port  # Validate port syntax/range before persisting it.
    return {'base_url': base_url, 'model': str(params.get('model', '')).strip()[:300]}


def load_preferences():
    try:
        data = json.loads(PREFERENCES_FILE.read_text(encoding='utf-8'))
        return validate_preferences(data) if isinstance(data, dict) else dict(DEFAULTS)
    except (OSError, ValueError, TypeError):
        return dict(DEFAULTS)


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
