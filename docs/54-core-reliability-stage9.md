# Этап 9: надёжность после повторного аудита

Реализация первого этапа [основного плана аудита](49-post-stage8-audit-and-next-plan.md).
Пункты A1–A5 исправляются до подключения новых субагентов. Дизайн Neutral, настольная
Лола и единый голосовой контур сохраняются. Этапы 10–14 остаются следующими шагами.

## A1: JSON не извлекается из неоднозначного ответа

`strict_json_loads` потребляет весь документ и отклоняет повторные ключи на любом
уровне, NaN и Infinity. `decode_envelope` требует anchored object. После объекта
нельзя дописать пояснение, второй объект или фрагмент другого ответа. Текст
«пример: {…}» не считается командой. Ошибка parser не доходит до ToolExecutor.

Старые полные `tool_calls`, single-tool envelopes и явно ограниченные wrappers
`<tool_call>`/fenced JSON сохранены для совместимости существующих профилей. Парсер
также принимает versioned `neutral.action.v1` tool/final. Запросы старых профилей
пока используют прежний prompt: миграция, presets и bounded repair относятся к
[этапу 10](51-text-tool-agency-plan.md). Это не скрытая смена настроек пользователя.
Аргументы native calls проходят тот же strict JSON decoder перед schema validation.

## A2: явное завершение ответа

`ModelResponseOutcome` — общий immutable контракт:

| status | Что подтверждено |
| --- | --- |
| complete | Получена явная terminal reason stop/tool_calls/function_call. |
| incomplete | EOF без terminal reason, неизвестная reason или length. |
| refused | Refusal/content filter. |
| cancelled | Отмена/срок текущей операции. |
| error | Ошибка получения/обработки ответа. |

Окончание итератора и SSE `[DONE]` сами по себе не синтезируют `stop`. В JSON adapter
сначала проверяется outcome, только затем разбираются calls. Native engine также
проверяет outcome до подготовки journal batch, approval и effects. Частичный текст
сохраняется, незавершённые calls не попадают в canonical tool history, задача paused.
UI показывает причину и позволяет продолжить обычным механизмом resume.

В checkpoint записывается `response_outcome`; дополнительный non-stream запрос
получает `aux_response_outcome`. Неоднозначный дополнительный ответ не обновляет
память. Responses adapter сохраняет статус non-stream ответа, вместо безусловного
`stop`. Дополнительная модельная проверка завершения остаётся необязательной и не
заменяет deterministic evidence команд.

## A3: content revision вместо одного счётчика

`WorkspaceRevisionService.capture` строит digest отсортированного manifest дерева:
относительный путь, hash содержимого файла, наличие каталогов и сами ссылки.
Ссылки/junction не обходятся. Исходники не сохраняются в manifest. До/после чтения
проверяется identity файла. Совпадения size/mtime недостаточно: same-size запись
с восстановленным mtime обнаруживается по содержимому.

Текущий scope `source-tree-v1` исключает `.git`, зависимости, caches, dist/build,
artifacts, `.test-data` и coverage. Лимиты: 10000 entries, 96 МБ суммарного чтения,
8 МБ на файл, 2 секунды. Если весь scope не прочитан, revision имеет complete=false
и не подтверждает проверки. Это явная ограниченная область, а не обещание проверки
каждого файла компьютера. Настраиваемые manifests/инкрементальный watcher — дальнейшее
развитие; большой проект может потребовать повторной проверки или изменения scope.

ToolExecutor фиксирует revision **после approval, перед запуском команды**.
Command receipt сохраняет её вместе с rollback generation. Если команда меняет
исходники в процессе, её старый fingerprint уже не подтверждает финальное состояние.
Затем StageVerifier сравнивает receipt с новым hash: commands_passed разрешён только
при полном совпадении. Старые receipts без hash становятся stale, автоматически к
новой версии не привязываются. Сохранённая ошибка остаётся ошибкой до успешного
повтора именно этой команды; посторонний успешный запуск её не отменяет.

Ручная запись EditorService вызывает `TaskService.workspace_changed`: пересчёт,
сохранение checkpoint и `workspace_evidence` для выбранного idle-чата. Это отдельное
UI-событие: обычные run events после task_end намеренно игнорируются. Внешние правки
обнаруживаются при следующей проверке/recovery/открытии, непрерывного watcher пока нет.
stale/incomplete evidence не переопределяется итоговой фразой модели «всё готово».

## A4: поздняя LSP диагностика

После initialize клиент проверяет `diagnosticProvider`. Если он объявлен, запрашивает
`textDocument/diagnostic` и ждёт полный report для открытого файла. `unchanged` без
предыдущего result ID не считается полным результатом; MethodNotFound переключает
клиент на push. Формат сверялся с [определениями протокола Microsoft](https://raw.githubusercontent.com/microsoft/vscode-languageserver-node/main/protocol/src/common/protocol.diagnostic.ts).

В push режиме первый пустой список не завершает процесс. Списки правильного URI/
version заменяют предыдущие; клиент наблюдает минимум 1,25 с и ждёт 0,75 с тишины,
оставаясь в deadline/cancellation операции. Push не предоставляет универсального
признака окончания всех анализаторов, поэтому UI получает соответствующее notice
и complete=false. Позднее сообщение за пределами окна возможно; отчёт не объявляется
доказательством чистоты всего проекта. Pull относится к ответу сервера об одном файле.

Malformed diagnostics отвергаются вместо преобразования в чистый пустой список.
Изменение файла проверяется также hash содержимого. Readonly запрет applyEdit/
executeCommand и завершение дочернего процесса сохраняются.

## A5: единый автоматический доступ

`WorkspaceAccessPolicy` применяется к read_file/read_range, list/search/glob,
исследователю, AGENTS.md и файловым mutations до preview/approval. Обычные `.env`,
приватные ключи, credential directories и дополнительные `.neutralignore` пути
закрыты по умолчанию; `.env.example/.sample/.template` доступны как примеры.
Каноническая цель проверяется также для aliases. Ручной EditorService не использует
автоматическое ограничение: пользователь может самостоятельно просматривать файлы.

`.neutralignore`: UTF-8 до 16 КБ, до 128 glob-правил, комментарии `#`, маски путей/
имён и папок. Это не полный gitignore parser; `!` не поддерживается. Модель не может
редактировать этот файл через file tools. Ошибка policy/config не открывает доступ.

В **IDE → Возможности IDE → Доступ модели к файлам проекта** можно указать до 64
существующих файлов относительно проекта и явно подтвердить передачу их содержимого
серверу модели. Папки, wildcard grants и пути вне root отклоняются. Пустой список
отзывает исключения. Разрешения хранятся вне проекта в profile/workspace-access.json;
модель не получает IPC для изменения grants. Настройки не входят в переносимый backup,
при восстановлении доступ нужно подтвердить заново.

Сам файл разрешений запрещён для model read/write и выдачи исключений, даже когда
профиль оказался внутри выбранного проекта. Canonical target .neutralignore защищён
от изменения также через alias. File policy повторно проверяется непосредственно
перед записью после approval: внешнее изменение правил во время просмотра diff
может отклонить ещё не выполненный эффект.

Перед каждым model request и ContextManager projection повторно проверяется известная
provenance файловых tool results. После отзыва они и связанные read_tool_result копии
заменяются ACCESS_REVOKED; каноническая история остаётся пользователю. Сам reader
артефактов также использует эту projection. Произвольный текст старых ответов модели,
ручной prompt и уже отправленные данные не являются семантически редактируемым
источником: отзыв не удаляет данные у провайдера. Для исключения ранее написанного
текста из контекста нужно начать новый чат.

Это host policy файловых адаптеров, не OS sandbox. Отдельно разрешённая команда или
произвольный внешний MCP server исполняет собственный код; regex по произвольным
arguments не даёт гарантии файловой изоляции. Для них сохраняются explicit approval,
scope UI и отдельный план изоляции. Политика не объявляется защитой любого внешнего ПО.

## Фоновые операции истории

Storage backup/status из настоящего JSON-lines main запускаются BackgroundJob, а не
под длительным tasks.lock. Один worker отклоняет дубликаты и имеет OperationContext.
Во время копирования Core отвечает health/cancel/голосовым командам. UI настроек истории
показывает кнопку отмены, а RPC timeout также посылает storage_cancel.

Backup проверяет отмену между SQLite pages, файлами и ZIP chunks по 64 КБ, при проверке
ZIP и перед atomic replace. Существующий архив не заменяется частичной копией. Отмена
кооперативная: отдельная системная дисковая операция не прерывается мгновенно. Проверка
report/SQLite может завершиться позже запроса отмены, но не блокирует bridge thread.
При выходе admission закрывается и worker ограниченно ожидается.

## Модули и проверки

Новые границы: [response_outcome.py](../agent/response_outcome.py),
[workspace_revision.py](../agent/workspace_revision.py),
[workspace_access.py](../agent/workspace_access.py),
[background_job.py](../core/python/background_job.py),
[WorkspaceAccessSettings.tsx](../apps/desktop/src/WorkspaceAccessSettings.tsx).
Именованные функции/классы включены в генерируемый справочник.

[Регрессии этапа](../tests/test_stage9_reliability.py) используют временные файлы,
настоящий EditorService, LSP subprocess и отдельный Core process. HTTP fixtures нормальных
ответов теперь отправляют terminal reason; отсутствующий terminal reason проверяется
отдельно как ошибка, а не используется как неверная норма в остальных сценариях.
До следующего изменения лимитов: 336 unit-тестов OK (один Windows symlink skip),
80 HTTP/Core тестов OK, typecheck/build и четыре Electron smoke OK; audit probes
подтвердили исправления A1–A5. Логи: `.test-data/stage9-{unit-final,http,build}.log`
и `.test-data/stage9-audit-probes.json`. Core freeze этого состояния прошёл,
но после изменений [главы 55](55-automatic-context-and-lola-layout.md) он устарел.
Пользователь остановил подготовку установщика: installer не собирается.
