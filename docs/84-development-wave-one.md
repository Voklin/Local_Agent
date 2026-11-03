# Выполнение плана: проверки, документация и пакет LESHY

3 ноября 2026. Основа — [аудит](81-project-audit-2026-11-03.md) и [план развития](superpowers/plans/2026-11-03-project-development.md).

## Реализовано

1. Launcher Electron возвращает nonzero при сигнале и отсутствующем коде завершения. Пять Node VM-тестов включают успешный/ошибочный exit и spawn error; ошибочные случаи наблюдались до исправления.
2. Обновлены аннотации новых IDE/LESHY-файлов и перемещённых API. Сторонний bundled CLI остаётся в file map, но не перечисляется как наш API. Отдельный Python-тест проверяет inventory, AST inputs и оглавление; отключение исключения воспроизводит ошибку теста.
3. Пересозданы шесть справочников, обновлены README, текущий статус и historical roadmap. Существующие материалы сохранили назначение исторических глав.
4. Добавлен отдельный `windows-ide` job: закреплённый runtime, native IDE, background isolation, темы, optional полная visual matrix и сохранение evidence. GUI fixtures принимают `LCA_TEST_PYTHON`; локальный `.venv-test` не обязателен в CI.
5. Старый объединённый PowerShell-step разделён: ошибка neutral-smoke больше не маскируется последующим успешным layout. Старый шаблон отдельно воспроизведён: последовательность exit 7, затем exit 0 возвращала 0.
6. Package smoke выбирает executable из конфигурации или точного переданного пути. Старый `Neutral.exe` не заменяет отсутствующий LESHY. Добавлен packaged IDE acceptance через общий frozen Core, подтверждение diff, запись и Undo/Save.
7. Собраны frozen Core и свежий NSIS в отдельный output. Результаты и открытые release gates — [приёмка пакета](82-leshy-release-acceptance.md).

## Проверки текущего этапа

| Проверка | Результат |
|---|---|
| Production build / TypeScript | PASS |
| Launcher tests | 5/5 |
| Package path tests | 4/4 |
| Reference inventory regression | 1/1 |
| Docs generate/check | PASS, 6 справочников; окончательные количества ссылок — в `docs-check.log` |
| Native IDE integration | PASS, 6 fixture HTTP requests |
| Background chats | PASS, 1 fixture request |
| LESHY themes | PASS, 0 inference requests |
| Frozen Core subprocess tests | 17/17 |
| Fresh package, restart и embedded IDE | PASS |
| YAML parsing и раздельные GUI steps | PASS локальной структурной проверки |

Логи: `artifacts/development-2026-11-03/`. Полные 494 unit / 129 migration из аудита — предыдущий baseline, их не следует называть новым прогоном после этих изменений.

## Решения и ограничения

Работа велась в существующей feature-ветке с большим незакоммиченным implementation: новый worktree от HEAD потерял бы аудируемое состояние. Файлы не добавлялись в индекс, пользовательские изменения не откатывались. Для дальнейшей интеграции требуется явный отбор файлов и фиксация одной ревизии.

Журнал выполнения сохранён в игнорируемом `artifacts/development-2026-11-03/progress.md` вместо Bash helpers: окружение этого запуска — PowerShell. Автоматического диапазона коммитов review нет.

Независимый reviewer успел подтвердить маскирование GUI failure в CI; замечание воспроизведено и исправлено. Полный независимый review не завершился из-за лимита модели reviewer. Дополнительно проведён собственный просмотр изменённых контрактов и результатов проверок; это не заменяет законченный независимый review перед merge.

Задача 1 завершена локально. Для закрытия задачи 2 нужен успешный remote Windows job на выбранном commit; задача 3 имеет успешную локальную сборку и packaged acceptance, но clean-machine install/upgrade/uninstall остаются UNVERIFIED. Задачи 4–6 ещё не реализованы.
