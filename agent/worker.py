import json
from PySide6.QtCore import QThread, Signal
from openai import OpenAI
from .tools import TOOL_DEFINITIONS, execute_tool

SYSTEM_PROMPT = """Ты локальный помощник по программированию. Отвечай по-русски, если пользователь пишет по-русски.
Для фактов о проекте используй инструменты, а не угадывай. Доступны только файлы внутри выбранной пользователем корневой директории.
Не пытайся читать файлы вне проекта и не утверждай, что изменил файлы: доступных инструментов записи пока нет.
Инструменты чтения: list_files, read_file, search_text. Не раскрывай содержимое секретов, если пользователь не просил его анализировать."""

class AgentWorker(QThread):
    chat = Signal(str, str)
    log = Signal(str)
    finished_text = Signal(str)
    failed = Signal(str)

    def __init__(self, base_url, api_key, model, project_root, prompt, force_tool=None):
        super().__init__()
        self.base_url, self.api_key, self.model = base_url, api_key, model
        self.project_root, self.prompt, self.force_tool = project_root, prompt, force_tool

    def run(self):
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key or "no-key", timeout=180, max_retries=0)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": self.prompt}]
            final = ""
            for turn in range(8):
                kwargs = dict(model=self.model, messages=messages, tools=TOOL_DEFINITIONS, tool_choice="auto", temperature=0.2)
                if turn == 0 and self.force_tool:
                    kwargs["tool_choice"] = {"type": "function", "function": {"name": self.force_tool}}
                response = client.chat.completions.create(**kwargs)
                msg = response.choices[0].message
                tool_calls = msg.tool_calls or []
                messages.append({"role": "assistant", "content": msg.content, "tool_calls": [tc.model_dump(exclude_none=True) for tc in tool_calls]})
                if msg.content:
                    final = msg.content
                    self.chat.emit("assistant", msg.content)
                if not tool_calls:
                    break
                for call in tool_calls:
                    name = call.function.name
                    try:
                        args = json.loads(call.function.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    self.log.emit(f"TOOL CALL: {name}({json.dumps(args, ensure_ascii=False)})")
                    result = execute_tool(name, args, self.project_root)
                    pretty = json.dumps(result, ensure_ascii=False, indent=2)
                    self.log.emit(f"TOOL RESULT: {pretty[:12000]}")
                    messages.append({"role": "tool", "tool_call_id": call.id, "content": pretty[:20000]})
            if not final:
                final = "Модель завершила обработку без текстового ответа. Посмотри журнал вызовов инструментов."
            self.finished_text.emit(final)
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")
