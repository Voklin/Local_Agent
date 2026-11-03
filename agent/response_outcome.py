"""Provider-independent terminal response contract; EOF is not completion."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ModelResponseOutcome:
    status: str
    finish_reason: str
    reason: str = ''

    @classmethod
    def classify(cls, finish_reason=None, *, refused=False, cancelled=False, error=False):
        """Normalize explicit terminal evidence without inventing a successful stop."""
        finish = finish_reason or 'unknown'
        if cancelled:
            return cls('cancelled', finish, 'Запрос остановлен.')
        if error:
            return cls('error', finish, 'Ошибка получения ответа модели.')
        if refused or finish in ('refusal', 'content_filter'):
            return cls('refused', 'refusal' if refused else finish,
                       'Модель отказала в ответе или сервер ограничил генерацию.')
        if finish in ('stop', 'tool_calls', 'function_call'):
            return cls('complete', finish)
        reason = ('Ответ оборван лимитом генерации.' if finish == 'length' else
                  'Поток закончился без подтверждения завершения ответа сервером.')
        return cls('incomplete', finish, reason + ' Частичный текст сохранён; можно продолжить задачу.')

    def snapshot(self):
        """Return a JSON-safe public outcome for checkpoints and the task interface."""
        return asdict(self)


def parse_completion_assessment(raw):
    """Accept an explicit boolean only; malformed model output is not evidence."""
    import re
    from .json_tools import strict_json_loads
    text=(raw or '').strip()
    if len(text)>8000:raise ValueError('Проверка завершения слишком велика')
    fenced=re.fullmatch(r'```(?:json)?\s*\n(.*?)\n```',text,re.S)
    if fenced:text=fenced.group(1)
    value=strict_json_loads(text)
    if not isinstance(value,dict) or type(value.get('complete')) is not bool or not isinstance(value.get('reason',''),str):
        raise ValueError('Проверка должна вернуть complete: true/false и текст reason')
    return value['complete'],value.get('reason','')[:500]


def answer_format_issue(prompt, text):
    """Validate an explicitly requested source-location format, never invent a location."""
    import re
    explicit=re.search(r'(?:ответь|отвечай|верни|answer|return)\s+(?:строго\s+|только\s+|only\s+)?(?:в\s+формате|in\s+(?:the\s+)?format)\s+[`"\s]*(?:путь\s*:\s*строка|path\s*:\s*line)',prompt,re.I)
    if explicit and not re.fullmatch(r'[^\r\n`]+:[1-9][0-9]*',(text or '').strip().strip('`')):
        return 'Нужен ровно путь:номер_строки, например src/example.py:42, без кода и пояснений. Используй только подтверждённое место из полученных результатов; пример не является источником.'
    return ''
