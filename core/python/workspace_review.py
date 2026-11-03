"""User-only diff/confirmation API; model tools cannot invoke workspace rollback."""
import time
import uuid
from agent.chat_store import save_chat
from agent.verifier import StageVerifier
from agent.workspace_snapshots import SnapshotStore


class WorkspaceReview:
    def __init__(self,tasks):
        self.tasks=tasks;self.proposal=None
        from .background_job import BackgroundJob
        self.checkpoint_job=BackgroundJob()

    def scope(self,root,params,*,review=False):
        self.tasks.idle()
        chat=self.tasks.chat
        if not root or not chat or chat['id']!=params.get('chat_id') or chat.get('mode')!='ide' or chat.get('project_root')!=str(root) or chat.get('project_id','')!=self.tasks.project_id:
            raise ValueError('Выберите IDE-чат этого проекта')
        task,_=self.tasks._recover_chat()
        if not review and task and (task.get('recovery_items') or task.get('recovery_error') or task.get('snapshot_attention')):
            raise ValueError('Сначала проверьте незавершённые действия')
        return SnapshotStore(root,chat['id']),task

    def list(self,root,params):
        store,task=self.scope(root,params,review=True)
        from agent.git_checkpoints import GitCheckpoints
        checkpoints=GitCheckpoints(store)
        rows=[{**r,'git_checkpoint':checkpoints.info(r['id'])} for r in store.list()]
        return {'ok':True,'snapshots':rows,'task':task}

    def preview(self,root,params):
        store,_=self.scope(root,params)
        proposal=store.preview(params.get('group_id'))
        self.proposal={**proposal,'id':uuid.uuid4().hex,'chat_id':params['chat_id'],'root':str(root),'expires':time.monotonic()+120}
        return {'ok':True,'proposal':{key:self.proposal[key] for key in ('id','group_id','paths','diff','truncated')}}

    def apply(self,root,params):
        store,task=self.scope(root,params)
        proposal=self.proposal
        self.proposal=None
        if params.get('confirmed') is not True or not proposal or proposal['id']!=params.get('proposal_id') or proposal['chat_id']!=params['chat_id'] or proposal['root']!=str(root) or proposal['expires']<time.monotonic():
            raise ValueError('Подтверждение отката отсутствует или устарело; сравните изменения заново')
        result=store.restore(proposal['group_id'],proposal['fingerprint'])
        from agent.project_index import notify_paths
        notify_paths(root,proposal['paths'])
        if task:
            # Durable revision is reconciled even if the process exits before this projection.
            task,_=self.tasks._recover_chat()
            StageVerifier().refresh(task)
            self.tasks.chat['task_checkpoint']=task
            save_chat(self.tasks.chat,checkpoint=True)
        return {**result,'snapshots':store.list(),'task':task}

    def review(self,root,params):
        store,_=self.scope(root,params,review=True)
        if params.get('confirmed') is not True:raise ValueError('Подтвердите, что вручную проверили файлы после прерванного отката')
        store.review(params.get('group_id'))
        task,_=self.tasks._recover_chat()
        return {'ok':True,'snapshots':store.list(),'task':task}


    def start_checkpoint(self,root,params,respond):
        """Freeze the selected chat/root before dispatch; Git IO never blocks bridge commands."""
        with self.tasks.lock:
            store,_=self.scope(root,params)
            group=params.get('group_id')
            def work(context):
                from agent.git_checkpoints import GitCheckpoints
                return GitCheckpoints(store).create(group,context)
            self.checkpoint_job.start(work,respond,timeout=90)

    def shutdown(self):
        """Cancel owned Git child work during Core shutdown."""
        self.checkpoint_job.shutdown()
