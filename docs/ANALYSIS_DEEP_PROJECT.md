# Глубокий анализ проекта LocalAgent (Neutral 7 / v7.0.1)

Дата анализа: по состоянию на ревизию репозитория, версия `7.0.1`.
Документ составлен на основе прямого чтения файлов и структуры проекта.

---

## 1. Что это за проект

**LocalAgent** — локальное ИИ-приложение для разработки (desktop agent), которое
объединяет в себе несколько ролей:

- **Кодовый агент** — выполняет задачи по работе с исходным кодом через инструменты
  (`list_files`, `read_file`, `search_text`, `write_file` и др.), используя доступные навыки.
- **Рабочее пространство (workspaces)** — ведение проектов, «разговоров» (conversations) и
  проектной памяти (memory).
- **IDE-подобный интерфейс** — инкрементальный индекс Python/JS/TS, поиск по коду (`Ctrl+P`),
  дерево файлов, предпросмотр контекста.
- **Голосовой компаньон «Лола»** — отдельная модель, характер, Windows TTS, нейроозвучка,
  распознавание речи (микрофон) и фраза активации («вокала»).

Проект позиционируется как **«Neutral»** — локальный, настраиваемый, с акцентом на приватность.

---

## 2. Технологический стек

Это **гибридное приложение** из двух связанных сред:

| Слой | Технология | Файлы / роли |
|------|-----------|--------------|
| GUI (пресет) | PySide6 (`>=6.8.0`) — Qt Widgets | `main.py`, `agent/ui.py` |
| UI-логика | React 19 + TypeScript, Vite 6 | `apps/desktop/src/*.tsx` |
| Electron оболочка | Electron 45 | `apps/desktop/electron/main.ts`, `preload.ts`, `lolaPreload.ts` |
| Ядро агента | Python (стандартная библиотека + PySide6) | `agent/**/*.py`, `core/python/**` |
| Сборщик | electron-builder 26.15.3, TypeScript ~5.7.2 | `electron-builder.json` |
| Модельный клиент | asyncio HTTP/SSE | `agent/model_client.py`, `model_gateway.py` |

Ключевая особенность архитектуры — **мост (bridge)**: Electron-процесс запускает отдельный
Python-процесс, который общается через stdin/stdout в формате JSON-lines. React-рендерер
общается с Electron через узкий preload-API (`window.lca`).

---

## 3. Архитектура и поток одного запроса

Общая схема (из `docs/03-architecture.md`):

```
React renderer (App.tsx) --window.lca--> preload.ts
      --> IPC invoke --> Electron main.ts (apps/desktop/electron/main.ts)
      --> stdin: JSON-lines --> bridge.py (core/python/bridge.py)
      --> TaskService / AgentEngine (agent/engine.py, 898 строк)
      --> ModelClient (asyncio loop) --> HTTP/SSE --> сервер модели
```

**Потоковая модель:**

- `bridge.main` работает в основном потоке: читает stdin, вызывает `handle`, печатает ответ.
- `TaskService.start` запускает отдельный daemon-поток `agent-task`, чтобы цикл модели не
  блокировал команду `cancel_task`.
- `ModelClient` создаёт ещё один daemon-поток `model-http` с отдельным asyncio loop; очередь
  на 64 чанка связывает асинхронную корутину с синхронным потребителем (обратное давление,
  чтобы producer не накапливал чанки при медленном клиенте).
- `bridge.emit` использует `output_lock`, чтобы два Python-потока не писали половинки разных
  JSON-строк в stdout одновременно.
- `list_models` — отдельное исключение из синхронного dispatch: запускается `model-discovery`
  параллельно с чтением stdin; разрешён только один такой worker.

**Миграция Qt → изолированный движок:**
Исходный `AgentWorker` объединял цикл задачи с наследованием от `QThread`. Electron не
использует Qt event loop, поэтому выделен отдельный `AgentEngine` (без Qt-импортов), который
можно запускать через два адаптера и проверять Core без GUI. Миграция постепенная: часть
вспомогательных классов ещё не встроена в активный сценарий, а React-представление пока
находится в одном большом компоненте (`App.tsx`).

**Перезапуск:** следующая команда может снова запустить Python, но состояние выбранного
проекта в новом процессе теряется. UI очищает выбранный проект и предлагает выбрать заново;
чаты и задачи на диске позволяют восстановить работу (это перезапуск процесса, а не
бесшовное восстановление всех переменных).

---

## 4. Структура кода

### 4.1 Python-ядро (`agent/`, ~90 файлов)

Модули группируются по ответственности:

- **Движок и цикл:** `engine.py` (898 строк), `worker.py`, `runtime.py` (`AgentRuntime`).
- **Модель:** `model_client.py`, `model_gateway.py`, `model_manager.py`, `model_discovery.py`,
  `model_preferences.py`, `model_probe.py`.
- **Контекст и инструменты:** `context_manager.py`, `context_builder.py`, `smart_context.py`,
  `context_tools.py`, `tools.py`, `tool_executor.py`, `tool_recovery.py`, `json_tools.py`.
- **Задачи и планирование:** `task_store.py`, `task_graph.py`, `planner.py`, `task_contract.py`,
  `run_state.py`, `run_policy.py`, `run_registry.py`, `inference_scheduler.py`.
- **Хранение данных:** `chat_store.py`, `conversation.py`, `project_memory.py`, `projects.py`,
  `storage.py`, `artifact_store.py`, `call_journal.py`, `request_budget.py`, `auto_budget.py`.
- **Безопасность и разрешения:** `security.py`, `workspace_access.py`, `workspace_edits.py`,
  `workspace_read.py`, `workspace_revision.py`, `workspace_search.py`, `workspace_snapshots.py`,
  `workspace_review.py`, `readonly_research.py`, `process_identity.py`.
- **Субагенты и делегирование:** `child_executor.py`, `delegation.py`, `subagent_profiles.py`,
  `verifyer.py`, `verification_evidence.py`, `scoped_verification.py` (тесты).
- **MCP:** `mcp.py`, `mcp_client.py`, `mcp_sessions.py`.
- **Компаньон «Лола»:** `companion_policy.py`, `companion_preferences.py`, `skills.py`.
- **GUI-адаптеры Qt:** `ui.py` (`MainWindow`).

### 4.2 Python Core Services (`core/python/`, ~20 файлов)

Высокоуровневые сервисы, работающие над ядром: `task_service.py`, `runtime_service.py`,
`session_service.py`, `run_session.py`, `background_job.py`, `editor_service.py`,
`memory_service.py`, `project_search.py`, `extension_service.py`, `neural_speech.py`,
`speech_service.py`, `transcription_service.py`, `telegram_service.py`, `optional_ide_service.py`,
`desktop_service.py`, `conversation_service.py`, `assistant_service.py`, `protocol.py`.

### 4.3 Electron + React (`apps/desktop/`)

- **Renderer (React):** ~45 компонентов в `src/*.tsx` — `App.tsx` (главный), панели чата,
  редактора, памяти, модели, подагентов, графа задач, фоновых чатов, Лола и т.д.
- **Electron main:** `main.ts`, `preload.ts` (узкий API), `lolaPreload.ts`, `speechRuntime.ts`,
  `desktopApps.ts`, `desktopLola.ts`, `assistantMedia.ts`.
- **Shared код:** `apps/desktop/shared/`, микрофон (`microphone.ts`), текст речи (`voiceText.ts`).
- Сборка: `vite build` + `build-electron.mjs`; typecheck для renderer и electron.

### 4.4 Инструменты и тесты

- `tools/` — аудит ядра, бенчмарки (агент, индекс проекта, storage), генерация документации
  (`generate_code_reference.py`, `extract_ts_symbols.cjs`), сборка Windows Core, проверка docs.
- `tests/` — ~60 Python-тестов + `tests/electron/*.cjs` smoke-тесты UI (studio, layout, visual,
  lola, background-runs, optional-ide).

---

## 5. Функционал

**Агент и задачи:** запуск задач с планированием (`TaskGraph`, зависимости), долгие задачи с
квитанциями выполнения, редактирование плана, восстановление без повторных действий; бюджеты
запросов (`RequestBudget`) и добровольный бюджет внешнего API (`auto_budget.py`).

**Рабочие расширения (skills):** редактор, поиск/`Ctrl+P`, запуск GGUF (локальный runtime),
память и чат, голосовой компаньон.

**Модели:** выбор между bundled GGUF-моделью CPU (включён в установочной версии) или
подключение LM Studio / другого llama-server; поддержка Qwen3-TTS (требует отдельную установку).

**Голос «Лола»:** фраза активации, Windows TTS, микрофонное распознавание, нейроозвучка.

**IDE-функции:** инкрементальный индекс определений/текста, предпросмотр источников перед
выдачей фактов, подтверждение внешней отправки (`context-pack`).

**Безопасность (из `MIGRATION_PLAN.md`):**
- `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`.
- Никакого произвольного IPC-forwarding или общего shell-доступа.
- Пути к файлам разрешаются внутри выбранного проекта, включая цели симлинков.
- Каждое изменение агента требует совпадающего явного подтверждения активного предложения
  (Apply / Reject / Cancel).
- Отказ от изменений проекта/чата/конфигурации, пока задача активна.

---

## 6. Тестирование и CI

**Python-тесты:** `unittest`, ~60 файлов в `tests/`. Ключевые направления: approval-flow,
editor-io/file-editing, storage, runtime-architecture/service, sandbox, mcp-reliability,
project-index/search/memory, task-graph/store/activity, run-* (policy/state/registry),
companion-policy, smart-context, speech-service и др.

**Electron/UI smoke:** `tests/electron/run.cjs` с конкретными сценариями (`studio-smoke`,
`studio-layout`, `studio-visual`, `lola-desktop-smoke`, `background-runs-smoke`,
`optional-ide-smoke`).

**CI (`.github/workflows/validate.yml`, `release-windows.yml`):**
- Проверка Python, сборка Electron, генерация и проверка документации (`check_docs.py`).
- Windows-сборка через electron-builder (`--win --x64`), SHA256SUMS, публикация релиза.
- Публикация релизов выполняется **только вручную**; PR содержит актуальные исходники.

---

## 7. Документация

Огромный и хорошо структурированный корпус в `docs/` (89 файлов). Темы:
архитектура, путь запроса, протоколы RPC/IPC, данные и разрешения, тесты/дебаг, текущий статус,
окно разработки (`WORK_PLAN.md`), руководство по разработке, расширения (редактор, поиск, runtime,
память, голос), нейросpeech и wake-word, установщик Windows, UI-студия, Neutral 7 (разговоры, ядро,
проекты, проверки сборки), субагенты, профили контекста, умный контекст/музыка/таймеры.

Есть справочники `docs/reference/python.md`, `typescript.md`, карта файлов и история README.
Процесс: `npm run docs:generate` (генерация code reference) + `npm run docs:check`.

---

## 8. Выявленные проблемы, риски и слабые места

1. **Огромный монолитный компонент `App.tsx`.** React-представление сосредоточено в одном
   большом файле; архитектура прямо отмечает это как незавершённую часть миграции. Это усложняет
   поддержку, рефакторинг и тестирование UI.

2. **`engine.py` — 898 строк.** Критический алгоритм (цикл модели + инструменты) в одном файле;
   риск трудночитаемости и регрессий.

3. **Потеря состояния при перезапуске Python-процесса.** Выбранный проект не восстанавливается
   автоматически; это ограничение UX, которое архитектурно известно, но остаётся.

4. **Сложность потоковой модели.** Три связанных потока (`bridge.main`, `agent-task`, `model-http`)
   с отдельными asyncio loop и lock'ами — источник тонких race-условий (задокументировано через
   `output_lock` и draft-таймеры).

5. **Зависимость GUI от PySide6.** Ядро агента (`agent/`) всё ещё имеет связь с Qt через
   `worker.py`; изоляция `AgentEngine` частичная, что ограничивает переносимость (например, на Linux/macOS).

6. **Внешние зависимости сборки.** Установочная версия требует bundled Windows Core + Visual C++
   Redist; для TTS/Qwen3 — отдельной speech-среды/моделей. Повышает порог установки.

7. **Огромный корпус документации vs. код.** 89 файлов docs при ~160 Python-файлах и большом UI —
   риск рассинхрона между документацией и фактическим поведением; есть автоматическая проверка, но
   она покрывает не всё.

8. **Ограничения функционала (из миграционного плана):** незавершённые части редактора и change-review,
   отсутствие хранилища креденшалей для API-ключей, частичная интеграция подагентов/расширений.

9. **Безопасность по умолчанию хорошая**, но концентрация разрешений в одном agent-слое и
   множество «сервисов» в `core/python` могут создавать новые векторы при добавлении функций без
   повторного аудита.

---

## 9. Рекомендации по улучшениям (без изменения кода — предложения)

**Архитектура/UI:**
- Дробить `App.tsx` на переиспользуемые хуки и компоненты; вынести state-логику в `use*`-хуки
  (уже есть `useTaskSession`, `useLolaSession` — расширить паттерн).
- Продолжить вынос UI-отрисовки потока из Qt (`text_delta`) в Electron, чтобы завершить
  миграцию рендеринга.

**Ядро:**
- Разбить `engine.py` на модули по ответственности (планирование, инструменты, бюджет, вывод),
  сохранив единый public API.
- Усилить изоляцию `AgentEngine` от Qt для полноценного запуска вне Windows/GUI.

**Надёжность:**
- Реализовать восстановление выбранного проекта при перезапуске Python-процесса из проектной памяти.
- Добавить хранилище креденшалей (опциональные API-ключи) с шифрованием в покое.

**Тестирование:**
- Расширить coverage на UI (`App.tsx`) и потоковую модель bridge; добавить regression-тесты для
  race-условий draft-таймеров.
- Автоматизировать аудит безопасности при добавлении новых инструментов/сервисов.

**Документация:**
- Удерживать docs в синхроне с кодом через `docs:check`, добавить тест на соответствие ключевых
  утверждений документации реальному поведению.

---

## 10. Итог

Это зрелое, хорошо документированное и безопасно спроектированное гибридное приложение
(Python-ядро + Electron/React), реализующее локального кодового агента с IDE-функциями и голосовым
компаньоном. Основные технические долги сосредоточены в UI (`App.tsx`), критическом `engine.py`
и сложной трёхпоточной модели bridge. Архитектурные границы (bridge, узкий preload-API, sandbox,
политика разрешений) проработаны и задокументированы; остаются незавершённые фичи редактора,
change-review и хранилища креденшалей, обозначенные в `MIGRATION_PLAN.md`.
