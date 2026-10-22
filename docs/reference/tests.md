# Справочник Python-тестов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [tests/migration/test_bridge.py](#module-tests-migration-test-bridge-py)
- [tests/migration/test_bridge_process.py](#module-tests-migration-test-bridge-process-py)
- [tests/migration/test_streaming.py](#module-tests-migration-test-streaming-py)
- [tests/migration/test_task_service.py](#module-tests-migration-test-task-service-py)
- [tests/test_approval_flow.py](#module-tests-test-approval-flow-py)
- [tests/test_chat_store.py](#module-tests-test-chat-store-py)
- [tests/test_conversation_history.py](#module-tests-test-conversation-history-py)
- [tests/test_editor_io.py](#module-tests-test-editor-io-py)
- [tests/test_file_editing.py](#module-tests-test-file-editing-py)
- [tests/test_limits.py](#module-tests-test-limits-py)
- [tests/test_model_gateway.py](#module-tests-test-model-gateway-py)
- [tests/test_model_manager.py](#module-tests-test-model-manager-py)
- [tests/test_model_preferences.py](#module-tests-test-model-preferences-py)
- [tests/test_project_memory.py](#module-tests-test-project-memory-py)
- [tests/test_runtime_architecture.py](#module-tests-test-runtime-architecture-py)
- [tests/test_sandbox.py](#module-tests-test-sandbox-py)
- [tests/test_task_store.py](#module-tests-test-task-store-py)

<a id="module-tests-migration-test-bridge-py"></a>

## `tests/migration/test_bridge.py`

Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи.

### `BridgeTests`

[Исходник](../../tests/migration/test_bridge.py#L12)

```python
class BridgeTests(unittest.TestCase)
```

Тестовый класс/фикстура: Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи.

### `BridgeTests.setUp`

[Исходник](../../tests/migration/test_bridge.py#L13)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BridgeTests.tearDown`

[Исходник](../../tests/migration/test_bridge.py#L18)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `BridgeTests.test_health`

[Исходник](../../tests/migration/test_bridge.py#L21)

```python
def test_health(self)
```

Проверка: Bridge сообщает доступность процесса.

### `BridgeTests.test_list_and_read`

[Исходник](../../tests/migration/test_bridge.py#L23)

```python
def test_list_and_read(self)
```

Проверка: Bridge перечисляет и читает файл выбранного проекта.

### `BridgeTests.test_parent_traversal_rejected`

[Исходник](../../tests/migration/test_bridge.py#L26)

```python
def test_parent_traversal_rejected(self)
```

Проверка: Bridge не разрешает ../ за пределами проекта.

### `BridgeTests.test_write_is_not_exposed`

[Исходник](../../tests/migration/test_bridge.py#L28)

```python
def test_write_is_not_exposed(self)
```

Проверка: Прямого write_file RPC в bridge нет.

<a id="module-tests-migration-test-bridge-process-py"></a>

## `tests/migration/test_bridge_process.py`

Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.

### `BridgeProcessTests`

[Исходник](../../tests/migration/test_bridge_process.py#L17)

```python
class BridgeProcessTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.

### `BridgeProcessTests.setUp`

[Исходник](../../tests/migration/test_bridge_process.py#L18)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BridgeProcessTests.read_output`

[Исходник](../../tests/migration/test_bridge_process.py#L31)

```python
def read_output(self)
```

Читает JSON-строки stdout тестового subprocess в очередь.

### `BridgeProcessTests.tearDown`

[Исходник](../../tests/migration/test_bridge_process.py#L38)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `BridgeProcessTests.until`

[Исходник](../../tests/migration/test_bridge_process.py#L50)

```python
def until(self, predicate)
```

Ожидает подходящее сообщение, сохраняя остальные для дальнейших проверок.

### `BridgeProcessTests.call`

[Исходник](../../tests/migration/test_bridge_process.py#L61)

```python
def call(self, method, **params)
```

Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.

### `BridgeProcessTests.test_malformed_input_does_not_reuse_previous_request_id`

[Исходник](../../tests/migration/test_bridge_process.py#L68)

```python
def test_malformed_input_does_not_reuse_previous_request_id(self)
```

Проверка: Ошибка JSON не получает ID предыдущей команды и не ломает следующий запрос.

### `BridgeProcessTests.test_bridge_remains_responsive_during_write_approval`

[Исходник](../../tests/migration/test_bridge_process.py#L77)

```python
def test_bridge_remains_responsive_during_write_approval(self)
```

Проверка: Реальный Core отвечает на health/cancel, пока engine ждёт согласия.

<a id="module-tests-migration-test-streaming-py"></a>

## `tests/migration/test_streaming.py`

Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки.

### `SlowHandler`

[Исходник](../../tests/migration/test_streaming.py#L18)

```python
class SlowHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки.

### `SlowHandler.log_message`

[Исходник](../../tests/migration/test_streaming.py#L19)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `SlowHandler.chunk`

[Исходник](../../tests/migration/test_streaming.py#L22)

```python
def chunk(self, text)
```

Пишет один SSE-чанк тестового текстового ответа.

### `SlowHandler.wait_for_disconnect`

[Исходник](../../tests/migration/test_streaming.py#L28)

```python
def wait_for_disconnect(self)
```

На стороне fixture ожидает реального закрытия клиентского сокета.

### `SlowHandler.do_POST`

[Исходник](../../tests/migration/test_streaming.py#L39)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `StreamingTests`

[Исходник](../../tests/migration/test_streaming.py#L67)

```python
class StreamingTests(unittest.TestCase)
```

Тестовый класс/фикстура: Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки.

### `StreamingTests.setUp`

[Исходник](../../tests/migration/test_streaming.py#L68)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `StreamingTests.tearDown`

[Исходник](../../tests/migration/test_streaming.py#L91)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `StreamingTests.start`

[Исходник](../../tests/migration/test_streaming.py#L104)

```python
def start(self, mode, auto_memory=False)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `StreamingTests.stop_and_assert`

[Исходник](../../tests/migration/test_streaming.py#L114)

```python
def stop_and_assert(self)
```

Отменяет engine и проверяет время завершения, закрытие сокета и paused checkpoint.

### `StreamingTests.test_cancel_before_server_returns_headers`

[Исходник](../../tests/migration/test_streaming.py#L124)

```python
def test_cancel_before_server_returns_headers(self)
```

Проверка: Отмена закрывает TCP до HTTP-заголовков без ожидания network timeout.

### `StreamingTests.test_cancel_during_stalled_sse_preserves_displayed_text`

[Исходник](../../tests/migration/test_streaming.py#L129)

```python
def test_cancel_during_stalled_sse_preserves_displayed_text(self)
```

Проверка: Отмена закрывает зависший SSE и сохраняет уже показанный текст.

### `StreamingTests.test_text_arrives_before_response_finishes`

[Исходник](../../tests/migration/test_streaming.py#L136)

```python
def test_text_arrives_before_response_finishes(self)
```

Проверка: Первый чанк виден раньше завершения модельного ответа.

### `StreamingTests.test_cancel_memory_request_does_not_mark_task_completed`

[Исходник](../../tests/migration/test_streaming.py#L148)

```python
def test_cancel_memory_request_does_not_mark_task_completed(self)
```

Проверка: Отмена необязательного memory-запроса оставляет task paused.

### `StreamingTests.test_preferences_reload_does_not_restore_api_key`

[Исходник](../../tests/migration/test_streaming.py#L153)

```python
def test_preferences_reload_does_not_restore_api_key(self)
```

Проверка: Новый сервис восстанавливает URL/модель, но не ключ.

### `StreamingTests.test_service_flushes_buffer_during_pause_and_final_uses_same_message_id`

[Исходник](../../tests/migration/test_streaming.py#L161)

```python
def test_service_flushes_buffer_during_pause_and_final_uses_same_message_id(self)
```

Проверка: Таймер допечатывает буфер при паузе и связывает финал с тем же bubble ID.

<a id="module-tests-migration-test-task-service-py"></a>

## `tests/migration/test_task_service.py`

HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `ModelHandler`

[Исходник](../../tests/migration/test_task_service.py#L15)

```python
class ModelHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `ModelHandler.log_message`

[Исходник](../../tests/migration/test_task_service.py#L16)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ModelHandler.do_GET`

[Исходник](../../tests/migration/test_task_service.py#L19)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `ModelHandler.do_POST`

[Исходник](../../tests/migration/test_task_service.py#L25)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `TaskServiceTests`

[Исходник](../../tests/migration/test_task_service.py#L49)

```python
class TaskServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `TaskServiceTests.setUpClass`

[Исходник](../../tests/migration/test_task_service.py#L51)

```python
@classmethod
def setUpClass(cls)
```

Создаёт общую HTTP-фикстуру и её поток для класса тестов.

### `TaskServiceTests.tearDownClass`

[Исходник](../../tests/migration/test_task_service.py#L58)

```python
@classmethod
def tearDownClass(cls)
```

Останавливает общий сервер и ждёт его поток.

### `TaskServiceTests.setUp`

[Исходник](../../tests/migration/test_task_service.py#L63)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TaskServiceTests.tearDown`

[Исходник](../../tests/migration/test_task_service.py#L79)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TaskServiceTests.event`

[Исходник](../../tests/migration/test_task_service.py#L85)

```python
def event(self, name)
```

Читает события до нужного имени и немедленно проваливает тест при failed.

### `TaskServiceTests.start`

[Исходник](../../tests/migration/test_task_service.py#L93)

```python
def start(self)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `TaskServiceTests.resolve`

[Исходник](../../tests/migration/test_task_service.py#L101)

```python
def resolve(self, approval, decision)
```

Передаёт проверяемое решение по предложению в TaskService.

### `TaskServiceTests.test_apply_only_after_matching_approval_and_persist_history`

[Исходник](../../tests/migration/test_task_service.py#L104)

```python
def test_apply_only_after_matching_approval_and_persist_history(self)
```

Проверка: Запись происходит после совпавших run/proposal ID, а история и завершение сохраняются.

### `TaskServiceTests.test_reject_does_not_write`

[Исходник](../../tests/migration/test_task_service.py#L120)

```python
def test_reject_does_not_write(self)
```

Проверка: Отказ и устаревшее подтверждение не создают файл.

### `TaskServiceTests.test_resume_preserves_task_and_recovery_marks_interrupted_task_paused`

[Исходник](../../tests/migration/test_task_service.py#L129)

```python
def test_resume_preserves_task_and_recovery_marks_interrupted_task_paused(self)
```

Проверка: Running после сбоя восстанавливается как paused и поддерживает новую попытку.

### `TaskServiceTests.test_new_prompt_after_pause_creates_new_task`

[Исходник](../../tests/migration/test_task_service.py#L146)

```python
def test_new_prompt_after_pause_creates_new_task(self)
```

Проверка: Новый prompt не выдаётся за продолжение старой задачи.

### `TaskServiceTests.test_cancel_while_waiting_pauses_task_and_unblocks_worker`

[Исходник](../../tests/migration/test_task_service.py#L158)

```python
def test_cancel_while_waiting_pauses_task_and_unblocks_worker(self)
```

Проверка: Отмена освобождает approval wait и сохраняет paused.

### `TaskServiceTests.test_busy_task_rejects_chat_and_configuration_changes`

[Исходник](../../tests/migration/test_task_service.py#L167)

```python
def test_busy_task_rejects_chat_and_configuration_changes(self)
```

Проверка: Активная задача запрещает смену чата, config и второй запуск.

### `TaskServiceTests.test_chats_are_scoped_to_project_and_ids_cannot_escape_store`

[Исходник](../../tests/migration/test_task_service.py#L176)

```python
def test_chats_are_scoped_to_project_and_ids_cannot_escape_store(self)
```

Проверка: ID и принадлежность проекта проверяются до загрузки чата.

### `TaskServiceTests.test_models_and_configuration_do_not_return_key`

[Исходник](../../tests/migration/test_task_service.py#L184)

```python
def test_models_and_configuration_do_not_return_key(self)
```

Проверка: Список моделей работает, а configuration response не содержит ключ.

### `TaskServiceTests.test_missing_model_and_bad_url_are_rejected`

[Исходник](../../tests/migration/test_task_service.py#L189)

```python
def test_missing_model_and_bad_url_are_rejected(self)
```

Проверка: Запуск без модели и неверные URL отклоняются.

<a id="module-tests-test-approval-flow-py"></a>

## `tests/test_approval_flow.py`

Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6.

### `ApprovalFlowTest`

[Исходник](../../tests/test_approval_flow.py#L11)

```python
@unittest.skipIf(AgentWorker is None, 'PySide6 is not installed in the test environment')
class ApprovalFlowTest(unittest.TestCase)
```

Тестовый класс/фикстура: Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6.

### `ApprovalFlowTest.test_approval_decisions_are_explicit`

[Исходник](../../tests/test_approval_flow.py#L12)

```python
def test_approval_decisions_are_explicit(self)
```

Проверка: Решения apply/reject/cancel явно доходят до Qt-адаптера движка.

<a id="module-tests-test-chat-store-py"></a>

## `tests/test_chat_store.py`

Создание, изменение, переименование и удаление чата в изолированном store.

### `ChatStoreTest`

[Исходник](../../tests/test_chat_store.py#L7)

```python
class ChatStoreTest(unittest.TestCase)
```

Тестовый класс/фикстура: Создание, изменение, переименование и удаление чата в изолированном store.

### `ChatStoreTest.test_create_save_load_rename_delete`

[Исходник](../../tests/test_chat_store.py#L8)

```python
def test_create_save_load_rename_delete(self)
```

Проверка: Полный жизненный цикл записи чата и индекса.

<a id="module-tests-test-conversation-history-py"></a>

## `tests/test_conversation_history.py`

Выбор истории и сокращение tool outputs/пар в conversation.py.

### `ConversationHistoryTests`

[Исходник](../../tests/test_conversation_history.py#L6)

```python
class ConversationHistoryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Выбор истории и сокращение tool outputs/пар в conversation.py.

### `ConversationHistoryTests.test_followup_keeps_previous_user_and_assistant_messages`

[Исходник](../../tests/test_conversation_history.py#L7)

```python
def test_followup_keeps_previous_user_and_assistant_messages(self)
```

Проверка: Повторный запрос сохраняет недавний контекст диалога.

### `ConversationHistoryTests.test_tool_call_and_tool_result_are_preserved`

[Исходник](../../tests/test_conversation_history.py#L18)

```python
def test_tool_call_and_tool_result_are_preserved(self)
```

Проверка: Связанные вызов и ответ инструмента сохраняются вместе.

### `ConversationHistoryTests.test_empty_history_starts_cleanly`

[Исходник](../../tests/test_conversation_history.py#L29)

```python
def test_empty_history_starts_cleanly(self)
```

Проверка: Пустая история создаёт корректный первый запрос.

### `ConversationHistoryTests.test_old_turns_are_trimmed_but_recent_confirmation_context_remains`

[Исходник](../../tests/test_conversation_history.py#L33)

```python
def test_old_turns_are_trimmed_but_recent_confirmation_context_remains(self)
```

Проверка: Старые ходы сокращаются без потери недавнего контекста согласия.

### `ConversationHistoryTests.test_live_compaction_preserves_system_original_request_and_recent_tool_pair`

[Исходник](../../tests/test_conversation_history.py#L50)

```python
def test_live_compaction_preserves_system_original_request_and_recent_tool_pair(self)
```

Проверка: compact_live_messages сохраняет system, исходный запрос и недавнюю tool-пару.

### `ConversationHistoryTests.test_tool_results_are_bounded_without_dropping_tool_call_pair`

[Исходник](../../tests/test_conversation_history.py#L66)

```python
def test_tool_results_are_bounded_without_dropping_tool_call_pair(self)
```

Проверка: Большой tool output ограничивается без удаления связанной структуры.

<a id="module-tests-test-editor-io-py"></a>

## `tests/test_editor_io.py`

Чтение/сохранение существующих файлов, размер и отказ вне корня.

### `EditorIOTests`

[Исходник](../../tests/test_editor_io.py#L8)

```python
class EditorIOTests(unittest.TestCase)
```

Тестовый класс/фикстура: Чтение/сохранение существующих файлов, размер и отказ вне корня.

### `EditorIOTests.setUp`

[Исходник](../../tests/test_editor_io.py#L9)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `EditorIOTests.tearDown`

[Исходник](../../tests/test_editor_io.py#L18)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `EditorIOTests.test_read_and_save_inside_project`

[Исходник](../../tests/test_editor_io.py#L21)

```python
def test_read_and_save_inside_project(self)
```

Проверка: Editor I/O читает и сохраняет файл внутри корня.

### `EditorIOTests.test_outside_file_is_denied_for_read_and_write`

[Исходник](../../tests/test_editor_io.py#L28)

```python
def test_outside_file_is_denied_for_read_and_write(self)
```

Проверка: Editor I/O отклоняет чтение и запись вне корня.

### `EditorIOTests.test_oversized_file_is_rejected`

[Исходник](../../tests/test_editor_io.py#L35)

```python
def test_oversized_file_is_rejected(self)
```

Проверка: Editor I/O отклоняет слишком большой файл.

### `EditorIOTests.test_nonexistent_file_cannot_be_saved`

[Исходник](../../tests/test_editor_io.py#L39)

```python
def test_nonexistent_file_cannot_be_saved(self)
```

Проверка: Editor I/O не создаёт отсутствующий файл через save.

<a id="module-tests-test-file-editing-py"></a>

## `tests/test_file_editing.py`

Preview без записи, explicit approval, overwrite и путь файла.

### `FileEditingTests`

[Исходник](../../tests/test_file_editing.py#L9)

```python
class FileEditingTests(unittest.TestCase)
```

Тестовый класс/фикстура: Preview без записи, explicit approval, overwrite и путь файла.

### `FileEditingTests.setUp`

[Исходник](../../tests/test_file_editing.py#L10)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `FileEditingTests.tearDown`

[Исходник](../../tests/test_file_editing.py#L18)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `FileEditingTests.test_preview_does_not_write`

[Исходник](../../tests/test_file_editing.py#L21)

```python
def test_preview_does_not_write(self)
```

Проверка: Расчёт diff не меняет файловую систему.

### `FileEditingTests.test_write_file_denies_without_explicit_approval`

[Исходник](../../tests/test_file_editing.py#L27)

```python
def test_write_file_denies_without_explicit_approval(self)
```

Проверка: Неподтверждённая запись отклоняется по умолчанию.

### `FileEditingTests.test_create_new_file`

[Исходник](../../tests/test_file_editing.py#L33)

```python
def test_create_new_file(self)
```

Проверка: Подтверждённая запись создаёт новый файл.

### `FileEditingTests.test_existing_file_requires_overwrite_flag`

[Исходник](../../tests/test_file_editing.py#L38)

```python
def test_existing_file_requires_overwrite_flag(self)
```

Проверка: Существующий файл требует явного overwrite.

### `FileEditingTests.test_overwrite_existing_file`

[Исходник](../../tests/test_file_editing.py#L43)

```python
def test_overwrite_existing_file(self)
```

Проверка: Подтверждённая разрешённая замена меняет существующий текст.

### `FileEditingTests.test_outside_path_denied`

[Исходник](../../tests/test_file_editing.py#L48)

```python
def test_outside_path_denied(self)
```

Проверка: Запись вне корня не допускается.

### `FileEditingTests.test_dispatch_write_requires_approval`

[Исходник](../../tests/test_file_editing.py#L52)

```python
def test_dispatch_write_requires_approval(self)
```

Проверка: Dispatcher также не обходит approval.

<a id="module-tests-test-limits-py"></a>

## `tests/test_limits.py`

Настраиваемое число entries и глубина обхода.

### `ConfigurableLimitsTests`

[Исходник](../../tests/test_limits.py#L8)

```python
class ConfigurableLimitsTests(unittest.TestCase)
```

Тестовый класс/фикстура: Настраиваемое число entries и глубина обхода.

### `ConfigurableLimitsTests.setUp`

[Исходник](../../tests/test_limits.py#L9)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ConfigurableLimitsTests.tearDown`

[Исходник](../../tests/test_limits.py#L19)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ConfigurableLimitsTests.test_list_files_obeys_entry_limit`

[Исходник](../../tests/test_limits.py#L22)

```python
def test_list_files_obeys_entry_limit(self)
```

Проверка: Перечисление ограничивается настроенным количеством записей.

### `ConfigurableLimitsTests.test_recursive_search_obeys_depth_limit`

[Исходник](../../tests/test_limits.py#L28)

```python
def test_recursive_search_obeys_depth_limit(self)
```

Проверка: Поиск учитывает предел глубины.

<a id="module-tests-test-model-gateway-py"></a>

## `tests/test_model_gateway.py`

Параметры endpoint удалённого/совместимого провайдера.

### `ModelGatewayTests`

[Исходник](../../tests/test_model_gateway.py#L6)

```python
class ModelGatewayTests(unittest.TestCase)
```

Тестовый класс/фикстура: Параметры endpoint удалённого/совместимого провайдера.

### `ModelGatewayTests.test_remote_endpoint`

[Исходник](../../tests/test_model_gateway.py#L7)

```python
def test_remote_endpoint(self)
```

Проверка: Gateway создаёт правильный URL, ID и provider-флаги.

<a id="module-tests-test-model-manager-py"></a>

## `tests/test_model_manager.py`

Сканирование GGUF, quantization, свободный порт и остановленный runtime.

### `ModelManagerTests`

[Исходник](../../tests/test_model_manager.py#L7)

```python
class ModelManagerTests(unittest.TestCase)
```

Тестовый класс/фикстура: Сканирование GGUF, quantization, свободный порт и остановленный runtime.

### `ModelManagerTests.test_scan_gguf_and_quantization`

[Исходник](../../tests/test_model_manager.py#L8)

```python
def test_scan_gguf_and_quantization(self)
```

Проверка: Сканирование выбирает GGUF и извлекает quantization из имени.

### `ModelManagerTests.test_free_port_is_valid`

[Исходник](../../tests/test_model_manager.py#L18)

```python
def test_free_port_is_valid(self)
```

Проверка: Полученный порт находится в допустимом диапазоне.

### `ModelManagerTests.test_status_stopped`

[Исходник](../../tests/test_model_manager.py#L23)

```python
def test_status_stopped(self)
```

Проверка: Остановленный LocalRuntime не объявляет себя running.

<a id="module-tests-test-model-preferences-py"></a>

## `tests/test_model_preferences.py`

Whitelist настроек, defaults и отказ URL с credentials/неверным портом.

### `ModelPreferencesTests`

[Исходник](../../tests/test_model_preferences.py#L9)

```python
class ModelPreferencesTests(unittest.TestCase)
```

Тестовый класс/фикстура: Whitelist настроек, defaults и отказ URL с credentials/неверным портом.

### `ModelPreferencesTests.setUp`

[Исходник](../../tests/test_model_preferences.py#L10)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ModelPreferencesTests.tearDown`

[Исходник](../../tests/test_model_preferences.py#L16)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ModelPreferencesTests.test_roundtrip_whitelists_nonsecret_fields`

[Исходник](../../tests/test_model_preferences.py#L20)

```python
def test_roundtrip_whitelists_nonsecret_fields(self)
```

Проверка: Preferences сохраняет и читает только URL/модель, отбрасывает ключ и посторонние поля.

### `ModelPreferencesTests.test_missing_corrupted_or_wrong_shape_uses_defaults`

[Исходник](../../tests/test_model_preferences.py#L27)

```python
def test_missing_corrupted_or_wrong_shape_uses_defaults(self)
```

Проверка: Отсутствующие/повреждённые preferences дают defaults.

### `ModelPreferencesTests.test_credentials_or_invalid_ports_do_not_replace_saved_preferences`

[Исходник](../../tests/test_model_preferences.py#L34)

```python
def test_credentials_or_invalid_ports_do_not_replace_saved_preferences(self)
```

Проверка: Плохой URL не заменяет ранее сохранённые настройки.

<a id="module-tests-test-project-memory-py"></a>

## `tests/test_project_memory.py`

Изоляция, лимиты, merge, формат контекста и очистка памяти.

### `ProjectMemoryTests`

[Исходник](../../tests/test_project_memory.py#L10)

```python
class ProjectMemoryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Изоляция, лимиты, merge, формат контекста и очистка памяти.

### `ProjectMemoryTests.test_round_trip_is_project_scoped`

[Исходник](../../tests/test_project_memory.py#L11)

```python
def test_round_trip_is_project_scoped(self)
```

Проверка: Память одного проекта не смешивается с другим.

### `ProjectMemoryTests.test_validation_limits_and_deduplicates`

[Исходник](../../tests/test_project_memory.py#L21)

```python
def test_validation_limits_and_deduplicates(self)
```

Проверка: Поля памяти ограничиваются и очищаются от дубликатов.

### `ProjectMemoryTests.test_context_is_compact_and_marked_as_reference`

[Исходник](../../tests/test_project_memory.py#L26)

```python
def test_context_is_compact_and_marked_as_reference(self)
```

Проверка: Память форматируется как ограниченная справочная информация.

### `ProjectMemoryTests.test_merge_preserves_missing_fields`

[Исходник](../../tests/test_project_memory.py#L33)

```python
def test_merge_preserves_missing_fields(self)
```

Проверка: Merge обновления не удаляет отсутствующие в нём старые поля.

### `ProjectMemoryTests.test_clear_only_clears_memory_file`

[Исходник](../../tests/test_project_memory.py#L40)

```python
def test_clear_only_clears_memory_file(self)
```

Проверка: Очистка памяти не удаляет другие данные.

<a id="module-tests-test-runtime-architecture-py"></a>

## `tests/test_runtime_architecture.py`

Структура плана, skills, размер контекста и verifier.

### `RuntimeArchitectureTests`

[Исходник](../../tests/test_runtime_architecture.py#L10)

```python
class RuntimeArchitectureTests(unittest.TestCase)
```

Тестовый класс/фикстура: Структура плана, skills, размер контекста и verifier.

### `RuntimeArchitectureTests.test_plan_has_stages`

[Исходник](../../tests/test_runtime_architecture.py#L11)

```python
def test_plan_has_stages(self)
```

Проверка: План содержит структурированные этапы.

### `RuntimeArchitectureTests.test_runtime_prepares_skills_without_tools`

[Исходник](../../tests/test_runtime_architecture.py#L17)

```python
def test_runtime_prepares_skills_without_tools(self)
```

Проверка: Выбор навыков не добавляет исполняемые tools сам по себе.

### `RuntimeArchitectureTests.test_context_is_bounded`

[Исходник](../../tests/test_runtime_architecture.py#L25)

```python
def test_context_is_bounded(self)
```

Проверка: ContextManager ограничивает проверяемый пример рабочего контекста.

### `RuntimeArchitectureTests.test_verifier_rejects_stopped_stage`

[Исходник](../../tests/test_runtime_architecture.py#L30)

```python
def test_verifier_rejects_stopped_stage(self)
```

Проверка: Verifier отклоняет завершение при stop_reason.

<a id="module-tests-test-sandbox-py"></a>

## `tests/test_sandbox.py`

Обёртка запуска внутренней security self-test suite.

### `SandboxIntegrationTest`

[Исходник](../../tests/test_sandbox.py#L5)

```python
class SandboxIntegrationTest(unittest.TestCase)
```

Тестовый класс/фикстура: Обёртка запуска внутренней security self-test suite.

### `SandboxIntegrationTest.test_sandbox_self_test_suite`

[Исходник](../../tests/test_sandbox.py#L6)

```python
def test_sandbox_self_test_suite(self)
```

Проверка: Внутренний набор проверок sandbox возвращает успешный итог.

<a id="module-tests-test-task-store-py"></a>

## `tests/test_task_store.py`

Round-trip checkpoint, переход этапа, завершение и очистка.

### `TaskStoreTests`

[Исходник](../../tests/test_task_store.py#L5)

```python
class TaskStoreTests(unittest.TestCase)
```

Тестовый класс/фикстура: Round-trip checkpoint, переход этапа, завершение и очистка.

### `TaskStoreTests.test_checkpoint_roundtrip`

[Исходник](../../tests/test_task_store.py#L6)

```python
def test_checkpoint_roundtrip(self)
```

Проверка: Checkpoint сохраняется, загружается, меняет этап, завершается и очищается.
