"""Explicit bounded memory editing; model-generated memory uses the same store lock."""
import hashlib
import json

from agent.project_memory import FIELDS, LIST_FIELDS, MEMORY_LOCK, empty_memory, memory_path, save_project_memory
from agent.security import canonical_root


def editable_memory(data):
    if not isinstance(data, dict) or set(data) != set(FIELDS) | set(LIST_FIELDS):
        raise ValueError('Передайте все семь полей памяти без дополнительных ключей')
    for name, limit in FIELDS.items():
        value = data[name]
        if not isinstance(value,str) or len(value)>limit or '\x00' in value:
            raise ValueError(f'{name}: строка до {limit} символов без NUL')
    for name, (count,limit) in LIST_FIELDS.items():
        values = data[name]
        if not isinstance(values,list) or len(values)>count or any(not isinstance(v,str) or len(v)>limit or '\x00' in v for v in values):
            raise ValueError(f'{name}: до {count} строк по {limit} символов без NUL')
    return data


def read_memory(root):
    root = str(canonical_root(root))
    with MEMORY_LOCK:
        path = memory_path(root)
        if path.exists():
            with path.open('rb') as stream:
                raw = stream.read(200001)
            if len(raw)>200000:
                raise ValueError('Файл памяти превышает 200 КБ; исходник сохранён')
            data = json.loads(raw.decode('utf-8'))
            if not isinstance(data,dict):
                raise ValueError('Некорректный файл памяти; исходник сохранён')
        else:
            raw = b''
            data = empty_memory(root)
        fields = {name:data.get(name, [] if name in LIST_FIELDS else '') for name in (*FIELDS,*LIST_FIELDS)}
        editable_memory(fields)
        return {'ok':True,'memory':fields,'revision':hashlib.sha256(raw).hexdigest(),'root':root}


def write_memory(root, params):
    root = str(canonical_root(root))
    fields = editable_memory(params.get('memory'))
    with MEMORY_LOCK:
        current = read_memory(root)
        if params.get('revision') != current['revision']:
            raise ValueError('MEMORY_CHANGED: память изменилась. Перечитайте её перед сохранением; черновик сохранён в окне.')
        save_project_memory(root,fields)
        return read_memory(root)
