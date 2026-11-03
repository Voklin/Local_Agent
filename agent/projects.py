"""Named workspaces group conversations without deleting or moving project files."""
from copy import deepcopy
from pathlib import Path
import json
import threading
import uuid
from .chat_store import APP_DIR, _now
from .storage import Storage, encode


class ProjectStore:
    def __init__(self, directory=None):
        self.path=Path(directory or APP_DIR)/'projects.json'
        self.lock=threading.RLock()
        self.database=Storage(self.path.parent).ready()

    def _database(self):
        """Projects share the same profile transaction store as their conversations."""
        return self.database

    def list(self):
        database = self._database()
        with database.transaction() as connection:
            return [json.loads(row['data']) for row in connection.execute('SELECT data FROM projects ORDER BY rowid')]

    def get(self, project_id):
        if project_id=='':return {'id':'','name':'Личное пространство','root':'','instructions':''}
        project=next((p for p in self.list() if p['id']==project_id),None)
        if project is None:raise ValueError('Проект не найден')
        return deepcopy(project)

    def save(self, params):
        with self.lock, self._database().transaction() as connection:
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
            connection.execute('INSERT INTO projects VALUES(?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data', (project['id'], encode(project)))
            return project

    def remove(self, project_id):
        with self.lock, self._database().transaction() as connection:
            self.get(project_id)
            if not project_id:raise ValueError('Личное пространство нельзя удалить')
            connection.execute("UPDATE chats SET project_id='',data=json_set(data,'$.project_id',''),summary=json_set(summary,'$.project_id','') WHERE project_id=?", (project_id,))
            connection.execute('DELETE FROM projects WHERE id=?', (project_id,))
