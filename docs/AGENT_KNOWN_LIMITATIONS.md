# Agent known limitations — 2026-10-29

The tested development build is usable for the recorded workflows. This is not a
claim of production readiness or of reliable completion of arbitrary development
requests. See [measured results](AGENT_READINESS_RESULTS.md).

## Confirmed limits and reproduction

1. **Model quality remains variable.** Ornith 1.5 9B passed the real native desktop
   repair with a readonly child and real tests. In the historical native multi-file
   benchmark it changed a declaration/import, then proposed incorrect caller text
   and an invalid short SHA256. The guards rejected those proposals and the
   10-turn experiment stopped before all references were repaired. Reproduce with
   `tools/benchmark_agent.py --out <new-directory> --model ornith-1.5-9b
   --protocol native --sizes small --cases multifile --live`. That benchmark uses
   a manual 8,192-token window; it does not measure unrestricted auto mode.
   A separate real desktop multi-file rename/repair passed in auto mode in
   141.512 s, including recovery from a failing test. It is a different JavaScript
   fixture with two source files, not a rerun of the exact Python benchmark.
2. **Small manual context can block a task.** The real JSON bugfix benchmark hit
   RequestBudget at 6,527 input + 1,536 output + 256 reserve > 8,192 tokens.
   No oversized HTTP request was sent and no mandatory instructions were cut.
   Reproduce with the same benchmark, `--protocol json --cases bugfix`. Use the
   actual loaded context in auto mode or explicitly configure sufficient manual
   space. A protected prompt/code handoff larger than the window still fails
   safely rather than losing requirements.
   A first real JSON desktop run also failed final formatting after executing
   correct work. Consistent JSON history fixed the observed repeat; malformed
   output still has only two safe regeneration attempts before a recoverable
   pause. It is never scanned for embedded command examples or executed loosely.
3. **Subagents are a project/IDE capability.** Chat without a workspace has no
   file/delegation tools. Open a project in IDE and enable Settings → Extensions
   → Subagents. `delegate_readonly` starts an enabled profile; the model may also
   propose `create_subagent_profile`, but generated profiles are disabled until
   the user enables them. Existing fan-out/depth guards and serial heavy local
   inference remain. Children cannot run commands or change files.
4. **Verification is scoped evidence.** Exit 0 confirms the executed command on
   its recorded source witness, not all possible acceptance criteria. With no
   configured checks or tests run, the UI must retain an unverified assessment.
   The agent cannot prove a requirement that has no executable or human check.
   Explicit denial/unknown effects can require a new user decision or recovery
   action. The same denied command is suppressed within its current run.
   When a model runs a configured command without its `check_id`, its result and
   the configured check can remain separate and the command can be proposed
   again. This was observed in JSON GUI runs. Exact configured checks with
   current witnesses are deduplicated; merging scopes or identities speculatively
   would weaken the existing evidence contract and was not introduced here.
5. **Saved files are the source of truth.** Unsaved editor buffers use the existing
   dirty guard; they are not indexed as a second overlay. Save/reconcile them
   before agent work. Corrupt/overflowed indexes expose recovery and verified
   fallback; a full rebuild can still be expensive for a large workspace.
6. **Process execution is not an OS sandbox.** Approved commands run with the
   user's process privileges; cwd/argv checks, no shell invocation, approval and
   cancellation do not prevent a program itself from reading/writing elsewhere.
   The optional container path was not validated with a live container here.
   Cwd is rechecked after approval; a hostile filesystem process racing after
   that check is not eliminated by an OS-level capability boundary.
7. **Memory is advisory.** Project summaries and child narrative conclusions are
   not executable proof. File hashes/source ranges, actual tool receipts and
   current tests take precedence. One live native run's optional memory response
   reached its output limit; the completed coding task was preserved.

## UNVERIFIED in this audit

- Live remote OpenAI/Responses APIs, live Ollama and a separate llama.cpp server.
  Deterministic protocol/transport tests do not substitute for those providers.
- Other real models, quantizations, repeated statistical quality trials and
  multi-hour production tasks across large real repositories.
- Windows symlink creation in this host's test permissions: related tests skip.
  Other path traversal, policy revocation and revision-conflict tests passed.
- Fresh installer/frozen Core packaging of these new changes and clean-machine
  installation. The source-built Electron renderer and Python Core were used.
- Full accessibility coverage, every display scale, all GUI states and native
  desktop automation: the computer-use inventory did not expose the isolated
  Electron window. Real Electron renderer captures and automated UI interactions
  were inspected instead.
- Isolated VRAM/CPU peak profiling, stress-level SQLite contention and throughput
  guarantees. Timings here are single runs and include other test activity.

## Next evidence to collect

Repeat the failing rename task in auto mode on several models with an immutable
reference oracle; measure success, retries and tool cost. Expand long-running
real-model tasks with interruption mid-command, provider disconnect and external
edits. Run Windows symlink/junction cases where those capabilities are available.
Then validate a locally built frozen Core/installer before any authorized release.
Keep the current executor, access policy and budget gates intact throughout.
