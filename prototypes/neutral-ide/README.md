# Neutral IDE — отдельный Code-OSS prototype

Откройте проект в Neutral и нажмите значок `</>` в заголовке файлов — **Открыть в Neutral IDE**. Запускается `artifacts/neutral-ide/runtime/NeutralIDE.exe`, со своим профилем, расширениями и shared storage. Установленный VS Code не ищется и не используется. Команда **Neutral: Агент** открывает собственную боковую панель.

Перед первым запуском из исходников:

```powershell
.venv-test/Scripts/python.exe prototypes/neutral-ide/prepare.py
npm run build
npm start
```

Повторная подготовка из проверенного ZIP без сети: `prepare.py --offline`.
Нужны Python с httpx, Node/npm и Windows x64. Runtime локальный, не включён в прежний установщик. Скрипт сохраняет upstream лицензии и проверяет зафиксированный SHA-256; это продуктовый прототип на публичной сборке VSCodium, а не результат собственной компиляции всего Code-OSS.

В IDE доступны вкладки, split, поиск, терминал, Git и штатный менеджер Open VSX/VSIX. Проверенная матрица находится в `extensions.lock.json`; установщик тестовых расширений работает только с `.test-data/neutral-ide`. Он не заполняет рабочий профиль пользователя.

```powershell
.venv-test/Scripts/python.exe prototypes/neutral-ide/install_test_extensions.py
.venv-test/Scripts/python.exe prototypes/neutral-ide/test_host.py
.venv-test/Scripts/python.exe prototypes/neutral-ide/test_host.py --ui
node tests/electron/run.cjs neutral-ide-smoke.cjs
```

`--ui` проверяет настоящий модальный диалог в обычном development host: VS Code специально отказывается показывать modal в Extension Test Mode. CDP и отключённый Workspace Trust применяются только к одноразовым тестовым проектам. Рабочий запуск сохраняет стандартную проверку доверия и не открывает CDP.

Команда **Neutral: Предпросмотр правки (прототип)** проверяет editor-owned edit: сохранённый UTF-8 файл до 256 КиБ → diff → явное подтверждение → несохранённый буфер → Ctrl+Z. Версия документа, SHA-256 буфера и диска перепроверяются; внешняя правка и dirty buffer отклоняются. Это проверка адаптера редактора. Модель Core пока не передаёт сюда свои предложения.

Ядро, история и генерация остаются в главном Neutral. Именованный канал разрешает только `status` и `focus`; модельные ключи, произвольные RPC и операции записи не экспортируются. Полное подключение approval/run/revision/working copy — обязательная следующая работа, прежде чем менять IDE по умолчанию. Подробности — [глава 73](../../docs/73-neutral-ide-prototype.md).
