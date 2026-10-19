# Local Coding Agent — Sandbox Edition

Windows GUI prototype: PySide6 + OpenAI-compatible local API (for example `llama-server`).

## Start

1. Keep `llama-server` running at `http://127.0.0.1:8080`.
2. Extract this folder somewhere writable.
3. Run `run.bat`.
4. In the GUI set Base URL to `http://127.0.0.1:8080/v1`, API key to `no-key`, and Model ID to the exact ID returned by `/v1/models`.
5. Select the project directory with **Browse…**.
6. Click **Test sandbox**, then **Test connection** and **Test tool calling**.

## Sandbox guarantees in this prototype

- All current file tools (`list_files`, `read_file`, `search_text`) resolve requested paths and reject paths that escape the selected project root.
- `..` traversal, outside absolute paths, and symlink/junction paths that resolve outside the root are rejected.
- The sandbox self-test uses temporary folders and does not create files in the user's project.
- The model does not get arbitrary filesystem access directly; tools enforce the boundary in Python.
- The GUI's selected root is the root passed to the tool dispatcher.

## Run tests

```powershell
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Or use **🔒 Test sandbox** inside the GUI.

## Important security limit

This is an application-level path sandbox for the current file tools, not a complete OS sandbox. No shell, write, delete, or Git tools are enabled in this version. Before adding any such tool, enforce the same root policy and add explicit confirmation/allowlists for commands and destructive actions. A future shell tool cannot be secured by checking only `cwd`; commands may access absolute paths or launch other programs. For stronger isolation, run the agent in a restricted Windows account/container/VM.
