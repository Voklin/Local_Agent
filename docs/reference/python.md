# Справочник Python

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [agent/__init__.py](#module-agent-init-py)
- [agent/chat_store.py](#module-agent-chat-store-py)
- [agent/companion_preferences.py](#module-agent-companion-preferences-py)
- [agent/context_manager.py](#module-agent-context-manager-py)
- [agent/conversation.py](#module-agent-conversation-py)
- [agent/delegation.py](#module-agent-delegation-py)
- [agent/editor_io.py](#module-agent-editor-io-py)
- [agent/engine.py](#module-agent-engine-py)
- [agent/ide_coordinator.py](#module-agent-ide-coordinator-py)
- [agent/ide_workflow.py](#module-agent-ide-workflow-py)
- [agent/json_tools.py](#module-agent-json-tools-py)
- [agent/mcp.py](#module-agent-mcp-py)
- [agent/model_client.py](#module-agent-model-client-py)
- [agent/model_discovery.py](#module-agent-model-discovery-py)
- [agent/model_gateway.py](#module-agent-model-gateway-py)
- [agent/model_lifecycle.py](#module-agent-model-lifecycle-py)
- [agent/model_manager.py](#module-agent-model-manager-py)
- [agent/model_preferences.py](#module-agent-model-preferences-py)
- [agent/model_probe.py](#module-agent-model-probe-py)
- [agent/planner.py](#module-agent-planner-py)
- [agent/process_job.py](#module-agent-process-job-py)
- [agent/project_memory.py](#module-agent-project-memory-py)
- [agent/runtime.py](#module-agent-runtime-py)
- [agent/security.py](#module-agent-security-py)
- [agent/skills.py](#module-agent-skills-py)
- [agent/smart_context.py](#module-agent-smart-context-py)
- [agent/task_activity.py](#module-agent-task-activity-py)
- [agent/task_store.py](#module-agent-task-store-py)
- [agent/tools.py](#module-agent-tools-py)
- [agent/ui.py](#module-agent-ui-py)
- [agent/verifier.py](#module-agent-verifier-py)
- [agent/worker.py](#module-agent-worker-py)
- [core/python/assistant_service.py](#module-core-python-assistant-service-py)
- [core/python/bridge.py](#module-core-python-bridge-py)
- [core/python/desktop_service.py](#module-core-python-desktop-service-py)
- [core/python/editor_service.py](#module-core-python-editor-service-py)
- [core/python/memory_service.py](#module-core-python-memory-service-py)
- [core/python/neural_speech.py](#module-core-python-neural-speech-py)
- [core/python/project_search.py](#module-core-python-project-search-py)
- [core/python/runtime_service.py](#module-core-python-runtime-service-py)
- [core/python/speech_service.py](#module-core-python-speech-service-py)
- [core/python/task_service.py](#module-core-python-task-service-py)
- [core/python/telegram_service.py](#module-core-python-telegram-service-py)
- [core/python/transcription_service.py](#module-core-python-transcription-service-py)
- [main.py](#module-main-py)
- [tools/build_windows_core.py](#module-tools-build-windows-core-py)
- [tools/check_docs.py](#module-tools-check-docs-py)
- [tools/check_live_model.py](#module-tools-check-live-model-py)
- [tools/doc_notes.py](#module-tools-doc-notes-py)
- [tools/generate_code_reference.py](#module-tools-generate-code-reference-py)
- [tools/prepare_windows_dependencies.py](#module-tools-prepare-windows-dependencies-py)
- [tools/tts/piper_server.py](#module-tools-tts-piper-server-py)
- [tools/tts/qwen_server.py](#module-tools-tts-qwen-server-py)
- [tools/tts/training/export_and_evaluate.py](#module-tools-tts-training-export-and-evaluate-py)
- [tools/tts/training/generate_serena.py](#module-tools-tts-training-generate-serena-py)
- [tools/tts/training/pipeline.py](#module-tools-tts-training-pipeline-py)
- [tools/tts/training/run_training.py](#module-tools-tts-training-run-training-py)

<a id="module-agent-init-py"></a>

## `agent/__init__.py`

Маркер Python-пакета agent; не запускает UI или модель.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-agent-chat-store-py"></a>

## `agent/chat_store.py`

JSON-чаты и индекс истории вне папки проекта.

### `_valid_id`

[Исходник](../../agent/chat_store.py#L19)

```python
def _valid_id(chat_id)
```

Проверяет 32-символьный hex UUID до доступа к пути файла чата.

### `_now`

[Исходник](../../agent/chat_store.py#L23)

```python
def _now() -> str
```

Возвращает UTC ISO-время для метаданных чата.

### `_atomic_write`

[Исходник](../../agent/chat_store.py#L27)

```python
def _atomic_write(path: Path, data: Any) -> None
```

Записывает JSON через временный файл и replace; общую транзакцию чата с индексом не создаёт.

### `_load_index`

[Исходник](../../agent/chat_store.py#L41)

```python
def _load_index() -> list[dict[str, Any]]
```

Читает индекс; при отсутствующем или повреждённом JSON возвращает пустой список.

### `list_chats`

[Исходник](../../agent/chat_store.py#L51)

```python
def list_chats() -> list[dict[str, Any]]
```

Возвращает метаданные чатов по убыванию updated_at; фильтрацию проекта делает сервис.

### `_metadata`

[Исходник](../../agent/chat_store.py#L55)

```python
def _metadata(chat)
```

Выбирает строковые метаданные канонического чата для производного индекса.

### `_cache_chat`

[Исходник](../../agent/chat_store.py#L59)

```python
def _cache_chat(chat=None, deleted_id=None)
```

Обновляет производный индекс; отказ возвращает предупреждение, сохраняя канонический JSON.

### `read_chat_catalog`

[Исходник](../../agent/chat_store.py#L72)

```python
def read_chat_catalog()
```

Сканирует канонические чаты, восстанавливает индекс и сообщает о повреждениях, не изменяя повреждённые исходники.

### `create_chat`

[Исходник](../../agent/chat_store.py#L97)

```python
def create_chat(project_root: str='', model: str='', title: str='Новый чат', mode=None) -> dict[str, Any]
```

Генерирует UUID, создаёт запись и добавляет её метаданные в индекс.

### `load_chat`

[Исходник](../../agent/chat_store.py#L119)

```python
def load_chat(chat_id: str) -> dict[str, Any] | None
```

Проверяет UUID и структуру JSON; отсутствие возвращает None, повреждение даёт ошибку с сохранением исходного файла.

### `save_chat`

[Исходник](../../agent/chat_store.py#L134)

```python
def save_chat(chat: dict[str, Any]) -> str | None
```

С fsync атомарно сохраняет чат; отказ производного индекса возвращает предупреждение, не отменяя сохранённую историю.

### `delete_chat`

[Исходник](../../agent/chat_store.py#L145)

```python
def delete_chat(chat_id: str) -> bool
```

Удаляет файл диалога и запись индекса; не меняет файлы проекта.

### `rename_chat`

[Исходник](../../agent/chat_store.py#L158)

```python
def rename_chat(chat_id: str, title: str) -> dict[str, Any] | None
```

Нормализует заголовок до 120 символов и сохраняет существующий чат.

### `title_from_messages`

[Исходник](../../agent/chat_store.py#L166)

```python
def title_from_messages(messages: list[dict[str, Any]]) -> str
```

Выбирает первое непустое user-сообщение и делает короткий заголовок.

<a id="module-agent-companion-preferences-py"></a>

## `agent/companion_preferences.py`

Независимый сохраняемый профиль Лолы: модель, endpoint, характер, STT и голос; секреты не сохраняются.

### `validate_profile`

[Исходник](../../agent/companion_preferences.py#L18)

```python
def validate_profile(params)
```

Проверяет независимый endpoint/model/tool protocol, характер до 6000 символов, STT URL, голос, темп, громкость и флаги.

### `load_profile`

[Исходник](../../agent/companion_preferences.py#L44)

```python
def load_profile()
```

Загружает companion.json, при отсутствии или повреждении использует независимые defaults с пустым ID модели.

### `save_profile`

[Исходник](../../agent/companion_preferences.py#L52)

```python
def save_profile(params)
```

Атомарно сохраняет только разрешённые публичные поля, исключая model/STT API keys.

<a id="module-agent-context-manager-py"></a>

## `agent/context_manager.py`

Сборка временного рабочего контекста с метаданными задачи, умным сжатием и статистикой.

### `ContextManager`

[Исходник](../../agent/context_manager.py#L8)

```python
class ContextManager
```

Единый builder модельного контекста с сохранением обязательных запросов и целых tool-пар.

### `ContextManager.__init__`

[Исходник](../../agent/context_manager.py#L9)

```python
def __init__(self, max_chars=80000, recent_rounds=12)
```

Инициализирует состояние экземпляра ContextManager; параметры показаны в сигнатуре, назначение описано у класса.

### `ContextManager.build`

[Исходник](../../agent/context_manager.py#L14)

```python
def build(self, messages, task=None, skills=None, request_index=None)
```

Добавляет task/skills к копии system prompt и вызывает общий compact_live_messages с жёстким JSON-бюджетом.

<a id="module-agent-conversation-py"></a>

## `agent/conversation.py`

Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп.

### `_message_size`

[Исходник](../../agent/conversation.py#L16)

```python
def _message_size(message)
```

Оценивает размер сериализованного сообщения в символах, не токенах модели.

### `_bounded_turn`

[Исходник](../../agent/conversation.py#L23)

```python
def _bounded_turn(turn)
```

Копирует ход и обрезает объёмные tool outputs, оставляя структуру сообщений.

### `select_recent_history`

[Исходник](../../agent/conversation.py#L39)

```python
def select_recent_history(history, max_chars=MAX_CONTEXT_CHARS, max_turns=MAX_CONTEXT_TURNS)
```

Выбирает недавние целые пользовательские ходы с ограничением объёма и количества.

### `build_messages`

[Исходник](../../agent/conversation.py#L82)

```python
def build_messages(history, prompt)
```

Глубоко копирует полную каноническую историю и добавляет новый запрос; сокращение выполняется только перед HTTP.

### `_complete_units`

[Исходник](../../agent/conversation.py#L89)

```python
def _complete_units(messages)
```

Копирует завершённые tool-пары и обычные сообщения; исключает незавершённые и осиротевшие tool-сообщения из проекции.

### `compact_live_messages`

[Исходник](../../agent/conversation.py#L122)

```python
def compact_live_messages(messages, max_chars=80000, keep_recent_rounds=10, request_index=None)
```

Сокращает текущий модельный контекст, группируя assistant tool calls и их результаты.

### `compact_live_messages.flatten`

[Исходник](../../agent/conversation.py#L144)

```python
def flatten()
```

Собирает system-сообщение и группы сообщений в плоский список.

### `compact_live_messages.size`

[Исходник](../../agent/conversation.py#L147)

```python
def size()
```

Измеряет точную длину сериализованного JSON текущего модельного контекста.

<a id="module-agent-delegation-py"></a>

## `agent/delegation.py`

Единственное определение delegate_task для передачи сложной задачи от Лолы основной модели.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-agent-editor-io-py"></a>

## `agent/editor_io.py`

Самостоятельные sandbox-функции текстового редактора; React preview их не использует для записи.

### `read_project_text`

[Исходник](../../agent/editor_io.py#L8)

```python
def read_project_text(project_root: str | Path, requested: str | Path, *, max_bytes: int=MAX_EDITOR_FILE_BYTES) -> tuple[Path, str]
```

Проверяет путь, существование и размер, затем возвращает Path и UTF-8 текст.

### `save_project_text`

[Исходник](../../agent/editor_io.py#L17)

```python
def save_project_text(project_root: str | Path, requested: str | Path, text: str) -> Path
```

Сохраняет существующий файл после повторной проверки пути; не является engine approval API.

<a id="module-agent-engine-py"></a>

## `agent/engine.py`

Независимый от UI цикл модели, инструментов, подтверждений, памяти и checkpoint.

### `EventHook`

[Исходник](../../agent/engine.py#L37)

```python
class EventHook
```

Синхронный набор callbacks для независимых от GUI событий движка.

### `EventHook.__init__`

[Исходник](../../agent/engine.py#L39)

```python
def __init__(self)
```

Инициализирует состояние экземпляра EventHook; параметры показаны в сигнатуре, назначение описано у класса.

### `EventHook.connect`

[Исходник](../../agent/engine.py#L42)

```python
def connect(self, callback)
```

Добавляет обработчик события.

### `EventHook.emit`

[Исходник](../../agent/engine.py#L45)

```python
def emit(self, *args)
```

Вызывает копию списка обработчиков с переданными аргументами в текущем потоке.

### `AgentEngine`

[Исходник](../../agent/engine.py#L50)

```python
class AgentEngine
```

Состояние и исполнение одного запуска модели с tools, approval, лимитами, памятью и checkpoint.

### `AgentEngine.requestInterruption`

[Исходник](../../agent/engine.py#L55)

```python
def requestInterruption(self)
```

Выставляет Event остановки и отменяет активные сетевые future клиента.

### `AgentEngine.isInterruptionRequested`

[Исходник](../../agent/engine.py#L60)

```python
def isInterruptionRequested(self)
```

Возвращает текущее состояние флага остановки.

### `AgentEngine.__init__`

[Исходник](../../agent/engine.py#L63)

```python
def __init__(self, base_url, api_key, model, project_root, prompt, force_tool=None, settings=None, history=None, memory=None, auto_memory=True, task_id=None, allow_tools=True, companion=False, tool_protocol='native', persona='', tool_definitions=None, tool_handler=None, role_instruction='', stage_only=False)
```

Инициализирует состояние экземпляра AgentEngine; параметры показаны в сигнатуре, назначение описано у класса.

### `AgentEngine._checkpoint`

[Исходник](../../agent/engine.py#L101)

```python
def _checkpoint(self, stage=None, event='')
```

Обновляет этап/последнее событие, сохраняет checkpoint и публикует снимок.

### `AgentEngine.task_snapshot`

[Исходник](../../agent/engine.py#L111)

```python
def task_snapshot(self)
```

Возвращает независимую копию checkpoint для атомарного сохранения в записи чата.

### `AgentEngine.resolve_write_approval`

[Исходник](../../agent/engine.py#L114)

```python
def resolve_write_approval(self, decision)
```

Принимает решение и освобождает ожидание записи; неизвестное решение превращает в reject.

### `AgentEngine._ask_write_approval`

[Исходник](../../agent/engine.py#L125)

```python
def _ask_write_approval(self, path, diff, exists)
```

Запрашивает согласие через событие и ждёт apply/reject/cancel с проверкой остановки.

### `AgentEngine._emit_change`

[Исходник](../../agent/engine.py#L147)

```python
def _emit_change(self, path, diff, exists, status, error='')
```

Публикует path/diff/status одного предложения изменения.

### `AgentEngine._looks_like_action_request`

[Исходник](../../agent/engine.py#L157)

```python
@staticmethod
def _looks_like_action_request(prompt)
```

Эвристически распознаёт просьбу действия по русским/английским словам.

### `AgentEngine._verify_task_completion`

[Исходник](../../agent/engine.py#L167)

```python
def _verify_task_completion(self, client, messages, max_tokens)
```

Дополнительным модельным запросом проверяет, не является ли финал только планом; при ошибке проверки разрешает завершение.

### `AgentEngine.run`

[Исходник](../../agent/engine.py#L203)

```python
def run(self)
```

Строит контекст, выполняет потоковые ходы и tools, обрабатывает остановку, сохраняет состояние и закрывает клиент.

<a id="module-agent-ide-coordinator-py"></a>

## `agent/ide_coordinator.py`

Четыре роли IDE, локальные передачи кода, ограниченное исправление, существующие diff approvals и подтверждённая проверка файлов.

### `RoleOutputError`

[Исходник](../../agent/ide_coordinator.py#L28)

```python
class RoleOutputError(ValueError)
```

Выделяет ошибки формата, для которых разрешён один повтор без записи неверного результата.

### `IDECoordinator`

[Исходник](../../agent/ide_coordinator.py#L32)

```python
class IDECoordinator(AgentEngine)
```

Последовательно координирует четыре AgentEngine с изоляцией прав, локальными артефактами и проверкой результата.

### `IDECoordinator.__init__`

[Исходник](../../agent/ide_coordinator.py#L33)

```python
def __init__(self, *, workflow_options, role_configs, resume=False, stage_factory=AgentEngine, lifecycle_factory=ModelLifecycle, **kwargs)
```

Инициализирует состояние экземпляра IDECoordinator; параметры показаны в сигнатуре, назначение описано у класса.

### `IDECoordinator._flow_snapshot`

[Исходник](../../agent/ide_coordinator.py#L55)

```python
def _flow_snapshot(self)
```

Добавляет безопасные названия/ID/статусы ролей и номер исправления к существующей задаче.

### `IDECoordinator._persist`

[Исходник](../../agent/ide_coordinator.py#L60)

```python
def _persist(self)
```

Атомарно сохраняет передачи ролей вне проекта и уведомляет UI о checkpoint.

### `IDECoordinator._lifecycle_event`

[Исходник](../../agent/ide_coordinator.py#L64)

```python
def _lifecycle_event(self, text)
```

Сохраняет точную активную модель для последующей очистки, передаёт состояние загрузки в журнал/план.

### `IDECoordinator.requestInterruption`

[Исходник](../../agent/ide_coordinator.py#L71)

```python
def requestInterruption(self)
```

Останавливает общий цикл и текущий дочерний HTTP/approval цикл.

### `IDECoordinator.resolve_write_approval`

[Исходник](../../agent/ide_coordinator.py#L75)

```python
def resolve_write_approval(self, decision)
```

Пересылает решение только текущему AgentEngine, сохраняющему проверку diff и revision.

### `IDECoordinator._child_task`

[Исходник](../../agent/ide_coordinator.py#L78)

```python
def _child_task(self, snapshot)
```

Объединяет counters, доказательства чтения и состояние дочерней роли; completed этапа не завершает весь цикл.

### `IDECoordinator._chat`

[Исходник](../../agent/ide_coordinator.py#L92)

```python
def _chat(self, role, text)
```

Помечает ответ ролью и сохраняет общую историю без подмены исходного запроса служебными prompt.

### `IDECoordinator._handoff`

[Исходник](../../agent/ide_coordinator.py#L97)

```python
def _handoff(self, role, checks)
```

Передаёт полные релевантные материалы/прочитанные файлы; при превышении бюджета останавливается без обрезки кода.

### `IDECoordinator._capture_context`

[Исходник](../../agent/ide_coordinator.py#L108)

```python
def _capture_context(self, messages)
```

Из успешных read_file tool results собирает контекст файлов для автора кода без собственных файловых инструментов.

### `IDECoordinator._structured_output`

[Исходник](../../agent/ide_coordinator.py#L116)

```python
def _structured_output(self, text, role)
```

Валидирует JSON автора/проверяющего, полные path/content и границы проекта до использования артефакта.

### `IDECoordinator._syntax_checks`

[Исходник](../../agent/ide_coordinator.py#L132)

```python
def _syntax_checks(self)
```

Читает только modified_files через sandbox и безопасно проверяет Python AST/JSON без запуска кода.

### `IDECoordinator._stage`

[Исходник](../../agent/ide_coordinator.py#L146)

```python
def _stage(self, role, checks)
```

Выбирает модель и права роли, связывает события/approvals, учитывает общий бюджет, проверяет ответ до передачи дальше.

### `IDECoordinator._stage.delta`

[Исходник](../../agent/ide_coordinator.py#L168)

```python
def delta(turn, text)
```

Даёт потокам уникальные role/cycle/turn ID и обозначает роль в первом фрагменте.

### `IDECoordinator._verdict`

[Исходник](../../agent/ide_coordinator.py#L190)

```python
def _verdict(self, text, checks)
```

Требует pass без issues, успешных статических проверок и чтения каждого изменённого файла текущим проверяющим.

### `IDECoordinator.run`

[Исходник](../../agent/ide_coordinator.py#L199)

```python
def run(self)
```

Выполняет полный/одиночный этап, один повтор формата, до двух циклов исправлений, pause/resume и обязательную выгрузку.

<a id="module-agent-ide-workflow-py"></a>

## `agent/ide_workflow.py`

Whitelist ролей IDE, отдельное сохранение без ключей и разрешение наследуемых моделей/endpoint без утечки основного токена.

### `validate_workflow`

[Исходник](../../agent/ide_workflow.py#L14)

```python
def validate_workflow(params)
```

Проверяет четыре роли, режим, провайдер, относительные настройки URL/ID, контекст и число исправлений; отбрасывает секреты.

### `load_workflow`

[Исходник](../../agent/ide_workflow.py#L40)

```python
def load_workflow()
```

Загружает отдельный JSON либо возвращает выключенный совместимый профиль по умолчанию.

### `save_workflow`

[Исходник](../../agent/ide_workflow.py#L45)

```python
def save_workflow(params)
```

Атомарно сохраняет только прошедшие whitelist настройки без API-ключей.

### `resolve_roles`

[Исходник](../../agent/ide_workflow.py#L49)

```python
def resolve_roles(workflow, primary, secrets=None)
```

Подставляет основные URL/ID и только для того же URL наследует основной ключ; проверяет назначение используемых ролей.

<a id="module-agent-json-tools-py"></a>

## `agent/json_tools.py`

Текстовый JSON tool protocol: преобразование истории, строгий parser envelope и адаптация stream к обычному executor.

### `prepare_json_request`

[Исходник](../../agent/json_tools.py#L8)

```python
def prepare_json_request(params)
```

Убирает native tools/tool_choice, добавляет JSON-схемы в system prompt и переводит tool history в обычные сообщения.

### `parse_tool_json`

[Исходник](../../agent/json_tools.py#L49)

```python
def parse_tool_json(content, allowed)
```

Принимает JSON только в начале ответа, целый fenced JSON или Qwen tool_call wrapper; хвост комментария игнорируется, поиск команд внутри произвольного текста запрещён; имена и arguments строго проверяются.

### `JsonToolStream`

[Исходник](../../agent/json_tools.py#L81)

```python
class JsonToolStream
```

Ограниченный буфер JSON-ответа поверх отменяемого native stream; возвращает существующему движку знакомую форму delta.tool_calls.

### `JsonToolStream.__init__`

[Исходник](../../agent/json_tools.py#L83)

```python
def __init__(self, source, allowed, choice)
```

Инициализирует состояние экземпляра JsonToolStream; параметры показаны в сигнатуре, назначение описано у класса.

### `JsonToolStream.__iter__`

[Исходник](../../agent/json_tools.py#L86)

```python
def __iter__(self)
```

Собирает до 1 МБ текста, проверяет обязательность/запрет вызова и создаёт native-shaped delta с UUID каждого вызова.

### `JsonToolStream.close`

[Исходник](../../agent/json_tools.py#L106)

```python
def close(self)
```

Закрывает исходный HTTP stream и освобождает отменяемый запрос.

<a id="module-agent-mcp-py"></a>

## `agent/mcp.py`

Реестр MCP-конфигураций без транспорта и исполнения внешних tools.

### `MCPServer`

[Исходник](../../agent/mcp.py#L6)

```python
@dataclass
class MCPServer
```

Dataclass конфигурации MCP-сервера; command/args/enabled/trusted остаются данными.

Поля, объявленные в классе:

```python
name: str
command: str = ''
args: list[str] | None = None
enabled: bool = True
trusted: bool = False
```

### `MCPRegistry`

[Исходник](../../agent/mcp.py#L13)

```python
class MCPRegistry
```

Реестр конфигураций; подключения и MCP transport здесь нет.

### `MCPRegistry.__init__`

[Исходник](../../agent/mcp.py#L14)

```python
def __init__(self, servers=None)
```

Инициализирует состояние экземпляра MCPRegistry; параметры показаны в сигнатуре, назначение описано у класса.

### `MCPRegistry.register`

[Исходник](../../agent/mcp.py#L16)

```python
def register(self, server)
```

Добавляет или заменяет сервер по имени.

### `MCPRegistry.remove`

[Исходник](../../agent/mcp.py#L17)

```python
def remove(self, name)
```

Удаляет запись по имени, если она есть.

### `MCPRegistry.enable`

[Исходник](../../agent/mcp.py#L18)

```python
def enable(self, name, enabled=True)
```

Изменяет enabled существующей записи.

### `MCPRegistry.list_servers`

[Исходник](../../agent/mcp.py#L20)

```python
def list_servers(self)
```

Возвращает все конфигурации как словари.

### `MCPRegistry.available`

[Исходник](../../agent/mcp.py#L21)

```python
def available(self)
```

Выбирает записи с enabled=True, не проверяя живое соединение.

### `MCPRegistry.manifest`

[Исходник](../../agent/mcp.py#L22)

```python
def manifest(self)
```

Формирует список включённых конфигураций для дальнейшей интеграции.

<a id="module-agent-model-client-py"></a>

## `agent/model_client.py`

Отменяемый async HTTP-клиент с синхронной поверхностью для движка.

### `ModelCancelled`

[Исходник](../../agent/model_client.py#L9)

```python
class ModelCancelled(Exception)
```

Внутреннее исключение отмены модельного запроса, обрабатываемое движком.

### `ModelStream`

[Исходник](../../agent/model_client.py#L13)

```python
class ModelStream
```

Синхронный итератор над async SSE-producer с ограниченной очередью.

### `ModelStream.__init__`

[Исходник](../../agent/model_client.py#L14)

```python
def __init__(self, owner, params)
```

Инициализирует состояние экземпляра ModelStream; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelStream._produce`

[Исходник](../../agent/model_client.py#L19)

```python
async def _produce(self, params)
```

Получает async stream, кладёт чанки в очередь и закрывает HTTP-контекст при выходе/отмене.

### `ModelStream.__iter__`

[Исходник](../../agent/model_client.py#L27)

```python
def __iter__(self)
```

Возвращает сам поток как Python-итератор.

### `ModelStream.__next__`

[Исходник](../../agent/model_client.py#L30)

```python
def __next__(self)
```

Ожидает очередной чанк короткими интервалами, проверяет отмену и завершение future.

### `ModelStream.close`

[Исходник](../../agent/model_client.py#L40)

```python
def close(self)
```

Отменяет future producer, закрывая незавершённый поток.

### `ModelClient`

[Исходник](../../agent/model_client.py#L44)

```python
class ModelClient
```

Async SDK в отдельном loop-потоке с синхронными create/result и отменой.

### `ModelClient.__init__`

[Исходник](../../agent/model_client.py#L45)

```python
def __init__(self, base_url, api_key, interrupted, timeout=180, tool_protocol='native')
```

Инициализирует состояние экземпляра ModelClient; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelClient.check_cancelled`

[Исходник](../../agent/model_client.py#L56)

```python
def check_cancelled(self)
```

Выбрасывает ModelCancelled, если общий Event установлен.

### `ModelClient.submit`

[Исходник](../../agent/model_client.py#L60)

```python
def submit(self, coroutine)
```

Планирует корутину в сетевом loop и учитывает её future в pending.

### `ModelClient._forget`

[Исходник](../../agent/model_client.py#L69)

```python
def _forget(self, future)
```

Убирает завершённую future из защищённого множества.

### `ModelClient.result`

[Исходник](../../agent/model_client.py#L73)

```python
def result(self, future)
```

Ждёт результат короткими интервалами и переводит cancellation в исключение движка.

### `ModelClient.create`

[Исходник](../../agent/model_client.py#L83)

```python
def create(self, **params)
```

Возвращает ModelStream для stream=True или готовый async-ответ для stream=False.

### `ModelClient.cancel`

[Исходник](../../agent/model_client.py#L93)

```python
def cancel(self)
```

Отменяет снимок всех активных future.

### `ModelClient.close`

[Исходник](../../agent/model_client.py#L99)

```python
def close(self)
```

Отменяет async-задачи, закрывает SDK и останавливает сетевой поток/loop.

### `ModelClient.close.shutdown`

[Исходник](../../agent/model_client.py#L100)

```python
async def shutdown()
```

Async-фаза закрытия: cancel/gather задач и client.close внутри принадлежащего loop.

<a id="module-agent-model-discovery-py"></a>

## `agent/model_discovery.py`

HTTPX-получение списка моделей с общим deadline, ограничением ответа и отменой сокета.

### `_request_models`

[Исходник](../../agent/model_discovery.py#L10)

```python
async def _request_models(config, max_bytes)
```

Читает HTTPX stream с ограничением размера и проверяет JSON data/models ID.

### `_wait_cancelled`

[Исходник](../../agent/model_discovery.py#L31)

```python
async def _wait_cancelled(cancelled)
```

Наблюдает threading.Event через короткие asyncio sleep без блокировки event loop.

### `_discover`

[Исходник](../../agent/model_discovery.py#L37)

```python
async def _discover(config, timeout, max_bytes, cancelled)
```

Соревнуется запросом, отменой и общим timeout; всегда отменяет и закрывает незавершённые задачи.

### `discover_models`

[Исходник](../../agent/model_discovery.py#L55)

```python
def discover_models(config, *, timeout=5.0, max_bytes=1000000, cancelled=None)
```

Синхронная точка входа фонового worker, запускающая отдельный asyncio loop.

<a id="module-agent-model-gateway-py"></a>

## `agent/model_gateway.py`

Отдельное представление endpoint провайдера/локального runtime; не включено в TaskService.

### `ModelEndpoint`

[Исходник](../../agent/model_gateway.py#L9)

```python
@dataclass
class ModelEndpoint
```

Dataclass параметров провайдера: URL, модель, ключ и local-флаг.

Поля, объявленные в классе:

```python
provider: str
base_url: str
model: str
api_key: str = 'no-key'
local: bool = False
```

### `ModelGateway`

[Исходник](../../agent/model_gateway.py#L17)

```python
class ModelGateway
```

Отдельная абстракция выбора provider/local endpoint; не используется TaskService.

### `ModelGateway.__init__`

[Исходник](../../agent/model_gateway.py#L18)

```python
def __init__(self, local_runtime: LocalRuntime | None=None)
```

Инициализирует состояние экземпляра ModelGateway; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelGateway.use_provider`

[Исходник](../../agent/model_gateway.py#L22)

```python
def use_provider(self, base_url: str, model: str, api_key: str='no-key', provider='OpenAI-compatible')
```

Создаёт endpoint по введённому URL, модели и ключу.

### `ModelGateway.use_local`

[Исходник](../../agent/model_gateway.py#L26)

```python
def use_local(self, model: str | None=None)
```

Создаёт endpoint уже запущенного LocalRuntime; иначе выбрасывает ошибку.

### `ModelGateway.status`

[Исходник](../../agent/model_gateway.py#L32)

```python
def status(self)
```

Возвращает endpoint и состояние локального runtime; endpoint может содержать ключ, не публикуйте его как безопасные preferences.

<a id="module-agent-model-lifecycle-py"></a>

## `agent/model_lifecycle.py`

Последовательная отменяемая загрузка/выгрузка назначенных моделей LM Studio 0.4+/Ollama и read-only каталог.

### `ModelLifecycle`

[Исходник](../../agent/model_lifecycle.py#L8)

```python
class ModelLifecycle
```

Управляет одной активной моделью роли, не запускает shell и не завершает чужие процессы.

### `ModelLifecycle.__init__`

[Исходник](../../agent/model_lifecycle.py#L9)

```python
def __init__(self, roles, interrupted, context_length=4096, notify=None)
```

Инициализирует состояние экземпляра ModelLifecycle; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelLifecycle.origin`

[Исходник](../../agent/model_lifecycle.py#L14)

```python
@staticmethod
def origin(config)
```

Разрешает нативное управление только на корне проверенного сервера без произвольных префиксов маршрута.

### `ModelLifecycle.request`

[Исходник](../../agent/model_lifecycle.py#L19)

```python
def request(self, config, method, route, payload=None, cleanup=False)
```

Выполняет ограниченный запрос с коротким наблюдением Event отмены и отдельным deadline очистки.

### `ModelLifecycle.request.run`

[Исходник](../../agent/model_lifecycle.py#L20)

```python
async def run()
```

Владеет asyncio request и гарантирует его отмену/закрытие при выходе.

### `ModelLifecycle.request.run.fetch`

[Исходник](../../agent/model_lifecycle.py#L21)

```python
async def fetch()
```

Передаёт токен только выбранному endpoint без redirects/proxy env; ограничивает JSON ответ двумя МБ.

### `ModelLifecycle.catalog`

[Исходник](../../agent/model_lifecycle.py#L44)

```python
def catalog(self, config)
```

Читает LM Studio model keys/instances, Ollama tags/ps или OpenAI model IDs без загрузки весов.

### `ModelLifecycle.unload`

[Исходник](../../agent/model_lifecycle.py#L56)

```python
def unload(self, config, instance, cleanup=False)
```

Выгружает точный instance_id LM Studio либо exact Ollama model через keep_alive=0.

### `ModelLifecycle.release`

[Исходник](../../agent/model_lifecycle.py#L65)

```python
def release(self)
```

Выгружает известную активную модель; при ошибке сохраняет владение и запрещает последующую загрузку.

### `ModelLifecycle.acquire`

[Исходник](../../agent/model_lifecycle.py#L72)

```python
def acquire(self, config)
```

Повторно использует ту же модель либо выгружает прежнюю, проверяет каталог/чужую память, затем загружает только назначенную.

<a id="module-agent-model-manager-py"></a>

## `agent/model_manager.py`

Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции.

### `LocalModel`

[Исходник](../../agent/model_manager.py#L31)

```python
@dataclass
class LocalModel
```

Dataclass GGUF-файла с путём, именем, размером и метаданными quantization/architecture.

Поля, объявленные в классе:

```python
path: str
name: str
size_bytes: int
quantization: str = 'unknown'
architecture: str = 'unknown'
```

### `LocalModel.size_gb`

[Исходник](../../agent/model_manager.py#L39)

```python
@property
def size_gb(self) -> float
```

Property размера файла в GiB-подобном делении на 1024^3.

### `LocalModel.to_dict`

[Исходник](../../agent/model_manager.py#L42)

```python
def to_dict(self)
```

Преобразует запись модели в словарь с округлённым size_gb.

### `ModelManager`

[Исходник](../../agent/model_manager.py#L48)

```python
class ModelManager
```

Сканирование и импорт GGUF в отдельный каталог моделей.

### `ModelManager.__init__`

[Исходник](../../agent/model_manager.py#L49)

```python
def __init__(self, models_dir: str | Path | None=None)
```

Инициализирует состояние экземпляра ModelManager; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelManager._quantization`

[Исходник](../../agent/model_manager.py#L54)

```python
@staticmethod
def _quantization(name: str) -> str
```

Определяет quantization по имени файла регулярным выражением; не анализирует бинарное содержимое.

### `ModelManager.scan`

[Исходник](../../agent/model_manager.py#L58)

```python
def scan(self) -> list[LocalModel]
```

Рекурсивно находит .gguf и возвращает доступные записи.

### `ModelManager.import_model`

[Исходник](../../agent/model_manager.py#L67)

```python
def import_model(self, source: str | Path, *, copy=True) -> LocalModel
```

Проверяет расширение/файл и при copy=True копирует в models_dir.

### `LocalRuntime`

[Исходник](../../agent/model_manager.py#L80)

```python
class LocalRuntime
```

Управляет отдельным процессом llama-server и его HTTP endpoint.

### `LocalRuntime.__init__`

[Исходник](../../agent/model_manager.py#L82)

```python
def __init__(self, *, runtime_path: str | Path | None=None)
```

Инициализирует состояние экземпляра LocalRuntime; параметры показаны в сигнатуре, назначение описано у класса.

### `LocalRuntime.find_executable`

[Исходник](../../agent/model_manager.py#L93)

```python
@staticmethod
def find_executable(explicit: str='') -> str | None
```

Ищет явно заданный путь, служебный runtime, текущий каталог и PATH.

### `LocalRuntime.free_port`

[Исходник](../../agent/model_manager.py#L109)

```python
@staticmethod
def free_port(host='127.0.0.1') -> int
```

Получает свободный локальный TCP-порт через временный bind.

### `LocalRuntime.running`

[Исходник](../../agent/model_manager.py#L115)

```python
@property
def running(self) -> bool
```

Property: процесс существует и ещё не завершился.

### `LocalRuntime.base_url`

[Исходник](../../agent/model_manager.py#L119)

```python
@property
def base_url(self) -> str
```

Property URL /v1 для назначенного порта.

### `LocalRuntime.start`

[Исходник](../../agent/model_manager.py#L122)

```python
def start(self, model: LocalModel, *, ctx_size=32768, gpu_layers=-1, port=None, extra_args=None, cancelled=None, timeout=120)
```

Запускает собственный llama-server с model/context/GPU flags, job и output drain; readiness до 120 секунд, отмена очищает процесс.

### `LocalRuntime._drain_output`

[Исходник](../../agent/model_manager.py#L172)

```python
def _drain_output(self, process)
```

Читает бинарный PIPE порциями 1024 байта без ожидания newline; хранит последние 100 порций.

### `LocalRuntime._healthy`

[Исходник](../../agent/model_manager.py#L184)

```python
def _healthy(self) -> bool
```

Проверяет HTTP /models с коротким timeout.

### `LocalRuntime.stop`

[Исходник](../../agent/model_manager.py#L193)

```python
def stop(self)
```

Завершает процесс, при необходимости убивает и очищает runtime-состояние.

### `LocalRuntime.status`

[Исходник](../../agent/model_manager.py#L216)

```python
def status(self) -> dict
```

Возвращает состояние процесса, порт, URL и метаданные модели.

### `LocalRuntime.__del__`

[Исходник](../../agent/model_manager.py#L226)

```python
def __del__(self)
```

Пытается закрыть процесс при удалении экземпляра; не заменяет явное управление жизненным циклом.

<a id="module-agent-model-preferences-py"></a>

## `agent/model_preferences.py`

Валидация endpoint и whitelist числовых настроек, миграция старого JSON и атомарное сохранение без API-ключа.

### `validate_settings`

[Исходник](../../agent/model_preferences.py#L24)

```python
def validate_settings(settings)
```

Проверяет конечность, тип, целочисленность и диапазон каждого разрешённого параметра; неизвестные поля не сохраняет.

### `validate_preferences`

[Исходник](../../agent/model_preferences.py#L38)

```python
def validate_preferences(params)
```

Разрешает HTTP(S) endpoint без credentials/query/fragment, проверяет порт и возвращает URL/ID и whitelist settings без ключа.

### `load_preferences`

[Исходник](../../agent/model_preferences.py#L53)

```python
def load_preferences()
```

Читает и проверяет JSON; при ошибке возвращает копию defaults, никогда не восстанавливает ключ.

### `save_preferences`

[Исходник](../../agent/model_preferences.py#L61)

```python
def save_preferences(params)
```

Атомарно сохраняет whitelist полей во внешний служебный JSON.

<a id="module-agent-model-probe-py"></a>

## `agent/model_probe.py`

Ограниченная отменяемая проверка draft-модели через Chat Completions без файлов, истории и сохранения настроек.

### `_request_probe`

[Исходник](../../agent/model_probe.py#L12)

```python
async def _request_probe(config, max_bytes)
```

Выполняет bounded HTTP POST с коротким prompt, параметрами черновика, заданным бюджетом токенов и проверкой текстового ответа.

### `_probe`

[Исходник](../../agent/model_probe.py#L38)

```python
async def _probe(config, cancelled, timeout, max_bytes)
```

Ограничивает полное время запроса и следит за Event отмены, закрывая обе asyncio-задачи в finally.

### `probe_model`

[Исходник](../../agent/model_probe.py#L54)

```python
def probe_model(config, *, cancelled=None, timeout=30, max_bytes=100000)
```

Проверяет ID, запускает отдельный asyncio loop и возвращает ответ/время без изменения истории или preferences.

<a id="module-agent-planner-py"></a>

## `agent/planner.py`

Структура этапа и детерминированный план по словам запроса.

### `PlanStage`

[Исходник](../../agent/planner.py#L7)

```python
@dataclass
class PlanStage
```

Dataclass этапа: ID, заголовок, цель, статус и декларативный max_turns.

Поля, объявленные в классе:

```python
id: str
title: str
objective: str = ''
status: str = 'pending'
max_turns: int = 50
```

### `PlanStage.to_dict`

[Исходник](../../agent/planner.py#L14)

```python
def to_dict(self)
```

Преобразует dataclass этапа в JSON-совместимый словарь.

### `build_plan`

[Исходник](../../agent/planner.py#L18)

```python
def build_plan(prompt: str) -> list[dict]
```

Строит этапы по эвристике слов действия, добавляя реализацию только подходящим запросам.

### `TaskPlanner`

[Исходник](../../agent/planner.py#L32)

```python
class TaskPlanner
```

Операции текущего этапа над переданным словарём задачи.

### `TaskPlanner.__init__`

[Исходник](../../agent/planner.py#L33)

```python
def __init__(self, task: dict)
```

Инициализирует состояние экземпляра TaskPlanner; параметры показаны в сигнатуре, назначение описано у класса.

### `TaskPlanner.current`

[Исходник](../../agent/planner.py#L35)

```python
@property
def current(self)
```

Property поиска записи текущего stage.

### `TaskPlanner.advance`

[Исходник](../../agent/planner.py#L38)

```python
def advance(self, reason='')
```

Помечает этап done, активирует следующий и записывает пояснение.

<a id="module-agent-process-job-py"></a>

## `agent/process_job.py`

Windows Job Object: kill-on-close только для собственного Popen и его потомков.

### `ProcessJob`

[Исходник](../../agent/process_job.py#L7)

```python
class ProcessJob
```

Владеет ненаследуемым Windows Job handle; закрытие завершает только присоединённое дерево.

### `ProcessJob.__init__`

[Исходник](../../agent/process_job.py#L8)

```python
def __init__(self, process)
```

Инициализирует состояние экземпляра ProcessJob; параметры показаны в сигнатуре, назначение описано у класса.

### `ProcessJob.__init__.BasicLimits`

[Исходник](../../agent/process_job.py#L14)

```python
class BasicLimits(ctypes.Structure)
```

ctypes структура JOBOBJECT_BASIC_LIMIT_INFORMATION с корректным pointer-size alignment.

### `ProcessJob.__init__.IoCounters`

[Исходник](../../agent/process_job.py#L19)

```python
class IoCounters(ctypes.Structure)
```

Шесть 64-битных IO_COUNTERS полей Windows API.

### `ProcessJob.__init__.ExtendedLimits`

[Исходник](../../agent/process_job.py#L22)

```python
class ExtendedLimits(ctypes.Structure)
```

ctypes JOBOBJECT_EXTENDED_LIMIT_INFORMATION для JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE.

### `ProcessJob.close`

[Исходник](../../agent/process_job.py#L46)

```python
def close(self)
```

Идемпотентно закрывает последний job handle, завершая присоединённые процессы.

<a id="module-agent-project-memory-py"></a>

## `agent/project_memory.py`

Компактная структурированная память проекта, очистка и форматирование для модели.

### `_now`

[Исходник](../../agent/project_memory.py#L30)

```python
def _now() -> str
```

Возвращает UTC ISO-время записи памяти.

### `_key`

[Исходник](../../agent/project_memory.py#L34)

```python
def _key(project_root: str) -> str
```

Хеширует нормализованный project_root для имени каталога памяти.

### `memory_path`

[Исходник](../../agent/project_memory.py#L39)

```python
def memory_path(project_root: str) -> Path
```

Формирует путь project_memory/<hash>/memory.json.

### `empty_memory`

[Исходник](../../agent/project_memory.py#L43)

```python
def empty_memory(project_root: str='') -> dict[str, Any]
```

Создаёт пустую структурированную память с корнем и полями версии.

### `_clean_text`

[Исходник](../../agent/project_memory.py#L58)

```python
def _clean_text(value: Any, limit: int) -> str
```

Удаляет NUL, нормализует пробелы и ограничивает строку.

### `validate_memory`

[Исходник](../../agent/project_memory.py#L65)

```python
def validate_memory(data: Any, project_root: str='') -> dict[str, Any]
```

Проверяет структуру, поля, длины и дубликаты памяти.

### `load_project_memory`

[Исходник](../../agent/project_memory.py#L89)

```python
def load_project_memory(project_root: str) -> dict[str, Any]
```

Загружает и валидирует запись; при ошибке создаёт пустую память.

### `save_project_memory`

[Исходник](../../agent/project_memory.py#L100)

```python
def save_project_memory(project_root: str, data: dict[str, Any]) -> dict[str, Any]
```

Валидирует и атомарно сохраняет JSON памяти выбранного проекта.

### `clear_project_memory`

[Исходник](../../agent/project_memory.py#L118)

```python
def clear_project_memory(project_root: str) -> None
```

Удаляет только память указанного проекта.

### `format_memory_context`

[Исходник](../../agent/project_memory.py#L128)

```python
def format_memory_context(memory: dict[str, Any], max_chars: int=3600) -> str
```

Формирует ограниченный справочный блок для system prompt.

### `merge_memory_update`

[Исходник](../../agent/project_memory.py#L154)

```python
def merge_memory_update(existing: dict[str, Any], update: Any, project_root: str) -> dict[str, Any]
```

Объединяет только разрешённые поля модельного обновления с существующей памятью и валидирует итог.

<a id="module-agent-runtime-py"></a>

## `agent/runtime.py`

Связь контекста, планировщика, навыков, verifier и MCP-реестра; часть границ ещё не подключена.

### `AgentRuntime`

[Исходник](../../agent/runtime.py#L8)

```python
class AgentRuntime
```

Граница оркестрации: планировщик, context builder, skills, verifier и MCP registry.

### `AgentRuntime.__init__`

[Исходник](../../agent/runtime.py#L9)

```python
def __init__(self, task, *, context_chars=80000, skills_root=None)
```

Инициализирует состояние экземпляра AgentRuntime; параметры показаны в сигнатуре, назначение описано у класса.

### `AgentRuntime.prepare`

[Исходник](../../agent/runtime.py#L21)

```python
def prepare(self)
```

Выбирает навыки по prompt и записывает их ID в task.

### `AgentRuntime.working_context`

[Исходник](../../agent/runtime.py#L26)

```python
def working_context(self, messages, request_index=None)
```

Передаёт сообщения, task и выбранные skills в ContextManager.

### `AgentRuntime.checkpoint`

[Исходник](../../agent/runtime.py#L29)

```python
def checkpoint(self, event)
```

Обновляет last_event в памяти; сам по себе не пишет JSON на диск.

### `AgentRuntime.complete_stage`

[Исходник](../../agent/runtime.py#L32)

```python
def complete_stage(self, reason='')
```

Делегирует переход этапа TaskPlanner.advance.

<a id="module-agent-security-py"></a>

## `agent/security.py`

Канонический корень и разрешение путей только внутри выбранного проекта.

### `AccessDenied`

[Исходник](../../agent/security.py#L9)

```python
class AccessDenied(PermissionError)
```

Ошибка выхода за разрешённый корень или невозможности безопасно разрешить путь.

### `canonical_root`

[Исходник](../../agent/security.py#L13)

```python
def canonical_root(root: str | Path) -> Path
```

Раскрывает и разрешает существующий корень; требует каталог.

### `resolve_allowed_path`

[Исходник](../../agent/security.py#L20)

```python
def resolve_allowed_path(root: str | Path, requested: str | Path='.', *, must_exist: bool=False) -> Path
```

Разрешает относительный/абсолютный путь и ссылки, затем проверяет принадлежность каноническому корню.

<a id="module-agent-skills-py"></a>

## `agent/skills.py`

Обнаружение, краткие метаданные, чтение и выбор SKILL.md по словам.

### `SkillManager`

[Исходник](../../agent/skills.py#L6)

```python
class SkillManager
```

Локальный реестр Markdown-навыков и простого лексического выбора.

### `SkillManager.__init__`

[Исходник](../../agent/skills.py#L7)

```python
def __init__(self, root=None)
```

Инициализирует состояние экземпляра SkillManager; параметры показаны в сигнатуре, назначение описано у класса.

### `SkillManager.discover`

[Исходник](../../agent/skills.py#L9)

```python
def discover(self)
```

Находит SKILL.md и возвращает метаданные каждого файла.

### `SkillManager._metadata`

[Исходник](../../agent/skills.py#L15)

```python
def _metadata(self, path)
```

Извлекает ID из каталога, заголовок, путь и краткую сводку.

### `SkillManager._summary`

[Исходник](../../agent/skills.py#L22)

```python
@staticmethod
def _summary(text)
```

Выбирает первую подходящую строку текста как summary до 300 символов.

### `SkillManager.load`

[Исходник](../../agent/skills.py#L28)

```python
def load(self, skill_id)
```

Читает полный текст навыка по ID; автоматически не исполняет его.

### `SkillManager.select`

[Исходник](../../agent/skills.py#L33)

```python
def select(self, prompt, limit=3)
```

Ранжирует метаданные по словам prompt и возвращает не больше limit совпадений.

<a id="module-agent-smart-context-py"></a>

## `agent/smart_context.py`

Детерминированное сжатие временного контекста с архивом ограничений и фактов без LLM-запросов и изменения канонической истории.

### `context_size`

[Исходник](../../agent/smart_context.py#L11)

```python
def context_size(messages)
```

Считает символы сериализованного JSON, а не токены модели.

### `text_digest`

[Исходник](../../agent/smart_context.py#L15)

```python
def text_digest(text)
```

Возвращает первые 16 hex символов SHA-256 для сверки сокращённого источника.

### `salient_text`

[Исходник](../../agent/smart_context.py#L19)

```python
def salient_text(text, query='', limit=1200)
```

Выбирает строки по запросу, ограничениям, началу и концу; маркирует фрагменты и исходный размер.

### `compact_tool_result`

[Исходник](../../agent/smart_context.py#L35)

```python
def compact_tool_result(content, query, limit)
```

Сохраняет валидный JSON с путём, статусом, ошибкой и fingerprint; сокращает крупные чтения и списки.

### `context_archive`

[Исходник](../../agent/smart_context.py#L58)

```python
def context_archive(units, budget)
```

Собирает ограничения исходных пользователей, краткие запросы, решения и последние факты tools; при невозможности сохранить ограничения останавливается.

### `context_archive.render`

[Исходник](../../agent/smart_context.py#L79)

```python
def render()
```

Сериализует архив как данные истории без повышения роли или прав.

### `smart_compact_messages`

[Исходник](../../agent/smart_context.py#L88)

```python
def smart_compact_messages(messages, max_chars=80000, keep_recent_rounds=12, request_index=None)
```

Защищает текущий запрос и код, сохраняет целые пары tools, архивирует старые группы и возвращает метрики без изменения истории.

<a id="module-agent-task-activity-py"></a>

## `agent/task_activity.py`

Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории.

### `begin_tool`

[Исходник](../../agent/task_activity.py#L11)

```python
def begin_tool(task, tool, args, call_id, message_index)
```

Создаёт запись метаданных и активирует research/implementation, добавляя отсутствующий этап записи и ограничивая журнал 100 элементами.

### `update_tool`

[Исходник](../../agent/task_activity.py#L32)

```python
def update_tool(task, activity_id, status, summary)
```

Обновляет статус/краткую сводку по внутреннему ID и время завершения терминального состояния.

### `finish_tool`

[Исходник](../../agent/task_activity.py#L44)

```python
def finish_tool(task, activity_id, tool, result)
```

Преобразует фактический result в безопасную сводку/статус без копирования содержимого файла или результатов поиска.

### `recover_tools`

[Исходник](../../agent/task_activity.py#L63)

```python
def recover_tools(task, messages)
```

Восстанавливает in-flight запись из соответствующего блока tool-call/result; неопределённый Apply отмечает unknown, остальные прерванные — interrupted.

<a id="module-agent-task-store-py"></a>

## `agent/task_store.py`

JSON-контрольные точки задач, этапы, статусы и восстановление.

### `_now`

[Исходник](../../agent/task_store.py#L17)

```python
def _now()
```

UTC ISO-время для checkpoint.

### `_key`

[Исходник](../../agent/task_store.py#L20)

```python
def _key(chat_id: str) -> str
```

SHA-256 от chat_id, сокращённый для имени файла задачи.

### `task_path`

[Исходник](../../agent/task_store.py#L23)

```python
def task_path(chat_id: str) -> Path
```

Возвращает путь tasks/<hash>.json.

### `default_stages`

[Исходник](../../agent/task_store.py#L26)

```python
def default_stages(prompt='')
```

Делегирует построение начального списка этапов build_plan.

### `new_task`

[Исходник](../../agent/task_store.py#L29)

```python
def new_task(chat_id, project_root, prompt)
```

Создаёт словарь running-задачи с планом, счётчиками и resume_state.

### `save_task`

[Исходник](../../agent/task_store.py#L41)

```python
def save_task(task)
```

Обновляет timestamp и записывает checkpoint через temporary+fsync+replace.

### `load_task`

[Исходник](../../agent/task_store.py#L56)

```python
def load_task(chat_id)
```

Читает checkpoint; отсутствие или повреждённый JSON даёт None.

### `clear_task`

[Исходник](../../agent/task_store.py#L63)

```python
def clear_task(chat_id)
```

Удаляет checkpoint, не удаляя историю чата.

### `set_stage`

[Исходник](../../agent/task_store.py#L67)

```python
def set_stage(task, stage_id, status='active', event='')
```

Закрывает посещённый активный этап, помечает непосещённые предыдущие skipped и активирует целевой.

### `finish_task`

[Исходник](../../agent/task_store.py#L79)

```python
def finish_task(task, status='completed', reason='')
```

Завершает посещённые этапы, пропускает pending и сохраняет итоговый статус/причину.

<a id="module-agent-tools-py"></a>

## `agent/tools.py`

Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test.

### `list_files`

[Исходник](../../agent/tools.py#L12)

```python
def list_files(root, path='.', recursive=False, max_entries=200, max_depth=5)
```

Перечисляет разрешённые файлы с фильтрами, ограничением entries и глубины обхода.

### `safe_relative`

[Исходник](../../agent/tools.py#L56)

```python
def safe_relative(target, base)
```

Возвращает относительное POSIX-представление пути для результатов tools.

### `read_file`

[Исходник](../../agent/tools.py#L61)

```python
def read_file(root, path)
```

Читает UTF-8 файл не больше 120000 байт внутри корня.

### `search_text`

[Исходник](../../agent/tools.py#L75)

```python
def search_text(root, query, path='.', case_sensitive=False, max_depth=5)
```

Ищет подстроку в UTF-8 файлах с пределами размера, глубины, числа совпадений и длины строки.

### `preview_file_change`

[Исходник](../../agent/tools.py#L123)

```python
def preview_file_change(root, path, content)
```

Строит unified diff и снимок SHA-256 исходных байтов/предлагаемого текста с нормализованным путём, не записывая файл.

### `write_file`

[Исходник](../../agent/tools.py#L166)

```python
def write_file(root, path, content, overwrite=False, *, approved=False, expected_snapshot=None)
```

Требует approval и совпадающий снимок preview; дважды проверяет состояние, атомарно заменяет существующий файл или создаёт новый без перезаписи.

### `execute_tool`

[Исходник](../../agent/tools.py#L231)

```python
def execute_tool(name, arguments, project_root, settings=None, *, approved=False, expected_snapshot=None)
```

Диспетчер четырёх функций; превращает ожидаемые ошибки в структурированный tool result.

### `run_sandbox_self_test`

[Исходник](../../agent/tools.py#L255)

```python
def run_sandbox_self_test()
```

Выполняет изолированный внутренний unittest-набор проверки файловой границы и возвращает сводку.

### `run_sandbox_self_test.SandboxTests`

[Исходник](../../agent/tools.py#L260)

```python
class SandboxTests(unittest.TestCase)
```

Внутренняя suite временных project/outside каталогов; не пользовательский runtime-класс.

### `run_sandbox_self_test.SandboxTests.setUp`

[Исходник](../../agent/tools.py#L261)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `run_sandbox_self_test.SandboxTests.tearDown`

[Исходник](../../agent/tools.py#L268)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `run_sandbox_self_test.SandboxTests.test_read_inside_allowed`

[Исходник](../../agent/tools.py#L269)

```python
def test_read_inside_allowed(self)
```

Проверка: Внутренний self-test разрешает чтение в корне.

### `run_sandbox_self_test.SandboxTests.test_parent_traversal_denied`

[Исходник](../../agent/tools.py#L270)

```python
def test_parent_traversal_denied(self)
```

Проверка: Внутренний self-test отклоняет выход через родительский каталог.

### `run_sandbox_self_test.SandboxTests.test_absolute_outside_denied`

[Исходник](../../agent/tools.py#L272)

```python
def test_absolute_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний абсолютный путь.

### `run_sandbox_self_test.SandboxTests.test_list_outside_denied`

[Исходник](../../agent/tools.py#L274)

```python
def test_list_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний list_files.

### `run_sandbox_self_test.SandboxTests.test_search_outside_denied`

[Исходник](../../agent/tools.py#L277)

```python
def test_search_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний search_text.

### `run_sandbox_self_test.SandboxTests.test_symlink_escape_denied`

[Исходник](../../agent/tools.py#L280)

```python
def test_symlink_escape_denied(self)
```

Проверка: Проверяет выход через ссылку; может быть skipped при запрете symlink в ОС.

<a id="module-agent-ui-py"></a>

## `agent/ui.py`

Сохранённый Qt GUI: панели, readonly preview, настройки, чат и approval dialog.

### `ApprovalDialog`

[Исходник](../../agent/ui.py#L53)

```python
class ApprovalDialog(QDialog)
```

Qt-диалог readonly diff с Apply/Reject/Cancel.

### `ApprovalDialog.__init__`

[Исходник](../../agent/ui.py#L54)

```python
def __init__(self, path, diff, exists, parent=None)
```

Инициализирует состояние экземпляра ApprovalDialog; параметры показаны в сигнатуре, назначение описано у класса.

### `MainWindow`

[Исходник](../../agent/ui.py#L71)

```python
class MainWindow(QMainWindow)
```

Сохранённый PySide6 GUI со своей QSettings-конфигурацией и AgentWorker.

### `MainWindow.__init__`

[Исходник](../../agent/ui.py#L72)

```python
def __init__(self)
```

Инициализирует состояние экземпляра MainWindow; параметры показаны в сигнатуре, назначение описано у класса.

### `MainWindow._build`

[Исходник](../../agent/ui.py#L93)

```python
def _build(self)
```

Собирает виджеты, панели, readonly preview, чат, кнопки и output.

### `MainWindow._make_simple_page`

[Исходник](../../agent/ui.py#L172)

```python
def _make_simple_page(self, title, message)
```

Создаёт простую Qt-страницу с заголовком и пояснением.

### `MainWindow._load_connection`

[Исходник](../../agent/ui.py#L177)

```python
def _load_connection(self)
```

Читает URL/ключ/модель из QSettings, в отличие от новых JSON preferences.

### `MainWindow._connection_dialog`

[Исходник](../../agent/ui.py#L181)

```python
def _connection_dialog(self)
```

Показывает поля подключения и сохраняет значения, включая ключ, в QSettings.

### `MainWindow._refresh_models`

[Исходник](../../agent/ui.py#L192)

```python
def _refresh_models(self)
```

Синхронно запрашивает список моделей и обновляет QComboBox.

### `MainWindow._choose_project`

[Исходник](../../agent/ui.py#L207)

```python
def _choose_project(self)
```

Выбирает каталог Qt-диалогом, сохраняет путь и обновляет дерево/чаты.

### `MainWindow._refresh_tree`

[Исходник](../../agent/ui.py#L212)

```python
def _refresh_tree(self)
```

Строит ограниченный предпросмотр дерева файлов с фильтрами.

### `MainWindow._filter_tree`

[Исходник](../../agent/ui.py#L227)

```python
def _filter_tree(self, text)
```

Ищет имена файлов по подстроке и ограничивает количество результатов.

### `MainWindow._open_tree_item`

[Исходник](../../agent/ui.py#L237)

```python
def _open_tree_item(self, item, column=0)
```

Переключает раскрытие каталога либо открывает файл элемента дерева.

### `MainWindow._open_search_item`

[Исходник](../../agent/ui.py#L241)

```python
def _open_search_item(self, item)
```

Открывает файл, выбранный в результатах поиска имени.

### `MainWindow._open_file`

[Исходник](../../agent/ui.py#L242)

```python
def _open_file(self, p)
```

Проверяет путь/размер и показывает UTF-8 readonly preview в новой или существующей вкладке.

### `MainWindow._close_preview_tab`

[Исходник](../../agent/ui.py#L262)

```python
def _close_preview_tab(self, index)
```

Удаляет вкладку и освобождает Qt-виджет.

### `MainWindow._switch_view`

[Исходник](../../agent/ui.py#L270)

```python
def _switch_view(self, key)
```

Переключает боковую/центральную страницу и заголовок.

### `MainWindow._append_message`

[Исходник](../../agent/ui.py#L282)

```python
def _append_message(self, role, content)
```

Экранирует текст для HTML и добавляет карточку сообщения в QTextBrowser.

### `MainWindow._send`

[Исходник](../../agent/ui.py#L287)

```python
def _send(self)
```

Берёт prompt из формы, показывает user-сообщение и запускает агента.

### `MainWindow.start_agent`

[Исходник](../../agent/ui.py#L293)

```python
def start_agent(self, prompt)
```

Создаёт чат/worker, подключает Qt Signals и блокирует повторную отправку; см. оговорку о повторном prompt в главе 11.

### `MainWindow._on_chat`

[Исходник](../../agent/ui.py#L316)

```python
def _on_chat(self, role, content)
```

Отображает сообщение движка и сохраняет assistant-текст в локальную историю GUI.

### `MainWindow._conversation_updated`

[Исходник](../../agent/ui.py#L319)

```python
def _conversation_updated(self, messages)
```

Принимает модельные сообщения движка и сохраняет чат.

### `MainWindow._save_chat`

[Исходник](../../agent/ui.py#L321)

```python
def _save_chat(self)
```

Обновляет запись чата с текущими проектом, моделью, историей и заголовком.

### `MainWindow._refresh_chats`

[Исходник](../../agent/ui.py#L327)

```python
def _refresh_chats(self)
```

Заполняет Qt-список подходящих чатов.

### `MainWindow._open_chat_item`

[Исходник](../../agent/ui.py#L334)

```python
def _open_chat_item(self, item)
```

Загружает выбранный чат и отображает его строковые сообщения.

### `MainWindow._new_chat`

[Исходник](../../agent/ui.py#L343)

```python
def _new_chat(self)
```

Очищает текущую историю GUI, если агент не запущен.

### `MainWindow._load_saved_chat`

[Исходник](../../agent/ui.py#L346)

```python
def _load_saved_chat(self)
```

Восстанавливает сохранённый QSettings chat ID и сообщения, если запись найдена.

### `MainWindow._approve_change`

[Исходник](../../agent/ui.py#L354)

```python
def _approve_change(self, path, diff, exists)
```

Показывает ApprovalDialog и преобразует код закрытия в решение движку.

### `MainWindow._log`

[Исходник](../../agent/ui.py#L359)

```python
def _log(self, text)
```

Добавляет диагностическую строку в Qt output.

### `MainWindow._show_output`

[Исходник](../../agent/ui.py#L360)

```python
def _show_output(self)
```

Переключает видимость output-панели.

### `MainWindow._stop_agent`

[Исходник](../../agent/ui.py#L361)

```python
def _stop_agent(self)
```

Запрашивает прерывание worker и отключает повторную кнопку остановки.

### `MainWindow._failed`

[Исходник](../../agent/ui.py#L363)

```python
def _failed(self, error)
```

Показывает ошибку и устанавливает статус GUI.

### `MainWindow._finished`

[Исходник](../../agent/ui.py#L365)

```python
def _finished(self)
```

Возвращает кнопки и статус в состояние готовности.

### `MainWindow._bind_shortcuts`

[Исходник](../../agent/ui.py#L367)

```python
def _bind_shortcuts(self)
```

Регистрирует клавиатурные действия для чата и проекта.

### `MainWindow._enter_send`

[Исходник](../../agent/ui.py#L372)

```python
def _enter_send(self)
```

Отличает Shift+Enter для новой строки от отправки.

### `MainWindow.closeEvent`

[Исходник](../../agent/ui.py#L376)

```python
def closeEvent(self, event)
```

Запрашивает остановку и сохраняет текущий проект/chat ID при закрытии Qt-окна.

<a id="module-agent-verifier-py"></a>

## `agent/verifier.py`

Отдельная детерминированная проверка результата этапа; engine не вызывает её автоматически.

### `StageVerifier`

[Исходник](../../agent/verifier.py#L3)

```python
class StageVerifier
```

Детерминированная проверка наличия результата этапа; не запускает команды или тесты.

### `StageVerifier.verify`

[Исходник](../../agent/verifier.py#L4)

```python
def verify(self, stage_id, *, tool_events=None, final_text='', stop_reason='')
```

Отклоняет stop_reason; принимает успешную запись или непустой финальный текст по правилам реализации.

<a id="module-agent-worker-py"></a>

## `agent/worker.py`

Qt QThread-адаптер вокруг AgentEngine; преобразует callbacks в Signal.

### `AgentWorker`

[Исходник](../../agent/worker.py#L6)

```python
class AgentWorker(QThread)
```

QThread-адаптер: содержит AgentEngine и Qt Signals для старого интерфейса.

### `AgentWorker.__init__`

[Исходник](../../agent/worker.py#L19)

```python
def __init__(self, *args, **kwargs)
```

Инициализирует состояние экземпляра AgentWorker; параметры показаны в сигнатуре, назначение описано у класса.

### `AgentWorker.run`

[Исходник](../../agent/worker.py#L25)

```python
def run(self)
```

Выполняет engine.run в контексте запущенного QThread.

### `AgentWorker.requestInterruption`

[Исходник](../../agent/worker.py#L28)

```python
def requestInterruption(self)
```

Делегирует остановку общему движку, включая сеть.

### `AgentWorker.isInterruptionRequested`

[Исходник](../../agent/worker.py#L31)

```python
def isInterruptionRequested(self)
```

Читает флаг остановки движка.

### `AgentWorker.resolve_write_approval`

[Исходник](../../agent/worker.py#L34)

```python
def resolve_write_approval(self, decision)
```

Передаёт решение Qt-диалога в движок.

### `AgentWorker._approval_result`

[Исходник](../../agent/worker.py#L38)

```python
@property
def _approval_result(self)
```

Property совместимости для проверки последнего решения в тестах.

<a id="module-core-python-assistant-service-py"></a>

## `core/python/assistant_service.py`

Локальные часы, ограниченный AST-калькулятор, атомарные заметки и отменяемые таймеры Лолы.

### `calculate`

[Исходник](../../core/python/assistant_service.py#L23)

```python
def calculate(expression)
```

Разбирает арифметику через AST с лимитами сложности, степени и конечного результата; не выполняет Python.

### `calculate.evaluate`

[Исходник](../../core/python/assistant_service.py#L28)

```python
def evaluate(node)
```

Рекурсивно разрешает только числа, скобки и whitelist арифметических операций.

### `AssistantService`

[Исходник](../../core/python/assistant_service.py#L41)

```python
class AssistantService
```

Владеет локальным хранилищем заметок, блокировкой и ограниченными таймерами до закрытия приложения.

### `AssistantService.__init__`

[Исходник](../../core/python/assistant_service.py#L42)

```python
def __init__(self, emit)
```

Инициализирует состояние экземпляра AssistantService; параметры показаны в сигнатуре, назначение описано у класса.

### `AssistantService.notes`

[Исходник](../../core/python/assistant_service.py#L45)

```python
def notes(self)
```

Читает ограниченный JSON список заметок; повреждённый файл сохраняется без перезаписи.

### `AssistantService.execute`

[Исходник](../../core/python/assistant_service.py#L52)

```python
def execute(self, name, args)
```

Выполняет именованную утилиту, валидирует параметры, атомарно пишет заметки или управляет таймерами.

### `AssistantService.fire`

[Исходник](../../core/python/assistant_service.py#L84)

```python
def fire(self, key)
```

Однократно удаляет таймер, отменяет callback и отправляет уведомление, если сервис ещё работает.

### `AssistantService.shutdown`

[Исходник](../../core/python/assistant_service.py#L90)

```python
def shutdown(self)
```

Отменяет все таймеры и запрещает новые операции.

<a id="module-core-python-bridge-py"></a>

## `core/python/bridge.py`

JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout.

### `emit`

[Исходник](../../core/python/bridge.py#L28)

```python
def emit(message)
```

Сериализует один JSON-объект и под Lock пишет целую UTF-8 строку stdout.

### `resolve_inside`

[Исходник](../../core/python/bridge.py#L49)

```python
def resolve_inside(relative: str) -> Path
```

Разрешает UI-путь относительно выбранного project_root и отклоняет выход наружу.

### `handle`

[Исходник](../../core/python/bridge.py#L59)

```python
def handle(method: str, params: dict) -> dict
```

Whitelist диспетчер RPC: состояние, проект, модель, чаты, задачи и readonly UI-файлы.

### `_handle`

[Исходник](../../core/python/bridge.py#L63)

```python
def _handle(method: str, params: dict) -> dict
```

Dispatcher RPC под общим TaskService lock: области чатов, профиль, STT, PC replies и Telegram; file scope по-прежнему ограничен.

### `main`

[Исходник](../../core/python/bridge.py#L202)

```python
def main() -> None
```

Цикл stdin JSON-lines с ID ответов, обработкой некорректного ввода и shutdown при EOF.

<a id="module-core-python-desktop-service-py"></a>

## `core/python/desktop_service.py`

Явно включаемые PC tools: human-prompt folder grants, read-only файлы, bounded web search и host screenshot broker.

### `music_url`

[Исходник](../../core/python/desktop_service.py#L33)

```python
def music_url(value)
```

Разрешает только HTTPS музыкальные хосты без credentials и нестандартного порта.

### `prompt_folders`

[Исходник](../../core/python/desktop_service.py#L40)

```python
def prompt_folders(prompt)
```

Извлекает существующие абсолютные пути только из исходного человеческого запроса и разрешает их до проверки вложенности.

### `SearchResults`

[Исходник](../../core/python/desktop_service.py#L57)

```python
class SearchResults(HTMLParser)
```

HTMLParser для ограниченного набора ссылок и заголовков поисковой выдачи; не исполняет HTML/JS.

### `SearchResults.__init__`

[Исходник](../../core/python/desktop_service.py#L59)

```python
def __init__(self)
```

Инициализирует состояние экземпляра SearchResults; параметры показаны в сигнатуре, назначение описано у класса.

### `SearchResults.handle_starttag`

[Исходник](../../core/python/desktop_service.py#L62)

```python
def handle_starttag(self, tag, attrs)
```

Распознаёт result__a, извлекает обычную HTTP(S) ссылку из DuckDuckGo redirect wrapper.

### `SearchResults.handle_data`

[Исходник](../../core/python/desktop_service.py#L74)

```python
def handle_data(self, data)
```

Собирает до 600 символов заголовка или snippet поискового результата без интерпретации разметки.

### `SearchResults.handle_endtag`

[Исходник](../../core/python/desktop_service.py#L78)

```python
def handle_endtag(self, tag)
```

Завершает ссылку и сохраняет не больше восьми результатов.

### `search_web`

[Исходник](../../core/python/desktop_service.py#L85)

```python
def search_web(query, cancelled)
```

Получает до восьми ограниченных текстовых результатов: DuckDuckGo HTML, затем Bing RSS при отказе, без чтения страниц и XML DTD.

### `DesktopService`

[Исходник](../../core/python/desktop_service.py#L120)

```python
class DesktopService
```

Сервис opt-in PC tools и брокер фиксированных операций Electron без произвольного shell.

### `DesktopService.__init__`

[Исходник](../../core/python/desktop_service.py#L121)

```python
def __init__(self, emit)
```

Инициализирует состояние экземпляра DesktopService; параметры показаны в сигнатуре, назначение описано у класса.

### `DesktopService.configure`

[Исходник](../../core/python/desktop_service.py#L127)

```python
def configure(self, params)
```

Сохраняет только boolean enabled в desktop-tools.json; каталоговые разрешения не сохраняются.

### `DesktopService.request`

[Исходник](../../core/python/desktop_service.py#L132)

```python
def request(self, operation, args, cancelled)
```

Создаёт одноразовый UUID host request, ждёт результат до 30 секунд с cooperative cancellation.

### `DesktopService.respond`

[Исходник](../../core/python/desktop_service.py#L145)

```python
def respond(self, params)
```

Принимает host-ответ только для существующего pending UUID и пробуждает ожидающий worker.

### `DesktopService.execute`

[Исходник](../../core/python/desktop_service.py#L155)

```python
def execute(self, name, args, prompt, cancelled)
```

Проверяет включение tools, исходный запрос скриншота, prompt-only папки и bounded поисковый запрос; неизвестные имена отклоняет.

<a id="module-core-python-editor-service-py"></a>

## `core/python/editor_service.py`

Ручной editor-протокол: strict UTF-8 чтение с revision, preview, одноразовый Apply через существующую атомарную snapshot-запись.

### `EditorService`

[Исходник](../../core/python/editor_service.py#L9)

```python
class EditorService
```

Хранит одно ручное предложение в памяти и использует общий sandbox/atomic write без автоматического подтверждения.

### `EditorService.__init__`

[Исходник](../../core/python/editor_service.py#L10)

```python
def __init__(self)
```

Инициализирует состояние экземпляра EditorService; параметры показаны в сигнатуре, назначение описано у класса.

### `EditorService.clear`

[Исходник](../../core/python/editor_service.py#L13)

```python
def clear(self)
```

Забывает pending proposal при новой подготовке, решении или смене проекта.

### `EditorService.read`

[Исходник](../../core/python/editor_service.py#L16)

```python
def read(self, root, path)
```

Читает ограниченные UTF-8 байты, отвергает NUL, возвращает LF-представление, newline-стиль и хеш исходных байтов.

### `EditorService.preview`

[Исходник](../../core/python/editor_service.py#L37)

```python
def preview(self, root, params)
```

Сверяет editor revision с диском, готовит конкретный diff и сохраняет одноразовый proposal без записи.

### `EditorService.resolve`

[Исходник](../../core/python/editor_service.py#L60)

```python
def resolve(self, root, params)
```

Проверяет ID/root/решение, потребляет proposal и выполняет Apply с повторной проверкой snapshot; Reject/Cancel не пишут.

<a id="module-core-python-memory-service-py"></a>

## `core/python/memory_service.py`

Строгий read/edit API памяти проекта с byte revision и защитой повреждённых файлов.

### `editable_memory`

[Исходник](../../core/python/memory_service.py#L9)

```python
def editable_memory(data)
```

Требует ровно семь редактируемых полей, проверяет типы, длины, число пунктов и отсутствие NUL до записи.

### `read_memory`

[Исходник](../../core/python/memory_service.py#L23)

```python
def read_memory(root)
```

Читает до 200 КБ strict JSON под memory lock; не исправляет и не затирает повреждённый store, возвращает SHA256 raw revision.

### `write_memory`

[Исходник](../../core/python/memory_service.py#L43)

```python
def write_memory(root, params)
```

Проверяет исходную byte revision под общим с auto-memory RLock, атомарно сохраняет только валидные поля и перечитывает результат.

<a id="module-core-python-neural-speech-py"></a>

## `core/python/neural_speech.py`

Отменяемый HTTP TTS: bounded PCM WAV, события звука и точное подтверждение плеера по sequence.

### `NeuralSpeech`

[Исходник](../../core/python/neural_speech.py#L12)

```python
class NeuralSpeech
```

Управляет отдельной нейроозвучкой через HTTP и плеер Electron, не импортируя PyTorch в Core.

### `NeuralSpeech.__init__`

[Исходник](../../core/python/neural_speech.py#L13)

```python
def __init__(self, emit)
```

Инициализирует состояние экземпляра NeuralSpeech; параметры показаны в сигнатуре, назначение описано у класса.

### `NeuralSpeech.status`

[Исходник](../../core/python/neural_speech.py#L18)

```python
def status(self, provider=None)
```

Возвращает состояние и фиксированный профиль miya-anime-ru без аудиобуфера или текста.

### `NeuralSpeech.speak`

[Исходник](../../core/python/neural_speech.py#L24)

```python
def speak(self, params, profile)
```

Проверяет текст/темп/громкость, запускает worker и ожидает подтверждения воспроизведения до 200 секунд с учётом замедленного темпа.

### `NeuralSpeech.speak.run`

[Исходник](../../core/python/neural_speech.py#L36)

```python
def run()
```

Получает WAV, публикует voice_audio и завершает операцию после плеера, отмены либо deadline.

### `NeuralSpeech.fetch`

[Исходник](../../core/python/neural_speech.py#L63)

```python
async def fetch(self, text, profile, cancelled)
```

Выполняет bounded async POST и закрывает HTTP socket при отмене.

### `NeuralSpeech.fetch.request`

[Исходник](../../core/python/neural_speech.py#L64)

```python
async def request()
```

Читает максимум 15 МБ и проверяет PCM16 mono WAV 8–48 kHz до 120 секунд.

### `NeuralSpeech.fetch.cancellation`

[Исходник](../../core/python/neural_speech.py#L76)

```python
async def cancellation()
```

Наблюдает Event отмены без блокировки event loop.

### `NeuralSpeech.playback`

[Исходник](../../core/python/neural_speech.py#L87)

```python
def playback(self, params)
```

Принимает только текущий sequence; устаревший ответ плеера не завершает новую озвучку.

### `NeuralSpeech.stop`

[Исходник](../../core/python/neural_speech.py#L94)

```python
def stop(self)
```

Отменяет сеть и публикует остановку глобальному плееру.

### `NeuralSpeech.shutdown`

[Исходник](../../core/python/neural_speech.py#L101)

```python
def shutdown(self)
```

Останавливает worker и ограниченно ждёт завершения.

<a id="module-core-python-project-search-py"></a>

## `core/python/project_search.py`

Ограниченный read-only поиск текста и путей с отменяемым отдельным worker.

### `search_project`

[Исходник](../../core/python/project_search.py#L13)

```python
def search_project(root, params, cancelled=None, *, timeout=3, max_files=15000, max_bytes=10000000)
```

Обходит выбранный корень без symlink-переходов; возвращает literal text matches или пути в пределах времени/байтов/числа файлов.

### `search_project.stop`

[Исходник](../../core/python/project_search.py#L38)

```python
def stop()
```

Проверяет cooperative cancellation и deadline, устанавливает честный статус неполного результата.

### `ProjectSearchService`

[Исходник](../../core/python/project_search.py#L118)

```python
class ProjectSearchService
```

Владеет одним отменяемым daemon worker; stdin JSON bridge остаётся доступен для других команд.

### `ProjectSearchService.__init__`

[Исходник](../../core/python/project_search.py#L119)

```python
def __init__(self)
```

Инициализирует состояние экземпляра ProjectSearchService; параметры показаны в сигнатуре, назначение описано у класса.

### `ProjectSearchService.start`

[Исходник](../../core/python/project_search.py#L125)

```python
def start(self, root, params, respond)
```

Фиксирует валидный корень/параметры и запускает worker; отклоняет параллельный поиск.

### `ProjectSearchService.start.run_search`

[Исходник](../../core/python/project_search.py#L134)

```python
def run_search()
```

Выполняет поиск, преобразует исключение в ответ и освобождает busy до отправки результата.

### `ProjectSearchService.cancel`

[Исходник](../../core/python/project_search.py#L146)

```python
def cancel(self)
```

Устанавливает event отмены только поискового worker.

### `ProjectSearchService.shutdown`

[Исходник](../../core/python/project_search.py#L150)

```python
def shutdown(self)
```

Запрашивает отмену и ограниченно ожидает собственный поток.

<a id="module-core-python-runtime-service-py"></a>

## `core/python/runtime_service.py`

Неблокирующий сервис запуска/остановки GGUF и состояний собственного llama-server.

### `RuntimeService`

[Исходник](../../core/python/runtime_service.py#L11)

```python
class RuntimeService
```

Отдельные lifecycle lock/thread/Event и состояния stopped/starting/running/stopping/error.

### `RuntimeService.__init__`

[Исходник](../../core/python/runtime_service.py#L12)

```python
def __init__(self)
```

Инициализирует состояние экземпляра RuntimeService; параметры показаны в сигнатуре, назначение описано у класса.

### `RuntimeService.start`

[Исходник](../../core/python/runtime_service.py#L29)

```python
def start(self, params)
```

Проверяет выбранные файлы, GGUF magic и integer параметры; создаёт один background worker.

### `RuntimeService.start.launch`

[Исходник](../../core/python/runtime_service.py#L62)

```python
def launch()
```

Ждёт readiness вне stdin bridge, публикует running/error и очищает отменённый запуск.

### `RuntimeService.status`

[Исходник](../../core/python/runtime_service.py#L81)

```python
def status(self)
```

Снимок состояния/метаданных/последнего вывода; обнаруживает завершение ранее готового сервера.

### `RuntimeService.stop`

[Исходник](../../core/python/runtime_service.py#L88)

```python
def stop(self)
```

Отменяет старт либо запускает собственный terminate worker; повторный Stop не создаёт новый поток.

### `RuntimeService.stop.terminate`

[Исходник](../../core/python/runtime_service.py#L96)

```python
def terminate()
```

Завершает только owned runtime и переводит сервис в stopped.

### `RuntimeService.shutdown`

[Исходник](../../core/python/runtime_service.py#L109)

```python
def shutdown(self)
```

Отменяет lifecycle, ограниченно ждёт worker и закрывает оставшийся owned runtime.

<a id="module-core-python-speech-service-py"></a>

## `core/python/speech_service.py`

Windows System.Speech через фиксированный PowerShell script и stdin JSON: каталог, TTS, Stop и owned job.

### `speech_command`

[Исходник](../../core/python/speech_service.py#L40)

```python
def speech_command()
```

Выбирает только системный Windows PowerShell и кодирует константный script в UTF-16LE; пользовательский текст не попадает в команду.

### `SpeechService`

[Исходник](../../core/python/speech_service.py#L50)

```python
class SpeechService
```

Владеет одним отменяемым Windows speech worker, cached каталогом и состоянием; микрофон не открывает.

### `SpeechService.__init__`

[Исходник](../../core/python/speech_service.py#L51)

```python
def __init__(self)
```

Инициализирует состояние экземпляра SpeechService; параметры показаны в сигнатуре, назначение описано у класса.

### `SpeechService.status`

[Исходник](../../core/python/speech_service.py#L61)

```python
def status(self)
```

Возвращает plain JSON состояния/ошибки/голосов/распознавателей без текста синтеза.

### `SpeechService.refresh`

[Исходник](../../core/python/speech_service.py#L66)

```python
def refresh(self)
```

Асинхронно перечисляет установленные голоса/распознаватели без звука и записи аудио.

### `SpeechService.speak`

[Исходник](../../core/python/speech_service.py#L69)

```python
def speak(self, params)
```

Проверяет выбранный installed voice, plain text до 6000 символов, rate/volume и запускает TTS worker.

### `SpeechService._start`

[Исходник](../../core/python/speech_service.py#L84)

```python
def _start(self, payload, state, timeout)
```

Фиксирует operation snapshot, проверяет single-flight, создаёт worker с отдельным timeout и cancel Event.

### `SpeechService._start.run`

[Исходник](../../core/python/speech_service.py#L93)

```python
def run()
```

Создаёт owned PowerShell/job, передаёт JSON через stdin, опрашивает communicate с коротким timeout, закрывает дерево и публикует итог.

### `SpeechService.stop`

[Исходник](../../core/python/speech_service.py#L151)

```python
def stop(self)
```

Только устанавливает cancel Event и stopping; stdin bridge не ждёт синтеза.

### `SpeechService.shutdown`

[Исходник](../../core/python/speech_service.py#L158)

```python
def shutdown(self)
```

Отменяет речь и ограниченно ждёт owned worker при выходе Core.

<a id="module-core-python-task-service-py"></a>

## `core/python/task_service.py`

Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval.

### `TaskService`

[Исходник](../../core/python/task_service.py#L28)

```python
class TaskService
```

Сервис одного Core-процесса: конфигурация, чат, активный run, поток и события UI.

### `TaskService.__init__`

[Исходник](../../core/python/task_service.py#L29)

```python
def __init__(self, emit, engine_factory=AgentEngine)
```

Инициализирует состояние экземпляра TaskService; параметры показаны в сигнатуре, назначение описано у класса.

### `TaskService.workflow_preferences`

[Исходник](../../core/python/task_service.py#L59)

```python
def workflow_preferences(self)
```

Возвращает настройки IDE без секретов.

### `TaskService.configure_workflow`

[Исходник](../../core/python/task_service.py#L62)

```python
def configure_workflow(self, params)
```

Проверяет настройки и ключи до сохранения; блокирует смену во время задачи, ключи оставляет в памяти.

### `TaskService.start_workflow_discovery`

[Исходник](../../core/python/task_service.py#L74)

```python
def start_workflow_discovery(self, params, respond)
```

Снимает конфигурацию выбранной роли и запускает отменяемое чтение каталога в отдельном потоке.

### `TaskService.start_workflow_discovery.discover`

[Исходник](../../core/python/task_service.py#L87)

```python
def discover()
```

Выбирает каталог нативного lifecycle либо обычный OpenAI discovery и возвращает ограниченную ошибку.

### `TaskService.idle`

[Исходник](../../core/python/task_service.py#L95)

```python
def idle(self)
```

Под RLock отказывает операции, пока task_running=True; после task_end живой завершающийся Thread не блокирует новый запрос.

### `TaskService.configure`

[Исходник](../../core/python/task_service.py#L100)

```python
def configure(self, params)
```

Сохраняет whitelist preferences и держит API-ключ только в памяти конфигурации.

### `TaskService.preferences`

[Исходник](../../core/python/task_service.py#L108)

```python
def preferences(self)
```

Возвращает URL и модель без ключа.

### `TaskService.request_delegation`

[Исходник](../../core/python/task_service.py#L112)

```python
def request_delegation(self, name, args)
```

Разрешает только delegate_task, валидирует target/prompt, создаёт одну pending передачу с исходным человеческим запросом.

### `TaskService.prepare_handoff`

[Исходник](../../core/python/task_service.py#L124)

```python
def prepare_handoff(self, root, params)
```

После завершения Лолы создаёт отдельный чат основной модели; IDE требует выбранного проекта, сохраняет источник результата.

### `TaskService.discard_handoff`

[Исходник](../../core/python/task_service.py#L138)

```python
def discard_handoff(self, params)
```

Удаляет pending передачу только по точному ID вне активной задачи, чтобы её можно было явно отклонить.

### `TaskService.companion_preferences`

[Исходник](../../core/python/task_service.py#L145)

```python
def companion_preferences(self)
```

Возвращает публичные поля отдельного профиля Лолы без API keys.

### `TaskService.configure_companion`

[Исходник](../../core/python/task_service.py#L148)

```python
def configure_companion(self, params)
```

Сохраняет независимый публичный профиль; ключи модели/STT оставляет только в памяти текущего Core.

### `TaskService.models`

[Исходник](../../core/python/task_service.py#L154)

```python
def models(self, config=None, cancelled=None)
```

Вызывает ограниченное отменяемое HTTPX-обнаружение моделей для копии настроек.

### `TaskService.diagnostic_config`

[Исходник](../../core/python/task_service.py#L157)

```python
def diagnostic_config(self, params=None)
```

Создаёт отдельную валидированную копию черновика либо текущих настроек, включая ключ только в памяти.

### `TaskService.start_model_probe`

[Исходник](../../core/python/task_service.py#L162)

```python
def start_model_probe(self, params, respond)
```

Запускает один фоновый worker проверки; запрещает параллельную проверку/активную задачу и фиксирует конфигурацию.

### `TaskService.start_model_probe.run_probe`

[Исходник](../../core/python/task_service.py#L169)

```python
def run_probe()
```

Вызывает probe_model и возвращает исходному RPC callback результат или ограниченную ошибку.

### `TaskService.cancel_model_setup`

[Исходник](../../core/python/task_service.py#L178)

```python
def cancel_model_setup(self)
```

Отменяет discovery и probe независимо от основной задачи агента.

### `TaskService.start_model_discovery`

[Исходник](../../core/python/task_service.py#L183)

```python
def start_model_discovery(self, respond, params=None)
```

Фиксирует копию настроек и запускает не больше одного discovery-потока, возвращающего ответ по исходному request ID.

### `TaskService.start_model_discovery.run_discovery`

[Исходник](../../core/python/task_service.py#L190)

```python
def run_discovery()
```

Получает список моделей или структурированную ошибку и вызывает callback ответа.

### `TaskService.move_chat`

[Исходник](../../core/python/task_service.py#L200)

```python
def move_chat(self, params)
```

Переносит канонический чат между Chat и voice без удаления сообщений; проверяет исходную область и idle.

### `TaskService.chats`

[Исходник](../../core/python/task_service.py#L214)

```python
def chats(self, root, mode=None)
```

Фильтрует индекс чатов по точной строке выбранного корня.

### `TaskService.rename`

[Исходник](../../core/python/task_service.py#L220)

```python
def rename(self, root, params)
```

Проверяет idle/title/chat scope, сохраняет только новое название и синхронизирует title выбранного чата.

### `TaskService.select_chat`

[Исходник](../../core/python/task_service.py#L236)

```python
def select_chat(self, root, chat_id=None, mode=None)
```

Загружает чат, восстанавливает embedded checkpoint/stream draft и возвращает предупреждения без повторного применения старого approval.

### `TaskService._recover_chat`

[Исходник](../../core/python/task_service.py#L252)

```python
def _recover_chat(self)
```

Восстанавливает состояние из embedded checkpoint, draft и точного блока tool result; при неопределённой записи требует проверки файла.

### `TaskService._persist_chat`

[Исходник](../../core/python/task_service.py#L321)

```python
def _persist_chat(self)
```

Сохраняет канонический чат и отправляет warning при отказе производного индекса.

### `TaskService._task_event`

[Исходник](../../core/python/task_service.py#L326)

```python
def _task_event(self, task)
```

Копирует checkpoint в тот же JSON с историей, сохраняет и публикует состояние задачи.

### `TaskService._event`

[Исходник](../../core/python/task_service.py#L332)

```python
def _event(self, kind, **data)
```

Добавляет общие run_id/chat_id к событию и передаёт emit.

### `TaskService._flush_text`

[Исходник](../../core/python/task_service.py#L335)

```python
def _flush_text(self)
```

Отменяет таймер и отправляет накопленный фрагмент с ID сообщения.

### `TaskService._flush_scheduled`

[Исходник](../../core/python/task_service.py#L344)

```python
def _flush_scheduled(self, run_id)
```

Под блокировкой допечатывает текст, только если таймер относится к текущему run.

### `TaskService._persist_draft`

[Исходник](../../core/python/task_service.py#L349)

```python
def _persist_draft(self)
```

Сохраняет текущий текст/run/turn как независимый draft и обновляет время записи.

### `TaskService._persist_draft_scheduled`

[Исходник](../../core/python/task_service.py#L354)

```python
def _persist_draft_scheduled(self, run_id, turn)
```

Сохраняет последний фрагмент даже при паузе сервера; проверяет run/turn и отменяет задачу при ошибке хранения.

### `TaskService._text_delta`

[Исходник](../../core/python/task_service.py#L365)

```python
def _text_delta(self, turn, text)
```

Отправляет порции текста примерно через 40 мс и сохраняет первый/периодический draft для crash recovery.

### `TaskService._chat_event`

[Исходник](../../core/python/task_service.py#L395)

```python
def _chat_event(self, role, text)
```

Допечатывает буфер и публикует полное сообщение с тем же ID, согласованно с таймером.

### `TaskService._request_approval`

[Исходник](../../core/python/task_service.py#L403)

```python
def _request_approval(self, path, diff, exists)
```

Создаёт UUID предложения или немедленно отменяет его, если двигатель уже остановлен.

### `TaskService.resolve_approval`

[Исходник](../../core/python/task_service.py#L411)

```python
def resolve_approval(self, params)
```

Проверяет актуальные run/proposal ID и разрешённое решение, затем освобождает engine wait.

### `TaskService.cancel`

[Исходник](../../core/python/task_service.py#L422)

```python
def cancel(self)
```

Отменяет исполнение задачи, ожидающее approval и фоновое обнаружение моделей.

### `TaskService.start`

[Исходник](../../core/python/task_service.py#L431)

```python
def start(self, root: Path, params)
```

Проверяет задачу, готовит историю/память, подписывает события и запускает agent-task.

### `TaskService.start.dispatch`

[Исходник](../../core/python/task_service.py#L465)

```python
def dispatch(name, args)
```

Направляет только разрешённые PC tools, delegate_task Лолы или обычные инструменты выбранного проекта; grants делегирования берёт из исходного человеческого запроса.

### `TaskService._save_messages`

[Исходник](../../core/python/task_service.py#L506)

```python
def _save_messages(self, messages)
```

Допечатывает stream-буфер, отменяет draft-таймер и сохраняет канонические сообщения вместе с checkpoint.

### `TaskService._run`

[Исходник](../../core/python/task_service.py#L518)

```python
def _run(self)
```

Завершает исполнение и сохранения, сбрасывает task_running под lock перед task_end; сообщает failed при ошибках.

### `TaskService.shutdown`

[Исходник](../../core/python/task_service.py#L558)

```python
def shutdown(self)
```

Отменяет операции и ограниченно ждёт потоки задачи и model discovery при EOF.

<a id="module-core-python-telegram-service-py"></a>

## `core/python/telegram_service.py`

Telegram long polling только для owner user ID: команды, состояние, ответы и текущие diff/approval; токен только в памяти Core.

### `TelegramService`

[Исходник](../../core/python/telegram_service.py#L9)

```python
class TelegramService
```

Владелец исходящего Telegram long polling; фильтрует owner ID/private chat и сериализует управление с Core.

### `TelegramService.__init__`

[Исходник](../../core/python/telegram_service.py#L10)

```python
def __init__(self, tasks, root, emit, start_task)
```

Инициализирует состояние экземпляра TelegramService; параметры показаны в сигнатуре, назначение описано у класса.

### `TelegramService.status`

[Исходник](../../core/python/telegram_service.py#L17)

```python
def status(self)
```

Возвращает состояние подключения, имя бота и owner ID без токена и URL с токеном.

### `TelegramService.start`

[Исходник](../../core/python/telegram_service.py#L22)

```python
def start(self, params)
```

Валидирует BotFather token и числовой owner ID, запускает один worker; токен хранит только в памяти.

### `TelegramService.api`

[Исходник](../../core/python/telegram_service.py#L37)

```python
def api(self, method, params=None)
```

Выполняет фиксированный запрос Telegram по TLS; необработанные HTTP exceptions не отправляются пользователю.

### `TelegramService.send`

[Исходник](../../core/python/telegram_service.py#L44)

```python
def send(self, text)
```

Отправляет plain text только owner, частями по 3500 символов, с общим лимитом 21000.

### `TelegramService.observe`

[Исходник](../../core/python/telegram_service.py#L50)

```python
def observe(self, event)
```

Ставит результаты удалённой задачи и approval уведомления в очередь до 100 записей, не блокируя Core HTTP.

### `TelegramService.command`

[Исходник](../../core/python/telegram_service.py#L61)

```python
def command(self, message)
```

Отбрасывает группы, посторонних и forwarded сообщения; под общим lock передаёт команду dispatcher.

### `TelegramService.dispatch`

[Исходник](../../core/python/telegram_service.py#L72)

```python
def dispatch(self, name, argument)
```

Реализует /status, /stop, /chat, /ide, /miya и точный /approve или /reject по актуальному ID.

### `TelegramService.poll`

[Исходник](../../core/python/telegram_service.py#L115)

```python
def poll(self)
```

Проверяет getMe, отбрасывает старую очередь, читает getUpdates и отправляет уведомления; повторяет сетевые ошибки без раскрытия токена.

### `TelegramService.stop`

[Исходник](../../core/python/telegram_service.py#L147)

```python
def stop(self)
```

Запрашивает отключение и закрывает HTTP client; токен не возвращает.

### `TelegramService.shutdown`

[Исходник](../../core/python/telegram_service.py#L154)

```python
def shutdown(self)
```

Отключает polling и ограниченно ждёт worker при закрытии Core.

<a id="module-core-python-transcription-service-py"></a>

## `core/python/transcription_service.py`

Ограниченная WAV-транскрипция через локальный whisper.cpp или совместимый API с отменой HTTP.

### `TranscriptionService`

[Исходник](../../core/python/transcription_service.py#L12)

```python
class TranscriptionService
```

Отдельный отменяемый STT worker; передаёт WAV на явно настроенный endpoint без хранения аудио на диске.

### `TranscriptionService.__init__`

[Исходник](../../core/python/transcription_service.py#L13)

```python
def __init__(self)
```

Инициализирует состояние экземпляра TranscriptionService; параметры показаны в сигнатуре, назначение описано у класса.

### `TranscriptionService.start`

[Исходник](../../core/python/transcription_service.py#L19)

```python
def start(self, params, profile, respond)
```

Проверяет base64 и WAV PCM16 mono 16 kHz до 60 секунд; не допускает второй одновременно работающий запрос.

### `TranscriptionService.start.transcribe`

[Исходник](../../core/python/transcription_service.py#L33)

```python
def transcribe()
```

Отправляет multipart file/model/language/response_format, проверяет текст и отвечает по исходному RPC ID.

### `TranscriptionService.request_audio`

[Исходник](../../core/python/transcription_service.py#L47)

```python
async def request_audio(self, audio, profile, cancelled)
```

Запускает async HTTP и наблюдатель отмены с общим deadline 90 секунд; закрывает socket при cancel.

### `TranscriptionService.request_audio.request`

[Исходник](../../core/python/transcription_service.py#L48)

```python
async def request()
```

Передаёт multipart WAV и читает до 1 МБ ответа, проверяя строку text до 50000 символов.

### `TranscriptionService.request_audio.cancellation`

[Исходник](../../core/python/transcription_service.py#L61)

```python
async def cancellation()
```

Проверяет межпоточный Event каждые 50 мс без блокировки asyncio loop.

### `TranscriptionService.stop`

[Исходник](../../core/python/transcription_service.py#L72)

```python
def stop(self)
```

Выставляет cancel flag и закрывает HTTP client активного распознавания.

### `TranscriptionService.shutdown`

[Исходник](../../core/python/transcription_service.py#L77)

```python
def shutdown(self)
```

Отменяет запрос и ограниченно ждёт завершения worker.

<a id="module-main-py"></a>

## `main.py`

Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-tools-build-windows-core-py"></a>

## `tools/build_windows_core.py`

PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков.

### `main`

[Исходник](../../tools/build_windows_core.py#L9)

```python
def main()
```

Проверяет Windows x64/Python 3.12 и вызывает PyInstaller с данными навыков, SDK и необходимым PEM runtime.

<a id="module-tools-check-docs-py"></a>

## `tools/check_docs.py`

Проверка локальных ссылок, source lines, покрытия аннотаций и актуальности каталога.

### `check_links`

[Исходник](../../tools/check_docs.py#L8)

```python
def check_links(files)
```

Проверяет локальные цели ссылок и существование строк #L; внешние URL не скачивает.

### `main`

[Исходник](../../tools/check_docs.py#L34)

```python
def main()
```

Сопоставляет структурные справочники с AST и завершает проверку ошибкой при расхождении/битой ссылке.

<a id="module-tools-check-live-model-py"></a>

## `tools/check_live_model.py`

Opt-in smoke реальной модели: disposable AppData/проект, Chat/IDE/Лола, без approvals записи, JSON отчёт.

### `fingerprint`

[Исходник](../../tools/check_live_model.py#L13)

```python
def fingerprint(root)
```

Хеширует только искусственные исходники, чтобы обнаружить неожиданную запись модели.

### `scenario`

[Исходник](../../tools/check_live_model.py#L19)

```python
def scenario(service, events, mode, root, timeout)
```

Запускает реальный task flow; все write approvals отклоняет, результат проверяет по событиям/истории.

### `main`

[Исходник](../../tools/check_live_model.py#L61)

```python
def main()
```

Изолирует AppData до импорта Core, проверяет выбранную модель без загрузок и записывает JSON-отчёт.

<a id="module-tools-doc-notes-py"></a>

## `tools/doc_notes.py`

Ручные назначения файлов и символов для справочников; не является runtime-модулем агента.

### `register`

[Исходник](../../tools/doc_notes.py#L107)

```python
def register(module, text)
```

Добавляет вручную написанные строки «имя | назначение» в словарь аннотаций.

<a id="module-tools-generate-code-reference-py"></a>

## `tools/generate_code_reference.py`

Извлекает объявления из Python/TypeScript AST и создаёт Markdown-каталоги.

### `configure_console`

[Исходник](../../tools/generate_code_reference.py#L25)

```python
def configure_console()
```

Включает UTF-8 для диагностического вывода CLI, включая Windows с исходной кодировкой CP1252.

### `git_executable`

[Исходник](../../tools/generate_code_reference.py#L32)

```python
def git_executable()
```

Находит Git в PATH, LCA_GIT или штатной поставке GitHub Desktop на Windows.

### `repository_files`

[Исходник](../../tools/generate_code_reference.py#L44)

```python
def repository_files()
```

Возвращает существующие tracked/untracked файлы Git без ignored-окружений и сборок.

### `file_description`

[Исходник](../../tools/generate_code_reference.py#L52)

```python
def file_description(name)
```

Находит ручное назначение файла или заголовок главы; неизвестный исходник требует аннотации.

### `python_symbols`

[Исходник](../../tools/generate_code_reference.py#L67)

```python
def python_symbols(path)
```

Извлекает классы, функции, методы и вложенные объявления Python с реальными строками.

### `python_symbols.visit`

[Исходник](../../tools/generate_code_reference.py#L72)

```python
def visit(node, scope=())
```

Рекурсивно обходит объявления, сохраняя квалифицированное имя родителя.

### `symbol_description`

[Исходник](../../tools/generate_code_reference.py#L96)

```python
def symbol_description(file, symbol)
```

Подбирает проверяемую ручную аннотацию; отсутствие назначения рабочего символа — ошибка.

### `markdown_symbol`

[Исходник](../../tools/generate_code_reference.py#L121)

```python
def markdown_symbol(file, symbol, description, language)
```

Формирует блок объявления с сигнатурой, назначением и ссылкой на строку исходника.

### `module_anchor`

[Исходник](../../tools/generate_code_reference.py#L131)

```python
def module_anchor(file)
```

Создаёт стабильный ASCII-якорь модуля для оглавления больших справочников.

### `render`

[Исходник](../../tools/generate_code_reference.py#L136)

```python
def render()
```

Строит содержимое всех справочников без изменения файлов рабочего приложения.

### `main`

[Исходник](../../tools/generate_code_reference.py#L212)

```python
def main()
```

Записывает справочники либо с --check проверяет, совпадают ли они с текущим AST.

<a id="module-tools-prepare-windows-dependencies-py"></a>

## `tools/prepare_windows_dependencies.py`

Загрузка официальных зависимостей по SHA256, выбор server/DLL и подготовка офлайн-пакета без запуска установщиков.

### `verified_download`

[Исходник](../../tools/prepare_windows_dependencies.py#L10)

```python
def verified_download(spec, destination)
```

Reuse a verified cache or download atomically, rejecting any hash mismatch.

### `prepare`

[Исходник](../../tools/prepare_windows_dependencies.py#L31)

```python
def prepare(root)
```

Stage server/DLLs/licenses and offline VC++ bootstrap under ignored build/.

<a id="module-tools-tts-piper-server-py"></a>

## `tools/tts/piper_server.py`

CPU Piper адаптер прежнего HTTP TTS API: русский ONNX голос, PCM16 WAV, лимиты и отмена между предложениями.

### `synthesize`

[Исходник](../../tools/tts/piper_server.py#L15)

```python
def synthesize(voice, text, guard)
```

Собирает чанки Piper в PCM16 mono WAV до 120 секунд/15 МиБ и проверяет отмену после каждого предложения.

### `main`

[Исходник](../../tools/tts/piper_server.py#L37)

```python
def main()
```

Загружает ONNX голос через CPUExecutionProvider, подключает синтез к общему HTTP handler и слушает только localhost.

<a id="module-tools-tts-qwen-server-py"></a>

## `tools/tts/qwen_server.py`

Отдельный localhost Qwen3-TTS сервер: VoiceDesign 1.7B или CustomVoice 0.6B с готовым голосом, русский язык и PCM16 WAV.

### `synthesize`

[Исходник](../../tools/tts/qwen_server.py#L17)

```python
def synthesize(model, text, style)
```

Генерирует русский звук: готовый speaker через CustomVoice либо описание через VoiceDesign; фиксирует seed и ограничение токенов, кодирует PCM16 WAV в памяти.

### `Handler`

[Исходник](../../tools/tts/qwen_server.py#L32)

```python
class Handler(BaseHTTPRequestHandler)
```

Loopback HTTP handler с JSON-only POST, запретом Origin и одним слотом генерации.

### `Handler.do_GET`

[Исходник](../../tools/tts/qwen_server.py#L33)

```python
def do_GET(self)
```

Возвращает health после загрузки модели; остальные GET получают 404.

### `Handler.do_POST`

[Исходник](../../tools/tts/qwen_server.py#L39)

```python
def do_POST(self)
```

Проверяет запрос и concurrency, останавливает talker при отключении клиента/deadline и освобождает слот в finally.

### `Handler.do_POST.guard`

[Исходник](../../tools/tts/qwen_server.py#L53)

```python
def guard(module, args)
```

PyTorch forward pre-hook проверяет срок 150 секунд и закрытие HTTP-сокета без чтения текста запроса.

### `Handler.reply`

[Исходник](../../tools/tts/qwen_server.py#L78)

```python
def reply(self, code, body, content_type)
```

Пишет ответ с явными Content-Type и Content-Length.

### `Handler.log_message`

[Исходник](../../tools/tts/qwen_server.py#L82)

```python
def log_message(self, format, *args)
```

Не сохраняет тексты и запросы пользователя в HTTP access log.

### `main`

[Исходник](../../tools/tts/qwen_server.py#L86)

```python
def main()
```

Выбирает VoiceDesign 1.7B либо CustomVoice 0.6B и speaker, получает локальный снимок, выбирает CPU/CUDA и dtype, проверяет запас VRAM и слушает только 127.0.0.1:9080.

<a id="module-tools-tts-training-export-and-evaluate-py"></a>

## `tools/tts/training/export_and_evaluate.py`

ONNX экспорт с совместимым tracer и CPU/STT проверкой четырёх новых фраз без объявления совпадения тембра.

### `main`

[Исходник](../../tools/tts/training/export_and_evaluate.py#L23)

```python
def main()
```

Экспортирует обученный VITS через legacy ONNX tracer, проверяет модель, синтезирует новые фразы на CPU и сохраняет оценку STT/задержки.

<a id="module-tools-tts-training-generate-serena-py"></a>

## `tools/tts/training/generate_serena.py`

Возобновляемый корпус Qwen Serena: закреплённая revision, PCM22k WAV, локальный STT отбор и provenance каждого примера.

### `texts`

[Исходник](../../tools/tts/training/generate_serena.py#L14)

```python
def texts()
```

Собирает уникальный русский корпус из исходных фраз и бытовых комбинаций без перезаписи WAV при продолжении.

### `normalize`

[Исходник](../../tools/tts/training/generate_serena.py#L38)

```python
def normalize(text)
```

Удаляет различия регистра, ё и пунктуации для приблизительного сравнения текста с STT.

### `main`

[Исходник](../../tools/tts/training/generate_serena.py#L43)

```python
def main()
```

Фиксирует manifest, пакетно генерирует Serena, передискретизирует WAV, проверяет STT и сохраняет принятые metadata/журнал.

<a id="module-tools-tts-training-pipeline-py"></a>

## `tools/tts/training/pipeline.py`

Однопроцессный локальный контроллер этапов с атомарным состоянием, границами шагов и остановкой при ошибках.

### `save_state`

[Исходник](../../tools/tts/training/pipeline.py#L13)

```python
def save_state(path, **values)
```

Атомарно обновляет JSON состояния этапа, PID и ошибку либо оценку без преждевременного статуса готовности.

### `run`

[Исходник](../../tools/tts/training/pipeline.py#L22)

```python
def run(command, log_path)
```

Запускает зависимый subprocess со структурированными аргументами и отдельным локальным журналом, возвращает exit code.

### `main`

[Исходник](../../tools/tts/training/pipeline.py#L31)

```python
def main()
```

Удерживает Windows lock, ждёт generator, выполняет ступени 6000/12000 шагов, экспорт и проверку; сообщает trial_ready только после ASR.

<a id="module-tools-tts-training-run-training-py"></a>

## `tools/tts/training/run_training.py`

Ограниченное Windows дообучение VITS: преобразование Linux checkpoint, warmstart, eSpeak workaround и resume.

### `SaveFinalCheckpoint`

[Исходник](../../tools/tts/training/run_training.py#L11)

```python
class SaveFinalCheckpoint(Callback)
```

Сохраняет фактические последние веса даже при достижении max_steps посередине эпохи.

### `SaveFinalCheckpoint.on_train_end`

[Исходник](../../tools/tts/training/run_training.py#L13)

```python
def on_train_end(self, trainer, pl_module)
```

Вызывает trainer.save_checkpoint для final.ckpt в корне training, независимо от эпохальных val_mel checkpoints.

### `prepare_checkpoint`

[Исходник](../../tools/tts/training/run_training.py#L17)

```python
def prepare_checkpoint(source, target)
```

Из доверенного Linux checkpoint извлекает state_dict с временной совместимостью Path, исключает старый оптимизатор и сохраняет описание hyperparameters.

### `main`

[Исходник](../../tools/tts/training/run_training.py#L31)

```python
def main()
```

Проверяет объём данных, задаёт warmstart/resume, BF16 GPU и ограниченные шаги, исправляет путь eSpeak и состав checkpoint callbacks.

### `main.resume_fit_start`

[Исходник](../../tools/tts/training/run_training.py#L85)

```python
def resume_fit_start(model)
```

Отключает сохранённый однократный warmstart при resume, чтобы LightningCLI не сбрасывал обученные веса к базовому голосу.
