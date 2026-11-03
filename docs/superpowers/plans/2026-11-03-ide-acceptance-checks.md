# IDE Acceptance Checks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Подключить существующие пользовательские acceptance checks Core к новой IDE-панели.

**Architecture:** Отдельные editor и pure codec внутри idePanel, общие IdeOptions/ValidationCommand и существующий startTask. Draft хранится как UI-состояние; canonical options и evidence принадлежат Core. Выполнение остаётся в ToolExecutor/approval/journal.

**Tech Stack:** React, TypeScript, Node test, Python unittest, Electron/Code-OSS fixtures.

**Spec:** [Контракт этапа](../../86-ide-acceptance-checks.md).

## Global Constraints

- Не импортировать прежние App/Studio/IdeTaskOptions UI.
- Не менять RequestBudget, JSON parser, scheduler или policy полномочий.
- Не исполнять команды в Ask/Plan; checks_only только явным действием Agent.
- Resume использует checkpoint; неизвестные эффекты не повторяются.
- Не выдавать exit 0 за доказательство всего проекта или всех критериев.
- Работать в текущем аудируемом dirty feature checkout, без массового staging/commit.

## Review Focus

Ранние события до startTask response; сохранность несохранённого запроса при checks_only; scope/dependencies и check_id; draft другого чата; ложный passing при отказе/старой ревизии/ручном критерии.

## Task 1: Codec и editor

Files: create `src/idePanel/acceptanceChecks.ts`, `acceptanceSettings.tsx` и `tests/electron/ide-acceptance.test.cjs`; modify `workspace.tsx`, `workspace.css`, `ideEntry.ts`, `vite-env.d.ts`.

- [x] Написать и увидеть RED unit-тестов сериализации, Ask/Plan и draft isolation.
- [x] Реализовать editor критериев, check definitions и scopes; стабильные IDs, max 8 checks / 12 criteria, без shell parsing.
- [x] Подключить отдельную страницу, per-chat draft, восстановление checkpoint и текущего webview draft.
- [x] Подключить normal start/checks_only/resume, не очищая prompt при ручной проверке.
- [x] Выполнить Node tests и build, сохранить ошибки/recovery semantics.

## Task 2: Evidence и вертикальная приёмка

Files: modify `runActivity.tsx`, `neutral-ide-integration.cjs`; create `tests/electron/ide-acceptance.cjs`; extend existing migration/verification tests only where coverage is missing.

- [x] Показать статусы criterion evidence и непроверенные критерии, scoped/current/failed/unconfirmed command outcome.
- [x] Настроить проверки через настоящий UI; получить missing-import exit 1, передать receipt модели, исправить import и получить exit 0 с тем же check_id.
- [x] Проверить checks_only без модели/HTTP, несохранённый запрос, возврат draft, invalid input, Ask/Plan и stale evidence.
- [x] Выполнить Node, unit/migration, native GUI, widths/themes, docs; провести независимый review и закрыть его важные замечания с regressions.

## Task 3: Поставка и отчёт

- [x] Обновить документацию и статусы плана с точными evidence.
- [x] При изменении runtime собрать отдельный актуальный кандидат и выполнить packaged smoke; clean-machine/remote CI оставить открытыми при отсутствии проверки.
