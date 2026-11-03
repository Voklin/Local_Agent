# Этап 17: расширенные проверки и восстановление

1 ноября 2026. Следующий этап после [памяти проекта](71-project-memory-stage16.md), по [Roadmap V2](57-roadmap-v2.md).

## Проверки по затронутым файлам

В IDE → «План и проверки» проверке назначается тип: тесты, линтер, типы, синтаксис, своя команда или LSP. Точные команды/аргументы задаёт пользователь; приложение не угадывает и не выполняет найденные package scripts автоматически. Каждое исполнение подтверждается штатным approval.

applies_to — необязательные шаблоны относительных путей. Автоматический запуск выбирает проверки по изменённым файлам, учитывая rename destination. Пустой список означает «всегда». Проверки, связанные с критерием приёмки, остаются обязательными; ручной checks-only выполняет весь набор. Пропуск по шаблону не считается успешным тестом. Результаты и список неприменимых checks видны в «Подробностях».

[required_checks](../agent/verification_plan.py) используется планировщиком и StageVerifier одинаково; отдельного конкурирующего VerificationPlan/executor нет. Сохранены CallJournal, ToolExecutor, RequestBudget и старые scopes. Старые checks без kind/applies_to сохраняют прежнее поведение. Успех посторонней команды не стирает известный провал. Семантический критерий без связанной проверяемой команды остаётся unverified; приложение не отмечает его автоматически выполненным по тексту модели.

## LSP как evidence

Выберите «LSP · сохранённый файл», укажите файл и файловую область с зависимостями; сервер настройте и включите в дополнительных возможностях IDE. Нужно также включённое расширение команд проекта. Программа-сервер выполняется с правами пользователя; область evidence не ограничивает её OS доступ. Существующий клиент работает с сохранённым UTF-8 файлом до 256 КБ; неподдерживаемый файл не становится успешной проверкой. Сам LSP клиент не принимает workspace/applyEdit/executeCommand.

Новый fixed tool run_project_diagnostics принимает только check_id уже заданной проверки. Перед запуском показываются сервер, argv, файл, назначение и scope. Approval записывается до started, время ожидания человека исключено из execution deadline. Tool проходит обычный журнал и учёт, readonly режим его не допускает. Checks-only не вызывает LLM.

Подтверждение требует полного pull ответа LSP, без ошибок severity 1, без truncation/изменения файла. Stabilized push без подтверждения завершения остаётся неполным. Некорректная severity — ошибка протокола, не clean report. Warnings не блокируют отсутствие ошибок, но видны в UI.

[diagnostics_evidence](../agent/diagnostics_evidence.py) связывает receipt с точным user check, сохранёнными файлами/зависимостями, настройками сервера и rollback revision. Изменение этих данных, отзыв доступа или неполный witness делают evidence stale/unverified. Обычная команда с тем же check_id не может выдать себя за LSP. Ошибки не закрываются финальной фразой модели. Критерии приёмки и TaskGraph используют этот же assessor. Полнота относится к одному сохранённому файлу, не всему проекту. Версии бинарных toolchains отдельно не фиксируются; нужные файлы конфигурации следует включать в dependencies.

## Восстановление и Git

Повторы и bounded recovery этапа 15 сохранены; новый контур исполнения не создаётся. Откат по-прежнему начинается с preview и отдельного подтверждения. Проверка after-state выполняется до эффектов и перед каждым файлом. Если внешний edit появился между файлами, он сохраняется; частичный откат имеет rollback_unknown и требует ручного review. Неизвестные side effects автоматически не повторяются.

В «Изменения и откат» у подтверждённого набора появилась кнопка **Сохранить Git-снимок**. [GitCheckpoints](../agent/git_checkpoints.py) архивирует before/after bytes из проверенных snapshot artifacts, вместе с manifest путей/хешей/типов, в отдельный bare Git внутри профиля Neutral. Требуется установленный Git. Git refs, HEAD, индекс, hooks и файлы пользовательского проекта не меняются; это не commit в рабочей ветке. Экспорт работает и для папки без .git. Модели этот UI-only API недоступен.

Git IO выполняется BackgroundJob, stdio Core остаётся отзывчивым; операцию можно отменить. Сохраняются только известные applied версии с текущим разрешением доступа; незавершённые/неизвестные группы экспортировать нельзя. Refs адресуются group + content digest, публикуются после записи всех объектов. Прерывание до публикации может оставить лишь unreachable объекты в приватном хранилище; исходники проекта не меняются. Метаданные repository/commit/ref доступны в UI и после restart.

Обычный откат использует прежний SnapshotStore с конфликтными guards. Git — независимый архив на случай повреждения рабочего snapshot-кеша; автоматического git reset/clean/checkout или принудительного восстановления из него нет. Для ручного чтения архива используется `git --git-dir=ПУТЬ show COMMIT:manifest.json`, затем blob entry из manifest. GUI не предлагает разрушительного восстановления в обход preview.

## Проверки

Уже прошли целевые сценарии: настоящий stdio LSP clean/error/incomplete, смена исходника/сервера, привязанный критерий без LLM, Git bytes/CRLF/HEAD/index, HTTP Core checkpoint/health и конфликт между двумя файлами rollback. Прежний regression 65 unit прошёл. Набор workflow/TaskGraph с правильным import path прошёл 12 сценариев. Один ранний запуск tests.migration.test_task_graph_execution без tests/migration в sys.path ошибся на импорте fixture; это исправлено runner-ом. Первый Git assertion выявил сохранённый Windows CRLF — oracle исправлен на точные исходные bytes, production backup не изменял строки.

Первый сквозной LSP тест выявил попытку поставить awaiting_approval после started. Новый tool внесён в approval_tools; теперь durable approval предшествует started. Гарантии журнала не ослаблялись. Итог: **482 unit tests (2 platform skips), 126 Core/HTTP tests**, npm build и полный Electron Studio smoke прошли. Логи: .test-data/stage17-unit-final.log, stage17-http-final.log, stage17-build-verified.log, stage17-electron-final.log. UI сделал 23 synthetic HTTP; LSP checks-only проверен с нулём model HTTP. Отдельный полный повтор UI прошёл ветку формы LSP, файловую область и возврат к обычной команде (stage17-electron-lsp-form.log); снимок stage17-lsp-check-form.png осмотрен.

Документация генерируется из исходников и проверяется tools/check_docs.py; git diff --check чистый. Снимок stage17-git-checkpoint.png осмотрен: кнопки и сохранённая Git-ссылка находятся в существующей панели «Изменения и откат». Доказательств улучшения качества произвольной LLM этим этапом не заявляется: он проверяет исполнение и свидетельства, не качество генерации.

## Файлы и совместимость

Новые модули: [verification_plan](../agent/verification_plan.py), [diagnostics_evidence](../agent/diagnostics_evidence.py), [git_checkpoints](../agent/git_checkpoints.py). Расширены существующие task_contract, StageVerifier, verification_evidence, engine, language_diagnostics, TaskGraph и workspace_access. Host — TaskExecution/TaskService, ExtensionService, WorkspaceReview и фиксированные RPC/IPC. UI — IdeTaskOptions, TaskProgress и WorkspaceReview в прежнем Studio дизайне.

SQLite schema остаётся 3. Старые check entries не становятся автоматически доказанными, новые поля optional. Перед откатом версии сохраните профиль: старый Core не понимает LSP checks, поэтому сначала верните их к обычным командам или откройте старый профиль без таких заданий. Private Git архив и канонические чаты не удаляются. Installer 7.0.1 этого этапа не содержит: изменения пока в исходниках.

Следующий пункт roadmap — **18: отдельный prototype gate настоящей IDE/extension host**, с измеримым go/no-go до интеграции. JSON-quality gate модели без native tools остаётся открытым, это отдельное ограничение качества, не закрываемое успешным unit-тестом.
