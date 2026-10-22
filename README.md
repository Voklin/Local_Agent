# LocalAgent

Настольный агент для работы с кодом: Electron + React + TypeScript и Python-ядро с подключением OpenAI-совместимой модели.

**Начать изучение: [подробное руководство на русском](docs/README.md).**

В руководстве описаны технологии, архитектура, этапы разработки, путь запроса, функции, классы, файлы, протоколы, хранение данных, тестирование и реальные ограничения. [Карта файлов](docs/reference/file-map.md) и справочники [Python](docs/reference/python.md) / [TypeScript](docs/reference/typescript.md) связаны с исходниками.

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

Для всех Python-тестов нужен полный `requirements.txt`. Текущий Windows workflow проверяет Python, сборку и документацию; скрытый Electron UI smoke запускается отдельно.

[Краткая памятка v6](README_V6_MIGRATION.md) · [План развития](MIGRATION_PLAN.md) · [Исторические README](docs/history/legacy-readme.md).

Три режима Chat/IDE/Ассистент и восстановление пустых ответов описаны в [главе 16](docs/16-workspaces-and-answer-recovery.md).
