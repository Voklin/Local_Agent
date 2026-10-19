import json
import threading
from .tools import preview_file_change
from .conversation import build_messages
from PySide6.QtCore import QThread, Signal
from openai import OpenAI
from .tools import TOOL_DEFINITIONS, execute_tool

SYSTEM_PROMPT = """Ты локальный помощник по программированию. Отвечай по-русски, если пользователь пишет по-русски.
Для фактов о проекте используй инструменты, а не угадывай. Доступны только файлы внутри выбранной пользователем корневой директории.
Не пытайся читать или изменять файлы вне проекта. Для изменения файлов используй write_file: приложение покажет diff и запросит подтверждение пользователя до записи. Не утверждай, что файл изменён, пока инструмент не вернул ok=true.
Инструменты: list_files, read_file, search_text, write_file. Не раскрывай содержимое секретов, если пользователь не просил его анализировать.
При запросе просмотра папок Users, Windows, профиля пользователя или других каталогов вне проекта объясни, что доступ ограничен выбранной директорией. Не повторяй отклонённый вызов инструмента."""

DEFAULT_SETTINGS = {
    "max_tool_calls": 10,
    "max_consecutive_errors": 3,
    "max_tokens": 2048,
    "max_entries": 200,
    "max_search_depth": 5,
}


class AgentWorker(QThread):
    chat = Signal(str, str)
    log = Signal(str)
    finished_text = Signal(str)
    failed = Signal(str)
    progress = Signal(int, int)
    write_approval_requested = Signal(str, str, bool)
    conversation_updated = Signal(object)

    def __init__(self, base_url, api_key, model, project_root, prompt, force_tool=None, settings=None, history=None):
        super().__init__()
        self.base_url, self.api_key, self.model = base_url, api_key, model
        self.project_root, self.prompt, self.force_tool = project_root, prompt, force_tool
        self.history = list(history or [])
        self.settings = {**DEFAULT_SETTINGS, **(settings or {})}
        self._approval_lock = threading.Lock()
        self._approval_event = None
        self._approval_result = False

    def resolve_write_approval(self, decision):
        """Receive Apply/Reject/Cancel from the GUI without a chat message."""
        if decision not in ("apply", "reject", "cancel"):
            decision = "reject"
        with self._approval_lock:
            self._approval_result = decision
            event = self._approval_event
        if event:
            event.set()

    def _ask_write_approval(self, path, diff, exists):
        event = threading.Event()
        with self._approval_lock:
            self._approval_event = event
            self._approval_result = "reject"
        self.write_approval_requested.emit(path, diff, exists)
        while not event.wait(0.1):
            if self.isInterruptionRequested():
                break
        with self._approval_lock:
            decision = self._approval_result
            self._approval_event = None
        if self.isInterruptionRequested():
            return "cancel"
        return decision

    def run(self):
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key or "no-key", timeout=180, max_retries=0)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(build_messages(self.history, self.prompt))
            final = ""
            tool_calls_count = 0
            consecutive_errors = 0
            stop_reason = ""
            max_tool_calls = max(1, int(self.settings["max_tool_calls"]))
            max_errors = max(1, int(self.settings["max_consecutive_errors"]))
            max_tokens = max(64, int(self.settings["max_tokens"]))

            for turn in range(8):
                if self.isInterruptionRequested():
                    stop_reason = "Остановлено пользователем."
                    break
                kwargs = dict(
                    model=self.model,
                    messages=messages,
                    tools=TOOL_DEFINITIONS,
                    tool_choice="auto",
                    temperature=0.2,
                    max_tokens=max_tokens,
                    stream=True,
                )
                if turn == 0 and self.force_tool:
                    kwargs["tool_choice"] = {"type": "function", "function": {"name": self.force_tool}}
                stream = client.chat.completions.create(**kwargs)
                content_parts = []
                tool_call_parts = {}
                interrupted = False
                try:
                    for chunk in stream:
                        if self.isInterruptionRequested():
                            interrupted = True
                            stream.close()
                            break
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta
                        if delta.content:
                            content_parts.append(delta.content)
                            self.progress.emit(tool_calls_count, max_tool_calls)
                        for tc in (delta.tool_calls or []):
                            item = tool_call_parts.setdefault(tc.index, {"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
                            if tc.id:
                                item["id"] = tc.id
                            if tc.function:
                                if tc.function.name:
                                    item["function"]["name"] += tc.function.name
                                if tc.function.arguments:
                                    item["function"]["arguments"] += tc.function.arguments
                finally:
                    stream.close()
                if interrupted or self.isInterruptionRequested():
                    stop_reason = "Остановлено пользователем."
                    break

                content = "".join(content_parts).strip()
                tool_calls = [tool_call_parts[index] for index in sorted(tool_call_parts)]
                if content:
                    final = content
                    self.chat.emit("assistant", content)
                if not tool_calls:
                    if content:
                        messages.append({"role": "assistant", "content": content})
                    break

                messages.append({
                    "role": "assistant",
                    "content": content or None,
                    "tool_calls": tool_calls,
                })
                hit_limit = False
                for call in tool_calls:
                    if self.isInterruptionRequested():
                        stop_reason = "Остановлено пользователем."
                        hit_limit = True
                        break
                    if tool_calls_count >= max_tool_calls:
                        stop_reason = f"Остановлено: достигнут лимит вызовов инструментов ({max_tool_calls})."
                        hit_limit = True
                        break
                    name = call["function"]["name"]
                    try:
                        args = json.loads(call["function"]["arguments"] or "{}")
                        if not isinstance(args, dict):
                            raise ValueError("Аргументы инструмента должны быть JSON-объектом")
                    except (json.JSONDecodeError, ValueError) as exc:
                        args = {}
                        result = {"ok": False, "error": f"Invalid tool arguments: {exc}"}
                    else:
                        self.log.emit(f"TOOL CALL [{tool_calls_count + 1}/{max_tool_calls}]: {name}({json.dumps(args, ensure_ascii=False)})")
                        if name == "write_file":
                            preview = preview_file_change(self.project_root, args.get("path", ""), args.get("content", ""))
                            if not preview.get("ok"):
                                result = preview
                            elif preview.get("exists") and not bool(args.get("overwrite", False)):
                                result = {"ok": False, "error": "Target exists but overwrite=false; no changes made"}
                            else:
                                decision = self._ask_write_approval(
                                    preview["path"], preview["diff"], preview["exists"]
                                )
                                if decision == "apply":
                                    result = execute_tool(
                                        name, args, self.project_root, self.settings, approved=True
                                    )
                                elif decision == "cancel":
                                    result = {
                                        "ok": False,
                                        "error": "User cancelled the proposed file change; no changes made",
                                        "code": "USER_CANCELLED",
                                    }
                                    stop_reason = "Остановлено пользователем: изменение файла отменено."
                                    hit_limit = True
                                else:
                                    result = {
                                        "ok": False,
                                        "error": "User denied the proposed file change; no changes made",
                                        "code": "USER_DENIED",
                                    }
                        else:
                            result = execute_tool(name, args, self.project_root, self.settings)
                    tool_calls_count += 1
                    self.progress.emit(tool_calls_count, max_tool_calls)
                    pretty = json.dumps(result, ensure_ascii=False, indent=2)
                    self.log.emit(f"TOOL RESULT: {pretty[:12000]}")
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": pretty[:20000]})
                    if result.get("code") == "USER_CANCELLED":
                        hit_limit = True
                        consecutive_errors = 0
                    elif result.get("ok") is True:
                        consecutive_errors = 0
                    else:
                        consecutive_errors += 1
                        self.log.emit(f"TOOL ERROR STREAK: {consecutive_errors}/{max_errors}")
                        if consecutive_errors >= max_errors:
                            stop_reason = f"Остановлено: подряд получено ошибок инструментов — {consecutive_errors} (лимит {max_errors})."
                            hit_limit = True
                            break
                if hit_limit:
                    break
            if self.isInterruptionRequested():
                stop_reason = "Остановлено пользователем."
            if stop_reason:
                self.chat.emit("system", stop_reason)
                self.log.emit(stop_reason)
                final = (final + "\n\n" if final else "") + stop_reason
            if not final:
                final = "Модель завершила обработку без текстового ответа. Посмотри журнал вызовов инструментов."
            self.conversation_updated.emit(messages[1:])
            self.finished_text.emit(final)
        except Exception as exc:
            if self.isInterruptionRequested():
                self.chat.emit("system", "Остановлено пользователем.")
                self.finished_text.emit("Остановлено пользователем.")
            else:
                self.failed.emit(f"{type(exc).__name__}: {exc}")
