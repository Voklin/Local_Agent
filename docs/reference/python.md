# Справочник Python

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [agent/__init__.py](#module-agent-init-py)
- [agent/artifact_store.py](#module-agent-artifact-store-py)
- [agent/auto_budget.py](#module-agent-auto-budget-py)
- [agent/call_journal.py](#module-agent-call-journal-py)
- [agent/capability_profiles.py](#module-agent-capability-profiles-py)
- [agent/chat_store.py](#module-agent-chat-store-py)
- [agent/child_executor.py](#module-agent-child-executor-py)
- [agent/companion_policy.py](#module-agent-companion-policy-py)
- [agent/companion_preferences.py](#module-agent-companion-preferences-py)
- [agent/connection_profiles.py](#module-agent-connection-profiles-py)
- [agent/container_runner.py](#module-agent-container-runner-py)
- [agent/context_builder.py](#module-agent-context-builder-py)
- [agent/context_manager.py](#module-agent-context-manager-py)
- [agent/context_tools.py](#module-agent-context-tools-py)
- [agent/conversation.py](#module-agent-conversation-py)
- [agent/delegation.py](#module-agent-delegation-py)
- [agent/diagnostics_evidence.py](#module-agent-diagnostics-evidence-py)
- [agent/editor_io.py](#module-agent-editor-io-py)
- [agent/engine.py](#module-agent-engine-py)
- [agent/git_checkpoints.py](#module-agent-git-checkpoints-py)
- [agent/inference_scheduler.py](#module-agent-inference-scheduler-py)
- [agent/json_tools.py](#module-agent-json-tools-py)
- [agent/language_diagnostics.py](#module-agent-language-diagnostics-py)
- [agent/managed_worktrees.py](#module-agent-managed-worktrees-py)
- [agent/mcp.py](#module-agent-mcp-py)
- [agent/mcp_client.py](#module-agent-mcp-client-py)
- [agent/mcp_sessions.py](#module-agent-mcp-sessions-py)
- [agent/model_client.py](#module-agent-model-client-py)
- [agent/model_discovery.py](#module-agent-model-discovery-py)
- [agent/model_gateway.py](#module-agent-model-gateway-py)
- [agent/model_manager.py](#module-agent-model-manager-py)
- [agent/model_preferences.py](#module-agent-model-preferences-py)
- [agent/model_probe.py](#module-agent-model-probe-py)
- [agent/operation_context.py](#module-agent-operation-context-py)
- [agent/optional_process.py](#module-agent-optional-process-py)
- [agent/planner.py](#module-agent-planner-py)
- [agent/process_identity.py](#module-agent-process-identity-py)
- [agent/process_job.py](#module-agent-process-job-py)
- [agent/progress_guard.py](#module-agent-progress-guard-py)
- [agent/project_command.py](#module-agent-project-command-py)
- [agent/project_index.py](#module-agent-project-index-py)
- [agent/project_index_policy.py](#module-agent-project-index-policy-py)
- [agent/project_instructions.py](#module-agent-project-instructions-py)
- [agent/project_knowledge.py](#module-agent-project-knowledge-py)
- [agent/project_memory.py](#module-agent-project-memory-py)
- [agent/project_symbols.py](#module-agent-project-symbols-py)
- [agent/projects.py](#module-agent-projects-py)
- [agent/readonly_research.py](#module-agent-readonly-research-py)
- [agent/request_budget.py](#module-agent-request-budget-py)
- [agent/response_outcome.py](#module-agent-response-outcome-py)
- [agent/responses_adapter.py](#module-agent-responses-adapter-py)
- [agent/run_policy.py](#module-agent-run-policy-py)
- [agent/run_registry.py](#module-agent-run-registry-py)
- [agent/run_state.py](#module-agent-run-state-py)
- [agent/runtime.py](#module-agent-runtime-py)
- [agent/security.py](#module-agent-security-py)
- [agent/skills.py](#module-agent-skills-py)
- [agent/smart_context.py](#module-agent-smart-context-py)
- [agent/storage.py](#module-agent-storage-py)
- [agent/subagent_profiles.py](#module-agent-subagent-profiles-py)
- [agent/task_activity.py](#module-agent-task-activity-py)
- [agent/task_contract.py](#module-agent-task-contract-py)
- [agent/task_graph.py](#module-agent-task-graph-py)
- [agent/task_store.py](#module-agent-task-store-py)
- [agent/tool_executor.py](#module-agent-tool-executor-py)
- [agent/tool_recovery.py](#module-agent-tool-recovery-py)
- [agent/tools.py](#module-agent-tools-py)
- [agent/ui.py](#module-agent-ui-py)
- [agent/verification_evidence.py](#module-agent-verification-evidence-py)
- [agent/verification_plan.py](#module-agent-verification-plan-py)
- [agent/verifier.py](#module-agent-verifier-py)
- [agent/worker.py](#module-agent-worker-py)
- [agent/workspace_access.py](#module-agent-workspace-access-py)
- [agent/workspace_edits.py](#module-agent-workspace-edits-py)
- [agent/workspace_read.py](#module-agent-workspace-read-py)
- [agent/workspace_revision.py](#module-agent-workspace-revision-py)
- [agent/workspace_search.py](#module-agent-workspace-search-py)
- [agent/workspace_snapshots.py](#module-agent-workspace-snapshots-py)
- [core/python/assistant_service.py](#module-core-python-assistant-service-py)
- [core/python/background_job.py](#module-core-python-background-job-py)
- [core/python/bridge.py](#module-core-python-bridge-py)
- [core/python/conversation_service.py](#module-core-python-conversation-service-py)
- [core/python/desktop_service.py](#module-core-python-desktop-service-py)
- [core/python/editor_service.py](#module-core-python-editor-service-py)
- [core/python/extension_service.py](#module-core-python-extension-service-py)
- [core/python/ide_completion.py](#module-core-python-ide-completion-py)
- [core/python/ide_sessions.py](#module-core-python-ide-sessions-py)
- [core/python/memory_service.py](#module-core-python-memory-service-py)
- [core/python/neural_speech.py](#module-core-python-neural-speech-py)
- [core/python/optional_ide_service.py](#module-core-python-optional-ide-service-py)
- [core/python/project_search.py](#module-core-python-project-search-py)
- [core/python/protocol.py](#module-core-python-protocol-py)
- [core/python/run_session.py](#module-core-python-run-session-py)
- [core/python/runtime_service.py](#module-core-python-runtime-service-py)
- [core/python/session_service.py](#module-core-python-session-service-py)
- [core/python/speech_service.py](#module-core-python-speech-service-py)
- [core/python/task_execution.py](#module-core-python-task-execution-py)
- [core/python/task_service.py](#module-core-python-task-service-py)
- [core/python/telegram_service.py](#module-core-python-telegram-service-py)
- [core/python/transcription_service.py](#module-core-python-transcription-service-py)
- [core/python/workspace_review.py](#module-core-python-workspace-review-py)
- [main.py](#module-main-py)
- [prototypes/neutral-ide/install_test_extensions.py](#module-prototypes-neutral-ide-install-test-extensions-py)
- [prototypes/neutral-ide/prepare.py](#module-prototypes-neutral-ide-prepare-py)
- [prototypes/neutral-ide/test_host.py](#module-prototypes-neutral-ide-test-host-py)
- [tools/audit_core_20261025.py](#module-tools-audit-core-20261025-py)
- [tools/audit_post_stage8.py](#module-tools-audit-post-stage8-py)
- [tools/benchmark_agent.py](#module-tools-benchmark-agent-py)
- [tools/benchmark_project_index.py](#module-tools-benchmark-project-index-py)
- [tools/benchmark_storage.py](#module-tools-benchmark-storage-py)
- [tools/build_windows_core.py](#module-tools-build-windows-core-py)
- [tools/check_docs.py](#module-tools-check-docs-py)
- [tools/check_live_model.py](#module-tools-check-live-model-py)
- [tools/doc_notes.py](#module-tools-doc-notes-py)
- [tools/generate_brand_icons.py](#module-tools-generate-brand-icons-py)
- [tools/generate_code_reference.py](#module-tools-generate-code-reference-py)
- [tools/prepare_windows_dependencies.py](#module-tools-prepare-windows-dependencies-py)
- [tools/test_agent_readiness.py](#module-tools-test-agent-readiness-py)
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

<a id="module-agent-artifact-store-py"></a>

## `agent/artifact_store.py`

Неизменяемые UTF-8 результаты инструментов: SHA-256, атомарная запись, проверка целостности.

### `ArtifactStore`

[Исходник](../../agent/artifact_store.py#L13)

```python
class ArtifactStore
```

Адресуемые по содержимому локальные outputs, общие для истории и квитанций; удаление чата не удаляет резервные исходники.

### `ArtifactStore.__init__`

[Исходник](../../agent/artifact_store.py#L16)

```python
def __init__(self, directory)
```

Инициализирует состояние экземпляра ArtifactStore; параметры показаны в сигнатуре, назначение описано у класса.

### `ArtifactStore.path`

[Исходник](../../agent/artifact_store.py#L19)

```python
def path(self, digest)
```

Разрешает только 64 hex SHA-256, без произвольного filesystem path.

### `ArtifactStore.put`

[Исходник](../../agent/artifact_store.py#L25)

```python
def put(self, text)
```

Записывает UTF-8 через временный файл, fsync/replace до ссылки в БД; существующие bytes проверяет для дедупликации.

### `ArtifactStore.get`

[Исходник](../../agent/artifact_store.py#L47)

```python
def get(self, reference)
```

Проверяет длину и SHA-256; отсутствующий или испорченный результат даёт явную ошибку и не запускает tool повторно.

<a id="module-agent-auto-budget-py"></a>

## `agent/auto_budget.py`

Read-only определение фактического окна LM Studio/Ollama/llama.cpp, bounded cache, разбор context rejection и SDK tokenizer только уже загруженного экземпляра.

### `local_endpoint`

[Исходник](../../agent/auto_budget.py#L18)

```python
def local_endpoint(url)
```

Определяет loopback/private/.local адрес для автоматической локальной task policy без DNS-запроса.

### `valid_window`

[Исходник](../../agent/auto_budget.py#L26)

```python
def valid_window(value)
```

Принимает только целое окно 512–1048576, исключая bool и некорректные metadata.

### `loaded_profile`

[Исходник](../../agent/auto_budget.py#L31)

```python
def loaded_profile(data, model, kind)
```

Выбирает контекст выбранного загруженного экземпляра; trained maximum не подменяет размер слота.

### `discover_profile`

[Исходник](../../agent/auto_budget.py#L62)

```python
async def discover_profile(base_url, model, api_key='', *, force=False)
```

Выполняет bounded GET metadata к настроенному origin, кэширует на 30 с; не запускает inference/load/unload.

### `discover_profile.read`

[Исходник](../../agent/auto_budget.py#L74)

```python
async def read(kind, path)
```

Ограничивает размер JSON 512 КБ и игнорирует неподдерживаемые endpoints/некорректные ответы.

### `context_rejection`

[Исходник](../../agent/auto_budget.py#L95)

```python
def context_rejection(error)
```

Извлекает только явно подписанное окно из HTTP 400/413/422 до начала потока; чужие числа не использует.

### `LoadedTokenizer`

[Исходник](../../agent/auto_budget.py#L115)

```python
class LoadedTokenizer
```

Владеет необязательным SDK handle уже загруженной модели; не вызывает model()/load().

### `LoadedTokenizer.__init__`

[Исходник](../../agent/auto_budget.py#L117)

```python
def __init__(self, client, model, cancelled)
```

Инициализирует состояние экземпляра LoadedTokenizer; параметры показаны в сигнатуре, назначение описано у класса.

### `LoadedTokenizer.connect`

[Исходник](../../agent/auto_budget.py#L121)

```python
@classmethod
def connect(cls, base_url, instances, cancelled)
```

На anonymous root/v1 HTTP LM Studio находит handle через list_loaded с timeout; освобождает неиспользованный client.

### `LoadedTokenizer.count`

[Исходник](../../agent/auto_budget.py#L137)

```python
def count(self, text)
```

Считает токены сериализованного prompt material на сервере, проверяя отмену до и после bounded RPC.

### `LoadedTokenizer.close`

[Исходник](../../agent/auto_budget.py#L145)

```python
def close(self)
```

Освобождает SDK sockets/threads вместе с общим ModelClient.

<a id="module-agent-call-journal-py"></a>

## `agent/call_journal.py`

Транзакционный журнал SQLite с прежними lifecycle/recovery контрактами и отдельным legacy JSONL reader.

### `_unknown`

[Исходник](../../agent/call_journal.py#L26)

```python
def _unknown(result)
```

Распознаёт неопределённый исход по коду или явному флагу результата.

### `_placeholder`

[Исходник](../../agent/call_journal.py#L32)

```python
def _placeholder(result)
```

Отличает синтетические записи восстановления от настоящих квитанций инструмента.

### `_replaceable`

[Исходник](../../agent/call_journal.py#L37)

```python
def _replaceable(result)
```

Разрешает заменять только отсутствующий, неизвестный либо синтетический результат.

### `_index`

[Исходник](../../agent/call_journal.py#L41)

```python
def _index(value)
```

Проверяет неотрицательный целочисленный якорь; bool не считается индексом.

### `_canonical_calls`

[Исходник](../../agent/call_journal.py#L47)

```python
def _canonical_calls(calls)
```

Нормализует имена, call IDs и исходные JSON-строки; дубликаты внутри пачки и неверная форма отклоняются.

### `_resolution_result`

[Исходник](../../agent/call_journal.py#L69)

```python
def _resolution_result(resolution)
```

Создаёт помеченное наблюдение пользователя; оно не выдумывает исходный вывод инструмента.

### `LegacyCallJournal`

[Исходник](../../agent/call_journal.py#L75)

```python
class LegacyCallJournal
```

Сохранённая JSONL реализация: читает и проверяет старые события; новый runtime использует подкласс CallJournal.

### `LegacyCallJournal.__init__`

[Исходник](../../agent/call_journal.py#L82)

```python
def __init__(self, chat_id, journal_id, directory=None)
```

Инициализирует состояние экземпляра LegacyCallJournal; параметры показаны в сигнатуре, назначение описано у класса.

### `LegacyCallJournal._read`

[Исходник](../../agent/call_journal.py#L95)

```python
def _read(self)
```

Читает ограниченные строки, проверяет version/identity; оборванный хвост допускается, повреждённая полная строка останавливает восстановление.

### `LegacyCallJournal._state`

[Исходник](../../agent/call_journal.py#L126)

```python
def _state(self)
```

Воспроизводит события в пачки и состояния вызовов, проверяя пересечения и монотонность фаз.

### `LegacyCallJournal._call_state`

[Исходник](../../agent/call_journal.py#L177)

```python
@staticmethod
def _call_state(batches, message_index, call_id)
```

Находит вызов строго по сохранённому якорю и ID либо отклоняет чужую идентичность.

### `LegacyCallJournal._unresolved_state`

[Исходник](../../agent/call_journal.py#L184)

```python
@staticmethod
def _unresolved_state(state)
```

Выделяет начатые эффекты без квитанции и результаты OUTCOME_UNKNOWN, ещё не проверенные человеком.

### `LegacyCallJournal._append`

[Исходник](../../agent/call_journal.py#L190)

```python
def _append(self, event, state_info)
```

Проверяет конечный JSON и размер, исправляет оборванный хвост, выполняет flush/fsync перед возвратом.

### `LegacyCallJournal.prepare_batch`

[Исходник](../../agent/call_journal.py#L210)

```python
def prepare_batch(self, calls, message_index, assistant_content=None)
```

Долговечно записывает полную пачку до любого исполнения; повтор той же пачки идемпотентен.

### `LegacyCallJournal.set_phase`

[Исходник](../../agent/call_journal.py#L228)

```python
def set_phase(self, message_index, call_id, phase, *, effectful=True)
```

Сохраняет prepared/awaiting_approval/started; запрещает откат фазы и изменение класса уже начатого эффекта.

### `LegacyCallJournal.record_result`

[Исходник](../../agent/call_journal.py#L244)

```python
def record_result(self, message_index, call_id, result)
```

Сохраняет настоящую квитанцию до контекста/UI; известный результат нельзя заменить другим.

### `LegacyCallJournal.entries`

[Исходник](../../agent/call_journal.py#L258)

```python
def entries(self)
```

Возвращает независимые копии вызовов с фазами, аргументами, квитанциями и ручными решениями.

### `LegacyCallJournal.delete_chat`

[Исходник](../../agent/call_journal.py#L272)

```python
@staticmethod
def delete_chat(chat_id)
```

Удаляет только файлы журналов указанного чата с проверкой идентичности и вычисленного имени.

### `LegacyCallJournal.unresolved`

[Исходник](../../agent/call_journal.py#L284)

```python
def unresolved(self)
```

Возвращает список эффектов, которые требуют проверки пользователем перед продолжением.

### `LegacyCallJournal.resolve`

[Исходник](../../agent/call_journal.py#L287)

```python
def resolve(self, message_index, call_id, resolution)
```

Долговечно сохраняет явное completed/not_executed для неизвестного эффекта; инструмент не запускается.

### `LegacyCallJournal._missing_result`

[Исходник](../../agent/call_journal.py#L300)

```python
@staticmethod
def _missing_result(state)
```

Различает не начатый вызов, прерванное чтение и неизвестный начатый эффект.

### `LegacyCallJournal.recover`

[Исходник](../../agent/call_journal.py#L309)

```python
def recover(self, messages)
```

Сначала проверяет все якоря на копии истории, затем восстанавливает полные пары, сохраняет настоящие receipts и возвращает нерешённые эффекты.

### `JournalTransaction`

[Исходник](../../agent/call_journal.py#L383)

```python
class JournalTransaction
```

Сочетает общий RLock эпохи с BEGIN IMMEDIATE, охватывающим проверку lifecycle и append в разных процессах.

### `JournalTransaction.__init__`

[Исходник](../../agent/call_journal.py#L386)

```python
def __init__(self, lock, database)
```

Инициализирует состояние экземпляра JournalTransaction; параметры показаны в сигнатуре, назначение описано у класса.

### `JournalTransaction.__enter__`

[Исходник](../../agent/call_journal.py#L391)

```python
def __enter__(self)
```

Захватывает thread lock и открывает реентерабельную транзакцию; при ошибке открытия освобождает lock.

### `JournalTransaction.__exit__`

[Исходник](../../agent/call_journal.py#L404)

```python
def __exit__(self, *error)
```

Завершает вложенный transaction context и всегда освобождает thread lock.

### `CallJournal`

[Исходник](../../agent/call_journal.py#L411)

```python
class CallJournal(LegacyCallJournal)
```

Канонический SQLite журнал с теми же prepared/started/receipt/recovery контрактами, однократным импортом эпохи и tombstones.

### `CallJournal.__init__`

[Исходник](../../agent/call_journal.py#L414)

```python
def __init__(self, chat_id, journal_id, directory=None)
```

Инициализирует состояние экземпляра CallJournal; параметры показаны в сигнатуре, назначение описано у класса.

### `CallJournal._stored_event`

[Исходник](../../agent/call_journal.py#L423)

```python
def _stored_event(self, event)
```

Большой JSON receipt заменяет ссылкой SHA-256; identity и фаза действия остаются непосредственно в БД.

### `CallJournal._read`

[Исходник](../../agent/call_journal.py#L433)

```python
def _read(self)
```

В одной транзакции проверяет legacy lifecycle, копирует и сверяет события, гидратирует результаты; corrupt complete row останавливает импорт.

### `CallJournal._append`

[Исходник](../../agent/call_journal.py#L462)

```python
def _append(self, event, state_info)
```

Атомарно добавляет SQLite receipt и один epoch tool counter по проверенной chat/journal/run привязке, включая artifact-backed result; повтор не удваивает счёт.

### `CallJournal.delete_chat`

[Исходник](../../agent/call_journal.py#L483)

```python
@staticmethod
def delete_chat(chat_id)
```

Удаляет события всех эпох выбранного чата и сохраняет запрет повторного импорта старых JSONL.

<a id="module-agent-capability-profiles-py"></a>

## `agent/capability_profiles.py`

Фиксированные ограничивающие профили Chat/IDE/Лолы; включённые расширения остаются источником разрешений.

### `mode_groups`

[Исходник](../../agent/capability_profiles.py#L9)

```python
def mode_groups(mode, root, definitions)
```

Ограничивает группы выбранным режимом и наличием root; не включает выключенные tools и не доверяет MCP annotations.

<a id="module-agent-chat-store-py"></a>

## `agent/chat_store.py`

Разговоры и метаданные истории в транзакционном SQLite с миграцией старых JSON.

### `_valid_id`

[Исходник](../../agent/chat_store.py#L19)

```python
def _valid_id(chat_id)
```

Проверяет 32-символьный hex UUID до доступа к канонической записи чата.

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

Атомарный JSON writer для настроек/совместимости; историю и checkpoint сохраняет Storage.

### `_database`

[Исходник](../../agent/chat_store.py#L41)

```python
def _database()
```

Выбирает SQLite профиль по текущему CHAT_DIR; тестовые временные каталоги не попадают в данные пользователя.

### `list_chats`

[Исходник](../../agent/chat_store.py#L47)

```python
def list_chats()
```

Возвращает metadata с pinned/updated_at порядком без чтения transcripts.

### `read_chat_catalog`

[Исходник](../../agent/chat_store.py#L51)

```python
def read_chat_catalog(**scope)
```

Выбирает компактную индексированную metadata проекцию и migration warnings; корпус JSON повторно не читает.

### `search_chats`

[Исходник](../../agent/chat_store.py#L56)

```python
def search_chats(query, **scope)
```

Передаёт ограниченный областью поиск title/user/assistant в индекс, без load_chat для каждого результата.

### `create_chat`

[Исходник](../../agent/chat_store.py#L61)

```python
def create_chat(project_root: str='', model: str='', title: str='Новый чат', mode=None) -> dict[str, Any]
```

Генерирует UUID и атомарно создаёт пустую историю, metadata и поисковую запись заголовка.

### `load_chat`

[Исходник](../../agent/chat_store.py#L82)

```python
def load_chat(chat_id: str) -> dict[str, Any] | None
```

Валидирует ID и возвращает согласованный SQLite snapshot с полными outputs и единственным checkpoint.

### `save_chat`

[Исходник](../../agent/chat_store.py#L88)

```python
def save_chat(chat: dict[str, Any], *, checkpoint=True) -> str | None
```

В одной транзакции сохраняет metadata/messages/index и явный checkpoint; ошибки откатывают всё изменение.

### `delete_chat`

[Исходник](../../agent/chat_store.py#L101)

```python
def delete_chat(chat_id: str) -> bool
```

Атомарно удаляет каноническую историю, задачу, поиск и receipts; сохраняет tombstone и legacy восстановительные материалы.

### `rename_chat`

[Исходник](../../agent/chat_store.py#L124)

```python
def rename_chat(chat_id: str, title: str) -> dict[str, Any] | None
```

Нормализует заголовок до 120 символов и сохраняет существующий чат.

### `title_from_messages`

[Исходник](../../agent/chat_store.py#L132)

```python
def title_from_messages(messages: list[dict[str, Any]]) -> str
```

Выбирает первое непустое user-сообщение и делает короткий заголовок.

<a id="module-agent-child-executor-py"></a>

## `agent/child_executor.py`

Real readonly child AgentEngine handoff with inherited connection, cancellable join, durable journal and fresh bounded handback.

### `ChildExecutor`

[Исходник](../../agent/child_executor.py#L13)

```python
class ChildExecutor
```

Владеет одним синхронным readonly handoff, переиспользует AgentEngine/ToolExecutor/CallJournal и общий scheduler.

### `ChildExecutor.__init__`

[Исходник](../../agent/child_executor.py#L14)

```python
def __init__(self, owner, root, definitions, config, profiles=None)
```

Инициализирует состояние экземпляра ChildExecutor; параметры показаны в сигнатуре, назначение описано у класса.

### `ChildExecutor.notify`

[Исходник](../../agent/child_executor.py#L19)

```python
def notify(self, run, task)
```

Проецирует текущий child state в canonical checkpoint родителя под control lock; это дерево исполнения, не второй план.

### `ChildExecutor.execute`

[Исходник](../../agent/child_executor.py#L27)

```python
def execute(self, args)
```

Создаёт bounded child на том же подключении, ждёт transport cleanup, сохраняет отдельные сообщения и возвращает только свежий ограниченный handback.

### `ChildExecutor.execute.dispatch`

[Исходник](../../agent/child_executor.py#L43)

```python
def dispatch(name, arguments)
```

Разрешает пересечение list_files/read_file/read_range, фиксирует SHA чтений и блокирует возврат stale/слишком широкого результата.

### `ChildExecutor.execute.messages`

[Исходник](../../agent/child_executor.py#L61)

```python
def messages(value)
```

Сохраняет историю ребёнка в его checkpoint, не смешивая её с родительским чатом или общим каталогом разговоров.

<a id="module-agent-companion-policy-py"></a>

## `agent/companion_policy.py`

Граница делегирования Лолы по исходному намерению человека и очистка ответов/озвучки от разметки.

### `is_coding_request`

[Исходник](../../agent/companion_policy.py#L6)

```python
def is_coding_request(prompt)
```

Определяет разрешённое делегирование по исходному запросу; исключает бытовые значения слова «код» и программы мероприятий.

### `clean_speech_text`

[Исходник](../../agent/companion_policy.py#L18)

```python
def clean_speech_text(text)
```

Удаляет Markdown/HTML/reasoning и блоки кода, сохраняет читаемые слова и переводит числовое умножение в речь.

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

<a id="module-agent-connection-profiles-py"></a>

## `agent/connection_profiles.py`

Именованные публичные конфигурации моделей без API-ключей.

### `ConnectionProfiles`

[Исходник](../../agent/connection_profiles.py#L9)

```python
class ConnectionProfiles
```

Каталог именованных публичных параметров API-моделей; секретные поля не принимаются в сохранённый профиль.

### `ConnectionProfiles.__init__`

[Исходник](../../agent/connection_profiles.py#L10)

```python
def __init__(self, directory=None)
```

Инициализирует состояние экземпляра ConnectionProfiles; параметры показаны в сигнатуре, назначение описано у класса.

### `ConnectionProfiles.list`

[Исходник](../../agent/connection_profiles.py#L13)

```python
def list(self)
```

Читает ограниченный по размеру список профилей из пользовательского каталога.

### `ConnectionProfiles.save`

[Исходник](../../agent/connection_profiles.py#L20)

```python
def save(self, params)
```

Проверяет имя/ID/параметры и атомарно добавляет или заменяет один из максимум 30 профилей.

### `ConnectionProfiles.remove`

[Исходник](../../agent/connection_profiles.py#L30)

```python
def remove(self, identity)
```

Удаляет выбранную запись, сохраняя другие профили и активную конфигурацию модели.

<a id="module-agent-container-runner-py"></a>

## `agent/container_runner.py`

Opt-in Linux Docker runner: readonly bind, без сети/pull, CPU/RAM/PID лимиты, отдельное approval и cleanup daemon container.

### `container_command`

[Исходник](../../agent/container_runner.py#L12)

```python
def container_command(root, args, settings, name)
```

Строит фиксированные Docker restrictions; user program/image/argv не становятся runtime options, cwd проверен внутри root.

### `container_status`

[Исходник](../../agent/container_runner.py#L27)

```python
def container_status(root, context)
```

Без установки/pull проверяет наличие Docker и Linux engine, отдельно сообщает только наличие wsl executable.

### `run_container`

[Исходник](../../agent/container_runner.py#L35)

```python
def run_container(root, args, settings, context, approve)
```

Показывает точный runtime proposal, требует approval, проверяет локальный образ, ограничивает время и удаляет только свой UUID container даже после отмены CLI.

<a id="module-agent-context-builder-py"></a>

## `agent/context_builder.py`

Подбор сохранённых диапазонов проекта, provenance, дедупликация, финальная проверка доступа/хеша и точный предпросмотр внешней отправки.

### `local_context_endpoint`

[Исходник](../../agent/context_builder.py#L20)

```python
def local_context_endpoint(url)
```

Разрешает автоматический локальный retrieval только HTTP(S) loopback, исключая LAN и внешние адреса.

### `encode_pack`

[Исходник](../../agent/context_builder.py#L29)

```python
def encode_pack(pack)
```

Сериализует source data отдельно от system instructions и без абсолютного корня проекта.

### `pack_message`

[Исходник](../../agent/context_builder.py#L34)

```python
def pack_message(pack)
```

Добавляет внутренние anchors для host guard, которые удаляются при подготовке HTTP payload.

### `source_proposal`

[Исходник](../../agent/context_builder.py#L39)

```python
def source_proposal(base_url, api_protocol, params)
```

Фиксирует конкретный endpoint, модель, диапазоны, hashes и точный текст для одного подтверждения; API key сюда не входит.

### `pack_summary`

[Исходник](../../agent/context_builder.py#L46)

```python
def pack_summary(messages, status='selected')
```

Возвращает только метаданные источников для task UI; тела исходников не сохраняются в canonical history.

### `visible_summary`

[Исходник](../../agent/context_builder.py#L55)

```python
def visible_summary(summary, root)
```

Повторно фильтрует исторические пути при загрузке задачи после изменения прав доступа.

### `trim_pack`

[Исходник](../../agent/context_builder.py#L65)

```python
def trim_pack(messages)
```

Убирает один optional source целиком; не режет пользовательский запрос или JSON посередине.

### `validate_context`

[Исходник](../../agent/context_builder.py#L79)

```python
def validate_context(messages, root, check_cancelled=lambda: None, cancelled=None)
```

Перед каждой HTTP попыткой проверяет trusted root, права, ignore policy и SHA полного файла; изменившееся исключается.

### `ContextBuilder`

[Исходник](../../agent/context_builder.py#L108)

```python
class ContextBuilder
```

Ограниченный retrieval без дополнительной LLM: явные файлы, определения/упоминания, недавние эффекты и имена тестов.

### `ContextBuilder.__init__`

[Исходник](../../agent/context_builder.py#L110)

```python
def __init__(self, root, interrupted=None)
```

Инициализирует состояние экземпляра ContextBuilder; параметры показаны в сигнатуре, назначение описано у класса.

### `ContextBuilder.check`

[Исходник](../../agent/context_builder.py#L117)

```python
def check(self)
```

Проверяет общую отмену перед очередной read/query операцией.

### `ContextBuilder.build`

[Исходник](../../agent/context_builder.py#L121)

```python
def build(self, prompt, messages, task=None)
```

Ранжирует и дедуплицирует saved-file ranges; повторно прочитанное содержимое в видимых tool receipts не дублируется.

### `ContextBuilder.build.add`

[Исходник](../../agent/context_builder.py#L124)

```python
def add(path, line, reason, kind='range', end=None)
```

Объединяет одинаковые path/line candidates с приоритетом причины первого попадания.

### `ContextBuilder.project`

[Исходник](../../agent/context_builder.py#L190)

```python
def project(self, params, prompt, task=None)
```

Создаёт временную копию model request с data envelope перед последним user message; история не изменяется.

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

Добавляет stable source markers, task/skills и причину сжатия к независимой проекции; исходная каноническая история не меняется.

<a id="module-agent-context-tools-py"></a>

## `agent/context_tools.py`

Безопасное чтение диапазонов сохранённых результатов и поиск включённых MCP без исполнения внешних действий.

### `find_mcp_tools`

[Исходник](../../agent/context_tools.py#L23)

```python
def find_mcp_tools(catalog, query, limit=4)
```

Ищет по коротким ключевым словам в разрешённом snapshot MCP и возвращает ограниченные aliases без исполнения.

### `read_saved_result`

[Исходник](../../agent/context_tools.py#L34)

```python
def read_saved_result(history, args)
```

Проверяет индекс и call ID только в текущем чате; возвращает диапазон символов, hash и next_offset без повторного запуска исходного действия.

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

Сохраняет результаты частичной пачки, дополняет отсутствующие явным OUTCOME_UNKNOWN; исключает осиротевшие и некорректные обмены из проекции.

### `compact_live_messages`

[Исходник](../../agent/conversation.py#L129)

```python
def compact_live_messages(messages, max_chars=80000, keep_recent_rounds=10, request_index=None)
```

Сокращает текущий модельный контекст, группируя assistant tool calls и их результаты.

### `compact_live_messages.flatten`

[Исходник](../../agent/conversation.py#L151)

```python
def flatten()
```

Собирает system-сообщение и группы сообщений в плоский список.

### `compact_live_messages.size`

[Исходник](../../agent/conversation.py#L154)

```python
def size()
```

Измеряет точную длину сериализованного JSON текущего модельного контекста.

<a id="module-agent-delegation-py"></a>

## `agent/delegation.py`

Единственное определение delegate_task для передачи сложной задачи от Лолы основной модели.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-agent-diagnostics-evidence-py"></a>

## `agent/diagnostics_evidence.py`

LSP как проверяемое свидетельство: user check, сохранённые файлы, настройки сервера, approval и строгая полнота результата.

### `config_digest`

[Исходник](../../agent/diagnostics_evidence.py#L12)

```python
def config_digest(settings)
```

Привязывает LSP evidence к enabled/program/argv/language/timeout серверного профиля.

### `run_diagnostics`

[Исходник](../../agent/diagnostics_evidence.py#L17)

```python
def run_diagnostics(root, task, args, settings, operation, approve)
```

Показывает точный сервер и файл, получает approval, выполняет существующий LSP клиент и сохраняет source witnesses.

### `assess_diagnostics`

[Исходник](../../agent/diagnostics_evidence.py#L43)

```python
def assess_diagnostics(task, entry)
```

Проверяет check/config/rollback/доступ/хеши; incomplete push или реальные ошибки не становятся clean evidence.

### `assess_diagnostics.verdict`

[Исходник](../../agent/diagnostics_evidence.py#L47)

```python
def verdict(status, summary)
```

Возвращает typed оценку с явной файловой областью, без подтверждения всего проекта.

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

[Исходник](../../agent/engine.py#L54)

```python
class EventHook
```

Синхронный набор callbacks для независимых от GUI событий движка.

### `EventHook.__init__`

[Исходник](../../agent/engine.py#L56)

```python
def __init__(self)
```

Инициализирует состояние экземпляра EventHook; параметры показаны в сигнатуре, назначение описано у класса.

### `EventHook.connect`

[Исходник](../../agent/engine.py#L59)

```python
def connect(self, callback)
```

Добавляет обработчик события.

### `EventHook.emit`

[Исходник](../../agent/engine.py#L62)

```python
def emit(self, *args)
```

Вызывает копию списка обработчиков с переданными аргументами в текущем потоке.

### `AgentEngine`

[Исходник](../../agent/engine.py#L67)

```python
class AgentEngine
```

Состояние и исполнение одного запуска модели с tools, approval, лимитами, памятью и checkpoint.

### `AgentEngine.requestInterruption`

[Исходник](../../agent/engine.py#L72)

```python
def requestInterruption(self)
```

Выставляет Event остановки и отменяет активные сетевые future клиента.

### `AgentEngine.isInterruptionRequested`

[Исходник](../../agent/engine.py#L77)

```python
def isInterruptionRequested(self)
```

Возвращает текущее состояние флага остановки.

### `AgentEngine.__init__`

[Исходник](../../agent/engine.py#L80)

```python
def __init__(self, base_url, api_key, model, project_root, prompt, force_tool=None, settings=None, history=None, memory=None, auto_memory=True, task_id=None, allow_tools=True, companion=False, tool_protocol='native', persona='', tool_definitions=None, tool_handler=None, context_note='', managed_extensions=False, api_protocol='chat', approval_tools=(), deferred_tools=None, task_options=None, operation=None, context_builder=None, source_approval=None)
```

Инициализирует состояние экземпляра AgentEngine; параметры показаны в сигнатуре, назначение описано у класса.

### `AgentEngine._dispatch_tool`

[Исходник](../../agent/engine.py#L168)

```python
def _dispatch_tool(self, name, args)
```

Обрабатывает readers/discovery локально, подключает выбранные MCP schemas к следующему ходу и делегирует остальные tools прежнему handler.

### `AgentEngine._instruction_guard`

[Исходник](../../agent/engine.py#L199)

```python
def _instruction_guard(self, args)
```

Перед предложением и после согласия проверяет актуальность scoped правил; новые правила требуют следующего модельного запроса до эффекта.

### `AgentEngine._sync_usage`

[Исходник](../../agent/engine.py#L211)

```python
def _sync_usage(self, client)
```

Копирует агрегированный reported usage и число принятых модельных запросов в task без включения секретов.

### `AgentEngine._model_create`

[Исходник](../../agent/engine.py#L222)

```python
def _model_create(self, client, request_purpose='agent', **params)
```

Проверяет полный адаптированный payload до client.create, сохраняет основной/вспомогательный бюджет и синхронизирует usage.

### `AgentEngine._should_update_memory`

[Исходник](../../agent/engine.py#L273)

```python
def _should_update_memory(self)
```

По умолчанию пропускает дополнительную LLM-память после read-only работы; учитывает успешную запись, просьбу запомнить и явный режим off/always.

### `AgentEngine._recover_execution`

[Исходник](../../agent/engine.py#L280)

```python
def _recover_execution(self, messages)
```

Сверяет историю без временного system prefix с журналом перед моделью и при завершении/ошибке.

### `AgentEngine._expire_runtime`

[Исходник](../../agent/engine.py#L287)

```python
def _expire_runtime(self)
```

Отмечает истечение общего срока и запускает существующий путь отмены HTTP, tools и ожидания подтверждения.

### `AgentEngine._check_runtime_deadline`

[Исходник](../../agent/engine.py#L291)

```python
def _check_runtime_deadline(self)
```

Проверяет общий deadline с учётом ожидания человека; переносит watchdog, пока разрешение ожидается.

### `AgentEngine.interruption_reason`

[Исходник](../../agent/engine.py#L303)

```python
def interruption_reason(self)
```

Различает сообщение об истечении срока задачи и об остановке пользователем.

### `AgentEngine._checkpoint`

[Исходник](../../agent/engine.py#L307)

```python
def _checkpoint(self, stage=None, event='')
```

Обновляет этап/последнее событие, сохраняет checkpoint и публикует снимок.

### `AgentEngine.task_snapshot`

[Исходник](../../agent/engine.py#L321)

```python
def task_snapshot(self)
```

Возвращает независимую копию checkpoint для атомарного сохранения в записи чата.

### `AgentEngine.resolve_write_approval`

[Исходник](../../agent/engine.py#L324)

```python
def resolve_write_approval(self, decision)
```

Принимает решение и освобождает ожидание записи; неизвестное решение превращает в reject.

### `AgentEngine._ask_write_approval`

[Исходник](../../agent/engine.py#L335)

```python
def _ask_write_approval(self, path, diff, exists)
```

Запрашивает согласие через событие и ждёт apply/reject/cancel с проверкой остановки.

### `AgentEngine._emit_change`

[Исходник](../../agent/engine.py#L360)

```python
def _emit_change(self, path, diff, exists, status, error='')
```

Публикует path/diff/status одного предложения изменения.

### `AgentEngine._looks_like_action_request`

[Исходник](../../agent/engine.py#L370)

```python
@staticmethod
def _looks_like_action_request(prompt)
```

Эвристически распознаёт просьбу действия по русским/английским словам.

### `AgentEngine._verify_task_completion`

[Исходник](../../agent/engine.py#L380)

```python
def _verify_task_completion(self, client, messages, max_tokens)
```

Дополнительным модельным запросом проверяет, не является ли финал только планом; при ошибке проверки разрешает завершение.

### `AgentEngine.run`

[Исходник](../../agent/engine.py#L417)

```python
def run(self)
```

Строит контекст, выполняет потоковые ходы и tools, обрабатывает остановку, сохраняет состояние и закрывает клиент.

### `AgentEngine._verification_feedback`

[Исходник](../../agent/engine.py#L940)

```python
def _verification_feedback(self, reason)
```

Формирует компактные факты проверок и незакрытых шагов для продолжения существующего цикла.

### `AgentEngine._run_configured_checks`

[Исходник](../../agent/engine.py#L948)

```python
def _run_configured_checks(self, messages, force=False)
```

Запускает только пользовательские commands через прежние ToolExecutor/journal/policy/approval; не добавляет отключённое расширение и не вызывает модель для checks_only.

<a id="module-agent-git-checkpoints-py"></a>

## `agent/git_checkpoints.py`

Приватный bare Git архив before/after подтверждённых snapshots; не меняет индекс, ветку, hooks и файлы проекта.

### `GitCheckpoints`

[Исходник](../../agent/git_checkpoints.py#L15)

```python
class GitCheckpoints
```

Хранит неизменяемые версии подтверждённых правок в отдельном Git Neutral, не подменяя конфликтный rollback.

### `GitCheckpoints.__init__`

[Исходник](../../agent/git_checkpoints.py#L17)

```python
def __init__(self, store)
```

Выбирает отдельный per-project каталог профиля и private bare repository.

### `GitCheckpoints.info`

[Исходник](../../agent/git_checkpoints.py#L24)

```python
def info(self, group_id)
```

Читает bounded метаданные только своего snapshot group и repository для UI после restart.

### `GitCheckpoints.create`

[Исходник](../../agent/git_checkpoints.py#L35)

```python
def create(self, group_id, context)
```

Экспортирует проверенные before/after bytes и manifest, создаёт private tree/commit/ref; не читает индекс пользователя.

### `GitCheckpoints.create.git`

[Исходник](../../agent/git_checkpoints.py#L46)

```python
def git(args)
```

Выполняет только заданные Git plumbing команды с отключёнными hooks/global config и ограниченным временем/выводом.

<a id="module-agent-inference-scheduler-py"></a>

## `agent/inference_scheduler.py`

Общая FIFO очередь физической генерации, cancellable tickets и reservations/usage для SDK, probe и readonly research.

### `InferenceScheduler`

[Исходник](../../agent/inference_scheduler.py#L10)

```python
class InferenceScheduler
```

Общая для процесса FIFO очередь одного тяжёлого inference; моделью и VRAM внешнего сервера не управляет.

### `InferenceScheduler.__init__`

[Исходник](../../agent/inference_scheduler.py#L12)

```python
def __init__(self)
```

Инициализирует состояние экземпляра InferenceScheduler; параметры показаны в сигнатуре, назначение описано у класса.

### `InferenceScheduler.acquire`

[Исходник](../../agent/inference_scheduler.py#L15)

```python
async def acquire(self, context, run_id='', purpose='agent')
```

Ждёт без владения ресурсом; cancellation удаляет точный ticket, сохраняя порядок остальных.

### `InferenceScheduler.release`

[Исходник](../../agent/inference_scheduler.py#L32)

```python
def release(self, ticket)
```

Освобождает только точный ticket-owner; запоздалое завершение не снимает следующего владельца.

### `InferenceScheduler.quarantine`

[Исходник](../../agent/inference_scheduler.py#L38)

```python
def quarantine(self, ticket)
```

После ошибки SDK close блокирует повторное использование exact ticket до подтверждённого закрытия его HTTP клиента; новый waiter получает объяснимую ошибку.

### `InferenceScheduler.status`

[Исходник](../../agent/inference_scheduler.py#L43)

```python
def status(self)
```

Метаданные busy/owner/waiting без prompt, секретов и предположений о резидентных моделях.

### `validate_model`

[Исходник](../../agent/inference_scheduler.py#L52)

```python
def validate_model(context, base_url, model, api_protocol='chat')
```

Единый контракт model/connection/API protocol для SDK, probe и raw research; дрейф binding требует нового run.

### `InferenceAttempt`

[Исходник](../../agent/inference_scheduler.py#L59)

```python
class InferenceAttempt
```

Одна reservation/SDK attempt: физический POST учитывается только transport hook, usage остаётся optional.

### `InferenceAttempt.__init__`

[Исходник](../../agent/inference_scheduler.py#L61)

```python
def __init__(self, context, purpose, reservation=None, scheduler=None)
```

Инициализирует состояние экземпляра InferenceAttempt; параметры показаны в сигнатуре, назначение описано у класса.

### `InferenceAttempt.acquire`

[Исходник](../../agent/inference_scheduler.py#L66)

```python
async def acquire(self)
```

Сохраняет reservation, ждёт FIFO ticket и записывает queue time; отменённое ожидание снимает резерв.

### `InferenceAttempt.on_http`

[Исходник](../../agent/inference_scheduler.py#L77)

```python
async def on_http(self, request)
```

HTTPX hook учитывает только POST chat/completions или responses, включая retries и repair.

### `InferenceAttempt.observe`

[Исходник](../../agent/inference_scheduler.py#L83)

```python
def observe(self, usage=None, terminal=None)
```

Запоминает последний cumulative usage кадр и terminal reason; не суммирует повторные кадры потока.

### `InferenceAttempt.finish`

[Исходник](../../agent/inference_scheduler.py#L89)

```python
def finish(self, state='finished', outcome=None, release=True)
```

Сохраняет terminal telemetry и в finally освобождает ticket после cleanup; missing usage не становится нулевой стоимостью.

### `scheduled_request`

[Исходник](../../agent/inference_scheduler.py#L103)

```python
@asynccontextmanager
async def scheduled_request(context, purpose, reservation=None)
```

Общий async context manager для raw probe/research с той же очередью и журналом попыток.

<a id="module-agent-json-tools-py"></a>

## `agent/json_tools.py`

Текстовый JSON tool protocol: преобразование истории, строгий parser envelope и адаптация stream к обычному executor.

### `strict_json_loads`

[Исходник](../../agent/json_tools.py#L9)

```python
def strict_json_loads(text)
```

Разбирает весь JSON, запрещает повторные ключи и NaN/Infinity на всех уровнях.

### `strict_json_loads.pairs`

[Исходник](../../agent/json_tools.py#L11)

```python
def pairs(items)
```

Собирает объект и отклоняет повторный ключ вместо молчаливой замены аргумента.

### `strict_json_loads.constant`

[Исходник](../../agent/json_tools.py#L18)

```python
def constant(_value)
```

Отклоняет нестандартные числовые константы JSON.

### `decode_envelope`

[Исходник](../../agent/json_tools.py#L23)

```python
def decode_envelope(content)
```

Принимает только anchored объект с явными совместимыми wrappers; не извлекает команды из пояснений.

### `prepare_json_request`

[Исходник](../../agent/json_tools.py#L38)

```python
def prepare_json_request(params)
```

Убирает native tools/tool_choice, добавляет JSON-схемы в system prompt и переводит tool history в обычные сообщения.

### `parse_tool_json`

[Исходник](../../agent/json_tools.py#L105)

```python
def parse_tool_json(content, allowed)
```

Проверяет весь envelope и allowlist; принимает строгий neutral.action.v1 и прежние полные envelopes, отвергает хвост/второй объект/повторные ключи.

### `JsonToolStream`

[Исходник](../../agent/json_tools.py#L135)

```python
class JsonToolStream
```

Ограниченный буфер JSON-ответа поверх отменяемого native stream; возвращает существующему движку знакомую форму delta.tool_calls.

### `JsonToolStream.__init__`

[Исходник](../../agent/json_tools.py#L137)

```python
def __init__(self, source, allowed, choice, repair=None, canonical=False)
```

Инициализирует состояние экземпляра JsonToolStream; параметры показаны в сигнатуре, назначение описано у класса.

### `JsonToolStream.__iter__`

[Исходник](../../agent/json_tools.py#L141)

```python
def __iter__(self)
```

Собирает до 1 МБ текста, проверяет обязательность/запрет вызова и создаёт native-shaped delta с UUID каждого вызова.

### `JsonToolStream._read_response`

[Исходник](../../agent/json_tools.py#L171)

```python
def _read_response(self)
```

Буферизует один bounded ответ до явного terminal outcome; EOF/length/refusal не входят в protocol repair.

### `JsonToolStream.close`

[Исходник](../../agent/json_tools.py#L187)

```python
def close(self)
```

Закрывает исходный HTTP stream и освобождает отменяемый запрос.

<a id="module-agent-language-diagnostics-py"></a>

## `agent/language_diagnostics.py`

Настоящий stdio LSP initialize/didOpen/publishDiagnostics; отказ server edits/commands, bounded framing и завершение процесса.

### `read_frame`

[Исходник](../../agent/language_diagnostics.py#L15)

```python
def read_frame(stream)
```

Читает Content-Length JSON-RPC с пределами 8КБ заголовка/1МБ тела; неполный frame отклоняется.

### `write_frame`

[Исходник](../../agent/language_diagnostics.py#L31)

```python
def write_frame(stream, value)
```

Кодирует JSON-RPC UTF-8 и длину в байтах, flush выполняется worker-писателем.

### `normalize_diagnostics`

[Исходник](../../agent/language_diagnostics.py#L36)

```python
def normalize_diagnostics(values)
```

Проверяет структуру/позиции; неверный payload не превращается в пустой отчёт без ошибок.

### `diagnose`

[Исходник](../../agent/language_diagnostics.py#L52)

```python
def diagnose(root, path, settings, context)
```

Ограниченная сессия настоящего LSP для сохранённого файла; чужие URI/версии игнорируются, server requests отклоняются, результат помечается stale при изменении файла.

### `diagnose.read`

[Исходник](../../agent/language_diagnostics.py#L68)

```python
def read()
```

Читает bounded frames в ограниченную очередь, сообщает о закрытии транспорта без блокировки bridge.

### `diagnose.write`

[Исходник](../../agent/language_diagnostics.py#L74)

```python
def write()
```

Единственный владелец stdin; потенциально зависшая запись прерывается уничтожением процесса по deadline.

### `diagnose.send`

[Исходник](../../agent/language_diagnostics.py#L81)

```python
def send(value)
```

Ставит JSON-RPC в очередь без блокировки, переполнение явно отклоняет.

<a id="module-agent-managed-worktrees-py"></a>

## `agent/managed_worktrees.py`

Пользовательские Git worktrees из HEAD, receipts владения, список/diff/open и удаление только неизменённой копии.

### `git_path`

[Исходник](../../agent/managed_worktrees.py#L15)

```python
def git_path()
```

Находит установленный Git через LCA_GIT или PATH; не устанавливает зависимости.

### `ManagedWorktrees`

[Исходник](../../agent/managed_worktrees.py#L21)

```python
class ManagedWorktrees
```

Управляет только созданными приложением checkout receipts; основной репозиторий и commits не удаляет.

### `ManagedWorktrees.__init__`

[Исходник](../../agent/managed_worktrees.py#L22)

```python
def __init__(self, directory)
```

Инициализирует состояние экземпляра ManagedWorktrees; параметры показаны в сигнатуре, назначение описано у класса.

### `ManagedWorktrees._records`

[Исходник](../../agent/managed_worktrees.py#L25)

```python
def _records(self)
```

Читает JSON реестр владения либо возвращает пустой список; повреждение не замалчивается.

### `ManagedWorktrees._git`

[Исходник](../../agent/managed_worktrees.py#L31)

```python
def _git(self, root, args, context)
```

Запускает bounded Git без hooks/fsmonitor/submodule recursion и prompt, с Windows longpaths; ошибка/обрезка требуют проверки.

### `ManagedWorktrees.repository`

[Исходник](../../agent/managed_worktrees.py#L39)

```python
def repository(self, root, context)
```

Требует выбранный Git top-level; для управляемой копии сверяет common-dir и находит исходного владельца.

### `ManagedWorktrees.list`

[Исходник](../../agent/managed_worktrees.py#L51)

```python
def list(self, root, context)
```

Сопоставляет scoped receipts с реальной porcelain -z регистрацией Git.

### `ManagedWorktrees._target`

[Исходник](../../agent/managed_worktrees.py#L61)

```python
def _target(self, row)
```

Проверяет UUID, конечное имя и containment пути внутри каталога управляемых копий.

### `ManagedWorktrees.create`

[Исходник](../../agent/managed_worktrees.py#L67)

```python
def create(self, root, label, context)
```

Сохраняет creating receipt до detached checkout из исходного HEAD; незавершённый effect помечает needs_review и не повторяет.

### `ManagedWorktrees.get`

[Исходник](../../agent/managed_worktrees.py#L85)

```python
def get(self, root, identity, context)
```

Требует owned ID выбранного репозитория, регистрацию и одинаковый git-common-dir, защищает от подменённого пути.

### `ManagedWorktrees.diff`

[Исходник](../../agent/managed_worktrees.py#L97)

```python
def diff(self, root, identity, context)
```

Возвращает bounded status и diff HEAD без external diff/textconv; новые файлы видны в status.

### `ManagedWorktrees.remove`

[Исходник](../../agent/managed_worktrees.py#L103)

```python
def remove(self, root, identity, context)
```

Не удаляет открытую/грязную копию, ignored/untracked файлы и новые commits; вызывает native Git remove без force только после проверок.

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

<a id="module-agent-mcp-client-py"></a>

## `agent/mcp_client.py`

SDK-адаптер MCP поверх session pool; нормализация bounded/untrusted результатов без раскрытия токенов.

### `validate_server`

[Исходник](../../agent/mcp_client.py#L12)

```python
def validate_server(value)
```

Проверяет ID, transport, URL или command/args и возвращает только разрешённые публичные поля.

### `MCPClient`

[Исходник](../../agent/mcp_client.py#L34)

```python
class MCPClient
```

Исполнитель короткоживущих MCP соединений; токен передаётся отдельно от публичных настроек.

### `MCPClient.__init__`

[Исходник](../../agent/mcp_client.py#L35)

```python
def __init__(self, log_dir)
```

Инициализирует состояние экземпляра MCPClient; параметры показаны в сигнатуре, назначение описано у класса.

### `MCPClient.operation`

[Исходник](../../agent/mcp_client.py#L40)

```python
def operation(self, server, name=None, arguments=None, interrupted=None, token='')
```

Запускает coroutine из синхронного диспетчера и превращает ошибки соединения в ограниченный результат.

### `MCPClient._connect`

[Исходник](../../agent/mcp_client.py#L45)

```python
@asynccontextmanager
async def _connect(self, server, token)
```

SDK stdio/HTTP контекст с ограниченным логом, без redirect/credential forwarding; принадлежит actor task.

### `MCPClient._exchange`

[Исходник](../../agent/mcp_client.py#L64)

```python
async def _exchange(self, client, name, arguments)
```

Получает catalog либо tool result; ограничивает тексты и заменяет media base64 метаданными.

### `MCPClient.shutdown`

[Исходник](../../agent/mcp_client.py#L85)

```python
def shutdown(self)
```

Закрывает принадлежащий адаптеру session pool.

<a id="module-agent-mcp-sessions-py"></a>

## `agent/mcp_sessions.py`

Ограниченный пул MCP actors: connect/use/exit в одной asyncio task, TTL, отмена, invalidation и shutdown без повтора effects.

### `MCPSessionPool`

[Исходник](../../agent/mcp_sessions.py#L9)

```python
class MCPSessionPool
```

Ленивый asyncio-loop и до четырёх endpoint/credential actors с idle TTL 45 секунд.

### `MCPSessionPool.__init__`

[Исходник](../../agent/mcp_sessions.py#L10)

```python
def __init__(self, connect, exchange, *, idle_seconds=45, max_sessions=4)
```

Инициализирует состояние экземпляра MCPSessionPool; параметры показаны в сигнатуре, назначение описано у класса.

### `MCPSessionPool._start`

[Исходник](../../agent/mcp_sessions.py#L15)

```python
def _start(self)
```

Запускает loop thread один раз; закрытый manager повторно не оживает.

### `MCPSessionPool.operation`

[Исходник](../../agent/mcp_sessions.py#L23)

```python
def operation(self, server, name, args, cancelled, token)
```

Хеширует только connection identity и token, передаёт parent cancellation, ограничивает синхронное ожидание без автоматического повтора.

### `MCPSessionPool._submit`

[Исходник](../../agent/mcp_sessions.py#L34)

```python
async def _submit(self, key, server, name, args, context, token)
```

Ставит запрос в actor queue и наблюдает отмену даже во время connect; просроченная очередь не исполняется позднее.

### `MCPSessionPool._actor`

[Исходник](../../agent/mcp_sessions.py#L53)

```python
async def _actor(self, key, actor, server, token)
```

В одной task открывает транспорт/Client, последовательно выполняет вызовы и закрывает контекст при idle/cancel/error.

### `MCPSessionPool._failure`

[Исходник](../../agent/mcp_sessions.py#L89)

```python
@staticmethod
def _failure(name, error)
```

Возвращает conservative unknown для tool effects и MCP_ERROR для discovery без исходных credentials.

### `MCPSessionPool.invalidate`

[Исходник](../../agent/mcp_sessions.py#L92)

```python
def invalidate(self, identity=None)
```

Прерывает выбранные endpoint actors при смене настроек/токена или выключении; не повторяет запросы.

### `MCPSessionPool.status`

[Исходник](../../agent/mcp_sessions.py#L99)

```python
def status(self)
```

Показывает количество сессий, IDs и число операций без endpoint URL и токенов.

### `MCPSessionPool.shutdown`

[Исходник](../../agent/mcp_sessions.py#L103)

```python
def shutdown(self)
```

Останавливает actors и loop, закрывает transport contexts и ждёт завершения thread ограниченное время.

### `MCPSessionPool._close`

[Исходник](../../agent/mcp_sessions.py#L116)

```python
async def _close(self)
```

Собирает закрытие actor tasks на их общем event loop.

<a id="module-agent-model-client-py"></a>

## `agent/model_client.py`

Отменяемый async HTTP-клиент с синхронной поверхностью для движка.

### `ModelCancelled`

[Исходник](../../agent/model_client.py#L12)

```python
class ModelCancelled(Exception)
```

Внутреннее исключение отмены модельного запроса, обрабатываемое движком.

### `SourceContextApprovalError`

[Исходник](../../agent/model_client.py#L16)

```python
class SourceContextApprovalError(ValueError)
```

Обратимая пауза, когда передача исходников отклонена или согласованный пакет изменился; не означает успешного HTTP.

### `ScheduledStream`

[Исходник](../../agent/model_client.py#L20)

```python
class ScheduledStream
```

Обёртка SDK AsyncStream: resource lease живёт до завершения фактического close, включая ошибку и отмену.

### `ScheduledStream.__init__`

[Исходник](../../agent/model_client.py#L22)

```python
def __init__(self, source, attempt)
```

Инициализирует состояние экземпляра ScheduledStream; параметры показаны в сигнатуре, назначение описано у класса.

### `ScheduledStream.__aenter__`

[Исходник](../../agent/model_client.py#L25)

```python
async def __aenter__(self)
```

Открывает SDK stream, при ошибке закрывает ресурс и telemetry до проброса исключения.

### `ScheduledStream.__aiter__`

[Исходник](../../agent/model_client.py#L31)

```python
def __aiter__(self)
```

Передаёт исходные SDK chunks существующему Responses/native адаптеру без изменения содержимого.

### `ScheduledStream.__aexit__`

[Исходник](../../agent/model_client.py#L34)

```python
async def __aexit__(self, kind, error, traceback)
```

Закрывает SDK ответ и завершает попытку при выходе из async with.

### `ScheduledStream.close`

[Исходник](../../agent/model_client.py#L37)

```python
async def close(self, error=None)
```

Shield cleanup против повторного Stop; queue не получает lease до окончания close; ошибка не скрывается.

### `ModelStream`

[Исходник](../../agent/model_client.py#L55)

```python
class ModelStream
```

Синхронный итератор над async SSE-producer с ограниченной очередью.

### `ModelStream.__init__`

[Исходник](../../agent/model_client.py#L56)

```python
def __init__(self, owner, params, original=None, purpose=None)
```

Инициализирует состояние экземпляра ModelStream; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelStream._produce`

[Исходник](../../agent/model_client.py#L62)

```python
async def _produce(self, params, original=None)
```

Читает настоящий HTTP-поток в ограниченную очередь, переводит Responses и учитывает последнее накопительное usage один раз; закрывает транспорт при отмене.

### `ModelStream.__iter__`

[Исходник](../../agent/model_client.py#L88)

```python
def __iter__(self)
```

Возвращает сам поток как Python-итератор.

### `ModelStream.__next__`

[Исходник](../../agent/model_client.py#L91)

```python
def __next__(self)
```

Ожидает очередной чанк короткими интервалами, проверяет отмену и завершение future.

### `ModelStream.close`

[Исходник](../../agent/model_client.py#L101)

```python
def close(self)
```

Отменяет future producer, закрывая незавершённый поток.

### `ModelClient`

[Исходник](../../agent/model_client.py#L105)

```python
class ModelClient
```

Async SDK в отдельном loop-потоке с синхронными create/result и отменой.

### `ModelClient.__init__`

[Исходник](../../agent/model_client.py#L106)

```python
def __init__(self, base_url, api_key, interrupted, timeout=180, tool_protocol='native', api_protocol='chat')
```

Инициализирует состояние экземпляра ModelClient; параметры показаны в сигнатуре, назначение описано у класса.

### `ModelClient.check_cancelled`

[Исходник](../../agent/model_client.py#L133)

```python
def check_cancelled(self)
```

Выбрасывает ModelCancelled, если общий Event установлен.

### `ModelClient._http_attempt`

[Исходник](../../agent/model_client.py#L137)

```python
async def _http_attempt(self, request)
```

Независимо от логического create считает физический inference POST в активной attempt.

### `ModelClient.prepare_budget`

[Исходник](../../agent/model_client.py#L141)

```python
def prepare_budget(self, settings, model, budget)
```

Разрешает окно до запроса и после JIT-загрузки; подключает tokenizer без загрузки или изменения GPU-параметров.

### `ModelClient.submit`

[Исходник](../../agent/model_client.py#L157)

```python
def submit(self, coroutine)
```

Планирует корутину в сетевом loop и учитывает её future в pending.

### `ModelClient._tracked`

[Исходник](../../agent/model_client.py#L166)

```python
async def _tracked(self, coroutine)
```

Отделяет корневые request workers от SDK cleanup tasks; shutdown не отменяет cleanup повторно.

### `ModelClient._forget`

[Исходник](../../agent/model_client.py#L172)

```python
def _forget(self, future)
```

Убирает завершённую future из защищённого множества.

### `ModelClient.result`

[Исходник](../../agent/model_client.py#L176)

```python
def result(self, future)
```

Ждёт результат короткими интервалами и переводит cancellation в исключение движка.

### `ModelClient.create`

[Исходник](../../agent/model_client.py#L186)

```python
def create(self, **params)
```

Применяет общий wire adapter и окончательный бюджет до HTTP; запускает native/JSON/Responses stream либо нестриминговое завершение с учётом usage.

### `ModelClient.create.complete`

[Исходник](../../agent/model_client.py#L207)

```python
async def complete()
```

Выбирает нестриминговый Chat Completions или Responses и приводит результат к ожидаемому интерфейсу choices.

### `ModelClient._repair_json`

[Исходник](../../agent/model_client.py#L218)

```python
def _repair_json(self, original, rejected, error, attempt)
```

Повторно генерирует отклонённый, неисполненный ответ через fit/check и Stop; учитывает запрос и repair без изменения canonical history.

### `ModelClient.record_usage`

[Исходник](../../agent/model_client.py#L234)

```python
def record_usage(self, usage)
```

Принимает только корректные неотрицательные input/output usage сервера; факт расхода хранится отдельно от оценки бюджета.

### `ModelClient.request`

[Исходник](../../agent/model_client.py#L245)

```python
async def request(self, endpoint, params, original=None, purpose=None)
```

Повторяет временные ошибки только до ответа; при явном 400/422 для stream_options допускает fallback без необязательной telemetry, не повторяет частичный поток.

### `ModelClient.cancel`

[Исходник](../../agent/model_client.py#L343)

```python
def cancel(self)
```

Отменяет снимок всех активных future.

### `ModelClient.close`

[Исходник](../../agent/model_client.py#L349)

```python
def close(self)
```

Отменяет async-задачи, закрывает SDK и останавливает сетевой поток/loop.

### `ModelClient.close.shutdown`

[Исходник](../../agent/model_client.py#L354)

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

[Исходник](../../agent/model_preferences.py#L26)

```python
def validate_settings(settings)
```

Проверяет конечность, тип, целочисленность и диапазон каждого разрешённого параметра; неизвестные поля не сохраняет.

### `validate_preferences`

[Исходник](../../agent/model_preferences.py#L53)

```python
def validate_preferences(params)
```

Разрешает HTTP(S) endpoint без credentials/query/fragment, проверяет порт и возвращает URL/ID и whitelist settings без ключа.

### `connection_key`

[Исходник](../../agent/model_preferences.py#L70)

```python
def connection_key(previous, public, params, key='api_key', endpoint='base_url')
```

Привязывает ключ к адресу сервиса: прежний либо явно повторённый старый ключ не переносится на новый endpoint.

### `load_preferences`

[Исходник](../../agent/model_preferences.py#L80)

```python
def load_preferences()
```

Читает и проверяет JSON; при ошибке возвращает копию defaults, никогда не восстанавливает ключ.

### `save_preferences`

[Исходник](../../agent/model_preferences.py#L88)

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
async def _request_probe(config, max_bytes, context=None)
```

Выполняет bounded HTTP POST с коротким prompt, параметрами черновика, заданным бюджетом токенов и проверкой текстового ответа.

### `_probe`

[Исходник](../../agent/model_probe.py#L54)

```python
async def _probe(config, cancelled, timeout, max_bytes)
```

Ограничивает полное время запроса и следит за Event отмены, закрывая обе asyncio-задачи в finally.

### `probe_model`

[Исходник](../../agent/model_probe.py#L70)

```python
def probe_model(config, *, cancelled=None, timeout=30, max_bytes=100000)
```

Проверяет ID, запускает отдельный asyncio loop и возвращает ответ/время без изменения истории или preferences.

<a id="module-agent-operation-context-py"></a>

## `agent/operation_context.py`

Общий deadline/cancel контракт и единый inference gate для задач, probe и последующих необязательных вычислений.

### `OperationContext`

[Исходник](../../agent/operation_context.py#L9)

```python
class OperationContext
```

Event-совместимый deadline/cancel token; дочерняя операция не продлевает срок родителя.

### `OperationContext.__init__`

[Исходник](../../agent/operation_context.py#L10)

```python
def __init__(self, timeout=None, parent=None)
```

Инициализирует состояние экземпляра OperationContext; параметры показаны в сигнатуре, назначение описано у класса.

### `OperationContext.set_deadline`

[Исходник](../../agent/operation_context.py#L15)

```python
def set_deadline(self, timeout)
```

Устанавливает или сокращает локальный monotonic deadline.

### `OperationContext.approval_wait`

[Исходник](../../agent/operation_context.py#L22)

```python
@contextmanager
def approval_wait(self)
```

Приостанавливает deadlines текущей операции и родителей на время разрешения; отмена остаётся немедленной.

### `OperationContext.remaining`

[Исходник](../../agent/operation_context.py#L38)

```python
def remaining(self, default=None)
```

Возвращает минимальный оставшийся срок своего и родительского контекстов.

### `OperationContext.is_set`

[Исходник](../../agent/operation_context.py#L48)

```python
def is_set(self)
```

Отмена активна при set, отмене родителя или истечении deadline.

### `OperationContext.set`

[Исходник](../../agent/operation_context.py#L51)

```python
def set(self)
```

Устанавливает сигнал отмены, не освобождая inference lease до фактического завершения.

### `OperationContext.wait`

[Исходник](../../agent/operation_context.py#L54)

```python
def wait(self, timeout=None)
```

Ожидает отмену/срок короткими ожиданиями, учитывая timeout вызывающего кода.

### `OperationContext.child`

[Исходник](../../agent/operation_context.py#L62)

```python
def child(self, timeout=None)
```

Создаёт дочерний контекст с общим родительским сигналом и собственным пределом.

### `InferenceLease`

[Исходник](../../agent/operation_context.py#L67)

```python
@dataclass
class InferenceLease
```

ID владельца, назначение и cancel context одной тяжёлой операции.

Поля, объявленные в классе:

```python
id: str
kind: str
context: OperationContext
```

### `InferenceGate`

[Исходник](../../agent/operation_context.py#L73)

```python
class InferenceGate
```

Разрешает одну inference, сохраняя владельца до завершения реального worker.

### `InferenceGate.__init__`

[Исходник](../../agent/operation_context.py#L75)

```python
def __init__(self)
```

Инициализирует состояние экземпляра InferenceGate; параметры показаны в сигнатуре, назначение описано у класса.

### `InferenceGate.begin`

[Исходник](../../agent/operation_context.py#L78)

```python
def begin(self, kind, timeout=None)
```

Выдаёт lease либо отклоняет конкурирующий запуск с понятным назначением текущей работы.

### `InferenceGate.end`

[Исходник](../../agent/operation_context.py#L84)

```python
def end(self, identity)
```

Освобождает gate только при совпадении ID; старый task_end не освобождает нового владельца.

### `InferenceGate.cancel`

[Исходник](../../agent/operation_context.py#L88)

```python
def cancel(self)
```

Сигнализирует отмену, не допускает преждевременный параллельный запуск.

### `InferenceGate.status`

[Исходник](../../agent/operation_context.py#L92)

```python
def status(self)
```

Возвращает безопасные busy/kind/limit без ключей и содержимого запросов.

<a id="module-agent-optional-process-py"></a>

## `agent/optional_process.py`

Без-shell subprocess с allowlist окружения, bounded output, общим deadline и закрытием дерева дочерних процессов.

### `process_env`

[Исходник](../../agent/optional_process.py#L10)

```python
def process_env()
```

Передаёт дочерним процессам системное окружение из allowlist без API/Telegram ключей и GIT/Docker overrides.

### `stop_process`

[Исходник](../../agent/optional_process.py#L15)

```python
def stop_process(process, job)
```

Закрывает Windows Job или POSIX process group, убивает оставшийся процесс и ограниченно ждёт exit.

### `run_bounded`

[Исходник](../../agent/optional_process.py#L25)

```python
def run_bounded(command, cwd, context, *, limit=64000, env=None)
```

Запускает argv без shell, ограничивает сохранённый stdout, наблюдает OperationContext и возвращает exit/cancel/elapsed.

### `run_bounded.read`

[Исходник](../../agent/optional_process.py#L34)

```python
def read()
```

Дренирует pipe до EOF, сохраняя не более limit bytes и полный счётчик для truncated.

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

<a id="module-agent-process-identity-py"></a>

## `agent/process_identity.py`

Read-only Windows/Linux process lifetime probe, tri-state uncertainty and PID reuse evidence for orphan telemetry recovery.

### `inspect_process`

[Исходник](../../agent/process_identity.py#L7)

```python
def inspect_process(pid)
```

Возвращает alive/dead/unknown и lifetime token; некорректные PID не приводятся к другому процессу, Windows сигналы не используются.

### `_windows_process`

[Исходник](../../agent/process_identity.py#L18)

```python
def _windows_process(pid)
```

Открывает query-only handle, читает creation FILETIME и exit code одного объекта процесса, гарантированно закрывает handle.

### `_linux_process`

[Исходник](../../agent/process_identity.py#L40)

```python
def _linux_process(pid)
```

Связывает boot ID с /proc start ticks, учитывает сложное comm и zombie; при скрытом /proc не объявляет owner мёртвым без проверки.

### `owner_alive`

[Исходник](../../agent/process_identity.py#L58)

```python
def owner_alive(pid)
```

Совместимая bool-проекция: unknown считается потенциально живым процессом, чтобы не восстанавливать чужой active run.

### `owner_ended`

[Исходник](../../agent/process_identity.py#L63)

```python
def owner_ended(pid, expected_token, inspect=inspect_process)
```

Принимает только доказанную смерть PID или несовпадение сопоставимых creation tokens; legacy/unknown/version mismatch сохраняет owner.

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

<a id="module-agent-progress-guard-py"></a>

## `agent/progress_guard.py`

Окно отпечатков вызовов и результатов для остановки чередующихся циклов без продвижения.

### `ProgressGuard`

[Исходник](../../agent/progress_guard.py#L7)

```python
class ProgressGuard
```

Ограниченное окно SHA256 отпечатков имени, аргументов и результата вызова.

### `ProgressGuard.__init__`

[Исходник](../../agent/progress_guard.py#L8)

```python
def __init__(self, window=16, threshold=4, task=None)
```

Инициализирует состояние экземпляра ProgressGuard; параметры показаны в сигнатуре, назначение описано у класса.

### `ProgressGuard.observe`

[Исходник](../../agent/progress_guard.py#L16)

```python
def observe(self, name, arguments, result)
```

Считает повтор результата/ошибки, игнорируя receipt IDs, timestamps и прочую volatile metadata; сохраняет bounded hashes в checkpoint.

### `ProgressGuard.observe.stable`

[Исходник](../../agent/progress_guard.py#L18)

```python
def stable(value)
```

Рекурсивно удаляет volatile metadata перед fingerprint, сохраняя фактическое содержимое результата.

### `ProgressGuard.recover_or_stop`

[Исходник](../../agent/progress_guard.py#L31)

```python
def recover_or_stop(self)
```

Разрешает ровно одну диагностическую попытку на логическую задачу; повтор после неё требует паузы, счётчик переживает resume.

<a id="module-agent-project-command-py"></a>

## `agent/project_command.py`

Опциональный запуск тестов/сборок после отдельного подтверждения; ограниченный вывод, время и ProcessJob.

### `run_project_command`

[Исходник](../../agent/project_command.py#L15)

```python
def run_project_command(root, args, interrupted, approve)
```

Проверяет cwd/аргументы, требует отдельное подтверждение и запускает программу без shell с deadline и ограниченным выводом.

### `run_project_command.read`

[Исходник](../../agent/project_command.py#L54)

```python
def read()
```

Непрерывно освобождает stdout/stderr pipe, сохраняя не больше 64 КБ и считая объём для признака усечения.

<a id="module-agent-project-index-py"></a>

## `agent/project_index.py`

Отдельный derived SQLite/WAL cache проекта, FTS5, durable queue точных путей, watcher, incremental update и проверенный retrieval.

### `ProjectIndex`

[Исходник](../../agent/project_index.py#L20)

```python
class ProjectIndex
```

Владеет одним derived cache/observer/updater; не использует chat DB и не выполняет исходный код.

### `ProjectIndex.__init__`

[Исходник](../../agent/project_index.py#L22)

```python
def __init__(self, root, *, watch=True)
```

Инициализирует состояние экземпляра ProjectIndex; параметры показаны в сигнатуре, назначение описано у класса.

### `ProjectIndex._claim`

[Исходник](../../agent/project_index.py#L40)

```python
def _claim(self)
```

Берёт OS-released owner lock кеша; второй Core не может молча конкурировать с пересборкой.

### `ProjectIndex.database`

[Исходник](../../agent/project_index.py#L54)

```python
@contextmanager
def database(self)
```

Открывает короткое независимое SQLite WAL соединение с bounded lock wait и Unicode casefold.

### `ProjectIndex._initialize`

[Исходник](../../agent/project_index.py#L63)

```python
def _initialize(self)
```

Создаёт versioned cache schema и optional FTS5 trigram, сохраняя pending paths до recovery scan.

### `ProjectIndex.status`

[Исходник](../../agent/project_index.py#L83)

```python
def status(self)
```

Возвращает state, counters, backend, watcher и approximate cache size без source contents/полного обхода.

### `ProjectIndex._cache_bytes`

[Исходник](../../agent/project_index.py#L91)

```python
def _cache_bytes(self)
```

Считает DB/WAL/SHM и выдерживает исчезновение WAL во время checkpoint.

### `ProjectIndex.rebuild`

[Исходник](../../agent/project_index.py#L99)

```python
def rebuild(self)
```

Планирует контролируемый background scan; по явному запросу архивирует повреждённый owned cache и создаёт новый.

### `ProjectIndex.cancel`

[Исходник](../../agent/project_index.py#L117)

```python
def cancel(self)
```

Останавливает background indexing, сохраняет очередь и не объявляет partial index готовым.

### `ProjectIndex.uncertain`

[Исходник](../../agent/project_index.py#L122)

```python
def uncertain(self, reason, *, purge=False)
```

Помечает потерю достоверности после overflow/policy/error, при необходимости просит удалить derived content.

### `ProjectIndex.enqueue`

[Исходник](../../agent/project_index.py#L126)

```python
def enqueue(self, paths)
```

Durable coalescing exact paths с token, чтобы новое событие не потерялось при обработке старого.

### `ProjectIndex.reconcile_command`

[Исходник](../../agent/project_index.py#L139)

```python
def reconcile_command(self, cwd='.')
```

Добавляет внутреннее событие bounded сверки cwd; evidence scope не считается sandbox программы.

### `ProjectIndex._watch`

[Исходник](../../agent/project_index.py#L146)

```python
def _watch(self)
```

Запускает observer до initial scan, объединяет события, прерывает чтение на смене правил и сигнализирует ошибки/overflow.

### `ProjectIndex._walk`

[Исходник](../../agent/project_index.py#L167)

```python
def _walk(self, policy, start=None, *, limit=100000, seconds=120)
```

Enumerates разрешённые saved files только при initial/recovery либо bounded subtree reconcile, без ссылок/junction.

### `ProjectIndex._read`

[Исходник](../../agent/project_index.py#L184)

```python
def _read(self, relative, policy, *, parse=True)
```

Ограниченно повторяет только чтение при Windows sharing/moving-file race, проверяет отмену между попытками.

### `ProjectIndex._read_once`

[Исходник](../../agent/project_index.py#L200)

```python
def _read_once(self, relative, policy, *, parse=True)
```

Проверяет policy/canonical target, regular file, bounded UTF-8 и stable before/after stat; возвращает hash и syntax symbols.

### `ProjectIndex._apply`

[Исходник](../../agent/project_index.py#L218)

```python
def _apply(self, records, pending=())
```

Применяет маленький batch, пропускает неизменившиеся SHA/policy/parser и потребляет только обработанные pending tokens.

### `ProjectIndex._purge`

[Исходник](../../agent/project_index.py#L243)

```python
def _purge(self)
```

Инвалидирует derived text/symbol/FTS rows при изменении доступа, не трогая чаты, journal или source files.

### `ProjectIndex._build`

[Исходник](../../agent/project_index.py#L250)

```python
def _build(self)
```

Под активным observer делает первичный scan, затем оставляет события периода scan в durable очереди для replay.

### `ProjectIndex._drain`

[Исходник](../../agent/project_index.py#L268)

```python
def _drain(self)
```

Обрабатывает точные edits/rename/delete и bounded directory/command reconciliation без штатного global rescan.

### `ProjectIndex._run`

[Исходник](../../agent/project_index.py#L296)

```python
def _run(self)
```

Единственный updater; переключает building/updating/ready/recovery, не запускает бесконечные автоматические rescan.

### `ProjectIndex.query`

[Исходник](../../agent/project_index.py#L318)

```python
def query(self, params, cancelled=None)
```

Читает bounded candidates в SQLite snapshot, повторно проверяет source hash/access и возвращает ranges с provenance; updating помечается partial.

### `ProjectIndex.close`

[Исходник](../../agent/project_index.py#L388)

```python
def close(self)
```

Останавливает observer/updater и освобождает owner lock; незавершённая очередь остаётся на диске.

### `get_index`

[Исходник](../../agent/project_index.py#L397)

```python
def get_index(root, *, create=False)
```

Находит instance по canonical workspace и profile; create используется только при явном выборе проекта/индексных tools.

### `notify_paths`

[Исходник](../../agent/project_index.py#L406)

```python
def notify_paths(root, paths)
```

Best-effort change feed после уже разрешённого эффекта; отказ кеша не повторяет и не отменяет запись.

### `close_indexes`

[Исходник](../../agent/project_index.py#L414)

```python
def close_indexes()
```

Закрывает instances при переключении проекта и завершении Core, не удаляя sources/cache recursively.

<a id="module-agent-project-index-policy-py"></a>

## `agent/project_index_policy.py`

Per-operation WorkspaceAccessPolicy и ancestor .gitignore с GitWildMatch, nested rules и policy provenance.

### `IndexPolicy`

[Исходник](../../agent/project_index_policy.py#L9)

```python
class IndexPolicy
```

Снимок правил автоматического доступа и .gitignore на одну операцию; новый retrieval создаёт новый экземпляр.

### `IndexPolicy.__init__`

[Исходник](../../agent/project_index_policy.py#L11)

```python
def __init__(self, root)
```

Инициализирует состояние экземпляра IndexPolicy; параметры показаны в сигнатуре, назначение описано у класса.

### `IndexPolicy.rules`

[Исходник](../../agent/project_index_policy.py#L15)

```python
def rules(self, directory)
```

Один раз компилирует bounded UTF-8 .gitignore папки, не читая недоступные правила или symlink.

### `IndexPolicy.permits`

[Исходник](../../agent/project_index_policy.py#L29)

```python
def permits(self, relative, directory=False)
```

Memoize фильтр для конкретного пути только в текущем снимке; это не замена canonical-path проверки при чтении.

### `IndexPolicy._permits`

[Исходник](../../agent/project_index_policy.py#L35)

```python
def _permits(self, relative, directory)
```

Применяет общую file policy, fixed excludes и GitWildMatch ко всем ancestors; запрещённый parent не оживает через child negation.

### `IndexPolicy.anchor_policy`

[Исходник](../../agent/project_index_policy.py#L49)

```python
def anchor_policy(self, relative)
```

Вычисляет hash file-access policy и правил ancestor .gitignore для конкретного результата.

<a id="module-agent-project-instructions-py"></a>

## `agent/project_instructions.py`

Ограниченное чтение AGENTS.md по иерархии выбранного пути; версии/области действия передаются модели и не расширяют права.

### `ProjectInstructions`

[Исходник](../../agent/project_instructions.py#L7)

```python
class ProjectInstructions
```

Хранит применимые scoped AGENTS.md, поколения их обновлений и ограниченный текст правил для system projection.

### `ProjectInstructions.__init__`

[Исходник](../../agent/project_instructions.py#L8)

```python
def __init__(self, root)
```

Инициализирует состояние экземпляра ProjectInstructions; параметры показаны в сигнатуре, назначение описано у класса.

### `ProjectInstructions.refresh`

[Исходник](../../agent/project_instructions.py#L11)

```python
def refresh(self, path='.')
```

Перечитывает цепочку AGENTS.md от корня до папки пути, замечает добавление/удаление/смену hash и проверяет 8/16 КБ лимиты.

### `ProjectInstructions.render`

[Исходник](../../agent/project_instructions.py#L36)

```python
def render(self)
```

Показывает источники, области и полные прочитанные правила с приоритетом пользователя и без дополнительных разрешений.

### `ProjectInstructions.summary`

[Исходник](../../agent/project_instructions.py#L43)

```python
def summary(self)
```

Возвращает только пути, области и hashes для компактного task и интерфейса.

<a id="module-agent-project-knowledge-py"></a>

## `agent/project_knowledge.py`

Память проекта: bounded записи с происхождением, SHA источников, инвалидацией доступа, лексическим/структурным поиском и свежестью перед POST.

### `now`

[Исходник](../../agent/project_knowledge.py#L22)

```python
def now()
```

Даёт UTC timestamp только при создании или изменении записи.

### `ProjectKnowledge`

[Исходник](../../agent/project_knowledge.py#L27)

```python
class ProjectKnowledge
```

Bounded каталог профильной памяти вне проекта; не заменяет канонические чаты и журналы.

### `ProjectKnowledge.__init__`

[Исходник](../../agent/project_knowledge.py#L29)

```python
def __init__(self, root)
```

Привязывает каталог knowledge.json к каноническому корню проекта и существующему профилю памяти.

### `ProjectKnowledge.load`

[Исходник](../../agent/project_knowledge.py#L32)

```python
def load(self)
```

Строго проверяет bounded schema и provenance, не исправляя повреждённый исходник молча.

### `ProjectKnowledge.save`

[Исходник](../../agent/project_knowledge.py#L49)

```python
def save(self, data)
```

Атомарно сохраняет ограниченный каталог без автоматического удаления пользовательских решений.

### `ProjectKnowledge.witness`

[Исходник](../../agent/project_knowledge.py#L54)

```python
def witness(self, path, policy, cache)
```

Хеширует только разрешённые выбранные файлы с ограниченным IO и повторной проверкой политики после чтения.

### `ProjectKnowledge.assess`

[Исходник](../../agent/project_knowledge.py#L89)

```python
def assess(self, item, policy, cache)
```

Отмечает изменение, удаление, отзыв доступа и смену политики; не объявляет гипотезу фактом или старую проверку текущей.

### `ProjectKnowledge.listing`

[Исходник](../../agent/project_knowledge.py#L102)

```python
def listing(self, query='', model=False, limit=120, identities=None)
```

Ранжирует текст и пути, затем исключает недоступные/устаревшие записи до model projection.

### `ProjectKnowledge.put`

[Исходник](../../agent/project_knowledge.py#L124)

```python
def put(self, params, origin='user', provenance=None, expected=None)
```

Создаёт host ID/время/provenance и source witnesses; модель может сохранять только гипотезы по известным источникам.

### `ProjectKnowledge.remove`

[Исходник](../../agent/project_knowledge.py#L156)

```python
def remove(self, identity)
```

Удаляет выбранную запись без изменения диалогов и исходного журнала.

### `ProjectKnowledge.context`

[Исходник](../../agent/project_knowledge.py#L161)

```python
def context(self, query, max_chars=3200)
```

Строит bounded справочные данные с явным различием свежести источника и истинности вывода.

### `invalid_source_path`

[Исходник](../../agent/project_knowledge.py#L171)

```python
def invalid_source_path(path)
```

Отклоняет абсолютный путь, диск Windows и traversal до разрешения источника.

### `remember_from_model`

[Исходник](../../agent/project_knowledge.py#L177)

```python
def remember_from_model(root, args, task)
```

Сверяет источники с успешными read receipts текущего journal и сохраняет только гипотезу.

### `capture_task_memory`

[Исходник](../../agent/project_knowledge.py#L191)

```python
def capture_task_memory(root, task)
```

Получает наблюдения файлов, scoped проверок и завершённой задачи из durable receipts/checkpoint, без копирования ответа модели.

### `memory_projection`

[Исходник](../../agent/project_knowledge.py#L222)

```python
def memory_projection(root, query)
```

Создаёт одно ограниченное data-сообщение с host metadata, удаляемой перед API.

### `validate_memory_projection`

[Исходник](../../agent/project_knowledge.py#L229)

```python
def validate_memory_projection(messages, root)
```

Перед POST, после очереди и при retry убирает изменённую память; сохранённые tool результаты сверяются заново.

### `has_memory_projection`

[Исходник](../../agent/project_knowledge.py#L246)

```python
def has_memory_projection(messages)
```

Находит host маркер и известные memory tools в original messages для транспортной перепроверки.

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

[Исходник](../../agent/project_memory.py#L92)

```python
def load_project_memory(project_root: str) -> dict[str, Any]
```

Загружает и валидирует запись; при ошибке создаёт пустую память.

### `save_project_memory`

[Исходник](../../agent/project_memory.py#L103)

```python
def save_project_memory(project_root: str, data: dict[str, Any], *, origin='user') -> dict[str, Any]
```

Валидирует и атомарно сохраняет JSON памяти выбранного проекта.

### `clear_project_memory`

[Исходник](../../agent/project_memory.py#L124)

```python
def clear_project_memory(project_root: str) -> None
```

Удаляет только память указанного проекта.

### `format_memory_context`

[Исходник](../../agent/project_memory.py#L134)

```python
def format_memory_context(memory: dict[str, Any], max_chars: int=3600) -> str
```

Формирует ограниченный справочный блок для system prompt.

### `merge_memory_update`

[Исходник](../../agent/project_memory.py#L160)

```python
def merge_memory_update(existing: dict[str, Any], update: Any, project_root: str) -> dict[str, Any]
```

Объединяет только разрешённые поля модельного обновления с существующей памятью и валидирует итог.

### `current_user_notes`

[Исходник](../../agent/project_memory.py#L171)

```python
def current_user_notes(root)
```

Подаёт в модель только пользовательские заметки с актуальной политикой; legacy/model summaries остаются в редакторе как история.

<a id="module-agent-project-symbols-py"></a>

## `agent/project_symbols.py`

Синтаксические определения/импорты Python AST и JS/TS/TSX Tree-sitter; никакого выполнения исходников или semantic reference resolution.

### `extract_symbols`

[Исходник](../../agent/project_symbols.py#L6)

```python
def extract_symbols(path, text)
```

Извлекает определения, методы, imports/exports и byte-column ranges через AST/Tree-sitter; parser error не блокирует текстовый индекс.

### `extract_symbols.add`

[Исходник](../../agent/project_symbols.py#L9)

```python
def add(name, kind, start, end, column=0, end_column=0)
```

Добавляет ограниченное именованное описание символа с точным source range и precision=syntax.

<a id="module-agent-projects-py"></a>

## `agent/projects.py`

Проекты в SQLite и атомарное отсоединение всех их чатов при удалении проекта.

### `ProjectStore`

[Исходник](../../agent/projects.py#L11)

```python
class ProjectStore
```

Каталог пространств, объединяющих разговоры общими инструкциями и необязательной папкой IDE.

### `ProjectStore.__init__`

[Исходник](../../agent/projects.py#L12)

```python
def __init__(self, directory=None)
```

Инициализирует состояние экземпляра ProjectStore; параметры показаны в сигнатуре, назначение описано у класса.

### `ProjectStore._database`

[Исходник](../../agent/projects.py#L17)

```python
def _database(self)
```

Возвращает один экземпляр Storage для вложенных транзакций save/list/get без повторного writer lock.

### `ProjectStore.list`

[Исходник](../../agent/projects.py#L21)

```python
def list(self)
```

Читает канонические метаданные проектов из общей БД профиля.

### `ProjectStore.get`

[Исходник](../../agent/projects.py#L26)

```python
def get(self, project_id)
```

Возвращает выбранный проект либо совместимое личное пространство с пустым ID.

### `ProjectStore.save`

[Исходник](../../agent/projects.py#L32)

```python
def save(self, params)
```

Проверяет имя, инструкции и существование папки; сохраняет проект с временными метками одной транзакцией.

### `ProjectStore.remove`

[Исходник](../../agent/projects.py#L53)

```python
def remove(self, project_id)
```

Одной транзакцией отсоединяет чаты всех режимов, обновляет metadata/summary и удаляет группу; файлы проекта не меняет.

<a id="module-agent-readonly-research-py"></a>

## `agent/readonly_research.py`

Отдельный readonly контекст: до 6 фрагментов/12000 символов, один HTTP запрос без tools/retry, cancel и usage.

### `collect_sources`

[Исходник](../../agent/readonly_research.py#L13)

```python
def collect_sources(root, query, context, max_files=6)
```

Lexical поиск до трёх слов, fallback имён, исключение распространённых credential файлов, до 6 range excerpts/12000 символов.

### `request_research`

[Исходник](../../agent/readonly_research.py#L32)

```python
async def request_research(config, query, sources, context, max_tokens)
```

Единственный bounded HTTP запрос Chat/Responses без action tools; проверяет payload budget и возвращает complete/usage без исходных credentials.

### `research_async`

[Исходник](../../agent/readonly_research.py#L69)

```python
async def research_async(config, query, sources, context, max_tokens)
```

Соревнуется с общим cancel/deadline; закрывает обе async tasks и HTTP при завершении.

### `research`

[Исходник](../../agent/readonly_research.py#L79)

```python
def research(root, query, config, context, max_tokens=1024)
```

Проверяет вопрос и модель, собирает источники, запускает запрос и возвращает path/line/SHA anchors и метрики.

<a id="module-agent-request-budget-py"></a>

## `agent/request_budget.py`

Автоматическое/ручное размещение окончательного Chat/JSON/Responses запроса: tokenizer/оценка, ответ, каталог schemas и компактные квитанции выполненного кода без изменения истории.

### `BudgetExceededError`

[Исходник](../../agent/request_budget.py#L10)

```python
class BudgetExceededError(ValueError)
```

Управляемая остановка: обязательные данные не помещаются в настроенное окно без изменения.

### `json_bytes`

[Исходник](../../agent/request_budget.py#L14)

```python
def json_bytes(value)
```

Измеряет байты конечного UTF-8 JSON для диагностики транспорта; байт не считается токеном.

### `prepare_model_request`

[Исходник](../../agent/request_budget.py#L18)

```python
def prepare_model_request(params, tool_protocol='native', api_protocol='chat', cache=None)
```

Убирает внутренние source markers и применяет ровно те же JSON-tool/Responses адаптеры, что и реальный транспорт; telemetry включается до измерения.

### `estimated_tokens`

[Исходник](../../agent/request_budget.py#L33)

```python
def estimated_tokens(value)
```

Взвешенная fallback оценка ASCII/кириллицы/CJK/emoji с JSON framing; не равняет UTF-8 байты токенам.

### `compact_completed_calls`

[Исходник](../../agent/request_budget.py#L48)

```python
def compact_completed_calls(messages, max_argument_chars=2000)
```

Только полностью парные исторические большие write/patch заменяет assistant-архивом с SHA/результатами/anchors; pending calls и canonical не меняет.

### `RequestBudget`

[Исходник](../../agent/request_budget.py#L86)

```python
class RequestBudget
```

Подбирает проекцию под фактическое окно с SDK tokenizer либо языковой оценкой, framing, запасом и обратной связью usage.

### `RequestBudget.__init__`

[Исходник](../../agent/request_budget.py#L88)

```python
def __init__(self, window_tokens=32768, reserve_tokens=512, *, mode='manual')
```

Инициализирует состояние экземпляра RequestBudget; параметры показаны в сигнатуре, назначение описано у класса.

### `RequestBudget.configure`

[Исходник](../../agent/request_budget.py#L95)

```python
def configure(self, profile, counter=None)
```

Принимает actual profile и необязательный counter; очищает bounded cache при смене профиля.

### `RequestBudget.learn_rejection`

[Исходник](../../agent/request_budget.py#L101)

```python
def learn_rejection(self, window)
```

После явного pre-stream отказа уточняет окно и повышает запас, не повторяя уже начатый ответ или инструмент.

### `RequestBudget.observe_usage`

[Исходник](../../agent/request_budget.py#L107)

```python
def observe_usage(self, usage)
```

Повышает оценочный запас, если сервер сообщил больше входных токенов, чем ожидалось.

### `RequestBudget.measure`

[Исходник](../../agent/request_budget.py#L114)

```python
def measure(self, payload, original_tools=())
```

Считает инструкции, историю, schemas и protocol, включая encrypted Responses items и JSON escaping; возвращает свободный остаток и fits/blocked.

### `RequestBudget.check`

[Исходник](../../agent/request_budget.py#L162)

```python
def check(self, payload, original_tools=())
```

Последний gate перед транспортом; при превышении бросает BudgetExceededError без HTTP.

### `RequestBudget.explanation`

[Исходник](../../agent/request_budget.py#L169)

```python
@staticmethod
def explanation(stats)
```

Формирует объяснение превышения окна с величинами входа, ответа и запаса без содержимого пользовательских данных.

### `RequestBudget.fit`

[Исходник](../../agent/request_budget.py#L179)

```python
def fit(self, params, *, tool_protocol='native', api_protocol='chat', cache=None, protected_text=None)
```

На копиях подбирает ответ, schemas и историю; в auto архивирует большие уже завершённые writes, сохраняя текущий запрос и невыполненные calls.

<a id="module-agent-response-outcome-py"></a>

## `agent/response_outcome.py`

Общий контракт терминального ответа модели: complete/incomplete/refused/cancelled/error; EOF не становится успешным stop.

### `ModelResponseOutcome`

[Исходник](../../agent/response_outcome.py#L6)

```python
@dataclass(frozen=True)
class ModelResponseOutcome
```

Неизменяемые status/finish_reason/reason; нормализует результат независимо от провайдера.

Поля, объявленные в классе:

```python
status: str
finish_reason: str
reason: str = ''
```

### `ModelResponseOutcome.classify`

[Исходник](../../agent/response_outcome.py#L12)

```python
@classmethod
def classify(cls, finish_reason=None, *, refused=False, cancelled=False, error=False)
```

Использует явную terminal reason, отказ/отмену/ошибку; неизвестный EOF классифицирует incomplete.

### `ModelResponseOutcome.snapshot`

[Исходник](../../agent/response_outcome.py#L28)

```python
def snapshot(self)
```

Возвращает JSON-safe состояние для checkpoint и интерфейса.

### `parse_completion_assessment`

[Исходник](../../agent/response_outcome.py#L33)

```python
def parse_completion_assessment(raw)
```

Строго разбирает явный boolean complete; строки, числа, дубликаты и произвольный текст не являются подтверждением.

### `answer_format_issue`

[Исходник](../../agent/response_outcome.py#L47)

```python
def answer_format_issue(prompt, text)
```

Проверяет явно запрошенный путь:строка и возвращает только инструкцию исправления формата без выдумывания источника.

<a id="module-agent-responses-adapter-py"></a>

## `agent/responses_adapter.py`

Преобразование канонической истории и потоковых событий OpenAI Responses в существующий цикл агента.

### `response_request`

[Исходник](../../agent/responses_adapter.py#L5)

```python
def response_request(params, cache=None)
```

Преобразует сообщения/tool results в Responses input, добавляет инструкции и store=false, сохраняет reasoning continuity внутри запуска.

### `chat_chunk`

[Исходник](../../agent/responses_adapter.py#L28)

```python
def chat_chunk(content=None, calls=None, finish=None)
```

Создаёт минимальный совместимый объект choices/delta для существующего потокового AgentEngine.

### `ResponseEvents`

[Исходник](../../agent/responses_adapter.py#L32)

```python
class ResponseEvents
```

Состояние преобразования одного Responses stream: индексы функций и уже полученные аргументы.

### `ResponseEvents.__init__`

[Исходник](../../agent/responses_adapter.py#L33)

```python
def __init__(self, cache)
```

Инициализирует состояние экземпляра ResponseEvents; параметры показаны в сигнатуре, назначение описано у класса.

### `ResponseEvents.translate`

[Исходник](../../agent/responses_adapter.py#L36)

```python
def translate(self, event)
```

Переводит текст и аргументы функций, обрабатывает завершение/ошибку и сохраняет output items для следующего tool turn.

### `response_completion`

[Исходник](../../agent/responses_adapter.py#L65)

```python
def response_completion(response)
```

Приводит нестриминговый output_text к интерфейсу Chat Completion, используемому проверкой завершения и памятью.

<a id="module-agent-run-policy-py"></a>

## `agent/run_policy.py`

Opt-in monetary planning for one logical task and all children/resumes; no local-auto cap, explicit unknown usage and capacity errors.

### `SpendingLimitError`

[Исходник](../../agent/run_policy.py#L9)

```python
class SpendingLimitError(BudgetExceededError)
```

Управляемая пауза по добровольному денежному порогу; наследует существующий BudgetExceededError.

### `ModelCapacityError`

[Исходник](../../agent/run_policy.py#L13)

```python
class ModelCapacityError(BudgetExceededError)
```

Управляемая пауза при подтверждённой нехватке памяти внешнего model server, без слепого повтора или выгрузки чужих моделей.

### `validate_spending`

[Исходник](../../agent/run_policy.py#L17)

```python
def validate_spending(value=None)
```

Проверяет явное включение, конечные суммы/цены и валюту; не подставляет выдуманные тарифы провайдера.

### `priced_tokens`

[Исходник](../../agent/run_policy.py#L29)

```python
def priced_tokens(policy, incoming, outgoing)
```

Пересчитывает токены по пользовательским ценам в целые нанодоли валюты с округлением вверх.

### `spending_snapshot`

[Исходник](../../agent/run_policy.py#L35)

```python
def spending_snapshot(connection, run_id)
```

Объединяет текущий journal задачи, детей и resume epochs; учитывает usage, активные резервы и неизвестные HTTP по оценке.

### `require_spending`

[Исходник](../../agent/run_policy.py#L59)

```python
def require_spending(connection, run_id, reservation)
```

В той же транзакции до reservation не допускает следующий внешний запрос сверх выбранного порога; local auto policy выключена.

### `capacity_failure`

[Исходник](../../agent/run_policy.py#L67)

```python
def capacity_failure(error)
```

Узко распознаёт сообщения OOM в ошибке сервера без сохранения его raw body в policy metadata.

<a id="module-agent-run-registry-py"></a>

## `agent/run_registry.py`

Сохраняемые epochs запуска и атомарный BudgetLedger в canonical SQLite v3; recovery orphan telemetry без повторения эффектов.

### `now`

[Исходник](../../agent/run_registry.py#L17)

```python
def now()
```

UTC timestamp для долговечных записей; elapsed/approval измеряются отдельно monotonic clock.

### `safe_usage`

[Исходник](../../agent/run_registry.py#L22)

```python
def safe_usage(value)
```

Нормализует две сообщённые провайдером token counts, сохраняя отсутствие telemetry как unknown.

### `BudgetLedger`

[Исходник](../../agent/run_registry.py#L31)

```python
class BudgetLedger
```

Инкрементальные счётчики, обновляемые в одной транзакции с attempt; никаких caps и самостоятельной политики остановки.

### `BudgetLedger.contribution`

[Исходник](../../agent/run_registry.py#L34)

```python
@staticmethod
def contribution(attempt)
```

Вычисляет вклад одной попытки: HTTP, один cumulative usage, reservation, queue и interrupt.

### `BudgetLedger.apply`

[Исходник](../../agent/run_registry.py#L43)

```python
@staticmethod
def apply(connection, run_id, before, after)
```

Атомарно прибавляет разность before/after; повторная запись terminal usage не удваивает токены.

### `RunRegistry`

[Исходник](../../agent/run_registry.py#L51)

```python
class RunRegistry
```

Отдельные run ID для исполнения/повтора, связь с chat/journal и parent, без копии prompt и нового execution authority.

### `RunRegistry.__init__`

[Исходник](../../agent/run_registry.py#L53)

```python
def __init__(self, directory=None, alive=None, inspect_owner=inspect_process)
```

Инициализирует состояние экземпляра RunRegistry; параметры показаны в сигнатуре, назначение описано у класса.

### `RunRegistry.ready`

[Исходник](../../agent/run_registry.py#L56)

```python
def ready(self)
```

При первом доступе атомарно восстанавливает только доказанно завершённые process lifetimes; кеширует probe на owner и снимает orphan reservations без replay.

### `RunRegistry.begin`

[Исходник](../../agent/run_registry.py#L85)

```python
def begin(self, *, kind, model, base_url, api_protocol='chat', chat_id='', journal_id='', run_id=None, operation=None, parent=None, spending_policy=None)
```

Создаёт новый epoch с PID/creation token, прежним connection inheritance и ограничениями prototype child identities; другая модель не загружается.

### `RunRegistry.update`

[Исходник](../../agent/run_registry.py#L114)

```python
def update(self, identity, **changes)
```

Короткая транзакция host lifecycle metadata; текущий ledger сохраняется без потери конкурентных delta updates.

### `RunRegistry.attempt`

[Исходник](../../agent/run_registry.py#L122)

```python
def attempt(self, run_id, purpose, reservation)
```

Создаёт reservation до очереди; это ещё не HTTP и не факт расхода токенов.

### `RunRegistry.record_tool`

[Исходник](../../agent/run_registry.py#L135)

```python
def record_tool(self, identity)
```

Атомарно увеличивает счётчик квитанций текущего epoch, независимо от сброса legacy task.tool_calls при resume.

### `RunRegistry.update_attempt`

[Исходник](../../agent/run_registry.py#L141)

```python
def update_attempt(self, identity, **changes)
```

Атомарно обновляет attempt и вклад в ledger; headers/payload/exception text не сохраняются.

### `RunRegistry.snapshot`

[Исходник](../../agent/run_registry.py#L150)

```python
def snapshot(self, identity)
```

Читает агрегированный ledger без сканирования всех attempts; для живого epoch добавляет текущее elapsed/approval время.

### `RunRegistry.history`

[Исходник](../../agent/run_registry.py#L166)

```python
def history(self, chat_id, limit=20)
```

Возвращает до 20 epochs выбранного чата с верхним backend пределом 50 записей.

### `RunRegistry.cancel`

[Исходник](../../agent/run_registry.py#L171)

```python
def cancel(self, identity)
```

Сигнализирует OperationContext всего живого дерева, не заявляя rollback или подтверждённое завершение tool effect.

### `RunContext`

[Исходник](../../agent/run_registry.py#L181)

```python
class RunContext
```

Состояние одного epoch: независимый ID, cancellation, исходная модель и монотонные durations; не второй план задач.

### `RunContext.__init__`

[Исходник](../../agent/run_registry.py#L183)

```python
def __init__(self, registry, identity, kind, model, base_url, api_protocol, chat_id, parent_id, operation)
```

Инициализирует состояние экземпляра RunContext; параметры показаны в сигнатуре, назначение описано у класса.

### `RunContext.observe`

[Исходник](../../agent/run_registry.py#L188)

```python
def observe(self, task)
```

Отражает существующий RunState и отдельный approval wait; legacy task counter не используется для вычитания новых вызовов.

### `RunContext.record_tool`

[Исходник](../../agent/run_registry.py#L197)

```python
def record_tool(self)
```

Регистрирует одну обработанную tool квитанцию; ошибка/отказ не выдаются за подтверждённый side effect.

### `RunContext.finish`

[Исходник](../../agent/run_registry.py#L201)

```python
def finish(self, state='completed')
```

Завершает epoch после cleanup; resume получает новый ID, неизвестные side effects не воспроизводятся.

### `RunContext.snapshot`

[Исходник](../../agent/run_registry.py#L213)

```python
def snapshot(self)
```

Возвращает metadata/ledger текущего epoch, без канонической истории и исходников.

<a id="module-agent-run-state-py"></a>

## `agent/run_state.py`

Проверяемый жизненный цикл запуска с совместимой проекцией legacy status; этапы плана хранятся независимо.

### `InvalidRunStateTransition`

[Исходник](../../agent/run_state.py#L7)

```python
class InvalidRunStateTransition(ValueError)
```

Ошибка неизвестного состояния или недопустимого перехода; исходный task не меняется.

### `RunState`

[Исходник](../../agent/run_state.py#L36)

```python
class RunState
```

Единственный контроллер поля run_state; поддерживает прежний status и не меняет содержательные этапы плана.

### `RunState.__init__`

[Исходник](../../agent/run_state.py#L44)

```python
def __init__(self, task: dict[str, Any] | None)
```

Инициализирует состояние экземпляра RunState; параметры показаны в сигнатуре, назначение описано у класса.

### `RunState.phase`

[Исходник](../../agent/run_state.py#L63)

```python
@property
def phase(self) -> str
```

Читает актуальную фазу из общего task, чтобы два адаптера не пользовались устаревшей копией.

### `RunState._validate_phase`

[Исходник](../../agent/run_state.py#L68)

```python
@staticmethod
def _validate_phase(phase: str) -> None
```

Отклоняет неизвестную фазу до изменения словаря задачи.

### `RunState._legacy_status`

[Исходник](../../agent/run_state.py#L73)

```python
@staticmethod
def _legacy_status(phase: str) -> str
```

Преобразует активные фазы в running, завершение в completed, остановки в paused.

### `RunState.transition`

[Исходник](../../agent/run_state.py#L78)

```python
def transition(self, phase: str, reason: str='') -> str
```

Проверяет матрицу переходов, обновляет reason/event, очищает причину при возобновлении и запрещает открывать completed заново.

### `RunState.revise_plan`

[Исходник](../../agent/run_state.py#L104)

```python
def revise_plan(self)
```

Только явная trusted user revision переводит завершённый task checkpoint в paused; завершённый run epoch и general transition contract не переоткрываются.

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

[Исходник](../../agent/skills.py#L16)

```python
def _metadata(self, path)
```

Извлекает ID из каталога, заголовок, путь и краткую сводку.

### `SkillManager._summary`

[Исходник](../../agent/skills.py#L23)

```python
@staticmethod
def _summary(text)
```

Выбирает первую подходящую строку текста как summary до 300 символов.

### `SkillManager.load`

[Исходник](../../agent/skills.py#L29)

```python
def load(self, skill_id)
```

Читает полный текст навыка по ID; автоматически не исполняет его.

### `SkillManager.select`

[Исходник](../../agent/skills.py#L34)

```python
def select(self, prompt, limit=3)
```

Ранжирует метаданные по словам prompt и возвращает не больше limit совпадений.

<a id="module-agent-smart-context-py"></a>

## `agent/smart_context.py`

Детерминированное сжатие временного контекста с архивом ограничений и фактов без LLM-запросов и изменения канонической истории.

### `context_size`

[Исходник](../../agent/smart_context.py#L12)

```python
def context_size(messages)
```

Считает символы сериализованного JSON, а не токены модели.

### `text_digest`

[Исходник](../../agent/smart_context.py#L16)

```python
def text_digest(text)
```

Возвращает первые 16 hex символов SHA-256 для сверки сокращённого источника.

### `salient_text`

[Исходник](../../agent/smart_context.py#L20)

```python
def salient_text(text, query='', limit=1200)
```

Выбирает строки по запросу, ограничениям, началу и концу; маркирует фрагменты и исходный размер.

### `_mcp_text`

[Исходник](../../agent/smart_context.py#L41)

```python
def _mcp_text(content)
```

Извлекает текст до 30 блоков MCP; не включает бинарные изображения, аудио и resource payload.

### `_bounded_tool_json`

[Исходник](../../agent/smart_context.py#L48)

```python
def _bounded_tool_json(result, limit)
```

Уменьшает детали сжатого результата до фактического размера JSON, сохраняя коды и статус исхода.

### `compact_tool_result`

[Исходник](../../agent/smart_context.py#L66)

```python
def compact_tool_result(content, query, limit, tool_call_id=None, message_index=None)
```

Сокращает только tool data, сохраняя receipt anchor, исходный file SHA отдельно от result digest и ссылки на полный результат.

### `context_archive`

[Исходник](../../agent/smart_context.py#L99)

```python
def context_archive(units, budget, source_offset=0)
```

Собирает ограничения исходных пользователей, краткие запросы, решения и последние факты tools; при невозможности сохранить ограничения останавливается.

### `context_archive.render`

[Исходник](../../agent/smart_context.py#L127)

```python
def render()
```

Сериализует архив как данные истории без повышения роли или прав.

### `smart_compact_messages`

[Исходник](../../agent/smart_context.py#L136)

```python
def smart_compact_messages(messages, max_chars=80000, keep_recent_rounds=12, request_index=None)
```

Защищает текущий запрос и код, сохраняет целые пары tools, архивирует старые группы и возвращает метрики без изменения истории.

<a id="module-agent-storage-py"></a>

## `agent/storage.py`

SQLite/WAL профиль: схемы v1→v2, копирующая миграция JSON, индекс истории, checkpoint/receipts, snapshot metadata и ZIP backup.

### `encode`

[Исходник](../../agent/storage.py#L24)

```python
def encode(value)
```

Сериализует конечный JSON без NaN/Infinity и без потери русского текста.

### `valid_chat`

[Исходник](../../agent/storage.py#L29)

```python
def valid_chat(value)
```

Проверяет 32-символьный hex ID и список канонических dict-сообщений до записи или импорта.

### `Storage`

[Исходник](../../agent/storage.py#L36)

```python
class Storage
```

Локальный transactional профиль; короткие connections, WAL/FULL durability, миграции, история, поиск, артефакты и резервные копии.

### `Storage.__init__`

[Исходник](../../agent/storage.py#L39)

```python
def __init__(self, directory)
```

Инициализирует состояние экземпляра Storage; параметры показаны в сигнатуре, назначение описано у класса.

### `Storage._connect`

[Исходник](../../agent/storage.py#L45)

```python
def _connect(self)
```

Включает foreign keys и FULL synchronous; закрывает connection даже при повреждении БД на этапе PRAGMA.

### `Storage.transaction`

[Исходник](../../agent/storage.py#L59)

```python
@contextmanager
def transaction(self)
```

BEGIN IMMEDIATE перед чтением изменяемого состояния; commit/rollback при выходе, вложенные вызовы используют тот же connection.

### `Storage.ready`

[Исходник](../../agent/storage.py#L78)

```python
def ready(self)
```

Проверяет user_version, атомарно создаёт базовую схему и upgrade v1→v2 со snapshots; legacy JSON копируется один раз, более новая схема отклоняется.

### `Storage.pack`

[Исходник](../../agent/storage.py#L140)

```python
def pack(self, text)
```

Для tool output больше 16 КиБ сохраняет immutable bytes и возвращает внутренний reference v1.

### `Storage.unpack`

[Исходник](../../agent/storage.py#L146)

```python
def unpack(self, value)
```

Загружает только внутреннюю ссылку артефакта с проверкой SHA-256; наружу возвращает полный исходный текст.

### `Storage._source`

[Исходник](../../agent/storage.py#L152)

```python
def _source(self, connection, path, kind, items, error=None)
```

Сохраняет относительный путь, исходный SHA-256, тип, число объектов и статус проверки миграции.

### `Storage._migrate`

[Исходник](../../agent/storage.py#L158)

```python
def _migrate(self, connection)
```

Копирует чаты/messages, embedded или отдельный checkpoint и проекты; сверяет counts и неизменность исходников перед общим commit.

### `Storage._search_entry`

[Исходник](../../agent/storage.py#L214)

```python
def _search_entry(self, connection, chat_id, position, text)
```

Индексирует только title/user/assistant, обновляет изменившиеся записи и удаляет устаревшие; tool data не становится поисковой инструкцией.

### `Storage.write_chat`

[Исходник](../../agent/storage.py#L221)

```python
def write_chat(self, connection, chat, *, checkpoint=False)
```

В единой транзакции обновляет metadata, изменённые сообщения, поиск и явный checkpoint; draft не затирает новую задачу.

### `Storage.load_chat`

[Исходник](../../agent/storage.py#L245)

```python
def load_chat(self, chat_id)
```

Открывает согласованный read snapshot, возвращает полный transcript и единственный checkpoint, гидратирует сохранённые результаты.

### `Storage.checkpoint`

[Исходник](../../agent/storage.py#L271)

```python
def checkpoint(self, connection, chat_id)
```

Читает каноническую задачу; повреждённый legacy checkpoint не выдаёт за отсутствие задачи и блокирует продолжение этого чата.

### `Storage.catalog`

[Исходник](../../agent/storage.py#L283)

```python
def catalog(self, *, root=None, mode=None, project_id=None, archived=None)
```

Выбирает компактную metadata проекцию по индексу scope, не открывая transcripts, drafts и legacy JSON.

### `Storage.search`

[Исходник](../../agent/storage.py#L305)

```python
def search(self, query, *, root, mode, project_id, archived=False, limit=300)
```

FTS5 trigram для casefold substring от 3 символов; короткие строки и runtime без FTS используют scoped SQL fallback.

### `Storage.report`

[Исходник](../../agent/storage.py#L341)

```python
def report(self)
```

Возвращает schema version, quick_check, счётчики объектов и проверенный migration manifest без содержимого разговоров.

### `Storage.backup`

[Исходник](../../agent/storage.py#L354)

```python
def backup(self, destination, *, cancelled=None)
```

Online SQLite snapshot с проверенными tool/snapshot artifacts и legacy источниками; ZIP проверяется и fsync выполняется до замены выбранного файла.

### `Storage.backup.check`

[Исходник](../../agent/storage.py#L360)

```python
def check(*_args)
```

Проверяет отмену/deadline между SQLite pages, записями и ZIP chunks, включая точку до замены destination.

### `Storage.backup.copy`

[Исходник](../../agent/storage.py#L362)

```python
def copy(archive, path, name)
```

Копирует ZIP entry порциями 64 КБ с сохранением метаданных и проверкой отмены.

<a id="module-agent-subagent-profiles-py"></a>

## `agent/subagent_profiles.py`

Версионированный атомарный каталог readonly профилей, пользовательский CRUD и выключенные черновики модели без повышения прав.

### `SubagentProfiles`

[Исходник](../../agent/subagent_profiles.py#L21)

```python
class SubagentProfiles
```

Хранит декларативные профили без отдельного model/execution контура.

### `SubagentProfiles.__init__`

[Исходник](../../agent/subagent_profiles.py#L23)

```python
def __init__(self, directory)
```

Привязывает каталог к extensions directory и создаёт reentrant lock.

### `SubagentProfiles.load`

[Исходник](../../agent/subagent_profiles.py#L26)

```python
def load(self)
```

Читает schema 1, проверяет ограничения и уникальность, отказывает при повреждении вместо повышения прав.

### `SubagentProfiles.validate`

[Исходник](../../agent/subagent_profiles.py#L41)

```python
@staticmethod
def validate(item)
```

Проверяет ограниченный текст, readonly tool allowlist, ID, включение и версию.

### `SubagentProfiles.catalog`

[Исходник](../../agent/subagent_profiles.py#L51)

```python
def catalog(self)
```

Возвращает независимый снимок данных для UI и выбора профиля.

### `SubagentProfiles.configure`

[Исходник](../../agent/subagent_profiles.py#L55)

```python
def configure(self, params, generated=False)
```

Разделяет trusted user CRUD и append-only выключенные model drafts; атомарно сохраняет каталог.

### `SubagentProfiles.resolve`

[Исходник](../../agent/subagent_profiles.py#L80)

```python
def resolve(self, identity)
```

Перед запуском проверяет актуальное включение каталога и выбранного профиля.

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

[Исходник](../../agent/task_activity.py#L73)

```python
def recover_tools(task, messages)
```

Восстанавливает in-flight запись из соответствующего блока tool-call/result; неопределённый Apply отмечает unknown, остальные прерванные — interrupted.

<a id="module-agent-task-contract-py"></a>

## `agent/task_contract.py`

Пользовательские параметры IDE, план модели и критерии с привязкой к настоящим проверкам.

### `validate_options`

[Исходник](../../agent/task_contract.py#L12)

```python
def validate_options(value)
```

До запуска задачи проверяет readonly/auto/checks_only, критерии, ссылки на IDs, программы, argv, cwd и timeout; некорректный ввод не расширяет права.

### `install_contract`

[Исходник](../../agent/task_contract.py#L55)

```python
def install_contract(task, options)
```

Сохраняет исходные пользовательские критерии, параметры и baseline долговечной ревизии откатов.

### `set_plan`

[Исходник](../../agent/task_contract.py#L67)

```python
def set_plan(task, args, source='model')
```

Добавляет модельные шаги и критерии, сохраняя пользовательские требования; неизвестные check_ids отклоняет, успех не выдумывает.

### `command_key`

[Исходник](../../agent/task_contract.py#L90)

```python
def command_key(arguments)
```

SHA-256 точного program/argv/cwd; название проверки не меняет фактически исполняемую команду.

### `acceptance_summary`

[Исходник](../../agent/task_contract.py#L96)

```python
def acceptance_summary(task)
```

Выводит unverified/failed/stale/checks_passed только по связанным пользовательским командам и ревизии файлов.

<a id="module-agent-task-graph-py"></a>

## `agent/task_graph.py`

Canonical plan_steps DAG: migration, validation, receipt-based completion and scoped stale-evidence propagation.

### `migrate_plan`

[Исходник](../../agent/task_graph.py#L20)

```python
def migrate_plan(task)
```

Обновляет canonical plan_steps до schema 2; прежние строки остаются advisory proposed, не получают выдуманное done.

### `prepare_steps`

[Исходник](../../agent/task_graph.py#L27)

```python
def prepare_steps(task, steps, source)
```

Проверяет типы, IDs, DAG/циклы, относительные affected files и ссылки только на проверки пользователя; сохраняет evidence неизменённых узлов.

### `witness`

[Исходник](../../agent/task_graph.py#L57)

```python
def witness(root, paths)
```

Сверяет только явные пути, включая отсутствие после delete; hashes/статистика и policy повторно проверяются без fingerprint всего проекта.

### `refresh_steps`

[Исходник](../../agent/task_graph.py#L78)

```python
def refresh_steps(task)
```

Делает устаревшими изменённые witness/checks и зависимые done узлы, не меняя task lifecycle и не исполняя tools.

### `update_step`

[Исходник](../../agent/task_graph.py#L97)

```python
def update_step(task, args)
```

Завершает узел только по успешным durable receipts, подходящему типу действия, покрытию файлов и актуальным пользовательским checks; сохраняет witness.

<a id="module-agent-task-store-py"></a>

## `agent/task_store.py`

Checkpoint задач в SQLite и совместимость прежнего файлового хранения.

### `_now`

[Исходник](../../agent/task_store.py#L18)

```python
def _now()
```

UTC ISO-время для checkpoint.

### `_key`

[Исходник](../../agent/task_store.py#L21)

```python
def _key(chat_id: str) -> str
```

SHA-256 от chat_id, сокращённый для имени файла задачи.

### `task_path`

[Исходник](../../agent/task_store.py#L24)

```python
def task_path(chat_id: str) -> Path
```

Возвращает путь tasks/<hash>.json.

### `default_stages`

[Исходник](../../agent/task_store.py#L27)

```python
def default_stages(prompt='')
```

Делегирует построение начального списка этапов build_plan.

### `new_task`

[Исходник](../../agent/task_store.py#L30)

```python
def new_task(chat_id, project_root, prompt)
```

Создаёт словарь running-задачи с планом, счётчиками и resume_state.

### `_database`

[Исходник](../../agent/task_store.py#L43)

```python
def _database()
```

Выбирает тот же профиль SQLite по TASK_DIR; хранит checkpoint вне папки рабочего проекта.

### `save_task`

[Исходник](../../agent/task_store.py#L49)

```python
def save_task(task)
```

Обновляет timestamp копии задачи и фиксирует единственный checkpoint в SQLite.

### `load_task`

[Исходник](../../agent/task_store.py#L63)

```python
def load_task(chat_id)
```

Читает каноническую задачу; отсутствующую возвращает как None, повреждённый legacy checkpoint не игнорирует.

### `clear_task`

[Исходник](../../agent/task_store.py#L69)

```python
def clear_task(chat_id)
```

Удаляет канонический checkpoint без удаления истории сообщений; JSON источники миграции остаются.

### `set_stage`

[Исходник](../../agent/task_store.py#L75)

```python
def set_stage(task, stage_id, status='active', event='')
```

Закрывает посещённый активный этап, помечает непосещённые предыдущие skipped и активирует целевой.

### `finish_task`

[Исходник](../../agent/task_store.py#L87)

```python
def finish_task(task, status='completed', reason='')
```

Завершает посещённые этапы, пропускает pending и сохраняет итоговый статус/причину.

<a id="module-agent-tool-executor-py"></a>

## `agent/tool_executor.py`

Единая валидация разрешённых tools, границы начала побочных эффектов, diff approval и сохранение результатов до публикации.

### `ToolPolicy`

[Исходник](../../agent/tool_executor.py#L20)

```python
class ToolPolicy
```

Снимок разрешённых определений для одного запуска с schema validation и консервативной классификацией эффекта.

### `ToolPolicy.__init__`

[Исходник](../../agent/tool_executor.py#L21)

```python
def __init__(self, definitions, read_only=False)
```

Инициализирует состояние экземпляра ToolPolicy; параметры показаны в сигнатуре, назначение описано у класса.

### `ToolPolicy.validate`

[Исходник](../../agent/tool_executor.py#L25)

```python
def validate(self, call)
```

Проверяет имя, JSON-аргументы и объявленную схему до вызова обработчика.

### `ToolPolicy.effectful`

[Исходник](../../agent/tool_executor.py#L34)

```python
@staticmethod
def effectful(name)
```

Считает только фиксированный список встроенных readers безопасным для повтора; неизвестные и MCP tools считаются эффектами.

### `ToolExecutor`

[Исходник](../../agent/tool_executor.py#L39)

```python
class ToolExecutor
```

Координирует policy, lifecycle, согласия и durable receipts; engine управляет модельным циклом.

### `ToolExecutor.__init__`

[Исходник](../../agent/tool_executor.py#L40)

```python
def __init__(self, root, definitions, handler, settings, interrupted, *, task, journal, state, checkpoint, approve_write, change, approval_tools=(), preview=None, runner=None, instruction_guard=None)
```

Инициализирует состояние экземпляра ToolExecutor; параметры показаны в сигнатуре, назначение описано у класса.

### `ToolExecutor._denial_key`

[Исходник](../../agent/tool_executor.py#L59)

```python
@staticmethod
def _denial_key(name, arguments)
```

Определяет повтор отклонённого действия; назначение и check_id не меняют тождество команды.

### `ToolExecutor.prepare_batch`

[Исходник](../../agent/tool_executor.py#L66)

```python
def prepare_batch(self, calls, message_index, content=None)
```

Записывает пачку в журнал и закрепляет канонический индекс для её вызовов.

### `ToolExecutor._access_guard`

[Исходник](../../agent/tool_executor.py#L70)

```python
def _access_guard(self, args)
```

Повторно проверяет файловые пути по текущей policy до preview и перед effect после approval.

### `ToolExecutor._phase`

[Исходник](../../agent/tool_executor.py#L81)

```python
def _phase(self, phase, status, summary)
```

Сначала сохраняет фазу, затем обновляет bounded activity/checkpoint; эффект начинается только после возврата.

### `ToolExecutor.before_external_approval`

[Исходник](../../agent/tool_executor.py#L88)

```python
def before_external_approval(self)
```

Переводит команду или подтверждаемый MCP в ожидание и долговечно отмечает отсутствие исполнения.

### `ToolExecutor.after_external_approval`

[Исходник](../../agent/tool_executor.py#L93)

```python
def after_external_approval(self, allowed)
```

После согласия сохраняет started до возврата внешнему обработчику; отказ не открывает эту границу.

### `ToolExecutor.command_approval_note`

[Исходник](../../agent/tool_executor.py#L101)

```python
def command_approval_note(self)
```

Добавляет к approval точную область evidence и предупреждение, что это не ограничение доступа программы.

### `ToolExecutor._begin_command`

[Исходник](../../agent/tool_executor.py#L110)

```python
def _begin_command(self)
```

После approval фиксирует исходный witness и rollback/generation до запуска эффекта.

### `ToolExecutor._finish`

[Исходник](../../agent/tool_executor.py#L118)

```python
def _finish(self, result)
```

Проверяет формат ответа, записывает квитанцию до task/UI и снимает pending_write.

### `ToolExecutor.reject`

[Исходник](../../agent/tool_executor.py#L160)

```python
def reject(self, call, error, code='TOOL_LIMIT')
```

Создаёт настоящую квитанцию отказа по лимиту без запуска инструмента.

### `ToolExecutor.execute`

[Исходник](../../agent/tool_executor.py#L163)

```python
def execute(self, call, blocked=None)
```

Валидирует и исполняет один call; различает исключение чтения и неопределённый исход эффекта.

### `ToolExecutor._write`

[Исходник](../../agent/tool_executor.py#L205)

```python
def _write(self, args)
```

Готовит diff, ждёт согласия, сохраняет started, проверяет snapshot и выполняет запись; неизвестный исход не превращает в успех.

### `ToolExecutor._mutate`

[Исходник](../../agent/tool_executor.py#L256)

```python
def _mutate(self, name, args)
```

Объединяет правила проекта, preview, ожидание одноразового согласия, durable started и применение новых файловых операций.

### `ToolExecutor._capture_snapshot`

[Исходник](../../agent/tool_executor.py#L291)

```python
def _capture_snapshot(self, name, args, preview)
```

До файлового эффекта долговечно сохраняет before-image; ошибка снимка останавливает dispatch, не отключая защиту ради записи.

<a id="module-agent-tool-recovery-py"></a>

## `agent/tool_recovery.py`

Сверка журнала с канонической историей, восстановление свидетельств и ограниченных метаданных интерфейса.

### `task_journal`

[Исходник](../../agent/tool_recovery.py#L13)

```python
def task_journal(task)
```

Присваивает legacy-задаче ID эпохи при необходимости и открывает соответствующий журнал.

### `_import_legacy`

[Исходник](../../agent/tool_recovery.py#L18)

```python
def _import_legacy(task, messages, journal)
```

Консервативно переносит только незавершённые старые пачки, используя прежние activity/pending_write; успешные старые блоки сохраняет.

### `recover_task`

[Исходник](../../agent/tool_recovery.py#L52)

```python
def recover_task(task, messages, *, import_legacy=False)
```

Восстанавливает канонические результаты, последние 100 activity, modified_files и команды; формирует безопасные recovery_items без сырых payload.

<a id="module-agent-tools-py"></a>

## `agent/tools.py`

Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test.

### `validate_tool_arguments`

[Исходник](../../agent/tools.py#L13)

```python
def validate_tool_arguments(definition, arguments)
```

Проверяет JSON-объект по объявленной схеме до вызова любого инструмента; ошибка называет поле и правило без значений аргументов.

### `list_files`

[Исходник](../../agent/tools.py#L26)

```python
def list_files(root, path='.', recursive=False, max_entries=200, max_depth=5)
```

Перечисляет разрешённые файлы с фильтрами, ограничением entries и глубины обхода.

### `safe_relative`

[Исходник](../../agent/tools.py#L74)

```python
def safe_relative(target, base)
```

Возвращает относительное POSIX-представление пути для результатов tools.

### `read_file`

[Исходник](../../agent/tools.py#L79)

```python
def read_file(root, path)
```

Читает bounded UTF-8 bytes со stable stat/SHA-256, сохраняет CRLF и не расширяет прежний file-tool лимит.

### `search_text`

[Исходник](../../agent/tools.py#L98)

```python
def search_text(root, query, path='.', case_sensitive=False, max_depth=5, cancelled=None, pattern='', limit=200)
```

Ищет подстроку в UTF-8 файлах с пределами размера, глубины, числа совпадений и длины строки.

### `preview_file_change`

[Исходник](../../agent/tools.py#L104)

```python
def preview_file_change(root, path, content, *, max_existing_bytes=MAX_READ_BYTES)
```

Строит unified diff и снимок SHA-256 исходных байтов/предлагаемого текста с нормализованным путём, не записывая файл.

### `write_file`

[Исходник](../../agent/tools.py#L148)

```python
def write_file(root, path, content, overwrite=False, *, approved=False, expected_snapshot=None, max_existing_bytes=MAX_READ_BYTES)
```

Применяет только подтверждённую ревизию; краткий Windows sharing violation повторяет atomic replace после повторной проверки snapshot/пути, не обходя FILE_CHANGED.

### `workspace_tool`

[Исходник](../../agent/tools.py#L225)

```python
def workspace_tool(name, description, properties, required)
```

Создаёт строгие bounded JSON schemas нового набора IDE с явными обязательными полями.

### `execute_tool`

[Исходник](../../agent/tools.py#L255)

```python
def execute_tool(name, arguments, project_root, settings=None, *, approved=False, expected_snapshot=None, cancelled=None)
```

Диспетчер четырёх функций; превращает ожидаемые ошибки в структурированный tool result.

### `run_sandbox_self_test`

[Исходник](../../agent/tools.py#L299)

```python
def run_sandbox_self_test()
```

Выполняет изолированный внутренний unittest-набор проверки файловой границы и возвращает сводку.

### `run_sandbox_self_test.SandboxTests`

[Исходник](../../agent/tools.py#L304)

```python
class SandboxTests(unittest.TestCase)
```

Внутренняя suite временных project/outside каталогов; не пользовательский runtime-класс.

### `run_sandbox_self_test.SandboxTests.setUp`

[Исходник](../../agent/tools.py#L305)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `run_sandbox_self_test.SandboxTests.tearDown`

[Исходник](../../agent/tools.py#L312)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `run_sandbox_self_test.SandboxTests.test_read_inside_allowed`

[Исходник](../../agent/tools.py#L313)

```python
def test_read_inside_allowed(self)
```

Проверка: Внутренний self-test разрешает чтение в корне.

### `run_sandbox_self_test.SandboxTests.test_parent_traversal_denied`

[Исходник](../../agent/tools.py#L314)

```python
def test_parent_traversal_denied(self)
```

Проверка: Внутренний self-test отклоняет выход через родительский каталог.

### `run_sandbox_self_test.SandboxTests.test_absolute_outside_denied`

[Исходник](../../agent/tools.py#L316)

```python
def test_absolute_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний абсолютный путь.

### `run_sandbox_self_test.SandboxTests.test_list_outside_denied`

[Исходник](../../agent/tools.py#L318)

```python
def test_list_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний list_files.

### `run_sandbox_self_test.SandboxTests.test_search_outside_denied`

[Исходник](../../agent/tools.py#L321)

```python
def test_search_outside_denied(self)
```

Проверка: Внутренний self-test отклоняет внешний search_text.

### `run_sandbox_self_test.SandboxTests.test_symlink_escape_denied`

[Исходник](../../agent/tools.py#L324)

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

<a id="module-agent-verification-evidence-py"></a>

## `agent/verification_evidence.py`

Versioned evidence команд: исполнение, точная пользовательская область, before/after source witnesses, актуальность и lazy migration.

### `now`

[Исходник](../../agent/verification_evidence.py#L10)

```python
def now()
```

Возвращает UTC-время границы исполнения, отдельно от ожидания approval.

### `normalize_scope`

[Исходник](../../agent/verification_evidence.py#L15)

```python
def normalize_scope(value=None)
```

Принимает workspace либо до 128 точных файлов и 128 зависимостей; отвергает абсолютные пути, traversal, glob и ADS.

### `configured_check`

[Исходник](../../agent/verification_evidence.py#L38)

```python
def configured_check(task, arguments)
```

Находит только точное совпадение пользовательских check_id, program/argv/cwd и timeout.

### `command_scope`

[Исходник](../../agent/verification_evidence.py#L46)

```python
def command_scope(task, arguments)
```

Возвращает scope пользователя для точной команды; произвольный вызов модели остаётся workspace.

### `command_digest`

[Исходник](../../agent/verification_evidence.py#L52)

```python
def command_digest(arguments, scope)
```

Связывает квитанцию с программой, argv, cwd, timeout и нормализованной областью/зависимостями.

### `capture_witness`

[Исходник](../../agent/verification_evidence.py#L59)

```python
def capture_witness(root, scope)
```

Вызывает полный capture либо capture_files; связывает revision с canonical workspace id без обхода постороннего дерева для scoped.

### `make_receipt`

[Исходник](../../agent/verification_evidence.py#L72)

```python
def make_receipt(arguments, scope, before, after, result, *, started_at, rollback_revision=0, generation=0)
```

Создаёт v2 immutable facts исполнения и before/after witnesses с rollback revision и generation для durable journal.

### `assess_evidence`

[Исходник](../../agent/verification_evidence.py#L82)

```python
def assess_evidence(task, entry, current_workspace=None)
```

Проверяет версию, command/scope binding, stable witnesses, текущие source/policy и rollback; не повышает legacy/incomplete до успеха.

### `assess_evidence.verdict`

[Исходник](../../agent/verification_evidence.py#L89)

```python
def verdict(status, summary)
```

Формирует раздельные status/summary/coverage без утверждения полной сверки при scoped result.

### `migrate_evidence`

[Исходник](../../agent/verification_evidence.py#L122)

```python
def migrate_evidence(task)
```

При чтении старого checkpoint помечает legacy rows unverified, сохраняя exit code, raw journal и историю.

<a id="module-agent-verification-plan-py"></a>

## `agent/verification_plan.py`

Детерминированный выбор пользовательских проверок по затронутым путям; связанные критерии не пропускаются.

### `required_checks`

[Исходник](../../agent/verification_plan.py#L8)

```python
def required_checks(task)
```

Выбирает проверки только по явным applies_to; критерии готовности и ручной checks-only требуют соответствующие проверки независимо от пути.

<a id="module-agent-verifier-py"></a>

## `agent/verifier.py`

Оценка фактических команд и diagnostics с учётом области и свежести исходников.

### `StageVerifier`

[Исходник](../../agent/verifier.py#L7)

```python
class StageVerifier
```

Детерминированная проверка наличия результата этапа; не запускает команды или тесты.

### `StageVerifier.record_command`

[Исходник](../../agent/verifier.py#L8)

```python
def record_command(self, task, arguments, result)
```

Хранит program/argv/cwd/purpose/exit code, точный configured check_id и generation receipt; чужой success не выдаёт за нужную проверку.

### `StageVerifier.record_diagnostics`

[Исходник](../../agent/verifier.py#L26)

```python
def record_diagnostics(self, task, args, result)
```

Записывает LSP отдельно от exit codes команды; провал другой проверки не стирается.

### `StageVerifier.command_summary`

[Исходник](../../agent/verifier.py#L34)

```python
def command_summary(self, task)
```

Отличает not_run, failed, stale, incomplete и commands_passed; после новых файловых изменений прежний exit zero устаревает.

### `StageVerifier.refresh`

[Исходник](../../agent/verifier.py#L61)

```python
def refresh(self, task)
```

Обновляет command/acceptance evidence после загрузки или отката без изменения lifecycle задачи; непокрытые критерии остаются видимыми.

### `StageVerifier.verify`

[Исходник](../../agent/verifier.py#L73)

```python
def verify(self, stage_id, *, tool_events=None, final_text='', stop_reason='', task=None)
```

Для реальной задачи учитывает журнал неизвестных действий, реальные команды и stop_reason; прежний вызов без task сохранён для совместимости.

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

<a id="module-agent-workspace-access-py"></a>

## `agent/workspace_access.py`

Общая политика автоматического доступа: секретные пути, .neutralignore, точечные пользовательские исключения и повторная проверка истории.

### `WorkspaceAccessPolicy`

[Исходник](../../agent/workspace_access.py#L10)

```python
class WorkspaceAccessPolicy
```

Загружает доверенные точечные разрешения вне проекта и дополнительные deny globs из .neutralignore.

### `WorkspaceAccessPolicy.__init__`

[Исходник](../../agent/workspace_access.py#L11)

```python
def __init__(self, root)
```

Инициализирует состояние экземпляра WorkspaceAccessPolicy; параметры показаны в сигнатуре, назначение описано у класса.

### `WorkspaceAccessPolicy.allows`

[Исходник](../../agent/workspace_access.py#L39)

```python
def allows(self, path)
```

Проверяет каноническую цель, стандартные секретные имена и маски; точечное UI-разрешение не распространяется на папку.

### `WorkspaceAccessPolicy.require`

[Исходник](../../agent/workspace_access.py#L56)

```python
def require(self, path, *, mutation=False)
```

Возвращает разрешённый путь или отказ; модели запрещено менять .neutralignore через file tools.

### `WorkspaceAccessPolicy.catalog`

[Исходник](../../agent/workspace_access.py#L63)

```python
def catalog(self)
```

Возвращает только root/пути исключений/маски, не содержимое защищённых файлов.

### `WorkspaceAccessPolicy.configure`

[Исходник](../../agent/workspace_access.py#L67)

```python
def configure(self, paths, confirmed=False)
```

Требует literal true согласие, существующие отдельные файлы внутри root; атомарно сохраняет до 64 исключений.

### `filter_model_history`

[Исходник](../../agent/workspace_access.py#L85)

```python
def filter_model_history(messages, root)
```

Повторно применяет права к известным файловым tool results и цепочкам read_tool_result, сохраняя исходную историю.

### `filter_model_history.denied`

[Исходник](../../agent/workspace_access.py#L91)

```python
def denied(path)
```

Считает некорректный или выходящий путь непригодным для автоматического контекста.

<a id="module-agent-workspace-edits-py"></a>

## `agent/workspace_edits.py`

Preview и подтверждаемое применение patch/create-directory/rename/delete со snapshot, проверкой корня и восстановимыми метаданными.

### `record_workspace_change`

[Исходник](../../agent/workspace_edits.py#L14)

```python
def record_workspace_change(task, name, result, call_id, message_index)
```

Идемпотентно строит последние 100 workspace_changes из успешных квитанций, учитывает изменённые/перемещённые файлы без сырых содержимых.

### `mutation_path`

[Исходник](../../agent/workspace_edits.py#L29)

```python
def mutation_path(root, path)
```

Проверяет путь в выбранном корне и запрещает корень, .git и пути через ссылки/junction для новых изменений.

### `file_revision`

[Исходник](../../agent/workspace_edits.py#L45)

```python
def file_revision(path)
```

Читает не более 1 МБ и сверяет inode/size/mtime до и после чтения; возвращает байты и SHA256 ревизии.

### `parent_revision`

[Исходник](../../agent/workspace_edits.py#L56)

```python
def parent_revision(path)
```

Получает identity каталога для обнаружения замены родителя между preview и apply.

### `preview_mutation`

[Исходник](../../agent/workspace_edits.py#L61)

```python
def preview_mutation(root, name, args)
```

Готовит diff или список путей без изменения диска; привязывает аргументы, исходник и назначение к snapshot.

### `apply_mutation`

[Исходник](../../agent/workspace_edits.py#L107)

```python
def apply_mutation(root, name, args, *, approved=False, expected_snapshot=None, cancelled=None)
```

Требует согласия и тот же snapshot, применяет одну операцию без замены назначения; после возможного частичного эффекта возвращает unknown вместо автоматического повтора.

<a id="module-agent-workspace-read-py"></a>

## `agent/workspace_read.py`

Чтение точных диапазонов UTF-8 со стабильной ревизией, отменой и явным отказом от обрезания длинной строки.

### `read_range`

[Исходник](../../agent/workspace_read.py#L8)

```python
def read_range(root, path, start_line=1, end_line=None, cancelled=None, *, max_bytes=8000000, max_chars=12000)
```

С отменой читает ограниченный UTF-8 источник, проверяет ревизию и возвращает целые строки/next_line/SHA256 без усечения текущей строки.

<a id="module-agent-workspace-revision-py"></a>

## `agent/workspace_revision.py`

Ограниченный content fingerprint исходников и сравнение проверяемых receipt с текущей ревизией проекта.

### `WorkspaceRevisionService`

[Исходник](../../agent/workspace_revision.py#L12)

```python
class WorkspaceRevisionService
```

Общая источник-ревизия для проверок, сохранений редактора, внешних изменений и recovery.

### `WorkspaceRevisionService.capture`

[Исходник](../../agent/workspace_revision.py#L15)

```python
@staticmethod
def capture(root, *, max_files=10000, max_bytes=96000000, timeout=2)
```

Хеширует ограниченное дерево исходников; ошибки/лимиты/изменение во время чтения дают incomplete, а не чистый fingerprint.

### `WorkspaceRevisionService.capture_files`

[Исходник](../../agent/workspace_revision.py#L54)

```python
@staticmethod
def capture_files(root, paths, *, max_bytes=96000000, timeout=2)
```

Хеширует только объявленные сохранённые файлы с текущей access policy; отказывает ссылкам, moving files и неполной сверке.

### `evidence_matches`

[Исходник](../../agent/workspace_revision.py#L90)

```python
def evidence_matches(task, entry)
```

Требует совпадение полного content digest, версии/области и rollback generation.

<a id="module-agent-workspace-search-py"></a>

## `agent/workspace_search.py`

Общий ограниченный поиск файлов/текста для модели и GUI: glob по сегментам пути, отмена, deadline и лимиты обхода/чтения.

### `glob_matches`

[Исходник](../../agent/workspace_search.py#L13)

```python
def glob_matches(path, pattern)
```

Сопоставляет регистронезависимые сегменты glob; ** допускает ноль или несколько папок, * внутри сегмента не пересекает разделитель.

### `glob_matches.match`

[Исходник](../../agent/workspace_search.py#L18)

```python
@lru_cache(maxsize=None)
def match(i, j)
```

С мемоизацией проверяет пару индексов пути/маски без экспоненциального обхода вариантов **.

### `search_project`

[Исходник](../../agent/workspace_search.py#L25)

```python
def search_project(root, params, cancelled=None, *, timeout=3, max_files=15000, max_bytes=10000000, use_index=True)
```

Выполняет один ограниченный обход для текстового поиска и glob; не следует ссылкам/junction, сообщает причину остановки и статистику.

### `search_project.stop`

[Исходник](../../agent/workspace_search.py#L69)

```python
def stop()
```

Проверяет Event и монотонный deadline во время обхода и чтения строк.

<a id="module-agent-workspace-snapshots-py"></a>

## `agent/workspace_snapshots.py`

Долговечные before/after снимки файловых tools, сегменты изменений, conflict-aware rollback и ручная проверка прерванного отката.

### `fingerprint`

[Исходник](../../agent/workspace_snapshots.py#L23)

```python
def fingerprint(value)
```

Выбирает вид, hash, filesystem identity и права для сравнения; внутренний artifact reference не является ревизией файла.

### `SnapshotStore`

[Исходник](../../agent/workspace_snapshots.py#L28)

```python
class SnapshotStore
```

Снимки подтверждённых файловых операций; группы разделяются после чужих правок, ограничены 80 путями и не охватывают произвольные команды.

### `SnapshotStore.__init__`

[Исходник](../../agent/workspace_snapshots.py#L31)

```python
def __init__(self, root, chat_id, journal_id='')
```

Инициализирует состояние экземпляра SnapshotStore; параметры показаны в сигнатуре, назначение описано у класса.

### `SnapshotStore.capture`

[Исходник](../../agent/workspace_snapshots.py#L37)

```python
def capture(self, relative)
```

Читает реальный путь внутри корня без symlink/junction, до 1 МБ; сохраняет исходные байты в immutable base64 artifact.

### `SnapshotStore._rows`

[Исходник](../../agent/workspace_snapshots.py#L47)

```python
def _rows(self, connection, group_id)
```

Выбирает упорядоченные записи группы строго для выбранного чата и root.

### `SnapshotStore._aggregate`

[Исходник](../../agent/workspace_snapshots.py#L52)

```python
def _aggregate(self, rows)
```

Объединяет первый before и последний подтверждённый after по каждому пути, пропуская не выполненные операции.

### `SnapshotStore.prepare`

[Исходник](../../agent/workspace_snapshots.py#L61)

```python
def prepare(self, operation, args, preview, message_index, call_id)
```

До started сохраняет before и ожидаемый результат; ручная правка между операциями начинает отдельный undo segment.

### `SnapshotStore.finish`

[Исходник](../../agent/workspace_snapshots.py#L88)

```python
def finish(self, identity, result)
```

Проверяет фактические post-edit bytes против ожидаемых; чужое изменение не присваивается агенту как безопасный after.

### `SnapshotStore.reconcile`

[Исходник](../../agent/workspace_snapshots.py#L106)

```python
def reconcile(self, entries)
```

После прерывания помечает незавершённый capture недоступным; только доказанное отсутствие эффекта снимает pending snapshot.

### `SnapshotStore.list`

[Исходник](../../agent/workspace_snapshots.py#L117)

```python
def list(self)
```

Даёт до 50 групп со статусами и путями без исходного содержимого; binary/text bytes не уходят в UI metadata.

### `SnapshotStore.revision`

[Исходник](../../agent/workspace_snapshots.py#L129)

```python
def revision(self)
```

Читает долговечный счётчик откатов этого чата и root, используемый для инвалидирования результатов проверок.

### `SnapshotStore.rollback_event`

[Исходник](../../agent/workspace_snapshots.py#L133)

```python
def rollback_event(self)
```

Возвращает последний долговечный результат rollback/review, чтобы recovery отличал полный откат от ручной проверки partial state и записывал этот факт в контекст модели.

### `SnapshotStore.attention`

[Исходник](../../agent/workspace_snapshots.py#L139)

```python
def attention(self)
```

Находит все незавершённые/частичные откаты в области, независимо от лимита видимой истории групп.

### `SnapshotStore._validate`

[Исходник](../../agent/workspace_snapshots.py#L143)

```python
def _validate(self, rows, before, after)
```

До первого эффекта сверяет root identity, все after-ревизии и отсутствие чужих детей в созданных папках.

### `SnapshotStore.preview`

[Исходник](../../agent/workspace_snapshots.py#L156)

```python
def preview(self, group_id)
```

Строит обратный diff и fingerprint всей группы; конфликт файлов отменяет proposal без изменений.

### `SnapshotStore._original_bytes`

[Исходник](../../agent/workspace_snapshots.py#L175)

```python
def _original_bytes(self, saved)
```

Проверяет artifact checksum, base64 и hash исходного файла до восстановления.

### `SnapshotStore._restore_file`

[Исходник](../../agent/workspace_snapshots.py#L180)

```python
def _restore_file(self, path, saved, expected)
```

Пишет оригинал через temp/fsync и повторную проверку ревизии; create-only не заменяет появившийся файл, chmod возвращает исходные права.

### `SnapshotStore.restore`

[Исходник](../../agent/workspace_snapshots.py#L196)

```python
def restore(self, group_id, expected_fingerprint)
```

Фиксирует rolling_back и revision до эффектов; прогресс хранит после каждого пути. Частичный сбой не повторяется автоматически.

### `SnapshotStore.review`

[Исходник](../../agent/workspace_snapshots.py#L225)

```python
def review(self, group_id)
```

Сохраняет явную ручную проверку прерванного отката и снимает блокировку без изменения файлов.

<a id="module-core-python-assistant-service-py"></a>

## `core/python/assistant_service.py`

Локальные часы, ограниченный AST-калькулятор, атомарные заметки и отменяемые таймеры Лолы.

### `calculate`

[Исходник](../../core/python/assistant_service.py#L26)

```python
def calculate(expression)
```

Разбирает арифметику через AST с лимитами сложности, степени и конечного результата; не выполняет Python.

### `calculate.evaluate`

[Исходник](../../core/python/assistant_service.py#L31)

```python
def evaluate(node)
```

Рекурсивно разрешает только числа, скобки и whitelist арифметических операций.

### `AssistantService`

[Исходник](../../core/python/assistant_service.py#L44)

```python
class AssistantService
```

Владеет локальным хранилищем заметок, блокировкой и ограниченными таймерами до закрытия приложения.

### `AssistantService.__init__`

[Исходник](../../core/python/assistant_service.py#L45)

```python
def __init__(self, emit)
```

Инициализирует состояние экземпляра AssistantService; параметры показаны в сигнатуре, назначение описано у класса.

### `AssistantService.notes`

[Исходник](../../core/python/assistant_service.py#L48)

```python
def notes(self)
```

Читает ограниченный JSON список заметок; повреждённый файл сохраняется без перезаписи.

### `AssistantService.execute`

[Исходник](../../core/python/assistant_service.py#L57)

```python
def execute(self, name, args)
```

Выполняет именованную утилиту, валидирует параметры, атомарно пишет заметки или управляет таймерами.

### `AssistantService.fire`

[Исходник](../../core/python/assistant_service.py#L92)

```python
def fire(self, key)
```

Однократно удаляет таймер, отменяет callback и отправляет уведомление, если сервис ещё работает.

### `AssistantService.shutdown`

[Исходник](../../core/python/assistant_service.py#L98)

```python
def shutdown(self)
```

Отменяет все таймеры и запрещает новые операции.

<a id="module-core-python-background-job-py"></a>

## `core/python/background_job.py`

Один отменяемый maintenance worker вне синхронного dispatch/TaskService.lock.

### `BackgroundJob`

[Исходник](../../core/python/background_job.py#L6)

```python
class BackgroundJob
```

Владеет одним daemon maintenance worker и OperationContext, не занимает inference gate.

### `BackgroundJob.__init__`

[Исходник](../../core/python/background_job.py#L7)

```python
def __init__(self)
```

Инициализирует состояние экземпляра BackgroundJob; параметры показаны в сигнатуре, назначение описано у класса.

### `BackgroundJob.start`

[Исходник](../../core/python/background_job.py#L10)

```python
def start(self, work, respond, timeout=240)
```

Отклоняет дубликат/закрытый сервис, фиксирует callback исходного RPC и запускает работу вне bridge thread.

### `BackgroundJob.start.run`

[Исходник](../../core/python/background_job.py#L15)

```python
def run()
```

Возвращает нормализованный успех/ошибку исходному запросу после работы и проверки отмены.

### `BackgroundJob.cancel`

[Исходник](../../core/python/background_job.py#L27)

```python
def cancel(self)
```

Сигнализирует отмену, не освобождая слот живого worker заранее.

### `BackgroundJob.shutdown`

[Исходник](../../core/python/background_job.py#L33)

```python
def shutdown(self)
```

Закрывает вход, отменяет операцию и ограниченно ждёт завершения.

<a id="module-core-python-bridge-py"></a>

## `core/python/bridge.py`

JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout.

### `emit`

[Исходник](../../core/python/bridge.py#L34)

```python
def emit(message)
```

Сериализует один JSON-объект и под Lock пишет целую UTF-8 строку stdout.

### `current_root`

[Исходник](../../core/python/bridge.py#L59)

```python
def current_root()
```

Возвращает корень scoped IDE view или выбранный desktop workspace.

### `resolve_inside`

[Исходник](../../core/python/bridge.py#L62)

```python
def resolve_inside(relative: str) -> Path
```

Разрешает UI-путь относительно выбранного project_root и отклоняет выход наружу.

### `handle`

[Исходник](../../core/python/bridge.py#L73)

```python
def handle(method: str, params: dict) -> dict
```

Whitelist диспетчер RPC: состояние, проект, модель, чаты, задачи и readonly UI-файлы.

### `_handle`

[Исходник](../../core/python/bridge.py#L77)

```python
def _handle(method: str, params: dict) -> dict
```

Dispatcher RPC под общим TaskService lock: области чатов, профиль, STT, PC replies и Telegram; file scope по-прежнему ограничен.

### `main`

[Исходник](../../core/python/bridge.py#L305)

```python
def main() -> None
```

Цикл stdin JSON-lines с ID ответов, обработкой некорректного ввода и shutdown при EOF.

### `main.maintain`

[Исходник](../../core/python/bridge.py#L334)

```python
def maintain(context, operation=method, arguments=dict(params))
```

Выполняет snapshot/report в выделенном maintenance worker; тяжёлая операция не держит tasks.lock.

<a id="module-core-python-conversation-service-py"></a>

## `core/python/conversation_service.py`

Операции организации чатов с проверкой пространства, режима и корня файлов.

### `ConversationService`

[Исходник](../../core/python/conversation_service.py#L12)

```python
class ConversationService
```

Сервис организации канонической истории без доступа к произвольным файлам проекта.

### `ConversationService.__init__`

[Исходник](../../core/python/conversation_service.py#L13)

```python
def __init__(self, tasks)
```

Инициализирует состояние экземпляра ConversationService; параметры показаны в сигнатуре, назначение описано у класса.

### `ConversationService.scoped`

[Исходник](../../core/python/conversation_service.py#L16)

```python
def scoped(self, root, params)
```

Проверяет одновременно ID, режим, корень файлов и пространство; чужой чат не допускается к операции.

### `ConversationService.update`

[Исходник](../../core/python/conversation_service.py#L23)

```python
def update(self, root, params)
```

Меняет pin/archive/project_id только в idle-состоянии и сбрасывает активный выбор при перемещении или архиве.

### `ConversationService.delete`

[Исходник](../../core/python/conversation_service.py#L41)

```python
def delete(self, root, params)
```

Требует подтверждение, удаляет выбранный чат и checkpoint, сбрасывает активный выбор.

### `ConversationService.fork`

[Исходник](../../core/python/conversation_service.py#L52)

```python
def fork(self, root, params)
```

Копирует завершённую историю без активного checkpoint или готовит повтор последнего запроса в независимой ветке.

### `ConversationService.export`

[Исходник](../../core/python/conversation_service.py#L72)

```python
def export(self, root, params)
```

Формирует ограниченный Markdown/JSON для системного окна сохранения; не пишет путь из model arguments.

### `ConversationService.search`

[Исходник](../../core/python/conversation_service.py#L87)

```python
def search(self, root, params)
```

Ищет название и user/assistant текст внутри режима/пространства, разделяет архив и сортирует закреплённые выше.

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

[Исходник](../../core/python/editor_service.py#L11)

```python
class EditorService
```

Хранит одно ручное предложение в памяти и использует общий sandbox/atomic write без автоматического подтверждения.

### `EditorService.__init__`

[Исходник](../../core/python/editor_service.py#L12)

```python
def __init__(self)
```

Инициализирует состояние экземпляра EditorService; параметры показаны в сигнатуре, назначение описано у класса.

### `EditorService.clear`

[Исходник](../../core/python/editor_service.py#L15)

```python
def clear(self)
```

Забывает pending proposal при новой подготовке, решении или смене проекта.

### `EditorService.read`

[Исходник](../../core/python/editor_service.py#L18)

```python
def read(self, root, path)
```

Читает ограниченные UTF-8 байты, отвергает NUL, возвращает LF-представление, newline-стиль и хеш исходных байтов.

### `EditorService.preview`

[Исходник](../../core/python/editor_service.py#L40)

```python
def preview(self, root, params)
```

Сверяет editor revision с диском и снимком diff, готовит предложение до 1 МБ и сохраняет одноразовый proposal без записи.

### `EditorService.resolve`

[Исходник](../../core/python/editor_service.py#L66)

```python
def resolve(self, root, params)
```

Проверяет ID/root/решение, потребляет proposal и выполняет Apply с повторной проверкой snapshot; Reject/Cancel не пишут.

<a id="module-core-python-extension-service-py"></a>

## `core/python/extension_service.py`

Единый реестр разрешённых возможностей, progressive skills, импорт пакетов и снимки для одного запуска.

### `function`

[Исходник](../../core/python/extension_service.py#L20)

```python
def function(name, description, properties, required=())
```

Собирает единообразное определение function tool с JSON Schema и запретом лишних аргументов.

### `mcp_alias`

[Исходник](../../core/python/extension_service.py#L28)

```python
def mcp_alias(server, name)
```

Строит допустимое имя tools из полного server ID, transport endpoint и имени действия, предотвращая совпадения общих префиксов.

### `ExtensionService`

[Исходник](../../core/python/extension_service.py#L34)

```python
class ExtensionService
```

Владелец публичного реестра tools/пакетов/навыков/MCP и отдельного хранилища токенов в памяти.

### `ExtensionService.__init__`

[Исходник](../../core/python/extension_service.py#L35)

```python
def __init__(self, directory=None, bundled=None)
```

Инициализирует состояние экземпляра ExtensionService; параметры показаны в сигнатуре, назначение описано у класса.

### `ExtensionService._migrate_aliases`

[Исходник](../../core/python/extension_service.py#L55)

```python
def _migrate_aliases(self)
```

В памяти переводит старые MCP aliases и ссылки плагинов; явное выключение сохраняется для каждого нового имени.

### `ExtensionService.save`

[Исходник](../../core/python/extension_service.py#L74)

```python
def save(self)
```

Атомарно пишет публичное состояние без токенов и API-ключей.

### `ExtensionService.skills`

[Исходник](../../core/python/extension_service.py#L77)

```python
def skills(self)
```

Объединяет метаданные встроенных SKILL.md и ограниченные пользовательские JSON-инструкции с переключателями.

### `ExtensionService.catalog`

[Исходник](../../core/python/extension_service.py#L90)

```python
def catalog(self)
```

Возвращает GUI наборы, инструменты, навыки, пакеты и MCP; секрет не возвращается, доступен только has_token.

### `ExtensionService.configure`

[Исходник](../../core/python/extension_service.py#L108)

```python
def configure(self, params)
```

Проверяет и применяет конкретное действие переключения/редактирования, не предоставляя модели универсальное изменение настроек.

### `ExtensionService._save_skill`

[Исходник](../../core/python/extension_service.py#L163)

```python
def _save_skill(self, params, generated=False)
```

Проверяет длины и ID; создаёт пользовательскую инструкцию или новый выключенный черновик опыта модели.

### `ExtensionService.import_plugin`

[Исходник](../../core/python/extension_service.py#L176)

```python
def import_plugin(self, manifest)
```

Валидирует ограниченный декларативный пакет до записи; импортирует выключенные навыки/серверы без произвольного кода.

### `ExtensionService._reserve_discovery`

[Исходник](../../core/python/extension_service.py#L199)

```python
def _reserve_discovery(self, identity)
```

Под блокировкой резервирует одну проверку сервера до создания worker и получает копию настроек с cancellation Event.

### `ExtensionService._release_discovery`

[Исходник](../../core/python/extension_service.py#L210)

```python
def _release_discovery(self, identity, record)
```

Освобождает только принадлежащую конкретному worker резервацию discovery.

### `ExtensionService.discover_server`

[Исходник](../../core/python/extension_service.py#L214)

```python
def discover_server(self, identity)
```

Подключается к MCP, получает схемы, назначает уникальные псевдонимы и отвергает устаревший результат при смене настроек.

### `ExtensionService.start_discovery`

[Исходник](../../core/python/extension_service.py#L219)

```python
def start_discovery(self, identity, respond)
```

Запускает одну асинхронную проверку MCP с callback исходного RPC запроса; повтор до окончания отклоняется.

### `ExtensionService.start_discovery.run_discovery`

[Исходник](../../core/python/extension_service.py#L222)

```python
def run_discovery()
```

Получает результат discovery, освобождает резервацию и отвечает исходному клиенту.

### `ExtensionService.cancel_discovery`

[Исходник](../../core/python/extension_service.py#L238)

```python
def cancel_discovery(self, identity=None)
```

Сигнализирует отмену одной или всех проверок MCP без запуска нового процесса.

### `ExtensionService.shutdown`

[Исходник](../../core/python/extension_service.py#L245)

```python
def shutdown(self)
```

Закрывает приём discovery, отменяет текущие проверки и ограниченно ожидает их workers.

### `ExtensionService._discover_server`

[Исходник](../../core/python/extension_service.py#L255)

```python
def _discover_server(self, server, token, cancelled)
```

Получает реальные схемы, проверяет уникальные имена и актуальность настроек; отменённый или устаревший каталог не публикуется.

### `ExtensionService.snapshot`

[Исходник](../../core/python/extension_service.py#L273)

```python
def snapshot(self, groups)
```

Фиксирует разрешения одного запуска и каталог метаданных навыков; тела инструкций в prompt не подставляются заранее.

### `ExtensionService.execute`

[Исходник](../../core/python/extension_service.py#L295)

```python
def execute(self, snapshot, name, args, interrupted, approve)
```

Повторно проверяет разрешение, обслуживает skills и MCP, валидирует схему и запрашивает отдельное подтверждение внешнего действия.

<a id="module-core-python-ide-completion-py"></a>

## `core/python/ide_completion.py`

Небольшой локальный запрос автодополнения без инструментов с проверкой контекста.

### `complete`

[Исходник](../../core/python/ide_completion.py#L7)

```python
def complete(root, config, params, cancelled)
```

Проверяет локальность endpoint, путь и размер контекста, запрашивает короткое автодополнение и закрывает клиент.

<a id="module-core-python-ide-sessions-py"></a>

## `core/python/ide_sessions.py`

Изолированные представления единого Core и editor-owned операции через scoped adapter.

### `IdeSessions`

[Исходник](../../core/python/ide_sessions.py#L16)

```python
class IdeSessions
```

Изолирует выбор чата, workspace и editor adapter разных IDE views единого Core.

### `IdeSessions.__init__`

[Исходник](../../core/python/ide_sessions.py#L17)

```python
def __init__(self, tasks, emit)
```

Инициализирует состояние экземпляра IdeSessions; параметры показаны в сигнатуре, назначение описано у класса.

### `IdeSessions.attach`

[Исходник](../../core/python/ide_sessions.py#L20)

```python
def attach(self, root)
```

Проверяет папку, создаёт отдельную сессию и связывает её с editor adapter.

### `IdeSessions.detach`

[Исходник](../../core/python/ide_sessions.py#L39)

```python
def detach(self, identity)
```

Отменяет только активные запуски закрываемого IDE view.

### `IdeSessions.control`

[Исходник](../../core/python/ide_sessions.py#L45)

```python
@contextmanager
def control(self, chat_id)
```

Временно выбирает сессию владельца IDE run для удалённого управления; неоднозначный запуск не выбирает.

### `IdeSessions.scope`

[Исходник](../../core/python/ide_sessions.py#L61)

```python
@contextmanager
def scope(self, identity, method)
```

Проверяет allowlist операции и устанавливает contextvars конкретного IDE view на время RPC.

### `IdeSessions.request`

[Исходник](../../core/python/ide_sessions.py#L69)

```python
def request(self, identity, phase, payload, cancelled)
```

Отправляет editor operation и ждёт связанный ответ с отменой и конечным timeout; apply без ответа остаётся unknown.

### `IdeSessions.complete`

[Исходник](../../core/python/ide_sessions.py#L82)

```python
def complete(self, params)
```

Принимает единственный валидный ответ с совпадающими session_id и operation_id.

### `IdeWorkspaceAdapter`

[Исходник](../../core/python/ide_sessions.py#L93)

```python
class IdeWorkspaceAdapter
```

Делегирует запись выбранному редактору вместо Python writer.

### `IdeWorkspaceAdapter.__init__`

[Исходник](../../core/python/ide_sessions.py#L94)

```python
def __init__(self, owner, identity)
```

Инициализирует состояние экземпляра IdeWorkspaceAdapter; параметры показаны в сигнатуре, назначение описано у класса.

### `IdeWorkspaceAdapter.guard`

[Исходник](../../core/python/ide_sessions.py#L97)

```python
def guard(self, cancelled)
```

Запрашивает у редактора предварительную проверку workspace.

### `IdeWorkspaceAdapter.prepare`

[Исходник](../../core/python/ide_sessions.py#L100)

```python
def prepare(self, name, args, preview, cancelled)
```

Получает editor state для конкретного предложения до approval.

### `IdeWorkspaceAdapter.execute`

[Исходник](../../core/python/ide_sessions.py#L103)

```python
def execute(self, name, args, preview, cancelled)
```

Повторно проверяет disk snapshot и передаёт подтверждённое изменение editor-owned apply.

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

[Исходник](../../core/python/memory_service.py#L47)

```python
def write_memory(root, params)
```

Проверяет исходную byte revision под общим с auto-memory RLock, атомарно сохраняет только валидные поля и перечитывает результат.

### `memory_action`

[Исходник](../../core/python/memory_service.py#L59)

```python
def memory_action(root, params)
```

Принимает только trusted UI CRUD/search с CAS и expected root; не даёт модели повышать гипотезы до пользовательских фактов.

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

<a id="module-core-python-optional-ide-service-py"></a>

## `core/python/optional_ide_service.py`

Настройки выключенных по умолчанию возможностей, один фоновый job, shared inference lease, отмена и независимые адаптеры.

### `validate_settings`

[Исходник](../../core/python/optional_ide_service.py#L19)

```python
def validate_settings(value)
```

Строго проверяет четыре группы, boolean, поля и бюджеты, отвергает произвольные shell/mount параметры.

### `OptionalIdeService`

[Исходник](../../core/python/optional_ide_service.py#L41)

```python
class OptionalIdeService
```

Владеет опциональными настройками и одним job; не встраивает обязательную цепочку моделей в AgentEngine.

### `OptionalIdeService.__init__`

[Исходник](../../core/python/optional_ide_service.py#L42)

```python
def __init__(self, tasks, directory=None)
```

Инициализирует состояние экземпляра OptionalIdeService; параметры показаны в сигнатуре, назначение описано у класса.

### `OptionalIdeService.catalog`

[Исходник](../../core/python/optional_ide_service.py#L50)

```python
def catalog(self)
```

Возвращает настройки, warning, job и shared gate status без credentials.

### `OptionalIdeService.configure`

[Исходник](../../core/python/optional_ide_service.py#L53)

```python
def configure(self, value)
```

Только при idle атомарно сохраняет проверенные настройки; выключения применяются к следующим запросам.

### `OptionalIdeService.start`

[Исходник](../../core/python/optional_ide_service.py#L57)

```python
def start(self, root, params, respond)
```

Проверяет root/opt-in/подтверждение, получает lease исследователя и запускает worker, сохраняя отзывчивость JSON-lines bridge.

### `OptionalIdeService.start.run`

[Исходник](../../core/python/optional_ide_service.py#L77)

```python
def run()
```

Выполняет один адаптер над снимком settings/root/config; в finally освобождает свой gate и возвращает результат исходному RPC.

### `OptionalIdeService.cancel`

[Исходник](../../core/python/optional_ide_service.py#L105)

```python
def cancel(self)
```

Сигнализирует своему job без преждевременного освобождения модели или повтора effect.

### `OptionalIdeService.command`

[Исходник](../../core/python/optional_ide_service.py#L110)

```python
def command(self, root, args, context, approve)
```

Направляет обычную approved IDE command в container adapter при включённой изоляции.

### `OptionalIdeService.shutdown`

[Исходник](../../core/python/optional_ide_service.py#L113)

```python
def shutdown(self)
```

Закрывает вход новых jobs, отменяет текущий и ограниченно ждёт worker.

<a id="module-core-python-project-search-py"></a>

## `core/python/project_search.py`

Асинхронный cancellable GUI worker над общим agent.workspace_search; самостоятельного второго алгоритма поиска нет.

### `ProjectSearchService`

[Исходник](../../core/python/project_search.py#L8)

```python
class ProjectSearchService
```

Владеет одним отменяемым daemon worker; stdin JSON bridge остаётся доступен для других команд.

### `ProjectSearchService.__init__`

[Исходник](../../core/python/project_search.py#L9)

```python
def __init__(self)
```

Инициализирует состояние экземпляра ProjectSearchService; параметры показаны в сигнатуре, назначение описано у класса.

### `ProjectSearchService.start`

[Исходник](../../core/python/project_search.py#L15)

```python
def start(self, root, params, respond)
```

Фиксирует валидный корень/параметры и запускает worker; отклоняет параллельный поиск.

### `ProjectSearchService.start.run_search`

[Исходник](../../core/python/project_search.py#L27)

```python
def run_search()
```

Выполняет поиск, преобразует исключение в ответ и освобождает busy до отправки результата.

### `ProjectSearchService.cancel`

[Исходник](../../core/python/project_search.py#L39)

```python
def cancel(self)
```

Устанавливает event отмены только поискового worker.

### `ProjectSearchService.shutdown`

[Исходник](../../core/python/project_search.py#L43)

```python
def shutdown(self)
```

Запрашивает отмену и ограниченно ожидает собственный поток.

<a id="module-core-python-protocol-py"></a>

## `core/python/protocol.py`

Версия критического RPC, проверка входного envelope, run IDs, решений и confirmed до dispatch.

### `require_text`

[Исходник](../../core/python/protocol.py#L8)

```python
def require_text(params, key, limit=200)
```

Проверяет обязательную ограниченную строку без NUL до обращения к сервису.

### `validate_request`

[Исходник](../../core/python/protocol.py#L14)

```python
def validate_request(request)
```

Принимает protocol v1 и legacy envelope без version, проверяет критические IDs/флаги/решения и возвращает method/params без выполнения.

<a id="module-core-python-run-session-py"></a>

## `core/python/run_session.py`

Independent session owner and frozen connection for one foreground/background run, with live snapshot and stream cursor.

### `RunSession`

[Исходник](../../core/python/run_session.py#L10)

```python
class RunSession(TaskExecution)
```

Изолированное состояние одного запуска: frozen config, собственный SessionService, operation, stream и approval; общие capability services не дублируются.

### `RunSession.__init__`

[Исходник](../../core/python/run_session.py#L11)

```python
def __init__(self, owner, chat)
```

Инициализирует состояние экземпляра RunSession; параметры показаны в сигнатуре, назначение описано у класса.

### `RunSession.chat`

[Исходник](../../core/python/run_session.py#L35)

```python
@property
def chat(self)
```

Возвращает канонический чат владельца, независимо от выбранной вкладки UI.

### `RunSession.idle`

[Исходник](../../core/python/run_session.py#L38)

```python
def idle(self)
```

Блокирует повторный запуск этого владельца без ограничения других чатов.

### `RunSession._recover_chat`

[Исходник](../../core/python/run_session.py#L41)

```python
def _recover_chat(self)
```

Проверяет сохранённый checkpoint до начала нового epoch через существующий SessionService.

### `RunSession.select_chat`

[Исходник](../../core/python/run_session.py#L44)

```python
def select_chat(self, *args, **kwargs)
```

Запрещает смену области внутри исполнения: coordinator обязан передать чат заранее.

### `RunSession.begin`

[Исходник](../../core/python/run_session.py#L47)

```python
def begin(self, root, params)
```

Создаёт собственную operation, запускает существующий loop и закрывает reservation/таймеры при ошибке старта.

### `RunSession.view`

[Исходник](../../core/python/run_session.py#L58)

```python
def view(self)
```

Под control lock копирует checkpoint/history и незавершённый текст с message_id; отдаёт live run, approval и event cursor без записи в историю.

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

<a id="module-core-python-session-service-py"></a>

## `core/python/session_service.py`

Выбор, scoped список/переименование/перенос чатов и восстановление canonical history отдельно от inference.

### `SessionService`

[Исходник](../../core/python/session_service.py#L10)

```python
class SessionService
```

Владелец выбранного чата/project_id и восстановления, не создаёт модель и не управляет React.

### `SessionService.__init__`

[Исходник](../../core/python/session_service.py#L11)

```python
def __init__(self, lock, idle, model_for_mode)
```

Инициализирует состояние экземпляра SessionService; параметры показаны в сигнатуре, назначение описано у класса.

### `SessionService.move_chat`

[Исходник](../../core/python/session_service.py#L15)

```python
def move_chat(self, params)
```

Переносит Chat/Лолу только внутри выбранной области с проверкой mode/root/project.

### `SessionService.chats`

[Исходник](../../core/python/session_service.py#L29)

```python
def chats(self, root, mode=None)
```

Читает индексированную metadata по scope без transcripts scan.

### `SessionService.rename`

[Исходник](../../core/python/session_service.py#L35)

```python
def rename(self, root, params)
```

Проверяет заголовок и принадлежность области, обновляет selected projection.

### `SessionService.select_chat`

[Исходник](../../core/python/session_service.py#L51)

```python
def select_chat(self, root, chat_id=None, mode=None, *, allow_busy=False)
```

Загружает проверенный scoped chat либо создаёт новый и восстанавливает checkpoint/stream fragment/receipts.

### `SessionService.recover`

[Исходник](../../core/python/session_service.py#L69)

```python
def recover(self)
```

Сверяет chat/task identity, чинит canonical tail из receipts, сохраняет неизвестные effects и rollback gates.

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

<a id="module-core-python-task-execution-py"></a>

## `core/python/task_execution.py`

Run-owned engine loop, tool dispatch, streaming timers, persistence and exact approval correlation; no UI selection state.

### `TaskExecution`

[Исходник](../../core/python/task_execution.py#L25)

```python
class TaskExecution
```

Общая реализация callbacks одного запуска; каждый RunSession владеет собственным chat, engine, таймерами и approval.

### `TaskExecution.request_delegation`

[Исходник](../../core/python/task_execution.py#L27)

```python
def request_delegation(self, name, args)
```

Разрешает только delegate_task, валидирует target/prompt, создаёт одну pending передачу с исходным человеческим запросом.

### `TaskExecution._persist_chat`

[Исходник](../../core/python/task_execution.py#L42)

```python
def _persist_chat(self, *, checkpoint=False)
```

Сохраняет канонический чат и отправляет warning при отказе производного индекса.

### `TaskExecution._task_event`

[Исходник](../../core/python/task_execution.py#L48)

```python
def _task_event(self, task)
```

Копирует checkpoint в тот же JSON с историей, сохраняет и публикует состояние задачи.

### `TaskExecution._event`

[Исходник](../../core/python/task_execution.py#L55)

```python
def _event(self, event_type, **data)
```

Под общим RLock выдаёт возрастающий cursor, chat/run/mode/root и сохраняет полный pending approval для возврата в чат.

### `TaskExecution._flush_text`

[Исходник](../../core/python/task_execution.py#L63)

```python
def _flush_text(self)
```

Отменяет таймер и отправляет накопленный фрагмент с ID сообщения.

### `TaskExecution._flush_scheduled`

[Исходник](../../core/python/task_execution.py#L73)

```python
def _flush_scheduled(self, run_id)
```

Под блокировкой допечатывает текст, только если таймер относится к текущему run.

### `TaskExecution._persist_draft`

[Исходник](../../core/python/task_execution.py#L79)

```python
def _persist_draft(self)
```

Сохраняет текущий текст/run/turn как независимый draft и обновляет время записи.

### `TaskExecution._persist_draft_scheduled`

[Исходник](../../core/python/task_execution.py#L85)

```python
def _persist_draft_scheduled(self, run_id, turn)
```

Сохраняет последний фрагмент даже при паузе сервера; проверяет run/turn и отменяет задачу при ошибке хранения.

### `TaskExecution._text_delta`

[Исходник](../../core/python/task_execution.py#L97)

```python
def _text_delta(self, turn, text)
```

Отправляет порции текста примерно через 40 мс и сохраняет первый/периодический draft для crash recovery.

### `TaskExecution._chat_event`

[Исходник](../../core/python/task_execution.py#L128)

```python
def _chat_event(self, role, text)
```

Допечатывает буфер и публикует полное сообщение с тем же ID, согласованно с таймером.

### `TaskExecution._request_approval`

[Исходник](../../core/python/task_execution.py#L138)

```python
def _request_approval(self, path, diff, exists)
```

Создаёт UUID предложения или немедленно отменяет его, если двигатель уже остановлен.

### `TaskExecution._approve_external`

[Исходник](../../core/python/task_execution.py#L150)

```python
def _approve_external(self, title, arguments, approval_kind='mcp')
```

Ждёт отдельное решение MCP/команды, проверяет актуальный запуск и поддерживает отмену независимо от файлового apply_all.

### `TaskExecution._wait_external_approval`

[Исходник](../../core/python/task_execution.py#L155)

```python
def _wait_external_approval(self, title, arguments, approval_kind)
```

Публикует внешний preview, освобождает inference gate и ждёт решение пользователя либо отмену.

### `TaskExecution.resolve_approval`

[Исходник](../../core/python/task_execution.py#L187)

```python
def resolve_approval(self, params)
```

Проверяет актуальные run/proposal ID и разрешённое решение, затем освобождает engine wait.

### `TaskExecution.cancel`

[Исходник](../../core/python/task_execution.py#L203)

```python
def cancel(self)
```

Отменяет исполнение задачи, ожидающее approval и фоновое обнаружение моделей.

### `TaskExecution._start`

[Исходник](../../core/python/task_execution.py#L216)

```python
def _start(self, root: Path, params)
```

Подготавливает capabilities/engine и запускает worker внутри уже полученного inference lease.

### `TaskExecution._start.dispatch`

[Исходник](../../core/python/task_execution.py#L277)

```python
def dispatch(name, args)
```

Направляет только разрешённые PC tools, delegate_task Лолы или обычные инструменты выбранного проекта; grants делегирования берёт из исходного человеческого запроса.

### `TaskExecution._save_messages`

[Исходник](../../core/python/task_execution.py#L354)

```python
def _save_messages(self, messages)
```

Допечатывает stream-буфер, отменяет draft-таймер и сохраняет канонические сообщения вместе с checkpoint.

### `TaskExecution._run`

[Исходник](../../core/python/task_execution.py#L369)

```python
def _run(self)
```

Завершает исполнение и сохранения, сбрасывает task_running под lock перед task_end; сообщает failed при ошибках.

<a id="module-core-python-task-service-py"></a>

## `core/python/task_service.py`

Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval.

### `TaskService`

[Исходник](../../core/python/task_service.py#L29)

```python
class TaskService
```

Координатор выбранной области и независимых RunSession; engine/thread/approval проецируют только выбранный чат.

### `TaskService.__init__`

[Исходник](../../core/python/task_service.py#L30)

```python
def __init__(self, emit, engine_factory=AgentEngine)
```

Инициализирует состояние экземпляра TaskService; параметры показаны в сигнатуре, назначение описано у класса.

### `TaskService.sessions`

[Исходник](../../core/python/task_service.py#L64)

```python
@property
def sessions(self)
```

Getter/setter выбранной SessionService в desktop или scoped IDE контексте.

### `TaskService.sessions`

[Исходник](../../core/python/task_service.py#L68)

```python
@sessions.setter
def sessions(self, value)
```

Getter/setter выбранной SessionService в desktop или scoped IDE контексте.

### `TaskService.workspace_adapter`

[Исходник](../../core/python/task_service.py#L72)

```python
@property
def workspace_adapter(self)
```

Возвращает editor adapter текущего IDE контекста.

### `TaskService.task_running`

[Исходник](../../core/python/task_service.py#L79)

```python
@property
def task_running(self)
```

Проверяет все run owners: глобальные изменения настроек/прав запрещены до завершения каждого.

### `TaskService.engine`

[Исходник](../../core/python/task_service.py#L83)

```python
@property
def engine(self)
```

Совместимая проекция engine выбранного владельца; фоновые callbacks используют собственную ссылку.

### `TaskService.engine`

[Исходник](../../core/python/task_service.py#L88)

```python
@engine.setter
def engine(self, value)
```

Совместимая проекция engine выбранного владельца; фоновые callbacks используют собственную ссылку.

### `TaskService.thread`

[Исходник](../../core/python/task_service.py#L92)

```python
@property
def thread(self)
```

Проекция потока выбранного владельца для join и диагностики, не общая переменная всех запусков.

### `TaskService.thread`

[Исходник](../../core/python/task_service.py#L97)

```python
@thread.setter
def thread(self, value)
```

Проекция потока выбранного владельца для join и диагностики, не общая переменная всех запусков.

### `TaskService.run_id`

[Исходник](../../core/python/task_service.py#L101)

```python
@property
def run_id(self)
```

Возвращает идентификатор выбранного запуска; setter оставлен для compatibility state до создания owner.

### `TaskService.run_id`

[Исходник](../../core/python/task_service.py#L106)

```python
@run_id.setter
def run_id(self, value)
```

Возвращает идентификатор выбранного запуска; setter оставлен для compatibility state до создания owner.

### `TaskService.approval`

[Исходник](../../core/python/task_service.py#L110)

```python
@property
def approval(self)
```

Читает ожидающее решение только выбранного owner; не возвращает approval другого чата.

### `TaskService.approval`

[Исходник](../../core/python/task_service.py#L115)

```python
@approval.setter
def approval(self, value)
```

Читает ожидающее решение только выбранного owner; не возвращает approval другого чата.

### `TaskService.handoff_pending`

[Исходник](../../core/python/task_service.py#L119)

```python
@property
def handoff_pending(self)
```

Проецирует передачу задачи Лолы выбранного owner и синхронизирует её явное удаление.

### `TaskService.handoff_pending`

[Исходник](../../core/python/task_service.py#L124)

```python
@handoff_pending.setter
def handoff_pending(self, value)
```

Проецирует передачу задачи Лолы выбранного owner и синхронизирует её явное удаление.

### `TaskService.idle`

[Исходник](../../core/python/task_service.py#L129)

```python
def idle(self)
```

Под RLock отказывает операции, пока task_running=True; после task_end живой завершающийся Thread не блокирует новый запрос.

### `TaskService.configure`

[Исходник](../../core/python/task_service.py#L134)

```python
def configure(self, params)
```

Разрешает идентичный повтор настроек без записи во время работы; изменения требуют глобального idle.

### `TaskService.preferences`

[Исходник](../../core/python/task_service.py#L145)

```python
def preferences(self)
```

Возвращает URL и модель без ключа.

### `TaskService.prepare_handoff`

[Исходник](../../core/python/task_service.py#L150)

```python
def prepare_handoff(self, root, params)
```

После завершения Лолы создаёт отдельный чат основной модели; IDE требует выбранного проекта, сохраняет источник результата.

### `TaskService.discard_handoff`

[Исходник](../../core/python/task_service.py#L163)

```python
def discard_handoff(self, params)
```

Удаляет pending передачу только по точному ID вне активной задачи, чтобы её можно было явно отклонить.

### `TaskService.companion_preferences`

[Исходник](../../core/python/task_service.py#L170)

```python
def companion_preferences(self)
```

Возвращает публичные поля отдельного профиля Лолы без API keys.

### `TaskService.configure_companion`

[Исходник](../../core/python/task_service.py#L173)

```python
def configure_companion(self, params)
```

Сохраняет независимый публичный профиль; ключи модели/STT оставляет только в памяти текущего Core.

### `TaskService.models`

[Исходник](../../core/python/task_service.py#L181)

```python
def models(self, config=None, cancelled=None)
```

Вызывает ограниченное отменяемое HTTPX-обнаружение моделей для копии настроек.

### `TaskService.diagnostic_config`

[Исходник](../../core/python/task_service.py#L184)

```python
def diagnostic_config(self, params=None)
```

Создаёт отдельную валидированную копию черновика либо текущих настроек, включая ключ только в памяти.

### `TaskService.start_model_probe`

[Исходник](../../core/python/task_service.py#L189)

```python
def start_model_probe(self, params, respond)
```

Запускает один фоновый worker проверки; запрещает параллельную проверку/активную задачу и фиксирует конфигурацию.

### `TaskService.start_model_probe.run_probe`

[Исходник](../../core/python/task_service.py#L200)

```python
def run_probe()
```

Вызывает probe_model и возвращает исходному RPC callback результат или ограниченную ошибку.

### `TaskService.cancel_model_setup`

[Исходник](../../core/python/task_service.py#L216)

```python
def cancel_model_setup(self)
```

Отменяет discovery и probe независимо от основной задачи агента.

### `TaskService.start_model_discovery`

[Исходник](../../core/python/task_service.py#L221)

```python
def start_model_discovery(self, respond, params=None)
```

Фиксирует копию настроек и запускает не больше одного discovery-потока, возвращающего ответ по исходному request ID.

### `TaskService.start_model_discovery.run_discovery`

[Исходник](../../core/python/task_service.py#L228)

```python
def run_discovery()
```

Получает список моделей или структурированную ошибку и вызывает callback ответа.

### `TaskService.chat`

[Исходник](../../core/python/task_service.py#L239)

```python
@property
def chat(self)
```

Совместимое свойство активного чата, фактическое состояние хранит SessionService.

### `TaskService.chat`

[Исходник](../../core/python/task_service.py#L243)

```python
@chat.setter
def chat(self, value)
```

Совместимое свойство активного чата, фактическое состояние хранит SessionService.

### `TaskService.project_id`

[Исходник](../../core/python/task_service.py#L247)

```python
@property
def project_id(self)
```

Совместимое свойство пространства, фактическое состояние хранит SessionService.

### `TaskService.project_id`

[Исходник](../../core/python/task_service.py#L251)

```python
@project_id.setter
def project_id(self, value)
```

Совместимое свойство пространства, фактическое состояние хранит SessionService.

### `TaskService.move_chat`

[Исходник](../../core/python/task_service.py#L254)

```python
def move_chat(self, params)
```

Переносит канонический чат между Chat и voice без удаления сообщений; проверяет исходную область и idle.

### `TaskService.chats`

[Исходник](../../core/python/task_service.py#L257)

```python
def chats(self, root, mode=None)
```

Фильтрует индекс чатов по точной строке выбранного корня.

### `TaskService.rename`

[Исходник](../../core/python/task_service.py#L260)

```python
def rename(self, root, params)
```

Проверяет idle/title/chat scope, сохраняет только новое название и синхронизирует title выбранного чата.

### `TaskService.select_chat`

[Исходник](../../core/python/task_service.py#L263)

```python
def select_chat(self, root, chat_id=None, mode=None)
```

Возвращает live snapshot с cursor вместо crash recovery для активного owner; новый/завершённый чат загружается отдельно.

### `TaskService._recover_chat`

[Исходник](../../core/python/task_service.py#L283)

```python
def _recover_chat(self)
```

Совместимый адаптер SessionService.recover.

### `TaskService._refresh_run_ledger`

[Исходник](../../core/python/task_service.py#L295)

```python
def _refresh_run_ledger(self, task)
```

Синхронизирует ledger и дочерние states из scoped registry после restart; чужие chat/run/parent записи игнорируются.

### `TaskService.workspace_changed`

[Исходник](../../core/python/task_service.py#L311)

```python
def workspace_changed(self, root)
```

После ручной записи пересчитывает evidence, сохраняет checkpoint и публикует отдельное scoped событие для idle UI.

### `TaskService.resolve_tool_recovery`

[Исходник](../../core/python/task_service.py#L324)

```python
def resolve_tool_recovery(self, params)
```

В idle проверяет выбранный чат, эпоху и call anchor, сохраняет наблюдение человека и возвращает обновлённые чат/task.

### `TaskService.start`

[Исходник](../../core/python/task_service.py#L344)

```python
def start(self, root, params)
```

Создаёт отдельный owner под RLock, запрещает дубликат чата/папки и разные model bindings, запускает поток без смены чужого состояния.

### `TaskService.update_plan`

[Исходник](../../core/python/task_service.py#L378)

```python
def update_plan(self, params)
```

В idle проверяет selected chat, валидирует и закрепляет пользовательский план, обновляет evidence и сохраняет checkpoint без HTTP/effects.

### `TaskService._persist_chat`

[Исходник](../../core/python/task_service.py#L397)

```python
def _persist_chat(self, *, checkpoint=False)
```

Сохраняет выбранный неисполняющийся чат после обновления workspace evidence, без использования run callbacks.

### `TaskService._event`

[Исходник](../../core/python/task_service.py#L401)

```python
def _event(self, event_type, **data)
```

Публикует workspace/warning событие координатора для выбранного чата; inference callbacks принадлежат TaskExecution.

### `TaskService._prune_runs`

[Исходник](../../core/python/task_service.py#L404)

```python
def _prune_runs(self)
```

Освобождает завершённые невыбранные owners после выхода их потока; durable история остаётся в SQLite.

### `TaskService.selected_run`

[Исходник](../../core/python/task_service.py#L410)

```python
def selected_run(self)
```

Находит владельца выбранного чата; не переключает состояние фоновых callbacks.

### `TaskService.active_runs`

[Исходник](../../core/python/task_service.py#L413)

```python
def active_runs(self)
```

Возвращает только безопасные метаданные активных чатов для навигации, без prompts, ключей и исходников.

### `TaskService.resolve_approval`

[Исходник](../../core/python/task_service.py#L419)

```python
def resolve_approval(self, params)
```

Передаёт решение выбранному owner, который проверяет точные run_id и approval_id.

### `TaskService.cancel`

[Исходник](../../core/python/task_service.py#L425)

```python
def cancel(self, params=None)
```

Останавливает только выбранный owner; устаревший run_id не затрагивает другой запуск.

### `TaskService.shutdown`

[Исходник](../../core/python/task_service.py#L435)

```python
def shutdown(self)
```

Закрывает приём новых задач, отменяет всех владельцев и ждёт их cleanup перед закрытием общих служб.

<a id="module-core-python-telegram-service-py"></a>

## `core/python/telegram_service.py`

Telegram long polling только для owner user ID: команды, состояние, ответы и текущие diff/approval; токен только в памяти Core.

### `TelegramService`

[Исходник](../../core/python/telegram_service.py#L11)

```python
class TelegramService
```

Владелец исходящего Telegram long polling; фильтрует owner ID/private chat и сериализует управление с Core.

### `TelegramService.__init__`

[Исходник](../../core/python/telegram_service.py#L12)

```python
def __init__(self, tasks, root, emit, start_task, control_context=None)
```

Инициализирует состояние экземпляра TelegramService; параметры показаны в сигнатуре, назначение описано у класса.

### `TelegramService.status`

[Исходник](../../core/python/telegram_service.py#L20)

```python
def status(self)
```

Возвращает состояние подключения, имя бота и owner ID без токена и URL с токеном.

### `TelegramService.start`

[Исходник](../../core/python/telegram_service.py#L25)

```python
def start(self, params)
```

Валидирует BotFather token и числовой owner ID, запускает один worker; токен хранит только в памяти.

### `TelegramService.api`

[Исходник](../../core/python/telegram_service.py#L40)

```python
def api(self, method, params=None)
```

Выполняет фиксированный запрос Telegram по TLS; необработанные HTTP exceptions не отправляются пользователю.

### `TelegramService.send`

[Исходник](../../core/python/telegram_service.py#L47)

```python
def send(self, text)
```

Отправляет plain text только owner, частями по 3500 символов, с общим лимитом 21000.

### `TelegramService.observe`

[Исходник](../../core/python/telegram_service.py#L53)

```python
def observe(self, event)
```

Ставит результаты удалённой задачи и approval уведомления в очередь до 100 записей, не блокируя Core HTTP.

### `TelegramService.command`

[Исходник](../../core/python/telegram_service.py#L64)

```python
def command(self, message)
```

Отбрасывает группы, посторонних и forwarded сообщения; под общим lock передаёт команду dispatcher.

### `TelegramService.dispatch`

[Исходник](../../core/python/telegram_service.py#L79)

```python
def dispatch(self, name, argument)
```

Реализует /status, /stop, /chat, /ide, /miya и точный /approve или /reject по актуальному ID.

### `TelegramService.poll`

[Исходник](../../core/python/telegram_service.py#L128)

```python
def poll(self)
```

Проверяет getMe, отбрасывает старую очередь, читает getUpdates и отправляет уведомления; повторяет сетевые ошибки без раскрытия токена.

### `TelegramService.stop`

[Исходник](../../core/python/telegram_service.py#L160)

```python
def stop(self)
```

Запрашивает отключение и закрывает HTTP client; токен не возвращает.

### `TelegramService.shutdown`

[Исходник](../../core/python/telegram_service.py#L167)

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

<a id="module-core-python-workspace-review-py"></a>

## `core/python/workspace_review.py`

Пользовательский API compare/preview/confirm/review; модели не получают инструмент отката.

### `WorkspaceReview`

[Исходник](../../core/python/workspace_review.py#L9)

```python
class WorkspaceReview
```

Ограниченный API пользовательского отката с одноразовым preview token на 120 секунд.

### `WorkspaceReview.__init__`

[Исходник](../../core/python/workspace_review.py#L10)

```python
def __init__(self, tasks)
```

Инициализирует состояние экземпляра WorkspaceReview; параметры показаны в сигнатуре, назначение описано у класса.

### `WorkspaceReview.scope`

[Исходник](../../core/python/workspace_review.py#L15)

```python
def scope(self, root, params, *, review=False)
```

Проверяет idle, IDE mode, chat/project/root и recovery gates; соседний чат не может применить чужой snapshot.

### `WorkspaceReview.list`

[Исходник](../../core/python/workspace_review.py#L25)

```python
def list(self, root, params)
```

Возвращает snapshots и восстановленный checkpoint выбранного IDE-чата.

### `WorkspaceReview.preview`

[Исходник](../../core/python/workspace_review.py#L32)

```python
def preview(self, root, params)
```

Проверяет все файлы и сохраняет proposal, привязанный к чату/root/group/fingerprint и сроку.

### `WorkspaceReview.apply`

[Исходник](../../core/python/workspace_review.py#L38)

```python
def apply(self, root, params)
```

Погашает подтверждение, выполняет повторную проверку и откат; обновляет устаревшую verification-проекцию из долговечного revision.

### `WorkspaceReview.review`

[Исходник](../../core/python/workspace_review.py#L55)

```python
def review(self, root, params)
```

При явном confirmed отмечает ручную проверку partial rollback; не повторяет filesystem effects.

### `WorkspaceReview.start_checkpoint`

[Исходник](../../core/python/workspace_review.py#L63)

```python
def start_checkpoint(self, root, params, respond)
```

Проверяет выбранный root/chat, затем запускает Git в существующем BackgroundJob без блокировки stdio dispatch.

### `WorkspaceReview.start_checkpoint.work`

[Исходник](../../core/python/workspace_review.py#L68)

```python
def work(context)
```

Создаёт private checkpoint только захваченного scope и group, с общим cancellation context.

### `WorkspaceReview.shutdown`

[Исходник](../../core/python/workspace_review.py#L73)

```python
def shutdown(self)
```

Отменяет собственные Git задачи при завершении Core.

<a id="module-main-py"></a>

## `main.py`

Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop.

Именованных классов/функций нет. Исполняемый entry point и константы описаны в главе о соответствующем слое.

<a id="module-prototypes-neutral-ide-install-test-extensions-py"></a>

## `prototypes/neutral-ide/install_test_extensions.py`

Установка закреплённых MIT Open VSX расширений и локального probe VSIX через настоящий CLI в отдельный test profile.

### `main`

[Исходник](../../prototypes/neutral-ide/install_test_extensions.py#L9)

```python
def main()
```

Сверяет VSIX SHA-256 и устанавливает фиксированные расширения и локальный probe в одноразовый профиль через Code-OSS CLI.

<a id="module-prototypes-neutral-ide-prepare-py"></a>

## `prototypes/neutral-ide/prepare.py`

Закреплённый Code-OSS/VSCodium ZIP, SHA-256, product/PE branding, ресурсы и установка встроенного extension без изменения пользовательского VS Code.

### `main`

[Исходник](../../prototypes/neutral-ide/prepare.py#L12)

```python
def main()
```

Проверяет upstream pin/archive и изолированно подготавливает Neutral runtime с лицензиями, иконкой и extension.

<a id="module-prototypes-neutral-ide-test-host-py"></a>

## `prototypes/neutral-ide/test_host.py`

Запуск настоящих Extension Host и normal-workbench UI тестов на одноразовых проектах; проверяет passed report, а не только exit code.

### `main`

[Исходник](../../prototypes/neutral-ide/test_host.py#L8)

```python
def main()
```

Создаёт одноразовый проект, запускает host или UI сценарий и требует успешный JSON report.

<a id="module-tools-audit-core-20261025-py"></a>

## `tools/audit_core_20261025.py`

Изолированные воспроизведения аудита Neutral 7: синтетические ответы модели и временные файлы, без изменения продукта или пользовательских данных.

### `chunk`

[Исходник](../../tools/audit_core_20261025.py#L29)

```python
def chunk(text=None, calls=None, finish='stop')
```

Создаёт синтетическое событие потока с явной причиной завершения для аудита.

### `tool`

[Исходник](../../tools/audit_core_20261025.py#L33)

```python
def tool(name, args, identity='call_a', index=0)
```

Создаёт синтетические аргументы вызова инструмента без его исполнения.

### `Stream`

[Исходник](../../tools/audit_core_20261025.py#L37)

```python
class Stream
```

Минимальный поток заранее заданных событий, без сетевого соединения.

### `Stream.__init__`

[Исходник](../../tools/audit_core_20261025.py#L38)

```python
def __init__(self, chunks)
```

Инициализирует состояние экземпляра Stream; параметры показаны в сигнатуре, назначение описано у класса.

### `Stream.__iter__`

[Исходник](../../tools/audit_core_20261025.py#L41)

```python
def __iter__(self)
```

Возвращает подготовленные события аудиторской фикстуры.

### `Stream.close`

[Исходник](../../tools/audit_core_20261025.py#L44)

```python
def close(self)
```

Имитирует закрытие потока; внешних ресурсов фикстура не создаёт.

### `engine_probe`

[Исходник](../../tools/audit_core_20261025.py#L48)

```python
def engine_probe(root, replies, prompt='Проверь результат', **options)
```

Запускает настоящий движок с синтетическим клиентом и временным TaskStore; возвращает статус, ошибки и использование verifier.

### `engine_probe.Client`

[Исходник](../../tools/audit_core_20261025.py#L49)

```python
class Client
```

Изолированный клиент фикстуры; ответы получаются из списка без HTTP.

### `engine_probe.Client.__init__`

[Исходник](../../tools/audit_core_20261025.py#L50)

```python
def __init__(self, *args, **kwargs)
```

Инициализирует состояние экземпляра engine_probe.Client; параметры показаны в сигнатуре, назначение описано у класса.

### `engine_probe.Client.create`

[Исходник](../../tools/audit_core_20261025.py#L53)

```python
def create(self, **kwargs)
```

Выдаёт следующий поток или положительный ответ фиктивной LLM-проверки, проверяя доверие движка к нему.

### `engine_probe.Client.close`

[Исходник](../../tools/audit_core_20261025.py#L58)

```python
def close(self)
```

Завершает фиктивный клиент без внешних ресурсов.

### `main`

[Исходник](../../tools/audit_core_20261025.py#L77)

```python
def main()
```

Собирает наблюдения о завершении, сжатии, восстановлении, схемах, MCP ID и endpoint credentials; выводит JSON, не объявляя найденные ошибки корректными.

<a id="module-tools-audit-post-stage8-py"></a>

## `tools/audit_post_stage8.py`

Read-only синтетический аудит границ tool parser, завершения потока, проверки записи, LSP и локальных файловых политик; не вызывает внешнюю модель и не изменяет проект.

### `SyntheticStream`

[Исходник](../../tools/audit_post_stage8.py#L25)

```python
class SyntheticStream
```

One controlled assistant chunk with no terminal finish_reason.

### `SyntheticStream.__init__`

[Исходник](../../tools/audit_post_stage8.py#L27)

```python
def __init__(self, text)
```

Инициализирует состояние экземпляра SyntheticStream; параметры показаны в сигнатуре, назначение описано у класса.

### `SyntheticStream.__iter__`

[Исходник](../../tools/audit_post_stage8.py#L28)

```python
def __iter__(self)
```

Return model data without using an HTTP endpoint.

### `SyntheticStream.close`

[Исходник](../../tools/audit_post_stage8.py#L31)

```python
def close(self)
```

Match the cancellable stream interface; no resource is held.

### `json_probes`

[Исходник](../../tools/audit_post_stage8.py#L36)

```python
def json_probes()
```

Observe trailing-data acceptance and manufactured completion for JSON calls.

### `json_probes.accepted`

[Исходник](../../tools/audit_post_stage8.py#L40)

```python
def accepted(text)
```

Observe rejection without turning a successful strict-parser guard into a probe crash.

### `eof_probe`

[Исходник](../../tools/audit_post_stage8.py#L49)

```python
def eof_probe(root)
```

Run the real engine with a synthetic EOF and its actual deterministic verifier.

### `eof_probe.Client`

[Исходник](../../tools/audit_post_stage8.py#L51)

```python
class Client
```

Offline substitute for HTTP only; the engine/verifier remain real.

### `eof_probe.Client.__init__`

[Исходник](../../tools/audit_post_stage8.py#L53)

```python
def __init__(self, *args, **kwargs)
```

Инициализирует состояние экземпляра eof_probe.Client; параметры показаны в сигнатуре, назначение описано у класса.

### `eof_probe.Client.create`

[Исходник](../../tools/audit_post_stage8.py#L54)

```python
def create(self, **params)
```

Produce a text reply that lacks a terminal completion status.

### `eof_probe.Client.close`

[Исходник](../../tools/audit_post_stage8.py#L57)

```python
def close(self)
```

No background transport is opened by the fixture.

### `eof_probe.Client.cancel`

[Исходник](../../tools/audit_post_stage8.py#L60)

```python
def cancel(self)
```

Satisfy engine cancellation without side effects.

### `edit_evidence_probe`

[Исходник](../../tools/audit_post_stage8.py#L71)

```python
def edit_evidence_probe(root)
```

Compare a synthetic command receipt with a real manual editor save.

### `lsp_probe`

[Исходник](../../tools/audit_post_stage8.py#L83)

```python
def lsp_probe(root)
```

Send empty then delayed nonempty publishDiagnostics through a real subprocess.

### `main`

[Исходник](../../tools/audit_post_stage8.py#L102)

```python
def main()
```

Print current observed gaps as JSON without changing production sources or data.

<a id="module-tools-benchmark-agent-py"></a>

## `tools/benchmark_agent.py`

Baseline 20a: owned synthetic repositories, frozen Agent/Core sources, real serial native/JSON runs, held-out arithmetic/diff/provenance/recovery checks and reports without editing user projects.

### `encode`

[Исходник](../../tools/benchmark_agent.py#L39)

```python
def encode(value)
```

Stable UTF-8 report representation without non-finite numbers.

### `save_report`

[Исходник](../../tools/benchmark_agent.py#L44)

```python
def save_report(path, value)
```

Replace one owned report atomically, retaining progress between cases.

### `case_outcome`

[Исходник](../../tools/benchmark_agent.py#L49)

```python
def case_outcome(case)
```

Keep task correctness separate from agent closure and a censored controlled experiment.

### `source_location_matches`

[Исходник](../../tools/benchmark_agent.py#L57)

```python
def source_location_matches(answer, location)
```

Match an actual relative path and whole line number, not :1 inside :10 or a different path.

### `write_summary`

[Исходник](../../tools/benchmark_agent.py#L62)

```python
def write_summary(output, report)
```

Render a human-readable result without implying failed tasks passed or benchmarks are universal.

### `snapshot_sources`

[Исходник](../../tools/benchmark_agent.py#L84)

```python
def snapshot_sources(output)
```

Freeze existing Agent/Core sources and exact hashes before application changes.

### `build_project`

[Исходник](../../tools/benchmark_agent.py#L96)

```python
def build_project(root, size)
```

Create deterministic owned fixture files with no dependency installation.

### `reset_project`

[Исходник](../../tools/benchmark_agent.py#L110)

```python
def reset_project(root)
```

Restore only known files in a benchmark-owned root, never recursively delete paths.

### `search_measurement`

[Исходник](../../tools/benchmark_agent.py#L120)

```python
def search_measurement(root, repetitions=9)
```

Measure existing lexical search; distinguish top-k recall from full corpus coverage.

### `fixture_validation`

[Исходник](../../tools/benchmark_agent.py#L136)

```python
def fixture_validation(root, case)
```

Validate a held-out pure-arithmetic contract without executing arbitrary model code.

### `model_metadata`

[Исходник](../../tools/benchmark_agent.py#L168)

```python
def model_metadata(base_url, model)
```

Read loaded model metadata only; refuse a baseline that would silently trigger a JIT load.

### `resource_sample`

[Исходник](../../tools/benchmark_agent.py#L180)

```python
def resource_sample()
```

Read whole-device VRAM; unavailable telemetry remains null rather than invented.

### `run_case`

[Исходник](../../tools/benchmark_agent.py#L190)

```python
def run_case(root, case, connection, profile)
```

Exercise the existing Engine/JSON/approval/journal pipeline, serially and within fixtures.

### `run_case.MeasuredClient`

[Исходник](../../tools/benchmark_agent.py#L197)

```python
class MeasuredClient(ModelClient)
```

Count physical inference POST attempts, including retries and auxiliary generations.

### `run_case.MeasuredClient.__init__`

[Исходник](../../tools/benchmark_agent.py#L199)

```python
def __init__(self, *args, **kwargs)
```

Инициализирует состояние экземпляра run_case.MeasuredClient; параметры показаны в сигнатуре, назначение описано у класса.

### `run_case.MeasuredClient.__init__.request_hook`

[Исходник](../../tools/benchmark_agent.py#L201)

```python
async def request_hook(request)
```

Count inference attempts without recording headers or secrets.

### `run_case.MeasuredClient.create`

[Исходник](../../tools/benchmark_agent.py#L208)

```python
def create(self, **params)
```

Fix generation seed for a reproducible controlled baseline.

### `run_case.execute`

[Исходник](../../tools/benchmark_agent.py#L215)

```python
def execute(interrupt=False)
```

Run one isolated generation sequence; approvals are limited to the known fixture sources.

### `run_case.execute.approve`

[Исходник](../../tools/benchmark_agent.py#L226)

```python
def approve(path, diff, exists)
```

Consent only to edits of this fixture's two arithmetic source files.

### `run_benchmark`

[Исходник](../../tools/benchmark_agent.py#L277)

```python
def run_benchmark(output, base_url, model, protocol, sizes, cases, live, context_pack=False, indexed=False, budget_mode='manual')
```

Persist a baseline incrementally, with explicit live-model versus deterministic coverage.

### `main`

[Исходник](../../tools/benchmark_agent.py#L320)

```python
def main()
```

Create a fresh report directory; model execution is explicitly opt-in.

<a id="module-tools-benchmark-project-index-py"></a>

## `tools/benchmark_project_index.py`

Воспроизводимые fresh synthetic корпуса baseline 20a и измерения индекса 40/1200/12000 файлов: Recall, p50/p95, update, CPU/RAM/cache.

### `process_memory`

[Исходник](../../tools/benchmark_project_index.py#L17)

```python
def process_memory()
```

Read Windows process working set and lifetime peak; these are not isolated index metrics.

### `process_memory.Counters`

[Исходник](../../tools/benchmark_project_index.py#L21)

```python
class Counters(ctypes.Structure)
```

PROCESS_MEMORY_COUNTERS with pointer-width SIZE_T fields.

### `wait_ready`

[Исходник](../../tools/benchmark_project_index.py#L32)

```python
def wait_ready(index, seconds=60)
```

Wait while the scan makes progress; failed/partial/stalled states never pass.

### `benchmark`

[Исходник](../../tools/benchmark_project_index.py#L44)

```python
def benchmark(output)
```

Create new fixtures, measure warm retrieval, then observe one external edit per size.

<a id="module-tools-benchmark-storage-py"></a>

## `tools/benchmark_storage.py`

Воспроизводимый локальный benchmark на синтетических JSON-чатах: перенос, p50/p95 списка и поиска.

### `measure`

[Исходник](../../tools/benchmark_storage.py#L14)

```python
def measure(operation, repetitions=12)
```

Return median and nearest-rank p95 in milliseconds, with warm caches explicit.

### `benchmark`

[Исходник](../../tools/benchmark_storage.py#L24)

```python
def benchmark(chats=2000, messages=25)
```

Build mixed Chat/IDE/voice JSON, copy-migrate, then compare equivalent lists.

### `benchmark.legacy_catalog`

[Исходник](../../tools/benchmark_storage.py#L40)

```python
def legacy_catalog()
```

Match the previous listing cost: decode every complete JSON transcript.

### `main`

[Исходник](../../tools/benchmark_storage.py#L59)

```python
def main()
```

Write reproducible machine-readable measurements without user history or secrets.

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

[Исходник](../../tools/doc_notes.py#L189)

```python
def register(module, text)
```

Добавляет вручную написанные строки «имя | назначение» в словарь аннотаций.

<a id="module-tools-generate-brand-icons-py"></a>

## `tools/generate_brand_icons.py`

Разработка: рендер SVG через Qt и запись PNG/многоразмерного ICO без Pillow.

### `main`

[Исходник](../../tools/generate_brand_icons.py#L9)

```python
def main()
```

Рендерит SVG в 512px PNG и записывает ICO directory/PNG-кадры семи разрешений для Windows.

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

[Исходник](../../tools/generate_code_reference.py#L71)

```python
def python_symbols(path)
```

Извлекает классы, функции, методы и вложенные объявления Python с реальными строками.

### `python_symbols.visit`

[Исходник](../../tools/generate_code_reference.py#L76)

```python
def visit(node, scope=())
```

Рекурсивно обходит объявления, сохраняя квалифицированное имя родителя.

### `symbol_description`

[Исходник](../../tools/generate_code_reference.py#L100)

```python
def symbol_description(file, symbol)
```

Подбирает проверяемую ручную аннотацию; отсутствие назначения рабочего символа — ошибка.

### `markdown_symbol`

[Исходник](../../tools/generate_code_reference.py#L125)

```python
def markdown_symbol(file, symbol, description, language)
```

Формирует блок объявления с сигнатурой, назначением и ссылкой на строку исходника.

### `module_anchor`

[Исходник](../../tools/generate_code_reference.py#L135)

```python
def module_anchor(file)
```

Создаёт стабильный ASCII-якорь модуля для оглавления больших справочников.

### `render`

[Исходник](../../tools/generate_code_reference.py#L140)

```python
def render()
```

Строит содержимое всех справочников без изменения файлов рабочего приложения.

### `main`

[Исходник](../../tools/generate_code_reference.py#L216)

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

<a id="module-tools-test-agent-readiness-py"></a>

## `tools/test_agent_readiness.py`

Запускает изолированный набор готовности и сохраняет JSON со статусом, временем и ошибками каждого теста.

### `EvidenceResult`

[Исходник](../../tools/test_agent_readiness.py#L25)

```python
class EvidenceResult(unittest.TextTestResult)
```

Keep test outcomes and timings alongside unittest's traceback log.

### `EvidenceResult.__init__`

[Исходник](../../tools/test_agent_readiness.py#L27)

```python
def __init__(self, *args, **kwargs)
```

Инициализирует состояние экземпляра EvidenceResult; параметры показаны в сигнатуре, назначение описано у класса.

### `EvidenceResult.startTest`

[Исходник](../../tools/test_agent_readiness.py#L31)

```python
def startTest(self, test)
```

Запоминает идентификатор, ожидание и начальный момент теста.

### `EvidenceResult.addFailure`

[Исходник](../../tools/test_agent_readiness.py#L37)

```python
def addFailure(self, test, err)
```

Сохраняет assertion traceback и FAILED в отчёте.

### `EvidenceResult.addError`

[Исходник](../../tools/test_agent_readiness.py#L41)

```python
def addError(self, test, err)
```

Сохраняет исключение инфраструктуры или теста и FAILED в отчёте.

### `EvidenceResult.addSkip`

[Исходник](../../tools/test_agent_readiness.py#L45)

```python
def addSkip(self, test, reason)
```

Отмечает непройденный сценарий UNVERIFIED с причиной пропуска.

### `EvidenceResult.addSubTest`

[Исходник](../../tools/test_agent_readiness.py#L49)

```python
def addSubTest(self, test, subtest, err)
```

Переносит ошибку subTest в общий статус тестового сценария.

### `EvidenceResult.stopTest`

[Исходник](../../tools/test_agent_readiness.py#L53)

```python
def stopTest(self, test)
```

Завершает измерение времени и добавляет запись в JSON evidence.

### `main`

[Исходник](../../tools/test_agent_readiness.py#L59)

```python
def main()
```

Use a fresh profile and writable temp root; never inherit the user's Neutral data.

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
