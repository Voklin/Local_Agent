"""Durable before/after evidence for approved file tools and guarded user rollback."""
from __future__ import annotations
import base64
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import uuid

from . import task_store
from .artifact_store import ArtifactStore
from .security import canonical_root
from .storage import Storage, encode
from .workspace_edits import mutation_path, file_revision, parent_revision


FILE_TOOLS=frozenset({'write_file','patch_file','rename_file','delete_file','create_directory'})


def fingerprint(value):
    """Compare kind, bytes and filesystem identity without the storage reference."""
    return {key:item for key,item in value.items() if key!='artifact'}


class SnapshotStore:
    """Operation receipts grouped into bounded, conflict-aware undo segments."""

    def __init__(self, root, chat_id, journal_id=''):
        self.root=canonical_root(root)
        self.chat_id=str(chat_id);self.journal_id=str(journal_id)
        self.database=Storage(Path(task_store.TASK_DIR).parent).ready()
        self.blobs=ArtifactStore(self.database.directory/'artifacts'/'workspace-snapshots')

    def capture(self, relative):
        """Capture only regular files up to 1 MB and real directories inside the root."""
        path=mutation_path(self.root,relative)
        parent=parent_revision(path.parent) if path.parent.is_dir() else None
        if not path.exists():return {'kind':'missing','parent':parent}
        if path.is_dir():return {'kind':'directory','identity':parent_revision(path),'parent':parent}
        raw,revision=file_revision(path)
        return {'kind':'file',**revision,'parent':parent,'mode':stat.S_IMODE(path.stat().st_mode),
            'artifact':self.blobs.put(base64.b64encode(raw).decode('ascii'))}

    def _rows(self, connection, group_id):
        rows=connection.execute('SELECT * FROM workspace_snapshots WHERE group_id=? AND chat_id=? AND root=? ORDER BY sequence', (group_id,self.chat_id,str(self.root))).fetchall()
        if not rows:raise ValueError('Снимок не принадлежит выбранному чату и проекту')
        return rows

    def _aggregate(self, rows):
        before={};after={}
        for row in rows:
            if row['status']!='applied':continue
            data=json.loads(row['data'])
            for path,value in data['before'].items():before.setdefault(path,value)
            after.update(data['after'])
        return before,after

    def prepare(self, operation, args, preview, message_index, call_id):
        """Commit originals before started; split a segment across intervening manual edits."""
        if operation=='create_directory':paths=preview['snapshot']['directories']
        else:paths=[preview['path']]+([preview['destination']] if operation=='rename_file' else [])
        before={path:self.capture(path) for path in paths}
        expected={}
        for path in paths:
            kind='directory' if operation=='create_directory' else 'missing' if operation=='delete_file' or (operation=='rename_file' and path==preview['path']) else 'file'
            expected[path]={'kind':kind}
            if kind=='file':
                raw=(args['content'] if operation=='write_file' else preview['content']).encode('utf-8') if operation!='rename_file' else None
                expected[path]['sha256']=hashlib.sha256(raw).hexdigest() if raw is not None else before[preview['path']]['sha256']
        with self.database.transaction() as connection:
            latest=connection.execute('SELECT group_id FROM workspace_snapshots WHERE chat_id=? AND journal_id=? AND root=? ORDER BY sequence DESC LIMIT 1',(self.chat_id,self.journal_id,str(self.root))).fetchone()
            group=latest['group_id'] if latest else uuid.uuid4().hex
            if latest:
                rows=self._rows(connection,group);_,previous=self._aggregate(rows)
                if (any(row['status'] not in ('applied','failed') for row in rows) or len(set(previous)|set(before))>80 or
                    any(path in previous and fingerprint(previous[path])!=fingerprint(value) for path,value in before.items())):
                    group=uuid.uuid4().hex
            identity=uuid.uuid4().hex
            data={'operation':operation,'before':before,'expected':expected,'after':{},
                  'message_index':message_index,'call_id':call_id,'root_identity':parent_revision(self.root)}
            connection.execute('INSERT INTO workspace_snapshots(id,group_id,chat_id,journal_id,root,status,data) VALUES(?,?,?,?,?,?,?)',
                (identity,group,self.chat_id,self.journal_id,str(self.root),'prepared',encode(data)))
        return identity,group

    def finish(self, identity, result):
        """Never adopt unexpected post-edit bytes as agent-owned, reversible output."""
        with self.database.transaction() as connection:
            row=connection.execute('SELECT * FROM workspace_snapshots WHERE id=? AND chat_id=?',(identity,self.chat_id)).fetchone()
            data=json.loads(row['data']);status='failed'
            if result.get('ok'):
                try:
                    after={path:self.capture(path) for path in data['expected']}
                    if any(any(value.get(key)!=expected for key,expected in data['expected'][path].items()) for path,value in after.items()):
                        raise ValueError('Файлы изменились сразу после операции')
                    data['after']=after;status='applied'
                except (OSError,ValueError) as exc:
                    status='unknown';data['error']=str(exc)[:500]
                    result={**result,'ok':False,'code':'OUTCOME_UNKNOWN','error':'Не удалось подтвердить состояние файлов после записи: '+str(exc)[:300]}
            elif result.get('code')=='OUTCOME_UNKNOWN':status='unknown'
            connection.execute('UPDATE workspace_snapshots SET status=?,data=? WHERE id=?',(status,encode(data),identity))
            return {**result,'snapshot_group_id':row['group_id']}

    def reconcile(self, entries):
        """An interrupted capture is unavailable unless a receipt proves no effect began."""
        anchors={(e['message_index'],e['call_id']):e for e in entries}
        with self.database.transaction() as connection:
            rows=connection.execute("SELECT * FROM workspace_snapshots WHERE chat_id=? AND journal_id=? AND status IN ('prepared','unknown')",(self.chat_id,self.journal_id)).fetchall()
            for row in rows:
                data=json.loads(row['data']);entry=anchors.get((data['message_index'],data['call_id']))
                result=(entry or {}).get('result') or {}
                safe=(entry and entry['phase']!='started') or result.get('code') in ('USER_CONFIRMED_NOT_EXECUTED','NOT_EXECUTED','USER_DENIED','USER_CANCELLED','FILE_CHANGED')
                connection.execute('UPDATE workspace_snapshots SET status=? WHERE id=?',('failed' if safe else 'unknown',row['id']))

    def list(self):
        with self.database.transaction() as connection:
            groups=connection.execute('SELECT group_id,max(sequence) AS last FROM workspace_snapshots WHERE chat_id=? AND root=? GROUP BY group_id ORDER BY last DESC LIMIT 50',(self.chat_id,str(self.root))).fetchall()
            items=[]
            for group in groups:
                rows=self._rows(connection,group['group_id']);before,after=self._aggregate(rows)
                statuses={row['status'] for row in rows}
                state=next((s for s in ('rollback_unknown','rolling_back','unknown','prepared','applied','rolled_back','abandoned') if s in statuses),'failed')
                items.append({'id':group['group_id'],'status':state,'paths':sorted({path for row in rows for path in json.loads(row['data'])['before']}),
                    'operations':[json.loads(row['data'])['operation'] for row in rows],'journal_id':rows[0]['journal_id']})
            return items

    def revision(self):
        with self.database.transaction() as connection:
            return connection.execute('SELECT coalesce(max(revision),0) FROM workspace_snapshots WHERE chat_id=? AND root=?',(self.chat_id,str(self.root))).fetchone()[0]

    def rollback_event(self):
        """Read the latest durable rollback/review outcome for canonical history."""
        with self.database.transaction() as connection:
            row=connection.execute('SELECT revision,status,group_id FROM workspace_snapshots WHERE chat_id=? AND root=? AND revision>0 ORDER BY revision DESC LIMIT 1',(self.chat_id,str(self.root))).fetchone()
            return dict(row) if row else None

    def attention(self):
        with self.database.transaction() as connection:
            return [dict(row) for row in connection.execute("SELECT DISTINCT group_id AS id,status FROM workspace_snapshots WHERE chat_id=? AND root=? AND status IN ('rolling_back','rollback_unknown')",(self.chat_id,str(self.root)))]

    def _validate(self, rows, before, after):
        if any(row['status'] not in ('applied','failed') for row in rows) or not after:raise ValueError('Снимок недоступен для автоматического отката')
        if any(json.loads(row['data'])['root_identity']!=parent_revision(self.root) for row in rows):raise ValueError('Корневая папка проекта была заменена')
        current={path:self.capture(path) for path in after}
        if any(fingerprint(current[path])!=fingerprint(expected) for path,expected in after.items()):
            raise ValueError('Файлы изменились после правок агента. Откат не будет перезаписывать ручные изменения.')
        for path,value in after.items():
            if value['kind']=='directory' and before[path]['kind']=='missing':
                for child in (self.root/path).iterdir():
                    relative=child.relative_to(self.root).as_posix()
                    if relative not in before or before[relative]['kind']!='missing':raise ValueError('В созданной папке есть новые файлы; автоматический откат отменён')
        return current

    def preview(self, group_id):
        """Compare all affected revisions and produce a user-reviewable inverse diff."""
        with self.database.transaction() as connection:
            rows=self._rows(connection,group_id);before,after=self._aggregate(rows)
            current=self._validate(rows,before,after)
        diffs=[]
        for path in sorted(before):
            old=after[path];new=before[path]
            if old['kind']=='file' or new['kind']=='file':
                try:
                    old_text=base64.b64decode(self.blobs.get(old['artifact'])).decode('utf-8') if old['kind']=='file' else ''
                    new_text=base64.b64decode(self.blobs.get(new['artifact'])).decode('utf-8') if new['kind']=='file' else ''
                    diffs.append(''.join(difflib.unified_diff(old_text.splitlines(True),new_text.splitlines(True),fromfile='current/'+path,tofile='restore/'+path)))
                except UnicodeDecodeError:diffs.append('Бинарный файл: '+path+' — восстановить исходные байты\n')
            elif old['kind']=='directory' and new['kind']=='missing':diffs.append('Удалить пустую созданную папку: '+path+'\n')
        signature=hashlib.sha256(encode({'rows':[(r['id'],r['status'],r['data']) for r in rows],'current':current}).encode()).hexdigest()
        diff='\n'.join(diffs)
        return {'group_id':group_id,'fingerprint':signature,'paths':sorted(before),'diff':diff[:240000], 'truncated':len(diff)>240000}

    def _original_bytes(self,saved):
        raw=base64.b64decode(self.blobs.get(saved['artifact']),validate=True)
        if hashlib.sha256(raw).hexdigest()!=saved['sha256']:raise ValueError('Повреждён исходник снимка')
        return raw

    def _restore_file(self, path, saved, expected):
        raw=self._original_bytes(saved)
        target=mutation_path(self.root,path)
        descriptor,temporary=tempfile.mkstemp(prefix='.neutral-restore-',dir=target.parent)
        try:
            with os.fdopen(descriptor,'wb') as stream:
                stream.write(raw);stream.flush();os.fsync(stream.fileno())
            if fingerprint(self.capture(path))!=fingerprint(expected):raise ValueError('Файл изменился перед восстановлением')
            if expected['kind']=='missing':
                if os.name=='nt':os.rename(temporary,target)
                else:os.link(temporary,target)
            else:os.replace(temporary,target)
            os.chmod(target,saved['mode'])
        finally:
            if os.path.exists(temporary):os.unlink(temporary)

    def restore(self, group_id, expected_fingerprint):
        """Persist intent before effects; any partial failure requires explicit user review."""
        with self.database.transaction() as connection:
            preview=self.preview(group_id)
            if preview['fingerprint']!=expected_fingerprint:raise ValueError('Preview устарел; сравните изменения заново')
            rows=self._rows(connection,group_id);before,after=self._aggregate(rows)
            self._validate(rows,before,after)
            # Read every backup before the first effect, including binary originals.
            for value in before.values():
                if value['kind']=='file':self._original_bytes(value)
            revision=connection.execute('SELECT coalesce(max(revision),0)+1 FROM workspace_snapshots').fetchone()[0]
            connection.execute("UPDATE workspace_snapshots SET status='rolling_back',revision=? WHERE group_id=? AND chat_id=?",(revision,group_id,self.chat_id))
        changed=[]
        try:
            paths=sorted(before,key=lambda p:(0 if before[p]['kind']=='file' else 1 if after[p]['kind']=='file' else 2,-p.count('/'),p))
            for path in paths:
                if fingerprint(self.capture(path))!=fingerprint(after[path]):raise ValueError('Путь изменился во время отката: '+path)
                if before[path]['kind']=='file':self._restore_file(path,before[path],after[path])
                elif before[path]['kind']=='missing' and after[path]['kind']=='file':mutation_path(self.root,path).unlink()
                elif before[path]['kind']=='missing' and after[path]['kind']=='directory':mutation_path(self.root,path).rmdir()
                changed.append(path)
                with self.database.transaction() as connection:
                    connection.execute('UPDATE workspace_snapshots SET rollback_progress=? WHERE group_id=? AND chat_id=?',(encode(changed),group_id,self.chat_id))
            status='rolled_back';error=''
        except Exception as exc:status='rollback_unknown';error=str(exc)[:500]
        with self.database.transaction() as connection:
            connection.execute('UPDATE workspace_snapshots SET status=?,rollback_error=? WHERE group_id=? AND chat_id=?',(status,error,group_id,self.chat_id))
        return {'ok':status=='rolled_back','status':status,'changed_paths':changed,'error':error}

    def review(self, group_id):
        """Record the user's manual review after partial rollback without touching files."""
        with self.database.transaction() as connection:
            rows=self._rows(connection,group_id)
            if not any(row['status'] in ('rolling_back','rollback_unknown') for row in rows):raise ValueError('Снимок не ожидает ручной проверки')
            revision=connection.execute('SELECT coalesce(max(revision),0)+1 FROM workspace_snapshots').fetchone()[0]
            connection.execute("UPDATE workspace_snapshots SET status='abandoned',revision=? WHERE group_id=? AND chat_id=?",(revision,group_id,self.chat_id))
