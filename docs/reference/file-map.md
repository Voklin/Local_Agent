# Карта файлов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

Перечислены файлы репозитория; зависимости, окружения и результаты сборки исключены правилами Git.

| Файл | Назначение |
| --- | --- |
| [.gitattributes](../../.gitattributes) | Автоопределение текстовых файлов и нормализация переводов строк в Git. |
| [.github/workflows/release-windows.yml](../../.github/workflows/release-windows.yml) | Явный release.json запускает сборку и проверки Windows, публикацию prerelease с SHA256 через GITHUB_TOKEN; существующую версию не перезаписывает. |
| [.github/workflows/validate.yml](../../.github/workflows/validate.yml) | Windows CI: Python/build/docs и отдельный job freeze/NSIS/packaged smoke с временным installer artifact. |
| [.gitignore](../../.gitignore) | Исключает окружения, сборки, кэши, тестовые данные и секретный .env из Git. |
| [MIGRATION_PLAN.md](../../MIGRATION_PLAN.md) | Выполненные границы миграции и оставшиеся этапы. |
| [README.md](../../README.md) | Краткий вход в проект, запуск и ссылка на учебное руководство. |
| [README_V6_MIGRATION.md](../../README_V6_MIGRATION.md) | Краткая инструкция текущего Electron-пути и его проверок. |
| [VERSION](../../VERSION) | Исторический маркер 5.8.0; не является единственным источником версии нового Electron-приложения. |
| [agent/__init__.py](../../agent/__init__.py) | Маркер Python-пакета agent; не запускает UI или модель. |
| [agent/artifact_store.py](../../agent/artifact_store.py) | Неизменяемые UTF-8 результаты инструментов: SHA-256, атомарная запись, проверка целостности. |
| [agent/auto_budget.py](../../agent/auto_budget.py) | Read-only определение фактического окна LM Studio/Ollama/llama.cpp, bounded cache, разбор context rejection и SDK tokenizer только уже загруженного экземпляра. |
| [agent/call_journal.py](../../agent/call_journal.py) | Транзакционный журнал SQLite с прежними lifecycle/recovery контрактами и отдельным legacy JSONL reader. |
| [agent/capability_profiles.py](../../agent/capability_profiles.py) | Фиксированные ограничивающие профили Chat/IDE/Лолы; включённые расширения остаются источником разрешений. |
| [agent/chat_store.py](../../agent/chat_store.py) | Разговоры и метаданные истории в транзакционном SQLite с миграцией старых JSON. |
| [agent/child_executor.py](../../agent/child_executor.py) | Real readonly child AgentEngine handoff with inherited connection, cancellable join, durable journal and fresh bounded handback. |
| [agent/companion_policy.py](../../agent/companion_policy.py) | Граница делегирования Лолы по исходному намерению человека и очистка ответов/озвучки от разметки. |
| [agent/companion_preferences.py](../../agent/companion_preferences.py) | Независимый сохраняемый профиль Лолы: модель, endpoint, характер, STT и голос; секреты не сохраняются. |
| [agent/connection_profiles.py](../../agent/connection_profiles.py) | Именованные публичные конфигурации моделей без API-ключей. |
| [agent/container_runner.py](../../agent/container_runner.py) | Opt-in Linux Docker runner: readonly bind, без сети/pull, CPU/RAM/PID лимиты, отдельное approval и cleanup daemon container. |
| [agent/context_builder.py](../../agent/context_builder.py) | Подбор сохранённых диапазонов проекта, provenance, дедупликация, финальная проверка доступа/хеша и точный предпросмотр внешней отправки. |
| [agent/context_manager.py](../../agent/context_manager.py) | Сборка временного рабочего контекста с метаданными задачи, умным сжатием и статистикой. |
| [agent/context_tools.py](../../agent/context_tools.py) | Безопасное чтение диапазонов сохранённых результатов и поиск включённых MCP без исполнения внешних действий. |
| [agent/conversation.py](../../agent/conversation.py) | Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп. |
| [agent/delegation.py](../../agent/delegation.py) | Единственное определение delegate_task для передачи сложной задачи от Лолы основной модели. |
| [agent/diagnostics_evidence.py](../../agent/diagnostics_evidence.py) | LSP как проверяемое свидетельство: user check, сохранённые файлы, настройки сервера, approval и строгая полнота результата. |
| [agent/editor_io.py](../../agent/editor_io.py) | Самостоятельные sandbox-функции текстового редактора; React preview их не использует для записи. |
| [agent/engine.py](../../agent/engine.py) | Независимый от UI цикл модели, инструментов, подтверждений, памяти и checkpoint. |
| [agent/git_checkpoints.py](../../agent/git_checkpoints.py) | Приватный bare Git архив before/after подтверждённых snapshots; не меняет индекс, ветку, hooks и файлы проекта. |
| [agent/inference_scheduler.py](../../agent/inference_scheduler.py) | Общая FIFO очередь физической генерации, cancellable tickets и reservations/usage для SDK, probe и readonly research. |
| [agent/json_tools.py](../../agent/json_tools.py) | Текстовый JSON tool protocol: преобразование истории, строгий parser envelope и адаптация stream к обычному executor. |
| [agent/language_diagnostics.py](../../agent/language_diagnostics.py) | Настоящий stdio LSP initialize/didOpen/publishDiagnostics; отказ server edits/commands, bounded framing и завершение процесса. |
| [agent/managed_worktrees.py](../../agent/managed_worktrees.py) | Пользовательские Git worktrees из HEAD, receipts владения, список/diff/open и удаление только неизменённой копии. |
| [agent/mcp.py](../../agent/mcp.py) | Реестр MCP-конфигураций без транспорта и исполнения внешних tools. |
| [agent/mcp_client.py](../../agent/mcp_client.py) | SDK-адаптер MCP поверх session pool; нормализация bounded/untrusted результатов без раскрытия токенов. |
| [agent/mcp_sessions.py](../../agent/mcp_sessions.py) | Ограниченный пул MCP actors: connect/use/exit в одной asyncio task, TTL, отмена, invalidation и shutdown без повтора effects. |
| [agent/model_client.py](../../agent/model_client.py) | Отменяемый async HTTP-клиент с синхронной поверхностью для движка. |
| [agent/model_discovery.py](../../agent/model_discovery.py) | HTTPX-получение списка моделей с общим deadline, ограничением ответа и отменой сокета. |
| [agent/model_gateway.py](../../agent/model_gateway.py) | Отдельное представление endpoint провайдера/локального runtime; не включено в TaskService. |
| [agent/model_manager.py](../../agent/model_manager.py) | Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции. |
| [agent/model_preferences.py](../../agent/model_preferences.py) | Валидация endpoint и whitelist числовых настроек, миграция старого JSON и атомарное сохранение без API-ключа. |
| [agent/model_probe.py](../../agent/model_probe.py) | Ограниченная отменяемая проверка draft-модели через Chat Completions без файлов, истории и сохранения настроек. |
| [agent/operation_context.py](../../agent/operation_context.py) | Общий deadline/cancel контракт и единый inference gate для задач, probe и последующих необязательных вычислений. |
| [agent/optional_process.py](../../agent/optional_process.py) | Без-shell subprocess с allowlist окружения, bounded output, общим deadline и закрытием дерева дочерних процессов. |
| [agent/planner.py](../../agent/planner.py) | Структура этапа и детерминированный план по словам запроса. |
| [agent/process_identity.py](../../agent/process_identity.py) | Read-only Windows/Linux process lifetime probe, tri-state uncertainty and PID reuse evidence for orphan telemetry recovery. |
| [agent/process_job.py](../../agent/process_job.py) | Windows Job Object: kill-on-close только для собственного Popen и его потомков. |
| [agent/progress_guard.py](../../agent/progress_guard.py) | Окно отпечатков вызовов и результатов для остановки чередующихся циклов без продвижения. |
| [agent/project_command.py](../../agent/project_command.py) | Опциональный запуск тестов/сборок после отдельного подтверждения; ограниченный вывод, время и ProcessJob. |
| [agent/project_index.py](../../agent/project_index.py) | Отдельный derived SQLite/WAL cache проекта, FTS5, durable queue точных путей, watcher, incremental update и проверенный retrieval. |
| [agent/project_index_policy.py](../../agent/project_index_policy.py) | Per-operation WorkspaceAccessPolicy и ancestor .gitignore с GitWildMatch, nested rules и policy provenance. |
| [agent/project_instructions.py](../../agent/project_instructions.py) | Ограниченное чтение AGENTS.md по иерархии выбранного пути; версии/области действия передаются модели и не расширяют права. |
| [agent/project_knowledge.py](../../agent/project_knowledge.py) | Память проекта: bounded записи с происхождением, SHA источников, инвалидацией доступа, лексическим/структурным поиском и свежестью перед POST. |
| [agent/project_memory.py](../../agent/project_memory.py) | Компактная структурированная память проекта, очистка и форматирование для модели. |
| [agent/project_symbols.py](../../agent/project_symbols.py) | Синтаксические определения/импорты Python AST и JS/TS/TSX Tree-sitter; никакого выполнения исходников или semantic reference resolution. |
| [agent/projects.py](../../agent/projects.py) | Проекты в SQLite и атомарное отсоединение всех их чатов при удалении проекта. |
| [agent/readonly_research.py](../../agent/readonly_research.py) | Отдельный readonly контекст: до 6 фрагментов/12000 символов, один HTTP запрос без tools/retry, cancel и usage. |
| [agent/request_budget.py](../../agent/request_budget.py) | Автоматическое/ручное размещение окончательного Chat/JSON/Responses запроса: tokenizer/оценка, ответ, каталог schemas и компактные квитанции выполненного кода без изменения истории. |
| [agent/response_outcome.py](../../agent/response_outcome.py) | Общий контракт терминального ответа модели: complete/incomplete/refused/cancelled/error; EOF не становится успешным stop. |
| [agent/responses_adapter.py](../../agent/responses_adapter.py) | Преобразование канонической истории и потоковых событий OpenAI Responses в существующий цикл агента. |
| [agent/run_policy.py](../../agent/run_policy.py) | Opt-in monetary planning for one logical task and all children/resumes; no local-auto cap, explicit unknown usage and capacity errors. |
| [agent/run_registry.py](../../agent/run_registry.py) | Сохраняемые epochs запуска и атомарный BudgetLedger в canonical SQLite v3; recovery orphan telemetry без повторения эффектов. |
| [agent/run_state.py](../../agent/run_state.py) | Проверяемый жизненный цикл запуска с совместимой проекцией legacy status; этапы плана хранятся независимо. |
| [agent/runtime.py](../../agent/runtime.py) | Связь контекста, планировщика, навыков, verifier и MCP-реестра; часть границ ещё не подключена. |
| [agent/security.py](../../agent/security.py) | Канонический корень и разрешение путей только внутри выбранного проекта. |
| [agent/skills.py](../../agent/skills.py) | Обнаружение, краткие метаданные, чтение и выбор SKILL.md по словам. |
| [agent/smart_context.py](../../agent/smart_context.py) | Детерминированное сжатие временного контекста с архивом ограничений и фактов без LLM-запросов и изменения канонической истории. |
| [agent/storage.py](../../agent/storage.py) | SQLite/WAL профиль: схемы v1→v2, копирующая миграция JSON, индекс истории, checkpoint/receipts, snapshot metadata и ZIP backup. |
| [agent/subagent_profiles.py](../../agent/subagent_profiles.py) | Версионированный атомарный каталог readonly профилей, пользовательский CRUD и выключенные черновики модели без повышения прав. |
| [agent/task_activity.py](../../agent/task_activity.py) | Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории. |
| [agent/task_contract.py](../../agent/task_contract.py) | Пользовательские параметры IDE, план модели и критерии с привязкой к настоящим проверкам. |
| [agent/task_graph.py](../../agent/task_graph.py) | Canonical plan_steps DAG: migration, validation, receipt-based completion and scoped stale-evidence propagation. |
| [agent/task_store.py](../../agent/task_store.py) | Checkpoint задач в SQLite и совместимость прежнего файлового хранения. |
| [agent/tool_executor.py](../../agent/tool_executor.py) | Единая валидация разрешённых tools, границы начала побочных эффектов, diff approval и сохранение результатов до публикации. |
| [agent/tool_recovery.py](../../agent/tool_recovery.py) | Сверка журнала с канонической историей, восстановление свидетельств и ограниченных метаданных интерфейса. |
| [agent/tools.py](../../agent/tools.py) | Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test. |
| [agent/ui.py](../../agent/ui.py) | Сохранённый Qt GUI: панели, readonly preview, настройки, чат и approval dialog. |
| [agent/verification_evidence.py](../../agent/verification_evidence.py) | Versioned evidence команд: исполнение, точная пользовательская область, before/after source witnesses, актуальность и lazy migration. |
| [agent/verification_plan.py](../../agent/verification_plan.py) | Детерминированный выбор пользовательских проверок по затронутым путям; связанные критерии не пропускаются. |
| [agent/verifier.py](../../agent/verifier.py) | Оценка фактических команд и diagnostics с учётом области и свежести исходников. |
| [agent/worker.py](../../agent/worker.py) | Qt QThread-адаптер вокруг AgentEngine; преобразует callbacks в Signal. |
| [agent/workspace_access.py](../../agent/workspace_access.py) | Общая политика автоматического доступа: секретные пути, .neutralignore, точечные пользовательские исключения и повторная проверка истории. |
| [agent/workspace_edits.py](../../agent/workspace_edits.py) | Preview и подтверждаемое применение patch/create-directory/rename/delete со snapshot, проверкой корня и восстановимыми метаданными. |
| [agent/workspace_read.py](../../agent/workspace_read.py) | Чтение точных диапазонов UTF-8 со стабильной ревизией, отменой и явным отказом от обрезания длинной строки. |
| [agent/workspace_revision.py](../../agent/workspace_revision.py) | Ограниченный content fingerprint исходников и сравнение проверяемых receipt с текущей ревизией проекта. |
| [agent/workspace_search.py](../../agent/workspace_search.py) | Общий ограниченный поиск файлов/текста для модели и GUI: glob по сегментам пути, отмена, deadline и лимиты обхода/чтения. |
| [agent/workspace_snapshots.py](../../agent/workspace_snapshots.py) | Долговечные before/after снимки файловых tools, сегменты изменений, conflict-aware rollback и ручная проверка прерванного отката. |
| [apps/desktop/.gitignore](../../apps/desktop/.gitignore) | Локальные исключения выходных директорий desktop-сборки. |
| [apps/desktop/build-electron.mjs](../../apps/desktop/build-electron.mjs) | Vite library-сборки main.cjs, preload.cjs и изолированного lolaPreload.cjs с внешними системными импортами. |
| [apps/desktop/electron/assistantMedia.ts](../../apps/desktop/electron/assistantMedia.ts) | Повторная host-валидация фиксированных музыкальных HTTPS URL и реального локального аудиофайла внутри разрешённых папок. |
| [apps/desktop/electron/desktopApps.ts](../../apps/desktop/electron/desktopApps.ts) | Каталог локально разрешённых EXE: системные приложения, выбор пользователем, ID без путей для модели и запуск без shell/аргументов. |
| [apps/desktop/electron/desktopLola.ts](../../apps/desktop/electron/desktopLola.ts) | Нативные прозрачное окно и Tray спутника Лолы, сохранение preferences, изоляция IPC и пересылка ограниченных пользовательских действий. |
| [apps/desktop/electron/lolaPreload.ts](../../apps/desktop/electron/lolaPreload.ts) | Изолированный preload popup с общим типизированным facade; main разрешает только голосовые операции и собственные chat/run IDs. |
| [apps/desktop/electron/main.ts](../../apps/desktop/electron/main.ts) | Окно, Python-процесс, single-instance lock, pending RPC, проверка sender и фиксированные IPC handlers; создаёт нативный desktop companion. |
| [apps/desktop/electron/neutralIde.ts](../../apps/desktop/electron/neutralIde.ts) | Собственный Code-OSS launcher: отдельные runtime/profile/shared storage и авторизованный named pipe только для status/focus. |
| [apps/desktop/electron/preload.ts](../../apps/desktop/electron/preload.ts) | Узкий window.lca API и отписываемый listener событий. |
| [apps/desktop/electron/speechRuntime.ts](../../apps/desktop/electron/speechRuntime.ts) | Запуск фиксированного локального Piper, установка проверенной Serena, health и остановка только своего процесса. |
| [apps/desktop/ide.html](../../apps/desktop/ide.html) | HTML entrypoint независимой панели в Code-OSS webview. |
| [apps/desktop/index.html](../../apps/desktop/index.html) | HTML-узел React и модульный entry point renderer. |
| [apps/desktop/lola.html](../../apps/desktop/lola.html) | Отдельный HTML entrypoint спутника с локальной строгой CSP. |
| [apps/desktop/package.json](../../apps/desktop/package.json) | Зависимости Electron/React и dev/build/typecheck-скрипты workspace. |
| [apps/desktop/shared/contextTypes.ts](../../apps/desktop/shared/contextTypes.ts) | Независимые от React типы budget/usage для протокола и renderer. |
| [apps/desktop/shared/createApi.ts](../../apps/desktop/shared/createApi.ts) | Общая фабрика фиксированного API для Electron preload и Code-OSS транспорта. |
| [apps/desktop/shared/ideTypes.ts](../../apps/desktop/shared/ideTypes.ts) | Общие validation command и IDE task options без renderer runtime. |
| [apps/desktop/shared/lolaDesktop.ts](../../apps/desktop/shared/lolaDesktop.ts) | Общие строгие типы, defaults и проверка состояния, команд и размещения настольной Лолы. |
| [apps/desktop/shared/optionalTypes.ts](../../apps/desktop/shared/optionalTypes.ts) | Типы настроек, discriminated requests и публичных результатов дополнительных IDE операций. |
| [apps/desktop/shared/protocol.ts](../../apps/desktop/shared/protocol.ts) | Общие типы критического IPC, версия, runtime guard событий и таблица timeout/cancel. |
| [apps/desktop/shared/taskTypes.ts](../../apps/desktop/shared/taskTypes.ts) | Единые task/recovery/evidence типы без зависимости Electron main от TSX. |
| [apps/desktop/src/App.tsx](../../apps/desktop/src/App.tsx) | React-состояние и представление проекта, настроек, чата, потока, checkpoint, diff и безопасного мостика действий настольной Лолы в единый голосовой контур. |
| [apps/desktop/src/AppearanceSettings.tsx](../../apps/desktop/src/AppearanceSettings.tsx) | Проверенные локальные настройки темы, акцента, плотности и панелей, синхронизация React и форма оформления. |
| [apps/desktop/src/ApprovalDialog.tsx](../../apps/desktop/src/ApprovalDialog.tsx) | Рабочий модальный запрос разрешения с типизированным решением и сведениями о действии. |
| [apps/desktop/src/BrandMark.tsx](../../apps/desktop/src/BrandMark.tsx) | Векторный знак Neutral: N и точка равновесия; цвет наследуется от темы. |
| [apps/desktop/src/ChatText.tsx](../../apps/desktop/src/ChatText.tsx) | Безопасные текстовые/code блоки без HTML, memoized parser и явное копирование. |
| [apps/desktop/src/CompanionSettings.tsx](../../apps/desktop/src/CompanionSettings.tsx) | Настройка характера, независимой модели, JSON/native protocol, автоматической передачи и STT Лолы. |
| [apps/desktop/src/ConnectionProfiles.tsx](../../apps/desktop/src/ConnectionProfiles.tsx) | Сохранение, выбор и удаление публичных профилей подключения модели. |
| [apps/desktop/src/ConnectionsSettings.tsx](../../apps/desktop/src/ConnectionsSettings.tsx) | Настройка PC-инструментов и Telegram; явное подключение владельца и защищённое сохранение токена. |
| [apps/desktop/src/ContextUsage.tsx](../../apps/desktop/src/ContextUsage.tsx) | Карточка оценки полного контекста, состава входа, отложенных MCP-схем и фактического usage сервера. |
| [apps/desktop/src/ConversationSidebar.tsx](../../apps/desktop/src/ConversationSidebar.tsx) | Проекты, поиск разговоров, закрепление, архив, копии, повтор, экспорт, перемещение и удаление. |
| [apps/desktop/src/DesktopLolaSettings.tsx](../../apps/desktop/src/DesktopLolaSettings.tsx) | Переиспользуемая доступная форма включения спутника, режима окон, размера и анимации с применением настроек. |
| [apps/desktop/src/DesktopLolaView.tsx](../../apps/desktop/src/DesktopLolaView.tsx) | Компактная оболочка спутника: bounded chat input, управление голосом, перетаскивание, виджет состояний и вызовы узкого preload API. |
| [apps/desktop/src/EditorPanel.tsx](../../apps/desktop/src/EditorPanel.tsx) | Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение. |
| [apps/desktop/src/ExtensionsSettings.tsx](../../apps/desktop/src/ExtensionsSettings.tsx) | Настройки наборов, отдельных tools, навыков, JSON-пакетов и MCP серверов. |
| [apps/desktop/src/GenerationFields.tsx](../../apps/desktop/src/GenerationFields.tsx) | Единые типы, значения, диапазоны, подсказки и форма генерации для Chat/IDE и отдельной модели Лолы. |
| [apps/desktop/src/IdeTaskOptions.tsx](../../apps/desktop/src/IdeTaskOptions.tsx) | Компактные параметры задачи IDE: только чтение, критерии, команды и post-edit проверки. |
| [apps/desktop/src/LocalRuntimePanel.tsx](../../apps/desktop/src/LocalRuntimePanel.tsx) | Реальный GGUF picker, context/GPU, lifecycle status и явный перенос endpoint в настройки. |
| [apps/desktop/src/LolaAvatar.tsx](../../apps/desktop/src/LolaAvatar.tsx) | Чиби по референсу: выбор ряда атласа 4×7 по состоянию Лолы, подпись, речевая волна и уменьшение движения. |
| [apps/desktop/src/MemoryPanel.tsx](../../apps/desktop/src/MemoryPanel.tsx) | Редактор семи полей памяти выбранного проекта с сохранением draft при конфликте. |
| [apps/desktop/src/ModelSettings.tsx](../../apps/desktop/src/ModelSettings.tsx) | Общее окно Neutral с боковыми разделами моделей, Лолы, расширений, ПК, оформления, контекста и runtime. |
| [apps/desktop/src/NeuralAudio.tsx](../../apps/desktop/src/NeuralAudio.tsx) | Единый плеер нейроозвучки: PCM WAV из Core, громкость/темп, Stop и подтверждение завершения. |
| [apps/desktop/src/OptionalIdePanel.tsx](../../apps/desktop/src/OptionalIdePanel.tsx) | Модальная тематическая панель исследователя/LSP/worktrees/изоляции с бюджетами, подтверждением, отменой и явным добавлением отчёта в задачу. |
| [apps/desktop/src/ProjectKnowledgePanel.tsx](../../apps/desktop/src/ProjectKnowledgePanel.tsx) | Редактор решений, фактов и гипотез; источники, статусы актуальности, поиск, исправление и удаление без model calls. |
| [apps/desktop/src/ProjectSearch.tsx](../../apps/desktop/src/ProjectSearch.tsx) | Боковой поиск и Ctrl+P: один IPC-запрос за раз, отмена и защита от устаревших результатов. |
| [apps/desktop/src/RunHistory.tsx](../../apps/desktop/src/RunHistory.tsx) | История epochs выбранного чата, физические HTTP попытки, известный usage, текущие оценки и время ожиданий. |
| [apps/desktop/src/SourceContextPreview.tsx](../../apps/desktop/src/SourceContextPreview.tsx) | Читаемый предпросмотр получателя, модели, диапазонов и полного текста автоматически выбранных исходников перед одной отправкой. |
| [apps/desktop/src/StorageSettings.tsx](../../apps/desktop/src/StorageSettings.tsx) | История и копии в настройках: проверка целостности, счётчики миграции, локальный ZIP export и явные ошибки. |
| [apps/desktop/src/StudioControls.tsx](../../apps/desktop/src/StudioControls.tsx) | Сохраняемая раскладка, доступные разделители панелей, модель под запросом, журнал инструментов и фокус модальных окон. |
| [apps/desktop/src/StudioFileTree.tsx](../../apps/desktop/src/StudioFileTree.tsx) | Ленивое настоящее дерево проекта с защитой от устаревших ответов после смены папки. |
| [apps/desktop/src/SubagentSettings.tsx](../../apps/desktop/src/SubagentSettings.tsx) | Настройки исследователей: профиль, инструкция, инструменты чтения, включение, удаление и общий переключатель. |
| [apps/desktop/src/TaskGraphPanel.tsx](../../apps/desktop/src/TaskGraphPanel.tsx) | Current task graph and trusted user editor with dependency/check selection; no direct effect execution. |
| [apps/desktop/src/TaskProgress.tsx](../../apps/desktop/src/TaskProgress.tsx) | Типизированная панель этапов, инструментов, результатов и продолжения задачи. |
| [apps/desktop/src/VoicePanel.tsx](../../apps/desktop/src/VoicePanel.tsx) | Рабочий разговор с Лолой без file tools, системная озвучка, голос/темп/громкость/Stop и честный отключённый STT. |
| [apps/desktop/src/VoiceSettings.tsx](../../apps/desktop/src/VoiceSettings.tsx) | Общая страница голоса Лолы с громкостью, скоростью, автоматической озвучкой и расширенной конфигурацией. |
| [apps/desktop/src/WakeListener.tsx](../../apps/desktop/src/WakeListener.tsx) | Явно включаемый микрофон во всех режимах: speech gate, STT, wake phrase, пауза при задаче/озвучке/ручной записи. |
| [apps/desktop/src/Welcome.tsx](../../apps/desktop/src/Welcome.tsx) | Пустое состояние Neutral с короткими сценариями и переходом в IDE. |
| [apps/desktop/src/WorkspaceAccessSettings.tsx](../../apps/desktop/src/WorkspaceAccessSettings.tsx) | Форма точечных разрешений файлов для модели в возможностях IDE с явным подтверждением передачи содержимого. |
| [apps/desktop/src/WorkspaceReview.tsx](../../apps/desktop/src/WorkspaceReview.tsx) | Список наборов правок, обратный diff, подтверждение отката и явное предупреждение конфликтов. |
| [apps/desktop/src/assets/leshy/autumn-birch-preview.webp](../../apps/desktop/src/assets/leshy/autumn-birch-preview.webp) | Уменьшенное preview фона autumn-birch для выбора оформления. |
| [apps/desktop/src/assets/leshy/autumn-birch.webp](../../apps/desktop/src/assets/leshy/autumn-birch.webp) | Ресурс LESHY: осенняя берёза. |
| [apps/desktop/src/assets/leshy/band-forest.svg](../../apps/desktop/src/assets/leshy/band-forest.svg) | Векторный мотив LESHY: band-forest. |
| [apps/desktop/src/assets/leshy/band-parchment.svg](../../apps/desktop/src/assets/leshy/band-parchment.svg) | Векторный мотив LESHY: band-parchment. |
| [apps/desktop/src/assets/leshy/band-twilight.svg](../../apps/desktop/src/assets/leshy/band-twilight.svg) | Векторный мотив LESHY: band-twilight. |
| [apps/desktop/src/assets/leshy/birch-cutout.webp](../../apps/desktop/src/assets/leshy/birch-cutout.webp) | Ресурс LESHY: берёза с прозрачностью. |
| [apps/desktop/src/assets/leshy/border.svg](../../apps/desktop/src/assets/leshy/border.svg) | Векторный мотив LESHY: border. |
| [apps/desktop/src/assets/leshy/corner.svg](../../apps/desktop/src/assets/leshy/corner.svg) | Векторный мотив LESHY: corner. |
| [apps/desktop/src/assets/leshy/diamond.svg](../../apps/desktop/src/assets/leshy/diamond.svg) | Векторный мотив LESHY: diamond. |
| [apps/desktop/src/assets/leshy/forest-depth-preview.webp](../../apps/desktop/src/assets/leshy/forest-depth-preview.webp) | Уменьшенное preview фона forest-depth для выбора оформления. |
| [apps/desktop/src/assets/leshy/forest-depth.webp](../../apps/desktop/src/assets/leshy/forest-depth.webp) | Ресурс LESHY: глубокий лесной фон. |
| [apps/desktop/src/assets/leshy/forest-preview.webp](../../apps/desktop/src/assets/leshy/forest-preview.webp) | Уменьшенное preview фона forest для выбора оформления. |
| [apps/desktop/src/assets/leshy/forest.webp](../../apps/desktop/src/assets/leshy/forest.webp) | Ресурс LESHY: лесной фон. |
| [apps/desktop/src/assets/leshy/painted-spots.json](../../apps/desktop/src/assets/leshy/painted-spots.json) | Манифест подготовленных живописных иллюстраций LESHY. |
| [apps/desktop/src/assets/leshy/parchment-preview.webp](../../apps/desktop/src/assets/leshy/parchment-preview.webp) | Уменьшенное preview фона parchment для выбора оформления. |
| [apps/desktop/src/assets/leshy/parchment.webp](../../apps/desktop/src/assets/leshy/parchment.webp) | Ресурс LESHY: светлый фон. |
| [apps/desktop/src/assets/leshy/rosette.svg](../../apps/desktop/src/assets/leshy/rosette.svg) | Векторный мотив LESHY: rosette. |
| [apps/desktop/src/assets/leshy/spot-archive-painted.webp](../../apps/desktop/src/assets/leshy/spot-archive-painted.webp) | Ресурс LESHY: живописный архив. |
| [apps/desktop/src/assets/leshy/spot-birch-painted.webp](../../apps/desktop/src/assets/leshy/spot-birch-painted.webp) | Ресурс LESHY: живописная берёза. |
| [apps/desktop/src/assets/leshy/spot-fern-painted.webp](../../apps/desktop/src/assets/leshy/spot-fern-painted.webp) | Ресурс LESHY: живописный папоротник. |
| [apps/desktop/src/assets/leshy/spot-mushrooms-painted.webp](../../apps/desktop/src/assets/leshy/spot-mushrooms-painted.webp) | Ресурс LESHY: живописные грибы. |
| [apps/desktop/src/assets/leshy/twilight-preview.webp](../../apps/desktop/src/assets/leshy/twilight-preview.webp) | Уменьшенное preview фона twilight для выбора оформления. |
| [apps/desktop/src/assets/leshy/twilight.webp](../../apps/desktop/src/assets/leshy/twilight.webp) | Ресурс LESHY: сумеречный фон. |
| [apps/desktop/src/assets/leshy/undergrowth-cutout.webp](../../apps/desktop/src/assets/leshy/undergrowth-cutout.webp) | Ресурс LESHY: лесной подлесок с прозрачностью. |
| [apps/desktop/src/assets/lola-chibi-atlas-v1.png](../../apps/desktop/src/assets/lola-chibi-atlas-v1.png) | Прозрачный атлас из 28 кадров в сетке 4×7 для семи состояний чиби Лолы. |
| [apps/desktop/src/assets/lola-chibi-atlas-v2.json](../../apps/desktop/src/assets/lola-chibi-atlas-v2.json) | Проверенные source rectangles всех 28 персонажей: SVG переносит их целиком на общий canvas с полями. |
| [apps/desktop/src/assets/lola-chibi-atlas-v2.png](../../apps/desktop/src/assets/lola-chibi-atlas-v2.png) | Новый исходный transparent PNG атлас 28 полных поз Лолы; не изменяется renderer-кодом. |
| [apps/desktop/src/assets/lola-chibi-atlas-v2.prompt.md](../../apps/desktop/src/assets/lola-chibi-atlas-v2.prompt.md) | Точный imagegen prompt и происхождение версии v2; исходный PNG сохранён без растровых правок. |
| [apps/desktop/src/assets/lola-chibi-concept-v1.png](../../apps/desktop/src/assets/lola-chibi-concept-v1.png) | Сгенерированный прозрачный полнофигурный концепт чиби Лолы; источник imagegen и промпт описаны рядом. |
| [apps/desktop/src/assets/lola-chibi.prompt.md](../../apps/desktop/src/assets/lola-chibi.prompt.md) | Точные промпты и происхождение concept/sprite atlas; пользовательский исходный AVIF сюда не копируется. |
| [apps/desktop/src/assets/miya-states.png](../../apps/desktop/src/assets/miya-states.png) | Прозрачный 4×2 атлас поз светловолосой аниме-горничной по пользовательскому референсу. |
| [apps/desktop/src/assets/miya-states.prompt.md](../../apps/desktop/src/assets/miya-states.prompt.md) | Сохранённые prompts встроенного image_gen и схема ячеек персонажа. |
| [apps/desktop/src/design/ForestSpot.tsx](../../apps/desktop/src/design/ForestSpot.tsx) | Иллюстративные акценты LESHY из подготовленных прозрачных WebP. |
| [apps/desktop/src/design/Ornaments.tsx](../../apps/desktop/src/design/Ornaments.tsx) | Общие SVG-мотивы рамок, углов, разделителей и лесного акцента. |
| [apps/desktop/src/design/ide-theme.css](../../apps/desktop/src/design/ide-theme.css) | Токены оформления IDE для трёх тем LESHY. |
| [apps/desktop/src/design/leshy-dialogs.css](../../apps/desktop/src/design/leshy-dialogs.css) | Оформление вложенных окон, подтверждений и настроек. |
| [apps/desktop/src/design/leshy-illustrations.css](../../apps/desktop/src/design/leshy-illustrations.css) | Размещение иллюстраций LESHY с отключаемыми фонами. |
| [apps/desktop/src/design/leshy-lola.css](../../apps/desktop/src/design/leshy-lola.css) | Применение LESHY к прозрачному окну и bubble Лолы. |
| [apps/desktop/src/design/leshy-motifs.css](../../apps/desktop/src/design/leshy-motifs.css) | Орнаменты и стыки панелей без перекрытия рабочего текста. |
| [apps/desktop/src/design/leshy-workspace.css](../../apps/desktop/src/design/leshy-workspace.css) | Оформление главного рабочего пространства LESHY. |
| [apps/desktop/src/design/leshy.css](../../apps/desktop/src/design/leshy.css) | Базовая палитра и общие поверхности LESHY. |
| [apps/desktop/src/design/themes.ts](../../apps/desktop/src/design/themes.ts) | Типы, нормализация и применение трёх тем LESHY. |
| [apps/desktop/src/ideEntry.ts](../../apps/desktop/src/ideEntry.ts) | Адаптер API Code-OSS webview к общему window.lca. |
| [apps/desktop/src/idePanel/acceptanceChecks.ts](../../apps/desktop/src/idePanel/acceptanceChecks.ts) | Подготовка существующих IdeOptions, изоляция draft по chat_id и readonly/resume guard без нового executor. |
| [apps/desktop/src/idePanel/acceptanceSettings.tsx](../../apps/desktop/src/idePanel/acceptanceSettings.tsx) | Независимый editor критериев, команд, scopes и ручного запуска checks_only в новой IDE. |
| [apps/desktop/src/idePanel/connectionSettings.tsx](../../apps/desktop/src/idePanel/connectionSettings.tsx) | Самостоятельная форма подключения и оформления; редактируемые настройки отделены от сохранённых. |
| [apps/desktop/src/idePanel/entry.tsx](../../apps/desktop/src/idePanel/entry.tsx) | Монтирует независимый AgentWorkspace и его стили. |
| [apps/desktop/src/idePanel/recoveryDiagnostics.ts](../../apps/desktop/src/idePanel/recoveryDiagnostics.ts) | Общий recovery gate и минимальная диагностика по allowlist без текста, путей и ключей. |
| [apps/desktop/src/idePanel/runActivity.tsx](../../apps/desktop/src/idePanel/runActivity.tsx) | Карточки этапов, инструментов, проверок и разрешения неизвестных эффектов. |
| [apps/desktop/src/idePanel/sessionState.ts](../../apps/desktop/src/idePanel/sessionState.ts) | Типы состояния новой панели и чистое преобразование событий с chat/run/sequence isolation. |
| [apps/desktop/src/idePanel/workspace.css](../../apps/desktop/src/idePanel/workspace.css) | Адаптивные стили независимой IDE-панели и approvals. |
| [apps/desktop/src/idePanel/workspace.tsx](../../apps/desktop/src/idePanel/workspace.tsx) | Независимая панель диалога, истории, подключений и действий агента. |
| [apps/desktop/src/lola-main.tsx](../../apps/desktop/src/lola-main.tsx) | Создаёт React root отдельного спутника и загружает только companion stylesheet. |
| [apps/desktop/src/main.tsx](../../apps/desktop/src/main.tsx) | Подключает CSS, создаёт React root и отображает App в StrictMode. |
| [apps/desktop/src/microphone.ts](../../apps/desktop/src/microphone.ts) | 16 kHz mono PCM16 WAV: подавление шума, блоки 64 мс, завершение по паузе, обрезка тишины и освобождение микрофона. |
| [apps/desktop/src/style.css](../../apps/desktop/src/style.css) | Стили IDE-панелей, сообщений, формы, modal и индикатора streaming. |
| [apps/desktop/src/styles/base.css](../../apps/desktop/src/styles/base.css) | Базовые панели, редактор, сообщения, подтверждения и карточки задачи; начало сохранённого CSS-каскада. |
| [apps/desktop/src/styles/companion.css](../../apps/desktop/src/styles/companion.css) | Сетка ассистента, атлас состояний и модальное окно настроек голоса. |
| [apps/desktop/src/styles/lola-desktop.css](../../apps/desktop/src/styles/lola-desktop.css) | Стили компактного прозрачного окна спутника, bubble и hit areas без ограничений основной IDE ширины. |
| [apps/desktop/src/styles/lola-sprites.css](../../apps/desktop/src/styles/lola-sprites.css) | Кадровые CSS-анимации семи состояний чиби-атласа и поддержка reduced-motion. |
| [apps/desktop/src/styles/modern.css](../../apps/desktop/src/styles/modern.css) | Актуальные токены тёмной/светлой темы, акценты, плотность, скрытие панелей и розовое оформление Лолы. |
| [apps/desktop/src/styles/neutral.css](../../apps/desktop/src/styles/neutral.css) | Общий дизайн Neutral: токены тем, боковая навигация, проекты, настройки, адаптация размера и reduced motion. |
| [apps/desktop/src/styles/studio.css](../../apps/desktop/src/styles/studio.css) | Графитово-мятная дизайн-система и рабочая компоновка IDE, Chat, настроек и узких окон. |
| [apps/desktop/src/styles/workspaces.css](../../apps/desktop/src/styles/workspaces.css) | Расположение Chat/IDE, общие окна и компоненты; сохранённый каскад без устаревших SVG-селекторов. |
| [apps/desktop/src/useLolaSession.tsx](../../apps/desktop/src/useLolaSession.tsx) | Независимая голосовая сессия popup Лолы: загрузка, live events, отправка, остановка, approval и recovery. |
| [apps/desktop/src/useTaskSession.ts](../../apps/desktop/src/useTaskSession.ts) | Состояние разговора и жизненного цикла UI; отбрасывание поздних/чужих событий и редукция stream/task_end. |
| [apps/desktop/src/vite-env.d.ts](../../apps/desktop/src/vite-env.d.ts) | Vite reference, CoreEvent и TypeScript-контракт Window.lca. |
| [apps/desktop/src/voiceText.ts](../../apps/desktop/src/voiceText.ts) | Очистка презентационной разметки потокового ответа Лолы перед показом и озвучкой. |
| [apps/desktop/src/wakePhrase.ts](../../apps/desktop/src/wakePhrase.ts) | Нормализация русской фразы и выделение команды только после совпадающего начала без потери пунктуации команды. |
| [apps/desktop/tsconfig.electron.json](../../apps/desktop/tsconfig.electron.json) | Статическая проверка Node/Electron main и preload без emit. |
| [apps/desktop/tsconfig.json](../../apps/desktop/tsconfig.json) | Статическая проверка React/DOM/JSX-кода renderer. |
| [apps/desktop/vite.config.ts](../../apps/desktop/vite.config.ts) | React-плагин, относительные assets, фиксированный локальный dev-порт и outDir. |
| [assets/leshy-sources/PROMPTS.md](../../assets/leshy-sources/PROMPTS.md) | Промпты и происхождение исходных растровых материалов LESHY. |
| [assets/leshy-sources/birch-cutout.png](../../assets/leshy-sources/birch-cutout.png) | Сохранённый исходный визуальный материал LESHY: birch-cutout. |
| [assets/leshy-sources/forest.png](../../assets/leshy-sources/forest.png) | Сохранённый исходный визуальный материал LESHY: forest. |
| [assets/leshy-sources/parchment.png](../../assets/leshy-sources/parchment.png) | Сохранённый исходный визуальный материал LESHY: parchment. |
| [assets/leshy-sources/twilight.png](../../assets/leshy-sources/twilight.png) | Сохранённый исходный визуальный материал LESHY: twilight. |
| [assets/leshy-sources/undergrowth-cutout.png](../../assets/leshy-sources/undergrowth-cutout.png) | Сохранённый исходный визуальный материал LESHY: undergrowth-cutout. |
| [assets/leshy-sources/user-antler-reference.png](../../assets/leshy-sources/user-antler-reference.png) | Сохранённый исходный визуальный материал LESHY: user-antler-reference. |
| [assets/leshy.ico](../../assets/leshy.ico) | Основной знак LESHY для приложения в формате ico. |
| [assets/leshy.png](../../assets/leshy.png) | Основной знак LESHY для приложения в формате png. |
| [assets/leshy.svg](../../assets/leshy.svg) | Основной знак LESHY для приложения в формате svg. |
| [assets/neutral.ico](../../assets/neutral.ico) | Многоразмерная иконка установщика/Windows: PNG-кадры от 16 до 256 пикселей. |
| [assets/neutral.png](../../assets/neutral.png) | Иконка окна Neutral, 512 пикселей, полученная из исходного SVG. |
| [assets/neutral.svg](../../assets/neutral.svg) | Редактируемый векторный исходник знака приложения и его фона. |
| [codex-skills.mjs](../../codex-skills.mjs) | Сторонний bundled Codex Skills CLI (MIT); учитывается как файл, его внутренности не являются API приложения. |
| [core/python/assistant_service.py](../../core/python/assistant_service.py) | Локальные часы, ограниченный AST-калькулятор, атомарные заметки и отменяемые таймеры Лолы. |
| [core/python/background_job.py](../../core/python/background_job.py) | Один отменяемый maintenance worker вне синхронного dispatch/TaskService.lock. |
| [core/python/bridge.py](../../core/python/bridge.py) | JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout. |
| [core/python/conversation_service.py](../../core/python/conversation_service.py) | Операции организации чатов с проверкой пространства, режима и корня файлов. |
| [core/python/desktop_service.py](../../core/python/desktop_service.py) | Явно включаемые PC tools: human-prompt folder grants, read-only файлы, bounded web search и host screenshot broker. |
| [core/python/editor_service.py](../../core/python/editor_service.py) | Ручной editor-протокол: strict UTF-8 чтение с revision, preview, одноразовый Apply через существующую атомарную snapshot-запись. |
| [core/python/extension_service.py](../../core/python/extension_service.py) | Единый реестр разрешённых возможностей, progressive skills, импорт пакетов и снимки для одного запуска. |
| [core/python/ide_completion.py](../../core/python/ide_completion.py) | Небольшой локальный запрос автодополнения без инструментов с проверкой контекста. |
| [core/python/ide_sessions.py](../../core/python/ide_sessions.py) | Изолированные представления единого Core и editor-owned операции через scoped adapter. |
| [core/python/memory_service.py](../../core/python/memory_service.py) | Строгий read/edit API памяти проекта с byte revision и защитой повреждённых файлов. |
| [core/python/neural_speech.py](../../core/python/neural_speech.py) | Отменяемый HTTP TTS: bounded PCM WAV, события звука и точное подтверждение плеера по sequence. |
| [core/python/optional_ide_service.py](../../core/python/optional_ide_service.py) | Настройки выключенных по умолчанию возможностей, один фоновый job, shared inference lease, отмена и независимые адаптеры. |
| [core/python/project_search.py](../../core/python/project_search.py) | Асинхронный cancellable GUI worker над общим agent.workspace_search; самостоятельного второго алгоритма поиска нет. |
| [core/python/protocol.py](../../core/python/protocol.py) | Версия критического RPC, проверка входного envelope, run IDs, решений и confirmed до dispatch. |
| [core/python/run_session.py](../../core/python/run_session.py) | Independent session owner and frozen connection for one foreground/background run, with live snapshot and stream cursor. |
| [core/python/runtime_service.py](../../core/python/runtime_service.py) | Неблокирующий сервис запуска/остановки GGUF и состояний собственного llama-server. |
| [core/python/session_service.py](../../core/python/session_service.py) | Выбор, scoped список/переименование/перенос чатов и восстановление canonical history отдельно от inference. |
| [core/python/speech_service.py](../../core/python/speech_service.py) | Windows System.Speech через фиксированный PowerShell script и stdin JSON: каталог, TTS, Stop и owned job. |
| [core/python/task_execution.py](../../core/python/task_execution.py) | Run-owned engine loop, tool dispatch, streaming timers, persistence and exact approval correlation; no UI selection state. |
| [core/python/task_service.py](../../core/python/task_service.py) | Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval. |
| [core/python/telegram_service.py](../../core/python/telegram_service.py) | Telegram long polling только для owner user ID: команды, состояние, ответы и текущие diff/approval; токен только в памяти Core. |
| [core/python/transcription_service.py](../../core/python/transcription_service.py) | Ограниченная WAV-транскрипция через локальный whisper.cpp или совместимый API с отменой HTTP. |
| [core/python/workspace_review.py](../../core/python/workspace_review.py) | Пользовательский API compare/preview/confirm/review; модели не получают инструмент отката. |
| [design_reference/DESIGN_REFERENCE.md](../../design_reference/DESIGN_REFERENCE.md) | Пояснение сохранённого визуального эталона и границ его переноса. |
| [design_reference/agent_studio_reference.py](../../design_reference/agent_studio_reference.py) | Архивный визуальный прототип с собственными механизмами; не импортируется рабочим main.py. |
| [docs.zip](../../docs.zip) | Локальный пользовательский архив документации; сохранён без изменений, приложение не использует его как исходник или настройку. |
| [docs/01-project-and-setup.md](../../docs/01-project-and-setup.md) | Ручная учебная глава или исторический материал: 1. Назначение проекта и запуск. |
| [docs/02-technologies.md](../../docs/02-technologies.md) | Ручная учебная глава или исторический материал: 2. Технологии и их роль. |
| [docs/03-architecture.md](../../docs/03-architecture.md) | Ручная учебная глава или исторический материал: 3. Архитектура и границы ответственности. |
| [docs/04-development-history.md](../../docs/04-development-history.md) | Ручная учебная глава или исторический материал: 4. Этапы развития и использованные решения. |
| [docs/05-request-walkthrough.md](../../docs/05-request-walkthrough.md) | Ручная учебная глава или исторический материал: 5. Один запрос от кнопки до результата. |
| [docs/06-python-core.md](../../docs/06-python-core.md) | Ручная учебная глава или исторический материал: 6. Python-ядро: классы, алгоритмы и данные. |
| [docs/07-desktop-and-ui.md](../../docs/07-desktop-and-ui.md) | Ручная учебная глава или исторический материал: 7. Интерфейс, Electron и сборка. |
| [docs/08-protocols.md](../../docs/08-protocols.md) | Ручная учебная глава или исторический материал: 8. API и протоколы. |
| [docs/09-data-and-security.md](../../docs/09-data-and-security.md) | Ручная учебная глава или исторический материал: 9. Хранилища, файлы и разрешения. |
| [docs/10-testing-and-debugging.md](../../docs/10-testing-and-debugging.md) | Ручная учебная глава или исторический материал: 10. Проверки и диагностика. |
| [docs/11-current-status.md](../../docs/11-current-status.md) | Ручная учебная глава или исторический материал: Текущее состояние LESHY. |
| [docs/12-development-guide.md](../../docs/12-development-guide.md) | Ручная учебная глава или исторический материал: 12. Как развивать проект и документацию. |
| [docs/13-learning-path.md](../../docs/13-learning-path.md) | Ручная учебная глава или исторический материал: 13. Учебный маршрут и словарь. |
| [docs/14-windows-packaging.md](../../docs/14-windows-packaging.md) | Ручная учебная глава или исторический материал: 14. Windows-сборка со встроенным Python Core. |
| [docs/15-task-progress.md](../../docs/15-task-progress.md) | Ручная учебная глава или исторический материал: 15. План задачи, инструменты и результаты. |
| [docs/16-workspaces-and-answer-recovery.md](../../docs/16-workspaces-and-answer-recovery.md) | Ручная учебная глава или исторический материал: 16. Три режима и восстановление пустого ответа. |
| [docs/17-model-settings-and-theme.md](../../docs/17-model-settings-and-theme.md) | Ручная учебная глава или исторический материал: 17. Настройка модели и общая палитра. |
| [docs/18-editor.md](../../docs/18-editor.md) | Ручная учебная глава или исторический материал: 18. Рабочий редактор IDE. |
| [docs/19-project-search.md](../../docs/19-project-search.md) | Ручная учебная глава или исторический материал: 19. Поиск по проекту и быстрое открытие. |
| [docs/20-local-runtime.md](../../docs/20-local-runtime.md) | Ручная учебная глава или исторический материал: 20. Локальная GGUF-модель внутри приложения. |
| [docs/21-memory-and-chat.md](../../docs/21-memory-and-chat.md) | Ручная учебная глава или исторический материал: 21. Память проекта и читаемый чат. |
| [docs/22-voice-companion.md](../../docs/22-voice-companion.md) | Ручная учебная глава или исторический материал: 22. Мия: разговор и системная озвучка. |
| [docs/23-autonomous-verification.md](../../docs/23-autonomous-verification.md) | Ручная учебная глава или исторический материал: 23. Результаты автономного сеанса 23 октября. |
| [docs/24-full-windows-installer.md](../../docs/24-full-windows-installer.md) | Ручная учебная глава или исторический материал: 24. Полный установщик Windows 6.0.1. |
| [docs/25-json-tools-and-cache.md](../../docs/25-json-tools-and-cache.md) | Ручная учебная глава или исторический материал: 25. Области чатов, JSON tool calling и квантование KV-кеша. |
| [docs/26-miya-model-and-stt.md](../../docs/26-miya-model-and-stt.md) | Ручная учебная глава или исторический материал: 26. Мия: характер, своя модель, голос и распознавание. |
| [docs/27-desktop-and-telegram.md](../../docs/27-desktop-and-telegram.md) | Ручная учебная глава или исторический материал: 27. Инструменты ПК и Telegram. |
| [docs/28-expansion-validation.md](../../docs/28-expansion-validation.md) | Ручная учебная глава или исторический материал: Проверка расширения 6.1. |
| [docs/29-neural-voice-and-wake.md](../../docs/29-neural-voice-and-wake.md) | Ручная учебная глава или исторический материал: 29. Нейроозвучка Мии и фраза активации. |
| [docs/30-miya-gpu-and-applications.md](../../docs/30-miya-gpu-and-applications.md) | Ручная учебная глава или исторический материал: 30. Мия 6.3: ускорение GPU, приложения и поиск. |
| [docs/31-miya-serena-and-character.md](../../docs/31-miya-serena-and-character.md) | Озвучка Serena по умолчанию, управление локальным Piper, простые настройки и состояния анимированного персонажа. |
| [docs/32-miya-settings-and-voice-input.md](../../docs/32-miya-settings-and-voice-input.md) | Диалог настроек Лолы, RMS-порог, завершение по паузе, обрезка PCM, автоотправка, отмена и измерения STT. |
| [docs/33-lola-refactor-and-appearance.md](../../docs/33-lola-refactor-and-appearance.md) | Ручная учебная глава или исторический материал: Лола, оформление и рефакторинг, 6.6. |
| [docs/34-ide-roles-and-model-lifecycle.md](../../docs/34-ide-roles-and-model-lifecycle.md) | Ручная учебная глава или исторический материал: IDE: дирижёр, код, сборка и проверка, 6.7. |
| [docs/35-smart-context-and-lola-tools.md](../../docs/35-smart-context-and-lola-tools.md) | Ручная учебная глава или исторический материал: 35. Умный контекст и повседневные инструменты Лолы. |
| [docs/36-neutral-guide.md](../../docs/36-neutral-guide.md) | Ручная учебная глава или исторический материал: Neutral 7: интерфейс, модели и Лола. |
| [docs/37-neutral-core-and-extensions.md](../../docs/37-neutral-core-and-extensions.md) | Ручная учебная глава или исторический материал: Neutral: ядро, расширения и проверка действий. |
| [docs/38-neutral-projects-and-conversations.md](../../docs/38-neutral-projects-and-conversations.md) | Ручная учебная глава или исторический материал: Neutral: проекты, разговоры и хранение. |
| [docs/39-neutral-validation.md](../../docs/39-neutral-validation.md) | Ручная учебная глава или исторический материал: Neutral 7.0.0: проверка итоговой сборки. |
| [docs/40-core-audit-and-roadmap.md](../../docs/40-core-audit-and-roadmap.md) | Ручная учебная глава или исторический материал: Аудит ядра Neutral и план развития. |
| [docs/41-core-reliability-stage-one.md](../../docs/41-core-reliability-stage-one.md) | Ручная учебная глава или исторический материал: Первый этап: надёжность ответов, инструментов и MCP. |
| [docs/42-core-execution-and-recovery.md](../../docs/42-core-execution-and-recovery.md) | Ручная учебная глава или исторический материал: Этап 2: исполнение и восстановление инструментов. |
| [docs/43-context-budget-and-economy.md](../../docs/43-context-budget-and-economy.md) | Ручная учебная глава или исторический материал: Этап 3: полный бюджет контекста и экономия. |
| [docs/44-ide-tools-and-progress-panel.md](../../docs/44-ide-tools-and-progress-panel.md) | Ручная учебная глава или исторический материал: Этап 4: инструменты IDE и закрытие подробностей. |
| [docs/45-transactional-storage-and-migration.md](../../docs/45-transactional-storage-and-migration.md) | Ручная учебная глава или исторический материал: Этап 5: транзакционное хранилище, миграция и резервные копии. |
| [docs/46-ide-acceptance-and-rollback.md](../../docs/46-ide-acceptance-and-rollback.md) | Ручная учебная глава или исторический материал: Этап 6: критерии готовности, проверки и откат IDE. |
| [docs/47-session-services-and-mcp.md](../../docs/47-session-services-and-mcp.md) | Ручная учебная глава или исторический материал: Этап 7: сессии, протокол и общий жизненный цикл. |
| [docs/48-optional-ide-capabilities.md](../../docs/48-optional-ide-capabilities.md) | Ручная учебная глава или исторический материал: Этап 8: дополнительные возможности IDE. |
| [docs/49-post-stage8-audit-and-next-plan.md](../../docs/49-post-stage8-audit-and-next-plan.md) | Ручная учебная глава или исторический материал: Аудит после этапов 7–8 и следующий план Neutral. |
| [docs/50-subagents-plan.md](../../docs/50-subagents-plan.md) | Ручная учебная глава или исторический материал: План пользовательских и создаваемых моделью субагентов. |
| [docs/51-text-tool-agency-plan.md](../../docs/51-text-tool-agency-plan.md) | Ручная учебная глава или исторический материал: План агентской работы моделей без native tool calling. |
| [docs/52-full-ide-and-vscode-extensions-plan.md](../../docs/52-full-ide-and-vscode-extensions-plan.md) | Ручная учебная глава или исторический материал: План полноценной IDE и расширений VS Code. |
| [docs/53-desktop-lola.md](../../docs/53-desktop-lola.md) | Ручная учебная глава или исторический материал: Настольная Лола: окно, трэй и чиби-анимации. |
| [docs/54-core-reliability-stage9.md](../../docs/54-core-reliability-stage9.md) | Ручная учебная глава или исторический материал: Этап 9: надёжность после повторного аудита. |
| [docs/55-automatic-context-and-lola-layout.md](../../docs/55-automatic-context-and-lola-layout.md) | Ручная учебная глава или исторический материал: Автоматический контекст и размещение Лолы. |
| [docs/56-roadmap-review-2026-10-27.md](../../docs/56-roadmap-review-2026-10-27.md) | Ручная учебная глава или исторический материал: Вердикт по обновлённой дорожной карте Neutral. |
| [docs/57-roadmap-v2.md](../../docs/57-roadmap-v2.md) | Ручная учебная глава или исторический материал: Neutral — Roadmap v2. |
| [docs/58-agent-baseline-20a.md](../../docs/58-agent-baseline-20a.md) | Ручная учебная глава или исторический материал: Этап 20a: воспроизводимый baseline реального агента. |
| [docs/59-json-compatibility-stage10.md](../../docs/59-json-compatibility-stage10.md) | Ручная учебная глава или исторический материал: Этап 10: JSON compatibility на реальной локальной модели. |
| [docs/60-scoped-verification-evidence.md](../../docs/60-scoped-verification-evidence.md) | Ручная учебная глава или исторический материал: Проверяемая область команды перед Project Intelligence. |
| [docs/61-project-intelligence-index.md](../../docs/61-project-intelligence-index.md) | Ручная учебная глава или исторический материал: Этап 13a: индекс сохранённых исходников проекта. |
| [docs/62-context-pack.md](../../docs/62-context-pack.md) | Ручная учебная глава или исторический материал: 62. ContextPack: подбор источников и подтверждение передачи. |
| [docs/63-run-registry-scheduler-ledger.md](../../docs/63-run-registry-scheduler-ledger.md) | Ручная учебная глава или исторический материал: 63. Этап 11a: Run Registry, очередь генераций и учёт расхода. |
| [docs/64-background-chat-runs.md](../../docs/64-background-chat-runs.md) | Ручная учебная глава или исторический материал: 64. Независимые фоновые чаты — следующий срез 11b. |
| [docs/65-process-identity-and-restart.md](../../docs/65-process-identity-and-restart.md) | Ручная учебная глава или исторический материал: 65. Владелец процесса и восстановление после аварии — 11c. |
| [docs/66-stage11-complete.md](../../docs/66-stage11-complete.md) | Ручная учебная глава или исторический материал: 66. Завершение этапа 11: исполнение дерева, ресурсы и расход. |
| [docs/67-taskgraph-and-long-tasks.md](../../docs/67-taskgraph-and-long-tasks.md) | Ручная учебная глава или исторический материал: 67. Этап 15: TaskGraph, evidence и долгие задачи. |
| [docs/68-subagent-profiles.md](../../docs/68-subagent-profiles.md) | Ручная учебная глава или исторический материал: Этап 12: создаваемые профили субагентов. |
| [docs/69-answer-quality.md](../../docs/69-answer-quality.md) | Ручная учебная глава или исторический материал: Качество ответов: измерения и первые исправления. |
| [docs/70-studio-installer-7.0.1.md](../../docs/70-studio-installer-7.0.1.md) | Ручная учебная глава или исторический материал: Neutral 7.0.1: прежний знак и установщик Studio. |
| [docs/71-project-memory-stage16.md](../../docs/71-project-memory-stage16.md) | Ручная учебная глава или исторический материал: Этап 16: память проекта и поиск по решениям. |
| [docs/72-verification-recovery-stage17.md](../../docs/72-verification-recovery-stage17.md) | Ручная учебная глава или исторический материал: Этап 17: расширенные проверки и восстановление. |
| [docs/73-neutral-ide-prototype.md](../../docs/73-neutral-ide-prototype.md) | Ручная учебная глава или исторический материал: 73. Neutral IDE: прототип отдельного приложения на Code-OSS. |
| [docs/74-native-ide-integration.md](../../docs/74-native-ide-integration.md) | Ручная учебная глава или исторический материал: Native IDE: панель агента и вход в редактор. |
| [docs/75-ide-panel-rebuild.md](../../docs/75-ide-panel-rebuild.md) | Ручная учебная глава или исторический материал: Новая панель IDE с нуля. |
| [docs/76-leshy-design-system.md](../../docs/76-leshy-design-system.md) | Ручная учебная глава или исторический материал: ЛЕШИЙ / LESHY — внедрение оформления. |
| [docs/77-leshy-ide-style-review.md](../../docs/77-leshy-ide-style-review.md) | Ручная учебная глава или исторический материал: LESHY IDE — оформление и визуальная проверка. |
| [docs/78-leshy-all-windows-review.md](../../docs/78-leshy-all-windows-review.md) | Ручная учебная глава или исторический материал: LESHY: окна и вложенные редакторы. |
| [docs/79-leshy-panel-ornaments-and-joins.md](../../docs/79-leshy-panel-ornaments-and-joins.md) | Ручная учебная глава или исторический материал: LESHY: панель агента, орнаменты и стыки. |
| [docs/80-leshy-painted-assets-and-motif-coverage.md](../../docs/80-leshy-painted-assets-and-motif-coverage.md) | Ручная учебная глава или исторический материал: LESHY: живописные ассеты и оформление всех семейств элементов. |
| [docs/81-project-audit-2026-11-03.md](../../docs/81-project-audit-2026-11-03.md) | Ручная учебная глава или исторический материал: Аудит LESHY / LocalAgent — 3 ноября 2026. |
| [docs/82-leshy-release-acceptance.md](../../docs/82-leshy-release-acceptance.md) | Ручная учебная глава или исторический материал: Приёмка свежего пакета LESHY — 3 ноября 2026. |
| [docs/83-agent-quality-baseline.md](../../docs/83-agent-quality-baseline.md) | Ручная учебная глава или исторический материал: Измеренный baseline агента — 3 ноября 2026. |
| [docs/84-development-wave-one.md](../../docs/84-development-wave-one.md) | Ручная учебная глава или исторический материал: Выполнение плана: проверки, документация и пакет LESHY. |
| [docs/85-recovery-and-session-state.md](../../docs/85-recovery-and-session-state.md) | Ручная учебная глава или исторический материал: Восстановление и состояние новой IDE-панели. |
| [docs/86-ide-acceptance-checks.md](../../docs/86-ide-acceptance-checks.md) | Ручная учебная глава или исторический материал: Проверки результата в новой IDE. |
| [docs/AGENT_KNOWN_LIMITATIONS.md](../../docs/AGENT_KNOWN_LIMITATIONS.md) | Ручная учебная глава или исторический материал: Agent known limitations — 2026-10-29. |
| [docs/AGENT_READINESS_AUDIT.md](../../docs/AGENT_READINESS_AUDIT.md) | Ручная учебная глава или исторический материал: Agent readiness audit — 2026-10-29. |
| [docs/AGENT_READINESS_RESULTS.md](../../docs/AGENT_READINESS_RESULTS.md) | Ручная учебная глава или исторический материал: Agent readiness results — 2026-10-29. |
| [docs/AGENT_READINESS_TESTS.md](../../docs/AGENT_READINESS_TESTS.md) | Ручная учебная глава или исторический материал: Agent readiness tests. |
| [docs/ANALYSIS_DEEP_PROJECT.md](../../docs/ANALYSIS_DEEP_PROJECT.md) | Ручная учебная глава или исторический материал: Глубокий анализ проекта LocalAgent (Neutral 7 / v7.0.1). |
| [docs/AUDIT_2026-10-24.md](../../docs/AUDIT_2026-10-24.md) | Ручная учебная глава или исторический материал: Проверка проекта от 24 октября 2026. |
| [docs/AUTONOMOUS_PLAN_2026-10-23.md](../../docs/AUTONOMOUS_PLAN_2026-10-23.md) | Ручная учебная глава или исторический материал: Автономный план LocalAgent — 23 октября 2026. |
| [docs/DESIGN_SYSTEM.md](../../docs/DESIGN_SYSTEM.md) | Ручная учебная глава или исторический материал: Дизайн-система Neutral — прототип. |
| [docs/EXPANSION_PLAN.md](../../docs/EXPANSION_PLAN.md) | Ручная учебная глава или исторический материал: План расширения LocalAgent. |
| [docs/NEURAL_VOICE_PLAN.md](../../docs/NEURAL_VOICE_PLAN.md) | Ручная учебная глава или исторический материал: План нейроозвучки и фразы активации. |
| [docs/NEUTRAL_PLAN_2026-10-25.md](../../docs/NEUTRAL_PLAN_2026-10-25.md) | Ручная учебная глава или исторический материал: Neutral: план сеанса 25 октября 2026. |
| [docs/README.md](../../docs/README.md) | Ручная учебная глава или исторический материал: LESHY: подробное руководство по проекту. |
| [docs/SERENA_TRAINING_PLAN.md](../../docs/SERENA_TRAINING_PLAN.md) | Разрешение, этапы и критерии пробной Serena, Windows окружение, provenance датасета, ограничения и восстановление обучения. |
| [docs/SUBAGENT_TRANSPARENCY_VALIDATION.md](../../docs/SUBAGENT_TRANSPARENCY_VALIDATION.md) | Ручная учебная глава или исторический материал: Subagent transparency and real-model validation — 2026-10-29. |
| [docs/UI_FUNCTIONAL_PROTOTYPE.md](../../docs/UI_FUNCTIONAL_PROTOTYPE.md) | Ручная учебная глава или исторический материал: Функциональный прототип Neutral. |
| [docs/UI_REDESIGN_PLAN.md](../../docs/UI_REDESIGN_PLAN.md) | Ручная учебная глава или исторический материал: План UI/UX-переработки Neutral. |
| [docs/UI_STUDIO_INTEGRATION.md](../../docs/UI_STUDIO_INTEGRATION.md) | Ручная учебная глава или исторический материал: Neutral Studio — интеграция утверждённого интерфейса. |
| [docs/UI_UX_AUDIT.md](../../docs/UI_UX_AUDIT.md) | Ручная учебная глава или исторический материал: Аудит интерфейса Neutral. |
| [docs/UI_UX_GAP_REVIEW.md](../../docs/UI_UX_GAP_REVIEW.md) | Ручная учебная глава или исторический материал: Проверка пропущенных деталей прототипа Neutral. |
| [docs/UI_VISUAL_REVIEW.md](../../docs/UI_VISUAL_REVIEW.md) | Ручная учебная глава или исторический материал: Отчёт о визуальной проверке прототипа. |
| [docs/WORK_PLAN.md](../../docs/WORK_PLAN.md) | Ручная учебная глава или исторический материал: План дальнейшей разработки LocalAgent. |
| [docs/history/legacy-readme.md](../../docs/history/legacy-readme.md) | Ручная учебная глава или исторический материал: Исторические README до учебной документации. |
| [docs/leshy-brief/01_LESHY_ASTRA_UI_REDESIGN.md](../../docs/leshy-brief/01_LESHY_ASTRA_UI_REDESIGN.md) | Ручная учебная глава или исторический материал: LESHY — промпт для GPT Astra: редизайн интерфейса. |
| [docs/leshy-brief/02_LESHY_ASSETS_GENERATION.md](../../docs/leshy-brief/02_LESHY_ASSETS_GENERATION.md) | Ручная учебная глава или исторический материал: LESHY — промпты для генерации орнаментов, фонов и UI-ассетов. |
| [docs/leshy-brief/03_LESHY_THEME_SYSTEM_GUIDE.md](../../docs/leshy-brief/03_LESHY_THEME_SYSTEM_GUIDE.md) | Ручная учебная глава или исторический материал: LESHY — технический гайд по темам и дизайн-системе. |
| [docs/leshy-brief/04_LESHY_LOGO_GENERATION.md](../../docs/leshy-brief/04_LESHY_LOGO_GENERATION.md) | Ручная учебная глава или исторический материал: Примечание к комплекту исходных материалов. |
| [docs/leshy-brief/README.md](../../docs/leshy-brief/README.md) | Ручная учебная глава или исторический материал: LESHY — комплект Markdown-промптов и дизайн-спецификаций. |
| [docs/leshy-brief/autumn-birch-generation.md](../../docs/leshy-brief/autumn-birch-generation.md) | Ручная учебная глава или исторический материал: Светлая тема: осенняя берёзовая роща. |
| [docs/leshy-brief/forest-depth-generation.md](../../docs/leshy-brief/forest-depth-generation.md) | Ручная учебная глава или исторический материал: Лесная тема: глубина пейзажа; берёзовая тема: спокойнее цвет. |
| [docs/leshy-brief/ornaments-2026-11-03/bands-reference.png](../../docs/leshy-brief/ornaments-2026-11-03/bands-reference.png) | Сохранённый образец орнаментов LESHY: bands-reference. |
| [docs/leshy-brief/ornaments-2026-11-03/motifs-reference.png](../../docs/leshy-brief/ornaments-2026-11-03/motifs-reference.png) | Сохранённый образец орнаментов LESHY: motifs-reference. |
| [docs/leshy-brief/retired-schematic-spots/archive.svg](../../docs/leshy-brief/retired-schematic-spots/archive.svg) | Архив заменённой схематической иллюстрации archive; не активный ресурс. |
| [docs/leshy-brief/retired-schematic-spots/birch.svg](../../docs/leshy-brief/retired-schematic-spots/birch.svg) | Архив заменённой схематической иллюстрации birch; не активный ресурс. |
| [docs/leshy-brief/retired-schematic-spots/fern.svg](../../docs/leshy-brief/retired-schematic-spots/fern.svg) | Архив заменённой схематической иллюстрации fern; не активный ресурс. |
| [docs/leshy-brief/retired-schematic-spots/mushrooms.svg](../../docs/leshy-brief/retired-schematic-spots/mushrooms.svg) | Архив заменённой схематической иллюстрации mushrooms; не активный ресурс. |
| [docs/leshy-brief/user-images/references/01_ornament_strips.png](../../docs/leshy-brief/user-images/references/01_ornament_strips.png) | Пользовательский визуальный референс LESHY: 01_ornament_strips. |
| [docs/leshy-brief/user-images/references/02_ornament_symbols.png](../../docs/leshy-brief/user-images/references/02_ornament_symbols.png) | Пользовательский визуальный референс LESHY: 02_ornament_symbols. |
| [docs/leshy-brief/user-images/references/03_illustration_1.png](../../docs/leshy-brief/user-images/references/03_illustration_1.png) | Пользовательский визуальный референс LESHY: 03_illustration_1. |
| [docs/leshy-brief/user-images/references/04_illustration_2.png](../../docs/leshy-brief/user-images/references/04_illustration_2.png) | Пользовательский визуальный референс LESHY: 04_illustration_2. |
| [docs/leshy-brief/user-images/references/05_illustration_3.png](../../docs/leshy-brief/user-images/references/05_illustration_3.png) | Пользовательский визуальный референс LESHY: 05_illustration_3. |
| [docs/leshy-brief/user-images/references/06_illustration_4.png](../../docs/leshy-brief/user-images/references/06_illustration_4.png) | Пользовательский визуальный референс LESHY: 06_illustration_4. |
| [docs/leshy-brief/user-images/references/07_illustration_5.png](../../docs/leshy-brief/user-images/references/07_illustration_5.png) | Пользовательский визуальный референс LESHY: 07_illustration_5. |
| [docs/leshy-brief/user-images/screenshots/Neutral_VSCode_extension.png](../../docs/leshy-brief/user-images/screenshots/Neutral_VSCode_extension.png) | Пользовательский снимок исходного интерфейса: Neutral_VSCode_extension. |
| [docs/leshy-brief/user-images/screenshots/Neutral_main_window.png](../../docs/leshy-brief/user-images/screenshots/Neutral_main_window.png) | Пользовательский снимок исходного интерфейса: Neutral_main_window. |
| [docs/reference/dependencies.md](../../docs/reference/dependencies.md) | Генерируемый документ: Объявленные и зафиксированные зависимости. |
| [docs/reference/design-reference.md](../../docs/reference/design-reference.md) | Генерируемый документ: Справочник архивного эталона дизайна. |
| [docs/reference/file-map.md](../../docs/reference/file-map.md) | Генерируемый документ: Карта файлов. |
| [docs/reference/python.md](../../docs/reference/python.md) | Генерируемый документ: Справочник Python. |
| [docs/reference/tests.md](../../docs/reference/tests.md) | Генерируемый документ: Справочник Python-тестов. |
| [docs/reference/typescript.md](../../docs/reference/typescript.md) | Генерируемый документ: Справочник TypeScript и JavaScript. |
| [docs/screenshots/studio/chat-1280x720.png](../../docs/screenshots/studio/chat-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: chat-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/chat-1440x900.png](../../docs/screenshots/studio/chat-1440x900.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: chat-1440x900.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/chat-1920x1080.png](../../docs/screenshots/studio/chat-1920x1080.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: chat-1920x1080.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-error-1280x720.png](../../docs/screenshots/studio/ide-error-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-error-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-history-1280x720.png](../../docs/screenshots/studio/ide-history-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-history-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-history-1440x900.png](../../docs/screenshots/studio/ide-history-1440x900.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-history-1440x900.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-history-1920x1080.png](../../docs/screenshots/studio/ide-history-1920x1080.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-history-1920x1080.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-history-empty-1280x720.png](../../docs/screenshots/studio/ide-history-empty-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-history-empty-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-tools-1280x720.png](../../docs/screenshots/studio/ide-tools-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-tools-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-working-1280x720.png](../../docs/screenshots/studio/ide-working-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-working-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-working-1440x900.png](../../docs/screenshots/studio/ide-working-1440x900.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-working-1440x900.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/ide-working-1920x1080.png](../../docs/screenshots/studio/ide-working-1920x1080.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: ide-working-1920x1080.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/lola-popup.png](../../docs/screenshots/studio/lola-popup.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: lola-popup.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/settings-1280x720.png](../../docs/screenshots/studio/settings-1280x720.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: settings-1280x720.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/settings-1440x900.png](../../docs/screenshots/studio/settings-1440x900.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: settings-1440x900.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/screenshots/studio/settings-1920x1080.png](../../docs/screenshots/studio/settings-1920x1080.png) | Снимок настоящего Electron renderer для визуальной проверки Studio: settings-1920x1080.png; сценарии и ограничения описаны в docs/UI_STUDIO_INTEGRATION.md. |
| [docs/sources.md](../../docs/sources.md) | Ручная учебная глава или исторический материал: Официальные материалы для изучения. |
| [docs/superpowers/plans/2026-11-03-ide-acceptance-checks.md](../../docs/superpowers/plans/2026-11-03-ide-acceptance-checks.md) | Ручная учебная глава или исторический материал: IDE Acceptance Checks Implementation Plan. |
| [docs/superpowers/plans/2026-11-03-leshy-panel-and-ornaments.md](../../docs/superpowers/plans/2026-11-03-leshy-panel-and-ornaments.md) | Ручная учебная глава или исторический материал: LESHY: panel, ornaments and window joins. |
| [docs/superpowers/plans/2026-11-03-leshy-raster-and-surface-coverage.md](../../docs/superpowers/plans/2026-11-03-leshy-raster-and-surface-coverage.md) | Ручная учебная глава или исторический материал: LESHY: raster assets and complete surface coverage. |
| [docs/superpowers/plans/2026-11-03-project-development.md](../../docs/superpowers/plans/2026-11-03-project-development.md) | Ручная учебная глава или исторический материал: LESHY Project Development Implementation Plan. |
| [electron-builder.json](../../electron-builder.json) | Allowlist приложения, extraResources Core и локальный NSIS installer без публикации. |
| [example.md](../../example.md) | Пользовательский демонстрационный Markdown; не является документацией API. |
| [main.py](../../main.py) | Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop. |
| [package-lock.json](../../package-lock.json) | Зафиксированное дерево npm-зависимостей; редактируется npm, а не вручную. |
| [package.json](../../package.json) | Корневой npm workspace и делегирование dev/build/typecheck. |
| [packaging/RELEASE_NOTES.md](../../packaging/RELEASE_NOTES.md) | Публикуемые инструкции установки, состав и реальные ограничения Windows prerelease. |
| [packaging/llama-LICENSE.txt](../../packaging/llama-LICENSE.txt) | MIT-лицензия ggml авторов из официального llama.cpp b11829. |
| [packaging/prerequisites.nsh](../../packaging/prerequisites.nsh) | NSIS bootstrap Visual C++: проверка версии реестра, офлайн-запуск, обработка ошибки и перезагрузки. |
| [packaging/release.json](../../packaging/release.json) | Явное намерение выпустить указанную версию; изменение запускает Release workflow текущей ветки. |
| [packaging/windows-dependencies.json](../../packaging/windows-dependencies.json) | Версии, официальные URL и SHA256 Windows runtime зависимостей. |
| [prototypes/neutral-ide/README.md](../../prototypes/neutral-ide/README.md) | Подготовка и запуск отдельной Neutral IDE; команды тестов и граница прототипа. |
| [prototypes/neutral-ide/extension/agent-view.cjs](../../prototypes/neutral-ide/extension/agent-view.cjs) | Webview provider новой панели, локальные ресурсы и маршрутизация сообщений. |
| [prototypes/neutral-ide/extension/client.cjs](../../prototypes/neutral-ide/extension/client.cjs) | Авторизованный клиент связи extension с общим Core. |
| [prototypes/neutral-ide/extension/extension.cjs](../../prototypes/neutral-ide/extension/extension.cjs) | Собственная боковая панель Core status/focus и прототип editor-owned diff с version/hash guards и явным modal. |
| [prototypes/neutral-ide/extension/icon.svg](../../prototypes/neutral-ide/extension/icon.svg) | Векторная N-иконка activity bar встроенного Neutral extension. |
| [prototypes/neutral-ide/extension/leshy-forest.json](../../prototypes/neutral-ide/extension/leshy-forest.json) | Нативная тема Code-OSS LESHY forest. |
| [prototypes/neutral-ide/extension/leshy-parchment.json](../../prototypes/neutral-ide/extension/leshy-parchment.json) | Нативная тема Code-OSS LESHY parchment. |
| [prototypes/neutral-ide/extension/leshy-twilight.json](../../prototypes/neutral-ide/extension/leshy-twilight.json) | Нативная тема Code-OSS LESHY twilight. |
| [prototypes/neutral-ide/extension/package.json](../../prototypes/neutral-ide/extension/package.json) | Встроенный Neutral extension: команды, theme и activity-bar webview contribution для Code-OSS. |
| [prototypes/neutral-ide/extension/theme.json](../../prototypes/neutral-ide/extension/theme.json) | Neutral Studio palette для собственной Code-OSS IDE. |
| [prototypes/neutral-ide/extension/workspace.cjs](../../prototypes/neutral-ide/extension/workspace.cjs) | Проверки dirty/version/hash и применение подтверждённых изменений средствами редактора. |
| [prototypes/neutral-ide/extensions.lock.json](../../prototypes/neutral-ide/extensions.lock.json) | Зафиксированные версии, engines, платформы, лицензии и SHA-256 пяти проверяемых Open VSX расширений. |
| [prototypes/neutral-ide/install_test_extensions.py](../../prototypes/neutral-ide/install_test_extensions.py) | Установка закреплённых MIT Open VSX расширений и локального probe VSIX через настоящий CLI в отдельный test profile. |
| [prototypes/neutral-ide/leshy-workbench.css](../../prototypes/neutral-ide/leshy-workbench.css) | Оформление закреплённого Code-OSS runtime без изменения пользовательского VS Code. |
| [prototypes/neutral-ide/prepare.py](../../prototypes/neutral-ide/prepare.py) | Закреплённый Code-OSS/VSCodium ZIP, SHA-256, product/PE branding, ресурсы и установка встроенного extension без изменения пользовательского VS Code. |
| [prototypes/neutral-ide/test_host.py](../../prototypes/neutral-ide/test_host.py) | Запуск настоящих Extension Host и normal-workbench UI тестов на одноразовых проектах; проверяет passed report, а не только exit code. |
| [prototypes/neutral-ide/tests/drive.cjs](../../prototypes/neutral-ide/tests/drive.cjs) | Локальный CDP-драйвер обычного test workbench: ввод replacement, screenshot и нажатие явного подтверждения. |
| [prototypes/neutral-ide/tests/host.cjs](../../prototypes/neutral-ide/tests/host.cjs) | Реальные API checks: tabs/splits/save/undo, stale edits, TypeScript, Open VSX theme/snippet/formatter/YAML, PTY и debugpy breakpoint. |
| [prototypes/neutral-ide/tests/processes.cjs](../../prototypes/neutral-ide/tests/processes.cjs) | Windows metadata своего дерева PID для ограниченной startup/RSS/CPU оценки. |
| [prototypes/neutral-ide/tests/ui-probe/extension.cjs](../../prototypes/neutral-ide/tests/ui-probe/extension.cjs) | Проверяет подтверждённый editor buffer edit, неизменность диска и undo в настоящем окне Code-OSS. |
| [prototypes/neutral-ide/tests/ui-probe/package.json](../../prototypes/neutral-ide/tests/ui-probe/package.json) | Только тестовый extension, который проверяет modal в normal development host; не копируется в runtime. |
| [prototypes/neutral-studio/.gitignore](../../prototypes/neutral-studio/.gitignore) | Архив этапа оценки Neutral Studio: .gitignore; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/README.md](../../prototypes/neutral-studio/README.md) | Архив этапа оценки Neutral Studio: README.md; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/app.css](../../prototypes/neutral-studio/app.css) | Архив этапа оценки Neutral Studio: app.css; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/app.js](../../prototypes/neutral-studio/app.js) | Архив этапа оценки Neutral Studio: app.js; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/build-functional.cjs](../../prototypes/neutral-studio/build-functional.cjs) | Архив этапа оценки Neutral Studio: build-functional.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-background-test.cjs](../../prototypes/neutral-studio/functional-background-test.cjs) | Архив этапа оценки Neutral Studio: functional-background-test.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-history-test.cjs](../../prototypes/neutral-studio/functional-history-test.cjs) | Архив этапа оценки Neutral Studio: functional-history-test.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-integration.cjs](../../prototypes/neutral-studio/functional-integration.cjs) | Архив этапа оценки Neutral Studio: functional-integration.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-lola-test.cjs](../../prototypes/neutral-studio/functional-lola-test.cjs) | Архив этапа оценки Neutral Studio: functional-lola-test.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-main.cjs](../../prototypes/neutral-studio/functional-main.cjs) | Архив этапа оценки Neutral Studio: functional-main.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-optional-test.cjs](../../prototypes/neutral-studio/functional-optional-test.cjs) | Архив этапа оценки Neutral Studio: functional-optional-test.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-tsconfig.json](../../prototypes/neutral-studio/functional-tsconfig.json) | Архив этапа оценки Neutral Studio: functional-tsconfig.json; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional-visual.cjs](../../prototypes/neutral-studio/functional-visual.cjs) | Архив этапа оценки Neutral Studio: functional-visual.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/BrandMark.tsx](../../prototypes/neutral-studio/functional/BrandMark.tsx) | Архив этапа оценки Neutral Studio: BrandMark.tsx; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/ChatText.tsx](../../prototypes/neutral-studio/functional/ChatText.tsx) | Архив этапа оценки Neutral Studio: ChatText.tsx; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/FunctionalControls.tsx](../../prototypes/neutral-studio/functional/FunctionalControls.tsx) | Архив этапа оценки Neutral Studio: FunctionalControls.tsx; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/functional.css](../../prototypes/neutral-studio/functional/functional.css) | Архив этапа оценки Neutral Studio: functional.css; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/neutral-equilibrium.png](../../prototypes/neutral-studio/functional/neutral-equilibrium.png) | Архив этапа оценки Neutral Studio: neutral-equilibrium.png; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/functional/neutral-equilibrium.svg](../../prototypes/neutral-studio/functional/neutral-equilibrium.svg) | Архив этапа оценки Neutral Studio: neutral-equilibrium.svg; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/index.html](../../prototypes/neutral-studio/index.html) | Архив этапа оценки Neutral Studio: index.html; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/launch-functional.cjs](../../prototypes/neutral-studio/launch-functional.cjs) | Архив этапа оценки Neutral Studio: launch-functional.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/launch.cjs](../../prototypes/neutral-studio/launch.cjs) | Архив этапа оценки Neutral Studio: launch.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/lola.css](../../prototypes/neutral-studio/lola.css) | Архив этапа оценки Neutral Studio: lola.css; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/lola.html](../../prototypes/neutral-studio/lola.html) | Архив этапа оценки Neutral Studio: lola.html; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/lola.js](../../prototypes/neutral-studio/lola.js) | Архив этапа оценки Neutral Studio: lola.js; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/main.cjs](../../prototypes/neutral-studio/main.cjs) | Архив этапа оценки Neutral Studio: main.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/package.json](../../prototypes/neutral-studio/package.json) | Архив этапа оценки Neutral Studio: package.json; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/preload.cjs](../../prototypes/neutral-studio/preload.cjs) | Архив этапа оценки Neutral Studio: preload.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/review-ui.css](../../prototypes/neutral-studio/review-ui.css) | Архив этапа оценки Neutral Studio: review-ui.css; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/review-ui.js](../../prototypes/neutral-studio/review-ui.js) | Архив этапа оценки Neutral Studio: review-ui.js; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/run-functional-test.cjs](../../prototypes/neutral-studio/run-functional-test.cjs) | Архив этапа оценки Neutral Studio: run-functional-test.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [prototypes/neutral-studio/verify-review.cjs](../../prototypes/neutral-studio/verify-review.cjs) | Архив этапа оценки Neutral Studio: verify-review.cjs; основная реализация находится в apps/desktop. История решений описана в docs/UI_STUDIO_INTEGRATION.md. |
| [requirements-build.txt](../../requirements-build.txt) | Точные Python-зависимости для Windows x64 freeze Core без Qt. |
| [requirements-core.txt](../../requirements-core.txt) | Диапазоны OpenAI/HTTPX и фиксированный официальный MCP SDK для ядра без Qt. |
| [requirements.txt](../../requirements.txt) | Полное Python-окружение с PySide6 и сохранённой зависимостью python-dotenv. |
| [run-desktop.bat](../../run-desktop.bat) | Запуск npm dev; выбирает .venv Python, если LCA_PYTHON не задан. |
| [run.bat](../../run.bat) | Старый запуск Qt с установкой зависимостей; содержит оставшуюся ссылку на отсутствующий .env.example. |
| [skills/coding/SKILL.md](../../skills/coding/SKILL.md) | Краткий навык coding; SkillManager использует метаданные для выбора по prompt. |
| [skills/debugging/SKILL.md](../../skills/debugging/SKILL.md) | Краткий навык debugging; SkillManager использует метаданные для выбора по prompt. |
| [skills/project_analysis/SKILL.md](../../skills/project_analysis/SKILL.md) | Краткий навык project_analysis; SkillManager использует метаданные для выбора по prompt. |
| [skills/testing/SKILL.md](../../skills/testing/SKILL.md) | Краткий навык testing; SkillManager использует метаданные для выбора по prompt. |
| [tests/electron/assistant-media.cjs](../../tests/electron/assistant-media.cjs) | Host-проверки музыкальных ссылок и путей аудио, включая junction, без воспроизведения и браузера. |
| [tests/electron/background-runs-smoke.cjs](../../tests/electron/background-runs-smoke.cjs) | Real renderer/Core test of switching active chats, queued Stop and a delta arriving between snapshot and IPC response. |
| [tests/electron/desktop-apps.cjs](../../tests/electron/desktop-apps.cjs) | Node-проверка границы каталога приложений: ID, запрет путей/команд, EXE, повторное добавление, удаление и браузер без реальных окон. |
| [tests/electron/ide-acceptance-run.cjs](../../tests/electron/ide-acceptance-run.cjs) | Запускает native IDE fixture в отдельном acceptance режиме; --json выбирает строгий JSON fixture. |
| [tests/electron/ide-acceptance.cjs](../../tests/electron/ide-acceptance.cjs) | Реальный UI/Core сценарий: без модели, отказ, missing import exit1→repair→exit0, stale evidence и draft isolation. |
| [tests/electron/ide-acceptance.test.cjs](../../tests/electron/ide-acceptance.test.cjs) | Node regressions сериализации, argv/scope/check_id, readonly/resume и восстановления draft. |
| [tests/electron/ide-session.test.cjs](../../tests/electron/ide-session.test.cjs) | Node-проверки ранних и повторных событий, завершённых runs и редактирования безопасной диагностики. |
| [tests/electron/leshy-themes.cjs](../../tests/electron/leshy-themes.cjs) | Изолированная Electron-проверка трёх тем, настроек и состояний окон. |
| [tests/electron/lola-desktop-smoke.cjs](../../tests/electron/lola-desktop-smoke.cjs) | Изолированный Electron fixture для настоящего окна/Tray Лолы, настроек, sender isolation, скрытого основного окна и единственного model/Core запроса. |
| [tests/electron/lola-preferences.cjs](../../tests/electron/lola-preferences.cjs) | Pure contract проверки defaults, валидации размеров/координат и bounded frame спутника. |
| [tests/electron/microphone.cjs](../../tests/electron/microphone.cjs) | Проверка захвата и обрезки WAV с фиктивным AudioContext без записи реального микрофона. |
| [tests/electron/neutral-ide-integration.cjs](../../tests/electron/neutral-ide-integration.cjs) | Сквозная проверка Desktop → Code-OSS webview → Core → editor, истории и approvals. |
| [tests/electron/neutral-ide-smoke.cjs](../../tests/electron/neutral-ide-smoke.cjs) | Изолированная проверка кнопки Neutral IDE, root/dirty guards, собственного executable/profile и реального Core через auth/allowlist. |
| [tests/electron/neutral-smoke.cjs](../../tests/electron/neutral-smoke.cjs) | Стабильный CI entrypoint полной проверки Studio; делегирует tests/electron/studio-smoke.cjs. |
| [tests/electron/optional-ide-smoke.cjs](../../tests/electron/optional-ide-smoke.cjs) | Реальный UI/Core workflow исследования, LSP, создания/отказа удаления/открытия worktree и панели Docker; отдельный профиль. |
| [tests/electron/packaged-ide.mjs](../../tests/electron/packaged-ide.mjs) | CDP-приёмка вложенной IDE свежего пакета: frozen Core, diff approval, editor-owned запись и Undo/Save. |
| [tests/electron/packaged-path.mjs](../../tests/electron/packaged-path.mjs) | Выбирает точный Windows executable из конфигурации сборки либо явного пути без fallback на старый бренд. |
| [tests/electron/packaged-path.test.mjs](../../tests/electron/packaged-path.test.mjs) | Проверки чистого LESHY output, старого Neutral output, обоих файлов и явного пути пакета. |
| [tests/electron/packaged-smoke.mjs](../../tests/electron/packaged-smoke.mjs) | CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском. |
| [tests/electron/readiness-live.cjs](../../tests/electron/readiness-live.cjs) | Явно запускаемая desktop приёмка с настоящей моделью LM Studio, readonly ребёнком, правкой и независимой проверкой одноразового проекта. |
| [tests/electron/run.cjs](../../tests/electron/run.cjs) | Запускает выбранную нативную Electron-проверку без ELECTRON_RUN_AS_NODE и с наследованием её exit code. |
| [tests/electron/runner-exit.test.cjs](../../tests/electron/runner-exit.test.cjs) | Node VM-проверки кодов launcher: успех, ошибка, сигнал и spawn failure. |
| [tests/electron/smoke.cjs](../../tests/electron/smoke.cjs) | Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop. |
| [tests/electron/studio-layout.cjs](../../tests/electron/studio-layout.cjs) | Нативная проверка pointer/keyboard resize, сохранения раскладок, фокуса, модели под запросом и IME. |
| [tests/electron/studio-smoke.cjs](../../tests/electron/studio-smoke.cjs) | Изолированная полная проверка рабочего renderer/IPC/Core: история, проекты, модель, инструменты, редактор, approvals и восстановление. |
| [tests/electron/studio-visual.cjs](../../tests/electron/studio-visual.cjs) | Снимает реальный renderer на трёх размерах: Chat, работа IDE, tools, история, пустой поиск, ошибка и настройки. |
| [tests/fixtures/lsp_diagnostics.py](../../tests/fixtures/lsp_diagnostics.py) | Локальный LSP fixture: чужой URI, попытка applyEdit, диагностика после отказа и режим зависшего stdin. |
| [tests/fixtures/mcp_echo.py](../../tests/fixtures/mcp_echo.py) | Настоящий локальный MCP сервер арифметики и ожидания для stdio/HTTP проверок. |
| [tests/migration/test_agent_readiness.py](../../tests/migration/test_agent_readiness.py) | Вертикальные A–I сценарии с HTTP-моделью, настоящими разрешениями, файлами, subprocess и контрольными точками в одноразовом проекте. |
| [tests/migration/test_background_runs.py](../../tests/migration/test_background_runs.py) | Real HTTP tests of two engine workers, isolated streams, queued cancellation, approvals and full shutdown. |
| [tests/migration/test_bridge.py](../../tests/migration/test_bridge.py) | Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи. |
| [tests/migration/test_bridge_process.py](../../tests/migration/test_bridge_process.py) | Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval. |
| [tests/migration/test_child_execution.py](../../tests/migration/test_child_execution.py) | Real HTTP parent-child-parent, cancellation, denied child writes, stale handback, OOM and pre-HTTP spending admission. |
| [tests/migration/test_delegation.py](../../tests/migration/test_delegation.py) | Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории. |
| [tests/migration/test_ide_acceptance.py](../../tests/migration/test_ide_acceptance.py) | Реальный HTTP workflow plan/write/command/rollback/recheck и отказ исполнения write в режиме чтения. |
| [tests/migration/test_ide_sessions.py](../../tests/migration/test_ide_sessions.py) | Bridge-проверки изоляции workspace, editor receipts и отмены закрытого IDE view. |
| [tests/migration/test_json_protocol.py](../../tests/migration/test_json_protocol.py) | Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor. |
| [tests/migration/test_model_discovery.py](../../tests/migration/test_model_discovery.py) | HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета. |
| [tests/migration/test_model_probe.py](../../tests/migration/test_model_probe.py) | Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены. |
| [tests/migration/test_neural_speech.py](../../tests/migration/test_neural_speech.py) | HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука. |
| [tests/migration/test_project_memory_v2.py](../../tests/migration/test_project_memory_v2.py) | Настоящий parent HTTP flow: гипотеза модели, новые чаты, актуальные решения и исключение изменённых источников. |
| [tests/migration/test_run_control.py](../../tests/migration/test_run_control.py) | Независимая localhost сверка ledger с HTTP, stream_options retry, JSON repair, usage и diff approval. |
| [tests/migration/test_run_owner_restart.py](../../tests/migration/test_run_owner_restart.py) | Kill/restart of a real isolated Core with streamed and queued chats, durable ledger and invalidated write consent. |
| [tests/migration/test_stage17_workflow.py](../../tests/migration/test_stage17_workflow.py) | Сквозные checks-only LSP и асинхронный Core checkpoint API с проверкой responsiveness и сохранности исходника. |
| [tests/migration/test_streaming.py](../../tests/migration/test_streaming.py) | Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки. |
| [tests/migration/test_task_graph_execution.py](../../tests/migration/test_task_graph_execution.py) | Multi-file task through context compaction, failed check, bounded diagnostic and actual Core restart without replay. |
| [tests/migration/test_task_service.py](../../tests/migration/test_task_service.py) | HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация. |
| [tests/migration/test_transcription.py](../../tests/migration/test_transcription.py) | Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону. |
| [tests/migration/test_tts_server.py](../../tests/migration/test_tts_server.py) | HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов. |
| [tests/migration/test_workspace_workflow.py](../../tests/migration/test_workspace_workflow.py) | Настоящий локальный HTTP/SSE workflow создания и изменения проекта через пять отдельных согласий и scoped инструкции. |
| [tests/test_agent_benchmark.py](../../tests/test_agent_benchmark.py) | Проверка владения fixtures, независимого oracle, строгого отчёта и запрета считать угаданный путь успешным поиском. |
| [tests/test_approval_flow.py](../../tests/test_approval_flow.py) | Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6. |
| [tests/test_assistant_service.py](../../tests/test_assistant_service.py) | Проверки утилит Лолы, сохранения заметок, таймеров, музыки и папок из исходного prompt. |
| [tests/test_auto_budget.py](../../tests/test_auto_budget.py) | Автонастройка без настоящей LLM: metadata/400/SSE, русский текст, каталог, большие выполненные записи и защита pending code. |
| [tests/test_call_journal.py](../../tests/test_call_journal.py) | Регрессии долговечного журнала: pairing, receipts, повреждения, конфликты, идентичность пачек и ручные решения. |
| [tests/test_chat_store.py](../../tests/test_chat_store.py) | Контракты SQLite chat API: миграционные warnings, запрет перечитывания JSON, rollback индекса и сохранность при повреждении БД. |
| [tests/test_companion_policy.py](../../tests/test_companion_policy.py) | Границы coding intent Лолы, очистка Markdown, математики и внутренних тегов. |
| [tests/test_context_builder.py](../../tests/test_context_builder.py) | Изолированные проверки ContextPack: индекс, source anchors, budget pruning, revoke, отмена, retry и согласие без внешней сети. |
| [tests/test_conversation_history.py](../../tests/test_conversation_history.py) | Выбор истории и сокращение tool outputs/пар в conversation.py. |
| [tests/test_core_reliability.py](../../tests/test_core_reliability.py) | Регрессии первого этапа аудита: завершение, отказ, аргументы, свидетельства команд, runtime и привязка ключей к endpoint; модель заменена локальной фикстурой. |
| [tests/test_docs_reference.py](../../tests/test_docs_reference.py) | Проверка инвентаризации стороннего CLI без включения его внутренностей в API приложения. |
| [tests/test_editor_io.py](../../tests/test_editor_io.py) | Чтение/сохранение существующих файлов, размер и отказ вне корня. |
| [tests/test_editor_service.py](../../tests/test_editor_service.py) | Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope. |
| [tests/test_expansion.py](../../tests/test_expansion.py) | Контракты разделения истории, профиля без секретов, JSON tools, KV whitelist, PC grants, Telegram owner и WAV validation. |
| [tests/test_file_editing.py](../../tests/test_file_editing.py) | Preview без записи, explicit approval, overwrite и путь файла. |
| [tests/test_ide_completion.py](../../tests/test_ide_completion.py) | Проверки локальности, размера запроса и завершения клиента автодополнения. |
| [tests/test_ide_execution.py](../../tests/test_ide_execution.py) | Проверки единственного editor writer, dirty/stale guards и неизвестных эффектов. |
| [tests/test_ide_remote_control.py](../../tests/test_ide_remote_control.py) | Проверки управления IDE-запуском владельцем без переключения desktop view. |
| [tests/test_ide_verification.py](../../tests/test_ide_verification.py) | 18 контрактов критериев, readonly enforcement, снимков, аварийного и частичного отката, backup и schema upgrade. |
| [tests/test_json_compatibility.py](../../tests/test_json_compatibility.py) | JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop. |
| [tests/test_limits.py](../../tests/test_limits.py) | Настраиваемое число entries и глубина обхода. |
| [tests/test_mcp_reliability.py](../../tests/test_mcp_reliability.py) | Регрессии идентичности MCP, миграции выключенных инструментов, единственной отменяемой discovery и настоящего медленного stdio сервера. |
| [tests/test_memory_service.py](../../tests/test_memory_service.py) | Память UI: CAS, invalid payload, corrupt file, scope и полный Unicode budget. |
| [tests/test_model_gateway.py](../../tests/test_model_gateway.py) | Параметры endpoint удалённого/совместимого провайдера. |
| [tests/test_model_manager.py](../../tests/test_model_manager.py) | Сканирование GGUF, quantization, свободный порт и остановленный runtime. |
| [tests/test_model_preferences.py](../../tests/test_model_preferences.py) | Whitelist настроек, defaults и отказ URL с credentials/неверным портом. |
| [tests/test_neutral_conversations.py](../../tests/test_neutral_conversations.py) | Изоляция проектов/режимов, архив, удаление, копия/повтор, экспорт и профили без ключей. |
| [tests/test_neutral_extensions.py](../../tests/test_neutral_extensions.py) | Переключатели, неизменяемый снимок, навыки-черновики, пакеты и реальные MCP transports. |
| [tests/test_optional_ide.py](../../tests/test_optional_ide.py) | 14 контрактов опциональности, бюджета, реального LSP/Git, недоверенных server edits, удаления и container argv/cleanup. |
| [tests/test_process_identity.py](../../tests/test_process_identity.py) | Real child lifetime probe plus conservative PID reuse, legacy owner and whole-tree telemetry recovery tests. |
| [tests/test_project_command.py](../../tests/test_project_command.py) | Подтверждение и отказ запуска, корень cwd, код возврата, лимит вывода и отмена процесса. |
| [tests/test_project_index.py](../../tests/test_project_index.py) | Изолированные AST/TS/FTS/watcher/cache тесты: exact ranges, incremental edits, policy revocation, offline recovery, cancel и corruption. |
| [tests/test_project_knowledge.py](../../tests/test_project_knowledge.py) | Проверки изоляции и свежести памяти, CAS, закрытия источников, транспортного retry и сохранения повреждённых данных. |
| [tests/test_project_memory.py](../../tests/test_project_memory.py) | Изоляция, лимиты, merge, формат контекста и очистка памяти. |
| [tests/test_project_search.py](../../tests/test_project_search.py) | Поиск: Unicode, фильтры, лимиты, пропуски бинарных файлов, отмена и single-flight. |
| [tests/test_request_budget.py](../../tests/test_request_budget.py) | Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP. |
| [tests/test_response_quality.py](../../tests/test_response_quality.py) | Строгая оценка завершения, ограниченная доработка, восстановление пустого ответа и отсутствие лишней проверки информационных вопросов. |
| [tests/test_responses_adapter.py](../../tests/test_responses_adapter.py) | Локальная HTTP/SSE фикстура OpenAI Responses: текст, функции, reasoning items, probe и retry. |
| [tests/test_run_policy.py](../../tests/test_run_policy.py) | Explicit paid-budget estimates across children/resume and atomic journal-to-epoch tool accounting. |
| [tests/test_run_registry.py](../../tests/test_run_registry.py) | Изолированные v2→v3, backup, orphan/live owner, cascade, model inheritance, FIFO и SDK stream-close проверки. |
| [tests/test_run_state.py](../../tests/test_run_state.py) | Контракты переходов между выполнением, подтверждением, проверкой и терминальными состояниями. |
| [tests/test_runtime_architecture.py](../../tests/test_runtime_architecture.py) | Структура плана, skills, размер контекста и verifier. |
| [tests/test_runtime_service.py](../../tests/test_runtime_service.py) | Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup. |
| [tests/test_sandbox.py](../../tests/test_sandbox.py) | Обёртка запуска внутренней security self-test suite. |
| [tests/test_scoped_verification.py](../../tests/test_scoped_verification.py) | Реальные команды и scoped receipts: большой проект, зависимости/доступ/rollback, смена root, legacy migration и restart без повторного эффекта. |
| [tests/test_services_and_sessions.py](../../tests/test_services_and_sessions.py) | 7 новых контрактов deadline/gate/protocol/profile и настоящего reuse/invalidate/cancel MCP stdio. |
| [tests/test_smart_context.py](../../tests/test_smart_context.py) | Проверки архива, неизменности истории, пар tools, полного кода, JSON и дедупликации. |
| [tests/test_speech_service.py](../../tests/test_speech_service.py) | TTS без динамиков/микрофона: WAV, JSON data boundary, cancellation и timeout cleanup. |
| [tests/test_stage17_verification.py](../../tests/test_stage17_verification.py) | Gate этапа 17: выбор проверок, настоящие LSP процессы, изоляция Git, CRLF и внешняя правка во время rollback. |
| [tests/test_stage9_reliability.py](../../tests/test_stage9_reliability.py) | Регрессии аудита A1–A5: JSON/EOF/revision/access/LSP и живой JSON-lines bridge во время backup. |
| [tests/test_storage.py](../../tests/test_storage.py) | Миграция всех режимов, реальные process exits, межпроцессные транзакции, большие outputs, индекс и проверенная ZIP-копия. |
| [tests/test_subagent_profiles.py](../../tests/test_subagent_profiles.py) | Долговечность черновиков и запрет повышения прав через модель, повреждение каталога и изоляция возвращаемых данных. |
| [tests/test_task_activity.py](../../tests/test_task_activity.py) | Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery. |
| [tests/test_task_graph.py](../../tests/test_task_graph.py) | DAG receipts, dependency validation, stale propagation, user plan authority, reload and persisted watchdog recovery. |
| [tests/test_task_store.py](../../tests/test_task_store.py) | Round-trip checkpoint, переход этапа, завершение и очистка. |
| [tests/test_tool_execution.py](../../tests/test_tool_execution.py) | Fault-injection исполнения: реальные остановки процессов, запрет повторения эффектов, сохранение успехов и ручное восстановление. |
| [tests/test_windows_dependencies.py](../../tests/test_windows_dependencies.py) | Тесты закреплённых загрузок: кэш без сети, отклонение подмены и атомарная замена повреждённого файла. |
| [tests/test_workspace_tools.py](../../tests/test_workspace_tools.py) | Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery. |
| [tools/audit_core_20261025.py](../../tools/audit_core_20261025.py) | Изолированные воспроизведения аудита Neutral 7: синтетические ответы модели и временные файлы, без изменения продукта или пользовательских данных. |
| [tools/audit_post_stage8.py](../../tools/audit_post_stage8.py) | Read-only синтетический аудит границ tool parser, завершения потока, проверки записи, LSP и локальных файловых политик; не вызывает внешнюю модель и не изменяет проект. |
| [tools/benchmark_agent.py](../../tools/benchmark_agent.py) | Baseline 20a: owned synthetic repositories, frozen Agent/Core sources, real serial native/JSON runs, held-out arithmetic/diff/provenance/recovery checks and reports without editing user projects. |
| [tools/benchmark_project_index.py](../../tools/benchmark_project_index.py) | Воспроизводимые fresh synthetic корпуса baseline 20a и измерения индекса 40/1200/12000 файлов: Recall, p50/p95, update, CPU/RAM/cache. |
| [tools/benchmark_storage.py](../../tools/benchmark_storage.py) | Воспроизводимый локальный benchmark на синтетических JSON-чатах: перенос, p50/p95 списка и поиска. |
| [tools/build_windows_core.py](../../tools/build_windows_core.py) | PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков. |
| [tools/check_docs.py](../../tools/check_docs.py) | Проверка локальных ссылок, source lines, покрытия аннотаций и актуальности каталога. |
| [tools/check_live_model.py](../../tools/check_live_model.py) | Opt-in smoke реальной модели: disposable AppData/проект, Chat/IDE/Лола, без approvals записи, JSON отчёт. |
| [tools/doc_notes.py](../../tools/doc_notes.py) | Ручные назначения файлов и символов для справочников; не является runtime-модулем агента. |
| [tools/extract_ts_symbols.cjs](../../tools/extract_ts_symbols.cjs) | TypeScript Compiler API: структурные объявления TS/JS без исполнения приложения. |
| [tools/generate_brand_icons.py](../../tools/generate_brand_icons.py) | Разработка: рендер SVG через Qt и запись PNG/многоразмерного ICO без Pillow. |
| [tools/generate_code_reference.py](../../tools/generate_code_reference.py) | Извлекает объявления из Python/TypeScript AST и создаёт Markdown-каталоги. |
| [tools/prepare_windows_dependencies.py](../../tools/prepare_windows_dependencies.py) | Загрузка официальных зависимостей по SHA256, выбор server/DLL и подготовка офлайн-пакета без запуска установщиков. |
| [tools/test_agent_readiness.py](../../tools/test_agent_readiness.py) | Запускает изолированный набор готовности и сохраняет JSON со статусом, временем и ошибками каждого теста. |
| [tools/tts/README.md](../../tools/tts/README.md) | Установка TTS, выбор аниме-профиля, ограничения ресурсов и настройка голосовой активации. |
| [tools/tts/piper_server.py](../../tools/tts/piper_server.py) | CPU Piper адаптер прежнего HTTP TTS API: русский ONNX голос, PCM16 WAV, лимиты и отмена между предложениями. |
| [tools/tts/qwen_server.py](../../tools/tts/qwen_server.py) | Отдельный localhost Qwen3-TTS сервер: VoiceDesign 1.7B или CustomVoice 0.6B с готовым голосом, русский язык и PCM16 WAV. |
| [tools/tts/requirements.txt](../../tools/tts/requirements.txt) | Дополнительные зависимости Qwen3-TTS; не добавляются в основной frozen Core. |
| [tools/tts/start-piper.ps1](../../tools/tts/start-piper.ps1) | Создаёт отдельную среду Piper Python 3.12, устанавливает piper-tts и запускает выбранный локальный ONNX голос. |
| [tools/tts/start-tts.ps1](../../tools/tts/start-tts.ps1) | Создаёт TTS среду Python 3.12 с PythonPath, устанавливает согласованные CPU/CUDA torch и torchaudio, поддерживает InstallOnly/LowMemory и запускает сервер. |
| [tools/tts/training/README.md](../../tools/tts/training/README.md) | Команды возобновляемой генерации, обучения и контроля локального конвейера Serena. |
| [tools/tts/training/export_and_evaluate.py](../../tools/tts/training/export_and_evaluate.py) | ONNX экспорт с совместимым tracer и CPU/STT проверкой четырёх новых фраз без объявления совпадения тембра. |
| [tools/tts/training/generate_serena.py](../../tools/tts/training/generate_serena.py) | Возобновляемый корпус Qwen Serena: закреплённая revision, PCM22k WAV, локальный STT отбор и provenance каждого примера. |
| [tools/tts/training/pipeline.py](../../tools/tts/training/pipeline.py) | Однопроцессный локальный контроллер этапов с атомарным состоянием, границами шагов и остановкой при ошибках. |
| [tools/tts/training/run_training.py](../../tools/tts/training/run_training.py) | Ограниченное Windows дообучение VITS: преобразование Linux checkpoint, warmstart, eSpeak workaround и resume. |
