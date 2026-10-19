# Local Coding Agent — v5.6 Code Editor Edition

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

## Configurable limits (v3 prototype changes)

The GUI now exposes these limits in **Agent limits (saved automatically)**. Values are persisted in Windows user settings via Qt `QSettings`:

- Maximum tool calls per request (default 10).
- Maximum consecutive tool errors (default 3).
- Maximum tokens per model response (default 2048; sent as `max_tokens`).
- Maximum entries in one file listing (default 200).
- Maximum recursive search/listing depth (default 5).
- **Stop** requests cancellation of the streaming model response and prevents further tool execution when the stream can be closed.

The worker also retains a hard cap of 8 model rounds. The token limit applies to each model response, not as a single cumulative token budget for the entire conversation turn. Streaming/cancellation support depends on the local OpenAI-compatible server implementation.

Run all automated tests:

```powershell
python -m unittest discover -s tests -v
```

## File editing (v4 prototype)

- Added `write_file` tool for UTF-8 text files inside the selected project.
- Before any write, the GUI shows the proposed path and a unified diff and requires explicit Yes/No approval. No is the default.
- Replacing an existing file also requires the model to set `overwrite=true`, followed by the same GUI approval.
- The dispatcher rejects writes unless its caller explicitly marks the operation as approved.
- Parent directories must already exist. Creating directories, shell execution, deleting files, and Git actions remain disabled.
- Writes are limited to 1 MB and use a temporary file plus atomic replacement. Existing files over the read/preview limit or non-UTF-8 files are refused.
- These protections are application-level controls, not a complete Windows OS sandbox. Review the diff before approving any change.

Run all tests after updating:

```powershell
python -m unittest discover -s tests -v
```

## v4.2 — Conversation history fix

- The agent now sends prior chat turns with each new user message, rather than sending only the latest message.
- Tool-call assistant messages and tool results are retained in the conversation context.
- Added a **New chat** button to clear the current in-memory conversation deliberately.
- The connection/tool-calling diagnostic runs without using or overwriting the normal chat history.
- Chat history is held in memory for the current app session; it is not persisted after closing the app.

Run regression tests from the project directory:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```


## v4.3 — GUI approval buttons
- File changes are approved with **Применить / Отклонить / Отмена**.
- No confirmation message needs to be typed in chat.
- **Применить** continues the current agent turn.
- **Отклонить** returns a tool result to the model so it can adapt.
- **Отмена** stops the current operation.


## v5 — Project workflow + persistent chat history

- Persistent chat history stored in `%LOCALAPPDATA%\LocalCodingAgent\chats`.
- Open previous chats from the GUI.
- Rename and delete chats.
- Each chat stores model messages/tool context, project directory and model ID.
- Reopening a chat restores the conversation context sent to the model.
- Chat history is stored separately from project files; the agent never copies project files into chat storage.
- File changes still require the v4.3 GUI approval dialog.

## v5.3 — Multi-file Diff Center + Batch Review

- Added a persistent **Центр изменений** in the right inspector.
- Every proposed file change is tracked with path, status and unified diff.
- Diff lines are visually distinguished for additions, removals and hunks.
- Select any change to inspect its diff without reopening the approval dialog.
- Added **Применить всё** and **Отклонить всё** approval actions. These apply only to subsequent file proposals in the current agent run and do not modify the sandbox/security rules.
- Added **Копировать diff** and **Очистить** controls.
- Existing explicit per-file approval remains the default.
- Sandbox, path validation, overwrite checks and atomic writes are unchanged.

### v5.3 safety model

`Применить всё` does not grant permanent write access. It is a temporary batch decision held only by the current `AgentWorker` run. A new request starts with no batch approval.


## v5.4 — Project Memory Engine

- Keeps conversation history separate from compact, structured long-term project memory.
- Stores memory per project outside the project directory in `%LOCALAPPDATA%\LocalCodingAgent\project_memory`.
- Adds project summary, current focus, next steps, decisions, constraints, conventions, and important-file notes.
- Injects a bounded memory snapshot into the system context; notes are explicitly treated as fallible reference data, not instructions.
- Sends only the newest complete conversation turns (bounded to a context budget) to the model instead of replaying the full transcript on every request; the full transcript is still preserved in chat history. Large tool outputs are clipped only in model context, not in saved history.
- Optionally updates memory after a successful response using a separate short model call. The memory updater receives the current request, final answer and tool metadata, but not raw file contents or tool results.
- Adds a **Память проекта…** dialog to inspect/edit the JSON memory or clear only the current project's memory. Chat history remains intact.
- Auto-update can be disabled in Settings. If memory generation fails, the normal agent response is not affected.
- Project memory does not change the sandbox, file access restrictions, or write approval flow.

Run tests: `python -m unittest discover -s tests -v`.

## v5.5 — Built-in Code Editor + UI refinement

- Adds a dedicated **Редактор** workspace alongside the chat, with a project file tree, multi-file tabs, path breadcrumb, in-file search, and a save button (`Ctrl+S`).
- Adds line numbers, current-line highlighting, a dark code-focused theme, and lightweight syntax coloring for common programming text.
- Supports UTF-8 text files up to 2 MB; binary/non-UTF-8 and oversized files are refused.
- The editor only opens and saves paths validated against the selected project root. The project tree skips common generated/vendor folders and is bounded to a maximum number of entries and nesting depth.
- Switching projects prompts about unsaved editor changes. Closing an edited tab also asks whether to save.
- Selecting a file in the Diff Center can open it in the editor. After an agent run, clean editor tabs reload changed files from disk; unsaved manual edits are left untouched.
- The Diff Center worker events are connected to the UI so proposed/applied/rejected change states populate the list.
- Agent writes still use the existing per-file approval/batch review flow. Manual editor saves are explicit user actions and do not grant the agent extra permissions.
- Added sandboxed editor I/O tests for in-project read/save, outside-path denial, oversized files and refusal to create a new file through the editor.

The GUI could not be launched in the build environment because PySide6 is not installed there. Python syntax checks and the non-GUI regression suite were run; install dependencies with `python -m pip install -r requirements.txt` before launching on Windows.


## v5.6 — Side-by-side Diff Viewer
- Two-panel read-only comparison for agent-proposed changes.
- Original and proposed content are captured in memory at preview time.
- Ctrl+Shift+D opens the selected change comparison.
- Existing sandbox, approval flow, chat history, project memory and editor are unchanged.
