"""Separate persistent model, personality and voice profile for Miya."""
from copy import deepcopy
import json
from pathlib import Path

from .chat_store import APP_DIR, _atomic_write
from .model_preferences import DEFAULTS, validate_preferences

PROFILE_FILE = APP_DIR / 'companion.json'
DEFAULT_PROFILE = {**deepcopy(DEFAULTS), 'persona':'Дружелюбная, спокойная, внимательная помощница. Отвечает кратко и по делу.',
                   'auto_delegate':True, 'voice':'', 'rate':0, 'volume':70, 'auto_speak':False,
                   'stt_url':'http://127.0.0.1:8080/inference', 'stt_model':'whisper-1', 'stt_language':'ru'}


def validate_profile(params):
    """Allow bounded user preferences and keep API keys out of persisted data."""
    result = {**deepcopy(DEFAULT_PROFILE), **validate_preferences(params)}
    for name, maximum in (('persona',6000),('voice',300),('stt_model',300),('stt_language',16)):
        value = params.get(name, DEFAULT_PROFILE[name])
        if not isinstance(value,str) or len(value)>maximum or '\x00' in value:
            raise ValueError(f'Некорректное поле профиля: {name}')
        result[name] = value
    for name, minimum, maximum in (('rate',-5,5),('volume',0,100)):
        value = params.get(name,DEFAULT_PROFILE[name])
        if isinstance(value,bool) or not isinstance(value,int) or not minimum<=value<=maximum:
            raise ValueError(f'Некорректное поле профиля: {name}')
        result[name]=value
    result['auto_speak']=params.get('auto_speak',False) is True
    result['auto_delegate']=params.get('auto_delegate',True) is True
    url=params.get('stt_url',DEFAULT_PROFILE['stt_url'])
    result['stt_url']=validate_preferences({'base_url':url})['base_url']
    return result


def load_profile():
    """Load an independent profile; older installations begin with no Miya model."""
    try:
        return validate_profile(json.loads(PROFILE_FILE.read_text('utf-8')))
    except (OSError,ValueError,TypeError):
        return deepcopy(DEFAULT_PROFILE)


def save_profile(params):
    """Atomically save public settings, excluding model/STT API keys."""
    profile=validate_profile(params)
    _atomic_write(PROFILE_FILE,profile)
    return profile
