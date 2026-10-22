# Local Coding Agent v6.0

The Electron + React interface is connected to the Python agent engine, with model settings, project chats, task recovery and explicit diff approval before each file write.

See [setup and validation](README_V6_MIGRATION.md). Start the new interface with `run-desktop.bat`; `run.bat` starts the retained PySide6 interface.

# Local Coding Agent v5.6.8 — Task Checkpoints + UI/UX

Windows GUI local coding agent for OpenAI-compatible local servers such as LM Studio.

## What's new in v5.6.8

### Task planner and checkpoints
- Every chat task gets a persistent five-stage plan:
  **Анализ → Исследование → Реализация → Проверка → Завершение**.
- The current stage, model cycle, tool-call count and last event are saved outside the project.
- If the agent is stopped, hits a limit, or fails unexpectedly, the task becomes **Приостановлена** instead of being lost.
- **Продолжить** resumes the task from the same chat and asks the agent to inspect the current project state before continuing.
- **Сбросить** removes only the task checkpoint; chat history remains intact.
- No project source code or raw tool output is stored in the checkpoint.

### UI/UX
- Redesigned workspace hierarchy with clearer chat/project context.
- New persistent task card in the right inspector.
- Stage progress, live status and last checkpoint event are visible while the agent works.
- Resume/reset actions are available without typing confirmation into the chat.
- Existing editor, Diff Viewer, change center, project memory, model selector and diagnostics are preserved.
- Approval workflow remains unchanged: file writes still require explicit GUI approval.
- Sandbox/security rules are unchanged.

## Existing capabilities retained
- Persistent chat history.
- Separate project memory outside project folders.
- Adaptive limits for large/long-running projects.
- Bounded live model context with preserved tool-call pairs.
- File tree, syntax-highlighted editor, line numbers, search, Ctrl+S, go-to-line and reload.
- Side-by-side Diff Viewer with synchronized scrolling and change navigation.
- Automatic model discovery through the OpenAI-compatible models endpoint.
- Sandbox self-tests.

## Run
1. Extract the ZIP.
2. `python -m pip install -r requirements.txt`
3. Run `run.bat`.
4. Configure LM Studio / OpenAI-compatible URL and select a model in Settings.

## Validation
- Python bytecode compilation and unit tests are included in the release validation.
- GUI should be smoke-tested on Windows with PySide6 and a running LM Studio server.


## v5.8.1 — Antigravity-inspired GUI foundation

This release replaces the previous GUI implementation with a new PySide6 shell. The agent backend, tool execution, sandbox/security checks, task runtime, skills, MCP registry, project memory, and approval-before-write flow remain separate and are not intentionally changed.

Current GUI foundation:
- compact activity rail and contextual sidebar;
- project explorer and filename search;
- agent chat with prompt composer;
- chat history list;
- OpenAI-compatible model selector and connection settings;
- file preview;
- Output panel;
- explicit Apply / Reject / Cancel dialog before file writes.

The embedded GGUF runtime and a full editor/terminal workspace are not part of this GUI-only step; they are planned for separate incremental updates.


## v5.8.2 — Agent Studio design applied

This update uses the uploaded `agent_studio.py` as a preserved visual reference and applies its dark IDE visual language to the current Local Coding Agent GUI.

- Blue-accent dark theme and clearer panel hierarchy.
- Activity rail labels/icons and a more legible top bar.
- Multiple read-only file preview tabs, with close/reorder controls.
- The original reference source is retained in `design_reference/agent_studio_reference.py`; see `design_reference/DESIGN_REFERENCE.md`.
- Preview tabs are deliberately read-only. Agent file writes still go through the existing permission checks and explicit approval dialog.

Validation in this environment: Python compilation passed; 32 unit tests passed and 1 GUI approval test was skipped because PySide6 is not installed here. The desktop UI was not runtime-smoke-tested in this environment.
