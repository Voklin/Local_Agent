"""Model-facing context projection; never modifies canonical chat messages."""
from __future__ import annotations
from copy import deepcopy
import json
from .conversation import compact_live_messages


class ContextManager:
    def __init__(self, max_chars=80000, recent_rounds=12):
        self.max_chars = max(256, int(max_chars))
        self.recent_rounds = max(2, int(recent_rounds))

    def build(self, messages, task=None, skills=None, request_index=None):
        projected = list(messages)
        meta = []
        if task:
            meta.append({"task_stage": task.get('stage'), "status": task.get('status'),
                         "last_event": task.get('last_event', ''),
                         'next_action': str(task.get('resume_state', {}).get('next_action', ''))[:500]})
        if skills:
            meta.append({"skills": [s.get('id') for s in skills]})
        if meta:
            state = "CURRENT AGENT STATE:\n" + json.dumps(meta, ensure_ascii=False)
            if projected and projected[0].get('role') == 'system':
                projected[0] = deepcopy(projected[0])
                projected[0]['content'] = str(projected[0].get('content', '')) + "\n\n" + state
            else:
                projected.insert(0, {"role": "system", "content": state})
                if request_index is not None:
                    request_index += 1
        return compact_live_messages(projected, self.max_chars, self.recent_rounds, request_index)
