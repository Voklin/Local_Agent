"""Fast per-operation index access policy plus actual ancestor .gitignore rules."""
import hashlib
import json
from pathlib import Path
from .workspace_access import WorkspaceAccessPolicy
from .workspace_search import EXCLUDED


class IndexPolicy:
    """Keep one bounded policy snapshot per scan/query; retrieval always builds a fresh one."""
    def __init__(self,root):
        self.access=WorkspaceAccessPolicy(root);self.root=self.access.root;self.ignores={};self.decisions={}
        self.version=hashlib.sha256(json.dumps({'exceptions':self.access.exceptions,'patterns':self.access.patterns},sort_keys=True).encode()).hexdigest()

    def rules(self,directory):
        """Compile a directory's GitWildMatch rules once without following ignore-file symlinks."""
        if directory not in self.ignores:
            import pathspec
            path=self.root/directory/'.gitignore'
            if path.is_symlink():raise ValueError('.gitignore не должен быть ссылкой')
            raw=b''
            if path.exists():
                self.access.require(path)
                with path.open('rb') as source:raw=source.read(64001)
            if len(raw)>64000:raise ValueError('.gitignore превышает 64 КБ')
            self.ignores[directory]=(pathspec.GitIgnoreSpec.from_lines(raw.decode('utf-8-sig').splitlines()),hashlib.sha256(raw).hexdigest())
        return self.ignores[directory]

    def permits(self,relative,directory=False):
        """Check fixed excludes, model grants and Git ignore rules including nested negation."""
        key=(relative,directory)
        if key not in self.decisions:self.decisions[key]=self._permits(relative,directory)
        return self.decisions[key]

    def _permits(self,relative,directory):
        """Evaluate a path once within this policy snapshot; every query gets a new snapshot."""
        parts=relative.replace('\\','/').split('/')
        if any(p in EXCLUDED or p.startswith('.local-agent-tmp-') for p in parts):return False
        if not self.access.allows(relative):return False
        for end in range(1,len(parts)+1):
            ignored=False
            for depth in range(end):
                parent='/'.join(parts[:depth]);local='/'.join(parts[depth:end])+('/' if end<len(parts) or directory else '')
                spec,_=self.rules(parent);match=spec.check_file(local)
                if match.include is not None:ignored=match.include
            if ignored:return False
        return True

    def anchor_policy(self,relative):
        """Identify the access policy and ancestor Git rules used for this exact source."""
        parts=relative.split('/')
        values=[self.version]+[self.rules('/'.join(parts[:i]))[1] for i in range(len(parts))]
        return hashlib.sha256(json.dumps(values).encode()).hexdigest()
