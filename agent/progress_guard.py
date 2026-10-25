"""Detect repeated outcomes, including alternating calls, without blocking progress."""
from collections import deque
import hashlib
import json


class ProgressGuard:
    def __init__(self,window=16,threshold=4):
        self.entries=deque(maxlen=window)
        self.threshold=threshold

    def observe(self,name,arguments,result):
        value=json.dumps([name,arguments,result],sort_keys=True,ensure_ascii=False,default=str)
        fingerprint=hashlib.sha256(value.encode()).hexdigest()
        self.entries.append(fingerprint)
        return sum(item==fingerprint for item in self.entries)>=self.threshold
