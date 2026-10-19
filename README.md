# Local Coding Agent v5.8

Windows local coding agent with a Cursor-inspired IDE shell, persistent task runtime, Skills/MCP architecture, OpenAI-compatible providers and an optional embedded llama.cpp/ GGUF runtime.

## v5.8 highlights

- Cursor-inspired workspace: activity bar, project explorer, editor, agent chat, inspector and bottom Output/Terminal/Problems panel.
- Local Model Manager for GGUF models.
- llama.cpp `llama-server` can be launched by the application itself; the Agent Core still talks through the same OpenAI-compatible interface.
- CUDA GPU layers and CPU offload are exposed through `GPU layers` (`-1` means all available layers).
- Remote/LM Studio providers remain supported.
- Existing sandbox, file permissions and explicit write approval are unchanged.
- Existing persistent chats, project memory, task checkpoints, diff viewer, editor and Skills/MCP architecture are retained.

## Local models

1. Obtain a compatible `llama-server` build and place it on PATH or select `llama-server.exe` in **Model → Model Manager**.
2. Import a `.gguf` model.
3. Select it and press **Запустить выбранную модель**.
4. The application switches its OpenAI-compatible endpoint to the local runtime and refreshes `/v1/models`.
5. Stop the runtime from Model Manager when finished.

The runtime is intentionally separated from Agent Core. The next backend can therefore be added without changing planner, tools, sandbox or permissions.

## Install

```text
python -m pip install -r requirements.txt
```

Run `run.bat` on Windows.

## Validation

The release includes unit tests for sandbox/security, chat history, task checkpoints, editor IO, runtime architecture and the v5.8 model manager. GUI/runtime integration requires a Windows environment with PySide6 and a llama.cpp build.
