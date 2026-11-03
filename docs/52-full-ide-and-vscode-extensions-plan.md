# План полноценной IDE и расширений VS Code

Текущая IDE имеет свой textarea/editor, tabs, diff approval, поиск и разовую LSP
диагностику. Полноценного VS Code Extension Host сейчас нет. Ни замена textarea
на Monaco, ни распаковка VSIX сами по себе не дают terminal/debug/SCM/workbench API.
VS Code исполняет расширения в отдельном host и ограничивает доступ к UI через
[Extension API](https://code.visualstudio.com/api/extension-capabilities/overview).

## Выбор основы через prototype

| Вариант | Польза | Цена и ограничения |
| --- | --- | --- |
| Продолжать свой editor / добавить Monaco | Хорошее редактирование при небольшом изменении Neutral | Придётся заново создавать workbench, Extension Host и значительную часть VS Code API; не выбираем как путь к массовой VSIX совместимости. |
| Theia Electron | Платформа для собственного IDE-продукта; удобнее сохранять Neutral и подключать наш Core. Есть установка VS Code extensions через Open VSX. | Совместимость проверяется по API/расширениям, а не объявляется 100%. Добавляется Node backend/extension host. |
| Собственный Code-OSS продукт | Ближе к upstream VS Code API и поведению workbench | Существенное сопровождение fork, обновления Electron/безопасности и перенос наших Chat/Лолы в платформу либо продуманная интеграция процессов. |

Предварительная рекомендация — **Theia Electron prototype**, поскольку Neutral
нужен собственный продукт с Chat/Лолой и сохранённым стилем. Если обязательная
приёмочная матрица extensions не проходит, выбрать Code-OSS до массового переноса.
Это инженерная рекомендация, окончательная платформа требует измеренного spike.
[Архитектура Theia](https://theia-ide.org/docs/architecture/),
[установка extensions](https://theia-ide.org/docs/user_install_vscode_extensions/).

Microsoft отделяет Code-OSS от своего branded продукта и Marketplace integration;
Marketplace не объявлен универсальным магазином для любых дистрибутивов. Поэтому
планируем **Open VSX + локальные VSIX**, с проверкой условий конкретного расширения.
Не обещаем доступ ко всем Microsoft proprietary extensions, debug adapters и
proposed API. [Позиция Microsoft](https://github.com/microsoft/vscode/wiki/Differences-between-the-repository-and-Visual-Studio-Code).

## Целевая архитектура

Neutral Core остаётся независимым сервисом задач/approval/history/subagents. IDE
workbench получает отдельный IDEAdapter; Chat и Лола используют те же task/run IDs.
Не загружаем удалённый редактор в привилегированный iframe и не выдаём extension
host API нашего трея, ключи модели или произвольный desktop RPC.

Предлагаемые границы: WorkspaceService, WorkingCopy/DocumentService, TerminalService,
DebugService, SCMAdapter, ExtensionManager и NeutralAgentBridge. Для Theia это
platform contributions; для Code-OSS — минимальный product fork + встроенное
Neutral extension с публичным workspace API и нужными узкими adapters.

Рабочие копии редактора должны иметь **одного владельца**. Core читает сохранённый
файл либо явно разрешённый snapshot unsaved buffer с document version. Применение
model diff проверяет ожидаемую version/hash, попадает в editor undo и выдаёт общую
workspace revision. Внешние изменения и commands инвалидируют evidence. Одновременная
запись старого Python writer и новой IDE в один файл недопустима.

## Prototype: условия go/no-go

На отдельной сборке, сохраняя существующую IDE как fallback:

1. Открыть проект, несколько файлов и split view, изменить/сохранить/undo, показать
   конфликт внешнего изменения; проверить Neutral palette и клавиатуру.
2. Установить из Open VSX theme, snippets, language server, formatter и debugger;
   отдельно проверить локальный VSIX и extension с собственным command/view.
3. Проверить activation events, commands, diagnostics, formatting, completion,
   goto definition/references/rename, settings, terminal и debug breakpoints.
4. Из Neutral предложить patch, подтвердить в UI, увидеть editor undo и stale checks.
5. Зафиксировать поддержанные версии/API, неработающие расширения, startup/RAM/CPU
   относительно текущего Neutral и стоимость сопровождения платформы.

Фикстура extension должна проверять реальный вызов API, а не только наличие папки
на диске. Перечень обязательных пользовательских расширений можно дополнять после
prototype; названия/популярность не заменяют проверку лицензии и совместимости.

## Полный пользовательский функционал

| Область | Что входит |
| --- | --- |
| Редактор | Multi-root workspaces, tabs/splits, символы, minimap по настройке, форматирование, rename/references, settings/keybindings, autosave и восстановление buffers. |
| Поиск и диагностика | Общий Problems view, versioned LSP, поиск/замена по проекту, excludes и read policy, переходы по результатам и быстрые открытия. |
| Terminal/tasks | Настоящий PTY + terminal view, среды и shell profiles, задачи сборки, bounded output/cancel для model commands. Ручной терминал пользователя явно отличается от действия модели. |
| Debug | DAP, launch configs, breakpoint/variables/call stack, debug console, session stop и очистка дочерних процессов. |
| Git/SCM | Статус, diff, staging/commit по пользовательскому действию, ветки, конфликты, worktree switch с dirty guard. Никаких автоматических merge/push от миграции. |
| Extensions | Поиск/карточка/установка/удаление/enable per workspace, версии и compatibility, local VSIX, обновления и rollback версии. Отдельно от skills/MCP/plugins агента. |
| Testing | Обнаружение и запуск тестов, реальный exit/result, связь с criteria/evidence и workspace revision. |

## Установка и доверие к extensions

Использовать extension manager выбранной платформы. Проверять engines.vscode,
OS/architecture/native dependencies, лицензии, integrity и безопасную staging
распаковку. Установка должна быть атомарной, со старой версией для rollback и
отменой скачивания. Workspace Trust и управление источниками объясняют, когда
расширение исполняет код с правами пользователя. Это не OS sandbox.

Модель может рекомендовать extension и подготовить запрос на установку. Фоновая
установка исполняемого расширения без пользовательского разрешения не входит
в план. Существующее разрешение пользователя можно сохранять в точной области.
Agent plugin import и VSIX install — разные форматы, каталоги и маршруты IPC.

## Перенос и приёмка

После решения по prototype: feature flag → read-only открытие → WorkingCopyAdapter
и diff approval → terminal/debug/SCM → Extension UI → migration default IDE.
Историю/чаты/Serena/ключи не переносить в extension storage как второй источник истины.
Старые JSON/SQLite backups сохраняются, пути проектов не меняются автоматически.

Финальная приёмка: реальные API-проверки выбранных extensions, dirty/undo/reload,
offline VSIX и обновление, авария extension host без потери Core, restart во время
approval, дефекты ZIP/сети/платформы, packaged запуск без dev-зависимостей. До этого
текущий editor не удаляется. Полноценная IDE не считается готовой по одному LSP
сообщению или screenshot с похожим на VS Code оформлением.
