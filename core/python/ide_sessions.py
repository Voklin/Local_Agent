"""Scoped IDE views of the single Core; editor effects never fall back to Python writes."""
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from pathlib import Path
import threading
import time
import uuid

from core.python.session_service import SessionService

IDE_METHODS=frozenset('ide_complete storage_status storage_backup storage_cancel extensions_import runtime_status runtime_start runtime_stop chat_export chat_search chat_update chat_delete chat_fork health list_files read_file list_chats new_chat load_chat rename_chat start_task cancel_task resolve_approval resolve_tool_recovery active_runs run_history update_task_plan get_model_settings configure_model list_models test_model cancel_model_setup connections_list connections_save connections_delete get_project_memory save_project_memory project_memory_action project_index search_project cancel_project_search workspace_access workspace_access_configure extensions_list extensions_configure mcp_discover mcp_cancel_discovery optional_settings optional_configure optional_run optional_cancel snapshot_list snapshot_preview snapshot_apply snapshot_review snapshot_checkpoint snapshot_checkpoint_cancel session_status ide_workspace_changed'.split())
IDE_ROOT=ContextVar('neutral_ide_root',default=None)


class IdeSessions:
    def __init__(self,tasks,emit):
        self.tasks=tasks;self.emit=emit;self.views={};self.pending={};self.lock=threading.RLock()

    def attach(self,root):
        root=Path(root).resolve(strict=True)
        if not root.is_dir():raise ValueError('Нужна папка проекта')
        identity=uuid.uuid4().hex
        session=SessionService(self.tasks.lock,self.tasks.idle,lambda mode:self.tasks.config['model'])
        session.project_id=self.tasks.project_id
        if session.project_id and str(self.tasks.projects.get(session.project_id).get('root','')).casefold()!=str(root).casefold():session.project_id=''
        if not session.project_id:
            matches=[project for project in self.tasks.projects.list() if str(project.get('root','')).casefold()==str(root).casefold()]
            if len(matches)==1:session.project_id=matches[0]['id']
        if self.tasks.chat and self.tasks.chat.get('mode')=='ide' and self.tasks.chat.get('project_root')==str(root):session.chat=self.tasks.chat
        self.views[identity]={'root':root,'session':session,'adapter':IdeWorkspaceAdapter(self,identity)}
        self.tasks.workspace_adapters[str(root)]=self.views[identity]['adapter']
        if session.chat is None:
            with self.scope(identity,'list_chats'):
                catalog=self.tasks.chats(root,'ide')['chats']
                if catalog:self.tasks.select_chat(root,catalog[0]['id'],'ide')
        return {'ok':True,'session_id':identity,'root':str(root),'project_id':session.project_id}

    def detach(self,identity):
        for run in list(self.tasks.runs.values()):
            if getattr(getattr(run,'workspace_adapter',None),'identity',None)==identity and run.task_running:run.cancel()
        return {'ok':True}

    @contextmanager
    def control(self,chat_id):
        run=self.tasks.runs.get(chat_id) if chat_id else None
        if run is None and not chat_id:
            active=[item for item in self.tasks.runs.values() if item.task_running and item.workspace_adapter]
            if len(active)==1:run=active[0]
        if run is None or not run.workspace_adapter:
            yield None;return
        adapter=run.workspace_adapter;view=self.views.get(adapter.identity)
        if not view:
            yield None;return
        session=SessionService(self.tasks.lock,self.tasks.idle,lambda mode:self.tasks.config['model']);session.project_id=run.project_id;session.chat=run.chat
        selected=self.tasks.view_session.set(session);editor=self.tasks.view_adapter.set(adapter);root=IDE_ROOT.set(view['root'])
        try:yield run
        finally:self.tasks.view_session.reset(selected);self.tasks.view_adapter.reset(editor);IDE_ROOT.reset(root)

    @contextmanager
    def scope(self,identity,method):
        if method not in IDE_METHODS:raise ValueError('Операция недоступна из IDE')
        view=self.views.get(identity)
        if not view:raise ValueError('IDE отключена от Core; переподключите панель')
        selection=self.tasks.view_session.set(view['session']);adapter=self.tasks.view_adapter.set(view['adapter']);root=IDE_ROOT.set(view['root'])
        try:yield view['root']
        finally:self.tasks.view_session.reset(selection);self.tasks.view_adapter.reset(adapter);IDE_ROOT.reset(root)

    def request(self,identity,phase,payload,cancelled):
        operation=uuid.uuid4().hex;pending={'event':threading.Event(),'result':None,'session':identity}
        with self.lock:self.pending[operation]=pending
        self.emit({'event':'ide_editor','session_id':identity,'operation_id':operation,'phase':phase,**payload})
        deadline=time.monotonic()+45
        try:
            while not pending['event'].wait(.05):
                if cancelled.is_set() or time.monotonic()>deadline:
                    return {'ok':False,'code':'OUTCOME_UNKNOWN' if phase=='apply' else 'IDE_DISCONNECTED','error':'Редактор не подтвердил операцию. Проверьте буфер и диск перед продолжением.'}
            return pending['result']
        finally:
            with self.lock:self.pending.pop(operation,None)

    def complete(self,params):
        with self.lock:
            pending=self.pending.get(params.get('operation_id'))
            if not pending or pending['session']!=params.get('session_id'):raise ValueError('Операция редактора устарела')
            result=params.get('result')
            if not isinstance(result,dict) or type(result.get('ok')) is not bool:raise ValueError('Некорректный ответ редактора')
            if pending['event'].is_set():raise ValueError('Ответ редактора уже принят')
            pending['result']=deepcopy(result);pending['event'].set()
        return {'ok':True}


class IdeWorkspaceAdapter:
    def __init__(self,owner,identity):
        self.owner=owner;self.identity=identity

    def guard(self,cancelled):
        return self.owner.request(self.identity,'guard',{},cancelled)

    def prepare(self,name,args,preview,cancelled):
        return self.owner.request(self.identity,'prepare',{'name':name,'args':args,'preview':preview},cancelled)

    def execute(self,name,args,preview,cancelled):
        from agent.tools import preview_file_change
        from agent.workspace_edits import preview_mutation
        root=self.owner.views[self.identity]['root']
        current=preview_file_change(root,args['path'],args['content']) if name=='write_file' else preview_mutation(root,name,args)
        if not current.get('ok') or current.get('snapshot')!=preview['snapshot']:
            return {'ok':False,'code':'FILE_CHANGED','error':'Файл или путь изменился после preview; нужно новое подтверждение'}
        return self.owner.request(self.identity,'apply',{'name':name,'args':args,'preview':preview},cancelled)
