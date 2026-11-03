"""Disposable per-workspace SQLite index, durable changes and a live filesystem observer."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import threading
import time
import uuid
from .security import canonical_root,resolve_allowed_path
from .project_index_policy import IndexPolicy
from .project_symbols import extract_symbols

_registry={};_registry_lock=threading.RLock()
MAX_PENDING=20000


class ProjectIndex:
    """Own one cache/watcher/worker; never use the chat database or execute source code."""
    def __init__(self,root,*,watch=True):
        from .task_store import TASK_DIR
        self.root=canonical_root(root);identity=str(self.root).casefold() if os.name=='nt' else str(self.root)
        self.workspace_id=hashlib.sha256(identity.encode()).hexdigest()
        self.directory=TASK_DIR.parent/'cache/project-index'/self.workspace_id;self.directory.mkdir(parents=True,exist_ok=True)
        self.path=self.directory/'index.sqlite3';self.stop=threading.Event();self.cancel_build=threading.Event();self.wake=threading.Event()
        self.watch_ready=threading.Event();self.watcher=None;self.worker=None;self.state='needs_rebuild';self.reason='Нужна первичная индексация'
        self.lock=threading.RLock();self.rebuild_requested=False;self.invalidate_requested=False;self.fts=False;self.scan_count=0;self.changed_count=0
        self.revision=0;self.file_count=0;self.parser_errors=0;self.owner=None;self.has_owner=False;self.watch_enabled=watch
        try:
            self._claim();self._initialize()
            if watch:
                self.watcher=threading.Thread(target=self._watch,daemon=True,name='project-index-watch');self.watcher.start()
            else:self.watch_ready.set()
            self.worker=threading.Thread(target=self._run,daemon=True,name='project-index-worker');self.worker.start()
            self.rebuild()
        except (OSError,sqlite3.Error,RuntimeError) as exc:self.state='degraded';self.reason=type(exc).__name__+': '+str(exc)[:160]

    def _claim(self):
        """Use an OS-released cache owner lock so another Core cannot silently race a rebuild."""
        self.owner=(self.directory/'owner.lock').open('a+b')
        if self.owner.seek(0,2)==0:self.owner.write(b'0');self.owner.flush()
        self.owner.seek(0)
        if os.name=='nt':
            import msvcrt
            msvcrt.locking(self.owner.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(self.owner,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.has_owner=True

    @contextmanager
    def database(self):
        """Short independent WAL connections keep cache work off chat/checkpoint transactions."""
        connection=sqlite3.connect(self.path,timeout=.5);connection.row_factory=sqlite3.Row
        connection.create_function('casefold',1,str.casefold,deterministic=True)
        try:
            connection.execute('PRAGMA busy_timeout=500')
            with connection:yield connection
        finally:connection.close()

    def _initialize(self):
        """Validate the cache schema and retain pending paths after an interrupted process."""
        with self.database() as db:
            version=db.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0,1):raise RuntimeError('Неизвестная версия кеша индекса')
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY,sha TEXT NOT NULL,content TEXT NOT NULL,folded TEXT NOT NULL,policy TEXT NOT NULL,parser TEXT NOT NULL,revision INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS symbols(path TEXT NOT NULL,name TEXT NOT NULL,folded TEXT NOT NULL,data TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS symbol_names ON symbols(folded);
                CREATE INDEX IF NOT EXISTS symbol_paths ON symbols(path);
                CREATE INDEX IF NOT EXISTS parser_status ON files(parser);
                CREATE TABLE IF NOT EXISTS pending(path TEXT PRIMARY KEY,token TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
                PRAGMA user_version=1;''')
            try:db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS text_fts USING fts5(path UNINDEXED,content,tokenize='trigram')");self.fts=True
            except sqlite3.OperationalError:self.fts=False
            self.revision=int((db.execute("SELECT value FROM meta WHERE key='revision'").fetchone() or ['0'])[0])
            self.file_count=db.execute('SELECT count(*) FROM files').fetchone()[0]
            self.parser_errors=db.execute("SELECT count(*) FROM files WHERE parser IN ('parser-unavailable-or-error','tree-sitter-partial')").fetchone()[0]

    def status(self):
        """Expose cache coverage, state and counters, without opening source files or returning snippets."""
        with self.lock:
            return {'ok':True,'state':self.state,'reason':self.reason,'workspace_id':self.workspace_id,'revision':self.revision,
                'files':self.file_count,'parser_errors':self.parser_errors,'full_scans':self.scan_count,'updated_files':self.changed_count,
                'backend':'fts5-trigram' if self.fts else 'sqlite-text','watcher':self.watch_ready.is_set() and self.watch_enabled,
                'cache_bytes':self._cache_bytes()}

    def _cache_bytes(self):
        """WAL files can disappear during checkpoint; status polling must tolerate that race."""
        total=0
        for suffix in ('','-wal','-shm'):
            try:total+=(self.directory/('index.sqlite3'+suffix)).stat().st_size
            except OSError:pass
        return total

    def rebuild(self):
        """Request a controlled background rescan; cancellation never claims a complete index."""
        if self.worker is None:
            if not self.has_owner:return self.status()
            # Explicit rebuild of this exclusively owned derived cache, never user source files.
            for suffix in ('','-wal','-shm'):
                source=self.directory/('index.sqlite3'+suffix)
                if source.exists():source.replace(self.directory/('index-'+uuid.uuid4().hex+suffix+'.broken'))
            try:
                self._initialize()
                if self.watch_enabled:
                    self.watcher=threading.Thread(target=self._watch,daemon=True,name='project-index-watch');self.watcher.start()
                else:self.watch_ready.set()
                self.worker=threading.Thread(target=self._run,daemon=True,name='project-index-worker');self.worker.start()
            except (OSError,sqlite3.Error) as exc:self.reason='Не удалось пересобрать кеш: '+type(exc).__name__;return self.status()
        self.cancel_build.clear();self.rebuild_requested=True;self.state='building';self.reason='Читаю сохранённые файлы';self.wake.set()
        return self.status()

    def cancel(self):
        """Cancel background work while retaining the durable queue and the old linear search."""
        self.cancel_build.set();self.rebuild_requested=False;self.state='needs_rebuild';self.reason='Индексация отменена';self.wake.set()
        return self.status()

    def uncertain(self,reason,*,purge=False):
        """Do not infer freshness after overflow, policy change, missed events or command uncertainty."""
        self.cancel_build.set();self.state='needs_rebuild';self.reason=reason;self.invalidate_requested|=purge;self.wake.set()

    def enqueue(self,paths):
        """Persist coalesced exact paths before waking the updater; no full scan for ordinary edits."""
        if self.stop.is_set() or self.worker is None:return
        with self.database() as db:
            for path in set(paths):
                relative=str(path).replace('\\','/')
                if relative.startswith('/') or '..' in relative.split('/') or ':' in relative:continue
                db.execute('INSERT INTO pending VALUES(?,?) ON CONFLICT(path) DO UPDATE SET token=excluded.token',(relative,uuid.uuid4().hex))
            if db.execute('SELECT count(*) FROM pending').fetchone()[0]>MAX_PENDING:
                db.execute('DELETE FROM pending');self.uncertain('Переполнение очереди; нужна пересборка');return
        if self.state=='ready':self.state='updating'
        self.wake.set()

    def reconcile_command(self,cwd='.'):
        """Commands are not confined by evidence scope; reconcile their cwd with a bounded walk."""
        target=resolve_allowed_path(self.root,cwd,must_exist=True);relative=target.relative_to(self.root).as_posix()
        with self.database() as db:db.execute('INSERT OR REPLACE INTO pending VALUES(?,?)',('\x00command/'+relative,uuid.uuid4().hex))
        if self.state=='ready':self.state='updating'
        self.wake.set()

    def _watch(self):
        """Subscribe before initial scan; exceptions/oversized event batches require explicit recovery."""
        try:
            from watchfiles import watch
            for changes in watch(self.root,stop_event=self.stop,debounce=100,step=25,rust_timeout=300,
                    yield_on_timeout=True,watch_filter=None,raise_interrupt=False):
                self.watch_ready.set()
                if self.stop.is_set():return
                if len(changes)>10000:self.uncertain('Переполнение очереди наблюдения');continue
                paths=[]
                for _change,path in changes:
                    try:relative=Path(path).relative_to(self.root).as_posix()
                    except ValueError:continue
                    from .workspace_search import EXCLUDED
                    if any(p in EXCLUDED or p.startswith('.local-agent-tmp-') for p in relative.split('/')):continue
                    if Path(relative).name in ('.gitignore','.neutralignore'):
                        self.cancel_build.set();self.uncertain('Правила изменились; пересоберите индекс',purge=True);continue
                    paths.append(relative)
                if paths:self.enqueue(paths)
        except Exception as exc:self.watch_ready.clear();self.uncertain('Наблюдение недоступно: '+type(exc).__name__)

    def _walk(self,policy,start=None,*,limit=100000,seconds=120):
        """Initial/recovery or bounded subtree enumeration; never follow symlinks or junctions."""
        stack=[start or self.root];deadline=time.monotonic()+seconds if seconds is not None else float('inf');count=0
        while stack:
            if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
            directory=stack.pop()
            with os.scandir(directory) as entries:
                for entry in entries:
                    if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
                    count+=1
                    if count>limit or time.monotonic()>deadline:raise RuntimeError('Обход неполон; нужна контролируемая пересборка')
                    if entry.is_symlink() or getattr(os.path,'isjunction',lambda p:False)(entry.path):continue
                    relative=Path(entry.path).relative_to(self.root).as_posix();is_directory=entry.is_dir(follow_symlinks=False)
                    if not policy.permits(relative,is_directory):continue
                    if is_directory:stack.append(Path(entry.path))
                    elif entry.is_file(follow_symlinks=False):yield relative

    def _read(self,relative,policy,*,parse=True):
        """Retry bounded read-only sharing/moving-file races during atomic editor saves."""
        for attempt in range(4):
            if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
            try:return self._read_once(relative,policy,parse=parse)
            except FileNotFoundError:
                # Watcher/subtree enumeration can race with a normal delete.
                # Absence is an incremental deletion, not an uncertain full tree.
                if not self.root.is_dir():raise
                return None
            except PermissionError:
                if attempt==3:raise
            except ValueError as exc:
                if str(exc)!='Файл изменился во время чтения' or attempt==3:raise
            self.stop.wait(.03*(2**attempt))

    def _read_once(self,relative,policy,*,parse=True):
        """Revalidate access and content; retain neither binary, protected nor unstable file data."""
        if not policy.permits(relative):return None
        raw_path=self.root/relative
        path=raw_path.resolve(strict=True);path.relative_to(self.root)
        if path!=raw_path:return None
        before=path.stat(follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):return None
        if before.st_size>1_000_000:return None
        with path.open('rb') as source:raw=source.read(1_000_001)
        after=path.stat()
        if len(raw)>1_000_000 or b'\0' in raw:return None
        if (before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):raise ValueError('Файл изменился во время чтения')
        try:text=raw.decode('utf-8-sig')
        except UnicodeError:return None
        symbols,parser=extract_symbols(relative,text) if parse else ([],None)
        return {'path':relative,'sha':hashlib.sha256(raw).hexdigest(),'content':text,'policy':policy.anchor_policy(relative),'symbols':symbols,'parser':parser}

    def _apply(self,records,pending=()):
        """Commit a small batch and consume only the queue tokens actually processed."""
        with self.database() as db:
            changed=[]
            for path,record in dict(records).items():
                old=db.execute('SELECT sha,policy,parser FROM files WHERE path=?',(path,)).fetchone()
                if not old and not record:continue
                if old and record and tuple(old)==(record['sha'],record['policy'],record['parser']):continue
                changed.append((path,record))
            records=changed
            if records:self.revision+=1
            for path,record in records:
                if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
                db.execute('DELETE FROM symbols WHERE path=?',(path,));db.execute('DELETE FROM files WHERE path=?',(path,))
                if self.fts:db.execute('DELETE FROM text_fts WHERE path=?',(path,))
                if record:
                    db.execute('INSERT INTO files VALUES(?,?,?,?,?,?,?)',(path,record['sha'],record['content'],record['content'].casefold(),record['policy'],record['parser'],self.revision))
                    db.executemany('INSERT INTO symbols VALUES(?,?,?,?)',[(path,s['name'],s['name'].casefold(),json.dumps(s)) for s in record['symbols']])
                    if self.fts:db.execute('INSERT INTO text_fts VALUES(?,?)',(path,record['content'].casefold()))
            for path,token in pending:db.execute('DELETE FROM pending WHERE path=? AND token=?',(path,token))
            db.execute("INSERT OR REPLACE INTO meta VALUES('revision',?)",(str(self.revision),))
            self.file_count=db.execute('SELECT count(*) FROM files').fetchone()[0]
            self.parser_errors=db.execute("SELECT count(*) FROM files WHERE parser IN ('parser-unavailable-or-error','tree-sitter-partial')").fetchone()[0]
        return len(records)

    def _purge(self):
        """Invalidate all derived content on policy change; raw chat/journal data is untouched."""
        with self.database() as db:
            db.execute('DELETE FROM files');db.execute('DELETE FROM symbols')
            if self.fts:db.execute('DELETE FROM text_fts')
        self.file_count=0;self.parser_errors=0

    def _build(self):
        """Start a fresh scan after subscription, then drain events that arrived during the scan."""
        if not self.watch_ready.wait(3):raise RuntimeError('Наблюдение за файлами не запущено')
        policy=IndexPolicy(self.root);self.policy_version=policy.version;self.root_ignore=policy.rules('')[1]
        with self.database() as db:db.execute('DELETE FROM pending')
        self._purge();self.scan_count+=1;self.parser_errors=0;records=[];total=0
        for relative in self._walk(policy,seconds=None):
            try:record=self._read(relative,policy)
            except (OSError,ValueError,UnicodeError):raise RuntimeError('Не удалось безопасно прочитать исходники; индекс неполон')
            if record:
                total+=len(record['content'].encode())
                if total>256_000_000:raise RuntimeError('Превышена ёмкость текстового кеша; индекс неполон')
                if record['parser']=='parser-unavailable-or-error':self.parser_errors+=1
                records.append((relative,record))
            if len(records)>=64:self._apply(records);records=[]
        if records:self._apply(records)
        if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')

    def _drain(self):
        """Replay coalesced file changes; directories/commands get only a bounded subtree reconciliation."""
        with self.database() as db:pending=[tuple(r) for r in db.execute('SELECT path,token FROM pending LIMIT 64')]
        if not pending:return False
        policy=IndexPolicy(self.root);records=[]
        for relative,token in pending:
            if self.stop.is_set() or self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
            if Path(relative).name in ('.gitignore','.neutralignore'):
                with self.database() as db:db.execute('DELETE FROM pending WHERE path=? AND token=?',(relative,token))
                self.uncertain('Правила доступа/исключений изменились; пересоберите индекс',purge=True);return False
            reconcile=relative.startswith('\x00command/');local=relative.removeprefix('\x00command/') if reconcile else relative
            target=resolve_allowed_path(self.root,local)
            if target.is_dir() or reconcile:
                existing=[]
                prefix='' if target==self.root else target.relative_to(self.root).as_posix()+'/'
                with self.database() as db:existing=[r[0] for r in db.execute('SELECT path FROM files WHERE substr(path,1,?)=?',(len(prefix),prefix))]
                seen=set(self._walk(policy,target,limit=2000,seconds=2)) if target.is_dir() else set()
                for path in seen|set(existing):records.append((path,self._read(path,policy) if path in seen else None))
            else:
                try:record=self._read(relative,policy) if target.exists() else None
                except (FileNotFoundError,UnicodeError):record=None
                records.append((relative,record))
                # A deleted/renamed directory may have no separate child events.
                if not target.exists():
                    prefix=relative+'/'
                    with self.database() as db:records.extend((r[0],None) for r in db.execute('SELECT path FROM files WHERE substr(path,1,?)=?',(len(prefix),prefix)))
        self.changed_count+=self._apply(records,pending);return True

    def _run(self):
        """One cache updater; normal edits never schedule a global rescan automatically."""
        while not self.stop.is_set():
            self.wake.wait(.2);self.wake.clear()
            try:
                if self.invalidate_requested:self.invalidate_requested=False;self._purge()
                if self.rebuild_requested:
                    self.rebuild_requested=False;self._build()
                    if self.cancel_build.is_set():raise InterruptedError('Индексация отменена')
                    self.state='updating'
                if self.state in ('updating','ready'):
                    while not self.stop.is_set() and not self.cancel_build.is_set() and not self.rebuild_requested and self._drain():pass
                    with self.lock:
                        if self.cancel_build.is_set():
                            if self.state!='needs_rebuild':self.state='needs_rebuild';self.reason='Индексация отменена'
                        elif self.rebuild_requested:self.state='building'
                        elif self.state in ('updating','ready'):
                            self.state='ready';self.reason='Индекс сохранённых файлов готов'
            except InterruptedError:
                if self.state!='needs_rebuild':self.state='needs_rebuild';self.reason='Индексация отменена'
            except Exception as exc:self.uncertain(str(exc)[:180] or type(exc).__name__)

    def query(self,params,cancelled=None):
        """Return only currently readable hash-verified hits, with exact source/index provenance."""
        if cancelled and cancelled.is_set():return {'ok':False,'code':'SEARCH_CANCELLED','matches':[],'reason':'cancelled'}
        if self.state not in ('ready','updating'):return None
        updating=self.state=='updating'
        mode=params.get('mode','text');query=params.get('query','');limit=params.get('limit',200)
        if mode not in ('text','files','symbols','outline') or not isinstance(query,str) or len(query)>200:raise ValueError('Некорректный поиск индекса')
        if type(limit) is not int or not 1<=limit<=2000:raise ValueError('Лимит поиска: 1–2000')
        if mode in ('text','symbols') and not query.strip():raise ValueError('Введите запрос поиска')
        if not isinstance(params.get('pattern',''),str) or len(params.get('pattern',''))>120 or type(params.get('case_sensitive',False)) is not bool:raise ValueError('Некорректная маска или регистр поиска')
        if type(params.get('max_depth',30)) is not int or not 0<=params.get('max_depth',30)<=30:raise ValueError('Глубина поиска: 0–30')
        limit=min(limit,200);policy=IndexPolicy(self.root)
        if policy.version!=self.policy_version or policy.rules('')[1]!=self.root_ignore:
            self.uncertain('Правила изменились; нужна пересборка',purge=True);return None
        from .workspace_search import glob_matches
        folder=resolve_allowed_path(self.root,params.get('path','.'),must_exist=True);relative_folder=folder.relative_to(self.root).as_posix()
        needle=query.casefold();matches=[];checked=0;deadline=time.monotonic()+3;stale=False;verified_bytes=0;bytes_exhausted=False
        with self.database() as db:
            db.execute('BEGIN')
            query_revision=int((db.execute("SELECT value FROM meta WHERE key='revision'").fetchone() or ['0'])[0])
            prefix='' if relative_folder=='.' else relative_folder+'/'
            scope_sql='(f.path=? OR substr(f.path,1,?)=?)';scope_args=(relative_folder,len(prefix),prefix)
            matching=query if params.get('case_sensitive') else needle
            if mode=='symbols':
                field='s.name' if params.get('case_sensitive') else 's.folded'
                rows=db.execute("SELECT f.path,f.sha,f.policy,f.revision,s.data AS symbol FROM symbols s JOIN files f ON f.path=s.path WHERE instr("+field+",?)>0 AND "+scope_sql+" ORDER BY (s.folded=?) DESC,(json_extract(s.data,'$.kind')='export'),s.path LIMIT 2001",(matching,*scope_args,needle)).fetchall()
            elif mode=='outline':rows=db.execute('SELECT f.path,f.sha,f.policy,f.revision,s.data AS symbol FROM symbols s JOIN files f ON f.path=s.path WHERE '+scope_sql+' ORDER BY f.path LIMIT 2001',scope_args).fetchall()
            elif mode=='files':
                field='f.path' if params.get('case_sensitive') else 'casefold(f.path)'
                rows=db.execute('SELECT f.path,f.sha,f.policy,f.revision FROM files f WHERE instr('+field+',?)>0 AND '+scope_sql+' ORDER BY f.path LIMIT 2001',(matching,*scope_args)).fetchall()
            elif self.fts and len(query)>=3:
                rows=db.execute('SELECT f.path,f.sha,f.policy,f.revision FROM text_fts t JOIN files f ON f.path=t.path WHERE text_fts MATCH ? AND '+scope_sql+' ORDER BY f.path LIMIT 2001',('"'+needle.replace('"','""')+'"',*scope_args)).fetchall()
            else:rows=db.execute('SELECT f.path,f.sha,f.policy,f.revision FROM files f WHERE instr(f.folded,?)>0 AND '+scope_sql+' ORDER BY f.path LIMIT 2001',(needle,*scope_args)).fetchall()
        verified={}
        for row in rows:
            if cancelled and cancelled.is_set():return {'ok':False,'code':'SEARCH_CANCELLED','matches':[],'reason':'cancelled'}
            if time.monotonic()>deadline:break
            path=row['path']
            if relative_folder!='.' and path!=relative_folder and not path.startswith(relative_folder+'/'):continue
            if params.get('pattern') and not glob_matches(path,params['pattern']):continue
            depth=len(Path(path).relative_to(relative_folder if relative_folder!='.' else '.').parts)-1
            if depth>params.get('max_depth',30):continue
            if not policy.permits(path):self.uncertain('Доступ к кешированным исходникам изменился',purge=True);return None
            if path not in verified:
                try:verified[path]=self._read(path,policy,parse=False)
                except (OSError,ValueError,UnicodeError):verified[path]=None
                checked+=1
                verified_bytes+=len(verified[path]['content'].encode()) if verified[path] else 0
                if verified_bytes>8_000_000:bytes_exhausted=True;break
            actual=verified[path]
            if not actual or actual['sha']!=row['sha'] or actual['policy']!=row['policy']:
                self.enqueue([path]);stale=True;continue
            fresh=IndexPolicy(self.root)
            if not fresh.permits(path) or fresh.anchor_policy(path)!=actual['policy']:
                self.uncertain('Правила изменились во время поиска',purge=True);return None
            anchor={'workspace_id':self.workspace_id,'sha256':row['sha'],'file_revision':row['revision'],'index_revision':query_revision,'policy_version':actual['policy'],'source_kind':'saved-file','freshness':'hash-verified'}
            if mode in ('symbols','outline'):
                symbol=json.loads(row['symbol']);matches.append({'path':path,'line':symbol['start_line'],'text':symbol['name'],**symbol,**anchor})
            elif mode=='files':matches.append({'path':path,'line':1,'text':'',**anchor})
            else:
                for number,line in enumerate(actual['content'].splitlines(),1):
                    if (query if params.get('case_sensitive') else needle) in (line if params.get('case_sensitive') else line.casefold()):
                        matches.append({'path':path,'line':number,'start_line':number,'end_line':number,'text':line[:300],**anchor})
                        if len(matches)>=limit:break
            if len(matches)>=limit:break
        parser_partial=self.parser_errors>0 and mode in ('symbols','outline')
        truncated=updating or parser_partial or stale or bytes_exhausted or len(matches)>=limit or len(rows)>=2001 or time.monotonic()>deadline
        return {'ok':True,'matches':matches[:limit],'truncated':truncated,'reason':'stale' if stale else 'updating' if updating else 'parser' if parser_partial else 'bytes' if bytes_exhausted else 'results' if truncated else '',
            'scanned_files':checked,'skipped_files':0,'backend':'project-index','index':self.status(),'coverage':'indexed-saved-files','precision':'syntax' if mode in ('symbols','outline') else 'literal'}

    def close(self):
        """Stop observer/updater and release cache ownership; durable pending paths survive restart."""
        self.stop.set();self.cancel_build.set();self.wake.set()
        for thread in (self.worker,self.watcher):
            if thread:thread.join(3)
        if self.worker and self.worker.is_alive():return
        if self.owner:self.owner.close();self.owner=None


def get_index(root,*,create=False):
    """Scope cache instances by both canonical workspace and current profile, including tests."""
    from .task_store import TASK_DIR
    key=(str(TASK_DIR.parent.resolve()),str(canonical_root(root)))
    with _registry_lock:
        if key not in _registry and create:_registry[key]=ProjectIndex(root)
        return _registry.get(key)


def notify_paths(root,paths):
    """Best-effort event feed after an already authorized effect; cache failure never repeats that effect."""
    try:
        index=get_index(root)
        if index:index.enqueue(paths)
    except (OSError,ValueError,sqlite3.Error):pass


def close_indexes():
    """Release all current process observers during project switches and Core shutdown."""
    with _registry_lock:
        instances=list(_registry.values());_registry.clear()
    for index in instances:index.close()
