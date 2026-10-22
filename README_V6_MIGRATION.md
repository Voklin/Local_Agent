# Local Coding Agent v6.0 — Electron agent bridge

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

The API key and model connection settings stay in process memory for the current session. Re-enter them after restarting the app or Python Core.

## Available behavior

- Existing tool loop: list files, read files, search text, propose file writes.
- Project-scoped paths and existing security checks.
- Explicit approval per write, correlated with a unique run and proposal ID. No direct file-write or terminal API is exposed to the renderer.
- Background tasks keep bridge commands responsive while waiting for the model or approval.
- Chat history, project memory, and task checkpoints use the existing application stores outside project folders.
- Chat history is filtered to the selected project. Paused tasks can be resumed; interrupted processes are detected when reopening a chat.
- Stop requests cancel pending approval. An in-flight model request can take up to the existing 180-second network timeout to stop.
- Renderer isolation, narrow preload API, sender validation, and blocked external navigation/window creation.
- Electron/Python failures are surfaced; after a Core failure choose the project again and reopen the saved chat.

The PySide6 app needs the full `requirements.txt`. Qt is not required for Electron's Python Core. This is a development build; distributable packaging is still pending.

## Validation

```powershell
npm run build
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/migration -v
```

The original tests include Qt adapter checks, so install `requirements.txt` to run every check. Migration tests use a local HTTP model fixture and do not require a running LM Studio server. They validate real streamed tool calls, explicit approvals, rejection, cancellation, chat persistence, task recovery, and the JSON-lines child process.

For the hidden real Electron smoke test, build the app, run `npm exec --workspace apps/desktop vite -- --host 127.0.0.1 --port 5173`, then in a second terminal set `LCA_PYTHON` and run:

```powershell
.\node_modules\electron\dist\electron.exe tests/electron/smoke.cjs
```

The smoke test uses a temporary project and local model fixture. It writes its result and screenshots under `.test-data/electron-smoke/`; it never uses a real project or model service.
