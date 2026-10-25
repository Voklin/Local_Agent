# Neutral

Neutral 7 — разговоры, проекты, IDE и голосовая Лола в едином настраиваемом интерфейсе.
Добавлены проекты/архив/поиск/экспорт чатов, профили API и OpenAI Responses,
переключаемые инструменты/плагины/навыки, настоящий MCP и предложения навыков агентом.
Основная модель работает одним циклом; прежняя система четырёх ролей удалена.
[Руководство Neutral 7](docs/36-neutral-guide.md) ·
[Ядро и расширения](docs/37-neutral-core-and-extensions.md) ·
[Проекты и разговоры](docs/38-neutral-projects-and-conversations.md) ·
[Проверки сборки 7.0.0](docs/39-neutral-validation.md).
[Оформление, рефакторинг, миграция и проверки](docs/33-lola-refactor-and-appearance.md).
[Историческая система ролей 6.7](docs/34-ide-roles-and-model-lifecycle.md).
[Умный контекст, музыка, заметки и таймеры Лолы](docs/35-smart-context-and-lola-tools.md).
[Проверка проекта и исправления от 24 октября](docs/AUDIT_2026-10-24.md).
Публикация релиза выполняется только вручную; PR содержит актуальные исходники.

Настольный агент для работы с кодом: Electron + React + TypeScript и Python-ядро с подключением OpenAI-совместимой модели.

**Начать изучение: [подробное руководство на русском](docs/README.md).**

В руководстве описаны технологии, архитектура, этапы разработки, путь запроса, функции, классы, файлы, протоколы, хранение данных, тестирование и реальные ограничения. [Карта файлов](docs/reference/file-map.md) и справочники [Python](docs/reference/python.md) / [TypeScript](docs/reference/typescript.md) связаны с исходниками.

## Установка Windows

Готовый Windows x64 installer: [GitHub Releases](https://github.com/Voklin/Local_Agent/releases). Python, Node.js, Electron, CPU llama.cpp и офлайн-установщик Visual C++ включены. Выберите GGUF-модель отдельно либо подключите LM Studio. [Состав и сборка установщика](docs/24-full-windows-installer.md).

## Запуск Electron

Из корня репозитория, после установки Python и Node.js с npm:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-core.txt
npm ci
.\run-desktop.bat
```

Укажите URL сервера и ID модели. В Chat можно общаться без папки; для работы с файлами откройте проект в IDE. Ответ появляется по мере генерации; запись файла требует просмотра diff и подтверждения. URL/модель сохраняются, API-ключ Electron Core остаётся в памяти. Подробности и сохранённый Qt GUI — в [инструкции запуска](docs/01-project-and-setup.md).

## Разработка

- [Архитектура](docs/03-architecture.md) и [путь одного запроса](docs/05-request-walkthrough.md).
- [Контракты RPC/IPC и событий](docs/08-protocols.md).
- [Данные и разрешения](docs/09-data-and-security.md).
- [Тесты и диагностика](docs/10-testing-and-debugging.md).
- [Готовые и незавершённые части](docs/11-current-status.md).
- [План дальнейшей разработки](docs/WORK_PLAN.md).
- [Как изменять проект и документацию](docs/12-development-guide.md).

```powershell
npm run build
python -m unittest discover -s tests -v
python -m unittest discover -s tests/migration -v
npm run docs:generate
npm run docs:check
```

Для всех Python-тестов нужен полный `requirements.txt`. Текущий Windows workflow проверяет Python, сборку, Neutral GUI и документацию; полный редактор/голосовой smoke дополнительно выполняется локально.

[Краткая памятка v6](README_V6_MIGRATION.md) · [План развития](MIGRATION_PLAN.md) · [Исторические README](docs/history/legacy-readme.md).

Три режима Chat/IDE/Ассистент и восстановление пустых ответов описаны в [главе 16](docs/16-workspaces-and-answer-recovery.md).

Рабочие расширения: [редактор](docs/18-editor.md), [поиск/Ctrl+P](docs/19-project-search.md), [запуск GGUF](docs/20-local-runtime.md), [память и чат](docs/21-memory-and-chat.md), [Лола и системная озвучка](docs/22-voice-companion.md). Для собственного GGUF в установочной версии CPU-сервер включён: выберите модель в настройках. Можно указать другой llama-server; загрузка весов моделей не выполняется. Лола имеет отдельную историю и модель, настраиваемый характер и Windows TTS; микрофон распознаётся через настроенный STT-сервер. Есть JSON tool calling, KV-кеш и owner-only Telegram-контроль. [Новые возможности](docs/25-json-tools-and-cache.md), [Лола/STT](docs/26-miya-model-and-stt.md), [PC/Telegram](docs/27-desktop-and-telegram.md).

Нейроозвучка «Лола · аниме на русском» и фраза активации: [глава 29](docs/29-neural-voice-and-wake.md). Для Qwen3-TTS требуется отдельная установка speech-среды/модели; для активации — работающий STT.
