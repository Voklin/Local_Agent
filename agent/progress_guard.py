"""Detect repeated outcomes, including alternating calls, without blocking progress."""
from collections import deque
import hashlib
import json


class ProgressGuard:
    def __init__(self,window=16,threshold=4,task=None):
        self.task=task
        prior=(task or {}).get('progress_watchdog',{})
        self.entries=deque(prior.get('entries',[]),maxlen=window)
        self.errors=deque(prior.get('errors',[]),maxlen=window)
        self.recoveries=prior.get('recovery_attempts',0)
        self.threshold=threshold

    def observe(self,name,arguments,result):
        volatile={'_run_id','_receipt','snapshot_group_id','workspace_generation','run_id','elapsed_ms','elapsed_seconds','updated_at','created_at','started_at','finished_at'}
        def stable(value):
            if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if k not in volatile}
            if isinstance(value,list):return [stable(v) for v in value]
            return value
        observed=stable(result)
        value=json.dumps([name,arguments,observed],sort_keys=True,ensure_ascii=False,default=str)
        fingerprint=hashlib.sha256(value.encode()).hexdigest()
        self.entries.append(fingerprint)
        error=hashlib.sha256(json.dumps([result.get('code'),result.get('error')],sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest() if not result.get('ok') else ''
        self.errors.append(error)
        if self.task is not None:self.task['progress_watchdog']={'entries':list(self.entries),'errors':list(self.errors),'recovery_attempts':self.recoveries}
        return sum(item==fingerprint for item in self.entries)>=self.threshold or bool(error and sum(item==error for item in self.errors)>=self.threshold)

    def recover_or_stop(self):
        if self.recoveries:return 'stop'
        self.recoveries=1
        if self.task is not None:self.task['progress_watchdog']['recovery_attempts']=1
        return 'diagnose'
