# 24. Полный установщик Windows 6.0.1

## Состав и установка

Цель этой версии — установить приложение без предварительной настройки Python,
Node.js или отдельного llama.cpp. Поддерживается Windows 10/11 x64.

| Компонент | Как поставляется | Для чего нужен |
| --- | --- | --- |
| Electron, Chromium, Node.js | Внутри приложения | Интерфейс и главный процесс |
| Python 3.12, OpenAI SDK, HTTPX и зависимости | PyInstaller Core | Логика агента и HTTP-клиент |
| llama.cpp b11829 CPU x64 | `resources/runtime/llama` | Собственный сервер GGUF |
| MS Visual C++ 14.44.35211 x64 | Официальный офлайн-bootstrap | Системные DLL сервера |
| System.Speech | Компонент Windows/.NET Framework | Озвучивание установленными голосами |

NSIS проверяет HKLM в 64-битном представлении реестра: `Installed` и `Version`
для `SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64`.
Подходящая или более новая версия пропускает bootstrap. Иначе перед установкой
приложения запускается включённый официальный `vc_redist.x64.exe` с
`/install /passive /norestart`. Он сам запрашивает UAC, если нужны права.
Код 3010 выставляет флаг перезагрузки; прочие ошибки останавливают установку.
Приложение сохраняет установку для текущего пользователя.

Весовые файлы GGUF, CUDA-драйверы, GPU-сборки сервера и дополнительные языковые
голоса не включены. Модель пользователь выбирает отдельно с учётом памяти ПК.
Базовая CPU-работа не требует CUDA и внешнего LM Studio. Для микрофона STT ещё
не подключён: установщик не превращает подготовленный интерфейс в распознавание речи.

## Подготовка зависимостей

[`windows-dependencies.json`](../packaging/windows-dependencies.json) фиксирует
официальные URL, версии и SHA256. Microsoft permalink может со временем изменить
содержимое: сборка тогда намеренно завершится ошибкой до ручной проверки новой
версии и обновления закреплённой суммы.

[`prepare_windows_dependencies.py`](../tools/prepare_windows_dependencies.py):

1. `verified_download` повторно использует только кэш с совпадающим SHA256;
   загружает во временный файл, сверяет сумму и лишь затем заменяет кэш.
2. `prepare` читает ZIP без `extractall`, принимает только плоские имена и копирует
   `llama-server.exe`, DLL и лицензии. Остальные CLI-exe не поставляются.
3. Добавляет MIT-лицензию llama.cpp и manifest происхождения в runtime.
4. Готовит VC++ bootstrap; ничего не устанавливает на машине сборки.

Бинарные зависимости хранятся в исключённом из Git `build/windows-deps`.
Настоящий NSIS hook — [`prerequisites.nsh`](../packaging/prerequisites.nsh).
[`electron-builder.json`](../electron-builder.json) добавляет runtime через
`extraResources` и hook через `nsis.include`.

В Electron `bundledRuntimePath()` возвращает существующий server из resources
или build-каталога разработки. `runtime:status` сообщает этот путь интерфейсу.
`runtime:start` использует ручной выбор exe либо встроенный сервер. Файл модели
по-прежнему выбирается нативным диалогом: renderer не получает право передавать
произвольный путь на исполнение. Кнопка «Другой llama-server» оставляет возможность
подключить совместимую GPU-сборку.

## Воспроизводимая сборка и публикация

Из корня проекта в Windows x64 с Python 3.12:

```powershell
python -m pip install -r requirements-build.txt
npm ci
python tools/prepare_windows_dependencies.py
python tools/build_windows_core.py
npm run package:win
node tests/electron/packaged-smoke.mjs
```

[`release-windows.yml`](../.github/workflows/release-windows.yml) собирает пакет
на Windows runner, проверяет frozen Core, интерфейс, документацию, настоящий
packaged exe и наличие встроенного сервера с DLL. После успешных проверок
публикует GitHub prerelease с exe и SHA256SUMS. Триггер — явное изменение
[`release.json`](../packaging/release.json) в ветке `codex/electron-agent-bridge`;
версия обязана совпадать с package.json. Уже существующий Release не перезаписывается.
Токен ограничен `contents: write` внутри workflow; личные токены в файлах не нужны.

[`test_windows_dependencies.py`](../tests/test_windows_dependencies.py) проверяет
валидный кэш без сети, отказ при подмене загрузки с сохранением старого файла и
атомарную замену повреждённого кэша. Packaged smoke запускает приложение без
доступного Python и Node.js в PATH и проверяет API ядра и встроенный runtime.
Тест на машине разработчика не равен установке в чистой Windows VM; отдельный
прогон bootstrap с отсутствующим VC++ и UAC остаётся проверкой для чистой VM.

Официальные источники: [llama.cpp b11829](https://github.com/ggml-org/llama.cpp/releases/tag/b11829),
[Microsoft: deployment и параметры VC++](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files),
[electron-builder NSIS](https://www.electron.build/nsis/).

В packaged smoke отключено только Chromium-замедление перекрытого окна, чтобы
unattended-проверка не зависела от активного окна рабочего стола. Deadline CDP
45 секунд покрывает 35-секундный model probe; deadline выхода 25 секунд покрывает
15-секундное завершение ядра. Локальная проверка выявила повторный `app.quit()`
после отменённого `will-quit`: ядро уже завершалось, но Electron мог оставаться.
Теперь после выхода ядра используется `app.exit(0)`; аварийный deadline
завершает процесс с кодом 1. Новые RPC во время завершения отклоняются, чтобы
не перезапускать ядро.
