# Измеренный baseline агента — 3 ноября 2026

## Условия и область выводов

По выбору пользователя native выполнялся на **Ornith 1.5 9B Q5_K_M**, JSON — на **Qwen 2.5 Coder 7B Instruct Q5_K_M**. Это сравнение двух связок «модель + протокол», не причинная оценка влияния протокола. Одновременно загружался только один тестовый экземпляр. Все экземпляры, созданные аудитом, после измерений выгружены; другие модели не выгружались.

Основной эксперимент: по три повтора bugfix и multifile на одинаковом synthetic small fixture (40 filler-файлов). Окно 8192, manual budget, максимум ответа 1536, reserve 256, temperature 0, seed 0, не более 10 циклов и 3 минут на эксперимент, request timeout 90 s. Это ограничения benchmark, не новый лимит local auto в приложении. ContextPack и индексный режим в этих опытах выключены одинаково для обеих связок.

Проверка результата — held-out AST oracle и разрешённые пути diff. Oracle не импортирует произвольный сгенерированный код. Отдельно записаны корректность кода и успешное завершение агента. Маленькая выборка не даёт статистики надёжности произвольных проектов.

Шесть основных прогонов имеют один source digest: `a1be3330cb3f67f70e4c4eceec8872312946ec577abe6822dfc892ce72a3ae95`. В каждой папке `artifacts/quality-20261103/*` сохранены report.json и baseline-sources.zip. Отчёт содержит commit, хеши, loaded model metadata, context, usage, receipts и transcript. Рабочее дерево незакоммичено.

## Основной manual baseline

| Связка | Задача | Oracle + diff | E2E | Медиана времени, s | POST всего | Вход / выход всего |
|---|---|---:|---:|---:|---:|---:|
| Ornith / native | bugfix | 3/3 | 3/3 | 12.966 | 20 | 58399 / 3133 |
| Ornith / native | multifile | 1/3 | 0/3 | 30.078 | 23 | 79233 / 6927 |
| Qwen 2.5 / JSON | bugfix | 0/3 | 0/3 | 4.874 | 17 | 43339 / 723 |
| Qwen 2.5 / JSON | multifile | 0/3 | 0/3 | 2.777 | 9 | 25647 / 489 |

Меньшее время не означает лучший результат: остановка на budget gate может быть быстрой. Token counts — суммы provider-reported usage по физическим запросам, не оценка уникального контекста.

Ornith исправила простой баг во всех трёх повторах. Для multifile один diff прошёл oracle, но агент остановился на лимите 10 циклов; другой повтор на этом лимите оставил неверный результат, третий остановился на RequestBudget. Ни один multifile не прошёл E2E.

Все шесть JSON manual-задач остановились на RequestBudget. Ни одна не прошла oracle; JSON repair во всех этих опытах — 0. Guard не отправлял запрос, превышающий его оценку окна. Эти результаты не доказывают дефект JSON parser или превосходство native на одной и той же модели.

## Диагностический follow-up auto

После наблюдения бюджетных остановок добавлен явный флаг `tools/benchmark_agent.py --budget-mode auto`; manual остаётся default. Проведён один дополнительный повтор двух задач на той же Qwen и том же окне 8192, без ContextPack. Изменился только экспериментальный выбор уже существующей политики бюджета; permission, parser и RequestBudget не ослаблялись. Это отдельный опыт, а не четвёртый повтор manual серии.

| Задача | Oracle + diff | E2E | Статус | Время, s | POST |
|---|---|---|---|---:|---:|
| bugfix | FAIL | FAIL | paused | 7.877 | 6 |
| multifile | FAIL | FAIL | completed | 4.210 | 4 |

В auto budget-остановка исчезла, но качество не стало достаточным. Bugfix повторял поиск `tax_total =`, не находил функцию и был остановлен ProgressGuard. В multifile модель изменила определение и вызов, оставила старый import и объявила успех; внешний oracle отклонил результат. В benchmark отсутствуют настроенные runtime acceptance commands: состояние completed здесь не означает verified.

## Наблюдения ресурсов

Счётчики записывались раз в секунду в `artifacts/development-2026-11-03/quality-resources.jsonl`. Монитор начат после загрузки Ornith и не покрывает начало её первого опыта. GPU — весь device с desktop/browser; RAM — сумма Windows WorkingSet64 процессов LM Studio и llama-server, где shared pages могут учитываться несколько раз. Это наблюдаемые максимумы, не изолированный абсолютный пик памяти модели.

| Связка | Samples | GPU max, MiB | Сумма working sets max, GiB |
|---|---:|---:|---:|
| Ornith/native | 109 | 11478 | 8.31 |
| Qwen/JSON manual | 29 | 9063 | 6.72 |
| Qwen/JSON auto | 12 | 9059 | 6.68 |

Изолированные CPU/RAM peaks и время до первого полезного результата — **UNVERIFIED**. wall_seconds включает обвязку эксперимента. Из этих измерений нельзя делать вывод о GPU throughput или требованиях к любому ПК.

## Детерминированная оркестрация и следующий этап

Текущие Core/migration-тесты покрывают long history, отклонённые действия, отмену approval, разрыв SSE и kill/restart без повторения эффекта. tests/test_scoped_verification.py и tests/test_ide_verification.py проверяют external edit, stale evidence и прерванный rollback. Эти сценарии выполнены с fixtures, а не повторены на реальной модели.

Следующий приоритет — дать новой IDE настройку явных acceptance checks и показывать незакрытые требования рядом с завершённым ответом. Использовать существующие task_options/check_id/StageVerifier и source witnesses. Код, пропустивший import, должен приводить к реальному failing check и bounded recovery; выполненная команда на устаревшей ревизии не должна подтверждать результат. JSON search recovery после повторных пустых результатов — следующий отдельный измеримый сценарий.

Gate следующего этапа: воспроизвести missing-import на неизменяемом fixture → получить реальный nonzero check → дать агенту receipt → либо исправить import и пройти тот же oracle, либо явно остановиться с непроверенным результатом. Для live native и JSON использовать закреплённые здесь модели; расширять выборку после получения нового результата. Embeddings, новый scheduler или новый parser этим опытом не обоснованы.

Открыто: реальные длинные задачи/отказы/разрывы/external edits/restarts, повтор auto серии, TTFT/first-useful measurement, чистая Windows и remote CI. [Выполнение UI/recovery](85-recovery-and-session-state.md).
