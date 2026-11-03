# Этап 13a: индекс сохранённых исходников проекта

27 октября 2026. Продолжение [Roadmap V2](57-roadmap-v2.md) после
[контракта evidence](60-scoped-verification-evidence.md). Реализован Project
Intelligence MVP для Python/JavaScript/TypeScript. ContextPack 14a, embeddings,
субагенты и семантическое разрешение references этой поставкой не добавляются.
Установщик не собирается.

## Пользовательский путь

При выборе папки или проекта Core запускает индексирование в фоне. Откройте
«Поиск по проекту»: здесь видны создание/обновление/готовность индекса, необходимость
пересборки и работа без индекса. Можно остановить индексацию и явно пересобрать кеш.
Режимы поиска — текст и определения символов; Ctrl+P использует поиск файлов.
Результат открывает сохранённый файл на найденной строке. Дизайн приложения сохранён.

Во время фонового обновления доступные результаты повторно проверяются по хешу
и помечаются частичными. Если кеш недоступен, обычный ограниченный поиск и read_range
сохраняются. Отмена индексации не отменяет агентскую задачу, не удаляет исходники
и не запускает модель. Запуск/состояние индекса не требуют новых ручных лимитов LLM.

Индекс включает доступные UTF-8 текстовые файлы до 1 МБ, исключает бинарные,
чувствительные пути, symlinks/junction, существующие generated/dependency exclusions,
`.neutralignore` и правила `.gitignore`, включая вложенные. Большие файлы можно
читать прежним read_range; отсутствие файла в индексе не доказывает его отсутствия
на диске. Несохранённый буфер не индексируется, dirty guard редактора сохранён.

## Архитектура и файлы

| Компонент | Назначение |
| --- | --- |
| [project_index.py](../agent/project_index.py) | Отдельный SQLite/WAL cache, OS owner lock, observer, durable queue, один updater и проверенный retrieval |
| [project_index_policy.py](../agent/project_index_policy.py) | Снимок WorkspaceAccessPolicy и ancestor .gitignore на одну операцию, GitWildMatch и policy hash |
| [project_symbols.py](../agent/project_symbols.py) | Python AST и Tree-sitter JS/JSX/TS/TSX: определения, классы, методы, imports/exports, точные диапазоны |
| [workspace_search.py](../agent/workspace_search.py) | Общая точка поиска: активный индекс → прежний bounded walk при отказе |
| [tools.py](../agent/tools.py) | search_files, search_symbols, project_outline; прежний search_text прозрачно использует индекс |
| [project_search.py](../core/python/project_search.py) | Отменяемый worker поиска Desktop без блокировки JSON-lines dispatch |
| [bridge.py](../core/python/bridge.py) | Выбор/закрытие проекта, узкий status/rebuild/cancel API; немедленная инвалидация после UI revoke |
| [ProjectSearch.tsx](../apps/desktop/src/ProjectSearch.tsx) | Выбор вида поиска, состояние индекса, stop/rebuild и защита от устаревших ответов |
| [benchmark_project_index.py](../tools/benchmark_project_index.py) | Независимые synthetic корпуса, frozen sources, latency/Recall/update/CPU/RAM/cache report |

Кеш расположен в профиле: `cache/project-index/<canonical-workspace-hash>/index.sqlite3`.
Он не входит в chat SQLite и не является источником истины. В нём находятся:

- `files`: путь, hash исходных байтов, UTF-8 текст и casefold-проекция, policy hash,
  parser status и file revision;
- `symbols`: имя/kind и source range, индексы имени и пути;
- `text_fts`: FTS5 trigram для буквальных подстрок; при отсутствии FTS5 используется
  SQLite text lookup, короткие запросы также идут без FTS;
- `pending`: точный путь и token последнего события; несколько изменений coalesce;
- `meta`: revision кеша. Версия cache schema — 1.

Соединения короткие, WAL; source parsing выполняется до небольшого write batch.
Неизменившиеся SHA/policy/parser не перезаписываются. Owner lock освобождается ОС
при завершении процесса и предотвращает конкурирующие пересборки двух Core.
Падение кеша не отменяет уже разрешённую запись и не повторяет её. Повреждённый кеш
не сбрасывается молча: обычный поиск остаётся, явная пересборка сохраняет broken
DB/WAL/SHM рядом и создаёт новый derived cache. Chat history/journal не меняются.

## Инкрементальность

Observer запускается до initial scan. После подтверждения подписки выполняется
первичный обход; события периода обхода остаются в durable queue. Updater обрабатывает
точные пути, затем потребляет только соответствующие tokens. Если во время обработки
пришло новое событие того же пути, оно не теряется.

События приходят из успешного atomic write редактора/tools, mutations, user rollback
и watchfiles. Внешние edit/rename/delete не требуют полного сканирования дерева.
При directory event выполняется ограниченная сверка соответствующего поддерева;
при delete удаляются также старые записи descendants. Команды запускаются прежним
ToolExecutor с approval; после исполнения планируется bounded reconciliation cwd.
Evidence scope команды не считается ограничением её файлового доступа.

Индексирование после offline/перезапуска требует контролируемого background rescan:
observer не может подтвердить изменения за время отсутствия процесса. После overflow,
ошибки наблюдения, отмены, повреждения или смены правил появляется `needs_rebuild`
либо `degraded`, без заявления о полной актуальности. Автоматического бесконечного
rescan нет. Изменение правил прерывает прежний scan и инвалидирует derived content;
при retrieval новое разрешение проверяется даже без filesystem event, например
при изменении file grants во внешнем profile JSON.

Границы ресурсов кеша: до 100000 entries первичного обхода, 256 МБ текста, 20000
pending paths, 10000 событий в одной watcher batch. Overflow переводит кеш в recovery,
а не молча теряет изменения. Первичный scan не имеет общего 120-секундного таймера:
при живом прогрессе он продолжает работу до готовности или Stop/capacity/error.
Проверка отмены выполняется между файлами и в обновлении batch. Это не новые
глобальные лимиты локальной модели.

Directory/command reconciliation ограничена 2000 entries и двумя секундами. Если
область больше, требуется явная пересборка, доступен обычный поиск. Поэтому команда
в корне очень большого проекта может перевести индекс в recovery; улучшение
command-aware reconciliation остаётся дальнейшей оптимизацией. Первоначальный
обход большого дерева также может занимать минуты; UI при этом остаётся доступен.

## Точность и provenance

Каждый выданный indexed hit содержит canonical workspace id, относительный path,
SHA-256 файла, file/index revision, policy version, source_kind=`saved-file`,
freshness=`hash-verified`. Для символов дополнительно идут kind, start/end line и
UTF-8 byte columns парсера. Нумерация строк начинается с 1. При BOM columns относятся
к декодированному source без BOM; это не byte offsets исходного файла.

Кандидаты читаются в одном SQLite read snapshot. Перед выдачей источник снова
читается и сравнивается с сохранённым hash; новый экземпляр policy проверяет доступ
и .gitignore. Изменившийся/запрещённый источник не выдаётся как прежний. История
результатов новых tools также проходит существующий filter_model_history при
следующей передаче модели. Это не предоставляет новых прав за пределами проекта.

Retrieval ограничен 2001 metadata candidates, 200 результатами, 8 МБ проверенных
исходников и тремя секундами. SQL не выгружает полные тексты всех candidates в RAM.
При ограничении, обновлении или неполном разборе выдача помечается `truncated` с
причиной. Ошибка/отсутствие parser не блокирует текстовый поиск. Синтаксические
определения не называются semantic references: для мест использования пока нужен
прежний literal search и проверка конкретных строк. Специальный semantic find_references
и транзитивные зависимости не реализованы.

Хеш подтверждает содержимое в момент чтения, не блокирует filesystem. Observer
eventual: индекс не является полным синхронным снимком дерева и не используется
как замена WorkspaceRevision/evidence. При silent потере OS events новые имена могут
отсутствовать до контролируемой пересборки; положительные кандидаты всё равно
проверяются по текущим байтам. Детектируются surfaced watcher errors, oversized
batches/queue, stale candidate и известные разрывы lifecycle, но универсальное
доказательство отсутствия потерянных OS events не заявляется.

## Проверки и измерения

[Unit](../tests/test_project_index.py) проверяют AST/Tree-sitter ranges, Unicode и
регистр, FTS fallback, настоящий watcher, editor save/rename/delete без rescan,
backdated bytes, nested ignore, revoke, corruption, offline recovery, overflow,
отмену в широкой папке и Windows read-sharing race. Symlink test пропускается там,
где ОС не разрешает создать тестовую ссылку.

[Реальный Core](../tests/migration/test_bridge_process.py) проверяет index API,
внешний edit, отсутствие full scan и fallback после cancel.
[Electron](../tests/electron/neutral-smoke.cjs) проверяет выбор «Определения символов»,
переход нового имени после внешнего изменения и отсутствие model requests.
Снимки `project-index-symbols.png` и `project-index-updated.png` просмотрены;
из-за отставания paint скрытого окна capture выполняется в два прохода.

Корпуса совпадают по генератору с [20a](58-agent-baseline-20a.md): 40/1200/12000
filler файлов и известные definition/caller. До измерения поставлены цели p95 <500 мс,
Recall@10=1, update <2 с и отсутствие rescan на обычный edit. Это цели данной машины,
не универсальные обещания. Один cold build на размер, 21 warm query; CPU/RAM —
метрики целого Python-процесса, peak — за всё время его жизни.

Окончательный последовательный прогон на актуальных исходниках:

| Filler | Initial build, с | Search p50 / p95, мс | Recall@10 | Внешний edit, мс | Без rescan |
| ---: | ---: | ---: | ---: | ---: | --- |
| 40 | 0,775 | 18,454 / 20,031 | 1 | 68,367 | да |
| 1200 | 24,945 | 32,773 / 86,369 | 1 | 92,262 | да |
| 12000 | 274,378 | 29,553 / 37,705 | 1 | 124,019 | да |

У большого корпуса cache около 15,7 MiB, process working set около 55,3 MiB,
lifetime peak около 56,9 MiB, build CPU 79,641 с. Первичный проход занял около
4,6 минуты; это фоновые чтение/разбор и обработка накопившихся событий. До индекса большой literal scan
исчерпывал около 3 с и имел Recall@10=0 на том же generator. Это сравнение retrieval,
а не доказательство качества решения задачи моделью. LLM baseline 2/15 из главы 59
этой поставкой заново не измерен и не объявляется исправленным.

Финальный unit suite: **400 тестов OK, два Windows skip**. HTTP/Core: **83 OK**.
При одном прогоне прежний TTS disconnect test получил WinError 10053; отдельные
три TTS-теста и последующий полный HTTP suite прошли. TTS implementation не менялась.
Renderer/main/preload build и Neutral Electron smoke прошли; после исправлений
регистра, состояния WAL и отмены связанные unit/HTTP проверки выполнены повторно.

v1 остановился на ошибке Windows HANDLE метрики памяти, v2/v4 выявили слишком общий
120-секундный предел initial scan. Ранний v3 прошёл при более лёгкой нагрузке
(p95 большого корпуса 14,109 мс, build 113,072 с); он не подменяет финальные числа.
Журналы и частичные отчёты сохранены. Окончательный прогон выполнялся последовательно
после unit/HTTP, без параллельной тестовой нагрузки:

- `.test-data/project-index-13a-accepted/report.json` — все метрики и source hashes;
- `.test-data/project-index-13a-accepted/report.md` — компактная таблица;
- `.test-data/project-index-13a-accepted/baseline-sources.zip` — точные Agent/Core/
  requirements и benchmark sources; hashes сверены с текущими файлами;
- `.test-data/index-unit-accepted.log`, `index-http-confirmed.log`,
  `index-electron-visual.log`, `index-build-releasecheck.log` — проверки.

Пороги retrieval/update на synthetic корпусах достигнуты. Это измерительный gate
13a с описанными пределами, не доказательство качества произвольной coding-задачи.
Документация и `git diff --check` проверены. Ветка `codex/electron-agent-bridge`,
HEAD `9572082e8f0c4ce625e515fdb7e5c0ac466a8b09`: изменения локальные, commit/push,
merge/release и установка поверх приложения не выполнялись; предыдущая рабочая
копия и пользовательский docs.zip сохранены. Модели LM Studio не переключались.

Первичные источники выбранных API: [watchfiles watch](https://watchfiles.helpmanual.io/api/watch/),
[py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter),
[TypeScript grammar](https://pypi.org/project/tree-sitter-typescript/0.23.2/).
Версии зафиксированы в requirements-core.txt и установлены в `.venv`/`.venv-test`.
Проверка packaged installer этой поставкой не выполнялась.

Следующий этап — 14a: ContextPack с выбором конкретных диапазонов, deduplication,
provenance и единственным финальным gate RequestBudget.fit.
