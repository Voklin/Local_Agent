# Local Coding Agent v6.0 — Electron agent bridge

For the detailed Russian learning guide, architecture and source reference, see [the project handbook](docs/README.md).

The Electron + React interface now runs the existing agent engine through a threaded Python JSON-lines service. The original PySide6 application remains available through `run.bat`.

## Windows setup

Use Node.js with npm and Python 3.11+ (validated with Python 3.12).
From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-core.txt
npm ci
.\run-desktop.bat
```

`run-desktop.bat` uses `.venv\Scripts\python.exe` when present. Alternatively set `LCA_PYTHON` to the full path of your Python executable and run `npm run dev`.

1. Open a project folder.
2. Open model settings, enter the OpenAI-compatible server URL (default LM Studio URL: `http://127.0.0.1:1234/v1`), and click **Загрузить модели**. A model ID can also be entered manually.
3. Send a task in the agent panel.
4. Review each proposed file diff and choose **Применить изменение**, **Отклонить изменение**, or **Отменить задачу**.

The server URL and selected model are saved outside the project and restored on restart. Use **Сохранить настройки** after editing them, or **Загрузить модели** to discover and save a model. The API key stays only in process memory and must be re-entered after restarting.

## Available behavior

- Existing tool loop: list files, read files, search text, propose file writes.
- Project-scoped paths and existing security checks.
- Explicit approval per write, correlated with a unique run and proposal ID. No direct file-write or terminal API is exposed to the renderer.
- Background tasks keep bridge commands responsive while waiting for the model or approval.
- Chat history, project memory, and task checkpoints use the existing application stores outside project folders.
- Chat history is filtered to the selected project. Paused tasks can be resumed; interrupted processes are detected when reopening a chat.
- Assistant text appears incrementally while the model generates it. The final answer replaces the streaming bubble instead of duplicating it.
- Stop requests cancel pending approval and active HTTP requests, including requests waiting for response headers or more stream data. The displayed partial answer and paused task are retained for recovery.
- Renderer isolation, narrow preload API, sender validation, and blocked external navigation/window creation.
- Electron/Python failures are surfaced; after a Core failure choose the project again and reopen the saved chat.

The PySide6 app needs the full `requirements.txt`. Qt is not required for Electron's Python Core. This is a development build; distributable packaging is still pending.

## Validation

```powershell
npm run build
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/migration -v
```

The original tests include Qt adapter checks, so install `requirements.txt` to run every check. Migration tests use a local HTTP model fixture and do not require a running LM Studio server. They validate real streamed tool calls and text, explicit approvals, rejection, socket-level cancellation, chat persistence, task recovery, settings persistence without keys, and the JSON-lines child process.

For the hidden real Electron smoke test, build the app, run `npm exec --workspace apps/desktop vite -- --host 127.0.0.1 --port 5173`, then in a second terminal set `LCA_PYTHON` and run:

```powershell
.\node_modules\electron\dist\electron.exe tests/electron/smoke.cjs
```

The smoke test checks file approval, incremental text without duplicate messages, settings restoration after a window reload, and stopping a stalled stream. It uses a temporary project and local model fixture. It writes its result and screenshots under `.test-data/electron-smoke/`; it never uses a real project or model service.
