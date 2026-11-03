# 65. Владелец процесса и восстановление после аварии — 11c

> Историческое состояние промежуточной поставки. Полный этап 11 завершён: [актуальные контракты и проверки](66-stage11-complete.md).

Дата: 28 октября 2026. Следующий срез [этапа 11](57-roadmap-v2.md),
после [фоновых чатов 11b](64-background-chat-runs.md).

## Что изменилось для пользователя

После аварийного завершения Core сохранённый ответ открывается без автоматического
повторения запроса. Запрос, который ожидал модель, не отправляется при восстановлении.
Незавершённые резервы и очередь снимаются; неизвестный расход не превращается в ноль
известных токенов. Старое разрешение на запись после restart не действует.

История запусков различает завершившийся процесс и повторное использование его PID.
Счётчики восстановленного запуска появляются непосредственно при загрузке чата:
отдельно открывать историю для обновления зависшего reservation больше не требуется.
Файлы проекта и автоматическая отправка данных внешней модели этим не разрешаются.

## Почему недостаточно PID

PID может перейти другому процессу. Проверка «этот PID существует» не доказывает,
что жив именно прежний Core. В `runs.data` теперь сохраняется `owner_token` рядом
с прежним `owner_pid`. Формат SQLite schema v3 не меняется — это дополнительное
поле существующего JSON, новая миграция таблиц не нужна.

| Платформа | Lifetime token и проверка |
| --- | --- |
| Windows | `win-filetime:<creation FILETIME>`. Query-only `OpenProcess`, `GetProcessTimes`, `GetExitCodeProcess` и обязательный `CloseHandle` для одного объекта процесса. Сигналы и завершение чужих процессов не используются. |
| Linux | `linux-start:<boot ID>:<start ticks>`. `/proc/<pid>/stat`, boot ID и распознавание zombie; имя процесса может содержать пробелы и скобки. |
| Другие ОС | Проверка существования без lifetime token. При невозможности сравнения нет доказательства повторного использования PID. |

`inspect_process` возвращает `alive`, `dead` или `unknown` вместе с доступным token.
`owner_ended` разрешает orphan recovery только по доказанному завершению PID либо
различию сопоставимых lifetime tokens. Недоступный процесс, отказ доступа, отсутствующий
старый token и неизвестная версия token не доказывают смерть владельца.
Такие записи сохраняются консервативно. Старые runs без token продолжают использовать
проверку существования PID; узнать задним числом их creation time нельзя.

`owner_alive` оставлен как совместимая bool-проекция: `unknown` защищает владельца
от ошибочного восстановления. Внутренние тесты прежнего `alive` callback сохранены.

## Реестр и checkpoint

При первом `RunRegistry.ready()` orphan detection выполняется в одной транзакции.
Probe кешируется для одинакового owner PID/token в этом проходе: дочерние prototype
records одного владельца не получают расходящихся результатов из повторных проверок.

Активный run завершившегося владельца переходит в `paused`; уже `paused` или `failed`
не переводится обратно в `running`. Включаются также terminal runs, у которых осталась
active attempt между записью checkpoint и завершением transport cleanup.
В каждой такой attempt устанавливаются `interrupted` и `unknown_after_restart`;
существующий BudgetLedger атомарно снимает estimates и queued count, сохраняя физические
HTTP attempts и действительно сообщённый usage. Повторное чтение не удваивает расход.

Новые metadata: `recovery_cause` (`owner_exited` или `owner_replaced`) и `recovered_at`.
Это время обнаружения сбоя, не выдуманное время завершения процесса. Ссылки parent/child
сохраняются. Восстановление telemetry дерева не является исполнением или возобновлением детей.

После `SessionService` recovery координатор вызывает `_refresh_run_ledger` для того же
chat/run. Изменённый ledger сохраняется в canonical chat/checkpoint существующим
атомарным механизмом. Run другой беседы не используется для счётчиков этого чата.
Live owner по-прежнему возвращает собственный snapshot и не проходит crash recovery.

## Файлы и функции

| Файл | Назначение |
| --- | --- |
| `agent/process_identity.py` | Независимые read-only probes, lifetime tokens, bool compatibility и консервативное решение о завершении owner. |
| `agent/run_registry.py` | Запись token, owner cache на recovery pass, причины восстановления и транзакционное обновление orphan attempts. |
| `core/python/task_service.py` | Обновление и сохранение ledger при открытии восстановленного чата. |
| `apps/desktop/shared/contextTypes.ts`, `RunHistory.tsx` | Типы recovery metadata и понятное пояснение повторно использованного PID. |
| `tests/test_process_identity.py` | Реальный собственный child process, Windows без `os.kill`, Linux parser, unknown/legacy и simulated PID reuse. |
| `tests/migration/test_run_owner_restart.py` | Настоящий subprocess Core, kill/restart с тем же изолированным профилем, stream/queue/approval. |

Подробные сигнатуры включены в [справочник Python](reference/python.md)
и [справочник тестов](reference/tests.md).

## Проверки и границы доказательств

- **20 unit** процесса/реестра/очереди, 1.539 s: `.test-data/owner-identity-unit.log`.
  Собственный child естественно завершается после закрытия stdin. Windows probe
  отдельно проверен при запрете `os.kill`. PID reuse моделируется изменением
  lifetime token в probe; система не заставляется переиспользовать настоящий PID.
- **2 actual Core kill/restart**, 7.010 s: `.test-data/owner-restart-http.log`.
  В первом сценарии один чат получает сохраняемый SSE фрагмент, другой ожидает queue.
  После kill/restart оба приостановлены, reservations/queue равны нулю, interrupted
  равен единице, partial присутствует ровно один раз. Независимый HTTP server получил
  ровно один запрос до и после повторной загрузки чатов. Во втором сценарии прежний
  write approval отвергается, файл не создаётся, новых HTTP нет.
- **32 task service regression**, 14.676 s: `.test-data/owner-task-regressions.log`.
- **3 background regression**, 3.650 s: `.test-data/owner-background-regressions.log`.
- `npm run build` и целевой Electron сценарий переключения потоков:
  `.test-data/owner-build.log`, `.test-data/owner-electron.log`.
- Генерация справочников, проверка Markdown ссылок и `git diff --check`.

Для экономии не повторялся общий baseline LLM и полный unit suite предыдущего среза:
проверены связанные контракты и реальный Core. Никакие пользовательские процессы
не завершались тестами. Все DB, HTTP и Core сценарии используют отдельные временные профили.

## Что остаётся

Полный этап 11 ещё открыт. Нужны реальный parent/child executor с handoff/join,
контракты результата и recovery исполнения дерева, provider resource groups и
политика residency/OOM разных моделей. Фоновые чаты пока используют одно подключение
и модель; управление внешней VRAM и многопроцессный scheduler не добавлены.
Первичная recovery проверка не является постоянным мониторингом других Core-процессов.

Для отката сохраняются прежние ограничения schema v3; не нужно удалять metadata,
checkpoint или journal вручную. Установщик, commit/push, merge/release и установка
поверх приложения в этом срезе не выполнялись. Предыдущие изменения и `docs.zip` сохранены.
