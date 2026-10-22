# Справочник Python

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [agent/__init__.py](#module-agent-init-py)
- [agent/chat_store.py](#module-agent-chat-store-py)
- [agent/context_manager.py](#module-agent-context-manager-py)
- [agent/conversation.py](#module-agent-conversation-py)
- [agent/editor_io.py](#module-agent-editor-io-py)
- [agent/engine.py](#module-agent-engine-py)
- [agent/mcp.py](#module-agent-mcp-py)
- [agent/model_client.py](#module-agent-model-client-py)
- [agent/model_gateway.py](#module-agent-model-gateway-py)
- [agent/model_manager.py](#module-agent-model-manager-py)
- [agent/model_preferences.py](#module-agent-model-preferences-py)
- [agent/planner.py](#module-agent-planner-py)
- [agent/project_memory.py](#module-agent-project-memory-py)
- [agent/runtime.py](#module-agent-runtime-py)
- [agent/security.py](#module-agent-security-py)
- [agent/skills.py](#module-agent-skills-py)
- [agent/task_store.py](#module-agent-task-store-py)
- [agent/tools.py](#module-agent-tools-py)
- [agent/ui.py](#module-agent-ui-py)
- [agent/verifier.py](#module-agent-verifier-py)
- [agent/worker.py](#module-agent-worker-py)
- [core/python/bridge.py](#module-core-python-bridge-py)
- [core/python/task_service.py](#module-core-python-task-service-py)
- [main.py](#module-main-py)
- [tools/check_docs.py](#module-tools-check-docs-py)
- [tools/doc_notes.py](#module-tools-doc-notes-py)
- [tools/generate_code_reference.py](#module-tools-generate-code-reference-py)

<a id="module-agent-init-py"></a>

## `agent/__init__.py`

Маркер Python-пакета agent; не запускает UI или модель.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-agent-chat-store-py"></a>

## `agent/chat_store.py`

JSON-чаты и индекс истории вне папки проекта.

### `_now`

[Исходник](../../agent/chat_store.py#L17)

```python
def _now() -> str
```

Возвращает UTC ISO-время для метаданных чата.

### `_atomic_write`

[Исходник](../../agent/chat_store.py#L21)

```python
def _atomic_write(path: Path, data: Any) -> None
```

Записывает JSON через временный файл и replace; общую транзакцию чата с индексом не создаёт.

### `_load_index`

[Исходник](../../agent/chat_store.py#L33)

```python
def _load_index() -> list[dict[str, Any]]
```

Читает индекс; при отсутствующем или повреждённом JSON возвращает пустой список.

### `list_chats`

[Исходник](../../agent/chat_store.py#L43)

```python
def list_chats() -> list[dict[str, Any]]
```

Возвращает метаданные чатов по убыванию updated_at; фильтрацию проекта делает сервис.

### `create_chat`

[Исходник](../../agent/chat_store.py#L47)

```python
def create_chat(project_root: str='', model: str='', title: str='Новый чат') -> dict[str, Any]
```

Генерирует UUID, создаёт запись и добавляет её метаданные в индекс.

### `load_chat`

[Исходник](../../agent/chat_store.py#L67)

```python
def load_chat(chat_id: str) -> dict[str, Any] | None
```

Читает JSON одного чата по ID; входной ID должен быть проверен вызывающим сервисом.

### `save_chat`

[Исходник](../../agent/chat_store.py#L76)

```python
def save_chat(chat: dict[str, Any]) -> None
```

Обновляет дату, JSON чата и отдельную запись индекса.

### `delete_chat`

[Исходник](../../agent/chat_store.py#L85)

```python
def delete_chat(chat_id: str) -> bool
```

Удаляет файл диалога и запись индекса; не меняет файлы проекта.

### `rename_chat`

[Исходник](../../agent/chat_store.py#L95)

```python
def rename_chat(chat_id: str, title: str) -> dict[str, Any] | None
```

Нормализует заголовок до 120 символов и сохраняет существующий чат.

### `title_from_messages`

[Исходник](../../agent/chat_store.py#L103)

```python
def title_from_messages(messages: list[dict[str, Any]]) -> str
```

Выбирает первое непустое user-сообщение и делает короткий заголовок.

<a id="module-agent-context-manager-py"></a>

## `agent/context_manager.py`

Простой ограничитель рабочего контекста активного AgentRuntime.

### `ContextManager`

[Исходник](../../agent/context_manager.py#L5)

```python
class ContextManager
```

Простой builder активного runtime-контекста: system, недавние сообщения и метаданные.

### `ContextManager.__init__`

[Исходник](../../agent/context_manager.py#L6)

```python
def __init__(self, max_chars=80000, recent_rounds=12)
```

Инициализирует состояние экземпляра ContextManager; параметры показаны в сигнатуре, назначение описано у класса.

### `ContextManager.build`

[Исходник](../../agent/context_manager.py#L8)

```python
def build(self, messages, task=None, skills=None)
```

Берёт хвост сообщений, добавляет состояние задачи/skills и сокращает содержимое; tool-пары отдельно не группирует.

<a id="module-agent-conversation-py"></a>

## `agent/conversation.py`

Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп.

### `_message_size`

[Исходник](../../agent/conversation.py#L15)

```python
def _message_size(message)
```

Оценивает размер сериализованного сообщения в символах, не токенах модели.

### `_bounded_turn`

[Исходник](../../agent/conversation.py#L22)

```python
def _bounded_turn(turn)
```

Копирует ход и обрезает объёмные tool outputs, оставляя структуру сообщений.

### `select_recent_history`

[Исходник](../../agent/conversation.py#L38)

```python
def select_recent_history(history, max_chars=MAX_CONTEXT_CHARS, max_turns=MAX_CONTEXT_TURNS)
```

Выбирает недавние целые пользовательские ходы с ограничением объёма и количества.

### `build_messages`

[Исходник](../../agent/conversation.py#L81)

```python
def build_messages(history, prompt)
```

Добавляет новый user prompt к выбранной недавней истории.

### `compact_live_messages`

[Исходник](../../agent/conversation.py#L88)

```python
def compact_live_messages(messages, max_chars=80000, keep_recent_rounds=10)
```

Сокращает текущий модельный контекст, группируя assistant tool calls и их результаты.

### `compact_live_messages.flatten`

[Исходник](../../agent/conversation.py#L120)

```python
def flatten(items)
```

Собирает system-сообщение и группы сообщений в плоский список.

### `compact_live_messages.total`

[Исходник](../../agent/conversation.py#L124)

```python
def total(items)
```

Считает символьный размер выбранных групп для ограничения контекста.

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

[Исходник](../../agent/engine.py#L31)

```python
class EventHook
```

Синхронный набор callbacks для независимых от GUI событий движка.

### `EventHook.__init__`

[Исходник](../../agent/engine.py#L33)

```python
def __init__(self)
```

Инициализирует состояние экземпляра EventHook; параметры показаны в сигнатуре, назначение описано у класса.

### `EventHook.connect`

[Исходник](../../agent/engine.py#L36)

```python
def connect(self, callback)
```

Добавляет обработчик события.

### `EventHook.emit`

[Исходник](../../agent/engine.py#L39)

```python
def emit(self, *args)
```

Вызывает копию списка обработчиков с переданными аргументами в текущем потоке.

### `AgentEngine`

[Исходник](../../agent/engine.py#L44)

```python
class AgentEngine
```

Состояние и исполнение одного запуска модели с tools, approval, лимитами, памятью и checkpoint.

### `AgentEngine.requestInterruption`

[Исходник](../../agent/engine.py#L49)

```python
def requestInterruption(self)
```

Выставляет Event остановки и отменяет активные сетевые future клиента.

### `AgentEngine.isInterruptionRequested`

[Исходник](../../agent/engine.py#L54)

```python
def isInterruptionRequested(self)
```

Возвращает текущее состояние флага остановки.

### `AgentEngine.__init__`

[Исходник](../../agent/engine.py#L57)

```python
def __init__(self, base_url, api_key, model, project_root, prompt, force_tool=None, settings=None, history=None, memory=None, auto_memory=True, task_id=None)
```

Инициализирует состояние экземпляра AgentEngine; параметры показаны в сигнатуре, назначение описано у класса.

### `AgentEngine._checkpoint`

[Исходник](../../agent/engine.py#L87)

```python
def _checkpoint(self, stage=None, event='')
```

Обновляет этап/последнее событие, сохраняет checkpoint и публикует снимок.

### `AgentEngine.resolve_write_approval`

[Исходник](../../agent/engine.py#L97)

```python
def resolve_write_approval(self, decision)
```

Принимает решение и освобождает ожидание записи; неизвестное решение превращает в reject.

### `AgentEngine._ask_write_approval`

[Исходник](../../agent/engine.py#L108)

```python
def _ask_write_approval(self, path, diff, exists)
```

Запрашивает согласие через событие и ждёт apply/reject/cancel с проверкой остановки.

### `AgentEngine._emit_change`

[Исходник](../../agent/engine.py#L130)

```python
def _emit_change(self, path, diff, exists, status, error='')
```

Публикует path/diff/status одного предложения изменения.

### `AgentEngine._looks_like_action_request`

[Исходник](../../agent/engine.py#L140)

```python
@staticmethod
def _looks_like_action_request(prompt)
```

Эвристически распознаёт просьбу действия по русским/английским словам.

### `AgentEngine._verify_task_completion`

[Исходник](../../agent/engine.py#L150)

```python
def _verify_task_completion(self, client, messages, max_tokens)
```

Дополнительным модельным запросом проверяет, не является ли финал только планом; при ошибке проверки разрешает завершение.

### `AgentEngine.run`

[Исходник](../../agent/engine.py#L186)

```python
def run(self)
```

Строит контекст, выполняет потоковые ходы и tools, обрабатывает остановку, сохраняет состояние и закрывает клиент.

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
def __init__(self, base_url, api_key, interrupted)
```

Инициализирует состояние экземпляра ModelClient; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelClient.check_cancelled`

[Исходник](../../agent/model_client.py#L55)

```python
def check_cancelled(self)
```

Выбрасывает ModelCancelled, если общий Event установлен.

### `ModelClient.submit`

[Исходник](../../agent/model_client.py#L59)

```python
def submit(self, coroutine)
```

Планирует корутину в сетевом loop и учитывает её future в pending.

### `ModelClient._forget`

[Исходник](../../agent/model_client.py#L68)

```python
def _forget(self, future)
```

Убирает завершённую future из защищённого множества.

### `ModelClient.result`

[Исходник](../../agent/model_client.py#L72)

```python
def result(self, future)
```

Ждёт результат короткими интервалами и переводит cancellation в исключение движка.

### `ModelClient.create`

[Исходник](../../agent/model_client.py#L82)

```python
def create(self, **params)
```

Возвращает ModelStream для stream=True или готовый async-ответ для stream=False.

### `ModelClient.cancel`

[Исходник](../../agent/model_client.py#L88)

```python
def cancel(self)
```

Отменяет снимок всех активных future.

### `ModelClient.close`

[Исходник](../../agent/model_client.py#L94)

```python
def close(self)
```

Отменяет async-задачи, закрывает SDK и останавливает сетевой поток/loop.

### `ModelClient.close.shutdown`

[Исходник](../../agent/model_client.py#L95)

```python
async def shutdown()
```

Async-фаза закрытия: cancel/gather задач и client.close внутри принадлежащего loop.

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

<a id="module-agent-model-manager-py"></a>

## `agent/model_manager.py`

Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции.

### `LocalModel`

[Исходник](../../agent/model_manager.py#L29)

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

[Исходник](../../agent/model_manager.py#L37)

```python
@property
def size_gb(self) -> float
```

Property размера файла в GiB-подобном делении на 1024^3.

### `LocalModel.to_dict`

[Исходник](../../agent/model_manager.py#L40)

```python
def to_dict(self)
```

Преобразует запись модели в словарь с округлённым size_gb.

### `ModelManager`

[Исходник](../../agent/model_manager.py#L46)

```python
class ModelManager
```

Сканирование и импорт GGUF в отдельный каталог моделей.

### `ModelManager.__init__`

[Исходник](../../agent/model_manager.py#L47)

```python
def __init__(self, models_dir: str | Path | None=None)
```

Инициализирует состояние экземпляра ModelManager; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelManager._quantization`

[Исходник](../../agent/model_manager.py#L52)

```python
@staticmethod
def _quantization(name: str) -> str
```

Определяет quantization по имени файла регулярным выражением; не анализирует бинарное содержимое.

### `ModelManager.scan`

[Исходник](../../agent/model_manager.py#L56)

```python
def scan(self) -> list[LocalModel]
```

Рекурсивно находит .gguf и возвращает доступные записи.

### `ModelManager.import_model`

[Исходник](../../agent/model_manager.py#L65)

```python
def import_model(self, source: str | Path, *, copy=True) -> LocalModel
```

Проверяет расширение/файл и при copy=True копирует в models_dir.

### `LocalRuntime`

[Исходник](../../agent/model_manager.py#L78)

```python
class LocalRuntime
```

Управляет отдельным процессом llama-server и его HTTP endpoint.

### `LocalRuntime.__init__`

[Исходник](../../agent/model_manager.py#L80)

```python
def __init__(self, *, runtime_path: str | Path | None=None)
```

Инициализирует состояние экземпляра LocalRuntime; параметры показаны в сигнатуре, назначение описано у класса.

### `LocalRuntime.find_executable`

[Исходник](../../agent/model_manager.py#L88)

```python
@staticmethod
def find_executable(explicit: str='') -> str | None
```

Ищет явно заданный путь, служебный runtime, текущий каталог и PATH.

### `LocalRuntime.free_port`

[Исходник](../../agent/model_manager.py#L104)

```python
@staticmethod
def free_port(host='127.0.0.1') -> int
```

Получает свободный локальный TCP-порт через временный bind.

### `LocalRuntime.running`

[Исходник](../../agent/model_manager.py#L110)

```python
@property
def running(self) -> bool
```

Property: процесс существует и ещё не завершился.

### `LocalRuntime.base_url`

[Исходник](../../agent/model_manager.py#L114)

```python
@property
def base_url(self) -> str
```

Property URL /v1 для назначенного порта.

### `LocalRuntime.start`

[Исходник](../../agent/model_manager.py#L117)

```python
def start(self, model: LocalModel, *, ctx_size=32768, gpu_layers=-1, port=None, extra_args=None)
```

Запускает llama-server с model/context/GPU flags и ждёт health до 45 секунд.

### `LocalRuntime._healthy`

[Исходник](../../agent/model_manager.py#L152)

```python
def _healthy(self) -> bool
```

Проверяет HTTP /models с коротким timeout.

### `LocalRuntime.stop`

[Исходник](../../agent/model_manager.py#L161)

```python
def stop(self)
```

Завершает процесс, при необходимости убивает и очищает runtime-состояние.

### `LocalRuntime.status`

[Исходник](../../agent/model_manager.py#L176)

```python
def status(self) -> dict
```

Возвращает состояние процесса, порт, URL и метаданные модели.

### `LocalRuntime.__del__`

[Исходник](../../agent/model_manager.py#L185)

```python
def __del__(self)
```

Пытается закрыть процесс при удалении экземпляра; не заменяет явное управление жизненным циклом.

<a id="module-agent-model-preferences-py"></a>

## `agent/model_preferences.py`

Валидация и сохранение только URL и ID модели для Electron Core.

### `validate_preferences`

[Исходник](../../agent/model_preferences.py#L12)

```python
def validate_preferences(params)
```

Разрешает HTTP(S) endpoint без credentials/query/fragment, проверяет порт и возвращает только URL/ID модели.

### `load_preferences`

[Исходник](../../agent/model_preferences.py#L23)

```python
def load_preferences()
```

Читает и проверяет JSON; при ошибке возвращает копию defaults, никогда не восстанавливает ключ.

### `save_preferences`

[Исходник](../../agent/model_preferences.py#L31)

```python
def save_preferences(params)
```

Атомарно сохраняет whitelist полей во внешний служебный JSON.

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

<a id="module-agent-project-memory-py"></a>

## `agent/project_memory.py`

Компактная структурированная память проекта, очистка и форматирование для модели.

### `_now`

[Исходник](../../agent/project_memory.py#L28)

```python
def _now() -> str
```

Возвращает UTC ISO-время записи памяти.

### `_key`

[Исходник](../../agent/project_memory.py#L32)

```python
def _key(project_root: str) -> str
```

Хеширует нормализованный project_root для имени каталога памяти.

### `memory_path`

[Исходник](../../agent/project_memory.py#L37)

```python
def memory_path(project_root: str) -> Path
```

Формирует путь project_memory/<hash>/memory.json.

### `empty_memory`

[Исходник](../../agent/project_memory.py#L41)

```python
def empty_memory(project_root: str='') -> dict[str, Any]
```

Создаёт пустую структурированную память с корнем и полями версии.

### `_clean_text`

[Исходник](../../agent/project_memory.py#L56)

```python
def _clean_text(value: Any, limit: int) -> str
```

Удаляет NUL, нормализует пробелы и ограничивает строку.

### `validate_memory`

[Исходник](../../agent/project_memory.py#L63)

```python
def validate_memory(data: Any, project_root: str='') -> dict[str, Any]
```

Проверяет структуру, поля, длины и дубликаты памяти.

### `load_project_memory`

[Исходник](../../agent/project_memory.py#L87)

```python
def load_project_memory(project_root: str) -> dict[str, Any]
```

Загружает и валидирует запись; при ошибке создаёт пустую память.

### `save_project_memory`

[Исходник](../../agent/project_memory.py#L98)

```python
def save_project_memory(project_root: str, data: dict[str, Any]) -> dict[str, Any]
```

Валидирует и атомарно сохраняет JSON памяти выбранного проекта.

### `clear_project_memory`

[Исходник](../../agent/project_memory.py#L115)

```python
def clear_project_memory(project_root: str) -> None
```

Удаляет только память указанного проекта.

### `format_memory_context`

[Исходник](../../agent/project_memory.py#L125)

```python
def format_memory_context(memory: dict[str, Any], max_chars: int=3600) -> str
```

Формирует ограниченный справочный блок для system prompt.

### `merge_memory_update`

[Исходник](../../agent/project_memory.py#L151)

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
def working_context(self, messages)
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

[Исходник](../../agent/task_store.py#L40)

```python
def save_task(task)
```

Обновляет timestamp и записывает checkpoint через temporary+fsync+replace.

### `load_task`

[Исходник](../../agent/task_store.py#L55)

```python
def load_task(chat_id)
```

Читает checkpoint; отсутствие или повреждённый JSON даёт None.

### `clear_task`

[Исходник](../../agent/task_store.py#L62)

```python
def clear_task(chat_id)
```

Удаляет checkpoint, не удаляя историю чата.

### `set_stage`

[Исходник](../../agent/task_store.py#L66)

```python
def set_stage(task, stage_id, status='active', event='')
```

Обновляет активный этап и помечает более ранние этапы завершёнными.

### `finish_task`

[Исходник](../../agent/task_store.py#L77)

```python
def finish_task(task, status='completed', reason='')
```

Завершает этапы, задаёт итоговый статус/причину и сохраняет checkpoint.

<a id="module-agent-tools-py"></a>

## `agent/tools.py`

Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test.

### `list_files`

[Исходник](../../agent/tools.py#L11)

```python
def list_files(root, path='.', recursive=False, max_entries=200, max_depth=5)
```

Перечисляет разрешённые файлы с фильтрами, ограничением entries и глубины обхода.

### `safe_relative`

[Исходник](../../agent/tools.py#L55)

```python
def safe_relative(target, base)
```

Возвращает относительное POSIX-представление пути для результатов tools.

### `read_file`

[Исходник](../../agent/tools.py#L60)

```python
def read_file(root, path)
```

Читает UTF-8 файл не больше 120000 байт внутри корня.

### `search_text`

[Исходник](../../agent/tools.py#L74)

```python
def search_text(root, query, path='.', case_sensitive=False, max_depth=5)
```

Ищет подстроку в UTF-8 файлах с пределами размера, глубины, числа совпадений и длины строки.

### `preview_file_change`

[Исходник](../../agent/tools.py#L122)

```python
def preview_file_change(root, path, content)
```

Проверяет предложение и строит unified diff, не записывая содержимое.

### `write_file`

[Исходник](../../agent/tools.py#L156)

```python
def write_file(root, path, content, overwrite=False, *, approved=False)
```

Требует approved, повторно проверяет путь/overwrite и записывает файл через temporary+fsync+replace.

### `execute_tool`

[Исходник](../../agent/tools.py#L201)

```python
def execute_tool(name, arguments, project_root, settings=None, *, approved=False)
```

Диспетчер четырёх функций; превращает ожидаемые ошибки в структурированный tool result.

### `run_sandbox_self_test`

[Исходник](../../agent/tools.py#L224)

```python
def run_sandbox_self_test()
```

Выполняет изолированный внутренний unittest-набор проверки файловой границы и возвращает сводку.

### `run_sandbox_self_test.SandboxTests`

[Исходник](../../agent/tools.py#L229)

```python
class SandboxTests(unittest.TestCase)
```

Внутренняя suite временных project/outside каталогов; не пользовательский runtime-класс.

### `run_sandbox_self_test.SandboxTests.setUp`

[Исходник](../../agent/tools.py#L230)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `run_sandbox_self_test.SandboxTests.tearDown`

[Исходник](../../agent/tools.py#L237)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `run_sandbox_self_test.SandboxTests.test_read_inside_allowed`

[Исходник](../../agent/tools.py#L238)

```python
def test_read_inside_allowed(self)
```

Проверка: Внутренний self-test разрешает чтение в корне.

### `run_sandbox_self_test.SandboxTests.test_parent_traversal_denied`

[Исходник](../../agent/tools.py#L239)

```python
def test_parent_traversal_denied(self)
```

Проверка: Внутренний self-test отклоняет выход через родительский каталог.

### `run_sandbox_self_test.SandboxTests.test_absolute_outside_denied`

[Исходник](../../agent/tools.py#L241)

```python
def test_absolute_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний абсолютный путь.

### `run_sandbox_self_test.SandboxTests.test_list_outside_denied`

[Исходник](../../agent/tools.py#L243)

```python
def test_list_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний list_files.

### `run_sandbox_self_test.SandboxTests.test_search_outside_denied`

[Исходник](../../agent/tools.py#L246)

```python
def test_search_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний search_text.

### `run_sandbox_self_test.SandboxTests.test_symlink_escape_denied`

[Исходник](../../agent/tools.py#L249)

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

<a id="module-core-python-bridge-py"></a>

## `core/python/bridge.py`

JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout.

### `emit`

[Исходник](../../core/python/bridge.py#L14)

```python
def emit(message)
```

Сериализует один JSON-объект и под Lock пишет целую UTF-8 строку stdout.

### `resolve_inside`

[Исходник](../../core/python/bridge.py#L25)

```python
def resolve_inside(relative: str) -> Path
```

Разрешает UI-путь относительно выбранного project_root и отклоняет выход наружу.

### `handle`

[Исходник](../../core/python/bridge.py#L35)

```python
def handle(method: str, params: dict) -> dict
```

Whitelist диспетчер RPC: состояние, проект, модель, чаты, задачи и readonly UI-файлы.

### `main`

[Исходник](../../core/python/bridge.py#L96)

```python
def main() -> None
```

Цикл stdin JSON-lines с ID ответов, обработкой некорректного ввода и shutdown при EOF.

<a id="module-core-python-task-service-py"></a>

## `core/python/task_service.py`

Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval.

### `TaskService`

[Исходник](../../core/python/task_service.py#L17)

```python
class TaskService
```

Сервис одного Core-процесса: конфигурация, чат, активный run, поток и события UI.

### `TaskService.__init__`

[Исходник](../../core/python/task_service.py#L18)

```python
def __init__(self, emit, engine_factory=AgentEngine)
```

Инициализирует состояние экземпляра TaskService; параметры показаны в сигнатуре, назначение описано у класса.

### `TaskService.idle`

[Исходник](../../core/python/task_service.py#L33)

```python
def idle(self)
```

Отказывает операции, когда поток текущей задачи ещё жив.

### `TaskService.configure`

[Исходник](../../core/python/task_service.py#L37)

```python
def configure(self, params)
```

Сохраняет whitelist preferences и держит API-ключ только в памяти конфигурации.

### `TaskService.preferences`

[Исходник](../../core/python/task_service.py#L45)

```python
def preferences(self)
```

Возвращает URL и модель без ключа.

### `TaskService.models`

[Исходник](../../core/python/task_service.py#L48)

```python
def models(self)
```

Запрашивает /models через urllib с timeout/лимитом ответа и возвращает ID.

### `TaskService.chats`

[Исходник](../../core/python/task_service.py#L59)

```python
def chats(self, root)
```

Фильтрует индекс чатов по точной строке выбранного корня.

### `TaskService.select_chat`

[Исходник](../../core/python/task_service.py#L62)

```python
def select_chat(self, root, chat_id=None)
```

Создаёт/загружает чат после проверки ID и проекта; running после перезапуска переводит в paused.

### `TaskService._event`

[Исходник](../../core/python/task_service.py#L80)

```python
def _event(self, kind, **data)
```

Добавляет общие run_id/chat_id к событию и передаёт emit.

### `TaskService._flush_text`

[Исходник](../../core/python/task_service.py#L83)

```python
def _flush_text(self)
```

Отменяет таймер и отправляет накопленный фрагмент с ID сообщения.

### `TaskService._flush_scheduled`

[Исходник](../../core/python/task_service.py#L92)

```python
def _flush_scheduled(self, run_id)
```

Под блокировкой допечатывает текст, только если таймер относится к текущему run.

### `TaskService._text_delta`

[Исходник](../../core/python/task_service.py#L97)

```python
def _text_delta(self, turn, text)
```

Собирает текст под RLock и организует отправку по размеру или интервалу около 40 мс.

### `TaskService._chat_event`

[Исходник](../../core/python/task_service.py#L111)

```python
def _chat_event(self, role, text)
```

Допечатывает буфер и публикует полное сообщение с тем же ID, согласованно с таймером.

### `TaskService._request_approval`

[Исходник](../../core/python/task_service.py#L119)

```python
def _request_approval(self, path, diff, exists)
```

Создаёт UUID предложения или немедленно отменяет его, если двигатель уже остановлен.

### `TaskService.resolve_approval`

[Исходник](../../core/python/task_service.py#L127)

```python
def resolve_approval(self, params)
```

Проверяет актуальные run/proposal ID и разрешённое решение, затем освобождает engine wait.

### `TaskService.cancel`

[Исходник](../../core/python/task_service.py#L138)

```python
def cancel(self)
```

Запрашивает отмену сетевого исполнения и незавершённого approval.

### `TaskService.start`

[Исходник](../../core/python/task_service.py#L146)

```python
def start(self, root: Path, params)
```

Проверяет задачу, готовит историю/память, подписывает события и запускает agent-task.

### `TaskService._save_messages`

[Исходник](../../core/python/task_service.py#L190)

```python
def _save_messages(self, messages)
```

Заменяет messages выбранного чата списком движка и сохраняет JSON.

### `TaskService._run`

[Исходник](../../core/python/task_service.py#L194)

```python
def _run(self)
```

Обёртка исполнения с failed и обязательным task_end/flush в finally.

### `TaskService.shutdown`

[Исходник](../../core/python/task_service.py#L205)

```python
def shutdown(self)
```

Запрашивает отмену и ограниченно ждёт поток при завершении моста.

<a id="module-main-py"></a>

## `main.py`

Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

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

<a id="module-tools-doc-notes-py"></a>

## `tools/doc_notes.py`

Ручные назначения файлов и символов для справочников; не является runtime-модулем агента.

### `register`

[Исходник](../../tools/doc_notes.py#L97)

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
