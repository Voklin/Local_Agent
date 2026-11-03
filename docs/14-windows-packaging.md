# 14. Windows-сборка со встроенным Python Core

## Что собирается

Разработческая установка требует Python, Node и исходники. Новый путь упаковки создаёт Windows x64 приложение с собственным Python 3.12 Core и Electron. Конфигурация есть в репозитории; готовность установщика на чистой машине подтверждается отдельно, по процедуре ниже. До такого испытания этап 5 целиком не считается завершённым.

`tools/build_windows_core.py` вызывает PyInstaller в режиме onedir: рядом с `lca-core.exe` находится `_internal` с интерпретатором, стандартной библиотекой, нативными модулями и зависимостями. Этот каталог нужно переносить целиком. Console bootloader необходим для JSON-lines stdin/stdout; Electron запускает процесс с `windowsHide`, поэтому отдельное консольное окно пользователю не требуется. Bridge явно выбирает UTF-8 для трёх стандартных потоков: frozen-приложение не должно зависеть от того, учитывает ли bootloader переменную PYTHONIOENCODING.

PyInstaller анализирует импорты. SDK содержит отложенные импорты ресурсов и типов, поэтому build включает `openai.resources` и `openai.types` явно. В комплект также входят Markdown-навыки из `skills`: SkillManager ищет их относительно своего модуля. Qt исключён, его интерфейс в пакет Electron не входит. В используемом bundled Python обнаружена модификация ssl.py, которая требует соседний codex-rejected-cas.pem. Build добавляет этот конкретный служебный PEM, если он существует рядом с ssl.py; стандартный CPython этого дополнения не требует. Без него даже создание HTTP-клиента завершалось FileNotFoundError. Проверка frozen Core должна выявлять подобные runtime-зависимости до распространения. Режим onedir выбран для простой диагностики состава и запуска без распаковки всего Core при каждом старте.

`electron-builder.json` задаёт allowlist собранных renderer/main/preload файлов, ASAR и extraResources для Core. В установленном приложении Main запускает абсолютный `resources/core/lca-core.exe`, без поиска Python в PATH и без LCA_PYTHON override. PYTHONHOME/PYTHONPATH удаляются из окружения этого дочернего процесса. В разработческом режиме прежний LCA_PYTHON сохраняется.

## Файлы и технологии

| Файл / каталог | Назначение |
| --- | --- |
| [requirements-build.txt](../requirements-build.txt) | Точные версии Python-зависимостей сборочного окружения, включая SDK и PyInstaller; обычный requirements-core остаётся диапазоном |
| [tools/build_windows_core.py](../tools/build_windows_core.py) | Проверка Windows x64 / Python 3.12 и воспроизводимая команда freeze |
| [electron-builder.json](../electron-builder.json) | Состав приложения, стабильный appId, Windows x64 и настройки NSIS |
| [package-lock.json](../package-lock.json) | Версии npm и electron-builder; сборочные пакеты находятся в devDependencies |
| `build/core/lca-core` | Промежуточный комплект Core; исключён из Git |
| `artifacts/windows/win-unpacked` | Папка приложения, которую можно тестировать до установщика |
| `artifacts/windows/LocalAgent-6.0.0-setup-x64.exe` | Ожидаемое имя NSIS артефакта текущей версии, если сборка installer завершилась |
| [tests/electron/packaged-smoke.mjs](../tests/electron/packaged-smoke.mjs) | Запуск настоящего packaged exe, проверка renderer → IPC → встроенный Core и повторного открытия |

Это фиксация набора зависимостей, а не обещание побитово одинакового exe: timestamps, ОС и упаковщик могут менять байты. Сборочные артефакты и пользовательские данные не попадают в Git.

## Сборка на Windows x64

Нужны Python 3.12 x64 и Node/npm на сборочной машине. Из корня репозитория:

```powershell
py -3.12 -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install -r requirements-build.txt
npm ci
.\.venv-build\Scripts\python.exe tools/build_windows_core.py
npm run package:win -- --dir
```

Последняя команда собирает UI и папку приложения. Для локального NSIS installer выполните `npm run package:win` без `--dir`. Команда всегда передаёт `--publish never`: создание установщика не публикует GitHub Release. Сначала собирается Core, затем оболочка; иначе упаковщик не найдёт extraResources. PyInstaller очищает только свои выходные build-каталоги; не запускайте freeze из окружения с пользовательскими файлами внутри build.

NSIS настроен на установку для текущего пользователя с выбором каталога. Автообновление не подключено. Исполняемые файлы пока не подписываются; перед распространением нужны отдельные проверки подписания и доверия Windows. Числовая версия Electron берётся из `apps/desktop/package.json`; исторический VERSION старого Qt-пути не является версией установщика. При изменении версии обновляйте также workspace и lock через npm, затем проверяйте сохранность данных.

## Проверки собранного комплекта

Для subprocess-набора можно передать абсолютный путь к frozen Core:

```powershell
$env:LCA_TEST_CORE = (Resolve-Path build/core/lca-core/lca-core.exe).Path
python -m unittest discover -s tests/migration -p test_bridge_process.py -v
Remove-Item Env:LCA_TEST_CORE
node tests/electron/packaged-smoke.mjs
```

Python нужен только тестовому драйверу первой команды. Проверяемый Core запускается из временной папки с PATH, содержащим лишь Windows System32, без PYTHONHOME/PYTHONPATH. Набор проверяет HTTP discovery, streaming, approval, подтверждённую запись, kill/reopen, сохранение настроек и отсутствие тестового ключа в JSON.

Node-драйвер второй команды запускает настоящий LocalAgent.exe дважды, с отдельными LOCALAPPDATA и Electron-профилем. Он поднимает временную HTTP-фикстуру, подключается через loopback Chrome DevTools Protocol, проверяет file renderer, изоляцию Node, health, discovery, настройки после повторного запуска и нормальное закрытие. PATH урезан, LCA_PYTHON/PYTHONHOME/PYTHONPATH намеренно указывают на отсутствующие пути. CDP включается только аргументами тестового запуска; приложение само не включает отладочный порт. Во время теста окно приложения может появиться, поэтому запускать его следует отдельно от пользовательской работы.

## Данные и диагностика

Чаты, checkpoint и настройки Core остаются в `%LOCALAPPDATA%/LocalCodingAgent`, независимо от каталога установки. Electron-профиль хранится в userData, а диагностический файл — `userData/logs/main.log`. Main записывает только версию, платформу, запуск/остановку Core и системный код ошибки; модельные ответы, ключ, запросы и stderr в этот файл не копируются. Файл ограничен примерно 1 МБ: при следующей записи после превышения он очищается. Это простая ограниченная диагностика, а не архив всех сеансов. Ошибка логирования не должна блокировать запуск.

Настройки NSIS не удаляют app data при uninstall. Этот флаг не заменяет проверку реального uninstall/upgrade: данные Core и профиль Electron находятся в разных каталогах. Ключ в Electron/Core хранится в памяти процесса; после полного закрытия его нужно ввести снова, если endpoint требует авторизацию. Windows Credential Manager в этом этапе не добавляется.

## Приёмка на чистой машине

Используйте новую Windows 11 x64 VM/Windows Sandbox без Python, Node, исходников и папок текущего разработчика. Скопируйте только installer или весь win-unpacked. Проверка с урезанным PATH на разработческой машине полезна, но не заменяет эту процедуру.

1. Установить приложение обычным пользователем; открыть из меню/ярлыка и каталога с пробелами и кириллицей. Проверить health, диагностику и отсутствие консольного окна Core.
2. Подключить отдельную тестовую папку и совместимый сервер модели. Проверить чтение, поток, Stop до заголовков и в потоке, Apply/Reject, внешний конфликт файла и восстановление paused после завершения собственного тестового процесса.
3. Полностью закрыть приложение и проверить завершение принадлежащего ему Core. Открыть снова: чаты и настройки сохраняются, старое approval не действует, ключ не записан в JSON или log.
4. Установить следующую локальную версию поверх первой. Проверить версию, сохранность прежнего чата и отсутствие перезаписи пользовательского проекта.
5. Удалить приложение и установить заново. Проверить сохранение данных и возможность их явного ручного удаления отдельно от проекта. Сохранить ОС, SHA commit, хеш installer, точные результаты и ограничения в WORK_PLAN.

## Официальные источники

Сборочный путь использует [PyInstaller usage](https://pyinstaller.org/en/stable/usage.html), [runtime information](https://pyinstaller.org/en/stable/runtime-information.html), [конфигурацию electron-builder](https://www.electron.build/configuration/) и [NSIS](https://www.electron.build/nsis/). Эти документы объясняют freeze, extraResources и installer; фактическую работоспособность именно LocalAgent подтверждают проверки проекта.

## Подтверждённое локальное состояние 22 октября 2026

Собраны Core, win-unpacked и NSIS размером около 130 МБ. Восемь subprocess-тестов frozen Core и два запуска настоящего packaged exe прошли. Непосредственный запрос frozen Core к работающему LM Studio qwen3.5-4b прочитал временный probe.txt, вернул точный маркер и сохранил completed чат. Ошибки первой сборки (UTF-8 stdio и обязательный PEM модифицированного Python) исправлены и перепроверены; они показывают, почему одного health недостаточно.

WindowsSandbox.exe в текущей среде не найден. Поэтому реальная установка, обновление и удаление на чистой VM не выполнялись. Готовность этапа 5 остаётся частичной. Последний SHA и результаты CI находятся в WORK_PLAN; исходники и локальные артефакты не являются опубликованным релизом. Windows CI собирает installer и проверяет пакет на отдельном runner; описание хранения artifacts — в [actions/upload-artifact](https://github.com/actions/upload-artifact).

Windows CI подтвердил путь упаковки на отдельном runner со штатным Python 3.12: job [windows-package, run 39842584271](https://github.com/Voklin/Local_Agent/actions/runs/39842584271/job/120047352881) успешно выполнил freeze, 8 subprocess-тестов, NSIS, настоящий packaged smoke и загрузку временного installer artifact. Это подтверждает независимость пакета от Python разработчика в PATH, но не заменяет приёмку install/upgrade/uninstall в чистой VM.
