# Local Coding Agent v5.6.7 — Adaptive Limits

Windows GUI local coding agent. Based on the user's confirmed working v5.6.6.

## What's new

- Higher limits for long coding tasks: up to 500 model cycles, 10,000 tool calls, 32,768 response tokens, 500,000 context characters, and 24 hours per task.
- Settings profiles: **Большой проект** and **Длительная задача**.
- Live model context is compacted between model requests while the canonical conversation transcript remains intact for chat history.
- Tool-call/result pairs are preserved during context compaction.
- Runtime limit and repeated identical tool-call loop detection.
- Tool-call limit returns explicit tool results instead of leaving dangling tool calls in the transcript.
- Existing sandbox, allowed-root restrictions, write approval, editor, Diff Viewer, memory, and model selection remain in place.

## Run

1. Extract the ZIP to a new folder.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Run `run.bat`.
4. Open Settings → choose **Большой проект** for normal large repositories or **Длительная задача** for extended tasks, then save.

## Validation

- `python -m py_compile agent/*.py main.py` — passed.
- `python -m unittest discover -s tests -v` — 27 passed, 1 skipped because PySide6 is unavailable in the build environment.
- The GUI was not launched in this build environment; please verify it on Windows with your LM Studio model.
