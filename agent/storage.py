"""Versioned SQLite/WAL storage for conversations, checkpoints and call events.

Legacy JSON is copied once, checked inside the migration transaction and retained.
There is no silent fallback to old files after a database has become authoritative.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import threading
import zipfile

from .artifact_store import ArtifactStore, ARTIFACT_THRESHOLD


SCHEMA_VERSION = 3


def encode(value):
    """Serialize finite JSON without changing its user-visible values."""
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':'))


def valid_chat(value):
    """Validate legacy and new canonical conversation shape before writing."""
    identity = value.get('id') if isinstance(value, dict) else None
    return (isinstance(identity, str) and len(identity) == 32 and all(c in '0123456789abcdef' for c in identity)
            and isinstance(value.get('messages'), list) and all(isinstance(m, dict) for m in value['messages']))


class Storage:
    """Short-lived connections, FULL synchronous commits and reentrant transactions."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.path = self.directory / 'neutral.sqlite3'
        self.artifacts = ArtifactStore(self.directory / 'artifacts' / 'tool-results')
        self.local = threading.local()

    def _connect(self):
        """Open the profile database, enforce foreign keys and bounded lock waits."""
        self.directory.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        try:
            connection.row_factory = sqlite3.Row
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute('PRAGMA synchronous=FULL')
        except BaseException:
            connection.close()
            raise
        return connection

    @contextmanager
    def transaction(self):
        """Reserve the writer before reading state; nested calls reuse its transaction."""
        active = getattr(self.local, 'connection', None)
        if active is not None:
            yield active
            return
        connection = self._connect()
        try:
            connection.execute('BEGIN IMMEDIATE')
            self.local.connection = connection
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            self.local.connection = None
            connection.close()

    def ready(self):
        """Apply the schema and one-time copy of legacy chat/task/project files."""
        connection = self._connect()
        try:
            version = connection.execute('PRAGMA user_version').fetchone()[0]
            if version > SCHEMA_VERSION:
                raise ValueError('Хранилище создано более новой версией Neutral; обновите приложение')
            if version == SCHEMA_VERSION and connection.execute("SELECT 1 FROM meta WHERE key='legacy_migration'").fetchone():
                return self
            connection.execute('PRAGMA journal_mode=WAL')
        finally:
            connection.close()
        with self.transaction() as connection:
            version = connection.execute('PRAGMA user_version').fetchone()[0]
            if version > SCHEMA_VERSION:
                raise ValueError('Хранилище создано более новой версией Neutral; обновите приложение')
            if version == 0:
                for statement in (
                    'CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)',
                    'CREATE TABLE chats(id TEXT PRIMARY KEY,title TEXT NOT NULL,updated_at TEXT NOT NULL,mode TEXT NOT NULL,project_id TEXT NOT NULL,project_root TEXT NOT NULL,archived INTEGER NOT NULL,pinned INTEGER NOT NULL,data TEXT NOT NULL,summary TEXT NOT NULL)',
                    'CREATE INDEX chat_scope ON chats(mode,project_id,project_root,archived,pinned DESC,updated_at DESC)',
                    'CREATE TABLE messages(chat_id TEXT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,position INTEGER NOT NULL,data TEXT NOT NULL,PRIMARY KEY(chat_id,position))',
                    'CREATE TABLE tasks(chat_id TEXT PRIMARY KEY,data TEXT NOT NULL)',
                    'CREATE TABLE chat_tombstones(id TEXT PRIMARY KEY)',
                    'CREATE TABLE projects(id TEXT PRIMARY KEY,data TEXT NOT NULL)',
                    'CREATE TABLE migration_sources(path TEXT PRIMARY KEY,sha256 TEXT,kind TEXT NOT NULL,items INTEGER NOT NULL,status TEXT NOT NULL,error TEXT)',
                    'CREATE TABLE journal_imports(chat_id TEXT NOT NULL,journal_id TEXT NOT NULL,sha256 TEXT,events INTEGER NOT NULL,warning TEXT,PRIMARY KEY(chat_id,journal_id))',
                    'CREATE TABLE journal_events(sequence INTEGER PRIMARY KEY,chat_id TEXT NOT NULL,journal_id TEXT NOT NULL,data TEXT NOT NULL)',
                    'CREATE INDEX journal_identity ON journal_events(chat_id,journal_id,sequence)',
                    'CREATE TABLE search_entries(rowid INTEGER PRIMARY KEY,chat_id TEXT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,position INTEGER NOT NULL,original TEXT NOT NULL,folded TEXT NOT NULL,UNIQUE(chat_id,position))',
                ):
                    connection.execute(statement)
                try:
                    connection.execute("CREATE VIRTUAL TABLE history_fts USING fts5(folded,content='search_entries',content_rowid='rowid',tokenize='trigram')")
                except sqlite3.OperationalError:
                    connection.execute("INSERT INTO meta VALUES('search_backend','substring')")
                else:
                    for statement in (
                        "CREATE TRIGGER search_insert AFTER INSERT ON search_entries BEGIN INSERT INTO history_fts(rowid,folded) VALUES(new.rowid,new.folded); END",
                        "CREATE TRIGGER search_delete AFTER DELETE ON search_entries BEGIN INSERT INTO history_fts(history_fts,rowid,folded) VALUES('delete',old.rowid,old.folded); END",
                        "CREATE TRIGGER search_update AFTER UPDATE ON search_entries BEGIN INSERT INTO history_fts(history_fts,rowid,folded) VALUES('delete',old.rowid,old.folded); INSERT INTO history_fts(rowid,folded) VALUES(new.rowid,new.folded); END",
                    ):
                        connection.execute(statement)
                    connection.execute("INSERT INTO meta VALUES('search_backend','fts5-trigram')")
                connection.execute('PRAGMA user_version=1')
            if version < 2:
                connection.execute("CREATE TABLE workspace_snapshots(sequence INTEGER PRIMARY KEY,id TEXT NOT NULL UNIQUE,group_id TEXT NOT NULL,chat_id TEXT NOT NULL,journal_id TEXT NOT NULL,root TEXT NOT NULL,status TEXT NOT NULL,data TEXT NOT NULL,rollback_progress TEXT NOT NULL DEFAULT '[]',rollback_error TEXT NOT NULL DEFAULT '',revision INTEGER NOT NULL DEFAULT 0)")
                connection.execute('CREATE INDEX snapshot_scope ON workspace_snapshots(chat_id,root,group_id,sequence)')
                connection.execute('PRAGMA user_version=2')
            if version < 3:
                connection.execute('CREATE TABLE runs(id TEXT PRIMARY KEY,chat_id TEXT NOT NULL,parent_id TEXT,updated_at TEXT NOT NULL,data TEXT NOT NULL,state TEXT NOT NULL)')
                connection.execute('CREATE INDEX run_chat ON runs(chat_id,updated_at DESC)')
                connection.execute('CREATE INDEX run_parent ON runs(parent_id)')
                connection.execute('CREATE INDEX run_state ON runs(state)')
                connection.execute('CREATE TABLE inference_attempts(id TEXT PRIMARY KEY,run_id TEXT NOT NULL REFERENCES runs(id),data TEXT NOT NULL)')
                connection.execute('CREATE INDEX attempt_run ON inference_attempts(run_id)')
                connection.execute('PRAGMA user_version=3')
            migrated = connection.execute("SELECT value FROM meta WHERE key='legacy_migration'").fetchone()
            if migrated is None:
                self._migrate(connection)
        return self

    def pack(self, text):
        """Replace a large tool value at rest with an authenticated content address."""
        if isinstance(text, str) and len(text.encode('utf-8')) > ARTIFACT_THRESHOLD:
            return {'_neutral_artifact_v1': self.artifacts.put(text)}
        return text

    def unpack(self, value):
        """Hydrate internal references before returning canonical history or receipts."""
        if isinstance(value, dict) and set(value) == {'_neutral_artifact_v1'}:
            return self.artifacts.get(value['_neutral_artifact_v1'])
        return value

    def _source(self, connection, path, kind, items, error=None):
        """Record the original checksum and verified object/message count."""
        connection.execute('INSERT INTO migration_sources VALUES(?,?,?,?,?,?)',
            (path.relative_to(self.directory).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest(), kind, items,
             'skipped' if error else 'verified', error))

    def _migrate(self, connection):
        """Copy valid inputs without touching them; preserve malformed data with warnings."""
        chats = self.directory / 'chats'
        tasks = self.directory / 'tasks'
        chat_count = message_count = 0
        for path in sorted(chats.iterdir()) if chats.exists() else []:
            if path.suffix != '.json' or len(path.stem) != 32 or any(c not in '0123456789abcdef' for c in path.stem):
                continue
            try:
                value = json.loads(path.read_text(encoding='utf-8'))
                if not valid_chat(value) or value['id'] != path.stem:
                    raise ValueError('Некорректная структура чата')
            except (ValueError, UnicodeError) as exc:
                self._source(connection, path, 'chat', 0, str(exc)[:250])
                continue
            self.write_chat(connection, value, checkpoint=True)
            self._source(connection, path, 'chat', len(value['messages']))
            chat_count += 1
            message_count += len(value['messages'])
        for path in sorted(tasks.glob('*.json')):
            try:
                value = json.loads(path.read_text(encoding='utf-8'))
                if not isinstance(value, dict) or not isinstance(value.get('chat_id'), str) or not value['chat_id']:
                    raise ValueError('Некорректная контрольная точка')
                expected = hashlib.sha256(value['chat_id'].encode('utf-8', errors='replace')).hexdigest()[:32]
                if path.stem != expected:
                    raise ValueError('Имя checkpoint не соответствует chat_id')
            except (ValueError, UnicodeError) as exc:
                self._source(connection, path, 'task', 0, str(exc)[:250])
                continue
            # The embedded checkpoint is the historical recovery authority.
            connection.execute('INSERT OR IGNORE INTO tasks VALUES(?,?)', (value['chat_id'], encode(value)))
            self._source(connection, path, 'task', 1)
        path = self.directory / 'projects.json'
        if path.exists():
            try:
                values = json.loads(path.read_text(encoding='utf-8'))
                if not isinstance(values, list) or any(not isinstance(v, dict) or not isinstance(v.get('id'), str) for v in values):
                    raise ValueError('Некорректный каталог проектов')
                if len({v['id'] for v in values}) != len(values):
                    raise ValueError('Повтор идентификатора проекта')
            except (ValueError, UnicodeError) as exc:
                # Projects cannot be silently replaced by an empty catalogue.
                raise ValueError('Миграция проектов остановлена; исходный каталог сохранён') from exc
            for value in values:
                connection.execute('INSERT INTO projects VALUES(?,?)', (value['id'], encode(value)))
            self._source(connection, path, 'project', len(values))
        actual_chats = connection.execute('SELECT count(*) FROM chats').fetchone()[0]
        actual_messages = connection.execute('SELECT count(*) FROM messages').fetchone()[0]
        if (actual_chats, actual_messages) != (chat_count, message_count):
            raise ValueError('Проверка количества чатов/сообщений при миграции не пройдена')
        for source in connection.execute('SELECT path,sha256 FROM migration_sources'):
            if hashlib.sha256((self.directory/source['path']).read_bytes()).hexdigest() != source['sha256']:
                raise ValueError('Исходные данные менялись во время миграции; закройте старую версию и повторите запуск')
        connection.execute("INSERT INTO meta VALUES('legacy_migration',?)", (encode({'version': 1, 'chats': chat_count, 'messages': message_count}),))

    def _search_entry(self, connection, chat_id, position, text):
        """Update only changed searchable title/user/assistant text, never tool payloads."""
        if not isinstance(text, str) or not text:
            connection.execute('DELETE FROM search_entries WHERE chat_id=? AND position=?', (chat_id, position))
        else:
            connection.execute('INSERT INTO search_entries(chat_id,position,original,folded) VALUES(?,?,?,?) ON CONFLICT(chat_id,position) DO UPDATE SET original=excluded.original,folded=excluded.folded WHERE original!=excluded.original', (chat_id, position, text, text.casefold()))

    def write_chat(self, connection, chat, *, checkpoint=False):
        """Commit metadata, changed messages, search index and explicit checkpoint together."""
        if not valid_chat(chat):
            raise ValueError('Некорректная структура чата')
        metadata = {key: value for key, value in chat.items() if key not in ('messages', 'task_checkpoint', 'storage_warning')}
        mode = chat.get('mode', 'ide' if chat.get('project_root') else 'chat')
        connection.execute('INSERT INTO chats VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,updated_at=excluded.updated_at,mode=excluded.mode,project_id=excluded.project_id,project_root=excluded.project_root,archived=excluded.archived,pinned=excluded.pinned,data=excluded.data,summary=excluded.summary',
            (chat['id'], str(chat.get('title','')), str(chat.get('updated_at','')), mode, chat.get('project_id',''), str(chat.get('project_root','')), chat.get('archived') is True, chat.get('pinned') is True, encode(metadata), encode({key:value for key,value in metadata.items() if key in ('id','title','created_at','updated_at','project_root','model','mode','project_id','pinned','archived')})))
        self._search_entry(connection, chat['id'], -1, chat.get('title',''))
        for position, message in enumerate(chat['messages']):
            stored = dict(message)
            if message.get('role') == 'tool':
                stored['content'] = self.pack(message.get('content'))
            connection.execute('INSERT INTO messages VALUES(?,?,?) ON CONFLICT(chat_id,position) DO UPDATE SET data=excluded.data WHERE data!=excluded.data', (chat['id'], position, encode(stored)))
            self._search_entry(connection, chat['id'], position, message.get('content') if message.get('role') in ('user','assistant') else None)
        connection.execute('DELETE FROM messages WHERE chat_id=? AND position>=?', (chat['id'], len(chat['messages'])))
        connection.execute('DELETE FROM search_entries WHERE chat_id=? AND position>=?', (chat['id'], len(chat['messages'])))
        task = chat.get('task_checkpoint')
        if isinstance(task, dict):
            if checkpoint:
                connection.execute('INSERT INTO tasks VALUES(?,?) ON CONFLICT(chat_id) DO UPDATE SET data=excluded.data', (chat['id'], encode(task)))
            else:
                connection.execute('INSERT OR IGNORE INTO tasks VALUES(?,?)', (chat['id'], encode(task)))

    def load_chat(self, chat_id):
        """Read a consistent metadata/messages/checkpoint snapshot without a writer lock."""
        connection = self._connect()
        try:
            connection.execute('BEGIN')
            row = connection.execute('SELECT data FROM chats WHERE id=?', (chat_id,)).fetchone()
            if row is None:
                bad = connection.execute("SELECT error FROM migration_sources WHERE path=? AND status='skipped'", ('chats/'+str(chat_id)+'.json',)).fetchone()
                if bad:
                    raise ValueError('Данные чата повреждены; исходный JSON сохранён для восстановления')
                return None
            value = json.loads(row['data'])
            messages = []
            for row in connection.execute('SELECT data FROM messages WHERE chat_id=? ORDER BY position', (chat_id,)):
                message = json.loads(row['data'])
                if message.get('role') == 'tool':
                    message['content'] = self.unpack(message.get('content'))
                messages.append(message)
            value['messages'] = messages
            task = self.checkpoint(connection, chat_id)
            if task is not None:
                value['task_checkpoint'] = task
            return value
        finally:
            connection.close()

    def checkpoint(self, connection, chat_id):
        """Never mistake a rejected legacy checkpoint for a fresh, effect-free chat."""
        row = connection.execute('SELECT data FROM tasks WHERE chat_id=?', (str(chat_id),)).fetchone()
        if row:
            from .verification_evidence import migrate_evidence
            return migrate_evidence(json.loads(row['data']))
        key = hashlib.sha256(str(chat_id).encode('utf-8', errors='replace')).hexdigest()[:32]
        bad = connection.execute("SELECT 1 FROM migration_sources WHERE path=? AND kind='task' AND status='skipped'", ('tasks/'+key+'.json',)).fetchone()
        if bad:
            raise ValueError('Контрольная точка задачи повреждена; исходник сохранён. Восстановите его из резервной копии перед продолжением чата.')
        return None

    def catalog(self, *, root=None, mode=None, project_id=None, archived=None):
        """Read indexed metadata only; no transcript or legacy JSON is opened."""
        clauses, values = [], []
        for key, value in (('project_root', root), ('mode', mode), ('project_id', project_id), ('archived', archived)):
            if value is not None:
                clauses.append(key+'=?')
                values.append(value)
        connection = self._connect()
        try:
            rows = connection.execute('SELECT summary AS data FROM chats'+(' WHERE '+' AND '.join(clauses) if clauses else '')+' ORDER BY pinned DESC,updated_at DESC', values)
            items = []
            for row in rows:
                data = json.loads(row['data'])
                # Drafts/recovery fragments may be large; never expose them in the catalogue.
                items.append({**{key: str(data.get(key,'')) for key in ('id','title','created_at','updated_at','project_root','model')},
                    'mode':data.get('mode','ide' if data.get('project_root') else 'chat'),'project_id':data.get('project_id',''),
                    'pinned':data.get('pinned') is True,'archived':data.get('archived') is True})
            warnings = [f"Не перенесён {row['path']}: {row['error']}; исходный файл сохранён." for row in connection.execute("SELECT path,error FROM migration_sources WHERE status='skipped'")]
            return {'chats': items, 'warnings': warnings}
        finally:
            connection.close()

    def search(self, query, *, root, mode, project_id, archived=False, limit=300):
        """Substring search with FTS5 trigrams; short queries use scoped SQL fallback."""
        query = query.strip().casefold()
        if not query:
            result = self.catalog(root=root, mode=mode, project_id=project_id, archived=archived)
            result['chats'] = result['chats'][:limit]
            return result
        connection = self._connect()
        try:
            backend = connection.execute("SELECT value FROM meta WHERE key='search_backend'").fetchone()[0]
            indexed = backend == 'fts5-trigram' and len(query) >= 3
            joins = ' JOIN search_entries s ON s.chat_id=c.id'
            if indexed:
                joins += ' JOIN history_fts f ON f.rowid=s.rowid'
                condition = 'history_fts MATCH ?'
                term = '"'+query.replace('"','""')+'"'
            else:
                condition = 'instr(s.folded,?)>0'
                term = query
            rows = connection.execute('SELECT c.id,min(s.position) AS position FROM chats c'+joins+' WHERE c.project_root=? AND c.mode=? AND c.project_id=? AND c.archived=? AND '+condition+' GROUP BY c.id ORDER BY c.pinned DESC,c.updated_at DESC LIMIT ?', (str(root),mode,project_id,archived,term,limit)).fetchall()
            # Only matched metadata and snippets are read, never the full chat corpus.
            items = []
            for row in rows:
                data = json.loads(connection.execute('SELECT summary AS data FROM chats WHERE id=?',(row['id'],)).fetchone()[0])
                item = {key:data.get(key,'') for key in ('id','title','created_at','updated_at','project_root','model','mode','project_id')}
                item.update(pinned=data.get('pinned') is True,archived=data.get('archived') is True)
                if row['position'] >= 0:
                    text = connection.execute('SELECT original FROM search_entries WHERE chat_id=? AND position=?',(row['id'],row['position'])).fetchone()[0]
                    index = text.casefold().find(query)
                    item['snippet'] = text[max(0,index-30):index+130]
                items.append(item)
            warnings = [f"Не перенесён {row['path']}; исходный файл сохранён." for row in connection.execute("SELECT path FROM migration_sources WHERE status='skipped'")]
            return {'chats':items,'warnings':warnings}
        finally:
            connection.close()

    def report(self):
        """Expose non-secret migration/health metadata for diagnostics and backups."""
        connection = self._connect()
        try:
            return {'version': connection.execute('PRAGMA user_version').fetchone()[0],
                    'integrity': connection.execute('PRAGMA quick_check').fetchone()[0],
                    'counts': {table:connection.execute('SELECT count(*) FROM '+table).fetchone()[0] for table in ('chats','messages','projects')},
                    'migration': json.loads(connection.execute("SELECT value FROM meta WHERE key='legacy_migration'").fetchone()[0]),
                    'sources': [dict(row) for row in connection.execute('SELECT * FROM migration_sources')],
                    'search_backend': connection.execute("SELECT value FROM meta WHERE key='search_backend'").fetchone()[0]}
        finally:
            connection.close()

    def backup(self, destination, *, cancelled=None):
        """Export a verified online SQLite snapshot, artifacts and original JSON.

        Restore with Neutral closed into a fresh profile, never over a live WAL
        database. The archive is replaced only after ZIP verification and fsync.
        """
        def check(*_args):
            if cancelled and cancelled.is_set():raise ValueError('Резервное копирование отменено или достигнут лимит')
        def copy(archive,path,name):
            check();info=zipfile.ZipInfo.from_file(path,name);info.compress_type=archive.compression
            with path.open('rb') as source,archive.open(info,'w') as target:
                while True:
                    check();block=source.read(65536)
                    if not block:break
                    target.write(block)
        check();destination = Path(destination)
        if destination.suffix.casefold() != '.zip':
            raise ValueError('Резервная копия должна иметь расширение .zip')
        if destination.resolve().is_relative_to(self.directory.resolve()):
            raise ValueError('Сохраните копию за пределами рабочего каталога данных')
        with tempfile.TemporaryDirectory(prefix='neutral_backup_') as temporary:
            snapshot = Path(temporary) / 'neutral.sqlite3'
            source = self._connect()
            target = sqlite3.connect(snapshot)
            try:
                source.backup(target,pages=128,progress=check)
            finally:
                target.close()
                source.close()
            connection = sqlite3.connect(snapshot)
            references = {}
            try:
                for table in ('messages', 'journal_events'):
                    for (data,) in connection.execute('SELECT data FROM '+table):
                        check()
                        value = json.loads(data)
                        content = value.get('content') if table == 'messages' else value.get('result')
                        if isinstance(content, dict) and set(content) == {'_neutral_artifact_v1'}:
                            reference = content['_neutral_artifact_v1']
                            self.artifacts.get(reference)
                            references[reference['sha256']] = reference
                snapshot_refs={}
                for (data,) in connection.execute('SELECT data FROM workspace_snapshots'):
                    check()
                    value=json.loads(data)
                    for collection in ('before','after'):
                        for state in value.get(collection,{}).values():
                            if state.get('artifact'):snapshot_refs[state['artifact']['sha256']]=state['artifact']
                from .artifact_store import ArtifactStore
                snapshot_blobs=ArtifactStore(self.directory/'artifacts'/'workspace-snapshots')
                for reference in snapshot_refs.values():snapshot_blobs.get(reference)
                if connection.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                    raise ValueError('Резервная копия SQLite не прошла проверку')
            finally:
                connection.close()
            descriptor, pending = tempfile.mkstemp(prefix='neutral_backup_', suffix='.tmp', dir=destination.parent)
            os.close(descriptor)
            try:
                with zipfile.ZipFile(pending, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                    copy(archive,snapshot, 'neutral.sqlite3')
                    for digest in references:
                        path = self.artifacts.path(digest)
                        copy(archive,path, path.relative_to(self.directory).as_posix())
                    for digest in snapshot_refs:
                        path=snapshot_blobs.path(digest)
                        copy(archive,path,path.relative_to(self.directory).as_posix())
                    legacy = [self.directory/'projects.json']
                    legacy.extend((self.directory/'chats').glob('*.json'))
                    legacy.extend((self.directory/'tasks').glob('*.json'))
                    legacy.extend((self.directory/'tasks'/'journals').glob('*.jsonl'))
                    for path in legacy:
                        if path.is_file():
                            copy(archive,path, 'legacy/'+path.relative_to(self.directory).as_posix())
                            if path.suffix == '.jsonl':
                                # Inactive epochs are imported lazily. Keep their
                                # recovery location usable after a ZIP restore too.
                                copy(archive,path, path.relative_to(self.directory).as_posix())
                    archive.writestr('backup.json', encode({'version':1,'schema_version':SCHEMA_VERSION,
                        'restore':'Close Neutral. Extract into a fresh profile; legacy/ contains original migration sources.',
                        'artifacts':len(references)}))
                with zipfile.ZipFile(pending) as archive:
                    for name in archive.namelist():
                        with archive.open(name) as source:
                            while source.read(65536):check()
                with open(pending, 'r+b') as stream:
                    os.fsync(stream.fileno())
                check();os.replace(pending, destination)
            finally:
                if os.path.exists(pending):
                    os.unlink(pending)
        return {'path':str(destination),'artifacts':len(references),'committed':True}
