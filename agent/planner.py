"""Task planning primitives for the v5.7 agent runtime."""
from __future__ import annotations
import re
from dataclasses import dataclass, asdict

@dataclass
class PlanStage:
    id: str
    title: str
    objective: str = ""
    status: str = "pending"
    max_turns: int = 50

    def to_dict(self): return asdict(self)

_ACTION = re.compile(r"(сделай|добавь|исправь|измени|реализуй|создай|напиши|разработай|проверь|запусти|рефактор|интегр|доработай|implement|create|fix|change|modify|refactor|test|run|build|add)", re.I)

def build_plan(prompt: str) -> list[dict]:
    text = prompt or ""
    stages = [
        PlanStage("analysis", "Анализ", "Понять цель, ограничения и критерии готовности.", max_turns=20),
        PlanStage("research", "Исследование", "Изучить только релевантные части проекта и существующие решения.", max_turns=40),
    ]
    if _ACTION.search(text):
        stages.append(PlanStage("implementation", "Реализация", "Внести необходимые изменения через разрешённые инструменты.", max_turns=100))
        stages.append(PlanStage("verification", "Проверка", "Запустить доступные проверки и убедиться, что результат соответствует задаче.", max_turns=60))
    else:
        stages.append(PlanStage("verification", "Ответ", "Проверить, что ответ полностью покрывает запрос.", max_turns=20))
    stages.append(PlanStage("finish", "Завершение", "Сформировать краткий результат и следующие шаги при необходимости.", max_turns=10))
    return [s.to_dict() for s in stages]

class TaskPlanner:
    def __init__(self, task: dict): self.task = task
    @property
    def current(self):
        sid = self.task.get("stage")
        return next((s for s in self.task.get("stages", []) if s.get("id") == sid), None)
    def advance(self, reason=""):
        stages = self.task.get("stages", [])
        idx = next((i for i,s in enumerate(stages) if s.get("id") == self.task.get("stage")), 0)
        if stages: stages[idx]["status"] = "done"
        if idx + 1 < len(stages):
            stages[idx+1]["status"] = "active"; self.task["stage"] = stages[idx+1]["id"]
        if reason: self.task["last_event"] = reason[:500]
        return self.task
