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
| [agent/chat_store.py](../../agent/chat_store.py) | JSON-чаты и индекс истории вне папки проекта. |
| [agent/companion_policy.py](../../agent/companion_policy.py) | Граница делегирования Лолы по исходному намерению человека и очистка ответов/озвучки от разметки. |
| [agent/companion_preferences.py](../../agent/companion_preferences.py) | Независимый сохраняемый профиль Лолы: модель, endpoint, характер, STT и голос; секреты не сохраняются. |
| [agent/connection_profiles.py](../../agent/connection_profiles.py) | Именованные публичные конфигурации моделей без API-ключей. |
| [agent/context_manager.py](../../agent/context_manager.py) | Сборка временного рабочего контекста с метаданными задачи, умным сжатием и статистикой. |
| [agent/conversation.py](../../agent/conversation.py) | Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп. |
| [agent/delegation.py](../../agent/delegation.py) | Единственное определение delegate_task для передачи сложной задачи от Лолы основной модели. |
| [agent/editor_io.py](../../agent/editor_io.py) | Самостоятельные sandbox-функции текстового редактора; React preview их не использует для записи. |
| [agent/engine.py](../../agent/engine.py) | Независимый от UI цикл модели, инструментов, подтверждений, памяти и checkpoint. |
| [agent/json_tools.py](../../agent/json_tools.py) | Текстовый JSON tool protocol: преобразование истории, строгий parser envelope и адаптация stream к обычному executor. |
| [agent/mcp.py](../../agent/mcp.py) | Реестр MCP-конфигураций без транспорта и исполнения внешних tools. |
| [agent/mcp_client.py](../../agent/mcp_client.py) | Настоящие соединения MCP stdio/Streamable HTTP с discovery, ограничениями, отменой и закрытием transport. |
| [agent/model_client.py](../../agent/model_client.py) | Отменяемый async HTTP-клиент с синхронной поверхностью для движка. |
| [agent/model_discovery.py](../../agent/model_discovery.py) | HTTPX-получение списка моделей с общим deadline, ограничением ответа и отменой сокета. |
| [agent/model_gateway.py](../../agent/model_gateway.py) | Отдельное представление endpoint провайдера/локального runtime; не включено в TaskService. |
| [agent/model_manager.py](../../agent/model_manager.py) | Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции. |
| [agent/model_preferences.py](../../agent/model_preferences.py) | Валидация endpoint и whitelist числовых настроек, миграция старого JSON и атомарное сохранение без API-ключа. |
| [agent/model_probe.py](../../agent/model_probe.py) | Ограниченная отменяемая проверка draft-модели через Chat Completions без файлов, истории и сохранения настроек. |
| [agent/planner.py](../../agent/planner.py) | Структура этапа и детерминированный план по словам запроса. |
| [agent/process_job.py](../../agent/process_job.py) | Windows Job Object: kill-on-close только для собственного Popen и его потомков. |
| [agent/progress_guard.py](../../agent/progress_guard.py) | Окно отпечатков вызовов и результатов для остановки чередующихся циклов без продвижения. |
| [agent/project_command.py](../../agent/project_command.py) | Опциональный запуск тестов/сборок после отдельного подтверждения; ограниченный вывод, время и ProcessJob. |
| [agent/project_memory.py](../../agent/project_memory.py) | Компактная структурированная память проекта, очистка и форматирование для модели. |
| [agent/projects.py](../../agent/projects.py) | Атомарное хранение именованных пространств: папка, инструкции и метаданные. |
| [agent/responses_adapter.py](../../agent/responses_adapter.py) | Преобразование канонической истории и потоковых событий OpenAI Responses в существующий цикл агента. |
| [agent/runtime.py](../../agent/runtime.py) | Связь контекста, планировщика, навыков, verifier и MCP-реестра; часть границ ещё не подключена. |
| [agent/security.py](../../agent/security.py) | Канонический корень и разрешение путей только внутри выбранного проекта. |
| [agent/skills.py](../../agent/skills.py) | Обнаружение, краткие метаданные, чтение и выбор SKILL.md по словам. |
| [agent/smart_context.py](../../agent/smart_context.py) | Детерминированное сжатие временного контекста с архивом ограничений и фактов без LLM-запросов и изменения канонической истории. |
| [agent/task_activity.py](../../agent/task_activity.py) | Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории. |
| [agent/task_store.py](../../agent/task_store.py) | JSON-контрольные точки задач, этапы, статусы и восстановление. |
| [agent/tools.py](../../agent/tools.py) | Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test. |
| [agent/ui.py](../../agent/ui.py) | Сохранённый Qt GUI: панели, readonly preview, настройки, чат и approval dialog. |
| [agent/verifier.py](../../agent/verifier.py) | Отдельная детерминированная проверка результата этапа; engine не вызывает её автоматически. |
| [agent/worker.py](../../agent/worker.py) | Qt QThread-адаптер вокруг AgentEngine; преобразует callbacks в Signal. |
| [apps/desktop/.gitignore](../../apps/desktop/.gitignore) | Локальные исключения выходных директорий desktop-сборки. |
| [apps/desktop/build-electron.mjs](../../apps/desktop/build-electron.mjs) | Две Vite library-сборки в main.cjs и preload.cjs с внешними системными импортами. |
| [apps/desktop/electron/assistantMedia.ts](../../apps/desktop/electron/assistantMedia.ts) | Повторная host-валидация фиксированных музыкальных HTTPS URL и реального локального аудиофайла внутри разрешённых папок. |
| [apps/desktop/electron/desktopApps.ts](../../apps/desktop/electron/desktopApps.ts) | Каталог локально разрешённых EXE: системные приложения, выбор пользователем, ID без путей для модели и запуск без shell/аргументов. |
| [apps/desktop/electron/main.ts](../../apps/desktop/electron/main.ts) | Окно, Python-процесс, pending RPC, проверка sender и фиксированные IPC handlers. |
| [apps/desktop/electron/preload.ts](../../apps/desktop/electron/preload.ts) | Узкий window.lca API и отписываемый listener событий. |
| [apps/desktop/electron/speechRuntime.ts](../../apps/desktop/electron/speechRuntime.ts) | Запуск фиксированного локального Piper, установка проверенной Serena, health и остановка только своего процесса. |
| [apps/desktop/index.html](../../apps/desktop/index.html) | HTML-узел React и модульный entry point renderer. |
| [apps/desktop/package.json](../../apps/desktop/package.json) | Зависимости Electron/React и dev/build/typecheck-скрипты workspace. |
| [apps/desktop/src/App.tsx](../../apps/desktop/src/App.tsx) | React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff. |
| [apps/desktop/src/AppearanceSettings.tsx](../../apps/desktop/src/AppearanceSettings.tsx) | Проверенные локальные настройки темы, акцента, плотности и панелей, синхронизация React и форма оформления. |
| [apps/desktop/src/BrandMark.tsx](../../apps/desktop/src/BrandMark.tsx) | Векторный знак Neutral: N и точка равновесия; цвет наследуется от темы. |
| [apps/desktop/src/ChatText.tsx](../../apps/desktop/src/ChatText.tsx) | Безопасные текстовые/code блоки без HTML, memoized parser и явное копирование. |
| [apps/desktop/src/CompanionSettings.tsx](../../apps/desktop/src/CompanionSettings.tsx) | Настройка характера, независимой модели, JSON/native protocol, автоматической передачи и STT Лолы. |
| [apps/desktop/src/ConnectionProfiles.tsx](../../apps/desktop/src/ConnectionProfiles.tsx) | Сохранение, выбор и удаление публичных профилей подключения модели. |
| [apps/desktop/src/ConnectionsSettings.tsx](../../apps/desktop/src/ConnectionsSettings.tsx) | Настройка PC-инструментов и Telegram; явное подключение владельца и защищённое сохранение токена. |
| [apps/desktop/src/ConversationSidebar.tsx](../../apps/desktop/src/ConversationSidebar.tsx) | Проекты, поиск разговоров, закрепление, архив, копии, повтор, экспорт, перемещение и удаление. |
| [apps/desktop/src/EditorPanel.tsx](../../apps/desktop/src/EditorPanel.tsx) | Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение. |
| [apps/desktop/src/ExtensionsSettings.tsx](../../apps/desktop/src/ExtensionsSettings.tsx) | Настройки наборов, отдельных tools, навыков, JSON-пакетов и MCP серверов. |
| [apps/desktop/src/GenerationFields.tsx](../../apps/desktop/src/GenerationFields.tsx) | Единые типы, значения, диапазоны, подсказки и форма генерации для Chat/IDE и отдельной модели Лолы. |
| [apps/desktop/src/LocalRuntimePanel.tsx](../../apps/desktop/src/LocalRuntimePanel.tsx) | Реальный GGUF picker, context/GPU, lifecycle status и явный перенос endpoint в настройки. |
| [apps/desktop/src/LolaAvatar.tsx](../../apps/desktop/src/LolaAvatar.tsx) | Персонаж по референсу: выбор позы из атласа по состоянию Лолы, подпись, речевая волна и уменьшение движения. |
| [apps/desktop/src/MemoryPanel.tsx](../../apps/desktop/src/MemoryPanel.tsx) | Редактор семи полей памяти выбранного проекта с сохранением draft при конфликте. |
| [apps/desktop/src/ModelSettings.tsx](../../apps/desktop/src/ModelSettings.tsx) | Общее окно Neutral с боковыми разделами моделей, Лолы, расширений, ПК, оформления, контекста и runtime. |
| [apps/desktop/src/NeuralAudio.tsx](../../apps/desktop/src/NeuralAudio.tsx) | Единый плеер нейроозвучки: PCM WAV из Core, громкость/темп, Stop и подтверждение завершения. |
| [apps/desktop/src/ProjectSearch.tsx](../../apps/desktop/src/ProjectSearch.tsx) | Боковой поиск и Ctrl+P: один IPC-запрос за раз, отмена и защита от устаревших результатов. |
| [apps/desktop/src/TaskProgress.tsx](../../apps/desktop/src/TaskProgress.tsx) | Типизированная панель этапов, инструментов, результатов и продолжения задачи. |
| [apps/desktop/src/VoicePanel.tsx](../../apps/desktop/src/VoicePanel.tsx) | Рабочий разговор с Лолой без file tools, системная озвучка, голос/темп/громкость/Stop и честный отключённый STT. |
| [apps/desktop/src/VoiceSettings.tsx](../../apps/desktop/src/VoiceSettings.tsx) | Общая страница голоса Лолы с громкостью, скоростью, автоматической озвучкой и расширенной конфигурацией. |
| [apps/desktop/src/WakeListener.tsx](../../apps/desktop/src/WakeListener.tsx) | Явно включаемый микрофон во всех режимах: speech gate, STT, wake phrase, пауза при задаче/озвучке/ручной записи. |
| [apps/desktop/src/Welcome.tsx](../../apps/desktop/src/Welcome.tsx) | Пустое состояние Neutral с короткими сценариями и переходом в IDE. |
| [apps/desktop/src/assets/miya-states.png](../../apps/desktop/src/assets/miya-states.png) | Прозрачный 4×2 атлас поз светловолосой аниме-горничной по пользовательскому референсу. |
| [apps/desktop/src/assets/miya-states.prompt.md](../../apps/desktop/src/assets/miya-states.prompt.md) | Сохранённые prompts встроенного image_gen и схема ячеек персонажа. |
| [apps/desktop/src/main.tsx](../../apps/desktop/src/main.tsx) | Подключает CSS, создаёт React root и отображает App в StrictMode. |
| [apps/desktop/src/microphone.ts](../../apps/desktop/src/microphone.ts) | 16 kHz mono PCM16 WAV: подавление шума, блоки 64 мс, завершение по паузе, обрезка тишины и освобождение микрофона. |
| [apps/desktop/src/style.css](../../apps/desktop/src/style.css) | Стили IDE-панелей, сообщений, формы, modal и индикатора streaming. |
| [apps/desktop/src/styles/base.css](../../apps/desktop/src/styles/base.css) | Базовые панели, редактор, сообщения, подтверждения и карточки задачи; начало сохранённого CSS-каскада. |
| [apps/desktop/src/styles/companion.css](../../apps/desktop/src/styles/companion.css) | Сетка ассистента, атлас состояний и модальное окно настроек голоса. |
| [apps/desktop/src/styles/modern.css](../../apps/desktop/src/styles/modern.css) | Актуальные токены тёмной/светлой темы, акценты, плотность, скрытие панелей и розовое оформление Лолы. |
| [apps/desktop/src/styles/neutral.css](../../apps/desktop/src/styles/neutral.css) | Общий дизайн Neutral: токены тем, боковая навигация, проекты, настройки, адаптация размера и reduced motion. |
| [apps/desktop/src/styles/workspaces.css](../../apps/desktop/src/styles/workspaces.css) | Расположение Chat/IDE, общие окна и компоненты; сохранённый каскад без устаревших SVG-селекторов. |
| [apps/desktop/src/vite-env.d.ts](../../apps/desktop/src/vite-env.d.ts) | Vite reference, CoreEvent и TypeScript-контракт Window.lca. |
| [apps/desktop/src/voiceText.ts](../../apps/desktop/src/voiceText.ts) | Очистка презентационной разметки потокового ответа Лолы перед показом и озвучкой. |
| [apps/desktop/src/wakePhrase.ts](../../apps/desktop/src/wakePhrase.ts) | Нормализация русской фразы и выделение команды только после совпадающего начала без потери пунктуации команды. |
| [apps/desktop/tsconfig.electron.json](../../apps/desktop/tsconfig.electron.json) | Статическая проверка Node/Electron main и preload без emit. |
| [apps/desktop/tsconfig.json](../../apps/desktop/tsconfig.json) | Статическая проверка React/DOM/JSX-кода renderer. |
| [apps/desktop/vite.config.ts](../../apps/desktop/vite.config.ts) | React-плагин, относительные assets, фиксированный локальный dev-порт и outDir. |
| [assets/neutral.ico](../../assets/neutral.ico) | Многоразмерная иконка установщика/Windows: PNG-кадры от 16 до 256 пикселей. |
| [assets/neutral.png](../../assets/neutral.png) | Иконка окна Neutral, 512 пикселей, полученная из исходного SVG. |
| [assets/neutral.svg](../../assets/neutral.svg) | Редактируемый векторный исходник знака приложения и его фона. |
| [core/python/assistant_service.py](../../core/python/assistant_service.py) | Локальные часы, ограниченный AST-калькулятор, атомарные заметки и отменяемые таймеры Лолы. |
| [core/python/bridge.py](../../core/python/bridge.py) | JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout. |
| [core/python/conversation_service.py](../../core/python/conversation_service.py) | Операции организации чатов с проверкой пространства, режима и корня файлов. |
| [core/python/desktop_service.py](../../core/python/desktop_service.py) | Явно включаемые PC tools: human-prompt folder grants, read-only файлы, bounded web search и host screenshot broker. |
| [core/python/editor_service.py](../../core/python/editor_service.py) | Ручной editor-протокол: strict UTF-8 чтение с revision, preview, одноразовый Apply через существующую атомарную snapshot-запись. |
| [core/python/extension_service.py](../../core/python/extension_service.py) | Единый реестр разрешённых возможностей, progressive skills, импорт пакетов и снимки для одного запуска. |
| [core/python/memory_service.py](../../core/python/memory_service.py) | Строгий read/edit API памяти проекта с byte revision и защитой повреждённых файлов. |
| [core/python/neural_speech.py](../../core/python/neural_speech.py) | Отменяемый HTTP TTS: bounded PCM WAV, события звука и точное подтверждение плеера по sequence. |
| [core/python/project_search.py](../../core/python/project_search.py) | Ограниченный read-only поиск текста и путей с отменяемым отдельным worker. |
| [core/python/runtime_service.py](../../core/python/runtime_service.py) | Неблокирующий сервис запуска/остановки GGUF и состояний собственного llama-server. |
| [core/python/speech_service.py](../../core/python/speech_service.py) | Windows System.Speech через фиксированный PowerShell script и stdin JSON: каталог, TTS, Stop и owned job. |
| [core/python/task_service.py](../../core/python/task_service.py) | Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval. |
| [core/python/telegram_service.py](../../core/python/telegram_service.py) | Telegram long polling только для owner user ID: команды, состояние, ответы и текущие diff/approval; токен только в памяти Core. |
| [core/python/transcription_service.py](../../core/python/transcription_service.py) | Ограниченная WAV-транскрипция через локальный whisper.cpp или совместимый API с отменой HTTP. |
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
| [docs/AUDIT_2026-10-24.md](../../docs/AUDIT_2026-10-24.md) | Ручная учебная глава или исторический материал: Проверка проекта от 24 октября 2026. |
| [docs/AUTONOMOUS_PLAN_2026-10-23.md](../../docs/AUTONOMOUS_PLAN_2026-10-23.md) | Ручная учебная глава или исторический материал: Автономный план LocalAgent — 23 октября 2026. |
| [docs/EXPANSION_PLAN.md](../../docs/EXPANSION_PLAN.md) | Ручная учебная глава или исторический материал: План расширения LocalAgent. |
| [docs/NEURAL_VOICE_PLAN.md](../../docs/NEURAL_VOICE_PLAN.md) | Ручная учебная глава или исторический материал: План нейроозвучки и фразы активации. |
| [docs/NEUTRAL_PLAN_2026-10-25.md](../../docs/NEUTRAL_PLAN_2026-10-25.md) | Ручная учебная глава или исторический материал: Neutral: план сеанса 25 октября 2026. |
| [docs/README.md](../../docs/README.md) | Ручная учебная глава или исторический материал: Neutral: подробное руководство по проекту. |
| [docs/SERENA_TRAINING_PLAN.md](../../docs/SERENA_TRAINING_PLAN.md) | Разрешение, этапы и критерии пробной Serena, Windows окружение, provenance датасета, ограничения и восстановление обучения. |
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
| [packaging/RELEASE_NOTES.md](../../packaging/RELEASE_NOTES.md) | Публикуемые инструкции установки, состав и реальные ограничения Windows prerelease. |
| [packaging/llama-LICENSE.txt](../../packaging/llama-LICENSE.txt) | MIT-лицензия ggml авторов из официального llama.cpp b11829. |
| [packaging/prerequisites.nsh](../../packaging/prerequisites.nsh) | NSIS bootstrap Visual C++: проверка версии реестра, офлайн-запуск, обработка ошибки и перезагрузки. |
| [packaging/release.json](../../packaging/release.json) | Явное намерение выпустить указанную версию; изменение запускает Release workflow текущей ветки. |
| [packaging/windows-dependencies.json](../../packaging/windows-dependencies.json) | Версии, официальные URL и SHA256 Windows runtime зависимостей. |
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
| [tests/electron/desktop-apps.cjs](../../tests/electron/desktop-apps.cjs) | Node-проверка границы каталога приложений: ID, запрет путей/команд, EXE, повторное добавление, удаление и браузер без реальных окон. |
| [tests/electron/microphone.cjs](../../tests/electron/microphone.cjs) | Проверка захвата и обрезки WAV с фиктивным AudioContext без записи реального микрофона. |
| [tests/electron/neutral-smoke.cjs](../../tests/electron/neutral-smoke.cjs) | Изолированная GUI-проверка нового Neutral: проекты/навыки/MCP/Node, подтверждения, история, темы и удаление. |
| [tests/electron/packaged-smoke.mjs](../../tests/electron/packaged-smoke.mjs) | CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском. |
| [tests/electron/smoke.cjs](../../tests/electron/smoke.cjs) | Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop. |
| [tests/fixtures/mcp_echo.py](../../tests/fixtures/mcp_echo.py) | Настоящий локальный MCP сервер арифметики и ожидания для stdio/HTTP проверок. |
| [tests/migration/test_bridge.py](../../tests/migration/test_bridge.py) | Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи. |
| [tests/migration/test_bridge_process.py](../../tests/migration/test_bridge_process.py) | Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval. |
| [tests/migration/test_delegation.py](../../tests/migration/test_delegation.py) | Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории. |
| [tests/migration/test_json_protocol.py](../../tests/migration/test_json_protocol.py) | Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor. |
| [tests/migration/test_model_discovery.py](../../tests/migration/test_model_discovery.py) | HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета. |
| [tests/migration/test_model_probe.py](../../tests/migration/test_model_probe.py) | Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены. |
| [tests/migration/test_neural_speech.py](../../tests/migration/test_neural_speech.py) | HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука. |
| [tests/migration/test_streaming.py](../../tests/migration/test_streaming.py) | Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки. |
| [tests/migration/test_task_service.py](../../tests/migration/test_task_service.py) | HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация. |
| [tests/migration/test_transcription.py](../../tests/migration/test_transcription.py) | Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону. |
| [tests/migration/test_tts_server.py](../../tests/migration/test_tts_server.py) | HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов. |
| [tests/test_approval_flow.py](../../tests/test_approval_flow.py) | Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6. |
| [tests/test_assistant_service.py](../../tests/test_assistant_service.py) | Проверки утилит Лолы, сохранения заметок, таймеров, музыки и папок из исходного prompt. |
| [tests/test_chat_store.py](../../tests/test_chat_store.py) | Создание, изменение, переименование и удаление чата в изолированном store. |
| [tests/test_companion_policy.py](../../tests/test_companion_policy.py) | Границы coding intent Лолы, очистка Markdown, математики и внутренних тегов. |
| [tests/test_conversation_history.py](../../tests/test_conversation_history.py) | Выбор истории и сокращение tool outputs/пар в conversation.py. |
| [tests/test_editor_io.py](../../tests/test_editor_io.py) | Чтение/сохранение существующих файлов, размер и отказ вне корня. |
| [tests/test_editor_service.py](../../tests/test_editor_service.py) | Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope. |
| [tests/test_expansion.py](../../tests/test_expansion.py) | Контракты разделения истории, профиля без секретов, JSON tools, KV whitelist, PC grants, Telegram owner и WAV validation. |
| [tests/test_file_editing.py](../../tests/test_file_editing.py) | Preview без записи, explicit approval, overwrite и путь файла. |
| [tests/test_limits.py](../../tests/test_limits.py) | Настраиваемое число entries и глубина обхода. |
| [tests/test_memory_service.py](../../tests/test_memory_service.py) | Память UI: CAS, invalid payload, corrupt file, scope и полный Unicode budget. |
| [tests/test_model_gateway.py](../../tests/test_model_gateway.py) | Параметры endpoint удалённого/совместимого провайдера. |
| [tests/test_model_manager.py](../../tests/test_model_manager.py) | Сканирование GGUF, quantization, свободный порт и остановленный runtime. |
| [tests/test_model_preferences.py](../../tests/test_model_preferences.py) | Whitelist настроек, defaults и отказ URL с credentials/неверным портом. |
| [tests/test_neutral_conversations.py](../../tests/test_neutral_conversations.py) | Изоляция проектов/режимов, архив, удаление, копия/повтор, экспорт и профили без ключей. |
| [tests/test_neutral_extensions.py](../../tests/test_neutral_extensions.py) | Переключатели, неизменяемый снимок, навыки-черновики, пакеты и реальные MCP transports. |
| [tests/test_project_command.py](../../tests/test_project_command.py) | Подтверждение и отказ запуска, корень cwd, код возврата, лимит вывода и отмена процесса. |
| [tests/test_project_memory.py](../../tests/test_project_memory.py) | Изоляция, лимиты, merge, формат контекста и очистка памяти. |
| [tests/test_project_search.py](../../tests/test_project_search.py) | Поиск: Unicode, фильтры, лимиты, пропуски бинарных файлов, отмена и single-flight. |
| [tests/test_responses_adapter.py](../../tests/test_responses_adapter.py) | Локальная HTTP/SSE фикстура OpenAI Responses: текст, функции, reasoning items, probe и retry. |
| [tests/test_runtime_architecture.py](../../tests/test_runtime_architecture.py) | Структура плана, skills, размер контекста и verifier. |
| [tests/test_runtime_service.py](../../tests/test_runtime_service.py) | Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup. |
| [tests/test_sandbox.py](../../tests/test_sandbox.py) | Обёртка запуска внутренней security self-test suite. |
| [tests/test_smart_context.py](../../tests/test_smart_context.py) | Проверки архива, неизменности истории, пар tools, полного кода, JSON и дедупликации. |
| [tests/test_speech_service.py](../../tests/test_speech_service.py) | TTS без динамиков/микрофона: WAV, JSON data boundary, cancellation и timeout cleanup. |
| [tests/test_task_activity.py](../../tests/test_task_activity.py) | Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery. |
| [tests/test_task_store.py](../../tests/test_task_store.py) | Round-trip checkpoint, переход этапа, завершение и очистка. |
| [tests/test_windows_dependencies.py](../../tests/test_windows_dependencies.py) | Тесты закреплённых загрузок: кэш без сети, отклонение подмены и атомарная замена повреждённого файла. |
| [tools/build_windows_core.py](../../tools/build_windows_core.py) | PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков. |
| [tools/check_docs.py](../../tools/check_docs.py) | Проверка локальных ссылок, source lines, покрытия аннотаций и актуальности каталога. |
| [tools/check_live_model.py](../../tools/check_live_model.py) | Opt-in smoke реальной модели: disposable AppData/проект, Chat/IDE/Лола, без approvals записи, JSON отчёт. |
| [tools/doc_notes.py](../../tools/doc_notes.py) | Ручные назначения файлов и символов для справочников; не является runtime-модулем агента. |
| [tools/extract_ts_symbols.cjs](../../tools/extract_ts_symbols.cjs) | TypeScript Compiler API: структурные объявления TS/JS без исполнения приложения. |
| [tools/generate_brand_icons.py](../../tools/generate_brand_icons.py) | Разработка: рендер SVG через Qt и запись PNG/многоразмерного ICO без Pillow. |
| [tools/generate_code_reference.py](../../tools/generate_code_reference.py) | Извлекает объявления из Python/TypeScript AST и создаёт Markdown-каталоги. |
| [tools/prepare_windows_dependencies.py](../../tools/prepare_windows_dependencies.py) | Загрузка официальных зависимостей по SHA256, выбор server/DLL и подготовка офлайн-пакета без запуска установщиков. |
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
