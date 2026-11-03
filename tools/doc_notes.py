"""Ручные объяснения для генерируемого справочника; код здесь не запускает агента."""

# Bundled third-party source stays in the inventory, outside our API reference.
THIRD_PARTY_SOURCES = frozenset({'codex-skills.mjs'})

CURRENT_FILE_NOTES = {
 'apps/desktop/ide.html':'HTML entrypoint независимой панели в Code-OSS webview.',
 'apps/desktop/shared/createApi.ts':'Общая фабрика фиксированного API для Electron preload и Code-OSS транспорта.',
 'apps/desktop/src/design/ForestSpot.tsx':'Иллюстративные акценты LESHY из подготовленных прозрачных WebP.',
 'apps/desktop/src/design/Ornaments.tsx':'Общие SVG-мотивы рамок, углов, разделителей и лесного акцента.',
 'apps/desktop/src/design/themes.ts':'Типы, нормализация и применение трёх тем LESHY.',
 'apps/desktop/src/design/ide-theme.css':'Токены оформления IDE для трёх тем LESHY.',
 'apps/desktop/src/design/leshy.css':'Базовая палитра и общие поверхности LESHY.',
 'apps/desktop/src/design/leshy-dialogs.css':'Оформление вложенных окон, подтверждений и настроек.',
 'apps/desktop/src/design/leshy-illustrations.css':'Размещение иллюстраций LESHY с отключаемыми фонами.',
 'apps/desktop/src/design/leshy-lola.css':'Применение LESHY к прозрачному окну и bubble Лолы.',
 'apps/desktop/src/design/leshy-motifs.css':'Орнаменты и стыки панелей без перекрытия рабочего текста.',
 'apps/desktop/src/design/leshy-workspace.css':'Оформление главного рабочего пространства LESHY.',
 'apps/desktop/src/ideEntry.ts':'Адаптер API Code-OSS webview к общему window.lca.',
 'apps/desktop/src/idePanel/entry.tsx':'Монтирует независимый AgentWorkspace и его стили.',
 'apps/desktop/src/idePanel/runActivity.tsx':'Карточки этапов, инструментов, проверок и разрешения неизвестных эффектов.',
 'apps/desktop/src/idePanel/workspace.tsx':'Независимая панель диалога, истории, подключений и действий агента.',
 'apps/desktop/src/idePanel/workspace.css':'Адаптивные стили независимой IDE-панели и approvals.',
 'core/python/ide_completion.py':'Небольшой локальный запрос автодополнения без инструментов с проверкой контекста.',
 'core/python/ide_sessions.py':'Изолированные представления единого Core и editor-owned операции через scoped adapter.',
 'prototypes/neutral-ide/extension/agent-view.cjs':'Webview provider новой панели, локальные ресурсы и маршрутизация сообщений.',
 'prototypes/neutral-ide/extension/client.cjs':'Авторизованный клиент связи extension с общим Core.',
 'prototypes/neutral-ide/extension/workspace.cjs':'Проверки dirty/version/hash и применение подтверждённых изменений средствами редактора.',
 'prototypes/neutral-ide/leshy-workbench.css':'Оформление закреплённого Code-OSS runtime без изменения пользовательского VS Code.',
 'tests/electron/leshy-themes.cjs':'Изолированная Electron-проверка трёх тем, настроек и состояний окон.',
 'tests/electron/neutral-ide-integration.cjs':'Сквозная проверка Desktop → Code-OSS webview → Core → editor, истории и approvals.',
 'tests/electron/runner-exit.test.cjs':'Node VM-проверки кодов launcher: успех, ошибка, сигнал и spawn failure.',
 'tests/migration/test_ide_sessions.py':'Bridge-проверки изоляции workspace, editor receipts и отмены закрытого IDE view.',
 'tests/test_ide_completion.py':'Проверки локальности, размера запроса и завершения клиента автодополнения.',
 'tests/test_ide_execution.py':'Проверки единственного editor writer, dirty/stale guards и неизвестных эффектов.',
 'tests/test_ide_remote_control.py':'Проверки управления IDE-запуском владельцем без переключения desktop view.',
 'codex-skills.mjs':'Сторонний bundled Codex Skills CLI (MIT); учитывается как файл, его внутренности не являются API приложения.',
 'example.md':'Пользовательский демонстрационный Markdown; не является документацией API.',
 'assets/leshy-sources/PROMPTS.md':'Промпты и происхождение исходных растровых материалов LESHY.',
 'apps/desktop/src/assets/leshy/painted-spots.json':'Манифест подготовленных живописных иллюстраций LESHY.',
}

for _asset, _purpose in {
 'forest':'лесной фон', 'forest-depth':'глубокий лесной фон', 'parchment':'светлый фон',
 'autumn-birch':'осенняя берёза', 'twilight':'сумеречный фон',
 'birch-cutout':'берёза с прозрачностью', 'undergrowth-cutout':'лесной подлесок с прозрачностью',
 'spot-archive-painted':'живописный архив', 'spot-birch-painted':'живописная берёза',
 'spot-fern-painted':'живописный папоротник', 'spot-mushrooms-painted':'живописные грибы',
}.items():
    CURRENT_FILE_NOTES['apps/desktop/src/assets/leshy/'+_asset+'.webp']='Ресурс LESHY: '+_purpose+'.'
for _asset in ('forest','forest-depth','parchment','autumn-birch','twilight'):
    CURRENT_FILE_NOTES['apps/desktop/src/assets/leshy/'+_asset+'-preview.webp']='Уменьшенное preview фона '+_asset+' для выбора оформления.'
for _asset in ('band-forest','band-parchment','band-twilight','border','corner','diamond','rosette'):
    CURRENT_FILE_NOTES['apps/desktop/src/assets/leshy/'+_asset+'.svg']='Векторный мотив LESHY: '+_asset+'.'
for _theme in ('forest','parchment','twilight'):
    CURRENT_FILE_NOTES['prototypes/neutral-ide/extension/leshy-'+_theme+'.json']='Нативная тема Code-OSS LESHY '+_theme+'.'
for _asset in ('birch-cutout','forest','parchment','twilight','undergrowth-cutout','user-antler-reference'):
    CURRENT_FILE_NOTES['assets/leshy-sources/'+_asset+'.png']='Сохранённый исходный визуальный материал LESHY: '+_asset+'.'
for _extension in ('ico','png','svg'):
    CURRENT_FILE_NOTES['assets/leshy.'+_extension]='Основной знак LESHY для приложения в формате '+_extension+'.'
for _asset in ('bands-reference','motifs-reference'):
    CURRENT_FILE_NOTES['docs/leshy-brief/ornaments-2026-11-03/'+_asset+'.png']='Сохранённый образец орнаментов LESHY: '+_asset+'.'
for _asset in ('archive','birch','fern','mushrooms'):
    CURRENT_FILE_NOTES['docs/leshy-brief/retired-schematic-spots/'+_asset+'.svg']='Архив заменённой схематической иллюстрации '+_asset+'; не активный ресурс.'
for _asset in ('01_ornament_strips','02_ornament_symbols','03_illustration_1','04_illustration_2','05_illustration_3','06_illustration_4','07_illustration_5'):
    CURRENT_FILE_NOTES['docs/leshy-brief/user-images/references/'+_asset+'.png']='Пользовательский визуальный референс LESHY: '+_asset+'.'
for _asset in ('Neutral_VSCode_extension','Neutral_main_window'):
    CURRENT_FILE_NOTES['docs/leshy-brief/user-images/screenshots/'+_asset+'.png']='Пользовательский снимок исходного интерфейса: '+_asset+'.'

FILE_NOTES = {
    'agent/task_activity.py': 'Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории.',
    'tests/test_task_activity.py': 'Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery.',
    'apps/desktop/src/TaskProgress.tsx': 'Типизированная панель этапов, инструментов, результатов и продолжения задачи.',
    'requirements-build.txt': 'Точные Python-зависимости для Windows x64 freeze Core без Qt.',
    'electron-builder.json': 'Allowlist приложения, extraResources Core и локальный NSIS installer без публикации.',
    'tools/build_windows_core.py': 'PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков.',
    'tests/electron/packaged-smoke.mjs': 'CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском.',
    'tools/audit_post_stage8.py': 'Read-only синтетический аудит границ tool parser, завершения потока, проверки записи, LSP и локальных файловых политик; не вызывает внешнюю модель и не изменяет проект.',
    'apps/desktop/shared/lolaDesktop.ts': 'Общие строгие типы, defaults и проверка состояния, команд и размещения настольной Лолы.',
    'apps/desktop/electron/desktopLola.ts': 'Нативные прозрачное окно и Tray спутника Лолы, сохранение preferences, изоляция IPC и пересылка ограниченных пользовательских действий.',
    'apps/desktop/electron/lolaPreload.ts': 'Изолированный минимальный API renderer спутника без доступа к основному API Neutral.',
    'apps/desktop/lola.html': 'Отдельный HTML entrypoint спутника с локальной строгой CSP.',
    'apps/desktop/src/lola-main.tsx': 'Создаёт React root отдельного спутника и загружает только companion stylesheet.',
    'apps/desktop/src/DesktopLolaView.tsx': 'Компактная оболочка спутника: bounded chat input, управление голосом, перетаскивание, виджет состояний и вызовы узкого preload API.',
    'apps/desktop/src/DesktopLolaSettings.tsx': 'Переиспользуемая доступная форма включения спутника, режима окон, размера и анимации с применением настроек.',
    'apps/desktop/src/styles/lola-sprites.css': 'Кадровые CSS-анимации семи состояний чиби-атласа и поддержка reduced-motion.',
    'apps/desktop/src/styles/lola-desktop.css': 'Стили компактного прозрачного окна спутника, bubble и hit areas без ограничений основной IDE ширины.',
    'apps/desktop/src/assets/lola-chibi-concept-v1.png': 'Сгенерированный прозрачный полнофигурный концепт чиби Лолы; источник imagegen и промпт описаны рядом.',
    'apps/desktop/src/assets/lola-chibi-atlas-v1.png': 'Прозрачный атлас из 28 кадров в сетке 4×7 для семи состояний чиби Лолы.',
    'apps/desktop/src/assets/lola-chibi.prompt.md': 'Точные промпты и происхождение concept/sprite atlas; пользовательский исходный AVIF сюда не копируется.',
    'tests/electron/lola-desktop-smoke.cjs': 'Изолированный Electron fixture для настоящего окна/Tray Лолы, настроек, sender isolation, скрытого основного окна и единственного model/Core запроса.',
    'tests/electron/lola-preferences.cjs': 'Pure contract проверки defaults, валидации размеров/координат и bounded frame спутника.',
    'agent/model_discovery.py': 'HTTPX-получение списка моделей с общим deadline, ограничением ответа и отменой сокета.',
    'tests/migration/test_model_discovery.py': 'HTTP-фикстура discovery: валидация ответа, медленный поток, общий deadline и отмена сокета.',
    'main.py': 'Точка входа сохранённого PySide6 GUI: QApplication, MainWindow, Qt event loop.',
    'VERSION': 'Исторический маркер 5.8.0; не является единственным источником версии нового Electron-приложения.',
    'README.md': 'Краткий вход в проект, запуск и ссылка на учебное руководство.',
    'README_V6_MIGRATION.md': 'Краткая инструкция текущего Electron-пути и его проверок.',
    'MIGRATION_PLAN.md': 'Выполненные границы миграции и оставшиеся этапы.',
    'package.json': 'Корневой npm workspace и делегирование dev/build/typecheck.',
    'package-lock.json': 'Зафиксированное дерево npm-зависимостей; редактируется npm, а не вручную.',
    'requirements-core.txt': 'Диапазоны OpenAI SDK и отдельного HTTPX model discovery для ядра без Qt.',
    'requirements.txt': 'Полное Python-окружение с PySide6 и сохранённой зависимостью python-dotenv.',
    'run.bat': 'Старый запуск Qt с установкой зависимостей; содержит оставшуюся ссылку на отсутствующий .env.example.',
    'run-desktop.bat': 'Запуск npm dev; выбирает .venv Python, если LCA_PYTHON не задан.',
    '.gitignore': 'Исключает окружения, сборки, кэши, тестовые данные и секретный .env из Git.',
    '.gitattributes': 'Автоопределение текстовых файлов и нормализация переводов строк в Git.',
    '.github/workflows/validate.yml': 'Windows CI: Python/build/docs и отдельный job freeze/NSIS/packaged smoke с временным installer artifact.',
    'agent/__init__.py': 'Маркер Python-пакета agent; не запускает UI или модель.',
    'agent/chat_store.py': 'JSON-чаты и индекс истории вне папки проекта.',
    'agent/context_manager.py': 'Простой ограничитель рабочего контекста активного AgentRuntime.',
    'agent/conversation.py': 'Выбор недавних ходов и сокращение модельных сообщений с учётом tool-call групп.',
    'agent/editor_io.py': 'Самостоятельные sandbox-функции текстового редактора; React preview их не использует для записи.',
    'agent/engine.py': 'Независимый от UI цикл модели, инструментов, подтверждений, памяти и checkpoint.',
    'agent/mcp.py': 'Реестр MCP-конфигураций без транспорта и исполнения внешних tools.',
    'agent/model_client.py': 'Отменяемый async HTTP-клиент с синхронной поверхностью для движка.',
    'agent/model_gateway.py': 'Отдельное представление endpoint провайдера/локального runtime; не включено в TaskService.',
    'agent/model_manager.py': 'Сканирование GGUF, импорт и управление отдельным llama-server; без Electron UI-интеграции.',
    'agent/model_preferences.py': 'Валидация и сохранение только URL и ID модели для Electron Core.',
    'agent/planner.py': 'Структура этапа и детерминированный план по словам запроса.',
    'agent/project_memory.py': 'Компактная структурированная память проекта, очистка и форматирование для модели.',
    'agent/runtime.py': 'Связь контекста, планировщика, навыков, verifier и MCP-реестра; часть границ ещё не подключена.',
    'agent/security.py': 'Канонический корень и разрешение путей только внутри выбранного проекта.',
    'agent/skills.py': 'Обнаружение, краткие метаданные, чтение и выбор SKILL.md по словам.',
    'agent/task_store.py': 'JSON-контрольные точки задач, этапы, статусы и восстановление.',
    'agent/tools.py': 'Четыре файловых инструмента, schema для модели, dispatcher и sandbox self-test.',
    'agent/ui.py': 'Сохранённый Qt GUI: панели, readonly preview, настройки, чат и approval dialog.',
    'agent/verifier.py': 'Отдельная детерминированная проверка результата этапа; engine не вызывает её автоматически.',
    'agent/worker.py': 'Qt QThread-адаптер вокруг AgentEngine; преобразует callbacks в Signal.',
    'core/python/bridge.py': 'JSON-lines вход процесса, dispatch команд, UI-файловый API и синхронизированный stdout.',
    'core/python/task_service.py': 'Состояние выбранного чата/модели, запуск потока задачи, events и корреляция approval.',
    'apps/desktop/.gitignore': 'Локальные исключения выходных директорий desktop-сборки.',
    'apps/desktop/package.json': 'Зависимости Electron/React и dev/build/typecheck-скрипты workspace.',
    'apps/desktop/index.html': 'HTML-узел React и модульный entry point renderer.',
    'apps/desktop/vite.config.ts': 'React-плагин, относительные assets, фиксированный локальный dev-порт и outDir.',
    'apps/desktop/tsconfig.json': 'Статическая проверка React/DOM/JSX-кода renderer.',
    'apps/desktop/tsconfig.electron.json': 'Статическая проверка Node/Electron main и preload без emit.',
    'apps/desktop/build-electron.mjs': 'Vite library-сборки main.cjs, preload.cjs и изолированного lolaPreload.cjs с внешними системными импортами.',
    'apps/desktop/electron/main.ts': 'Окно, Python-процесс, single-instance lock, pending RPC, проверка sender и фиксированные IPC handlers; создаёт нативный desktop companion.',
    'apps/desktop/electron/preload.ts': 'Узкий window.lca API и отписываемый listener событий.',
    'apps/desktop/src/main.tsx': 'Подключает CSS, создаёт React root и отображает App в StrictMode.',
    'apps/desktop/src/App.tsx': 'React-состояние и представление проекта, настроек, чата, потока, checkpoint, diff и безопасного мостика действий настольной Лолы в единый голосовой контур.',
    'apps/desktop/src/style.css': 'Стили IDE-панелей, сообщений, формы, modal и индикатора streaming.',
    'apps/desktop/src/vite-env.d.ts': 'Vite reference, CoreEvent и TypeScript-контракт Window.lca.',
    'design_reference/DESIGN_REFERENCE.md': 'Пояснение сохранённого визуального эталона и границ его переноса.',
    'design_reference/agent_studio_reference.py': 'Архивный визуальный прототип с собственными механизмами; не импортируется рабочим main.py.',
    'tests/test_approval_flow.py': 'Проверяет явные решения Qt-адаптера; пропускается при отсутствии PySide6.',
    'tests/test_chat_store.py': 'Создание, изменение, переименование и удаление чата в изолированном store.',
    'tests/test_conversation_history.py': 'Выбор истории и сокращение tool outputs/пар в conversation.py.',
    'tests/test_editor_io.py': 'Чтение/сохранение существующих файлов, размер и отказ вне корня.',
    'tests/test_file_editing.py': 'Preview без записи, explicit approval, overwrite и путь файла.',
    'tests/test_limits.py': 'Настраиваемое число entries и глубина обхода.',
    'tests/test_model_gateway.py': 'Параметры endpoint удалённого/совместимого провайдера.',
    'tests/test_model_manager.py': 'Сканирование GGUF, quantization, свободный порт и остановленный runtime.',
    'tests/test_model_preferences.py': 'Whitelist настроек, defaults и отказ URL с credentials/неверным портом.',
    'tests/test_project_memory.py': 'Изоляция, лимиты, merge, формат контекста и очистка памяти.',
    'tests/test_runtime_architecture.py': 'Структура плана, skills, размер контекста и verifier.',
    'tests/test_sandbox.py': 'Обёртка запуска внутренней security self-test suite.',
    'tests/test_task_store.py': 'Round-trip checkpoint, переход этапа, завершение и очистка.',
    'tests/migration/test_bridge.py': 'Вызовы bridge.handle: health, файлы, traversal и запрет прямой записи.',
    'tests/migration/test_bridge_process.py': 'Реальный Python subprocess, malformed JSON, responsiveness и cancel при approval.',
    'tests/migration/test_task_service.py': 'HTTP-фикстура и реальный engine: apply/reject/cancel, чаты, recovery и конфигурация.',
    'tests/migration/test_streaming.py': 'Задержанный HTTP/SSE: отмена сокета, частичный текст, пакетирование и настройки.',
    'tests/electron/smoke.cjs': 'Скрытое настоящее Electron-окно: все слои, запись, поток, reload и Stop.',
    'tools/doc_notes.py': 'Ручные назначения файлов и символов для справочников; не является runtime-модулем агента.',
    'tools/generate_code_reference.py': 'Извлекает объявления из Python/TypeScript AST и создаёт Markdown-каталоги.',
    'tools/extract_ts_symbols.cjs': 'TypeScript Compiler API: структурные объявления TS/JS без исполнения приложения.',
    'tools/check_docs.py': 'Проверка локальных ссылок, source lines, покрытия аннотаций и актуальности каталога.',
}

SYMBOL_NOTES = {}

DEPENDENCY_NOTES = {
    'electron-builder': 'Упаковка Electron, включение frozen Core и создание локального NSIS installer.',
    '@vitejs/plugin-react': 'Преобразование React/JSX и интеграция с dev-server Vite.',
    'concurrently': 'Параллельный запуск dev-сервера и Electron-команды.',
    'electron': 'Настольный runtime Chromium/Node и его TypeScript API.',
    'lucide-react': 'Иконки React-компонентов интерфейса.',
    'react': 'Компоненты и hooks состояния UI.',
    'react-dom': 'Создание React root и отрисовка в DOM.',
    'vite': 'Dev-server и сборка renderer/main/preload.',
    'wait-on': 'Ожидание TCP-порта Vite перед запуском Electron.',
    '@types/react': 'Статические описания API React для TypeScript.',
    '@types/react-dom': 'Статические описания React DOM для TypeScript.',
    'typescript': 'Компилятор проверки типов и AST API генератора документации.',
}


def register(module, text):
    """Добавляет вручную написанные строки «имя | назначение» в словарь аннотаций."""
    for line in text.strip().splitlines():
        name, description = line.split('|', 1)
        SYMBOL_NOTES[f'{module}:{name.strip()}'] = description.strip()


register('agent/chat_store.py', '''
_valid_id | Проверяет 32-символьный hex UUID до доступа к пути файла чата.
_metadata | Выбирает строковые метаданные канонического чата для производного индекса.
_cache_chat | Обновляет производный индекс; отказ возвращает предупреждение, сохраняя канонический JSON.
read_chat_catalog | Сканирует канонические чаты, восстанавливает индекс и сообщает о повреждениях, не изменяя повреждённые исходники.
_now | Возвращает UTC ISO-время для метаданных чата.
_atomic_write | Записывает JSON через временный файл и replace; общую транзакцию чата с индексом не создаёт.
_load_index | Читает индекс; при отсутствующем или повреждённом JSON возвращает пустой список.
list_chats | Возвращает метаданные чатов по убыванию updated_at; фильтрацию проекта делает сервис.
create_chat | Генерирует UUID, создаёт запись и добавляет её метаданные в индекс.
load_chat | Проверяет UUID и структуру JSON; отсутствие возвращает None, повреждение даёт ошибку с сохранением исходного файла.
save_chat | С fsync атомарно сохраняет чат; отказ производного индекса возвращает предупреждение, не отменяя сохранённую историю.
delete_chat | Удаляет файл диалога и запись индекса; не меняет файлы проекта.
rename_chat | Нормализует заголовок до 120 символов и сохраняет существующий чат.
title_from_messages | Выбирает первое непустое user-сообщение и делает короткий заголовок.
''')
register('agent/conversation.py', '''
_message_size | Оценивает размер сериализованного сообщения в символах, не токенах модели.
_bounded_turn | Копирует ход и обрезает объёмные tool outputs, оставляя структуру сообщений.
select_recent_history | Выбирает недавние целые пользовательские ходы с ограничением объёма и количества.
build_messages | Глубоко копирует полную каноническую историю и добавляет новый запрос; сокращение выполняется только перед HTTP.
compact_live_messages | Сокращает текущий модельный контекст, группируя assistant tool calls и их результаты.
compact_live_messages.flatten | Собирает system-сообщение и группы сообщений в плоский список.
compact_live_messages.size | Измеряет точную длину сериализованного JSON текущего модельного контекста.
_complete_units | Сохраняет результаты частичной пачки, дополняет отсутствующие явным OUTCOME_UNKNOWN; исключает осиротевшие и некорректные обмены из проекции.
''')
register('agent/context_manager.py', '''
ContextManager | Единый builder модельного контекста с сохранением обязательных запросов и целых tool-пар.
ContextManager.build | Добавляет task/skills к копии system prompt и вызывает общий compact_live_messages с жёстким JSON-бюджетом.
''')
register('agent/editor_io.py', '''
read_project_text | Проверяет путь, существование и размер, затем возвращает Path и UTF-8 текст.
save_project_text | Сохраняет существующий файл после повторной проверки пути; не является engine approval API.
''')
register('agent/engine.py', '''
AgentEngine.task_snapshot | Возвращает независимую копию checkpoint для атомарного сохранения в записи чата.
EventHook | Синхронный набор callbacks для независимых от GUI событий движка.
EventHook.connect | Добавляет обработчик события.
EventHook.emit | Вызывает копию списка обработчиков с переданными аргументами в текущем потоке.
AgentEngine | Состояние и исполнение одного запуска модели с tools, approval, лимитами, памятью и checkpoint.
AgentEngine.requestInterruption | Выставляет Event остановки и отменяет активные сетевые future клиента.
AgentEngine.isInterruptionRequested | Возвращает текущее состояние флага остановки.
AgentEngine._checkpoint | Обновляет этап/последнее событие, сохраняет checkpoint и публикует снимок.
AgentEngine.resolve_write_approval | Принимает решение и освобождает ожидание записи; неизвестное решение превращает в reject.
AgentEngine._ask_write_approval | Запрашивает согласие через событие и ждёт apply/reject/cancel с проверкой остановки.
AgentEngine._emit_change | Публикует path/diff/status одного предложения изменения.
AgentEngine._looks_like_action_request | Эвристически распознаёт просьбу действия по русским/английским словам.
AgentEngine._verify_task_completion | Дополнительным модельным запросом проверяет, не является ли финал только планом; при ошибке проверки разрешает завершение.
AgentEngine.run | Строит контекст, выполняет потоковые ходы и tools, обрабатывает остановку, сохраняет состояние и закрывает клиент.
''')
register('agent/model_client.py', '''
ModelCancelled | Внутреннее исключение отмены модельного запроса, обрабатываемое движком.
ModelStream | Синхронный итератор над async SSE-producer с ограниченной очередью.
ModelStream._produce | Получает async stream, кладёт чанки в очередь и закрывает HTTP-контекст при выходе/отмене.
ModelStream.__iter__ | Возвращает сам поток как Python-итератор.
ModelStream.__next__ | Ожидает очередной чанк короткими интервалами, проверяет отмену и завершение future.
ModelStream.close | Отменяет future producer, закрывая незавершённый поток.
ModelClient | Async SDK в отдельном loop-потоке с синхронными create/result и отменой.
ModelClient.check_cancelled | Выбрасывает ModelCancelled, если общий Event установлен.
ModelClient.submit | Планирует корутину в сетевом loop и учитывает её future в pending.
ModelClient._forget | Убирает завершённую future из защищённого множества.
ModelClient.result | Ждёт результат короткими интервалами и переводит cancellation в исключение движка.
ModelClient.create | Возвращает ModelStream для stream=True или готовый async-ответ для stream=False.
ModelClient.cancel | Отменяет снимок всех активных future.
ModelClient.close | Отменяет async-задачи, закрывает SDK и останавливает сетевой поток/loop.
ModelClient.close.shutdown | Async-фаза закрытия: cancel/gather задач и client.close внутри принадлежащего loop.
''')
register('agent/model_preferences.py', '''
validate_preferences | Разрешает HTTP(S) endpoint без credentials/query/fragment, проверяет порт и возвращает URL/ID и whitelist settings без ключа.
load_preferences | Читает и проверяет JSON; при ошибке возвращает копию defaults, никогда не восстанавливает ключ.
save_preferences | Атомарно сохраняет whitelist полей во внешний служебный JSON.
''')
register('agent/security.py', '''
AccessDenied | Ошибка выхода за разрешённый корень или невозможности безопасно разрешить путь.
canonical_root | Раскрывает и разрешает существующий корень; требует каталог.
resolve_allowed_path | Разрешает относительный/абсолютный путь и ссылки, затем проверяет принадлежность каноническому корню.
''')
register('agent/tools.py', '''
list_files | Перечисляет разрешённые файлы с фильтрами, ограничением entries и глубины обхода.
safe_relative | Возвращает относительное POSIX-представление пути для результатов tools.
read_file | Читает UTF-8 файл не больше 120000 байт внутри корня.
search_text | Ищет подстроку в UTF-8 файлах с пределами размера, глубины, числа совпадений и длины строки.
preview_file_change | Строит unified diff и снимок SHA-256 исходных байтов/предлагаемого текста с нормализованным путём, не записывая файл.
write_file | Требует approval и совпадающий снимок preview; дважды проверяет состояние, атомарно заменяет существующий файл или создаёт новый без перезаписи.
execute_tool | Диспетчер четырёх функций; превращает ожидаемые ошибки в структурированный tool result.
run_sandbox_self_test | Выполняет изолированный внутренний unittest-набор проверки файловой границы и возвращает сводку.
run_sandbox_self_test.SandboxTests | Внутренняя suite временных project/outside каталогов; не пользовательский runtime-класс.
''')
register('agent/project_memory.py', '''
_now | Возвращает UTC ISO-время записи памяти.
_key | Хеширует нормализованный project_root для имени каталога памяти.
memory_path | Формирует путь project_memory/<hash>/memory.json.
empty_memory | Создаёт пустую структурированную память с корнем и полями версии.
_clean_text | Удаляет NUL, нормализует пробелы и ограничивает строку.
validate_memory | Проверяет структуру, поля, длины и дубликаты памяти.
load_project_memory | Загружает и валидирует запись; при ошибке создаёт пустую память.
save_project_memory | Валидирует и атомарно сохраняет JSON памяти выбранного проекта.
clear_project_memory | Удаляет только память указанного проекта.
format_memory_context | Формирует ограниченный справочный блок для system prompt.
merge_memory_update | Объединяет только разрешённые поля модельного обновления с существующей памятью и валидирует итог.
''')
register('agent/task_store.py', '''
_now | UTC ISO-время для checkpoint.
_key | SHA-256 от chat_id, сокращённый для имени файла задачи.
task_path | Возвращает путь tasks/<hash>.json.
default_stages | Делегирует построение начального списка этапов build_plan.
new_task | Создаёт словарь running-задачи с планом, счётчиками и resume_state.
save_task | Обновляет timestamp и записывает checkpoint через temporary+fsync+replace.
load_task | Читает checkpoint; отсутствие или повреждённый JSON даёт None.
clear_task | Удаляет checkpoint, не удаляя историю чата.
set_stage | Закрывает посещённый активный этап, помечает непосещённые предыдущие skipped и активирует целевой.
finish_task | Завершает посещённые этапы, пропускает pending и сохраняет итоговый статус/причину.
''')
register('agent/planner.py', '''
PlanStage | Dataclass этапа: ID, заголовок, цель, статус и декларативный max_turns.
PlanStage.to_dict | Преобразует dataclass этапа в JSON-совместимый словарь.
build_plan | Строит этапы по эвристике слов действия, добавляя реализацию только подходящим запросам.
TaskPlanner | Операции текущего этапа над переданным словарём задачи.
TaskPlanner.current | Property поиска записи текущего stage.
TaskPlanner.advance | Помечает этап done, активирует следующий и записывает пояснение.
''')
register('agent/runtime.py', '''
AgentRuntime | Граница оркестрации: планировщик, context builder, skills, verifier и MCP registry.
AgentRuntime.prepare | Выбирает навыки по prompt и записывает их ID в task.
AgentRuntime.working_context | Передаёт сообщения, task и выбранные skills в ContextManager.
AgentRuntime.checkpoint | Обновляет last_event в памяти; сам по себе не пишет JSON на диск.
AgentRuntime.complete_stage | Делегирует переход этапа TaskPlanner.advance.
''')
register('agent/skills.py', '''
SkillManager | Локальный реестр Markdown-навыков и простого лексического выбора.
SkillManager.discover | Находит SKILL.md и возвращает метаданные каждого файла.
SkillManager._metadata | Извлекает ID из каталога, заголовок, путь и краткую сводку.
SkillManager._summary | Выбирает первую подходящую строку текста как summary до 300 символов.
SkillManager.load | Читает полный текст навыка по ID; автоматически не исполняет его.
SkillManager.select | Ранжирует метаданные по словам prompt и возвращает не больше limit совпадений.
''')
register('agent/mcp.py', '''
MCPServer | Dataclass конфигурации MCP-сервера; command/args/enabled/trusted остаются данными.
MCPRegistry | Реестр конфигураций; подключения и MCP transport здесь нет.
MCPRegistry.register | Добавляет или заменяет сервер по имени.
MCPRegistry.remove | Удаляет запись по имени, если она есть.
MCPRegistry.enable | Изменяет enabled существующей записи.
MCPRegistry.list_servers | Возвращает все конфигурации как словари.
MCPRegistry.available | Выбирает записи с enabled=True, не проверяя живое соединение.
MCPRegistry.manifest | Формирует список включённых конфигураций для дальнейшей интеграции.
''')
register('agent/model_gateway.py', '''
ModelEndpoint | Dataclass параметров провайдера: URL, модель, ключ и local-флаг.
ModelGateway | Отдельная абстракция выбора provider/local endpoint; не используется TaskService.
ModelGateway.use_provider | Создаёт endpoint по введённому URL, модели и ключу.
ModelGateway.use_local | Создаёт endpoint уже запущенного LocalRuntime; иначе выбрасывает ошибку.
ModelGateway.status | Возвращает endpoint и состояние локального runtime; endpoint может содержать ключ, не публикуйте его как безопасные preferences.
''')
register('agent/model_manager.py', '''
LocalModel | Dataclass GGUF-файла с путём, именем, размером и метаданными quantization/architecture.
LocalModel.size_gb | Property размера файла в GiB-подобном делении на 1024^3.
LocalModel.to_dict | Преобразует запись модели в словарь с округлённым size_gb.
ModelManager | Сканирование и импорт GGUF в отдельный каталог моделей.
ModelManager._quantization | Определяет quantization по имени файла регулярным выражением; не анализирует бинарное содержимое.
ModelManager.scan | Рекурсивно находит .gguf и возвращает доступные записи.
ModelManager.import_model | Проверяет расширение/файл и при copy=True копирует в models_dir.
LocalRuntime | Управляет отдельным процессом llama-server и его HTTP endpoint.
LocalRuntime.find_executable | Ищет явно заданный путь, служебный runtime, текущий каталог и PATH.
LocalRuntime.free_port | Получает свободный локальный TCP-порт через временный bind.
LocalRuntime.running | Property: процесс существует и ещё не завершился.
LocalRuntime.base_url | Property URL /v1 для назначенного порта.
LocalRuntime.start | Запускает собственный llama-server с model/context/GPU flags, job и output drain; readiness до 120 секунд, отмена очищает процесс.
LocalRuntime._healthy | Проверяет HTTP /models с коротким timeout.
LocalRuntime.stop | Завершает процесс, при необходимости убивает и очищает runtime-состояние.
LocalRuntime.status | Возвращает состояние процесса, порт, URL и метаданные модели.
LocalRuntime.__del__ | Пытается закрыть процесс при удалении экземпляра; не заменяет явное управление жизненным циклом.
''')
register('agent/verifier.py', '''
StageVerifier | Детерминированная проверка наличия результата этапа; не запускает команды или тесты.
StageVerifier.verify | Для реальной задачи учитывает журнал неизвестных действий, реальные команды и stop_reason; прежний вызов без task сохранён для совместимости.
''')
register('agent/worker.py', '''
AgentWorker | QThread-адаптер: содержит AgentEngine и Qt Signals для старого интерфейса.
AgentWorker.run | Выполняет engine.run в контексте запущенного QThread.
AgentWorker.requestInterruption | Делегирует остановку общему движку, включая сеть.
AgentWorker.isInterruptionRequested | Читает флаг остановки движка.
AgentWorker.resolve_write_approval | Передаёт решение Qt-диалога в движок.
AgentWorker._approval_result | Property совместимости для проверки последнего решения в тестах.
''')
register('core/python/bridge.py', '''
emit | Сериализует один JSON-объект и под Lock пишет целую UTF-8 строку stdout.
resolve_inside | Разрешает UI-путь относительно выбранного project_root и отклоняет выход наружу.
handle | Whitelist диспетчер RPC: состояние, проект, модель, чаты, задачи и readonly UI-файлы.
main | Цикл stdin JSON-lines с ID ответов, обработкой некорректного ввода и shutdown при EOF.
''')
register('core/python/task_service.py', '''
TaskService._recover_chat | Восстанавливает состояние из embedded checkpoint, draft и точного блока tool result; при неопределённой записи требует проверки файла.
TaskService._persist_chat | Сохраняет канонический чат и отправляет warning при отказе производного индекса.
TaskService._task_event | Копирует checkpoint в тот же JSON с историей, сохраняет и публикует состояние задачи.
TaskService._persist_draft | Сохраняет текущий текст/run/turn как независимый draft и обновляет время записи.
TaskService._persist_draft_scheduled | Сохраняет последний фрагмент даже при паузе сервера; проверяет run/turn и отменяет задачу при ошибке хранения.
TaskService.start_model_discovery | Фиксирует копию настроек и запускает не больше одного discovery-потока, возвращающего ответ по исходному request ID.
TaskService.start_model_discovery.run_discovery | Получает список моделей или структурированную ошибку и вызывает callback ответа.
TaskService | Сервис одного Core-процесса: конфигурация, чат, активный run, поток и события UI.
TaskService.idle | Под RLock отказывает операции, пока task_running=True; после task_end живой завершающийся Thread не блокирует новый запрос.
TaskService.configure | Сохраняет whitelist preferences и держит API-ключ только в памяти конфигурации.
TaskService.preferences | Возвращает URL и модель без ключа.
TaskService.models | Вызывает ограниченное отменяемое HTTPX-обнаружение моделей для копии настроек.
TaskService.chats | Фильтрует индекс чатов по точной строке выбранного корня.
TaskService.select_chat | Загружает чат, восстанавливает embedded checkpoint/stream draft и возвращает предупреждения без повторного применения старого approval.
TaskService._event | Добавляет общие run_id/chat_id к событию и передаёт emit.
TaskService._flush_text | Отменяет таймер и отправляет накопленный фрагмент с ID сообщения.
TaskService._flush_scheduled | Под блокировкой допечатывает текст, только если таймер относится к текущему run.
TaskService._text_delta | Отправляет порции текста примерно через 40 мс и сохраняет первый/периодический draft для crash recovery.
TaskService._chat_event | Допечатывает буфер и публикует полное сообщение с тем же ID, согласованно с таймером.
TaskService._request_approval | Создаёт UUID предложения или немедленно отменяет его, если двигатель уже остановлен.
TaskService.resolve_approval | Проверяет актуальные run/proposal ID и разрешённое решение, затем освобождает engine wait.
TaskService.cancel | Отменяет исполнение задачи, ожидающее approval и фоновое обнаружение моделей.
TaskService.start | Проверяет задачу, готовит историю/память, подписывает события и запускает agent-task.
TaskService._save_messages | Допечатывает stream-буфер, отменяет draft-таймер и сохраняет канонические сообщения вместе с checkpoint.
TaskService._run | Завершает исполнение и сохранения, сбрасывает task_running под lock перед task_end; сообщает failed при ошибках.
TaskService.shutdown | Отменяет операции и ограниченно ждёт потоки задачи и model discovery при EOF.
''')
register('agent/ui.py', '''
ApprovalDialog | Qt-диалог readonly diff с Apply/Reject/Cancel.
MainWindow | Сохранённый PySide6 GUI со своей QSettings-конфигурацией и AgentWorker.
MainWindow._build | Собирает виджеты, панели, readonly preview, чат, кнопки и output.
MainWindow._make_simple_page | Создаёт простую Qt-страницу с заголовком и пояснением.
MainWindow._load_connection | Читает URL/ключ/модель из QSettings, в отличие от новых JSON preferences.
MainWindow._connection_dialog | Показывает поля подключения и сохраняет значения, включая ключ, в QSettings.
MainWindow._refresh_models | Синхронно запрашивает список моделей и обновляет QComboBox.
MainWindow._choose_project | Выбирает каталог Qt-диалогом, сохраняет путь и обновляет дерево/чаты.
MainWindow._refresh_tree | Строит ограниченный предпросмотр дерева файлов с фильтрами.
MainWindow._filter_tree | Ищет имена файлов по подстроке и ограничивает количество результатов.
MainWindow._open_tree_item | Переключает раскрытие каталога либо открывает файл элемента дерева.
MainWindow._open_search_item | Открывает файл, выбранный в результатах поиска имени.
MainWindow._open_file | Проверяет путь/размер и показывает UTF-8 readonly preview в новой или существующей вкладке.
MainWindow._close_preview_tab | Удаляет вкладку и освобождает Qt-виджет.
MainWindow._switch_view | Переключает боковую/центральную страницу и заголовок.
MainWindow._append_message | Экранирует текст для HTML и добавляет карточку сообщения в QTextBrowser.
MainWindow._send | Берёт prompt из формы, показывает user-сообщение и запускает агента.
MainWindow.start_agent | Создаёт чат/worker, подключает Qt Signals и блокирует повторную отправку; см. оговорку о повторном prompt в главе 11.
MainWindow._on_chat | Отображает сообщение движка и сохраняет assistant-текст в локальную историю GUI.
MainWindow._conversation_updated | Принимает модельные сообщения движка и сохраняет чат.
MainWindow._save_chat | Обновляет запись чата с текущими проектом, моделью, историей и заголовком.
MainWindow._refresh_chats | Заполняет Qt-список подходящих чатов.
MainWindow._open_chat_item | Загружает выбранный чат и отображает его строковые сообщения.
MainWindow._new_chat | Очищает текущую историю GUI, если агент не запущен.
MainWindow._load_saved_chat | Восстанавливает сохранённый QSettings chat ID и сообщения, если запись найдена.
MainWindow._approve_change | Показывает ApprovalDialog и преобразует код закрытия в решение движку.
MainWindow._log | Добавляет диагностическую строку в Qt output.
MainWindow._show_output | Переключает видимость output-панели.
MainWindow._stop_agent | Запрашивает прерывание worker и отключает повторную кнопку остановки.
MainWindow._failed | Показывает ошибку и устанавливает статус GUI.
MainWindow._finished | Возвращает кнопки и статус в состояние готовности.
MainWindow._bind_shortcuts | Регистрирует клавиатурные действия для чата и проекта.
MainWindow._enter_send | Отличает Shift+Enter для новой строки от отправки.
MainWindow.closeEvent | Запрашивает остановку и сохраняет текущий проект/chat ID при закрытии Qt-окна.
''')

register('design_reference/agent_studio_reference.py', '''
Hl.__init__.f | Создаёт QTextCharFormat для цвета/жирности/курсива подсветки прототипа.
Main.do_search.f | Фоновый обход и поиск текстовых совпадений в файлах эталона.
Main.do_search.ok | Отображает найденные пути/строки и снимает busy-состояние эталона.
Main.fetch_models.f | HTTP GET /models в отдельной фоновой задаче прототипа.
Main.fetch_models.ok | Обновляет список ID, статус соединения и начальный выбор модели эталона.
Main.resources.f | Получает RAM через необязательный psutil и VRAM через nvidia-smi в прототипе.
Main.mcp_connect.f | Экспериментально запускает subprocess и MCP initialize/tools/list в эталоне; не подключено к рабочему MCPRegistry.
Main.mcp_connect.f.rpc | Пишет JSON-RPC объект одной строкой в stdin экспериментального MCP-процесса эталона.
Main.mcp_connect.ok | Сохраняет список tools и состояние MCP-подключения прототипа.
Main.mcp_connect.bad | Показывает ошибку экспериментального MCP-подключения эталона.
''')

TEST_PURPOSES = {
    'multiple_tools_keep_same_archive_anchor_for_write_recovery': 'Несколько tools одного ответа сохраняют общий assistant anchor; восстановление учитывает точный результат записи.',
    'activity_is_bounded_metadata_with_monotonic_ids': 'Журнал содержит максимум 100 записей, устойчивые ID и метаданные без содержимого файлов.',
    'tool_outcomes_distinguish_denial_cancel_failure_and_truncation': 'Различаются отказ, отмена, ошибка и успех с ограниченной выдачей.',
    'activity_recovery_uses_anchored_result_and_is_idempotent': 'Повторённый tool ID не даёт ложного успеха; восстановление использует точный блок и не повторяется.',
    'recovery_interrupts_waiting_without_replaying_approval': 'Ожидание approval после сбоя становится interrupted без повторного согласия.',
    'stage_transitions_skip_unvisited_and_keep_only_one_active': 'Непосещённые этапы пропускаются, при возврате остаётся ровно один active.',

    'approved_write_and_preferences_survive_process_restart': 'Подтверждённая запись и настройки переживают рестарт bridge; ключ не попадает в JSON.',
    'unreadable_directory_is_not_reported_as_empty_catalog': 'Недоступный каталог чатов выдаёт ошибку вместо ложного пустого списка.',
    'missing_corrupt_and_stale_index_is_rebuilt_from_chat_files': 'Отсутствующий, повреждённый и устаревший индекс восстанавливается из канонических файлов.',
    'index_failure_does_not_lose_saved_transcript': 'Ошибка записи индекса не отменяет сохранение истории; повторный каталог исправляет кэш.',
    'corrupted_chat_is_reported_without_modifying_source': 'Повреждённый чат остаётся нетронутым, валидные чаты доступны и предупреждение содержит ID.',
    'store_rejects_path_like_chat_ids': 'Файловые пути вместо UUID не читаются, не удаляются и не сохраняются.',
    'fsync_failure_leaves_previous_chat_and_cleans_temporary_file': 'Ошибка fsync не заменяет предыдущий JSON и удаляет временный файл.',
    'embedded_checkpoint_restores_missing_task_file': 'Embedded checkpoint восстанавливает отсутствующий task-файл без потери истории.',
    'recovery_does_not_confuse_reused_tool_ids_with_old_success': 'Старый результат с повторённым tool_call_id не скрывает неопределённую новую запись.',
    'recovery_recognizes_saved_tool_result_before_task_checkpoint': 'Сохранённый результат в нужном блоке позволяет восстановить учёт успешной записи.',
    'stream_draft_is_recovered_once_and_other_run_is_preserved_separately': 'Draft текущего запуска восстанавливается один раз; чужой фрагмент сохраняется отдельно.',
    'unexpected_engine_exception_still_persists_pause_and_task_end': 'Неожиданная ошибка engine сохраняет paused и обязательно отправляет task_end.',
    'index_cache_failure_warns_without_aborting_agent': 'Отказ кэша индекса предупреждает UI, сохраняя полный успешный агентский цикл.',
    'persistence_failure_before_apply_never_writes_and_still_ends_task': 'При отказе сохранения перед Apply файл не меняется, задача завершается с ошибкой.',
    'process_kill_before_headers_recovers_user_request_and_paused_task': 'Реальный kill subprocess до HTTP-заголовков сохраняет запрос и paused при открытии.',
    'process_kill_during_stream_recovers_partial_once': 'Реальный kill во время паузы SSE восстанавливает последний сохранённый фрагмент без дубля.',
    'process_kill_during_approval_never_replays_permission': 'После kill во время approval старые ID отклоняются, resume требует нового согласия.',
    'valid_discovery_filters_invalid_ids': 'Валидный список моделей возвращается без неправильных/пустых ID.',
    'invalid_json_shape_status_and_size_are_rejected': 'Ошибочные JSON, data, HTTP status и превышение размера дают отказ.',
    'total_deadline_stops_slow_trickle': 'Общий deadline закрывает медленно поступающий HTTP body, даже если отдельные чтения не зависли.',
    'cancellation_closes_stalled_socket': 'Отмена discovery закрывает реальное зависшее HTTP-соединение.',
    'bridge_models_discovery_keeps_commands_responsive_and_pins_config': 'JSON-lines отвечает на health/новые команды во время discovery, ограничивает worker и сохраняет снимок настроек.',
    'bridge_cancel_closes_discovery_socket': 'cancel_task отвечает без ожидания discovery и закрывает его HTTP-сокет.',
    'snapshot_is_required_and_model_cannot_supply_it': 'Модельные аргументы не могут подменить обязательный снимок подтверждения.',
    'external_edit_after_preview_is_not_overwritten': 'Изменённый после diff файл не перезаписывается.',
    'deleted_existing_file_requires_new_approval': 'Удаление существующего файла после preview требует нового согласия.',
    'snapshot_binds_path_and_proposed_content': 'Снимок связан с конкретным путём и предлагаемым текстом.',
    'byte_level_line_ending_change_invalidates_preview': 'Изменение CRLF/LF обнаруживается по исходным байтам.',
    'second_snapshot_check_catches_edit_during_temp_write': 'Повторная проверка обнаруживает правку во время записи временного файла.',
    'atomic_create_refuses_file_that_appears_after_final_check': 'Атомарное создание не затирает файл, появившийся после последней проверки.',
    'matching_approval_refuses_new_external_file': 'Верный approval ID не разрешает запись поверх внешнего файла, появившегося после diff.',
    'archive_builder_keeps_all_turns_and_copies_nested_calls': 'Канонический builder сохраняет все ходы и независимо копирует вложенные tool calls.',
    'model_context_omits_unfinished_and_orphaned_tool_exchanges': 'Модель не получает незавершённые и осиротевшие tool calls/results.',
    'serialized_context_budget_keeps_current_request_and_tool_pairs': 'JSON-бюджет соблюдается с Unicode/экранированием при сохранении запроса и tool-пар.',
    'oversized_mandatory_instructions_fail_without_truncation': 'Обязательные инструкции не обрезаются молча при превышении бюджета.',
    'current_run_request_survives_internal_continuation': 'Исходный запрос текущего запуска сохраняется рядом с внутренним продолжением.',
    'long_archive_survives_model_compaction_and_service_restart': 'Длинная история сохраняется целиком после реального HTTP tool loop и повторного открытия сервиса.',
    'forced_tool_uses_single_definition_then_restores_auto': 'Первый запрос ограничен одним required-инструментом, следующие используют auto и полный набор.',
    'approval_decisions_are_explicit': 'Решения apply/reject/cancel явно доходят до Qt-адаптера движка.',
    'create_save_load_rename_delete': 'Полный жизненный цикл записи чата и индекса.',
    'followup_keeps_previous_user_and_assistant_messages': 'Повторный запрос сохраняет недавний контекст диалога.',
    'tool_call_and_tool_result_are_preserved': 'Связанные вызов и ответ инструмента сохраняются вместе.',
    'empty_history_starts_cleanly': 'Пустая история создаёт корректный первый запрос.',
    'old_turns_are_trimmed_but_recent_confirmation_context_remains': 'Старые ходы сокращаются без потери недавнего контекста согласия.',
    'live_compaction_preserves_system_original_request_and_recent_tool_pair': 'compact_live_messages сохраняет system, исходный запрос и недавнюю tool-пару.',
    'tool_results_are_bounded_without_dropping_tool_call_pair': 'Большой tool output ограничивается без удаления связанной структуры.',
    'read_and_save_inside_project': 'Editor I/O читает и сохраняет файл внутри корня.',
    'outside_file_is_denied_for_read_and_write': 'Editor I/O отклоняет чтение и запись вне корня.',
    'oversized_file_is_rejected': 'Editor I/O отклоняет слишком большой файл.',
    'nonexistent_file_cannot_be_saved': 'Editor I/O не создаёт отсутствующий файл через save.',
    'preview_does_not_write': 'Расчёт diff не меняет файловую систему.',
    'write_file_denies_without_explicit_approval': 'Неподтверждённая запись отклоняется по умолчанию.',
    'create_new_file': 'Подтверждённая запись создаёт новый файл.',
    'existing_file_requires_overwrite_flag': 'Существующий файл требует явного overwrite.',
    'overwrite_existing_file': 'Подтверждённая разрешённая замена меняет существующий текст.',
    'outside_path_denied': 'Запись вне корня не допускается.',
    'dispatch_write_requires_approval': 'Dispatcher также не обходит approval.',
    'list_files_obeys_entry_limit': 'Перечисление ограничивается настроенным количеством записей.',
    'recursive_search_obeys_depth_limit': 'Поиск учитывает предел глубины.',
    'remote_endpoint': 'Gateway создаёт правильный URL, ID и provider-флаги.',
    'scan_gguf_and_quantization': 'Сканирование выбирает GGUF и извлекает quantization из имени.',
    'free_port_is_valid': 'Полученный порт находится в допустимом диапазоне.',
    'status_stopped': 'Остановленный LocalRuntime не объявляет себя running.',
    'roundtrip_whitelists_nonsecret_fields': 'Preferences сохраняет и читает только URL/модель, отбрасывает ключ и посторонние поля.',
    'missing_corrupted_or_wrong_shape_uses_defaults': 'Отсутствующие/повреждённые preferences дают defaults.',
    'credentials_or_invalid_ports_do_not_replace_saved_preferences': 'Плохой URL не заменяет ранее сохранённые настройки.',
    'round_trip_is_project_scoped': 'Память одного проекта не смешивается с другим.',
    'validation_limits_and_deduplicates': 'Поля памяти ограничиваются и очищаются от дубликатов.',
    'context_is_compact_and_marked_as_reference': 'Память форматируется как ограниченная справочная информация.',
    'merge_preserves_missing_fields': 'Merge обновления не удаляет отсутствующие в нём старые поля.',
    'clear_only_clears_memory_file': 'Очистка памяти не удаляет другие данные.',
    'plan_has_stages': 'План содержит структурированные этапы.',
    'runtime_prepares_skills_without_tools': 'Выбор навыков не добавляет исполняемые tools сам по себе.',
    'context_is_bounded': 'ContextManager ограничивает проверяемый пример рабочего контекста.',
    'verifier_rejects_stopped_stage': 'Verifier отклоняет завершение при stop_reason.',
    'sandbox_self_test_suite': 'Внутренний набор проверок sandbox возвращает успешный итог.',
    'checkpoint_roundtrip': 'Checkpoint сохраняется, загружается, меняет этап, завершается и очищается.',
    'health': 'Bridge сообщает доступность процесса.',
    'list_and_read': 'Bridge перечисляет и читает файл выбранного проекта.',
    'parent_traversal_rejected': 'Bridge не разрешает ../ за пределами проекта.',
    'write_is_not_exposed': 'Прямого write_file RPC в bridge нет.',
    'malformed_input_does_not_reuse_previous_request_id': 'Ошибка JSON не получает ID предыдущей команды и не ломает следующий запрос.',
    'bridge_remains_responsive_during_write_approval': 'Реальный Core отвечает на health/cancel, пока engine ждёт согласия.',
    'apply_only_after_matching_approval_and_persist_history': 'Запись происходит после совпавших run/proposal ID, а история и завершение сохраняются.',
    'reject_does_not_write': 'Отказ и устаревшее подтверждение не создают файл.',
    'resume_preserves_task_and_recovery_marks_interrupted_task_paused': 'Running после сбоя восстанавливается как paused и поддерживает новую попытку.',
    'new_prompt_after_pause_creates_new_task': 'Новый prompt не выдаётся за продолжение старой задачи.',
    'cancel_while_waiting_pauses_task_and_unblocks_worker': 'Отмена освобождает approval wait и сохраняет paused.',
    'busy_task_rejects_chat_and_configuration_changes': 'Активная задача запрещает смену чата, config и второй запуск.',
    'chats_are_scoped_to_project_and_ids_cannot_escape_store': 'ID и принадлежность проекта проверяются до загрузки чата.',
    'models_and_configuration_do_not_return_key': 'Список моделей работает, а configuration response не содержит ключ.',
    'missing_model_and_bad_url_are_rejected': 'Запуск без модели и неверные URL отклоняются.',
    'cancel_before_server_returns_headers': 'Отмена закрывает TCP до HTTP-заголовков без ожидания network timeout.',
    'cancel_during_stalled_sse_preserves_displayed_text': 'Отмена закрывает зависший SSE и сохраняет уже показанный текст.',
    'text_arrives_before_response_finishes': 'Первый чанк виден раньше завершения модельного ответа.',
    'cancel_memory_request_does_not_mark_task_completed': 'Отмена необязательного memory-запроса оставляет task paused.',
    'preferences_reload_does_not_restore_api_key': 'Новый сервис восстанавливает URL/модель, но не ключ.',
    'service_flushes_buffer_during_pause_and_final_uses_same_message_id': 'Таймер допечатывает буфер при паузе и связывает финал с тем же bubble ID.',
    'read_inside_allowed': 'Внутренний self-test разрешает чтение в корне.',
    'parent_traversal_denied': 'Внутренний self-test отклоняет выход через родительский каталог.',
    'absolute_outside_denied': 'Внутренний self-test отклоняет внешний абсолютный путь.',
    'list_outside_denied': 'Внутренний self-test отклоняет внешний list_files.',
    'search_outside_denied': 'Внутренний self-test отклоняет внешний search_text.',
    'symlink_escape_denied': 'Проверяет выход через ссылку; может быть skipped при запрете symlink в ОС.',
}

TEST_HELPERS = {
    'write_with_failed_index': 'Пропускает каноническую запись и имитирует отказ только кэша индекса.',
    'fail_index_only': 'Имитирует отказ индекса во время полного агентского цикла.',
    'start_process': 'Запускает отдельный тестовый bridge с изолированным LOCALAPPDATA и stdout reader.',
    'stop_process': 'Завершает только принадлежащий тесту subprocess, закрывает каналы и ждёт reader.',
    'start_crash_scenario': 'Запускает тестовый сервер и задачу перед контролируемым аварийным завершением.',
    'reopen_after_kill': 'Убивает тестовый subprocess, запускает новый и открывает сохранённый чат.',
    'start_discovery_server': 'Запускает управляемую HTTP-фикстуру и отправляет discovery в реальный bridge subprocess.',
    'run': 'В тесте запускает сетевой вызов в отдельном потоке и передаёт результат/ошибку в очередь.',
    'late_create': 'Имитирует создание внешнего файла непосредственно перед атомарным созданием агентом.',
    'setUp': 'Создаёт изолированные данные и подмены перед каждым тестом этого класса.',
    'tearDown': 'Закрывает ресурсы и удаляет временные данные после теста.',
    'setUpClass': 'Создаёт общую HTTP-фикстуру и её поток для класса тестов.',
    'tearDownClass': 'Останавливает общий сервер и ждёт его поток.',
    'read_output': 'Читает JSON-строки stdout тестового subprocess в очередь.',
    'until': 'Ожидает подходящее сообщение, сохраняя остальные для дальнейших проверок.',
    'call': 'Посылает запрос отдельному Core-процессу и ждёт совпавший ID ответа.',
    'log_message': 'Отключает стандартный HTTP-log тестовой фикстуры.',
    'do_GET': 'Отдаёт детерминированный список моделей тестового HTTP-сервера.',
    'do_POST': 'Исполняет сценарий тестовой модели: чанки, tool call или намеренное ожидание отмены.',
    'chunk': 'Пишет один SSE-чанк тестового текстового ответа.',
    'wait_for_disconnect': 'На стороне fixture ожидает реального закрытия клиентского сокета.',
    'start': 'Готовит и запускает проверяемый engine/service в сценарии данного теста.',
    'event': 'Читает события до нужного имени и немедленно проваливает тест при failed.',
    'resolve': 'Передаёт проверяемое решение по предложению в TaskService.',
    'stop_and_assert': 'Отменяет engine и проверяет время завершения, закрытие сокета и paused checkpoint.',
}

DESIGN_CLASSES = {
    'Job': 'Фоновое Qt-задание произвольного callable в визуальном прототипе.',
    'ChatWorker': 'Поток генерации чата в прототипе, отдельный от рабочего AgentEngine.',
    'Runner': 'Собственный экспериментальный исполнитель задач эталона; его tools не являются разрешёнными tools LocalAgent.',
    'Hl': 'Подсветка синтаксиса редактора эталона.',
    'LineNums': 'Виджет поля номеров строк редактора эталона.',
    'CodeEdit': 'Редактор эталона с номерами строк, подсветкой и действиями ввода.',
    'ClickText': 'Текстовый виджет с обработкой двойного щелчка.',
    'Inp': 'Поле ввода с собственной обработкой клавиш.',
    'DiffDlg': 'Диалог сравнения изменений в эталоне.',
    'Palette': 'Палитра команд эталонного интерфейса.',
    'Main': 'Главное окно большого архивного прототипа; не импортируется production-путём проекта.',
}
DESIGN_METHODS = {
    'qss': 'Строит строку Qt stylesheet для параметров темы эталона.',
    'btn': 'Создаёт кнопку с текстом, callback и визуальными флагами.',
    'mono': 'Создаёт моноширинный шрифт заданного размера.',
    'stream_chat': 'Сетевой потоковый helper модели прототипа; отдельная реализация от ModelClient.',
    'run': 'Выполняет задание/чат/цикл соответствующего класса прототипа; см. тело конкретного класса.',
    'step': 'Обновляет шаг экспериментальной задачи Runner.',
    'ask': 'Обращается к модели из экспериментального Runner.',
    'tool': 'Диспетчер инструментов экспериментального Runner; не переносится в рабочую систему автоматически.',
    'highlightBlock': 'Подсвечивает один текстовый блок редактора.',
    'sizeHint': 'Возвращает рекомендуемый размер виджета номеров строк.',
    'paintEvent': 'Рисует виджет по событию Qt.',
    'lnw': 'Вычисляет ширину поля номеров строк.',
    'upd_w': 'Обновляет отступ редактора под номера строк.',
    'upd_ln': 'Обновляет область номеров строк при прокрутке/изменении.',
    'resizeEvent': 'Переразмещает поле номеров строк при изменении размера.',
    'paint_ln': 'Рисует видимые номера строк.',
    'hl_line': 'Подсвечивает текущую строку редактора.',
    'keyPressEvent': 'Обрабатывает ввод клавиатуры виджета эталона.',
    'ins_comp': 'Вставляет выбранное дополнение текста.',
    'mouseDoubleClickEvent': 'Обрабатывает двойной щелчок по тексту.',
    'go': 'Переходит к выбранному фрагменту diff.',
    'fill': 'Заполняет список палитры команд.',
    'data': 'Формирует путь служебных данных прототипа.',
    'jload': 'Загружает JSON прототипа с fallback.',
    'jsave': 'Сохраняет JSON прототипа.',
    'save_cfg': 'Сохраняет конфигурацию прототипа.',
    'log': 'Добавляет сообщение в диагностический вывод.',
    'show_logs': 'Показывает сохранённые диагностические сообщения.',
    'toast': 'Показывает краткое уведомление.',
    'job': 'Запускает действие через фоновый Job.',
    'busy': 'Меняет состояние занятости UI.',
    'build': 'Собирает виджеты и панели главного окна эталона.',
    'bind_keys': 'Подключает клавиатурные действия прототипа.',
    'show_side': 'Переключает боковую страницу.',
    'side_box': 'Создаёт контейнер боковой страницы.',
    'pg_files': 'Создаёт страницу проводника.',
    'filter_files': 'Фильтрует видимые файлы.',
    'tree_menu': 'Показывает контекстное меню дерева.',
    'fs_new': 'Создаёт файловый объект средствами эталона; не доступно текущему Electron tool API.',
    'fs_rename': 'Переименовывает файловый объект средствами эталона.',
    'fs_delete': 'Удаляет файловый объект средствами эталона; не часть рабочих tools LocalAgent.',
    'pg_search': 'Создаёт страницу поиска.',
    'do_search': 'Выполняет поиск в прототипе.',
    'pg_agents': 'Создаёт страницу задач/агентов прототипа.',
    'refresh_tasks': 'Обновляет список экспериментальных задач.',
    'pick_task': 'Выбирает задачу из списка.',
    'new_task': 'Создаёт экспериментальную задачу.',
    'pg_chats': 'Создаёт страницу чатов.',
    'chat_menu': 'Показывает меню действий над чатом.',
    'refresh_chats': 'Обновляет список чатов прототипа.',
    'new_chat': 'Создаёт новый чат прототипа.',
    'pick_chat': 'Открывает выбранный чат.',
    'rename_chat': 'Переименовывает чат прототипа.',
    'delete_chat': 'Удаляет чат прототипа.',
    'pg_models': 'Создаёт страницу модели и локального runtime.',
    'set_cfg': 'Меняет поле конфигурации прототипа.',
    'prov_changed': 'Обновляет настройки при смене провайдера.',
    'set_model': 'Выбирает ID модели.',
    'fetch_models': 'Запрашивает список моделей для прототипа.',
    'import_gguf': 'Импортирует GGUF через UI эталона.',
    'refresh_gguf': 'Обновляет отображаемый список GGUF.',
    'start_gguf': 'Запускает локальный runtime прототипа.',
    'stop_gguf': 'Останавливает локальный runtime прототипа.',
    'resources': 'Обновляет сведения о ресурсах.',
    'pg_skills': 'Создаёт страницу навыков.',
    'refresh_skills': 'Обновляет список навыков прототипа.',
    'skill_toggle': 'Переключает состояние навыка в прототипе.',
    'skill_desc': 'Показывает описание выбранного навыка.',
    'skills_text': 'Собирает текст включённых навыков прототипа.',
    'refresh_mcp': 'Обновляет список MCP-конфигураций эталона.',
    'mcp_toggle': 'Переключает флаг MCP-конфигурации.',
    'mcp_add': 'Добавляет MCP-конфигурацию в UI прототипа.',
    'mcp_del': 'Удаляет MCP-конфигурацию прототипа.',
    'mcp_connect': 'Обрабатывает действие подключения MCP в эталоне; не доказывает наличие транспорта в рабочем MCPRegistry.',
    'pg_memory': 'Создаёт страницу памяти проекта прототипа.',
    'mem_path': 'Определяет путь памяти прототипа.',
    'mem_load': 'Загружает память прототипа.',
    'mem_save': 'Сохраняет память из UI прототипа.',
    'mem_clear': 'Очищает память прототипа.',
    'pg_settings': 'Создаёт страницу настроек.',
    'apply_theme': 'Применяет stylesheet выбранной темы.',
    'toggle_theme': 'Переключает тему.',
    'apply_editor_prefs': 'Применяет настройки редактора.',
    'bottom': 'Переключает нижнюю панель прототипа.',
    'run_cmd': 'Запускает команду средствами эталона; рабочий агент такого tool не имеет.',
    'cmd_done': 'Обрабатывает завершение команды прототипа.',
    'stop_cmd': 'Останавливает команду прототипа.',
    'findbar': 'Создаёт панель поиска в редакторе.',
    'ed': 'Получает текущий редактор.',
    'toggle_find': 'Переключает панель поиска/замены.',
    'find': 'Ищет текст в редакторе.',
    'replace1': 'Заменяет одно совпадение в редакторе.',
    'replace_all': 'Заменяет все совпадения в редакторе.',
    'goto_line': 'Переходит к заданной строке.',
    'open_file': 'Открывает файл во вкладке редактора эталона.',
    'sync_stack': 'Согласует стек редакторов и вкладки.',
    'tab_mod': 'Обновляет индикатор изменения вкладки.',
    'pos_status': 'Обновляет строку состояния позиции курсора.',
    'save': 'Сохраняет открытый документ эталона.',
    'close_tab': 'Закрывает вкладку редактора.',
    'diagnose': 'Выполняет диагностическое действие прототипа.',
    'chat_panel': 'Собирает чат-панель эталона.',
    'render_chat': 'Отображает сообщения прототипа.',
    'sys_prompt': 'Формирует system prompt прототипа.',
    'send': 'Отправляет пользовательский запрос прототипа.',
    'on_chunk': 'Отображает полученный текстовый фрагмент.',
    'gen_end': 'Завершает состояние генерации в UI.',
    'on_done': 'Обрабатывает успешное завершение фоновой генерации.',
    'on_fail': 'Обрабатывает ошибку фоновой генерации.',
    'stop_gen': 'Запрашивает остановку генерации прототипа.',
    'copy_last': 'Копирует последний ответ.',
    'resend': 'Повторяет запрос/генерацию прототипа.',
    'task_panel': 'Создаёт подробную панель экспериментальной задачи.',
    'show_task': 'Отображает выбранную задачу.',
    'start_task': 'Запускает экспериментальный Runner.',
    'on_task_changed': 'Обновляет UI после изменения задачи.',
    'pause_resume': 'Переключает паузу/продолжение экспериментальной задачи.',
    'cancel_task': 'Запрашивает отмену экспериментальной задачи.',
    'rerun_task': 'Повторно запускает задачу прототипа.',
    'restore_cp': 'Восстанавливает экспериментальный checkpoint.',
    'review': 'Показывает просмотр предлагаемых изменений эталона.',
    'final_diff': 'Собирает итоговый diff прототипа.',
    'tick': 'Периодически обновляет состояние UI.',
    'open_project': 'Выбирает каталог проекта прототипа.',
    'new_project': 'Создаёт учебный проект средствами эталона.',
    'load_project': 'Переключает загруженный проект прототипа.',
    'restore': 'Восстанавливает сохранённое состояние окна прототипа.',
    'closeEvent': 'Сохраняет состояние и закрывает ресурсы эталона.',
}

TS_NOTES = {
    'showWarning': 'Публикует диагностическое предупреждение в логе и чате, не добавляя одинаковый текст повторно.',
    'fileName': 'Возвращает фиксированное имя main.cjs или preload.cjs для соответствующей сборки Vite.',
    'dialog.showOpenDialog': 'Только в smoke-тесте возвращает учебный каталог вместо настоящего системного диалога.',
    'extract': 'Читает один TS/JS-файл, создаёт AST и возвращает его именованные объявления без исполнения кода.',
    'add': 'Добавляет структурную запись символа с квалифицированным именем, сигнатурой и строкой.',
    'visit': 'Обходит TypeScript AST, распознавая типы, функции и именованные callbacks.',
    'publish': 'Передаёт Core-событие живому renderer через фиксированный core:event.',
    'startBackend': 'Лениво запускает Python, подключает stdout/stderr и обработчики завершения.',
    'stopped': 'Однократно сбрасывает процесс, завершает pending RPC ошибкой и сообщает backend_stopped.',
    'callBackend': 'Посылает JSON-lines запрос с ID/Promise, таймером и ограничением pending.',
    'createWindow': 'Создаёт изолированное Electron-окно и подключает его жизненный цикл.',
    'handle': 'Регистрирует IPC handler с проверкой sender и mainFrame.',
    'health': 'Фиксированный preload-вызов проверки Core.',
    'chooseProject': 'Выбор проекта: UI → native dialog → проверяемый set_project.',
    'listFiles': 'Preload-запрос списка файлов по относительному пути.',
    'readFile': 'Preload-запрос readonly текста файла.',
    'systemInfo': 'Preload-запрос home/platform у main, без tool модели.',
    'configureModel': 'Передаёт URL/модель/сеансовый ключ в фиксированный model:configure.',
    'listModels': 'Запрашивает ID доступных моделей.',
    'getModelSettings': 'Читает сохранённые URL/ID без ключа.',
    'listChats': 'Получает чаты выбранного проекта.',
    'newChat': 'Создаёт пустой чат проекта.',
    'loadChat': 'Загружает проверяемый ID чата.',
    'startTask': 'Посылает prompt и resume-флаг, получает принятие задачи.',
    'cancelTask': 'Запрашивает отмену через task:cancel.',
    'resolveApproval': 'Передаёт run/proposal ID и явное решение.',
    'onEvent': 'Подписывает callback на core:event и возвращает отписку.',
    'listener': 'Адаптирует Electron event в пользовательские данные callback.',
    'App': 'Корневой React-компонент приложения с состояниями, эффектами и обработчиками.',
    'FileItem': 'Тип элемента readonly-проводника: имя, относительный путь, вид файла/каталога.',
    'Message': 'Тип UI-сообщения, включая ID и признак streaming; не полный Chat Completions transcript.',
    'ChatSummary': 'Тип метаданных чата для бокового списка.',
    'CoreEvent': 'Общее событие Core; дополнительные поля пока описаны через any.',
    'Window': 'Расширение глобального Window контрактом фиксированного lca API.',
    'report': 'Добавляет диагностическую строку, сохраняя ограниченный хвост UI-лога.',
    'refreshChats': 'Запрашивает и обновляет список чатов.',
    'refreshFiles': 'Обновляет элементы и текущий относительный каталог проводника.',
    'openFile': 'Открывает каталог или загружает текст файла в preview.',
    'selectChat': 'Создаёт/загружает чат, заменяет UI-историю и checkpoint при отсутствии активной задачи.',
    'configure': 'Передаёт текущие поля модели сервису и выбрасывает ошибку при отказе.',
    'saveSettings': 'Сохраняет настройки и отображает результат в output.',
    'discoverModels': 'Настраивает сервер, загружает модели, выбирает ID и сохраняет выбор.',
    'sendPrompt': 'Проверяет готовность, блокирует повторный старт, создаёт чат и отправляет задачу/продолжение.',
    'decide': 'Защищает от повторного нажатия и отправляет решение по текущему approval.',
    'cancel': 'Показывает состояние остановки и вызывает cancelTask.',
    'fail': 'В smoke-тесте записывает ошибку в result.json и завершает Electron.',
    'encode': 'Сериализует детерминированный SSE-чанк модельной фикстуры.',
    'releaseModelText': 'Завершает задержанный ответ фикстуры после проверки видимого частичного текста.',
    'poll': 'В тесте ожидает DOM-условие с ограничением времени.',
    'BrowserWindow.prototype.show': 'Только в smoke-тесте подавляет показ настоящего окна пользователю.',
}

register('agent/model_discovery.py', '''
_request_models | Читает HTTPX stream с ограничением размера и проверяет JSON data/models ID.
_wait_cancelled | Наблюдает threading.Event через короткие asyncio sleep без блокировки event loop.
_discover | Соревнуется запросом, отменой и общим timeout; всегда отменяет и закрывает незавершённые задачи.
discover_models | Синхронная точка входа фонового worker, запускающая отдельный asyncio loop.
''')

register('tools/build_windows_core.py', '''
main | Проверяет Windows x64/Python 3.12 и вызывает PyInstaller с данными навыков, SDK и необходимым PEM runtime.
''')
TS_NOTES.update({
 'getIDEWorkflow':'Читает публичные настройки ролей IDE через узкий IPC без API-ключей.',
 'configureIDEWorkflow':'Сохраняет проверенный профиль ролей через backend idle guard.',
 'listIDEModels':'Запрашивает отменяемый каталог сервера выбранной роли без загрузки весов.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.cancelRecording':'Инвалидирует результат STT, освобождает микрофон и отменяет HTTP; поздний ответ не меняет текст.',
 'tests/electron/microphone.cjs:main':'Без устройства проверяет конец речи, границы PCM после обрезки, тишину, ограничения аудио и остановку tracks.',
 'tests/electron/microphone.cjs:getUserMedia':'Создаёт фиктивный MediaStream, сохраняя запрошенные ограничения микрофона.',
 'tests/electron/microphone.cjs:getUserMedia.getTracks':'Возвращает фиктивную дорожку для проверки освобождения устройства.',
 'tests/electron/microphone.cjs:getUserMedia.getTracks.stop':'Считает остановки дорожки при завершении и отмене записи.',
 'tests/electron/microphone.cjs:btoa':'Кодирует тестовый PCM WAV в base64 через Node Buffer.',
 'tests/electron/microphone.cjs:main.block':'Передаёт детерминированный блок речи либо тишины обработчику AudioContext.',
 'tests/electron/microphone.cjs:main.block.getChannelData':'Возвращает 1024 сэмпла с заданной тестовой амплитудой.',
    'diagnostic': 'Добавляет только lifecycle-диагностику в ограниченный main.log; ошибка I/O не блокирует приложение.',
    'tests/electron/packaged-smoke.mjs:freePort': 'Резервирует свободный loopback-порт для тестового Chromium CDP.',
    'tests/electron/packaged-smoke.mjs:connectPage': 'Ожидает file renderer настоящего exe и открывает WebSocket CDP с ограниченным временем.',
    'tests/electron/packaged-smoke.mjs:evaluate': 'Последовательно исполняет одно тестовое выражение через CDP с тайм-аутом.',
    'tests/electron/packaged-smoke.mjs:evaluate.receive': 'Сопоставляет CDP response с запросом и возвращает значение либо ошибку JavaScript.',
    'tests/electron/packaged-smoke.mjs:run': 'Запускает packaged exe с изолированными данными/урезанным PATH и проверяет Core, настройки и нормальное закрытие.',
    'tests/electron/packaged-smoke.mjs:main': 'Поднимает HTTP-фикстуру, дважды проверяет пакет и отсутствие ключа в настройках/диагностике.',
})

register('agent/task_activity.py', '''
begin_tool | Создаёт запись метаданных и активирует research/implementation, добавляя отсутствующий этап записи и ограничивая журнал 100 элементами.
update_tool | Обновляет статус/краткую сводку по внутреннему ID и время завершения терминального состояния.
finish_tool | Преобразует фактический result в безопасную сводку/статус без копирования содержимого файла или результатов поиска.
recover_tools | Восстанавливает in-flight запись из соответствующего блока tool-call/result; неопределённый Apply отмечает unknown, остальные прерванные — interrupted.
''')
TS_NOTES.update({
    'apps/desktop/src/TaskProgress.tsx:TaskStage': 'UI-представление этапа: идентификатор, название, цель и статус исполнения.',
    'apps/desktop/src/TaskProgress.tsx:ToolActivity': 'UI-проекция метаданных tool: устойчивый ID, путь, этап, статус и сводка без raw content.',
    'apps/desktop/src/TaskProgress.tsx:TaskSnapshot': 'Тип полей checkpoint, используемых панелью плана и результатов.',
    'apps/desktop/src/TaskProgress.tsx:TaskProgress': 'Показывает посещённые/пропущенные этапы, последние операции, изменённые файлы, остановку и кнопку resume.',
})
FILE_NOTES['apps/desktop/src/VoicePanel.tsx'] = 'Подготовительный экран голосового ассистента: SVG-эскиз горничной, честные состояния отсутствующих STT/TTS и контракты будущей сессии; аудио пока не записывает.'
TS_NOTES.update({
    'switchMode': 'Переключает Chat/IDE/voice только в idle, сбрасывает выбранный UI-чат и загружает историю соответствующей области.',
    'WorkspaceMode': 'Три пространства интерфейса: обычный разговор, работа с проектом и будущий голосовой ассистент.',
    'VoiceSessionState': 'Будущие состояния аудиосессии: отключена, слушает, думает, говорит, ошибка; сейчас backend не реализован.',
    'VoicePanel': 'Рисует эскиз горничной и карточки ещё не подключённых голосовых возможностей, предлагает перейти в Chat.',
})
TEST_PURPOSES.update({
 'resume_cannot_silently_switch_workflow_to_single_model':'После паузы смена команды IDE на одну модель требует новой задачи, старый workflow не обходится через Resume.',
 'standalone_review_requires_file_evidence':'Одиночный проверяющий не может объявить pass без чтения хотя бы одного файла проекта.',
    'empty_after_tool_recovers_without_repeating_write': 'SSE с reasoning без content после Apply приводит к одному text-only повтору, без повторной записи и без служебного user в архиве.',
    'permanently_empty_model_pauses_after_two_retries': 'Три пустых ответа после успешной записи дают paused/failed, сохраняют единственный tool result и файл.',
    'chat_without_project_has_no_tools_and_separate_history': 'Глобальный Chat работает без папки, не передаёт tools и не смешивает историю с проектом.',
    'chat_refuses_unsolicited_tool': 'Неожиданный tool от сервера в Chat отклоняется до approval/выполнения, задача приостанавливается.',
})

TEST_PURPOSES.update({'chat_scope_does_not_require_selected_folder': 'Bridge выбирает пустую область Chat без папки, а IDE требует проект.', 'unknown_mode_is_rejected': 'Bridge отклоняет voice и прочие неисполняемые режимы до сервиса.'})

TEST_PURPOSES['task_end_allows_immediate_configuration_before_thread_returns'] = 'Синхронный callback task_end меняет настройки, пока прежний поток ещё жив: завершённое исполнение уже idle.'
TEST_HELPERS['observe'] = 'Перехватывает task_end, проверяет ещё живой worker и синхронно меняет настройки до возврата потока.'
FILE_NOTES.update({
 'apps/desktop/src/AppearanceSettings.tsx':'Проверенные локальные настройки темы, акцента, плотности и панелей, синхронизация React и форма оформления.',
 'apps/desktop/src/GenerationFields.tsx':'Единые типы, значения, диапазоны, подсказки и форма генерации для Chat/IDE и отдельной модели Лолы.',
 'apps/desktop/src/styles/base.css':'Базовые панели, редактор, сообщения, подтверждения и карточки задачи; начало сохранённого CSS-каскада.',
 'apps/desktop/src/styles/workspaces.css':'Расположение Chat/IDE, общие окна и компоненты; сохранённый каскад без устаревших SVG-селекторов.',
 'apps/desktop/src/styles/companion.css':'Сетка ассистента, атлас состояний и модальное окно настроек голоса.',
 'apps/desktop/src/styles/modern.css':'Актуальные токены тёмной/светлой темы, акценты, плотность, скрытие панелей и розовое оформление Лолы.',
 'docs/32-miya-settings-and-voice-input.md':'Диалог настроек Лолы, RMS-порог, завершение по паузе, обрезка PCM, автоотправка, отмена и измерения STT.',
 'tests/electron/microphone.cjs':'Проверка захвата и обрезки WAV с фиктивным AudioContext без записи реального микрофона.',
    'agent/model_probe.py': 'Ограниченная отменяемая проверка draft-модели через Chat Completions без файлов, истории и сохранения настроек.',
    'tests/migration/test_model_probe.py': 'Реальный HTTP-стенд проверки ответа, пустого/некорректного/слишком большого результата, deadline и отмены.',
    'apps/desktop/src/ModelSettings.tsx': 'Модальное окно draft-настроек: endpoint, ключ, список моделей, тест ответа, генерация, лимиты, сохранение и focus trap.',
    'agent/model_preferences.py': 'Валидация endpoint и whitelist числовых настроек, миграция старого JSON и атомарное сохранение без API-ключа.',
})
register('agent/model_preferences.py', '''
validate_settings | Проверяет конечность, тип, целочисленность и диапазон каждого разрешённого параметра; неизвестные поля не сохраняет.
''')
register('agent/model_probe.py', '''
_request_probe | Выполняет bounded HTTP POST с коротким prompt, параметрами черновика, заданным бюджетом токенов и проверкой текстового ответа.
_probe | Ограничивает полное время запроса и следит за Event отмены, закрывая обе asyncio-задачи в finally.
probe_model | Проверяет ID, запускает отдельный asyncio loop и возвращает ответ/время без изменения истории или preferences.
''')
register('core/python/task_service.py', '''
TaskService.diagnostic_config | Создаёт отдельную валидированную копию черновика либо текущих настроек, включая ключ только в памяти.
TaskService.start_model_probe | Запускает один фоновый worker проверки; запрещает параллельную проверку/активную задачу и фиксирует конфигурацию.
TaskService.start_model_probe.run_probe | Вызывает probe_model и возвращает исходному RPC callback результат или ограниченную ошибку.
TaskService.cancel_model_setup | Отменяет discovery и probe независимо от основной задачи агента.
''')
TS_NOTES.update({
 'Appearance':'Разрешённые значения темы, акцента, плотности и трёх видимых панелей.',
 'readAppearance':'Читает localStorage с whitelist и fallback; повреждённые или неподдерживаемые поля не ломают запуск.',
 'saveAppearance':'Сохраняет внешний вид локально и сообщает компонентам об изменении.',
 'useAppearance':'Подписывает React на локальное событие настроек и storage, удаляет обработчики при unmount.',
 'apps/desktop/src/AppearanceSettings.tsx:useAppearance.refresh':'Перечитывает и проверяет оформление после изменения в этом или другом окне.',
 'AppearanceSettings':'Показывает темы, акценты, плотность и панели с немедленным применением без изменения модели.',
 'apps/desktop/src/AppearanceSettings.tsx:AppearanceSettings.update':'Применяет частичное изменение оформления и показывает результат сохранения.',
 'GenerationFields':'Отрисовывает общий контракт генерации с disabled, числовыми границами и пояснениями для обоих профилей.',
    'GenerationSettings': 'Числовой контракт семи применяемых настроек: sampling, token/context budgets, HTTP timeout и ограничения цикла.',
    'ModelConfig': 'Конфигурация окна/IPC: URL, ID, временный API-ключ и числовые настройки.',
    'ModelSettings': 'Модальное окно с отдельным draft; применяет настройки только после успешного backend save.',
    'change': 'Меняет поле черновика и помечает его несохранённым; новый URL сбрасывает устаревший список моделей.',
    'validate': 'Проверяет URL и диапазоны полей до отправки, backend повторяет обязательную валидацию.',
    'perform': 'Последовательно выполняет discovery, bounded probe или save с явным статусом и обработкой ошибок в окне.',
    'resetGeneration': 'Возвращает числовые поля к defaults только в черновике, не меняет endpoint/ID/ключ.',
    'handleKeys': 'Закрывает окно по Escape вне операции и удерживает Tab-навигацию в доступных контролах диалога.',
    'modelConfig': 'Явно перечисляет поля model IPC, остальные поля renderer не передаёт в Core.',
    'testModel': 'Посылает фиксированный RPC диагностики без произвольного prompt и файлов.',
    'cancelModelSetup': 'Отменяет текущую диагностику модели через отдельный фиксированный канал.',
})
TEST_PURPOSES.update({
    'old_preferences_gain_generation_defaults': 'Старый JSON с URL/ID получает числовые defaults без смены endpoint и модели.',
    'generation_roundtrip_and_invalid_values_do_not_replace_file': 'Числовые настройки переживают сохранение; NaN, bool, дробный integer и выход за диапазон не перезаписывают файл.',
    'draft_probe_uses_generation_without_saving_configuration': 'Probe получает draft sampling/ID, но не меняет сохранённые настройки и не отправляет tools/историю.',
    'saved_generation_is_used_by_engine': 'Настройки из preferences реально попадают в HTTP streaming payload и переживают новый TaskService.',
    'probe_requires_real_text_and_bounds_bad_responses': 'Проверка принимает текст и отклоняет пустой результат, неверную структуру, большой ответ и HTTP 401.',
    'probe_deadline_and_cancellation_are_bounded': 'Зависший HTTP прерывается общим deadline и Event отмены.',
    'draft_probe_keeps_bridge_responsive_and_can_be_cancelled': 'Во время зависшего probe реальный bridge отвечает health/cancel и сохраняет прежнюю конфигурацию.',
})

TS_NOTES.pop('discoverModels', None)
TS_NOTES.pop('saveSettings', None)
FILE_NOTES.update({
    'core/python/editor_service.py': 'Ручной editor-протокол: strict UTF-8 чтение с revision, preview, одноразовый Apply через существующую атомарную snapshot-запись.',
    'apps/desktop/src/EditorPanel.tsx': 'Рабочие вкладки/черновики редактора, виртуальный gutter, поиск/строка, hotkeys, reload и подтверждённое сохранение.',
    'tests/test_editor_service.py': 'Контракты editor revisions, CRLF, отсутствия записи до Apply, stale/replay, бинарных/больших/внешних файлов и project scope.',
})
register('core/python/editor_service.py', '''
EditorService | Хранит одно ручное предложение в памяти и использует общий sandbox/atomic write без автоматического подтверждения.
EditorService.clear | Забывает pending proposal при новой подготовке, решении или смене проекта.
EditorService.read | Читает ограниченные UTF-8 байты, отвергает NUL, возвращает LF-представление, newline-стиль и хеш исходных байтов.
EditorService.preview | Сверяет editor revision с диском и снимком diff, готовит предложение до 1 МБ и сохраняет одноразовый proposal без записи.
EditorService.resolve | Проверяет ID/root/решение, потребляет proposal и выполняет Apply с повторной проверкой snapshot; Reject/Cancel не пишут.
''')
TS_NOTES.update({
    'EditorDocument': 'Документ вкладки: текущий текст, исходный текст, byte revision и стиль строк.',
    'EditorHandle': 'Узкая ref-поверхность open/refresh/reset/hasDirty, сохраняющая drafts при переключении режимов.',
    'EditorProps': 'Корень/видимость/busy и callbacks редактора; file access остаётся в Core.',
    'EditorPanel': 'Компонент редактора с сохраняемыми между режимами вкладками и snapshot-approval.',
    'selectDocument': 'Добавляет или заменяет документ вкладки и выбирает его активным.',
    'read': 'Запрашивает strict editor_read и отбрасывает ответ, относящийся к уже сменившемуся корню.',
    'open': 'Открывает существующую вкладку без потери draft либо читает файл; может перейти к нужной строке.',
    'refresh': 'Обновляет только чистую вкладку после записи агента, dirty draft сохраняет и предупреждает о конфликте.',
    'closeTab': 'Закрывает вкладку; грязный текст требует явного подтверждения отказа от сохранения.',
    'reload': 'Перечитывает активный файл после подтверждения потери draft; при ошибке текст остаётся.',
    'save': 'Получает preview по исходной byte revision, не пишет файл и показывает отдельный диалог.',
    'decide': 'Отправляет решение editor proposal либо агентского approval в зависимости от компонента; сохраняет локальный draft при отказе.',
    'updatePosition': 'Вычисляет line/column по положению selectionStart в UTF-16 textarea.',
    'moveToLine': 'Ограничивает номер строки, вычисляет offset и перемещает курсор/прокрутку.',
    'findNext': 'Ищет следующую текстовую строку без учёта регистра с циклическим возвратом в начало файла.',
    'shortcuts': 'Обрабатывает Ctrl+S/F/G/Shift+R только в видимом editor и вне модальных диалогов.',
    'confirmEditorDiscard': 'Показывает нативное предупреждение с безопасным default Cancel; возвращает только явный отказ от сохранения.',
    'editorRead': 'Вызывает отдельное strict editor_read через фиксированный IPC.',
    'editorPreview': 'Передаёт draft и исходную revision для preview без записи.',
    'editorResolve': 'Передаёт только proposal ID и явное решение, не произвольную команду записи.',
    'setEditorDirty': 'Сообщает main о несохранённых вкладках для защиты закрытия окна.',
})
TEST_PURPOSES.update({
    'read_preview_and_one_shot_apply_preserve_crlf': 'Read сохраняет byte hash/CRLF; preview не пишет, Apply пишет один раз и обновляет revision.',
    'external_change_before_preview_and_after_approval_is_never_overwritten': 'Оба момента внешнего изменения возвращают FILE_CHANGED без перезаписи.',
    'reject_cancel_and_replaced_proposals_do_not_write': 'Отказ/отмена и старый ID после новой подготовки не меняют файл.',
    'unchanged_text_has_no_pending_write': 'Неизменённый текст не создаёт write approval.',
    'outside_binary_invalid_utf8_and_large_files_are_rejected': 'Editor отвергает traversal, неверную кодировку, NUL и превышение 1 МБ.',
    'proposal_cannot_be_applied_to_another_project': 'Proposal одного корня не применяется к другому проекту.',
    'editor_preview_blocks_task_and_project_switch_invalidates_approval': 'Bridge не запускает агента во время editor approval, set_project сбрасывает старый ID.',
    'editor_writes_are_rejected_while_agent_is_running': 'Ручной preview не начинается, пока task service занят.',
})
TEST_HELPERS['proposal'] = 'Читает текущую revision и создаёт тестовый editor preview без записи.'
TS_NOTES['reset'] = 'Сбрасывает editor-вкладки, pending diff и уведомления после подтверждённой смены проекта.'
TS_NOTES['apps/desktop/src/EditorPanel.tsx:EditorPanel.decide'] = 'Потребляет editor proposal через Apply/Reject/Cancel; при отказе или конфликте сохраняет draft, после успеха обновляет revision.'
TS_NOTES['decide'] = 'Передаёт явное решение по текущему approval агента, защищая от повторных кликов.'
TS_NOTES['hasDirty'] = 'Читает актуальные editor tabs через ref для проверки unsaved перед нативной сменой проекта.'
TS_NOTES['dialog.showMessageBox'] = 'В Electron smoke подменяет нативное подтверждение несохранённых изменений управляемым ответом Cancel/Discard.'

FILE_NOTES.update({
 'core/python/project_search.py':'Ограниченный read-only поиск текста и путей с отменяемым отдельным worker.',
 'apps/desktop/src/ProjectSearch.tsx':'Боковой поиск и Ctrl+P: один IPC-запрос за раз, отмена и защита от устаревших результатов.',
 'tests/test_project_search.py':'Поиск: Unicode, фильтры, лимиты, пропуски бинарных файлов, отмена и single-flight.',
})
SYMBOL_NOTES.update({
 'core/python/project_search.py:search_project':'Обходит выбранный корень без symlink-переходов; возвращает literal text matches или пути в пределах времени/байтов/числа файлов.',
 'core/python/project_search.py:search_project.stop':'Проверяет cooperative cancellation и deadline, устанавливает честный статус неполного результата.',
 'core/python/project_search.py:ProjectSearchService':'Владеет одним отменяемым daemon worker; stdin JSON bridge остаётся доступен для других команд.',
 'core/python/project_search.py:ProjectSearchService.start':'Фиксирует валидный корень/параметры и запускает worker; отклоняет параллельный поиск.',
 'core/python/project_search.py:ProjectSearchService.start.run_search':'Выполняет поиск, преобразует исключение в ответ и освобождает busy до отправки результата.',
 'core/python/project_search.py:ProjectSearchService.cancel':'Устанавливает event отмены только поискового worker.',
 'core/python/project_search.py:ProjectSearchService.shutdown':'Запрашивает отмену и ограниченно ожидает собственный поток.',
})
TS_NOTES.update({
 'apps/desktop/src/ProjectSearch.tsx:Match':'Найденный относительный путь, номер строки и ограниченный текстовый preview.',
 'apps/desktop/src/ProjectSearch.tsx:Props':'Корень, видимость, режим quick open и переход в editor.',
 'ProjectSearch':'Единая форма text/files с bounded результатами, явной отменой и клавиатурным выбором.',
 'apps/desktop/src/ProjectSearch.tsx:ProjectSearch.search':'Последовательно отменяет предыдущий запрос, отправляет новый и применяет только актуальный ticket/root.',
 'apps/desktop/src/ProjectSearch.tsx:ProjectSearch.cancel':'Инвалидирует результаты и запрашивает отмену собственного поиска.',
 'openSearchFile':'Переходит в IDE и открывает результат на нужной строке, сохраняя sidebar поиска.',
 'searchProject':'Вызывает фиксированный read-only IPC поиска с текстом/маской/регистром.',
 'cancelProjectSearch':'Отменяет поиск независимо от остановки агента.',
})
TEST_PURPOSES.update({
 'literal_text_line_case_and_path_filter':'Unicode пути, literal matching, номера строк, регистр и маска файлов.',
 'files_ignored_binary_encoding_size_and_result_limits':'Игнорируемые каталоги, NUL/encoding/размер, быстрый поиск путей и truncated results.',
 'cancel_time_and_budget_are_reported':'Отмена, deadline, file/byte budget и строгая валидация параметров.',
 'symlink_cannot_expand_search_scope':'Внешний symlink не читается; при отсутствии Windows privilege тест явно skipped.',
 'worker_cancellation_single_flight_and_invalid_root_recovery':'Busy worker не допускает второй поиск, отменяется, неверный root не оставляет busy навсегда.',
 'project_search_requires_root_and_does_not_block_bridge':'Настоящий bridge требует root, возвращает строку поиска и остаётся доступен health/cancel.',
})
TEST_HELPERS['slow']='Управляемая barrier-фикстура поискового worker для детерминированной проверки отмены.'

FILE_NOTES.update({
 'agent/process_job.py':'Windows Job Object: kill-on-close только для собственного Popen и его потомков.',
 'core/python/runtime_service.py':'Неблокирующий сервис запуска/остановки GGUF и состояний собственного llama-server.',
 'apps/desktop/src/LocalRuntimePanel.tsx':'Реальный GGUF picker, context/GPU, lifecycle status и явный перенос endpoint в настройки.',
 'tests/test_runtime_service.py':'Проверки lifecycle, bounded output, отмены, ошибок и Windows crash cleanup.',
})
SYMBOL_NOTES.update({
 'agent/model_manager.py:LocalRuntime._drain_output':'Читает бинарный PIPE порциями 1024 байта без ожидания newline; хранит последние 100 порций.',
 'agent/process_job.py:ProcessJob':'Владеет ненаследуемым Windows Job handle; закрытие завершает только присоединённое дерево.',
 'agent/process_job.py:ProcessJob.__init__.BasicLimits':'ctypes структура JOBOBJECT_BASIC_LIMIT_INFORMATION с корректным pointer-size alignment.',
 'agent/process_job.py:ProcessJob.__init__.IoCounters':'Шесть 64-битных IO_COUNTERS полей Windows API.',
 'agent/process_job.py:ProcessJob.__init__.ExtendedLimits':'ctypes JOBOBJECT_EXTENDED_LIMIT_INFORMATION для JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE.',
 'agent/process_job.py:ProcessJob.close':'Идемпотентно закрывает последний job handle, завершая присоединённые процессы.',
 'core/python/runtime_service.py:RuntimeService':'Отдельные lifecycle lock/thread/Event и состояния stopped/starting/running/stopping/error.',
 'core/python/runtime_service.py:RuntimeService.start':'Проверяет выбранные файлы, GGUF magic и integer параметры; создаёт один background worker.',
 'core/python/runtime_service.py:RuntimeService.start.launch':'Ждёт readiness вне stdin bridge, публикует running/error и очищает отменённый запуск.',
 'core/python/runtime_service.py:RuntimeService.status':'Снимок состояния/метаданных/последнего вывода; обнаруживает завершение ранее готового сервера.',
 'core/python/runtime_service.py:RuntimeService.stop':'Отменяет старт либо запускает собственный terminate worker; повторный Stop не создаёт новый поток.',
 'core/python/runtime_service.py:RuntimeService.stop.terminate':'Завершает только owned runtime и переводит сервис в stopped.',
 'core/python/runtime_service.py:RuntimeService.shutdown':'Отменяет lifecycle, ограниченно ждёт worker и закрывает оставшийся owned runtime.',
})
TS_NOTES.update({
 'LocalRuntimePanel':'Панель собственного GGUF с file picker, реальным lifecycle и явным переносом endpoint без сохранения.',
 'apps/desktop/src/LocalRuntimePanel.tsx:LocalRuntimePanel.refresh':'Раз в секунду читает runtime status и игнорирует ответ после unmount.',
 'pick':'Получает только выбранный системным диалогом путь GGUF/runtime; отмена не меняет выбор.',
 'control':'Отправляет start/stop собственного сервера и показывает ошибку без блокировки настроек на время загрузки.',
 'pickRuntimeFile':'Вызывает системный выбор GGUF или установленного llama-server.',
 'startRuntime':'Передаёт только context/GPU; пути берутся main из предыдущего file picker.',
 'runtimeStatus':'Читает lifecycle собственного сервера без управления внешним LM Studio.',
 'stopRuntime':'Останавливает только собственный локальный runtime через фиксированный IPC.',
})
TEST_PURPOSES.update({
 'validation_does_not_launch_arbitrary_files':'Имя executable, GGUF header и integer/range проверяются до старта.',
 'start_cancel_is_nonblocking_and_cannot_restart_until_worker_finishes':'Start возвращает сразу, Stop отменяет worker, параллельный restart запрещён.',
 'start_failure_is_visible_without_busy_deadlock':'Ошибка старта становится видимым error и не оставляет вечный busy.',
 'output_drain_is_bounded_even_without_newlines':'500 КБ вывода без newline не превышают 100 порций в памяти.',
 'readiness_timeout_cleans_only_owned_process':'Timeout завершает реальный собственный процесс и закрывает его job.',
 'windows_job_close_terminates_owned_child':'Закрытие Windows job завершает присоединённого потомка.',
 'parent_crash_closes_job_and_terminates_child':'Авария владельца job автоматически завершает его дочернее дерево.',
 'runtime_commands_validate_without_blocking_other_commands':'Bridge status/start validation/stop не нарушают health без модели.',
})
TEST_HELPERS['launching']='Управляемая barrier-фикстура долгой загрузки с cooperative cancel.'
TEST_HELPERS['Output']='BytesIO-фикстура длинного stdout без перевода строки.'

FILE_NOTES.update({
 'core/python/memory_service.py':'Строгий read/edit API памяти проекта с byte revision и защитой повреждённых файлов.',
 'apps/desktop/src/MemoryPanel.tsx':'Редактор семи полей памяти выбранного проекта с сохранением draft при конфликте.',
 'apps/desktop/src/ChatText.tsx':'Безопасные текстовые/code блоки без HTML, memoized parser и явное копирование.',
 'tests/test_memory_service.py':'Память UI: CAS, invalid payload, corrupt file, scope и полный Unicode budget.',
})
SYMBOL_NOTES.update({
 'core/python/memory_service.py:editable_memory':'Требует ровно семь редактируемых полей, проверяет типы, длины, число пунктов и отсутствие NUL до записи.',
 'core/python/memory_service.py:read_memory':'Читает до 200 КБ strict JSON под memory lock; не исправляет и не затирает повреждённый store, возвращает SHA256 raw revision.',
 'core/python/memory_service.py:write_memory':'Проверяет исходную byte revision под общим с auto-memory RLock, атомарно сохраняет только валидные поля и перечитывает результат.',
 'core/python/task_service.py:TaskService.rename':'Проверяет idle/title/chat scope, сохраняет только новое название и синхронизирует title выбранного чата.',
})
TS_NOTES.update({
 'MemoryPanel':'Модальный редактор ограниченной памяти IDE; Chat не использует эти заметки.',
 'apps/desktop/src/MemoryPanel.tsx:MemoryPanel.show':'Проверяет ответ/корень, преобразует списки в строки и фиксирует original/revision после успешного чтения или записи.',
 'apps/desktop/src/MemoryPanel.tsx:MemoryPanel.save':'Преобразует строки списков, отправляет snapshot revision, при конфликте сохраняет draft в окне.',
 'apps/desktop/src/MemoryPanel.tsx:MemoryPanel.close':'Закрывает чистую форму; для dirty показывает явный выбор сохранить редактирование или потерять draft.',
 'TextPart':'Один plain/code сегмент безопасного текстового renderer с подписью языка.',
 'splitCodeBlocks':'Линейно разбирает отдельные тройные backtick fences, включая незакрытый streaming code block; HTML не интерпретируется.',
 'apps/desktop/src/ChatText.tsx:splitCodeBlocks.flush':'Добавляет накопленные строки текущего сегмента и очищает буфер.',
 'ChatText':'Memoizes разбор текста, выводит code как React text nodes и показывает кнопку копирования.',
 'apps/desktop/src/ChatText.tsx:ChatText.copy':'Пишет только выбранный code segment через Clipboard API и показывает успех/ошибку.',
 'apps/desktop/src/App.tsx:App.renameChat':'Отправляет переименование выбранного chat ID в текущем scope и обновляет список после успешного сохранения.',
 'renameChat':'Фиксированный IPC переименования ID/title/mode без изменения сообщений.',
 'getProjectMemory':'Читает семь полей и byte revision памяти текущего проекта.',
 'saveProjectMemory':'Передаёт editable memory и исходную revision для конфликтобезопасной записи.',
})
TEST_PURPOSES.update({
 'round_trip_and_external_update_preserve_stale_draft':'Manual memory round trip и отказ после auto-memory update без перезаписи новых заметок.',
 'invalid_fields_do_not_modify_store':'Неверные типы/длины/count/extra keys не создают файл памяти.',
 'corrupt_memory_is_preserved_and_other_project_is_isolated':'Повреждённый JSON не затирается; другой root получает отдельную пустую память.',
 'full_unicode_budget_is_readable':'Полные разрешённые поля с четырёхбайтным Unicode помещаются в bounded reader и проходят round trip.',
 'rename_preserves_messages_and_scope_and_active_title':'Название сохраняется без изменения сообщений, обновляет active chat и не пересекает Chat/IDE scope.',
 'rename_rejected_during_active_task':'Переименование запрещено во время реальной задачи, ожидающей approval.',
 'project_memory_and_chat_rename_are_scoped':'Реальный JSON bridge проверяет root памяти, stale revision и scope переименования.',
})

FILE_NOTES.update({
 'core/python/speech_service.py':'Windows System.Speech через фиксированный PowerShell script и stdin JSON: каталог, TTS, Stop и owned job.',
 'tests/test_speech_service.py':'TTS без динамиков/микрофона: WAV, JSON data boundary, cancellation и timeout cleanup.',
 'apps/desktop/src/VoicePanel.tsx':'Рабочий разговор с Лолой без file tools, системная озвучка, голос/темп/громкость/Stop и честный отключённый STT.',
})
SYMBOL_NOTES.update({
 'core/python/speech_service.py:speech_command':'Выбирает только системный Windows PowerShell и кодирует константный script в UTF-16LE; пользовательский текст не попадает в команду.',
 'core/python/speech_service.py:SpeechService':'Владеет одним отменяемым Windows speech worker, cached каталогом и состоянием; микрофон не открывает.',
 'core/python/speech_service.py:SpeechService.status':'Возвращает plain JSON состояния/ошибки/голосов/распознавателей без текста синтеза.',
 'core/python/speech_service.py:SpeechService.refresh':'Асинхронно перечисляет установленные голоса/распознаватели без звука и записи аудио.',
 'core/python/speech_service.py:SpeechService.speak':'Проверяет выбранный installed voice, plain text до 6000 символов, rate/volume и запускает TTS worker.',
 'core/python/speech_service.py:SpeechService._start':'Фиксирует operation snapshot, проверяет single-flight, создаёт worker с отдельным timeout и cancel Event.',
 'core/python/speech_service.py:SpeechService._start.run':'Создаёт owned PowerShell/job, передаёт JSON через stdin, опрашивает communicate с коротким timeout, закрывает дерево и публикует итог.',
 'core/python/speech_service.py:SpeechService.stop':'Только устанавливает cancel Event и stopping; stdin bridge не ждёт синтеза.',
 'core/python/speech_service.py:SpeechService.shutdown':'Отменяет речь и ограниченно ждёт owned worker при выходе Core.',
})
TS_NOTES.update({
 'VoiceSessionState':'Состояния голосовой оболочки: disconnected/idle/listening/thinking/speaking/error; listening зарезервирован до подключения STT.',
 'VoicePanel':'Разговор с персонажем и реальный Windows TTS: каталог, voice/rate/volume, manual/opt-in auto speech и отдельный Stop.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.refresh':'Читает plain status раз в 500 мс; отбрасывает ответы после unmount. Инициализация discovery учитывает StrictMode cleanup.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.speak':'Отправляет до 6000 символов с выбранным голосом/темпом/громкостью и показывает lifecycle/ошибку.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.stop':'Останавливает только озвучку; не отменяет модельную генерацию.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.send':'Передаёт введённую фразу в общий task flow voice без файловых инструментов.',
 'voiceStatus':'Читает состояние системной озвучки через фиксированный IPC.',
 'refreshVoices':'Перечисляет системные голоса/распознаватели без запроса микрофона.',
 'speak':'Передаёт только text/voice/rate/volume для plain TTS; пути/PowerShell code не принимаются.',
 'stopVoice':'Запрашивает отмену собственного speech worker.',
 'handlerForVoiceStatus':'В Electron fixture хранит реальный status handler для симуляции speaking без воспроизведения.',
 'ipcMain.handle':'В Electron fixture перехватывает только speech playback для проверки UI/Stop без звука; остальные IPC проходят в настоящий main.',
})
TEST_PURPOSES.update({
 'invalid_text_voice_and_numeric_options_never_start_audio':'Невалидные text/voice/rate/volume не создают worker и не открывают аудиоустройство.',
 'catalog_runs_outside_bridge_and_returns_installed_choices':'Каталог выполняется в отдельном процессе/потоке, busy защищает второй старт.',
 'json_text_is_data_and_stop_cleans_owned_worker':'Unicode/quotes/PowerShell-подобные символы передаются неизменённым JSON; Stop быстро завершает своё дерево.',
 'timeout_is_visible_and_worker_can_be_reused':'Deadline завершает worker и делает ошибку видимой вместо вечного busy.',
 'real_system_voice_renders_wave_without_speakers_or_microphone':'Установленный Windows голос синтезирует PCM WAV; динамики и микрофон не используются.',
 'voice_persona_uses_chat_scope_without_file_tools':'Лола включается только для voice, uses empty Chat scope без tools/auto-memory.',
 'voice_catalog_and_cancel_keep_bridge_responsive_without_microphone':'Настоящий bridge разрешает voice без root, каталог/Stop не блокируют health, неизвестный voice отвергается.',
})

FILE_NOTES['tools/check_live_model.py']='Opt-in smoke реальной модели: disposable AppData/проект, Chat/IDE/Лола, без approvals записи, JSON отчёт.'

FILE_NOTES.update({
    "tools/prepare_windows_dependencies.py": "Загрузка официальных зависимостей по SHA256, выбор server/DLL и подготовка офлайн-пакета без запуска установщиков.",
    "packaging/windows-dependencies.json": "Версии, официальные URL и SHA256 Windows runtime зависимостей.",
    "packaging/prerequisites.nsh": "NSIS bootstrap Visual C++: проверка версии реестра, офлайн-запуск, обработка ошибки и перезагрузки.",
    "packaging/llama-LICENSE.txt": "MIT-лицензия ggml авторов из официального llama.cpp b11829.",
})
TS_NOTES["bundledRuntimePath"] = "Находит включённый CPU llama-server в resources packaged приложения или в build для разработки; не принимает путь от renderer."

FILE_NOTES.update({
    ".github/workflows/release-windows.yml": "Явный release.json запускает сборку и проверки Windows, публикацию prerelease с SHA256 через GITHUB_TOKEN; существующую версию не перезаписывает.",
    "packaging/release.json": "Явное намерение выпустить указанную версию; изменение запускает Release workflow текущей ветки.",
    "packaging/RELEASE_NOTES.md": "Публикуемые инструкции установки, состав и реальные ограничения Windows prerelease.",
})

FILE_NOTES["tests/test_windows_dependencies.py"] = "Тесты закреплённых загрузок: кэш без сети, отклонение подмены и атомарная замена повреждённого файла."
TEST_PURPOSES.update({
 "verified_cache_does_not_download": "Подтверждает повторное использование валидного SHA256-кэша без сетевого обращения.",
 "mismatch_preserves_old_file_and_removes_partial": "Не допускает подменённый файл и удаляет частичную загрузку, сохраняя старый кэш.",
 "success_replaces_corrupt_cache": "Заменяет повреждённый кэш только после успешной проверки новой загрузки.",
})


FILE_NOTES.update({
 'agent/json_tools.py':'Текстовый JSON tool protocol: преобразование истории, строгий parser envelope и адаптация stream к обычному executor.',
 'agent/companion_preferences.py':'Независимый сохраняемый профиль Лолы: модель, endpoint, характер, STT и голос; секреты не сохраняются.',
 'agent/delegation.py':'Единственное определение delegate_task для передачи сложной задачи от Лолы основной модели.',
 'core/python/transcription_service.py':'Ограниченная WAV-транскрипция через локальный whisper.cpp или совместимый API с отменой HTTP.',
 'core/python/desktop_service.py':'Явно включаемые PC tools: human-prompt folder grants, read-only файлы, bounded web search и host screenshot broker.',
 'core/python/telegram_service.py':'Telegram long polling только для owner user ID: команды, состояние, ответы и текущие diff/approval; токен только в памяти Core.',
 'apps/desktop/src/CompanionSettings.tsx':'Настройка характера, независимой модели, JSON/native protocol, автоматической передачи и STT Лолы.',
 'apps/desktop/src/ConnectionsSettings.tsx':'Настройка PC-инструментов и Telegram; явное подключение владельца и защищённое сохранение токена.',
 'apps/desktop/src/microphone.ts':'16 kHz mono PCM16 WAV: подавление шума, блоки 64 мс, завершение по паузе, обрезка тишины и освобождение микрофона.',
 'tests/test_expansion.py':'Контракты разделения истории, профиля без секретов, JSON tools, KV whitelist, PC grants, Telegram owner и WAV validation.',
 'tests/migration/test_json_protocol.py':'Реальный HTTP-сервер без native tools: JSON read/write через тот же diff и approval executor.',
})
register('agent/json_tools.py', """
prepare_json_request | Убирает native tools/tool_choice, добавляет JSON-схемы в system prompt и переводит tool history в обычные сообщения.
parse_tool_json | Принимает только целый JSON envelope с 1–8 разрешёнными вызовами и объектами аргументов; не ищет команды в примерах внутри текста.
JsonToolStream | Ограниченный буфер JSON-ответа поверх отменяемого native stream; возвращает существующему движку знакомую форму delta.tool_calls.
JsonToolStream.__iter__ | Собирает до 1 МБ текста, проверяет обязательность/запрет вызова и создаёт native-shaped delta с UUID каждого вызова.
JsonToolStream.close | Закрывает исходный HTTP stream и освобождает отменяемый запрос.
""")
register('agent/companion_preferences.py', """
validate_profile | Проверяет независимый endpoint/model/tool protocol, характер до 6000 символов, STT URL, голос, темп, громкость и флаги.
load_profile | Загружает companion.json, при отсутствии или повреждении использует независимые defaults с пустым ID модели.
save_profile | Атомарно сохраняет только разрешённые публичные поля, исключая model/STT API keys.
""")
register('core/python/transcription_service.py', """
TranscriptionService | Отдельный отменяемый STT worker; передаёт WAV на явно настроенный endpoint без хранения аудио на диске.
TranscriptionService.start | Проверяет base64 и WAV PCM16 mono 16 kHz до 60 секунд; не допускает второй одновременно работающий запрос.
TranscriptionService.start.transcribe | Отправляет multipart file/model/language/response_format, проверяет текст и отвечает по исходному RPC ID.
TranscriptionService.stop | Выставляет cancel flag и закрывает HTTP client активного распознавания.
TranscriptionService.shutdown | Отменяет запрос и ограниченно ждёт завершения worker.
""")
register('core/python/desktop_service.py', """
prompt_folders | Извлекает существующие абсолютные пути только из исходного человеческого запроса и разрешает их до проверки вложенности.
SearchResults | HTMLParser для ограниченного набора ссылок и заголовков поисковой выдачи; не исполняет HTML/JS.
SearchResults.handle_starttag | Распознаёт result__a, извлекает обычную HTTP(S) ссылку из DuckDuckGo redirect wrapper.
SearchResults.handle_data | Собирает текст текущего заголовка не длиннее 300 символов.
SearchResults.handle_endtag | Завершает ссылку и сохраняет не больше восьми результатов.
DesktopService | Сервис opt-in PC tools и брокер фиксированных операций Electron без произвольного shell.
DesktopService.configure | Сохраняет только boolean enabled в desktop-tools.json; каталоговые разрешения не сохраняются.
DesktopService.request | Создаёт одноразовый UUID host request, ждёт результат до 30 секунд с cooperative cancellation.
DesktopService.respond | Принимает host-ответ только для существующего pending UUID и пробуждает ожидающий worker.
DesktopService.execute | Проверяет включение tools, исходный запрос скриншота, prompt-only папки и bounded поисковый запрос; неизвестные имена отклоняет.
""")
register('core/python/telegram_service.py', """
TelegramService | Владелец исходящего Telegram long polling; фильтрует owner ID/private chat и сериализует управление с Core.
TelegramService.status | Возвращает состояние подключения, имя бота и owner ID без токена и URL с токеном.
TelegramService.start | Валидирует BotFather token и числовой owner ID, запускает один worker; токен хранит только в памяти.
TelegramService.api | Выполняет фиксированный запрос Telegram по TLS; необработанные HTTP exceptions не отправляются пользователю.
TelegramService.send | Отправляет plain text только owner, частями по 3500 символов, с общим лимитом 21000.
TelegramService.observe | Ставит результаты удалённой задачи и approval уведомления в очередь до 100 записей, не блокируя Core HTTP.
TelegramService.command | Отбрасывает группы, посторонних и forwarded сообщения; под общим lock передаёт команду dispatcher.
TelegramService.dispatch | Реализует /status, /stop, /chat, /ide, /miya и точный /approve или /reject по актуальному ID.
TelegramService.poll | Проверяет getMe, отбрасывает старую очередь, читает getUpdates и отправляет уведомления; повторяет сетевые ошибки без раскрытия токена.
TelegramService.stop | Запрашивает отключение и закрывает HTTP client; токен не возвращает.
TelegramService.shutdown | Отключает polling и ограниченно ждёт worker при закрытии Core.
""")
register('core/python/task_service.py', """
TaskService.move_chat | Переносит канонический чат между Chat и voice без удаления сообщений; проверяет исходную область и idle.
TaskService.request_delegation | Разрешает только delegate_task, валидирует target/prompt, создаёт одну pending передачу с исходным человеческим запросом.
TaskService.prepare_handoff | После завершения Лолы создаёт отдельный чат основной модели; IDE требует выбранного проекта, сохраняет источник результата.
TaskService.companion_preferences | Возвращает публичные поля отдельного профиля Лолы без API keys.
TaskService.configure_companion | Сохраняет независимый публичный профиль; ключи модели/STT оставляет только в памяти текущего Core.
TaskService.start.dispatch | Направляет только разрешённые PC tools, delegate_task Лолы или обычные инструменты выбранного проекта; grants делегирования берёт из исходного человеческого запроса.
""")
register('core/python/bridge.py', """
_handle | Dispatcher RPC под общим TaskService lock: области чатов, профиль, STT, PC replies и Telegram; file scope по-прежнему ограничен.
""")
TEST_PURPOSES.update({
 'companion_scope_rejects_cross_loading':'Chat/voice списки раздельны; чужая область отклоняется при load/rename.',
 'profile_does_not_persist_keys_or_change_main_model':'Сохраняет собственную модель/характер Лолы и не пишет API keys в JSON.',
 'json_tools_never_execute_embedded_examples':'Принимает целый envelope и отклоняет unknown tools; пример с окружающим текстом не выполняется.',
 'json_request_has_no_native_roles_or_api_fields':'Удаляет native API tool fields и переводит tool roles в текстовые результаты.',
 'json_stream_converts_complete_reply_to_tool_delta':'Склеивает разорванный JSON и формирует обычный tool delta без показа служебного JSON как ответа.',
 'pc_folders_come_only_from_human_prompt':'Читает только папку из исходного запроса и отказывает сторонней папке и неразрешённому скриншоту.',
 'telegram_ignores_other_users_groups_and_forwards':'Посторонние, группы и пересылки не вызывают даже Stop; owner private command работает.',
 'telegram_approval_keeps_exact_current_id':'Передаёт точный approval ID и текущий run ID обычному механизму подтверждения.',
 'kv_cache_validates_before_launch':'Отклоняет произвольный cache type и передаёт только whitelisted K/V/Flash Attention flags.',
 'transcription_rejects_invalid_audio_without_network':'Некорректный WAV отклоняется до запуска сетевого worker.',
 'json_only_model_uses_same_write_approval':'Сервер отвергает native tools API, но JSON read/write проходят через реальный HTTP и обязательный diff approval.',
})
TS_NOTES.update({
 'desktopRequest':'Исполняет только screenshot или фиксированный DuckDuckGo search URL, публикует локальный preview и отвечает Core по одноразовому UUID.',
 'getCompanionSettings':'Читает независимый публичный профиль Лолы через allowlisted IPC.',
 'configureCompanion':'Сохраняет настройки Лолы отдельно от основной модели и оставляет секреты только в памяти Core.',
 'transcribe':'Передаёт ограниченную base64 WAV-запись в отменяемый STT RPC.',
 'cancelTranscription':'Отменяет текущую транскрипцию и закрывает её сокет.',
 'prepareHandoff':'Переносит pending задание Лолы в новый чат основной модели по точному ID.',
 'moveChat':'Переносит только Chat/voice историю в другую область по явному действию пользователя.',
 'desktopSettings':'Читает opt-in состояние PC tools без доступа к файлам.',
 'configureDesktop':'Включает/выключает PC tools; аргументы модели не могут изменить это разрешение.',
 'telegramStatus':'Читает безопасный статус бота без token и HTTP URL.',
 'connectTelegram':'Подключает token/owner либо явно выбранную защищённую локальную запись; секрет не возвращается renderer.',
 'disconnectTelegram':'Отключает polling бота через Core.',
 'forgetTelegram':'Удаляет только сохранённую encrypted запись токена по явной кнопке пользователя.',
 'apps/desktop/src/App.tsx:App.moveChat':'Переносит выбранный личный чат в область Лолы или обратно и обновляет текущий список.',
 'apps/desktop/src/App.tsx:App.returnToMiya':'Загружает исходный voice чат с добавленным результатом основной модели.',
 'apps/desktop/src/App.tsx:App.acceptHandoff':'Создаёт основную задачу из pending передачи, синхронизирует mode/chat/run refs и запускает модель.',
 'CompanionSettings':'Форма собственного характера, модели, tool protocol, автоматической передачи и STT профиля Лолы.',
 'apps/desktop/src/CompanionSettings.tsx:CompanionSettings.save':'Валидирует профиль в Core, сохраняет публичные настройки, не сохраняет API keys.',
 'apps/desktop/src/CompanionSettings.tsx:CompanionSettings.discover':'Загружает модели именно с чернового endpoint Лолы без изменения основной конфигурации.',
 'ConnectionsSettings':'Настройка opt-in инструментов ПК и owner-only Telegram подключения с защищённым сохранением токена.',
 'apps/desktop/src/ConnectionsSettings.tsx:ConnectionsSettings.refresh':'Обновляет безопасный статус Telegram с cleanup при закрытии настроек.',
 'apps/desktop/src/ConnectionsSettings.tsx:ConnectionsSettings.toggle':'Применяет переключатель PC tools через Core только вне задачи.',
 'apps/desktop/src/ConnectionsSettings.tsx:ConnectionsSettings.connect':'Передаёт token/owner и флаг remember/use_saved; очищает поле token после подключения.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.record':'Запускает явную запись микрофона или завершает текущую; ошибки и unmount освобождают tracks.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.finishRecording':'Отклоняет запись без речи, формирует обрезанный WAV, распознаёт и проверяет актуальность запроса; отправляет текст только при включённой настройке.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.saveVoice':'Сохраняет выбранный голос, темп, громкость и auto-speak в отдельном профиле.',
 'this.processor.onaudioprocess':'Копирует mono float samples до 960000 frames, затем автоматически завершает запись по лимиту 60 секунд.',
 'ascii':'Записывает фиксированные RIFF/WAVE/fmt/data метки в WAV DataView.',
})

FILE_NOTES['tests/migration/test_transcription.py']='Реальный multipart WAV запрос к HTTP STT fixture и отмена зависшего сервера без доступа к микрофону.'
register('core/python/transcription_service.py', """
TranscriptionService.request_audio | Запускает async HTTP и наблюдатель отмены с общим deadline 90 секунд; закрывает socket при cancel.
TranscriptionService.request_audio.request | Передаёт multipart WAV и читает до 1 МБ ответа, проверяя строку text до 50000 символов.
TranscriptionService.request_audio.cancellation | Проверяет межпоточный Event каждые 50 мс без блокировки asyncio loop.
""")
TEST_PURPOSES.update({
 'real_multipart_returns_editable_text':'Отправляет WAV по настоящему HTTP, проверяет multipart file/language и возврат распознанного текста.',
 'cancel_closes_stalled_request_promptly':'Отменяет STT до HTTP headers и завершает worker менее чем за две секунды.',
})

FILE_NOTES['tests/migration/test_delegation.py']='Реальные HTTP-запросы к двум разным ID моделей: Лола ставит передачу, основная модель отвечает, итог сохраняется в voice истории.'
TEST_PURPOSES['independent_model_delegates_and_returns_result']='Изолирует ID моделей и чаты, выполняет delegate_task и возвращает MAIN_MODEL_RESULT в исходную историю Лолы.'

TEST_PURPOSES.update({
 'telegram_poll_drops_backlog_and_never_sends_to_stranger':'Проверяет настоящий dispatcher с HTTPX MockTransport: старый /stop и чужой user игнорируются; status отправляется только owner; токен очищается.',
 'cache_preferences_survive_new_service':'Параметры K/V/threads сохраняются и восстанавливаются новым RuntimeService без сохранения пути модели.',
})
TEST_HELPERS['transport']='HTTPX MockTransport Telegram: getMe/getUpdates/sendMessage без настоящего токена или внешнего сетевого запроса.'

register('core/python/task_service.py', """
TaskService.discard_handoff | Удаляет pending передачу только по точному ID вне активной задачи, чтобы её можно было явно отклонить.
""")
TS_NOTES.update({
 'cancelHandoff':'Отклоняет pending передачу Лолы по точному ID без запуска основной модели.',
 'apps/desktop/src/App.tsx:App.declineHandoff':'Очищает pending передачу и в Core, и в интерфейсе; старое задание больше не блокирует следующее.',
})
TEST_PURPOSES.update({
 'companion_profile_and_history_are_independent_in_real_process':'Через настоящий stdio/Core проверяет отдельную модель, отсутствие ключей в ответах, разделение истории, cross-scope отказ и перенос старого чата.',
 'desktop_telegram_and_invalid_stt_keep_real_bridge_responsive':'Через настоящий процесс проверяет PC opt-in, безопасный Telegram status, отказ невалидному аудио и отзывчивость health.',
})

TS_NOTES['desktopCapturer.getSources']='GUI fixture возвращает синтетический 1×1 NativeImage вместо захвата настоящего экрана; проверяет host broker и preview без чтения рабочего стола пользователя.'
register('core/python/desktop_service.py', """
SearchResults.handle_data | Собирает до 600 символов заголовка или snippet поискового результата без интерпретации разметки.
""")
register('agent/json_tools.py', """
parse_tool_json | Принимает JSON только в начале ответа, целый fenced JSON или Qwen tool_call wrapper; хвост комментария игнорируется, поиск команд внутри произвольного текста запрещён; имена и arguments строго проверяются.
""")

FILE_NOTES.update({
 'core/python/neural_speech.py':'Отменяемый HTTP TTS: bounded PCM WAV, события звука и точное подтверждение плеера по sequence.',
 'apps/desktop/src/NeuralAudio.tsx':'Единый плеер нейроозвучки: PCM WAV из Core, громкость/темп, Stop и подтверждение завершения.',
 'apps/desktop/src/WakeListener.tsx':'Явно включаемый микрофон во всех режимах: speech gate, STT, wake phrase, пауза при задаче/озвучке/ручной записи.',
 'apps/desktop/src/wakePhrase.ts':'Нормализация русской фразы и выделение команды только после совпадающего начала без потери пунктуации команды.',
 'tools/tts/qwen_server.py':'Отдельный localhost Qwen3-TTS сервер: VoiceDesign 1.7B или CustomVoice 0.6B с готовым голосом, русский язык и PCM16 WAV.',
 'tools/tts/start-tts.ps1':'Создаёт TTS среду Python 3.12 с PythonPath, устанавливает согласованные CPU/CUDA torch и torchaudio, поддерживает InstallOnly/LowMemory и запускает сервер.',
 'tools/tts/requirements.txt':'Дополнительные зависимости Qwen3-TTS; не добавляются в основной frozen Core.',
 'tools/tts/piper_server.py':'CPU Piper адаптер прежнего HTTP TTS API: русский ONNX голос, PCM16 WAV, лимиты и отмена между предложениями.',
 'tools/tts/start-piper.ps1':'Создаёт отдельную среду Piper Python 3.12, устанавливает piper-tts и запускает выбранный локальный ONNX голос.',
 'tools/tts/README.md':'Установка TTS, выбор аниме-профиля, ограничения ресурсов и настройка голосовой активации.',
 'tests/migration/test_neural_speech.py':'HTTP PCM fixture, точный sequence плеера и отмена зависшего синтеза без настоящего звука.',
})
register('core/python/neural_speech.py', """
NeuralSpeech | Управляет отдельной нейроозвучкой через HTTP и плеер Electron, не импортируя PyTorch в Core.
NeuralSpeech.status | Возвращает состояние и фиксированный профиль miya-anime-ru без аудиобуфера или текста.
NeuralSpeech.speak | Проверяет текст/темп/громкость, запускает worker и ожидает подтверждения воспроизведения до 200 секунд с учётом замедленного темпа.
NeuralSpeech.speak.run | Получает WAV, публикует voice_audio и завершает операцию после плеера, отмены либо deadline.
NeuralSpeech.fetch | Выполняет bounded async POST и закрывает HTTP socket при отмене.
NeuralSpeech.fetch.request | Читает максимум 15 МБ и проверяет PCM16 mono WAV 8–48 kHz до 120 секунд.
NeuralSpeech.fetch.cancellation | Наблюдает Event отмены без блокировки event loop.
NeuralSpeech.playback | Принимает только текущий sequence; устаревший ответ плеера не завершает новую озвучку.
NeuralSpeech.stop | Отменяет сеть и публикует остановку глобальному плееру.
NeuralSpeech.shutdown | Останавливает worker и ограниченно ждёт завершения.
""")
register('tools/tts/qwen_server.py', """
synthesize | Генерирует русский звук: готовый speaker через CustomVoice либо описание через VoiceDesign; фиксирует seed и ограничение токенов, кодирует PCM16 WAV в памяти.
Handler | Loopback HTTP handler с JSON-only POST, запретом Origin и одним слотом генерации.
Handler.do_GET | Возвращает health после загрузки модели; остальные GET получают 404.
Handler.do_POST | Проверяет запрос и concurrency, останавливает talker при отключении клиента/deadline и освобождает слот в finally.
Handler.do_POST.guard | PyTorch forward pre-hook проверяет срок 150 секунд и закрытие HTTP-сокета без чтения текста запроса.
Handler.reply | Пишет ответ с явными Content-Type и Content-Length.
Handler.log_message | Не сохраняет тексты и запросы пользователя в HTTP access log.
main | Выбирает VoiceDesign 1.7B либо CustomVoice 0.6B и speaker, получает локальный снимок, выбирает CPU/CUDA и dtype, проверяет запас VRAM и слушает только 127.0.0.1:9080.
""")
register('tools/tts/piper_server.py', """
synthesize | Собирает чанки Piper в PCM16 mono WAV до 120 секунд/15 МиБ и проверяет отмену после каждого предложения.
main | Загружает ONNX голос через CPUExecutionProvider, подключает синтез к общему HTTP handler и слушает только localhost.
""")
TEST_PURPOSES['piper_backend_wav_and_disconnect_guard']='Проверяет HTTP callback Piper, формат/число кадров WAV, освобождение слота и распространение отмены между чанками.'
TS_NOTES.update({
 'NeuralAudio':'Проигрывает только события Core, останавливает старый Audio и подтверждает текущую озвучку.',
 'WakeListener':'Управляет явно включённым прослушиванием и паузами без обращения к чат-модели.',
 'WakeListener.refresh':'Обновляет профиль при сохранении настроек и не включает микрофон автоматически.',
 'WakeListener.capture':'Получает состояние ручной записи для исключения конкурентного STT.',
 'WakeListener.cycle':'Записывает фрагмент до тишины/12 секунд, распознаёт речь и активирует Лолу по началу фразы.',
 'normalizeSpeech':'Приводит русскую фразу к нижнему регистру, ё→е и пробелам между словами.',
 'wakeCommand':'Проверяет фразу только в начале; возвращает исходный хвост с пунктуацией либо null.',
 'activateMiya':'Открывает/фокусирует окно, переключает режим и передаёт распознанный текст Лоле.',
 'player.onended':'Подтверждает завершение только текущего Audio по sequence.',
 'player.onerror':'Сообщает Core о невозможности воспроизведения текущего Audio.',
})
TEST_PURPOSES.update({
 'http_audio_and_exact_playback_sequence':'Проверяет реальный HTTP WAV, русский язык/описание, предел текста и отказ устаревшему sequence.',
 'cancel_closes_stalled_synthesis':'Отменяет запрос до headers менее чем за две секунды и запрещает поздний playback ack.',
})
TEST_HELPERS['emit']='Собирает события тестовой нейроозвучки и сигнализирует о готовом WAV без вывода звука.'
TS_NOTES.update({
 'voicePlayback':'Фиксированный IPC сообщает Core об окончании/ошибке текущего sequence звука.',
 'openTtsFolder':'Открывает только штатную папку sidecar TTS, без запуска команды из ответа модели.',
 'activateAssistant':'Показывает и фокусирует окно после явной включённой фразы активации.',
 'wakeListening':'Отключает background throttling только пока пользователь включил прослушивание.',
})
for _wake_symbol in ('WakeListener.refresh','WakeListener.capture','WakeListener.cycle'):
    TS_NOTES['apps/desktop/src/WakeListener.tsx:'+_wake_symbol]=TS_NOTES.pop(_wake_symbol)

FILE_NOTES['tests/migration/test_tts_server.py']='HTTP-регрессии серверной отмены TTS, освобождения busy и ограничения времени без нейронных весов.'
TEST_PURPOSES.update({
 'http_busy_and_deadline_have_actionable_messages':'Проверяет понятные сообщения Core для HTTP 429/504 без отправки звука и показа HTTPStatusError.',
 'disconnect_releases_busy_server_and_allows_retry':'Закрывает настоящий HTTP-сокет во время генерации, проверяет освобождение 429 и успешный повтор.',
 'deadline_returns_504_and_removes_hook':'Проверяет HTTP 504 при deadline и обязательное удаление hook/освобождение слота.',
})
TEST_HELPERS.update({
 'register_forward_pre_hook':'Устанавливает тестовую проверку отмены как PyTorch talker без установки torch.',
 'remove':'Удаляет тестовый forward hook после окончания или отмены запроса.',
 'generate':'Имитирует шаги нейронной генерации с forward hook и создаёт короткий PCM WAV без звука.',
})
FILE_NOTES.update({
 'apps/desktop/electron/desktopApps.ts':'Каталог локально разрешённых EXE: системные приложения, выбор пользователем, ID без путей для модели и запуск без shell/аргументов.',
 'tests/electron/desktop-apps.cjs':'Node-проверка границы каталога приложений: ID, запрет путей/команд, EXE, повторное добавление, удаление и браузер без реальных окон.',
})
TS_NOTES.update({
 'apps/desktop/electron/main.ts:desktopApplications':'Создаёт host-каталог приложений с запуском EXE без shell и аргументов и фиксированным URL браузера.',
 'apps/desktop/electron/desktopApps.ts:Application':'Приватная запись разрешённого приложения: ID, отображаемое имя и выбранный пользователем путь EXE.',
 'changeApplication':'Добавляет EXE через системный picker или удаляет разрешение по ID, обновляет список и ошибки в UI.',
 'desktopApplications':'Создаёт или запрашивает каталог разрешённых приложений ПК; модель получает ID и названия без путей.',
 'addDesktopApplication':'Открывает только системный EXE-picker для добавления разрешённого приложения.',
 'removeDesktopApplication':'Удаляет пользовательское разрешение запуска по ID через фиксированный IPC.',
})
TEST_PURPOSES['application_tools_broker_ids_without_shell_or_arguments']='Проверяет передачу ID приложений в host broker, отказ путям/аргументам, отмену и общий выключатель PC tools.'
TEST_PURPOSES['search_falls_back_to_bing_and_rejects_non_web_links']='Имитирует таймаут DuckDuckGo и проверяет Bing RSS fallback с фильтрацией file-ссылок.'

FILE_NOTES.update({
 'docs/SERENA_TRAINING_PLAN.md':'Разрешение, этапы и критерии пробной Serena, Windows окружение, provenance датасета, ограничения и восстановление обучения.',
 'docs/31-miya-serena-and-character.md':'Озвучка Serena по умолчанию, управление локальным Piper, простые настройки и состояния анимированного персонажа.',
 'apps/desktop/electron/speechRuntime.ts':'Запуск фиксированного локального Piper, установка проверенной Serena, health и остановка только своего процесса.',
 'apps/desktop/src/LolaAvatar.tsx':'Чиби по референсу: выбор ряда атласа 4×7 по состоянию Лолы, подпись, речевая волна и уменьшение движения.',
 'apps/desktop/src/assets/miya-states.png':'Прозрачный 4×2 атлас поз светловолосой аниме-горничной по пользовательскому референсу.',
 'apps/desktop/src/assets/miya-states.prompt.md':'Сохранённые prompts встроенного image_gen и схема ячеек персонажа.',
 'tools/tts/training/README.md':'Команды возобновляемой генерации, обучения и контроля локального конвейера Serena.',
 'tools/tts/training/generate_serena.py':'Возобновляемый корпус Qwen Serena: закреплённая revision, PCM22k WAV, локальный STT отбор и provenance каждого примера.',
 'tools/tts/training/run_training.py':'Ограниченное Windows дообучение VITS: преобразование Linux checkpoint, warmstart, eSpeak workaround и resume.',
 'tools/tts/training/export_and_evaluate.py':'ONNX экспорт с совместимым tracer и CPU/STT проверкой четырёх новых фраз без объявления совпадения тембра.',
 'tools/tts/training/pipeline.py':'Однопроцессный локальный контроллер этапов с атомарным состоянием, границами шагов и остановкой при ошибках.',
})
TS_NOTES.update({
 'LolaAvatar':'Выбирает четыре кадра нужного состояния из чиби-атласа, показывает подпись и поддерживает отключение анимации.',
 'LolaState':'Допустимые состояния персонажа: ожидание, слушание, размышление, работа, речь, успех и ошибка.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.selectProvider':'Останавливает текущую озвучку, сохраняет выбранный движок профиля и обновляет каталог.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.startSerena':'Запрашивает запуск/проверку управляемого Piper и выводит понятное состояние или ошибку.',
 'speechRuntime':'Создаёт один сервис Piper с локальными фиксированными путями вместо команд renderer.',
})
register('tools/tts/training/generate_serena.py', """
texts | Собирает уникальный русский корпус из исходных фраз и бытовых комбинаций без перезаписи WAV при продолжении.
normalize | Удаляет различия регистра, ё и пунктуации для приблизительного сравнения текста с STT.
main | Фиксирует manifest, пакетно генерирует Serena, передискретизирует WAV, проверяет STT и сохраняет принятые metadata/журнал.
""")
register('tools/tts/training/run_training.py', """
SaveFinalCheckpoint | Сохраняет фактические последние веса даже при достижении max_steps посередине эпохи.
SaveFinalCheckpoint.on_train_end | Вызывает trainer.save_checkpoint для final.ckpt в корне training, независимо от эпохальных val_mel checkpoints.
prepare_checkpoint | Из доверенного Linux checkpoint извлекает state_dict с временной совместимостью Path, исключает старый оптимизатор и сохраняет описание hyperparameters.
main | Проверяет объём данных, задаёт warmstart/resume, BF16 GPU и ограниченные шаги, исправляет путь eSpeak и состав checkpoint callbacks.
main.resume_fit_start | Отключает сохранённый однократный warmstart при resume, чтобы LightningCLI не сбрасывал обученные веса к базовому голосу.
""")
register('tools/tts/training/export_and_evaluate.py', """
main | Экспортирует обученный VITS через legacy ONNX tracer, проверяет модель, синтезирует новые фразы на CPU и сохраняет оценку STT/задержки.
""")
register('tools/tts/training/pipeline.py', """
save_state | Атомарно обновляет JSON состояния этапа, PID и ошибку либо оценку без преждевременного статуса готовности.
run | Запускает зависимый subprocess со структурированными аргументами и отдельным локальным журналом, возвращает exit code.
main | Удерживает Windows lock, ждёт generator, выполняет ступени 6000/12000 шагов, экспорт и проверку; сообщает trial_ready только после ASR.
""")
TEST_HELPERS['search_transport']='Локальная HTTPX-фикстура недоступного первого поисковика и безопасной RSS-выдачи второго.'
register('core/python/desktop_service.py', """
search_web | Получает до восьми ограниченных текстовых результатов: DuckDuckGo HTML, затем Bing RSS при отказе, без чтения страниц и XML DTD.
""")

TEST_PURPOSES['lola_wake_migration_preserves_custom_phrase'] = 'Стандартная старая фраза становится Привет, Лола; пользовательская фраза сохраняется.'

FILE_NOTES.update({
 'agent/ide_workflow.py':'Whitelist ролей IDE, отдельное сохранение без ключей и разрешение наследуемых моделей/endpoint без утечки основного токена.',
 'agent/model_lifecycle.py':'Последовательная отменяемая загрузка/выгрузка назначенных моделей LM Studio 0.4+/Ollama и read-only каталог.',
 'agent/ide_coordinator.py':'Четыре роли IDE, локальные передачи кода, ограниченное исправление, существующие diff approvals и подтверждённая проверка файлов.',
 'apps/desktop/src/IDEWorkflowSettings.tsx':'Настройка четырёх ролей и компактный переключатель цикла/отдельного этапа в существующем оформлении IDE.',
 'tests/migration/test_ide_workflow.py':'Реальный loopback HTTP/SSE проверяет роли, память моделей, согласование записи, исправления, чтение проверяющим и resume.',
})
register('agent/ide_workflow.py', '''
validate_workflow | Проверяет четыре роли, режим, провайдер, относительные настройки URL/ID, контекст и число исправлений; отбрасывает секреты.
load_workflow | Загружает отдельный JSON либо возвращает выключенный совместимый профиль по умолчанию.
save_workflow | Атомарно сохраняет только прошедшие whitelist настройки без API-ключей.
resolve_roles | Подставляет основные URL/ID и только для того же URL наследует основной ключ; проверяет назначение используемых ролей.
''')
register('agent/model_lifecycle.py', '''
ModelLifecycle | Управляет одной активной моделью роли, не запускает shell и не завершает чужие процессы.
ModelLifecycle.origin | Разрешает нативное управление только на корне проверенного сервера без произвольных префиксов маршрута.
ModelLifecycle.request | Выполняет ограниченный запрос с коротким наблюдением Event отмены и отдельным deadline очистки.
ModelLifecycle.request.run | Владеет asyncio request и гарантирует его отмену/закрытие при выходе.
ModelLifecycle.request.run.fetch | Передаёт токен только выбранному endpoint без redirects/proxy env; ограничивает JSON ответ двумя МБ.
ModelLifecycle.catalog | Читает LM Studio model keys/instances, Ollama tags/ps или OpenAI model IDs без загрузки весов.
ModelLifecycle.unload | Выгружает точный instance_id LM Studio либо exact Ollama model через keep_alive=0.
ModelLifecycle.release | Выгружает известную активную модель; при ошибке сохраняет владение и запрещает последующую загрузку.
ModelLifecycle.acquire | Повторно использует ту же модель либо выгружает прежнюю, проверяет каталог/чужую память, затем загружает только назначенную.
''')
register('agent/ide_coordinator.py', '''
RoleOutputError | Выделяет ошибки формата, для которых разрешён один повтор без записи неверного результата.
IDECoordinator | Последовательно координирует четыре AgentEngine с изоляцией прав, локальными артефактами и проверкой результата.
IDECoordinator._flow_snapshot | Добавляет безопасные названия/ID/статусы ролей и номер исправления к существующей задаче.
IDECoordinator._persist | Атомарно сохраняет передачи ролей вне проекта и уведомляет UI о checkpoint.
IDECoordinator._lifecycle_event | Сохраняет точную активную модель для последующей очистки, передаёт состояние загрузки в журнал/план.
IDECoordinator.requestInterruption | Останавливает общий цикл и текущий дочерний HTTP/approval цикл.
IDECoordinator.resolve_write_approval | Пересылает решение только текущему AgentEngine, сохраняющему проверку diff и revision.
IDECoordinator._child_task | Объединяет counters, доказательства чтения и состояние дочерней роли; completed этапа не завершает весь цикл.
IDECoordinator._chat | Помечает ответ ролью и сохраняет общую историю без подмены исходного запроса служебными prompt.
IDECoordinator._handoff | Передаёт полные релевантные материалы/прочитанные файлы; при превышении бюджета останавливается без обрезки кода.
IDECoordinator._capture_context | Из успешных read_file tool results собирает контекст файлов для автора кода без собственных файловых инструментов.
IDECoordinator._structured_output | Валидирует JSON автора/проверяющего, полные path/content и границы проекта до использования артефакта.
IDECoordinator._syntax_checks | Читает только modified_files через sandbox и безопасно проверяет Python AST/JSON без запуска кода.
IDECoordinator._stage | Выбирает модель и права роли, связывает события/approvals, учитывает общий бюджет, проверяет ответ до передачи дальше.
IDECoordinator._stage.delta | Даёт потокам уникальные role/cycle/turn ID и обозначает роль в первом фрагменте.
IDECoordinator._verdict | Требует pass без issues, успешных статических проверок и чтения каждого изменённого файла текущим проверяющим.
IDECoordinator.run | Выполняет полный/одиночный этап, один повтор формата, до двух циклов исправлений, pause/resume и обязательную выгрузку.
''')
register('core/python/task_service.py', '''
TaskService.workflow_preferences | Возвращает настройки IDE без секретов.
TaskService.configure_workflow | Проверяет настройки и ключи до сохранения; блокирует смену во время задачи, ключи оставляет в памяти.
TaskService.start_workflow_discovery | Снимает конфигурацию выбранной роли и запускает отменяемое чтение каталога в отдельном потоке.
TaskService.start_workflow_discovery.discover | Выбирает каталог нативного lifecycle либо обычный OpenAI discovery и возвращает ограниченную ошибку.
''')
TS_NOTES.update({
 'IDEWorkflowSettings':'Загружает draft четырёх ролей, endpoint/ID/протокол, память/исправления и сохраняет независимо от Chat/Лолы.',
 'apps/desktop/src/IDEWorkflowSettings.tsx:IDEWorkflowSettings.changeRole':'Изменяет только выбранную роль в локальном draft.',
 'apps/desktop/src/IDEWorkflowSettings.tsx:IDEWorkflowSettings.discover':'Получает список на выбранном сервере роли без загрузки весов и сохраняет datalist.',
 'apps/desktop/src/IDEWorkflowSettings.tsx:IDEWorkflowSettings.save':'Сохраняет whitelist ролей, уведомляет App и очищает отображаемые временные ключи.',
 'IDEWorkflowBar':'Компактный выбор одной модели, полного цикла либо отдельной роли; открывает настройки в той же палитре.',
 'apps/desktop/src/IDEWorkflowSettings.tsx:IDEWorkflowBar.select':'Меняет режим IDE через backend idle guard, затем обновляет конфигурацию App.',
})
TEST_PURPOSES.update({
 'pipeline_real_sse_diff_and_one_resident_model':'Полный цикл через настоящие HTTP/SSE создаёт файл после одного diff; roles имеют разные права, peak моделей равен одному.',
 'rejected_write_does_not_reach_reviewer':'Отклонённая запись не создаёт файл и не объявляется проверенным результатом.',
 'reviewer_revision_has_bounded_repair_cycle':'revise возвращает код автору/сборщику; повторный diff и перечитывание заканчиваются pass.',
 'verdict_without_reading_changed_file_cannot_pass':'Самодекларация pass без чтения изменённого файла приостанавливает цикл.',
 'resume_repeats_only_unfinished_review':'После невалидного verdict продолжение выполняет только проверяющего, не повторяя запись/approval.',
 'author_path_escape_stops_before_builder':'Путь за пределами выбранного проекта останавливает передачу до сборщика.',
 'unrelated_loaded_model_is_not_evicted':'Посторонняя загруженная модель сохраняется, цикл не загружает вторую.',
 'same_model_is_reused_until_release':'Соседние роли с той же моделью не загружают её повторно, финальная выгрузка одна.',
 'ollama_pipeline_loads_and_unloads_serially':'Нативные tags/ps/generate Ollama обеспечивают полный последовательный цикл с одной моделью в памяти.',
 'cancel_interrupts_stalled_model_load':'Остановка закрывает настоящий зависший HTTP запроса загрузки менее чем за две секунды.',
 'role_secrets_never_persist_or_leak_to_different_endpoint':'Ключи не попадают в файл/ответ; основной токен не наследуется другим сервером.',
 'invalid_configuration_does_not_mutate_saved_roles':'Некорректный API-ключ не приводит к частичному сохранению конфигурации.',
 'chat_mode_never_uses_role_coordinator':'Включённый профиль IDE не меняет исполнение Chat и не управляет моделями при его запуске.',
})
register('tests/migration/test_ide_workflow.py', '''
WorkflowHandler.reply | Отдаёт JSON нативных fixture endpoints без обращения к внешним моделям.
WorkflowHandler.do_GET | Эмулирует LM Studio catalog и Ollama tags/ps с состоянием загруженных моделей.
WorkflowHandler.do_POST | Эмулирует load/unload и ответы ролей через SSE, фиксирует права и пик памяти.
WorkflowTests.emit | Собирает события и подтверждает/отклоняет точный proposal активного тестового запуска.
WorkflowTests.run_workflow | Запускает настоящий TaskService/Coordinator и ждёт bounded завершения потока.
WorkflowTests.test_cancel_interrupts_stalled_model_load.acquire | Захватывает результат отменяемой фоновой загрузки для проверки сокета.
''')

FILE_NOTES.update({
 'agent/smart_context.py':'Детерминированное сжатие временного контекста с архивом ограничений и фактов без LLM-запросов и изменения канонической истории.',
 'core/python/assistant_service.py':'Локальные часы, ограниченный AST-калькулятор, атомарные заметки и отменяемые таймеры Лолы.',
 'apps/desktop/electron/assistantMedia.ts':'Повторная host-валидация фиксированных музыкальных HTTPS URL и реального локального аудиофайла внутри разрешённых папок.',
 'tests/test_smart_context.py':'Проверки архива, неизменности истории, пар tools, полного кода, JSON и дедупликации.',
 'tests/test_assistant_service.py':'Проверки утилит Лолы, сохранения заметок, таймеров, музыки и папок из исходного prompt.',
 'tests/electron/assistant-media.cjs':'Host-проверки музыкальных ссылок и путей аудио, включая junction, без воспроизведения и браузера.',
 'agent/context_manager.py':'Сборка временного рабочего контекста с метаданными задачи, умным сжатием и статистикой.'
})
register('agent/smart_context.py', '''
context_size | Считает символы сериализованного JSON, а не токены модели.
text_digest | Возвращает первые 16 hex символов SHA-256 для сверки сокращённого источника.
salient_text | Выбирает строки по запросу, ограничениям, началу и концу; маркирует фрагменты и исходный размер.
compact_tool_result | Сохраняет валидный JSON с путём, статусом, ошибкой и fingerprint; сокращает крупные чтения и списки.
context_archive | Собирает ограничения исходных пользователей, краткие запросы, решения и последние факты tools; при невозможности сохранить ограничения останавливается.
context_archive.render | Сериализует архив как данные истории без повышения роли или прав.
smart_compact_messages | Защищает текущий запрос и код, сохраняет целые пары tools, архивирует старые группы и возвращает метрики без изменения истории.
''')
register('core/python/assistant_service.py', '''
calculate | Разбирает арифметику через AST с лимитами сложности, степени и конечного результата; не выполняет Python.
calculate.evaluate | Рекурсивно разрешает только числа, скобки и whitelist арифметических операций.
AssistantService | Владеет локальным хранилищем заметок, блокировкой и ограниченными таймерами до закрытия приложения.
AssistantService.notes | Читает ограниченный JSON список заметок; повреждённый файл сохраняется без перезаписи.
AssistantService.execute | Выполняет именованную утилиту, валидирует параметры, атомарно пишет заметки или управляет таймерами.
AssistantService.fire | Однократно удаляет таймер, отменяет callback и отправляет уведомление, если сервис ещё работает.
AssistantService.shutdown | Отменяет все таймеры и запрещает новые операции.
''')
register('core/python/desktop_service.py', '''
music_url | Разрешает только HTTPS музыкальные хосты без credentials и нестандартного порта.
''')
TS_NOTES.update({
 'validateMusicURL':'Повторно проверяет HTTPS URL по точному whitelist музыкальных хостов, без credentials и нестандартных портов.',
 'validateAudioPath':'Канонизирует файл и корни, запрещает UNC/исполняемые расширения и выход из исходных папок через junction.'
})
TEST_PURPOSES.update({
 'old_design_constraint_survives_long_history':'Сжатие сохраняет старое ограничение дизайна и последний запрос, не меняя канонический список.',
 'tool_pairs_and_write_arguments_are_never_cut':'Полные аргументы записи и связанный tool_call_id сохраняются вместе.',
 'current_code_handoff_is_protected_or_rejected':'Текущий код передаётся полностью либо выдаётся ошибка бюджета без обрезки.',
 'large_tool_json_keeps_error_path_and_valid_json':'Сокращённый результат чтения остаётся JSON с путём, fingerprint и релевантным фрагментом.',
 'archive_never_becomes_system_permissions':'Старый текст остаётся данными assistant и не добавляет системных разрешений.',
 'repeated_tool_facts_are_deduplicated_and_history_unchanged':'Архив оставляет последний факт по пути без изменения полной истории.',
 'calculator_has_no_calls_names_or_unbounded_powers':'AST-калькулятор считает арифметику и отвергает вызовы, имена и слишком большую степень.',
 'notes_persist_without_arbitrary_paths':'Заметки переживают новый экземпляр, повреждённое хранилище не перезаписывается.',
 'timer_emits_once_and_cancelled_timer_does_not_fire':'Таймер уведомляет один раз, отменённый не срабатывает, shutdown очищает сервис.',
 'music_links_reject_executables_private_hosts_and_spoofing':'Музыкальный URL не допускает протоколы файлов, private hosts и поддельные домены.',
 'music_search_encodes_query_and_does_not_claim_playback':'Музыкальный поиск кодирует запрос и не подтверждает звучание после открытия страницы.',
 'local_audio_requires_original_prompt_folder_and_extension':'Локальный плеер принимает только аудио из явно указанной исходной папки.'
})
TEST_PURPOSES.update({
 'editor_can_save_files_up_to_one_mb_and_recheck_conflicts':'Редактор применяет файл ровно 1 МБ и отказывает при внешнем изменении; лимит агентского preview остаётся 120 КБ.',
 'change_between_revision_check_and_diff_does_not_authorize_stale_draft':'Изменение файла между проверкой revision и снимком diff не создаёт разрешения на устаревший черновик.',
 'full_unicode_notes_capacity_stays_readable_after_restart':'200 заметок по 4000 кириллических символов сохраняются и читаются новым сервисом; 201-я не меняет файл.',
 'note_limit_counts_whitespace_without_corrupting_store':'Пробелы учитываются в лимите 4000 символов; отказ сохраняет прежнее хранилище.',
 'nested_explorer_paths_match_editor_paths':'Вложенный путь проводника совпадает с каноническим POSIX-путём вкладки на Windows.',
})
TEST_HELPERS['external_change']='Детерминированно меняет файл между проверкой editor revision и построением снимка diff.'
TS_NOTES['tests/electron/smoke.cjs:win.webContents.executeJavaScript']='Добавляет текст неудавшегося renderer-шага к ошибке скрытого Electron smoke для диагностики.'

# Neutral 7 removes the four-role coordinator, retaining historical narrative docs.
_removed_role_modules=('agent/ide_coordinator.py','agent/ide_workflow.py','agent/model_lifecycle.py','apps/desktop/src/IDEWorkflowSettings.tsx','tests/migration/test_ide_workflow.py')
for _module in _removed_role_modules:
    FILE_NOTES.pop(_module,None)
    for _key in list(SYMBOL_NOTES):
        if _key.startswith(_module+':'):SYMBOL_NOTES.pop(_key)
    for _key in list(TS_NOTES):
        if _key.startswith(_module+':'):TS_NOTES.pop(_key)
for _name in ('configure_workflow','start_workflow_discovery','start_workflow_discovery.discover','workflow_preferences'):
    SYMBOL_NOTES.pop('core/python/task_service.py:TaskService.'+_name,None)
for _name in ('IDEWorkflowBar','IDEWorkflowSettings','apps/desktop/src/App.tsx:App.moveChat','configureIDEWorkflow','getIDEWorkflow','listIDEModels'):
    TS_NOTES.pop(_name,None)

FILE_NOTES.update({
 'agent/companion_policy.py':'Граница делегирования Лолы по исходному намерению человека и очистка ответов/озвучки от разметки.',
 'agent/connection_profiles.py':'Именованные публичные конфигурации моделей без API-ключей.',
 'agent/mcp_client.py':'Настоящие соединения MCP stdio/Streamable HTTP с discovery, ограничениями, отменой и закрытием transport.',
 'agent/progress_guard.py':'Окно отпечатков вызовов и результатов для остановки чередующихся циклов без продвижения.',
 'agent/project_command.py':'Опциональный запуск тестов/сборок после отдельного подтверждения; ограниченный вывод, время и ProcessJob.',
 'agent/projects.py':'Атомарное хранение именованных пространств: папка, инструкции и метаданные.',
 'agent/responses_adapter.py':'Преобразование канонической истории и потоковых событий OpenAI Responses в существующий цикл агента.',
 'apps/desktop/src/BrandMark.tsx':'Векторный знак Neutral: N и точка равновесия; цвет наследуется от темы.',
 'apps/desktop/src/ConnectionProfiles.tsx':'Сохранение, выбор и удаление публичных профилей подключения модели.',
 'apps/desktop/src/ConversationSidebar.tsx':'Проекты, поиск разговоров, закрепление, архив, копии, повтор, экспорт, перемещение и удаление.',
 'apps/desktop/src/ExtensionsSettings.tsx':'Настройки наборов, отдельных tools, навыков, JSON-пакетов и MCP серверов.',
 'apps/desktop/src/VoiceSettings.tsx':'Общая страница голоса Лолы с громкостью, скоростью, автоматической озвучкой и расширенной конфигурацией.',
 'apps/desktop/src/Welcome.tsx':'Пустое состояние Neutral с короткими сценариями и переходом в IDE.',
 'apps/desktop/src/styles/neutral.css':'Общий дизайн Neutral: токены тем, боковая навигация, проекты, настройки, адаптация размера и reduced motion.',
 'apps/desktop/src/voiceText.ts':'Очистка презентационной разметки потокового ответа Лолы перед показом и озвучкой.',
 'assets/neutral.ico':'Многоразмерная иконка установщика/Windows: PNG-кадры от 16 до 256 пикселей.',
 'assets/neutral.png':'Иконка окна Neutral, 512 пикселей, полученная из исходного SVG.',
 'assets/neutral.svg':'Редактируемый векторный исходник знака приложения и его фона.',
 'core/python/conversation_service.py':'Операции организации чатов с проверкой пространства, режима и корня файлов.',
 'core/python/extension_service.py':'Единый реестр разрешённых возможностей, progressive skills, импорт пакетов и снимки для одного запуска.',
 'tests/electron/neutral-smoke.cjs':'Изолированная GUI-проверка нового Neutral: проекты/навыки/MCP/Node, подтверждения, история, темы и удаление.',
 'tests/fixtures/mcp_echo.py':'Настоящий локальный MCP сервер арифметики и ожидания для stdio/HTTP проверок.',
 'tests/test_companion_policy.py':'Границы coding intent Лолы, очистка Markdown, математики и внутренних тегов.',
 'tests/test_neutral_conversations.py':'Изоляция проектов/режимов, архив, удаление, копия/повтор, экспорт и профили без ключей.',
 'tests/test_neutral_extensions.py':'Переключатели, неизменяемый снимок, навыки-черновики, пакеты и реальные MCP transports.',
 'tests/test_project_command.py':'Подтверждение и отказ запуска, корень cwd, код возврата, лимит вывода и отмена процесса.',
 'tests/test_responses_adapter.py':'Локальная HTTP/SSE фикстура OpenAI Responses: текст, функции, reasoning items, probe и retry.',
 'tools/generate_brand_icons.py':'Разработка: рендер SVG через Qt и запись PNG/многоразмерного ICO без Pillow.',
 'requirements-core.txt':'Диапазоны OpenAI/HTTPX и фиксированный официальный MCP SDK для ядра без Qt.',
 'apps/desktop/src/ModelSettings.tsx':'Общее окно Neutral с боковыми разделами моделей, Лолы, расширений, ПК, оформления, контекста и runtime.',
})
register('agent/companion_policy.py','''
is_coding_request | Определяет разрешённое делегирование по исходному запросу; исключает бытовые значения слова «код» и программы мероприятий.
clean_speech_text | Удаляет Markdown/HTML/reasoning и блоки кода, сохраняет читаемые слова и переводит числовое умножение в речь.
''')
register('agent/connection_profiles.py','''
ConnectionProfiles | Каталог именованных публичных параметров API-моделей; секретные поля не принимаются в сохранённый профиль.
ConnectionProfiles.list | Читает ограниченный по размеру список профилей из пользовательского каталога.
ConnectionProfiles.save | Проверяет имя/ID/параметры и атомарно добавляет или заменяет один из максимум 30 профилей.
ConnectionProfiles.remove | Удаляет выбранную запись, сохраняя другие профили и активную конфигурацию модели.
''')
register('agent/mcp_client.py','''
validate_server | Проверяет ID, transport, URL или command/args и возвращает только разрешённые публичные поля.
MCPClient | Исполнитель короткоживущих MCP соединений; токен передаётся отдельно от публичных настроек.
MCPClient.operation | Запускает coroutine из синхронного диспетчера и превращает ошибки соединения в ограниченный результат.
MCPClient._operate | Ограничивает общее время и отслеживает отмену, закрывая transport и его внутреннюю задачу.
MCPClient._operate.exchange | Открывает stdio/HTTP клиент, получает страницы схем или выполняет один tool, ограничивая результаты.
''')
register('agent/model_client.py','''
ModelClient.create.complete | Выбирает нестриминговый Chat Completions или Responses и приводит результат к ожидаемому интерфейсу choices.
ModelClient.request | Повторяет временные сетевые/429/5xx ошибки до начала ответа максимум два раза; не повторяет частичный поток.
''')
register('agent/progress_guard.py','''
ProgressGuard | Ограниченное окно SHA256 отпечатков имени, аргументов и результата вызова.
ProgressGuard.observe | Добавляет результат и обнаруживает четыре одинаковых исхода в последних шестнадцати действиях, включая A/B цикл.
''')
register('agent/project_command.py','''
run_project_command | Проверяет cwd/аргументы, требует отдельное подтверждение и запускает программу без shell с deadline и ограниченным выводом.
run_project_command.read | Непрерывно освобождает stdout/stderr pipe, сохраняя не больше 64 КБ и считая объём для признака усечения.
''')
register('agent/projects.py','''
ProjectStore | Каталог пространств, объединяющих разговоры общими инструкциями и необязательной папкой IDE.
ProjectStore.list | Читает до 1 МБ каталога и явно сообщает повреждение вместо молчаливой потери данных.
ProjectStore.get | Возвращает выбранный проект либо совместимое личное пространство с пустым ID.
ProjectStore.save | Проверяет имя, инструкции и существование папки; атомарно сохраняет проект с временными метками.
ProjectStore.remove | Удаляет только метаданные группы; перенос разговоров организует bridge, файлы проекта не затрагиваются.
''')
register('agent/responses_adapter.py','''
response_request | Преобразует сообщения/tool results в Responses input, добавляет инструкции и store=false, сохраняет reasoning continuity внутри запуска.
chat_chunk | Создаёт минимальный совместимый объект choices/delta для существующего потокового AgentEngine.
ResponseEvents | Состояние преобразования одного Responses stream: индексы функций и уже полученные аргументы.
ResponseEvents.translate | Переводит текст и аргументы функций, обрабатывает завершение/ошибку и сохраняет output items для следующего tool turn.
response_completion | Приводит нестриминговый output_text к интерфейсу Chat Completion, используемому проверкой завершения и памятью.
''')
register('core/python/conversation_service.py','''
ConversationService | Сервис организации канонической истории без доступа к произвольным файлам проекта.
ConversationService.scoped | Проверяет одновременно ID, режим, корень файлов и пространство; чужой чат не допускается к операции.
ConversationService.update | Меняет pin/archive/project_id только в idle-состоянии и сбрасывает активный выбор при перемещении или архиве.
ConversationService.delete | Требует подтверждение, удаляет выбранный чат и checkpoint, сбрасывает активный выбор.
ConversationService.fork | Копирует завершённую историю без активного checkpoint или готовит повтор последнего запроса в независимой ветке.
ConversationService.export | Формирует ограниченный Markdown/JSON для системного окна сохранения; не пишет путь из model arguments.
ConversationService.search | Ищет название и user/assistant текст внутри режима/пространства, разделяет архив и сортирует закреплённые выше.
''')
register('core/python/extension_service.py','''
function | Собирает единообразное определение function tool с JSON Schema и запретом лишних аргументов.
ExtensionService | Владелец публичного реестра tools/пакетов/навыков/MCP и отдельного хранилища токенов в памяти.
ExtensionService.save | Атомарно пишет публичное состояние без токенов и API-ключей.
ExtensionService.skills | Объединяет метаданные встроенных SKILL.md и ограниченные пользовательские JSON-инструкции с переключателями.
ExtensionService.catalog | Возвращает GUI наборы, инструменты, навыки, пакеты и MCP; секрет не возвращается, доступен только has_token.
ExtensionService.configure | Проверяет и применяет конкретное действие переключения/редактирования, не предоставляя модели универсальное изменение настроек.
ExtensionService._save_skill | Проверяет длины и ID; создаёт пользовательскую инструкцию или новый выключенный черновик опыта модели.
ExtensionService.import_plugin | Валидирует ограниченный декларативный пакет до записи; импортирует выключенные навыки/серверы без произвольного кода.
ExtensionService.discover_server | Подключается к MCP, получает схемы, назначает уникальные псевдонимы и отвергает устаревший результат при смене настроек.
ExtensionService.snapshot | Фиксирует разрешения одного запуска и каталог метаданных навыков; тела инструкций в prompt не подставляются заранее.
ExtensionService.execute | Повторно проверяет разрешение, обслуживает skills и MCP, валидирует схему и запрашивает отдельное подтверждение внешнего действия.
''')
register('core/python/task_service.py','''
TaskService._approve_external | Ждёт отдельное решение MCP/команды, проверяет актуальный запуск и поддерживает отмену независимо от файлового apply_all.
''')
register('core/python/bridge.py','''
''')
register('tests/fixtures/mcp_echo.py','''
add | MCP fixture складывает два целых числа, чтобы проверка транспорта не затрагивала файлы и внешние сервисы.
wait_seconds | Отложенный MCP ответ для проверки отмены и закрытия соединения.
''')
SYMBOL_NOTES['tools/generate_brand_icons.py:main']='Рендерит SVG в 512px PNG и записывает ICO directory/PNG-кадры семи разрешений для Windows.'
for _file,_name,_description in [
 ('tests/test_companion_policy.py','CompanionPolicyTests','Проверки coding-only намерения и чистого текста Лолы.'),
 ('tests/test_neutral_conversations.py','NeutralConversationTests','Изолированное временное хранилище проектов и чатов для мутаций/экспорта.'),
 ('tests/test_neutral_extensions.py','NeutralExtensionsTests','Проверки реестра и настоящих локальных MCP соединений.'),
 ('tests/test_project_command.py','ProjectCommandTests','Проверки подтверждения и жизненного цикла собственного тестового процесса.'),
 ('tests/test_responses_adapter.py','ResponsesHandler','HTTP/SSE фикстура Responses без платных API вызовов.'),
 ('tests/test_responses_adapter.py','ResponsesAdapterTests','Проверки канонической истории, потоковых functions, reasoning, probe и retry.'),
]:SYMBOL_NOTES[_file+':'+_name]=_description
SYMBOL_NOTES['tests/test_project_command.py:ProjectCommandTests.test_success_and_nonzero_exit_are_observable.approve']='Сохраняет предложение команды и подтверждает только тестовый запуск для проверки формы approval.'
TEST_PURPOSES.update({
 'chat_without_project_has_only_extension_tools_and_separate_history':'Chat получает только разрешённые нефайловые расширения, сохраняет отдельную историю и не пишет проект.',
 'only_coding_requests_can_delegate':'Кодирование допускается к делегированию, обычные вопросы, музыка, бытовые коды и функции устройств исключаются.',
 'speech_removes_markdown_preserving_words_and_math':'Разметка/код не озвучиваются, читаемые слова и числовое умножение сохраняются.',
 'internal_reasoning_is_not_spoken':'Закрытые think-теги удаляются из голоса и видимого итогового текста.',
 'project_instructions_and_chat_move_preserve_canonical_messages':'Перемещение меняет пространство без потери сообщений; поиск и доступ проверяют группу/режим.',
 'pin_archive_delete_and_explicit_confirmation':'Закрепление и архив видны в индексе; удаление требует подтверждения и убирает только выбранный чат.',
 'fork_and_retry_never_reuse_checkpoint_or_change_original':'Новая ветка имеет новый ID и не наследует checkpoint; исходная история сохраняется.',
 'exports_and_search_keep_modes_isolated':'Экспорт сохраняет нужные сообщения, поиск Chat не раскрывает отдельную историю Лолы.',
 'profiles_strip_secrets_and_validate_protocol':'Профили сохраняют Responses-настройки без ключа и отклоняют credentials в URL.',
 'disabled_tools_and_groups_are_enforced_and_snapshot_is_frozen':'Отключённые tools недоступны следующему запуску; прежний снимок не изменяется задним числом.',
 'generated_skill_is_reviewable_draft_and_lazy_loaded_after_enable':'Опыт создаётся выключенным, после включения читается по запросу, body не включается в каталог prompt.',
 'learning_toggle_and_plugin_validation':'Выключение обучения убирает create_skill, пакет не ссылается на неизвестный tool и включается явно.',
 'mcp_stdio_discovery_call_confirmation_and_cancellation':'Настоящий stdio SDK проходит discovery, отказ, проверку JSON Schema, вызов и отмену ожидания.',
 'server_url_does_not_store_credentials_and_change_invalidates_tools':'MCP URL с паролем отклоняется, токен не записывается и сбрасывается при смене адреса.',
 'mcp_streamable_http_discovers_and_calls_real_server':'Официальный локальный Streamable HTTP сервер отдаёт схемы и выполняет подтверждённый tool.',
 'progress_guard_detects_alternation_but_allows_changing_results':'Чередующийся A/B цикл останавливается по повтору результата; новый результат считается продвижением.',
 'rejected_command_never_executes_and_scope_cannot_escape':'Отказ не создаёт файл и cwd вне корня не допускается.',
 'success_and_nonzero_exit_are_observable':'Запуск показывает точное предложение, возвращает Unicode-вывод и различает exit 0/7.',
 'output_is_bounded_and_cancellation_stops_child':'Объём stdout ограничен 64 КБ, отмена быстро завершает собственный процесс.',
 'streaming_tools_and_reasoning_are_carried_between_calls':'Responses functions собираются из delta, output и зашифрованный reasoning передаются в следующий turn.',
 'nonstream_probe_uses_responses_and_retry_is_before_stream':'Временный 503 повторяется до потока, probe и нестриминговое завершение используют Responses.',
 'transcript_conversion_does_not_send_unknown_chat_metadata':'В API уходят только поля протокола, неизвестные локальные метаданные не передаются.',
})
TS_NOTES.update({
 'listWorkspaces':'Получает список пространств через ограниченный preload IPC.',
 'saveWorkspace':'Передаёт создание/изменение имени, папки и инструкций проекта.',
 'selectWorkspace':'Переключает пространство и его папку после проверок текущего состояния.',
 'deleteWorkspace':'Удаляет подтверждённую группу с сохранением разговоров и файлов.',
 'searchChats':'Запрашивает поиск названий/сообщений внутри режима, проекта и архива.',
 'updateChat':'Меняет закрепление, архив или проект выбранного разговора.',
 'deleteChat':'Передаёт подтверждённое удаление конкретного чата.',
 'forkChat':'Создаёт независимую копию или подготавливает повтор в новой ветке.',
 'exportChat':'Получает Markdown/JSON и открывает системное окно сохранения в main.',
 'listExtensions':'Получает публичный каталог возможностей без секретов.',
 'configureExtensions':'Передаёт конкретное действие настройки реестра в Core.',
 'discoverMcp':'Запускает асинхронное подключение MCP и получение схем tools.',
 'listConnections':'Читает именованные публичные профили модели.',
 'saveConnection':'Сохраняет профиль API без секретного ключа.',
 'deleteConnection':'Удаляет один выбранный публичный профиль.',
 'importPlugin':'Открывает системный выбор ограниченного JSON манифеста.',
 'pickWorkspaceFolder':'Выбирает папку для проекта без немедленного переключения текущего корня.',
 'apps/desktop/src/App.tsx:App.resetConversation':'Сбрасывает UI-ссылки на чат/запуск, сообщения, checkpoint, approval и ввод.',
 'apps/desktop/src/App.tsx:App.switchWorkspace':'Проверяет активность/черновики, переключает группу в Core и обновляет редактор, папку и историю.',
 'apps/desktop/src/App.tsx:App.openFork':'Открывает возвращённую копию, очищает checkpoint и подставляет запрос повтора во ввод.',
 'BrandMark':'Рисует согласованный с темой знак Neutral с точкой равновесия.',
 'ConnectionProfiles':'Показывает сохранённые подключения, имя профиля и действия сохранения/удаления.',
 'apps/desktop/src/ConnectionProfiles.tsx:ConnectionProfiles.remove':'Удаляет подтверждённый профиль и обновляет список без смены активной модели.',
 'apps/desktop/src/ConversationSidebar.tsx:Project':'Публичные поля пространства: ID, имя, папка и инструкции.',
 'apps/desktop/src/ConversationSidebar.tsx:Conversation':'Метаданные строки истории, фрагмент поиска и флаги pin/archive.',
 'apps/desktop/src/ConversationSidebar.tsx:Props':'Контракт sidebar с App: выбранный режим/проект, callbacks открытия, сброса, копии и ошибок.',
 'ConversationSidebar':'Управляет проектами и scoped-историей через конкретные preload методы.',
 'apps/desktop/src/ConversationSidebar.tsx:ConversationSidebar.run':'Сериализует GUI-действие, выводит ошибку и обновляет каталог после успеха.',
 'apps/desktop/src/ConversationSidebar.tsx:ConversationSidebar.update':'Применяет флаги/перемещение и сбрасывает активный чат при выходе из текущего списка.',
 'apps/desktop/src/ConversationSidebar.tsx:ConversationSidebar.saveProject':'Сохраняет форму проекта и переключает приложение на созданное/изменённое пространство.',
 'apps/desktop/src/ConversationSidebar.tsx:ConversationSidebar.remove':'Выполняет явно подтверждённое удаление чата/группы и обновляет активный выбор.',
 'apps/desktop/src/ExtensionsSettings.tsx:Skill':'Публичная инструкция навыка, происхождение и состояние включения.',
 'ExtensionsSettings':'Интерфейс пакетов, групп, tools, навыков, MCP подключения/проверки и подтверждения удаления.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.run':'Ограничивает одновременные операции и перечитывает публичный реестр после успеха.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.toggle':'Отправляет переключение конкретной возможности через валидируемый Core метод.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.includes':'Локально фильтрует название/описание по строке поиска расширений.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.saveSkill':'Сохраняет пользовательскую инструкцию, оставляя явное включение отдельным действием.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.saveServer':'Преобразует строки аргументов в массив и сохраняет MCP публично, токен передаётся отдельно.',
 'VoiceSettings':'Общая настройка голоса/громкости/скорости Лолы и её расширенного профиля.',
 'Welcome':'Пустое состояние с брендом, примерами ввода и переходом в IDE.',
 'plainVoiceText':'Удаляет разметку из потокового отображения и текста для TTS без исполнения HTML.',
 'tests/electron/neutral-smoke.cjs:BrowserWindow.prototype.loadURL':'Открывает собранный renderer вместо пользовательского Vite, изолируя GUI-проверку.',
 'tests/electron/neutral-smoke.cjs:dialog.showSaveDialog':'Выбирает только тестовый путь экспорта без системного диалога пользователю.',
 'tests/electron/neutral-smoke.cjs:js':'Выполняет renderer-шаг, даёт React завершить обновление и добавляет код к ошибке.',
 'tests/electron/neutral-smoke.cjs:click':'Нажимает выбранный DOM-контрол через реальный renderer.',
 'tests/electron/neutral-smoke.cjs:textButton':'Находит кнопку в заданной области по точному видимому тексту.',
 'tests/electron/neutral-smoke.cjs:input':'Изменяет native input/textarea и посылает React input event.',
 'tests/electron/neutral-smoke.cjs:capture':'Сохраняет screenshot и геометрию основных панелей для визуальной проверки.',
 'tests/electron/neutral-smoke.cjs:finish':'Пишет итог и диагностику ошибки, закрывает только тестовое приложение и HTTP fixture.',
})

TS_NOTES['tests/electron/smoke.cjs:BrowserWindow.prototype.loadURL']='Открывает готовый renderer из dist, чтобы полная проверка редактора и голоса не зависела от пользовательского Vite.'

TEST_PURPOSES['lola_uses_her_own_responses_protocol_and_tools']='Лола использует собственный Responses endpoint, вызывает калькулятор и сохраняет чистый ответ независимо от основной конфигурации.'

FILE_NOTES['tools/audit_core_20261025.py']='Изолированные воспроизведения аудита Neutral 7: синтетические ответы модели и временные файлы, без изменения продукта или пользовательских данных.'
SYMBOL_NOTES.update({
 'tools/audit_core_20261025.py:chunk':'Создаёт синтетическое событие потока с явной причиной завершения для аудита.',
 'tools/audit_core_20261025.py:tool':'Создаёт синтетические аргументы вызова инструмента без его исполнения.',
 'tools/audit_core_20261025.py:Stream':'Минимальный поток заранее заданных событий, без сетевого соединения.',
 'tools/audit_core_20261025.py:Stream.__iter__':'Возвращает подготовленные события аудиторской фикстуры.',
 'tools/audit_core_20261025.py:Stream.close':'Имитирует закрытие потока; внешних ресурсов фикстура не создаёт.',
 'tools/audit_core_20261025.py:engine_probe':'Запускает настоящий движок с синтетическим клиентом и временным TaskStore; возвращает статус, ошибки и использование verifier.',
 'tools/audit_core_20261025.py:engine_probe.Client':'Изолированный клиент фикстуры; ответы получаются из списка без HTTP.',
 'tools/audit_core_20261025.py:engine_probe.Client.create':'Выдаёт следующий поток или положительный ответ фиктивной LLM-проверки, проверяя доверие движка к нему.',
 'tools/audit_core_20261025.py:engine_probe.Client.close':'Завершает фиктивный клиент без внешних ресурсов.',
 'tools/audit_core_20261025.py:main':'Собирает наблюдения о завершении, сжатии, восстановлении, схемах, MCP ID и endpoint credentials; выводит JSON, не объявляя найденные ошибки корректными.',
})

FILE_NOTES.update({
 'tests/test_core_reliability.py':'Регрессии первого этапа аудита: завершение, отказ, аргументы, свидетельства команд, runtime и привязка ключей к endpoint; модель заменена локальной фикстурой.',
 'tests/test_mcp_reliability.py':'Регрессии идентичности MCP, миграции выключенных инструментов, единственной отменяемой discovery и настоящего медленного stdio сервера.',
})
SYMBOL_NOTES.update({
 'agent/engine.py:AgentEngine._expire_runtime':'Отмечает истечение общего срока и запускает существующий путь отмены HTTP, tools и ожидания подтверждения.',
 'agent/engine.py:AgentEngine.interruption_reason':'Различает сообщение об истечении срока задачи и об остановке пользователем.',
 'agent/tools.py:validate_tool_arguments':'Проверяет JSON-объект по объявленной схеме до вызова любого инструмента; ошибка называет поле и правило без значений аргументов.',
 'agent/verifier.py:StageVerifier.record_command':'Сохраняет ограниченные метаданные результата команды; повтор той же программы с аргументами и cwd заменяет её прежний исход.',
 'agent/verifier.py:StageVerifier.command_summary':'Различает отсутствие проверок, провал команды и успешные команды; не объявляет все требования задачи автоматически проверенными.',
 'agent/model_preferences.py:connection_key':'Привязывает ключ к адресу сервиса: прежний либо явно повторённый старый ключ не переносится на новый endpoint.',
 'agent/smart_context.py:_mcp_text':'Извлекает текст до 30 блоков MCP; не включает бинарные изображения, аудио и resource payload.',
 'agent/smart_context.py:_bounded_tool_json':'Уменьшает детали сжатого результата до фактического размера JSON, сохраняя коды и статус исхода.',
 'core/python/extension_service.py:mcp_alias':'Строит допустимое имя tools из полного server ID, transport endpoint и имени действия, предотвращая совпадения общих префиксов.',
 'core/python/extension_service.py:ExtensionService._migrate_aliases':'В памяти переводит старые MCP aliases и ссылки плагинов; явное выключение сохраняется для каждого нового имени.',
 'core/python/extension_service.py:ExtensionService._reserve_discovery':'Под блокировкой резервирует одну проверку сервера до создания worker и получает копию настроек с cancellation Event.',
 'core/python/extension_service.py:ExtensionService._release_discovery':'Освобождает только принадлежащую конкретному worker резервацию discovery.',
 'core/python/extension_service.py:ExtensionService.start_discovery':'Запускает одну асинхронную проверку MCP с callback исходного RPC запроса; повтор до окончания отклоняется.',
 'core/python/extension_service.py:ExtensionService.start_discovery.run_discovery':'Получает результат discovery, освобождает резервацию и отвечает исходному клиенту.',
 'core/python/extension_service.py:ExtensionService.cancel_discovery':'Сигнализирует отмену одной или всех проверок MCP без запуска нового процесса.',
 'core/python/extension_service.py:ExtensionService.shutdown':'Закрывает приём discovery, отменяет текущие проверки и ограниченно ожидает их workers.',
 'core/python/extension_service.py:ExtensionService._discover_server':'Получает реальные схемы, проверяет уникальные имена и актуальность настроек; отменённый или устаревший каталог не публикуется.',
 'tests/test_core_reliability.py:delta':'Создаёт событие фиктивного модельного потока с текстом, calls, refusal и finish_reason.',
 'tests/test_core_reliability.py:call':'Создаёт фиктивный вызов инструмента с JSON-аргументами и стабильным call ID.',
 'tests/test_core_reliability.py:Stream':'Итерируемый поток заранее заданных ответов без HTTP и ресурсов.',
 'tests/test_core_reliability.py:Stream.__iter__':'Возвращает события фикстуры в исходном порядке.',
 'tests/test_core_reliability.py:Stream.close':'Совместимое закрытие фиктивного потока без внешних ресурсов.',
 'tests/test_core_reliability.py:CoreReliabilityTests':'Проверяет настоящий AgentEngine и настройки на временном TaskStore и синтетическом ModelClient.',
 'tests/test_core_reliability.py:CoreReliabilityTests.run_engine':'Запускает движок с заранее заданными ответами, собирает историю/события и проверяет отсутствие аварийного failed.',
 'tests/test_core_reliability.py:CoreReliabilityTests.run_engine.Client':'Фиктивный клиент с ограниченной последовательностью потоков и положительным ответом необязательной LLM-проверки.',
 'tests/test_core_reliability.py:CoreReliabilityTests.run_engine.Client.create':'Возвращает следующий поток либо фиксированную проверку завершения без HTTP.',
 'tests/test_core_reliability.py:CoreReliabilityTests.run_engine.Client.close':'Завершает фиктивный клиент без сетевых действий.',
 'tests/test_core_reliability.py:CoreReliabilityTests.run_engine.Client.cancel':'Совместимый метод отмены клиента; сам движок проверяет Event прерывания.',
 'tests/test_core_reliability.py:CoreReliabilityTests.test_runtime_expiry_interrupts_an_outstanding_approval.expire_at_approval':'Имитирует истечение срока ровно при запросе подтверждения и вызывает настоящий обработчик ожидания.',
 'tests/test_mcp_reliability.py:MCPReliabilityTests':'Проверяет service/transport MCP в изолированном каталоге; закрывает все discovery после каждого теста.',
 'tests/test_mcp_reliability.py:MCPReliabilityTests.add_server':'Сохраняет явно настроенный сервер фикстуры и возвращает его публичную запись.',
 'tests/test_mcp_reliability.py:MCPReliabilityTests.test_single_discovery_is_cancellable_and_does_not_publish_late_tools.operation':'Удерживает фиктивное discovery до cancellation, затем возвращает опоздавшие схемы для проверки их отклонения.',
 'tests/test_mcp_reliability.py:MCPReliabilityTests.test_shutdown_cancels_workers_and_rejects_new_discovery.operation':'Имитирует работу транспорта до отмены при shutdown сервиса.',
})
TEST_PURPOSES.update({
 'truncated_answer_is_saved_and_paused':'оборванный лимитом текст сохраняется, задача приостанавливается и получает причину length',
 'truncated_native_tool_is_never_executed':'инструмент не исполняется даже при завершённом JSON, если сервер сообщил length',
 'native_refusal_is_visible_and_not_completed':'нативный отказ виден в истории и не превращается в успешное завершение',
 'malformed_write_returns_error_and_allows_model_repair':'path=null возвращает ошибку tool, после которой модель продолжает отвечать',
 'preview_io_error_is_a_tool_result_not_a_failed_run':'ошибка диска при подготовке diff возвращается модели без аварии всего запуска',
 'failed_command_cannot_be_overruled_by_final_answer':'exit 7 сохраняется и блокирует completed несмотря на положительный текст модели',
 'successful_retry_of_same_command_resolves_failed_evidence':'успешный повтор той же команды заменяет прежний провал',
 'unrelated_success_does_not_erase_failed_command':'успех другой команды не стирает провал обязательной проверки',
 'answer_without_commands_is_explicitly_unverified':'ответ без выполненных команд получает явное not_run и сообщение о неподтверждённой проверке',
 'runtime_uses_one_minute_and_timer_is_always_cancelled':'лимит в одну минуту не повышается до пяти, а таймер закрывается после задачи',
 'runtime_expiry_interrupts_an_outstanding_approval':'истечение срока прерывает ожидание diff, сохраняет задачу и не записывает файл',
 'json_truncation_does_not_parse_or_execute_complete_prefix':'JSON-адаптер сохраняет length и не исполняет полный-looking JSON-префикс оборванного ответа',
 'responses_incomplete_and_refusal_are_not_cached_as_success':'Responses incomplete/refusal сохраняют причину остановки без кэширования успешного tool output',
 'endpoint_change_clears_omitted_or_stale_model_and_stt_keys':'смена адреса Лолы/STT очищает отсутствующий или явно повторённый старый ключ без его записи на диск',
 'key_is_retained_for_same_endpoint_and_fresh_key_for_new_endpoint':'ключ сохраняется для прежнего сервера, а новый адрес принимает новый введённый ключ',
 'full_endpoint_alias_separates_long_prefixes_and_connections':'общий префикс ID и одинаковые имена tools не смешивают серверы и соединения',
 'migrate_legacy_collision_preserves_disabled_tools_and_plugin_links':'старые aliases мигрируют со ссылками плагинов и сохраняют явные выключения',
 'duplicate_names_are_rejected_before_overwriting_previous_catalog':'повторяющиеся имена MCP не перезаписывают прежний корректный каталог',
 'single_discovery_is_cancellable_and_does_not_publish_late_tools':'одна discovery на сервер отменяется, её опоздавшие схемы не включаются',
 'shutdown_cancels_workers_and_rejects_new_discovery':'закрытие сервиса отменяет worker и запрещает новые проверки',
 'real_stdio_discovery_can_finish_after_old_ten_second_deadline':'настоящий stdio сервер с задержкой запуска 11 секунд успешно возвращает инструменты',
 'command_compaction_keeps_exit_code_and_failure_evidence':'сжатие команды сохраняет exit code и фрагменты stdout/stderr с причиной провала',
 'mcp_compaction_keeps_text_blocks_and_excludes_binary_content':'сжатие MCP сохраняет значимые текстовые блоки и исключает бинарные данные',
 'single_line_output_keeps_diagnostic_beyond_prefix':'ошибка в конце длинной строки не теряется при выборе диагностического фрагмента',
 'compacted_json_honors_escaping_budget_and_outcome_metadata':'фактический JSON-size после escaping укладывается в бюджет и сохраняет outcome',
 'compaction_preserves_note_privacy_and_canonical_result_reference':'сжатие заметок сохраняет приватность и ссылку на канонический tool call',
 'archived_command_keeps_failure_summary_and_call_reference':'архив истории содержит краткую ошибку команды, код выхода и call ID',
})
TS_NOTES.update({
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.discoverServer':'Показывает ожидание конкретного MCP сервера, получает каталог и сбрасывает состояние после ответа исходного запроса.',
 'apps/desktop/src/ExtensionsSettings.tsx:ExtensionsSettings.cancelDiscovery':'Отменяет проверку MCP через отдельный IPC без создания повторной discovery.',
 'cancelMcpDiscovery':'Явный preload API отмены проверки MCP: передаёт ID сервера в ограниченный IPC обработчик main/Core.',
})

FILE_NOTES.update({
 'agent/run_state.py':'Проверяемый жизненный цикл запуска с совместимой проекцией legacy status; этапы плана хранятся независимо.',
 'agent/call_journal.py':'Долговечный JSONL-журнал вызовов с fsync, квитанциями результатов и консервативным восстановлением истории.',
 'agent/tool_executor.py':'Единая валидация разрешённых tools, границы начала побочных эффектов, diff approval и сохранение результатов до публикации.',
 'agent/tool_recovery.py':'Сверка журнала с канонической историей, восстановление свидетельств и ограниченных метаданных интерфейса.',
 'tests/test_run_state.py':'Контракты переходов между выполнением, подтверждением, проверкой и терминальными состояниями.',
 'tests/test_call_journal.py':'Регрессии долговечного журнала: pairing, receipts, повреждения, конфликты, идентичность пачек и ручные решения.',
 'tests/test_tool_execution.py':'Fault-injection исполнения: реальные остановки процессов, запрет повторения эффектов, сохранение успехов и ручное восстановление.',
})

FILE_NOTES.update({
 'agent/request_budget.py':'Автоматическое/ручное размещение окончательного Chat/JSON/Responses запроса: tokenizer/оценка, ответ, каталог schemas и компактные квитанции выполненного кода без изменения истории.',
 'agent/context_tools.py':'Безопасное чтение диапазонов сохранённых результатов и поиск включённых MCP без исполнения внешних действий.',
 'apps/desktop/src/ContextUsage.tsx':'Карточка оценки полного контекста, состава входа, отложенных MCP-схем и фактического usage сервера.',
 'tests/test_request_budget.py':'Регрессии окон 4K/8K/32K, JSON/Responses, больших схем, неизменности кода, стабильных references, lazy MCP и usage через локальный HTTP.',
})
SYMBOL_NOTES.update({
 'agent/request_budget.py:BudgetExceededError':'Управляемая остановка: обязательные данные не помещаются в настроенное окно без изменения.',
 'agent/request_budget.py:json_bytes':'Измеряет байты конечного UTF-8 JSON для диагностики транспорта; байт не считается токеном.',
 'agent/request_budget.py:prepare_model_request':'Убирает внутренние source markers и применяет ровно те же JSON-tool/Responses адаптеры, что и реальный транспорт; telemetry включается до измерения.',
 'agent/request_budget.py:RequestBudget':'Подбирает проекцию под фактическое окно с SDK tokenizer либо языковой оценкой, framing, запасом и обратной связью usage.',
 'agent/request_budget.py:RequestBudget.measure':'Считает инструкции, историю, schemas и protocol, включая encrypted Responses items и JSON escaping; возвращает свободный остаток и fits/blocked.',
 'agent/request_budget.py:RequestBudget.check':'Последний gate перед транспортом; при превышении бросает BudgetExceededError без HTTP.',
 'agent/request_budget.py:RequestBudget.explanation':'Формирует объяснение превышения окна с величинами входа, ответа и запаса без содержимого пользовательских данных.',
 'agent/request_budget.py:RequestBudget.fit':'На копиях подбирает ответ, schemas и историю; в auto архивирует большие уже завершённые writes, сохраняя текущий запрос и невыполненные calls.',
 'agent/context_tools.py:find_mcp_tools':'Ищет по коротким ключевым словам в разрешённом snapshot MCP и возвращает ограниченные aliases без исполнения.',
 'agent/context_tools.py:read_saved_result':'Проверяет индекс и call ID только в текущем чате; возвращает диапазон символов, hash и next_offset без повторного запуска исходного действия.',
 'agent/model_client.py:ModelClient.record_usage':'Принимает только корректные неотрицательные input/output usage сервера; факт расхода хранится отдельно от оценки бюджета.',
 'agent/engine.py:AgentEngine._dispatch_tool':'Обрабатывает readers/discovery локально, подключает выбранные MCP schemas к следующему ходу и делегирует остальные tools прежнему handler.',
 'agent/engine.py:AgentEngine._sync_usage':'Копирует агрегированный reported usage и число принятых модельных запросов в task без включения секретов.',
 'agent/engine.py:AgentEngine._model_create':'Проверяет полный адаптированный payload до client.create, сохраняет основной/вспомогательный бюджет и синхронизирует usage.',
 'agent/engine.py:AgentEngine._should_update_memory':'По умолчанию пропускает дополнительную LLM-память после read-only работы; учитывает успешную запись, просьбу запомнить и явный режим off/always.',
 'agent/context_manager.py:ContextManager.build':'Добавляет stable source markers, task/skills и причину сжатия к независимой проекции; исходная каноническая история не меняется.',
 'agent/model_client.py:ModelClient.create':'Применяет общий wire adapter и окончательный бюджет до HTTP; запускает native/JSON/Responses stream либо нестриминговое завершение с учётом usage.',
 'agent/model_client.py:ModelStream._produce':'Читает настоящий HTTP-поток в ограниченную очередь, переводит Responses и учитывает последнее накопительное usage один раз; закрывает транспорт при отмене.',
 'agent/model_client.py:ModelClient.request':'Повторяет временные ошибки только до ответа; при явном 400/422 для stream_options допускает fallback без необязательной telemetry, не повторяет частичный поток.',
 'tests/test_request_budget.py:definition':'Строит синтетическую JSON schema контролируемого размера для измерения overhead.',
})
TEST_PURPOSES.update({
 '4k_8k_32k_windows_fit_complete_native_and_json_payloads':'полный native/JSON payload помещается в окна 4K/8K/32K после сжатия без изменения текущего запроса',
 'large_russian_current_request_is_rejected_without_clipping':'длинный обязательный русский запрос сохраняется целиком и отклоняется до отправки',
 'schemas_and_json_protocol_overhead_are_included':'слишком большие schemas не обходят бюджет ни через native tools, ни через JSON-инструкции',
 'responses_encrypted_items_count_and_remain_intact':'encrypted reasoning включается в измерение, но не обрезается и не меняется',
 'write_arguments_are_preserved_or_rejected':'полный код write_file нельзя незаметно сократить ради окна модели',
 'result_reader_anchors_survive_two_compaction_passes':'канонический якорь результата сохраняется после char- и token-проекций; приватный marker не уходит в HTTP',
 'reader_checks_identity_and_reassembles_character_ranges':'диапазоны собирают исходный Unicode-текст, чужой индекс/ID не читается',
 'deferred_tools_require_discovery_and_are_bounded':'MCP недоступен policy до discovery; подключается ограниченный набор схем без их дублирования в результате поиска',
 'mcp_only_profile_still_exposes_discovery_without_full_schemas':'профиль с одними MCP и выключенными базовыми группами сохраняет доступ к discovery',
 'memory_update_defaults_skip_read_only_tasks':'обычное чтение не вызывает обновление памяти; write/off/always переключают правило явно',
 'legacy_large_reply_does_not_reset_endpoint_and_new_invalid_window_is_rejected':'старые настройки большого ответа сохраняют URL/model, новые противоречивые лимиты отклоняются',
 'real_transport_rejects_oversized_schemas_before_http':'настоящий ModelClient не отправляет HTTP при переполнении schemas',
 'reported_stream_usage_is_counted_once_per_response':'несколько накопительных usage в одном SSE ответе учитываются один раз',
 'optional_usage_rejection_falls_back_before_stream_only':'сервер без stream_options повторяется без telemetry только после отказа до начала потока',
 'engine_budget_pause_preserves_request_and_sends_no_http':'Engine сохраняет большой исходный запрос и paused/blocked, не вызывая сервер',
 'read_only_answer_skips_memory_request_and_exposes_reported_usage':'реальный read-only ответ делает один запрос, сохраняет настоящий usage и пропускает лишнюю LLM-память',
})
TS_NOTES.update({
 'RequestBudgetSnapshot':'Оценка окончательного входа, окна, ответа/запаса, breakdown и MCP-schema counts без сырых payload.',
 'ModelUsageSnapshot':'Сумма фактических input/output tokens и число запросов, для которых сервер прислал usage.',
 'ContextUsage':'Показывает состав контекста, резерв и причины сжатия отдельно от фактического reported usage.',
 'apps/desktop/src/ContextUsage.tsx:ContextUsage.number':'Форматирует значения токенов в русской локали без изменения бюджета.',
 'GenerationFields':'Показывает числовые лимиты, окно/резерв, пресеты 4K/8K/32K и явный режим обновления памяти.',
 'LocalRuntimePanel':'Управляет локальным GGUF и переносит endpoint, модель и настоящий ctx_size в черновик настроек без автоматического сохранения.',
})

FILE_NOTES.update({
 'agent/workspace_search.py':'Общий ограниченный поиск файлов/текста для модели и GUI: glob по сегментам пути, отмена, deadline и лимиты обхода/чтения.',
 'agent/workspace_read.py':'Чтение точных диапазонов UTF-8 со стабильной ревизией, отменой и явным отказом от обрезания длинной строки.',
 'agent/workspace_edits.py':'Preview и подтверждаемое применение patch/create-directory/rename/delete со snapshot, проверкой корня и восстановимыми метаданными.',
 'agent/project_instructions.py':'Ограниченное чтение AGENTS.md по иерархии выбранного пути; версии/области действия передаются модели и не расширяют права.',
 'core/python/project_search.py':'Асинхронный cancellable GUI worker над общим agent.workspace_search; самостоятельного второго алгоритма поиска нет.',
 'tests/test_workspace_tools.py':'Контракты нового набора IDE: диапазоны, newline, revisions, preview/approval, вложенные папки, rename/delete, отмена, AGENTS и journal recovery.',
 'tests/migration/test_workspace_workflow.py':'Настоящий локальный HTTP/SSE workflow создания и изменения проекта через пять отдельных согласий и scoped инструкции.',
})
SYMBOL_NOTES.pop('core/python/project_search.py:search_project',None)
SYMBOL_NOTES.pop('core/python/project_search.py:search_project.stop',None)
SYMBOL_NOTES.update({
 'agent/workspace_search.py:glob_matches':'Сопоставляет регистронезависимые сегменты glob; ** допускает ноль или несколько папок, * внутри сегмента не пересекает разделитель.',
 'agent/workspace_search.py:glob_matches.match':'С мемоизацией проверяет пару индексов пути/маски без экспоненциального обхода вариантов **.',
 'agent/workspace_search.py:search_project':'Выполняет один ограниченный обход для текстового поиска и glob; не следует ссылкам/junction, сообщает причину остановки и статистику.',
 'agent/workspace_search.py:search_project.stop':'Проверяет Event и монотонный deadline во время обхода и чтения строк.',
 'agent/workspace_edits.py:record_workspace_change':'Идемпотентно строит последние 100 workspace_changes из успешных квитанций, учитывает изменённые/перемещённые файлы без сырых содержимых.',
 'agent/workspace_edits.py:mutation_path':'Проверяет путь в выбранном корне и запрещает корень, .git и пути через ссылки/junction для новых изменений.',
 'agent/workspace_edits.py:file_revision':'Читает не более 1 МБ и сверяет inode/size/mtime до и после чтения; возвращает байты и SHA256 ревизии.',
 'agent/workspace_edits.py:parent_revision':'Получает identity каталога для обнаружения замены родителя между preview и apply.',
 'agent/workspace_edits.py:preview_mutation':'Готовит diff или список путей без изменения диска; привязывает аргументы, исходник и назначение к snapshot.',
 'agent/workspace_edits.py:apply_mutation':'Требует согласия и тот же snapshot, применяет одну операцию без замены назначения; после возможного частичного эффекта возвращает unknown вместо автоматического повтора.',
 'agent/workspace_read.py:read_range':'С отменой читает ограниченный UTF-8 источник, проверяет ревизию и возвращает целые строки/next_line/SHA256 без усечения текущей строки.',
 'agent/project_instructions.py:ProjectInstructions':'Хранит применимые scoped AGENTS.md, поколения их обновлений и ограниченный текст правил для system projection.',
 'agent/project_instructions.py:ProjectInstructions.refresh':'Перечитывает цепочку AGENTS.md от корня до папки пути, замечает добавление/удаление/смену hash и проверяет 8/16 КБ лимиты.',
 'agent/project_instructions.py:ProjectInstructions.render':'Показывает источники, области и полные прочитанные правила с приоритетом пользователя и без дополнительных разрешений.',
 'agent/project_instructions.py:ProjectInstructions.summary':'Возвращает только пути, области и hashes для компактного task и интерфейса.',
 'agent/tool_executor.py:ToolExecutor._mutate':'Объединяет правила проекта, preview, ожидание одноразового согласия, durable started и применение новых файловых операций.',
 'agent/engine.py:AgentEngine._instruction_guard':'Перед предложением и после согласия проверяет актуальность scoped правил; новые правила требуют следующего модельного запроса до эффекта.',
 'agent/tools.py:workspace_tool':'Создаёт строгие bounded JSON schemas нового набора IDE с явными обязательными полями.',
 'tests/test_workspace_tools.py:WorkspaceToolsTests.apply':'Применяет настоящий preview/snapshot в изолированном проекте для проверок побочных эффектов.',
 'tests/test_workspace_tools.py:WorkspaceToolsTests.test_partial_directory_cancel_is_unknown_and_not_rolled_back.CancelAfterFirst.is_set':'Имитирует отмену после создания первого каталога для проверки частичного исхода.',
 'tests/test_workspace_tools.py:WorkspaceToolsTests.test_search_cancels_while_scanning_rather_than_only_before_it.CancelDuringScan.is_set':'Выдаёт отмену после нескольких проверок внутри настоящего обхода.',
 'tests/test_workspace_tools.py:WorkspaceToolsTests.test_scoped_rules_are_loaded_before_mutation_and_refresh_after_change.Client.create':'Принимает модельную проекцию с подключёнными scoped правилами без HTTP и реальной LLM.',
 'tests/test_workspace_tools.py:WorkspaceToolsTests.test_exception_after_patch_is_unknown_not_a_replayable_failure.fail_after_effect':'Имитирует исключение после изменения файла, когда результат эффекта нельзя считать обычным отказом.',
})
TEST_PURPOSES.update({
 'range_preserves_crlf_line_numbers_and_full_revision':'диапазон сохраняет CRLF, номера строк и SHA256 всей ревизии',
 'range_reads_large_source_and_can_be_cancelled':'часть большого исходника читается без выдачи всего файла; отмена возвращается явно',
 'range_never_silently_truncates_one_long_line':'длинная строка не выдаётся как целая после скрытого обрезания',
 'patch_changes_one_fragment_preserving_other_bytes':'точечная правка меняет один фрагмент и сохраняет остальные байты/CRLF; snapshot переживает JSON roundtrip',
 'ambiguous_or_missing_patch_does_not_modify_file':'ноль или несколько совпадений не дают произвольную замену',
 'patch_requires_approval_and_refuses_changed_revision':'без согласия запись запрещена, ручная правка после preview сохраняется',
 'read_revision_can_be_bound_before_preview':'ожидаемый hash из read_range отклоняет устаревшее предложение ещё до diff',
 'nested_directory_creation_and_existing_directory':'вложенные папки создаются только после preview; существующий каталог не меняется',
 'new_file_can_be_created_after_explicit_directory_tool':'новая вложенная структура создаётся через разрешённые операции без shell',
 'partial_directory_cancel_is_unknown_and_not_rolled_back':'частично созданная цепочка не удаляется молча и требует проверки результата',
 'rename_never_overwrites_destination':'существующее или появившееся назначение не затирается',
 'rename_and_delete_have_distinct_previews_and_results':'перенос и удаление показывают разные намерения и возвращают структурированные квитанции',
 'root_outside_and_recursive_directory_deletion_are_denied':'корень, внешние пути, .git и рекурсивное удаление недоступны новым операциям',
 'glob_and_text_search_share_bounds_and_cancellation':'GUI/model используют один поиск, **/* работает по сегментам, лимиты и отмена действуют в tools',
 'search_cancels_while_scanning_rather_than_only_before_it':'поиск останавливается уже в процессе обхода, не только при входе',
 'scoped_rules_are_loaded_before_mutation_and_refresh_after_change':'вложенные правила доходят до модели перед согласием; их смена блокирует прежнее предложение',
 'instructions_are_bounded_and_do_not_expand_root':'AGENTS.md не расширяет корень и не обрезается при превышении ограничения',
 'receipt_recovers_workspace_change_without_repeating_patch':'журнал восстанавливает метаданные patch без повторной записи файла',
 'exception_after_patch_is_unknown_not_a_replayable_failure':'исключение после побочного эффекта остаётся unknown и блокирует автоматический повтор',
 'agent_creates_and_changes_nested_project_through_fresh_approvals':'реальный HTTP/SSE-агент учитывает scoped правила, создаёт структуру, читает/правит/перемещает/удаляет с пятью свежими согласиями',
 'cancel_with_assistant_commentary_is_paused':'отмена предложения не становится completed даже при промежуточном тексте модели',
})
TS_NOTES.update({
 'apps/desktop/src/App.tsx:App.closeProgress':'Скрывает подробности без отмены задачи и при X/Escape возвращает фокус переключателю.',
 'apps/desktop/src/App.tsx:App.dismissProgress':'Обрабатывает Escape и pointerdown вне панели; уважает уже обработанные события и модальные диалоги.',
 'tests/electron/neutral-smoke.cjs:done':'В локальной HTTP-фикстуре проверяет успешную квитанцию конкретного шага создания каталога, файла и patch.',
 'tests/electron/neutral-smoke.cjs:releaseStage4':'Завершает удерживаемый SSE-поток только после проверки, что закрытие подробностей не остановило задачу.',
})
SYMBOL_NOTES['tests/test_workspace_tools.py:WorkspaceToolsTests.test_write_batch_permission_does_not_authorize_delete.reject_delete']='Отклоняет новое удаление через настоящий approval hook, проверяя независимость от прежнего apply_all для write_file.'
TEST_PURPOSES['write_batch_permission_does_not_authorize_delete']='разрешение пакета write_file не распространяется на новое удаление, которое получает отдельный preview и решение'
SYMBOL_NOTES.update({
 'agent/run_state.py:InvalidRunStateTransition':'Ошибка неизвестного состояния или недопустимого перехода; исходный task не меняется.',
 'agent/run_state.py:RunState':'Единственный контроллер поля run_state; поддерживает прежний status и не меняет содержательные этапы плана.',
 'agent/run_state.py:RunState.phase':'Читает актуальную фазу из общего task, чтобы два адаптера не пользовались устаревшей копией.',
 'agent/run_state.py:RunState._validate_phase':'Отклоняет неизвестную фазу до изменения словаря задачи.',
 'agent/run_state.py:RunState._legacy_status':'Преобразует активные фазы в running, завершение в completed, остановки в paused.',
 'agent/run_state.py:RunState.transition':'Проверяет матрицу переходов, обновляет reason/event, очищает причину при возобновлении и запрещает открывать completed заново.',
 'agent/call_journal.py:_unknown':'Распознаёт неопределённый исход по коду или явному флагу результата.',
 'agent/call_journal.py:_placeholder':'Отличает синтетические записи восстановления от настоящих квитанций инструмента.',
 'agent/call_journal.py:_replaceable':'Разрешает заменять только отсутствующий, неизвестный либо синтетический результат.',
 'agent/call_journal.py:_index':'Проверяет неотрицательный целочисленный якорь; bool не считается индексом.',
 'agent/call_journal.py:_canonical_calls':'Нормализует имена, call IDs и исходные JSON-строки; дубликаты внутри пачки и неверная форма отклоняются.',
 'agent/call_journal.py:_resolution_result':'Создаёт помеченное наблюдение пользователя; оно не выдумывает исходный вывод инструмента.',
 'agent/call_journal.py:CallJournal':'Хранит вызовы одной эпохи задачи; якорь сообщения плюс call ID различают повторяющиеся IDs модели.',
 'agent/call_journal.py:CallJournal._read':'Читает ограниченные строки, проверяет version/identity; оборванный хвост допускается, повреждённая полная строка останавливает восстановление.',
 'agent/call_journal.py:CallJournal._state':'Воспроизводит события в пачки и состояния вызовов, проверяя пересечения и монотонность фаз.',
 'agent/call_journal.py:CallJournal._call_state':'Находит вызов строго по сохранённому якорю и ID либо отклоняет чужую идентичность.',
 'agent/call_journal.py:CallJournal._unresolved_state':'Выделяет начатые эффекты без квитанции и результаты OUTCOME_UNKNOWN, ещё не проверенные человеком.',
 'agent/call_journal.py:CallJournal._append':'Проверяет конечный JSON и размер, исправляет оборванный хвост, выполняет flush/fsync перед возвратом.',
 'agent/call_journal.py:CallJournal.prepare_batch':'Долговечно записывает полную пачку до любого исполнения; повтор той же пачки идемпотентен.',
 'agent/call_journal.py:CallJournal.set_phase':'Сохраняет prepared/awaiting_approval/started; запрещает откат фазы и изменение класса уже начатого эффекта.',
 'agent/call_journal.py:CallJournal.record_result':'Сохраняет настоящую квитанцию до контекста/UI; известный результат нельзя заменить другим.',
 'agent/call_journal.py:CallJournal.entries':'Возвращает независимые копии вызовов с фазами, аргументами, квитанциями и ручными решениями.',
 'agent/call_journal.py:CallJournal.delete_chat':'Удаляет только файлы журналов указанного чата с проверкой идентичности и вычисленного имени.',
 'agent/call_journal.py:CallJournal.unresolved':'Возвращает список эффектов, которые требуют проверки пользователем перед продолжением.',
 'agent/call_journal.py:CallJournal.resolve':'Долговечно сохраняет явное completed/not_executed для неизвестного эффекта; инструмент не запускается.',
 'agent/call_journal.py:CallJournal._missing_result':'Различает не начатый вызов, прерванное чтение и неизвестный начатый эффект.',
 'agent/call_journal.py:CallJournal.recover':'Сначала проверяет все якоря на копии истории, затем восстанавливает полные пары, сохраняет настоящие receipts и возвращает нерешённые эффекты.',
 'agent/tool_executor.py:ToolPolicy':'Снимок разрешённых определений для одного запуска с schema validation и консервативной классификацией эффекта.',
 'agent/tool_executor.py:ToolPolicy.validate':'Проверяет имя, JSON-аргументы и объявленную схему до вызова обработчика.',
 'agent/tool_executor.py:ToolPolicy.effectful':'Считает только фиксированный список встроенных readers безопасным для повтора; неизвестные и MCP tools считаются эффектами.',
 'agent/tool_executor.py:ToolExecutor':'Координирует policy, lifecycle, согласия и durable receipts; engine управляет модельным циклом.',
 'agent/tool_executor.py:ToolExecutor.prepare_batch':'Записывает пачку в журнал и закрепляет канонический индекс для её вызовов.',
 'agent/tool_executor.py:ToolExecutor._phase':'Сначала сохраняет фазу, затем обновляет bounded activity/checkpoint; эффект начинается только после возврата.',
 'agent/tool_executor.py:ToolExecutor.before_external_approval':'Переводит команду или подтверждаемый MCP в ожидание и долговечно отмечает отсутствие исполнения.',
 'agent/tool_executor.py:ToolExecutor.after_external_approval':'После согласия сохраняет started до возврата внешнему обработчику; отказ не открывает эту границу.',
 'agent/tool_executor.py:ToolExecutor._finish':'Проверяет формат ответа, записывает квитанцию до task/UI и снимает pending_write.',
 'agent/tool_executor.py:ToolExecutor.reject':'Создаёт настоящую квитанцию отказа по лимиту без запуска инструмента.',
 'agent/tool_executor.py:ToolExecutor.execute':'Валидирует и исполняет один call; различает исключение чтения и неопределённый исход эффекта.',
 'agent/tool_executor.py:ToolExecutor._write':'Готовит diff, ждёт согласия, сохраняет started, проверяет snapshot и выполняет запись; неизвестный исход не превращает в успех.',
 'agent/tool_recovery.py:task_journal':'Присваивает legacy-задаче ID эпохи при необходимости и открывает соответствующий журнал.',
 'agent/tool_recovery.py:_import_legacy':'Консервативно переносит только незавершённые старые пачки, используя прежние activity/pending_write; успешные старые блоки сохраняет.',
 'agent/tool_recovery.py:recover_task':'Восстанавливает канонические результаты, последние 100 activity, modified_files и команды; формирует безопасные recovery_items без сырых payload.',
 'agent/engine.py:AgentEngine._recover_execution':'Сверяет историю без временного system prefix с журналом перед моделью и при завершении/ошибке.',
 'core/python/task_service.py:TaskService.resolve_tool_recovery':'В idle проверяет выбранный чат, эпоху и call anchor, сохраняет наблюдение человека и возвращает обновлённые чат/task.',
 'tests/test_call_journal.py:assistant':'Создаёт независимую каноническую assistant-пачку фикстуры.',
 'tests/test_call_journal.py:receipt':'Создаёт каноническое tool-сообщение с JSON-квитанцией.',
 'tests/test_call_journal.py:CallJournalTests.result':'Читает JSON-квитанцию из указанного сообщения восстановленной истории.',
 'tests/test_tool_execution.py:ToolExecutionTests.executor':'Создаёт настоящий ToolExecutor с временным журналом и настраиваемыми границами отказов.',
 'tests/test_tool_execution.py:ToolExecutionTests.test_external_approval_durably_starts_only_after_agreement.handler':'Проверяет durable phase до и после разрешения внешнего действия.',
 'tests/test_tool_execution.py:ToolExecutionTests.test_external_denial_never_marks_effect_started.handler':'Возвращает отказ после настоящих hooks подтверждения, не начиная эффект.',
 'tests/test_tool_execution.py:ToolExecutionTests.test_saved_receipt_survives_checkpoint_failure.checkpoint':'Имитирует потерю доступности chat projection сразу после сохранения квитанции.',
})
TEST_PURPOSES.update({
 'approval_execution_verification_and_completion_share_legacy_status':'фазы lifecycle согласованы с legacy status и не меняют содержательные этапы',
 'unknown_effect_pause_and_failure_can_resume_with_reason_cleared':'остановленные задачи возобновляются с очисткой прежней причины',
 'recovery_can_reclassify_stopped_run_without_executing_it':'восстановление может уточнить остановку, не запуская модель или инструмент',
 'completed_run_cannot_reopen_or_change_terminal_outcome':'завершённую эпоху нельзя открыть повторно или заменить её исход',
 'finishing_without_tools_and_during_execution_is_permitted':'обычный ответ и окончание tool-цикла допускают завершение',
 'approval_wait_cannot_be_marked_completed':'ожидание нерешённого согласия не считается завершением',
 'legacy_tasks_migrate_without_losing_event_or_plan':'legacy status преобразуется без потери last_event и плана',
 'unrecognized_legacy_status_requires_attention':'неизвестный прежний status требует проверки',
 'existing_run_phase_takes_precedence_and_is_shared':'два контроллера видят одну фазу task',
 'repeated_transition_preserves_event_and_reason':'повтор фазы без новой причины не стирает сведения',
 'unknown_phase_is_rejected_without_changing_task':'неизвестная фаза отклоняется до мутации задачи',
 'optional_task_obeys_same_transitions':'запуск без persistence соблюдает ту же матрицу',
 'reasons_are_bounded_and_nonempty_for_failures':'причины ошибок ограничены и не теряются',
 'default_directory_uses_current_task_dir_and_chat_epoch_are_isolated':'журналы разных чатов и эпох используют независимые файлы',
 'prepare_and_started_are_fsynced_before_return':'prepared и started выполняют fsync до перехода к эффекту',
 'prepared_batch_and_awaiting_approval_are_never_executed':'не начатые вызовы восстанавливаются как NOT_EXECUTED',
 'started_read_only_and_effectful_calls_are_classified_conservatively':'потеря чтения отличается от неизвестного эффекта',
 'saved_receipt_restores_missing_chat_tail':'durable receipt восстанавливает потерянный хвост чата',
 'partial_batch_preserves_receipt_and_pairs_every_call':'успех соседнего call не теряется при незавершённой пачке',
 'real_canonical_receipt_replaces_placeholder_and_clears_gate':'сохранённый настоящий ответ снимает синтетический unknown',
 'stored_real_receipt_replaces_canonical_unknown':'настоящая квитанция из журнала заменяет неизвестный результат в чате',
 'resolutions_are_durable_explicit_and_replace_only_unknowns':'наблюдения человека переживают перезапуск и не заменяют известный ответ',
 'never_started_and_real_receipts_cannot_be_resolved':'ручная проверка доступна только неопределённым эффектам',
 'field_only_unknown_result_is_unresolved_and_can_be_resolved':'явный outcome_unknown распознаётся без специального code',
 'started_effect_can_be_resolved_when_no_receipt_was_written':'начатый эффект без ответа можно явно проверить',
 'torn_final_row_is_ignored_and_repaired_before_append':'оборванный JSONL-хвост не разрушает предыдущие receipts',
 'valid_unterminated_final_event_is_kept_when_appending':'полное последнее событие без перевода строки сохраняется',
 'complete_corrupt_row_is_not_silently_skipped':'повреждённая полная строка останавливает восстановление',
 'identity_mismatches_leave_history_and_file_untouched':'чужой call anchor не меняет исходные данные',
 'all_anchors_validate_before_adopting_any_canonical_receipt':'конфликт поздней пачки не приводит к частичному принятию ранних receipts',
 'multiple_missing_tail_batches_restore_at_their_exact_anchors':'несколько последовательных пачек восстанавливаются в своих позициях',
 'anchor_beyond_history_is_not_blindly_appended':'далёкий индекс не дописывается в чужую историю',
 'conflicting_real_receipts_fail_without_overwriting_either_copy':'конфликт двух настоящих квитанций сохраняет обе исходные копии',
 'batch_and_call_collisions_are_rejected_before_append':'пересечение якорей и дубликаты внутри пачки отклоняются до записи',
 'row_limit_and_invalid_json_values_preserve_the_existing_file':'слишком большой и не конечный JSON не повреждают журнал',
 'phases_cannot_move_backwards_or_reclassify_started_effects':'фазы монотонны и класс уже начатого вызова неизменен',
 'recovery_restores_missing_assistant_content':'сохранённый текст assistant восстанавливается вместе с вызовами',
 'separate_instances_share_the_same_transaction_lock':'два экземпляра одного журнала разделяют блокировку',
 'invalid_arguments_never_start_or_dispatch':'ошибка схемы не запускает handler и сохраняет настоящий отказ',
 'prepared_record_failure_prevents_dispatch':'ошибка записи пачки предотвращает исполнение',
 'started_record_failure_prevents_effect':'ошибка started предотвращает побочный эффект',
 'effect_exception_is_unknown_but_read_exception_is_retryable':'исключение эффекта требует проверки, исключение reader допускает повтор',
 'denied_write_never_starts_and_keeps_file_unchanged':'отказ от diff не сохраняет started и не меняет файл',
 'external_approval_durably_starts_only_after_agreement':'команда/MCP пересекает границу started только после согласия',
 'external_denial_never_marks_effect_started':'отклонённый внешний call остаётся не начатым',
 'saved_receipt_survives_checkpoint_failure':'ошибка chat checkpoint не теряет durable результат инструмента',
 'reused_call_ids_are_bound_to_their_batch':'повтор ID модели в другой пачке не заимствует прежний успех',
 'real_process_exit_at_five_execution_boundaries':'настоящий os._exit до/после эффекта и receipts не повторяет действие и сохраняет успех соседнего call',
 'recovery_metadata_is_bounded_and_idempotent':'105 вызовов дают не более 100 UI-записей без повторного изменения IDs',
 'verification_recovers_failed_commands_from_receipts':'провал команды восстанавливается из журнала и блокирует ложное completed',
 'unknown_effect_blocks_new_prompt_resume_and_fork_until_review':'неизвестный эффект блокирует новые запуски и копирование до проверки; устаревшие решения отвергаются',
 'deleting_chat_removes_only_its_journals':'удаление истории не затрагивает журналы других чатов',
 'unknown_flag_never_appears_as_success':'неопределённый исход не отображается зелёным успехом даже при противоречивом ok=true обработчика',
 'receipt_without_boolean_outcome_is_rejected_before_adoption':'невалидное поле ok не записывается и не принимается из истории как настоящий результат',
 'model_context_preserves_partial_batch_and_omits_orphans':'частичный успех остаётся в контексте, отсутствующий ответ помечен unknown, orphan исключён',
})
TS_NOTES.update({
 'TaskRecoveryItem':'Публичный якорь неизвестного эффекта: call ID, индекс сообщения, tool, безопасные path/summary.',
 'TaskRecoveryResolution':'Два явных наблюдения пользователя: выполнено либо не выполнялось; исходный payload не выдумывается.',
 'taskStatusLabel':'Показывает lifecycle, ошибку и неподтверждённый исход отдельно от завершения модели.',
 'apps/desktop/src/App.tsx:App.resolveToolRecovery':'Сериализует ручную проверку, вызывает фиксированный IPC и применяет возвращённые task/history только к прежнему выбранному чату.',
 'resolveToolRecovery':'Ограниченный preload API проверки неизвестного действия; передаёт chat/epoch/call identity и явное наблюдение.',
})


# Этап 5: старый JSONL reader остаётся для versioned migration и его fault-тестов.
for _stage5_key in list(SYMBOL_NOTES):
    if _stage5_key.startswith('agent/call_journal.py:CallJournal.'):
        SYMBOL_NOTES[_stage5_key.replace(':CallJournal.', ':LegacyCallJournal.')] = SYMBOL_NOTES.pop(_stage5_key)
for _stage5_key in ('agent/chat_store.py:_load_index','agent/chat_store.py:_metadata','agent/chat_store.py:_cache_chat'):
    SYMBOL_NOTES.pop(_stage5_key, None)
FILE_NOTES.update({
 'agent/artifact_store.py':'Неизменяемые UTF-8 результаты инструментов: SHA-256, атомарная запись, проверка целостности.',
 'agent/storage.py':'SQLite/WAL профиль: схема v1, копирующая миграция JSON, индекс чатов/поиска, checkpoint, receipts и ZIP backup.',
 'agent/chat_store.py':'Совместимый API чатов поверх транзакционного SQLite; JSON writer сохранён для настроек, старые чаты только мигрируются.',
 'agent/task_store.py':'Единственная каноническая таблица checkpoint; legacy task_path оставлен для миграции и диагностики.',
 'agent/projects.py':'Проекты в SQLite и атомарное отсоединение всех их чатов при удалении проекта.',
 'agent/call_journal.py':'Транзакционный журнал SQLite с прежними lifecycle/recovery контрактами и отдельным legacy JSONL reader.',
 'tests/test_chat_store.py':'Контракты SQLite chat API: миграционные warnings, запрет перечитывания JSON, rollback индекса и сохранность при повреждении БД.',
 'tests/test_storage.py':'Миграция всех режимов, реальные process exits, межпроцессные транзакции, большие outputs, индекс и проверенная ZIP-копия.',
 'tools/benchmark_storage.py':'Воспроизводимый локальный benchmark на синтетических JSON-чатах: перенос, p50/p95 списка и поиска.',
 'apps/desktop/src/StorageSettings.tsx':'История и копии в настройках: проверка целостности, счётчики миграции, локальный ZIP export и явные ошибки.',
})
SYMBOL_NOTES.update({
 'agent/chat_store.py:_database':'Выбирает SQLite профиль по текущему CHAT_DIR; тестовые временные каталоги не попадают в данные пользователя.',
 'agent/chat_store.py:search_chats':'Передаёт ограниченный областью поиск title/user/assistant в индекс, без load_chat для каждого результата.',
 'agent/task_store.py:_database':'Выбирает тот же профиль SQLite по TASK_DIR; хранит checkpoint вне папки рабочего проекта.',
 'agent/projects.py:ProjectStore._database':'Возвращает один экземпляр Storage для вложенных транзакций save/list/get без повторного writer lock.',
 'agent/call_journal.py:LegacyCallJournal':'Сохранённая JSONL реализация: читает и проверяет старые события; новый runtime использует подкласс CallJournal.',
 'agent/call_journal.py:CallJournal':'Канонический SQLite журнал с теми же prepared/started/receipt/recovery контрактами, однократным импортом эпохи и tombstones.',
 'agent/call_journal.py:CallJournal._read':'В одной транзакции проверяет legacy lifecycle, копирует и сверяет события, гидратирует результаты; corrupt complete row останавливает импорт.',
 'agent/call_journal.py:CallJournal._stored_event':'Большой JSON receipt заменяет ссылкой SHA-256; identity и фаза действия остаются непосредственно в БД.',
 'agent/call_journal.py:CallJournal._append':'Записывает событие и внешний результат до возврата из транзакции; к удалённому чату новые эффекты не привязываются.',
 'agent/call_journal.py:CallJournal.delete_chat':'Удаляет события всех эпох выбранного чата и сохраняет запрет повторного импорта старых JSONL.',
 'agent/call_journal.py:JournalTransaction':'Сочетает общий RLock эпохи с BEGIN IMMEDIATE, охватывающим проверку lifecycle и append в разных процессах.',
 'agent/call_journal.py:JournalTransaction.__enter__':'Захватывает thread lock и открывает реентерабельную транзакцию; при ошибке открытия освобождает lock.',
 'agent/call_journal.py:JournalTransaction.__exit__':'Завершает вложенный transaction context и всегда освобождает thread lock.',
 'agent/storage.py:encode':'Сериализует конечный JSON без NaN/Infinity и без потери русского текста.',
 'agent/storage.py:valid_chat':'Проверяет 32-символьный hex ID и список канонических dict-сообщений до записи или импорта.',
 'agent/storage.py:Storage':'Локальный transactional профиль; короткие connections, WAL/FULL durability, миграции, история, поиск, артефакты и резервные копии.',
 'agent/storage.py:Storage._connect':'Включает foreign keys и FULL synchronous; закрывает connection даже при повреждении БД на этапе PRAGMA.',
 'agent/storage.py:Storage.transaction':'BEGIN IMMEDIATE перед чтением изменяемого состояния; commit/rollback при выходе, вложенные вызовы используют тот же connection.',
 'agent/storage.py:Storage.ready':'Проверяет user_version, атомарно создаёт v1 и выполняет одноразовую миграцию; готовый профиль не сканирует legacy файлы.',
 'agent/storage.py:Storage.pack':'Для tool output больше 16 КиБ сохраняет immutable bytes и возвращает внутренний reference v1.',
 'agent/storage.py:Storage.unpack':'Загружает только внутреннюю ссылку артефакта с проверкой SHA-256; наружу возвращает полный исходный текст.',
 'agent/storage.py:Storage._source':'Сохраняет относительный путь, исходный SHA-256, тип, число объектов и статус проверки миграции.',
 'agent/storage.py:Storage._migrate':'Копирует чаты/messages, embedded или отдельный checkpoint и проекты; сверяет counts и неизменность исходников перед общим commit.',
 'agent/storage.py:Storage._search_entry':'Индексирует только title/user/assistant, обновляет изменившиеся записи и удаляет устаревшие; tool data не становится поисковой инструкцией.',
 'agent/storage.py:Storage.write_chat':'В единой транзакции обновляет metadata, изменённые сообщения, поиск и явный checkpoint; draft не затирает новую задачу.',
 'agent/storage.py:Storage.load_chat':'Открывает согласованный read snapshot, возвращает полный transcript и единственный checkpoint, гидратирует сохранённые результаты.',
 'agent/storage.py:Storage.checkpoint':'Читает каноническую задачу; повреждённый legacy checkpoint не выдаёт за отсутствие задачи и блокирует продолжение этого чата.',
 'agent/storage.py:Storage.catalog':'Выбирает компактную metadata проекцию по индексу scope, не открывая transcripts, drafts и legacy JSON.',
 'agent/storage.py:Storage.search':'FTS5 trigram для casefold substring от 3 символов; короткие строки и runtime без FTS используют scoped SQL fallback.',
 'agent/storage.py:Storage.report':'Возвращает schema version, quick_check, счётчики объектов и проверенный migration manifest без содержимого разговоров.',
 'agent/storage.py:Storage.backup':'Создаёт online SQLite snapshot, добавляет проверенные referenced artifacts и legacy источники; ZIP проверяет до атомарной замены выбранного файла.',
 'agent/artifact_store.py:ArtifactStore':'Адресуемые по содержимому локальные outputs, общие для истории и квитанций; удаление чата не удаляет резервные исходники.',
 'agent/artifact_store.py:ArtifactStore.path':'Разрешает только 64 hex SHA-256, без произвольного filesystem path.',
 'agent/artifact_store.py:ArtifactStore.put':'Записывает UTF-8 через временный файл, fsync/replace до ссылки в БД; существующие bytes проверяет для дедупликации.',
 'agent/artifact_store.py:ArtifactStore.get':'Проверяет длину и SHA-256; отсутствующий или испорченный результат даёт явную ошибку и не запускает tool повторно.',
 'tests/test_storage.py:conversation':'Строит детерминированный старый чат с полями scope и русским текстом, без реальных данных пользователя.',
 'tests/test_storage.py:tool_call':'Создаёт фиксированный call anchor для проверки импорта/квитанций без настоящей записи файла.',
 'tests/test_storage.py:StorageTests':'Изолированный профиль для транзакций, миграционных сбоев, процесса, индекса и ZIP восстановления.',
 'tests/test_storage.py:StorageTests.legacy':'Пишет настоящий старый JSON до первого открытия SQLite и возвращает путь для сравнения исходных bytes.',
})
TEST_PURPOSES.update({
 'migration_preserves_modes_projects_checkpoints_and_original_bytes':'Chat/IDE/Лола, проект и приоритет embedded checkpoint сохраняются; counts и SHA исходников проверены.',
 'interrupted_migration_is_rolled_back_and_can_retry':'сбой до manifest откатывает схему/данные целиком; следующий запуск успешно повторяет перенос.',
 'malformed_project_catalog_stops_migration_without_losing_chats':'повреждённый каталог проектов не превращается в пустой и не фиксирует частичную миграцию.',
 'future_schema_is_not_downgraded':'более новый user_version отклоняется без перезаписи данных.',
 'corrupt_checkpoint_cannot_be_treated_as_a_new_chat':'нечитаемая задача блокирует продолжение вместо потери сведений о возможных эффектах.',
 'readonly_catalog_and_search_never_open_full_chats_or_legacy_files':'список и поиск используют SQL metadata/index; сохраняют mode/project scope и русскую подстроку.',
 'sql_fallback_preserves_substring_search':'поиск без FTS5 сохраняет casefold substring семантику.',
 'task_and_history_commit_together_without_stale_draft_overwrite':'старый draft не затирает новую задачу; ошибка индекса откатывает сообщения и metadata.',
 'real_process_exit_before_and_after_chat_commit':'os._exit до commit оставляет старые сообщения/checkpoint, после commit сохраняет новые целиком.',
 'large_outputs_are_referenced_and_hydrated_without_reexecution':'большой результат занимает компактную ссылку в messages/journal, дедуплицируется и дочитывается по прежнему anchor.',
 'missing_or_corrupt_artifact_fails_without_mutating_history':'потеря или неверная checksum outputs не выдаёт фиктивный успех и не изменяет исходник.',
 'legacy_receipts_migrate_once_and_torn_tail_is_retained':'настоящая квитанция импортируется однократно, incomplete JSONL tail остаётся в исходнике с warning.',
 'corrupt_complete_journal_blocks_import_and_keeps_source':'повреждённая полная JSONL строка блокирует восстановление без частичного принятия событий.',
 'two_processes_share_atomic_call_validation':'параллельные prepare/started сохраняют одну монотонную последовательность без дублирования batch.',
 'deletion_is_atomic_and_cannot_resurrect_legacy_data':'удаление history/task/events не позволяет старому JSON/JSONL вернуться при перезапуске.',
 'project_removal_detaches_all_chat_modes_in_one_transaction':'удаление проекта переносит его Chat/IDE/voice в личное пространство одной транзакцией.',
 'verified_backup_restores_database_receipts_and_full_outputs':'ZIP восстанавливает БД, full outputs, активные и ещё не импортированные старые журналы.',
 'catalog_ignores_legacy_cache_after_migration':'legacy index больше не нужен, не читается и не переписывается списком SQLite.',
 'index_failure_rolls_back_transcript_and_metadata':'потеря search index write не оставляет частично сохранённый чат.',
 'corrupted_legacy_chat_is_reported_without_modifying_source':'повреждённый JSON остаётся с warning и не создаёт ложный пустой чат.',
 'unreadable_legacy_directory_is_not_an_empty_catalog':'отказ доступа к источнику останавливает миграцию, повтор после исправления возможен.',
 'corrupt_database_never_falls_back_to_old_json':'повреждённая каноническая БД не подменяется старой историей и connection не остаётся открытым.',
 'checkpoint_survives_absent_legacy_task_file':'канонический checkpoint не зависит от отдельного legacy файла.',
 'legacy_index_is_not_used_during_agent_execution':'HTTP agent approval/result/task_end работают с полностью запрещённым JSON writer истории.',
})
TS_NOTES.update({
 'StorageReport':'Публичные счётчики, результат integrity check и итоги копирующей миграции без содержимого чатов.',
 'StorageSettings':'Раздел истории/копий в существующем дизайне настроек; запрос только при открытии раздела.',
 'apps/desktop/src/StorageSettings.tsx:StorageSettings.inspectStorage':'Показывает текущую целостность и счётчики или явную ошибку; никакие данные не изменяет.',
 'apps/desktop/src/StorageSettings.tsx:StorageSettings.backupStorage':'Открывает системный выбор ZIP, отображает отмену, ошибку либо подтверждённый путь готовой копии.',
 'storageStatus':'Фиксированный preload IPC проверки локального хранилища, без произвольной команды.',
 'backupStorage':'Фиксированный IPC резервной копии; путь берётся только из системного dialog в main.',
})

# Прежние имена API сохраняются; их описания теперь соответствуют SQLite пути.
register('agent/chat_store.py', """
_valid_id | Проверяет 32-символьный hex UUID до доступа к канонической записи чата.
read_chat_catalog | Выбирает компактную индексированную metadata проекцию и migration warnings; корпус JSON повторно не читает.
_atomic_write | Атомарный JSON writer для настроек/совместимости; историю и checkpoint сохраняет Storage.
list_chats | Возвращает metadata с pinned/updated_at порядком без чтения transcripts.
create_chat | Генерирует UUID и атомарно создаёт пустую историю, metadata и поисковую запись заголовка.
load_chat | Валидирует ID и возвращает согласованный SQLite snapshot с полными outputs и единственным checkpoint.
save_chat | В одной транзакции сохраняет metadata/messages/index и явный checkpoint; ошибки откатывают всё изменение.
delete_chat | Атомарно удаляет каноническую историю, задачу, поиск и receipts; сохраняет tombstone и legacy восстановительные материалы.
""")
register('agent/task_store.py', """
save_task | Обновляет timestamp копии задачи и фиксирует единственный checkpoint в SQLite.
load_task | Читает каноническую задачу; отсутствующую возвращает как None, повреждённый legacy checkpoint не игнорирует.
clear_task | Удаляет канонический checkpoint без удаления истории сообщений; JSON источники миграции остаются.
""")
register('agent/projects.py', """
ProjectStore.list | Читает канонические метаданные проектов из общей БД профиля.
ProjectStore.save | Проверяет имя, инструкции и существование папки; сохраняет проект с временными метками одной транзакцией.
ProjectStore.remove | Одной транзакцией отсоединяет чаты всех режимов, обновляет metadata/summary и удаляет группу; файлы проекта не меняет.
""")


# Этап 6: критерии, ограничение чтения, подтверждаемые проверки и снимки файлов.
FILE_NOTES.update({
 'agent/task_contract.py':'Пользовательские параметры IDE, план модели и критерии с привязкой к настоящим проверкам.',
 'agent/workspace_snapshots.py':'Долговечные before/after снимки файловых tools, сегменты изменений, conflict-aware rollback и ручная проверка прерванного отката.',
 'core/python/workspace_review.py':'Пользовательский API compare/preview/confirm/review; модели не получают инструмент отката.',
 'apps/desktop/src/IdeTaskOptions.tsx':'Компактные параметры задачи IDE: только чтение, критерии, команды и post-edit проверки.',
 'apps/desktop/src/WorkspaceReview.tsx':'Список наборов правок, обратный diff, подтверждение отката и явное предупреждение конфликтов.',
 'tests/test_ide_verification.py':'18 контрактов критериев, readonly enforcement, снимков, аварийного и частичного отката, backup и schema upgrade.',
 'tests/migration/test_ide_acceptance.py':'Реальный HTTP workflow plan/write/command/rollback/recheck и отказ исполнения write в режиме чтения.',
})
register('agent/task_contract.py', """
validate_options | До запуска задачи проверяет readonly/auto/checks_only, критерии, ссылки на IDs, программы, argv, cwd и timeout; некорректный ввод не расширяет права.
install_contract | Сохраняет исходные пользовательские критерии, параметры и baseline долговечной ревизии откатов.
set_plan | Добавляет модельные шаги и критерии, сохраняя пользовательские требования; неизвестные check_ids отклоняет, успех не выдумывает.
command_key | SHA-256 точного program/argv/cwd; название проверки не меняет фактически исполняемую команду.
acceptance_summary | Выводит unverified/failed/stale/checks_passed только по связанным пользовательским командам и ревизии файлов.
""")
register('agent/workspace_snapshots.py', """
fingerprint | Выбирает вид, hash, filesystem identity и права для сравнения; внутренний artifact reference не является ревизией файла.
SnapshotStore | Снимки подтверждённых файловых операций; группы разделяются после чужих правок, ограничены 80 путями и не охватывают произвольные команды.
SnapshotStore.capture | Читает реальный путь внутри корня без symlink/junction, до 1 МБ; сохраняет исходные байты в immutable base64 artifact.
SnapshotStore._rows | Выбирает упорядоченные записи группы строго для выбранного чата и root.
SnapshotStore._aggregate | Объединяет первый before и последний подтверждённый after по каждому пути, пропуская не выполненные операции.
SnapshotStore.prepare | До started сохраняет before и ожидаемый результат; ручная правка между операциями начинает отдельный undo segment.
SnapshotStore.finish | Проверяет фактические post-edit bytes против ожидаемых; чужое изменение не присваивается агенту как безопасный after.
SnapshotStore.reconcile | После прерывания помечает незавершённый capture недоступным; только доказанное отсутствие эффекта снимает pending snapshot.
SnapshotStore.list | Даёт до 50 групп со статусами и путями без исходного содержимого; binary/text bytes не уходят в UI metadata.
SnapshotStore.revision | Читает долговечный счётчик откатов этого чата и root, используемый для инвалидирования результатов проверок.
SnapshotStore.attention | Находит все незавершённые/частичные откаты в области, независимо от лимита видимой истории групп.
SnapshotStore._validate | До первого эффекта сверяет root identity, все after-ревизии и отсутствие чужих детей в созданных папках.
SnapshotStore.preview | Строит обратный diff и fingerprint всей группы; конфликт файлов отменяет proposal без изменений.
SnapshotStore._original_bytes | Проверяет artifact checksum, base64 и hash исходного файла до восстановления.
SnapshotStore._restore_file | Пишет оригинал через temp/fsync и повторную проверку ревизии; create-only не заменяет появившийся файл, chmod возвращает исходные права.
SnapshotStore.restore | Фиксирует rolling_back и revision до эффектов; прогресс хранит после каждого пути. Частичный сбой не повторяется автоматически.
SnapshotStore.review | Сохраняет явную ручную проверку прерванного отката и снимает блокировку без изменения файлов.
""")
register('core/python/workspace_review.py', """
WorkspaceReview | Ограниченный API пользовательского отката с одноразовым preview token на 120 секунд.
WorkspaceReview.scope | Проверяет idle, IDE mode, chat/project/root и recovery gates; соседний чат не может применить чужой snapshot.
WorkspaceReview.list | Возвращает snapshots и восстановленный checkpoint выбранного IDE-чата.
WorkspaceReview.preview | Проверяет все файлы и сохраняет proposal, привязанный к чату/root/group/fingerprint и сроку.
WorkspaceReview.apply | Погашает подтверждение, выполняет повторную проверку и откат; обновляет устаревшую verification-проекцию из долговечного revision.
WorkspaceReview.review | При явном confirmed отмечает ручную проверку partial rollback; не повторяет filesystem effects.
""")
register('agent/verifier.py', """
StageVerifier.refresh | Обновляет command/acceptance evidence после загрузки или отката без изменения lifecycle задачи; непокрытые критерии остаются видимыми.
StageVerifier.record_command | Хранит program/argv/cwd/purpose/exit code, точный configured check_id и generation receipt; чужой success не выдаёт за нужную проверку.
StageVerifier.command_summary | Отличает not_run, failed, stale, incomplete и commands_passed; после новых файловых изменений прежний exit zero устаревает.
""")
register('agent/engine.py', """
AgentEngine._run_configured_checks | Запускает только пользовательские commands через прежние ToolExecutor/journal/policy/approval; не добавляет отключённое расширение и не вызывает модель для checks_only.
""")
register('agent/tool_executor.py', """
ToolExecutor._capture_snapshot | До файлового эффекта долговечно сохраняет before-image; ошибка снимка останавливает dispatch, не отключая защиту ради записи.
""")
register('tests/test_ide_verification.py', """
IdeVerificationTests | Изолированный project/profile для проверки rollback и прав без реальных данных пользователя.
IdeVerificationTests.executor | Строит настоящий executor с журналом и фикстурным подтверждением файлов, без внешней модели.
IdeVerificationTests.apply | Выполняет одну файловую операцию через durable batch и canonical receipt, возвращает проверенный результат.
IdeVerificationTests.test_partial_rollback_is_durable_and_never_replayed_implicitly.fail_second | Воспроизводит отказ второго файла после успешного восстановления первого.
IdeVerificationTests.test_manual_change_during_partial_restore_is_preserved.concurrent_edit | Вставляет чужую правку второго файла между filesystem effects отката.
""")
register('tests/migration/test_ide_acceptance.py', """
AcceptanceHandler | Локальный HTTP/SSE fixture выдаёт конкретный plan, write и final либо намеренно запрещённый readonly write.
IdeAcceptanceTests | Поднимает настоящий bridge service и HTTP сервер с временным profile/project.
IdeAcceptanceTests.finish | Обрабатывает реальные approval events, подтверждает предложенные команды и ждёт task_end без ошибок.
""")
TEST_PURPOSES.update({
 'roundtrip_nested_create_patch_rename_delete_preserves_original_bytes':'один набор отменяет mkdir/write/patch/rename/delete и возвращает исходные CRLF bytes.',
 'manual_edit_after_preview_blocks_entire_rollback':'последующая ручная правка не даёт начать откат даже соседнего файла.',
 'untracked_file_in_created_directory_is_never_removed':'созданная папка с новым чужим файлом не удаляется автоматически.',
 'intervening_manual_revision_starts_a_separate_undo_segment':'откат второй правки возвращает ручную промежуточную версию и не затирает её первым сегментом.',
 'binary_rename_undo_is_byte_exact':'обратный перенос восстанавливает двоичный файл без перекодирования.',
 'snapshot_failure_prevents_file_dispatch':'ошибка сохранения before не допускает write и не пересекает started.',
 'read_only_blocks_files_commands_and_unknown_external_tools':'readonly policy блокирует mutators, команды и неизвестные внешние effects до dispatch.',
 'model_plan_cannot_erase_user_criteria_or_invent_evidence':'модель не удаляет критерии пользователя и не придумывает IDs или успех проверок.',
 'checks_are_exactly_linked_and_invalidated_by_further_edits':'неверный argv не подтверждает критерий; новая правка делает правильный старый тест устаревшим.',
 'rollback_invalidates_receipts_even_after_projection_loss':'долговечная rollback revision инвалидирует старые тесты после recovery без повторного увеличения generation.',
 'partial_rollback_is_durable_and_never_replayed_implicitly':'частичный отказ сохраняет состояние и требует ручной проверки без автоматического повтора.',
 'prepared_snapshot_is_not_automatically_adopted_after_crash':'потерянный after нельзя выдать за безопасный snapshot даже при успешном tool receipt.',
 'snapshot_backup_can_restore_originals_in_a_fresh_profile':'ZIP включает необходимые snapshot artifacts, из которых можно восстановить оригиналы после переноса.',
 'schema_one_upgrade_preserves_canonical_history':'транзакционная миграция SQLite v1 в v2 сохраняет каноническую историю.',
 'user_checks_use_real_approval_without_model_or_extra_capabilities':'checks_only не вызывает модель и не включает отключённые команды; purpose виден в обычном approval.',
 'invalid_options_do_not_start_commands_or_replace_task':'неверные ограничения и пустые команды отклоняются до работы.',
 'real_process_exit_during_rollback_requires_manual_review':'настоящий os._exit между effects оставляет rolling_back, сохраняет соседние данные и блокирует неподтверждённое продолжение.',
 'manual_change_during_partial_restore_is_preserved':'изменение второго файла уже во время отката сохраняется, состояние становится rollback_unknown.',
 'http_plan_auto_check_rollback_and_failed_recheck':'HTTP plan и write, обычное одобрение post-edit команды, stale после rollback и failed recheck без дополнительных model requests.',
 'read_only_http_malicious_call_is_not_dispatched':'навязанный моделью write блокируется даже при отсутствии schema в readonly payload, без approval и изменения файла.',
})
TS_NOTES.update({
 'ValidationCommand':'Пользовательская программа проверки: purpose, argv, cwd, timeout и ID для acceptance links.',
 'IdeOptions':'Ограничения IDE задачи, пользовательские критерии и список явно настроенных проверок.',
 'serializeIdeOptions':'Убирает пустые строки критериев с сохранением правильных связей check_ids по новым индексам.',
 'IdeTaskOptions':'Сворачиваемая форма IDE с readonly, критериями, командами и запуском проверок без модели.',
 'apps/desktop/src/IdeTaskOptions.tsx:IdeTaskOptions.updateCheck':'Изменяет одну проверку по ID, сохраняя остальные настройки задачи.',
 'apps/desktop/src/IdeTaskOptions.tsx:IdeTaskOptions.removeCheck':'Удаляет проверку вместе с её ссылками из критериев.',
 'WorkspaceSnapshot':'Публичные status/path/operation метаданные набора; оригиналы файлов остаются в локальном хранилище.',
 'RollbackPreview':'Ограниченный обратный diff и одноразовый ID подтверждения, без внутренних backup references.',
 'WorkspaceReview':'Пользовательский список snapshots и diff/confirm workflow; блокирует действия при несохранённом editor draft.',
 'apps/desktop/src/WorkspaceReview.tsx:WorkspaceReview.compareSnapshot':'Получает новое предложение отката после серверной проверки root/chat/revisions.',
 'apps/desktop/src/WorkspaceReview.tsx:WorkspaceReview.applyRollback':'Подтверждает текущий одноразовый preview, показывает conflict/partial error и обновляет stale evidence.',
 'apps/desktop/src/WorkspaceReview.tsx:WorkspaceReview.confirmManualReview':'Фиксирует явную проверку после partial rollback без повторения эффекта.',
 'listSnapshots':'Фиксированный IPC списка снимков текущего IDE-чата.',
 'previewRollback':'Фиксированный IPC обратного diff и server-issued proposal.',
 'applyRollback':'Фиксированный IPC подтверждения rollback proposal, без произвольного файла/команды.',
 'reviewRollback':'Фиксированный IPC явного наблюдения после partial rollback; данные файлов не изменяет.',
})

SYMBOL_NOTES['agent/workspace_snapshots.py:SnapshotStore.rollback_event']='Возвращает последний долговечный результат rollback/review, чтобы recovery отличал полный откат от ручной проверки partial state и записывал этот факт в контекст модели.'

FILE_NOTES.update({
 'agent/storage.py':'SQLite/WAL профиль: схемы v1→v2, копирующая миграция JSON, индекс истории, checkpoint/receipts, snapshot metadata и ZIP backup.',
 'agent/verifier.py':'Детерминированные свидетельства program/argv/purpose/exit code и generation; критерии unverified/failed/stale/checks_passed без модельного выдумывания успеха.',
})
SYMBOL_NOTES.update({
 'agent/storage.py:Storage.ready':'Проверяет user_version, атомарно создаёт базовую схему и upgrade v1→v2 со snapshots; legacy JSON копируется один раз, более новая схема отклоняется.',
 'agent/storage.py:Storage.backup':'Online SQLite snapshot с проверенными tool/snapshot artifacts и legacy источниками; ZIP проверяется и fsync выполняется до замены выбранного файла.',
})


# Этап 7: отдельные session/run contracts и повторно используемые MCP actors.
FILE_NOTES.update({
 'agent/operation_context.py':'Общий deadline/cancel контракт и единый inference gate для задач, probe и последующих необязательных вычислений.',
 'agent/capability_profiles.py':'Фиксированные ограничивающие профили Chat/IDE/Лолы; включённые расширения остаются источником разрешений.',
 'agent/mcp_sessions.py':'Ограниченный пул MCP actors: connect/use/exit в одной asyncio task, TTL, отмена, invalidation и shutdown без повтора effects.',
 'agent/mcp_client.py':'SDK-адаптер MCP поверх session pool; нормализация bounded/untrusted результатов без раскрытия токенов.',
 'core/python/session_service.py':'Выбор, scoped список/переименование/перенос чатов и восстановление canonical history отдельно от inference.',
 'core/python/protocol.py':'Версия критического RPC, проверка входного envelope, run IDs, решений и confirmed до dispatch.',
 'apps/desktop/shared/protocol.ts':'Общие типы критического IPC, версия, runtime guard событий и таблица timeout/cancel.',
 'apps/desktop/shared/contextTypes.ts':'Независимые от React типы budget/usage для протокола и renderer.',
 'apps/desktop/shared/taskTypes.ts':'Единые task/recovery/evidence типы без зависимости Electron main от TSX.',
 'apps/desktop/shared/ideTypes.ts':'Общие validation command и IDE task options без renderer runtime.',
 'apps/desktop/src/useTaskSession.ts':'Состояние разговора и жизненного цикла UI; отбрасывание поздних/чужих событий и редукция stream/task_end.',
 'tests/test_services_and_sessions.py':'7 новых контрактов deadline/gate/protocol/profile и настоящего reuse/invalidate/cancel MCP stdio.',
})
for _stage7_key in list(SYMBOL_NOTES):
    if _stage7_key.startswith('agent/mcp_client.py:MCPClient._operate'):
        SYMBOL_NOTES.pop(_stage7_key)
register('agent/operation_context.py', """
OperationContext | Event-совместимый deadline/cancel token; дочерняя операция не продлевает срок родителя.
OperationContext.set_deadline | Устанавливает или сокращает локальный monotonic deadline.
OperationContext.remaining | Возвращает минимальный оставшийся срок своего и родительского контекстов.
OperationContext.is_set | Отмена активна при set, отмене родителя или истечении deadline.
OperationContext.set | Устанавливает сигнал отмены, не освобождая inference lease до фактического завершения.
OperationContext.wait | Ожидает отмену/срок короткими ожиданиями, учитывая timeout вызывающего кода.
OperationContext.child | Создаёт дочерний контекст с общим родительским сигналом и собственным пределом.
InferenceLease | ID владельца, назначение и cancel context одной тяжёлой операции.
InferenceGate | Разрешает одну inference, сохраняя владельца до завершения реального worker.
InferenceGate.begin | Выдаёт lease либо отклоняет конкурирующий запуск с понятным назначением текущей работы.
InferenceGate.end | Освобождает gate только при совпадении ID; старый task_end не освобождает нового владельца.
InferenceGate.cancel | Сигнализирует отмену, не допускает преждевременный параллельный запуск.
InferenceGate.status | Возвращает безопасные busy/kind/limit без ключей и содержимого запросов.
""")
register('agent/capability_profiles.py', """
mode_groups | Ограничивает группы выбранным режимом и наличием root; не включает выключенные tools и не доверяет MCP annotations.
""")
register('agent/mcp_sessions.py', """
MCPSessionPool | Ленивый asyncio-loop и до четырёх endpoint/credential actors с idle TTL 45 секунд.
MCPSessionPool._start | Запускает loop thread один раз; закрытый manager повторно не оживает.
MCPSessionPool.operation | Хеширует только connection identity и token, передаёт parent cancellation, ограничивает синхронное ожидание без автоматического повтора.
MCPSessionPool._submit | Ставит запрос в actor queue и наблюдает отмену даже во время connect; просроченная очередь не исполняется позднее.
MCPSessionPool._actor | В одной task открывает транспорт/Client, последовательно выполняет вызовы и закрывает контекст при idle/cancel/error.
MCPSessionPool._failure | Возвращает conservative unknown для tool effects и MCP_ERROR для discovery без исходных credentials.
MCPSessionPool.invalidate | Прерывает выбранные endpoint actors при смене настроек/токена или выключении; не повторяет запросы.
MCPSessionPool.status | Показывает количество сессий, IDs и число операций без endpoint URL и токенов.
MCPSessionPool.shutdown | Останавливает actors и loop, закрывает transport contexts и ждёт завершения thread ограниченное время.
MCPSessionPool._close | Собирает закрытие actor tasks на их общем event loop.
""")
register('agent/mcp_client.py', """
MCPClient._connect | SDK stdio/HTTP контекст с ограниченным логом, без redirect/credential forwarding; принадлежит actor task.
MCPClient._exchange | Получает catalog либо tool result; ограничивает тексты и заменяет media base64 метаданными.
MCPClient.shutdown | Закрывает принадлежащий адаптеру session pool.
""")
register('core/python/session_service.py', """
SessionService | Владелец выбранного чата/project_id и восстановления, не создаёт модель и не управляет React.
SessionService.move_chat | Переносит Chat/Лолу только внутри выбранной области с проверкой mode/root/project.
SessionService.chats | Читает индексированную metadata по scope без transcripts scan.
SessionService.rename | Проверяет заголовок и принадлежность области, обновляет selected projection.
SessionService.select_chat | Загружает проверенный scoped chat либо создаёт новый и восстанавливает checkpoint/stream fragment/receipts.
SessionService.recover | Сверяет chat/task identity, чинит canonical tail из receipts, сохраняет неизвестные effects и rollback gates.
""")
register('core/python/task_service.py', """
TaskService.chat | Совместимое свойство активного чата, фактическое состояние хранит SessionService.
TaskService.project_id | Совместимое свойство пространства, фактическое состояние хранит SessionService.
TaskService._start | Подготавливает capabilities/engine и запускает worker внутри уже полученного inference lease.
TaskService.start | Сериализует тяжёлую работу через gate; синхронная ошибка подготовки освобождает только свой lease.
TaskService._recover_chat | Совместимый адаптер SessionService.recover.
TaskService.select_chat | Совместимый адаптер выбора/создания чата отдельным SessionService.
""")
register('core/python/protocol.py', """
require_text | Проверяет обязательную ограниченную строку без NUL до обращения к сервису.
validate_request | Принимает protocol v1 и legacy envelope без version, проверяет критические IDs/флаги/решения и возвращает method/params без выполнения.
""")
register('tests/test_services_and_sessions.py', """
ServiceBoundaryTests | Изолированные проверки границ сервисов без внешних учётных записей и моделей.
ServiceBoundaryTests.test_probe_and_task_share_one_heavy_inference_gate.probe | Держит fixture probe до отмены, чтобы проверить отказ конкурирующей задачи.
ServiceBoundaryTests.test_mcp_cancellation_during_connect_is_prompt.connect | Асинхронный connect fixture без побочных эффектов, намеренно задержанный для отмены.
ServiceBoundaryTests.test_mcp_cancellation_during_connect_is_prompt.exchange | Безопасный ответ fixture; до него отменённое подключение не должно дойти.
""")
TEST_PURPOSES.update({
 'child_deadline_is_bounded_and_parent_cancel_is_immediate':'child соблюдает срок и отмену родителя, не продлевает время операции.',
 'stale_gate_owner_cannot_release_a_new_inference':'конкурирующая inference отклоняется, старый lease не освобождает новый.',
 'protocol_rejects_wrong_version_ids_and_non_boolean_approval':'несовместимая версия, неверный run_id и строковое confirmed не проходят dispatch.',
 'mode_profiles_cannot_enable_project_tools_in_chat_or_voice':'профиль режима ограничивает группы даже при переданном root.',
 'probe_and_task_share_one_heavy_inference_gate':'реальный TaskService не запускает задачу одновременно с probe и освобождает gate после отмены.',
 'mcp_reuses_process_and_invalidates_without_replaying_calls':'два реальных вызова используют PID одного MCP process; label/catalog не меняют transport identity, invalidate создаёт новый PID.',
 'mcp_cancellation_during_connect_is_prompt':'отмена на connect возвращается быстро и закрывает actor, tool эффект не повторяется.',
})
SYMBOL_NOTES['tests/fixtures/mcp_echo.py:session_identity']='Возвращает только PID fixture процесса, чтобы проверить реальное переиспользование транспорта.'
if 'Message' in TS_NOTES:TS_NOTES['SessionMessage']=TS_NOTES.pop('Message')
TS_NOTES.update({
 'AgentMode':'Три допустимых wire-режима Chat/IDE/Лола.',
 'RpcFailure':'Явный отказ с текстом и необязательным code, без фиктивных полей успеха.',
 'RpcResult':'Discriminated union успеха и отказа для критического API.',
 'StartTaskOptions':'Типизированные параметры IDE и режим проверки без модели.',
 'StartTaskResult':'Успешный chat/run identity либо явная ошибка старта.',
 'ApprovalDecision':'Только apply/reject/cancel; произвольная строка не проходит компиляцию/валидацию.',
 'RecoveryRequest':'Якорь конкретного call и явное пользовательское наблюдение.',
 'SnapshotSummary':'Публичные snapshot metadata без backup bytes.',
 'SnapshotScope':'Выбранный chat ID для операций review.',
 'SnapshotPreview':'Обратный diff, ограничение отображения и одноразовый ID proposal.',
 'SnapshotListResult':'Типизированный список снимков и восстановленный checkpoint либо отказ.',
 'SnapshotApplyResult':'Успех либо partial failure с необязательными актуальными snapshots/task; UI обрабатывает оба исхода.',
 'TaskEventBase':'Run/chat correlation и версия критических событий.',
 'TaskLifecycleEvent':'Discriminated lifecycle events вместо неограниченных полей task/stream/approval.',
 'isTaskEvent':'Проверяет wire envelope критического события до изменения UI state.',
 'rpcTimeout':'Одна таблица допустимых таймаутов main→Core, включая долгие backup/snapshot запросы.',
 'rpcCancellation':'Связывает истечение RPC с соответствующей отменой поиска/STT/discovery/probe/задачи без повтора effects.',
 'SessionMessage':'Публичное сообщение UI с устойчивым stream ID и признаком незавершённого текста.',
 'useTaskSession':'Владелец сообщений/задачи/busy/run refs; run_id задаётся до стартового IPC.',
 'apps/desktop/src/useTaskSession.ts:useTaskSession.accepts':'Не принимает чужую область, старый run или события после task_end; ранний start bind не зависит от порядка ответа IPC.',
 'apps/desktop/src/useTaskSession.ts:useTaskSession.reduce':'Применяет только проверенные lifecycle events и завершает streaming при task_end.',
})

# Stage 7: moved nested dispatcher keeps its original documented responsibility.
for key in list(SYMBOL_NOTES):
    if key.startswith("core/python/task_service.py:TaskService.start."):
        SYMBOL_NOTES[key.replace("TaskService.start.","TaskService._start.")]=SYMBOL_NOTES.pop(key)

for old,new,names in [("ContextUsage.tsx","contextTypes.ts",["RequestBudgetSnapshot","ModelUsageSnapshot"]),("TaskProgress.tsx","taskTypes.ts",["TaskStage","ToolActivity","TaskRecoveryItem","TaskRecoveryResolution","TaskSnapshot"]),("IdeTaskOptions.tsx","ideTypes.ts",["ValidationCommand","IdeOptions"])]:
    for name in names:
        TS_NOTES["apps/desktop/shared/"+new+":"+name]=TS_NOTES.pop("apps/desktop/src/"+old+":"+name,TS_NOTES.get(name,""))

for name in ("IdeOptions","ModelUsageSnapshot","RequestBudgetSnapshot","TaskRecoveryItem","TaskRecoveryResolution","ValidationCommand"):
    TS_NOTES.pop(name,None)


# Этап 8: необязательные, ограниченные пользовательские возможности IDE.
FILE_NOTES.update({
 'agent/optional_process.py':'Без-shell subprocess с allowlist окружения, bounded output, общим deadline и закрытием дерева дочерних процессов.',
 'agent/readonly_research.py':'Отдельный readonly контекст: до 6 фрагментов/12000 символов, один HTTP запрос без tools/retry, cancel и usage.',
 'agent/language_diagnostics.py':'Настоящий stdio LSP initialize/didOpen/publishDiagnostics; отказ server edits/commands, bounded framing и завершение процесса.',
 'agent/managed_worktrees.py':'Пользовательские Git worktrees из HEAD, receipts владения, список/diff/open и удаление только неизменённой копии.',
 'agent/container_runner.py':'Opt-in Linux Docker runner: readonly bind, без сети/pull, CPU/RAM/PID лимиты, отдельное approval и cleanup daemon container.',
 'core/python/optional_ide_service.py':'Настройки выключенных по умолчанию возможностей, один фоновый job, shared inference lease, отмена и независимые адаптеры.',
 'apps/desktop/shared/optionalTypes.ts':'Типы настроек, discriminated requests и публичных результатов дополнительных IDE операций.',
 'apps/desktop/src/OptionalIdePanel.tsx':'Модальная тематическая панель исследователя/LSP/worktrees/изоляции с бюджетами, подтверждением, отменой и явным добавлением отчёта в задачу.',
 'tests/test_optional_ide.py':'14 контрактов опциональности, бюджета, реального LSP/Git, недоверенных server edits, удаления и container argv/cleanup.',
 'tests/fixtures/lsp_diagnostics.py':'Локальный LSP fixture: чужой URI, попытка applyEdit, диагностика после отказа и режим зависшего stdin.',
 'tests/electron/optional-ide-smoke.cjs':'Реальный UI/Core workflow исследования, LSP, создания/отказа удаления/открытия worktree и панели Docker; отдельный профиль.',
})
register('agent/optional_process.py', """
process_env | Передаёт дочерним процессам системное окружение из allowlist без API/Telegram ключей и GIT/Docker overrides.
stop_process | Закрывает Windows Job или POSIX process group, убивает оставшийся процесс и ограниченно ждёт exit.
run_bounded | Запускает argv без shell, ограничивает сохранённый stdout, наблюдает OperationContext и возвращает exit/cancel/elapsed.
run_bounded.read | Дренирует pipe до EOF, сохраняя не более limit bytes и полный счётчик для truncated.
""")
register('agent/readonly_research.py', """
collect_sources | Lexical поиск до трёх слов, fallback имён, исключение распространённых credential файлов, до 6 range excerpts/12000 символов.
request_research | Единственный bounded HTTP запрос Chat/Responses без action tools; проверяет payload budget и возвращает complete/usage без исходных credentials.
research_async | Соревнуется с общим cancel/deadline; закрывает обе async tasks и HTTP при завершении.
research | Проверяет вопрос и модель, собирает источники, запускает запрос и возвращает path/line/SHA anchors и метрики.
""")
register('agent/language_diagnostics.py', """
read_frame | Читает Content-Length JSON-RPC с пределами 8КБ заголовка/1МБ тела; неполный frame отклоняется.
write_frame | Кодирует JSON-RPC UTF-8 и длину в байтах, flush выполняется worker-писателем.
diagnose | Ограниченная сессия настоящего LSP для сохранённого файла; чужие URI/версии игнорируются, server requests отклоняются, результат помечается stale при изменении файла.
diagnose.read | Читает bounded frames в ограниченную очередь, сообщает о закрытии транспорта без блокировки bridge.
diagnose.write | Единственный владелец stdin; потенциально зависшая запись прерывается уничтожением процесса по deadline.
diagnose.send | Ставит JSON-RPC в очередь без блокировки, переполнение явно отклоняет.
""")
register('agent/managed_worktrees.py', """
git_path | Находит установленный Git через LCA_GIT или PATH; не устанавливает зависимости.
ManagedWorktrees | Управляет только созданными приложением checkout receipts; основной репозиторий и commits не удаляет.
ManagedWorktrees._records | Читает JSON реестр владения либо возвращает пустой список; повреждение не замалчивается.
ManagedWorktrees._git | Запускает bounded Git без hooks/fsmonitor/submodule recursion и prompt, с Windows longpaths; ошибка/обрезка требуют проверки.
ManagedWorktrees.repository | Требует выбранный Git top-level; для управляемой копии сверяет common-dir и находит исходного владельца.
ManagedWorktrees.list | Сопоставляет scoped receipts с реальной porcelain -z регистрацией Git.
ManagedWorktrees._target | Проверяет UUID, конечное имя и containment пути внутри каталога управляемых копий.
ManagedWorktrees.create | Сохраняет creating receipt до detached checkout из исходного HEAD; незавершённый effect помечает needs_review и не повторяет.
ManagedWorktrees.get | Требует owned ID выбранного репозитория, регистрацию и одинаковый git-common-dir, защищает от подменённого пути.
ManagedWorktrees.diff | Возвращает bounded status и diff HEAD без external diff/textconv; новые файлы видны в status.
ManagedWorktrees.remove | Не удаляет открытую/грязную копию, ignored/untracked файлы и новые commits; вызывает native Git remove без force только после проверок.
""")
register('agent/container_runner.py', """
container_command | Строит фиксированные Docker restrictions; user program/image/argv не становятся runtime options, cwd проверен внутри root.
container_status | Без установки/pull проверяет наличие Docker и Linux engine, отдельно сообщает только наличие wsl executable.
run_container | Показывает точный runtime proposal, требует approval, проверяет локальный образ, ограничивает время и удаляет только свой UUID container даже после отмены CLI.
""")
register('core/python/optional_ide_service.py', """
validate_settings | Строго проверяет четыре группы, boolean, поля и бюджеты, отвергает произвольные shell/mount параметры.
OptionalIdeService | Владеет опциональными настройками и одним job; не встраивает обязательную цепочку моделей в AgentEngine.
OptionalIdeService.catalog | Возвращает настройки, warning, job и shared gate status без credentials.
OptionalIdeService.configure | Только при idle атомарно сохраняет проверенные настройки; выключения применяются к следующим запросам.
OptionalIdeService.start | Проверяет root/opt-in/подтверждение, получает lease исследователя и запускает worker, сохраняя отзывчивость JSON-lines bridge.
OptionalIdeService.start.run | Выполняет один адаптер над снимком settings/root/config; в finally освобождает свой gate и возвращает результат исходному RPC.
OptionalIdeService.cancel | Сигнализирует своему job без преждевременного освобождения модели или повтора effect.
OptionalIdeService.command | Направляет обычную approved IDE command в container adapter при включённой изоляции.
OptionalIdeService.shutdown | Закрывает вход новых jobs, отменяет текущий и ограниченно ждёт worker.
""")
register('tests/fixtures/lsp_diagnostics.py', """
main | Обслуживает реальные JSON-RPC frames fixture; выдаёт диагностику только после отказа applyEdit, --stall не читает stdin для проверки отмены.
""")
register('tests/test_optional_ide.py', """
OptionalIdeTests.model | Поднимает локальный HTTP fixture и конфигурацию модели; release/shutdown зарегистрированы в cleanup.
OptionalIdeTests.service | Создаёт isolated optional service с настоящим inference gate и idle guard.
OptionalIdeTests.service.idle | Не позволяет менять scope/settings во время фонового optional job.
OptionalIdeTests.git | Запускает только тестовый Git в disposable репозитории и проверяет exit code.
OptionalIdeTests.repository | Создаёт минимальный initial commit и manager отдельного каталога без обращения к проектному Git.
OptionalIdeTests.test_container_denial_never_contacts_docker_and_cancel_cleans_daemon_container.execute | Fixture Docker argv responses для проверки отказа/cleanup без установки Docker.
""")
TEST_PURPOSES.update({
 'optional_features_default_off_and_require_exact_confirmation':'все возможности выключены; запуск без opt-in и строковое confirmed отклоняются.',
 'optional_settings_reject_shell_fields_and_unbounded_budgets':'таймауты, image options, пустой LSP program и произвольные mounts не проходят настройки.',
 'research_one_request_bounded_sources_no_tools_and_no_secret_excerpt':'один настоящий HTTP запрос без tools/credential excerpts; bounded источники и неизменённый проект.',
 'research_offline_budget_refuses_before_http':'payload не помещается в окно и отклоняется до контакта с моделью.',
 'research_holds_shared_gate_until_cancelled_worker_exits':'исследователь удерживает единый gate, отмена закрывает HTTP и освобождает владельца только после worker.',
 'lsp_real_frames_reports_location_and_refuses_server_edit':'реальный LSP stderr/stdin transport, location, отбрасывание чужого URI и отказ workspace/applyEdit.',
 'lsp_deadline_interrupts_server_that_never_reads_stdin':'deadline закрывает зависший server и заблокированную большую запись didOpen без зависания bridge.',
 'lsp_frame_limits_and_foreign_paths_are_rejected':'oversized/truncated frame и файл вне root отклоняются.',
 'worktree_create_diff_remove_keeps_primary_checkout_unchanged':'реальный detached checkout, shared список из копии, запрет удаления открытой копии и сохранность исходных ручных правок.',
 'worktree_refuses_unknown_id_dirty_untracked_and_new_commits':'чужой ID, новые файлы и commits не допускают удаления; настоящий diff сохраняется.',
 'worktree_owned_path_cannot_escape_managed_directory':'подменённый receipt не разрешает путь за пределами managed directory.',
 'container_argv_fixed_boundaries_no_network_no_host_write':'фиксированные сетевые/файловые/CPU/user ограничения и проверенный cwd.',
 'container_denial_never_contacts_docker_and_cancel_cleans_daemon_container':'отказ не контактирует с Docker; отмена всегда удаляет daemon container по выданному UUID.',
 'bounded_process_deadline_kills_child_and_filters_environment':'дочерний процесс заканчивается по сроку, ключи не передаются через env.',
 'optional_lsp_is_opt_in_cancellable_and_bridge_stays_responsive':'настоящий Core process отвечает health/cancel во время LSP, блокирует смену проекта и затем принимает повторный успешный запуск.',
})
TS_NOTES.update({
 'OptionalSettings':'Четыре opt-in группы с явными пределами и пользовательской конфигурацией сервера/образа.',
 'OptionalRequest':'Discriminated union research/diagnostics/worktrees/runtime; эффекты требуют literal true confirmation.',
 'ManagedWorktree':'Публичный ownership receipt с commit/status/path и фактической регистрацией.',
 'LanguageDiagnostic':'Нормализованная 1-based строка/колонка, severity/message/source от сервера.',
 'OptionalResult':'Ограниченный результат фонового IDE RPC с root correlation, метриками, sources/diagnostics/worktrees.',
 'OptionalCatalog':'Типизированные settings и состояние единого inference gate без ключей.',
 'OptionalIdePanel':'Нативный modal dialog с явными opt-in, сохранением settings, stop, отчётом, diagnostics и подтверждёнными Git effects.',
 'apps/desktop/src/OptionalIdePanel.tsx:OptionalIdePanel.save':'Сохраняет проверенные настройки и блокирует повторный клик через ref до завершения IPC.',
 'apps/desktop/src/OptionalIdePanel.tsx:OptionalIdePanel.run':'Один job, root correlation, ошибки и обновление списков без автоотправки отчёта модели.',
 'apps/desktop/src/OptionalIdePanel.tsx:OptionalIdePanel.confirm':'Создаёт/удаляет копию только по отдельному явному подтверждению, затем обновляет список.',
 'apps/desktop/src/App.tsx:App.openWorktree':'Через проверенный owned ID открывает копию, сбрасывает editor/chat projection и загружает scoped каталог.',
})

TS_NOTES.update({
 'optionalSettings':'Читает typed catalog дополнительных возможностей через preload IPC.',
 'configureOptionalIde':'Передаёт четыре группы проверяемых opt-in настроек Core без секретов.',
 'runOptionalIde':'Запускает typed пользовательский IDE job через отменяемый длительный IPC.',
 'cancelOptionalIde':'Сигнализирует отмену текущего optional job, не освобождая gate преждевременно.',
 'openManagedWorktree':'Открывает только проверенный owned Git ID; main не принимает произвольный путь renderer.',
 'tests/electron/optional-ide-smoke.cjs:js':'Выполняет renderer JavaScript только в тестовом Electron окне.',
 'tests/electron/optional-ide-smoke.cjs:poll':'Ожидает наблюдаемое DOM условие с ограниченным timeout.',
 'tests/electron/optional-ide-smoke.cjs:click':'Нажимает известный тестовый элемент и даёт React применить состояние.',
 'tests/electron/optional-ide-smoke.cjs:button':'Находит точную подпись кнопки внутри optional dialog.',
 'tests/electron/optional-ide-smoke.cjs:input':'Меняет controlled input через native setter и input event.',
 'tests/electron/optional-ide-smoke.cjs:save':'Сохраняет settings UI и ждёт подтверждение Core.',
 'tests/electron/optional-ide-smoke.cjs:capture':'Дожидается repaint и сохраняет PNG реального окна.',
 'tests/electron/optional-ide-smoke.cjs:finish':'Сохраняет результат и диагностический screenshot, закрывает локальный fixture и тестовое приложение.',
})

TS_NOTES["tests/electron/optional-ide-smoke.cjs:BrowserWindow.prototype.loadURL"]="Открывает собранный renderer из dist только в изолированном optional IDE smoke."

TS_NOTES.update({
 'apps/desktop/electron/desktopLola.ts:status':'IPC callback возвращает bounded снимок настроек/состояния desktop companion.',
 'apps/desktop/electron/desktopLola.ts:action':'IPC callback проверяет и передаёт только allowlist пользовательских действий; настройки сначала показывают Neutral.',
 'apps/desktop/electron/desktopLola.ts:main':'IPC callback показывает главное окно Neutral.',
 'apps/desktop/electron/desktopLola.ts:menu':'IPC callback открывает нативное контекстное меню спутника.',
 'apps/desktop/electron/desktopLola.ts:hover':'IPC callback меняет передачу кликов через прозрачное окно.',
 'apps/desktop/electron/desktopLola.ts:move':'IPC callback применяет ограниченную проверенную дельту перемещения.',
 'apps/desktop/electron/desktopLola.ts:click':'Обработчик пункта native Tray выполняет только заранее заданное действие меню.',
 'apps/desktop/electron/lolaPreload.ts:status':'Запрашивает bounded snapshot из main process.',
 'apps/desktop/electron/lolaPreload.ts:action':'Отправляет одно типизированное действие companion allowlist.',
 'apps/desktop/electron/lolaPreload.ts:showMain':'Просит main process показать Neutral без передачи произвольных аргументов.',
 'apps/desktop/electron/lolaPreload.ts:menu':'Показывает нативное меню Tray/спутника.',
 'apps/desktop/electron/lolaPreload.ts:hover':'Сообщает main process о попадании pointer в интерактивную зону.',
 'apps/desktop/electron/lolaPreload.ts:move':'Передаёт ограниченную дельту pointer для нативного перемещения окна.',
 'apps/desktop/electron/lolaPreload.ts:onState':'Подписывает React на bounded визуальные обновления и возвращает disposer.',
 'apps/desktop/electron/lolaPreload.ts:onState.receive':'Передаёт проверенный IPC payload callback UI.',
 'LolaAnimationState':'Семь UI-анимационных состояний без связи с модельными командами.',
 'LolaDesktopSettings':'Persisted opt-in настройки режима, размера, анимации, click-through и положения.',
 'LolaDesktopFrame':'Bounded отображаемые подпись/ответ и наблюдаемые статусы голоса/работы.',
 'LolaDesktopAction':'Allowlist пользовательского ask/record/stop/settings действия.',
 'LolaVoiceAction':'Одноразовая команда основному владельцу VoicePanel.',
 'validateLolaSettings':'Fail-closed проверка prefs спутника, режима, диапазона размера и координат.',
 'validateLolaFrame':'Ограничивает длину текста и enum состояния перед renderer-передачей.',
 'fitLolaBounds':'Размещает окно в доступной области выбранного монитора.',
 'apps/desktop/src/DesktopLolaView.tsx:DesktopLolaView':'Отдельный overlay UI для компактного вопроса/ответа, drag и контролов существующего voice owner.',
 'apps/desktop/src/DesktopLolaView.tsx:DesktopLolaView.change':'Обновляет движение персонажа при смене системного reduced-motion preference.',
 'apps/desktop/src/DesktopLolaView.tsx:DesktopLolaView.pointer':'Определяет интерактивные hit areas для click-through native окна.',
 'apps/desktop/src/DesktopLolaView.tsx:DesktopLolaView.leave':'Возвращает сквозные клики, когда окно теряет pointer focus.',
 'apps/desktop/src/DesktopLolaView.tsx:DesktopLolaView.action':'Отправляет allowlisted команду и локально показывает bounded ошибку.',
 'apps/desktop/src/DesktopLolaSettings.tsx:DesktopLolaSettings':'Общая пользовательская настройка opt-in спутника из главного Voice settings.',
 'apps/desktop/src/DesktopLolaSettings.tsx:DesktopLolaSettings.save':'Применяет валидацию в main process и показывает результат сохранения.',
 'apps/desktop/electron/main.ts:showMain':'Создаёт или восстанавливает основное окно при выборе действий спутника.',
 'apps/desktop/electron/main.ts:dispatch':'Направляет ограниченное действие UI через уже существующий основной event bridge.',
 'apps/desktop/electron/main.ts:notify':'Обновляет main renderer и background throttling при сохранении настройки спутника.',
 'apps/desktop/electron/main.ts:quit':'Tray callback завершает приложение через штатный quit lifecycle.',
 'apps/desktop/src/App.tsx:App.desktopAction.current':'Связывает ограниченные действия спутника с единственным App/VoicePanel без второго аудиоконтроллера.',
 'apps/desktop/src/WakeListener.tsx:WakeListener.stop':'Отключает wake listening после команды Stop, пришедшей через спутника.',
 'getDesktopLola':'Читает сохранённые настройки и presentation состояния спутника.',
 'configureDesktopLola':'Передаёт настройки спутника main process для проверки и записи.',
 'presentDesktopLola':'Передаёт main process только bounded UI presentation frame.',
 'tests/electron/lola-desktop-smoke.cjs:js':'Выполняет UI проверку в изолированном тестовом окне.',
 'tests/electron/lola-desktop-smoke.cjs:poll':'Ожидает DOM/API условие с жёстким timeout.',
 'tests/electron/lola-desktop-smoke.cjs:input':'Задаёт controlled input через native DOM setter в тестовом окне.',
 'tests/electron/lola-desktop-smoke.cjs:capture':'Сохраняет кадр настоящего изолированного Electron окна для визуальной проверки.',
 'tests/electron/lola-desktop-smoke.cjs:finish':'Сохраняет machine-readable результат, закрывает fixture и завершает тестовое приложение.',
 'tests/electron/lola-desktop-smoke.cjs:BrowserWindow.prototype.show':'Подавляет показ тестового основного окна, чтобы GUI smoke не вмешивался в desktop session.',
 'tests/electron/lola-desktop-smoke.cjs:BrowserWindow.prototype.showInactive':'Делает тестовое окно почти прозрачным при сохранении настоящего нативного lifecycle.',
 'tests/electron/lola-desktop-smoke.cjs:BrowserWindow.prototype.loadURL':'Направляет dev entrypoint на собранные локальные тестовые страницы.',
 'tests/electron/lola-desktop-smoke.cjs:dialog.showMessageBox':'Автоматизирует только тестовый discard confirmation.',
 'tests/electron/lola-desktop-smoke.cjs:ipcMain.handle':'Перехватывает ссылки на handlers для проверки настоящей sender authorization.',
 'tests/electron/lola-desktop-smoke.cjs:BrowserWindow.prototype.setIgnoreMouseEvents':'Записывает click-through решения настоящего окна для утверждений теста.',
 'tests/electron/lola-desktop-smoke.cjs:childProcess.spawn':'Считает фактические старты Core, не подменяя сам процесс.',
})

FILE_NOTES.update({
 'agent/response_outcome.py':'Общий контракт терминального ответа модели: complete/incomplete/refused/cancelled/error; EOF не становится успешным stop.',
 'agent/workspace_revision.py':'Ограниченный content fingerprint исходников и сравнение проверяемых receipt с текущей ревизией проекта.',
 'agent/workspace_access.py':'Общая политика автоматического доступа: секретные пути, .neutralignore, точечные пользовательские исключения и повторная проверка истории.',
 'core/python/background_job.py':'Один отменяемый maintenance worker вне синхронного dispatch/TaskService.lock.',
 'apps/desktop/src/WorkspaceAccessSettings.tsx':'Форма точечных разрешений файлов для модели в возможностях IDE с явным подтверждением передачи содержимого.',
 'tests/test_stage9_reliability.py':'Регрессии аудита A1–A5: JSON/EOF/revision/access/LSP и живой JSON-lines bridge во время backup.',
})
register('agent/response_outcome.py', '''
ModelResponseOutcome | Неизменяемые status/finish_reason/reason; нормализует результат независимо от провайдера.
ModelResponseOutcome.classify | Использует явную terminal reason, отказ/отмену/ошибку; неизвестный EOF классифицирует incomplete.
ModelResponseOutcome.snapshot | Возвращает JSON-safe состояние для checkpoint и интерфейса.
''')
register('agent/json_tools.py', '''
strict_json_loads | Разбирает весь JSON, запрещает повторные ключи и NaN/Infinity на всех уровнях.
strict_json_loads.pairs | Собирает объект и отклоняет повторный ключ вместо молчаливой замены аргумента.
strict_json_loads.constant | Отклоняет нестандартные числовые константы JSON.
decode_envelope | Принимает только anchored объект с явными совместимыми wrappers; не извлекает команды из пояснений.
parse_tool_json | Проверяет весь envelope и allowlist; принимает строгий neutral.action.v1 и прежние полные envelopes, отвергает хвост/второй объект/повторные ключи.
''')
register('agent/workspace_revision.py', '''
WorkspaceRevisionService | Общая источник-ревизия для проверок, сохранений редактора, внешних изменений и recovery.
WorkspaceRevisionService.capture | Хеширует ограниченное дерево исходников; ошибки/лимиты/изменение во время чтения дают incomplete, а не чистый fingerprint.
evidence_matches | Требует совпадение полного content digest, версии/области и rollback generation.
''')
register('agent/workspace_access.py', '''
WorkspaceAccessPolicy | Загружает доверенные точечные разрешения вне проекта и дополнительные deny globs из .neutralignore.
WorkspaceAccessPolicy.allows | Проверяет каноническую цель, стандартные секретные имена и маски; точечное UI-разрешение не распространяется на папку.
WorkspaceAccessPolicy.require | Возвращает разрешённый путь или отказ; модели запрещено менять .neutralignore через file tools.
WorkspaceAccessPolicy.catalog | Возвращает только root/пути исключений/маски, не содержимое защищённых файлов.
WorkspaceAccessPolicy.configure | Требует literal true согласие, существующие отдельные файлы внутри root; атомарно сохраняет до 64 исключений.
filter_model_history | Повторно применяет права к известным файловым tool results и цепочкам read_tool_result, сохраняя исходную историю.
filter_model_history.denied | Считает некорректный или выходящий путь непригодным для автоматического контекста.
''')
register('core/python/background_job.py', '''
BackgroundJob | Владеет одним daemon maintenance worker и OperationContext, не занимает inference gate.
BackgroundJob.start | Отклоняет дубликат/закрытый сервис, фиксирует callback исходного RPC и запускает работу вне bridge thread.
BackgroundJob.start.run | Возвращает нормализованный успех/ошибку исходному запросу после работы и проверки отмены.
BackgroundJob.cancel | Сигнализирует отмену, не освобождая слот живого worker заранее.
BackgroundJob.shutdown | Закрывает вход, отменяет операцию и ограниченно ждёт завершения.
''')
register('agent/language_diagnostics.py', '''
normalize_diagnostics | Проверяет структуру/позиции; неверный payload не превращается в пустой отчёт без ошибок.
''')
register('agent/storage.py', '''
Storage.backup.check | Проверяет отмену/deadline между SQLite pages, записями и ZIP chunks, включая точку до замены destination.
Storage.backup.copy | Копирует ZIP entry порциями 64 КБ с сохранением метаданных и проверкой отмены.
''')
register('core/python/bridge.py', '''
main.maintain | Выполняет snapshot/report в выделенном maintenance worker; тяжёлая операция не держит tasks.lock.
''')
register('core/python/task_service.py', '''
TaskService.workspace_changed | После ручной записи пересчитывает evidence, сохраняет checkpoint и публикует отдельное scoped событие для idle UI.
''')
TEST_PURPOSES.update({
 'eof_without_terminal_reason_preserves_partial_and_pauses':'EOF сохраняет частичный текст, выставляет incomplete и paused вместо completed.',
 'eof_without_terminal_reason_never_executes_native_call':'Полные аргументы native call без terminal reason не исполняются и не попадают в canonical tool block.',
 'json_rejects_suffix_second_object_duplicate_keys_and_nan':'хвост, второй объект, повторные ключи и NaN не превращаются в команды; anchored compatibility wrapper остаётся.',
 'versioned_json_and_incomplete_stream_share_terminal_contract':'v1 action/final корректны; EOF JSON не синтезирует успешный tool_calls.',
 'editor_and_external_changes_invalidate_content_evidence':'ручной EditorService save и same-size запись с восстановленным mtime инвалидируют checks.',
 'legacy_and_over_budget_revisions_cannot_certify_checks':'старые receipts без content hash и превышенный бюджет fingerprint не получают зелёный статус.',
 'shared_access_policy_requires_exact_user_exception':'read/range/search/list используют общую политику; ручной editor доступен; точечный grant/revoke требует UI consent.',
 'delayed_lsp_replaces_initial_empty_and_pull_is_preferred':'реальный subprocess выдаёт пустой push и позднюю ошибку; pull даёт явный полный отчёт.',
 'revocation_filters_known_saved_results_without_deleting_chat':'отзыв доступа скрывает содержимое и read_tool_result-копию в новых запросах, сохраняя пользовательскую историю.',
 'background_job_cancel_and_duplicate_are_bounded':'один worker, отказ дублю и коррелированная отмена без преждевременного освобождения слота.',
 'cancelled_backup_preserves_existing_destination':'отмена не заменяет имеющийся архив пользователя.',
 'real_bridge_health_and_cancel_respond_during_backup':'настоящий subprocess отвечает health/cancel, пока backup worker ожидает; исходный RPC получает отказ после отмены.',
})
register('tests/test_stage9_reliability.py', '''
Stage9Tests.test_background_job_cancel_and_duplicate_are_bounded.work | Fixture ожидает отмену OperationContext и не блокирует вызывающий поток.
Stage9Tests.test_background_job_cancel_and_duplicate_are_bounded.respond | Сохраняет ответ worker и завершает ожидание теста.
Stage9Tests.test_real_bridge_health_and_cancel_respond_during_backup.read | Читает JSON-lines ответы настоящего Core subprocess в очередь.
Stage9Tests.test_real_bridge_health_and_cancel_respond_during_backup.send | Отправляет один тестовый RPC без shell.
''')
TS_NOTES.update({
 'workspaceAccess':'Читает правила автоматического файлового доступа для выбранного Core проекта.',
 'configureWorkspaceAccess':'Передаёт точные пути и явное согласие; модель этого API не получает.',
 'cancelStorageBackup':'Просит Core отменить текущий maintenance job без блокировки UI.',
 'WorkspaceAccessSettings':'Форма точечных исключений с уведомлением о передаче содержимого серверу модели.',
 'apps/desktop/src/WorkspaceAccessSettings.tsx:WorkspaceAccessSettings.save':'Проверяет согласие, отправляет grants и игнорирует поздний ответ при смене проекта.',
})

register('agent/tool_executor.py', '''
ToolExecutor._access_guard | Повторно проверяет файловые пути по текущей policy до preview и перед effect после approval.
''')
register('tests/test_core_reliability.py', '''
CoreReliabilityTests.test_access_policy_is_rechecked_after_file_approval.approve | Меняет .neutralignore во время fixture approval для проверки отказа записи.
''')
TEST_PURPOSES.update({
 'access_policy_is_rechecked_after_file_approval':'новое правило во время просмотра diff блокирует ещё не выполненную запись.',
 'policy_metadata_cannot_be_granted_or_changed_as_a_project_file':'модель не может получить grant на собственный файл разрешений даже при выборе профиля как проекта.',
 'backup_commit_is_not_relabelled_cancelled_after_replace':'реальный ZIP сохранён атомарно; отмена сразу после replace не скрывает уже совершённый commit.',
})
register('tests/test_stage9_reliability.py', '''
Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.commit | После настоящего os.replace сигнализирует позднюю отмену для проверки границы commit.
Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.work | Создаёт настоящий backup с подменой только точки фиксации.
Stage9Tests.test_backup_commit_is_not_relabelled_cancelled_after_replace.respond | Собирает ответ фоновой операции после позднего cancel.
''')

FILE_NOTES.update({
 'agent/auto_budget.py':'Read-only определение фактического окна LM Studio/Ollama/llama.cpp, bounded cache, разбор context rejection и SDK tokenizer только уже загруженного экземпляра.',
 'tools/benchmark_agent.py':'Baseline 20a: owned synthetic repositories, frozen Agent/Core sources, real serial native/JSON runs, held-out arithmetic/diff/provenance/recovery checks and reports without editing user projects.',
 'tests/test_agent_benchmark.py':'Проверка владения fixtures, независимого oracle, строгого отчёта и запрета считать угаданный путь успешным поиском.',
 'docs.zip':'Локальный пользовательский архив документации; сохранён без изменений, приложение не использует его как исходник или настройку.',
 'tests/test_auto_budget.py':'Автонастройка без настоящей LLM: metadata/400/SSE, русский текст, каталог, большие выполненные записи и защита pending code.',
 'apps/desktop/src/assets/lola-chibi-atlas-v2.png':'Новый исходный transparent PNG атлас 28 полных поз Лолы; не изменяется renderer-кодом.',
 'apps/desktop/src/assets/lola-chibi-atlas-v2.json':'Проверенные source rectangles всех 28 персонажей: SVG переносит их целиком на общий canvas с полями.',
 'apps/desktop/src/assets/lola-chibi-atlas-v2.prompt.md':'Точный imagegen prompt и происхождение версии v2; исходный PNG сохранён без растровых правок.',
})
register('agent/auto_budget.py', '''
local_endpoint | Определяет loopback/private/.local адрес для автоматической локальной task policy без DNS-запроса.
valid_window | Принимает только целое окно 512–1048576, исключая bool и некорректные metadata.
loaded_profile | Выбирает контекст выбранного загруженного экземпляра; trained maximum не подменяет размер слота.
discover_profile | Выполняет bounded GET metadata к настроенному origin, кэширует на 30 с; не запускает inference/load/unload.
discover_profile.read | Ограничивает размер JSON 512 КБ и игнорирует неподдерживаемые endpoints/некорректные ответы.
context_rejection | Извлекает только явно подписанное окно из HTTP 400/413/422 до начала потока; чужие числа не использует.
LoadedTokenizer | Владеет необязательным SDK handle уже загруженной модели; не вызывает model()/load().
LoadedTokenizer.connect | На anonymous root/v1 HTTP LM Studio находит handle через list_loaded с timeout; освобождает неиспользованный client.
LoadedTokenizer.count | Считает токены сериализованного prompt material на сервере, проверяя отмену до и после bounded RPC.
LoadedTokenizer.close | Освобождает SDK sockets/threads вместе с общим ModelClient.
''')
register('agent/model_client.py', '''
ModelClient.prepare_budget | Разрешает окно до запроса и после JIT-загрузки; подключает tokenizer без загрузки или изменения GPU-параметров.
''')
register('agent/request_budget.py', '''
estimated_tokens | Взвешенная fallback оценка ASCII/кириллицы/CJK/emoji с JSON framing; не равняет UTF-8 байты токенам.
compact_completed_calls | Только полностью парные исторические большие write/patch заменяет assistant-архивом с SHA/результатами/anchors; pending calls и canonical не меняет.
RequestBudget.configure | Принимает actual profile и необязательный counter; очищает bounded cache при смене профиля.
RequestBudget.learn_rejection | После явного pre-stream отказа уточняет окно и повышает запас, не повторяя уже начатый ответ или инструмент.
RequestBudget.observe_usage | Повышает оценочный запас, если сервер сообщил больше входных токенов, чем ожидалось.
''')
register('tests/test_auto_budget.py', '''
AutoBudgetTests.server | Запускает отдельный HTTP metadata/context-rejection/SSE fixture и регистрирует очистку.
AutoBudgetTests.test_schema_catalog_preserves_selected_tool_and_human_request.tool | Создаёт намеренно большую synthetic schema для проверки отложенной загрузки.
''')
TEST_PURPOSES.update({
 'loaded_context_is_not_training_maximum_or_another_instance':'выбранный loaded instance задаёт окно вместо trained maximum/чужого слота.',
 'fixture_is_deterministic_and_reset_touches_only_owned_sources':'reset восстанавливает только собственные fixture files и отказывается от каталога без правильного marker.',
 'initial_bug_fails_and_real_minimal_fix_passes':'oracle отвергает исходный баг и принимает минимальную правильную правку независимо от ответа модели.',
 'multifile_requires_definition_and_caller':'переименование требует согласованного definition/caller; добавленные эффекты module не считаются корректным diff.',
 'model_code_is_not_imported_or_executed_by_oracle':'произвольные вызовы, module statements и изменённые сигнатуры отклоняются без исполнения кода модели.',
 'search_reports_coverage_and_real_paths':'baseline измеряет настоящий поиск с source paths и отдельной полнотой обхода.',
 'report_serialization_is_strict_and_atomic':'UTF-8 отчёт атомарен; NaN не повреждает уже записанный результат.',
 'censored_experiment_is_distinct_from_incorrect_code':'правильная правка на cutoff эксперимента отделяется от неверного diff и полного E2E завершения.',
 'correct_location_without_successful_tool_evidence_is_not_success':'угаданный путь или неуспешное чтение не подтверждают поиск исходника.',
 'location_oracle_does_not_accept_numeric_or_path_prefixes':'строка 10 и совпадение суффикса чужого пути не подменяют точный source location :1.',
 'discovery_is_cached_metadata_only':'определение окна использует только GET и cache, без генерации/управления моделями.',
 'russian_prompt_fits_without_byte_equals_token_false_block':'русский prompt сохраняется целиком и помещается по токенам, даже когда байтов больше окна.',
 'auto_normalizes_irrelevant_manual_settings':'устаревшие невалидные числовые поля не ломают auto; manual остаётся строгим.',
 'auto_provisional_window_does_not_inherit_old_manual_cap':'неизвестный сервер получает временный auto profile, не устаревший ручной cap 4K; исходные prefs не меняются.',
 'schema_catalog_preserves_selected_tool_and_human_request':'редкие schemas откладываются, обязательный tool и текущий запрос сохраняются.',
 'mandatory_prompt_never_disappears_to_claim_fit':'физически невозможный запрос не обрезается ради ложного fits.',
 'rejected_pre_stream_request_is_adapted_once_without_replaying_effects':'реальный HTTP 400 уточняет окно и уменьшает запрос до первого SSE.',
 'error_parser_does_not_treat_unrelated_numbers_as_context':'обратная связь допускается только для подписанного bounded размера окна.',
 'sdk_uses_only_loaded_handles_and_token_count_is_cached':'SDK никогда не загружает модель; один токенизированный payload повторно берётся из cache.',
 'completed_large_write_is_projected_but_pending_code_is_never_trimmed':'выполненная запись 40+ КБ помещается квитанцией в 4K; pending код остаётся нетронутым.',
 'small_slot_keeps_instructions_and_uses_minimal_tool_catalog':'малое окно IDE откладывает даже core schemas, сохраняя полные инструкции и место для ответа.',
 'auto_local_continues_text_without_duplicate_canonical_fragments':'length продолжается одним итоговым сообщением без старого таймера локальной задачи.',
 'auto_local_retries_truncated_call_without_executing_its_fragment':'неполный вызов не выполняется; исполняется только заново полученный полный вызов.',
 'auto_continuation_keeps_one_ui_message_and_loaded_context':'реальные metadata/SSE/Core сохраняют один message_id и canonical ответ, используя detected 4K и игнорируя старые лимиты циклов.',
})

FILE_NOTES['tests/test_json_compatibility.py']='JSON compatibility: bounded regeneration, строгие terminal outcomes, настоящий SSE и неизменность approval/budget/Stop.'
register('tests/test_json_compatibility.py', '''
action | Формирует полный action envelope для детерминированных SSE ответов.
Source.__iter__ | Выдаёт один chunk с заданным terminal evidence и refusal.
Source.close | Делает закрытие источника наблюдаемым для теста repair.
JsonCompatibilityTests.server | Запускает временный loopback SSE endpoint с очередью ответов и очисткой.
JsonCompatibilityTests.test_prose_is_regenerated_never_extracted.repair | Возвращает отдельный корректный read вместо скрытого в пояснении write.
JsonCompatibilityTests.test_repairs_are_bounded_and_ambiguous_batches_never_yield.repair | Записывает номер попытки и снова выдаёт ошибочный batch для проверки границы.
JsonCompatibilityTests.test_transport_cancellation_is_not_protocol_repair.Cancelled.__iter__ | Имитирует отмену получения ответа до протокольного разбора.
JsonCompatibilityTests.test_repaired_write_still_waits_for_approval.reject | Проверяет неизменность файла до approval и отклоняет запись.
''')
register('agent/json_tools.py', '''
JsonToolStream._read_response | Буферизует один bounded ответ до явного terminal outcome; EOF/length/refusal не входят в protocol repair.
''')
register('agent/model_client.py', '''
ModelClient._repair_json | Повторно генерирует отклонённый, неисполненный ответ через fit/check и Stop; учитывает запрос и repair без изменения canonical history.
''')
TEST_PURPOSES.update({
 'prose_is_regenerated_never_extracted':'команда внутри пояснения не исполняется; наружу попадает только отдельный принятый ответ repair.',
 'repairs_are_bounded_and_ambiguous_batches_never_yield':'ровно до двух исправлений; валидный префикс невалидного batch не становится вызовом.',
 'incomplete_and_refused_responses_never_enter_repair':'EOF/length/refusal не запускают protocol retry и не выдают tool delta.',
 'transport_cancellation_is_not_protocol_repair':'отмена и ошибка транспортного итератора распространяются без новой генерации.',
 'required_and_none_choices_survive_regeneration':'repair не обходит обязательный инструмент и запрет инструментов в финальном ответе.',
 'request_has_one_protocol_and_compact_schemas':'canonical action в истории и инструкциях; нет native API tools/roles и мутации исходных данных.',
 'compact_core_catalog_keeps_required_and_custom_schema':'сокращаются только optional core поля; required/write/custom/MCP схемы и оригиналы сохраняются.',
 'real_transport_repairs_are_counted_fitted_and_isolated':'настоящие SSE POST/usage учитывают repair, fit сохраняет исходную задачу и canonical историю.',
 'repair_cannot_bypass_budget_or_pending_stop':'невмещаемый запрос и Stop блокируют repair до транспортного запроса.',
 'repaired_write_still_waits_for_approval':'Engine отклоняет исправленную JSON-запись через approval, файл не меняется, task usage учитывает repair.',
})

FILE_NOTES.update({
 'agent/verification_evidence.py':'Versioned evidence команд: исполнение, точная пользовательская область, before/after source witnesses, актуальность и lazy migration.',
 'tests/test_scoped_verification.py':'Реальные команды и scoped receipts: большой проект, зависимости/доступ/rollback, смена root, legacy migration и restart без повторного эффекта.',
})
register('agent/verification_evidence.py', '''
now | Возвращает UTC-время границы исполнения, отдельно от ожидания approval.
normalize_scope | Принимает workspace либо до 128 точных файлов и 128 зависимостей; отвергает абсолютные пути, traversal, glob и ADS.
configured_check | Находит только точное совпадение пользовательских check_id, program/argv/cwd и timeout.
command_scope | Возвращает scope пользователя для точной команды; произвольный вызов модели остаётся workspace.
command_digest | Связывает квитанцию с программой, argv, cwd, timeout и нормализованной областью/зависимостями.
capture_witness | Вызывает полный capture либо capture_files; связывает revision с canonical workspace id без обхода постороннего дерева для scoped.
make_receipt | Создаёт v2 immutable facts исполнения и before/after witnesses с rollback revision и generation для durable journal.
assess_evidence | Проверяет версию, command/scope binding, stable witnesses, текущие source/policy и rollback; не повышает legacy/incomplete до успеха.
assess_evidence.verdict | Формирует раздельные status/summary/coverage без утверждения полной сверки при scoped result.
migrate_evidence | При чтении старого checkpoint помечает legacy rows unverified, сохраняя exit code, raw journal и историю.
''')
register('agent/workspace_revision.py', '''
WorkspaceRevisionService.capture_files | Хеширует только объявленные сохранённые файлы с текущей access policy; отказывает ссылкам, moving files и неполной сверке.
''')
register('agent/tool_executor.py', '''
ToolExecutor.command_approval_note | Добавляет к approval точную область evidence и предупреждение, что это не ограничение доступа программы.
ToolExecutor._begin_command | После approval фиксирует исходный witness и rollback/generation до запуска эффекта.
''')
register('tests/test_scoped_verification.py', '''
ScopedVerificationTests.install | Устанавливает пользовательскую команду, scope и связанный критерий.
ScopedVerificationTests.run_check | Проводит реальный процесс через journal, executor, approval и StageVerifier.
ScopedVerificationTests.run_check.approve | Подтверждает внешнее действие в обычных границах executor и сохраняет текст области.
ScopedVerificationTests.run_check.dispatch | Вызывает run_project_command либо локальный handler теста.
''')
TS_NOTES['apps/desktop/shared/ideTypes.ts:EvidenceScope']='Пользовательская область доказательств: весь проект либо точные сохранённые файлы и объявленные зависимости.'
TEST_PURPOSES.update({
 'large_unrelated_file_does_not_block_explicit_scope':'exit=0 на выбранных файлах даёт scoped_passed без полного обхода и без project_complete.',
 'default_workspace_remains_unverified_when_tree_is_incomplete':'успех произвольной команды не повышает неполный fingerprint большого дерева до подтверждённой проверки.',
 'dependency_change_invalidates_but_unrelated_edit_does_not':'backdated изменение зависимости инвалидирует witness; посторонняя правка и generation не отравляют file scope.',
 'command_mutation_cannot_certify_post_execution_snapshot':'успешная команда, изменившая покрываемый файл между before/after, не подтверждает стабильный tested snapshot.',
 'nonzero_command_is_a_failed_criterion_not_just_stale':'связанный критерий показывает неуспешную команду как failed отдельно от актуальности исходников.',
 'check_config_and_rollback_invalidate_receipt':'смена списка зависимостей или rollback revision не позволяет принять старую квитанцию.',
 'policy_revocation_and_missing_dependency_block_cached_evidence':'новая .neutralignore или удаление зависимости запрещают использовать прежний witness.',
 'models_cannot_choose_scope_or_reuse_another_command':'модель не передаёт scope tool-аргументом; только точный пользовательский command/check_id/timeout наследует область.',
 'scope_validation_rejects_globs_escape_and_ambiguous_paths':'scope состоит из точных относительных файлов, без glob, traversal, ADS и двусмысленных разделителей.',
 'receipt_cannot_be_transplanted_to_another_workspace':'одинаковые байты в другом canonical workspace не принимаются как тот же снимок.',
 'malformed_or_incomplete_witness_is_never_success':'exit=0 не компенсирует отсутствие, неполноту или повреждённую структуру witness.',
 'legacy_checkpoint_is_unverified_without_losing_exit_or_history':'v1 fingerprint не восстанавливает commands_passed при загрузке; exit code сохраняется.',
 'receipt_survives_restart_without_reexecuting_command':'restart восстанавливает v2 receipt из журнала и сверяет scope без нового Popen.',
 'scoped_check_runs_on_large_project_and_reloads_without_model':'Core проводит checks-only/approval/save/reload выбранного файла с большим посторонним файлом и без model request.',
})

FILE_NOTES.update({
 'agent/project_index.py':'Отдельный derived SQLite/WAL cache проекта, FTS5, durable queue точных путей, watcher, incremental update и проверенный retrieval.',
 'agent/project_index_policy.py':'Per-operation WorkspaceAccessPolicy и ancestor .gitignore с GitWildMatch, nested rules и policy provenance.',
 'agent/project_symbols.py':'Синтаксические определения/импорты Python AST и JS/TS/TSX Tree-sitter; никакого выполнения исходников или semantic reference resolution.',
 'tests/test_project_index.py':'Изолированные AST/TS/FTS/watcher/cache тесты: exact ranges, incremental edits, policy revocation, offline recovery, cancel и corruption.',
 'tools/benchmark_project_index.py':'Воспроизводимые fresh synthetic корпуса baseline 20a и измерения индекса 40/1200/12000 файлов: Recall, p50/p95, update, CPU/RAM/cache.',
})
register('agent/project_symbols.py', '''
extract_symbols | Извлекает определения, методы, imports/exports и byte-column ranges через AST/Tree-sitter; parser error не блокирует текстовый индекс.
extract_symbols.add | Добавляет ограниченное именованное описание символа с точным source range и precision=syntax.
''')
register('agent/project_index_policy.py', '''
IndexPolicy | Снимок правил автоматического доступа и .gitignore на одну операцию; новый retrieval создаёт новый экземпляр.
IndexPolicy.rules | Один раз компилирует bounded UTF-8 .gitignore папки, не читая недоступные правила или symlink.
IndexPolicy.permits | Memoize фильтр для конкретного пути только в текущем снимке; это не замена canonical-path проверки при чтении.
IndexPolicy._permits | Применяет общую file policy, fixed excludes и GitWildMatch ко всем ancestors; запрещённый parent не оживает через child negation.
IndexPolicy.anchor_policy | Вычисляет hash file-access policy и правил ancestor .gitignore для конкретного результата.
''')
register('agent/project_index.py', '''
ProjectIndex | Владеет одним derived cache/observer/updater; не использует chat DB и не выполняет исходный код.
ProjectIndex._claim | Берёт OS-released owner lock кеша; второй Core не может молча конкурировать с пересборкой.
ProjectIndex.database | Открывает короткое независимое SQLite WAL соединение с bounded lock wait и Unicode casefold.
ProjectIndex._initialize | Создаёт versioned cache schema и optional FTS5 trigram, сохраняя pending paths до recovery scan.
ProjectIndex.status | Возвращает state, counters, backend, watcher и approximate cache size без source contents/полного обхода.
ProjectIndex._cache_bytes | Считает DB/WAL/SHM и выдерживает исчезновение WAL во время checkpoint.
ProjectIndex.rebuild | Планирует контролируемый background scan; по явному запросу архивирует повреждённый owned cache и создаёт новый.
ProjectIndex.cancel | Останавливает background indexing, сохраняет очередь и не объявляет partial index готовым.
ProjectIndex.uncertain | Помечает потерю достоверности после overflow/policy/error, при необходимости просит удалить derived content.
ProjectIndex.enqueue | Durable coalescing exact paths с token, чтобы новое событие не потерялось при обработке старого.
ProjectIndex.reconcile_command | Добавляет внутреннее событие bounded сверки cwd; evidence scope не считается sandbox программы.
ProjectIndex._watch | Запускает observer до initial scan, объединяет события, прерывает чтение на смене правил и сигнализирует ошибки/overflow.
ProjectIndex._walk | Enumerates разрешённые saved files только при initial/recovery либо bounded subtree reconcile, без ссылок/junction.
ProjectIndex._read | Ограниченно повторяет только чтение при Windows sharing/moving-file race, проверяет отмену между попытками.
ProjectIndex._read_once | Проверяет policy/canonical target, regular file, bounded UTF-8 и stable before/after stat; возвращает hash и syntax symbols.
ProjectIndex._apply | Применяет маленький batch, пропускает неизменившиеся SHA/policy/parser и потребляет только обработанные pending tokens.
ProjectIndex._purge | Инвалидирует derived text/symbol/FTS rows при изменении доступа, не трогая чаты, journal или source files.
ProjectIndex._build | Под активным observer делает первичный scan, затем оставляет события периода scan в durable очереди для replay.
ProjectIndex._drain | Обрабатывает точные edits/rename/delete и bounded directory/command reconciliation без штатного global rescan.
ProjectIndex._run | Единственный updater; переключает building/updating/ready/recovery, не запускает бесконечные автоматические rescan.
ProjectIndex.query | Читает bounded candidates в SQLite snapshot, повторно проверяет source hash/access и возвращает ranges с provenance; updating помечается partial.
ProjectIndex.close | Останавливает observer/updater и освобождает owner lock; незавершённая очередь остаётся на диске.
get_index | Находит instance по canonical workspace и profile; create используется только при явном выборе проекта/индексных tools.
notify_paths | Best-effort change feed после уже разрешённого эффекта; отказ кеша не повторяет и не отменяет запись.
close_indexes | Закрывает instances при переключении проекта и завершении Core, не удаляя sources/cache recursively.
''')
register('tests/test_project_index.py', '''
ProjectIndexTests.wait | Ожидает проверяемый state/source fact до bounded deadline, при ошибке показывает status индекса.
ProjectIndexTests.hits | Получает текущие hash-verified matches либо пустой результат недоступного индекса.
ProjectIndexTests.test_cancel_interrupts_flat_directory_before_reading_remaining_files.paused_read | Задерживает одно чтение после начала пересборки для воспроизводимой проверки отмены до остальных файлов.
ProjectIndexTests.test_transient_writer_sharing_error_does_not_disable_index.transient | Имитирует один краткий Windows sharing error, затем возвращает настоящее чтение файла.
''')
TEST_PURPOSES.update({
 'python_typescript_symbols_have_exact_ranges_and_provenance':'AST/TS определения и методы имеют ожидаемые строки, kind, SHA, workspace и precision=syntax.',
 'text_files_and_short_query_work_without_fts':'SQLite text fallback поддерживает кириллицу, короткий запрос и поиск пути, сохраняя indexed backend.',
 'case_sensitive_symbols_and_file_paths_respect_request':'флаг регистра последовательно применяется к определениям и именам файлов.',
 'transient_writer_sharing_error_does_not_disable_index':'краткий Windows sharing conflict восстанавливается bounded read-only retry без отключения индекса.',
 'queue_overflow_requires_recovery_without_unbounded_backlog':'переполнение очереди не оставляет неограниченный backlog и не возвращает ложное ready; новые события всё ещё допустимы.',
 'cancel_interrupts_flat_directory_before_reading_remaining_files':'отмена внутри широкой папки/пакета прерывает дальнейшее чтение и освобождает worker.',
 'updating_cache_returns_verified_partial_hits':'фоновый delta update возвращает проверенные положительные результаты с partial marker, вместо ложного отсутствия.',
 'symlink_targets_are_never_indexed_through_aliases':'внешняя и внутренняя symlink alias не индексируются, обычные файлы остаются доступны.',
 'editor_save_external_rename_delete_are_incremental':'настоящий editor save и внешние rename/delete обновляют cache без роста full_scans.',
 'stale_backdated_bytes_are_never_returned':'same-size/backdated внешняя правка не позволяет выдать старый SHA/range как текущий.',
 'root_nested_gitignore_and_policy_revoke_old_cache':'nested .gitignore и .neutralignore инвалидируют cached source, explicit rebuild применяет новые правила.',
 'exact_grant_revocation_is_checked_even_without_workspace_event':'внешнее profile grant/revoke повторно проверяется retrieval и не раскрывает бывший разрешённый .env.',
 'ignored_parent_cannot_be_restored_by_child_negation':'правила Git не позволяют !child внутри целиком игнорируемого parent без разрешения parent.',
 'parser_failure_and_non_utf8_leave_text_search_available':'parser dependency/syntax error не ломают text search; non-UTF8 binary не попадает в cache.',
 'durable_queue_coalesces_and_restart_recovers_offline_edit':'pending path coalesces, controlled startup rescan восстанавливает внешний offline edit.',
 'overflow_cancel_and_explicit_rebuild_never_claim_ready':'неопределённость и cancel дают fallback/needs_rebuild, explicit rebuild возвращает готовый индекс.',
 'corrupt_derived_cache_requires_explicit_rebuild':'повреждённый derived SQLite не сбрасывается молча; fallback работает, explicit rebuild сохраняет broken cache отдельно.',
 'scoped_outline_and_cancellation_do_not_return_other_sources':'outline выбранного файла не раскрывает другие scopes, отменённый поиск возвращает SEARCH_CANCELLED.',
 'index_search_updates_and_controls_in_real_core':'реальный JSON-lines Core активирует индекс, видит внешний edit без full scan и поддерживает cancel/rebuild/fallback.',
})
TS_NOTES.update({
 'apps/desktop/src/ProjectSearch.tsx:ProjectSearch.indexAction':'Вызывает только status/rebuild/cancel индекса и показывает ошибку без запуска модели/команд.',
 'apps/desktop/src/ProjectSearch.tsx:ProjectSearch.refresh':'Периодически получает лёгкий статус индекса только для текущей видимой панели; cleanup отбрасывает поздние ответы.',
 'projectIndex':'Узкий renderer→main→Core API управления derived индексом выбранного проекта.',
})


FILE_NOTES.update({
 'agent/context_builder.py':'Подбор сохранённых диапазонов проекта, provenance, дедупликация, финальная проверка доступа/хеша и точный предпросмотр внешней отправки.',
 'tests/test_context_builder.py':'Изолированные проверки ContextPack: индекс, source anchors, budget pruning, revoke, отмена, retry и согласие без внешней сети.',
 'apps/desktop/src/SourceContextPreview.tsx':'Читаемый предпросмотр получателя, модели, диапазонов и полного текста автоматически выбранных исходников перед одной отправкой.',
})
register('agent/context_builder.py', '''
local_context_endpoint | Разрешает автоматический локальный retrieval только HTTP(S) loopback, исключая LAN и внешние адреса.
encode_pack | Сериализует source data отдельно от system instructions и без абсолютного корня проекта.
pack_message | Добавляет внутренние anchors для host guard, которые удаляются при подготовке HTTP payload.
source_proposal | Фиксирует конкретный endpoint, модель, диапазоны, hashes и точный текст для одного подтверждения; API key сюда не входит.
pack_summary | Возвращает только метаданные источников для task UI; тела исходников не сохраняются в canonical history.
visible_summary | Повторно фильтрует исторические пути при загрузке задачи после изменения прав доступа.
trim_pack | Убирает один optional source целиком; не режет пользовательский запрос или JSON посередине.
validate_context | Перед каждой HTTP попыткой проверяет trusted root, права, ignore policy и SHA полного файла; изменившееся исключается.
ContextBuilder | Ограниченный retrieval без дополнительной LLM: явные файлы, определения/упоминания, недавние эффекты и имена тестов.
ContextBuilder.check | Проверяет общую отмену перед очередной read/query операцией.
ContextBuilder.build | Ранжирует и дедуплицирует saved-file ranges; повторно прочитанное содержимое в видимых tool receipts не дублируется.
ContextBuilder.build.add | Объединяет одинаковые path/line candidates с приоритетом причины первого попадания.
ContextBuilder.project | Создаёт временную копию model request с data envelope перед последним user message; история не изменяется.
''')
register('tests/test_context_builder.py', '''
ContextBuilderTests | Изолирует проект, derived index и profile для тестов, не использует реальные исходники и внешние API.
ContextBuilderTests.setUp | Создаёт две синтетические Python sources и отдельный профиль, закрывает watcher перед cleanup.
ContextBuilderTests.params | Формирует обязательный запрос и optional ContextPack для проверки реального финального budget/HTTP guard.
ContextBuilderTests.client | Создаёт SDK client с запрещёнными redirect/proxy; внешний hostname никогда не запрашивается в этих тестах.
ContextBuilderTests.send | Передаёт запрос через настоящий ModelClient.request в in-memory endpoint, включая retry 500.
ContextBuilderTests.send.create | Учитывает точные транспортные payload и при необходимости один раз имитирует ответ 500.
ContextBuilderTests.test_remote_requires_concrete_approval_and_has_no_redirects_or_proxy.approve | Проверяет адрес, модель и текст фактического предложения до разрешения каждого отдельного HTTP attempt.
ContextBuilderTests.test_rejection_and_edit_during_preview_never_reach_endpoint.approve | Отказывает либо меняет source во время ожидания, чтобы проверить отсутствие HTTP при недействительном согласии.
ContextBuilderTests.test_local_retry_omits_changed_sources.create | После первой попытки меняет файл; повторный HTTP не должен получить старый source fragment.
''')
TEST_PURPOSES.update({
 'ephemeral_pack_and_anchors_keep_canonical_history_untouched':'Model projection содержит saved-file hashes/ranges, canonical history и system sources не смешиваются, host metadata не уходит в SDK.',
 'index_selects_symbol_and_related_test_without_duplicate_ranges':'Активный индекс находит символ и вероятный тест по имени, перекрывающиеся диапазоны не дублируются.',
 'policy_and_content_rechecked_after_selection':'Внешнее изменение файла или .neutralignore после retrieval исключает прежний фрагмент.',
 'existing_visible_read_is_not_duplicated_but_changed_content_is_selected':'Уже видимый read receipt не дублируется; изменившиеся сохранённые bytes выбираются заново.',
 'denied_missing_foreign_and_cancelled_sources':'Ignore, отсутствующие/внешние пути, чужой workspace и Stop не дают source данных.',
 'grant_revocation_hides_sources_and_invalidates_pack':'Отзыв точного grant инвалидирует пакет и скрывает исторический путь из UI.',
 'budget_drops_whole_fragments_before_current_prompt':'RequestBudget удаляет целые optional fragments, сохраняет JSON и обязательный user request.',
 'remote_requires_concrete_approval_and_has_no_redirects_or_proxy':'Для каждой HTTP попытки внешнему endpoint нужен точный preview; redirect и environment proxy отключены.',
 'rejection_and_edit_during_preview_never_reach_endpoint':'Отказ и изменение source во время ожидания не доходят даже до fake endpoint.',
 'no_callback_strips_remote_pack_but_loopback_validates_it':'Без доверенного approval callback автоматические источники внешнему серверу не отправляются.',
 'local_retry_omits_changed_sources':'Повтор после 500 заново проверяет source и исключает старое содержимое.',
 'source_context_approval_reject_and_changed_preview_send_no_http':'Реальный TaskService блокирует HTTP на approval, отказ/изменение приводит к paused, а не ложному выполнению.',
})
SYMBOL_NOTES['agent/model_client.py:SourceContextApprovalError']='Обратимая пауза, когда передача исходников отклонена или согласованный пакет изменился; не означает успешного HTTP.'
TS_NOTES['apps/desktop/src/SourceContextPreview.tsx:SourceContextPreview']='Показывает адрес получателя, модель и неизменённые source bodies; полный JSON доступен отдельно, HTML из исходников не исполняется.'

TEST_PURPOSES.update({
 'destination_change_during_approval_requires_new_preview':'Смена endpoint во время ожидания отменяет согласие и не вызывает HTTP.',
 'source_context_confirmed_http_preserves_write_approval':'После отдельного согласия реальный локальный HTTP получает пакет; последующая запись требует собственного diff approval, Stop не пишет файл.',
})
register('tests/test_context_builder.py', '''
ContextBuilderTests.test_destination_change_during_approval_requires_new_preview.approve | Меняет configured recipient прямо в callback подтверждения для отрицательной проверки повторной привязки.
''')

TS_NOTES['apps/desktop/src/App.tsx:App.clearSources']='Скрывает прежние source anchors после сохранения изменённых workspace grants до нового task snapshot.'
TEST_PURPOSES['automatic_rollout_keeps_measured_json_regression_disabled']='Автоматический ContextPack включён для native IDE, JSON с измеренной регрессией остаётся выключен; remote требует host approval callback.'

TS_NOTES['tests/electron/neutral-smoke.cjs:win.webContents.send']='Сохраняет настоящее approval событие изолированного Core, чтобы проверить UI preview fixture и затем восстановить реальное ожидающее подтверждение.'

TEST_PURPOSES['optional_sources_do_not_displace_available_tool_schemas']='Auto budget сначала снимает optional source fragments, сохраняя схемы инструментов, которые помещались до retrieval.'

TEST_PURPOSES['unchanged_fragment_does_not_reuse_an_obsolete_whole_file_hash']='Правка за пределами выбранных строк меняет полный hash: прежний read_range receipt не отменяет новый anchor даже при совпавшем фрагменте.'


FILE_NOTES.update({
 'agent/run_registry.py':'Сохраняемые epochs запуска и атомарный BudgetLedger в canonical SQLite v3; recovery orphan telemetry без повторения эффектов.',
 'agent/inference_scheduler.py':'Общая FIFO очередь физической генерации, cancellable tickets и reservations/usage для SDK, probe и readonly research.',
 'tests/test_run_registry.py':'Изолированные v2→v3, backup, orphan/live owner, cascade, model inheritance, FIFO и SDK stream-close проверки.',
 'tests/migration/test_run_control.py':'Независимая localhost сверка ledger с HTTP, stream_options retry, JSON repair, usage и diff approval.',
 'apps/desktop/src/RunHistory.tsx':'История epochs выбранного чата, физические HTTP попытки, известный usage, текущие оценки и время ожиданий.',
})
register('agent/run_registry.py', '''
now | UTC timestamp для долговечных записей; elapsed/approval измеряются отдельно monotonic clock.
owner_alive | Только проверяет жив ли PID: Windows OpenProcess/GetExitCodeProcess/CloseHandle, без сигналов; неоднозначность считается живым owner.
safe_usage | Нормализует две сообщённые провайдером token counts, сохраняя отсутствие telemetry как unknown.
BudgetLedger | Инкрементальные счётчики, обновляемые в одной транзакции с attempt; никаких caps и самостоятельной политики остановки.
BudgetLedger.contribution | Вычисляет вклад одной попытки: HTTP, один cumulative usage, reservation, queue и interrupt.
BudgetLedger.apply | Атомарно прибавляет разность before/after; повторная запись terminal usage не удваивает токены.
RunRegistry | Отдельные run ID для исполнения/повтора, связь с chat/journal и parent, без копии prompt и нового execution authority.
RunRegistry.ready | Лениво открывает профиль, применяет v3 и помечает только runs с доказанно мёртвым owner как paused; unresolved attempts становятся interrupted.
RunRegistry.begin | Создаёт новый epoch и привязывает OperationContext; внутренние дети наследуют подключение/модель, depth=1 и fan-out≤3.
RunRegistry.update | Короткая транзакция host lifecycle metadata; текущий ledger сохраняется без потери конкурентных delta updates.
RunRegistry.attempt | Создаёт reservation до очереди; это ещё не HTTP и не факт расхода токенов.
RunRegistry.update_attempt | Атомарно обновляет attempt и вклад в ledger; headers/payload/exception text не сохраняются.
RunRegistry.snapshot | Читает агрегированный ledger без сканирования всех attempts; для живого epoch добавляет текущее elapsed/approval время.
RunRegistry.history | Возвращает до 20 epochs выбранного чата с верхним backend пределом 50 записей.
RunRegistry.cancel | Сигнализирует OperationContext всего живого дерева, не заявляя rollback или подтверждённое завершение tool effect.
RunContext | Состояние одного epoch: независимый ID, cancellation, исходная модель и монотонные durations; не второй план задач.
RunContext.observe | Отражает существующий RunState, измеряет approval wait и дельту tool calls относительно возобновлённого checkpoint.
RunContext.finish | Завершает epoch после cleanup; resume получает новый ID, неизвестные side effects не воспроизводятся.
RunContext.snapshot | Возвращает metadata/ledger текущего epoch, без канонической истории и исходников.
''')
register('agent/inference_scheduler.py', '''
InferenceScheduler | Общая для процесса FIFO очередь одного тяжёлого inference; моделью и VRAM внешнего сервера не управляет.
InferenceScheduler.acquire | Ждёт без владения ресурсом; cancellation удаляет точный ticket, сохраняя порядок остальных.
InferenceScheduler.release | Освобождает только точный ticket-owner; запоздалое завершение не снимает следующего владельца.
InferenceScheduler.status | Метаданные busy/owner/waiting без prompt, секретов и предположений о резидентных моделях.
validate_model | Единый контракт model/connection/API protocol для SDK, probe и raw research; дрейф binding требует нового run.
InferenceAttempt | Одна reservation/SDK attempt: физический POST учитывается только transport hook, usage остаётся optional.
InferenceAttempt.acquire | Сохраняет reservation, ждёт FIFO ticket и записывает queue time; отменённое ожидание снимает резерв.
InferenceAttempt.on_http | HTTPX hook учитывает только POST chat/completions или responses, включая retries и repair.
InferenceAttempt.observe | Запоминает последний cumulative usage кадр и terminal reason; не суммирует повторные кадры потока.
InferenceAttempt.finish | Сохраняет terminal telemetry и в finally освобождает ticket после cleanup; missing usage не становится нулевой стоимостью.
scheduled_request | Общий async context manager для raw probe/research с той же очередью и журналом попыток.
''')
register('agent/model_client.py', '''
ScheduledStream | Обёртка SDK AsyncStream: resource lease живёт до завершения фактического close, включая ошибку и отмену.
ScheduledStream.__aenter__ | Открывает SDK stream, при ошибке закрывает ресурс и telemetry до проброса исключения.
ScheduledStream.__aiter__ | Передаёт исходные SDK chunks существующему Responses/native адаптеру без изменения содержимого.
ScheduledStream.__aexit__ | Закрывает SDK ответ и завершает попытку при выходе из async with.
ScheduledStream.close | Shield cleanup против повторного Stop; queue не получает lease до окончания close; ошибка не скрывается.
ModelClient._http_attempt | Независимо от логического create считает физический inference POST в активной attempt.
ModelClient._tracked | Отделяет корневые request workers от SDK cleanup tasks; shutdown не отменяет cleanup повторно.
''')
register('tests/test_run_registry.py', '''
RunRegistryTests | Изолированная canonical DB и только синтетические модель/endpoint, без внешних HTTP вызовов.
RunRegistryTests.setUp | Создаёт временный профиль и Registry, cleanup не затрагивает пользовательскую SQLite.
RunRegistryTests.run_context | Создаёт host run на example.invalid без сетевого обращения для положительных/отрицательных сценариев.
SchedulerTests | Async проверки FIFO/cleanup/cancel и освобождения ресурса перед ожиданием дочернего run.
SchedulerTests.test_stream_close_holds_lease_until_sdk_cleanup_finishes.Response | SDK fixture с явно задержанным close для проверки повторного Stop.
SchedulerTests.test_stream_close_holds_lease_until_sdk_cleanup_finishes.Response.close | Сообщает о начале cleanup и ждёт отдельного разрешения теста, не обращаясь к сети.
''')
register('tests/migration/test_run_control.py', '''
Handler | Localhost OpenAI fixture: один отказ optional поля, malformed JSON, protocol repair или отдельная write proposal.
Handler.log_message | Подавляет служебный HTTP шум; тест сохраняет структурированные requests в памяти.
Handler.do_GET | Отдаёт минимальный каталог модели для локального auto discovery, без inference telemetry.
Handler.do_POST | Независимо считает POST и отправляет SSE/usage; первый stream_options отказ не содержит usage.
RunControlHttpTests | Реальный TaskService/SDK/HTTP с изолированным профилем и очередью событий.
RunControlHttpTests.setUp | Подменяет profile constants, запускает localhost сервер и конфигурирует Core без пользовательских данных.
RunControlHttpTests.stop_server | Завершает сервер и его listener после cleanup Core.
RunControlHttpTests.event | Ожидает конкретное Core событие, немедленно поднимает ошибку при failed.
''')
TEST_PURPOSES.update({
 'resume_epochs_are_independent_and_duplicate_ids_are_rejected':'Повтор имеет новый run ID при прежнем journal; использованный ID нельзя повторно исполнить.',
 'child_inheritance_bounds_and_cascade_cancel':'Дети наследуют модель/подключение, depth/fan-out ограничены и cancel распространяется по дереву.',
 'ledger_idempotent_usage_and_reservations_are_not_charges':'Reservation не считается HTTP/стоимостью, cumulative usage добавляется один раз даже при повторной terminal записи.',
 'orphan_recovery_releases_estimates_and_never_replays_http':'Restart отмечает orphan run paused, снимает резерв, сохраняет unknown usage и не запускает HTTP.',
 'live_owner_is_preserved_and_pid_check_does_not_signal_it':'Проверка текущего PID безопасна, live owner не объявляется прерванным другим Registry.',
 'approval_time_is_separate_from_elapsed_and_model_queue':'Время подтверждения отдельно от model queue, elapsed и счётчика инструментов.',
 'schema_two_upgrade_preserves_existing_task_and_backup_contains_runs':'Миграция v2→v3 сохраняет checkpoint и восстановленный ZIP содержит run telemetry.',
 'delete_chat_also_deletes_its_run_metadata':'Удаление чата стирает связанные run/attempt metadata без остаточного history.',
 'model_binding_rejects_child_or_parent_configuration_drift':'Смена модели в текущем run отклоняется до HTTP, не загружая новую модель.',
 'fifo_waiter_cancel_and_stale_release':'FIFO сохраняет порядок после отмены waiter; старый owner не освобождает нового.',
 'parent_waits_for_child_without_holding_generation_lease':'Ресурс parent отпускается перед child, после завершения parent может снова получить очередь без deadlock.',
 'stream_close_holds_lease_until_sdk_cleanup_finishes':'Двойной Stop не освобождает lease посреди SDK close; следующий запрос ждёт реального cleanup.',
 'cancelled_queued_reservation_has_no_http_or_token_charge':'Отменённый waiter снимает резерв, не делает HTTP и не нарушает текущий lease.',
 'physical_attempts_include_optional_field_retry_and_json_repair_once':'Три физические POST попытки совпадают с ledger: optional retry и JSON repair; usage дважды не считается.',
 'waiting_write_approval_has_no_generation_lease_and_cancel_preserves_file':'Diff approval не удерживает модель, Stop не пишет файл и завершает epoch paused.',
 'delete_during_subtree_read_is_incremental_absence':'Удаление между directory enumeration и чтением трактуется как absence, не как необходимость полного rescan.',
})
register('tests/test_project_index.py', '''
ProjectIndexTests.test_delete_during_subtree_read_is_incremental_absence.disappearing | Детерминированно удаляет один источник непосредственно перед read_once, проверяя штатный file-delete race.
''')
SYMBOL_NOTES['tests/test_services_and_sessions.py:ServiceBoundaryTests.setUp']='Изолирует профиль долговечного run telemetry, включая замоканный probe, от пользовательского AppData.'
TS_NOTES.update({
 'runHistory':'Узкий renderer→main→Core вызов истории только выбранного чата; записи из иной scope не возвращаются.',
 'apps/desktop/src/RunHistory.tsx:RunHistory':'Загружает bounded epochs выбранного чата при раскрытии, отбрасывает поздние ответы и позволяет обновить историю.',
 'apps/desktop/src/RunHistory.tsx:Ledger':'Показывает физические HTTP, только сообщённые tokens, outstanding estimates и wait time; не выдаёт unknown usage за ноль.',
})

TS_NOTES.update({
 'RunLedgerSnapshot':'Агрегаты реального HTTP, известного usage, reservations, очереди и approval time для UI без политики caps.',
 'RunSnapshot':'Публичные metadata одного epoch: модель, state, duration, инструменты и ledger; без prompt/ключей/исходников.',
})

register('agent/inference_scheduler.py', '''
InferenceScheduler.quarantine | После ошибки SDK close блокирует повторное использование exact ticket до подтверждённого закрытия его HTTP клиента; новый waiter получает объяснимую ошибку.
''')
register('tests/test_run_registry.py', '''
SchedulerTests.test_failed_close_blocks_reuse_until_owning_client_cleanup.Response | SDK fixture с ошибкой close для проверки карантина ресурса.
SchedulerTests.test_failed_close_blocks_reuse_until_owning_client_cleanup.Response.close | Детерминированно поднимает OSError cleanup, не обращаясь к реальным сокетам.
''')
TEST_PURPOSES['failed_close_blocks_reuse_until_owning_client_cleanup']='Ошибка SDK close не разрешает следующую генерацию; ошибка объяснима, очередь не зависает, owner cleanup снимает карантин.'

register('agent/run_registry.py', '''
RunRegistry.record_tool | Атомарно увеличивает счётчик квитанций текущего epoch, независимо от сброса legacy task.tool_calls при resume.
RunContext.record_tool | Регистрирует одну обработанную tool квитанцию; ошибка/отказ не выдаются за подтверждённый side effect.
RunContext.observe | Отражает существующий RunState и отдельный approval wait; legacy task counter не используется для вычитания новых вызовов.
''')

# 11b: execution methods retain their reviewed contracts after moving modules.
for _key,_value in list(SYMBOL_NOTES.items()):
    if _key.startswith('core/python/task_service.py:TaskService.'):
        SYMBOL_NOTES.setdefault(_key.replace('core/python/task_service.py:TaskService.','core/python/task_execution.py:TaskExecution.'),_value)
FILE_NOTES.update({
 'core/python/task_execution.py':'Run-owned engine loop, tool dispatch, streaming timers, persistence and exact approval correlation; no UI selection state.',
 'core/python/run_session.py':'Independent session owner and frozen connection for one foreground/background run, with live snapshot and stream cursor.',
 'tests/migration/test_background_runs.py':'Real HTTP tests of two engine workers, isolated streams, queued cancellation, approvals and full shutdown.',
 'tests/electron/background-runs-smoke.cjs':'Real renderer/Core test of switching active chats, queued Stop and a delta arriving between snapshot and IPC response.',
})
register('core/python/task_service.py', """
TaskService | Координатор выбранной области и независимых RunSession; engine/thread/approval проецируют только выбранный чат.
TaskService.selected_run | Находит владельца выбранного чата; не переключает состояние фоновых callbacks.
TaskService.active_runs | Возвращает только безопасные метаданные активных чатов для навигации, без prompts, ключей и исходников.
TaskService.task_running | Проверяет все run owners: глобальные изменения настроек/прав запрещены до завершения каждого.
TaskService.engine | Совместимая проекция engine выбранного владельца; фоновые callbacks используют собственную ссылку.
TaskService.thread | Проекция потока выбранного владельца для join и диагностики, не общая переменная всех запусков.
TaskService.run_id | Возвращает идентификатор выбранного запуска; setter оставлен для compatibility state до создания owner.
TaskService.approval | Читает ожидающее решение только выбранного owner; не возвращает approval другого чата.
TaskService.handoff_pending | Проецирует передачу задачи Лолы выбранного owner и синхронизирует её явное удаление.
TaskService.start | Создаёт отдельный owner под RLock, запрещает дубликат чата/папки и разные model bindings, запускает поток без смены чужого состояния.
TaskService.configure | Разрешает идентичный повтор настроек без записи во время работы; изменения требуют глобального idle.
TaskService.select_chat | Возвращает live snapshot с cursor вместо crash recovery для активного owner; новый/завершённый чат загружается отдельно.
TaskService.resolve_approval | Передаёт решение выбранному owner, который проверяет точные run_id и approval_id.
TaskService.cancel | Останавливает только выбранный owner; устаревший run_id не затрагивает другой запуск.
TaskService.shutdown | Закрывает приём новых задач, отменяет всех владельцев и ждёт их cleanup перед закрытием общих служб.
""")
register('core/python/task_execution.py', """
TaskExecution | Общая реализация callbacks одного запуска; каждый RunSession владеет собственным chat, engine, таймерами и approval.
TaskExecution._event | Под общим RLock выдаёт возрастающий cursor, chat/run/mode/root и сохраняет полный pending approval для возврата в чат.
""")
register('core/python/run_session.py', """
RunSession | Изолированное состояние одного запуска: frozen config, собственный SessionService, operation, stream и approval; общие capability services не дублируются.
RunSession.chat | Возвращает канонический чат владельца, независимо от выбранной вкладки UI.
RunSession.idle | Блокирует повторный запуск этого владельца без ограничения других чатов.
RunSession._recover_chat | Проверяет сохранённый checkpoint до начала нового epoch через существующий SessionService.
RunSession.select_chat | Запрещает смену области внутри исполнения: coordinator обязан передать чат заранее.
RunSession.begin | Создаёт собственную operation, запускает существующий loop и закрывает reservation/таймеры при ошибке старта.
RunSession.view | Под control lock копирует checkpoint/history и незавершённый текст с message_id; отдаёт live run, approval и event cursor без записи в историю.
""")
register('tests/migration/test_background_runs.py', """
BackgroundRunTests.install_handler | Ставит локальную SSE fixture с удерживаемым потоком и write approval; пользовательские серверы не используются.
BackgroundRunTests.install_handler.Handler | Локальный OpenAI-compatible HTTP handler для двух независимых engine workers.
BackgroundRunTests.install_handler.Handler.log_message | Подавляет журнал HTTP fixture в отчёте тестов.
BackgroundRunTests.install_handler.Handler.do_GET | Объявляет одну fixture модель для runtime discovery.
BackgroundRunTests.install_handler.Handler.do_POST | Удерживает alpha stream, возвращает write tool или финал; закрытый клиент не превращается в серверный сбой.
BackgroundRunTests.event | Ждёт конкретный тип события и chat_id; ошибки engine считаются провалом теста.
BackgroundRunTests.wait_queued | Проверяет durable queued reservation второго запуска, не подменяя scheduler.
""")
TEST_PURPOSES.update({
 'switch_and_cancel_queued_chat_preserve_other_live_stream':'Возврат к живому потоку не делает crash recovery; отмена очереди не отправляет HTTP и не меняет другой чат.',
 'two_approvals_are_scoped_and_same_workspace_has_one_writer':'Два проекта получают разные approvals; чужое решение отклоняется, отменённый проект не меняется, один root имеет одного writer.',
 'shutdown_cancels_all_owners_and_mismatched_models_are_not_started':'Shutdown отменяет владельцев и очередь; разные model bindings не запускаются одновременно, закрытый service не принимает работу.',
 'busy_task_allows_selection_but_rejects_configuration_and_same_workspace_run':'Во время работы разрешён выбор нового чата, но изменение конфигурации и второй writer той же папки запрещены.',
})
TS_NOTES.update({
 'apps/desktop/src/App.tsx:App.openBackgroundRun':'Переходит в режим выбранного фонового чата и загружает его live snapshot без остановки других задач.',
 'apps/desktop/src/App.tsx:App.restoreBackgroundRuns':'Объединяет snapshot с более свежими событиями, не воскрешая завершённые run IDs при позднем IPC ответе.',
 'tests/electron/background-runs-smoke.cjs:BrowserWindow.prototype.show':'Скрывает только тестовое окно, сохраняя настоящий Electron renderer.',
 'tests/electron/background-runs-smoke.cjs:BrowserWindow.prototype.loadURL':'Открывает собранный renderer вместо пользовательского dev сервера.',
 'tests/electron/background-runs-smoke.cjs:ipcMain.handle':'Задерживает только тестовый chat load после backend snapshot и добавляет реальную SSE delta для проверки гонки IPC.',
 'tests/electron/background-runs-smoke.cjs:done':'Завершает ровно один удерживаемый SSE response после проверки изоляции.',
 'tests/electron/background-runs-smoke.cjs:js':'Выполняет проверяемый шаг в изолированном renderer.',
 'tests/electron/background-runs-smoke.cjs:poll':'Ждёт DOM состояние с ограниченным timeout.',
 'tests/electron/background-runs-smoke.cjs:click':'Нажимает известный DOM элемент и даёт React завершить обработчик.',
 'tests/electron/background-runs-smoke.cjs:input':'Меняет controlled поле через native setter и input event.',
 'tests/electron/background-runs-smoke.cjs:finish':'Сохраняет результат/диагностику и закрывает только тестовое приложение и HTTP fixture.',
})

_moved_execution_methods={'request_delegation','_persist_chat','_task_event','_event','_flush_text','_flush_scheduled','_persist_draft','_persist_draft_scheduled','_text_delta','_chat_event','_request_approval','_approve_external','resolve_approval','cancel','_start','_save_messages','_run'}
for _key in list(SYMBOL_NOTES):
    if _key.startswith('core/python/task_execution.py:TaskExecution.') and _key.split('TaskExecution.',1)[1].split('.')[0] not in _moved_execution_methods:
        SYMBOL_NOTES.pop(_key)
    if _key.startswith('core/python/task_service.py:TaskService.') and _key.split('TaskService.',1)[1].split('.')[0] in (_moved_execution_methods-{'resolve_approval','cancel'}):
        SYMBOL_NOTES.pop(_key)

TS_NOTES['apps/desktop/electron/preload.ts:activeRuns']='Возвращает безопасный каталог живых run owners через фиксированный IPC маршрут.'

register('core/python/task_service.py', """
TaskService._persist_chat | Сохраняет выбранный неисполняющийся чат после обновления workspace evidence, без использования run callbacks.
TaskService._event | Публикует workspace/warning событие координатора для выбранного чата; inference callbacks принадлежат TaskExecution.
TaskService._prune_runs | Освобождает завершённые невыбранные owners после выхода их потока; durable история остаётся в SQLite.
""")
TS_NOTES['apps/desktop/src/App.tsx:App.receiveEvent.current']='Принимает lifecycle события всех чатов, буферизует target во время load и применяет к выбранному view только новые cursors правильного run.'

TS_NOTES['tests/electron/background-runs-smoke.cjs:appendAlpha']='Добавляет новый реальный SSE фрагмент между snapshot и поздним IPC response, проверяя отсутствие потерь и дублей.'

TEST_PURPOSES['telegram_cannot_stop_or_approve_another_selected_chat']='Telegram не отменяет и не подтверждает чужой выбранный чат; foreign background approval не становится remote pending действием.'

# 11c: process lifetime evidence is shared independently of registry accounting.
SYMBOL_NOTES.pop('agent/run_registry.py:owner_alive',None)
FILE_NOTES.update({
 'agent/process_identity.py':'Read-only Windows/Linux process lifetime probe, tri-state uncertainty and PID reuse evidence for orphan telemetry recovery.',
 'tests/test_process_identity.py':'Real child lifetime probe plus conservative PID reuse, legacy owner and whole-tree telemetry recovery tests.',
 'tests/migration/test_run_owner_restart.py':'Kill/restart of a real isolated Core with streamed and queued chats, durable ledger and invalidated write consent.',
})
register('agent/process_identity.py', """
inspect_process | Возвращает alive/dead/unknown и lifetime token; некорректные PID не приводятся к другому процессу, Windows сигналы не используются.
_windows_process | Открывает query-only handle, читает creation FILETIME и exit code одного объекта процесса, гарантированно закрывает handle.
_linux_process | Связывает boot ID с /proc start ticks, учитывает сложное comm и zombie; при скрытом /proc не объявляет owner мёртвым без проверки.
owner_alive | Совместимая bool-проекция: unknown считается потенциально живым процессом, чтобы не восстанавливать чужой active run.
owner_ended | Принимает только доказанную смерть PID или несовпадение сопоставимых creation tokens; legacy/unknown/version mismatch сохраняет owner.
""")
register('agent/run_registry.py', """
RunRegistry.ready | При первом доступе атомарно восстанавливает только доказанно завершённые process lifetimes; кеширует probe на owner и снимает orphan reservations без replay.
RunRegistry.begin | Создаёт новый epoch с PID/creation token, прежним connection inheritance и ограничениями prototype child identities; другая модель не загружается.
""")
register('core/python/task_service.py', """
TaskService._refresh_run_ledger | Обновляет checkpoint только ledger соответствующего chat/run после orphan recovery; возвращает факт изменения для атомарного сохранения при load.
""")
register('tests/test_process_identity.py', """
ProcessIdentityTests.test_linux_start_ticks_parse_complex_process_name.read | Подставляет proc stat и boot ID независимо от разделителей путей хостовой ОС.
""")
register('tests/migration/test_run_owner_restart.py', """
RestartHandler | Локальная SSE fixture: удерживаемый ответ либо неподтверждённый write tool, без обращения к внешней модели.
RestartHandler.log_message | Подавляет HTTP fixture access log.
RestartHandler.do_GET | Возвращает одну fixture модель для runtime discovery Core.
RestartHandler.do_POST | Отправляет сохраняемый фрагмент или write proposal; держит socket до закрытия убитым тестовым Core.
RunOwnerRestartTests.server | Поднимает отдельный HTTP fixture и конфигурирует только изолированный профиль subprocess Core.
RunOwnerRestartTests.restart | Убивает только принадлежащий тесту Core, дожидается выхода и запускает новый процесс с тем же тестовым профилем.
""")
TEST_PURPOSES.update({
 'real_process_lifetime_is_stable_then_dead_without_signalling_probe':'Проверяет lifetime текущего и собственного дочернего процесса; после естественного выхода child probe доказывает завершение owner.',
 'windows_probe_never_uses_os_kill':'Windows lifetime probe работает при запрете любого os.kill вызова.',
 'uncertain_or_incomparable_identity_never_proves_owner_ended':'Access uncertainty, legacy token и разные token schemes не считаются смертью; сравнимый новый token доказывает PID reuse.',
 'linux_start_ticks_parse_complex_process_name':'Парсер Linux proc stat сохраняет start ticks при пробелах и скобках в имени процесса.',
 'reused_pid_recovers_whole_tree_once_preserving_terminal_state':'Повтор PID снимает reservations всего prototype дерева одной транзакцией, сохраняет failed/paused и не удваивает HTTP usage.',
 'legacy_or_unreadable_live_owner_keeps_reservations':'Отсутствие creation token или недоступный live owner сохраняет активное состояние и reservation.',
 'kill_recovers_stream_and_queue_without_http_or_duplicate_fragment':'Настоящий kill/restart Core сохраняет один partial ответ, снимает очередь и reservations двух чатов без нового HTTP.',
 'kill_invalidates_write_consent_without_replaying_the_action':'Старый approval после kill/restart недействителен: файл не создаётся и write request автоматически не повторяется.',
})

FILE_NOTES.update({
 'agent/run_policy.py':'Opt-in monetary planning for one logical task and all children/resumes; no local-auto cap, explicit unknown usage and capacity errors.',
 'agent/child_executor.py':'Real readonly child AgentEngine handoff with inherited connection, cancellable join, durable journal and fresh bounded handback.',
 'agent/task_graph.py':'Canonical plan_steps DAG: migration, validation, receipt-based completion and scoped stale-evidence propagation.',
 'apps/desktop/src/TaskGraphPanel.tsx':'Current task graph and trusted user editor with dependency/check selection; no direct effect execution.',
 'tests/test_run_policy.py':'Explicit paid-budget estimates across children/resume and atomic journal-to-epoch tool accounting.',
 'tests/test_task_graph.py':'DAG receipts, dependency validation, stale propagation, user plan authority, reload and persisted watchdog recovery.',
 'tests/migration/test_child_execution.py':'Real HTTP parent-child-parent, cancellation, denied child writes, stale handback, OOM and pre-HTTP spending admission.',
 'tests/migration/test_task_graph_execution.py':'Multi-file task through context compaction, failed check, bounded diagnostic and actual Core restart without replay.',
})
register('agent/run_policy.py', """
SpendingLimitError | Управляемая пауза по добровольному денежному порогу; наследует существующий BudgetExceededError.
ModelCapacityError | Управляемая пауза при подтверждённой нехватке памяти внешнего model server, без слепого повтора или выгрузки чужих моделей.
validate_spending | Проверяет явное включение, конечные суммы/цены и валюту; не подставляет выдуманные тарифы провайдера.
priced_tokens | Пересчитывает токены по пользовательским ценам в целые нанодоли валюты с округлением вверх.
spending_snapshot | Объединяет текущий journal задачи, детей и resume epochs; учитывает usage, активные резервы и неизвестные HTTP по оценке.
require_spending | В той же транзакции до reservation не допускает следующий внешний запрос сверх выбранного порога; local auto policy выключена.
capacity_failure | Узко распознаёт сообщения OOM в ошибке сервера без сохранения его raw body в policy metadata.
""")
register('agent/child_executor.py', """
ChildExecutor | Владеет одним синхронным readonly handoff, переиспользует AgentEngine/ToolExecutor/CallJournal и общий scheduler.
ChildExecutor.notify | Проецирует текущий child state в canonical checkpoint родителя под control lock; это дерево исполнения, не второй план.
ChildExecutor.execute | Создаёт bounded child на том же подключении, ждёт transport cleanup, сохраняет отдельные сообщения и возвращает только свежий ограниченный handback.
ChildExecutor.execute.dispatch | Разрешает пересечение list_files/read_file/read_range, фиксирует SHA чтений и блокирует возврат stale/слишком широкого результата.
ChildExecutor.execute.messages | Сохраняет историю ребёнка в его checkpoint, не смешивая её с родительским чатом или общим каталогом разговоров.
""")
register('agent/task_graph.py', """
migrate_plan | Обновляет canonical plan_steps до schema 2; прежние строки остаются advisory proposed, не получают выдуманное done.
prepare_steps | Проверяет типы, IDs, DAG/циклы, относительные affected files и ссылки только на проверки пользователя; сохраняет evidence неизменённых узлов.
witness | Сверяет только явные пути, включая отсутствие после delete; hashes/статистика и policy повторно проверяются без fingerprint всего проекта.
refresh_steps | Делает устаревшими изменённые witness/checks и зависимые done узлы, не меняя task lifecycle и не исполняя tools.
update_step | Завершает узел только по успешным durable receipts, подходящему типу действия, покрытию файлов и актуальным пользовательским checks; сохраняет witness.
""")
register('agent/progress_guard.py', """
ProgressGuard.observe | Считает повтор результата/ошибки, игнорируя receipt IDs, timestamps и прочую volatile metadata; сохраняет bounded hashes в checkpoint.
ProgressGuard.observe.stable | Рекурсивно удаляет volatile metadata перед fingerprint, сохраняя фактическое содержимое результата.
ProgressGuard.recover_or_stop | Разрешает ровно одну диагностическую попытку на логическую задачу; повтор после неё требует паузы, счётчик переживает resume.
""")
register('agent/run_state.py', """
RunState.revise_plan | Только явная trusted user revision переводит завершённый task checkpoint в paused; завершённый run epoch и general transition contract не переоткрываются.
""")
register('core/python/task_service.py', """
TaskService.update_plan | В idle проверяет selected chat, валидирует и закрепляет пользовательский план, обновляет evidence и сохраняет checkpoint без HTTP/effects.
TaskService._refresh_run_ledger | Синхронизирует ledger и дочерние states из scoped registry после restart; чужие chat/run/parent записи игнорируются.
""")
register('agent/call_journal.py', """
CallJournal._append | Атомарно добавляет SQLite receipt и один epoch tool counter по проверенной chat/journal/run привязке, включая artifact-backed result; повтор не удваивает счёт.
""")
register('tests/test_run_policy.py', """
RunPolicyTests.begin | Создаёт synthetic external run с общим journal задачи и явно заданными тестовыми ценами.
""")
register('tests/test_task_graph.py', """
TaskGraphTests.node | Создаёт typed change node с явным путём и dependencies для отрицательных и положительных проверок.
TaskGraphTests.write | Применяет настоящее подтверждённое write через ToolExecutor и возвращает его durable receipt reference.
""")
register('tests/migration/test_child_execution.py', """
ChildHandler | HTTP fixture для реального parent-child-parent, ошибок памяти и попытки запрещённой записи ребёнком.
ChildHandler.log_message | Подавляет локальный HTTP access log.
ChildHandler.do_GET | Объявляет только synthetic fixture модель.
ChildHandler.do_POST | Возвращает delegate/read/final либо OOM; удерживает child stream для проверки отмены и stale handback.
ChildExecutionTests.start | Настраивает изолированный root и запускает реальный native engine с optional child hold.
ChildExecutionTests.test_changed_source_discards_entire_child_answer.checkpoint | Детерминированно меняет synthetic source после child completion до свежести handback.
""")
register('tests/migration/test_task_graph_execution.py', """
options | Даёт точную пользовательскую проверку двух файлов с scoped witness; отрицательный режим задаёт exit 1.
GraphHandler | Native HTTP model fixture, читающий canonical task state и штатные compressed archives без подмены executor/journal.
GraphHandler.log_message | Подавляет HTTP fixture access log.
GraphHandler.do_GET | Отказывает discovery: manual test window задан явно и не зависит от внешнего сервера.
GraphHandler.do_POST | Генерирует graph/write/receipt/check/final sequence или повтор чтения; умеет ждать kill между зависимыми шагами.
GraphExecutionTests.run_graph | Выполняет multi-file sequence в реальном TaskService с явными approvals и включённым тестовым command plugin.
GraphRestartTests.advance | Даёт approvals только известным тестовым действиям и ждёт заданной точки настоящего Core без второго consumer RPC очереди.
""")
register('tests/test_workspace_tools.py', """
WorkspaceToolsTests.test_write_sharing_retry_rechecks_revision_before_atomic_replace.transient | Один раз моделирует Windows sharing violation, затем вызывает настоящий atomic replace.
""")
TEST_PURPOSES.update({
 'children_and_resume_share_reported_and_unknown_cost':'Порог объединяет детей и resume; HTTP без usage сохраняет оценку, новый epoch не сбрасывает затраты задачи.',
 'cancel_before_http_releases_money_and_exact_usage_is_idempotent':'Отмена очереди снимает денежный резерв без расхода; повтор usage update не удваивает сумму.',
 'local_auto_ignores_paid_budget_and_unfinished_children_block_completion':'Local auto не получает денежных caps; родитель не закрывается completed до закрытия детей, Stop каскадный.',
 'invalid_prices_and_capacity_error_classification':'Неверные цены/суммы отклоняются; OOM не смешивается с обычным HTTP 500.',
 'durable_receipt_and_epoch_tool_counter_commit_together':'Durable artifact-backed receipt и счётчик tools коммитятся одной транзакцией до следующего checkpoint, повтор не удваивается.',
 'parent_child_handoff_joins_and_ledger_matches_real_http':'Настоящая цепочка parent-child-parent даёт четыре HTTP, отдельные child rights/evidence и нулевые reservations после join.',
 'parent_cancel_cascades_and_closes_child_transport':'Stop родителя прерывает child stream, освобождает scheduler и приостанавливает оба runs.',
 'changed_source_discards_entire_child_answer':'Изменение файла перед handback удаляет весь child answer вместо передачи stale фактов.',
 'memory_exhaustion_pauses_without_retry':'OOM fixture получает один HTTP, задача paused с понятной причиной и без повторного запроса.',
 'child_cannot_gain_write_permission_from_model_output':'Смоделированный запрещённый write ребёнка не создаёт файл и не выдаёт права/approval.',
 'explicit_external_budget_blocks_before_physical_http':'Явный внешний budget отклоняет запрос до физического POST и сохраняет task paused.',
 'graph_completion_requires_receipts_and_staleness_propagates':'Typed DAG завершается по настоящим mutation receipts; внешний edit инвалидирует узел и его зависимости.',
 'cycles_unknown_checks_and_user_plan_overwrite_are_rejected':'Циклы/неизвестные check IDs отвергаются; модель не стирает закреплённый пользователем граф.',
 'saved_witness_survives_reload_and_unknown_receipt_is_not_evidence':'Неизвестный эффект не закрывает шаг; успешные witness/receipt links переживают сохранение/загрузку.',
 'legacy_steps_remain_advisory_not_false_completed':'Legacy строковый план мигрирует в proposed/advisory без утверждения выполнения.',
 'watchdog_ignores_receipt_ids_and_preserves_one_recovery_across_resume':'Volatile IDs не маскируют повтор; одна диагностика сохраняется через resume, новые результаты не блокируются.',
 'graph_receipt_reference_survives_compaction':'Сжатие крупного tool output сохраняет точный assistant-batch receipt anchor для TaskGraph evidence.',
 'multi_file_graph_completes_with_scoped_checks_after_compaction':'Два больших файла, три approvals, сжатие контекста и точная check_id проверка закрывают граф по evidence.',
 'failed_check_cannot_be_hidden_by_final_text':'Финальная фраза модели не скрывает exit 1: task paused, verification failed и узел не done.',
 'repeated_results_get_one_diagnostic_then_pause':'Повтор получает одну read-only диагностическую попытку, затем безопасную паузу с checkpoint.',
 'real_restart_preserves_completed_node_and_never_replays_its_write':'Kill/restart Core между шагами сохраняет done узел и не повторяет его файловую операцию после resume.',
 'kill_recovers_parent_child_tree_without_restarting_child':'Kill во время child generation восстанавливает оба registry states/ledger и UI child projection без нового HTTP.',
 'write_sharing_retry_rechecks_revision_before_atomic_replace':'Короткая Windows file lock пауза повторяет только отказавший atomic replace после проверки прежнего SHA, без снятия guards.',
})
TS_NOTES.update({
 'apps/desktop/src/TaskGraphPanel.tsx:TaskGraphPanel':'Показывает canonical DAG и редактор user-owned плана с dependencies/checks; рабочая задача редактируется только после idle.',
 'apps/desktop/src/TaskGraphPanel.tsx:TaskGraphPanel.patch':'Обновляет только локальный черновик одного узла до явного сохранения.',
 'apps/desktop/src/TaskGraphPanel.tsx:TaskGraphPanel.save':'Передаёт whitelist полей выбранного плана trusted IPC и заменяет UI checkpoint только после успешной host validation.',
})

TS_NOTES['apps/desktop/electron/preload.ts:updateTaskPlan']='Передаёт только план выбранного task через фиксированный IPC; эффектов или model calls здесь нет.'

TS_NOTES['apps/desktop/shared/taskTypes.ts:PlanNode']='Тип canonical plan_steps schema 2: зависимости, affected files, проверочные IDs, evidence и состояние; legacy strings поддержаны явно.'

register('agent/tools.py', """
read_file | Читает bounded UTF-8 bytes со stable stat/SHA-256, сохраняет CRLF и не расширяет прежний file-tool лимит.
write_file | Применяет только подтверждённую ревизию; краткий Windows sharing violation повторяет atomic replace после повторной проверки snapshot/пути, не обходя FILE_CHANGED.
""")

register('agent/smart_context.py', """
compact_tool_result | Сокращает только tool data, сохраняя receipt anchor, исходный file SHA отдельно от result digest и ссылки на полный результат.
""")


FILE_NOTES.update({
 'agent/subagent_profiles.py':'Версионированный атомарный каталог readonly профилей, пользовательский CRUD и выключенные черновики модели без повышения прав.',
 'apps/desktop/src/SubagentSettings.tsx':'Настройки исследователей: профиль, инструкция, инструменты чтения, включение, удаление и общий переключатель.',
 'tests/test_subagent_profiles.py':'Долговечность черновиков и запрет повышения прав через модель, повреждение каталога и изоляция возвращаемых данных.',
 'tests/test_response_quality.py':'Строгая оценка завершения, ограниченная доработка, восстановление пустого ответа и отсутствие лишней проверки информационных вопросов.',
})
register('agent/subagent_profiles.py', """
SubagentProfiles | Хранит декларативные профили без отдельного model/execution контура.
SubagentProfiles.__init__ | Привязывает каталог к extensions directory и создаёт reentrant lock.
SubagentProfiles.load | Читает schema 1, проверяет ограничения и уникальность, отказывает при повреждении вместо повышения прав.
SubagentProfiles.validate | Проверяет ограниченный текст, readonly tool allowlist, ID, включение и версию.
SubagentProfiles.catalog | Возвращает независимый снимок данных для UI и выбора профиля.
SubagentProfiles.configure | Разделяет trusted user CRUD и append-only выключенные model drafts; атомарно сохраняет каталог.
SubagentProfiles.resolve | Перед запуском проверяет актуальное включение каталога и выбранного профиля.
""")
register('agent/response_outcome.py', """
parse_completion_assessment | Строго разбирает явный boolean complete; строки, числа, дубликаты и произвольный текст не являются подтверждением.
""")
register('tests/test_subagent_profiles.py', """
SubagentProfileTests.fields | Возвращает минимальный допустимый readonly профиль для независимых negative cases.
""")
register('tests/test_response_quality.py', """
ResponseQualityTests | Проверяет контракт ответа с настоящим engine loop и контролируемым provider fixture.
ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client | Возвращает видимый прогресс и отрицательную typed оценку, считает все обращения.
ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.__init__ | Не создаёт сетевой backend для unit fixture.
ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.create | Разделяет stream answer и nonstream assessment для проверки bounded recovery.
ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.close | Завершает пустой fixture client без сетевых ресурсов.
ResponseQualityTests.test_explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success.Client.cancel | Совместимый cancellation hook fixture без внешних эффектов.
""")
TEST_PURPOSES.update({
 'generated_draft_survives_restart_and_requires_user_enablement':'Черновик переживает новое хранилище, запускается только после user enable и сохраняет версии; удаление запрещает resolve.',
 'model_cannot_overwrite_enable_or_add_capabilities':'Модель не меняет ID, enabled, model или readonly allowlist и не работает при общем отключении.',
 'corruption_fails_closed_and_catalog_copies_cannot_grant_rights':'Копии каталога не изменяют права; повреждение schema не включает default исследователя.',
 'user_profile_narrows_child_tools_and_persists_exact_version':'Настоящий child HTTP получает только пересечение tools, checkpoint хранит точный профиль и версию.',
 'disabled_profile_does_not_create_child_or_inference':'Выключенный черновик даёт ACCESS_DENIED без child run и лишних HTTP.',
 'disabling_subagents_preserves_single_agent_without_child_tools':'Общий switch удаляет делегирование и создание профилей, сохраняя штатное чтение основного агента.',
 'model_creates_only_disabled_draft_via_real_tool_dispatch':'Настоящий parent tool dispatch создаёт выключенный model draft без запуска дочерней модели.',
 'completion_assessment_rejects_truthy_strings_missing_and_ambiguous_json':'complete принимает только boolean; неоднозначный JSON не превращается в положительную оценку.',
 'explicit_incomplete_after_two_recoveries_pauses_instead_of_false_success':'Три отрицательные оценки ограничивают доработку двумя циклами, затем paused вместо completed.',
 'informational_answer_has_no_verification_model_overhead':'Информационный ответ не запускает отдельную model verification и остаётся нормальным completed.',
 'empty_terminal_answer_gets_bounded_text_recovery':'Пустой terminal response получает содержательный текст без фиктивного пустого completed.',
})
TS_NOTES.update({
 'apps/desktop/src/SubagentSettings.tsx:Profile':'Ограниченный readonly профиль с происхождением и версией, без собственного подключения модели.',
 'apps/desktop/src/SubagentSettings.tsx:Catalog':'Снимок общего переключателя и списка профилей.',
 'apps/desktop/src/SubagentSettings.tsx:SubagentSettings':'Редактор инструкции и readonly tools, явное включение/удаление и общий switch в прежнем оформлении.',
 'apps/desktop/src/SubagentSettings.tsx:SubagentSettings.persist':'Сохраняет trusted user draft через существующий IPC; закрывает редактор только при успехе.',
})

register('agent/response_outcome.py', """
answer_format_issue | Проверяет явно запрошенный путь:строка и возвращает только инструкцию исправления формата без выдумывания источника.
""")
TEST_PURPOSES.update({
 'explicit_source_location_format_repairs_without_replaying_tools':'Неправильный формат получает одну текстовую доработку без повторных файловых операций.',
 'format_guard_does_not_apply_to_freeform_questions':'Проверка действует только на явный формат ответа; обычное обсуждение формата не ограничивается.',
})

# Утверждённая оболочка Studio: архив прототипа перечисляется только в карте файлов.
FILE_NOTES.update({
 'apps/desktop/src/ApprovalDialog.tsx':'Рабочий модальный запрос разрешения с типизированным решением и сведениями о действии.',
 'apps/desktop/src/StudioControls.tsx':'Сохраняемая раскладка, доступные разделители панелей, модель под запросом, журнал инструментов и фокус модальных окон.',
 'apps/desktop/src/StudioFileTree.tsx':'Ленивое настоящее дерево проекта с защитой от устаревших ответов после смены папки.',
 'apps/desktop/src/styles/studio.css':'Графитово-мятная дизайн-система и рабочая компоновка IDE, Chat, настроек и узких окон.',
 'apps/desktop/src/useLolaSession.tsx':'Независимая голосовая сессия popup Лолы: загрузка, live events, отправка, остановка, approval и recovery.',
 'tests/electron/run.cjs':'Запускает выбранную нативную Electron-проверку без ELECTRON_RUN_AS_NODE и с наследованием её exit code.',
 'tests/electron/studio-smoke.cjs':'Изолированная полная проверка рабочего renderer/IPC/Core: история, проекты, модель, инструменты, редактор, approvals и восстановление.',
 'tests/electron/studio-layout.cjs':'Нативная проверка pointer/keyboard resize, сохранения раскладок, фокуса, модели под запросом и IME.',
 'tests/electron/studio-visual.cjs':'Снимает реальный renderer на трёх размерах: Chat, работа IDE, tools, история, пустой поиск, ошибка и настройки.',
})
FILE_NOTES['apps/desktop/electron/lolaPreload.ts']='Изолированный preload popup с общим типизированным facade; main разрешает только голосовые операции и собственные chat/run IDs.'
FILE_NOTES['tests/electron/neutral-smoke.cjs']='Стабильный CI entrypoint полной проверки Studio; делегирует tests/electron/studio-smoke.cjs.'
TS_NOTES.pop('apps/desktop/src/App.tsx:App.desktopAction.current',None)
for _key in list(TS_NOTES):
    if _key.startswith('tests/electron/neutral-smoke.cjs:'):
        TS_NOTES[_key.replace('neutral-smoke.cjs:','studio-smoke.cjs:')]=TS_NOTES.pop(_key)
TS_NOTES.update({
 'apps/desktop/electron/desktopLola.ts:ready':'После renderer acknowledgement освобождает отложенные команды открытия чата и действия Лолы.',
 'apps/desktop/electron/lolaPreload.ts:ready':'Подтверждает установку event listener popup до доставки отложенных команд.',
 'apps/desktop/electron/main.ts:allowedLolaRequest':'Ограничивает popup голосовыми API и известными voice chat/run IDs; запрещает основной model/workspace config.',
 'apps/desktop/electron/preload.ts:openLola':'Открывает настоящее отдельное окно Лолы через фиксированный IPC.',
 'apps/desktop/electron/preload.ts:lolaMicrophone':'Сообщает главному wake listener о ручной записи popup, исключая конкурирующий захват.',
 'apps/desktop/src/App.tsx:App.dismiss':'Закрывает IDE drawer и возвращает клавиатурный фокус на кнопку открытия.',
 'apps/desktop/src/App.tsx:App.onRename':'Применяет новое название выбранного разговора из рабочего sidebar.',
 'apps/desktop/src/ApprovalDialog.tsx:ApprovalDialog':'Показывает настоящее ожидающее разрешение, preview и доступные решения через callback.',
 'apps/desktop/src/ChatText.tsx:inline':'Разбирает безопасные inline code, выделение и HTTP(S) ссылки без raw HTML.',
 'apps/desktop/src/ChatText.tsx:Markdown':'Отображает ограниченный Markdown ответа с кодом, таблицами, списками и заголовками.',
 'apps/desktop/src/ChatText.tsx:Markdown.cells':'Выделяет ячейки строк Markdown-таблицы по разделителям.',
 'apps/desktop/src/StudioControls.tsx:Panel':'Допустимые изменяемые панели: навигация, агент, контекст и категории настроек.',
 'apps/desktop/src/StudioControls.tsx:Layout':'Сохраняемые ширины, видимость панелей и сторона контекста Chat.',
 'apps/desktop/src/StudioControls.tsx:validated':'Проверяет finite размеры, ограничивает диапазонами и подставляет defaults.',
 'apps/desktop/src/StudioControls.tsx:readLayout':'Безопасно читает сохранённую раскладку с возвратом defaults при повреждении.',
 'apps/desktop/src/StudioControls.tsx:StudioLayoutProvider':'Публикует общую раскладку и текущую ширину viewport обоим режимам.',
 'apps/desktop/src/StudioControls.tsx:StudioLayoutProvider.resize':'Обновляет viewport после изменения настоящего окна.',
 'apps/desktop/src/StudioControls.tsx:StudioLayoutProvider.update':'Проверяет и сохраняет частичное изменение раскладки.',
 'apps/desktop/src/StudioControls.tsx:useStudioLayout':'Получает типизированную раскладку; требует provider.',
 'apps/desktop/src/StudioControls.tsx:ResizeRail':'Меняет ширину pointer capture, стрелками, Home/End и двойным щелчком.',
 'apps/desktop/src/StudioControls.tsx:LayoutPresets':'Сохраняет и восстанавливает именованные локальные раскладки, сбрасывает панели.',
 'apps/desktop/src/StudioControls.tsx:ComposerModel':'Получает список моделей от сервера, блокирует смену во время запуска и показывает ошибки.',
 'apps/desktop/src/StudioControls.tsx:ComposerModel.select':'Применяет ID через configureModel либо открывает настройки подключения.',
 'apps/desktop/src/StudioControls.tsx:InlineTools':'Отображает реальные tool_activity и статусы в раскрываемых строках переписки.',
 'apps/desktop/src/StudioControls.tsx:DialogFocus':'Удерживает Tab в верхнем видимом modal и возвращает предыдущий фокус.',
 'apps/desktop/src/StudioControls.tsx:DialogFocus.top':'Находит последнее видимое aria-modal окно или открытый dialog.',
 'apps/desktop/src/StudioControls.tsx:DialogFocus.check':'При изменении DOM переводит фокус внутрь нового modal или возвращает при закрытии.',
 'apps/desktop/src/StudioControls.tsx:DialogFocus.keys':'Зацикливает Tab и Shift+Tab среди доступных контролов modal.',
 'apps/desktop/src/StudioFileTree.tsx:Item':'Запись каталога IPC: имя, относительный путь и file/directory kind.',
 'apps/desktop/src/StudioFileTree.tsx:StudioFileTree':'Показывает настоящее дерево проекта, loading, пустые каталоги и ошибки.',
 'apps/desktop/src/StudioFileTree.tsx:StudioFileTree.load':'Читает каталог через listFiles; игнорирует устаревший epoch и сменившийся root.',
 'apps/desktop/src/StudioFileTree.tsx:StudioFileTree.toggle':'Раскрывает каталог и запрашивает ещё не загруженное содержимое.',
 'apps/desktop/src/StudioFileTree.tsx:StudioFileTree.branch':'Рекурсивно строит раскрытые каталоги и строки открытия настоящих файлов.',
 'apps/desktop/src/VoicePanel.tsx:VoicePanel.changed':'Перечитывает настройки голоса после изменения конфигурации в другом окне.',
 'apps/desktop/src/VoiceSettings.tsx:VoiceSettings.preview':'Запрашивает пробную озвучку выбранным голосом и показывает результат сервиса.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession':'Владеет голосовой перепиской popup и headless контроллером записи/воспроизведения.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.select':'Загружает voice chat, snapshot и approval с буферизацией событий во время загрузки.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.send':'Запускает реальную voice задачу после готовности сессии и проверки recovery.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.stop':'Останавливает запись/озвучку и только собственный текущий run.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.resolve':'Применяет пользовательское решение по прерванному tool journal и обновляет snapshot.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.receive.current':'Маршрутизирует команды popup и scoped live events с cursor/run фильтрами.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.clearDraft':'Очищает переданный из STT черновик после переноса в поле popup.',
 'apps/desktop/src/useLolaSession.tsx:useLolaSession.resume':'Продолжает собственную голосовую задачу через тот же send с resume flag.',
 'tests/electron/studio-smoke.cjs:selectIdeConversation':'Открывает историю у чата IDE и выбирает реальный разговор по названию.',
})
for _module in ('studio-layout.cjs','studio-visual.cjs'):
    for _name in ('BrowserWindow.prototype.loadURL','dialog.showSaveDialog','done','releaseStage4','js','click','textButton','input','capture','finish'):
        TS_NOTES['tests/electron/'+_module+':'+_name]=TS_NOTES['tests/electron/studio-smoke.cjs:'+_name]
    TS_NOTES['tests/electron/'+_module+':releaseVisual']='Освобождает удерживаемый fixture SSE после снимка состояния выполняющейся задачи.'
TS_NOTES['tests/electron/studio-layout.cjs:width']='Измеряет ширину настоящей панели после pointer/keyboard resize для проверки clamp и persistence.'

TS_NOTES['BrandMark']='Рисует прежний знак N с точкой равновесия в геометрии и цветах Studio; статические PNG/ICO используют ту же форму.'
TS_NOTES['tests/electron/packaged-smoke.mjs:run']='Проверяет bundled Core/schema 3 и сохранение истории в packaged Studio без Python в PATH; IDE/Chat остаются в main, микрофон проверяется в отдельной Лоле.'

# Readiness audit: active engine corrections and repeatable isolated evidence.
FILE_NOTES.update({
 'tests/migration/test_agent_readiness.py':'Вертикальные A–I сценарии с HTTP-моделью, настоящими разрешениями, файлами, subprocess и контрольными точками в одноразовом проекте.',
 'tests/electron/readiness-live.cjs':'Явно запускаемая desktop приёмка с настоящей моделью LM Studio, readonly ребёнком, правкой и независимой проверкой одноразового проекта.',
 'tools/test_agent_readiness.py':'Запускает изолированный набор готовности и сохраняет JSON со статусом, временем и ошибками каждого теста.',
})
SYMBOL_NOTES.update({
 'agent/engine.py:AgentEngine._check_runtime_deadline':'Проверяет общий deadline с учётом ожидания человека; переносит watchdog, пока разрешение ожидается.',
 'agent/engine.py:AgentEngine._verification_feedback':'Формирует компактные факты проверок и незакрытых шагов для продолжения существующего цикла.',
 'agent/operation_context.py:OperationContext.approval_wait':'Приостанавливает deadlines текущей операции и родителей на время разрешения; отмена остаётся немедленной.',
 'agent/tool_executor.py:ToolExecutor._denial_key':'Определяет повтор отклонённого действия; назначение и check_id не меняют тождество команды.',
 'core/python/task_execution.py:TaskExecution._wait_external_approval':'Публикует внешний preview, освобождает inference gate и ждёт решение пользователя либо отмену.',
 'tests/migration/test_agent_readiness.py:AgentReadinessTests.finish':'Обрабатывает настоящие approval events, проверяет состояния и освобождение scheduler после task_end.',
 'tests/migration/test_agent_readiness.py:AgentReadinessTests.check':'Описывает реальную Python-команду проверки временного проекта без записи bytecode.',
 'tests/migration/test_agent_readiness.py:AgentReadinessTests.fixture':'Создаёт ошибочную функцию и независимую исполняемую проверку в disposable проекте.',
 'tests/migration/test_agent_readiness.py:AgentReadinessTests.receipts':'Читает реальные tool results из канонической истории завершённой задачи.',
 'tests/migration/test_agent_readiness.py:AgentReadinessTests.test_e_h_long_task_retains_goal_and_uses_full_canonical_history.decide':'Проверяет сохранение цели в каждом HTTP-запросе и последовательно выбирает 24 различных файла.',
 'tests/test_project_command.py:ProjectCommandTests.test_replaced_working_directory_after_approval_is_not_executed.replace':'Подменяет каталог во время approval callback и проверяет отказ до запуска процесса.',
 'tools/test_agent_readiness.py:EvidenceResult.startTest':'Запоминает идентификатор, ожидание и начальный момент теста.',
 'tools/test_agent_readiness.py:EvidenceResult.addFailure':'Сохраняет assertion traceback и FAILED в отчёте.',
 'tools/test_agent_readiness.py:EvidenceResult.addError':'Сохраняет исключение инфраструктуры или теста и FAILED в отчёте.',
 'tools/test_agent_readiness.py:EvidenceResult.addSkip':'Отмечает непройденный сценарий UNVERIFIED с причиной пропуска.',
 'tools/test_agent_readiness.py:EvidenceResult.addSubTest':'Переносит ошибку subTest в общий статус тестового сценария.',
 'tools/test_agent_readiness.py:EvidenceResult.stopTest':'Завершает измерение времени и добавляет запись в JSON evidence.',
})
TEST_PURPOSES.update({
 'a_exploration_returns_current_source_references':'исследование возвращает актуальные строки файла и корректную ссылку.',
 'b_simple_edit_and_real_test':'правка проходит diff approval, затем настоящий Python-тест подтверждает результат.',
 'c_multi_file_json_edit_and_test':'strict JSON выполняет согласованные правки двух файлов и реальную проверку.',
 'd_failed_auto_check_returns_to_model_and_recovers':'AssertionError автоматической проверки возвращается модели; исправление и повторный тест дают успех.',
 'd_auto_checks_run_even_without_file_edits':'заданные пользователем auto checks выполняются и без предшествующей записи.',
 'g_denied_auto_check_is_not_automatically_replayed':'отказ проверки сохраняется и не вызывает повторного approval.',
 'g_rejected_edit_is_returned_to_model':'отклонённая правка не меняет файл, USER_DENIED возвращается следующему запросу.',
 'g_repeated_denied_command_does_not_prompt_again':'смена purpose/check_id не позволяет повторно предложить отклонённую команду в том же запуске.',
 'e_h_long_task_retains_goal_and_uses_full_canonical_history':'24 больших результата превышают рабочий контекст, но цель, ссылки и полная история сохраняются.',
 'i_cancel_approval_then_resume_without_duplicate_effect':'остановка на approval сохраняет resumable checkpoint без повторения эффекта.',
 'child_transport_failure_returns_control_to_parent':'после ограниченных HTTP-повторов ошибка ребёнка возвращается родителю и освобождает scheduler.',
 'chat_explains_subagent_mode_without_exposing_project_tools':'Chat объясняет доступность субагентов в IDE без выдачи файловых или дочерних инструментов.',
 'replaced_working_directory_after_approval_is_not_executed':'подмена cwd между preview и подтверждением блокирует запуск программы.',
 'subagent_tools_remain_discoverable_and_preferred_when_requested':'русский поиск находит субагентов; бюджет сохраняет предпочитаемые разрешённые схемы.',
 'approval_wait_freezes_nested_deadlines_but_not_cancellation':'человеческое ожидание не расходует deadline родителя/ребёнка; Stop распространяется сразу.',
 'approval_exception_restores_deadline_once':'исключение во вложенном approval снимает паузу и сдвигает deadline ровно один раз.',
 'archive_uses_serialized_message_size':'архив учитывает JSON escaping и помещается в окно, сохраняя исходную историю и актуальный SHA256.',
 'decoded_final_history_restores_json_without_promoting_examples':'декодированный ответ возвращается в JSON envelope; показанные примеры инструментов остаются текстом, каноническая история не меняется.',
 'readonly_parent_hint_matches_child_capabilities':'readonly родитель может делегировать чтение, но подсказка и схемы не обещают создание профиля.',
})
TS_NOTES.update({
 'tests/electron/readiness-live.cjs:BrowserWindow.prototype.show':'Подавляет показ окна только в headless тесте; NEUTRAL_INSPECT_GUI оставляет окно для осмотра.',
 'tests/electron/readiness-live.cjs:dialog.showOpenDialog':'Выбирает только созданную тестом disposable папку через штатный workspace UI.',
 'tests/electron/readiness-live.cjs:js':'Выполняет сценарий внутри настоящего Electron renderer.',
 'tests/electron/readiness-live.cjs:poll':'Ожидает наблюдаемое состояние DOM с ограничением времени теста.',
 'tests/electron/readiness-live.cjs:click':'Нажимает найденный элемент интерфейса.',
 'tests/electron/readiness-live.cjs:input':'Заполняет React input/textarea штатным setter и input event.',
 'tests/electron/readiness-live.cjs:button':'Нажимает кнопку с точным текстом в указанной области.',
 'tests/electron/readiness-live.cjs:capture':'Сохраняет PNG настоящего renderer для проверки layout и разрешений.',
 'tests/electron/readiness-live.cjs:finish':'Сохраняет фактический checkpoint, события, решения и screenshot; отмечает ошибки приёмки.',
 'tests/electron/readiness-live.cjs:win.webContents.send':'Наблюдает реальные Core events и approval для отчёта, затем передаёт их штатному renderer.',
})


FILE_NOTES.update({
 'agent/project_knowledge.py':'Память проекта: bounded записи с происхождением, SHA источников, инвалидацией доступа, лексическим/структурным поиском и свежестью перед POST.',
 'apps/desktop/src/ProjectKnowledgePanel.tsx':'Редактор решений, фактов и гипотез; источники, статусы актуальности, поиск, исправление и удаление без model calls.',
 'tests/test_project_knowledge.py':'Проверки изоляции и свежести памяти, CAS, закрытия источников, транспортного retry и сохранения повреждённых данных.',
 'tests/migration/test_project_memory_v2.py':'Настоящий parent HTTP flow: гипотеза модели, новые чаты, актуальные решения и исключение изменённых источников.',
})
register('agent/project_knowledge.py', """
now | Даёт UTC timestamp только при создании или изменении записи.
ProjectKnowledge | Bounded каталог профильной памяти вне проекта; не заменяет канонические чаты и журналы.
ProjectKnowledge.__init__ | Привязывает каталог knowledge.json к каноническому корню проекта и существующему профилю памяти.
ProjectKnowledge.load | Строго проверяет bounded schema и provenance, не исправляя повреждённый исходник молча.
ProjectKnowledge.save | Атомарно сохраняет ограниченный каталог без автоматического удаления пользовательских решений.
ProjectKnowledge.witness | Хеширует только разрешённые выбранные файлы с ограниченным IO и повторной проверкой политики после чтения.
ProjectKnowledge.assess | Отмечает изменение, удаление, отзыв доступа и смену политики; не объявляет гипотезу фактом или старую проверку текущей.
ProjectKnowledge.listing | Ранжирует текст и пути, затем исключает недоступные/устаревшие записи до model projection.
ProjectKnowledge.put | Создаёт host ID/время/provenance и source witnesses; модель может сохранять только гипотезы по известным источникам.
ProjectKnowledge.remove | Удаляет выбранную запись без изменения диалогов и исходного журнала.
ProjectKnowledge.context | Строит bounded справочные данные с явным различием свежести источника и истинности вывода.
invalid_source_path | Отклоняет абсолютный путь, диск Windows и traversal до разрешения источника.
remember_from_model | Сверяет источники с успешными read receipts текущего journal и сохраняет только гипотезу.
capture_task_memory | Получает наблюдения файлов, scoped проверок и завершённой задачи из durable receipts/checkpoint, без копирования ответа модели.
memory_projection | Создаёт одно ограниченное data-сообщение с host metadata, удаляемой перед API.
validate_memory_projection | Перед POST, после очереди и при retry убирает изменённую память; сохранённые tool результаты сверяются заново.
has_memory_projection | Находит host маркер и известные memory tools в original messages для транспортной перепроверки.
""")
register('agent/project_memory.py', """
current_user_notes | Подаёт в модель только пользовательские заметки с актуальной политикой; legacy/model summaries остаются в редакторе как история.
""")
register('core/python/memory_service.py', """
memory_action | Принимает только trusted UI CRUD/search с CAS и expected root; не даёт модели повышать гипотезы до пользовательских фактов.
""")
register('tests/test_project_knowledge.py', """
ProjectKnowledgeTests | Изолированные negative gates памяти и реальная HTTP проверка invalidation при повторе.
ProjectKnowledgeTests.put | Создаёт короткую пользовательскую запись с источником main.py для независимых проверок.
ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler | Реальный localhost provider: меняет источник между первым HTTP 500 и повтором.
ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler.log_message | Подавляет служебный access log fixture.
ProjectKnowledgeTests.test_http_retry_rechecks_fitted_memory_before_second_post.Handler.do_POST | Сохраняет payload, изменяет файл и возвращает bounded retry либо terminal JSON.
""")
register('tests/migration/test_project_memory_v2.py', """
MemoryHandler | Управляемый localhost provider для настоящего read/remember/final/verification flow.
MemoryHandler.log_message | Подавляет HTTP access log fixture.
MemoryHandler.do_GET | Объявляет только synthetic модель изолированного теста.
MemoryHandler.do_POST | Предлагает чтение и запись гипотезы либо финальный ответ; сохраняет реальные запросы для проверки контекста.
ProjectMemoryHttpTests | Сквозные сценарии TaskService с отдельным профилем, включением памяти и новыми чатами.
ProjectMemoryHttpTests.start | Запускает native engine с памятью и ждёт terminal task с закрытым worker.
""")
TEST_PURPOSES.update({
 'new_instance_finds_decision_and_timestamp_does_not_change_on_reads':'Новый экземпляр находит решение по проекту, чтение сохраняет timestamps, другой root не видит запись.',
 'file_changes_deletion_and_revocation_remove_entire_model_note':'Внешняя правка, удаление и запрет neutralignore убирают всю запись из model context.',
 'policy_change_invalidates_sourceless_decision_and_gitignore_source':'Изменение политики закрывает даже заметку без источников; gitignore применяется к привязанному файлу.',
 'ui_cas_preserves_external_edits_and_rejects_root_switch':'UI CAS учитывает оба каталога памяти, отклоняет старый revision и смену проекта, user notes сверяют политику.',
 'model_proposal_cannot_promote_or_anchor_unread_sources':'Модель не создаёт подтверждённый факт и не связывает вывод с непрочитанным источником; traversal запрещён.',
 'old_tool_memory_is_reprojected_after_revocation_without_changing_history':'Сохранённый tool answer не возвращает закрытую память в новый запрос; canonical transcript сохранён.',
 'legacy_and_model_notes_are_not_automatically_presented_as_current':'Старые и модельные summaries доступны в UI, но не подаются как актуальная справка.',
 'context_is_bounded_and_no_semantic_verification_is_invented':'Ранжированная проекция имеет ограниченный размер и не выдаёт хеш источника за доказательство вывода.',
 'fitted_memory_is_removed_after_change_and_metadata_never_reaches_api':'Смена source после fit исключает memory message; служебный маркер не передаётся в API.',
 'http_retry_rechecks_fitted_memory_before_second_post':'Настоящий provider меняет файл между HTTP 500 и retry; второй POST не содержит закрытые данные.',
 'corrupt_record_catalog_is_reported_without_rewriting_it':'Повреждённый provenance обнаруживается без перезаписи исходного файла.',
 'new_chat_receives_decision_and_hypothesis_but_changed_source_removes_both':'Реальный engine сохраняет гипотезу и наблюдения, новый чат находит решение, внешний edit исключает его.',
 'disabling_memory_group_removes_tools_and_automatic_projection':'Общий switch памяти исключает tools и автоматическую подачу данных следующему запуску.',
})
TS_NOTES.update({
 'apps/desktop/src/ProjectKnowledgePanel.tsx:RecordNote':'Запись памяти с типом, источниками, временем, происхождением и вычисленным состоянием актуальности.',
 'apps/desktop/src/ProjectKnowledgePanel.tsx:Draft':'Локальный черновик user-owned решения, факта или гипотезы до CAS сохранения.',
 'apps/desktop/src/ProjectKnowledgePanel.tsx:ProjectKnowledgePanel':'Показывает bounded список записей и редактор источников в существующем стиле Studio.',
 'apps/desktop/src/ProjectKnowledgePanel.tsx:ProjectKnowledgePanel.action':'Передаёт fixed IPC с revision/root; сохраняет черновик при конфликте и обновляет UI только при успехе.',
 'apps/desktop/electron/preload.ts:projectMemoryAction':'Передаёт только memory CRUD/search через фиксированный IPC без доступа renderer к файловой системе.',
})

TEST_PURPOSES['external_memory_preview_is_text_and_rejection_keeps_data_out_of_model']='Внешняя модель получает данные памяти только после текстового preview; отказ не пропускает приватную запись ни в один HTTP payload.'

TS_NOTES['saveProjectMemory']='Сохраняет семь справочных полей через fixed IPC с CAS revision и optional expected root; renderer не пишет файлы напрямую.'


FILE_NOTES.update({
 'agent/verification_plan.py':'Детерминированный выбор пользовательских проверок по затронутым путям; связанные критерии не пропускаются.',
 'agent/diagnostics_evidence.py':'LSP как проверяемое свидетельство: user check, сохранённые файлы, настройки сервера, approval и строгая полнота результата.',
 'agent/git_checkpoints.py':'Приватный bare Git архив before/after подтверждённых snapshots; не меняет индекс, ветку, hooks и файлы проекта.',
 'tests/test_stage17_verification.py':'Gate этапа 17: выбор проверок, настоящие LSP процессы, изоляция Git, CRLF и внешняя правка во время rollback.',
 'tests/migration/test_stage17_workflow.py':'Сквозные checks-only LSP и асинхронный Core checkpoint API с проверкой responsiveness и сохранности исходника.',
})
register('agent/verification_plan.py', """
required_checks | Выбирает проверки только по явным applies_to; критерии готовности и ручной checks-only требуют соответствующие проверки независимо от пути.
""")
register('agent/diagnostics_evidence.py', """
config_digest | Привязывает LSP evidence к enabled/program/argv/language/timeout серверного профиля.
run_diagnostics | Показывает точный сервер и файл, получает approval, выполняет существующий LSP клиент и сохраняет source witnesses.
assess_diagnostics | Проверяет check/config/rollback/доступ/хеши; incomplete push или реальные ошибки не становятся clean evidence.
assess_diagnostics.verdict | Возвращает typed оценку с явной файловой областью, без подтверждения всего проекта.
""")
register('agent/git_checkpoints.py', """
GitCheckpoints | Хранит неизменяемые версии подтверждённых правок в отдельном Git Neutral, не подменяя конфликтный rollback.
GitCheckpoints.__init__ | Выбирает отдельный per-project каталог профиля и private bare repository.
GitCheckpoints.info | Читает bounded метаданные только своего snapshot group и repository для UI после restart.
GitCheckpoints.create | Экспортирует проверенные before/after bytes и manifest, создаёт private tree/commit/ref; не читает индекс пользователя.
GitCheckpoints.create.git | Выполняет только заданные Git plumbing команды с отключёнными hooks/global config и ограниченным временем/выводом.
""")
register('agent/verifier.py', """
StageVerifier.record_diagnostics | Записывает LSP отдельно от exit codes команды; провал другой проверки не стирается.
""")
register('core/python/workspace_review.py', """
WorkspaceReview.start_checkpoint | Проверяет выбранный root/chat, затем запускает Git в существующем BackgroundJob без блокировки stdio dispatch.
WorkspaceReview.start_checkpoint.work | Создаёт private checkpoint только захваченного scope и group, с общим cancellation context.
WorkspaceReview.shutdown | Отменяет собственные Git задачи при завершении Core.
""")
register('tests/test_stage17_verification.py', """
Stage17Tests | Изолированные regression gates выбора проверок, LSP и Git/checkpoint recovery.
Stage17Tests.lsp_task | Формирует user-defined scoped LSP check и выполняет настоящий stdio fixture сервер.
Stage17Tests.test_external_edit_during_multi_file_rollback_is_preserved_and_requires_review.restore | Вставляет внешнюю правку второго файла после восстановления первого, проверяя конфликтный контракт.
""")
register('tests/migration/test_stage17_workflow.py', """
Stage17HttpTests | Настоящий TaskService checks-only flow с approved LSP и без обращения к модели.
Stage17HttpTests.run_lsp | Настраивает известный LSP fixture, ждёт точный approval и terminal task, проверяет нулевой HTTP расход.
Stage17BridgeTests | Реальный stdio Core, async Git checkpoint и сохранность агентской правки.
""")
TEST_PURPOSES.update({
 'full_lsp_clean_is_scoped_and_file_or_server_change_invalidates':'Полный чистый pull подтверждает только файл, изменение файла или конфигурации делает результат stale.',
 'lsp_errors_and_incomplete_push_never_pass':'Ошибки LSP и неполный push не позволяют объявить проверку успешной.',
 'user_selectors_skip_unrelated_checks_but_not_acceptance_requirements':'applies_to пропускает только нерелевантные проверки; критерий и ручной checks-only сохраняют обязательность.',
 'git_snapshot_uses_confirmed_bytes_and_never_changes_project_index_or_head':'Private Git возвращает точные before/after bytes, включая CRLF, и сохраняет HEAD/index проекта.',
 'external_edit_during_multi_file_rollback_is_preserved_and_requires_review':'Внешний edit между восстановлением двух файлов не перезаписывается, результат rollback_unknown требует ручной проверки.',
 'command_receipt_cannot_impersonate_lsp_check':'Обычная команда не наследует LSP check_id/evidence; некорректная severity не превращается в отсутствие ошибок.',
 'revoked_lsp_source_is_hidden_from_future_model_history':'Отзыв доступа удаляет LSP diagnostics из model projection, не меняя canonical history.',
 'complete_lsp_check_and_criterion_pass_without_model_http':'Checks-only LSP через реальный worker и approval подтверждает criterion; изменение сервера инвалидирует evidence.',
 'lsp_error_keeps_task_paused_and_does_not_satisfy_criterion':'LSP errors оставляют задачу paused и критерий failed без model HTTP.',
 'checkpoint_api_saves_confirmed_write_and_keeps_core_responsive':'Асинхронный private Git RPC позволяет health ответ во время работы и сохраняет подтверждённую агентскую запись.',
})
TS_NOTES.update({
 'apps/desktop/src/WorkspaceReview.tsx:WorkspaceReview.saveCheckpoint':'Сохраняет known snapshot в private Git через fixed async IPC; показывает repository/commit/ref и сохраняет текущий проект.',
 'apps/desktop/electron/preload.ts:createGitCheckpoint':'Отправляет выбранный chat/group для архивирования в отдельном Git без прямого файлового доступа renderer.',
 'apps/desktop/electron/preload.ts:cancelGitCheckpoint':'Отменяет только собственную background задачу создания private Git checkpoint.',
})

# Stage 18: isolated Code-OSS feasibility prototype, not default editor migration.
FILE_NOTES.update({
 'apps/desktop/electron/neutralIde.ts':'Собственный Code-OSS launcher: отдельные runtime/profile/shared storage и авторизованный named pipe только для status/focus.',
 'tests/electron/neutral-ide-smoke.cjs':'Изолированная проверка кнопки Neutral IDE, root/dirty guards, собственного executable/profile и реального Core через auth/allowlist.',
 'prototypes/neutral-ide/README.md':'Подготовка и запуск отдельной Neutral IDE; команды тестов и граница прототипа.',
 'prototypes/neutral-ide/prepare.py':'Закреплённый Code-OSS/VSCodium ZIP, SHA-256, product/PE branding, ресурсы и установка встроенного extension без изменения пользовательского VS Code.',
 'prototypes/neutral-ide/install_test_extensions.py':'Установка закреплённых MIT Open VSX расширений и локального probe VSIX через настоящий CLI в отдельный test profile.',
 'prototypes/neutral-ide/test_host.py':'Запуск настоящих Extension Host и normal-workbench UI тестов на одноразовых проектах; проверяет passed report, а не только exit code.',
 'prototypes/neutral-ide/extensions.lock.json':'Зафиксированные версии, engines, платформы, лицензии и SHA-256 пяти проверяемых Open VSX расширений.',
 'prototypes/neutral-ide/extension/package.json':'Встроенный Neutral extension: команды, theme и activity-bar webview contribution для Code-OSS.',
 'prototypes/neutral-ide/extension/theme.json':'Neutral Studio palette для собственной Code-OSS IDE.',
 'prototypes/neutral-ide/extension/icon.svg':'Векторная N-иконка activity bar встроенного Neutral extension.',
 'prototypes/neutral-ide/extension/extension.cjs':'Собственная боковая панель Core status/focus и прототип editor-owned diff с version/hash guards и явным modal.',
 'prototypes/neutral-ide/tests/host.cjs':'Реальные API checks: tabs/splits/save/undo, stale edits, TypeScript, Open VSX theme/snippet/formatter/YAML, PTY и debugpy breakpoint.',
 'prototypes/neutral-ide/tests/drive.cjs':'Локальный CDP-драйвер обычного test workbench: ввод replacement, screenshot и нажатие явного подтверждения.',
 'prototypes/neutral-ide/tests/processes.cjs':'Windows metadata своего дерева PID для ограниченной startup/RSS/CPU оценки.',
 'prototypes/neutral-ide/tests/ui-probe/package.json':'Только тестовый extension, который проверяет modal в normal development host; не копируется в runtime.',
 'prototypes/neutral-ide/tests/ui-probe/extension.cjs':'Проверяет подтверждённый editor buffer edit, неизменность диска и undo в настоящем окне Code-OSS.',
})
SYMBOL_NOTES.update({
 'prototypes/neutral-ide/prepare.py:main':'Проверяет upstream pin/archive и изолированно подготавливает Neutral runtime с лицензиями, иконкой и extension.',
 'prototypes/neutral-ide/install_test_extensions.py:main':'Сверяет VSIX SHA-256 и устанавливает фиксированные расширения и локальный probe в одноразовый профиль через Code-OSS CLI.',
 'prototypes/neutral-ide/test_host.py:main':'Создаёт одноразовый проект, запускает host или UI сценарий и требует успешный JSON report.',
})
TS_NOTES.update({
 'openNeutralIde':'Вызывает фиксированный main IPC запуска собственного Neutral IDE; renderer не передаёт executable или произвольные аргументы.',
 'tests/electron/neutral-ide-smoke.cjs:BrowserWindow.prototype.show':'Скрывает только окно тестируемого desktop, не меняя его Core/IPC.',
 'tests/electron/neutral-ide-smoke.cjs:dialog.showOpenDialog':'Выбирает одноразовый тестовый проект для настоящего project route.',
 'tests/electron/neutral-ide-smoke.cjs:ipcMain.handle':'Сохраняет результат настоящего ide:open для проверки собственного PID и последующего закрытия тестового дерева.',
 'tests/electron/neutral-ide-smoke.cjs:delay':'Небольшая асинхронная пауза в polling smoke.',
 'tests/electron/neutral-ide-smoke.cjs:js':'Выполняет действия в renderer реального тестового окна Neutral.',
 'tests/electron/neutral-ide-smoke.cjs:wait':'Ожидает проверяемое условие с конечным timeout.',
 'tests/electron/neutral-ide-smoke.cjs:request':'Обращается к реальному named pipe для status/focus и отрицательных auth/allowlist checks.',
 'tests/electron/neutral-ide-smoke.cjs:finish':'Сохраняет отчёт, закрывает собственную IDE/process tree и завершает Electron с корректным exit code после штатного quit.',
})

FILE_NOTES.update(CURRENT_FILE_NOTES)
FILE_NOTES.update({
 'apps/desktop/src/idePanel/acceptanceChecks.ts':'Подготовка существующих IdeOptions, изоляция draft по chat_id и readonly/resume guard без нового executor.',
 'apps/desktop/src/idePanel/acceptanceSettings.tsx':'Независимый editor критериев, команд, scopes и ручного запуска checks_only в новой IDE.',
 'tests/electron/ide-acceptance.cjs':'Реальный UI/Core сценарий: без модели, отказ, missing import exit1→repair→exit0, stale evidence и draft isolation.',
 'tests/electron/ide-acceptance-run.cjs':'Запускает native IDE fixture в отдельном acceptance режиме; --json выбирает строгий JSON fixture.',
 'tests/electron/ide-acceptance.test.cjs':'Node regressions сериализации, argv/scope/check_id, readonly/resume и восстановления draft.',
})
TS_NOTES.update({
 'apps/desktop/src/idePanel/acceptanceChecks.ts:AcceptanceDraft':'Локальный editable draft с точным chat_id, не canonical evidence.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:canResumeInMode':'Не позволяет Ask/Plan возобновить сохранённую Agent-задачу с правом выполнения команд.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:emptyAcceptanceOptions':'Создаёт независимый пустой набор options без общих mutable arrays.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:copyOptions':'Копирует массивы критериев, links, argv и scope/dependencies перед редактированием.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:isDraft':'Проверяет форму восстановленного view draft, допуская незавершённый ввод и отклоняя повреждённые структуры.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:isDraft.strings':'Проверяет массив строк локального draft.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:acceptanceDraftForChat':'Восстанавливает только draft выбранного чата либо копию его canonical checkpoint options.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:removeAcceptanceCheck':'Удаляет check definition и его связи с критериями, не мутируя исходный draft.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:paths':'Нормализует явные relative file/dependency paths для существующего Core evidence scope.',
 'apps/desktop/src/idePanel/acceptanceChecks.ts:prepareAcceptanceOptions':'Сохраняет argv/check_id/scope, нормализует критерии и links, исключает команды в Ask/Plan и валидирует checks_only.',
 'apps/desktop/src/idePanel/acceptanceSettings.tsx:AcceptanceSettings':'Редактор пользовательских критериев, команд, LSP/scopes и запуска проверок без модели.',
 'apps/desktop/src/idePanel/acceptanceSettings.tsx:AcceptanceSettings.updateCheck':'Обновляет выбранный check с сохранением его stable id.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.changeChecks':'Сохраняет draft только для текущего чата и синхронный ref для отправки.',
 'tests/electron/ide-acceptance.cjs:runAcceptance':'Выполняет native/JSON вертикальный сценарий configured checks через настоящий Core и editor.',
 'tests/electron/ide-acceptance.cjs:runAcceptance.input':'Вводит поле по доступному имени через React-совместимый DOM setter.',
 'tests/electron/ide-acceptance.cjs:runAcceptance.textButton':'Нажимает кнопку с точной подписью в acceptance fixture.',
 'tests/electron/ide-acceptance.cjs:runAcceptance.nav':'Открывает раздел новой панели по подписи навигации.',
 'tests/electron/ide-acceptance.cjs:runAcceptance.loadCurrent':'Читает canonical checkpoint текущего тестового чата после завершения запуска.',
 'tests/electron/ide-acceptance.cjs:runAcceptance.approve':'Разрешает или отклоняет точную команду и ожидает task_end, не путая его с закрытием approval.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde.setCheckField':'Настраивает packaged check по доступному имени, дожидаясь React commit.',
})
register('tests/test_agent_benchmark.py', '''
AgentBenchmarkTests.test_auto_budget_trial_is_explicit_and_manual_default_is_preserved | Явный auto эксперимент передаёт режим в существующий Engine, сохраняя manual 8192 по умолчанию.
''')
FILE_NOTES.update({
 'apps/desktop/src/idePanel/connectionSettings.tsx':'Самостоятельная форма подключения и оформления; редактируемые настройки отделены от сохранённых.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts':'Общий recovery gate и минимальная диагностика по allowlist без текста, путей и ключей.',
 'apps/desktop/src/idePanel/sessionState.ts':'Типы состояния новой панели и чистое преобразование событий с chat/run/sequence isolation.',
 'tests/electron/ide-session.test.cjs':'Node-проверки ранних и повторных событий, завершённых runs и редактирования безопасной диагностики.',
})
TS_NOTES.update({
 'apps/desktop/shared/createApi.ts:createApi.copyTaskDiagnostics':'По явному действию пользователя копирует минимальный диагностический JSON через фиксированный host channel.',
 'apps/desktop/src/idePanel/connectionSettings.tsx:ConnectionSettings':'Отображает независимую форму подключения, preview тем и подсказку о плане, правилах и MCP.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts:RecoveryState':'Минимальные поля задачи, влияющие на блокировку восстановления.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts:hasRecoveryBlockers':'Запрещает resume при неизвестном действии, нечитаемом журнале или неподтверждённом rollback.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts:safeId':'Пропускает только ограниченный hex-идентификатор; произвольный текст в диагностику не попадает.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts:count':'Принимает только неотрицательный целочисленный счётчик.',
 'apps/desktop/src/idePanel/recoveryDiagnostics.ts:recoveryDiagnostics':'Строит bounded JSON с идентичностями, счётчиками и recovery flags, без error narrative и исходников.',
 'apps/desktop/src/idePanel/runActivity.tsx:RunActivity.copyDiagnostics':'Показывает pending/result копирования безопасной диагностики.',
 'apps/desktop/src/idePanel/runActivity.tsx:RunActivity.confirmObservation':'Ожидает подтверждение Core; ошибка сохраняет проверяемое решение на экране.',
 'apps/desktop/src/idePanel/sessionState.ts:Line':'Тип строки переписки с ролью, текстом и optional message id.',
 'apps/desktop/src/idePanel/sessionState.ts:Reference':'Сохранённая ссылка на диапазон файла редактора.',
 'apps/desktop/src/idePanel/sessionState.ts:SessionIdentity':'Точный chat/run и последняя принятая последовательность события.',
 'apps/desktop/src/idePanel/sessionState.ts:PanelApproval':'Существующий approval payload из общего протокола.',
 'apps/desktop/src/idePanel/sessionState.ts:ModelConnection':'Тип сохранённого или редактируемого подключения панели.',
 'apps/desktop/src/idePanel/sessionState.ts:ChatSelection':'Результат выбора чата с checkpoint, approval и active run.',
 'apps/desktop/src/idePanel/sessionState.ts:SessionUpdate':'Изменяемые проекции одного принятого события панели.',
 'apps/desktop/src/idePanel/sessionState.ts:projectTaskEvent':'Отклоняет чужие/старые/невалидные события, обновляет текст и lifecycle без побочных эффектов.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.setMessages':'Синхронно обновляет transcript ref и React state, сохраняя соседние delta до следующего render.',
})
FILE_NOTES['tests/electron/packaged-ide.mjs']='CDP-приёмка вложенной IDE свежего пакета: frozen Core, diff approval, editor-owned запись и Undo/Save.'
TS_NOTES.update({
 'tests/electron/packaged-ide.mjs:until':'Ожидает конкретное условие packaged IDE с конечным timeout и последней ошибкой.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde':'Открывает временный workspace в упакованной IDE и проверяет approval, запись и Undo без системного Python.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde.socket.onmessage':'Разбирает CDP contexts и коррелированные ответы собственной IDE.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde.send':'Отправляет CDP-команду с уникальным id и ограниченным ожиданием.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde.evaluate':'Выполняет выражение в выбранном CDP context и проверяет исключения.',
 'tests/electron/packaged-ide.mjs:verifyPackagedIde.panel':'Выполняет выражение только в webview упакованной панели агента.',
 'tests/electron/packaged-smoke.mjs:run.desktop':'Передаёт последовательные CDP-выражения desktop в packaged IDE acceptance helper.',
})
FILE_NOTES.update({
 'tests/electron/packaged-path.mjs':'Выбирает точный Windows executable из конфигурации сборки либо явного пути без fallback на старый бренд.',
 'tests/electron/packaged-path.test.mjs':'Проверки чистого LESHY output, старого Neutral output, обоих файлов и явного пути пакета.',
})
TS_NOTES.update({
 'tests/electron/packaged-path.mjs:resolvePackagedExecutable':'Разрешает существующий файл текущего productName/executableName или точного переданного пути.',
 'tests/electron/packaged-path.test.mjs:fixture':'Создаёт одноразовую конфигурацию и output с заданными именами executable.',
})
FILE_NOTES['tests/test_docs_reference.py']='Проверка инвентаризации стороннего CLI без включения его внутренностей в API приложения.'
register('tests/test_docs_reference.py', '''
ReferenceInventoryTests | Проверяет инвентаризацию и вход AST extractor для стороннего и собственного кода.
ReferenceInventoryTests.test_vendor_is_in_inventory_but_not_in_ast_or_toc | Сторонний CLI остаётся в file map, но не передаётся extractor и не попадает в оглавление API; собственный entrypoint остаётся.
''')
FILE_NOTES.update({
 'agent/chat_store.py':'Разговоры и метаданные истории в транзакционном SQLite с миграцией старых JSON.',
 'agent/task_store.py':'Checkpoint задач в SQLite и совместимость прежнего файлового хранения.',
 'agent/verifier.py':'Оценка фактических команд и diagnostics с учётом области и свежести исходников.',
})
register('core/python/bridge.py', '''
current_root | Возвращает корень scoped IDE view или выбранный desktop workspace.
''')
register('core/python/ide_completion.py', '''
complete | Проверяет локальность endpoint, путь и размер контекста, запрашивает короткое автодополнение и закрывает клиент.
''')
register('core/python/ide_sessions.py', '''
IdeSessions | Изолирует выбор чата, workspace и editor adapter разных IDE views единого Core.
IdeSessions.attach | Проверяет папку, создаёт отдельную сессию и связывает её с editor adapter.
IdeSessions.detach | Отменяет только активные запуски закрываемого IDE view.
IdeSessions.control | Временно выбирает сессию владельца IDE run для удалённого управления; неоднозначный запуск не выбирает.
IdeSessions.scope | Проверяет allowlist операции и устанавливает contextvars конкретного IDE view на время RPC.
IdeSessions.request | Отправляет editor operation и ждёт связанный ответ с отменой и конечным timeout; apply без ответа остаётся unknown.
IdeSessions.complete | Принимает единственный валидный ответ с совпадающими session_id и operation_id.
IdeWorkspaceAdapter | Делегирует запись выбранному редактору вместо Python writer.
IdeWorkspaceAdapter.guard | Запрашивает у редактора предварительную проверку workspace.
IdeWorkspaceAdapter.prepare | Получает editor state для конкретного предложения до approval.
IdeWorkspaceAdapter.execute | Повторно проверяет disk snapshot и передаёт подтверждённое изменение editor-owned apply.
''')
register('core/python/task_service.py', '''
TaskService.sessions | Getter/setter выбранной SessionService в desktop или scoped IDE контексте.
TaskService.workspace_adapter | Возвращает editor adapter текущего IDE контекста.
''')
register('tests/migration/test_ide_sessions.py', '''
IdeScopeBridgeTests | Реальный bridge fixture с несколькими независимыми IDE views.
IdeScopeBridgeTests.scoped | Вызывает bridge method в явно выбранной IDE-сессии.
IdeScopeBridgeTests.test_ide_root_and_selection_do_not_mutate_desktop_or_other_view | Выбор корня и чата одной IDE не меняет desktop или соседний view.
IdeScopeBridgeTests.test_editor_prepare_apply_receipts_are_scoped_and_python_never_writes | Ответы prepare/apply привязаны к editor scope, Python writer не выполняется.
IdeScopeBridgeTests.test_closed_ide_cancels_only_its_run_before_file_effect | Закрытие IDE отменяет её run до файлового эффекта, не затрагивая другие.
''')
register('tests/test_companion_policy.py', '''
LolaIdeIsolationTests.test_lola_delegate_schema_and_runtime_exclude_ide | Лола не получает полномочия IDE через схему или runtime delegation.
LolaIdeIsolationTests.test_old_pending_lola_ide_handoff_cannot_start_ide | Старый handoff Лолы не обходит текущую изоляцию IDE.
''')
register('tests/test_ide_completion.py', '''
CompletionTests | Ограничения и жизненный цикл локального автодополнения.
CompletionTests.test_remote_does_not_construct_client | Удалённый endpoint не создаёт completion client.
CompletionTests.test_outside_root_rejected | Файл за пределами проекта отклоняется до запроса.
CompletionTests.test_small_request_no_tools_and_cleanup | Короткий completion не включает инструменты и закрывает клиент.
CompletionTests.test_large_context_rejected_before_http | Слишком большой completion context не отправляется по HTTP.
''')
register('tests/test_ide_execution.py', '''
IdeExecutionTests | Executor fixture, проверяющий editor-owned записи и конфликтные состояния.
IdeExecutionTests.write_call | Создаёт конкретное предложение write_file для executor fixture.
IdeExecutionTests.test_dirty_editor_rejects_before_approval_and_never_uses_python_writer | Dirty buffer отклоняет предложение до approval и до Python writer.
IdeExecutionTests.test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation | Editor остаётся единственным writer, сохраняются snapshot, receipt и generation.
IdeExecutionTests.test_editor_is_only_writer_and_keeps_snapshot_receipt_and_generation.effect | Имитирует только подтверждённый editor effect тестового workspace.
IdeExecutionTests.test_unknown_editor_effect_is_not_replayed_or_sent_to_python_writer | Неизвестный editor outcome не повторяется и не перенаправляется Python writer.
IdeExecutionTests.test_stale_disk_never_reaches_external_editor_apply | Изменившийся disk snapshot блокирует внешний editor apply.
''')
register('tests/test_ide_remote_control.py', '''
IdeRemoteControlTests | Проверки удалённого управления владельцем IDE-задачи.
IdeRemoteControlTests.owner | Создаёт тестового владельца IDE-сессии.
IdeRemoteControlTests.test_remote_owner_controls_native_run_without_switching_desktop | Управление native run не меняет выбранный desktop чат.
IdeRemoteControlTests.test_remote_owner_controls_native_run_without_switching_desktop.command | Имитирует командный ответ только текущего owner fixture.
IdeRemoteControlTests.test_ambiguous_native_runs_are_not_silently_selected | Несколько подходящих native runs требуют явной идентичности.
''')
TS_NOTES.update({
 'apps/desktop/electron/main.ts:readSharedTheme':'Читает общую тему LESHY из сохранённого профиля.',
 'apps/desktop/electron/main.ts:writeSharedTheme':'Сохраняет выбранную общую тему для desktop и IDE.',
 'apps/desktop/electron/neutralIde.ts:send':'Передаёт разрешённый ответ клиенту собственного IDE транспорта.',
 'apps/desktop/shared/createApi.ts:ApiTransport':'Минимальный транспорт invoke/on/removeListener для общей API-фабрики.',
 'apps/desktop/shared/createApi.ts:createApi':'Создаёт фиксированную поверхность API поверх выбранного транспорта.',
 'apps/desktop/src/App.tsx:App.attachEditorContext':'Добавляет контекст выбранного редактором файла к следующему запросу.',
 'apps/desktop/src/App.tsx:App.take':'Принимает переданный редактором черновик и контекст.',
 'apps/desktop/src/App.tsx:App.launchNativeIde':'Открывает собственную IDE для выбранного workspace с проверкой состояния.',
 'apps/desktop/src/AppearanceSettings.tsx:startAppearanceSync':'Подключает начальную тему и события, не позволяя позднему ответу перезаписать выбор пользователя.',
 'apps/desktop/src/AppearanceSettings.tsx:startAppearanceSync.receive':'Принимает обновление темы и инвалидирует устаревшую начальную загрузку.',
 'apps/desktop/src/design/ForestSpot.tsx:ForestSpotKind':'Допустимые виды живописной иллюстрации LESHY.',
 'apps/desktop/src/design/ForestSpot.tsx:ForestSpot':'Выбирает подготовленный ресурс и доступное представление иллюстрации.',
 'apps/desktop/src/design/Ornaments.tsx:Diamond':'Декоративный ромб через общий CSS mask.',
 'apps/desktop/src/design/Ornaments.tsx:OrnamentDiamond':'Общий компонент орнаментального ромба.',
 'apps/desktop/src/design/Ornaments.tsx:OrnamentDivider':'Декоративный разделитель с ромбом.',
 'apps/desktop/src/design/Ornaments.tsx:OrnamentCorner':'Угол рамки через общий SVG mask.',
 'apps/desktop/src/design/Ornaments.tsx:OrnamentLeaf':'Декоративная векторная ветка, скрытая от accessibility tree.',
 'apps/desktop/src/design/Ornaments.tsx:OrnamentFrame':'Четыре декоративных угла рамки.',
 'apps/desktop/src/design/Ornaments.tsx:WoodlandAccent':'Лесной декоративный акцент с внешним классом размещения.',
 'apps/desktop/src/design/themes.ts:LeshyTheme':'Идентификатор одной из трёх тем LESHY.',
 'apps/desktop/src/design/themes.ts:normalizeTheme':'Преобразует legacy light и неизвестные значения в поддерживаемую тему.',
 'apps/desktop/src/design/themes.ts:applyTheme':'Применяет data attributes и color-scheme темы к документу.',
 'apps/desktop/src/ideEntry.ts:acquireVsCodeApi':'Объявление предоставленного Code-OSS API webview.',
 'apps/desktop/src/ideEntry.ts:invoke':'Отправляет RPC webview с идентичностью запроса.',
 'apps/desktop/src/ideEntry.ts:on':'Подключает слушателя событий IDE транспорта.',
 'apps/desktop/src/ideEntry.ts:removeListener':'Удаляет слушателя событий IDE транспорта.',
 'apps/desktop/src/idePanel/runActivity.tsx:RunActivity':'Показывает фактические этапы, инструменты, проверки и ручное разрешение unknown effects.',
 'apps/desktop/src/idePanel/sessionState.ts:Line':'Строка локальной переписки с ролью, текстом и optional message id.',
 'apps/desktop/src/idePanel/sessionState.ts:Reference':'Ссылка на сохранённый диапазон файла редактора.',
 'apps/desktop/src/idePanel/workspace.tsx:Page':'Допустимая страница независимой IDE-панели.',
 'apps/desktop/src/idePanel/workspace.tsx:api':'Возвращает предоставленный транспортом window.lca.',
 'apps/desktop/src/idePanel/workspace.tsx:checked':'Преобразует failed RPC result в видимую ошибку операции.',
 'apps/desktop/src/idePanel/workspace.tsx:Content':'Отображает текст и блоки кода сообщения в новой панели.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace':'Независимое состояние диалога, истории, настроек и approvals IDE.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.act':'Сериализует UI-операцию и показывает её ошибку и busy state.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.select':'Загружает выбранный чат либо создаёт новый с восстановлением текущего run.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.takeEdit':'Забирает editor draft, добавляет ссылку на контекст и фокусирует ввод.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.trap':'Удерживает Tab-фокус внутри активного approval.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.escape':'Возвращает к диалогу по Escape вне approval.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.send':'Проверяет recovery/busy, назначает run id до startTask и отправляет выбранный Agent/Ask/Plan запрос.',
 'apps/desktop/src/idePanel/workspace.tsx:AgentWorkspace.attach':'Добавляет один диапазон редактора на путь, ограничивая список восьмью ссылками.',
 'tests/electron/leshy-themes.cjs:BrowserWindow.prototype.loadURL':'Загружает production renderer вместо dev server в тестовом окне.',
 'tests/electron/leshy-themes.cjs:dialog.showSaveDialog':'Направляет экспорт в изолированный output теста.',
 'tests/electron/leshy-themes.cjs:releaseVisual':'Разрешает fixture после визуальной контрольной точки.',
 'tests/electron/leshy-themes.cjs:done':'Завершает тестовый сценарий и освобождает его ресурсы.',
 'tests/electron/leshy-themes.cjs:releaseStage4':'Разрешает отложенный HTTP fixture этапа.',
 'tests/electron/leshy-themes.cjs:js':'Вычисляет выражение в тестовом renderer.',
 'tests/electron/leshy-themes.cjs:click':'Нажимает найденный renderer control.',
 'tests/electron/leshy-themes.cjs:textButton':'Находит кнопку по отображаемому тексту.',
 'tests/electron/leshy-themes.cjs:input':'Вводит значение с React-совместимыми событиями.',
 'tests/electron/leshy-themes.cjs:capture':'Сохраняет screenshot текущего состояния renderer.',
 'tests/electron/leshy-themes.cjs:finish':'Сохраняет отчёт и завершает Electron с кодом результата.',
 'tests/electron/neutral-ide-integration.cjs:delay':'Короткая асинхронная пауза ожидания fixture.',
 'tests/electron/neutral-ide-integration.cjs:until':'Ожидает проверяемое условие с конечным timeout.',
 'tests/electron/neutral-ide-integration.cjs:desktop':'Выполняет выражение в desktop renderer.',
 'tests/electron/neutral-ide-integration.cjs:connect':'Создаёт loopback CDP-клиент собственного Code-OSS.',
 'tests/electron/neutral-ide-integration.cjs:connect.socket.onmessage':'Разбирает CDP ответы и события сессий.',
 'tests/electron/neutral-ide-integration.cjs:connect.send':'Отправляет CDP-команду с уникальным id и optional session.',
 'tests/electron/neutral-ide-integration.cjs:connect.close':'Закрывает тестовое CDP соединение.',
 'tests/electron/neutral-ide-integration.cjs:evaluate':'Выполняет выражение в выбранном execution context.',
 'tests/electron/neutral-ide-integration.cjs:findWebview':'Находит execution context независимой панели агента.',
 'tests/electron/neutral-ide-integration.cjs:panel':'Вычисляет выражение в webview панели.',
 'tests/electron/neutral-ide-integration.cjs:semanticBorder':'Сравнивает цвет границы с семантическим CSS token.',
 'tests/electron/neutral-ide-integration.cjs:screenshot':'Сохраняет CDP screenshot Code-OSS.',
 'tests/electron/neutral-ide-integration.cjs:finish':'Сохраняет report/requests и закрывает только своё дерево IDE.',
 'tests/electron/neutral-ide-integration.cjs:resizePanel':'Меняет ширину панели для проверки компактных состояний.',
 'tests/electron/neutral-ide-integration.cjs:checkControls':'Проверяет геометрию и доступность controls панели.',
 'tests/electron/runner-exit.test.cjs:launch':'Выполняет реальный launcher в VM с изолированным process и spawn.',
 'tests/electron/runner-exit.test.cjs:launch.spawn':'Возвращает тестовый дочерний процесс без запуска Electron.',
 'tests/electron/runner-exit.test.cjs:launch.spawn.on':'Запоминает callback lifecycle для моделирования exit/error.',
 'tests/electron/studio-smoke.cjs:captureThemes':'Сохраняет состояния desktop в трёх темах LESHY.',
})
for _method, _purpose in {
 'getAppearanceTheme':'читает общую тему', 'setAppearanceTheme':'изменяет общую тему',
 'ideShell':'открывает shell редактора', 'idePreviewDiff':'показывает diff редактора',
 'ideOpenFile':'открывает файл редактора', 'openLola':'открывает настольную Лолу',
 'lolaMicrophone':'передаёт действие микрофона Лоле', 'ideEditDraft':'получает editor draft',
 'ideEditorContext':'получает выбранный диапазон редактора', 'projectMemoryAction':'выполняет действие памяти проекта',
 'createGitCheckpoint':'создаёт private Git checkpoint', 'cancelGitCheckpoint':'отменяет создание checkpoint',
 'updateTaskPlan':'обновляет план текущей задачи', 'activeRuns':'читает активные запуски',
}.items():
    TS_NOTES['apps/desktop/shared/createApi.ts:createApi.'+_method]='Фиксированный API: '+_purpose+' через выбранный транспорт.'
for _method in ('activeRuns','cancelGitCheckpoint','createGitCheckpoint','lolaMicrophone','openLola','projectMemoryAction','updateTaskPlan'):
    TS_NOTES.pop('apps/desktop/electron/preload.ts:'+_method)
