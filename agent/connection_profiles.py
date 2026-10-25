"""Named model presets containing public settings only; secrets stay in memory."""
import json
import uuid
from pathlib import Path
from .chat_store import APP_DIR,_atomic_write
from .model_preferences import validate_preferences


class ConnectionProfiles:
    def __init__(self,directory=None):
        self.file=Path(directory or APP_DIR)/'connections.json'

    def list(self):
        if not self.file.exists():return []
        if self.file.stat().st_size>1_000_000:raise ValueError('Каталог подключений слишком большой')
        data=json.loads(self.file.read_text(encoding='utf-8'))
        if not isinstance(data,list):raise ValueError('Каталог подключений повреждён')
        return data

    def save(self,params):
        records=self.list();name=params.get('name','').strip()
        if not 1<=len(name)<=100:raise ValueError('Название подключения: от 1 до 100 символов')
        identity=params.get('id') or uuid.uuid4().hex
        if not isinstance(identity,str) or len(identity)!=32 or any(c not in '0123456789abcdef' for c in identity):raise ValueError('Некорректный ID подключения')
        profile={'id':identity,'name':name,**validate_preferences(params)}
        others=[p for p in records if p['id']!=identity]
        if len(others)>=30:raise ValueError('Максимум 30 подключений')
        _atomic_write(self.file,others+[profile]);return profile

    def remove(self,identity):
        records=self.list()
        if not any(p['id']==identity for p in records):raise ValueError('Подключение не найдено')
        _atomic_write(self.file,[p for p in records if p['id']!=identity])
