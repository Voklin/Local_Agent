"""Durable run identities and inference telemetry; never an execution or spending policy."""
from datetime import datetime,timezone
import hashlib
import json
import os
import threading
import time
import uuid
from .operation_context import OperationContext
from .process_identity import owner_alive,inspect_process,owner_ended
from .storage import Storage,encode

ACTIVE={'running','waiting_approval','executing','verifying'}
TERMINAL={'completed','paused','failed','needs_attention'}


def now():
    """UTC time for durable records; elapsed durations use the monotonic clock."""
    return datetime.now(timezone.utc).isoformat()


def safe_usage(value):
    """Normalize provider-reported token counts without inventing missing usage."""
    if hasattr(value,'model_dump'):value=value.model_dump()
    if not isinstance(value,dict):return None
    incoming=value.get('input_tokens',value.get('prompt_tokens'));outgoing=value.get('output_tokens',value.get('completion_tokens'))
    if any(type(v) is not int or v<0 for v in (incoming,outgoing)):return None
    return {'input_tokens':incoming,'output_tokens':outgoing}


class BudgetLedger:
    """Incremental accounting in the same transaction as each attempt; never a stop policy."""
    @staticmethod
    def contribution(attempt):
        """One row's exact contribution, including unknown usage and outstanding reservations."""
        a=attempt or {};usage=a.get('usage') or {};active=a.get('state')=='active'
        return {'http_attempts':a.get('http_attempts',0),'reservations':int(bool(attempt)),
            'requests_reported':int(a.get('usage') is not None),'input_tokens':usage.get('input_tokens',0),'output_tokens':usage.get('output_tokens',0),
            'active_reserved_tokens':sum(a.get('reservation',{}).values()) if active else 0,
            'queued_requests':int(active and a.get('phase')=='queued'),'interrupted':int(a.get('state')=='interrupted'),'queue_ms':a.get('queue_ms',0)}

    @staticmethod
    def apply(connection,run_id,before,after):
        """Apply a reversible delta atomically; repeated terminal updates do not double-count tokens."""
        row=connection.execute('SELECT data FROM runs WHERE id=?',(run_id,)).fetchone();value=json.loads(row[0])
        old=BudgetLedger.contribution(before);new=BudgetLedger.contribution(after);ledger=value.get('ledger',{})
        value['ledger']={key:ledger.get(key,0)+new[key]-old[key] for key in new}
        connection.execute('UPDATE runs SET data=? WHERE id=?',(encode(value),run_id))


class RunRegistry:
    """Append independent runs to the existing profile DB; retain the task/journal as execution authority."""
    def __init__(self,directory=None,alive=None,inspect_owner=inspect_process):
        self.directory=directory;self.alive=alive;self.inspect_owner=inspect_owner;self.lock=threading.RLock();self.handles={};self.database=None

    def ready(self):
        """Resolve the test/user profile lazily, migrate once and recover only orphan telemetry."""
        with self.lock:
            if self.database:return self.database
            from .task_store import TASK_DIR
            database=Storage(self.directory or TASK_DIR.parent).ready()
            with database.transaction() as c:
                rows=c.execute("SELECT id,data FROM runs WHERE state IN ('running','waiting_approval','executing','verifying') UNION SELECT r.id,r.data FROM runs r JOIN inference_attempts a ON a.run_id=r.id WHERE json_extract(a.data,'$.state')='active'").fetchall()
                owners={}
                for row in rows:
                    value=json.loads(row['data'])
                    pid=value.get('owner_pid');token=value.get('owner_token')
                    key=(pid if type(pid) is int else None,token if isinstance(token,str) else None)
                    if key not in owners:
                        owners[key]=('owner_exited' if not self.alive(key[0]) else None) if self.alive else owner_ended(*key,inspect=self.inspect_owner)
                    cause=owners[key]
                    if not cause:continue
                    value.update(state='paused' if value['state'] in ACTIVE else value['state'],recovered=True,recovery_cause=cause,recovered_at=now(),reason='Процесс владельца завершился; продолжение только через checkpoint и проверку журнала')
                    c.execute('UPDATE runs SET data=?,updated_at=?,state=? WHERE id=?',(encode(value),now(),value['state'],row['id']))
                    for item in c.execute('SELECT id,data FROM inference_attempts WHERE run_id=?',(row['id'],)).fetchall():
                        attempt=json.loads(item['data'])
                        if attempt['state']=='active':
                            before=dict(attempt)
                            attempt.update(state='interrupted',ended_at=now(),outcome='unknown_after_restart')
                            c.execute('UPDATE inference_attempts SET data=? WHERE id=?',(encode(attempt),item['id']))
                            BudgetLedger.apply(c,row['id'],before,attempt)
            self.database=database
            return database

    def begin(self,*,kind,model,base_url,api_protocol='chat',chat_id='',journal_id='',run_id=None,operation=None,parent=None,spending_policy=None):
        """Create a fresh run; child prototypes inherit the connection and cancellation, never load another model."""
        database=self.ready();identity=run_id or uuid.uuid4().hex
        if not isinstance(identity,str) or len(identity)!=32 or any(c not in '0123456789abcdef' for c in identity):raise ValueError('Некорректный run ID')
        with self.lock,database.transaction() as c:
            if c.execute('SELECT 1 FROM runs WHERE id=?',(identity,)).fetchone():raise ValueError('Этот run ID уже использован')
            if parent:
                if parent.registry is not self or parent.closed or parent.operation.is_set():raise ValueError('Родительский запуск недоступен')
                if parent.parent_id:raise ValueError('В MVP разрешён только один уровень дочерних запусков')
                if (model,base_url.rstrip('/'),api_protocol)!=(parent.model,parent.base_url,parent.api_protocol):raise ValueError('Дочерний запуск наследует модель и подключение родителя')
                if c.execute('SELECT COUNT(*) FROM runs WHERE parent_id=?',(parent.id,)).fetchone()[0]>=3:raise ValueError('Не более трёх дочерних запусков в MVP')
                chat_id=parent.chat_id;operation=OperationContext(parent=parent.operation)
                spending_policy=json.loads(c.execute('SELECT data FROM runs WHERE id=?',(parent.id,)).fetchone()[0]).get('spending_policy')
            operation=operation or OperationContext()
            handle=RunContext(self,identity,kind,model,base_url.rstrip('/'),api_protocol,chat_id,parent.id if parent else None,operation)
            from .run_policy import validate_spending
            from .auto_budget import local_endpoint
            policy=validate_spending(spending_policy)
            if local_endpoint(base_url):policy={**policy,'enabled':False}
            value={'spending_policy':policy,'id':identity,'parent_id':handle.parent_id,'chat_id':chat_id,'journal_id':journal_id,'kind':kind,
                'model':str(model)[:1024],'connection_id':hashlib.sha256((base_url.rstrip('/')+'|'+api_protocol).encode()).hexdigest(),
                'owner_pid':os.getpid(),'owner_token':self.inspect_owner(os.getpid())[1],'state':'running','created_at':now(),'elapsed_ms':0,'approval_ms':0,'tool_calls':0,'cancel_requested':False,'depth':1 if parent else 0,'fan_out':0}
            c.execute('INSERT INTO runs VALUES(?,?,?,?,?,?)',(identity,chat_id,handle.parent_id,now(),encode(value),value['state']))
            if parent:
                record=json.loads(c.execute('SELECT data FROM runs WHERE id=?',(parent.id,)).fetchone()[0]);record['fan_out']+=1
                c.execute('UPDATE runs SET data=? WHERE id=?',(encode(record),parent.id))
            self.handles[identity]=handle;operation.run_context=handle
            return handle

    def update(self,identity,**changes):
        """Apply host metadata only; call journal and task lifecycle remain separate."""
        with self.ready().transaction() as c:
            row=c.execute('SELECT data FROM runs WHERE id=?',(identity,)).fetchone()
            if not row:raise ValueError('Запуск не найден')
            value=json.loads(row[0]);value.update(changes)
            c.execute('UPDATE runs SET data=?,updated_at=?,state=? WHERE id=?',(encode(value),now(),value['state'],identity))

    def attempt(self,run_id,purpose,reservation):
        """Reserve telemetry before queueing; a reservation is not a physical HTTP attempt or a token charge."""
        identity=uuid.uuid4().hex
        reserve={k:int(reservation.get(k,0)) for k in ('input_tokens_estimate','output_tokens_reserved')}
        value={'id':identity,'run_id':run_id,'purpose':purpose,'state':'active','phase':'queued','http_attempts':0,'usage':None,
            'reservation':reserve,'created_at':now(),'queue_ms':0,'outcome':'pending'}
        with self.ready().transaction() as c:
            from .run_policy import require_spending
            require_spending(c,run_id,reserve)
            c.execute('INSERT INTO inference_attempts VALUES(?,?,?)',(identity,run_id,encode(value)))
            BudgetLedger.apply(c,run_id,None,value)
        return identity

    def record_tool(self,identity):
        """Count one returned tool receipt in this epoch, independent of legacy task counter resets."""
        with self.ready().transaction() as c:
            value=json.loads(c.execute('SELECT data FROM runs WHERE id=?',(identity,)).fetchone()[0]);value['tool_calls']+=1
            c.execute('UPDATE runs SET data=? WHERE id=?',(encode(value),identity))

    def update_attempt(self,identity,**changes):
        """Persist telemetry without request content, headers, credentials or exception text."""
        with self.ready().transaction() as c:
            row=c.execute('SELECT data FROM inference_attempts WHERE id=?',(identity,)).fetchone()
            if not row:return
            value=json.loads(row[0]);before=dict(value);value.update(changes)
            c.execute('UPDATE inference_attempts SET data=? WHERE id=?',(encode(value),identity))
            BudgetLedger.apply(c,value['run_id'],before,value)

    def snapshot(self,identity):
        """Aggregate actual attempts, reported usage and outstanding reservations without imposing caps."""
        with self.ready().transaction() as c:
            row=c.execute('SELECT data FROM runs WHERE id=?',(identity,)).fetchone()
            if not row:raise ValueError('Запуск не найден')
            value=json.loads(row[0])
            from .run_policy import spending_snapshot
            spending=spending_snapshot(c,identity)
            if spending:value['spending']={k:v for k,v in spending.items() if k not in ('_remaining_nanos','policy')}
        value.setdefault('ledger',BudgetLedger.contribution(None))
        with self.lock:handle=self.handles.get(identity)
        if handle and not handle.closed:
            value['elapsed_ms']=round((time.monotonic()-handle.started)*1000)
            if handle.last_phase=='waiting_approval':value['approval_ms']=round(handle.approval_ms+(time.monotonic()-handle.phase_at)*1000)
        return value

    def history(self,chat_id,limit=20):
        """Return bounded selected-chat run history, including prior resume epochs."""
        with self.ready().transaction() as c:ids=[r[0] for r in c.execute('SELECT id FROM runs WHERE chat_id=? ORDER BY updated_at DESC LIMIT ?',(chat_id,min(50,max(1,int(limit)))))]
        return [self.snapshot(identity) for identity in ids]

    def cancel(self,identity):
        """Signal an entire live subtree; never infer that a tool effect was rolled back."""
        with self.lock:
            handle=self.handles.get(identity)
            if handle:handle.operation.set()
            children=[h.id for h in self.handles.values() if h.parent_id==identity and not h.closed]
        if handle:self.update(identity,cancel_requested=True)
        for child in children:self.cancel(child)


class RunContext:
    """One execution epoch with independent identity, inherited cancellation and measured wait time."""
    def __init__(self,registry,identity,kind,model,base_url,api_protocol,chat_id,parent_id,operation):
        self.registry=registry;self.id=identity;self.kind=kind;self.model=model;self.base_url=base_url;self.api_protocol=api_protocol
        self.chat_id=chat_id;self.parent_id=parent_id;self.operation=operation
        self.started=time.monotonic();self.last_phase='running';self.phase_at=self.started;self.approval_ms=0;self.closed=False

    def observe(self,task):
        """Mirror existing lifecycle; waiting for a person is measured separately from generation."""
        if self.closed:return
        stamp=time.monotonic();state=task.get('run_state',task.get('status','running'))
        if state not in ACTIVE|TERMINAL:state='running'
        if self.last_phase=='waiting_approval':self.approval_ms+=(stamp-self.phase_at)*1000
        self.last_phase=state;self.phase_at=stamp
        self.registry.update(self.id,state=state,elapsed_ms=round((stamp-self.started)*1000),approval_ms=round(self.approval_ms))

    def record_tool(self):
        """Record a tool receipt without inferring its effect succeeded or reusing a prior run's counter."""
        if not self.closed:self.registry.record_tool(self.id)

    def finish(self,state='completed'):
        """Close an epoch after transport/tool cleanup; do not replay effects or reuse this identity on resume."""
        if self.closed:return
        with self.registry.lock:
            children=[h for h in self.registry.handles.values() if h.parent_id==self.id and not h.closed]
        if children:
            if state=='completed':raise ValueError('Родитель не завершён: дождитесь дочерних запусков')
            self.registry.cancel(self.id)
        self.observe({'run_state':state})
        self.registry.update(self.id,ended_at=now());self.closed=True
        with self.registry.lock:self.registry.handles.pop(self.id,None)

    def snapshot(self):
        """Read durable metadata, not prompts or filesystem evidence."""
        return self.registry.snapshot(self.id)
