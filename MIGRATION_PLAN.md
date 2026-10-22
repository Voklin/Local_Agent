# Local Coding Agent v6.0 migration plan

## Completed: desktop shell, safe bridge, and agent execution

- Electron main process owns a separate Python JSON-lines process.
- React renderer uses an isolated, narrow preload API.
- `agent/engine.py` contains the existing tool/model loop without Qt imports.
- `agent/worker.py` forwards engine events into Qt signals for the original PySide6 UI.
- `core/python/task_service.py` owns threaded execution, model configuration, project chats, checkpoints, cancellation, and correlated write approvals.
- Chat, task, and project-memory stores remain outside the selected project.
- Per-write Apply / Reject / Cancel UI preserves the existing preview and approval semantics.
- Main-process and renderer TypeScript checks are part of the build.
- Python unit/integration tests and a hidden real Electron smoke test cover the migration.

## Next milestones

1. Add distributable Windows packaging with the Python Core bundled.
2. Persist non-secret model preferences and integrate a credential store for optional API keys.
3. Improve streaming text presentation and immediate cancellation of network requests.
4. Restore remaining editor and change-review features incrementally.

## Security constraints

- `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`.
- No arbitrary IPC forwarding or generic shell access.
- Resolve file paths inside the selected project, including symlink targets.
- Every agent write requires a matching, explicit approval for the active proposal.
- Reject project/chat/configuration changes while a task is active.

See `README_V6_MIGRATION.md` for setup, validation, and current limitations.
