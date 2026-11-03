# Аудит после этапов 7–8 и следующий план Neutral

Исторический аудит. Текущая последовательность после review —
[Roadmap V2](57-roadmap-v2.md); прежняя нумерация IDE 13–14 ниже историческая.

Дата: 26 октября 2026. Проверена текущая рабочая копия, включая незакоммиченные
изменения предыдущих этапов. Это новый аудит, а не повторное объявление старого
плана выполненным. Таблица ниже сохраняет исходные наблюдения аудита.
Реализация исправлений A1–A5 описана в [этапе 9](54-core-reliability-stage9.md).
По отдельному уточнению пользователя настольная Лола реализуется сейчас; её итог
и проверки описываются в [главе 53](53-desktop-lola.md).

## Результат проверки

Свежий проход: 321 unit-тест OK (один Windows symlink privilege skip), 80 HTTP/Core
тестов OK. Логи находятся в `.test-data/post-stage8-audit-{unit,http}.log`.
Дополнительные воспроизведения находятся в [audit_post_stage8.py](../tools/audit_post_stage8.py).
Они используют искусственные ответы, временный проект и настоящий локальный LSP
fixture; не вызывают модель, не читают настоящие секреты и не изменяют рабочий проект.
Это наблюдения текущих проблем, а не регрессии, ожидающие успешного прохождения.

| ID / приоритет | Наблюдение и осн | Что изменить |
| --- | --- | --- |
| A1 / P1 | `parse_tool_json` принимает JSON с последующим пояснением «это пример» и первый объект перед вторым JSON. Подтверждено probe; [raw_decode](../agent/json_tools.py#L60) не проверяет остаток строки. Допуск инструмента и approval продолжают действовать, но намерение ответа распознаётся неоднозначно. | Полное потребление input, versioned action envelope, запрет извлечения actions из примеров; тесты trailing/multiple objects/duplicate keys. |
| A2 / P1 | При EOF без finish_reason настоящий Engine завершает ответ как `completed`, сохраняя `finish_reason=unknown`. JSON adapter дополнительно превращает такой EOF в `tool_calls`/`stop`. Подтверждено probe. | Общий `ModelResponseOutcome`: complete/incomplete/refused/cancelled/error. Unknown не повышать до completed и не исполнять effectful calls; совместимость с особенностями сервера задавать явно. |
| A3 / P1 | После настоящего сохранения через EditorService прежний synthetic command receipt остаётся `commands_passed`. Проверка основана на `workspace_generation`, которую [ToolExecutor](../agent/tool_executor.py#L85) меняет только для своих file tools; [EditorService](../core/python/editor_service.py#L66) не уведомляет task evidence. | Общий WorkspaceRevisionService для editor, agent tools, команд и внешних изменений; evidence связывать с revision и нужными content hashes, а не только счётчиком вызовов. |
| A4 / P2 | LSP-клиент возвращает первый `publishDiagnostics`, даже пустой, и закрывает сервер до позднего результата анализа. Реальный subprocess fixture сначала публикует пусто и планирует ошибку позже; probe возвращает 0 диагностик. [Источник](../agent/language_diagnostics.py#L93). | Предпочитать pull diagnostics при capability; для push собирать обновления до quiet interval/ограниченного deadline, учитывать version и superseding списки. Не утверждать завершение всей проверки по первому пустому списку. |
| A5 / P2 | Искусственный `.env` доступен обычному read_file, а researcher имеет собственные исключения. Root containment работает; это отсутствие общей политики чувствительных путей, а не выход за root. | WorkspaceAccessPolicy для model tools/context/research/MCP file adapters: чувствительные шаблоны, `.neutralignore`, явное разрешение конкретного исключения. Ручной пользовательский редактор отделить от автоматической отправки модели. |

У A3 receipt намеренно синтетический; проверяется именно invalidation после
настоящего editor save, а не качество внешнего теста. У A4 отложенная диагностика
может не успеть отправиться, поскольку клиент уже завершает процесс — это и есть
воспроизведение преждевременного завершения.

## Архитектурные ограничения

1. **Одна активная mutable-сессия.** SessionService выделен, но TaskService всё ещё
   владеет единственными engine/thread/run_id/approval и выбранным chat. Для одного
   запуска это рабочее ограничение, для дерева субагентов нужен registry независимых
   RunContext. Нельзя просто запустить ещё один поток того же TaskService.
2. **Inference lease на всю задачу.** Текущий gate защищает VRAM. Если родитель
   удержит его и будет ждать ребёнка, очередь с ожиданием может взаимно заблокироваться;
   сейчас конкурентный вызов просто отклоняется. Планировщик должен выдавать lease
   на HTTP generation и отпускать его на ожидании/IO, сохраняя лимит inference=1.
3. **Нет общего бюджета дерева.** Turn/runtime/payload limits уже есть, но нужны
   root ledger, reservation дочерних бюджетов и учёт дополнительных запросов,
   повторов HTTP, проверки завершения и памяти. `request_count` сейчас считает
   логические create, а transport retry может выполнить несколько HTTP attempts.
4. **Часть долгого RPC синхронна.** `storage_backup` выполняется в основном dispatch
   под tasks.lock. Большая копия потенциально задержит health/voice/cancel; на большой
   реальной базе это отдельно не измерялось. Перевести в bounded background jobs.
5. **Границы слоёв частично смешаны.** Engine — 784 строки, TaskService — 542,
   bridge — 311 на момент аудита. Важнее ответственности: orchestration, persistence,
   transport, presentation и recovery местами остаются в одном владельце. Размер
   файла сам по себе не является ошибкой. Переносить по сценарию с адаптерами.
6. **IPC типизирован частично.** Критические команды уже описаны, но settings и часть
   events используют any, runtime guard проверяет лишь часть полей. Перед extension
   host и дополнительными окнами нужны role-scoped IPC и полные схемы сообщений.
7. **IDE пока редактор проекта.** Textarea с подсветкой, вкладками и разовыми LSP
   проверками не содержит Extension Host, PTY/DAP и workbench API. Установка ZIP/VSIX
   в текущий каталог не сделает VS Code API рабочим.
8. **Обслуживание хранилища.** SQLite/journal/snapshots сохранять. Добавить measured
   orphan GC, квоты, versioned backup manifest для optional settings/worktree refs;
   не удалять snapshots/voice weights или каталоги пользователя при уборке.

Контур Лолы до текущей доработки принадлежал renderer основного окна: WakeListener,
NeuralAudio и VoicePanel. Реализация 53 сохраняет один renderer-владелец скрытым
вместо второго голосового сеанса. Полное отделение VoiceSessionController в отдельный
audio host остаётся следующим архитектурным шагом; падение основного renderer пока
останавливает голос. Обычное скрытие в трэй от падения renderer отличается.

## Что сохранить

Существующие CallJournal/ToolExecutor, approval с revision, guards неизвестных
effects, RequestBudget после адаптации, SQLite/WAL, snapshots с conflict-aware
rollback, ограниченные MCP actors и разделение Chat/IDE/Лолы — полезный фундамент.
Новый план не возвращает обязательные четыре роли и не меняет дизайн Neutral.
Результат тестов не доказывает отсутствие всех дефектов, что показывают новые probes.

## Порядок реализации

| Следующий этап | Результат | Критерий завершения |
| --- | --- | --- |
| 9. Надёжность | A1–A5, outcome contract, общая revision/access policy, async jobs | Новые probes превращены в regression tests: ambiguous JSON не выполняется, EOF paused, editor/terminal changes stale, LSP поздняя ошибка видна. |
| 10. JSON-агент | [Протокол и экономия](51-text-tool-agency-plan.md) | Невалидный ответ чинится в пределах бюджета, нет повторных effects; измерены parsing/repair/latency на выбранных локальных моделях. |
| 11. Run registry и scheduler | Независимые контексты, дерево runs, ledger и общий inference slot | Родитель ждёт ребёнка без deadlock; отмена/рестарт/recovery корректны для всего дерева. |
| 12. Пользовательские субагенты | [Registry, UI, модельные черновики](50-subagents-plan.md) | Пользователь создаёт профиль; модель создаёт разрешённый временный профиль/черновик; ребёнок не повышает права; дерево видно в UI. |
| Лола сейчас | [Настольный спутник и чиби-анимации](53-desktop-lola.md) | Отдельный ограниченный renderer, трэй, скрытие основного окна, один голос/микрофон, остановка и реальная проверка окон. |
| 13. IDE prototype | [Выбор workbench](52-full-ide-and-vscode-extensions-plan.md) | Реальные extensions активируются, работают команды/diagnostics/format/debug, сохраняются стиль и одни working copies. |
| 14. Полная IDE | Перенос IDE за feature flag, extensions UI, terminal/debug/SCM/testing | Приёмочная матрица расширений, migration/recovery, packaged smoke; прежняя история сохранена. |

Этапы 9–12 применять последовательно; настольная оболочка Лолы независима от
многозадачности и не разрешает фоновые субагенты автоматически. Развитие IDE —
существенный отдельный объём с prototype gate, а не обещание одного малого обновления.

Подробные технологии, предполагаемые классы и acceptance описаны в главах 50–53.
Предлагаемые имена модулей в планах не означают, что эти модули уже существуют.
