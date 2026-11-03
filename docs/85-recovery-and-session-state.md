# Восстановление и состояние новой IDE-панели

3 ноября 2026. Выполнение задач 4–5 [плана развития](superpowers/plans/2026-11-03-project-development.md).

## Что изменилось

Карточки неизвестного эффекта, нечитаемого журнала и неизвестного rollback показаны перед журналом этапов. Продолжение остаётся заблокированным. Для каждого состояния дан следующий шаг: проверить фактические файлы/сервис, получить диагностику, сохранить копию профиля, открыть снимки в главном окне. Автоматического исправления журнала и повторного запуска неизвестного действия нет.

Кнопка «Скопировать диагностику» строит минимальный JSON по allowlist: schema, проверенные hex-идентификаторы, счётчики, индекс сообщения и recovery flags. Ключи, содержимое файлов, пути, сообщения, конфигурация модели и error narrative не экспортируются. Копирование проходит через фиксированный host channel; произвольные команды из webview не добавлены. В GUI-тесте проверены сборка отчёта, передача host-методу и видимый результат; OS clipboard adapter не проверялся чтением обратно, чтобы не менять пользовательский clipboard автоматическим тестом.

Подтверждение наблюдения теперь ожидает результат Core. При ошибке выбор остаётся на экране и показывает, что наблюдение не сохранено. В Core по-прежнему передаются точные chat_id, journal_id, message_index и call_id. Нечитаемый journal и неизвестный rollback не разблокируются этими кнопками.

Состояние событий вынесено в `sessionState.ts`: точный chat/run, event_seq, замена stream каноническим сообщением и завершение run. Соседние text_delta используют синхронный transcript ref, чтобы не потерять части ответа между React render. События другого/закрытого run, повторы и невалидные sequence отбрасываются. run_id назначается до startTask, поэтому ранний ответ принимается.

Для task, approval, подключения и истории удалён локальный `any`; используются общие task/protocol-типы и GenerationSettings. Форма вынесена в самостоятельный `connectionSettings.tsx`, в ней сохранены темы LESHY и разделение editable/saved config. Добавлена подсказка: текущий план — в «Работе», подробный editor пока отсутствует, правила — AGENTS.md, MCP/навыки — главное окно.

## Замечания review и исправления

1. Во время задержанного сохранения поля подключения оставались редактируемыми, а поздний ответ стирал новый ввод. GUI regression сначала воспроизвела ошибку; disabled fieldset теперь закрывает редактирование до ответа. При отказе сохранения исходный editable draft остаётся.
2. Удалённое из формы пустое поле api_key снова появлялось как пустая строка в main IPC и очищало текущий ключ. Regression на реальной AST-функции modelConfig сначала падала; main теперь сохраняет различие omitted и explicit empty. Для другого endpoint Core по-прежнему отбрасывает прежний ключ через connection_key.

Независимый review не обнаружил важных проблем изоляции событий, blockers и allowlist diagnostics; риск черновика подтверждён и исправлен. Контракт ключа дополнительно проверен по исходникам Core и IPC regression. После исправлений выполнены covering tests и native GUI; повторный независимый review не проводился.

## Проверки

| Проверка | Текущий результат |
|---|---|
| Чистые функции состояния + main key projection | 9 Node-тестов PASS |
| TypeScript/Vite/Electron | PASS |
| Python unit suite | 496 тестов, OK, 3 skips |
| Core/migration suite | 129 тестов, OK |
| Benchmark regression suite | 10 тестов PASS |
| Native IDE | PASS, 6 fixture requests; diff/write/Undo, настройки, черновик, keyboard focus trap, recovery rejection и диагностический JSON |
| Ширина и темы | 240/320/420 px × 3 темы × 4 страницы + approval; отдельно CSS zoom 200%, PASS |
| Документация | Полная проверка и пересоздание справочников; итоговые количества в `panel-final-docs.log` |

Снимки `recovery-blockers.png`, `recovery-diagnostics.png`, компактные настройки и zoom 200% просмотрены. Recovery UI fixture подменяет только результат loadChat; подтверждение несуществующего journal проверяет реальный Core и получает отказ. Нельзя считать это фактическим повреждением пользовательского профиля.

Существующие тесты не дублировались: test_unknown_effect_blocks_new_prompt_resume_and_fork_until_review; kill/restart и отмена approval в test_run_owner_restart.py; partial rollback без replay в test_ide_verification.py; corrupt journal в test_call_journal.py. Они вошли в текущие полные suites.

## Качество модели и поставка

По выбору пользователя измерены Ornith/native и Qwen 2.5 Coder/JSON; результаты, ограничение manual 8192 и отдельный auto follow-up — [baseline](83-agent-quality-baseline.md). Модельный ответ «выполнено» не заменяет passing oracle или configured acceptance check.

Первый installer из [приёмки этапа 1](82-leshy-release-acceptance.md) не включает эти последующие изменения панели. Актуальный кандидат `artifacts/windows-20261103-recovery/LESHY-7.0.1-setup-x64.exe` собран, packaged smoke с перезапуском и embedded IDE approval/write/Undo прошёл. Размер 428111201 байт; SHA256 `04a55ad1fb7ee8cb3c895a598df93dbc35ee6ef968f4d01304e11eb5f67ae296`. Проверено совпадение Core-исходников с ранее проверенным frozen Core; manifest — `artifacts/development-2026-11-03/recovery-release.json`. Ни установка на чистую Windows, ни remote CI, ни публикация этим этапом не закрываются.

Следующий приоритет — настраиваемые acceptance checks в новой IDE на существующем Core, затем измеримое восстановление после повторных пустых поисков. Незакрытые пункты Task 6: реальные interruption/denial/long-task сценарии, полный profiling и время до первого полезного результата.
