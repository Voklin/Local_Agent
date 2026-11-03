"""In-memory run lifecycle, separate from plan stages and persistence."""
from __future__ import annotations

from typing import Any


class InvalidRunStateTransition(ValueError):
    """An unknown phase or a transition outside the run lifecycle."""


_ACTIVE_PHASES = frozenset({'running', 'waiting_approval', 'executing', 'verifying'})
_STOPPED_PHASES = frozenset({'needs_attention', 'paused', 'failed'})
_PHASES = _ACTIVE_PHASES | _STOPPED_PHASES | {'completed'}
_TRANSITIONS = {
    'running': _ACTIVE_PHASES | _STOPPED_PHASES | {'completed'},
    'waiting_approval': {'running', 'executing'} | _STOPPED_PHASES,
    'executing': _ACTIVE_PHASES | _STOPPED_PHASES | {'completed'},
    'verifying': _ACTIVE_PHASES | _STOPPED_PHASES | {'completed'},
    'needs_attention': {'running'} | _STOPPED_PHASES,
    'paused': {'running'} | _STOPPED_PHASES,
    'failed': {'running'} | _STOPPED_PHASES,
    'completed': frozenset(),
}
_EVENTS = {
    'running': 'Задача выполняется',
    'waiting_approval': 'Ожидание подтверждения',
    'executing': 'Выполнение инструмента',
    'verifying': 'Проверка результата',
    'completed': 'Задача завершена',
    'needs_attention': 'Требуется внимание: результат исполнения не подтверждён',
    'paused': 'Задача приостановлена',
    'failed': 'Ошибка выполнения задачи',
}


class RunState:
    """Mutate one task's lifecycle; callers own checkpoint persistence.

    Legacy ``status`` is maintained for existing UI consumers. Plan ``stage``
    and ``stages`` are intentionally independent of the execution lifecycle.
    Passing ``None`` provides the same transitions without a persisted task.
    """

    def __init__(self, task: dict[str, Any] | None):
        if task is not None and not isinstance(task, dict):
            raise TypeError('RunState requires a task dictionary or None')
        self.task = task
        if task is None:
            self._phase = 'running'
            return
        phase = task.get('run_state')
        if phase is None:
            phase = {'running': 'running', 'paused': 'paused',
                     'completed': 'completed'}.get(task.get('status', 'running'), 'needs_attention')
        self._validate_phase(phase)
        self._phase = phase
        task['run_state'] = phase
        task['status'] = self._legacy_status(phase)
        task.setdefault('stop_reason', '')
        task.setdefault('last_event', _EVENTS[phase])

    @property
    def phase(self) -> str:
        """Read shared task state so multiple controllers cannot become stale."""
        return self.task['run_state'] if self.task is not None else self._phase

    @staticmethod
    def _validate_phase(phase: str) -> None:
        if not isinstance(phase, str) or phase not in _PHASES:
            raise InvalidRunStateTransition(f'Unknown run phase: {phase!r}')

    @staticmethod
    def _legacy_status(phase: str) -> str:
        if phase in _ACTIVE_PHASES:
            return 'running'
        return 'completed' if phase == 'completed' else 'paused'

    def transition(self, phase: str, reason: str = '') -> str:
        """Apply a valid transition and return the resulting phase.

        Repeating a phase without a reason preserves its event and stop reason.
        Active phases clear a previous stop reason. Completed runs cannot be
        reopened; stopped runs must return to ``running`` before execution.
        """
        self._validate_phase(phase)
        current = self.phase
        self._validate_phase(current)
        if phase != current and phase not in _TRANSITIONS[current]:
            raise InvalidRunStateTransition(f'Cannot transition run from {current!r} to {phase!r}')
        reason = str(reason or '')[:500]
        if self.task is not None:
            task = self.task
            task['run_state'] = phase
            task['status'] = self._legacy_status(phase)
            if phase in _ACTIVE_PHASES:
                task['stop_reason'] = ''
            elif reason or phase != current:
                task['stop_reason'] = reason or ('' if phase == 'completed' else _EVENTS[phase])
            if phase != current or reason:
                task['last_event'] = reason or _EVENTS[phase]
        self._phase = phase
        return phase

    def revise_plan(self):
        """A trusted user revision reopens the task checkpoint, not the completed run epoch."""
        if self.phase!='completed':return
        reason='План изменён пользователем. Проверьте шаги и продолжите задачу.'
        self.task.update(run_state='paused',status='paused',stop_reason=reason,last_event=reason)
        self._phase='paused'
