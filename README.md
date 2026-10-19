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

### UI/UX — minimalist layout
- The right inspector is hidden by default to give the chat and editor more space. Open it with the **Панель** button when you need task progress, changes or diagnostics.
- Narrower project/chat sidebar and a quieter top bar.
- Flatter surfaces, fewer borders and cards, tighter visual hierarchy, muted neutral palette and one restrained accent color.
- Project selection and memory actions are compacted into the sidebar/composer.
- New persistent task card in the optional right inspector.
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
