# Карта файлов

Этот файл создаётся `python tools/generate_code_reference.py`. Сигнатуры и номера строк извлечены из исходников; назначения — из ручных аннотаций. Изменяйте объяснения в `tools/doc_notes.py`, затем пересоздайте справочник.

Блоки сигнатур приводятся без тела; это справочные объявления, а не самостоятельные программы.

[К руководству](../README.md)

Перечислены файлы репозитория; зависимости, окружения и результаты сборки исключены правилами Git.

| Файл | Назначение |
| --- | --- |
| [.gitattributes](../../.gitattributes) | Автоопределение текстовых файлов и нормализация переводов строк в Git. |
| [.github/workflows/validate.yml](../../.github/workflows/validate.yml) | Windows CI: Python/build/docs и отдельный job freeze/NSIS/packaged smoke с временным installer artifact. |
| [.gitignore](../../.gitignore) | Исключает окружения, сборки, кэши, тестовые данные и секретный .env из Git. |
| [MIGRATION_PLAN.md](../../MIGRATION_PLAN.md) | Выполненные границы миграции и оставшиеся этапы. |
| [README.md](../../README.md) | Краткий вход в проект, запуск и ссылка на учебное руководство. |
| [README_V6_MIGRATION.md](../../README_V6_MIGRATION.md) | Краткая инструкция текущего Electron-пути и его проверок. |
| [VERSION](../../VERSION) | Исторический маркер 5.8.0; не является единственным источником версии нового Electron-приложения. |
| [agent/__init__.py](../../agent/__init__.py) | Маркер Python-пакета agent; не запускает UI или модель. |
| [agent/chat_store.py](../../agent/chat_store.py) | JSON-чаты и индекс истории вне папки проекта. |
| [agent/context_manager.py](../../agent/context_manager.py) | Простой ограничитель рабочего контекста активного AgentRuntime. |
| [agent/conversation.py](../../agent/conversation.py) | Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп. |
| [agent/editor_io.py](../../agent/editor_io.py) | Самостоятельные sandbox-функции текстового редактора; React preview их не использует для записи. |
| [agent/engine.py](../../agent/engine.py) | Независимый от UI цикл модели, инструментов, подтверждений, памяти и checkpoint. |
| [agent/mcp.py](../../agent/mcp.py) | Реестр MCP-конфигураций без транспорта и исполнения внешних tools. |
| [agent/model_client.py](../../agent/model_client.py) | Отменяемый async HTTP-клиент с синхронной поверхностью для движка. |
| [agent/model_discovery.py](../../agent/model_discovery.py) | HTTPX-получение списка моделей с общим deadline, ограничением ответа и отменой сокета. |
| [agent/model_gateway.py](../../agent/model_gateway.py) | Отдельное представление endpoint провайдера/локального runtime; не включено в TaskService. |
| [agent/model_manager.py](../../agent/model_manager.py) | Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции. |
| [agent/model_preferences.py](../../agent/model_preferences.py) | Валидация endpoint и whitelist числовых настроек, миграция старого JSON и атомарное сохранение без API-ключа. |
| [agent/model_probe.py](../../agent/model_probe.py) | Ограниченная отменяемая проверка draft-модели через Chat Completions без файлов, истории и сохранения настроек. |
| [agent/planner.py](../../agent/planner.py) | Структура этапа и детерминированный план по словам запроса. |
| [agent/project_memory.py](../../agent/project_memory.py) | Компактная структурированная память проекта, очистка и форматирование для модели. |
| [agent/runtime.py](../../agent/runtime.py) | Связь контекста, планировщика, навыков, verifier и MCP-реестра; часть границ ещё не подключена. |
| [agent/security.py](../../agent/security.py) | Канонический корень и разрешение путей только внутри выбранного проекта. |
| [agent/skills.py](../../agent/skills.py) | Обнаружение, краткие метаданные, чтение и выбор SKILL.md по словам. |
| [agent/task_activity.py](../../agent/task_activity.py) | Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории. |
| [agent/task_store.py](../../agent/task_store.py) | JSON-контрольные точки задач, этапы, статусы и восстановление. |
| [agent/tools.py](../../agent/tools.py) | Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test. |
| [agent/ui.py](../../agent/ui.py) | Сохранённый Qt GUI: панели, readonly preview, настройки, чат и approval dialog. |
| [agent/verifier.py](../../agent/verifier.py) | Отдельная детерминированная проверка результата этапа; engine не вызывает её автоматически. |
| [agent/worker.py](../../agent/worker.py) | Qt QThread-адаптер вокруг AgentEngine; преобразует callbacks в Signal. |
| [apps/desktop/.gitignore](../../apps/desktop/.gitignore) | Локальные исключения выходных директорий desktop-сборки. |
| [apps/desktop/build-electron.mjs](../../apps/desktop/build-electron.mjs) | Две Vite library-сборки в main.cjs и preload.cjs с внешними системными импортами. |
| [apps/desktop/electron/main.ts](../../apps/desktop/electron/main.ts) | Окно, Python-процесс, pending RPC, проверка sender и фиксированные IPC handlers. |
| [apps/desktop/electron/preload.ts](../../apps/desktop/electron/preload.ts) | Узкий window.lca API и отписываемый listener событий. |
| [apps/desktop/index.html](../../apps/desktop/index.html) | HTML-узел React и модульный entry point renderer. |
| [apps/desktop/package.json](../../apps/desktop/package.json) | Зависимости Electron/React и dev/build/typecheck-скрипты workspace. |
| [apps/desktop/src/App.tsx](../../apps/desktop/src/App.tsx) | React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff. |
| [apps/desktop/src/EditorPanel.tsx](../../apps/desktop/src/EditorPanel.tsx) | Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение. |
| [apps/desktop/src/ModelSettings.tsx](../../apps/desktop/src/ModelSettings.tsx) | Модальное окно draft-настроек: endpoint, ключ, список моделей, тест ответа, генерация, лимиты, сохранение и focus trap. |
| [apps/desktop/src/TaskProgress.tsx](../../apps/desktop/src/TaskProgress.tsx) | Типизированная панель этапов, инструментов, результатов и продолжения задачи. |
| [apps/desktop/src/VoicePanel.tsx](../../apps/desktop/src/VoicePanel.tsx) | Подготовительный экран голосового ассистента: SVG-эскиз горничной, честные состояния отсутствующих STT/TTS и контракты будущей сессии; аудио пока не записывает. |
| [apps/desktop/src/main.tsx](../../apps/desktop/src/main.tsx) | Подключает CSS, создаёт React root и отображает App в StrictMode. |
| [apps/desktop/src/style.css](../../apps/desktop/src/style.css) | Стили IDE-панелей, сообщений, формы, modal и индикатора streaming. |
| [apps/desktop/src/vite-env.d.ts](../../apps/desktop/src/vite-env.d.ts) | Vite reference, CoreEvent и TypeScript-контракт Window.lca. |
| [apps/desktop/tsconfig.electron.json](../../apps/desktop/tsconfig.electron.json) | Статическая проверка Node/Electron main и preload без emit. |
| [apps/desktop/tsconfig.json](../../apps/desktop/tsconfig.json) | Статическая проверка React/DOM/JSX-кода renderer. |
| [apps/desktop/vite.config.ts](../../apps/desktop/vite.config.ts) | React-плагин, относительные assets, фиксированный локальный dev-порт и outDir. |
| [core/python/bridge.py](../../core/python/bridge.py) | JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout. |
| [core/python/editor_service.py](../../core/python/editor_service.py) | Ручной editor-протокол: strict UTF-8 чтение с revision, preview, одноразовый Apply через существующую атомарную snapshot-запись. |
| [core/python/task_service.py](../../core/python/task_service.py) | Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval. |
| [design_reference/DESIGN_REFERENCE.md](../../design_reference/DESIGN_REFERENCE.md) | Пояснение сохранённого визуального эталона и границ его переноса. |
| [design_reference/agent_studio_reference.py](../../design_reference/agent_studio_reference.py) | Архивный визуальный прототип с собственными механизмами; не импортируется рабочим main.py. |
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
| [docs/11-current-status.md](../../docs/11-current-status.md) | Ручная учебная глава или исторический материал: 11. Реальный статус и технический долг. |
| [docs/12-development-guide.md](../../docs/12-development-guide.md) | Ручная учебная глава или исторический материал: 12. Как развивать проект и документацию. |
| [docs/13-learning-path.md](../../docs/13-learning-path.md) | Ручная учебная глава или исторический материал: 13. Учебный маршрут и словарь. |
| [docs/14-windows-packaging.md](../../docs/14-windows-packaging.md) | Ручная учебная глава или исторический материал: 14. Windows-сборка со встроенным Python Core. |
| [docs/15-task-progress.md](../../docs/15-task-progress.md) | Ручная учебная глава или исторический материал: 15. План задачи, инструменты и результаты. |
| [docs/16-workspaces-and-answer-recovery.md](../../docs/16-workspaces-and-answer-recovery.md) | Ручная учебная глава или исторический материал: 16. Три режима и восстановление пустого ответа. |
| [docs/17-model-settings-and-theme.md](../../docs/17-model-settings-and-theme.md) | Ручная учебная глава или исторический материал: 17. Настройка модели и общая палитра. |
| [docs/18-editor.md](../../docs/18-editor.md) | Ручная учебная глава или исторический материал: 18. Рабочий редактор IDE. |
| [docs/AUTONOMOUS_PLAN_2026-10-23.md](../../docs/AUTONOMOUS_PLAN_2026-10-23.md) | Ручная учебная глава или исторический материал: Автономный план LocalAgent — 23 октября 2026. |
| [docs/README.md](../../docs/README.md) | Ручная учебная глава или исторический материал: LocalAgent: подробное руководство по проекту. |
| [docs/WORK_PLAN.md](../../docs/WORK_PLAN.md) | Ручная учебная глава или исторический материал: План дальнейшей разработки LocalAgent. |
| [docs/history/legacy-readme.md](../../docs/history/legacy-readme.md) | Ручная учебная глава или исторический материал: Исторические README до учебной документации. |
| [docs/reference/dependencies.md](../../docs/reference/dependencies.md) | Генерируемый документ: Объявленные и зафиксированные зависимости. |
| [docs/reference/design-reference.md](../../docs/reference/design-reference.md) | Генерируемый документ: Справочник архивного эталона дизайна. |
| [docs/reference/file-map.md](../../docs/reference/file-map.md) | Генерируемый документ: Карта файлов. |
| [docs/reference/python.md](../../docs/reference/python.md) | Генерируемый документ: Справочник Python. |
| [docs/reference/tests.md](../../docs/reference/tests.md) | Генерируемый документ: Справочник Python-тестов. |
| [docs/reference/typescript.md](../../docs/reference/typescript.md) | Генерируемый документ: Справочник TypeScript и JavaScript. |
| [docs/sources.md](../../docs/sources.md) | Ручная учебная глава или исторический материал: Официальные материалы для изучения. |
| [electron-builder.json](../../electron-builder.json) | Allowlist приложения, extraResources Core и локальный NSIS installer без публикации. |
| [main.py](../../main.py) | Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop. |
| [package-lock.json](../../package-lock.json) | Зафиксированное дерево npm-зависимостей; редактируется npm, а не вручную. |
| [package.json](../../package.json) | Корневой npm workspace и делегирование dev/build/typecheck. |
| [requirements-build.txt](../../requirements-build.txt) | Точные Python-зависимости для Windows x64 freeze Core без Qt. |
| [requirements-core.txt](../../requirements-core.txt) | Диапазоны OpenAI SDK и отдельного HTTPX model discovery для ядра без Qt. |
| [requirements.txt](../../requirements.txt) | Полное Python-окружение с PySide6 и сохранённой зависимостью python-dotenv. |
| [run-desktop.bat](../../run-desktop.bat) | Запуск npm dev; выбирает .venv Python, если LCA_PYTHON не задан. |
| [run.bat](../../run.bat) | Старый запуск Qt с установкой зависимостей; содержит оставшуюся ссылку на отсутствующий .env.example. |
| [skills/coding/SKILL.md](../../skills/coding/SKILL.md) | Краткий навык coding; SkillManager использует метаданные для выбора по prompt. |
| [skills/debugging/SKILL.md](../../skills/debugging/SKILL.md) | Краткий навык debugging; SkillManager использует метаданные для выбора по prompt. |
| [skills/project_analysis/SKILL.md](../../skills/project_analysis/SKILL.md) | Краткий навык project_analysis; SkillManager использует метаданные для выбора по prompt. |
| [skills/testing/SKILL.md](../../skills/testing/SKILL.md) | Краткий навык testing; SkillManager использует метаданные для выбора по prompt. |
| [tests/electron/packaged-smoke.mjs](../../tests/electron/packaged-smoke.mjs) | CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском. |
| [tests/electron/smoke.cjs](../../tests/electron/smoke.cjs) | Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop. |
| [tests/migration/test_bridge.py](../../tests/migration/test_bridge.py) | Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи. |
| [tests/migration/test_bridge_process.py](../../tests/migration/test_bridge_process.py) | Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval. |
| [tests/migration/test_model_discovery.py](../../tests/migration/test_model_discovery.py) | HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета. |
| [tests/migration/test_model_probe.py](../../tests/migration/test_model_probe.py) | Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены. |
| [tests/migration/test_streaming.py](../../tests/migration/test_streaming.py) | Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки. |
| [tests/migration/test_task_service.py](../../tests/migration/test_task_service.py) | HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация. |
| [tests/test_approval_flow.py](../../tests/test_approval_flow.py) | Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6. |
| [tests/test_chat_store.py](../../tests/test_chat_store.py) | Создание, изменение, переименование и удаление чата в изолированном store. |
| [tests/test_conversation_history.py](../../tests/test_conversation_history.py) | Выбор истории и сокращение tool outputs/пар в conversation.py. |
| [tests/test_editor_io.py](../../tests/test_editor_io.py) | Чтение/сохранение существующих файлов, размер и отказ вне корня. |
| [tests/test_editor_service.py](../../tests/test_editor_service.py) | Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope. |
| [tests/test_file_editing.py](../../tests/test_file_editing.py) | Preview без записи, explicit approval, overwrite и путь файла. |
| [tests/test_limits.py](../../tests/test_limits.py) | Настраиваемое число entries и глубина обхода. |
| [tests/test_model_gateway.py](../../tests/test_model_gateway.py) | Параметры endpoint удалённого/совместимого провайдера. |
| [tests/test_model_manager.py](../../tests/test_model_manager.py) | Сканирование GGUF, quantization, свободный порт и остановленный runtime. |
| [tests/test_model_preferences.py](../../tests/test_model_preferences.py) | Whitelist настроек, defaults и отказ URL с credentials/неверным портом. |
| [tests/test_project_memory.py](../../tests/test_project_memory.py) | Изоляция, лимиты, merge, формат контекста и очистка памяти. |
| [tests/test_runtime_architecture.py](../../tests/test_runtime_architecture.py) | Структура плана, skills, размер контекста и verifier. |
| [tests/test_sandbox.py](../../tests/test_sandbox.py) | Обёртка запуска внутренней security self-test suite. |
| [tests/test_task_activity.py](../../tests/test_task_activity.py) | Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery. |
| [tests/test_task_store.py](../../tests/test_task_store.py) | Round-trip checkpoint, переход этапа, завершение и очистка. |
| [tools/build_windows_core.py](../../tools/build_windows_core.py) | PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков. |
| [tools/check_docs.py](../../tools/check_docs.py) | Проверка локальных ссылок, source lines, покрытия аннотаций и актуальности каталога. |
| [tools/doc_notes.py](../../tools/doc_notes.py) | Ручные назначения файлов и символов для справочников; не является runtime-модулем агента. |
| [tools/extract_ts_symbols.cjs](../../tools/extract_ts_symbols.cjs) | TypeScript Compiler API: структурные объявления TS/JS без исполнения приложения. |
| [tools/generate_code_reference.py](../../tools/generate_code_reference.py) | Извлекает объявления из Python/TypeScript AST и создаёт Markdown-каталоги. |
