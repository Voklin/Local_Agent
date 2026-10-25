# Neutral 7.0.0: проверка итоговой сборки

25 октября 2026, Windows x64. Проверяется рабочая ветка
`codex/electron-agent-bridge`. Исходные исправления аудита 24 октября включены.

| Проверка | Результат |
| --- | --- |
| Python unit (`unittest discover -s tests -v`) | 147 тестов, OK; 1 skip — Windows не предоставил привилегию создания symlink |
| Python migration/integration | 76 тестов, OK |
| Настоящий frozen Core, JSON-lines subprocess | 15 тестов, OK |
| MCP SDK stdio и Streamable HTTP | Настоящие локальные серверы: discovery, JSON Schema, вызов, отказ и отмена — OK |
| MCP из собранного Core | Реальное stdio discovery двух tools — OK |
| OpenAI Responses | Локальный HTTP/SSE: текст, functions, encrypted reasoning continuity, retry, probe и отдельная модель Лолы — OK |
| Команды проекта | Отказ без запуска, scope cwd, exit 0/7, Unicode, лимит вывода и отмена — OK |
| TypeScript, Vite, Electron main/preload | Build — OK |
| Новый Neutral GUI smoke | Проекты, инструкции, навык, MCP approval, Node с exit 0, pin/archive/copy/export/delete, темы и компактное окно — OK |
| Полный прежний GUI smoke | Редактор, вложенные Windows-пути/junction, revision/diff conflict, история, stream/cancel, STT WAV, TTS playback, wake phrase — OK |
| Host application / microphone / media tests | Все три Node-проверки — OK |
| Документация | 6 AST-справочников с ручными аннотациями; проверка Markdown-ссылок и source lines — OK |
| Packaged Neutral.exe | Два реальных запуска с урезанным PATH и отсутствующим внешним Python: Core, discovery, настройки после перезапуска, системный каталог голосов и чистый выход — OK |

Установщик: `artifacts/windows/Neutral-7.0.0-setup-x64.exe`.
Рядом записан `SHA256SUMS.txt`. В пакет включены Electron/Node, frozen Python Core
с MCP/OpenAI зависимостями, CPU llama.cpp и установщик Visual C++.
Голосовые веса, обучающий корпус и модельные GGUF не включаются.

SHA256 итогового установщика:

```text
29bf6265b379f432feae3b1c0663e3fdfc3c0d11fa0a246206de2e266afde909
```

Платные API не вызывались. LM Studio доступен и возвращает каталог моделей,
но загруженных экземпляров не было; ради проверки сборки модели на GPU не загружались.
Реальные модельные качества и субъективный тембр голоса этими проверками не измеряются.

Установка/обновление/удаление на чистой виртуальной машине в этом сеансе не выполнялись.
Текущее пользовательское приложение не заменялось. Релиз и слияние не выполнялись;
installer создан локально, публикация исходников идёт в существующий draft PR.

Подробности устройства: [руководство](36-neutral-guide.md),
[ядро и расширения](37-neutral-core-and-extensions.md),
[чаты и данные](38-neutral-projects-and-conversations.md).
