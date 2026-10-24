"""Ручные объяснения для генерируемого справочника; код здесь не запускает агента."""

FILE_NOTES = {
    'agent/task_activity.py': 'Ограниченный журнал метаданных tools и восстановление незавершённых операций из канонической истории.',
    'tests/test_task_activity.py': 'Контракты журнала: лимиты, статусы, отсутствие содержимого файлов, этапы и anchored recovery.',
    'apps/desktop/src/TaskProgress.tsx': 'Типизированная панель этапов, инструментов, результатов и продолжения задачи.',
    'requirements-build.txt': 'Точные Python-зависимости для Windows x64 freeze Core без Qt.',
    'electron-builder.json': 'Allowlist приложения, extraResources Core и локальный NSIS installer без публикации.',
    'tools/build_windows_core.py': 'PyInstaller onedir сборка Windows x64 Core с Python 3.12 и данными навыков.',
    'tests/electron/packaged-smoke.mjs': 'CDP-проверка настоящего packaged exe с урезанным PATH, discovery и повторным запуском.',
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
    'apps/desktop/build-electron.mjs': 'Две Vite library-сборки в main.cjs и preload.cjs с внешними системными импортами.',
    'apps/desktop/electron/main.ts': 'Окно, Python-процесс, pending RPC, проверка sender и фиксированные IPC handlers.',
    'apps/desktop/electron/preload.ts': 'Узкий window.lca API и отписываемый listener событий.',
    'apps/desktop/src/main.tsx': 'Подключает CSS, создаёт React root и отображает App в StrictMode.',
    'apps/desktop/src/App.tsx': 'React-состояние и представление проекта, настроек, чата, потока, checkpoint и diff.',
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
_complete_units | Копирует завершённые tool-пары и обычные сообщения; исключает незавершённые и осиротевшие tool-сообщения из проекции.
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
StageVerifier.verify | Отклоняет stop_reason; принимает успешную запись или непустой финальный текст по правилам реализации.
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
EditorService.preview | Сверяет editor revision с диском, готовит конкретный diff и сохраняет одноразовый proposal без записи.
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
 'apps/desktop/src/LolaAvatar.tsx':'Персонаж по референсу: выбор позы из атласа по состоянию Лолы, подпись, речевая волна и уменьшение движения.',
 'apps/desktop/src/assets/miya-states.png':'Прозрачный 4×2 атлас поз светловолосой аниме-горничной по пользовательскому референсу.',
 'apps/desktop/src/assets/miya-states.prompt.md':'Сохранённые prompts встроенного image_gen и схема ячеек персонажа.',
 'tools/tts/training/README.md':'Команды возобновляемой генерации, обучения и контроля локального конвейера Serena.',
 'tools/tts/training/generate_serena.py':'Возобновляемый корпус Qwen Serena: закреплённая revision, PCM22k WAV, локальный STT отбор и provenance каждого примера.',
 'tools/tts/training/run_training.py':'Ограниченное Windows дообучение VITS: преобразование Linux checkpoint, warmstart, eSpeak workaround и resume.',
 'tools/tts/training/export_and_evaluate.py':'ONNX экспорт с совместимым tracer и CPU/STT проверкой четырёх новых фраз без объявления совпадения тембра.',
 'tools/tts/training/pipeline.py':'Однопроцессный локальный контроллер этапов с атомарным состоянием, границами шагов и остановкой при ошибках.',
})
TS_NOTES.update({
 'LolaAvatar':'Показывает позу, подпись и движение персонажа по фактическому состоянию, поддерживает отключение анимации.',
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
