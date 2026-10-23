# Справочник Python-тестов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [tests/migration/test_bridge.py](#module-tests-migration-test-bridge-py)
- [tests/migration/test_bridge_process.py](#module-tests-migration-test-bridge-process-py)
- [tests/migration/test_model_discovery.py](#module-tests-migration-test-model-discovery-py)
- [tests/migration/test_model_probe.py](#module-tests-migration-test-model-probe-py)
- [tests/migration/test_streaming.py](#module-tests-migration-test-streaming-py)
- [tests/migration/test_task_service.py](#module-tests-migration-test-task-service-py)
- [tests/test_approval_flow.py](#module-tests-test-approval-flow-py)
- [tests/test_chat_store.py](#module-tests-test-chat-store-py)
- [tests/test_conversation_history.py](#module-tests-test-conversation-history-py)
- [tests/test_editor_io.py](#module-tests-test-editor-io-py)
- [tests/test_editor_service.py](#module-tests-test-editor-service-py)
- [tests/test_file_editing.py](#module-tests-test-file-editing-py)
- [tests/test_limits.py](#module-tests-test-limits-py)
- [tests/test_memory_service.py](#module-tests-test-memory-service-py)
- [tests/test_model_gateway.py](#module-tests-test-model-gateway-py)
- [tests/test_model_manager.py](#module-tests-test-model-manager-py)
- [tests/test_model_preferences.py](#module-tests-test-model-preferences-py)
- [tests/test_project_memory.py](#module-tests-test-project-memory-py)
- [tests/test_project_search.py](#module-tests-test-project-search-py)
- [tests/test_runtime_architecture.py](#module-tests-test-runtime-architecture-py)
- [tests/test_runtime_service.py](#module-tests-test-runtime-service-py)
- [tests/test_sandbox.py](#module-tests-test-sandbox-py)
- [tests/test_speech_service.py](#module-tests-test-speech-service-py)
- [tests/test_task_activity.py](#module-tests-test-task-activity-py)
- [tests/test_task_store.py](#module-tests-test-task-store-py)

<a id="module-tests-migration-test-bridge-py"></a>

## `tests/migration/test_bridge.py`

Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи.

### `BridgeTests`

[Исходник](../../tests/migration/test_bridge.py#L13)

```python
class BridgeTests(unittest.TestCase)
```

Тестовый класс/фикстура: Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи.

### `BridgeTests.setUp`

[Исходник](../../tests/migration/test_bridge.py#L14)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BridgeTests.tearDown`

[Исходник](../../tests/migration/test_bridge.py#L20)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `BridgeTests.test_chat_scope_does_not_require_selected_folder`

[Исходник](../../tests/migration/test_bridge.py#L24)

```python
def test_chat_scope_does_not_require_selected_folder(self)
```

Проверка: Bridge выбирает пустую область Chat без папки, а IDE требует проект.

### `BridgeTests.test_unknown_mode_is_rejected`

[Исходник](../../tests/migration/test_bridge.py#L32)

```python
def test_unknown_mode_is_rejected(self)
```

Проверка: Bridge отклоняет voice и прочие неисполняемые режимы до сервиса.

### `BridgeTests.test_editor_preview_blocks_task_and_project_switch_invalidates_approval`

[Исходник](../../tests/migration/test_bridge.py#L36)

```python
def test_editor_preview_blocks_task_and_project_switch_invalidates_approval(self)
```

Проверка: Bridge не запускает агента во время editor approval, set_project сбрасывает старый ID.

### `BridgeTests.test_editor_writes_are_rejected_while_agent_is_running`

[Исходник](../../tests/migration/test_bridge.py#L47)

```python
def test_editor_writes_are_rejected_while_agent_is_running(self)
```

Проверка: Ручной preview не начинается, пока task service занят.

### `BridgeTests.test_health`

[Исходник](../../tests/migration/test_bridge.py#L54)

```python
def test_health(self)
```

Проверка: Bridge сообщает доступность процесса.

### `BridgeTests.test_list_and_read`

[Исходник](../../tests/migration/test_bridge.py#L56)

```python
def test_list_and_read(self)
```

Проверка: Bridge перечисляет и читает файл выбранного проекта.

### `BridgeTests.test_parent_traversal_rejected`

[Исходник](../../tests/migration/test_bridge.py#L59)

```python
def test_parent_traversal_rejected(self)
```

Проверка: Bridge не разрешает ../ за пределами проекта.

### `BridgeTests.test_write_is_not_exposed`

[Исходник](../../tests/migration/test_bridge.py#L61)

```python
def test_write_is_not_exposed(self)
```

Проверка: Прямого write_file RPC в bridge нет.

<a id="module-tests-migration-test-bridge-process-py"></a>

## `tests/migration/test_bridge_process.py`

Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.

### `BridgeProcessTests`

[Исходник](../../tests/migration/test_bridge_process.py#L22)

```python
class BridgeProcessTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.

### `BridgeProcessTests.setUp`

[Исходник](../../tests/migration/test_bridge_process.py#L23)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BridgeProcessTests.start_process`

[Исходник](../../tests/migration/test_bridge_process.py#L34)

```python
def start_process(self)
```

Запускает отдельный тестовый bridge с изолированным LOCALAPPDATA и stdout reader.

### `BridgeProcessTests.read_output`

[Исходник](../../tests/migration/test_bridge_process.py#L49)

```python
def read_output(self)
```

Читает JSON-строки stdout тестового subprocess в очередь.

### `BridgeProcessTests.stop_process`

[Исходник](../../tests/migration/test_bridge_process.py#L56)

```python
def stop_process(self, kill=False)
```

Завершает только принадлежащий тесту subprocess, закрывает каналы и ждёт reader.

### `BridgeProcessTests.tearDown`

[Исходник](../../tests/migration/test_bridge_process.py#L75)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `BridgeProcessTests.start_crash_scenario`

[Исходник](../../tests/migration/test_bridge_process.py#L87)

```python
def start_crash_scenario(self, handler, mode=None)
```

Запускает тестовый сервер и задачу перед контролируемым аварийным завершением.

### `BridgeProcessTests.reopen_after_kill`

[Исходник](../../tests/migration/test_bridge_process.py#L100)

```python
def reopen_after_kill(self, chat_id)
```

Убивает тестовый subprocess, запускает новый и открывает сохранённый чат.

### `BridgeProcessTests.test_voice_catalog_and_cancel_keep_bridge_responsive_without_microphone`

[Исходник](../../tests/migration/test_bridge_process.py#L110)

```python
def test_voice_catalog_and_cancel_keep_bridge_responsive_without_microphone(self)
```

Проверка: Настоящий bridge разрешает voice без root, каталог/Stop не блокируют health, неизвестный voice отвергается.

### `BridgeProcessTests.test_project_memory_and_chat_rename_are_scoped`

[Исходник](../../tests/migration/test_bridge_process.py#L118)

```python
def test_project_memory_and_chat_rename_are_scoped(self)
```

Проверка: Реальный JSON bridge проверяет root памяти, stale revision и scope переименования.

### `BridgeProcessTests.test_runtime_commands_validate_without_blocking_other_commands`

[Исходник](../../tests/migration/test_bridge_process.py#L130)

```python
def test_runtime_commands_validate_without_blocking_other_commands(self)
```

Проверка: Bridge status/start validation/stop не нарушают health без модели.

### `BridgeProcessTests.test_project_search_requires_root_and_does_not_block_bridge`

[Исходник](../../tests/migration/test_bridge_process.py#L137)

```python
def test_project_search_requires_root_and_does_not_block_bridge(self)
```

Проверка: Настоящий bridge требует root, возвращает строку поиска и остаётся доступен health/cancel.

### `BridgeProcessTests.test_process_kill_before_headers_recovers_user_request_and_paused_task`

[Исходник](../../tests/migration/test_bridge_process.py#L147)

```python
def test_process_kill_before_headers_recovers_user_request_and_paused_task(self)
```

Проверка: Реальный kill subprocess до HTTP-заголовков сохраняет запрос и paused при открытии.

### `BridgeProcessTests.test_approved_write_and_preferences_survive_process_restart`

[Исходник](../../tests/migration/test_bridge_process.py#L154)

```python
def test_approved_write_and_preferences_survive_process_restart(self)
```

Проверка: Подтверждённая запись и настройки переживают рестарт bridge; ключ не попадает в JSON.

### `BridgeProcessTests.test_process_kill_during_stream_recovers_partial_once`

[Исходник](../../tests/migration/test_bridge_process.py#L168)

```python
def test_process_kill_during_stream_recovers_partial_once(self)
```

Проверка: Реальный kill во время паузы SSE восстанавливает последний сохранённый фрагмент без дубля.

### `BridgeProcessTests.test_process_kill_during_approval_never_replays_permission`

[Исходник](../../tests/migration/test_bridge_process.py#L191)

```python
def test_process_kill_during_approval_never_replays_permission(self)
```

Проверка: После kill во время approval старые ID отклоняются, resume требует нового согласия.

### `BridgeProcessTests.start_discovery_server`

[Исходник](../../tests/migration/test_bridge_process.py#L207)

```python
def start_discovery_server(self, mode)
```

Запускает управляемую HTTP-фикстуру и отправляет discovery в реальный bridge subprocess.

### `BridgeProcessTests.test_bridge_models_discovery_keeps_commands_responsive_and_pins_config`

[Исходник](../../tests/migration/test_bridge_process.py#L222)

```python
def test_bridge_models_discovery_keeps_commands_responsive_and_pins_config(self)
```

Проверка: JSON-lines отвечает на health/новые команды во время discovery, ограничивает worker и сохраняет снимок настроек.

### `BridgeProcessTests.test_draft_probe_keeps_bridge_responsive_and_can_be_cancelled`

[Исходник](../../tests/migration/test_bridge_process.py#L232)

```python
def test_draft_probe_keeps_bridge_responsive_and_can_be_cancelled(self)
```

Проверка: Во время зависшего probe реальный bridge отвечает health/cancel и сохраняет прежнюю конфигурацию.

### `BridgeProcessTests.test_bridge_cancel_closes_discovery_socket`

[Исходник](../../tests/migration/test_bridge_process.py#L253)

```python
def test_bridge_cancel_closes_discovery_socket(self)
```

Проверка: cancel_task отвечает без ожидания discovery и закрывает его HTTP-сокет.

### `BridgeProcessTests.until`

[Исходник](../../tests/migration/test_bridge_process.py#L261)

```python
def until(self, predicate)
```

Ожидает подходящее сообщение, сохраняя остальные для дальнейших проверок.

### `BridgeProcessTests.call`

[Исходник](../../tests/migration/test_bridge_process.py#L272)

```python
def call(self, method, **params)
```

Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.

### `BridgeProcessTests.test_malformed_input_does_not_reuse_previous_request_id`

[Исходник](../../tests/migration/test_bridge_process.py#L279)

```python
def test_malformed_input_does_not_reuse_previous_request_id(self)
```

Проверка: Ошибка JSON не получает ID предыдущей команды и не ломает следующий запрос.

### `BridgeProcessTests.test_bridge_remains_responsive_during_write_approval`

[Исходник](../../tests/migration/test_bridge_process.py#L288)

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

<a id="module-tests-migration-test-model-probe-py"></a>

## `tests/migration/test_model_probe.py`

Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены.

### `ProbeHandler`

[Исходник](../../tests/migration/test_model_probe.py#L12)

```python
class ProbeHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены.

### `ProbeHandler.log_message`

[Исходник](../../tests/migration/test_model_probe.py#L13)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ProbeHandler.do_POST`

[Исходник](../../tests/migration/test_model_probe.py#L16)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `ModelProbeTests`

[Исходник](../../tests/migration/test_model_probe.py#L37)

```python
class ModelProbeTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены.

### `ModelProbeTests.setUp`

[Исходник](../../tests/migration/test_model_probe.py#L38)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ModelProbeTests.tearDown`

[Исходник](../../tests/migration/test_model_probe.py#L47)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ModelProbeTests.test_probe_requires_real_text_and_bounds_bad_responses`

[Исходник](../../tests/migration/test_model_probe.py#L53)

```python
def test_probe_requires_real_text_and_bounds_bad_responses(self)
```

Проверка: Проверка принимает текст и отклоняет пустой результат, неверную структуру, большой ответ и HTTP 401.

### `ModelProbeTests.test_probe_deadline_and_cancellation_are_bounded`

[Исходник](../../tests/migration/test_model_probe.py#L63)

```python
def test_probe_deadline_and_cancellation_are_bounded(self)
```

Проверка: Зависший HTTP прерывается общим deadline и Event отмены.

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

[Исходник](../../tests/migration/test_task_service.py#L61)

```python
class TaskServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `TaskServiceTests.setUpClass`

[Исходник](../../tests/migration/test_task_service.py#L63)

```python
@classmethod
def setUpClass(cls)
```

Создаёт общую HTTP-фикстуру и её поток для класса тестов.

### `TaskServiceTests.tearDownClass`

[Исходник](../../tests/migration/test_task_service.py#L70)

```python
@classmethod
def tearDownClass(cls)
```

Останавливает общий сервер и ждёт его поток.

### `TaskServiceTests.setUp`

[Исходник](../../tests/migration/test_task_service.py#L75)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TaskServiceTests.tearDown`

[Исходник](../../tests/migration/test_task_service.py#L91)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TaskServiceTests.event`

[Исходник](../../tests/migration/test_task_service.py#L97)

```python
def event(self, name)
```

Читает события до нужного имени и немедленно проваливает тест при failed.

### `TaskServiceTests.test_voice_persona_uses_chat_scope_without_file_tools`

[Исходник](../../tests/migration/test_task_service.py#L105)

```python
def test_voice_persona_uses_chat_scope_without_file_tools(self)
```

Проверка: Мия включается только для voice, uses empty Chat scope без tools/auto-memory.

### `TaskServiceTests.test_rename_preserves_messages_and_scope_and_active_title`

[Исходник](../../tests/migration/test_task_service.py#L114)

```python
def test_rename_preserves_messages_and_scope_and_active_title(self)
```

Проверка: Название сохраняется без изменения сообщений, обновляет active chat и не пересекает Chat/IDE scope.

### `TaskServiceTests.test_rename_rejected_during_active_task`

[Исходник](../../tests/migration/test_task_service.py#L124)

```python
def test_rename_rejected_during_active_task(self)
```

Проверка: Переименование запрещено во время реальной задачи, ожидающей approval.

### `TaskServiceTests.start`

[Исходник](../../tests/migration/test_task_service.py#L128)

```python
def start(self)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `TaskServiceTests.resolve`

[Исходник](../../tests/migration/test_task_service.py#L136)

```python
def resolve(self, approval, decision)
```

Передаёт проверяемое решение по предложению в TaskService.

### `TaskServiceTests.test_draft_probe_uses_generation_without_saving_configuration`

[Исходник](../../tests/migration/test_task_service.py#L139)

```python
def test_draft_probe_uses_generation_without_saving_configuration(self)
```

Проверка: Probe получает draft sampling/ID, но не меняет сохранённые настройки и не отправляет tools/историю.

### `TaskServiceTests.test_saved_generation_is_used_by_engine`

[Исходник](../../tests/migration/test_task_service.py#L158)

```python
def test_saved_generation_is_used_by_engine(self)
```

Проверка: Настройки из preferences реально попадают в HTTP streaming payload и переживают новый TaskService.

### `TaskServiceTests.test_empty_after_tool_recovers_without_repeating_write`

[Исходник](../../tests/migration/test_task_service.py#L172)

```python
def test_empty_after_tool_recovers_without_repeating_write(self)
```

Проверка: SSE с reasoning без content после Apply приводит к одному text-only повтору, без повторной записи и без служебного user в архиве.

### `TaskServiceTests.test_permanently_empty_model_pauses_after_two_retries`

[Исходник](../../tests/migration/test_task_service.py#L188)

```python
def test_permanently_empty_model_pauses_after_two_retries(self)
```

Проверка: Три пустых ответа после успешной записи дают paused/failed, сохраняют единственный tool result и файл.

### `TaskServiceTests.test_chat_without_project_has_no_tools_and_separate_history`

[Исходник](../../tests/migration/test_task_service.py#L207)

```python
def test_chat_without_project_has_no_tools_and_separate_history(self)
```

Проверка: Глобальный Chat работает без папки, не передаёт tools и не смешивает историю с проектом.

### `TaskServiceTests.test_task_end_allows_immediate_configuration_before_thread_returns`

[Исходник](../../tests/migration/test_task_service.py#L222)

```python
def test_task_end_allows_immediate_configuration_before_thread_returns(self)
```

Проверка: Синхронный callback task_end меняет настройки, пока прежний поток ещё жив: завершённое исполнение уже idle.

### `TaskServiceTests.test_task_end_allows_immediate_configuration_before_thread_returns.observe`

[Исходник](../../tests/migration/test_task_service.py#L226)

```python
def observe(event)
```

Перехватывает task_end, проверяет ещё живой worker и синхронно меняет настройки до возврата потока.

### `TaskServiceTests.test_chat_refuses_unsolicited_tool`

[Исходник](../../tests/migration/test_task_service.py#L243)

```python
def test_chat_refuses_unsolicited_tool(self)
```

Проверка: Неожиданный tool от сервера в Chat отклоняется до approval/выполнения, задача приостанавливается.

### `TaskServiceTests.test_apply_only_after_matching_approval_and_persist_history`

[Исходник](../../tests/migration/test_task_service.py#L258)

```python
def test_apply_only_after_matching_approval_and_persist_history(self)
```

Проверка: Запись происходит после совпавших run/proposal ID, а история и завершение сохраняются.

### `TaskServiceTests.test_long_archive_survives_model_compaction_and_service_restart`

[Исходник](../../tests/migration/test_task_service.py#L280)

```python
def test_long_archive_survives_model_compaction_and_service_restart(self)
```

Проверка: Длинная история сохраняется целиком после реального HTTP tool loop и повторного открытия сервиса.

### `TaskServiceTests.test_forced_tool_uses_single_definition_then_restores_auto`

[Исходник](../../tests/migration/test_task_service.py#L307)

```python
def test_forced_tool_uses_single_definition_then_restores_auto(self)
```

Проверка: Первый запрос ограничен одним required-инструментом, следующие используют auto и полный набор.

### `TaskServiceTests.test_multiple_tools_keep_same_archive_anchor_for_write_recovery`

[Исходник](../../tests/migration/test_task_service.py#L320)

```python
def test_multiple_tools_keep_same_archive_anchor_for_write_recovery(self)
```

Проверка: Несколько tools одного ответа сохраняют общий assistant anchor; восстановление учитывает точный результат записи.

### `TaskServiceTests.test_reject_does_not_write`

[Исходник](../../tests/migration/test_task_service.py#L340)

```python
def test_reject_does_not_write(self)
```

Проверка: Отказ и устаревшее подтверждение не создают файл.

### `TaskServiceTests.test_matching_approval_refuses_new_external_file`

[Исходник](../../tests/migration/test_task_service.py#L349)

```python
def test_matching_approval_refuses_new_external_file(self)
```

Проверка: Верный approval ID не разрешает запись поверх внешнего файла, появившегося после diff.

### `TaskServiceTests.test_embedded_checkpoint_restores_missing_task_file`

[Исходник](../../tests/migration/test_task_service.py#L364)

```python
def test_embedded_checkpoint_restores_missing_task_file(self)
```

Проверка: Embedded checkpoint восстанавливает отсутствующий task-файл без потери истории.

### `TaskServiceTests.test_recovery_does_not_confuse_reused_tool_ids_with_old_success`

[Исходник](../../tests/migration/test_task_service.py#L377)

```python
def test_recovery_does_not_confuse_reused_tool_ids_with_old_success(self)
```

Проверка: Старый результат с повторённым tool_call_id не скрывает неопределённую новую запись.

### `TaskServiceTests.test_recovery_recognizes_saved_tool_result_before_task_checkpoint`

[Исходник](../../tests/migration/test_task_service.py#L402)

```python
def test_recovery_recognizes_saved_tool_result_before_task_checkpoint(self)
```

Проверка: Сохранённый результат в нужном блоке позволяет восстановить учёт успешной записи.

### `TaskServiceTests.test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately`

[Исходник](../../tests/migration/test_task_service.py#L415)

```python
def test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately(self)
```

Проверка: Draft текущего запуска восстанавливается один раз; чужой фрагмент сохраняется отдельно.

### `TaskServiceTests.test_unexpected_engine_exception_still_persists_pause_and_task_end`

[Исходник](../../tests/migration/test_task_service.py#L433)

```python
def test_unexpected_engine_exception_still_persists_pause_and_task_end(self)
```

Проверка: Неожиданная ошибка engine сохраняет paused и обязательно отправляет task_end.

### `TaskServiceTests.test_index_cache_failure_warns_without_aborting_agent`

[Исходник](../../tests/migration/test_task_service.py#L443)

```python
def test_index_cache_failure_warns_without_aborting_agent(self)
```

Проверка: Отказ кэша индекса предупреждает UI, сохраняя полный успешный агентский цикл.

### `TaskServiceTests.test_index_cache_failure_warns_without_aborting_agent.fail_index_only`

[Исходник](../../tests/migration/test_task_service.py#L445)

```python
def fail_index_only(path, data)
```

Имитирует отказ индекса во время полного агентского цикла.

### `TaskServiceTests.test_persistence_failure_before_apply_never_writes_and_still_ends_task`

[Исходник](../../tests/migration/test_task_service.py#L461)

```python
def test_persistence_failure_before_apply_never_writes_and_still_ends_task(self)
```

Проверка: При отказе сохранения перед Apply файл не меняется, задача завершается с ошибкой.

### `TaskServiceTests.test_resume_preserves_task_and_recovery_marks_interrupted_task_paused`

[Исходник](../../tests/migration/test_task_service.py#L474)

```python
def test_resume_preserves_task_and_recovery_marks_interrupted_task_paused(self)
```

Проверка: Running после сбоя восстанавливается как paused и поддерживает новую попытку.

### `TaskServiceTests.test_new_prompt_after_pause_creates_new_task`

[Исходник](../../tests/migration/test_task_service.py#L491)

```python
def test_new_prompt_after_pause_creates_new_task(self)
```

Проверка: Новый prompt не выдаётся за продолжение старой задачи.

### `TaskServiceTests.test_cancel_while_waiting_pauses_task_and_unblocks_worker`

[Исходник](../../tests/migration/test_task_service.py#L503)

```python
def test_cancel_while_waiting_pauses_task_and_unblocks_worker(self)
```

Проверка: Отмена освобождает approval wait и сохраняет paused.

### `TaskServiceTests.test_busy_task_rejects_chat_and_configuration_changes`

[Исходник](../../tests/migration/test_task_service.py#L512)

```python
def test_busy_task_rejects_chat_and_configuration_changes(self)
```

Проверка: Активная задача запрещает смену чата, config и второй запуск.

### `TaskServiceTests.test_chats_are_scoped_to_project_and_ids_cannot_escape_store`

[Исходник](../../tests/migration/test_task_service.py#L521)

```python
def test_chats_are_scoped_to_project_and_ids_cannot_escape_store(self)
```

Проверка: ID и принадлежность проекта проверяются до загрузки чата.

### `TaskServiceTests.test_models_and_configuration_do_not_return_key`

[Исходник](../../tests/migration/test_task_service.py#L529)

```python
def test_models_and_configuration_do_not_return_key(self)
```

Проверка: Список моделей работает, а configuration response не содержит ключ.

### `TaskServiceTests.test_missing_model_and_bad_url_are_rejected`

[Исходник](../../tests/migration/test_task_service.py#L534)

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

<a id="module-tests-test-editor-service-py"></a>

## `tests/test_editor_service.py`

Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope.

### `EditorServiceTests`

[Исходник](../../tests/test_editor_service.py#L9)

```python
class EditorServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope.

### `EditorServiceTests.setUp`

[Исходник](../../tests/test_editor_service.py#L10)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `EditorServiceTests.tearDown`

[Исходник](../../tests/test_editor_service.py#L18)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `EditorServiceTests.proposal`

[Исходник](../../tests/test_editor_service.py#L21)

```python
def proposal(self, content='edited\nsecond\n')
```

Читает текущую revision и создаёт тестовый editor preview без записи.

### `EditorServiceTests.test_read_preview_and_one_shot_apply_preserve_crlf`

[Исходник](../../tests/test_editor_service.py#L25)

```python
def test_read_preview_and_one_shot_apply_preserve_crlf(self)
```

Проверка: Read сохраняет byte hash/CRLF; preview не пишет, Apply пишет один раз и обновляет revision.

### `EditorServiceTests.test_external_change_before_preview_and_after_approval_is_never_overwritten`

[Исходник](../../tests/test_editor_service.py#L40)

```python
def test_external_change_before_preview_and_after_approval_is_never_overwritten(self)
```

Проверка: Оба момента внешнего изменения возвращают FILE_CHANGED без перезаписи.

### `EditorServiceTests.test_reject_cancel_and_replaced_proposals_do_not_write`

[Исходник](../../tests/test_editor_service.py#L53)

```python
def test_reject_cancel_and_replaced_proposals_do_not_write(self)
```

Проверка: Отказ/отмена и старый ID после новой подготовки не меняют файл.

### `EditorServiceTests.test_unchanged_text_has_no_pending_write`

[Исходник](../../tests/test_editor_service.py#L64)

```python
def test_unchanged_text_has_no_pending_write(self)
```

Проверка: Неизменённый текст не создаёт write approval.

### `EditorServiceTests.test_outside_binary_invalid_utf8_and_large_files_are_rejected`

[Исходник](../../tests/test_editor_service.py#L69)

```python
def test_outside_binary_invalid_utf8_and_large_files_are_rejected(self)
```

Проверка: Editor отвергает traversal, неверную кодировку, NUL и превышение 1 МБ.

### `EditorServiceTests.test_proposal_cannot_be_applied_to_another_project`

[Исходник](../../tests/test_editor_service.py#L80)

```python
def test_proposal_cannot_be_applied_to_another_project(self)
```

Проверка: Proposal одного корня не применяется к другому проекту.

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

<a id="module-tests-test-memory-service-py"></a>

## `tests/test_memory_service.py`

Память UI: CAS, invalid payload, corrupt file, scope и полный Unicode budget.

### `MemoryServiceTests`

[Исходник](../../tests/test_memory_service.py#L10)

```python
class MemoryServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: Память UI: CAS, invalid payload, corrupt file, scope и полный Unicode budget.

### `MemoryServiceTests.setUp`

[Исходник](../../tests/test_memory_service.py#L11)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `MemoryServiceTests.tearDown`

[Исходник](../../tests/test_memory_service.py#L16)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `MemoryServiceTests.test_round_trip_and_external_update_preserve_stale_draft`

[Исходник](../../tests/test_memory_service.py#L19)

```python
def test_round_trip_and_external_update_preserve_stale_draft(self)
```

Проверка: Manual memory round trip и отказ после auto-memory update без перезаписи новых заметок.

### `MemoryServiceTests.test_invalid_fields_do_not_modify_store`

[Исходник](../../tests/test_memory_service.py#L30)

```python
def test_invalid_fields_do_not_modify_store(self)
```

Проверка: Неверные типы/длины/count/extra keys не создают файл памяти.

### `MemoryServiceTests.test_corrupt_memory_is_preserved_and_other_project_is_isolated`

[Исходник](../../tests/test_memory_service.py#L36)

```python
def test_corrupt_memory_is_preserved_and_other_project_is_isolated(self)
```

Проверка: Повреждённый JSON не затирается; другой root получает отдельную пустую память.

### `MemoryServiceTests.test_full_unicode_budget_is_readable`

[Исходник](../../tests/test_memory_service.py#L43)

```python
def test_full_unicode_budget_is_readable(self)
```

Проверка: Полные разрешённые поля с четырёхбайтным Unicode помещаются в bounded reader и проходят round trip.

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

### `ModelPreferencesTests.test_old_preferences_gain_generation_defaults`

[Исходник](../../tests/test_model_preferences.py#L41)

```python
def test_old_preferences_gain_generation_defaults(self)
```

Проверка: Старый JSON с URL/ID получает числовые defaults без смены endpoint и модели.

### `ModelPreferencesTests.test_generation_roundtrip_and_invalid_values_do_not_replace_file`

[Исходник](../../tests/test_model_preferences.py#L46)

```python
def test_generation_roundtrip_and_invalid_values_do_not_replace_file(self)
```

Проверка: Числовые настройки переживают сохранение; NaN, bool, дробный integer и выход за диапазон не перезаписывают файл.

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

<a id="module-tests-test-project-search-py"></a>

## `tests/test_project_search.py`

Поиск: Unicode, фильтры, лимиты, пропуски бинарных файлов, отмена и single-flight.

### `ProjectSearchTests`

[Исходник](../../tests/test_project_search.py#L10)

```python
class ProjectSearchTests(unittest.TestCase)
```

Тестовый класс/фикстура: Поиск: Unicode, фильтры, лимиты, пропуски бинарных файлов, отмена и single-flight.

### `ProjectSearchTests.setUp`

[Исходник](../../tests/test_project_search.py#L11)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ProjectSearchTests.tearDown`

[Исходник](../../tests/test_project_search.py#L17)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `ProjectSearchTests.test_literal_text_line_case_and_path_filter`

[Исходник](../../tests/test_project_search.py#L20)

```python
def test_literal_text_line_case_and_path_filter(self)
```

Проверка: Unicode пути, literal matching, номера строк, регистр и маска файлов.

### `ProjectSearchTests.test_files_ignored_binary_encoding_size_and_result_limits`

[Исходник](../../tests/test_project_search.py#L28)

```python
def test_files_ignored_binary_encoding_size_and_result_limits(self)
```

Проверка: Игнорируемые каталоги, NUL/encoding/размер, быстрый поиск путей и truncated results.

### `ProjectSearchTests.test_cancel_time_and_budget_are_reported`

[Исходник](../../tests/test_project_search.py#L43)

```python
def test_cancel_time_and_budget_are_reported(self)
```

Проверка: Отмена, deadline, file/byte budget и строгая валидация параметров.

### `ProjectSearchTests.test_symlink_cannot_expand_search_scope`

[Исходник](../../tests/test_project_search.py#L52)

```python
def test_symlink_cannot_expand_search_scope(self)
```

Проверка: Внешний symlink не читается; при отсутствии Windows privilege тест явно skipped.

### `ProjectSearchTests.test_worker_cancellation_single_flight_and_invalid_root_recovery`

[Исходник](../../tests/test_project_search.py#L59)

```python
def test_worker_cancellation_single_flight_and_invalid_root_recovery(self)
```

Проверка: Busy worker не допускает второй поиск, отменяется, неверный root не оставляет busy навсегда.

### `ProjectSearchTests.test_worker_cancellation_single_flight_and_invalid_root_recovery.slow`

[Исходник](../../tests/test_project_search.py#L61)

```python
def slow(root, params, cancelled)
```

Управляемая barrier-фикстура поискового worker для детерминированной проверки отмены.

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

<a id="module-tests-test-runtime-service-py"></a>

## `tests/test_runtime_service.py`

Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup.

### `RuntimeServiceTests`

[Исходник](../../tests/test_runtime_service.py#L16)

```python
class RuntimeServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup.

### `RuntimeServiceTests.setUp`

[Исходник](../../tests/test_runtime_service.py#L17)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `RuntimeServiceTests.tearDown`

[Исходник](../../tests/test_runtime_service.py#L25)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `RuntimeServiceTests.test_validation_does_not_launch_arbitrary_files`

[Исходник](../../tests/test_runtime_service.py#L28)

```python
def test_validation_does_not_launch_arbitrary_files(self)
```

Проверка: Имя executable, GGUF header и integer/range проверяются до старта.

### `RuntimeServiceTests.test_start_cancel_is_nonblocking_and_cannot_restart_until_worker_finishes`

[Исходник](../../tests/test_runtime_service.py#L35)

```python
def test_start_cancel_is_nonblocking_and_cannot_restart_until_worker_finishes(self)
```

Проверка: Start возвращает сразу, Stop отменяет worker, параллельный restart запрещён.

### `RuntimeServiceTests.test_start_cancel_is_nonblocking_and_cannot_restart_until_worker_finishes.launching`

[Исходник](../../tests/test_runtime_service.py#L37)

```python
def launching(model, **kwargs)
```

Управляемая barrier-фикстура долгой загрузки с cooperative cancel.

### `RuntimeServiceTests.test_start_failure_is_visible_without_busy_deadlock`

[Исходник](../../tests/test_runtime_service.py#L49)

```python
def test_start_failure_is_visible_without_busy_deadlock(self)
```

Проверка: Ошибка старта становится видимым error и не оставляет вечный busy.

### `RuntimeServiceTests.test_output_drain_is_bounded_even_without_newlines`

[Исходник](../../tests/test_runtime_service.py#L55)

```python
def test_output_drain_is_bounded_even_without_newlines(self)
```

Проверка: 500 КБ вывода без newline не превышают 100 порций в памяти.

### `RuntimeServiceTests.test_output_drain_is_bounded_even_without_newlines.Output`

[Исходник](../../tests/test_runtime_service.py#L56)

```python
class Output
```

Тестовый класс/фикстура: Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup.

### `RuntimeServiceTests.test_readiness_timeout_cleans_only_owned_process`

[Исходник](../../tests/test_runtime_service.py#L62)

```python
def test_readiness_timeout_cleans_only_owned_process(self)
```

Проверка: Timeout завершает реальный собственный процесс и закрывает его job.

### `RuntimeServiceTests.test_parent_crash_closes_job_and_terminates_child`

[Исходник](../../tests/test_runtime_service.py#L71)

```python
@unittest.skipUnless(sys.platform == 'win32', 'Windows job only')
def test_parent_crash_closes_job_and_terminates_child(self)
```

Проверка: Авария владельца job автоматически завершает его дочернее дерево.

### `RuntimeServiceTests.test_windows_job_close_terminates_owned_child`

[Исходник](../../tests/test_runtime_service.py#L95)

```python
@unittest.skipUnless(sys.platform == 'win32', 'Windows job only')
def test_windows_job_close_terminates_owned_child(self)
```

Проверка: Закрытие Windows job завершает присоединённого потомка.

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

<a id="module-tests-test-speech-service-py"></a>

## `tests/test_speech_service.py`

TTS без динамиков/микрофона: WAV, JSON data boundary, cancellation и timeout cleanup.

### `SpeechServiceTests`

[Исходник](../../tests/test_speech_service.py#L15)

```python
class SpeechServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: TTS без динамиков/микрофона: WAV, JSON data boundary, cancellation и timeout cleanup.

### `SpeechServiceTests.setUp`

[Исходник](../../tests/test_speech_service.py#L16)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `SpeechServiceTests.tearDown`

[Исходник](../../tests/test_speech_service.py#L20)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `SpeechServiceTests.test_invalid_text_voice_and_numeric_options_never_start_audio`

[Исходник](../../tests/test_speech_service.py#L23)

```python
def test_invalid_text_voice_and_numeric_options_never_start_audio(self)
```

Проверка: Невалидные text/voice/rate/volume не создают worker и не открывают аудиоустройство.

### `SpeechServiceTests.test_catalog_runs_outside_bridge_and_returns_installed_choices`

[Исходник](../../tests/test_speech_service.py#L29)

```python
def test_catalog_runs_outside_bridge_and_returns_installed_choices(self)
```

Проверка: Каталог выполняется в отдельном процессе/потоке, busy защищает второй старт.

### `SpeechServiceTests.test_json_text_is_data_and_stop_cleans_owned_worker`

[Исходник](../../tests/test_speech_service.py#L38)

```python
def test_json_text_is_data_and_stop_cleans_owned_worker(self)
```

Проверка: Unicode/quotes/PowerShell-подобные символы передаются неизменённым JSON; Stop быстро завершает своё дерево.

### `SpeechServiceTests.test_timeout_is_visible_and_worker_can_be_reused`

[Исходник](../../tests/test_speech_service.py#L53)

```python
def test_timeout_is_visible_and_worker_can_be_reused(self)
```

Проверка: Deadline завершает worker и делает ошибку видимой вместо вечного busy.

### `SpeechServiceTests.test_real_system_voice_renders_wave_without_speakers_or_microphone`

[Исходник](../../tests/test_speech_service.py#L65)

```python
@unittest.skipUnless(os.name == 'nt', 'Windows System.Speech only')
def test_real_system_voice_renders_wave_without_speakers_or_microphone(self)
```

Проверка: Установленный Windows голос синтезирует PCM WAV; динамики и микрофон не используются.

<a id="module-tests-test-task-activity-py"></a>

## `tests/test_task_activity.py`

Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery.

### `TaskActivityTests`

[Исходник](../../tests/test_task_activity.py#L7)

```python
class TaskActivityTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery.

### `TaskActivityTests.test_activity_is_bounded_metadata_with_monotonic_ids`

[Исходник](../../tests/test_task_activity.py#L8)

```python
def test_activity_is_bounded_metadata_with_monotonic_ids(self)
```

Проверка: Журнал содержит максимум 100 записей, устойчивые ID и метаданные без содержимого файлов.

### `TaskActivityTests.test_tool_outcomes_distinguish_denial_cancel_failure_and_truncation`

[Исходник](../../tests/test_task_activity.py#L20)

```python
def test_tool_outcomes_distinguish_denial_cancel_failure_and_truncation(self)
```

Проверка: Различаются отказ, отмена, ошибка и успех с ограниченной выдачей.

### `TaskActivityTests.test_activity_recovery_uses_anchored_result_and_is_idempotent`

[Исходник](../../tests/test_task_activity.py#L33)

```python
def test_activity_recovery_uses_anchored_result_and_is_idempotent(self)
```

Проверка: Повторённый tool ID не даёт ложного успеха; восстановление использует точный блок и не повторяется.

### `TaskActivityTests.test_recovery_interrupts_waiting_without_replaying_approval`

[Исходник](../../tests/test_task_activity.py#L50)

```python
def test_recovery_interrupts_waiting_without_replaying_approval(self)
```

Проверка: Ожидание approval после сбоя становится interrupted без повторного согласия.

### `TaskActivityTests.test_stage_transitions_skip_unvisited_and_keep_only_one_active`

[Исходник](../../tests/test_task_activity.py#L58)

```python
def test_stage_transitions_skip_unvisited_and_keep_only_one_active(self)
```

Проверка: Непосещённые этапы пропускаются, при возврате остаётся ровно один active.

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
