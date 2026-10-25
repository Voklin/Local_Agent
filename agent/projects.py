"""Named workspaces group conversations without deleting or moving project files."""
from copy import deepcopy
from pathlib import Path
import json
import threading
import uuid
from .chat_store import APP_DIR, _atomic_write, _now


class ProjectStore:
    def __init__(self, directory=None):
        self.path=Path(directory or APP_DIR)/'projects.json'
        self.lock=threading.RLock()

    def list(self):
        if not self.path.exists():return []
        with self.path.open('rb') as stream:raw=stream.read(1_000_001)
        if len(raw)>1_000_000:raise ValueError('Каталог проектов слишком велик')
        data=json.loads(raw)
        if not isinstance(data,list) or any(not isinstance(p,dict) or not isinstance(p.get('id'),str) for p in data):
            raise ValueError('Каталог проектов повреждён; исходные данные сохранены')
        return data

    def get(self, project_id):
        if project_id=='':return {'id':'','name':'Личное пространство','root':'','instructions':''}
        project=next((p for p in self.list() if p['id']==project_id),None)
        if project is None:raise ValueError('Проект не найден')
        return deepcopy(project)

    def save(self, params):
        with self.lock:
            values=self.list();project_id=params.get('id')
            old=self.get(project_id) if project_id else None
            name=params.get('name',old.get('name') if old else '')
            instructions=params.get('instructions',old.get('instructions','') if old else '')
            if not isinstance(name,str) or not 1<=len(name.strip())<=100 or '\x00' in name:raise ValueError('Название проекта: 1–100 символов')
            if not isinstance(instructions,str) or len(instructions)>6000 or '\x00' in instructions:raise ValueError('Инструкции проекта: до 6000 символов')
            root=params.get('root',old.get('root','') if old else '')
            if not isinstance(root,str):raise ValueError('Некорректная папка проекта')
            if root:
                target=Path(root).expanduser().resolve(strict=True)
                if not target.is_dir():raise ValueError('Выберите существующую папку')
                root=str(target)
            if not old and len(values)>=100:raise ValueError('Достигнут предел 100 проектов')
            project={'id':project_id or uuid.uuid4().hex,'name':name.strip(),'root':root,'instructions':instructions,
                     'created_at':old['created_at'] if old else _now(),'updated_at':_now(),
                     'pinned':params.get('pinned',old.get('pinned',False) if old else False) is True}
            _atomic_write(self.path,[p for p in values if p['id']!=project['id']]+[project])
            return project

    def remove(self, project_id):
        with self.lock:
            self.get(project_id)
            if not project_id:raise ValueError('Личное пространство нельзя удалить')
            _atomic_write(self.path,[p for p in self.list() if p['id']!=project_id])
