# Проверки результата в новой IDE

## Цель и решение

Продолжение плана 3 ноября 2026 по результатам quality baseline: пользователь задаёт критерии и точные команды проверки в независимой IDE-панели. Существующий Core исполняет их через approval/ToolExecutor/CallJournal и связывает evidence с check_id и ревизией исходников.

Раздел открывается из composer и «Работы». Команда задаётся программой и отдельными строками argv, без shell-конкатенации. Критерий связывается с существующей проверкой либо остаётся ручным. Сохраняются scope и dependencies, timeout, kind и applies_to. Не добавляется новый executor или verifier.

Настройки следующего запуска — UI draft. В пределах view они сохраняются отдельно для каждого чата; текущий draft переживает reload через существующее Code-OSS webview state. Canonical options сохраняются Core при старте задачи и восстанавливаются из checkpoint. Черновик не заменяет evidence или сохранённые options уже исполняемой задачи.

Agent использует подготовленные options. Ask/Plan передают read_only без исполняемых checks и критериев; draft для Agent сохраняется. Ручной checks_only не требует модели и не очищает несохранённый текст запроса. Resume передаёт сохранённые Core options, не применяя новые drafts. Любой неизвестный эффект продолжает блокировать запуск.

UI отдельно показывает исполнение команды, актуальность evidence и статус критериев. Exit 0 для files scope не становится подтверждением всего проекта; критерий без связи остаётся непроверенным. Ошибочная/отклонённая/устаревшая проверка не превращается в успешную по тексту ответа модели.

## Приёмка

- Unit: пустые критерии и reindex links; stable check IDs; argv boundaries; scope/dependencies; Ask/Plan; checks_only; изоляция draft разных чатов.
- Native IDE: настройки через форму → failing missing-import check → receipt в модель → исправление → passing тот же check_id; command approval не обходится.
- Native IDE: checks_only без модели и без HTTP, сохранение draft запроса, изоляция/восстановление options, invalid config без старта.
- Core: отказ команды без автоматического replay, stale witness после external edit, partial scope и ручной критерий.
- Build, полные unit/migration, документация, реальные 240/320/420 px и темы.

Установка на чистой Windows, remote CI и расширенная статистика реальной LLM остаются отдельными gates. Новый этап проверяет wiring UI и Core на детерминированном HTTP fixture; старые модельные результаты не переписываются.

## Результат 3 ноября 2026

Реализованы отдельный editor проверок и критериев, запуск checks_only без модели, per-chat drafts и отображение актуальности evidence. Ask/Plan не получают команд, включая resume сохранённой Agent-задачи. Повреждённый draft отбрасывается; Windows LSP paths нормализуются; cwd сохраняет значимые пробелы.

Native и строгий JSON fixtures прошли один сценарий восстановления импорта каждый: реальный Node завершился с exit 1, receipt дошёл до модели, исправление дало exit 0 с прежним check_id. На протокол — 6 HTTP-запросов и 5 подтверждений в repair-сценарии. Отдельно проверены отказ команды, отсутствие модели/HTTP при checks_only, сохранность несохранённого запроса, смена чатов, invalid input, stale evidence после внешней правки и непроверенный ручной критерий. Это проверка интеграции, а не новое измерение качества Ornith/Qwen.

| Проверка | Результат |
|---|---|
| Node regressions | 27 passed, включая 9 codec cases; граничные случаи проверены RED → GREEN |
| Python unit | 496 OK, 3 skips |
| Core/migration | 129 OK |
| Production build | PASS |
| Native IDE regression и UI matrix | PASS: 240/320/420 px, forest/parchment/twilight и существующий zoom 200%; скриншоты формы и evidence просмотрены |
| Независимый review | Важных P1/P2 замечаний нет |
| Packaged smoke и embedded IDE | PASS: запуск/перезапуск, migration, approval/write/Undo, настроенная проверка через bundled Node при stripped PATH |

Кандидат: `artifacts/windows-20261103-acceptance/LESHY-7.0.1-setup-x64.exe`. Manifest с SHA-256 и результатами: `artifacts/acceptance-20261103/release.json`; логи — в той же папке. Frozen Core переиспользован после сверки 101 исходного файла agent/core с manifest исходной сборки: изменений нет. Установщик не подписан; установка/обновление на чистой Windows и remote CI — UNVERIFIED. Публикация не выполнялась.

Следующий ограниченный этап по [quality baseline](83-agent-quality-baseline.md) — JSON recovery после повторных пустых поисков с внешней проверкой конечного diff.
