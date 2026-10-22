"""Qt adapter for the UI-independent agent engine."""
from PySide6.QtCore import QThread, Signal
from .engine import AgentEngine, DEFAULT_SETTINGS, SYSTEM_PROMPT


class AgentWorker(QThread):
    chat = Signal(str, str)
    log = Signal(str)
    finished_text = Signal(str)
    failed = Signal(str)
    progress = Signal(int, int)
    write_approval_requested = Signal(str, str, bool)
    conversation_updated = Signal(object)
    change_event = Signal(object)
    memory_updated = Signal(object)
    task_updated = Signal(object)
    text_delta = Signal(int, str)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._engine = AgentEngine(*args, **kwargs)
        for name in AgentEngine.event_names:
            getattr(self._engine, name).connect(getattr(self, name).emit)

    def run(self):
        self._engine.run()

    def requestInterruption(self):
        self._engine.requestInterruption()

    def isInterruptionRequested(self):
        return self._engine.isInterruptionRequested()

    def resolve_write_approval(self, decision):
        self._engine.resolve_write_approval(decision)

    @property
    def _approval_result(self):
        return self._engine._approval_result
