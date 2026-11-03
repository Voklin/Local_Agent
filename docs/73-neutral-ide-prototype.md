# 73. Neutral IDE: прототип отдельного приложения на Code-OSS

Дата проверки: 1 ноября 2026. Пользователь выбрал собственную отдельную IDE, а не открытие установленного VS Code. Существующая Studio, Chat и Лола сохранены.

## Результат и граница готовности

Подготовлена собственная локальная копия Code-OSS через VSCodium **1.143.17232 / VS Code API 1.143.1**, с именем Neutral IDE, N-иконкой, Neutral Studio theme, собственным executable/profile/shared storage и встроенным Neutral extension. В главном окне добавлена кнопка **Открыть в Neutral IDE**. Рабочая папка берётся из текущего Core; несохранённые изменения старого редактора блокируют передачу.

**GO для выбора Code-OSS как платформы. NO-GO для замены текущего редактора по умолчанию:** полная цепочка предложения модели из Core, общего approval, editor undo и инвалидации evidence ещё не подключена. Проверка editor API ниже выполнена отдельной пользовательской командой и не выдаётся за end-to-end агентскую правку. Gate 18 остаётся открытым в этой части; этап 19 не объявлен завершённым.

Это воспроизводимый прототип поверх публичного MIT runtime, а не собственная сборка всего upstream из исходников и не установщик готовой новой IDE. Исходный план требовал отдельной ветки; здесь source-прототип изолирован каталогом `prototypes/neutral-ide`, но существующая грязная рабочая копия не переносилась и не коммитилась автоматически.

## Основа и распространение

Официальный ZIP релиза VSCodium проверяется по закреплённому SHA-256:
`a1090868af8ac0ac04c22d79fdd02246fa115a78daf38a741d8db06df1753c1d`.
Ссылки, версия и лицензии сохраняются в локальном `artifacts/neutral-ide/base-manifest.json`.

Минимальный product fork меняет имя, app ID, mutex, URL protocol, ресурсы и PE icon/version. Main не вызывает `code` из PATH и не ищет системный VS Code. Автоматическое обновление runtime отключено: перед новым upstream pin нужно повторить матрицу API. Upstream product metadata и лицензии сохраняются; слепое удаление metadata новых встроенных компонентов не входит в поддержанный fork.

Реестр — [Open VSX](https://open-vsx.org/), локальный VSIX устанавливается штатным extension manager. MIT исходники VS Code не дают права обещать доступ ко всем расширениям Microsoft Marketplace. Основа: [различия исходников и продукта Microsoft](https://github.com/microsoft/vscode/wiki/Differences-between-the-repository-and-Visual-Studio-Code), [VSCodium](https://github.com/VSCodium/vscodium), [релиз 1.143.17232](https://github.com/VSCodium/vscodium/releases/tag/1.143.17232).

## Архитектура прототипа

`Neutral renderer → fixed IPC ide:open → NeutralIde → собственный NeutralIDE.exe → встроенный neutral.neutral-agent → именованный канал → текущий Core health`.

`NeutralIde` в Electron main владеет запуском и каналом. `connect()` создаёт случайное имя Windows pipe и 256-bit token; `open()` проверяет продукт, проект и запускает его с отдельными `--user-data-dir`, `--extensions-dir`, `--shared-data-dir`; `dispose()` закрывает свои сокеты и удаляет только собственный descriptor. Ошибка создания descriptor возвращается вызывающему коду. Размер сообщения ограничен 4096 байт, idle timeout 5 секунд, сравнение токена constant-time. Поддерживаются только `status` и `focus`. Ни shell, ни конфиг моделей, ни история, ни произвольный Core method через этот канал недоступны.

Descriptor хранится вне проекта в профиле Neutral. Это аутентификация канала между своими локальными процессами, а не sandbox против исполняемого кода того же пользователя. Установленные VSIX работают с обычными правами Extension Host; устанавливать непроверенные расширения автоматически модель не может.

Встроенный extension добавляет N-значок в activity bar и собственную боковую панель. `request()` читает актуальный descriptor при обращении, поэтому перезапуск Neutral не требует зашивать порт или секрет в проект. `renderBridge()` использует CSP с nonce и textContent для результатов. Главное окно сохраняет единственный Core, scheduler, модельные подключения и историю. IDE не вызывает `set_project`, `new_chat`, `start_task` и не меняет активный разговор за спиной интерфейса.

## Рабочая копия и доказательства

`capture(document,replacement)` принимает сохранённый UTF-8 файл внутри реального workspace, до 256 КиБ, с проверкой canonical path. Контракт содержит `source_kind=disk`, URI, document version, buffer hash, disk base hash и replacement. Dirty buffer, двоичный/слишком большой файл, путь вне проекта и расхождение буфера/диска отклоняются.

`neutral.previewEdit` запрашивает тестовый replacement, показывает стандартный diff и отдельный modal **Применить**. `apply(snapshot)` повторно проверяет версию/хэши/доступ, затем использует `workspace.applyEdit`. На диск автоматически не сохраняет: undo принадлежит редактору, сохранение — пользователю. Preview content provider не создаёт временную копию исходника на диске. После команды виртуальный preview освобождается.

Это ограниченный прототип. Race с произвольным внешним процессом после последнего чтения диска нельзя объявлять устранённым атомарной транзакцией. Штатный редактор сохраняет external-change conflict. Для agent writes необходим общий WorkingCopyAdapter, document lease и receipt в каноническом execution contract; до этого Python writer и новый IDE не объявляются единым владельцем буфера.

## Проверенная совместимость

Все пять Open VSX артефактов закреплены по SHA-256, MIT license metadata и платформе в [extensions.lock.json](../prototypes/neutral-ide/extensions.lock.json). Проверки выполняются реальным Extension Host, без вызова LLM.

| Область | Версия / источник | Фактическая проверка |
| --- | --- | --- |
| Theme | dracula-theme.theme-dracula 2.25.1 | Установка VSIX, contribution и переключение темы/настройки обратно в Neutral |
| Snippets | dsznajder.es7-react-js-snippets 4.4.3 | Загрузка snippets и реальная вставка через editor.action.insertSnippet |
| Language server | redhat.vscode-yaml 2.1.2026102308 | Активация server и error diagnostics на невалидном YAML; эта конкретная датированная версия не объявляется универсальным production default |
| Formatter | esbenp.prettier-vscode 12.4.0 | Форматирование JS через provider, применение edit и сохранение результата |
| Debugger | ms-python.debugpy 2026.6.0 win32-x64 | Настоящий Python launch, breakpoint, stackTrace, scopes, variables, continue и termination |
| Builtin TypeScript | runtime 1.143.1 | Completion, definition, references, rename и error diagnostics |
| Local VSIX | neutral.probe 0.1.0 | Штатная установка и реальное выполнение extension command |
| Terminal | builtin PTY + PowerShell | processId и выполнение команды с проверкой созданного marker |
| Editor | builtin workbench | Tabs/split, save, undo, отказ stale buffer/disk/outside workspace, сохранность draft при внешнем изменении |
| Neutral UI | modal в обычном workbench | Видимый diff, кнопка Применить, изменение только буфера, undo |
| Desktop bridge | текущий Electron + Python Core | Кнопка, root/dirty guards, запуск собственного exe/profile, auth/allowlist, status/focus |

Доступность других расширений, proprietary Marketplace пакетов, удалённых extension hosts, нативных зависимостей и proposed APIs не установлена этой матрицей. CLI совместимость не заменяет проверку API. Исторический xabikos.JavaScriptSnippets с engines `0.10.x` не включён в рабочую матрицу; выбран пакет с подходящим engines range. Для debugpy выбирается именно win32-x64, а не случайный platform latest.

## Файлы и воспроизведение

- [README прототипа](../prototypes/neutral-ide/README.md): команды подготовки, запуска и проверок.
- [prepare.py](../prototypes/neutral-ide/prepare.py): закреплённый ZIP, hash, безопасные пути распаковки/лимит размера, product identity, ресурсы, PE branding и встроенный extension. Маркер другой версии отклоняется; незавершённая распаковка может повториться. Кириллический workspace поддерживается: legacy rcedit работает с относительными именами во временном staging.
- [install_test_extensions.py](../prototypes/neutral-ide/install_test_extensions.py): проверенные VSIX через настоящий CLI, отдельный test profile; генерирует и устанавливает локальный probe VSIX.
- [test_host.py](../prototypes/neutral-ide/test_host.py): одноразовые проекты, host/UI сценарии, отчёты. Успех требует `status=passed`, поскольку Code-OSS может завершить упавшие Extension Tests с exit 0.
- [host.cjs](../prototypes/neutral-ide/tests/host.cjs): API/assertions и настоящие language/debug/PTY сценарии.
- [drive.cjs](../prototypes/neutral-ide/tests/drive.cjs): CDP-драйвер modal, screenshot и измерения в собственном тестовом окне.
- [ui-probe](../prototypes/neutral-ide/tests/ui-probe/extension.cjs): отдельный test extension для normal development host; никогда не копируется в runtime.
- [processes.cjs](../prototypes/neutral-ide/tests/processes.cjs): измерение дерева своего PID через Windows process metadata; без остановки сторонних процессов.
- [neutralIde.ts](../apps/desktop/electron/neutralIde.ts): desktop launcher и ограниченный канал.
- [neutral-ide-smoke.cjs](../tests/electron/neutral-ide-smoke.cjs): изолированный main/renderer/Core тест; закрывает только запущенный им IDE PID/tree.

Артефакты проверок лежат в `.test-data/neutral-ide` и `.test-data/stage18-desktop`: installation.json, host-report.json, ui-report.json, startup.json, preview-confirmation.png, launcher.png и журналы. Они локальные и ignored. Тестовый CDP и отключение Trust не переносятся в рабочий запуск.

## Открытая часть gate и следующая работа

1. До миграции реализовать root/chat/run-bound agent bridge с тем же ToolExecutor/CallJournal/approval; не выдавать расширениям общий RPC.
2. Связать Core patch proposal с working copy snapshot, editor version и обоими hashes. Проверить явное approval, отмену, rename/multi-file edits, restart и отсутствие двух writers. Записать editor receipt и инвалидировать StageVerifier/ContextPack evidence.
3. Отдельно проверить SCM staging/conflicts/worktrees и Testing API реальными сценариями: наличие upstream панелей ещё не такое доказательство. Проверить Extension Host crash/restart, offline updates/rollback и compatibility failures.
4. Зафиксировать собственную воспроизводимую source-сборку или audited runtime supply chain, нормальное обновление и установку двух приложений. Нужны Windows packaged smoke и пользовательская миграция с fallback.
5. Сравнить производительность на одинаковых проектах несколькими cold/warm прогонами. Текущие одноразовые startup/RSS/CPU snapshots — оценка порядка затрат, не p50/p95 benchmark и не требование к ПК.

Существующий установщик не пересобирался. Модели, голосовой корпус, веса и ключи в прототип не включались. Коммит, push, merge и release в этом этапе не выполнялись.

## Финальные проверки этой рабочей копии

- `npm run build`: typecheck, renderer и Electron main/preloads — passed.
- `neutral-ide-smoke.cjs`: реальный desktop/Core launcher и отрицательные проверки — passed.
- Основной `studio-smoke.cjs`: passed, 23 запроса к синтетической HTTP fixture; это не LLM quality benchmark.
- Extension Host: 8 групп проверок passed; UI normal-workbench: 5 утверждений passed, в том числе собственная activity view. Diff и итоговая панель визуально просмотрены.
- Документация и локальные ссылки проверены; Git whitespace check без ошибок. Python Core в этом изменении не переписывался, его полный unit/HTTP matrix заново не запускался.

Единичный warm startup, без нагрузки LLM, hardware acceleration в тестах отключено. Из дерева исключены PowerShell/conhost измерителя; RSS суммирует working sets и может повторно учитывать общие страницы, CPU — накопленное процессорное время, а не процент загрузки. Разные стартовые экраны и test extensions не позволяют считать это строгим сравнительным benchmark.

| Приложение | Первое проверенное отображение | Сумма RSS дерева | Накопленное CPU time |
| --- | --- | --- | --- |
| Neutral Studio | 330 мс | 339.2 МиБ | 1.02 с |
| Neutral IDE с тестовыми extensions | 1137 мс | 1047.5 МиБ | 4.73 с |

Git на завершение: `codex/electron-agent-bridge`, HEAD `9572082`. Подготовленные изменения остаются в рабочей копии вместе с ранее существовавшими изменениями; коммит/push не выполнены. Следующий предмет работы — общий WorkingCopy/approval contract и оставшаяся часть gate, а не переключение default editor.


## Исправление невидимого окна по сообщению пользователя

Подтверждён дефект запуска: `windowsHide: true` передавался интерактивному Code-OSS, поэтому создавались процесс, журналы и Extension Host, но главное окно оставалось скрытым. В `NeutralIde.open()` установлен `windowsHide: false`; фоновые Core/службы не менялись.

Регрессия воспроизведена в одноразовом профиле: прежняя сборка дала `Timeout visible IDE window`, новая прошла. Desktop smoke теперь требует ненулевой `Process.MainWindowHandle` именно запущенного IDE PID — Windows возвращает здесь видимое главное окно. Тест закрывает собственный PID/tree и возвращает ненулевой exit code при ошибке через Electron `will-quit`, независимо от Node `process.exitCode`.

После исправления заново прошли `npm run build` и `neutral-ide-smoke.cjs`. Логи: `.test-data/stage18-visible-before.log`, `stage18-visible-build.log`, `stage18-visible-after.log`. Прежняя проверка по наличию процесса и каталога журналов была недостаточной. Код и сборка обновлены; запущенному до исправления Neutral требуется перезапуск для обновления main process.
