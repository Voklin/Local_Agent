# 62. ContextPack: подбор источников и подтверждение передачи

Этап 14a продолжает индекс из [главы 61](61-project-intelligence-index.md).
Это первый вертикальный срез: конкретные сохранённые фрагменты попадают в
модельный запрос, сохраняют происхождение и проверяются перед HTTP. Каноническая
история, разрешения записи и итоговая проверка задачи остаются отдельными.

## Пользовательский путь

1. В IDE пользователь выбирает проект и задаёт вопрос с именем файла/символа.
2. Подбор использует уже активный индекс, явно указанные пути, последние изменения
   и успешные результаты tools. По имени исходника добавляются возможные тесты.
3. В подробностях работы модели появляется блок «Источники контекста»: файл,
   диапазон и причина выбора. Это выбранные saved sources, не покрытие всего проекта.
4. Существующий RequestBudget.fit подгоняет весь запрос под фактическое окно.
   Наименее приоритетные optional fragments исключаются целиком, пользовательский
   запрос не обрезается. Новых обязательных настроек количества токенов нет.
5. Loopback-сервер получает допустимые источники автоматически. Для внешнего API
   показывается получатель с endpoint, модель, каждый диапазон, SHA-256 и полный
   передаваемый текст. «Отправить эти исходники» разрешает одну HTTP попытку.
6. Отказ приостанавливает задачу без передачи пакета. Изменение исходника, политики
   или получателя во время ожидания отменяет согласие. Продолжение создаёт новый
   preview. Retry и JSON protocol repair не наследуют старое согласие.

Автоподбор для JSON tool protocol отключён по умолчанию после измеренной регрессии
Qwen 2.5 Coder. Controlled benchmark может явно передать ContextBuilder, это
внутренний экспериментальный параметр Engine, а не скрытая настройка пользователя.
Chat без project tools и Лола новые source packs не получают. Выключение
проектных read tools также отключает автоматическое чтение; активный MCP/навык
сам по себе его не включает.

## Контракты и файлы

- [context_builder.py](../agent/context_builder.py): ranking, overlapping range
  deduplication, visible receipt deduplication, source anchors и финальная validation.
- [engine.py](../agent/engine.py): временная model projection после фильтра доступа
  и перед единственным RequestBudget.fit. Canonical _messages не изменяются.
- [request_budget.py](../agent/request_budget.py): снятие низкоприоритетных fragments
  до сокращения tool schemas и общей компрессии истории; удаление host metadata
  из SDK payload.
- [model_client.py](../agent/model_client.py): повторное чтение в worker перед
  каждой физической попыткой, проверка доступа/политики/хеша и конкретного согласия.
- [task_service.py](../core/python/task_service.py): отдельное context approval,
  waiting_approval, Stop и существующее решение по run_id/approval_id. Отдельное
  согласие на source не разрешает запись файла или запуск команды.
- [SourceContextPreview.tsx](../apps/desktop/src/SourceContextPreview.tsx): читаемый
  recipient/model/source preview, полный JSON по раскрытию. React экранирует текст.
- [TaskProgress.tsx](../apps/desktop/src/TaskProgress.tsx): paths/ranges/reasons без
  source bodies. После изменения grants прошлый список скрывается; при загрузке
  history metadata снова проходит текущую политику доступа.
- [benchmark_agent.py](../tools/benchmark_agent.py): --indexed / --context-pack,
  physical HTTP source evidence и прежний held-out oracle correctness конечного diff.

При дедупликации receipt с SHA должен совпадать с текущим полным hash. Для
legacy read_file без SHA дедупликация допускается только при сравнении полного
текста небольшого файла; совпадение одного фрагмента не подтверждает старый hash.

Source anchor содержит workspace_id, path, source_kind=saved-file, start/end_line,
sha256 полного файла, policy_version, причину, kind и content выбранных строк.
Абсолютный root находится только в host metadata, не в HTTP payload. Полный source
pack не сохраняется в истории/checkpoint. В checkpoint остаются metadata последнего
запроса и счётчик снятых под бюджет фрагментов.

Source data идёт отдельным user-role JSON перед текущим запросом. В system добавлено
только правило интерпретации untrusted source data. Комментарии/строки исходника
не получают полномочий изменять правила, запускать tools или подтверждать готовность.
Проверка SHA подтверждает сохранённые bytes, а не качество программы.

## Границы безопасности

После fit допускается только удаление источников, поэтому payload не растёт в обход
budget gate. На HTTP retry/JSON repair данные проверяются заново. При внешнем
approval после ожидания пакет сверяется ещё раз: изменившиеся данные не отправляются
под старым согласием. Проверки и начало HTTP не являются одной файловой транзакцией;
пакет фиксирует наблюдавшийся снимок, последующие изменения проверяются edit/verification
механизмами отдельно.

HTTPX environment proxy и redirects отключены для model transport: указанный в
preview получатель не может быть заменён автоматическим перенаправлением. Это
может потребовать явного сетевого решения для окружений с обязательным proxy;
добавление доверенного proxy UI в эту поставку не входит.

Без host approval callback внешнему API новый auto ContextPack удаляется. LAN адрес
тоже требует подтверждения; автоматически разрешён только HTTP(S) loopback.
Telegram не подтверждает source передачу по усечённому preview: полный просмотр
доступен в приложении, удалённый /reject по-прежнему возможен. Ключ подключения из настроек в preview
не включается. Существующие вручную заданные сообщения/инструкции проекта и
результаты явно вызванных tools используют прежние правила доступа и передачи;
новое окно относится к автоматически собранным источникам ContextPack.

## Ограничения MVP и fallback

Только сохранённые файлы; dirty editor guard не снят, unsaved overlay отсутствует.
Подбор лексический, без embeddings или дополнительного inference. Кандидаты:
явные пути, до шести identifier terms, definition/text hits, недавние эффекты и
имена тестов. Не более 12 диапазонов по 60 строк; это защита read fan-out, а не
новый ручной token cap. Существующий range reader ограничивает file bytes/line size.
Границы и тесты по имени не доказывают полноту dependency graph.

Если индекс ещё не готов или недоступен, остаются явные пути и tool evidence;
полный обход проекта ради заполнения prompt не запускается. При отсутствии
релевантных sources Engine работает обычными tools. Неполная выдача не означает
отсутствия определения во всём проекте. Источники не заменяют StageVerifier и
не закрывают quality gate JSON моделей.

## Проверки и измерения

Финальные проверки:

- **415 unit**, два платформенных пропуска: `.test-data/context-unit-accepted.log`.
- **85 Core/HTTP**, все прошли: `.test-data/context-http-final.log`. В предыдущем
  прогоне один TTS disconnect тест не успел освободить lock; отдельные три TTS
  теста и полный повтор HTTP прошли. Это тайминговый сбой, код TTS не менялся.
- Дополнительно **42 budget/source/auto проверки** и **15 source security tests**:
  `context-budget-final.log`, `context-sources-final.log`.
- `npm run build` и Electron GUI smoke прошли; реальные Core события и localhost
  HTTP, отображение источников, renderer preview fixture и IPC решения проверены.
  Скриншоты осмотрены: `.test-data/neutral-gui/context-sources.png` и
  `context-approval.png`. Backend разрешение подтверждено отдельно настоящими
  HTTP тестами; example.invalid в renderer fixture никогда не запрашивается.
- Redirect/proxy выключены, source root/hash/policy/revoke, retry, отказ,
  изменившийся preview/recipient, Stop/stale ID, отдельный write approval,
  удаление всех 12 optional fragments и legacy receipt hash проверены.

### Парный LM Studio прогон

Одна загруженная модель за раз, context 8192, GPU ratio 1 со strict VRAM cap,
KV cache на CPU, eval batch 128, Flash Attention, K/V q8_0, seed 0. Engine manual
профиль фиксирует 1536 output tokens, 10 turns и 3 минуты на один запуск, чтобы
сравнение оставалось совместимым с baseline 20a. Это экспериментальные отсечки,
они не добавлены в пользовательский local auto режим. В recovery два запуска.

| Модель / протокол | Режим | Correct task/diff | E2E | HTTP | Reported input / output |
|---|---|---:|---:|---:|---:|
| Qwen 2.5 Coder 7B / JSON | без pack | 1/5 | 1/5 | 22 | 55073 / 1280 |
| Qwen 2.5 Coder 7B / JSON | с pack | 0/5 | 0/5 | 28 | 74463 / 1524 |
| Ornith 1.5 9B / native | без pack | 4/5 | 3/5 | 24 | 54482 / 3051 |
| Ornith 1.5 9B / native | с pack | 5/5 | 4/5 | 21 | 52613 / 3617 |

На Ornith pack сохранил правильные результаты поиска, исправил конечное
многофайловое переименование и прошёл recovery. Многофайловый diff правильный,
но Engine не успел завершить ответ до отсечки: это **не** полный E2E success.
Улучшение 4/5 → 5/5 относится к независимому oracle конечной задачи, а не к
доверию фразе модели «готово». Результат позволяет включить первый срез для
native project tools; он не подтверждает произвольные большие проекты.

На Qwen дополнительный JSON source envelope ухудшил результат и увеличил число
HTTP запросов. JSON rollout оставлен выключенным. Обычные JSON tools продолжают
работать; gate главы 59 остаётся открытым.

Точные отчёты и собственные неизменяемые source archives:

- [Qwen control](../.test-data/context-14a-qwen-control/report.json),
  [Qwen pack](../.test-data/context-14a-qwen-pack/report.json);
- [Ornith control](../.test-data/context-14a-ornith-control/report.json),
  [Ornith pack](../.test-data/context-14a-ornith-pack/report.json);
- [агрегат](../.test-data/context-14a-comparison.json).

В каждой папке есть report.md и baseline-sources.zip с hashes. Пары не выдаются
за один Git commit: между запусками уточнялись host guards и порядок pruning;
manual контроль без pack от этих ветвей не зависит. Последующее уточнение
дедупликации полного SHA проверено unit-тестами; маленькие целиком выбранные
fixture файлы используют тот же путь сравнения текста.

Это по одному прогону пяти **small** задач. Фоновые тесты и runtime cutoffs
влияют на wall time, поэтому время 642.535 → 576.534 с не является строгим
latency benchmark. Usage приводится только там, где сервер успел его сообщить;
прерванные генерации имеют неполное покрытие. Универсальная экономия токенов,
качество на medium/large и устойчивость нескольких повторов не доказаны;
они остаются gate 20b. Индекс medium/large отдельно измерен в главе 61.

Installer, commit/push, merge/release и реальные внешние API этой поставкой не
выполнялись. На финальной проверке REST и SDK LM Studio не показывают загруженных моделей.
Причина последующей выгрузки сервером отдельно не исследовалась. Во время прогона
Qwen была выгружена перед загрузкой Ornith; одновременно обе не загружались.

## Следующий шаг

По основному порядку сначала [11a/11b — Run Registry/Scheduler/Ledger](63-run-registry-scheduler-ledger.md),
после них 14b/15 — устойчивые задачи и контекстные циклы. Надёжность JSON tool agency остаётся
отдельным незакрытым gate главы 59; дополнительный контекст сам по себе её не решил.

## Состояние рабочей копии и откат

Ветка `codex/electron-agent-bridge`, HEAD
`9572082e8f0c4ce625e515fdb7e5c0ac466a8b09`, 182 изменённых/новых пути на момент
приёмки. Рабочая копия уже содержала предыдущие этапы; они не очищались и не
выдавались за изменения только 14a. Пользовательский docs.zip сохранён (491560 байт).
Новые основные файлы: context_builder.py, SourceContextPreview.tsx,
test_context_builder.py и эта глава. Изменены Engine/ModelClient/RequestBudget,
TaskService/SessionService/TelegramService, UI task/approval и benchmark/docs.
Схема canonical SQLite и данные чатов не мигрировали, кеш индекса совместим.

Для ограниченного отката функциональности внутренний параметр Engine
context_builder=False отключает model projection. Удалять весь dirty diff,
сбрасывать прежние стадии или восстанавливать старую SQLite ради этого не нужно.
Следующая поставка требует отдельного запроса пользователя.
