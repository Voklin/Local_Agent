"""Ручные объяснения для генерируемого справочника; код здесь не запускает агента."""

FILE_NOTES = {
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
validate_preferences | Разрешает HTTP(S) endpoint без credentials/query/fragment, проверяет порт и возвращает только URL/ID модели.
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
set_stage | Обновляет активный этап и помечает более ранние этапы завершёнными.
finish_task | Завершает этапы, задаёт итоговый статус/причину и сохраняет checkpoint.
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
LocalRuntime.start | Запускает llama-server с model/context/GPU flags и ждёт health до 45 секунд.
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
TaskService.idle | Отказывает операции, когда поток текущей задачи ещё жив.
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
TaskService._run | Обёртка исполнения с failed и обязательным task_end/flush в finally.
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
    'diagnostic': 'Добавляет только lifecycle-диагностику в ограниченный main.log; ошибка I/O не блокирует приложение.',
    'tests/electron/packaged-smoke.mjs:freePort': 'Резервирует свободный loopback-порт для тестового Chromium CDP.',
    'tests/electron/packaged-smoke.mjs:connectPage': 'Ожидает file renderer настоящего exe и открывает WebSocket CDP с ограниченным временем.',
    'tests/electron/packaged-smoke.mjs:evaluate': 'Последовательно исполняет одно тестовое выражение через CDP с тайм-аутом.',
    'tests/electron/packaged-smoke.mjs:evaluate.receive': 'Сопоставляет CDP response с запросом и возвращает значение либо ошибку JavaScript.',
    'tests/electron/packaged-smoke.mjs:run': 'Запускает packaged exe с изолированными данными/урезанным PATH и проверяет Core, настройки и нормальное закрытие.',
    'tests/electron/packaged-smoke.mjs:main': 'Поднимает HTTP-фикстуру, дважды проверяет пакет и отсутствие ключа в настройках/диагностике.',
})
