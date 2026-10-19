"""Bounded working-context builder. Canonical chat history remains untouched."""
from __future__ import annotations
import json

class ContextManager:
    def __init__(self, max_chars=80000, recent_rounds=12):
        self.max_chars=max(256,int(max_chars)); self.recent_rounds=max(2,int(recent_rounds))
    def build(self, messages, task=None, skills=None):
        system=[m for m in messages if m.get('role')=='system'][:1]
        body=[m for m in messages if m.get('role')!='system'][-self.recent_rounds*3:]
        meta=[]
        if task: meta.append({"task_stage":task.get('stage'),"status":task.get('status'),"last_event":task.get('last_event','')})
        if skills: meta.append({"skills":[s.get('id') for s in skills]})
        if meta: body.insert(0,{"role":"system","content":"CURRENT AGENT STATE:\n"+json.dumps(meta,ensure_ascii=False)})
        result=system+body
        while len(json.dumps(result,ensure_ascii=False)) > self.max_chars and len(body) > 3:
            body.pop(0); result=system+body
        encoded = json.dumps(result, ensure_ascii=False)
        if len(encoded) > self.max_chars:
            # Keep the most recent messages but trim their content rather than exceeding the budget.
            budget = max(80, self.max_chars - len(json.dumps(system, ensure_ascii=False)) - 80)
            recent = body[-3:]
            per = max(20, budget // max(1, len(recent)))
            trimmed=[]
            for m in recent:
                item=dict(m)
                if isinstance(item.get('content'), str): item['content']=item['content'][:per]
                trimmed.append(item)
            result=system+trimmed
        return result
