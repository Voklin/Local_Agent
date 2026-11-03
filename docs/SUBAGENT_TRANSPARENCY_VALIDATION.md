# Subagent transparency and real-model validation — 2026-10-29

Implemented in the existing task snapshot and details drawer:
- Child checkpoints publish cycle, tool count and the last 40 tool activity records (tool, path, status, summary). No private reasoning or raw file bodies are added.
- Expand a child under Details → Overview and subagents → Work progress to inspect its actions during execution and after completion/cancellation.
- Main tool calls no longer appear in the conversation. Details → Tools contains their expandable journal. Recovery controls remain in Overview.
- Existing executor permissions, readonly child restrictions and serial inference scheduling are unchanged.

Validation:
- TypeScript/Electron production build: PASSED (`artifacts/readiness/transparency-build.log`).
- Child HTTP regressions: 13 tests PASSED, 27.233 seconds, including propagated action records (`transparency-child-final.log`).
- Documentation/reference checks: PASSED.
- Real LM Studio native multi-file desktop experiment: FAILED at the 180-second experiment watchdog (184.390 seconds overall). A readonly child successfully read README.md and verify.js, then remained in inference on cycle 2. No edit/command approvals occurred. UI cancellation propagated, preserved a paused checkpoint and retained both successful read activities. This is a test cutoff, not a new application execution limit.
- Real-model evidence: `artifacts/readiness/transparency-validation.log` and `artifacts/readiness/live-gui-multifile/report.json` / `events.json`. Earlier dated reports remain separate evidence; they do not turn this attempt into a pass.

Scope: actual desktop/Core/LM Studio with an isolated representative coding fixture, not an arbitrary production repository benchmark. Current sustained model completion is NOT established by this attempt. Repeat with the model idle and inspect provider latency before attributing the stall to the agent. Live raw token-by-token child output and pagination beyond the snapshot activity tail are not implemented.

Final deterministic Electron GUI smoke: PASSED (artifacts/readiness/transparency-smoke-final.log). Includes the relocated recovery journal, child completion, approvals, cancellation and persistence workflows.

## Follow-up — 2026-11-01

LM Studio was reachable with no models loaded. Loaded Qwen2.5-Coder 7B Q5_K_M under `neutral-validation-7b`, 32,768 context, full GPU offload, one prediction at a time. One JSON multi-file GUI experiment failed in 105.020 seconds. The child repeatedly read total.js; ProgressGuard performed its diagnostic attempt and paused it. The parent continued but did not complete the rename and eventually paused for repeated results. The independent caller oracle rejected the outcome. No success is inferred from a final model message.

Evidence: `artifacts/readiness/validation-2026-11-01.log` and `live-gui-json-multifile/report.json` / `events.json`. The child snapshot retained nine action records. This is evidence of unproductive model behavior, not proof of the cause of the earlier Ornith delay. Qwen was unloaded before a single native Ornith control experiment; no parallel heavy model runs were started.

Native control result: PASSED in 101.333 seconds with Ornith 1.5 9B Q5_K_M (`neutral-validation-native`), 32,768 loaded context, full GPU offload, one prediction at a time. Parent completed 10 cycles and 11 tool calls. The harness required a completed readonly child, applied diffs in both source files, unchanged requirements and oracle, independent passing behavior/API assertions, no tool journal inside chat, and a working Details → Tools tab. Evidence: `artifacts/readiness/validation-native-2026-11-01.log`, `live-gui-multifile/report.json`, `events.json`, `tools-tab.png` and `completed.png`.

The earlier 180-second Ornith stall did not recur in this configuration. Its root cause remains UNVERIFIED; do not infer a fix merely from changing context/parallelism or getting one passing trial. The server emitted one SDK unknown-call diagnostic during startup; the end-to-end acceptance still passed. No production engine limits or permissions were changed. Ornith remains loaded for the user under the above API identifier; the previous Qwen test instance was unloaded. This session used two sequential model experiments and did not rerun the entire test matrix.

Next acceptance: an isolated copy of an actual repository with independently reproduced failing tests. The synthetic multi-file GUI fixture is now confirmed with the new transparency interface, but that broader repository acceptance remains UNVERIFIED.
