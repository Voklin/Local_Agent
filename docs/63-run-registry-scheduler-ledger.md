# 63. Этап 11a: Run Registry, очередь генераций и учёт расхода

> Историческое состояние промежуточной поставки. Полный этап 11 завершён: [актуальные контракты и проверки](66-stage11-complete.md).

**Статус:** первая поставка этапа 11 основного [roadmap](57-roadmap-v2.md).
После 14a следующий обязательный компонент — 11, перед TaskGraph 15. Упоминание
14b/15 в конце предыдущей главы не отменяет эту зависимость.

## Что видно пользователю

В подробностях работы модели появился блок «Запуски и фактический расход».
Он показывает физические отправки модели, только сообщённые сервером токены,
оценки ещё активных запросов, ожидание модели и отдельное время подтверждений.
По раскрытию загружается история выбранного чата; у каждого продолжения свой ID,
модель, статус, длительность и число вызовов инструментов. Полные счётчики
прошлого запуска раскрываются отдельно. Чужой chat_id Core отклоняет.

Reservation — ещё не отправка и не списание токенов. Нет usage — расход неизвестен,
а не равен нулю. Денежная стоимость не вычисляется по выдуманной цене провайдера.
Новые token/time caps для local auto не добавлены. RequestBudget остаётся единственным
окончательным ограничением вместимости HTTP запроса.

Запись файла/команда/MCP по-прежнему требуют своих подтверждений. Окно approval не
занимает ресурс генерации. Сам интерфейс пока сохраняет один активный выбранный
чат: существующий admission guard защищает mutable SessionService. Это ограничение
UI jobs, а не владение ресурсом модели на всё время задачи.

## Архитектура и новые файлы

- [run_registry.py](../agent/run_registry.py): RunRegistry, RunContext и BudgetLedger.
- [inference_scheduler.py](../agent/inference_scheduler.py): общая FIFO очередь,
  InferenceAttempt и scheduled_request для SDK/probe/research.
- [model_client.py](../agent/model_client.py): ScheduledStream, физический transport
  hook и отдельные request workers/SDK cleanup tasks.
- [RunHistory.tsx](../apps/desktop/src/RunHistory.tsx): выбранная история и понятный
  расход; тела исходников, prompt и ключи в этот компонент не передаются.
- [test_run_registry.py](../tests/test_run_registry.py),
  [test_run_control.py](../tests/migration/test_run_control.py): durable/FIFO/HTTP проверки.

TaskService регистрирует Chat/IDE/Лолу, проверку модели и opt-in исследование.
OperationContext получает ссылку на RunContext. Основная, вспомогательная memory
генерация, JSON repair, probe и research проходят одну очередь процесса.
Старый InferenceGate остаётся только admission guard UI-сервиса для совместимости;
session_status/optional status показывают настоящую очередь scheduler.

Прямой ModelClient вне Core тоже использует общую очередь, но durable run появляется
только при явной привязке OperationContext к Registry. Это сохраняет совместимость
старого Qt/низкоуровневых тестовых адаптеров; полная миграция этих entrypoints отдельно.

## RunContext и состояние

Каждое исполнение/продолжение получает новый 32-символьный run ID. Chat ID и journal ID
сохраняют связь с прежней историей и checkpoint. Повторно исполнить уже использованный
run ID нельзя. Task state/RunState и CallJournal остаются авторитетом выполнения:
RunRegistry отражает их metadata, не создаёт второй план и не подтверждает side effects.

Run содержит kind, model, hash подключения, parent_id, depth/fan_out, PID владельца,
state, timestamps, elapsed, approval wait и свой счётчик обработанных tool receipts.
Ключи, заголовки HTTP, prompt, source text и текст сетевых исключений не сохраняются.
Legacy task.tool_calls при генерации сбрасывается, поэтому RunContext считает receipts
отдельными событиями, а не вычитает старое значение. При crash между durable journal
receipt и telemetry increment счётчик может недосчитаться; авторитет эффекта — journal,
атомарное согласование этих событий относится к 11b.

Внутренний контракт дочерних prototypes: наследование model/base URL/API protocol,
parent cancellation, depth=1 и всего до трёх детей на epoch. Drift подключения
проверяется на SDK, probe и raw research путях. Создание дочерних агентов пользователем
или моделью и запуск их инструментов в этой поставке **не включены** — это этап 12.
Наследование профиля само по себе не предоставляет ребёнку tool permissions.

## Lease: очередь и закрытие HTTP

1. Подготовить/подогнать запрос обычным RequestBudget.
2. Проверить ContextPack и, для внешнего API, получить конкретное согласие пользователя.
3. Создать reservation telemetry и cancellable FIFO ticket.
4. Дождаться свободного ресурса, повторно проверить binding модели и source hashes/
   permissions после ожидания. Изменившийся внешний preview не переиспользуется.
5. HTTPX request hook считает только POST /chat/completions или /responses.
6. Держать ticket, пока SDK stream действительно не закрыт. Перед retry он
   освобождается, следующая попытка встаёт в хвост. Backoff не занимает ресурс.
7. Последний cumulative usage кадр учитывается один раз; отсутствие terminal frame
   хранится как unconfirmed, не объявляется корректным полным ответом.

Старый ticket не освобождает новый. Отмена ожидающего запроса снимает именно его
reservation и не делает HTTP. Во время ожидания tools/approval/будущего child run
генерация родителя ресурс не удерживает. SDK cleanup защищён shield от повторного
Stop; shutdown отменяет request workers и ждёт их cleanup вместо отмены всех tasks.
При ошибке SDK close ticket помещается в карантин. Следующий waiter получает
объяснимую ошибку, не занимает вечную очередь и не делает HTTP. Карантин снимается
только после успешного закрытия владеющего HTTP клиента; при его сбое требуется
перезапуск Core. Не заявляется, что один лишь failed close освободил соединение.

Один inference на процесс не гарантирует одну модель в VRAM. Scheduler не управляет
внешним LM Studio, его другими клиентами, TTS/STT или другой копией Core. Автоматической
выгрузки пользовательских моделей/OOM residency policy здесь нет.

## BudgetLedger: корректность и стоимость запросов

Таблица inference_attempts хранит purpose, reservation, факт HTTP attempt, phase,
state, queue/elapsed timestamps, последний usage и terminal outcome.
Purpose различает agent, json_repair и вспомогательные генерации; исходники не входят
в telemetry. Условный отказ optional stream_options тоже является физическим HTTP.
Отказ от source preview не является HTTP и не тарифицируется нашим счётчиком.

Счётчики Run обновляются в одной SQLite транзакции с before/after вкладом attempt.
Повторная terminal запись даёт нулевую дельту. Snapshot читает готовый aggregate,
не пересчитывает всю историю attempts на каждый checkpoint. Reservation освобождается
при завершении/ошибке/отмене, но unknown usage не превращается в доказанную нулевую цену.
Учёт — наблюдение, не самостоятельная политика остановки.

## SQLite v3, recovery и удаление

Storage мигрирует v1/v2 → v3 атомарно. Добавлены runs и inference_attempts, индексы
по chat/state/parent/run. Сообщения, checkpoints, journal и snapshots не меняют
формат. Online backup включает новые таблицы; восстановление проверено.
Удаление чата удаляет его run/attempt metadata в той же транзакции.

После restart только owner с доказанно завершённым PID позволяет пометить активный
run как paused/recovered. Незавершённые попытки получают interrupted/unknown_after_restart,
их reservation снимается, в том числе при сбое **после task paused, но до конца
HTTP cleanup**. Для уже terminal task состояние не повышается обратно в running.
Никакой HTTP или tool effect автоматически не повторяется.
SessionService и CallJournal требуют прежнюю проверку неизвестных эффектов перед resume.
Windows liveness использует OpenProcess/GetExitCodeProcess/CloseHandle; сигналы или
TerminateProcess для проверки PID не используются. Access denied считается неопределённостью,
а не доказанным завершением. PID reuse консервативно может оставить прошлый owner активным;
уточнение process creation token — следующий шаг, автоматическое исполнение от этого не появляется.

Старый Core v2 не должен открывать профиль v3: существующая защита версии его остановит.
Для отката на старую сборку нужна её **собственная предмиграционная резервная копия**;
не удалять новые таблицы вручную и не сбрасывать общий dirty Git diff.
Пользовательский профиль и установка приложения тестами не заменялись: все DB тестов
и живой генерации находились в отдельных временных профилях.

## Проверки и измерения

- **430 unit**, два платформенных пропуска: `.test-data/run-unit-accepted.log`.
- **87 Core/HTTP**: `.test-data/run-http.log`.
- Дополнительные **37** cleanup/stream/source проверки: `.test-data/run-cleanup.log`.
- Ещё **22** финальные recovery проверки и **23** проверки с failed-close guard:
  `.test-data/run-recovery-final.log`, `.test-data/run-close-failure.log`.
  Отдельно проверен resume-safe счётчик инструментов: `.test-data/run-tools-final.log`.
- TypeScript/build и Electron smoke: `.test-data/run-build-final.log`,
  `.test-data/run-electron-final.log`. Скриншот run-ledger.png осмотрен.
- Реальная Ornith 1.5 9B: **одна HTTP попытка**, usage **1146 input / 301 output**,
  ledger совпал с независимым request hook и ModelClient totals, резерв 0, task completed.
  [Точный отчёт](../.test-data/run-live-11a/report.json) содержит профиль, hashes и metadata;
  [скрипт](../.test-data/run-live-check.py) и log сохранены локально.
- Профиль живого теста: context 8192, strict VRAM cap, KV CPU, batch 128, Flash Attention,
  K/V q8_0. Перед загрузкой проверено отсутствие других резидентных моделей.
  Внешние API не вызывались. Тест учёта не доказывает качество coding задач. После него уточнены только guards
  orphan discovery для paused task, failed SDK close и resume-safe tool counter; они проверены отдельно,
  модельный payload не изменён. Исходные hashes отчёта сохранены без подмены.

В общем наборе найдена существовавшая гонка index subtree enumeration → file delete:
FileNotFoundError ошибочно требовал full rebuild. Теперь отсутствие обрабатывается
инкрементально (удаление root всё ещё ошибка). Добавлена детерминированная проверка.
Две старые фикстуры обновлены под v3 и явный registry dependency. GUI проверка сверяет
реальные HTTP, включая auxiliary memory request, вместо ошибочного предположения о двух.

## Что ещё требуется для полного этапа 11

11a даёт durable identity/ledger и общий ресурсный арбитраж. Последующая поставка
[фоновых чатов 11b](64-background-chat-runs.md) закрыла отдельные owners и переключение.
Ниже сохранён исходный перечень следующего объёма; его актуальный статус — в главе 64.

- отдельный execution/session owner на каждый одновременно активный run вместо
  одного mutable TaskService.chat/engine; независимые background чаты и UI переключение;
- кооперативное parent/child handoff в настоящем executor, а не только контракт/queue
  prototype tests; recovery дерева с UI и проверка kill/restart отдельного Core;
- process creation identity, resource groups/provider capabilities и явная политика
  разных моделей/OOM, не выдающая lease за управление VRAM;
- добровольный денежный бюджет платных провайдеров с согласованными ценами/поведением.

Субагенты 12 и TaskGraph 15 не объявляются завершёнными этим срезом. Gate JSON
compatibility Qwen из главы 59 остаётся открытым; работа auto ContextPack из 14a сохранена.
Установщик не собирался, commit/push, merge/release и установка поверх приложения
не выполнялись. Ранее подготовленные изменения и docs.zip сохранены.
