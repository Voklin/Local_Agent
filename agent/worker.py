from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from openai import OpenAI
from PySide6.QtCore import QThread, Signal

from .tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """Ты — локальный coding agent. Отвечай по-русски, если пользователь не попросил иначе.
Ты можешь использовать инструменты list_files, read_file и search_text для изучения выбранного проекта.
Перед выводами о коде изучай реальные файлы через инструменты, не выдумывай структуру проекта.
В этой версии инструменты только для чтения: не утверждай, что изменил файлы или запустил сборку.
Вызывай инструменты через tool calling API, а не печатай JSON вызова в обычном тексте.
Пути инструментов должны быть относительными к корню проекта.
"""


class AgentWorker(QThread):
    log = Signal(str)
    answer = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        project_root: Path,
        user_text: str,
        force_tool: str | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.base_url = base_url.strip()
        self.api_key = api_key.strip() or "no-key"
        self.model = model.strip()
        self.project_root = project_root.resolve()
        self.user_text = user_text
        self.force_tool = force_tool

    def run(self) -> None:
        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=180.0,
                max_retries=0,
            )
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": SYSTEM_PROMPT + f"\nКорень проекта: {self.project_root}"},
                {"role": "user", "content": self.user_text},
            ]
            max_rounds = 8
            for round_no in range(max_rounds):
                self.log.emit(f"Запрос к модели — шаг {round_no + 1}/{max_rounds}")
                kwargs: dict[str, Any] = {
                    "model": self.model,
                    "messages": messages,
                    "tools": TOOL_DEFINITIONS,
                    "tool_choice": "auto",
                    "temperature": 0.2,
                }
                if self.force_tool and round_no == 0:
                    kwargs["tool_choice"] = {
                        "type": "function",
                        "function": {"name": self.force_tool},
                    }
                response = client.chat.completions.create(**kwargs)
                message = response.choices[0].message
                tool_calls = message.tool_calls or []
                assistant_message: dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content or "",
                }
                if tool_calls:
                    assistant_message["tool_calls"] = [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments,
                            },
                        }
                        for call in tool_calls
                    ]
                messages.append(assistant_message)

                if not tool_calls:
                    self.answer.emit(message.content or "(Модель вернула пустой ответ.)")
                    return

                for call in tool_calls:
                    name = call.function.name
                    try:
                        args = json.loads(call.function.arguments or "{}")
                        if not isinstance(args, dict):
                            raise ValueError("Arguments must be a JSON object")
                    except Exception as exc:
                        result: dict[str, Any] = {"error": f"Invalid tool arguments: {exc}"}
                        args = {}
                    else:
                        self.log.emit(f"TOOL CALL: {name}({json.dumps(args, ensure_ascii=False)})")
                        try:
                            result = execute_tool(self.project_root, name, args)
                        except Exception as exc:
                            result = {"error": f"{type(exc).__name__}: {exc}"}
                    pretty = json.dumps(result, ensure_ascii=False, indent=2)
                    self.log.emit(f"TOOL RESULT: {name}\n{pretty[:5000]}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": pretty[:12000],
                    })
            self.answer.emit("Достигнут лимит вызовов модели за один запрос. Попробуй уточнить задачу.")
        except Exception as exc:
            self.error.emit(f"{type(exc).__name__}: {exc}")
