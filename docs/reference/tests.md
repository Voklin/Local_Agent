# Справочник Python-тестов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [tests/migration/test_bridge.py](#module-tests-migration-test-bridge-py)
- [tests/migration/test_bridge_process.py](#module-tests-migration-test-bridge-process-py)
- [tests/migration/test_model_discovery.py](#module-tests-migration-test-model-discovery-py)
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

[Исходник](../../tests/migration/test_bridge_process.py#L20)

```python
class BridgeProcessTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.

### `BridgeProcessTests.setUp`

[Исходник](../../tests/migration/test_bridge_process.py#L21)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BridgeProcessTests.start_process`

[Исходник](../../tests/migration/test_bridge_process.py#L32)

```python
def start_process(self)
```

Запускает отдельный тестовый bridge с изолированным LOCALAPPDATA и stdout reader.

### `BridgeProcessTests.read_output`

[Исходник](../../tests/migration/test_bridge_process.py#L46)

```python
def read_output(self)
```

Читает JSON-строки stdout тестового subprocess в очередь.

### `BridgeProcessTests.stop_process`

[Исходник](../../tests/migration/test_bridge_process.py#L53)

```python
def stop_process(self, kill=False)
```

Завершает только принадлежащий тесту subprocess, закрывает каналы и ждёт reader.

### `BridgeProcessTests.tearDown`

[Исходник](../../tests/migration/test_bridge_process.py#L69)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `BridgeProcessTests.start_crash_scenario`

[Исходник](../../tests/migration/test_bridge_process.py#L81)

```python
def start_crash_scenario(self, handler, mode=None)
```

Запускает тестовый сервер и задачу перед контролируемым аварийным завершением.

### `BridgeProcessTests.reopen_after_kill`

[Исходник](../../tests/migration/test_bridge_process.py#L94)

```python
def reopen_after_kill(self, chat_id)
```

Убивает тестовый subprocess, запускает новый и открывает сохранённый чат.

### `BridgeProcessTests.test_process_kill_before_headers_recovers_user_request_and_paused_task`

[Исходник](../../tests/migration/test_bridge_process.py#L104)

```python
def test_process_kill_before_headers_recovers_user_request_and_paused_task(self)
```

Проверка: Реальный kill subprocess до HTTP-заголовков сохраняет запрос и paused при открытии.

### `BridgeProcessTests.test_approved_write_and_preferences_survive_process_restart`

[Исходник](../../tests/migration/test_bridge_process.py#L111)

```python
def test_approved_write_and_preferences_survive_process_restart(self)
```

Проверка: Подтверждённая запись и настройки переживают рестарт bridge; ключ не попадает в JSON.

### `BridgeProcessTests.test_process_kill_during_stream_recovers_partial_once`

[Исходник](../../tests/migration/test_bridge_process.py#L125)

```python
def test_process_kill_during_stream_recovers_partial_once(self)
```

Проверка: Реальный kill во время паузы SSE восстанавливает последний сохранённый фрагмент без дубля.

### `BridgeProcessTests.test_process_kill_during_approval_never_replays_permission`

[Исходник](../../tests/migration/test_bridge_process.py#L148)

```python
def test_process_kill_during_approval_never_replays_permission(self)
```

Проверка: После kill во время approval старые ID отклоняются, resume требует нового согласия.

### `BridgeProcessTests.start_discovery_server`

[Исходник](../../tests/migration/test_bridge_process.py#L163)

```python
def start_discovery_server(self, mode)
```

Запускает управляемую HTTP-фикстуру и отправляет discovery в реальный bridge subprocess.

### `BridgeProcessTests.test_bridge_models_discovery_keeps_commands_responsive_and_pins_config`

[Исходник](../../tests/migration/test_bridge_process.py#L178)

```python
def test_bridge_models_discovery_keeps_commands_responsive_and_pins_config(self)
```

Проверка: JSON-lines отвечает на health/новые команды во время discovery, ограничивает worker и сохраняет снимок настроек.

### `BridgeProcessTests.test_bridge_cancel_closes_discovery_socket`

[Исходник](../../tests/migration/test_bridge_process.py#L188)

```python
def test_bridge_cancel_closes_discovery_socket(self)
```

Проверка: cancel_task отвечает без ожидания discovery и закрывает его HTTP-сокет.

### `BridgeProcessTests.until`

[Исходник](../../tests/migration/test_bridge_process.py#L196)

```python
def until(self, predicate)
```

Ожидает подходящее сообщение, сохраняя остальные для дальнейших проверок.

### `BridgeProcessTests.call`

[Исходник](../../tests/migration/test_bridge_process.py#L207)

```python
def call(self, method, **params)
```

Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.

### `BridgeProcessTests.test_malformed_input_does_not_reuse_previous_request_id`

[Исходник](../../tests/migration/test_bridge_process.py#L214)

```python
def test_malformed_input_does_not_reuse_previous_request_id(self)
```

Проверка: Ошибка JSON не получает ID предыдущей команды и не ломает следующий запрос.

### `BridgeProcessTests.test_bridge_remains_responsive_during_write_approval`

[Исходник](../../tests/migration/test_bridge_process.py#L223)

```python
def test_bridge_remains_responsive_during_write_approval(self)
```

Проверка: Реальный Core отвечает на health/cancel, пока engine ждёт согласия.

<a id="module-tests-migration-test-model-discovery-py"></a>

## `tests/migration/test_model_discovery.py`

HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета.

### `DiscoveryHandler`

[Исходник](../../tests/migration/test_model_discovery.py#L13)

```python
class DiscoveryHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета.

### `DiscoveryHandler.log_message`

[Исходник](../../tests/migration/test_model_discovery.py#L14)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `DiscoveryHandler.do_GET`

[Исходник](../../tests/migration/test_model_discovery.py#L17)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `ModelDiscoveryTests`

[Исходник](../../tests/migration/test_model_discovery.py#L51)

```python
class ModelDiscoveryTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета.

### `ModelDiscoveryTests.setUp`

[Исходник](../../tests/migration/test_model_discovery.py#L52)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ModelDiscoveryTests.tearDown`

[Исходник](../../tests/migration/test_model_discovery.py#L62)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ModelDiscoveryTests.test_valid_discovery_filters_invalid_ids`

[Исходник](../../tests/migration/test_model_discovery.py#L68)

```python
def test_valid_discovery_filters_invalid_ids(self)
```

Проверка: Валидный список моделей возвращается без неправильных/пустых ID.

### `ModelDiscoveryTests.test_invalid_json_shape_status_and_size_are_rejected`

[Исходник](../../tests/migration/test_model_discovery.py#L71)

```python
def test_invalid_json_shape_status_and_size_are_rejected(self)
```

Проверка: Ошибочные JSON, data, HTTP status и превышение размера дают отказ.

### `ModelDiscoveryTests.test_total_deadline_stops_slow_trickle`

[Исходник](../../tests/migration/test_model_discovery.py#L78)

```python
def test_total_deadline_stops_slow_trickle(self)
```

Проверка: Общий deadline закрывает медленно поступающий HTTP body, даже если отдельные чтения не зависли.

### `ModelDiscoveryTests.test_cancellation_closes_stalled_socket`

[Исходник](../../tests/migration/test_model_discovery.py#L86)

```python
def test_cancellation_closes_stalled_socket(self)
```

Проверка: Отмена discovery закрывает реальное зависшее HTTP-соединение.

### `ModelDiscoveryTests.test_cancellation_closes_stalled_socket.run`

[Исходник](../../tests/migration/test_model_discovery.py#L90)

```python
def run()
```

В тесте запускает сетевой вызов в отдельном потоке и передаёт результат/ошибку в очередь.

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

[Исходник](../../tests/migration/test_task_service.py#L16)

```python
class ModelHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `ModelHandler.log_message`

[Исходник](../../tests/migration/test_task_service.py#L17)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ModelHandler.do_GET`

[Исходник](../../tests/migration/test_task_service.py#L20)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `ModelHandler.do_POST`

[Исходник](../../tests/migration/test_task_service.py#L26)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `TaskServiceTests`

[Исходник](../../tests/migration/test_task_service.py#L50)

```python
class TaskServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `TaskServiceTests.setUpClass`

[Исходник](../../tests/migration/test_task_service.py#L52)

```python
@classmethod
def setUpClass(cls)
```

Создаёт общую HTTP-фикстуру и её поток для класса тестов.

### `TaskServiceTests.tearDownClass`

[Исходник](../../tests/migration/test_task_service.py#L59)

```python
@classmethod
def tearDownClass(cls)
```

Останавливает общий сервер и ждёт его поток.

### `TaskServiceTests.setUp`

[Исходник](../../tests/migration/test_task_service.py#L64)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TaskServiceTests.tearDown`

[Исходник](../../tests/migration/test_task_service.py#L80)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TaskServiceTests.event`

[Исходник](../../tests/migration/test_task_service.py#L86)

```python
def event(self, name)
```

Читает события до нужного имени и немедленно проваливает тест при failed.

### `TaskServiceTests.start`

[Исходник](../../tests/migration/test_task_service.py#L94)

```python
def start(self)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `TaskServiceTests.resolve`

[Исходник](../../tests/migration/test_task_service.py#L102)

```python
def resolve(self, approval, decision)
```

Передаёт проверяемое решение по предложению в TaskService.

### `TaskServiceTests.test_apply_only_after_matching_approval_and_persist_history`

[Исходник](../../tests/migration/test_task_service.py#L105)

```python
def test_apply_only_after_matching_approval_and_persist_history(self)
```

Проверка: Запись происходит после совпавших run/proposal ID, а история и завершение сохраняются.

### `TaskServiceTests.test_long_archive_survives_model_compaction_and_service_restart`

[Исходник](../../tests/migration/test_task_service.py#L122)

```python
def test_long_archive_survives_model_compaction_and_service_restart(self)
```

Проверка: Длинная история сохраняется целиком после реального HTTP tool loop и повторного открытия сервиса.

### `TaskServiceTests.test_forced_tool_uses_single_definition_then_restores_auto`

[Исходник](../../tests/migration/test_task_service.py#L149)

```python
def test_forced_tool_uses_single_definition_then_restores_auto(self)
```

Проверка: Первый запрос ограничен одним required-инструментом, следующие используют auto и полный набор.

### `TaskServiceTests.test_reject_does_not_write`

[Исходник](../../tests/migration/test_task_service.py#L162)

```python
def test_reject_does_not_write(self)
```

Проверка: Отказ и устаревшее подтверждение не создают файл.

### `TaskServiceTests.test_matching_approval_refuses_new_external_file`

[Исходник](../../tests/migration/test_task_service.py#L170)

```python
def test_matching_approval_refuses_new_external_file(self)
```

Проверка: Верный approval ID не разрешает запись поверх внешнего файла, появившегося после diff.

### `TaskServiceTests.test_embedded_checkpoint_restores_missing_task_file`

[Исходник](../../tests/migration/test_task_service.py#L184)

```python
def test_embedded_checkpoint_restores_missing_task_file(self)
```

Проверка: Embedded checkpoint восстанавливает отсутствующий task-файл без потери истории.

### `TaskServiceTests.test_recovery_does_not_confuse_reused_tool_ids_with_old_success`

[Исходник](../../tests/migration/test_task_service.py#L197)

```python
def test_recovery_does_not_confuse_reused_tool_ids_with_old_success(self)
```

Проверка: Старый результат с повторённым tool_call_id не скрывает неопределённую новую запись.

### `TaskServiceTests.test_recovery_recognizes_saved_tool_result_before_task_checkpoint`

[Исходник](../../tests/migration/test_task_service.py#L222)

```python
def test_recovery_recognizes_saved_tool_result_before_task_checkpoint(self)
```

Проверка: Сохранённый результат в нужном блоке позволяет восстановить учёт успешной записи.

### `TaskServiceTests.test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately`

[Исходник](../../tests/migration/test_task_service.py#L235)

```python
def test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately(self)
```

Проверка: Draft текущего запуска восстанавливается один раз; чужой фрагмент сохраняется отдельно.

### `TaskServiceTests.test_unexpected_engine_exception_still_persists_pause_and_task_end`

[Исходник](../../tests/migration/test_task_service.py#L253)

```python
def test_unexpected_engine_exception_still_persists_pause_and_task_end(self)
```

Проверка: Неожиданная ошибка engine сохраняет paused и обязательно отправляет task_end.

### `TaskServiceTests.test_index_cache_failure_warns_without_aborting_agent`

[Исходник](../../tests/migration/test_task_service.py#L263)

```python
def test_index_cache_failure_warns_without_aborting_agent(self)
```

Проверка: Отказ кэша индекса предупреждает UI, сохраняя полный успешный агентский цикл.

### `TaskServiceTests.test_index_cache_failure_warns_without_aborting_agent.fail_index_only`

[Исходник](../../tests/migration/test_task_service.py#L265)

```python
def fail_index_only(path, data)
```

Имитирует отказ индекса во время полного агентского цикла.

### `TaskServiceTests.test_persistence_failure_before_apply_never_writes_and_still_ends_task`

[Исходник](../../tests/migration/test_task_service.py#L281)

```python
def test_persistence_failure_before_apply_never_writes_and_still_ends_task(self)
```

Проверка: При отказе сохранения перед Apply файл не меняется, задача завершается с ошибкой.

### `TaskServiceTests.test_resume_preserves_task_and_recovery_marks_interrupted_task_paused`

[Исходник](../../tests/migration/test_task_service.py#L294)

```python
def test_resume_preserves_task_and_recovery_marks_interrupted_task_paused(self)
```

Проверка: Running после сбоя восстанавливается как paused и поддерживает новую попытку.

### `TaskServiceTests.test_new_prompt_after_pause_creates_new_task`

[Исходник](../../tests/migration/test_task_service.py#L311)

```python
def test_new_prompt_after_pause_creates_new_task(self)
```

Проверка: Новый prompt не выдаётся за продолжение старой задачи.

### `TaskServiceTests.test_cancel_while_waiting_pauses_task_and_unblocks_worker`

[Исходник](../../tests/migration/test_task_service.py#L323)

```python
def test_cancel_while_waiting_pauses_task_and_unblocks_worker(self)
```

Проверка: Отмена освобождает approval wait и сохраняет paused.

### `TaskServiceTests.test_busy_task_rejects_chat_and_configuration_changes`

[Исходник](../../tests/migration/test_task_service.py#L332)

```python
def test_busy_task_rejects_chat_and_configuration_changes(self)
```

Проверка: Активная задача запрещает смену чата, config и второй запуск.

### `TaskServiceTests.test_chats_are_scoped_to_project_and_ids_cannot_escape_store`

[Исходник](../../tests/migration/test_task_service.py#L341)

```python
def test_chats_are_scoped_to_project_and_ids_cannot_escape_store(self)
```

Проверка: ID и принадлежность проекта проверяются до загрузки чата.

### `TaskServiceTests.test_models_and_configuration_do_not_return_key`

[Исходник](../../tests/migration/test_task_service.py#L349)

```python
def test_models_and_configuration_do_not_return_key(self)
```

Проверка: Список моделей работает, а configuration response не содержит ключ.

### `TaskServiceTests.test_missing_model_and_bad_url_are_rejected`

[Исходник](../../tests/migration/test_task_service.py#L354)

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

### `ChatRecoveryTests`

[Исходник](../../tests/test_chat_store.py#L10)

```python
class ChatRecoveryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Создание, изменение, переименование и удаление чата в изолированном store.

### `ChatRecoveryTests.setUp`

[Исходник](../../tests/test_chat_store.py#L11)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ChatRecoveryTests.tearDown`

[Исходник](../../tests/test_chat_store.py#L19)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ChatRecoveryTests.test_missing_corrupt_and_stale_index_is_rebuilt_from_chat_files`

[Исходник](../../tests/test_chat_store.py#L24)

```python
def test_missing_corrupt_and_stale_index_is_rebuilt_from_chat_files(self)
```

Проверка: Отсутствующий, повреждённый и устаревший индекс восстанавливается из канонических файлов.

### `ChatRecoveryTests.test_index_failure_does_not_lose_saved_transcript`

[Исходник](../../tests/test_chat_store.py#L38)

```python
def test_index_failure_does_not_lose_saved_transcript(self)
```

Проверка: Ошибка записи индекса не отменяет сохранение истории; повторный каталог исправляет кэш.

### `ChatRecoveryTests.test_index_failure_does_not_lose_saved_transcript.write_with_failed_index`

[Исходник](../../tests/test_chat_store.py#L40)

```python
def write_with_failed_index(path, data)
```

Пропускает каноническую запись и имитирует отказ только кэша индекса.

### `ChatRecoveryTests.test_corrupted_chat_is_reported_without_modifying_source`

[Исходник](../../tests/test_chat_store.py#L56)

```python
def test_corrupted_chat_is_reported_without_modifying_source(self)
```

Проверка: Повреждённый чат остаётся нетронутым, валидные чаты доступны и предупреждение содержит ID.

### `ChatRecoveryTests.test_store_rejects_path_like_chat_ids`

[Исходник](../../tests/test_chat_store.py#L68)

```python
def test_store_rejects_path_like_chat_ids(self)
```

Проверка: Файловые пути вместо UUID не читаются, не удаляются и не сохраняются.

### `ChatRecoveryTests.test_unreadable_directory_is_not_reported_as_empty_catalog`

[Исходник](../../tests/test_chat_store.py#L77)

```python
def test_unreadable_directory_is_not_reported_as_empty_catalog(self)
```

Проверка: Недоступный каталог чатов выдаёт ошибку вместо ложного пустого списка.

### `ChatRecoveryTests.test_fsync_failure_leaves_previous_chat_and_cleans_temporary_file`

[Исходник](../../tests/test_chat_store.py#L82)

```python
def test_fsync_failure_leaves_previous_chat_and_cleans_temporary_file(self)
```

Проверка: Ошибка fsync не заменяет предыдущий JSON и удаляет временный файл.

### `ChatStoreTest`

[Исходник](../../tests/test_chat_store.py#L93)

```python
class ChatStoreTest(unittest.TestCase)
```

Тестовый класс/фикстура: Создание, изменение, переименование и удаление чата в изолированном store.

### `ChatStoreTest.test_create_save_load_rename_delete`

[Исходник](../../tests/test_chat_store.py#L94)

```python
def test_create_save_load_rename_delete(self)
```

Проверка: Полный жизненный цикл записи чата и индекса.

<a id="module-tests-test-conversation-history-py"></a>

## `tests/test_conversation_history.py`

Выбор истории и сокращение tool outputs/пар в conversation.py.

### `ConversationHistoryTests`

[Исходник](../../tests/test_conversation_history.py#L9)

```python
class ConversationHistoryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Выбор истории и сокращение tool outputs/пар в conversation.py.

### `ConversationHistoryTests.test_archive_builder_keeps_all_turns_and_copies_nested_calls`

[Исходник](../../tests/test_conversation_history.py#L10)

```python
def test_archive_builder_keeps_all_turns_and_copies_nested_calls(self)
```

Проверка: Канонический builder сохраняет все ходы и независимо копирует вложенные tool calls.

### `ConversationHistoryTests.test_model_context_omits_unfinished_and_orphaned_tool_exchanges`

[Исходник](../../tests/test_conversation_history.py#L18)

```python
def test_model_context_omits_unfinished_and_orphaned_tool_exchanges(self)
```

Проверка: Модель не получает незавершённые и осиротевшие tool calls/results.

### `ConversationHistoryTests.test_serialized_context_budget_keeps_current_request_and_tool_pairs`

[Исходник](../../tests/test_conversation_history.py#L35)

```python
def test_serialized_context_budget_keeps_current_request_and_tool_pairs(self)
```

Проверка: JSON-бюджет соблюдается с Unicode/экранированием при сохранении запроса и tool-пар.

### `ConversationHistoryTests.test_oversized_mandatory_instructions_fail_without_truncation`

[Исходник](../../tests/test_conversation_history.py#L46)

```python
def test_oversized_mandatory_instructions_fail_without_truncation(self)
```

Проверка: Обязательные инструкции не обрезаются молча при превышении бюджета.

### `ConversationHistoryTests.test_current_run_request_survives_internal_continuation`

[Исходник](../../tests/test_conversation_history.py#L52)

```python
def test_current_run_request_survives_internal_continuation(self)
```

Проверка: Исходный запрос текущего запуска сохраняется рядом с внутренним продолжением.

### `ConversationHistoryTests.test_followup_keeps_previous_user_and_assistant_messages`

[Исходник](../../tests/test_conversation_history.py#L60)

```python
def test_followup_keeps_previous_user_and_assistant_messages(self)
```

Проверка: Повторный запрос сохраняет недавний контекст диалога.

### `ConversationHistoryTests.test_tool_call_and_tool_result_are_preserved`

[Исходник](../../tests/test_conversation_history.py#L71)

```python
def test_tool_call_and_tool_result_are_preserved(self)
```

Проверка: Связанные вызов и ответ инструмента сохраняются вместе.

### `ConversationHistoryTests.test_empty_history_starts_cleanly`

[Исходник](../../tests/test_conversation_history.py#L82)

```python
def test_empty_history_starts_cleanly(self)
```

Проверка: Пустая история создаёт корректный первый запрос.

### `ConversationHistoryTests.test_old_turns_are_trimmed_but_recent_confirmation_context_remains`

[Исходник](../../tests/test_conversation_history.py#L86)

```python
def test_old_turns_are_trimmed_but_recent_confirmation_context_remains(self)
```

Проверка: Старые ходы сокращаются без потери недавнего контекста согласия.

### `ConversationHistoryTests.test_live_compaction_preserves_system_original_request_and_recent_tool_pair`

[Исходник](../../tests/test_conversation_history.py#L103)

```python
def test_live_compaction_preserves_system_original_request_and_recent_tool_pair(self)
```

Проверка: compact_live_messages сохраняет system, исходный запрос и недавнюю tool-пару.

### `ConversationHistoryTests.test_tool_results_are_bounded_without_dropping_tool_call_pair`

[Исходник](../../tests/test_conversation_history.py#L119)

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

[Исходник](../../tests/test_file_editing.py#L10)

```python
class FileEditingTests(unittest.TestCase)
```

Тестовый класс/фикстура: Preview без записи, explicit approval, overwrite и путь файла.

### `FileEditingTests.setUp`

[Исходник](../../tests/test_file_editing.py#L11)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `FileEditingTests.tearDown`

[Исходник](../../tests/test_file_editing.py#L19)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `FileEditingTests.test_preview_does_not_write`

[Исходник](../../tests/test_file_editing.py#L22)

```python
def test_preview_does_not_write(self)
```

Проверка: Расчёт diff не меняет файловую систему.

### `FileEditingTests.test_write_file_denies_without_explicit_approval`

[Исходник](../../tests/test_file_editing.py#L28)

```python
def test_write_file_denies_without_explicit_approval(self)
```

Проверка: Неподтверждённая запись отклоняется по умолчанию.

### `FileEditingTests.test_create_new_file`

[Исходник](../../tests/test_file_editing.py#L34)

```python
def test_create_new_file(self)
```

Проверка: Подтверждённая запись создаёт новый файл.

### `FileEditingTests.test_existing_file_requires_overwrite_flag`

[Исходник](../../tests/test_file_editing.py#L40)

```python
def test_existing_file_requires_overwrite_flag(self)
```

Проверка: Существующий файл требует явного overwrite.

### `FileEditingTests.test_overwrite_existing_file`

[Исходник](../../tests/test_file_editing.py#L46)

```python
def test_overwrite_existing_file(self)
```

Проверка: Подтверждённая разрешённая замена меняет существующий текст.

### `FileEditingTests.test_outside_path_denied`

[Исходник](../../tests/test_file_editing.py#L52)

```python
def test_outside_path_denied(self)
```

Проверка: Запись вне корня не допускается.

### `FileEditingTests.test_dispatch_write_requires_approval`

[Исходник](../../tests/test_file_editing.py#L56)

```python
def test_dispatch_write_requires_approval(self)
```

Проверка: Dispatcher также не обходит approval.

### `FileEditingTests.test_snapshot_is_required_and_model_cannot_supply_it`

[Исходник](../../tests/test_file_editing.py#L67)

```python
def test_snapshot_is_required_and_model_cannot_supply_it(self)
```

Проверка: Модельные аргументы не могут подменить обязательный снимок подтверждения.

### `FileEditingTests.test_external_edit_after_preview_is_not_overwritten`

[Исходник](../../tests/test_file_editing.py#L74)

```python
def test_external_edit_after_preview_is_not_overwritten(self)
```

Проверка: Изменённый после diff файл не перезаписывается.

### `FileEditingTests.test_deleted_existing_file_requires_new_approval`

[Исходник](../../tests/test_file_editing.py#L81)

```python
def test_deleted_existing_file_requires_new_approval(self)
```

Проверка: Удаление существующего файла после preview требует нового согласия.

### `FileEditingTests.test_snapshot_binds_path_and_proposed_content`

[Исходник](../../tests/test_file_editing.py#L88)

```python
def test_snapshot_binds_path_and_proposed_content(self)
```

Проверка: Снимок связан с конкретным путём и предлагаемым текстом.

### `FileEditingTests.test_byte_level_line_ending_change_invalidates_preview`

[Исходник](../../tests/test_file_editing.py#L95)

```python
def test_byte_level_line_ending_change_invalidates_preview(self)
```

Проверка: Изменение CRLF/LF обнаруживается по исходным байтам.

### `FileEditingTests.test_second_snapshot_check_catches_edit_during_temp_write`

[Исходник](../../tests/test_file_editing.py#L104)

```python
def test_second_snapshot_check_catches_edit_during_temp_write(self)
```

Проверка: Повторная проверка обнаруживает правку во время записи временного файла.

### `FileEditingTests.test_atomic_create_refuses_file_that_appears_after_final_check`

[Исходник](../../tests/test_file_editing.py#L113)

```python
def test_atomic_create_refuses_file_that_appears_after_final_check(self)
```

Проверка: Атомарное создание не затирает файл, появившийся после последней проверки.

### `FileEditingTests.test_atomic_create_refuses_file_that_appears_after_final_check.late_create`

[Исходник](../../tests/test_file_editing.py#L119)

```python
def late_create(source, destination)
```

Имитирует создание внешнего файла непосредственно перед атомарным созданием агентом.

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

[Исходник](../../tests/test_task_store.py#L7)

```python
class TaskStoreTests(unittest.TestCase)
```

Тестовый класс/фикстура: Round-trip checkpoint, переход этапа, завершение и очистка.

### `TaskStoreTests.test_checkpoint_roundtrip`

[Исходник](../../tests/test_task_store.py#L8)

```python
def test_checkpoint_roundtrip(self)
```

Проверка: Checkpoint сохраняется, загружается, меняет этап, завершается и очищается.
