# Agent readiness audit — 2026-10-29

Scope: the existing Neutral 7.0.1 checkout in `LocalAgent`. The sibling legacy
checkout is excluded. A large pre-existing dirty working tree is preserved;
this audit does not reset, publish or package those changes as a release.

## Initial architecture review

The active desktop path is Electron `main.ts` → isolated `preload.ts` IPC →
React `App.tsx`/`useTaskSession.ts` → newline JSON Python `bridge.py` →
`TaskService` → run-owned `RunSession`/`TaskExecution` → `AgentEngine`.
`ModelClient` streams chat/responses requests through `RequestBudget` and the
inference scheduler. `ToolExecutor` validates calls, journals intent/results,
requests approvals and applies revision-checked workspace edits. Results return
to the canonical transcript before the next request. SQLite stores checkpoints,
chat data, runs and attempt accounting; the project index is a separate cache.

| Area | Initial finding / verification status |
| --- | --- |
| Desktop build | TypeScript and Vite/Electron build passed in this audit. Runtime still pending. |
| Main execution | Integrated native/JSON loop, bounded transport retries and checkpoint recovery exist. Deterministic final verification occurs **after** the continuation loop: investigate failed-test recovery first. |
| Completion | Model completion assessment is advisory. Existing verifier accepts a final answer with no command evidence; inspect how unverified edits are presented. |
| Permissions | Existing executor, approvals, workspace policy, snapshots and revision checks are active. Preserve these boundaries; exercise denial/revocation and restart. |
| Resource control | Local auto uses an unbounded iteration generator. Manual/external execution has several elapsed-time checks; approval waits require regression coverage. |
| Subagents | Existing readonly `ChildExecutor` uses the same engine and scheduler, revalidates source hashes and limits fan-out/depth. Verify failure handback, cancellation and parent continuation. |
| Context | `ContextManager` projects history; `RequestBudget` is the final transport gate. `ContextBuilder` supplies source hashes/ranges; JSON automatic packs are intentionally disabled after earlier measured quality regression. |
| Index | Incremental SQLite cache/watchfiles, policy checks and explicit rebuild/fallback exist. Overflow/corruption recovery and live source checks need executable validation. |
| Unsaved files | Current design uses saved sources plus editor dirty guard. Buffer overlays are not implemented. |
| Memory | Structured project summaries exist, but are not a hash-validated source of current code facts. |
| GUI state | Existing run state/plan stages and background run registry are separate concepts. Check final-result display and approval/resume controls against real events. |
| Tests/CI | Extensive unit, HTTP/Core and Electron fixtures exist. Initial Python launch hit sandbox temporary-directory ACL errors; that run is invalid evidence of product failure. Retrying with isolated writable TEMP and profile. |

## Execution priorities

1. Establish valid isolated unit/HTTP/GUI baselines and preserve logs.
2. Reproduce early completion after failed/stale checks, then integrate bounded
   evidence-driven recovery into the existing loop. Keep unknown effects and
   rejected approvals out of automatic replay.
3. Verify approval wait timing, cancellation and resumable checkpoints; fix
   confirmed defects without adding another lifecycle or budget manager.
4. Exercise A–I with deterministic providers and disposable repositories;
   cover native and strict JSON paths, long tasks, readonly children and context
   pressure. Probe available local models separately.
5. Launch the desktop, exercise J, inspect screenshots and repair confirmed UI
   defects while retaining the design.
6. Run regression/build/documentation checks and publish measured results and
   explicit UNVERIFIED limitations in the accompanying readiness documents.

This is the initial audit, not a claim that roadmap milestones or existing tests
prove everyday autonomy. Final evidence is recorded in AGENT_READINESS_RESULTS.md.

## Stabilization checkpoint

The prioritized vertical fixes were implemented in the existing engine, context
projection and executor. Deterministic A–I, a built desktop smoke, and real native
and JSON LM Studio desktop tasks have executed. The user's reported subagent
denial was traced to a Chat conversation with no project, then covered with
mode-aware capability hints and real parent-child handback. Full results and
retained failures are in [AGENT_READINESS_RESULTS.md](AGENT_READINESS_RESULTS.md);
[AGENT_KNOWN_LIMITATIONS.md](AGENT_KNOWN_LIMITATIONS.md) records untested providers,
packaging, host skips and the next quality experiments. No release was made.
