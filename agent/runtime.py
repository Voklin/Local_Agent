"""v5.7 orchestration boundary: Planner -> Executor -> Verifier -> Checkpoint."""
from .planner import TaskPlanner, build_plan
from .verifier import StageVerifier
from .context_manager import ContextManager
from .skills import SkillManager
from .mcp import MCPRegistry

class AgentRuntime:
    def __init__(self, task, *, context_chars=80000, skills_root=None):
        self.task=task
        if not task.get('stages') or task.get('version',1)<2:
            task['stages']=build_plan(task.get('prompt',''))
            task['version']=2
            task['stage']=task['stages'][0]['id']
            task['status']='running'
        self.planner=TaskPlanner(task)
        self.verifier=StageVerifier()
        self.context=ContextManager(context_chars)
        self.skills=SkillManager(skills_root)
        self.mcp=MCPRegistry()
    def prepare(self):
        selected=self.skills.select(self.task.get('prompt',''))
        self.task['selected_skills']=[s['id'] for s in selected]
        self.task['runtime_version']='5.7'
        return selected
    def working_context(self,messages):
        selected=[x for x in self.skills.discover() if x['id'] in self.task.get('selected_skills',[])]
        return self.context.build(messages,self.task,selected)
    def checkpoint(self,event):
        self.task['last_event']=str(event)[:500]
        return self.task
    def complete_stage(self, reason=''):
        return self.planner.advance(reason)
