# LESHY Project Development Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Получить воспроизводимую поставку LESHY и измеряемую надёжность основного сценария «запрос → контекст → diff → проверка → объяснение».

**Architecture:** Развивать существующее Python-ядро, SQLite/WAL, ToolExecutor/CallJournal и независимую Code-OSS IDE-панель. Сначала восстановить проверки поставки, затем закрыть сценарии восстановления и измерить качество; новые функции выбирать по результатам измерений.

**Tech Stack:** Python, unittest, Electron, React 19, TypeScript, Vite, Code-OSS, SQLite, локальные OpenAI-compatible HTTP fixtures.

**Spec:** [Аудит 3 ноября 2026](../../81-project-audit-2026-11-03.md). Это предлагаемый план; реализация продуктовых изменений не входит в текущую задачу аудита.

**Прогресс 3 ноября:** задача 1 завершена локально; задача 2 реализована и проверена локально, remote CI ожидается; задача 3 — свежий пакет и embedded IDE acceptance прошли, clean-machine gate открыт. Задачи 4–5 реализованы и проверены; Task 6 имеет измеренный базовый срез, расширенные live-сценарии и profiling ещё открыты. [Первая волна](../../84-development-wave-one.md), [recovery и IDE](../../85-recovery-and-session-state.md), [quality baseline](../../83-agent-quality-baseline.md).

## Global Constraints

- Сохранять ToolExecutor, CallJournal, approval/revision, WorkspaceAccessPolicy, RequestBudget и существующую машину состояний.
- Сохранять независимость `src/idePanel`; не импортировать старую App/Studio UI в новую панель.
- Не вводить обязательный ручной token/time/turn cap для local auto; ledger остаётся учётом.
- Не воспроизводить действия с неизвестным эффектом, не принимать narrative модели за доказательство.
- Не менять appId, пути профилей и схемы хранения из-за смены отображаемого бренда без миграции.
- Существующее грязное дерево сохранять; фиксировать только отобранные файлы, не использовать массовый `git add .`.
- Реальные модели запускать последовательно; сначала одна используемая модель, расширять матрицу при наличии новых вопросов.

## Review Focus

1. Аварийное завершение GUI-теста обязано давать nonzero — задача 1.
2. Старый executable в output не должен подменять новый — задача 3.
3. Перезапуск после неизвестного эффекта не должен повторять инструмент — задача 4.
4. События фонового run не должны попадать в другой чат — задачи 2 и 5.
5. Успешный процесс на старых исходниках не должен подтверждать текущий результат — задача 6.

## Порядок и размер

| Волна | Задачи | Результат | Оценка работы одного разработчика |
|---|---|---|---|
| 1 / P1 | 1–2 | Достоверный baseline и CI основного пути | 3–5 рабочих дней |
| 2 / P1 | 3 | Свежая поставка с проверкой установки/обновления | 2–4 дня |
| 3 / P2 | 4–5 | Понятное восстановление и поддерживаемая IDE-панель | 5–8 дней |
| 4 / P2 | 6 | Сравнимые измерения native/JSON и дальнейший backlog | 3–5 дней |

Оценки — ориентир аудита, без обязательства календарной даты; неизвестные дефекты baseline могут их изменить. Волны 3–4 не требуют новой подсистемы inference или embeddings.

## Task 1: Вернуть достоверность проверок и актуальный статус

**Files:** Modify `tests/electron/run.cjs`, `tools/doc_notes.py`, `README.md`, `docs/README.md`, `docs/11-current-status.md`, `docs/57-roadmap-v2.md`; regenerate `docs/reference/*.md`; create `tests/electron/runner-exit.test.cjs`.

**Interfaces:** CLI launcher сохраняет аргумент имени сценария; код завершения 0 означает только нормальный `exit(0)` дочернего процесса.

- [x] Зафиксировать исходное состояние и результаты аудита с ревизией; согласовать состав отдельных коммитов по подсистемам, не включая чужие изменения автоматически.
- [x] Добавить независимый тест launcher: `exit(0)` → 0, `exit(7)` → 7, signal → nonzero, spawn error → nonzero. Использовать подмену spawn, чтобы не зависеть от GUI.
- [x] Исправить обработчик завершения с явным учётом `(code, signal)`.
- [x] Дополнить назначения новых файлов и пересоздать справочники командой `npm run docs:generate`; исправить последующие ошибки полного `npm run docs:check`.
- [x] Обновить текущее описание функций, бренда и readiness. Старые главы оставить доступными, явно пометив заменённые контракты.
- [x] Проверить `node --test tests/electron/runner-exit.test.cjs`, `npm run docs:check`, `npm run build`; успех — exit 0 всех команд и отсутствие ложного успеха signal-сценария.

## Task 2: Добавить CI для текущей IDE и фоновых запусков

**Files:** Modify `.github/workflows/validate.yml`, `package.json`, при необходимости `prototypes/neutral-ide/prepare.py`; existing tests `tests/electron/neutral-ide-integration.cjs`, `background-runs-smoke.cjs`, `leshy-themes.cjs`.

**Interfaces:** Runtime готовится существующим `prepare.py`; новый gate запускается через исправленный launcher из задачи 1. Использовать изолированные временные профили и HTTP fixture.

- [x] Добавить подготовку закреплённого runtime и отдельный native IDE job после build; сохранять logs/result/screenshots при ошибке.
- [x] Включить `node tests/electron/run.cjs neutral-ide-integration.cjs`: поток, diff approval, запись, Ctrl+Z, Ask/Plan, история и настройки должны пройти.
- [x] Включить `npm run test:ui:background`: переключение чатов, раздельная отмена и идентичность событий должны пройти.
- [x] Добавить короткий theme smoke; полную матрицу тем и масштабов вынести в отдельный управляемый job, сохранив текущие fixtures.
- [ ] Проверить timeout и nonzero для искусственно завершённого fixture-процесса: job обязан падать.
- [ ] Принять задачу только после успешного Windows job на выбранном commit; локальный запуск не является доказательством remote CI.

## Task 3: Проверить свежую поставку LESHY

**Files:** Modify `tests/electron/packaged-smoke.mjs`, `electron-builder.json`, `.github/workflows/validate.yml`; existing `tools/build_windows_core.py`, `tools/prepare_windows_dependencies.py`; create `docs/82-leshy-release-acceptance.md`.

**Interfaces:** Путь package smoke к executable явно передаётся из сборки либо вычисляется из её конфигурации. Старый `Neutral.exe` не выбирается как fallback.

- [x] Добавить проверку выбора executable: чистый LESHY output; только старый Neutral output; оба файла. Приёмка использует только текущий артефакт, отсутствие текущего даёт ошибку.
- [x] Подготовить новый отдельный output-каталог и frozen Core, собрать `npm run package:win`; сохранить commit, версии, SHA256 и список ресурсов.
- [x] Запустить package smoke по точному новому пути со stripped PATH и временным профилем; проверить Core, SQLite, предпочтения, перезапуск и отсутствие ключей в логах.
- [x] Дополнить package gate реальным запуском вложенной IDE: открыть workspace, отправить fixture-задачу, подтвердить diff, записать и отменить через editor.
- [ ] Проверить установку, обновление с копией старого профиля, сохранение данных и удаление на чистой Windows/VM. Исходный пользовательский профиль не использовать.
- [x] Записать результаты в release acceptance. Сборка пакета и успешный smoke без установки не закрывают пункт чистой машины. Публикация релиза — отдельное действие.

## Task 4: Сделать восстановление длинных задач понятным

**Files:** Modify `apps/desktop/src/idePanel/runActivity.tsx`, `workspace.tsx`, `core/python/workspace_review.py`, при необходимости `agent/tool_recovery.py`; extend `tests/test_tool_execution.py`, `tests/migration/test_run_owner_restart.py`, `tests/electron/neutral-ide-integration.cjs`.

**Interfaces:** Сохранить `resolveToolRecovery` и точные `chat_id/journal_id/message_index/call_id`. Диагностический экспорт не меняет canonical journal.

- [x] Добавить сценарии: Stop во время approval; exit после начала эффекта до receipt; restart; повреждённый journal; неизвестный rollback. Проверять, что повторный эффект не запускается.
- [x] Для каждого blocked-состояния показать причину, доступный следующий шаг и экспорт диагностики без API-ключей и лишнего содержимого проекта.
- [x] Для corrupted journal сохранить блокировку, обеспечить доступ к диагностике и копии состояния. Автоматическое исправление журнала проектировать отдельно, если для него нет доказуемого контракта.
- [x] Добавить в IDE переходы к настройкам правил/MCP/плана или явное объяснение места настройки; не создавать второй источник настроек.
- [x] Выполнить focused Python suites и native IDE сценарий. Критерий: неизвестный эффект не повторён, пользователь может получить диагностику, receipt не потерян.

## Task 5: Упростить состояние новой IDE без изменения транспорта

**Files:** Modify `apps/desktop/src/idePanel/workspace.tsx`; create `apps/desktop/src/idePanel/sessionState.ts`, `connectionSettings.tsx`; reuse `apps/desktop/shared/protocol.ts` after checking its actual types; extend native IDE fixture.

**Interfaces:** Сохранить существующие методы `window.lca`, маршрутизацию chat/run/event_seq и независимую UI-границу. Новые внутренние типы выводить из текущего протокола, не придумывать дублирующую схему.

- [x] Зафиксировать тестами раннее событие до startTask response, дубликат event_seq, событие чужого run, task_end и несохранённые настройки модели.
- [x] Заменить `any` для task/approval/config/history реальными типами; вынести преобразование событий в `sessionState.ts` и форму подключения в собственный компонент.
- [x] Сохранить раздельное редактируемое и сохранённое подключение, focus trap approval и содержимое unsaved draft.
- [x] Выполнить `npm run build` и native IDE fixture; визуально проверить 240/320/420 px, три темы, клавиатуру и 200% масштаб. Успех TypeScript не закрывает визуальную приёмку.

## Task 6: Измерить качество и выбрать следующую функцию

**Files:** Extend `tools/benchmark_agent.py`, `tests/test_agent_benchmark.py`, `tests/test_scoped_verification.py`; create `docs/83-agent-quality-baseline.md`; reuse current immutable fixtures and oracle.

**Interfaces:** Отчёт привязан к commit, model ID/quantization, loaded context, native/JSON, версии fixture, oracle и точным командам. Пропущенные измерения остаются UNVERIFIED.

- [ ] Выбрать неизменяемые fixtures: исправление бага; multi-file rename; длинное чтение; отказ действия; разрыв соединения; external edit; restart между effect и receipt.
- [x] Сначала прогнать deterministic orchestration. Отдельно проверить stale witness: exit 0 до external edit не даёт текущего passing evidence.
- [x] Выполнить согласованные пользователем по три повтора: Ornith/native и Qwen 2.5 Coder/JSON, bugfix и multifile. Сохранены diff/oracle, статусы, repairs, HTTP requests, usage и полное время. Это сравнение разных моделей; время до первого полезного результата остаётся открытым.
- [ ] Измерить RAM/VRAM отдельно от конкурентных тяжёлых запусков. Небольшую выборку не выдавать за универсальный процент качества.
- [x] По измерениям выбрать следующий ограниченный этап: configured acceptance checks в новой IDE, затем JSON recovery после повторных пустых поисков. Embeddings, новые write-capable субагенты и отдельный inference engine требуют самостоятельного обоснования.
- [x] Опубликовать локальный baseline-документ с доступными evidence; обновить один актуальный backlog с критериями входа и выхода.

## Откат и завершение волн

Каждая задача поставляется отдельным reviewable изменением. UI/CI изменения откатываются отдельно от хранения; при миграциях требуется копия профиля и проверка восстановления. Закрытие волны требует свежего результата её проверок на одной ревизии. Декоративная доработка, новая модель или зелёный unit suite не заменяют package acceptance и оценку конечного diff.

**Acceptance checks:** следующий ограниченный этап выполнен; [реализация и приёмка](../../86-ide-acceptance-checks.md), [закрытый implementation plan](2026-11-03-ide-acceptance-checks.md). Следующий приоритет — JSON recovery после повторных пустых поисков, с внешней проверкой diff. Clean-machine и remote CI остаются открытыми.
