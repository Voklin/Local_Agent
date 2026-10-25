"""Lightweight, lazy-loaded SKILL.md registry. Skills never become tools by themselves."""
from __future__ import annotations
from pathlib import Path
import re

class SkillManager:
    def __init__(self, root=None):
        self.root = Path(root) if root else Path(__file__).resolve().parent.parent / "skills"
    def discover(self):
        result=[]
        if getattr(self,'disabled',False):return result
        if not self.root.exists(): return result
        for p in sorted(self.root.rglob("SKILL.md")):
            result.append(self._metadata(p))
        return result
    def _metadata(self, path):
        text=path.read_text(encoding="utf-8", errors="replace")[:12000]
        title=path.parent.name
        m=re.search(r"^#\s+(.+)$", text, re.M)
        if m: title=m.group(1).strip()
        return {"id": path.parent.name, "title": title, "path": str(path), "summary": self._summary(text)}
    @staticmethod
    def _summary(text):
        for line in text.splitlines():
            line=line.strip()
            if line and not line.startswith("#") and not line.startswith("-"):
                return line[:300]
        return ""
    def load(self, skill_id):
        for item in self.discover():
            if item["id"] == skill_id:
                return Path(item["path"]).read_text(encoding="utf-8", errors="replace")
        return None
    def select(self, prompt, limit=3):
        words=set(re.findall(r"[\wа-яё]+", (prompt or '').lower()))
        scored=[]
        for item in self.discover():
            hay=(item['id']+' '+item['title']+' '+item['summary']).lower()
            score=sum(1 for w in words if len(w)>2 and w in hay)
            scored.append((score,item))
        return [x[1] for x in sorted(scored,key=lambda x:x[0],reverse=True)[:limit] if x[0]>0]
