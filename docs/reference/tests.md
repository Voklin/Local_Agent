# Справочник Python-тестов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

## Оглавление модулей

- [tests/fixtures/lsp_diagnostics.py](#module-tests-fixtures-lsp-diagnostics-py)
- [tests/fixtures/mcp_echo.py](#module-tests-fixtures-mcp-echo-py)
- [tests/migration/test_agent_readiness.py](#module-tests-migration-test-agent-readiness-py)
- [tests/migration/test_background_runs.py](#module-tests-migration-test-background-runs-py)
- [tests/migration/test_bridge.py](#module-tests-migration-test-bridge-py)
- [tests/migration/test_bridge_process.py](#module-tests-migration-test-bridge-process-py)
- [tests/migration/test_child_execution.py](#module-tests-migration-test-child-execution-py)
- [tests/migration/test_delegation.py](#module-tests-migration-test-delegation-py)
- [tests/migration/test_ide_acceptance.py](#module-tests-migration-test-ide-acceptance-py)
- [tests/migration/test_ide_sessions.py](#module-tests-migration-test-ide-sessions-py)
- [tests/migration/test_json_protocol.py](#module-tests-migration-test-json-protocol-py)
- [tests/migration/test_model_discovery.py](#module-tests-migration-test-model-discovery-py)
- [tests/migration/test_model_probe.py](#module-tests-migration-test-model-probe-py)
- [tests/migration/test_neural_speech.py](#module-tests-migration-test-neural-speech-py)
- [tests/migration/test_project_memory_v2.py](#module-tests-migration-test-project-memory-v2-py)
- [tests/migration/test_run_control.py](#module-tests-migration-test-run-control-py)
- [tests/migration/test_run_owner_restart.py](#module-tests-migration-test-run-owner-restart-py)
- [tests/migration/test_stage17_workflow.py](#module-tests-migration-test-stage17-workflow-py)
- [tests/migration/test_streaming.py](#module-tests-migration-test-streaming-py)
- [tests/migration/test_task_graph_execution.py](#module-tests-migration-test-task-graph-execution-py)
- [tests/migration/test_task_service.py](#module-tests-migration-test-task-service-py)
- [tests/migration/test_transcription.py](#module-tests-migration-test-transcription-py)
- [tests/migration/test_tts_server.py](#module-tests-migration-test-tts-server-py)
- [tests/migration/test_workspace_workflow.py](#module-tests-migration-test-workspace-workflow-py)
- [tests/test_agent_benchmark.py](#module-tests-test-agent-benchmark-py)
- [tests/test_approval_flow.py](#module-tests-test-approval-flow-py)
- [tests/test_assistant_service.py](#module-tests-test-assistant-service-py)
- [tests/test_auto_budget.py](#module-tests-test-auto-budget-py)
- [tests/test_call_journal.py](#module-tests-test-call-journal-py)
- [tests/test_chat_store.py](#module-tests-test-chat-store-py)
- [tests/test_companion_policy.py](#module-tests-test-companion-policy-py)
- [tests/test_context_builder.py](#module-tests-test-context-builder-py)
- [tests/test_conversation_history.py](#module-tests-test-conversation-history-py)
- [tests/test_core_reliability.py](#module-tests-test-core-reliability-py)
- [tests/test_docs_reference.py](#module-tests-test-docs-reference-py)
- [tests/test_editor_io.py](#module-tests-test-editor-io-py)
- [tests/test_editor_service.py](#module-tests-test-editor-service-py)
- [tests/test_expansion.py](#module-tests-test-expansion-py)
- [tests/test_file_editing.py](#module-tests-test-file-editing-py)
- [tests/test_ide_completion.py](#module-tests-test-ide-completion-py)
- [tests/test_ide_execution.py](#module-tests-test-ide-execution-py)
- [tests/test_ide_remote_control.py](#module-tests-test-ide-remote-control-py)
- [tests/test_ide_verification.py](#module-tests-test-ide-verification-py)
- [tests/test_json_compatibility.py](#module-tests-test-json-compatibility-py)
- [tests/test_limits.py](#module-tests-test-limits-py)
- [tests/test_mcp_reliability.py](#module-tests-test-mcp-reliability-py)
- [tests/test_memory_service.py](#module-tests-test-memory-service-py)
- [tests/test_model_gateway.py](#module-tests-test-model-gateway-py)
- [tests/test_model_manager.py](#module-tests-test-model-manager-py)
- [tests/test_model_preferences.py](#module-tests-test-model-preferences-py)
- [tests/test_neutral_conversations.py](#module-tests-test-neutral-conversations-py)
- [tests/test_neutral_extensions.py](#module-tests-test-neutral-extensions-py)
- [tests/test_optional_ide.py](#module-tests-test-optional-ide-py)
- [tests/test_process_identity.py](#module-tests-test-process-identity-py)
- [tests/test_project_command.py](#module-tests-test-project-command-py)
- [tests/test_project_index.py](#module-tests-test-project-index-py)
- [tests/test_project_knowledge.py](#module-tests-test-project-knowledge-py)
- [tests/test_project_memory.py](#module-tests-test-project-memory-py)
- [tests/test_project_search.py](#module-tests-test-project-search-py)
- [tests/test_request_budget.py](#module-tests-test-request-budget-py)
- [tests/test_response_quality.py](#module-tests-test-response-quality-py)
- [tests/test_responses_adapter.py](#module-tests-test-responses-adapter-py)
- [tests/test_run_policy.py](#module-tests-test-run-policy-py)
- [tests/test_run_registry.py](#module-tests-test-run-registry-py)
- [tests/test_run_state.py](#module-tests-test-run-state-py)
- [tests/test_runtime_architecture.py](#module-tests-test-runtime-architecture-py)
- [tests/test_runtime_service.py](#module-tests-test-runtime-service-py)
- [tests/test_sandbox.py](#module-tests-test-sandbox-py)
- [tests/test_scoped_verification.py](#module-tests-test-scoped-verification-py)
- [tests/test_services_and_sessions.py](#module-tests-test-services-and-sessions-py)
- [tests/test_smart_context.py](#module-tests-test-smart-context-py)
- [tests/test_speech_service.py](#module-tests-test-speech-service-py)
- [tests/test_stage17_verification.py](#module-tests-test-stage17-verification-py)
- [tests/test_stage9_reliability.py](#module-tests-test-stage9-reliability-py)
- [tests/test_storage.py](#module-tests-test-storage-py)
- [tests/test_subagent_profiles.py](#module-tests-test-subagent-profiles-py)
- [tests/test_task_activity.py](#module-tests-test-task-activity-py)
- [tests/test_task_graph.py](#module-tests-test-task-graph-py)
- [tests/test_task_store.py](#module-tests-test-task-store-py)
- [tests/test_tool_execution.py](#module-tests-test-tool-execution-py)
- [tests/test_windows_dependencies.py](#module-tests-test-windows-dependencies-py)
- [tests/test_workspace_tools.py](#module-tests-test-workspace-tools-py)

<a id="module-tests-fixtures-lsp-diagnostics-py"></a>

## `tests/fixtures/lsp_diagnostics.py`

Локальный LSP fixture: чужой URI, попытка applyEdit, диагностика после отказа и режим зависшего stdin.

### `main`

[Исходник](../../tests/fixtures/lsp_diagnostics.py#L9)

```python
def main()
```

Обслуживает реальные JSON-RPC frames fixture; выдаёт диагностику только после отказа applyEdit, --stall не читает stdin для проверки отмены.

<a id="module-tests-fixtures-mcp-echo-py"></a>

## `tests/fixtures/mcp_echo.py`

Настоящий локальный MCP сервер арифметики и ожидания для stdio/HTTP проверок.

### `add`

[Исходник](../../tests/fixtures/mcp_echo.py#L9)

```python
@server.tool()
def add(a: int, b: int) -> str
```

MCP fixture складывает два целых числа, чтобы проверка транспорта не затрагивала файлы и внешние сервисы.

### `wait_seconds`

[Исходник](../../tests/fixtures/mcp_echo.py#L14)

```python
@server.tool()
async def wait_seconds(seconds: int) -> str
```

Отложенный MCP ответ для проверки отмены и закрытия соединения.

### `session_identity`

[Исходник](../../tests/fixtures/mcp_echo.py#L20)

```python
@server.tool()
def session_identity() -> str
```

Возвращает только PID fixture процесса, чтобы проверить реальное переиспользование транспорта.

<a id="module-tests-migration-test-agent-readiness-py"></a>

## `tests/migration/test_agent_readiness.py`

Вертикальные A–I сценарии с HTTP-моделью, настоящими разрешениями, файлами, subprocess и контрольными точками в одноразовом проекте.

### `ReadinessHandler`

[Исходник](../../tests/migration/test_agent_readiness.py#L14)

```python
class ReadinessHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Вертикальные A–I сценарии с HTTP-моделью, настоящими разрешениями, файлами, subprocess и контрольными точками в одноразовом проекте.

### `ReadinessHandler.log_message`

[Исходник](../../tests/migration/test_agent_readiness.py#L17)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ReadinessHandler.do_GET`

[Исходник](../../tests/migration/test_agent_readiness.py#L20)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `ReadinessHandler.do_POST`

[Исходник](../../tests/migration/test_agent_readiness.py#L26)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `AgentReadinessTests`

[Исходник](../../tests/migration/test_agent_readiness.py#L63)

```python
class AgentReadinessTests(unittest.TestCase)
```

Тестовый класс/фикстура: Вертикальные A–I сценарии с HTTP-моделью, настоящими разрешениями, файлами, subprocess и контрольными точками в одноразовом проекте.

### `AgentReadinessTests.start`

[Исходник](../../tests/migration/test_agent_readiness.py#L68)

```python
def start(self, actions, *, options=None, protocol='native', history=None)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `AgentReadinessTests.finish`

[Исходник](../../tests/migration/test_agent_readiness.py#L82)

```python
def finish(self, decision='apply')
```

Обрабатывает настоящие approval events, проверяет состояния и освобождение scheduler после task_end.

### `AgentReadinessTests.check`

[Исходник](../../tests/migration/test_agent_readiness.py#L100)

```python
def check(self)
```

Описывает реальную Python-команду проверки временного проекта без записи bytecode.

### `AgentReadinessTests.fixture`

[Исходник](../../tests/migration/test_agent_readiness.py#L106)

```python
def fixture(self)
```

Создаёт ошибочную функцию и независимую исполняемую проверку в disposable проекте.

### `AgentReadinessTests.receipts`

[Исходник](../../tests/migration/test_agent_readiness.py#L110)

```python
def receipts(self)
```

Читает реальные tool results из канонической истории завершённой задачи.

### `AgentReadinessTests.test_a_exploration_returns_current_source_references`

[Исходник](../../tests/migration/test_agent_readiness.py#L113)

```python
def test_a_exploration_returns_current_source_references(self)
```

Проверка: исследование возвращает актуальные строки файла и корректную ссылку.

### `AgentReadinessTests.test_b_simple_edit_and_real_test`

[Исходник](../../tests/migration/test_agent_readiness.py#L122)

```python
def test_b_simple_edit_and_real_test(self)
```

Проверка: правка проходит diff approval, затем настоящий Python-тест подтверждает результат.

### `AgentReadinessTests.test_c_multi_file_json_edit_and_test`

[Исходник](../../tests/migration/test_agent_readiness.py#L132)

```python
def test_c_multi_file_json_edit_and_test(self)
```

Проверка: strict JSON выполняет согласованные правки двух файлов и реальную проверку.

### `AgentReadinessTests.test_d_failed_auto_check_returns_to_model_and_recovers`

[Исходник](../../tests/migration/test_agent_readiness.py#L144)

```python
def test_d_failed_auto_check_returns_to_model_and_recovers(self)
```

Проверка: AssertionError автоматической проверки возвращается модели; исправление и повторный тест дают успех.

### `AgentReadinessTests.test_d_auto_checks_run_even_without_file_edits`

[Исходник](../../tests/migration/test_agent_readiness.py#L158)

```python
def test_d_auto_checks_run_even_without_file_edits(self)
```

Проверка: заданные пользователем auto checks выполняются и без предшествующей записи.

### `AgentReadinessTests.test_g_denied_auto_check_is_not_automatically_replayed`

[Исходник](../../tests/migration/test_agent_readiness.py#L166)

```python
def test_g_denied_auto_check_is_not_automatically_replayed(self)
```

Проверка: отказ проверки сохраняется и не вызывает повторного approval.

### `AgentReadinessTests.test_g_rejected_edit_is_returned_to_model`

[Исходник](../../tests/migration/test_agent_readiness.py#L174)

```python
def test_g_rejected_edit_is_returned_to_model(self)
```

Проверка: отклонённая правка не меняет файл, USER_DENIED возвращается следующему запросу.

### `AgentReadinessTests.test_g_repeated_denied_command_does_not_prompt_again`

[Исходник](../../tests/migration/test_agent_readiness.py#L184)

```python
def test_g_repeated_denied_command_does_not_prompt_again(self)
```

Проверка: смена purpose/check_id не позволяет повторно предложить отклонённую команду в том же запуске.

### `AgentReadinessTests.test_e_h_long_task_retains_goal_and_uses_full_canonical_history`

[Исходник](../../tests/migration/test_agent_readiness.py#L196)

```python
def test_e_h_long_task_retains_goal_and_uses_full_canonical_history(self)
```

Проверка: 24 больших результата превышают рабочий контекст, но цель, ссылки и полная история сохраняются.

### `AgentReadinessTests.test_e_h_long_task_retains_goal_and_uses_full_canonical_history.decide`

[Исходник](../../tests/migration/test_agent_readiness.py#L200)

```python
def decide(index, payload)
```

Проверяет сохранение цели в каждом HTTP-запросе и последовательно выбирает 24 различных файла.

### `AgentReadinessTests.test_i_cancel_approval_then_resume_without_duplicate_effect`

[Исходник](../../tests/migration/test_agent_readiness.py#L212)

```python
def test_i_cancel_approval_then_resume_without_duplicate_effect(self)
```

Проверка: остановка на approval сохраняет resumable checkpoint без повторения эффекта.

<a id="module-tests-migration-test-background-runs-py"></a>

## `tests/migration/test_background_runs.py`

Real HTTP tests of two engine workers, isolated streams, queued cancellation, approvals and full shutdown.

### `BackgroundRunTests`

[Исходник](../../tests/migration/test_background_runs.py#L11)

```python
class BackgroundRunTests(unittest.TestCase)
```

Тестовый класс/фикстура: Real HTTP tests of two engine workers, isolated streams, queued cancellation, approvals and full shutdown.

### `BackgroundRunTests.install_handler`

[Исходник](../../tests/migration/test_background_runs.py#L15)

```python
def install_handler(self)
```

Ставит локальную SSE fixture с удерживаемым потоком и write approval; пользовательские серверы не используются.

### `BackgroundRunTests.install_handler.Handler`

[Исходник](../../tests/migration/test_background_runs.py#L19)

```python
class Handler(BaseHTTPRequestHandler)
```

Локальный OpenAI-compatible HTTP handler для двух независимых engine workers.

### `BackgroundRunTests.install_handler.Handler.log_message`

[Исходник](../../tests/migration/test_background_runs.py#L20)

```python
def log_message(self, *args)
```

Подавляет журнал HTTP fixture в отчёте тестов.

### `BackgroundRunTests.install_handler.Handler.do_GET`

[Исходник](../../tests/migration/test_background_runs.py#L22)

```python
def do_GET(self)
```

Объявляет одну fixture модель для runtime discovery.

### `BackgroundRunTests.install_handler.Handler.do_POST`

[Исходник](../../tests/migration/test_background_runs.py#L26)

```python
def do_POST(self)
```

Удерживает alpha stream, возвращает write tool или финал; закрытый клиент не превращается в серверный сбой.

### `BackgroundRunTests.event`

[Исходник](../../tests/migration/test_background_runs.py#L45)

```python
def event(self, name, chat_id=None)
```

Ждёт конкретный тип события и chat_id; ошибки engine считаются провалом теста.

### `BackgroundRunTests.wait_queued`

[Исходник](../../tests/migration/test_background_runs.py#L53)

```python
def wait_queued(self, run)
```

Проверяет durable queued reservation второго запуска, не подменяя scheduler.

### `BackgroundRunTests.test_switch_and_cancel_queued_chat_preserve_other_live_stream`

[Исходник](../../tests/migration/test_background_runs.py#L60)

```python
def test_switch_and_cancel_queued_chat_preserve_other_live_stream(self)
```

Проверка: Возврат к живому потоку не делает crash recovery; отмена очереди не отправляет HTTP и не меняет другой чат.

### `BackgroundRunTests.test_two_approvals_are_scoped_and_same_workspace_has_one_writer`

[Исходник](../../tests/migration/test_background_runs.py#L90)

```python
def test_two_approvals_are_scoped_and_same_workspace_has_one_writer(self)
```

Проверка: Два проекта получают разные approvals; чужое решение отклоняется, отменённый проект не меняется, один root имеет одного writer.

### `BackgroundRunTests.test_shutdown_cancels_all_owners_and_mismatched_models_are_not_started`

[Исходник](../../tests/migration/test_background_runs.py#L112)

```python
def test_shutdown_cancels_all_owners_and_mismatched_models_are_not_started(self)
```

Проверка: Shutdown отменяет владельцев и очередь; разные model bindings не запускаются одновременно, закрытый service не принимает работу.

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

### `BridgeTests.test_nested_explorer_paths_match_editor_paths`

[Исходник](../../tests/migration/test_bridge.py#L60)

```python
def test_nested_explorer_paths_match_editor_paths(self)
```

Проверка: Вложенный путь проводника совпадает с каноническим POSIX-путём вкладки на Windows.

### `BridgeTests.test_parent_traversal_rejected`

[Исходник](../../tests/migration/test_bridge.py#L67)

```python
def test_parent_traversal_rejected(self)
```

Проверка: Bridge не разрешает ../ за пределами проекта.

### `BridgeTests.test_write_is_not_exposed`

[Исходник](../../tests/migration/test_bridge.py#L69)

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

### `BridgeProcessTests.test_index_search_updates_and_controls_in_real_core`

[Исходник](../../tests/migration/test_bridge_process.py#L119)

```python
def test_index_search_updates_and_controls_in_real_core(self)
```

Проверка: реальный JSON-lines Core активирует индекс, видит внешний edit без full scan и поддерживает cancel/rebuild/fallback.

### `BridgeProcessTests.test_companion_profile_and_history_are_independent_in_real_process`

[Исходник](../../tests/migration/test_bridge_process.py#L149)

```python
def test_companion_profile_and_history_are_independent_in_real_process(self)
```

Проверка: Через настоящий stdio/Core проверяет отдельную модель, отсутствие ключей в ответах, разделение истории, cross-scope отказ и перенос старого чата.

### `BridgeProcessTests.test_desktop_telegram_and_invalid_stt_keep_real_bridge_responsive`

[Исходник](../../tests/migration/test_bridge_process.py#L164)

```python
def test_desktop_telegram_and_invalid_stt_keep_real_bridge_responsive(self)
```

Проверка: Через настоящий процесс проверяет PC opt-in, безопасный Telegram status, отказ невалидному аудио и отзывчивость health.

### `BridgeProcessTests.test_project_memory_and_chat_rename_are_scoped`

[Исходник](../../tests/migration/test_bridge_process.py#L173)

```python
def test_project_memory_and_chat_rename_are_scoped(self)
```

Проверка: Реальный JSON bridge проверяет root памяти, stale revision и scope переименования.

### `BridgeProcessTests.test_runtime_commands_validate_without_blocking_other_commands`

[Исходник](../../tests/migration/test_bridge_process.py#L185)

```python
def test_runtime_commands_validate_without_blocking_other_commands(self)
```

Проверка: Bridge status/start validation/stop не нарушают health без модели.

### `BridgeProcessTests.test_project_search_requires_root_and_does_not_block_bridge`

[Исходник](../../tests/migration/test_bridge_process.py#L192)

```python
def test_project_search_requires_root_and_does_not_block_bridge(self)
```

Проверка: Настоящий bridge требует root, возвращает строку поиска и остаётся доступен health/cancel.

### `BridgeProcessTests.test_process_kill_before_headers_recovers_user_request_and_paused_task`

[Исходник](../../tests/migration/test_bridge_process.py#L202)

```python
def test_process_kill_before_headers_recovers_user_request_and_paused_task(self)
```

Проверка: Реальный kill subprocess до HTTP-заголовков сохраняет запрос и paused при открытии.

### `BridgeProcessTests.test_approved_write_and_preferences_survive_process_restart`

[Исходник](../../tests/migration/test_bridge_process.py#L209)

```python
def test_approved_write_and_preferences_survive_process_restart(self)
```

Проверка: Подтверждённая запись и настройки переживают рестарт bridge; ключ не попадает в JSON.

### `BridgeProcessTests.test_process_kill_during_stream_recovers_partial_once`

[Исходник](../../tests/migration/test_bridge_process.py#L223)

```python
def test_process_kill_during_stream_recovers_partial_once(self)
```

Проверка: Реальный kill во время паузы SSE восстанавливает последний сохранённый фрагмент без дубля.

### `BridgeProcessTests.test_process_kill_during_approval_never_replays_permission`

[Исходник](../../tests/migration/test_bridge_process.py#L247)

```python
def test_process_kill_during_approval_never_replays_permission(self)
```

Проверка: После kill во время approval старые ID отклоняются, resume требует нового согласия.

### `BridgeProcessTests.start_discovery_server`

[Исходник](../../tests/migration/test_bridge_process.py#L265)

```python
def start_discovery_server(self, mode)
```

Запускает управляемую HTTP-фикстуру и отправляет discovery в реальный bridge subprocess.

### `BridgeProcessTests.test_bridge_models_discovery_keeps_commands_responsive_and_pins_config`

[Исходник](../../tests/migration/test_bridge_process.py#L280)

```python
def test_bridge_models_discovery_keeps_commands_responsive_and_pins_config(self)
```

Проверка: JSON-lines отвечает на health/новые команды во время discovery, ограничивает worker и сохраняет снимок настроек.

### `BridgeProcessTests.test_draft_probe_keeps_bridge_responsive_and_can_be_cancelled`

[Исходник](../../tests/migration/test_bridge_process.py#L290)

```python
def test_draft_probe_keeps_bridge_responsive_and_can_be_cancelled(self)
```

Проверка: Во время зависшего probe реальный bridge отвечает health/cancel и сохраняет прежнюю конфигурацию.

### `BridgeProcessTests.test_bridge_cancel_closes_discovery_socket`

[Исходник](../../tests/migration/test_bridge_process.py#L311)

```python
def test_bridge_cancel_closes_discovery_socket(self)
```

Проверка: cancel_task отвечает без ожидания discovery и закрывает его HTTP-сокет.

### `BridgeProcessTests.until`

[Исходник](../../tests/migration/test_bridge_process.py#L319)

```python
def until(self, predicate)
```

Ожидает подходящее сообщение, сохраняя остальные для дальнейших проверок.

### `BridgeProcessTests.call`

[Исходник](../../tests/migration/test_bridge_process.py#L330)

```python
def call(self, method, **params)
```

Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.

### `BridgeProcessTests.test_malformed_input_does_not_reuse_previous_request_id`

[Исходник](../../tests/migration/test_bridge_process.py#L337)

```python
def test_malformed_input_does_not_reuse_previous_request_id(self)
```

Проверка: Ошибка JSON не получает ID предыдущей команды и не ломает следующий запрос.

### `BridgeProcessTests.test_bridge_remains_responsive_during_write_approval`

[Исходник](../../tests/migration/test_bridge_process.py#L346)

```python
def test_bridge_remains_responsive_during_write_approval(self)
```

Проверка: Реальный Core отвечает на health/cancel, пока engine ждёт согласия.

### `BridgeProcessTests.test_optional_lsp_is_opt_in_cancellable_and_bridge_stays_responsive`

[Исходник](../../tests/migration/test_bridge_process.py#L371)

```python
def test_optional_lsp_is_opt_in_cancellable_and_bridge_stays_responsive(self)
```

Проверка: настоящий Core process отвечает health/cancel во время LSP, блокирует смену проекта и затем принимает повторный успешный запуск.

<a id="module-tests-migration-test-child-execution-py"></a>

## `tests/migration/test_child_execution.py`

Real HTTP parent-child-parent, cancellation, denied child writes, stale handback, OOM and pre-HTTP spending admission.

### `ChildHandler`

[Исходник](../../tests/migration/test_child_execution.py#L9)

```python
class ChildHandler(BaseHTTPRequestHandler)
```

HTTP fixture для реального parent-child-parent, ошибок памяти и попытки запрещённой записи ребёнком.

### `ChildHandler.log_message`

[Исходник](../../tests/migration/test_child_execution.py#L10)

```python
def log_message(self, *args)
```

Подавляет локальный HTTP access log.

### `ChildHandler.do_GET`

[Исходник](../../tests/migration/test_child_execution.py#L12)

```python
def do_GET(self)
```

Объявляет только synthetic fixture модель.

### `ChildHandler.do_POST`

[Исходник](../../tests/migration/test_child_execution.py#L15)

```python
def do_POST(self)
```

Возвращает delegate/read/final либо OOM; удерживает child stream для проверки отмены и stale handback.

### `ChildExecutionTests`

[Исходник](../../tests/migration/test_child_execution.py#L38)

```python
class ChildExecutionTests(unittest.TestCase)
```

Тестовый класс/фикстура: Real HTTP parent-child-parent, cancellation, denied child writes, stale handback, OOM and pre-HTTP spending admission.

### `ChildExecutionTests.start`

[Исходник](../../tests/migration/test_child_execution.py#L43)

```python
def start(self, hold=False, options=None)
```

Настраивает изолированный root и запускает реальный native engine с optional child hold.

### `ChildExecutionTests.test_parent_child_handoff_joins_and_ledger_matches_real_http`

[Исходник](../../tests/migration/test_child_execution.py#L49)

```python
def test_parent_child_handoff_joins_and_ledger_matches_real_http(self)
```

Проверка: Настоящая цепочка parent-child-parent даёт четыре HTTP, отдельные child rights/evidence и нулевые reservations после join.

### `ChildExecutionTests.test_parent_cancel_cascades_and_closes_child_transport`

[Исходник](../../tests/migration/test_child_execution.py#L63)

```python
def test_parent_cancel_cascades_and_closes_child_transport(self)
```

Проверка: Stop родителя прерывает child stream, освобождает scheduler и приостанавливает оба runs.

### `ChildExecutionTests.test_child_transport_failure_returns_control_to_parent`

[Исходник](../../tests/migration/test_child_execution.py#L69)

```python
def test_child_transport_failure_returns_control_to_parent(self)
```

Проверка: после ограниченных HTTP-повторов ошибка ребёнка возвращается родителю и освобождает scheduler.

### `ChildExecutionTests.test_changed_source_discards_entire_child_answer`

[Исходник](../../tests/migration/test_child_execution.py#L79)

```python
def test_changed_source_discards_entire_child_answer(self)
```

Проверка: Изменение файла перед handback удаляет весь child answer вместо передачи stale фактов.

### `ChildExecutionTests.test_changed_source_discards_entire_child_answer.checkpoint`

[Исходник](../../tests/migration/test_child_execution.py#L87)

```python
def checkpoint(*args, **kwargs)
```

Детерминированно меняет synthetic source после child completion до свежести handback.

### `ChildExecutionTests.test_memory_exhaustion_pauses_without_retry`

[Исходник](../../tests/migration/test_child_execution.py#L97)

```python
def test_memory_exhaustion_pauses_without_retry(self)
```

Проверка: OOM fixture получает один HTTP, задача paused с понятной причиной и без повторного запроса.

### `ChildExecutionTests.test_child_cannot_gain_write_permission_from_model_output`

[Исходник](../../tests/migration/test_child_execution.py#L104)

```python
def test_child_cannot_gain_write_permission_from_model_output(self)
```

Проверка: Смоделированный запрещённый write ребёнка не создаёт файл и не выдаёт права/approval.

### `ChildExecutionTests.test_explicit_external_budget_blocks_before_physical_http`

[Исходник](../../tests/migration/test_child_execution.py#L110)

```python
def test_explicit_external_budget_blocks_before_physical_http(self)
```

Проверка: Явный внешний budget отклоняет запрос до физического POST и сохраняет task paused.

### `ChildExecutionTests.test_user_profile_narrows_child_tools_and_persists_exact_version`

[Исходник](../../tests/migration/test_child_execution.py#L121)

```python
def test_user_profile_narrows_child_tools_and_persists_exact_version(self)
```

Проверка: Настоящий child HTTP получает только пересечение tools, checkpoint хранит точный профиль и версию.

### `ChildExecutionTests.test_disabled_profile_does_not_create_child_or_inference`

[Исходник](../../tests/migration/test_child_execution.py#L133)

```python
def test_disabled_profile_does_not_create_child_or_inference(self)
```

Проверка: Выключенный черновик даёт ACCESS_DENIED без child run и лишних HTTP.

### `ChildExecutionTests.test_disabling_subagents_preserves_single_agent_without_child_tools`

[Исходник](../../tests/migration/test_child_execution.py#L141)

```python
def test_disabling_subagents_preserves_single_agent_without_child_tools(self)
```

Проверка: Общий switch удаляет делегирование и создание профилей, сохраняя штатное чтение основного агента.

### `ChildExecutionTests.test_chat_explains_subagent_mode_without_exposing_project_tools`

[Исходник](../../tests/migration/test_child_execution.py#L148)

```python
def test_chat_explains_subagent_mode_without_exposing_project_tools(self)
```

Проверка: Chat объясняет доступность субагентов в IDE без выдачи файловых или дочерних инструментов.

### `ChildExecutionTests.test_readonly_parent_hint_matches_child_capabilities`

[Исходник](../../tests/migration/test_child_execution.py#L160)

```python
def test_readonly_parent_hint_matches_child_capabilities(self)
```

Проверка: readonly родитель может делегировать чтение, но подсказка и схемы не обещают создание профиля.

### `ChildExecutionTests.test_model_creates_only_disabled_draft_via_real_tool_dispatch`

[Исходник](../../tests/migration/test_child_execution.py#L169)

```python
def test_model_creates_only_disabled_draft_via_real_tool_dispatch(self)
```

Проверка: Настоящий parent tool dispatch создаёт выключенный model draft без запуска дочерней модели.

<a id="module-tests-migration-test-delegation-py"></a>

## `tests/migration/test_delegation.py`

Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории.

### `DelegationHandler`

[Исходник](../../tests/migration/test_delegation.py#L16)

```python
class DelegationHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории.

### `DelegationHandler.log_message`

[Исходник](../../tests/migration/test_delegation.py#L17)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `DelegationHandler.do_POST`

[Исходник](../../tests/migration/test_delegation.py#L19)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `DelegationTests`

[Исходник](../../tests/migration/test_delegation.py#L29)

```python
class DelegationTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории.

### `DelegationTests.test_independent_model_delegates_and_returns_result`

[Исходник](../../tests/migration/test_delegation.py#L30)

```python
def test_independent_model_delegates_and_returns_result(self)
```

Проверка: Изолирует ID моделей и чаты, выполняет delegate_task и возвращает MAIN_MODEL_RESULT в исходную историю Лолы.

<a id="module-tests-migration-test-ide-acceptance-py"></a>

## `tests/migration/test_ide_acceptance.py`

Реальный HTTP workflow plan/write/command/rollback/recheck и отказ исполнения write в режиме чтения.

### `AcceptanceHandler`

[Исходник](../../tests/migration/test_ide_acceptance.py#L17)

```python
class AcceptanceHandler(BaseHTTPRequestHandler)
```

Локальный HTTP/SSE fixture выдаёт конкретный plan, write и final либо намеренно запрещённый readonly write.

### `AcceptanceHandler.log_message`

[Исходник](../../tests/migration/test_ide_acceptance.py#L18)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `AcceptanceHandler.do_POST`

[Исходник](../../tests/migration/test_ide_acceptance.py#L19)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `IdeAcceptanceTests`

[Исходник](../../tests/migration/test_ide_acceptance.py#L40)

```python
class IdeAcceptanceTests(unittest.TestCase)
```

Поднимает настоящий bridge service и HTTP сервер с временным profile/project.

### `IdeAcceptanceTests.setUp`

[Исходник](../../tests/migration/test_ide_acceptance.py#L41)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `IdeAcceptanceTests.finish`

[Исходник](../../tests/migration/test_ide_acceptance.py#L53)

```python
def finish(self)
```

Обрабатывает реальные approval events, подтверждает предложенные команды и ждёт task_end без ошибок.

### `IdeAcceptanceTests.test_http_plan_auto_check_rollback_and_failed_recheck`

[Исходник](../../tests/migration/test_ide_acceptance.py#L64)

```python
def test_http_plan_auto_check_rollback_and_failed_recheck(self)
```

Проверка: HTTP plan и write, обычное одобрение post-edit команды, stale после rollback и failed recheck без дополнительных model requests.

### `IdeAcceptanceTests.test_read_only_http_malicious_call_is_not_dispatched`

[Исходник](../../tests/migration/test_ide_acceptance.py#L87)

```python
def test_read_only_http_malicious_call_is_not_dispatched(self)
```

Проверка: навязанный моделью write блокируется даже при отсутствии schema в readonly payload, без approval и изменения файла.

### `IdeAcceptanceTests.test_scoped_check_runs_on_large_project_and_reloads_without_model`

[Исходник](../../tests/migration/test_ide_acceptance.py#L97)

```python
def test_scoped_check_runs_on_large_project_and_reloads_without_model(self)
```

Проверка: Core проводит checks-only/approval/save/reload выбранного файла с большим посторонним файлом и без model request.

<a id="module-tests-migration-test-ide-sessions-py"></a>

## `tests/migration/test_ide_sessions.py`

Bridge-проверки изоляции workspace, editor receipts и отмены закрытого IDE view.

### `IdeScopeBridgeTests`

[Исходник](../../tests/migration/test_ide_sessions.py#L11)

```python
class IdeScopeBridgeTests(unittest.TestCase)
```

Реальный bridge fixture с несколькими независимыми IDE views.

### `IdeScopeBridgeTests.scoped`

[Исходник](../../tests/migration/test_ide_sessions.py#L20)

```python
def scoped(self, scope, operation, **params)
```

Вызывает bridge method в явно выбранной IDE-сессии.

### `IdeScopeBridgeTests.test_ide_root_and_selection_do_not_mutate_desktop_or_other_view`

[Исходник](../../tests/migration/test_ide_sessions.py#L25)

```python
def test_ide_root_and_selection_do_not_mutate_desktop_or_other_view(self)
```

Выбор корня и чата одной IDE не меняет desktop или соседний view.

### `IdeScopeBridgeTests.test_editor_prepare_apply_receipts_are_scoped_and_python_never_writes`

[Исходник](../../tests/migration/test_ide_sessions.py#L38)

```python
def test_editor_prepare_apply_receipts_are_scoped_and_python_never_writes(self)
```

Ответы prepare/apply привязаны к editor scope, Python writer не выполняется.

### `IdeScopeBridgeTests.test_closed_ide_cancels_only_its_run_before_file_effect`

[Исходник](../../tests/migration/test_ide_sessions.py#L58)

```python
def test_closed_ide_cancels_only_its_run_before_file_effect(self)
```

Закрытие IDE отменяет её run до файлового эффекта, не затрагивая другие.

<a id="module-tests-migration-test-json-protocol-py"></a>

## `tests/migration/test_json_protocol.py`

Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor.

### `JsonOnlyHandler`

[Исходник](../../tests/migration/test_json_protocol.py#L16)

```python
class JsonOnlyHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor.

### `JsonOnlyHandler.log_message`

[Исходник](../../tests/migration/test_json_protocol.py#L17)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `JsonOnlyHandler.do_POST`

[Исходник](../../tests/migration/test_json_protocol.py#L19)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `JsonProtocolTests`

[Исходник](../../tests/migration/test_json_protocol.py#L38)

```python
class JsonProtocolTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor.

### `JsonProtocolTests.test_json_only_model_uses_same_write_approval`

[Исходник](../../tests/migration/test_json_protocol.py#L39)

```python
def test_json_only_model_uses_same_write_approval(self)
```

Проверка: Сервер отвергает native tools API, но JSON read/write проходят через реальный HTTP и обязательный diff approval.

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

<a id="module-tests-migration-test-neural-speech-py"></a>

## `tests/migration/test_neural_speech.py`

HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.

### `NeuralSpeechTests`

[Исходник](../../tests/migration/test_neural_speech.py#L14)

```python
class NeuralSpeechTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.

### `NeuralSpeechTests.test_http_busy_and_deadline_have_actionable_messages`

[Исходник](../../tests/migration/test_neural_speech.py#L15)

```python
def test_http_busy_and_deadline_have_actionable_messages(self)
```

Проверка: Проверяет понятные сообщения Core для HTTP 429/504 без отправки звука и показа HTTPStatusError.

### `NeuralSpeechTests.test_http_busy_and_deadline_have_actionable_messages.Handler`

[Исходник](../../tests/migration/test_neural_speech.py#L18)

```python
class Handler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.

### `NeuralSpeechTests.test_http_busy_and_deadline_have_actionable_messages.Handler.do_POST`

[Исходник](../../tests/migration/test_neural_speech.py#L19)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `NeuralSpeechTests.test_http_busy_and_deadline_have_actionable_messages.Handler.log_message`

[Исходник](../../tests/migration/test_neural_speech.py#L21)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `NeuralSpeechTests.test_http_audio_and_exact_playback_sequence`

[Исходник](../../tests/migration/test_neural_speech.py#L32)

```python
def test_http_audio_and_exact_playback_sequence(self)
```

Проверка: Проверяет реальный HTTP WAV, русский язык/описание, предел текста и отказ устаревшему sequence.

### `NeuralSpeechTests.test_http_audio_and_exact_playback_sequence.Handler`

[Исходник](../../tests/migration/test_neural_speech.py#L37)

```python
class Handler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.

### `NeuralSpeechTests.test_http_audio_and_exact_playback_sequence.Handler.do_POST`

[Исходник](../../tests/migration/test_neural_speech.py#L38)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `NeuralSpeechTests.test_http_audio_and_exact_playback_sequence.Handler.log_message`

[Исходник](../../tests/migration/test_neural_speech.py#L41)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `NeuralSpeechTests.test_http_audio_and_exact_playback_sequence.emit`

[Исходник](../../tests/migration/test_neural_speech.py#L45)

```python
def emit(event)
```

Собирает события тестовой нейроозвучки и сигнализирует о готовом WAV без вывода звука.

### `NeuralSpeechTests.test_cancel_closes_stalled_synthesis`

[Исходник](../../tests/migration/test_neural_speech.py#L61)

```python
def test_cancel_closes_stalled_synthesis(self)
```

Проверка: Отменяет запрос до headers менее чем за две секунды и запрещает поздний playback ack.

### `NeuralSpeechTests.test_cancel_closes_stalled_synthesis.Handler`

[Исходник](../../tests/migration/test_neural_speech.py#L63)

```python
class Handler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.

### `NeuralSpeechTests.test_cancel_closes_stalled_synthesis.Handler.do_POST`

[Исходник](../../tests/migration/test_neural_speech.py#L64)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `NeuralSpeechTests.test_cancel_closes_stalled_synthesis.Handler.log_message`

[Исходник](../../tests/migration/test_neural_speech.py#L65)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

<a id="module-tests-migration-test-project-memory-v2-py"></a>

## `tests/migration/test_project_memory_v2.py`

Настоящий parent HTTP flow: гипотеза модели, новые чаты, актуальные решения и исключение изменённых источников.

### `MemoryHandler`

[Исходник](../../tests/migration/test_project_memory_v2.py#L10)

```python
class MemoryHandler(BaseHTTPRequestHandler)
```

Управляемый localhost provider для настоящего read/remember/final/verification flow.

### `MemoryHandler.log_message`

[Исходник](../../tests/migration/test_project_memory_v2.py#L11)

```python
def log_message(self, *args)
```

Подавляет HTTP access log fixture.

### `MemoryHandler.do_GET`

[Исходник](../../tests/migration/test_project_memory_v2.py#L12)

```python
def do_GET(self)
```

Объявляет только synthetic модель изолированного теста.

### `MemoryHandler.do_POST`

[Исходник](../../tests/migration/test_project_memory_v2.py#L14)

```python
def do_POST(self)
```

Предлагает чтение и запись гипотезы либо финальный ответ; сохраняет реальные запросы для проверки контекста.

### `ProjectMemoryHttpTests`

[Исходник](../../tests/migration/test_project_memory_v2.py#L30)

```python
class ProjectMemoryHttpTests(unittest.TestCase)
```

Сквозные сценарии TaskService с отдельным профилем, включением памяти и новыми чатами.

### `ProjectMemoryHttpTests.start`

[Исходник](../../tests/migration/test_project_memory_v2.py#L35)

```python
def start(self, prompt)
```

Запускает native engine с памятью и ждёт terminal task с закрытым worker.

### `ProjectMemoryHttpTests.test_new_chat_receives_decision_and_hypothesis_but_changed_source_removes_both`

[Исходник](../../tests/migration/test_project_memory_v2.py#L40)

```python
def test_new_chat_receives_decision_and_hypothesis_but_changed_source_removes_both(self)
```

Проверка: Реальный engine сохраняет гипотезу и наблюдения, новый чат находит решение, внешний edit исключает его.

### `ProjectMemoryHttpTests.test_disabling_memory_group_removes_tools_and_automatic_projection`

[Исходник](../../tests/migration/test_project_memory_v2.py#L56)

```python
def test_disabling_memory_group_removes_tools_and_automatic_projection(self)
```

Проверка: Общий switch памяти исключает tools и автоматическую подачу данных следующему запуску.

### `ProjectMemoryHttpTests.test_external_memory_preview_is_text_and_rejection_keeps_data_out_of_model`

[Исходник](../../tests/migration/test_project_memory_v2.py#L67)

```python
def test_external_memory_preview_is_text_and_rejection_keeps_data_out_of_model(self)
```

Проверка: Внешняя модель получает данные памяти только после текстового preview; отказ не пропускает приватную запись ни в один HTTP payload.

<a id="module-tests-migration-test-run-control-py"></a>

## `tests/migration/test_run_control.py`

Независимая localhost сверка ledger с HTTP, stream_options retry, JSON repair, usage и diff approval.

### `Handler`

[Исходник](../../tests/migration/test_run_control.py#L14)

```python
class Handler(BaseHTTPRequestHandler)
```

Localhost OpenAI fixture: один отказ optional поля, malformed JSON, protocol repair или отдельная write proposal.

### `Handler.log_message`

[Исходник](../../tests/migration/test_run_control.py#L15)

```python
def log_message(self, *args)
```

Подавляет служебный HTTP шум; тест сохраняет структурированные requests в памяти.

### `Handler.do_GET`

[Исходник](../../tests/migration/test_run_control.py#L17)

```python
def do_GET(self)
```

Отдаёт минимальный каталог модели для локального auto discovery, без inference telemetry.

### `Handler.do_POST`

[Исходник](../../tests/migration/test_run_control.py#L21)

```python
def do_POST(self)
```

Независимо считает POST и отправляет SSE/usage; первый stream_options отказ не содержит usage.

### `RunControlHttpTests`

[Исходник](../../tests/migration/test_run_control.py#L36)

```python
class RunControlHttpTests(unittest.TestCase)
```

Реальный TaskService/SDK/HTTP с изолированным профилем и очередью событий.

### `RunControlHttpTests.setUp`

[Исходник](../../tests/migration/test_run_control.py#L37)

```python
def setUp(self)
```

Подменяет profile constants, запускает localhost сервер и конфигурирует Core без пользовательских данных.

### `RunControlHttpTests.stop_server`

[Исходник](../../tests/migration/test_run_control.py#L49)

```python
def stop_server(self)
```

Завершает сервер и его listener после cleanup Core.

### `RunControlHttpTests.event`

[Исходник](../../tests/migration/test_run_control.py#L52)

```python
def event(self, name)
```

Ожидает конкретное Core событие, немедленно поднимает ошибку при failed.

### `RunControlHttpTests.test_physical_attempts_include_optional_field_retry_and_json_repair_once`

[Исходник](../../tests/migration/test_run_control.py#L58)

```python
def test_physical_attempts_include_optional_field_retry_and_json_repair_once(self)
```

Проверка: Три физические POST попытки совпадают с ledger: optional retry и JSON repair; usage дважды не считается.

### `RunControlHttpTests.test_waiting_write_approval_has_no_generation_lease_and_cancel_preserves_file`

[Исходник](../../tests/migration/test_run_control.py#L69)

```python
def test_waiting_write_approval_has_no_generation_lease_and_cancel_preserves_file(self)
```

Проверка: Diff approval не удерживает модель, Stop не пишет файл и завершает epoch paused.

<a id="module-tests-migration-test-run-owner-restart-py"></a>

## `tests/migration/test_run_owner_restart.py`

Kill/restart of a real isolated Core with streamed and queued chats, durable ledger and invalidated write consent.

### `RestartHandler`

[Исходник](../../tests/migration/test_run_owner_restart.py#L12)

```python
class RestartHandler(BaseHTTPRequestHandler)
```

Локальная SSE fixture: удерживаемый ответ либо неподтверждённый write tool, без обращения к внешней модели.

### `RestartHandler.log_message`

[Исходник](../../tests/migration/test_run_owner_restart.py#L13)

```python
def log_message(self, *args)
```

Подавляет HTTP fixture access log.

### `RestartHandler.do_GET`

[Исходник](../../tests/migration/test_run_owner_restart.py#L15)

```python
def do_GET(self)
```

Возвращает одну fixture модель для runtime discovery Core.

### `RestartHandler.do_POST`

[Исходник](../../tests/migration/test_run_owner_restart.py#L19)

```python
def do_POST(self)
```

Отправляет сохраняемый фрагмент или write proposal; держит socket до закрытия убитым тестовым Core.

### `RunOwnerRestartTests`

[Исходник](../../tests/migration/test_run_owner_restart.py#L33)

```python
class RunOwnerRestartTests(unittest.TestCase)
```

Тестовый класс/фикстура: Kill/restart of a real isolated Core with streamed and queued chats, durable ledger and invalidated write consent.

### `RunOwnerRestartTests.server`

[Исходник](../../tests/migration/test_run_owner_restart.py#L42)

```python
def server(self)
```

Поднимает отдельный HTTP fixture и конфигурирует только изолированный профиль subprocess Core.

### `RunOwnerRestartTests.restart`

[Исходник](../../tests/migration/test_run_owner_restart.py#L49)

```python
def restart(self)
```

Убивает только принадлежащий тесту Core, дожидается выхода и запускает новый процесс с тем же тестовым профилем.

### `RunOwnerRestartTests.test_kill_recovers_stream_and_queue_without_http_or_duplicate_fragment`

[Исходник](../../tests/migration/test_run_owner_restart.py#L54)

```python
def test_kill_recovers_stream_and_queue_without_http_or_duplicate_fragment(self)
```

Проверка: Настоящий kill/restart Core сохраняет один partial ответ, снимает очередь и reservations двух чатов без нового HTTP.

### `RunOwnerRestartTests.test_kill_invalidates_write_consent_without_replaying_the_action`

[Исходник](../../tests/migration/test_run_owner_restart.py#L79)

```python
def test_kill_invalidates_write_consent_without_replaying_the_action(self)
```

Проверка: Старый approval после kill/restart недействителен: файл не создаётся и write request автоматически не повторяется.

### `RunOwnerRestartTests.test_kill_recovers_parent_child_tree_without_restarting_child`

[Исходник](../../tests/migration/test_run_owner_restart.py#L91)

```python
def test_kill_recovers_parent_child_tree_without_restarting_child(self)
```

Проверка: Kill во время child generation восстанавливает оба registry states/ledger и UI child projection без нового HTTP.

<a id="module-tests-migration-test-stage17-workflow-py"></a>

## `tests/migration/test_stage17_workflow.py`

Сквозные checks-only LSP и асинхронный Core checkpoint API с проверкой responsiveness и сохранности исходника.

### `Stage17HttpTests`

[Исходник](../../tests/migration/test_stage17_workflow.py#L12)

```python
class Stage17HttpTests(unittest.TestCase)
```

Настоящий TaskService checks-only flow с approved LSP и без обращения к модели.

### `Stage17HttpTests.run_lsp`

[Исходник](../../tests/migration/test_stage17_workflow.py#L17)

```python
def run_lsp(self, clean)
```

Настраивает известный LSP fixture, ждёт точный approval и terminal task, проверяет нулевой HTTP расход.

### `Stage17HttpTests.test_complete_lsp_check_and_criterion_pass_without_model_http`

[Исходник](../../tests/migration/test_stage17_workflow.py#L33)

```python
def test_complete_lsp_check_and_criterion_pass_without_model_http(self)
```

Проверка: Checks-only LSP через реальный worker и approval подтверждает criterion; изменение сервера инвалидирует evidence.

### `Stage17HttpTests.test_lsp_error_keeps_task_paused_and_does_not_satisfy_criterion`

[Исходник](../../tests/migration/test_stage17_workflow.py#L40)

```python
def test_lsp_error_keeps_task_paused_and_does_not_satisfy_criterion(self)
```

Проверка: LSP errors оставляют задачу paused и критерий failed без model HTTP.

### `Stage17BridgeTests`

[Исходник](../../tests/migration/test_stage17_workflow.py#L46)

```python
class Stage17BridgeTests(unittest.TestCase)
```

Реальный stdio Core, async Git checkpoint и сохранность агентской правки.

### `Stage17BridgeTests.test_checkpoint_api_saves_confirmed_write_and_keeps_core_responsive`

[Исходник](../../tests/migration/test_stage17_workflow.py#L56)

```python
def test_checkpoint_api_saves_confirmed_write_and_keeps_core_responsive(self)
```

Проверка: Асинхронный private Git RPC позволяет health ответ во время работы и сохраняет подтверждённую агентскую запись.

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

### `SlowHandler.do_GET`

[Исходник](../../tests/migration/test_streaming.py#L22)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `SlowHandler.chunk`

[Исходник](../../tests/migration/test_streaming.py#L28)

```python
def chunk(self, text)
```

Пишет один SSE-чанк тестового текстового ответа.

### `SlowHandler.wait_for_disconnect`

[Исходник](../../tests/migration/test_streaming.py#L34)

```python
def wait_for_disconnect(self)
```

На стороне fixture ожидает реального закрытия клиентского сокета.

### `SlowHandler.do_POST`

[Исходник](../../tests/migration/test_streaming.py#L45)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `StreamingTests`

[Исходник](../../tests/migration/test_streaming.py#L79)

```python
class StreamingTests(unittest.TestCase)
```

Тестовый класс/фикстура: Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки.

### `StreamingTests.setUp`

[Исходник](../../tests/migration/test_streaming.py#L80)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `StreamingTests.tearDown`

[Исходник](../../tests/migration/test_streaming.py#L104)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `StreamingTests.start`

[Исходник](../../tests/migration/test_streaming.py#L117)

```python
def start(self, mode, auto_memory=False)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `StreamingTests.stop_and_assert`

[Исходник](../../tests/migration/test_streaming.py#L127)

```python
def stop_and_assert(self)
```

Отменяет engine и проверяет время завершения, закрытие сокета и paused checkpoint.

### `StreamingTests.test_cancel_before_server_returns_headers`

[Исходник](../../tests/migration/test_streaming.py#L137)

```python
def test_cancel_before_server_returns_headers(self)
```

Проверка: Отмена закрывает TCP до HTTP-заголовков без ожидания network timeout.

### `StreamingTests.test_cancel_during_stalled_sse_preserves_displayed_text`

[Исходник](../../tests/migration/test_streaming.py#L142)

```python
def test_cancel_during_stalled_sse_preserves_displayed_text(self)
```

Проверка: Отмена закрывает зависший SSE и сохраняет уже показанный текст.

### `StreamingTests.test_text_arrives_before_response_finishes`

[Исходник](../../tests/migration/test_streaming.py#L149)

```python
def test_text_arrives_before_response_finishes(self)
```

Проверка: Первый чанк виден раньше завершения модельного ответа.

### `StreamingTests.test_cancel_memory_request_does_not_mark_task_completed`

[Исходник](../../tests/migration/test_streaming.py#L161)

```python
def test_cancel_memory_request_does_not_mark_task_completed(self)
```

Проверка: Отмена необязательного memory-запроса оставляет task paused.

### `StreamingTests.test_preferences_reload_does_not_restore_api_key`

[Исходник](../../tests/migration/test_streaming.py#L166)

```python
def test_preferences_reload_does_not_restore_api_key(self)
```

Проверка: Новый сервис восстанавливает URL/модель, но не ключ.

### `StreamingTests.test_service_flushes_buffer_during_pause_and_final_uses_same_message_id`

[Исходник](../../tests/migration/test_streaming.py#L174)

```python
def test_service_flushes_buffer_during_pause_and_final_uses_same_message_id(self)
```

Проверка: Таймер допечатывает буфер при паузе и связывает финал с тем же bubble ID.

### `StreamingTests.test_auto_continuation_keeps_one_ui_message_and_loaded_context`

[Исходник](../../tests/migration/test_streaming.py#L202)

```python
def test_auto_continuation_keeps_one_ui_message_and_loaded_context(self)
```

Проверка: реальные metadata/SSE/Core сохраняют один message_id и canonical ответ, используя detected 4K и игнорируя старые лимиты циклов.

<a id="module-tests-migration-test-task-graph-execution-py"></a>

## `tests/migration/test_task_graph_execution.py`

Multi-file task through context compaction, failed check, bounded diagnostic and actual Core restart without replay.

### `options`

[Исходник](../../tests/migration/test_task_graph_execution.py#L17)

```python
def options(fail=False)
```

Даёт точную пользовательскую проверку двух файлов с scoped witness; отрицательный режим задаёт exit 1.

### `GraphHandler`

[Исходник](../../tests/migration/test_task_graph_execution.py#L21)

```python
class GraphHandler(BaseHTTPRequestHandler)
```

Native HTTP model fixture, читающий canonical task state и штатные compressed archives без подмены executor/journal.

### `GraphHandler.log_message`

[Исходник](../../tests/migration/test_task_graph_execution.py#L22)

```python
def log_message(self, *args)
```

Подавляет HTTP fixture access log.

### `GraphHandler.do_GET`

[Исходник](../../tests/migration/test_task_graph_execution.py#L23)

```python
def do_GET(self)
```

Отказывает discovery: manual test window задан явно и не зависит от внешнего сервера.

### `GraphHandler.do_POST`

[Исходник](../../tests/migration/test_task_graph_execution.py#L25)

```python
def do_POST(self)
```

Генерирует graph/write/receipt/check/final sequence или повтор чтения; умеет ждать kill между зависимыми шагами.

### `GraphExecutionTests`

[Исходник](../../tests/migration/test_task_graph_execution.py#L73)

```python
class GraphExecutionTests(unittest.TestCase)
```

Тестовый класс/фикстура: Multi-file task through context compaction, failed check, bounded diagnostic and actual Core restart without replay.

### `GraphExecutionTests.run_graph`

[Исходник](../../tests/migration/test_task_graph_execution.py#L77)

```python
def run_graph(self, fail=False)
```

Выполняет multi-file sequence в реальном TaskService с явными approvals и включённым тестовым command plugin.

### `GraphExecutionTests.test_multi_file_graph_completes_with_scoped_checks_after_compaction`

[Исходник](../../tests/migration/test_task_graph_execution.py#L92)

```python
def test_multi_file_graph_completes_with_scoped_checks_after_compaction(self)
```

Проверка: Два больших файла, три approvals, сжатие контекста и точная check_id проверка закрывают граф по evidence.

### `GraphExecutionTests.test_failed_check_cannot_be_hidden_by_final_text`

[Исходник](../../tests/migration/test_task_graph_execution.py#L101)

```python
def test_failed_check_cannot_be_hidden_by_final_text(self)
```

Проверка: Финальная фраза модели не скрывает exit 1: task paused, verification failed и узел не done.

### `GraphExecutionTests.test_repeated_results_get_one_diagnostic_then_pause`

[Исходник](../../tests/migration/test_task_graph_execution.py#L106)

```python
def test_repeated_results_get_one_diagnostic_then_pause(self)
```

Проверка: Повтор получает одну read-only диагностическую попытку, затем безопасную паузу с checkpoint.

### `GraphRestartTests`

[Исходник](../../tests/migration/test_task_graph_execution.py#L115)

```python
class GraphRestartTests(unittest.TestCase)
```

Тестовый класс/фикстура: Multi-file task through context compaction, failed check, bounded diagnostic and actual Core restart without replay.

### `GraphRestartTests.advance`

[Исходник](../../tests/migration/test_task_graph_execution.py#L124)

```python
def advance(self, waiting=False)
```

Даёт approvals только известным тестовым действиям и ждёт заданной точки настоящего Core без второго consumer RPC очереди.

### `GraphRestartTests.test_real_restart_preserves_completed_node_and_never_replays_its_write`

[Исходник](../../tests/migration/test_task_graph_execution.py#L135)

```python
def test_real_restart_preserves_completed_node_and_never_replays_its_write(self)
```

Проверка: Kill/restart Core между шагами сохраняет done узел и не повторяет его файловую операцию после resume.

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

[Исходник](../../tests/migration/test_task_service.py#L68)

```python
class TaskServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.

### `TaskServiceTests.setUpClass`

[Исходник](../../tests/migration/test_task_service.py#L70)

```python
@classmethod
def setUpClass(cls)
```

Создаёт общую HTTP-фикстуру и её поток для класса тестов.

### `TaskServiceTests.tearDownClass`

[Исходник](../../tests/migration/test_task_service.py#L77)

```python
@classmethod
def tearDownClass(cls)
```

Останавливает общий сервер и ждёт его поток.

### `TaskServiceTests.setUp`

[Исходник](../../tests/migration/test_task_service.py#L82)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TaskServiceTests.tearDown`

[Исходник](../../tests/migration/test_task_service.py#L98)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TaskServiceTests.event`

[Исходник](../../tests/migration/test_task_service.py#L104)

```python
def event(self, name)
```

Читает события до нужного имени и немедленно проваливает тест при failed.

### `TaskServiceTests.test_voice_persona_uses_chat_scope_without_file_tools`

[Исходник](../../tests/migration/test_task_service.py#L112)

```python
def test_voice_persona_uses_chat_scope_without_file_tools(self)
```

Проверка: Лола включается только для voice, uses empty Chat scope без tools/auto-memory.

### `TaskServiceTests.test_source_context_approval_reject_and_changed_preview_send_no_http`

[Исходник](../../tests/migration/test_task_service.py#L123)

```python
def test_source_context_approval_reject_and_changed_preview_send_no_http(self)
```

Проверка: Реальный TaskService блокирует HTTP на approval, отказ/изменение приводит к paused, а не ложному выполнению.

### `TaskServiceTests.test_source_context_confirmed_http_preserves_write_approval`

[Исходник](../../tests/migration/test_task_service.py#L142)

```python
def test_source_context_confirmed_http_preserves_write_approval(self)
```

Проверка: После отдельного согласия реальный локальный HTTP получает пакет; последующая запись требует собственного diff approval, Stop не пишет файл.

### `TaskServiceTests.test_rename_preserves_messages_and_scope_and_active_title`

[Исходник](../../tests/migration/test_task_service.py#L158)

```python
def test_rename_preserves_messages_and_scope_and_active_title(self)
```

Проверка: Название сохраняется без изменения сообщений, обновляет active chat и не пересекает Chat/IDE scope.

### `TaskServiceTests.test_rename_rejected_during_active_task`

[Исходник](../../tests/migration/test_task_service.py#L168)

```python
def test_rename_rejected_during_active_task(self)
```

Проверка: Переименование запрещено во время реальной задачи, ожидающей approval.

### `TaskServiceTests.start`

[Исходник](../../tests/migration/test_task_service.py#L172)

```python
def start(self)
```

Готовит и запускает проверяемый engine/service в сценарии данного теста.

### `TaskServiceTests.resolve`

[Исходник](../../tests/migration/test_task_service.py#L180)

```python
def resolve(self, approval, decision)
```

Передаёт проверяемое решение по предложению в TaskService.

### `TaskServiceTests.test_draft_probe_uses_generation_without_saving_configuration`

[Исходник](../../tests/migration/test_task_service.py#L183)

```python
def test_draft_probe_uses_generation_without_saving_configuration(self)
```

Проверка: Probe получает draft sampling/ID, но не меняет сохранённые настройки и не отправляет tools/историю.

### `TaskServiceTests.test_saved_generation_is_used_by_engine`

[Исходник](../../tests/migration/test_task_service.py#L202)

```python
def test_saved_generation_is_used_by_engine(self)
```

Проверка: Настройки из preferences реально попадают в HTTP streaming payload и переживают новый TaskService.

### `TaskServiceTests.test_empty_after_tool_recovers_without_repeating_write`

[Исходник](../../tests/migration/test_task_service.py#L216)

```python
def test_empty_after_tool_recovers_without_repeating_write(self)
```

Проверка: SSE с reasoning без content после Apply приводит к одному text-only повтору, без повторной записи и без служебного user в архиве.

### `TaskServiceTests.test_permanently_empty_model_pauses_after_two_retries`

[Исходник](../../tests/migration/test_task_service.py#L232)

```python
def test_permanently_empty_model_pauses_after_two_retries(self)
```

Проверка: Три пустых ответа после успешной записи дают paused/failed, сохраняют единственный tool result и файл.

### `TaskServiceTests.test_chat_without_project_has_only_extension_tools_and_separate_history`

[Исходник](../../tests/migration/test_task_service.py#L251)

```python
def test_chat_without_project_has_only_extension_tools_and_separate_history(self)
```

Проверка: Chat получает только разрешённые нефайловые расширения, сохраняет отдельную историю и не пишет проект.

### `TaskServiceTests.test_task_end_allows_immediate_configuration_before_thread_returns`

[Исходник](../../tests/migration/test_task_service.py#L266)

```python
def test_task_end_allows_immediate_configuration_before_thread_returns(self)
```

Проверка: Синхронный callback task_end меняет настройки, пока прежний поток ещё жив: завершённое исполнение уже idle.

### `TaskServiceTests.test_task_end_allows_immediate_configuration_before_thread_returns.observe`

[Исходник](../../tests/migration/test_task_service.py#L270)

```python
def observe(event)
```

Перехватывает task_end, проверяет ещё живой worker и синхронно меняет настройки до возврата потока.

### `TaskServiceTests.test_chat_refuses_unsolicited_tool`

[Исходник](../../tests/migration/test_task_service.py#L287)

```python
def test_chat_refuses_unsolicited_tool(self)
```

Проверка: Неожиданный tool от сервера в Chat отклоняется до approval/выполнения, задача приостанавливается.

### `TaskServiceTests.test_apply_only_after_matching_approval_and_persist_history`

[Исходник](../../tests/migration/test_task_service.py#L304)

```python
def test_apply_only_after_matching_approval_and_persist_history(self)
```

Проверка: Запись происходит после совпавших run/proposal ID, а история и завершение сохраняются.

### `TaskServiceTests.test_long_archive_survives_model_compaction_and_service_restart`

[Исходник](../../tests/migration/test_task_service.py#L326)

```python
def test_long_archive_survives_model_compaction_and_service_restart(self)
```

Проверка: Длинная история сохраняется целиком после реального HTTP tool loop и повторного открытия сервиса.

### `TaskServiceTests.test_forced_tool_uses_single_definition_then_restores_auto`

[Исходник](../../tests/migration/test_task_service.py#L353)

```python
def test_forced_tool_uses_single_definition_then_restores_auto(self)
```

Проверка: Первый запрос ограничен одним required-инструментом, следующие используют auto и полный набор.

### `TaskServiceTests.test_multiple_tools_keep_same_archive_anchor_for_write_recovery`

[Исходник](../../tests/migration/test_task_service.py#L366)

```python
def test_multiple_tools_keep_same_archive_anchor_for_write_recovery(self)
```

Проверка: Несколько tools одного ответа сохраняют общий assistant anchor; восстановление учитывает точный результат записи.

### `TaskServiceTests.test_reject_does_not_write`

[Исходник](../../tests/migration/test_task_service.py#L386)

```python
def test_reject_does_not_write(self)
```

Проверка: Отказ и устаревшее подтверждение не создают файл.

### `TaskServiceTests.test_matching_approval_refuses_new_external_file`

[Исходник](../../tests/migration/test_task_service.py#L395)

```python
def test_matching_approval_refuses_new_external_file(self)
```

Проверка: Верный approval ID не разрешает запись поверх внешнего файла, появившегося после diff.

### `TaskServiceTests.test_checkpoint_survives_absent_legacy_task_file`

[Исходник](../../tests/migration/test_task_service.py#L410)

```python
def test_checkpoint_survives_absent_legacy_task_file(self)
```

Проверка: канонический checkpoint не зависит от отдельного legacy файла.

### `TaskServiceTests.test_recovery_does_not_confuse_reused_tool_ids_with_old_success`

[Исходник](../../tests/migration/test_task_service.py#L423)

```python
def test_recovery_does_not_confuse_reused_tool_ids_with_old_success(self)
```

Проверка: Старый результат с повторённым tool_call_id не скрывает неопределённую новую запись.

### `TaskServiceTests.test_recovery_recognizes_saved_tool_result_before_task_checkpoint`

[Исходник](../../tests/migration/test_task_service.py#L451)

```python
def test_recovery_recognizes_saved_tool_result_before_task_checkpoint(self)
```

Проверка: Сохранённый результат в нужном блоке позволяет восстановить учёт успешной записи.

### `TaskServiceTests.test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately`

[Исходник](../../tests/migration/test_task_service.py#L464)

```python
def test_stream_draft_is_recovered_once_and_other_run_is_preserved_separately(self)
```

Проверка: Draft текущего запуска восстанавливается один раз; чужой фрагмент сохраняется отдельно.

### `TaskServiceTests.test_unexpected_engine_exception_still_persists_pause_and_task_end`

[Исходник](../../tests/migration/test_task_service.py#L482)

```python
def test_unexpected_engine_exception_still_persists_pause_and_task_end(self)
```

Проверка: Неожиданная ошибка engine сохраняет paused и обязательно отправляет task_end.

### `TaskServiceTests.test_legacy_index_is_not_used_during_agent_execution`

[Исходник](../../tests/migration/test_task_service.py#L492)

```python
def test_legacy_index_is_not_used_during_agent_execution(self)
```

Проверка: HTTP agent approval/result/task_end работают с полностью запрещённым JSON writer истории.

### `TaskServiceTests.test_persistence_failure_before_apply_never_writes_and_still_ends_task`

[Исходник](../../tests/migration/test_task_service.py#L504)

```python
def test_persistence_failure_before_apply_never_writes_and_still_ends_task(self)
```

Проверка: При отказе сохранения перед Apply файл не меняется, задача завершается с ошибкой.

### `TaskServiceTests.test_resume_preserves_task_and_recovery_marks_interrupted_task_paused`

[Исходник](../../tests/migration/test_task_service.py#L517)

```python
def test_resume_preserves_task_and_recovery_marks_interrupted_task_paused(self)
```

Проверка: Running после сбоя восстанавливается как paused и поддерживает новую попытку.

### `TaskServiceTests.test_new_prompt_after_pause_creates_new_task`

[Исходник](../../tests/migration/test_task_service.py#L534)

```python
def test_new_prompt_after_pause_creates_new_task(self)
```

Проверка: Новый prompt не выдаётся за продолжение старой задачи.

### `TaskServiceTests.test_cancel_while_waiting_pauses_task_and_unblocks_worker`

[Исходник](../../tests/migration/test_task_service.py#L546)

```python
def test_cancel_while_waiting_pauses_task_and_unblocks_worker(self)
```

Проверка: Отмена освобождает approval wait и сохраняет paused.

### `TaskServiceTests.test_busy_task_allows_selection_but_rejects_configuration_and_same_workspace_run`

[Исходник](../../tests/migration/test_task_service.py#L555)

```python
def test_busy_task_allows_selection_but_rejects_configuration_and_same_workspace_run(self)
```

Проверка: Во время работы разрешён выбор нового чата, но изменение конфигурации и второй writer той же папки запрещены.

### `TaskServiceTests.test_chats_are_scoped_to_project_and_ids_cannot_escape_store`

[Исходник](../../tests/migration/test_task_service.py#L564)

```python
def test_chats_are_scoped_to_project_and_ids_cannot_escape_store(self)
```

Проверка: ID и принадлежность проекта проверяются до загрузки чата.

### `TaskServiceTests.test_models_and_configuration_do_not_return_key`

[Исходник](../../tests/migration/test_task_service.py#L572)

```python
def test_models_and_configuration_do_not_return_key(self)
```

Проверка: Список моделей работает, а configuration response не содержит ключ.

### `TaskServiceTests.test_missing_model_and_bad_url_are_rejected`

[Исходник](../../tests/migration/test_task_service.py#L577)

```python
def test_missing_model_and_bad_url_are_rejected(self)
```

Проверка: Запуск без модели и неверные URL отклоняются.

<a id="module-tests-migration-test-transcription-py"></a>

## `tests/migration/test_transcription.py`

Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону.

### `TranscriptionHandler`

[Исходник](../../tests/migration/test_transcription.py#L15)

```python
class TranscriptionHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону.

### `TranscriptionHandler.log_message`

[Исходник](../../tests/migration/test_transcription.py#L16)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `TranscriptionHandler.do_POST`

[Исходник](../../tests/migration/test_transcription.py#L18)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `TranscriptionTests`

[Исходник](../../tests/migration/test_transcription.py#L28)

```python
class TranscriptionTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону.

### `TranscriptionTests.setUp`

[Исходник](../../tests/migration/test_transcription.py#L29)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TranscriptionTests.tearDown`

[Исходник](../../tests/migration/test_transcription.py#L40)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TranscriptionTests.test_real_multipart_returns_editable_text`

[Исходник](../../tests/migration/test_transcription.py#L43)

```python
def test_real_multipart_returns_editable_text(self)
```

Проверка: Отправляет WAV по настоящему HTTP, проверяет multipart file/language и возврат распознанного текста.

### `TranscriptionTests.test_cancel_closes_stalled_request_promptly`

[Исходник](../../tests/migration/test_transcription.py#L51)

```python
def test_cancel_closes_stalled_request_promptly(self)
```

Проверка: Отменяет STT до HTTP headers и завершает worker менее чем за две секунды.

<a id="module-tests-migration-test-tts-server-py"></a>

## `tests/migration/test_tts_server.py`

HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов.

### `FakeTalker`

[Исходник](../../tests/migration/test_tts_server.py#L19)

```python
class FakeTalker
```

Тестовый класс/фикстура: HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов.

### `FakeTalker.register_forward_pre_hook`

[Исходник](../../tests/migration/test_tts_server.py#L20)

```python
def register_forward_pre_hook(self, hook)
```

Устанавливает тестовую проверку отмены как PyTorch talker без установки torch.

### `FakeTalker.remove`

[Исходник](../../tests/migration/test_tts_server.py#L24)

```python
def remove(self)
```

Удаляет тестовый forward hook после окончания или отмены запроса.

### `TtsServerTests`

[Исходник](../../tests/migration/test_tts_server.py#L28)

```python
class TtsServerTests(unittest.TestCase)
```

Тестовый класс/фикстура: HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов.

### `TtsServerTests.setUp`

[Исходник](../../tests/migration/test_tts_server.py#L29)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TtsServerTests.generate`

[Исходник](../../tests/migration/test_tts_server.py#L38)

```python
def generate(self, model, text, style)
```

Имитирует шаги нейронной генерации с forward hook и создаёт короткий PCM WAV без звука.

### `TtsServerTests.tearDown`

[Исходник](../../tests/migration/test_tts_server.py#L47)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `TtsServerTests.test_disconnect_releases_busy_server_and_allows_retry`

[Исходник](../../tests/migration/test_tts_server.py#L50)

```python
def test_disconnect_releases_busy_server_and_allows_retry(self)
```

Проверка: Закрывает настоящий HTTP-сокет во время генерации, проверяет освобождение 429 и успешный повтор.

### `TtsServerTests.test_deadline_returns_504_and_removes_hook`

[Исходник](../../tests/migration/test_tts_server.py#L67)

```python
def test_deadline_returns_504_and_removes_hook(self)
```

Проверка: Проверяет HTTP 504 при deadline и обязательное удаление hook/освобождение слота.

### `TtsServerTests.test_piper_backend_wav_and_disconnect_guard`

[Исходник](../../tests/migration/test_tts_server.py#L73)

```python
def test_piper_backend_wav_and_disconnect_guard(self)
```

Проверка: Проверяет HTTP callback Piper, формат/число кадров WAV, освобождение слота и распространение отмены между чанками.

<a id="module-tests-migration-test-workspace-workflow-py"></a>

## `tests/migration/test_workspace_workflow.py`

Настоящий локальный HTTP/SSE workflow создания и изменения проекта через пять отдельных согласий и scoped инструкции.

### `WorkspaceHandler`

[Исходник](../../tests/migration/test_workspace_workflow.py#L16)

```python
class WorkspaceHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Настоящий локальный HTTP/SSE workflow создания и изменения проекта через пять отдельных согласий и scoped инструкции.

### `WorkspaceHandler.log_message`

[Исходник](../../tests/migration/test_workspace_workflow.py#L17)

```python
def log_message(self, *_)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `WorkspaceHandler.do_POST`

[Исходник](../../tests/migration/test_workspace_workflow.py#L19)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `WorkspaceWorkflowTests`

[Исходник](../../tests/migration/test_workspace_workflow.py#L45)

```python
class WorkspaceWorkflowTests(unittest.TestCase)
```

Тестовый класс/фикстура: Настоящий локальный HTTP/SSE workflow создания и изменения проекта через пять отдельных согласий и scoped инструкции.

### `WorkspaceWorkflowTests.test_agent_creates_and_changes_nested_project_through_fresh_approvals`

[Исходник](../../tests/migration/test_workspace_workflow.py#L46)

```python
def test_agent_creates_and_changes_nested_project_through_fresh_approvals(self)
```

Проверка: реальный HTTP/SSE-агент учитывает scoped правила, создаёт структуру, читает/правит/перемещает/удаляет с пятью свежими согласиями

<a id="module-tests-test-agent-benchmark-py"></a>

## `tests/test_agent_benchmark.py`

Проверка владения fixtures, независимого oracle, строгого отчёта и запрета считать угаданный путь успешным поиском.

### `AgentBenchmarkTests`

[Исходник](../../tests/test_agent_benchmark.py#L12)

```python
class AgentBenchmarkTests(unittest.TestCase)
```

Тестовый класс/фикстура: Проверка владения fixtures, независимого oracle, строгого отчёта и запрета считать угаданный путь успешным поиском.

### `AgentBenchmarkTests.test_auto_budget_trial_is_explicit_and_manual_default_is_preserved`

[Исходник](../../tests/test_agent_benchmark.py#L13)

```python
def test_auto_budget_trial_is_explicit_and_manual_default_is_preserved(self)
```

Явный auto эксперимент передаёт режим в существующий Engine, сохраняя manual 8192 по умолчанию.

### `AgentBenchmarkTests.setUp`

[Исходник](../../tests/test_agent_benchmark.py#L28)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `AgentBenchmarkTests.test_fixture_is_deterministic_and_reset_touches_only_owned_sources`

[Исходник](../../tests/test_agent_benchmark.py#L32)

```python
def test_fixture_is_deterministic_and_reset_touches_only_owned_sources(self)
```

Проверка: reset восстанавливает только собственные fixture files и отказывается от каталога без правильного marker.

### `AgentBenchmarkTests.test_initial_bug_fails_and_real_minimal_fix_passes`

[Исходник](../../tests/test_agent_benchmark.py#L41)

```python
def test_initial_bug_fails_and_real_minimal_fix_passes(self)
```

Проверка: oracle отвергает исходный баг и принимает минимальную правильную правку независимо от ответа модели.

### `AgentBenchmarkTests.test_multifile_requires_definition_and_caller`

[Исходник](../../tests/test_agent_benchmark.py#L47)

```python
def test_multifile_requires_definition_and_caller(self)
```

Проверка: переименование требует согласованного definition/caller; добавленные эффекты module не считаются корректным diff.

### `AgentBenchmarkTests.test_model_code_is_not_imported_or_executed_by_oracle`

[Исходник](../../tests/test_agent_benchmark.py#L56)

```python
def test_model_code_is_not_imported_or_executed_by_oracle(self)
```

Проверка: произвольные вызовы, module statements и изменённые сигнатуры отклоняются без исполнения кода модели.

### `AgentBenchmarkTests.test_search_reports_coverage_and_real_paths`

[Исходник](../../tests/test_agent_benchmark.py#L67)

```python
def test_search_reports_coverage_and_real_paths(self)
```

Проверка: baseline измеряет настоящий поиск с source paths и отдельной полнотой обхода.

### `AgentBenchmarkTests.test_report_serialization_is_strict_and_atomic`

[Исходник](../../tests/test_agent_benchmark.py#L75)

```python
def test_report_serialization_is_strict_and_atomic(self)
```

Проверка: UTF-8 отчёт атомарен; NaN не повреждает уже записанный результат.

### `AgentBenchmarkTests.test_censored_experiment_is_distinct_from_incorrect_code`

[Исходник](../../tests/test_agent_benchmark.py#L82)

```python
def test_censored_experiment_is_distinct_from_incorrect_code(self)
```

Проверка: правильная правка на cutoff эксперимента отделяется от неверного diff и полного E2E завершения.

### `AgentBenchmarkTests.test_location_oracle_does_not_accept_numeric_or_path_prefixes`

[Исходник](../../tests/test_agent_benchmark.py#L91)

```python
def test_location_oracle_does_not_accept_numeric_or_path_prefixes(self)
```

Проверка: строка 10 и совпадение суффикса чужого пути не подменяют точный source location :1.

### `AgentBenchmarkTests.test_correct_location_without_successful_tool_evidence_is_not_success`

[Исходник](../../tests/test_agent_benchmark.py#L97)

```python
def test_correct_location_without_successful_tool_evidence_is_not_success(self)
```

Проверка: угаданный путь или неуспешное чтение не подтверждают поиск исходника.

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

<a id="module-tests-test-assistant-service-py"></a>

## `tests/test_assistant_service.py`

Проверки утилит Лолы, сохранения заметок, таймеров, музыки и папок из исходного prompt.

### `AssistantTests`

[Исходник](../../tests/test_assistant_service.py#L11)

```python
class AssistantTests(unittest.TestCase)
```

Тестовый класс/фикстура: Проверки утилит Лолы, сохранения заметок, таймеров, музыки и папок из исходного prompt.

### `AssistantTests.test_calculator_has_no_calls_names_or_unbounded_powers`

[Исходник](../../tests/test_assistant_service.py#L12)

```python
def test_calculator_has_no_calls_names_or_unbounded_powers(self)
```

Проверка: AST-калькулятор считает арифметику и отвергает вызовы, имена и слишком большую степень.

### `AssistantTests.test_notes_persist_without_arbitrary_paths`

[Исходник](../../tests/test_assistant_service.py#L17)

```python
def test_notes_persist_without_arbitrary_paths(self)
```

Проверка: Заметки переживают новый экземпляр, повреждённое хранилище не перезаписывается.

### `AssistantTests.test_timer_emits_once_and_cancelled_timer_does_not_fire`

[Исходник](../../tests/test_assistant_service.py#L27)

```python
def test_timer_emits_once_and_cancelled_timer_does_not_fire(self)
```

Проверка: Таймер уведомляет один раз, отменённый не срабатывает, shutdown очищает сервис.

### `AssistantTests.test_full_unicode_notes_capacity_stays_readable_after_restart`

[Исходник](../../tests/test_assistant_service.py#L34)

```python
def test_full_unicode_notes_capacity_stays_readable_after_restart(self)
```

Проверка: 200 заметок по 4000 кириллических символов сохраняются и читаются новым сервисом; 201-я не меняет файл.

### `AssistantTests.test_note_limit_counts_whitespace_without_corrupting_store`

[Исходник](../../tests/test_assistant_service.py#L48)

```python
def test_note_limit_counts_whitespace_without_corrupting_store(self)
```

Проверка: Пробелы учитываются в лимите 4000 символов; отказ сохраняет прежнее хранилище.

### `AssistantTests.test_music_links_reject_executables_private_hosts_and_spoofing`

[Исходник](../../tests/test_assistant_service.py#L57)

```python
def test_music_links_reject_executables_private_hosts_and_spoofing(self)
```

Проверка: Музыкальный URL не допускает протоколы файлов, private hosts и поддельные домены.

### `AssistantTests.test_music_search_encodes_query_and_does_not_claim_playback`

[Исходник](../../tests/test_assistant_service.py#L62)

```python
def test_music_search_encodes_query_and_does_not_claim_playback(self)
```

Проверка: Музыкальный поиск кодирует запрос и не подтверждает звучание после открытия страницы.

### `AssistantTests.test_local_audio_requires_original_prompt_folder_and_extension`

[Исходник](../../tests/test_assistant_service.py#L69)

```python
def test_local_audio_requires_original_prompt_folder_and_extension(self)
```

Проверка: Локальный плеер принимает только аудио из явно указанной исходной папки.

<a id="module-tests-test-auto-budget-py"></a>

## `tests/test_auto_budget.py`

Автонастройка без настоящей LLM: metadata/400/SSE, русский текст, каталог, большие выполненные записи и защита pending code.

### `BudgetHandler`

[Исходник](../../tests/test_auto_budget.py#L20)

```python
class BudgetHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Автонастройка без настоящей LLM: metadata/400/SSE, русский текст, каталог, большие выполненные записи и защита pending code.

### `BudgetHandler.log_message`

[Исходник](../../tests/test_auto_budget.py#L22)

```python
def log_message(self, *_args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `BudgetHandler.do_GET`

[Исходник](../../tests/test_auto_budget.py#L24)

```python
def do_GET(self)
```

Отдаёт детерминированный список моделей тестового HTTP-сервера.

### `BudgetHandler.do_POST`

[Исходник](../../tests/test_auto_budget.py#L32)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `AutoBudgetTests`

[Исходник](../../tests/test_auto_budget.py#L42)

```python
class AutoBudgetTests(unittest.TestCase)
```

Тестовый класс/фикстура: Автонастройка без настоящей LLM: metadata/400/SSE, русский текст, каталог, большие выполненные записи и защита pending code.

### `AutoBudgetTests.server`

[Исходник](../../tests/test_auto_budget.py#L44)

```python
def server(self)
```

Запускает отдельный HTTP metadata/context-rejection/SSE fixture и регистрирует очистку.

### `AutoBudgetTests.test_loaded_context_is_not_training_maximum_or_another_instance`

[Исходник](../../tests/test_auto_budget.py#L51)

```python
def test_loaded_context_is_not_training_maximum_or_another_instance(self)
```

Проверка: выбранный loaded instance задаёт окно вместо trained maximum/чужого слота.

### `AutoBudgetTests.test_discovery_is_cached_metadata_only`

[Исходник](../../tests/test_auto_budget.py#L59)

```python
def test_discovery_is_cached_metadata_only(self)
```

Проверка: определение окна использует только GET и cache, без генерации/управления моделями.

### `AutoBudgetTests.test_russian_prompt_fits_without_byte_equals_token_false_block`

[Исходник](../../tests/test_auto_budget.py#L66)

```python
def test_russian_prompt_fits_without_byte_equals_token_false_block(self)
```

Проверка: русский prompt сохраняется целиком и помещается по токенам, даже когда байтов больше окна.

### `AutoBudgetTests.test_auto_normalizes_irrelevant_manual_settings`

[Исходник](../../tests/test_auto_budget.py#L75)

```python
def test_auto_normalizes_irrelevant_manual_settings(self)
```

Проверка: устаревшие невалидные числовые поля не ломают auto; manual остаётся строгим.

### `AutoBudgetTests.test_auto_provisional_window_does_not_inherit_old_manual_cap`

[Исходник](../../tests/test_auto_budget.py#L81)

```python
def test_auto_provisional_window_does_not_inherit_old_manual_cap(self)
```

Проверка: неизвестный сервер получает временный auto profile, не устаревший ручной cap 4K; исходные prefs не меняются.

### `AutoBudgetTests.test_schema_catalog_preserves_selected_tool_and_human_request`

[Исходник](../../tests/test_auto_budget.py#L90)

```python
def test_schema_catalog_preserves_selected_tool_and_human_request(self)
```

Проверка: редкие schemas откладываются, обязательный tool и текущий запрос сохраняются.

### `AutoBudgetTests.test_schema_catalog_preserves_selected_tool_and_human_request.tool`

[Исходник](../../tests/test_auto_budget.py#L92)

```python
def tool(name)
```

Создаёт намеренно большую synthetic schema для проверки отложенной загрузки.

### `AutoBudgetTests.test_mandatory_prompt_never_disappears_to_claim_fit`

[Исходник](../../tests/test_auto_budget.py#L103)

```python
def test_mandatory_prompt_never_disappears_to_claim_fit(self)
```

Проверка: физически невозможный запрос не обрезается ради ложного fits.

### `AutoBudgetTests.test_rejected_pre_stream_request_is_adapted_once_without_replaying_effects`

[Исходник](../../tests/test_auto_budget.py#L110)

```python
def test_rejected_pre_stream_request_is_adapted_once_without_replaying_effects(self)
```

Проверка: реальный HTTP 400 уточняет окно и уменьшает запрос до первого SSE.

### `AutoBudgetTests.test_error_parser_does_not_treat_unrelated_numbers_as_context`

[Исходник](../../tests/test_auto_budget.py#L119)

```python
def test_error_parser_does_not_treat_unrelated_numbers_as_context(self)
```

Проверка: обратная связь допускается только для подписанного bounded размера окна.

### `AutoBudgetTests.test_sdk_uses_only_loaded_handles_and_token_count_is_cached`

[Исходник](../../tests/test_auto_budget.py#L125)

```python
def test_sdk_uses_only_loaded_handles_and_token_count_is_cached(self)
```

Проверка: SDK никогда не загружает модель; один токенизированный payload повторно берётся из cache.

### `AutoBudgetTests.test_completed_large_write_is_projected_but_pending_code_is_never_trimmed`

[Исходник](../../tests/test_auto_budget.py#L137)

```python
def test_completed_large_write_is_projected_but_pending_code_is_never_trimmed(self)
```

Проверка: выполненная запись 40+ КБ помещается квитанцией в 4K; pending код остаётся нетронутым.

### `AutoBudgetTests.test_small_slot_keeps_instructions_and_uses_minimal_tool_catalog`

[Исходник](../../tests/test_auto_budget.py#L153)

```python
def test_small_slot_keeps_instructions_and_uses_minimal_tool_catalog(self)
```

Проверка: малое окно IDE откладывает даже core schemas, сохраняя полные инструкции и место для ответа.

<a id="module-tests-test-call-journal-py"></a>

## `tests/test_call_journal.py`

Регрессии долговечного журнала: pairing, receipts, повреждения, конфликты, идентичность пачек и ручные решения.

### `call`

[Исходник](../../tests/test_call_journal.py#L14)

```python
def call(call_id='call-1', name='write_file', arguments='{"path":"a.txt","content":"hello"}')
```

Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.

### `assistant`

[Исходник](../../tests/test_call_journal.py#L18)

```python
def assistant(calls, content=None)
```

Создаёт независимую каноническую assistant-пачку фикстуры.

### `receipt`

[Исходник](../../tests/test_call_journal.py#L22)

```python
def receipt(call_id, result)
```

Создаёт каноническое tool-сообщение с JSON-квитанцией.

### `CallJournalTests`

[Исходник](../../tests/test_call_journal.py#L26)

```python
class CallJournalTests(unittest.TestCase)
```

Тестовый класс/фикстура: Регрессии долговечного журнала: pairing, receipts, повреждения, конфликты, идентичность пачек и ручные решения.

### `CallJournalTests.setUp`

[Исходник](../../tests/test_call_journal.py#L27)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `CallJournalTests.result`

[Исходник](../../tests/test_call_journal.py#L33)

```python
def result(self, messages, index=1)
```

Читает JSON-квитанцию из указанного сообщения восстановленной истории.

### `CallJournalTests.test_default_directory_uses_current_task_dir_and_chat_epoch_are_isolated`

[Исходник](../../tests/test_call_journal.py#L36)

```python
def test_default_directory_uses_current_task_dir_and_chat_epoch_are_isolated(self)
```

Проверка: журналы разных чатов и эпох используют независимые файлы

### `CallJournalTests.test_prepare_and_started_are_fsynced_before_return`

[Исходник](../../tests/test_call_journal.py#L44)

```python
def test_prepare_and_started_are_fsynced_before_return(self)
```

Проверка: prepared и started выполняют fsync до перехода к эффекту

### `CallJournalTests.test_prepared_batch_and_awaiting_approval_are_never_executed`

[Исходник](../../tests/test_call_journal.py#L54)

```python
def test_prepared_batch_and_awaiting_approval_are_never_executed(self)
```

Проверка: не начатые вызовы восстанавливаются как NOT_EXECUTED

### `CallJournalTests.test_started_read_only_and_effectful_calls_are_classified_conservatively`

[Исходник](../../tests/test_call_journal.py#L66)

```python
def test_started_read_only_and_effectful_calls_are_classified_conservatively(self)
```

Проверка: потеря чтения отличается от неизвестного эффекта

### `CallJournalTests.test_saved_receipt_restores_missing_chat_tail`

[Исходник](../../tests/test_call_journal.py#L78)

```python
def test_saved_receipt_restores_missing_chat_tail(self)
```

Проверка: durable receipt восстанавливает потерянный хвост чата

### `CallJournalTests.test_partial_batch_preserves_receipt_and_pairs_every_call`

[Исходник](../../tests/test_call_journal.py#L92)

```python
def test_partial_batch_preserves_receipt_and_pairs_every_call(self)
```

Проверка: успех соседнего call не теряется при незавершённой пачке

### `CallJournalTests.test_real_canonical_receipt_replaces_placeholder_and_clears_gate`

[Исходник](../../tests/test_call_journal.py#L107)

```python
def test_real_canonical_receipt_replaces_placeholder_and_clears_gate(self)
```

Проверка: сохранённый настоящий ответ снимает синтетический unknown

### `CallJournalTests.test_stored_real_receipt_replaces_canonical_unknown`

[Исходник](../../tests/test_call_journal.py#L119)

```python
def test_stored_real_receipt_replaces_canonical_unknown(self)
```

Проверка: настоящая квитанция из журнала заменяет неизвестный результат в чате

### `CallJournalTests.test_resolutions_are_durable_explicit_and_replace_only_unknowns`

[Исходник](../../tests/test_call_journal.py#L127)

```python
def test_resolutions_are_durable_explicit_and_replace_only_unknowns(self)
```

Проверка: наблюдения человека переживают перезапуск и не заменяют известный ответ

### `CallJournalTests.test_never_started_and_real_receipts_cannot_be_resolved`

[Исходник](../../tests/test_call_journal.py#L151)

```python
def test_never_started_and_real_receipts_cannot_be_resolved(self)
```

Проверка: ручная проверка доступна только неопределённым эффектам

### `CallJournalTests.test_field_only_unknown_result_is_unresolved_and_can_be_resolved`

[Исходник](../../tests/test_call_journal.py#L163)

```python
def test_field_only_unknown_result_is_unresolved_and_can_be_resolved(self)
```

Проверка: явный outcome_unknown распознаётся без специального code

### `CallJournalTests.test_started_effect_can_be_resolved_when_no_receipt_was_written`

[Исходник](../../tests/test_call_journal.py#L171)

```python
def test_started_effect_can_be_resolved_when_no_receipt_was_written(self)
```

Проверка: начатый эффект без ответа можно явно проверить

### `CallJournalTests.test_torn_final_row_is_ignored_and_repaired_before_append`

[Исходник](../../tests/test_call_journal.py#L179)

```python
def test_torn_final_row_is_ignored_and_repaired_before_append(self)
```

Проверка: оборванный JSONL-хвост не разрушает предыдущие receipts

### `CallJournalTests.test_valid_unterminated_final_event_is_kept_when_appending`

[Исходник](../../tests/test_call_journal.py#L192)

```python
def test_valid_unterminated_final_event_is_kept_when_appending(self)
```

Проверка: полное последнее событие без перевода строки сохраняется

### `CallJournalTests.test_complete_corrupt_row_is_not_silently_skipped`

[Исходник](../../tests/test_call_journal.py#L199)

```python
def test_complete_corrupt_row_is_not_silently_skipped(self)
```

Проверка: повреждённая полная строка останавливает восстановление

### `CallJournalTests.test_identity_mismatches_leave_history_and_file_untouched`

[Исходник](../../tests/test_call_journal.py#L213)

```python
def test_identity_mismatches_leave_history_and_file_untouched(self)
```

Проверка: чужой call anchor не меняет исходные данные

### `CallJournalTests.test_all_anchors_validate_before_adopting_any_canonical_receipt`

[Исходник](../../tests/test_call_journal.py#L233)

```python
def test_all_anchors_validate_before_adopting_any_canonical_receipt(self)
```

Проверка: конфликт поздней пачки не приводит к частичному принятию ранних receipts

### `CallJournalTests.test_multiple_missing_tail_batches_restore_at_their_exact_anchors`

[Исходник](../../tests/test_call_journal.py#L246)

```python
def test_multiple_missing_tail_batches_restore_at_their_exact_anchors(self)
```

Проверка: несколько последовательных пачек восстанавливаются в своих позициях

### `CallJournalTests.test_anchor_beyond_history_is_not_blindly_appended`

[Исходник](../../tests/test_call_journal.py#L257)

```python
def test_anchor_beyond_history_is_not_blindly_appended(self)
```

Проверка: далёкий индекс не дописывается в чужую историю

### `CallJournalTests.test_conflicting_real_receipts_fail_without_overwriting_either_copy`

[Исходник](../../tests/test_call_journal.py#L264)

```python
def test_conflicting_real_receipts_fail_without_overwriting_either_copy(self)
```

Проверка: конфликт двух настоящих квитанций сохраняет обе исходные копии

### `CallJournalTests.test_batch_and_call_collisions_are_rejected_before_append`

[Исходник](../../tests/test_call_journal.py#L274)

```python
def test_batch_and_call_collisions_are_rejected_before_append(self)
```

Проверка: пересечение якорей и дубликаты внутри пачки отклоняются до записи

### `CallJournalTests.test_row_limit_and_invalid_json_values_preserve_the_existing_file`

[Исходник](../../tests/test_call_journal.py#L285)

```python
def test_row_limit_and_invalid_json_values_preserve_the_existing_file(self)
```

Проверка: слишком большой и не конечный JSON не повреждают журнал

### `CallJournalTests.test_phases_cannot_move_backwards_or_reclassify_started_effects`

[Исходник](../../tests/test_call_journal.py#L293)

```python
def test_phases_cannot_move_backwards_or_reclassify_started_effects(self)
```

Проверка: фазы монотонны и класс уже начатого вызова неизменен

### `CallJournalTests.test_recovery_restores_missing_assistant_content`

[Исходник](../../tests/test_call_journal.py#L300)

```python
def test_recovery_restores_missing_assistant_content(self)
```

Проверка: сохранённый текст assistant восстанавливается вместе с вызовами

### `CallJournalTests.test_separate_instances_share_the_same_transaction_lock`

[Исходник](../../tests/test_call_journal.py#L306)

```python
def test_separate_instances_share_the_same_transaction_lock(self)
```

Проверка: два экземпляра одного журнала разделяют блокировку

<a id="module-tests-test-chat-store-py"></a>

## `tests/test_chat_store.py`

Контракты SQLite chat API: миграционные warnings, запрет перечитывания JSON, rollback индекса и сохранность при повреждении БД.

### `ChatRecoveryTests`

[Исходник](../../tests/test_chat_store.py#L11)

```python
class ChatRecoveryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты SQLite chat API: миграционные warnings, запрет перечитывания JSON, rollback индекса и сохранность при повреждении БД.

### `ChatRecoveryTests.setUp`

[Исходник](../../tests/test_chat_store.py#L12)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ChatRecoveryTests.test_catalog_ignores_legacy_cache_after_migration`

[Исходник](../../tests/test_chat_store.py#L21)

```python
def test_catalog_ignores_legacy_cache_after_migration(self)
```

Проверка: legacy index больше не нужен, не читается и не переписывается списком SQLite.

### `ChatRecoveryTests.test_index_failure_rolls_back_transcript_and_metadata`

[Исходник](../../tests/test_chat_store.py#L30)

```python
def test_index_failure_rolls_back_transcript_and_metadata(self)
```

Проверка: потеря search index write не оставляет частично сохранённый чат.

### `ChatRecoveryTests.test_corrupted_legacy_chat_is_reported_without_modifying_source`

[Исходник](../../tests/test_chat_store.py#L40)

```python
def test_corrupted_legacy_chat_is_reported_without_modifying_source(self)
```

Проверка: повреждённый JSON остаётся с warning и не создаёт ложный пустой чат.

### `ChatRecoveryTests.test_store_rejects_path_like_chat_ids`

[Исходник](../../tests/test_chat_store.py#L52)

```python
def test_store_rejects_path_like_chat_ids(self)
```

Проверка: Файловые пути вместо UUID не читаются, не удаляются и не сохраняются.

### `ChatRecoveryTests.test_unreadable_legacy_directory_is_not_an_empty_catalog`

[Исходник](../../tests/test_chat_store.py#L58)

```python
def test_unreadable_legacy_directory_is_not_an_empty_catalog(self)
```

Проверка: отказ доступа к источнику останавливает миграцию, повтор после исправления возможен.

### `ChatRecoveryTests.test_corrupt_database_never_falls_back_to_old_json`

[Исходник](../../tests/test_chat_store.py#L65)

```python
def test_corrupt_database_never_falls_back_to_old_json(self)
```

Проверка: повреждённая каноническая БД не подменяется старой историей и connection не остаётся открытым.

### `ChatStoreTest`

[Исходник](../../tests/test_chat_store.py#L74)

```python
class ChatStoreTest(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты SQLite chat API: миграционные warnings, запрет перечитывания JSON, rollback индекса и сохранность при повреждении БД.

### `ChatStoreTest.test_create_save_load_rename_delete`

[Исходник](../../tests/test_chat_store.py#L75)

```python
def test_create_save_load_rename_delete(self)
```

Проверка: Полный жизненный цикл записи чата и индекса.

<a id="module-tests-test-companion-policy-py"></a>

## `tests/test_companion_policy.py`

Границы coding intent Лолы, очистка Markdown, математики и внутренних тегов.

### `CompanionPolicyTests`

[Исходник](../../tests/test_companion_policy.py#L5)

```python
class CompanionPolicyTests(unittest.TestCase)
```

Проверки coding-only намерения и чистого текста Лолы.

### `CompanionPolicyTests.test_only_coding_requests_can_delegate`

[Исходник](../../tests/test_companion_policy.py#L6)

```python
def test_only_coding_requests_can_delegate(self)
```

Проверка: Кодирование допускается к делегированию, обычные вопросы, музыка, бытовые коды и функции устройств исключаются.

### `CompanionPolicyTests.test_speech_removes_markdown_preserving_words_and_math`

[Исходник](../../tests/test_companion_policy.py#L12)

```python
def test_speech_removes_markdown_preserving_words_and_math(self)
```

Проверка: Разметка/код не озвучиваются, читаемые слова и числовое умножение сохраняются.

### `CompanionPolicyTests.test_internal_reasoning_is_not_spoken`

[Исходник](../../tests/test_companion_policy.py#L19)

```python
def test_internal_reasoning_is_not_spoken(self)
```

Проверка: Закрытые think-теги удаляются из голоса и видимого итогового текста.

### `LolaIdeIsolationTests`

[Исходник](../../tests/test_companion_policy.py#L23)

```python
class LolaIdeIsolationTests(unittest.TestCase)
```

Тестовый класс/фикстура: Границы coding intent Лолы, очистка Markdown, математики и внутренних тегов.

### `LolaIdeIsolationTests.test_lola_delegate_schema_and_runtime_exclude_ide`

[Исходник](../../tests/test_companion_policy.py#L24)

```python
def test_lola_delegate_schema_and_runtime_exclude_ide(self)
```

Лола не получает полномочия IDE через схему или runtime delegation.

### `LolaIdeIsolationTests.test_old_pending_lola_ide_handoff_cannot_start_ide`

[Исходник](../../tests/test_companion_policy.py#L34)

```python
def test_old_pending_lola_ide_handoff_cannot_start_ide(self)
```

Старый handoff Лолы не обходит текущую изоляцию IDE.

<a id="module-tests-test-context-builder-py"></a>

## `tests/test_context_builder.py`

Изолированные проверки ContextPack: индекс, source anchors, budget pruning, revoke, отмена, retry и согласие без внешней сети.

### `ContextBuilderTests`

[Исходник](../../tests/test_context_builder.py#L20)

```python
class ContextBuilderTests(unittest.TestCase)
```

Изолирует проект, derived index и profile для тестов, не использует реальные исходники и внешние API.

### `ContextBuilderTests.setUp`

[Исходник](../../tests/test_context_builder.py#L22)

```python
def setUp(self)
```

Создаёт две синтетические Python sources и отдельный профиль, закрывает watcher перед cleanup.

### `ContextBuilderTests.params`

[Исходник](../../tests/test_context_builder.py#L31)

```python
def params(self)
```

Формирует обязательный запрос и optional ContextPack для проверки реального финального budget/HTTP guard.

### `ContextBuilderTests.test_ephemeral_pack_and_anchors_keep_canonical_history_untouched`

[Исходник](../../tests/test_context_builder.py#L36)

```python
def test_ephemeral_pack_and_anchors_keep_canonical_history_untouched(self)
```

Проверка: Model projection содержит saved-file hashes/ranges, canonical history и system sources не смешиваются, host metadata не уходит в SDK.

### `ContextBuilderTests.test_automatic_rollout_keeps_measured_json_regression_disabled`

[Исходник](../../tests/test_context_builder.py#L47)

```python
def test_automatic_rollout_keeps_measured_json_regression_disabled(self)
```

Проверка: Автоматический ContextPack включён для native IDE, JSON с измеренной регрессией остаётся выключен; remote требует host approval callback.

### `ContextBuilderTests.test_index_selects_symbol_and_related_test_without_duplicate_ranges`

[Исходник](../../tests/test_context_builder.py#L57)

```python
def test_index_selects_symbol_and_related_test_without_duplicate_ranges(self)
```

Проверка: Активный индекс находит символ и вероятный тест по имени, перекрывающиеся диапазоны не дублируются.

### `ContextBuilderTests.test_policy_and_content_rechecked_after_selection`

[Исходник](../../tests/test_context_builder.py#L65)

```python
def test_policy_and_content_rechecked_after_selection(self)
```

Проверка: Внешнее изменение файла или .neutralignore после retrieval исключает прежний фрагмент.

### `ContextBuilderTests.test_existing_visible_read_is_not_duplicated_but_changed_content_is_selected`

[Исходник](../../tests/test_context_builder.py#L73)

```python
def test_existing_visible_read_is_not_duplicated_but_changed_content_is_selected(self)
```

Проверка: Уже видимый read receipt не дублируется; изменившиеся сохранённые bytes выбираются заново.

### `ContextBuilderTests.test_unchanged_fragment_does_not_reuse_an_obsolete_whole_file_hash`

[Исходник](../../tests/test_context_builder.py#L80)

```python
def test_unchanged_fragment_does_not_reuse_an_obsolete_whole_file_hash(self)
```

Проверка: Правка за пределами выбранных строк меняет полный hash: прежний read_range receipt не отменяет новый anchor даже при совпавшем фрагменте.

### `ContextBuilderTests.test_denied_missing_foreign_and_cancelled_sources`

[Исходник](../../tests/test_context_builder.py#L88)

```python
def test_denied_missing_foreign_and_cancelled_sources(self)
```

Проверка: Ignore, отсутствующие/внешние пути, чужой workspace и Stop не дают source данных.

### `ContextBuilderTests.test_grant_revocation_hides_sources_and_invalidates_pack`

[Исходник](../../tests/test_context_builder.py#L98)

```python
def test_grant_revocation_hides_sources_and_invalidates_pack(self)
```

Проверка: Отзыв точного grant инвалидирует пакет и скрывает исторический путь из UI.

### `ContextBuilderTests.test_budget_drops_whole_fragments_before_current_prompt`

[Исходник](../../tests/test_context_builder.py#L109)

```python
def test_budget_drops_whole_fragments_before_current_prompt(self)
```

Проверка: RequestBudget удаляет целые optional fragments, сохраняет JSON и обязательный user request.

### `ContextBuilderTests.test_optional_sources_do_not_displace_available_tool_schemas`

[Исходник](../../tests/test_context_builder.py#L122)

```python
def test_optional_sources_do_not_displace_available_tool_schemas(self)
```

Проверка: Auto budget сначала снимает optional source fragments, сохраняя схемы инструментов, которые помещались до retrieval.

### `ContextBuilderTests.client`

[Исходник](../../tests/test_context_builder.py#L131)

```python
def client(self, remote=True)
```

Создаёт SDK client с запрещёнными redirect/proxy; внешний hostname никогда не запрашивается в этих тестах.

### `ContextBuilderTests.send`

[Исходник](../../tests/test_context_builder.py#L137)

```python
def send(self, client, callback=None, fail_first=False)
```

Передаёт запрос через настоящий ModelClient.request в in-memory endpoint, включая retry 500.

### `ContextBuilderTests.send.create`

[Исходник](../../tests/test_context_builder.py#L140)

```python
async def create(**request)
```

Учитывает точные транспортные payload и при необходимости один раз имитирует ответ 500.

### `ContextBuilderTests.test_remote_requires_concrete_approval_and_has_no_redirects_or_proxy`

[Исходник](../../tests/test_context_builder.py#L149)

```python
def test_remote_requires_concrete_approval_and_has_no_redirects_or_proxy(self)
```

Проверка: Для каждой HTTP попытки внешнему endpoint нужен точный preview; redirect и environment proxy отключены.

### `ContextBuilderTests.test_remote_requires_concrete_approval_and_has_no_redirects_or_proxy.approve`

[Исходник](../../tests/test_context_builder.py#L151)

```python
def approve(text)
```

Проверяет адрес, модель и текст фактического предложения до разрешения каждого отдельного HTTP attempt.

### `ContextBuilderTests.test_rejection_and_edit_during_preview_never_reach_endpoint`

[Исходник](../../tests/test_context_builder.py#L161)

```python
def test_rejection_and_edit_during_preview_never_reach_endpoint(self)
```

Проверка: Отказ и изменение source во время ожидания не доходят даже до fake endpoint.

### `ContextBuilderTests.test_rejection_and_edit_during_preview_never_reach_endpoint.approve`

[Исходник](../../tests/test_context_builder.py#L165)

```python
def approve(_text)
```

Отказывает либо меняет source во время ожидания, чтобы проверить отсутствие HTTP при недействительном согласии.

### `ContextBuilderTests.test_destination_change_during_approval_requires_new_preview`

[Исходник](../../tests/test_context_builder.py#L170)

```python
def test_destination_change_during_approval_requires_new_preview(self)
```

Проверка: Смена endpoint во время ожидания отменяет согласие и не вызывает HTTP.

### `ContextBuilderTests.test_destination_change_during_approval_requires_new_preview.approve`

[Исходник](../../tests/test_context_builder.py#L172)

```python
def approve(_text)
```

Меняет configured recipient прямо в callback подтверждения для отрицательной проверки повторной привязки.

### `ContextBuilderTests.test_no_callback_strips_remote_pack_but_loopback_validates_it`

[Исходник](../../tests/test_context_builder.py#L177)

```python
def test_no_callback_strips_remote_pack_but_loopback_validates_it(self)
```

Проверка: Без доверенного approval callback автоматические источники внешнему серверу не отправляются.

### `ContextBuilderTests.test_local_retry_omits_changed_sources`

[Исходник](../../tests/test_context_builder.py#L185)

```python
def test_local_retry_omits_changed_sources(self)
```

Проверка: Повтор после 500 заново проверяет source и исключает старое содержимое.

### `ContextBuilderTests.test_local_retry_omits_changed_sources.create`

[Исходник](../../tests/test_context_builder.py#L187)

```python
async def create(**request)
```

После первой попытки меняет файл; повторный HTTP не должен получить старый source fragment.

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

### `ConversationHistoryTests.test_model_context_preserves_partial_batch_and_omits_orphans`

[Исходник](../../tests/test_conversation_history.py#L18)

```python
def test_model_context_preserves_partial_batch_and_omits_orphans(self)
```

Проверка: частичный успех остаётся в контексте, отсутствующий ответ помечен unknown, orphan исключён

### `ConversationHistoryTests.test_serialized_context_budget_keeps_current_request_and_tool_pairs`

[Исходник](../../tests/test_conversation_history.py#L38)

```python
def test_serialized_context_budget_keeps_current_request_and_tool_pairs(self)
```

Проверка: JSON-бюджет соблюдается с Unicode/экранированием при сохранении запроса и tool-пар.

### `ConversationHistoryTests.test_oversized_mandatory_instructions_fail_without_truncation`

[Исходник](../../tests/test_conversation_history.py#L49)

```python
def test_oversized_mandatory_instructions_fail_without_truncation(self)
```

Проверка: Обязательные инструкции не обрезаются молча при превышении бюджета.

### `ConversationHistoryTests.test_current_run_request_survives_internal_continuation`

[Исходник](../../tests/test_conversation_history.py#L55)

```python
def test_current_run_request_survives_internal_continuation(self)
```

Проверка: Исходный запрос текущего запуска сохраняется рядом с внутренним продолжением.

### `ConversationHistoryTests.test_followup_keeps_previous_user_and_assistant_messages`

[Исходник](../../tests/test_conversation_history.py#L63)

```python
def test_followup_keeps_previous_user_and_assistant_messages(self)
```

Проверка: Повторный запрос сохраняет недавний контекст диалога.

### `ConversationHistoryTests.test_tool_call_and_tool_result_are_preserved`

[Исходник](../../tests/test_conversation_history.py#L74)

```python
def test_tool_call_and_tool_result_are_preserved(self)
```

Проверка: Связанные вызов и ответ инструмента сохраняются вместе.

### `ConversationHistoryTests.test_empty_history_starts_cleanly`

[Исходник](../../tests/test_conversation_history.py#L85)

```python
def test_empty_history_starts_cleanly(self)
```

Проверка: Пустая история создаёт корректный первый запрос.

### `ConversationHistoryTests.test_old_turns_are_trimmed_but_recent_confirmation_context_remains`

[Исходник](../../tests/test_conversation_history.py#L89)

```python
def test_old_turns_are_trimmed_but_recent_confirmation_context_remains(self)
```

Проверка: Старые ходы сокращаются без потери недавнего контекста согласия.

### `ConversationHistoryTests.test_live_compaction_preserves_system_original_request_and_recent_tool_pair`

[Исходник](../../tests/test_conversation_history.py#L106)

```python
def test_live_compaction_preserves_system_original_request_and_recent_tool_pair(self)
```

Проверка: compact_live_messages сохраняет system, исходный запрос и недавнюю tool-пару.

### `ConversationHistoryTests.test_tool_results_are_bounded_without_dropping_tool_call_pair`

[Исходник](../../tests/test_conversation_history.py#L122)

```python
def test_tool_results_are_bounded_without_dropping_tool_call_pair(self)
```

Проверка: Большой tool output ограничивается без удаления связанной структуры.

<a id="module-tests-test-core-reliability-py"></a>

## `tests/test_core_reliability.py`

Регрессии первого этапа аудита: завершение, отказ, аргументы, свидетельства команд, runtime и привязка ключей к endpoint; модель заменена локальной фикстурой.

### `delta`

[Исходник](../../tests/test_core_reliability.py#L18)

```python
def delta(text=None, calls=(), finish='stop', refusal=None)
```

Создаёт событие фиктивного модельного потока с текстом, calls, refusal и finish_reason.

### `call`

[Исходник](../../tests/test_core_reliability.py#L22)

```python
def call(name, arguments, identity='test_call')
```

Создаёт фиктивный вызов инструмента с JSON-аргументами и стабильным call ID.

### `Stream`

[Исходник](../../tests/test_core_reliability.py#L26)

```python
class Stream
```

Итерируемый поток заранее заданных ответов без HTTP и ресурсов.

### `Stream.__init__`

[Исходник](../../tests/test_core_reliability.py#L27)

```python
def __init__(self, chunks)
```

Инициализирует состояние экземпляра Stream; параметры показаны в сигнатуре, назначение описано у класса.

### `Stream.__iter__`

[Исходник](../../tests/test_core_reliability.py#L28)

```python
def __iter__(self)
```

Возвращает события фикстуры в исходном порядке.

### `Stream.close`

[Исходник](../../tests/test_core_reliability.py#L29)

```python
def close(self)
```

Совместимое закрытие фиктивного потока без внешних ресурсов.

### `CoreReliabilityTests`

[Исходник](../../tests/test_core_reliability.py#L32)

```python
class CoreReliabilityTests(unittest.TestCase)
```

Проверяет настоящий AgentEngine и настройки на временном TaskStore и синтетическом ModelClient.

### `CoreReliabilityTests.setUp`

[Исходник](../../tests/test_core_reliability.py#L33)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `CoreReliabilityTests.run_engine`

[Исходник](../../tests/test_core_reliability.py#L38)

```python
def run_engine(self, replies, handler=None, **options)
```

Запускает движок с заранее заданными ответами, собирает историю/события и проверяет отсутствие аварийного failed.

### `CoreReliabilityTests.run_engine.Client`

[Исходник](../../tests/test_core_reliability.py#L39)

```python
class Client
```

Фиктивный клиент с ограниченной последовательностью потоков и положительным ответом необязательной LLM-проверки.

### `CoreReliabilityTests.run_engine.Client.__init__`

[Исходник](../../tests/test_core_reliability.py#L40)

```python
def __init__(self, *_, **__)
```

Инициализирует состояние экземпляра CoreReliabilityTests.run_engine.Client; параметры показаны в сигнатуре, назначение описано у класса.

### `CoreReliabilityTests.run_engine.Client.create`

[Исходник](../../tests/test_core_reliability.py#L41)

```python
def create(self, **request)
```

Возвращает следующий поток либо фиксированную проверку завершения без HTTP.

### `CoreReliabilityTests.run_engine.Client.close`

[Исходник](../../tests/test_core_reliability.py#L44)

```python
def close(self)
```

Завершает фиктивный клиент без сетевых действий.

### `CoreReliabilityTests.run_engine.Client.cancel`

[Исходник](../../tests/test_core_reliability.py#L45)

```python
def cancel(self)
```

Совместимый метод отмены клиента; сам движок проверяет Event прерывания.

### `CoreReliabilityTests.test_truncated_answer_is_saved_and_paused`

[Исходник](../../tests/test_core_reliability.py#L57)

```python
def test_truncated_answer_is_saved_and_paused(self)
```

Проверка: оборванный лимитом текст сохраняется, задача приостанавливается и получает причину length

### `CoreReliabilityTests.test_truncated_native_tool_is_never_executed`

[Исходник](../../tests/test_core_reliability.py#L63)

```python
def test_truncated_native_tool_is_never_executed(self)
```

Проверка: инструмент не исполняется даже при завершённом JSON, если сервер сообщил length

### `CoreReliabilityTests.test_eof_without_terminal_reason_preserves_partial_and_pauses`

[Исходник](../../tests/test_core_reliability.py#L69)

```python
def test_eof_without_terminal_reason_preserves_partial_and_pauses(self)
```

Проверка: EOF сохраняет частичный текст, выставляет incomplete и paused вместо completed.

### `CoreReliabilityTests.test_eof_without_terminal_reason_never_executes_native_call`

[Исходник](../../tests/test_core_reliability.py#L76)

```python
def test_eof_without_terminal_reason_never_executes_native_call(self)
```

Проверка: Полные аргументы native call без terminal reason не исполняются и не попадают в canonical tool block.

### `CoreReliabilityTests.test_access_policy_is_rechecked_after_file_approval`

[Исходник](../../tests/test_core_reliability.py#L83)

```python
def test_access_policy_is_rechecked_after_file_approval(self)
```

Проверка: новое правило во время просмотра diff блокирует ещё не выполненную запись.

### `CoreReliabilityTests.test_access_policy_is_rechecked_after_file_approval.approve`

[Исходник](../../tests/test_core_reliability.py#L85)

```python
def approve(*_args)
```

Меняет .neutralignore во время fixture approval для проверки отказа записи.

### `CoreReliabilityTests.test_auto_local_continues_text_without_duplicate_canonical_fragments`

[Исходник](../../tests/test_core_reliability.py#L93)

```python
def test_auto_local_continues_text_without_duplicate_canonical_fragments(self)
```

Проверка: length продолжается одним итоговым сообщением без старого таймера локальной задачи.

### `CoreReliabilityTests.test_auto_local_retries_truncated_call_without_executing_its_fragment`

[Исходник](../../tests/test_core_reliability.py#L101)

```python
def test_auto_local_retries_truncated_call_without_executing_its_fragment(self)
```

Проверка: неполный вызов не выполняется; исполняется только заново полученный полный вызов.

### `CoreReliabilityTests.test_native_refusal_is_visible_and_not_completed`

[Исходник](../../tests/test_core_reliability.py#L110)

```python
def test_native_refusal_is_visible_and_not_completed(self)
```

Проверка: нативный отказ виден в истории и не превращается в успешное завершение

### `CoreReliabilityTests.test_malformed_write_returns_error_and_allows_model_repair`

[Исходник](../../tests/test_core_reliability.py#L115)

```python
def test_malformed_write_returns_error_and_allows_model_repair(self)
```

Проверка: path=null возвращает ошибку tool, после которой модель продолжает отвечать

### `CoreReliabilityTests.test_preview_io_error_is_a_tool_result_not_a_failed_run`

[Исходник](../../tests/test_core_reliability.py#L122)

```python
def test_preview_io_error_is_a_tool_result_not_a_failed_run(self)
```

Проверка: ошибка диска при подготовке diff возвращается модели без аварии всего запуска

### `CoreReliabilityTests.test_cancel_with_assistant_commentary_is_paused`

[Исходник](../../tests/test_core_reliability.py#L128)

```python
def test_cancel_with_assistant_commentary_is_paused(self)
```

Проверка: отмена предложения не становится completed даже при промежуточном тексте модели

### `CoreReliabilityTests.test_failed_command_cannot_be_overruled_by_final_answer`

[Исходник](../../tests/test_core_reliability.py#L134)

```python
def test_failed_command_cannot_be_overruled_by_final_answer(self)
```

Проверка: exit 7 сохраняется и блокирует completed несмотря на положительный текст модели

### `CoreReliabilityTests.test_successful_retry_of_same_command_resolves_failed_evidence`

[Исходник](../../tests/test_core_reliability.py#L143)

```python
def test_successful_retry_of_same_command_resolves_failed_evidence(self)
```

Проверка: успешный повтор той же команды заменяет прежний провал

### `CoreReliabilityTests.test_unrelated_success_does_not_erase_failed_command`

[Исходник](../../tests/test_core_reliability.py#L153)

```python
def test_unrelated_success_does_not_erase_failed_command(self)
```

Проверка: успех другой команды не стирает провал обязательной проверки

### `CoreReliabilityTests.test_answer_without_commands_is_explicitly_unverified`

[Исходник](../../tests/test_core_reliability.py#L161)

```python
def test_answer_without_commands_is_explicitly_unverified(self)
```

Проверка: ответ без выполненных команд получает явное not_run и сообщение о неподтверждённой проверке

### `CoreReliabilityTests.test_runtime_uses_one_minute_and_timer_is_always_cancelled`

[Исходник](../../tests/test_core_reliability.py#L166)

```python
def test_runtime_uses_one_minute_and_timer_is_always_cancelled(self)
```

Проверка: лимит в одну минуту не повышается до пяти, а таймер закрывается после задачи

### `CoreReliabilityTests.test_runtime_expiry_interrupts_an_outstanding_approval`

[Исходник](../../tests/test_core_reliability.py#L174)

```python
def test_runtime_expiry_interrupts_an_outstanding_approval(self)
```

Проверка: истечение срока прерывает ожидание diff, сохраняет задачу и не записывает файл

### `CoreReliabilityTests.test_runtime_expiry_interrupts_an_outstanding_approval.expire_at_approval`

[Исходник](../../tests/test_core_reliability.py#L176)

```python
def expire_at_approval(engine, path, diff, exists)
```

Имитирует истечение срока ровно при запросе подтверждения и вызывает настоящий обработчик ожидания.

### `CoreReliabilityTests.test_json_truncation_does_not_parse_or_execute_complete_prefix`

[Исходник](../../tests/test_core_reliability.py#L185)

```python
def test_json_truncation_does_not_parse_or_execute_complete_prefix(self)
```

Проверка: JSON-адаптер сохраняет length и не исполняет полный-looking JSON-префикс оборванного ответа

### `CoreReliabilityTests.test_responses_incomplete_and_refusal_are_not_cached_as_success`

[Исходник](../../tests/test_core_reliability.py#L192)

```python
def test_responses_incomplete_and_refusal_are_not_cached_as_success(self)
```

Проверка: Responses incomplete/refusal сохраняют причину остановки без кэширования успешного tool output

### `CoreReliabilityTests.test_endpoint_change_clears_omitted_or_stale_model_and_stt_keys`

[Исходник](../../tests/test_core_reliability.py#L200)

```python
def test_endpoint_change_clears_omitted_or_stale_model_and_stt_keys(self)
```

Проверка: смена адреса Лолы/STT очищает отсутствующий или явно повторённый старый ключ без его записи на диск

### `CoreReliabilityTests.test_key_is_retained_for_same_endpoint_and_fresh_key_for_new_endpoint`

[Исходник](../../tests/test_core_reliability.py#L212)

```python
def test_key_is_retained_for_same_endpoint_and_fresh_key_for_new_endpoint(self)
```

Проверка: ключ сохраняется для прежнего сервера, а новый адрес принимает новый введённый ключ

<a id="module-tests-test-docs-reference-py"></a>

## `tests/test_docs_reference.py`

Проверка инвентаризации стороннего CLI без включения его внутренностей в API приложения.

### `ReferenceInventoryTests`

[Исходник](../../tests/test_docs_reference.py#L12)

```python
class ReferenceInventoryTests(unittest.TestCase)
```

Проверяет инвентаризацию и вход AST extractor для стороннего и собственного кода.

### `ReferenceInventoryTests.test_vendor_is_in_inventory_but_not_in_ast_or_toc`

[Исходник](../../tests/test_docs_reference.py#L14)

```python
def test_vendor_is_in_inventory_but_not_in_ast_or_toc(self)
```

Сторонний CLI остаётся в file map, но не передаётся extractor и не попадает в оглавление API; собственный entrypoint остаётся.

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

[Исходник](../../tests/test_editor_service.py#L11)

```python
class EditorServiceTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope.

### `EditorServiceTests.setUp`

[Исходник](../../tests/test_editor_service.py#L12)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `EditorServiceTests.tearDown`

[Исходник](../../tests/test_editor_service.py#L20)

```python
def tearDown(self)
```

Закрывает ресурсы и удаляет временные данные после теста.

### `EditorServiceTests.proposal`

[Исходник](../../tests/test_editor_service.py#L23)

```python
def proposal(self, content='edited\nsecond\n')
```

Читает текущую revision и создаёт тестовый editor preview без записи.

### `EditorServiceTests.test_read_preview_and_one_shot_apply_preserve_crlf`

[Исходник](../../tests/test_editor_service.py#L27)

```python
def test_read_preview_and_one_shot_apply_preserve_crlf(self)
```

Проверка: Read сохраняет byte hash/CRLF; preview не пишет, Apply пишет один раз и обновляет revision.

### `EditorServiceTests.test_external_change_before_preview_and_after_approval_is_never_overwritten`

[Исходник](../../tests/test_editor_service.py#L42)

```python
def test_external_change_before_preview_and_after_approval_is_never_overwritten(self)
```

Проверка: Оба момента внешнего изменения возвращают FILE_CHANGED без перезаписи.

### `EditorServiceTests.test_reject_cancel_and_replaced_proposals_do_not_write`

[Исходник](../../tests/test_editor_service.py#L55)

```python
def test_reject_cancel_and_replaced_proposals_do_not_write(self)
```

Проверка: Отказ/отмена и старый ID после новой подготовки не меняют файл.

### `EditorServiceTests.test_unchanged_text_has_no_pending_write`

[Исходник](../../tests/test_editor_service.py#L66)

```python
def test_unchanged_text_has_no_pending_write(self)
```

Проверка: Неизменённый текст не создаёт write approval.

### `EditorServiceTests.test_editor_can_save_files_up_to_one_mb_and_recheck_conflicts`

[Исходник](../../tests/test_editor_service.py#L71)

```python
def test_editor_can_save_files_up_to_one_mb_and_recheck_conflicts(self)
```

Проверка: Редактор применяет файл ровно 1 МБ и отказывает при внешнем изменении; лимит агентского preview остаётся 120 КБ.

### `EditorServiceTests.test_change_between_revision_check_and_diff_does_not_authorize_stale_draft`

[Исходник](../../tests/test_editor_service.py#L86)

```python
def test_change_between_revision_check_and_diff_does_not_authorize_stale_draft(self)
```

Проверка: Изменение файла между проверкой revision и снимком diff не создаёт разрешения на устаревший черновик.

### `EditorServiceTests.test_change_between_revision_check_and_diff_does_not_authorize_stale_draft.external_change`

[Исходник](../../tests/test_editor_service.py#L88)

```python
def external_change(*args, **kwargs)
```

Детерминированно меняет файл между проверкой editor revision и построением снимка diff.

### `EditorServiceTests.test_outside_binary_invalid_utf8_and_large_files_are_rejected`

[Исходник](../../tests/test_editor_service.py#L97)

```python
def test_outside_binary_invalid_utf8_and_large_files_are_rejected(self)
```

Проверка: Editor отвергает traversal, неверную кодировку, NUL и превышение 1 МБ.

### `EditorServiceTests.test_proposal_cannot_be_applied_to_another_project`

[Исходник](../../tests/test_editor_service.py#L108)

```python
def test_proposal_cannot_be_applied_to_another_project(self)
```

Проверка: Proposal одного корня не применяется к другому проекту.

<a id="module-tests-test-expansion-py"></a>

## `tests/test_expansion.py`

Контракты разделения истории, профиля без секретов, JSON tools, KV whitelist, PC grants, Telegram owner и WAV validation.

### `ExpansionTests`

[Исходник](../../tests/test_expansion.py#L25)

```python
class ExpansionTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты разделения истории, профиля без секретов, JSON tools, KV whitelist, PC grants, Telegram owner и WAV validation.

### `ExpansionTests.test_lola_wake_migration_preserves_custom_phrase`

[Исходник](../../tests/test_expansion.py#L26)

```python
def test_lola_wake_migration_preserves_custom_phrase(self)
```

Проверка: Стандартная старая фраза становится Привет, Лола; пользовательская фраза сохраняется.

### `ExpansionTests.test_search_falls_back_to_bing_and_rejects_non_web_links`

[Исходник](../../tests/test_expansion.py#L30)

```python
def test_search_falls_back_to_bing_and_rejects_non_web_links(self)
```

Проверка: Имитирует таймаут DuckDuckGo и проверяет Bing RSS fallback с фильтрацией file-ссылок.

### `ExpansionTests.test_search_falls_back_to_bing_and_rejects_non_web_links.search_transport`

[Исходник](../../tests/test_expansion.py#L32)

```python
def search_transport(request)
```

Локальная HTTPX-фикстура недоступного первого поисковика и безопасной RSS-выдачи второго.

### `ExpansionTests.test_application_tools_broker_ids_without_shell_or_arguments`

[Исходник](../../tests/test_expansion.py#L43)

```python
def test_application_tools_broker_ids_without_shell_or_arguments(self)
```

Проверка: Проверяет передачу ID приложений в host broker, отказ путям/аргументам, отмену и общий выключатель PC tools.

### `ExpansionTests.test_companion_scope_rejects_cross_loading`

[Исходник](../../tests/test_expansion.py#L59)

```python
def test_companion_scope_rejects_cross_loading(self)
```

Проверка: Chat/voice списки раздельны; чужая область отклоняется при load/rename.

### `ExpansionTests.test_profile_does_not_persist_keys_or_change_main_model`

[Исходник](../../tests/test_expansion.py#L72)

```python
def test_profile_does_not_persist_keys_or_change_main_model(self)
```

Проверка: Сохраняет собственную модель/характер Лолы и не пишет API keys в JSON.

### `ExpansionTests.test_json_tools_never_execute_embedded_examples`

[Исходник](../../tests/test_expansion.py#L80)

```python
def test_json_tools_never_execute_embedded_examples(self)
```

Проверка: Принимает целый envelope и отклоняет unknown tools; пример с окружающим текстом не выполняется.

### `ExpansionTests.test_json_request_has_no_native_roles_or_api_fields`

[Исходник](../../tests/test_expansion.py#L88)

```python
def test_json_request_has_no_native_roles_or_api_fields(self)
```

Проверка: Удаляет native API tool fields и переводит tool roles в текстовые результаты.

### `ExpansionTests.test_json_stream_converts_complete_reply_to_tool_delta`

[Исходник](../../tests/test_expansion.py#L102)

```python
def test_json_stream_converts_complete_reply_to_tool_delta(self)
```

Проверка: Склеивает разорванный JSON и формирует обычный tool delta без показа служебного JSON как ответа.

### `ExpansionTests.test_pc_folders_come_only_from_human_prompt`

[Исходник](../../tests/test_expansion.py#L108)

```python
def test_pc_folders_come_only_from_human_prompt(self)
```

Проверка: Читает только папку из исходного запроса и отказывает сторонней папке и неразрешённому скриншоту.

### `ExpansionTests.test_telegram_ignores_other_users_groups_and_forwards`

[Исходник](../../tests/test_expansion.py#L120)

```python
def test_telegram_ignores_other_users_groups_and_forwards(self)
```

Проверка: Посторонние, группы и пересылки не вызывают даже Stop; owner private command работает.

### `ExpansionTests.test_telegram_approval_keeps_exact_current_id`

[Исходник](../../tests/test_expansion.py#L128)

```python
def test_telegram_approval_keeps_exact_current_id(self)
```

Проверка: Передаёт точный approval ID и текущий run ID обычному механизму подтверждения.

### `ExpansionTests.test_telegram_cannot_stop_or_approve_another_selected_chat`

[Исходник](../../tests/test_expansion.py#L150)

```python
def test_telegram_cannot_stop_or_approve_another_selected_chat(self)
```

Проверка: Telegram не отменяет и не подтверждает чужой выбранный чат; foreign background approval не становится remote pending действием.

### `ExpansionTests.test_telegram_poll_drops_backlog_and_never_sends_to_stranger`

[Исходник](../../tests/test_expansion.py#L159)

```python
def test_telegram_poll_drops_backlog_and_never_sends_to_stranger(self)
```

Проверка: Проверяет настоящий dispatcher с HTTPX MockTransport: старый /stop и чужой user игнорируются; status отправляется только owner; токен очищается.

### `ExpansionTests.test_telegram_poll_drops_backlog_and_never_sends_to_stranger.transport`

[Исходник](../../tests/test_expansion.py#L163)

```python
def transport(request)
```

HTTPX MockTransport Telegram: getMe/getUpdates/sendMessage без настоящего токена или внешнего сетевого запроса.

### `ExpansionTests.test_cache_preferences_survive_new_service`

[Исходник](../../tests/test_expansion.py#L181)

```python
def test_cache_preferences_survive_new_service(self)
```

Проверка: Параметры K/V/threads сохраняются и восстанавливаются новым RuntimeService без сохранения пути модели.

### `ExpansionTests.test_kv_cache_validates_before_launch`

[Исходник](../../tests/test_expansion.py#L195)

```python
def test_kv_cache_validates_before_launch(self)
```

Проверка: Отклоняет произвольный cache type и передаёт только whitelisted K/V/Flash Attention flags.

### `ExpansionTests.test_transcription_rejects_invalid_audio_without_network`

[Исходник](../../tests/test_expansion.py#L206)

```python
def test_transcription_rejects_invalid_audio_without_network(self)
```

Проверка: Некорректный WAV отклоняется до запуска сетевого worker.

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

<a id="module-tests-test-ide-completion-py"></a>

## `tests/test_ide_completion.py`

Проверки локальности, размера запроса и завершения клиента автодополнения.

### `CompletionTests`

[Исходник](../../tests/test_ide_completion.py#L7)

```python
class CompletionTests(unittest.TestCase)
```

Ограничения и жизненный цикл локального автодополнения.

### `CompletionTests.test_remote_does_not_construct_client`

[Исходник](../../tests/test_ide_completion.py#L8)

```python
def test_remote_does_not_construct_client(self)
```

Удалённый endpoint не создаёт completion client.

### `CompletionTests.test_outside_root_rejected`

[Исходник](../../tests/test_ide_completion.py#L13)

```python
def test_outside_root_rejected(self)
```

Файл за пределами проекта отклоняется до запроса.

### `CompletionTests.test_small_request_no_tools_and_cleanup`

[Исходник](../../tests/test_ide_completion.py#L18)

```python
def test_small_request_no_tools_and_cleanup(self)
```

Короткий completion не включает инструменты и закрывает клиент.

### `CompletionTests.test_large_context_rejected_before_http`

[Исходник](../../tests/test_ide_completion.py#L27)

```python
def test_large_context_rejected_before_http(self)
```

Слишком большой completion context не отправляется по HTTP.

<a id="module-tests-test-ide-execution-py"></a>

## `tests/test_ide_execution.py`

Проверки единственного editor writer, dirty/stale guards и неизвестных эффектов.

### `IdeExecutionTests`

[Исходник](../../tests/test_ide_execution.py#L11)

```python
class IdeExecutionTests(unittest.TestCase)
```

Executor fixture, проверяющий editor-owned записи и конфликтные состояния.

### `IdeExecutionTests.write_call`

[Исходник](../../tests/test_ide_execution.py#L15)

```python
def write_call(self)
```

Создаёт конкретное предложение write_file для executor fixture.

### `IdeExecutionTests.test_dirty_editor_rejects_before_approval_and_never_uses_python_writer`

[Исходник](../../tests/test_ide_execution.py#L19)

```python
def test_dirty_editor_rejects_before_approval_and_never_uses_python_writer(self)
```

Dirty buffer отклоняет предложение до approval и до Python writer.

### `IdeExecutionTests.test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation`

[Исходник](../../tests/test_ide_execution.py#L26)

```python
def test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation(self)
```

Editor остаётся единственным writer, сохраняются snapshot, receipt и generation.

### `IdeExecutionTests.test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation.effect`

[Исходник](../../tests/test_ide_execution.py#L29)

```python
def effect(*_)
```

Имитирует только подтверждённый editor effect тестового workspace.

### `IdeExecutionTests.test_unknown_editor_effect_is_not_replayed_or_sent_to_python_writer`

[Исходник](../../tests/test_ide_execution.py#L36)

```python
def test_unknown_editor_effect_is_not_replayed_or_sent_to_python_writer(self)
```

Неизвестный editor outcome не повторяется и не перенаправляется Python writer.

### `IdeExecutionTests.test_stale_disk_never_reaches_external_editor_apply`

[Исходник](../../tests/test_ide_execution.py#L42)

```python
def test_stale_disk_never_reaches_external_editor_apply(self)
```

Изменившийся disk snapshot блокирует внешний editor apply.

<a id="module-tests-test-ide-remote-control-py"></a>

## `tests/test_ide_remote_control.py`

Проверки управления IDE-запуском владельцем без переключения desktop view.

### `IdeRemoteControlTests`

[Исходник](../../tests/test_ide_remote_control.py#L13)

```python
class IdeRemoteControlTests(unittest.TestCase)
```

Проверки удалённого управления владельцем IDE-задачи.

### `IdeRemoteControlTests.owner`

[Исходник](../../tests/test_ide_remote_control.py#L14)

```python
def owner(self)
```

Создаёт тестового владельца IDE-сессии.

### `IdeRemoteControlTests.test_remote_owner_controls_native_run_without_switching_desktop`

[Исходник](../../tests/test_ide_remote_control.py#L21)

```python
def test_remote_owner_controls_native_run_without_switching_desktop(self)
```

Управление native run не меняет выбранный desktop чат.

### `IdeRemoteControlTests.test_remote_owner_controls_native_run_without_switching_desktop.command`

[Исходник](../../tests/test_ide_remote_control.py#L23)

```python
def command(text)
```

Имитирует командный ответ только текущего owner fixture.

### `IdeRemoteControlTests.test_ambiguous_native_runs_are_not_silently_selected`

[Исходник](../../tests/test_ide_remote_control.py#L28)

```python
def test_ambiguous_native_runs_are_not_silently_selected(self)
```

Несколько подходящих native runs требуют явной идентичности.

<a id="module-tests-test-ide-verification-py"></a>

## `tests/test_ide_verification.py`

18 контрактов критериев, readonly enforcement, снимков, аварийного и частичного отката, backup и schema upgrade.

### `IdeVerificationTests`

[Исходник](../../tests/test_ide_verification.py#L32)

```python
class IdeVerificationTests(unittest.TestCase)
```

Изолированный project/profile для проверки rollback и прав без реальных данных пользователя.

### `IdeVerificationTests.setUp`

[Исходник](../../tests/test_ide_verification.py#L33)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `IdeVerificationTests.executor`

[Исходник](../../tests/test_ide_verification.py#L43)

```python
def executor(self, **options)
```

Строит настоящий executor с журналом и фикстурным подтверждением файлов, без внешней модели.

### `IdeVerificationTests.apply`

[Исходник](../../tests/test_ide_verification.py#L47)

```python
def apply(self, name, args, executor=None)
```

Выполняет одну файловую операцию через durable batch и canonical receipt, возвращает проверенный результат.

### `IdeVerificationTests.test_roundtrip_nested_create_patch_rename_delete_preserves_original_bytes`

[Исходник](../../tests/test_ide_verification.py#L57)

```python
def test_roundtrip_nested_create_patch_rename_delete_preserves_original_bytes(self)
```

Проверка: один набор отменяет mkdir/write/patch/rename/delete и возвращает исходные CRLF bytes.

### `IdeVerificationTests.test_manual_edit_after_preview_blocks_entire_rollback`

[Исходник](../../tests/test_ide_verification.py#L73)

```python
def test_manual_edit_after_preview_blocks_entire_rollback(self)
```

Проверка: последующая ручная правка не даёт начать откат даже соседнего файла.

### `IdeVerificationTests.test_untracked_file_in_created_directory_is_never_removed`

[Исходник](../../tests/test_ide_verification.py#L84)

```python
def test_untracked_file_in_created_directory_is_never_removed(self)
```

Проверка: созданная папка с новым чужим файлом не удаляется автоматически.

### `IdeVerificationTests.test_intervening_manual_revision_starts_a_separate_undo_segment`

[Исходник](../../tests/test_ide_verification.py#L91)

```python
def test_intervening_manual_revision_starts_a_separate_undo_segment(self)
```

Проверка: откат второй правки возвращает ручную промежуточную версию и не затирает её первым сегментом.

### `IdeVerificationTests.test_binary_rename_undo_is_byte_exact`

[Исходник](../../tests/test_ide_verification.py#L101)

```python
def test_binary_rename_undo_is_byte_exact(self)
```

Проверка: обратный перенос восстанавливает двоичный файл без перекодирования.

### `IdeVerificationTests.test_snapshot_failure_prevents_file_dispatch`

[Исходник](../../tests/test_ide_verification.py#L109)

```python
def test_snapshot_failure_prevents_file_dispatch(self)
```

Проверка: ошибка сохранения before не допускает write и не пересекает started.

### `IdeVerificationTests.test_read_only_blocks_files_commands_and_unknown_external_tools`

[Исходник](../../tests/test_ide_verification.py#L117)

```python
def test_read_only_blocks_files_commands_and_unknown_external_tools(self)
```

Проверка: readonly policy блокирует mutators, команды и неизвестные внешние effects до dispatch.

### `IdeVerificationTests.test_model_plan_cannot_erase_user_criteria_or_invent_evidence`

[Исходник](../../tests/test_ide_verification.py#L128)

```python
def test_model_plan_cannot_erase_user_criteria_or_invent_evidence(self)
```

Проверка: модель не удаляет критерии пользователя и не придумывает IDs или успех проверок.

### `IdeVerificationTests.test_checks_are_exactly_linked_and_invalidated_by_further_edits`

[Исходник](../../tests/test_ide_verification.py#L136)

```python
def test_checks_are_exactly_linked_and_invalidated_by_further_edits(self)
```

Проверка: неверный argv не подтверждает критерий; новая правка делает правильный старый тест устаревшим.

### `IdeVerificationTests.test_rollback_invalidates_receipts_even_after_projection_loss`

[Исходник](../../tests/test_ide_verification.py#L150)

```python
def test_rollback_invalidates_receipts_even_after_projection_loss(self)
```

Проверка: долговечная rollback revision инвалидирует старые тесты после recovery без повторного увеличения generation.

### `IdeVerificationTests.test_partial_rollback_is_durable_and_never_replayed_implicitly`

[Исходник](../../tests/test_ide_verification.py#L164)

```python
def test_partial_rollback_is_durable_and_never_replayed_implicitly(self)
```

Проверка: частичный отказ сохраняет состояние и требует ручной проверки без автоматического повтора.

### `IdeVerificationTests.test_partial_rollback_is_durable_and_never_replayed_implicitly.fail_second`

[Исходник](../../tests/test_ide_verification.py#L169)

```python
def fail_second(path, *args)
```

Воспроизводит отказ второго файла после успешного восстановления первого.

### `IdeVerificationTests.test_prepared_snapshot_is_not_automatically_adopted_after_crash`

[Исходник](../../tests/test_ide_verification.py#L182)

```python
def test_prepared_snapshot_is_not_automatically_adopted_after_crash(self)
```

Проверка: потерянный after нельзя выдать за безопасный snapshot даже при успешном tool receipt.

### `IdeVerificationTests.test_snapshot_backup_can_restore_originals_in_a_fresh_profile`

[Исходник](../../tests/test_ide_verification.py#L189)

```python
def test_snapshot_backup_can_restore_originals_in_a_fresh_profile(self)
```

Проверка: ZIP включает необходимые snapshot artifacts, из которых можно восстановить оригиналы после переноса.

### `IdeVerificationTests.test_schema_one_upgrade_preserves_canonical_history`

[Исходник](../../tests/test_ide_verification.py#L203)

```python
def test_schema_one_upgrade_preserves_canonical_history(self)
```

Проверка: транзакционная миграция SQLite v1 в v2 сохраняет каноническую историю.

### `IdeVerificationTests.test_user_checks_use_real_approval_without_model_or_extra_capabilities`

[Исходник](../../tests/test_ide_verification.py#L213)

```python
def test_user_checks_use_real_approval_without_model_or_extra_capabilities(self)
```

Проверка: checks_only не вызывает модель и не включает отключённые команды; purpose виден в обычном approval.

### `IdeVerificationTests.test_invalid_options_do_not_start_commands_or_replace_task`

[Исходник](../../tests/test_ide_verification.py#L235)

```python
def test_invalid_options_do_not_start_commands_or_replace_task(self)
```

Проверка: неверные ограничения и пустые команды отклоняются до работы.

### `IdeVerificationTests.test_real_process_exit_during_rollback_requires_manual_review`

[Исходник](../../tests/test_ide_verification.py#L239)

```python
def test_real_process_exit_during_rollback_requires_manual_review(self)
```

Проверка: настоящий os._exit между effects оставляет rolling_back, сохраняет соседние данные и блокирует неподтверждённое продолжение.

### `IdeVerificationTests.test_manual_change_during_partial_restore_is_preserved`

[Исходник](../../tests/test_ide_verification.py#L265)

```python
def test_manual_change_during_partial_restore_is_preserved(self)
```

Проверка: изменение второго файла уже во время отката сохраняется, состояние становится rollback_unknown.

### `IdeVerificationTests.test_manual_change_during_partial_restore_is_preserved.concurrent_edit`

[Исходник](../../tests/test_ide_verification.py#L269)

```python
def concurrent_edit(path, *args)
```

Вставляет чужую правку второго файла между filesystem effects отката.

<a id="module-tests-test-json-compatibility-py"></a>

## `tests/test_json_compatibility.py`

JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.

### `action`

[Исходник](../../tests/test_json_compatibility.py#L18)

```python
def action(kind='tool', **values)
```

Формирует полный action envelope для детерминированных SSE ответов.

### `Source`

[Исходник](../../tests/test_json_compatibility.py#L23)

```python
class Source
```

Тестовый класс/фикстура: JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.

### `Source.__init__`

[Исходник](../../tests/test_json_compatibility.py#L25)

```python
def __init__(self, text, finish='stop', refusal=None)
```

Инициализирует состояние экземпляра Source; параметры показаны в сигнатуре, назначение описано у класса.

### `Source.__iter__`

[Исходник](../../tests/test_json_compatibility.py#L27)

```python
def __iter__(self)
```

Выдаёт один chunk с заданным terminal evidence и refusal.

### `Source.close`

[Исходник](../../tests/test_json_compatibility.py#L29)

```python
def close(self)
```

Делает закрытие источника наблюдаемым для теста repair.

### `Handler`

[Исходник](../../tests/test_json_compatibility.py#L32)

```python
class Handler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.

### `Handler.log_message`

[Исходник](../../tests/test_json_compatibility.py#L34)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `Handler.do_POST`

[Исходник](../../tests/test_json_compatibility.py#L35)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `JsonCompatibilityTests`

[Исходник](../../tests/test_json_compatibility.py#L50)

```python
class JsonCompatibilityTests(unittest.TestCase)
```

Тестовый класс/фикстура: JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.

### `JsonCompatibilityTests.test_decoded_final_history_restores_json_without_promoting_examples`

[Исходник](../../tests/test_json_compatibility.py#L51)

```python
def test_decoded_final_history_restores_json_without_promoting_examples(self)
```

Проверка: декодированный ответ возвращается в JSON envelope; показанные примеры инструментов остаются текстом, каноническая история не меняется.

### `JsonCompatibilityTests.server`

[Исходник](../../tests/test_json_compatibility.py#L64)

```python
def server(self, replies)
```

Запускает временный loopback SSE endpoint с очередью ответов и очисткой.

### `JsonCompatibilityTests.test_prose_is_regenerated_never_extracted`

[Исходник](../../tests/test_json_compatibility.py#L71)

```python
def test_prose_is_regenerated_never_extracted(self)
```

Проверка: команда внутри пояснения не исполняется; наружу попадает только отдельный принятый ответ repair.

### `JsonCompatibilityTests.test_prose_is_regenerated_never_extracted.repair`

[Исходник](../../tests/test_json_compatibility.py#L75)

```python
def repair(text, error, attempt)
```

Возвращает отдельный корректный read вместо скрытого в пояснении write.

### `JsonCompatibilityTests.test_repairs_are_bounded_and_ambiguous_batches_never_yield`

[Исходник](../../tests/test_json_compatibility.py#L82)

```python
def test_repairs_are_bounded_and_ambiguous_batches_never_yield(self)
```

Проверка: ровно до двух исправлений; валидный префикс невалидного batch не становится вызовом.

### `JsonCompatibilityTests.test_repairs_are_bounded_and_ambiguous_batches_never_yield.repair`

[Исходник](../../tests/test_json_compatibility.py#L86)

```python
def repair(text, error, attempt)
```

Записывает номер попытки и снова выдаёт ошибочный batch для проверки границы.

### `JsonCompatibilityTests.test_incomplete_and_refused_responses_never_enter_repair`

[Исходник](../../tests/test_json_compatibility.py#L91)

```python
def test_incomplete_and_refused_responses_never_enter_repair(self)
```

Проверка: EOF/length/refusal не запускают protocol retry и не выдают tool delta.

### `JsonCompatibilityTests.test_transport_cancellation_is_not_protocol_repair`

[Исходник](../../tests/test_json_compatibility.py#L100)

```python
def test_transport_cancellation_is_not_protocol_repair(self)
```

Проверка: отмена и ошибка транспортного итератора распространяются без новой генерации.

### `JsonCompatibilityTests.test_transport_cancellation_is_not_protocol_repair.Cancelled`

[Исходник](../../tests/test_json_compatibility.py#L102)

```python
class Cancelled(Source)
```

Тестовый класс/фикстура: JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.

### `JsonCompatibilityTests.test_transport_cancellation_is_not_protocol_repair.Cancelled.__iter__`

[Исходник](../../tests/test_json_compatibility.py#L103)

```python
def __iter__(self)
```

Имитирует отмену получения ответа до протокольного разбора.

### `JsonCompatibilityTests.test_required_and_none_choices_survive_regeneration`

[Исходник](../../tests/test_json_compatibility.py#L107)

```python
def test_required_and_none_choices_survive_regeneration(self)
```

Проверка: repair не обходит обязательный инструмент и запрет инструментов в финальном ответе.

### `JsonCompatibilityTests.test_request_has_one_protocol_and_compact_schemas`

[Исходник](../../tests/test_json_compatibility.py#L114)

```python
def test_request_has_one_protocol_and_compact_schemas(self)
```

Проверка: canonical action в истории и инструкциях; нет native API tools/roles и мутации исходных данных.

### `JsonCompatibilityTests.test_compact_core_catalog_keeps_required_and_custom_schema`

[Исходник](../../tests/test_json_compatibility.py#L124)

```python
def test_compact_core_catalog_keeps_required_and_custom_schema(self)
```

Проверка: сокращаются только optional core поля; required/write/custom/MCP схемы и оригиналы сохраняются.

### `JsonCompatibilityTests.test_real_transport_repairs_are_counted_fitted_and_isolated`

[Исходник](../../tests/test_json_compatibility.py#L139)

```python
def test_real_transport_repairs_are_counted_fitted_and_isolated(self)
```

Проверка: настоящие SSE POST/usage учитывают repair, fit сохраняет исходную задачу и canonical историю.

### `JsonCompatibilityTests.test_repair_cannot_bypass_budget_or_pending_stop`

[Исходник](../../tests/test_json_compatibility.py#L155)

```python
def test_repair_cannot_bypass_budget_or_pending_stop(self)
```

Проверка: невмещаемый запрос и Stop блокируют repair до транспортного запроса.

### `JsonCompatibilityTests.test_repaired_write_still_waits_for_approval`

[Исходник](../../tests/test_json_compatibility.py#L166)

```python
def test_repaired_write_still_waits_for_approval(self)
```

Проверка: Engine отклоняет исправленную JSON-запись через approval, файл не меняется, task usage учитывает repair.

### `JsonCompatibilityTests.test_repaired_write_still_waits_for_approval.reject`

[Исходник](../../tests/test_json_compatibility.py#L181)

```python
def reject(*args)
```

Проверяет неизменность файла до approval и отклоняет запись.

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

<a id="module-tests-test-mcp-reliability-py"></a>

## `tests/test_mcp_reliability.py`

Регрессии идентичности MCP, миграции выключенных инструментов, единственной отменяемой discovery и настоящего медленного stdio сервера.

### `MCPReliabilityTests`

[Исходник](../../tests/test_mcp_reliability.py#L19)

```python
class MCPReliabilityTests(unittest.TestCase)
```

Проверяет service/transport MCP в изолированном каталоге; закрывает все discovery после каждого теста.

### `MCPReliabilityTests.setUp`

[Исходник](../../tests/test_mcp_reliability.py#L20)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `MCPReliabilityTests.add_server`

[Исходник](../../tests/test_mcp_reliability.py#L26)

```python
def add_server(self, identity='echo', **options)
```

Сохраняет явно настроенный сервер фикстуры и возвращает его публичную запись.

### `MCPReliabilityTests.test_full_endpoint_alias_separates_long_prefixes_and_connections`

[Исходник](../../tests/test_mcp_reliability.py#L30)

```python
def test_full_endpoint_alias_separates_long_prefixes_and_connections(self)
```

Проверка: общий префикс ID и одинаковые имена tools не смешивают серверы и соединения

### `MCPReliabilityTests.test_migrate_legacy_collision_preserves_disabled_tools_and_plugin_links`

[Исходник](../../tests/test_mcp_reliability.py#L42)

```python
def test_migrate_legacy_collision_preserves_disabled_tools_and_plugin_links(self)
```

Проверка: старые aliases мигрируют со ссылками плагинов и сохраняют явные выключения

### `MCPReliabilityTests.test_duplicate_names_are_rejected_before_overwriting_previous_catalog`

[Исходник](../../tests/test_mcp_reliability.py#L61)

```python
def test_duplicate_names_are_rejected_before_overwriting_previous_catalog(self)
```

Проверка: повторяющиеся имена MCP не перезаписывают прежний корректный каталог

### `MCPReliabilityTests.test_single_discovery_is_cancellable_and_does_not_publish_late_tools`

[Исходник](../../tests/test_mcp_reliability.py#L70)

```python
def test_single_discovery_is_cancellable_and_does_not_publish_late_tools(self)
```

Проверка: одна discovery на сервер отменяется, её опоздавшие схемы не включаются

### `MCPReliabilityTests.test_single_discovery_is_cancellable_and_does_not_publish_late_tools.operation`

[Исходник](../../tests/test_mcp_reliability.py#L73)

```python
def operation(*_, interrupted=None, **kwargs)
```

Удерживает фиктивное discovery до cancellation, затем возвращает опоздавшие схемы для проверки их отклонения.

### `MCPReliabilityTests.test_shutdown_cancels_workers_and_rejects_new_discovery`

[Исходник](../../tests/test_mcp_reliability.py#L87)

```python
def test_shutdown_cancels_workers_and_rejects_new_discovery(self)
```

Проверка: закрытие сервиса отменяет worker и запрещает новые проверки

### `MCPReliabilityTests.test_shutdown_cancels_workers_and_rejects_new_discovery.operation`

[Исходник](../../tests/test_mcp_reliability.py#L89)

```python
def operation(*_, interrupted=None, **kwargs)
```

Имитирует работу транспорта до отмены при shutdown сервиса.

### `MCPReliabilityTests.test_real_stdio_discovery_can_finish_after_old_ten_second_deadline`

[Исходник](../../tests/test_mcp_reliability.py#L99)

```python
def test_real_stdio_discovery_can_finish_after_old_ten_second_deadline(self)
```

Проверка: настоящий stdio сервер с задержкой запуска 11 секунд успешно возвращает инструменты

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

<a id="module-tests-test-neutral-conversations-py"></a>

## `tests/test_neutral_conversations.py`

Изоляция проектов/режимов, архив, удаление, копия/повтор, экспорт и профили без ключей.

### `NeutralConversationTests`

[Исходник](../../tests/test_neutral_conversations.py#L13)

```python
class NeutralConversationTests(unittest.TestCase)
```

Изолированное временное хранилище проектов и чатов для мутаций/экспорта.

### `NeutralConversationTests.setUp`

[Исходник](../../tests/test_neutral_conversations.py#L14)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `NeutralConversationTests.test_project_instructions_and_chat_move_preserve_canonical_messages`

[Исходник](../../tests/test_neutral_conversations.py#L26)

```python
def test_project_instructions_and_chat_move_preserve_canonical_messages(self)
```

Проверка: Перемещение меняет пространство без потери сообщений; поиск и доступ проверяют группу/режим.

### `NeutralConversationTests.test_pin_archive_delete_and_explicit_confirmation`

[Исходник](../../tests/test_neutral_conversations.py#L36)

```python
def test_pin_archive_delete_and_explicit_confirmation(self)
```

Проверка: Закрепление и архив видны в индексе; удаление требует подтверждения и убирает только выбранный чат.

### `NeutralConversationTests.test_fork_and_retry_never_reuse_checkpoint_or_change_original`

[Исходник](../../tests/test_neutral_conversations.py#L46)

```python
def test_fork_and_retry_never_reuse_checkpoint_or_change_original(self)
```

Проверка: Новая ветка имеет новый ID и не наследует checkpoint; исходная история сохраняется.

### `NeutralConversationTests.test_exports_and_search_keep_modes_isolated`

[Исходник](../../tests/test_neutral_conversations.py#L54)

```python
def test_exports_and_search_keep_modes_isolated(self)
```

Проверка: Экспорт сохраняет нужные сообщения, поиск Chat не раскрывает отдельную историю Лолы.

### `NeutralConversationTests.test_profiles_strip_secrets_and_validate_protocol`

[Исходник](../../tests/test_neutral_conversations.py#L62)

```python
def test_profiles_strip_secrets_and_validate_protocol(self)
```

Проверка: Профили сохраняют Responses-настройки без ключа и отклоняют credentials в URL.

<a id="module-tests-test-neutral-extensions-py"></a>

## `tests/test_neutral_extensions.py`

Переключатели, неизменяемый снимок, навыки-черновики, пакеты и реальные MCP transports.

### `NeutralExtensionsTests`

[Исходник](../../tests/test_neutral_extensions.py#L15)

```python
class NeutralExtensionsTests(unittest.TestCase)
```

Проверки реестра и настоящих локальных MCP соединений.

### `NeutralExtensionsTests.setUp`

[Исходник](../../tests/test_neutral_extensions.py#L16)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `NeutralExtensionsTests.test_disabled_tools_and_groups_are_enforced_and_snapshot_is_frozen`

[Исходник](../../tests/test_neutral_extensions.py#L21)

```python
def test_disabled_tools_and_groups_are_enforced_and_snapshot_is_frozen(self)
```

Проверка: Отключённые tools недоступны следующему запуску; прежний снимок не изменяется задним числом.

### `NeutralExtensionsTests.test_generated_skill_is_reviewable_draft_and_lazy_loaded_after_enable`

[Исходник](../../tests/test_neutral_extensions.py#L30)

```python
def test_generated_skill_is_reviewable_draft_and_lazy_loaded_after_enable(self)
```

Проверка: Опыт создаётся выключенным, после включения читается по запросу, body не включается в каталог prompt.

### `NeutralExtensionsTests.test_learning_toggle_and_plugin_validation`

[Исходник](../../tests/test_neutral_extensions.py#L42)

```python
def test_learning_toggle_and_plugin_validation(self)
```

Проверка: Выключение обучения убирает create_skill, пакет не ссылается на неизвестный tool и включается явно.

### `NeutralExtensionsTests.test_mcp_stdio_discovery_call_confirmation_and_cancellation`

[Исходник](../../tests/test_neutral_extensions.py#L51)

```python
def test_mcp_stdio_discovery_call_confirmation_and_cancellation(self)
```

Проверка: Настоящий stdio SDK проходит discovery, отказ, проверку JSON Schema, вызов и отмену ожидания.

### `NeutralExtensionsTests.test_server_url_does_not_store_credentials_and_change_invalidates_tools`

[Исходник](../../tests/test_neutral_extensions.py#L66)

```python
def test_server_url_does_not_store_credentials_and_change_invalidates_tools(self)
```

Проверка: MCP URL с паролем отклоняется, токен не записывается и сбрасывается при смене адреса.

### `NeutralExtensionsTests.test_mcp_streamable_http_discovers_and_calls_real_server`

[Исходник](../../tests/test_neutral_extensions.py#L73)

```python
def test_mcp_streamable_http_discovers_and_calls_real_server(self)
```

Проверка: Официальный локальный Streamable HTTP сервер отдаёт схемы и выполняет подтверждённый tool.

### `NeutralExtensionsTests.test_progress_guard_detects_alternation_but_allows_changing_results`

[Исходник](../../tests/test_neutral_extensions.py#L90)

```python
def test_progress_guard_detects_alternation_but_allows_changing_results(self)
```

Проверка: Чередующийся A/B цикл останавливается по повтору результата; новый результат считается продвижением.

<a id="module-tests-test-optional-ide-py"></a>

## `tests/test_optional_ide.py`

14 контрактов опциональности, бюджета, реального LSP/Git, недоверенных server edits, удаления и container argv/cleanup.

### `ResearchHandler`

[Исходник](../../tests/test_optional_ide.py#L27)

```python
class ResearchHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: 14 контрактов опциональности, бюджета, реального LSP/Git, недоверенных server edits, удаления и container argv/cleanup.

### `ResearchHandler.log_message`

[Исходник](../../tests/test_optional_ide.py#L28)

```python
def log_message(self, *args)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ResearchHandler.do_POST`

[Исходник](../../tests/test_optional_ide.py#L29)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `OptionalIdeTests`

[Исходник](../../tests/test_optional_ide.py#L38)

```python
class OptionalIdeTests(unittest.TestCase)
```

Тестовый класс/фикстура: 14 контрактов опциональности, бюджета, реального LSP/Git, недоверенных server edits, удаления и container argv/cleanup.

### `OptionalIdeTests.setUp`

[Исходник](../../tests/test_optional_ide.py#L39)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `OptionalIdeTests.model`

[Исходник](../../tests/test_optional_ide.py#L43)

```python
def model(self, hold=False)
```

Поднимает локальный HTTP fixture и конфигурацию модели; release/shutdown зарегистрированы в cleanup.

### `OptionalIdeTests.service`

[Исходник](../../tests/test_optional_ide.py#L48)

```python
def service(self, config=None)
```

Создаёт isolated optional service с настоящим inference gate и idle guard.

### `OptionalIdeTests.service.idle`

[Исходник](../../tests/test_optional_ide.py#L52)

```python
def idle()
```

Не позволяет менять scope/settings во время фонового optional job.

### `OptionalIdeTests.git`

[Исходник](../../tests/test_optional_ide.py#L57)

```python
def git(self, *args, cwd=None)
```

Запускает только тестовый Git в disposable репозитории и проверяет exit code.

### `OptionalIdeTests.repository`

[Исходник](../../tests/test_optional_ide.py#L62)

```python
def repository(self)
```

Создаёт минимальный initial commit и manager отдельного каталога без обращения к проектному Git.

### `OptionalIdeTests.test_optional_features_default_off_and_require_exact_confirmation`

[Исходник](../../tests/test_optional_ide.py#L66)

```python
def test_optional_features_default_off_and_require_exact_confirmation(self)
```

Проверка: все возможности выключены; запуск без opt-in и строковое confirmed отклоняются.

### `OptionalIdeTests.test_optional_settings_reject_shell_fields_and_unbounded_budgets`

[Исходник](../../tests/test_optional_ide.py#L74)

```python
def test_optional_settings_reject_shell_fields_and_unbounded_budgets(self)
```

Проверка: таймауты, image options, пустой LSP program и произвольные mounts не проходят настройки.

### `OptionalIdeTests.test_research_one_request_bounded_sources_no_tools_and_no_secret_excerpt`

[Исходник](../../tests/test_optional_ide.py#L84)

```python
def test_research_one_request_bounded_sources_no_tools_and_no_secret_excerpt(self)
```

Проверка: один настоящий HTTP запрос без tools/credential excerpts; bounded источники и неизменённый проект.

### `OptionalIdeTests.test_research_offline_budget_refuses_before_http`

[Исходник](../../tests/test_optional_ide.py#L92)

```python
def test_research_offline_budget_refuses_before_http(self)
```

Проверка: payload не помещается в окно и отклоняется до контакта с моделью.

### `OptionalIdeTests.test_research_holds_shared_gate_until_cancelled_worker_exits`

[Исходник](../../tests/test_optional_ide.py#L97)

```python
def test_research_holds_shared_gate_until_cancelled_worker_exits(self)
```

Проверка: исследователь удерживает единый gate, отмена закрывает HTTP и освобождает владельца только после worker.

### `OptionalIdeTests.test_lsp_real_frames_reports_location_and_refuses_server_edit`

[Исходник](../../tests/test_optional_ide.py#L107)

```python
def test_lsp_real_frames_reports_location_and_refuses_server_edit(self)
```

Проверка: реальный LSP stderr/stdin transport, location, отбрасывание чужого URI и отказ workspace/applyEdit.

### `OptionalIdeTests.test_lsp_deadline_interrupts_server_that_never_reads_stdin`

[Исходник](../../tests/test_optional_ide.py#L114)

```python
def test_lsp_deadline_interrupts_server_that_never_reads_stdin(self)
```

Проверка: deadline закрывает зависший server и заблокированную большую запись didOpen без зависания bridge.

### `OptionalIdeTests.test_lsp_frame_limits_and_foreign_paths_are_rejected`

[Исходник](../../tests/test_optional_ide.py#L120)

```python
def test_lsp_frame_limits_and_foreign_paths_are_rejected(self)
```

Проверка: oversized/truncated frame и файл вне root отклоняются.

### `OptionalIdeTests.test_worktree_create_diff_remove_keeps_primary_checkout_unchanged`

[Исходник](../../tests/test_optional_ide.py#L126)

```python
def test_worktree_create_diff_remove_keeps_primary_checkout_unchanged(self)
```

Проверка: реальный detached checkout, shared список из копии, запрет удаления открытой копии и сохранность исходных ручных правок.

### `OptionalIdeTests.test_worktree_refuses_unknown_id_dirty_untracked_and_new_commits`

[Исходник](../../tests/test_optional_ide.py#L136)

```python
def test_worktree_refuses_unknown_id_dirty_untracked_and_new_commits(self)
```

Проверка: чужой ID, новые файлы и commits не допускают удаления; настоящий diff сохраняется.

### `OptionalIdeTests.test_worktree_owned_path_cannot_escape_managed_directory`

[Исходник](../../tests/test_optional_ide.py#L147)

```python
def test_worktree_owned_path_cannot_escape_managed_directory(self)
```

Проверка: подменённый receipt не разрешает путь за пределами managed directory.

### `OptionalIdeTests.test_container_argv_fixed_boundaries_no_network_no_host_write`

[Исходник](../../tests/test_optional_ide.py#L152)

```python
def test_container_argv_fixed_boundaries_no_network_no_host_write(self)
```

Проверка: фиксированные сетевые/файловые/CPU/user ограничения и проверенный cwd.

### `OptionalIdeTests.test_container_denial_never_contacts_docker_and_cancel_cleans_daemon_container`

[Исходник](../../tests/test_optional_ide.py#L158)

```python
def test_container_denial_never_contacts_docker_and_cancel_cleans_daemon_container(self)
```

Проверка: отказ не контактирует с Docker; отмена всегда удаляет daemon container по выданному UUID.

### `OptionalIdeTests.test_container_denial_never_contacts_docker_and_cancel_cleans_daemon_container.execute`

[Исходник](../../tests/test_optional_ide.py#L163)

```python
def execute(command, *args, **kwargs)
```

Fixture Docker argv responses для проверки отказа/cleanup без установки Docker.

### `OptionalIdeTests.test_bounded_process_deadline_kills_child_and_filters_environment`

[Исходник](../../tests/test_optional_ide.py#L174)

```python
def test_bounded_process_deadline_kills_child_and_filters_environment(self)
```

Проверка: дочерний процесс заканчивается по сроку, ключи не передаются через env.

<a id="module-tests-test-process-identity-py"></a>

## `tests/test_process_identity.py`

Real child lifetime probe plus conservative PID reuse, legacy owner and whole-tree telemetry recovery tests.

### `ProcessIdentityTests`

[Исходник](../../tests/test_process_identity.py#L14)

```python
class ProcessIdentityTests(unittest.TestCase)
```

Тестовый класс/фикстура: Real child lifetime probe plus conservative PID reuse, legacy owner and whole-tree telemetry recovery tests.

### `ProcessIdentityTests.test_real_process_lifetime_is_stable_then_dead_without_signalling_probe`

[Исходник](../../tests/test_process_identity.py#L15)

```python
def test_real_process_lifetime_is_stable_then_dead_without_signalling_probe(self)
```

Проверка: Проверяет lifetime текущего и собственного дочернего процесса; после естественного выхода child probe доказывает завершение owner.

### `ProcessIdentityTests.test_windows_probe_never_uses_os_kill`

[Исходник](../../tests/test_process_identity.py#L32)

```python
@unittest.skipUnless(os.name == 'nt', 'Windows query-only process handles')
def test_windows_probe_never_uses_os_kill(self)
```

Проверка: Windows lifetime probe работает при запрете любого os.kill вызова.

### `ProcessIdentityTests.test_uncertain_or_incomparable_identity_never_proves_owner_ended`

[Исходник](../../tests/test_process_identity.py#L36)

```python
def test_uncertain_or_incomparable_identity_never_proves_owner_ended(self)
```

Проверка: Access uncertainty, legacy token и разные token schemes не считаются смертью; сравнимый новый token доказывает PID reuse.

### `ProcessIdentityTests.test_linux_start_ticks_parse_complex_process_name`

[Исходник](../../tests/test_process_identity.py#L44)

```python
def test_linux_start_ticks_parse_complex_process_name(self)
```

Проверка: Парсер Linux proc stat сохраняет start ticks при пробелах и скобках в имени процесса.

### `ProcessIdentityTests.test_linux_start_ticks_parse_complex_process_name.read`

[Исходник](../../tests/test_process_identity.py#L46)

```python
def read(path, *args, **kwargs)
```

Подставляет proc stat и boot ID независимо от разделителей путей хостовой ОС.

### `OwnerRecoveryTests`

[Исходник](../../tests/test_process_identity.py#L52)

```python
class OwnerRecoveryTests(unittest.TestCase)
```

Тестовый класс/фикстура: Real child lifetime probe plus conservative PID reuse, legacy owner and whole-tree telemetry recovery tests.

### `OwnerRecoveryTests.test_reused_pid_recovers_whole_tree_once_preserving_terminal_state`

[Исходник](../../tests/test_process_identity.py#L56)

```python
def test_reused_pid_recovers_whole_tree_once_preserving_terminal_state(self)
```

Проверка: Повтор PID снимает reservations всего prototype дерева одной транзакцией, сохраняет failed/paused и не удваивает HTTP usage.

### `OwnerRecoveryTests.test_legacy_or_unreadable_live_owner_keeps_reservations`

[Исходник](../../tests/test_process_identity.py#L76)

```python
def test_legacy_or_unreadable_live_owner_keeps_reservations(self)
```

Проверка: Отсутствие creation token или недоступный live owner сохраняет активное состояние и reservation.

<a id="module-tests-test-project-command-py"></a>

## `tests/test_project_command.py`

Подтверждение и отказ запуска, корень cwd, код возврата, лимит вывода и отмена процесса.

### `ProjectCommandTests`

[Исходник](../../tests/test_project_command.py#L10)

```python
class ProjectCommandTests(unittest.TestCase)
```

Проверки подтверждения и жизненного цикла собственного тестового процесса.

### `ProjectCommandTests.setUp`

[Исходник](../../tests/test_project_command.py#L11)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ProjectCommandTests.test_rejected_command_never_executes_and_scope_cannot_escape`

[Исходник](../../tests/test_project_command.py#L14)

```python
def test_rejected_command_never_executes_and_scope_cannot_escape(self)
```

Проверка: Отказ не создаёт файл и cwd вне корня не допускается.

### `ProjectCommandTests.test_success_and_nonzero_exit_are_observable`

[Исходник](../../tests/test_project_command.py#L20)

```python
def test_success_and_nonzero_exit_are_observable(self)
```

Проверка: Запуск показывает точное предложение, возвращает Unicode-вывод и различает exit 0/7.

### `ProjectCommandTests.test_success_and_nonzero_exit_are_observable.approve`

[Исходник](../../tests/test_project_command.py#L22)

```python
def approve(*args)
```

Сохраняет предложение команды и подтверждает только тестовый запуск для проверки формы approval.

### `ProjectCommandTests.test_replaced_working_directory_after_approval_is_not_executed`

[Исходник](../../tests/test_project_command.py#L28)

```python
def test_replaced_working_directory_after_approval_is_not_executed(self)
```

Проверка: подмена cwd между preview и подтверждением блокирует запуск программы.

### `ProjectCommandTests.test_replaced_working_directory_after_approval_is_not_executed.replace`

[Исходник](../../tests/test_project_command.py#L31)

```python
def replace(*_args)
```

Подменяет каталог во время approval callback и проверяет отказ до запуска процесса.

### `ProjectCommandTests.test_output_is_bounded_and_cancellation_stops_child`

[Исходник](../../tests/test_project_command.py#L41)

```python
def test_output_is_bounded_and_cancellation_stops_child(self)
```

Проверка: Объём stdout ограничен 64 КБ, отмена быстро завершает собственный процесс.

<a id="module-tests-test-project-index-py"></a>

## `tests/test_project_index.py`

Изолированные AST/TS/FTS/watcher/cache тесты: exact ranges, incremental edits, policy revocation, offline recovery, cancel и corruption.

### `ProjectIndexTests`

[Исходник](../../tests/test_project_index.py#L19)

```python
class ProjectIndexTests(unittest.TestCase)
```

Тестовый класс/фикстура: Изолированные AST/TS/FTS/watcher/cache тесты: exact ranges, incremental edits, policy revocation, offline recovery, cancel и corruption.

### `ProjectIndexTests.setUp`

[Исходник](../../tests/test_project_index.py#L21)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ProjectIndexTests.wait`

[Исходник](../../tests/test_project_index.py#L30)

```python
def wait(self, predicate, seconds=15)
```

Ожидает проверяемый state/source fact до bounded deadline, при ошибке показывает status индекса.

### `ProjectIndexTests.hits`

[Исходник](../../tests/test_project_index.py#L38)

```python
def hits(self, query, mode='symbols', **params)
```

Получает текущие hash-verified matches либо пустой результат недоступного индекса.

### `ProjectIndexTests.test_python_typescript_symbols_have_exact_ranges_and_provenance`

[Исходник](../../tests/test_project_index.py#L43)

```python
def test_python_typescript_symbols_have_exact_ranges_and_provenance(self)
```

Проверка: AST/TS определения и методы имеют ожидаемые строки, kind, SHA, workspace и precision=syntax.

### `ProjectIndexTests.test_text_files_and_short_query_work_without_fts`

[Исходник](../../tests/test_project_index.py#L51)

```python
def test_text_files_and_short_query_work_without_fts(self)
```

Проверка: SQLite text fallback поддерживает кириллицу, короткий запрос и поиск пути, сохраняя indexed backend.

### `ProjectIndexTests.test_case_sensitive_symbols_and_file_paths_respect_request`

[Исходник](../../tests/test_project_index.py#L57)

```python
def test_case_sensitive_symbols_and_file_paths_respect_request(self)
```

Проверка: флаг регистра последовательно применяется к определениям и именам файлов.

### `ProjectIndexTests.test_transient_writer_sharing_error_does_not_disable_index`

[Исходник](../../tests/test_project_index.py#L62)

```python
def test_transient_writer_sharing_error_does_not_disable_index(self)
```

Проверка: краткий Windows sharing conflict восстанавливается bounded read-only retry без отключения индекса.

### `ProjectIndexTests.test_transient_writer_sharing_error_does_not_disable_index.transient`

[Исходник](../../tests/test_project_index.py#L65)

```python
def transient(*args, **kwargs)
```

Имитирует один краткий Windows sharing error, затем возвращает настоящее чтение файла.

### `ProjectIndexTests.test_updating_cache_returns_verified_partial_hits`

[Исходник](../../tests/test_project_index.py#L72)

```python
def test_updating_cache_returns_verified_partial_hits(self)
```

Проверка: фоновый delta update возвращает проверенные положительные результаты с partial marker, вместо ложного отсутствия.

### `ProjectIndexTests.test_queue_overflow_requires_recovery_without_unbounded_backlog`

[Исходник](../../tests/test_project_index.py#L78)

```python
def test_queue_overflow_requires_recovery_without_unbounded_backlog(self)
```

Проверка: переполнение очереди не оставляет неограниченный backlog и не возвращает ложное ready; новые события всё ещё допустимы.

### `ProjectIndexTests.test_cancel_interrupts_flat_directory_before_reading_remaining_files`

[Исходник](../../tests/test_project_index.py#L88)

```python
def test_cancel_interrupts_flat_directory_before_reading_remaining_files(self)
```

Проверка: отмена внутри широкой папки/пакета прерывает дальнейшее чтение и освобождает worker.

### `ProjectIndexTests.test_cancel_interrupts_flat_directory_before_reading_remaining_files.paused_read`

[Исходник](../../tests/test_project_index.py#L92)

```python
def paused_read(*args, **kwargs)
```

Задерживает одно чтение после начала пересборки для воспроизводимой проверки отмены до остальных файлов.

### `ProjectIndexTests.test_symlink_targets_are_never_indexed_through_aliases`

[Исходник](../../tests/test_project_index.py#L102)

```python
def test_symlink_targets_are_never_indexed_through_aliases(self)
```

Проверка: внешняя и внутренняя symlink alias не индексируются, обычные файлы остаются доступны.

### `ProjectIndexTests.test_editor_save_external_rename_delete_are_incremental`

[Исходник](../../tests/test_project_index.py#L112)

```python
def test_editor_save_external_rename_delete_are_incremental(self)
```

Проверка: настоящий editor save и внешние rename/delete обновляют cache без роста full_scans.

### `ProjectIndexTests.test_delete_during_subtree_read_is_incremental_absence`

[Исходник](../../tests/test_project_index.py#L123)

```python
def test_delete_during_subtree_read_is_incremental_absence(self)
```

Проверка: Удаление между directory enumeration и чтением трактуется как absence, не как необходимость полного rescan.

### `ProjectIndexTests.test_delete_during_subtree_read_is_incremental_absence.disappearing`

[Исходник](../../tests/test_project_index.py#L125)

```python
def disappearing(relative, policy, **kwargs)
```

Детерминированно удаляет один источник непосредственно перед read_once, проверяя штатный file-delete race.

### `ProjectIndexTests.test_stale_backdated_bytes_are_never_returned`

[Исходник](../../tests/test_project_index.py#L134)

```python
def test_stale_backdated_bytes_are_never_returned(self)
```

Проверка: same-size/backdated внешняя правка не позволяет выдать старый SHA/range как текущий.

### `ProjectIndexTests.test_root_nested_gitignore_and_policy_revoke_old_cache`

[Исходник](../../tests/test_project_index.py#L140)

```python
def test_root_nested_gitignore_and_policy_revoke_old_cache(self)
```

Проверка: nested .gitignore и .neutralignore инвалидируют cached source, explicit rebuild применяет новые правила.

### `ProjectIndexTests.test_exact_grant_revocation_is_checked_even_without_workspace_event`

[Исходник](../../tests/test_project_index.py#L149)

```python
def test_exact_grant_revocation_is_checked_even_without_workspace_event(self)
```

Проверка: внешнее profile grant/revoke повторно проверяется retrieval и не раскрывает бывший разрешённый .env.

### `ProjectIndexTests.test_ignored_parent_cannot_be_restored_by_child_negation`

[Исходник](../../tests/test_project_index.py#L158)

```python
def test_ignored_parent_cannot_be_restored_by_child_negation(self)
```

Проверка: правила Git не позволяют !child внутри целиком игнорируемого parent без разрешения parent.

### `ProjectIndexTests.test_parser_failure_and_non_utf8_leave_text_search_available`

[Исходник](../../tests/test_project_index.py#L164)

```python
def test_parser_failure_and_non_utf8_leave_text_search_available(self)
```

Проверка: parser dependency/syntax error не ломают text search; non-UTF8 binary не попадает в cache.

### `ProjectIndexTests.test_durable_queue_coalesces_and_restart_recovers_offline_edit`

[Исходник](../../tests/test_project_index.py#L175)

```python
def test_durable_queue_coalesces_and_restart_recovers_offline_edit(self)
```

Проверка: pending path coalesces, controlled startup rescan восстанавливает внешний offline edit.

### `ProjectIndexTests.test_overflow_cancel_and_explicit_rebuild_never_claim_ready`

[Исходник](../../tests/test_project_index.py#L182)

```python
def test_overflow_cancel_and_explicit_rebuild_never_claim_ready(self)
```

Проверка: неопределённость и cancel дают fallback/needs_rebuild, explicit rebuild возвращает готовый индекс.

### `ProjectIndexTests.test_corrupt_derived_cache_requires_explicit_rebuild`

[Исходник](../../tests/test_project_index.py#L188)

```python
def test_corrupt_derived_cache_requires_explicit_rebuild(self)
```

Проверка: повреждённый derived SQLite не сбрасывается молча; fallback работает, explicit rebuild сохраняет broken cache отдельно.

### `ProjectIndexTests.test_scoped_outline_and_cancellation_do_not_return_other_sources`

[Исходник](../../tests/test_project_index.py#L195)

```python
def test_scoped_outline_and_cancellation_do_not_return_other_sources(self)
```

Проверка: outline выбранного файла не раскрывает другие scopes, отменённый поиск возвращает SEARCH_CANCELLED.

<a id="module-tests-test-project-knowledge-py"></a>

## `tests/test_project_knowledge.py`

Проверки изоляции и свежести памяти, CAS, закрытия источников, транспортного retry и сохранения повреждённых данных.

### `ProjectKnowledgeTests`

[Исходник](../../tests/test_project_knowledge.py#L13)

```python
class ProjectKnowledgeTests(unittest.TestCase)
```

Изолированные negative gates памяти и реальная HTTP проверка invalidation при повторе.

### `ProjectKnowledgeTests.setUp`

[Исходник](../../tests/test_project_knowledge.py#L14)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ProjectKnowledgeTests.put`

[Исходник](../../tests/test_project_knowledge.py#L21)

```python
def put(self, **extra)
```

Создаёт короткую пользовательскую запись с источником main.py для независимых проверок.

### `ProjectKnowledgeTests.test_new_instance_finds_decision_and_timestamp_does_not_change_on_reads`

[Исходник](../../tests/test_project_knowledge.py#L24)

```python
def test_new_instance_finds_decision_and_timestamp_does_not_change_on_reads(self)
```

Проверка: Новый экземпляр находит решение по проекту, чтение сохраняет timestamps, другой root не видит запись.

### `ProjectKnowledgeTests.test_file_changes_deletion_and_revocation_remove_entire_model_note`

[Исходник](../../tests/test_project_knowledge.py#L30)

```python
def test_file_changes_deletion_and_revocation_remove_entire_model_note(self)
```

Проверка: Внешняя правка, удаление и запрет neutralignore убирают всю запись из model context.

### `ProjectKnowledgeTests.test_policy_change_invalidates_sourceless_decision_and_gitignore_source`

[Исходник](../../tests/test_project_knowledge.py#L38)

```python
def test_policy_change_invalidates_sourceless_decision_and_gitignore_source(self)
```

Проверка: Изменение политики закрывает даже заметку без источников; gitignore применяется к привязанному файлу.

### `ProjectKnowledgeTests.test_ui_cas_preserves_external_edits_and_rejects_root_switch`

[Исходник](../../tests/test_project_knowledge.py#L44)

```python
def test_ui_cas_preserves_external_edits_and_rejects_root_switch(self)
```

Проверка: UI CAS учитывает оба каталога памяти, отклоняет старый revision и смену проекта, user notes сверяют политику.

### `ProjectKnowledgeTests.test_model_proposal_cannot_promote_or_anchor_unread_sources`

[Исходник](../../tests/test_project_knowledge.py#L54)

```python
def test_model_proposal_cannot_promote_or_anchor_unread_sources(self)
```

Проверка: Модель не создаёт подтверждённый факт и не связывает вывод с непрочитанным источником; traversal запрещён.

### `ProjectKnowledgeTests.test_old_tool_memory_is_reprojected_after_revocation_without_changing_history`

[Исходник](../../tests/test_project_knowledge.py#L61)

```python
def test_old_tool_memory_is_reprojected_after_revocation_without_changing_history(self)
```

Проверка: Сохранённый tool answer не возвращает закрытую память в новый запрос; canonical transcript сохранён.

### `ProjectKnowledgeTests.test_legacy_and_model_notes_are_not_automatically_presented_as_current`

[Исходник](../../tests/test_project_knowledge.py#L70)

```python
def test_legacy_and_model_notes_are_not_automatically_presented_as_current(self)
```

Проверка: Старые и модельные summaries доступны в UI, но не подаются как актуальная справка.

### `ProjectKnowledgeTests.test_context_is_bounded_and_no_semantic_verification_is_invented`

[Исходник](../../tests/test_project_knowledge.py#L77)

```python
def test_context_is_bounded_and_no_semantic_verification_is_invented(self)
```

Проверка: Ранжированная проекция имеет ограниченный размер и не выдаёт хеш источника за доказательство вывода.

### `ProjectKnowledgeTests.test_fitted_memory_is_removed_after_change_and_metadata_never_reaches_api`

[Исходник](../../tests/test_project_knowledge.py#L84)

```python
def test_fitted_memory_is_removed_after_change_and_metadata_never_reaches_api(self)
```

Проверка: Смена source после fit исключает memory message; служебный маркер не передаётся в API.

### `ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post`

[Исходник](../../tests/test_project_knowledge.py#L95)

```python
def test_http_retry_rechecks_fitted_memory_before_second_post(self)
```

Проверка: Настоящий provider меняет файл между HTTP 500 и retry; второй POST не содержит закрытые данные.

### `ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler`

[Исходник](../../tests/test_project_knowledge.py#L101)

```python
class Handler(BaseHTTPRequestHandler)
```

Реальный localhost provider: меняет источник между первым HTTP 500 и повтором.

### `ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler.log_message`

[Исходник](../../tests/test_project_knowledge.py#L102)

```python
def log_message(self, *args)
```

Подавляет служебный access log fixture.

### `ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler.do_POST`

[Исходник](../../tests/test_project_knowledge.py#L103)

```python
def do_POST(self)
```

Сохраняет payload, изменяет файл и возвращает bounded retry либо terminal JSON.

### `ProjectKnowledgeTests.test_corrupt_record_catalog_is_reported_without_rewriting_it`

[Исходник](../../tests/test_project_knowledge.py#L117)

```python
def test_corrupt_record_catalog_is_reported_without_rewriting_it(self)
```

Проверка: Повреждённый provenance обнаруживается без перезаписи исходного файла.

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

<a id="module-tests-test-request-budget-py"></a>

## `tests/test_request_budget.py`

Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP.

### `definition`

[Исходник](../../tests/test_request_budget.py#L19)

```python
def definition(name='mcp_test', width=1)
```

Строит синтетическую JSON schema контролируемого размера для измерения overhead.

### `UsageHandler`

[Исходник](../../tests/test_request_budget.py#L24)

```python
class UsageHandler(BaseHTTPRequestHandler)
```

Тестовый класс/фикстура: Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP.

### `UsageHandler.log_message`

[Исходник](../../tests/test_request_budget.py#L25)

```python
def log_message(self, *_)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `UsageHandler.do_POST`

[Исходник](../../tests/test_request_budget.py#L27)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `RequestBudgetTests`

[Исходник](../../tests/test_request_budget.py#L43)

```python
class RequestBudgetTests(unittest.TestCase)
```

Тестовый класс/фикстура: Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP.

### `RequestBudgetTests.setUp`

[Исходник](../../tests/test_request_budget.py#L44)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `RequestBudgetTests.test_4k_8k_32k_windows_fit_complete_native_and_json_payloads`

[Исходник](../../tests/test_request_budget.py#L48)

```python
def test_4k_8k_32k_windows_fit_complete_native_and_json_payloads(self)
```

Проверка: полный native/JSON payload помещается в окна 4K/8K/32K после сжатия без изменения текущего запроса

### `RequestBudgetTests.test_subagent_tools_remain_discoverable_and_preferred_when_requested`

[Исходник](../../tests/test_request_budget.py#L64)

```python
def test_subagent_tools_remain_discoverable_and_preferred_when_requested(self)
```

Проверка: русский поиск находит субагентов; бюджет сохраняет предпочитаемые разрешённые схемы.

### `RequestBudgetTests.test_large_russian_current_request_is_rejected_without_clipping`

[Исходник](../../tests/test_request_budget.py#L78)

```python
def test_large_russian_current_request_is_rejected_without_clipping(self)
```

Проверка: длинный обязательный русский запрос сохраняется целиком и отклоняется до отправки

### `RequestBudgetTests.test_schemas_and_json_protocol_overhead_are_included`

[Исходник](../../tests/test_request_budget.py#L85)

```python
def test_schemas_and_json_protocol_overhead_are_included(self)
```

Проверка: слишком большие schemas не обходят бюджет ни через native tools, ни через JSON-инструкции

### `RequestBudgetTests.test_responses_encrypted_items_count_and_remain_intact`

[Исходник](../../tests/test_request_budget.py#L94)

```python
def test_responses_encrypted_items_count_and_remain_intact(self)
```

Проверка: encrypted reasoning включается в измерение, но не обрезается и не меняется

### `RequestBudgetTests.test_write_arguments_are_preserved_or_rejected`

[Исходник](../../tests/test_request_budget.py#L106)

```python
def test_write_arguments_are_preserved_or_rejected(self)
```

Проверка: полный код write_file нельзя незаметно сократить ради окна модели

### `RequestBudgetTests.test_result_reader_anchors_survive_two_compaction_passes`

[Исходник](../../tests/test_request_budget.py#L114)

```python
def test_result_reader_anchors_survive_two_compaction_passes(self)
```

Проверка: канонический якорь результата сохраняется после char- и token-проекций; приватный marker не уходит в HTTP

### `RequestBudgetTests.test_reader_checks_identity_and_reassembles_character_ranges`

[Исходник](../../tests/test_request_budget.py#L132)

```python
def test_reader_checks_identity_and_reassembles_character_ranges(self)
```

Проверка: диапазоны собирают исходный Unicode-текст, чужой индекс/ID не читается

### `RequestBudgetTests.test_deferred_tools_require_discovery_and_are_bounded`

[Исходник](../../tests/test_request_budget.py#L146)

```python
def test_deferred_tools_require_discovery_and_are_bounded(self)
```

Проверка: MCP недоступен policy до discovery; подключается ограниченный набор схем без их дублирования в результате поиска

### `RequestBudgetTests.test_mcp_only_profile_still_exposes_discovery_without_full_schemas`

[Исходник](../../tests/test_request_budget.py#L159)

```python
def test_mcp_only_profile_still_exposes_discovery_without_full_schemas(self)
```

Проверка: профиль с одними MCP и выключенными базовыми группами сохраняет доступ к discovery

### `RequestBudgetTests.test_memory_update_defaults_skip_read_only_tasks`

[Исходник](../../tests/test_request_budget.py#L172)

```python
def test_memory_update_defaults_skip_read_only_tasks(self)
```

Проверка: обычное чтение не вызывает обновление памяти; write/off/always переключают правило явно

### `RequestBudgetTests.test_legacy_large_reply_does_not_reset_endpoint_and_new_invalid_window_is_rejected`

[Исходник](../../tests/test_request_budget.py#L180)

```python
def test_legacy_large_reply_does_not_reset_endpoint_and_new_invalid_window_is_rejected(self)
```

Проверка: старые настройки большого ответа сохраняют URL/model, новые противоречивые лимиты отклоняются

### `BudgetTransportTests`

[Исходник](../../tests/test_request_budget.py#L187)

```python
class BudgetTransportTests(unittest.TestCase)
```

Тестовый класс/фикстура: Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP.

### `BudgetTransportTests.setUp`

[Исходник](../../tests/test_request_budget.py#L188)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `BudgetTransportTests.test_real_transport_rejects_oversized_schemas_before_http`

[Исходник](../../tests/test_request_budget.py#L194)

```python
def test_real_transport_rejects_oversized_schemas_before_http(self)
```

Проверка: настоящий ModelClient не отправляет HTTP при переполнении schemas

### `BudgetTransportTests.test_reported_stream_usage_is_counted_once_per_response`

[Исходник](../../tests/test_request_budget.py#L199)

```python
def test_reported_stream_usage_is_counted_once_per_response(self)
```

Проверка: несколько накопительных usage в одном SSE ответе учитываются один раз

### `BudgetTransportTests.test_optional_usage_rejection_falls_back_before_stream_only`

[Исходник](../../tests/test_request_budget.py#L205)

```python
def test_optional_usage_rejection_falls_back_before_stream_only(self)
```

Проверка: сервер без stream_options повторяется без telemetry только после отказа до начала потока

### `BudgetTransportTests.test_engine_budget_pause_preserves_request_and_sends_no_http`

[Исходник](../../tests/test_request_budget.py#L211)

```python
def test_engine_budget_pause_preserves_request_and_sends_no_http(self)
```

Проверка: Engine сохраняет большой исходный запрос и paused/blocked, не вызывая сервер

### `BudgetTransportTests.test_read_only_answer_skips_memory_request_and_exposes_reported_usage`

[Исходник](../../tests/test_request_budget.py#L220)

```python
def test_read_only_answer_skips_memory_request_and_exposes_reported_usage(self)
```

Проверка: реальный read-only ответ делает один запрос, сохраняет настоящий usage и пропускает лишнюю LLM-память

<a id="module-tests-test-response-quality-py"></a>

## `tests/test_response_quality.py`

Строгая оценка завершения, ограниченная доработка, восстановление пустого ответа и отсутствие лишней проверки информационных вопросов.

### `ResponseQualityTests`

[Исходник](../../tests/test_response_quality.py#L11)

```python
class ResponseQualityTests(unittest.TestCase)
```

Проверяет контракт ответа с настоящим engine loop и контролируемым provider fixture.

### `ResponseQualityTests.test_completion_assessment_rejects_truthy_strings_missing_and_ambiguous_json`

[Исходник](../../tests/test_response_quality.py#L14)

```python
def test_completion_assessment_rejects_truthy_strings_missing_and_ambiguous_json(self)
```

Проверка: complete принимает только boolean; неоднозначный JSON не превращается в положительную оценку.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success`

[Исходник](../../tests/test_response_quality.py#L20)

```python
def test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success(self)
```

Проверка: Три отрицательные оценки ограничивают доработку двумя циклами, затем paused вместо completed.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client`

[Исходник](../../tests/test_response_quality.py#L22)

```python
class Client
```

Возвращает видимый прогресс и отрицательную typed оценку, считает все обращения.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.__init__`

[Исходник](../../tests/test_response_quality.py#L23)

```python
def __init__(self, *args, **kwargs)
```

Не создаёт сетевой backend для unit fixture.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.create`

[Исходник](../../tests/test_response_quality.py#L24)

```python
def create(self, **kwargs)
```

Разделяет stream answer и nonstream assessment для проверки bounded recovery.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.close`

[Исходник](../../tests/test_response_quality.py#L28)

```python
def close(self)
```

Завершает пустой fixture client без сетевых ресурсов.

### `ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.cancel`

[Исходник](../../tests/test_response_quality.py#L29)

```python
def cancel(self)
```

Совместимый cancellation hook fixture без внешних эффектов.

### `ResponseQualityTests.test_informational_answer_has_no_verification_model_overhead`

[Исходник](../../tests/test_response_quality.py#L38)

```python
def test_informational_answer_has_no_verification_model_overhead(self)
```

Проверка: Информационный ответ не запускает отдельную model verification и остаётся нормальным completed.

### `ResponseQualityTests.test_empty_terminal_answer_gets_bounded_text_recovery`

[Исходник](../../tests/test_response_quality.py#L44)

```python
def test_empty_terminal_answer_gets_bounded_text_recovery(self)
```

Проверка: Пустой terminal response получает содержательный текст без фиктивного пустого completed.

### `ResponseQualityTests.test_explicit_source_location_format_repairs_without_replaying_tools`

[Исходник](../../tests/test_response_quality.py#L51)

```python
def test_explicit_source_location_format_repairs_without_replaying_tools(self)
```

Проверка: Неправильный формат получает одну текстовую доработку без повторных файловых операций.

### `ResponseQualityTests.test_format_guard_does_not_apply_to_freeform_questions`

[Исходник](../../tests/test_response_quality.py#L57)

```python
def test_format_guard_does_not_apply_to_freeform_questions(self)
```

Проверка: Проверка действует только на явный формат ответа; обычное обсуждение формата не ограничивается.

<a id="module-tests-test-responses-adapter-py"></a>

## `tests/test_responses_adapter.py`

Локальная HTTP/SSE фикстура OpenAI Responses: текст, функции, reasoning items, probe и retry.

### `ResponsesHandler`

[Исходник](../../tests/test_responses_adapter.py#L14)

```python
class ResponsesHandler(BaseHTTPRequestHandler)
```

HTTP/SSE фикстура Responses без платных API вызовов.

### `ResponsesHandler.log_message`

[Исходник](../../tests/test_responses_adapter.py#L15)

```python
def log_message(self, *_)
```

Отключает стандартный HTTP-log тестовой фикстуры.

### `ResponsesHandler.do_POST`

[Исходник](../../tests/test_responses_adapter.py#L17)

```python
def do_POST(self)
```

Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.

### `ResponsesHandler.do_POST.event`

[Исходник](../../tests/test_responses_adapter.py#L27)

```python
def event(data)
```

Читает события до нужного имени и немедленно проваливает тест при failed.

### `ResponsesAdapterTests`

[Исходник](../../tests/test_responses_adapter.py#L40)

```python
class ResponsesAdapterTests(unittest.TestCase)
```

Проверки канонической истории, потоковых functions, reasoning, probe и retry.

### `ResponsesAdapterTests.setUp`

[Исходник](../../tests/test_responses_adapter.py#L41)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ResponsesAdapterTests.test_streaming_tools_and_reasoning_are_carried_between_calls`

[Исходник](../../tests/test_responses_adapter.py#L48)

```python
def test_streaming_tools_and_reasoning_are_carried_between_calls(self)
```

Проверка: Responses functions собираются из delta, output и зашифрованный reasoning передаются в следующий turn.

### `ResponsesAdapterTests.test_nonstream_probe_uses_responses_and_retry_is_before_stream`

[Исходник](../../tests/test_responses_adapter.py#L64)

```python
def test_nonstream_probe_uses_responses_and_retry_is_before_stream(self)
```

Проверка: Временный 503 повторяется до потока, probe и нестриминговое завершение используют Responses.

### `ResponsesAdapterTests.test_transcript_conversion_does_not_send_unknown_chat_metadata`

[Исходник](../../tests/test_responses_adapter.py#L74)

```python
def test_transcript_conversion_does_not_send_unknown_chat_metadata(self)
```

Проверка: В API уходят только поля протокола, неизвестные локальные метаданные не передаются.

### `ResponsesAdapterTests.test_lola_uses_her_own_responses_protocol_and_tools`

[Исходник](../../tests/test_responses_adapter.py#L78)

```python
def test_lola_uses_her_own_responses_protocol_and_tools(self)
```

Проверка: Лола использует собственный Responses endpoint, вызывает калькулятор и сохраняет чистый ответ независимо от основной конфигурации.

<a id="module-tests-test-run-policy-py"></a>

## `tests/test_run_policy.py`

Explicit paid-budget estimates across children/resume and atomic journal-to-epoch tool accounting.

### `RunPolicyTests`

[Исходник](../../tests/test_run_policy.py#L9)

```python
class RunPolicyTests(unittest.TestCase)
```

Тестовый класс/фикстура: Explicit paid-budget estimates across children/resume and atomic journal-to-epoch tool accounting.

### `RunPolicyTests.setUp`

[Исходник](../../tests/test_run_policy.py#L10)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `RunPolicyTests.begin`

[Исходник](../../tests/test_run_policy.py#L14)

```python
def begin(self, **kwargs)
```

Создаёт synthetic external run с общим journal задачи и явно заданными тестовыми ценами.

### `RunPolicyTests.test_children_and_resume_share_reported_and_unknown_cost`

[Исходник](../../tests/test_run_policy.py#L17)

```python
def test_children_and_resume_share_reported_and_unknown_cost(self)
```

Проверка: Порог объединяет детей и resume; HTTP без usage сохраняет оценку, новый epoch не сбрасывает затраты задачи.

### `RunPolicyTests.test_cancel_before_http_releases_money_and_exact_usage_is_idempotent`

[Исходник](../../tests/test_run_policy.py#L28)

```python
def test_cancel_before_http_releases_money_and_exact_usage_is_idempotent(self)
```

Проверка: Отмена очереди снимает денежный резерв без расхода; повтор usage update не удваивает сумму.

### `RunPolicyTests.test_local_auto_ignores_paid_budget_and_unfinished_children_block_completion`

[Исходник](../../tests/test_run_policy.py#L37)

```python
def test_local_auto_ignores_paid_budget_and_unfinished_children_block_completion(self)
```

Проверка: Local auto не получает денежных caps; родитель не закрывается completed до закрытия детей, Stop каскадный.

### `RunPolicyTests.test_invalid_prices_and_capacity_error_classification`

[Исходник](../../tests/test_run_policy.py#L44)

```python
def test_invalid_prices_and_capacity_error_classification(self)
```

Проверка: Неверные цены/суммы отклоняются; OOM не смешивается с обычным HTTP 500.

### `RunPolicyTests.test_durable_receipt_and_epoch_tool_counter_commit_together`

[Исходник](../../tests/test_run_policy.py#L50)

```python
def test_durable_receipt_and_epoch_tool_counter_commit_together(self)
```

Проверка: Durable artifact-backed receipt и счётчик tools коммитятся одной транзакцией до следующего checkpoint, повтор не удваивается.

<a id="module-tests-test-run-registry-py"></a>

## `tests/test_run_registry.py`

Изолированные v2→v3, backup, orphan/live owner, cascade, model inheritance, FIFO и SDK stream-close проверки.

### `RunRegistryTests`

[Исходник](../../tests/test_run_registry.py#L17)

```python
class RunRegistryTests(unittest.TestCase)
```

Изолированная canonical DB и только синтетические модель/endpoint, без внешних HTTP вызовов.

### `RunRegistryTests.setUp`

[Исходник](../../tests/test_run_registry.py#L18)

```python
def setUp(self)
```

Создаёт временный профиль и Registry, cleanup не затрагивает пользовательскую SQLite.

### `RunRegistryTests.run_context`

[Исходник](../../tests/test_run_registry.py#L22)

```python
def run_context(self, **kwargs)
```

Создаёт host run на example.invalid без сетевого обращения для положительных/отрицательных сценариев.

### `RunRegistryTests.test_resume_epochs_are_independent_and_duplicate_ids_are_rejected`

[Исходник](../../tests/test_run_registry.py#L26)

```python
def test_resume_epochs_are_independent_and_duplicate_ids_are_rejected(self)
```

Проверка: Повтор имеет новый run ID при прежнем journal; использованный ID нельзя повторно исполнить.

### `RunRegistryTests.test_child_inheritance_bounds_and_cascade_cancel`

[Исходник](../../tests/test_run_registry.py#L34)

```python
def test_child_inheritance_bounds_and_cascade_cancel(self)
```

Проверка: Дети наследуют модель/подключение, depth/fan-out ограничены и cancel распространяется по дереву.

### `RunRegistryTests.test_ledger_idempotent_usage_and_reservations_are_not_charges`

[Исходник](../../tests/test_run_registry.py#L44)

```python
def test_ledger_idempotent_usage_and_reservations_are_not_charges(self)
```

Проверка: Reservation не считается HTTP/стоимостью, cumulative usage добавляется один раз даже при повторной terminal записи.

### `RunRegistryTests.test_orphan_recovery_releases_estimates_and_never_replays_http`

[Исходник](../../tests/test_run_registry.py#L51)

```python
def test_orphan_recovery_releases_estimates_and_never_replays_http(self)
```

Проверка: Restart отмечает orphan run paused, снимает резерв, сохраняет unknown usage и не запускает HTTP.

### `RunRegistryTests.test_live_owner_is_preserved_and_pid_check_does_not_signal_it`

[Исходник](../../tests/test_run_registry.py#L64)

```python
def test_live_owner_is_preserved_and_pid_check_does_not_signal_it(self)
```

Проверка: Проверка текущего PID безопасна, live owner не объявляется прерванным другим Registry.

### `RunRegistryTests.test_approval_time_is_separate_from_elapsed_and_model_queue`

[Исходник](../../tests/test_run_registry.py#L69)

```python
def test_approval_time_is_separate_from_elapsed_and_model_queue(self)
```

Проверка: Время подтверждения отдельно от model queue, elapsed и счётчика инструментов.

### `RunRegistryTests.test_schema_two_upgrade_preserves_existing_task_and_backup_contains_runs`

[Исходник](../../tests/test_run_registry.py#L76)

```python
def test_schema_two_upgrade_preserves_existing_task_and_backup_contains_runs(self)
```

Проверка: Миграция v2→v3 сохраняет checkpoint и восстановленный ZIP содержит run telemetry.

### `RunRegistryTests.test_delete_chat_also_deletes_its_run_metadata`

[Исходник](../../tests/test_run_registry.py#L92)

```python
def test_delete_chat_also_deletes_its_run_metadata(self)
```

Проверка: Удаление чата стирает связанные run/attempt metadata без остаточного history.

### `RunRegistryTests.test_model_binding_rejects_child_or_parent_configuration_drift`

[Исходник](../../tests/test_run_registry.py#L99)

```python
def test_model_binding_rejects_child_or_parent_configuration_drift(self)
```

Проверка: Смена модели в текущем run отклоняется до HTTP, не загружая новую модель.

### `SchedulerTests`

[Исходник](../../tests/test_run_registry.py#L105)

```python
class SchedulerTests(unittest.IsolatedAsyncioTestCase)
```

Async проверки FIFO/cleanup/cancel и освобождения ресурса перед ожиданием дочернего run.

### `SchedulerTests.test_fifo_waiter_cancel_and_stale_release`

[Исходник](../../tests/test_run_registry.py#L106)

```python
async def test_fifo_waiter_cancel_and_stale_release(self)
```

Проверка: FIFO сохраняет порядок после отмены waiter; старый owner не освобождает нового.

### `SchedulerTests.test_parent_waits_for_child_without_holding_generation_lease`

[Исходник](../../tests/test_run_registry.py#L118)

```python
async def test_parent_waits_for_child_without_holding_generation_lease(self)
```

Проверка: Ресурс parent отпускается перед child, после завершения parent может снова получить очередь без deadlock.

### `SchedulerTests.test_stream_close_holds_lease_until_sdk_cleanup_finishes`

[Исходник](../../tests/test_run_registry.py#L124)

```python
async def test_stream_close_holds_lease_until_sdk_cleanup_finishes(self)
```

Проверка: Двойной Stop не освобождает lease посреди SDK close; следующий запрос ждёт реального cleanup.

### `SchedulerTests.test_stream_close_holds_lease_until_sdk_cleanup_finishes.Response`

[Исходник](../../tests/test_run_registry.py#L127)

```python
class Response
```

SDK fixture с явно задержанным close для проверки повторного Stop.

### `SchedulerTests.test_stream_close_holds_lease_until_sdk_cleanup_finishes.Response.close`

[Исходник](../../tests/test_run_registry.py#L128)

```python
async def close(self)
```

Сообщает о начале cleanup и ждёт отдельного разрешения теста, не обращаясь к сети.

### `SchedulerTests.test_cancelled_queued_reservation_has_no_http_or_token_charge`

[Исходник](../../tests/test_run_registry.py#L135)

```python
async def test_cancelled_queued_reservation_has_no_http_or_token_charge(self)
```

Проверка: Отменённый waiter снимает резерв, не делает HTTP и не нарушает текущий lease.

### `SchedulerTests.test_failed_close_blocks_reuse_until_owning_client_cleanup`

[Исходник](../../tests/test_run_registry.py#L145)

```python
async def test_failed_close_blocks_reuse_until_owning_client_cleanup(self)
```

Проверка: Ошибка SDK close не разрешает следующую генерацию; ошибка объяснима, очередь не зависает, owner cleanup снимает карантин.

### `SchedulerTests.test_failed_close_blocks_reuse_until_owning_client_cleanup.Response`

[Исходник](../../tests/test_run_registry.py#L147)

```python
class Response
```

SDK fixture с ошибкой close для проверки карантина ресурса.

### `SchedulerTests.test_failed_close_blocks_reuse_until_owning_client_cleanup.Response.close`

[Исходник](../../tests/test_run_registry.py#L148)

```python
async def close(self)
```

Детерминированно поднимает OSError cleanup, не обращаясь к реальным сокетам.

<a id="module-tests-test-run-state-py"></a>

## `tests/test_run_state.py`

Контракты переходов между выполнением, подтверждением, проверкой и терминальными состояниями.

### `RunStateTests`

[Исходник](../../tests/test_run_state.py#L7)

```python
class RunStateTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты переходов между выполнением, подтверждением, проверкой и терминальными состояниями.

### `RunStateTests.test_approval_execution_verification_and_completion_share_legacy_status`

[Исходник](../../tests/test_run_state.py#L8)

```python
def test_approval_execution_verification_and_completion_share_legacy_status(self)
```

Проверка: фазы lifecycle согласованы с legacy status и не меняют содержательные этапы

### `RunStateTests.test_unknown_effect_pause_and_failure_can_resume_with_reason_cleared`

[Исходник](../../tests/test_run_state.py#L26)

```python
def test_unknown_effect_pause_and_failure_can_resume_with_reason_cleared(self)
```

Проверка: остановленные задачи возобновляются с очисткой прежней причины

### `RunStateTests.test_recovery_can_reclassify_stopped_run_without_executing_it`

[Исходник](../../tests/test_run_state.py#L42)

```python
def test_recovery_can_reclassify_stopped_run_without_executing_it(self)
```

Проверка: восстановление может уточнить остановку, не запуская модель или инструмент

### `RunStateTests.test_completed_run_cannot_reopen_or_change_terminal_outcome`

[Исходник](../../tests/test_run_state.py#L54)

```python
def test_completed_run_cannot_reopen_or_change_terminal_outcome(self)
```

Проверка: завершённую эпоху нельзя открыть повторно или заменить её исход

### `RunStateTests.test_finishing_without_tools_and_during_execution_is_permitted`

[Исходник](../../tests/test_run_state.py#L65)

```python
def test_finishing_without_tools_and_during_execution_is_permitted(self)
```

Проверка: обычный ответ и окончание tool-цикла допускают завершение

### `RunStateTests.test_approval_wait_cannot_be_marked_completed`

[Исходник](../../tests/test_run_state.py#L73)

```python
def test_approval_wait_cannot_be_marked_completed(self)
```

Проверка: ожидание нерешённого согласия не считается завершением

### `RunStateTests.test_legacy_tasks_migrate_without_losing_event_or_plan`

[Исходник](../../tests/test_run_state.py#L84)

```python
def test_legacy_tasks_migrate_without_losing_event_or_plan(self)
```

Проверка: legacy status преобразуется без потери last_event и плана

### `RunStateTests.test_unrecognized_legacy_status_requires_attention`

[Исходник](../../tests/test_run_state.py#L96)

```python
def test_unrecognized_legacy_status_requires_attention(self)
```

Проверка: неизвестный прежний status требует проверки

### `RunStateTests.test_existing_run_phase_takes_precedence_and_is_shared`

[Исходник](../../tests/test_run_state.py#L101)

```python
def test_existing_run_phase_takes_precedence_and_is_shared(self)
```

Проверка: два контроллера видят одну фазу task

### `RunStateTests.test_repeated_transition_preserves_event_and_reason`

[Исходник](../../tests/test_run_state.py#L111)

```python
def test_repeated_transition_preserves_event_and_reason(self)
```

Проверка: повтор фазы без новой причины не стирает сведения

### `RunStateTests.test_unknown_phase_is_rejected_without_changing_task`

[Исходник](../../tests/test_run_state.py#L122)

```python
def test_unknown_phase_is_rejected_without_changing_task(self)
```

Проверка: неизвестная фаза отклоняется до мутации задачи

### `RunStateTests.test_optional_task_obeys_same_transitions`

[Исходник](../../tests/test_run_state.py#L135)

```python
def test_optional_task_obeys_same_transitions(self)
```

Проверка: запуск без persistence соблюдает ту же матрицу

### `RunStateTests.test_reasons_are_bounded_and_nonempty_for_failures`

[Исходник](../../tests/test_run_state.py#L146)

```python
def test_reasons_are_bounded_and_nonempty_for_failures(self)
```

Проверка: причины ошибок ограничены и не теряются

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

<a id="module-tests-test-scoped-verification-py"></a>

## `tests/test_scoped_verification.py`

Реальные команды и scoped receipts: большой проект, зависимости/доступ/rollback, смена root, legacy migration и restart без повторного эффекта.

### `ScopedVerificationTests`

[Исходник](../../tests/test_scoped_verification.py#L23)

```python
class ScopedVerificationTests(unittest.TestCase)
```

Тестовый класс/фикстура: Реальные команды и scoped receipts: большой проект, зависимости/доступ/rollback, смена root, legacy migration и restart без повторного эффекта.

### `ScopedVerificationTests.setUp`

[Исходник](../../tests/test_scoped_verification.py#L25)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ScopedVerificationTests.install`

[Исходник](../../tests/test_scoped_verification.py#L37)

```python
def install(self)
```

Устанавливает пользовательскую команду, scope и связанный критерий.

### `ScopedVerificationTests.run_check`

[Исходник](../../tests/test_scoped_verification.py#L41)

```python
def run_check(self, arguments=None, handler=None)
```

Проводит реальный процесс через journal, executor, approval и StageVerifier.

### `ScopedVerificationTests.run_check.approve`

[Исходник](../../tests/test_scoped_verification.py#L45)

```python
def approve(*_args)
```

Подтверждает внешнее действие в обычных границах executor и сохраняет текст области.

### `ScopedVerificationTests.run_check.dispatch`

[Исходник](../../tests/test_scoped_verification.py#L47)

```python
def dispatch(_name, values)
```

Вызывает run_project_command либо локальный handler теста.

### `ScopedVerificationTests.test_large_unrelated_file_does_not_block_explicit_scope`

[Исходник](../../tests/test_scoped_verification.py#L57)

```python
def test_large_unrelated_file_does_not_block_explicit_scope(self)
```

Проверка: exit=0 на выбранных файлах даёт scoped_passed без полного обхода и без project_complete.

### `ScopedVerificationTests.test_default_workspace_remains_unverified_when_tree_is_incomplete`

[Исходник](../../tests/test_scoped_verification.py#L68)

```python
def test_default_workspace_remains_unverified_when_tree_is_incomplete(self)
```

Проверка: успех произвольной команды не повышает неполный fingerprint большого дерева до подтверждённой проверки.

### `ScopedVerificationTests.test_dependency_change_invalidates_but_unrelated_edit_does_not`

[Исходник](../../tests/test_scoped_verification.py#L77)

```python
def test_dependency_change_invalidates_but_unrelated_edit_does_not(self)
```

Проверка: backdated изменение зависимости инвалидирует witness; посторонняя правка и generation не отравляют file scope.

### `ScopedVerificationTests.test_command_mutation_cannot_certify_post_execution_snapshot`

[Исходник](../../tests/test_scoped_verification.py#L86)

```python
def test_command_mutation_cannot_certify_post_execution_snapshot(self)
```

Проверка: успешная команда, изменившая покрываемый файл между before/after, не подтверждает стабильный tested snapshot.

### `ScopedVerificationTests.test_nonzero_command_is_a_failed_criterion_not_just_stale`

[Исходник](../../tests/test_scoped_verification.py#L93)

```python
def test_nonzero_command_is_a_failed_criterion_not_just_stale(self)
```

Проверка: связанный критерий показывает неуспешную команду как failed отдельно от актуальности исходников.

### `ScopedVerificationTests.test_check_config_and_rollback_invalidate_receipt`

[Исходник](../../tests/test_scoped_verification.py#L99)

```python
def test_check_config_and_rollback_invalidate_receipt(self)
```

Проверка: смена списка зависимостей или rollback revision не позволяет принять старую квитанцию.

### `ScopedVerificationTests.test_policy_revocation_and_missing_dependency_block_cached_evidence`

[Исходник](../../tests/test_scoped_verification.py#L107)

```python
def test_policy_revocation_and_missing_dependency_block_cached_evidence(self)
```

Проверка: новая .neutralignore или удаление зависимости запрещают использовать прежний witness.

### `ScopedVerificationTests.test_models_cannot_choose_scope_or_reuse_another_command`

[Исходник](../../tests/test_scoped_verification.py#L114)

```python
def test_models_cannot_choose_scope_or_reuse_another_command(self)
```

Проверка: модель не передаёт scope tool-аргументом; только точный пользовательский command/check_id/timeout наследует область.

### `ScopedVerificationTests.test_scope_validation_rejects_globs_escape_and_ambiguous_paths`

[Исходник](../../tests/test_scoped_verification.py#L123)

```python
def test_scope_validation_rejects_globs_escape_and_ambiguous_paths(self)
```

Проверка: scope состоит из точных относительных файлов, без glob, traversal, ADS и двусмысленных разделителей.

### `ScopedVerificationTests.test_receipt_cannot_be_transplanted_to_another_workspace`

[Исходник](../../tests/test_scoped_verification.py#L129)

```python
def test_receipt_cannot_be_transplanted_to_another_workspace(self)
```

Проверка: одинаковые байты в другом canonical workspace не принимаются как тот же снимок.

### `ScopedVerificationTests.test_malformed_or_incomplete_witness_is_never_success`

[Исходник](../../tests/test_scoped_verification.py#L136)

```python
def test_malformed_or_incomplete_witness_is_never_success(self)
```

Проверка: exit=0 не компенсирует отсутствие, неполноту или повреждённую структуру witness.

### `ScopedVerificationTests.test_legacy_checkpoint_is_unverified_without_losing_exit_or_history`

[Исходник](../../tests/test_scoped_verification.py#L146)

```python
def test_legacy_checkpoint_is_unverified_without_losing_exit_or_history(self)
```

Проверка: v1 fingerprint не восстанавливает commands_passed при загрузке; exit code сохраняется.

### `ScopedVerificationTests.test_receipt_survives_restart_without_reexecuting_command`

[Исходник](../../tests/test_scoped_verification.py#L156)

```python
def test_receipt_survives_restart_without_reexecuting_command(self)
```

Проверка: restart восстанавливает v2 receipt из журнала и сверяет scope без нового Popen.

<a id="module-tests-test-services-and-sessions-py"></a>

## `tests/test_services_and_sessions.py`

7 новых контрактов deadline/gate/protocol/profile и настоящего reuse/invalidate/cancel MCP stdio.

### `ServiceBoundaryTests`

[Исходник](../../tests/test_services_and_sessions.py#L20)

```python
class ServiceBoundaryTests(unittest.TestCase)
```

Изолированные проверки границ сервисов без внешних учётных записей и моделей.

### `ServiceBoundaryTests.setUp`

[Исходник](../../tests/test_services_and_sessions.py#L21)

```python
def setUp(self)
```

Изолирует профиль долговечного run telemetry, включая замоканный probe, от пользовательского AppData.

### `ServiceBoundaryTests.test_child_deadline_is_bounded_and_parent_cancel_is_immediate`

[Исходник](../../tests/test_services_and_sessions.py#L27)

```python
def test_child_deadline_is_bounded_and_parent_cancel_is_immediate(self)
```

Проверка: child соблюдает срок и отмену родителя, не продлевает время операции.

### `ServiceBoundaryTests.test_stale_gate_owner_cannot_release_a_new_inference`

[Исходник](../../tests/test_services_and_sessions.py#L34)

```python
def test_stale_gate_owner_cannot_release_a_new_inference(self)
```

Проверка: конкурирующая inference отклоняется, старый lease не освобождает новый.

### `ServiceBoundaryTests.test_approval_wait_freezes_nested_deadlines_but_not_cancellation`

[Исходник](../../tests/test_services_and_sessions.py#L41)

```python
def test_approval_wait_freezes_nested_deadlines_but_not_cancellation(self)
```

Проверка: человеческое ожидание не расходует deadline родителя/ребёнка; Stop распространяется сразу.

### `ServiceBoundaryTests.test_approval_exception_restores_deadline_once`

[Исходник](../../tests/test_services_and_sessions.py#L61)

```python
def test_approval_exception_restores_deadline_once(self)
```

Проверка: исключение во вложенном approval снимает паузу и сдвигает deadline ровно один раз.

### `ServiceBoundaryTests.test_protocol_rejects_wrong_version_ids_and_non_boolean_approval`

[Исходник](../../tests/test_services_and_sessions.py#L73)

```python
def test_protocol_rejects_wrong_version_ids_and_non_boolean_approval(self)
```

Проверка: несовместимая версия, неверный run_id и строковое confirmed не проходят dispatch.

### `ServiceBoundaryTests.test_mode_profiles_cannot_enable_project_tools_in_chat_or_voice`

[Исходник](../../tests/test_services_and_sessions.py#L79)

```python
def test_mode_profiles_cannot_enable_project_tools_in_chat_or_voice(self)
```

Проверка: профиль режима ограничивает группы даже при переданном root.

### `ServiceBoundaryTests.test_probe_and_task_share_one_heavy_inference_gate`

[Исходник](../../tests/test_services_and_sessions.py#L85)

```python
def test_probe_and_task_share_one_heavy_inference_gate(self)
```

Проверка: реальный TaskService не запускает задачу одновременно с probe и освобождает gate после отмены.

### `ServiceBoundaryTests.test_probe_and_task_share_one_heavy_inference_gate.probe`

[Исходник](../../tests/test_services_and_sessions.py#L87)

```python
def probe(*args, cancelled=None, **kwargs)
```

Держит fixture probe до отмены, чтобы проверить отказ конкурирующей задачи.

### `ServiceBoundaryTests.test_mcp_reuses_process_and_invalidates_without_replaying_calls`

[Исходник](../../tests/test_services_and_sessions.py#L99)

```python
def test_mcp_reuses_process_and_invalidates_without_replaying_calls(self)
```

Проверка: два реальных вызова используют PID одного MCP process; label/catalog не меняют transport identity, invalidate создаёт новый PID.

### `ServiceBoundaryTests.test_mcp_cancellation_during_connect_is_prompt`

[Исходник](../../tests/test_services_and_sessions.py#L117)

```python
def test_mcp_cancellation_during_connect_is_prompt(self)
```

Проверка: отмена на connect возвращается быстро и закрывает actor, tool эффект не повторяется.

### `ServiceBoundaryTests.test_mcp_cancellation_during_connect_is_prompt.connect`

[Исходник](../../tests/test_services_and_sessions.py#L121)

```python
@asynccontextmanager
async def connect(*args)
```

Асинхронный connect fixture без побочных эффектов, намеренно задержанный для отмены.

### `ServiceBoundaryTests.test_mcp_cancellation_during_connect_is_prompt.exchange`

[Исходник](../../tests/test_services_and_sessions.py#L124)

```python
async def exchange(*args)
```

Безопасный ответ fixture; до него отменённое подключение не должно дойти.

<a id="module-tests-test-smart-context-py"></a>

## `tests/test_smart_context.py`

Проверки архива, неизменности истории, пар tools, полного кода, JSON и дедупликации.

### `SmartContextTests`

[Исходник](../../tests/test_smart_context.py#L7)

```python
class SmartContextTests(unittest.TestCase)
```

Тестовый класс/фикстура: Проверки архива, неизменности истории, пар tools, полного кода, JSON и дедупликации.

### `SmartContextTests.test_archive_uses_serialized_message_size`

[Исходник](../../tests/test_smart_context.py#L8)

```python
def test_archive_uses_serialized_message_size(self)
```

Проверка: архив учитывает JSON escaping и помещается в окно, сохраняя исходную историю и актуальный SHA256.

### `SmartContextTests.test_graph_receipt_reference_survives_compaction`

[Исходник](../../tests/test_smart_context.py#L22)

```python
def test_graph_receipt_reference_survives_compaction(self)
```

Проверка: Сжатие крупного tool output сохраняет точный assistant-batch receipt anchor для TaskGraph evidence.

### `SmartContextTests.test_old_design_constraint_survives_long_history`

[Исходник](../../tests/test_smart_context.py#L29)

```python
def test_old_design_constraint_survives_long_history(self)
```

Проверка: Сжатие сохраняет старое ограничение дизайна и последний запрос, не меняя канонический список.

### `SmartContextTests.test_tool_pairs_and_write_arguments_are_never_cut`

[Исходник](../../tests/test_smart_context.py#L37)

```python
def test_tool_pairs_and_write_arguments_are_never_cut(self)
```

Проверка: Полные аргументы записи и связанный tool_call_id сохраняются вместе.

### `SmartContextTests.test_current_code_handoff_is_protected_or_rejected`

[Исходник](../../tests/test_smart_context.py#L45)

```python
def test_current_code_handoff_is_protected_or_rejected(self)
```

Проверка: Текущий код передаётся полностью либо выдаётся ошибка бюджета без обрезки.

### `SmartContextTests.test_large_tool_json_keeps_error_path_and_valid_json`

[Исходник](../../tests/test_smart_context.py#L51)

```python
def test_large_tool_json_keeps_error_path_and_valid_json(self)
```

Проверка: Сокращённый результат чтения остаётся JSON с путём, fingerprint и релевантным фрагментом.

### `SmartContextTests.test_command_compaction_keeps_exit_code_and_failure_evidence`

[Исходник](../../tests/test_smart_context.py#L57)

```python
def test_command_compaction_keeps_exit_code_and_failure_evidence(self)
```

Проверка: сжатие команды сохраняет exit code и фрагменты stdout/stderr с причиной провала

### `SmartContextTests.test_mcp_compaction_keeps_text_blocks_and_excludes_binary_content`

[Исходник](../../tests/test_smart_context.py#L67)

```python
def test_mcp_compaction_keeps_text_blocks_and_excludes_binary_content(self)
```

Проверка: сжатие MCP сохраняет значимые текстовые блоки и исключает бинарные данные

### `SmartContextTests.test_single_line_output_keeps_diagnostic_beyond_prefix`

[Исходник](../../tests/test_smart_context.py#L80)

```python
def test_single_line_output_keeps_diagnostic_beyond_prefix(self)
```

Проверка: ошибка в конце длинной строки не теряется при выборе диагностического фрагмента

### `SmartContextTests.test_compacted_json_honors_escaping_budget_and_outcome_metadata`

[Исходник](../../tests/test_smart_context.py#L85)

```python
def test_compacted_json_honors_escaping_budget_and_outcome_metadata(self)
```

Проверка: фактический JSON-size после escaping укладывается в бюджет и сохраняет outcome

### `SmartContextTests.test_compaction_preserves_note_privacy_and_canonical_result_reference`

[Исходник](../../tests/test_smart_context.py#L94)

```python
def test_compaction_preserves_note_privacy_and_canonical_result_reference(self)
```

Проверка: сжатие заметок сохраняет приватность и ссылку на канонический tool call

### `SmartContextTests.test_archived_command_keeps_failure_summary_and_call_reference`

[Исходник](../../tests/test_smart_context.py#L108)

```python
def test_archived_command_keeps_failure_summary_and_call_reference(self)
```

Проверка: архив истории содержит краткую ошибку команды, код выхода и call ID

### `SmartContextTests.test_archive_never_becomes_system_permissions`

[Исходник](../../tests/test_smart_context.py#L118)

```python
def test_archive_never_becomes_system_permissions(self)
```

Проверка: Старый текст остаётся данными assistant и не добавляет системных разрешений.

### `SmartContextTests.test_repeated_tool_facts_are_deduplicated_and_history_unchanged`

[Исходник](../../tests/test_smart_context.py#L125)

```python
def test_repeated_tool_facts_are_deduplicated_and_history_unchanged(self)
```

Проверка: Архив оставляет последний факт по пути без изменения полной истории.

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

<a id="module-tests-test-stage17-verification-py"></a>

## `tests/test_stage17_verification.py`

Gate этапа 17: выбор проверок, настоящие LSP процессы, изоляция Git, CRLF и внешняя правка во время rollback.

### `Stage17Tests`

[Исходник](../../tests/test_stage17_verification.py#L22)

```python
class Stage17Tests(unittest.TestCase)
```

Изолированные regression gates выбора проверок, LSP и Git/checkpoint recovery.

### `Stage17Tests.lsp_task`

[Исходник](../../tests/test_stage17_verification.py#L27)

```python
def lsp_task(self, *flags)
```

Формирует user-defined scoped LSP check и выполняет настоящий stdio fixture сервер.

### `Stage17Tests.test_full_lsp_clean_is_scoped_and_file_or_server_change_invalidates`

[Исходник](../../tests/test_stage17_verification.py#L37)

```python
def test_full_lsp_clean_is_scoped_and_file_or_server_change_invalidates(self)
```

Проверка: Полный чистый pull подтверждает только файл, изменение файла или конфигурации делает результат stale.

### `Stage17Tests.test_lsp_errors_and_incomplete_push_never_pass`

[Исходник](../../tests/test_stage17_verification.py#L46)

```python
def test_lsp_errors_and_incomplete_push_never_pass(self)
```

Проверка: Ошибки LSP и неполный push не позволяют объявить проверку успешной.

### `Stage17Tests.test_user_selectors_skip_unrelated_checks_but_not_acceptance_requirements`

[Исходник](../../tests/test_stage17_verification.py#L55)

```python
def test_user_selectors_skip_unrelated_checks_but_not_acceptance_requirements(self)
```

Проверка: applies_to пропускает только нерелевантные проверки; критерий и ручной checks-only сохраняют обязательность.

### `Stage17Tests.test_git_snapshot_uses_confirmed_bytes_and_never_changes_project_index_or_head`

[Исходник](../../tests/test_stage17_verification.py#L65)

```python
def test_git_snapshot_uses_confirmed_bytes_and_never_changes_project_index_or_head(self)
```

Проверка: Private Git возвращает точные before/after bytes, включая CRLF, и сохраняет HEAD/index проекта.

### `Stage17Tests.test_external_edit_during_multi_file_rollback_is_preserved_and_requires_review`

[Исходник](../../tests/test_stage17_verification.py#L81)

```python
def test_external_edit_during_multi_file_rollback_is_preserved_and_requires_review(self)
```

Проверка: Внешний edit между восстановлением двух файлов не перезаписывается, результат rollback_unknown требует ручной проверки.

### `Stage17Tests.test_external_edit_during_multi_file_rollback_is_preserved_and_requires_review.restore`

[Исходник](../../tests/test_stage17_verification.py#L85)

```python
def restore(path, saved, expected)
```

Вставляет внешнюю правку второго файла после восстановления первого, проверяя конфликтный контракт.

### `Stage17Tests.test_command_receipt_cannot_impersonate_lsp_check`

[Исходник](../../tests/test_stage17_verification.py#L94)

```python
def test_command_receipt_cannot_impersonate_lsp_check(self)
```

Проверка: Обычная команда не наследует LSP check_id/evidence; некорректная severity не превращается в отсутствие ошибок.

### `Stage17Tests.test_revoked_lsp_source_is_hidden_from_future_model_history`

[Исходник](../../tests/test_stage17_verification.py#L103)

```python
def test_revoked_lsp_source_is_hidden_from_future_model_history(self)
```

Проверка: Отзыв доступа удаляет LSP diagnostics из model projection, не меняя canonical history.

<a id="module-tests-test-stage9-reliability-py"></a>

## `tests/test_stage9_reliability.py`

Регрессии аудита A1–A5: JSON/EOF/revision/access/LSP и живой JSON-lines bridge во время backup.

### `Stage9Tests`

[Исходник](../../tests/test_stage9_reliability.py#L29)

```python
class Stage9Tests(unittest.TestCase)
```

Тестовый класс/фикстура: Регрессии аудита A1–A5: JSON/EOF/revision/access/LSP и живой JSON-lines bridge во время backup.

### `Stage9Tests.setUp`

[Исходник](../../tests/test_stage9_reliability.py#L31)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `Stage9Tests.test_json_rejects_suffix_second_object_duplicate_keys_and_nan`

[Исходник](../../tests/test_stage9_reliability.py#L38)

```python
def test_json_rejects_suffix_second_object_duplicate_keys_and_nan(self)
```

Проверка: хвост, второй объект, повторные ключи и NaN не превращаются в команды; anchored compatibility wrapper остаётся.

### `Stage9Tests.test_versioned_json_and_incomplete_stream_share_terminal_contract`

[Исходник](../../tests/test_stage9_reliability.py#L46)

```python
def test_versioned_json_and_incomplete_stream_share_terminal_contract(self)
```

Проверка: v1 action/final корректны; EOF JSON не синтезирует успешный tool_calls.

### `Stage9Tests.test_editor_and_external_changes_invalidate_content_evidence`

[Исходник](../../tests/test_stage9_reliability.py#L57)

```python
def test_editor_and_external_changes_invalidate_content_evidence(self)
```

Проверка: ручной EditorService save и same-size запись с восстановленным mtime инвалидируют checks.

### `Stage9Tests.test_legacy_and_over_budget_revisions_cannot_certify_checks`

[Исходник](../../tests/test_stage9_reliability.py#L72)

```python
def test_legacy_and_over_budget_revisions_cannot_certify_checks(self)
```

Проверка: старые receipts без content hash и превышенный бюджет fingerprint не получают зелёный статус.

### `Stage9Tests.test_shared_access_policy_requires_exact_user_exception`

[Исходник](../../tests/test_stage9_reliability.py#L79)

```python
def test_shared_access_policy_requires_exact_user_exception(self)
```

Проверка: read/range/search/list используют общую политику; ручной editor доступен; точечный grant/revoke требует UI consent.

### `Stage9Tests.test_delayed_lsp_replaces_initial_empty_and_pull_is_preferred`

[Исходник](../../tests/test_stage9_reliability.py#L98)

```python
def test_delayed_lsp_replaces_initial_empty_and_pull_is_preferred(self)
```

Проверка: реальный subprocess выдаёт пустой push и позднюю ошибку; pull даёт явный полный отчёт.

### `Stage9Tests.test_policy_metadata_cannot_be_granted_or_changed_as_a_project_file`

[Исходник](../../tests/test_stage9_reliability.py#L107)

```python
def test_policy_metadata_cannot_be_granted_or_changed_as_a_project_file(self)
```

Проверка: модель не может получить grant на собственный файл разрешений даже при выборе профиля как проекта.

### `Stage9Tests.test_revocation_filters_known_saved_results_without_deleting_chat`

[Исходник](../../tests/test_stage9_reliability.py#L114)

```python
def test_revocation_filters_known_saved_results_without_deleting_chat(self)
```

Проверка: отзыв доступа скрывает содержимое и read_tool_result-копию в новых запросах, сохраняя пользовательскую историю.

### `Stage9Tests.test_background_job_cancel_and_duplicate_are_bounded`

[Исходник](../../tests/test_stage9_reliability.py#L129)

```python
def test_background_job_cancel_and_duplicate_are_bounded(self)
```

Проверка: один worker, отказ дублю и коррелированная отмена без преждевременного освобождения слота.

### `Stage9Tests.test_background_job_cancel_and_duplicate_are_bounded.work`

[Исходник](../../tests/test_stage9_reliability.py#L132)

```python
def work(context)
```

Fixture ожидает отмену OperationContext и не блокирует вызывающий поток.

### `Stage9Tests.test_background_job_cancel_and_duplicate_are_bounded.respond`

[Исходник](../../tests/test_stage9_reliability.py#L135)

```python
def respond(value)
```

Сохраняет ответ worker и завершает ожидание теста.

### `Stage9Tests.test_cancelled_backup_preserves_existing_destination`

[Исходник](../../tests/test_stage9_reliability.py#L142)

```python
def test_cancelled_backup_preserves_existing_destination(self)
```

Проверка: отмена не заменяет имеющийся архив пользователя.

### `Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace`

[Исходник](../../tests/test_stage9_reliability.py#L150)

```python
def test_backup_commit_is_not_relabelled_cancelled_after_replace(self)
```

Проверка: реальный ZIP сохранён атомарно; отмена сразу после replace не скрывает уже совершённый commit.

### `Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.commit`

[Исходник](../../tests/test_stage9_reliability.py#L155)

```python
def commit(source, destination)
```

После настоящего os.replace сигнализирует позднюю отмену для проверки границы commit.

### `Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.work`

[Исходник](../../tests/test_stage9_reliability.py#L158)

```python
def work(context)
```

Создаёт настоящий backup с подменой только точки фиксации.

### `Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.respond`

[Исходник](../../tests/test_stage9_reliability.py#L161)

```python
def respond(value)
```

Собирает ответ фоновой операции после позднего cancel.

### `Stage9Tests.test_real_bridge_health_and_cancel_respond_during_backup`

[Исходник](../../tests/test_stage9_reliability.py#L166)

```python
def test_real_bridge_health_and_cancel_respond_during_backup(self)
```

Проверка: настоящий subprocess отвечает health/cancel, пока backup worker ожидает; исходный RPC получает отказ после отмены.

### `Stage9Tests.test_real_bridge_health_and_cancel_respond_during_backup.read`

[Исходник](../../tests/test_stage9_reliability.py#L178)

```python
def read()
```

Читает JSON-lines ответы настоящего Core subprocess в очередь.

### `Stage9Tests.test_real_bridge_health_and_cancel_respond_during_backup.send`

[Исходник](../../tests/test_stage9_reliability.py#L182)

```python
def send(identity, method, params=None)
```

Отправляет один тестовый RPC без shell.

<a id="module-tests-test-storage-py"></a>

## `tests/test_storage.py`

Миграция всех режимов, реальные process exits, межпроцессные транзакции, большие outputs, индекс и проверенная ZIP-копия.

### `conversation`

[Исходник](../../tests/test_storage.py#L21)

```python
def conversation(identity='1' * 32, mode='chat', messages=None)
```

Строит детерминированный старый чат с полями scope и русским текстом, без реальных данных пользователя.

### `tool_call`

[Исходник](../../tests/test_storage.py#L27)

```python
def tool_call()
```

Создаёт фиксированный call anchor для проверки импорта/квитанций без настоящей записи файла.

### `StorageTests`

[Исходник](../../tests/test_storage.py#L31)

```python
class StorageTests(unittest.TestCase)
```

Изолированный профиль для транзакций, миграционных сбоев, процесса, индекса и ZIP восстановления.

### `StorageTests.setUp`

[Исходник](../../tests/test_storage.py#L32)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `StorageTests.legacy`

[Исходник](../../tests/test_storage.py#L43)

```python
def legacy(self, value)
```

Пишет настоящий старый JSON до первого открытия SQLite и возвращает путь для сравнения исходных bytes.

### `StorageTests.test_migration_preserves_modes_projects_checkpoints_and_original_bytes`

[Исходник](../../tests/test_storage.py#L49)

```python
def test_migration_preserves_modes_projects_checkpoints_and_original_bytes(self)
```

Проверка: Chat/IDE/Лола, проект и приоритет embedded checkpoint сохраняются; counts и SHA исходников проверены.

### `StorageTests.test_interrupted_migration_is_rolled_back_and_can_retry`

[Исходник](../../tests/test_storage.py#L73)

```python
def test_interrupted_migration_is_rolled_back_and_can_retry(self)
```

Проверка: сбой до manifest откатывает схему/данные целиком; следующий запуск успешно повторяет перенос.

### `StorageTests.test_malformed_project_catalog_stops_migration_without_losing_chats`

[Исходник](../../tests/test_storage.py#L87)

```python
def test_malformed_project_catalog_stops_migration_without_losing_chats(self)
```

Проверка: повреждённый каталог проектов не превращается в пустой и не фиксирует частичную миграцию.

### `StorageTests.test_future_schema_is_not_downgraded`

[Исходник](../../tests/test_storage.py#L98)

```python
def test_future_schema_is_not_downgraded(self)
```

Проверка: более новый user_version отклоняется без перезаписи данных.

### `StorageTests.test_corrupt_checkpoint_cannot_be_treated_as_a_new_chat`

[Исходник](../../tests/test_storage.py#L105)

```python
def test_corrupt_checkpoint_cannot_be_treated_as_a_new_chat(self)
```

Проверка: нечитаемая задача блокирует продолжение вместо потери сведений о возможных эффектах.

### `StorageTests.test_readonly_catalog_and_search_never_open_full_chats_or_legacy_files`

[Исходник](../../tests/test_storage.py#L118)

```python
def test_readonly_catalog_and_search_never_open_full_chats_or_legacy_files(self)
```

Проверка: список и поиск используют SQL metadata/index; сохраняют mode/project scope и русскую подстроку.

### `StorageTests.test_sql_fallback_preserves_substring_search`

[Исходник](../../tests/test_storage.py#L133)

```python
def test_sql_fallback_preserves_substring_search(self)
```

Проверка: поиск без FTS5 сохраняет casefold substring семантику.

### `StorageTests.test_task_and_history_commit_together_without_stale_draft_overwrite`

[Исходник](../../tests/test_storage.py#L139)

```python
def test_task_and_history_commit_together_without_stale_draft_overwrite(self)
```

Проверка: старый draft не затирает новую задачу; ошибка индекса откатывает сообщения и metadata.

### `StorageTests.test_real_process_exit_before_and_after_chat_commit`

[Исходник](../../tests/test_storage.py#L157)

```python
def test_real_process_exit_before_and_after_chat_commit(self)
```

Проверка: os._exit до commit оставляет старые сообщения/checkpoint, после commit сохраняет новые целиком.

### `StorageTests.test_large_outputs_are_referenced_and_hydrated_without_reexecution`

[Исходник](../../tests/test_storage.py#L182)

```python
def test_large_outputs_are_referenced_and_hydrated_without_reexecution(self)
```

Проверка: большой результат занимает компактную ссылку в messages/journal, дедуплицируется и дочитывается по прежнему anchor.

### `StorageTests.test_missing_or_corrupt_artifact_fails_without_mutating_history`

[Исходник](../../tests/test_storage.py#L205)

```python
def test_missing_or_corrupt_artifact_fails_without_mutating_history(self)
```

Проверка: потеря или неверная checksum outputs не выдаёт фиктивный успех и не изменяет исходник.

### `StorageTests.test_legacy_receipts_migrate_once_and_torn_tail_is_retained`

[Исходник](../../tests/test_storage.py#L218)

```python
def test_legacy_receipts_migrate_once_and_torn_tail_is_retained(self)
```

Проверка: настоящая квитанция импортируется однократно, incomplete JSONL tail остаётся в исходнике с warning.

### `StorageTests.test_corrupt_complete_journal_blocks_import_and_keeps_source`

[Исходник](../../tests/test_storage.py#L234)

```python
def test_corrupt_complete_journal_blocks_import_and_keeps_source(self)
```

Проверка: повреждённая полная JSONL строка блокирует восстановление без частичного принятия событий.

### `StorageTests.test_two_processes_share_atomic_call_validation`

[Исходник](../../tests/test_storage.py#L244)

```python
def test_two_processes_share_atomic_call_validation(self)
```

Проверка: параллельные prepare/started сохраняют одну монотонную последовательность без дублирования batch.

### `StorageTests.test_deletion_is_atomic_and_cannot_resurrect_legacy_data`

[Исходник](../../tests/test_storage.py#L265)

```python
def test_deletion_is_atomic_and_cannot_resurrect_legacy_data(self)
```

Проверка: удаление history/task/events не позволяет старому JSON/JSONL вернуться при перезапуске.

### `StorageTests.test_project_removal_detaches_all_chat_modes_in_one_transaction`

[Исходник](../../tests/test_storage.py#L280)

```python
def test_project_removal_detaches_all_chat_modes_in_one_transaction(self)
```

Проверка: удаление проекта переносит его Chat/IDE/voice в личное пространство одной транзакцией.

### `StorageTests.test_verified_backup_restores_database_receipts_and_full_outputs`

[Исходник](../../tests/test_storage.py#L292)

```python
def test_verified_backup_restores_database_receipts_and_full_outputs(self)
```

Проверка: ZIP восстанавливает БД, full outputs, активные и ещё не импортированные старые журналы.

<a id="module-tests-test-subagent-profiles-py"></a>

## `tests/test_subagent_profiles.py`

Долговечность черновиков и запрет повышения прав через модель, повреждение каталога и изоляция возвращаемых данных.

### `SubagentProfileTests`

[Исходник](../../tests/test_subagent_profiles.py#L8)

```python
class SubagentProfileTests(unittest.TestCase)
```

Тестовый класс/фикстура: Долговечность черновиков и запрет повышения прав через модель, повреждение каталога и изоляция возвращаемых данных.

### `SubagentProfileTests.setUp`

[Исходник](../../tests/test_subagent_profiles.py#L9)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `SubagentProfileTests.fields`

[Исходник](../../tests/test_subagent_profiles.py#L13)

```python
def fields(self)
```

Возвращает минимальный допустимый readonly профиль для независимых negative cases.

### `SubagentProfileTests.test_generated_draft_survives_restart_and_requires_user_enablement`

[Исходник](../../tests/test_subagent_profiles.py#L16)

```python
def test_generated_draft_survives_restart_and_requires_user_enablement(self)
```

Проверка: Черновик переживает новое хранилище, запускается только после user enable и сохраняет версии; удаление запрещает resolve.

### `SubagentProfileTests.test_model_cannot_overwrite_enable_or_add_capabilities`

[Исходник](../../tests/test_subagent_profiles.py#L27)

```python
def test_model_cannot_overwrite_enable_or_add_capabilities(self)
```

Проверка: Модель не меняет ID, enabled, model или readonly allowlist и не работает при общем отключении.

### `SubagentProfileTests.test_corruption_fails_closed_and_catalog_copies_cannot_grant_rights`

[Исходник](../../tests/test_subagent_profiles.py#L35)

```python
def test_corruption_fails_closed_and_catalog_copies_cannot_grant_rights(self)
```

Проверка: Копии каталога не изменяют права; повреждение schema не включает default исследователя.

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

<a id="module-tests-test-task-graph-py"></a>

## `tests/test_task_graph.py`

DAG receipts, dependency validation, stale propagation, user plan authority, reload and persisted watchdog recovery.

### `TaskGraphTests`

[Исходник](../../tests/test_task_graph.py#L19)

```python
class TaskGraphTests(unittest.TestCase)
```

Тестовый класс/фикстура: DAG receipts, dependency validation, stale propagation, user plan authority, reload and persisted watchdog recovery.

### `TaskGraphTests.setUp`

[Исходник](../../tests/test_task_graph.py#L20)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `TaskGraphTests.node`

[Исходник](../../tests/test_task_graph.py#L26)

```python
def node(self, identity, path, depends=())
```

Создаёт typed change node с явным путём и dependencies для отрицательных и положительных проверок.

### `TaskGraphTests.write`

[Исходник](../../tests/test_task_graph.py#L29)

```python
def write(self, path, index)
```

Применяет настоящее подтверждённое write через ToolExecutor и возвращает его durable receipt reference.

### `TaskGraphTests.test_graph_completion_requires_receipts_and_staleness_propagates`

[Исходник](../../tests/test_task_graph.py#L38)

```python
def test_graph_completion_requires_receipts_and_staleness_propagates(self)
```

Проверка: Typed DAG завершается по настоящим mutation receipts; внешний edit инвалидирует узел и его зависимости.

### `TaskGraphTests.test_cycles_unknown_checks_and_user_plan_overwrite_are_rejected`

[Исходник](../../tests/test_task_graph.py#L49)

```python
def test_cycles_unknown_checks_and_user_plan_overwrite_are_rejected(self)
```

Проверка: Циклы/неизвестные check IDs отвергаются; модель не стирает закреплённый пользователем граф.

### `TaskGraphTests.test_saved_witness_survives_reload_and_unknown_receipt_is_not_evidence`

[Исходник](../../tests/test_task_graph.py#L57)

```python
def test_saved_witness_survives_reload_and_unknown_receipt_is_not_evidence(self)
```

Проверка: Неизвестный эффект не закрывает шаг; успешные witness/receipt links переживают сохранение/загрузку.

### `TaskGraphTests.test_legacy_steps_remain_advisory_not_false_completed`

[Исходник](../../tests/test_task_graph.py#L68)

```python
def test_legacy_steps_remain_advisory_not_false_completed(self)
```

Проверка: Legacy строковый план мигрирует в proposed/advisory без утверждения выполнения.

### `TaskGraphTests.test_watchdog_ignores_receipt_ids_and_preserves_one_recovery_across_resume`

[Исходник](../../tests/test_task_graph.py#L75)

```python
def test_watchdog_ignores_receipt_ids_and_preserves_one_recovery_across_resume(self)
```

Проверка: Volatile IDs не маскируют повтор; одна диагностика сохраняется через resume, новые результаты не блокируются.

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

<a id="module-tests-test-tool-execution-py"></a>

## `tests/test_tool_execution.py`

Fault-injection исполнения: реальные остановки процессов, запрет повторения эффектов, сохранение успехов и ручное восстановление.

### `ToolExecutionTests`

[Исходник](../../tests/test_tool_execution.py#L59)

```python
class ToolExecutionTests(unittest.TestCase)
```

Тестовый класс/фикстура: Fault-injection исполнения: реальные остановки процессов, запрет повторения эффектов, сохранение успехов и ручное восстановление.

### `ToolExecutionTests.setUp`

[Исходник](../../tests/test_tool_execution.py#L60)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `ToolExecutionTests.executor`

[Исходник](../../tests/test_tool_execution.py#L69)

```python
def executor(self, handler=None, **options)
```

Создаёт настоящий ToolExecutor с временным журналом и настраиваемыми границами отказов.

### `ToolExecutionTests.test_invalid_arguments_never_start_or_dispatch`

[Исходник](../../tests/test_tool_execution.py#L75)

```python
def test_invalid_arguments_never_start_or_dispatch(self)
```

Проверка: ошибка схемы не запускает handler и сохраняет настоящий отказ

### `ToolExecutionTests.test_prepared_record_failure_prevents_dispatch`

[Исходник](../../tests/test_tool_execution.py#L81)

```python
def test_prepared_record_failure_prevents_dispatch(self)
```

Проверка: ошибка записи пачки предотвращает исполнение

### `ToolExecutionTests.test_started_record_failure_prevents_effect`

[Исходник](../../tests/test_tool_execution.py#L87)

```python
def test_started_record_failure_prevents_effect(self)
```

Проверка: ошибка started предотвращает побочный эффект

### `ToolExecutionTests.test_effect_exception_is_unknown_but_read_exception_is_retryable`

[Исходник](../../tests/test_tool_execution.py#L94)

```python
def test_effect_exception_is_unknown_but_read_exception_is_retryable(self)
```

Проверка: исключение эффекта требует проверки, исключение reader допускает повтор

### `ToolExecutionTests.test_denied_write_never_starts_and_keeps_file_unchanged`

[Исходник](../../tests/test_tool_execution.py#L103)

```python
def test_denied_write_never_starts_and_keeps_file_unchanged(self)
```

Проверка: отказ от diff не сохраняет started и не меняет файл

### `ToolExecutionTests.test_external_approval_durably_starts_only_after_agreement`

[Исходник](../../tests/test_tool_execution.py#L113)

```python
def test_external_approval_durably_starts_only_after_agreement(self)
```

Проверка: команда/MCP пересекает границу started только после согласия

### `ToolExecutionTests.test_external_approval_durably_starts_only_after_agreement.handler`

[Исходник](../../tests/test_tool_execution.py#L115)

```python
def handler(*_)
```

Проверяет durable phase до и после разрешения внешнего действия.

### `ToolExecutionTests.test_external_denial_never_marks_effect_started`

[Исходник](../../tests/test_tool_execution.py#L123)

```python
def test_external_denial_never_marks_effect_started(self)
```

Проверка: отклонённый внешний call остаётся не начатым

### `ToolExecutionTests.test_external_denial_never_marks_effect_started.handler`

[Исходник](../../tests/test_tool_execution.py#L124)

```python
def handler(*_)
```

Возвращает отказ после настоящих hooks подтверждения, не начиная эффект.

### `ToolExecutionTests.test_saved_receipt_survives_checkpoint_failure`

[Исходник](../../tests/test_tool_execution.py#L132)

```python
def test_saved_receipt_survives_checkpoint_failure(self)
```

Проверка: ошибка chat checkpoint не теряет durable результат инструмента

### `ToolExecutionTests.test_saved_receipt_survives_checkpoint_failure.checkpoint`

[Исходник](../../tests/test_tool_execution.py#L133)

```python
def checkpoint(*_)
```

Имитирует потерю доступности chat projection сразу после сохранения квитанции.

### `ToolExecutionTests.test_reused_call_ids_are_bound_to_their_batch`

[Исходник](../../tests/test_tool_execution.py#L142)

```python
def test_reused_call_ids_are_bound_to_their_batch(self)
```

Проверка: повтор ID модели в другой пачке не заимствует прежний успех

### `ToolExecutionTests.test_real_process_exit_at_five_execution_boundaries`

[Исходник](../../tests/test_tool_execution.py#L152)

```python
def test_real_process_exit_at_five_execution_boundaries(self)
```

Проверка: настоящий os._exit до/после эффекта и receipts не повторяет действие и сохраняет успех соседнего call

### `ToolExecutionTests.test_recovery_metadata_is_bounded_and_idempotent`

[Исходник](../../tests/test_tool_execution.py#L179)

```python
def test_recovery_metadata_is_bounded_and_idempotent(self)
```

Проверка: 105 вызовов дают не более 100 UI-записей без повторного изменения IDs

### `ToolExecutionTests.test_verification_recovers_failed_commands_from_receipts`

[Исходник](../../tests/test_tool_execution.py#L187)

```python
def test_verification_recovers_failed_commands_from_receipts(self)
```

Проверка: провал команды восстанавливается из журнала и блокирует ложное completed

### `ToolExecutionTests.test_unknown_effect_blocks_new_prompt_resume_and_fork_until_review`

[Исходник](../../tests/test_tool_execution.py#L195)

```python
def test_unknown_effect_blocks_new_prompt_resume_and_fork_until_review(self)
```

Проверка: неизвестный эффект блокирует новые запуски и копирование до проверки; устаревшие решения отвергаются

### `ToolExecutionTests.test_deleting_chat_removes_only_its_journals`

[Исходник](../../tests/test_tool_execution.py#L218)

```python
def test_deleting_chat_removes_only_its_journals(self)
```

Проверка: удаление истории не затрагивает журналы других чатов

### `ToolExecutionTests.test_unknown_flag_never_appears_as_success`

[Исходник](../../tests/test_tool_execution.py#L224)

```python
def test_unknown_flag_never_appears_as_success(self)
```

Проверка: неопределённый исход не отображается зелёным успехом даже при противоречивом ok=true обработчика

### `ToolExecutionTests.test_receipt_without_boolean_outcome_is_rejected_before_adoption`

[Исходник](../../tests/test_tool_execution.py#L231)

```python
def test_receipt_without_boolean_outcome_is_rejected_before_adoption(self)
```

Проверка: невалидное поле ok не записывается и не принимается из истории как настоящий результат

<a id="module-tests-test-windows-dependencies-py"></a>

## `tests/test_windows_dependencies.py`

Тесты закреплённых загрузок: кэш без сети, отклонение подмены и атомарная замена повреждённого файла.

### `WindowsDependenciesTests`

[Исходник](../../tests/test_windows_dependencies.py#L12)

```python
class WindowsDependenciesTests(unittest.TestCase)
```

Тестовый класс/фикстура: Тесты закреплённых загрузок: кэш без сети, отклонение подмены и атомарная замена повреждённого файла.

### `WindowsDependenciesTests.test_verified_cache_does_not_download`

[Исходник](../../tests/test_windows_dependencies.py#L13)

```python
def test_verified_cache_does_not_download(self)
```

Проверка: Подтверждает повторное использование валидного SHA256-кэша без сетевого обращения.

### `WindowsDependenciesTests.test_mismatch_preserves_old_file_and_removes_partial`

[Исходник](../../tests/test_windows_dependencies.py#L21)

```python
def test_mismatch_preserves_old_file_and_removes_partial(self)
```

Проверка: Не допускает подменённый файл и удаляет частичную загрузку, сохраняя старый кэш.

### `WindowsDependenciesTests.test_success_replaces_corrupt_cache`

[Исходник](../../tests/test_windows_dependencies.py#L32)

```python
def test_success_replaces_corrupt_cache(self)
```

Проверка: Заменяет повреждённый кэш только после успешной проверки новой загрузки.

<a id="module-tests-test-workspace-tools-py"></a>

## `tests/test_workspace_tools.py`

Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.

### `WorkspaceToolsTests`

[Исходник](../../tests/test_workspace_tools.py#L22)

```python
class WorkspaceToolsTests(unittest.TestCase)
```

Тестовый класс/фикстура: Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.

### `WorkspaceToolsTests.test_write_sharing_retry_rechecks_revision_before_atomic_replace`

[Исходник](../../tests/test_workspace_tools.py#L24)

```python
@unittest.skipUnless(os.name == 'nt', 'Windows sharing violations')
def test_write_sharing_retry_rechecks_revision_before_atomic_replace(self)
```

Проверка: Короткая Windows file lock пауза повторяет только отказавший atomic replace после проверки прежнего SHA, без снятия guards.

### `WorkspaceToolsTests.test_write_sharing_retry_rechecks_revision_before_atomic_replace.transient`

[Исходник](../../tests/test_workspace_tools.py#L28)

```python
def transient(source, destination)
```

Один раз моделирует Windows sharing violation, затем вызывает настоящий atomic replace.

### `WorkspaceToolsTests.setUp`

[Исходник](../../tests/test_workspace_tools.py#L36)

```python
def setUp(self)
```

Создаёт изолированные данные и подмены перед каждым тестом этого класса.

### `WorkspaceToolsTests.apply`

[Исходник](../../tests/test_workspace_tools.py#L41)

```python
def apply(self, name, args)
```

Применяет настоящий preview/snapshot в изолированном проекте для проверок побочных эффектов.

### `WorkspaceToolsTests.test_range_preserves_crlf_line_numbers_and_full_revision`

[Исходник](../../tests/test_workspace_tools.py#L45)

```python
def test_range_preserves_crlf_line_numbers_and_full_revision(self)
```

Проверка: диапазон сохраняет CRLF, номера строк и SHA256 всей ревизии

### `WorkspaceToolsTests.test_range_reads_large_source_and_can_be_cancelled`

[Исходник](../../tests/test_workspace_tools.py#L51)

```python
def test_range_reads_large_source_and_can_be_cancelled(self)
```

Проверка: часть большого исходника читается без выдачи всего файла; отмена возвращается явно

### `WorkspaceToolsTests.test_range_never_silently_truncates_one_long_line`

[Исходник](../../tests/test_workspace_tools.py#L58)

```python
def test_range_never_silently_truncates_one_long_line(self)
```

Проверка: длинная строка не выдаётся как целая после скрытого обрезания

### `WorkspaceToolsTests.test_patch_changes_one_fragment_preserving_other_bytes`

[Исходник](../../tests/test_workspace_tools.py#L62)

```python
def test_patch_changes_one_fragment_preserving_other_bytes(self)
```

Проверка: точечная правка меняет один фрагмент и сохраняет остальные байты/CRLF; snapshot переживает JSON roundtrip

### `WorkspaceToolsTests.test_ambiguous_or_missing_patch_does_not_modify_file`

[Исходник](../../tests/test_workspace_tools.py#L69)

```python
def test_ambiguous_or_missing_patch_does_not_modify_file(self)
```

Проверка: ноль или несколько совпадений не дают произвольную замену

### `WorkspaceToolsTests.test_patch_requires_approval_and_refuses_changed_revision`

[Исходник](../../tests/test_workspace_tools.py#L76)

```python
def test_patch_requires_approval_and_refuses_changed_revision(self)
```

Проверка: без согласия запись запрещена, ручная правка после preview сохраняется

### `WorkspaceToolsTests.test_read_revision_can_be_bound_before_preview`

[Исходник](../../tests/test_workspace_tools.py#L84)

```python
def test_read_revision_can_be_bound_before_preview(self)
```

Проверка: ожидаемый hash из read_range отклоняет устаревшее предложение ещё до diff

### `WorkspaceToolsTests.test_nested_directory_creation_and_existing_directory`

[Исходник](../../tests/test_workspace_tools.py#L90)

```python
def test_nested_directory_creation_and_existing_directory(self)
```

Проверка: вложенные папки создаются только после preview; существующий каталог не меняется

### `WorkspaceToolsTests.test_new_file_can_be_created_after_explicit_directory_tool`

[Исходник](../../tests/test_workspace_tools.py#L98)

```python
def test_new_file_can_be_created_after_explicit_directory_tool(self)
```

Проверка: новая вложенная структура создаётся через разрешённые операции без shell

### `WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back`

[Исходник](../../tests/test_workspace_tools.py#L106)

```python
def test_partial_directory_cancel_is_unknown_and_not_rolled_back(self)
```

Проверка: частично созданная цепочка не удаляется молча и требует проверки результата

### `WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back.CancelAfterFirst`

[Исходник](../../tests/test_workspace_tools.py#L107)

```python
class CancelAfterFirst
```

Тестовый класс/фикстура: Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.

### `WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back.CancelAfterFirst.__init__`

[Исходник](../../tests/test_workspace_tools.py#L108)

```python
def __init__(self)
```

Инициализирует состояние экземпляра WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back.CancelAfterFirst; параметры показаны в сигнатуре, назначение описано у класса.

### `WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back.CancelAfterFirst.is_set`

[Исходник](../../tests/test_workspace_tools.py#L109)

```python
def is_set(self)
```

Имитирует отмену после создания первого каталога для проверки частичного исхода.

### `WorkspaceToolsTests.test_rename_never_overwrites_destination`

[Исходник](../../tests/test_workspace_tools.py#L115)

```python
def test_rename_never_overwrites_destination(self)
```

Проверка: существующее или появившееся назначение не затирается

### `WorkspaceToolsTests.test_rename_and_delete_have_distinct_previews_and_results`

[Исходник](../../tests/test_workspace_tools.py#L123)

```python
def test_rename_and_delete_have_distinct_previews_and_results(self)
```

Проверка: перенос и удаление показывают разные намерения и возвращают структурированные квитанции

### `WorkspaceToolsTests.test_root_outside_and_recursive_directory_deletion_are_denied`

[Исходник](../../tests/test_workspace_tools.py#L131)

```python
def test_root_outside_and_recursive_directory_deletion_are_denied(self)
```

Проверка: корень, внешние пути, .git и рекурсивное удаление недоступны новым операциям

### `WorkspaceToolsTests.test_glob_and_text_search_share_bounds_and_cancellation`

[Исходник](../../tests/test_workspace_tools.py#L140)

```python
def test_glob_and_text_search_share_bounds_and_cancellation(self)
```

Проверка: GUI/model используют один поиск, **/* работает по сегментам, лимиты и отмена действуют в tools

### `WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it`

[Исходник](../../tests/test_workspace_tools.py#L152)

```python
def test_search_cancels_while_scanning_rather_than_only_before_it(self)
```

Проверка: поиск останавливается уже в процессе обхода, не только при входе

### `WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it.CancelDuringScan`

[Исходник](../../tests/test_workspace_tools.py#L154)

```python
class CancelDuringScan
```

Тестовый класс/фикстура: Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.

### `WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it.CancelDuringScan.__init__`

[Исходник](../../tests/test_workspace_tools.py#L155)

```python
def __init__(self)
```

Инициализирует состояние экземпляра WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it.CancelDuringScan; параметры показаны в сигнатуре, назначение описано у класса.

### `WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it.CancelDuringScan.is_set`

[Исходник](../../tests/test_workspace_tools.py#L156)

```python
def is_set(self)
```

Выдаёт отмену после нескольких проверок внутри настоящего обхода.

### `WorkspaceToolsTests.test_scoped_rules_are_loaded_before_mutation_and_refresh_after_change`

[Исходник](../../tests/test_workspace_tools.py#L160)

```python
def test_scoped_rules_are_loaded_before_mutation_and_refresh_after_change(self)
```

Проверка: вложенные правила доходят до модели перед согласием; их смена блокирует прежнее предложение

### `WorkspaceToolsTests.test_scoped_rules_are_loaded_before_mutation_and_refresh_after_change.Client`

[Исходник](../../tests/test_workspace_tools.py#L171)

```python
class Client
```

Тестовый класс/фикстура: Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.

### `WorkspaceToolsTests.test_scoped_rules_are_loaded_before_mutation_and_refresh_after_change.Client.create`

[Исходник](../../tests/test_workspace_tools.py#L172)

```python
def create(self, **params)
```

Принимает модельную проекцию с подключёнными scoped правилами без HTTP и реальной LLM.

### `WorkspaceToolsTests.test_instructions_are_bounded_and_do_not_expand_root`

[Исходник](../../tests/test_workspace_tools.py#L179)

```python
def test_instructions_are_bounded_and_do_not_expand_root(self)
```

Проверка: AGENTS.md не расширяет корень и не обрезается при превышении ограничения

### `WorkspaceToolsTests.test_receipt_recovers_workspace_change_without_repeating_patch`

[Исходник](../../tests/test_workspace_tools.py#L187)

```python
def test_receipt_recovers_workspace_change_without_repeating_patch(self)
```

Проверка: журнал восстанавливает метаданные patch без повторной записи файла

### `WorkspaceToolsTests.test_exception_after_patch_is_unknown_not_a_replayable_failure`

[Исходник](../../tests/test_workspace_tools.py#L198)

```python
def test_exception_after_patch_is_unknown_not_a_replayable_failure(self)
```

Проверка: исключение после побочного эффекта остаётся unknown и блокирует автоматический повтор

### `WorkspaceToolsTests.test_exception_after_patch_is_unknown_not_a_replayable_failure.fail_after_effect`

[Исходник](../../tests/test_workspace_tools.py#L201)

```python
def fail_after_effect(*args, **kwargs)
```

Имитирует исключение после изменения файла, когда результат эффекта нельзя считать обычным отказом.

### `WorkspaceToolsTests.test_write_batch_permission_does_not_authorize_delete`

[Исходник](../../tests/test_workspace_tools.py#L208)

```python
def test_write_batch_permission_does_not_authorize_delete(self)
```

Проверка: разрешение пакета write_file не распространяется на новое удаление, которое получает отдельный preview и решение

### `WorkspaceToolsTests.test_write_batch_permission_does_not_authorize_delete.reject_delete`

[Исходник](../../tests/test_workspace_tools.py#L211)

```python
def reject_delete(*args)
```

Отклоняет новое удаление через настоящий approval hook, проверяя независимость от прежнего apply_all для write_file.
