"""Validated tool dispatch with durable boundaries around side effects."""
from copy import deepcopy
import hashlib
import json
import sqlite3

from .tools import execute_tool, preview_file_change, validate_tool_arguments
from .task_activity import begin_tool, update_tool, finish_tool
from .workspace_edits import MUTATION_TOOLS, preview_mutation, record_workspace_change
from .verification_evidence import command_scope,capture_witness,make_receipt,now

READ_ONLY_TOOLS = frozenset({'list_files','read_file','search_text','skills_list','skill_view',
    'search_files','search_symbols','project_outline',
    'read_tool_result','discover_mcp_tools','discover_tools',
    'search_project_memory','delegate_readonly','read_range','glob_files','get_project_instructions','set_task_plan','update_task_step',
    'get_local_time','calculate','list_notes','list_timers','list_applications',
    'read_allowed_file','list_allowed_folder'})


class ToolPolicy:
    def __init__(self, definitions, read_only=False):
        self.read_only=read_only
        self.definitions = {item['function']['name']:deepcopy(item) for item in definitions}

    def validate(self, call):
        name = call['function']['name']
        if name not in self.definitions:raise ValueError('Инструмент не разрешён для этого режима')
        from .json_tools import strict_json_loads
        arguments = strict_json_loads(call['function'].get('arguments') or '{}')
        validate_tool_arguments(self.definitions[name], arguments)
        return name, arguments

    @staticmethod
    def effectful(name):
        # External MCP annotations are descriptive, not permission guarantees.
        return name not in READ_ONLY_TOOLS


class ToolExecutor:
    def __init__(self, root, definitions, handler, settings, interrupted, *, task,
                 journal, state, checkpoint, approve_write, change, approval_tools=(), preview=None, runner=None, instruction_guard=None):
        self.root,self.handler,self.settings,self.interrupted=root,handler,settings,interrupted
        self.task,self.journal,self.state=task,journal,state
        self.checkpoint,self.approve_write,self.change=checkpoint,approve_write,change
        self.policy=ToolPolicy(definitions, bool((task or {}).get('options',{}).get('read_only')))
        self.preview=preview or preview_file_change
        self.runner=runner or execute_tool
        self.approval_tools=frozenset(approval_tools)
        self.index=None;self.current=None;self.activity=None;self.denied=False
        self.started=False
        self.instruction_guard=instruction_guard
        self.snapshot_store=None;self.snapshot_id=None
        self.workspace_adapter=None
        self.command_revision=None
        self.command_scope=None;self.command_started=None;self.command_arguments={}
        self.denied_calls=set();self.denial_key=None

    @staticmethod
    def _denial_key(name, arguments):
        """Ignore command labels when remembering an explicit denial within this run."""
        if name=='run_project_command':
            from .task_contract import command_key
            return name+':'+command_key(arguments)
        return name+':'+hashlib.sha256(json.dumps(arguments,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

    def prepare_batch(self, calls, message_index, content=None):
        if self.journal:self.journal.prepare_batch(calls,message_index,content)
        self.index=message_index

    def _access_guard(self,args):
        """Re-evaluate current policy both before preview and immediately before a file effect."""
        from .workspace_access import WorkspaceAccessPolicy
        try:
            access=WorkspaceAccessPolicy(self.root)
            for key in ('path','destination'):
                if args.get(key):access.require(args[key],mutation=True)
        except (ValueError,OSError) as exc:
            return {'ok':False,'code':'ACCESS_DENIED','error':str(exc)[:500]}
        return None

    def _phase(self, phase, status, summary):
        if self.journal:self.journal.set_phase(self.index,self.current['id'],phase,
            effectful=self.policy.effectful(self.current['function']['name']))
        if phase=='started':self.started=True
        update_tool(self.task,self.activity,status,summary)
        self.checkpoint(None,summary)

    def before_external_approval(self):
        if not self.current:return
        self.state.transition('waiting_approval')
        self._phase('awaiting_approval','awaiting_approval','Ожидается подтверждение внешнего действия')

    def after_external_approval(self, allowed):
        if not self.current:return
        self.denied=not allowed
        if allowed and self.current['function']['name']=='run_project_command':
            self._begin_command()
        self.state.transition('executing' if allowed else 'running')
        if allowed:self._phase('started','running','Выполняется подтверждённое действие')

    def command_approval_note(self):
        """Show the user-declared evidence boundary alongside the program approval."""
        if not self.current or self.current['function']['name']!='run_project_command':return ''
        scope=command_scope(self.task,self.command_arguments)
        if scope['kind']=='workspace':return '\n\nОбласть подтверждения: весь проект (полная сверка исходников).'
        return ('\n\nОбласть подтверждения: только выбранные файлы:\n'+'\n'.join(scope['files'])+
            '\nОбъявленные зависимости:\n'+('\n'.join(scope['dependencies']) or 'Не указаны')+
            '\nОстальной проект не сверяется. Команда при этом запускается как обычная программа; список файлов не ограничивает её доступ.')

    def _begin_command(self):
        """Capture the approved source state before dispatch, excluding approval wait from execution time."""
        self.command_scope=command_scope(self.task,self.command_arguments)
        self.command_revision=capture_witness(self.root,self.command_scope)
        self.command_rollback=(self.task or {}).get('observed_rollback_revision',0)
        self.command_generation=(self.task or {}).get('workspace_generation',0)
        self.command_started=now()

    def _finish(self, result):
        if not isinstance(result,dict) or type(result.get('ok')) is not bool:
            result={'ok':False,'error':'Инструмент вернул неверный формат',
                    'code':'OUTCOME_UNKNOWN' if self.policy.effectful(self.current['function']['name']) else 'TOOL_ERROR'}
        if result.get('code')=='OUTCOME_UNKNOWN' or result.get('outcome_unknown') is True:
            result={**result,'ok':False,'code':'OUTCOME_UNKNOWN'}
        if self.denied:
            result={**result,'ok':False,'code':'USER_CANCELLED' if self.interrupted.is_set() else 'USER_DENIED'}
        if result.get('code')=='USER_DENIED' and self.denial_key:self.denied_calls.add(self.denial_key)
        if self.snapshot_id:
            result=self.snapshot_store.finish(self.snapshot_id,result)
        if self.task:
            from .workspace_snapshots import FILE_TOOLS
            generation=self.task.get('workspace_generation',0)
            if self.current['function']['name'] in FILE_TOOLS and result.get('ok') and not result.get('unchanged'):
                generation+=1
            if self.current['function']['name'] in FILE_TOOLS or self.current['function']['name']=='run_project_command':result={**result,'workspace_generation':generation}
            self.task['workspace_generation']=generation
        if self.current['function']['name']=='run_project_command':
            scope=self.command_scope or command_scope(self.task,self.command_arguments)
            before=self.command_revision or {'complete':False,'digest':None,'error':'Команда не начиналась'}
            after=capture_witness(self.root,scope) if self.command_started else dict(before)
            receipt=make_receipt(self.command_arguments,scope,before,after,result,started_at=self.command_started,
                rollback_revision=getattr(self,'command_rollback',0),generation=getattr(self,'command_generation',0))
            result={**result,'workspace_revision':before,'verification_receipt':receipt}
        # Receipt is durable before it is sent to a model or chat projection.
        result={k:v for k,v in result.items() if k!='_run_id'}
        result['_receipt']={'message_index':self.index,'call_id':self.current['id']}
        if self.task and self.task.get('run_id'):result['_run_id']=self.task['run_id']
        if self.journal:self.journal.record_result(self.index,self.current['id'],result)
        if self.current['function']['name']=='run_project_command' and self.started:
            from .project_index import get_index
            try:
                index=get_index(self.root)
                if index:index.reconcile_command(self.command_arguments.get('cwd','.'))
            except (OSError,ValueError,sqlite3.Error):pass
        finish_tool(self.task,self.activity,self.current['function']['name'],result)
        record_workspace_change(self.task,self.current['function']['name'],result,self.current['id'],self.index)
        if self.task:self.task['pending_write']=None
        self.checkpoint(None,'Результат инструмента сохранён')
        return result

    def reject(self, call, error, code='TOOL_LIMIT'):
        return self.execute(call, blocked={'ok':False,'error':error,'code':code})

    def execute(self, call, blocked=None):
        self.current=call;self.denied=False;self.started=False;self.snapshot_id=None;self.command_revision=None
        self.denial_key=None
        self.command_scope=None;self.command_started=None;self.command_arguments={}
        name=call['function']['name']
        try:args=json.loads(call['function'].get('arguments') or '{}')
        except (ValueError,TypeError):args={}
        self.activity=begin_tool(self.task,name,args,call['id'],self.index)
        self.checkpoint(None,'Подготовлен инструмент '+name)
        try:
            if blocked is not None:return self._finish(blocked)
            if self.policy.read_only and self.policy.effectful(name):
                return self._finish({'ok':False,'code':'READ_ONLY','error':'Режим только чтения: изменения, программы и внешние действия отключены'})
            try:name,args=self.policy.validate(call)
            except (ValueError,TypeError,KeyError) as exc:
                return self._finish({'ok':False,'code':'INVALID_TOOL_ARGUMENTS','error':'Invalid tool arguments: '+str(exc)[:500]})
            if name=='run_project_command':self.command_arguments=deepcopy(args)
            self.denial_key=self._denial_key(name,args)
            if self.denial_key in self.denied_calls:
                return self._finish({'ok':False,'code':'USER_DENIED',
                    'error':'Пользователь уже отклонил это действие в текущем запуске. Оно не выполнялось; не запрашивайте его повторно.'})
            if name in MUTATION_TOOLS or name=='write_file':
                denied=self._access_guard(args)
                if denied:return self._finish(denied)
            if self.interrupted.is_set():return self._finish({'ok':False,'code':'USER_CANCELLED','error':'Остановлено пользователем'})
            if name=='write_file':return self._finish(self._write(args))
            if name in MUTATION_TOOLS:return self._finish(self._mutate(name,args))
            self.state.transition('executing')
            if name not in self.approval_tools:self._phase('started','running','Выполняется инструмент '+name)
            if name=='run_project_command' and name not in self.approval_tools:
                self._begin_command()
            try:
                result=self.handler(name,args) if self.handler else self.runner(name,args,self.root,self.settings)
            except Exception as exc:
                result={'ok':False,'code':'OUTCOME_UNKNOWN' if self.started and self.policy.effectful(name) else 'TOOL_ERROR',
                        'error':'Ошибка инструмента: '+(str(exc)[:500] if isinstance(exc,(ValueError,PermissionError,FileNotFoundError)) else type(exc).__name__)}
            if name in self.approval_tools and isinstance(result,dict) and result.get('ok') and not self.started:
                result={'ok':False,'code':'OUTCOME_UNKNOWN','error':'Внешний обработчик не подтвердил границу исполнения. Проверьте результат действия.'}
            return self._finish(result)
        finally:
            self.current=None;self.activity=None

    def _write(self, args):
        if self.instruction_guard:
            blocked=self.instruction_guard(args)
            if blocked:return blocked
        try:preview=self.preview(self.root,args['path'],args['content'])
        except (OSError,ValueError,TypeError) as exc:
            preview={'ok':False,'error':'Не удалось подготовить diff: '+str(exc)[:500]}
        if not preview.get('ok'):
            self.change(args.get('path',''),'',False,'error',preview.get('error',''))
            return preview
        if preview['exists'] and not args.get('overwrite',False):
            result={'ok':False,'error':'Target exists but overwrite=false; no changes made'}
            self.change(preview['path'],preview['diff'],True,'rejected',result['error'])
            return result
        if self.workspace_adapter:
            editor=self.workspace_adapter.prepare('write_file',args,preview,self.interrupted)
            if not editor.get('ok'):return editor
            preview['editor_state']=editor.get('editor_state')
        if self.task:
            self.task['pending_write']={'path':preview['path'],'call_id':self.current['id'],
                'message_index':self.index,'status':'awaiting_approval','snapshot':preview['snapshot']}
        self.state.transition('waiting_approval')
        self._phase('awaiting_approval','awaiting_approval','Ожидается решение по diff')
        self.change(preview['path'],preview['diff'],preview['exists'],'pending','')
        decision=self.approve_write(preview['path'],preview['diff'],preview['exists'])
        if decision!='apply' or self.interrupted.is_set():
            cancelled=decision=='cancel' or self.interrupted.is_set()
            result={'ok':False,'code':'USER_CANCELLED' if cancelled else 'USER_DENIED',
                    'error':'User cancelled the proposed file change; no changes made' if cancelled else 'User denied the proposed file change; no changes made'}
            self.state.transition('running')
            self.change(preview['path'],preview['diff'],preview['exists'],'cancelled' if cancelled else 'rejected',result['error'])
            return result
        if self.task:self.task['pending_write']['status']='applying'
        if self.instruction_guard:
            blocked=self.instruction_guard(args)
            if blocked:
                self.state.transition('running')
                self.change(preview['path'],preview['diff'],preview['exists'],'error',blocked['error'])
                return blocked
        captured=self._capture_snapshot('write_file',args,preview)
        if captured:return captured
        self.state.transition('executing')
        self._phase('started','applying','Записывается подтверждённое изменение')
        try:result=self.workspace_adapter.execute('write_file',args,preview,self.interrupted) if self.workspace_adapter else self.runner('write_file',args,self.root,self.settings,approved=True,expected_snapshot=preview['snapshot'])
        except Exception as exc:result={'ok':False,'code':'OUTCOME_UNKNOWN','error':'Запись могла завершиться до ошибки: '+type(exc).__name__}
        if result.get('ok') and self.task:
            paths=self.task.setdefault('modified_files',[])
            if preview['path'] not in paths:paths.append(preview['path'])
        self.change(preview['path'],preview['diff'],preview['exists'],'applied' if result.get('ok') else 'error',result.get('error',''))
        return result

    def _mutate(self, name, args):
        if self.instruction_guard:
            blocked=self.instruction_guard(args)
            if blocked:return blocked
        try:preview=preview_mutation(self.root,name,args)
        except (OSError,ValueError,PermissionError) as exc:return {'ok':False,'error':str(exc)[:500]}
        if not preview.get('ok'):return preview
        if preview.get('unchanged'):return {'ok':True,'path':preview['path'],'operation':name,'unchanged':True}
        if self.workspace_adapter:
            editor=self.workspace_adapter.prepare(name,args,preview,self.interrupted)
            if not editor.get('ok'):return editor
            preview['editor_state']=editor.get('editor_state')
        if self.task:self.task['pending_write']={'path':preview['path'],'call_id':self.current['id'],
            'message_index':self.index,'status':'awaiting_approval','snapshot':preview['snapshot'],'operation':name}
        self.state.transition('waiting_approval');self._phase('awaiting_approval','awaiting_approval','Ожидается подтверждение файловой операции')
        self.change(preview['path'],preview['diff'],preview['exists'],'pending','')
        decision=self.approve_write(preview['path'],preview['diff'],preview['exists'])
        if decision!='apply' or self.interrupted.is_set():
            cancelled=decision=='cancel' or self.interrupted.is_set()
            self.state.transition('running')
            self.change(preview['path'],preview['diff'],preview['exists'],'cancelled' if cancelled else 'rejected','Изменение не применено')
            return {'ok':False,'code':'USER_CANCELLED' if cancelled else 'USER_DENIED','error':'Изменение не применено'}
        if self.instruction_guard:
            blocked=self.instruction_guard(args)
            if blocked:
                self.state.transition('running');self.change(preview['path'],preview['diff'],preview['exists'],'error',blocked['error']);return blocked
        if self.task:self.task['pending_write']['status']='applying'
        captured=self._capture_snapshot(name,args,preview)
        if captured:return captured
        self.state.transition('executing');self._phase('started','applying','Применяется подтверждённая файловая операция')
        try:result=self.workspace_adapter.execute(name,args,preview,self.interrupted) if self.workspace_adapter else self.runner(name,args,self.root,self.settings,approved=True,expected_snapshot=preview['snapshot'],cancelled=self.interrupted)
        except Exception as exc:result={'ok':False,'code':'OUTCOME_UNKNOWN','error':'Исход файловой операции неизвестен: '+type(exc).__name__}
        self.change(preview['path'],preview['diff'],preview['exists'],'applied' if result.get('ok') else 'error',result.get('error',''))
        return result

    def _capture_snapshot(self, name, args, preview):
        """A failed before-image write prevents the corresponding file effect."""
        denied=self._access_guard(args)
        if denied:return denied
        if not self.task or not self.task.get('journal_id'):return None
        from .workspace_snapshots import SnapshotStore
        try:
            if self.snapshot_store is None:self.snapshot_store=SnapshotStore(self.root,self.task['chat_id'],self.task['journal_id'])
            self.snapshot_id,group=self.snapshot_store.prepare(name,args,preview,self.index,self.current['id'])
            self.task['snapshot_group_id']=group
        except (OSError,ValueError) as exc:
            return {'ok':False,'code':'SNAPSHOT_FAILED','error':'Изменение не начато: не удалось сохранить исходник. '+str(exc)[:300]}
        return None
