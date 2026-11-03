# Agent readiness results — 2026-10-29

Scope: Neutral 7.0.1 development checkout, Windows x64, Python 3.12, built
Electron/React desktop, actual LM Studio localhost server with `ornith-1.5-9b`.
LM Studio reported GGUF Q5_K_M, 7,564,249,248 model bytes and a loaded context of
50,176 tokens. No model/server settings or user projects were changed.

The existing dirty working tree was preserved. These results describe this
combined checkout, not a clean published commit or a new installer.

## Confirmed defects and corrections

| Initial failure | Root cause | Correction and executable evidence |
| --- | --- | --- |
| Failed configured test ended the task without repair | Automatic checks and final deterministic verification ran after the continuation loop | Checks/verification now feed actual failure receipts into the existing loop; unchanged evidence gets bounded recovery. The fixture goes from exit 1 to correction to exit 0. |
| A configured check never ran if no files changed | Automatic verification was gated on write events | Explicit configured auto checks run before completion even with no edits; successful current checks are not repeated. |
| Denied command could lose meaningful status/re-prompt | Results without an exit code were not retained as command evidence | Preserve all command outcomes in verifier/recovery, suppress a denied command's repeated argv/cwd identity in the current run; do not replay denied or uncertain effects. |
| Human approval could consume execution deadline | Independent elapsed-time checks and timer treated approval as inference | Shared OperationContext pauses nested deadlines during approvals; watchdog follows remaining execution time; Stop still propagates immediately. |
| Approved cwd could be replaced before process launch | Folder was resolved before the human wait | Resolve and compare directory identity again after approval; replacement regression proves no process started. |
| Long task failed at context boundary | Archive size omitted JSON escaping/message envelope | Existing smart compaction now budgets serialized archive messages. 24 large reads complete while preserving the original goal and canonical receipts. |
| JSON continuation saw inconsistent assistant history | Decoded final answers were replayed as plain text despite the required JSON wire protocol | Restore final envelopes in the transport projection, keeping examples as text and canonical history intact. Strict parsing, two protocol retries and the approval boundary are unchanged. |
| Model said Neutral had no subagents | The observed real conversation was Chat with empty project_root; prompt did not distinguish current mode from product capability | Explain IDE/project prerequisites; enabled tools are discoverable with Russian `субагент`; explicit subagent requests retain eligible schemas under RequestBudget pressure. Real desktop delegation and deterministic draft-profile tests verify both paths. |
| Child server failure risked breaking continuation | Failure handback needed vertical coverage | Added real HTTP failure test: bounded child retries return failure data, parent continues, scheduler/ledger reservations release. No replacement child subsystem. |

Local automatic execution retains its existing unbounded turn iterator and
automatic resource management. No global token/time/cycle cap was introduced.
No permission boundary, source revision check or unknown-effect recovery was
removed. Existing task/run states remain authoritative; no duplicate manager,
scheduler, migration or state machine was added.

## Measurements and evidence

All paths below are relative to the checkout and gitignored under `artifacts/`.
Counts include skipped tests; a skip is UNVERIFIED.

| Run | Observed result | Evidence |
| --- | --- | --- |
| Initial unit baseline | 458 tests, 2 skipped, 67.036 s; no failures | `artifacts/readiness/baseline-unit-verified.log` |
| Initial Core/migration baseline | 107 tests, 108.724 s; no failures | `artifacts/readiness/baseline-migration-verified.log` |
| Reproduction before engine fixes | 3 failing readiness cases | `artifacts/readiness/readiness-baseline.log` |
| Focused integrated regressions | 54 tests passed, 40.034 s | `artifacts/readiness/focused-2.log` |
| Readiness A–I runner | 76 tests, 1 skipped, 75.197 s; no failures | `artifacts/readiness/scenarios.json`, `scenarios.log` |
| Full unit suite before JSON history correction | 463 tests, 2 skipped, 70.000 s; no failures | `artifacts/readiness/final-unit.log` |
| Final unit suite including JSON history correction | 464 tests, 2 skipped, 66.691 s; no failures | `artifacts/readiness/final-unit-json.log` |
| Final Core/migration suite | 119 tests passed, 135.727 s | `artifacts/readiness/final-migration.log` |
| TypeScript/Vite/Electron build | Passed | `artifacts/readiness/final-build.log` |
| Deterministic desktop J | Passed; initial 25, final 23 physical model fixture requests | `artifacts/readiness/gui-studio-fixed.log`, `final-gui.log`, `.test-data/studio-smoke/result.json` |
| Real native desktop J/F/B/G | Passed in 61.603 s; 6 parent turns, 7 parent tool calls, one completed readonly child; one patch and one command approval | `artifacts/readiness/live-gui/report.json`, `events.json`, `completed.png`, `approval-*.png` |
| Real JSON desktop after history correction | Passed in 78.487 s; 10 parent turns, 9 parent tool calls and one completed readonly child | `artifacts/readiness/live-gui-json/passed-after-json-history.json`, `passed-after-json-history-events.json` |
| Final real JSON desktop and visual capture | Passed in 109.615 s; 12 parent turns, 10 parent tool calls, completed child and current passing checks | `artifacts/readiness/live-gui-json/report.json`, `events.json`, `completed.png` |
| Real native multi-file desktop C/D/F/G | Passed in 141.512 s; 7 parent turns, 7 parent tool calls, completed readonly child, 3 approved patches across 2 files and 2 approved test runs | `artifacts/readiness/live-gui-multifile/report.json`, `events.json`, `completed.png` |
| JSON continuation regressions after the live failure | 55 tests passed, 28.238 s | `artifacts/readiness/json-regression.log` |
| Final child/readiness regressions after mode-hint refinement | 23 tests passed, 38.524 s | `artifacts/readiness/final-child-readiness.log` |
| Documentation | 101 Markdown documents; generated references and local links validated | `artifacts/readiness/final-docs.log` |
| Historical live native benchmark | 2/3 correct (exploration, bugfix); multi-file incomplete at experiment limit; 48.377 s total | `artifacts/readiness/live-ornith-native/report.json` |
| Historical live JSON benchmark | 1/2 correct (exploration); bugfix safely stopped on manual context budget; 16.339 s total | `artifacts/readiness/live-ornith-json/report.json` |

The first real GUI attempt repaired the source and passed the independent oracle,
but the harness incorrectly rejected the built-in Electron Node runtime because
it only allowed `node.exe`. It is recorded as a failed harness attempt
(`live-gui/attempt-denied-by-harness.json`), not a successful end-to-end run.
The allowlist now admits the exact built-in runtime with only `verify.js` in the
disposable cwd. That exposed repeated-denial behavior which received a regression
and executor fix. The second native GUI attempt passed the complete acceptance.

The first JSON desktop attempt repaired the source and passed its tests, but
paused after exhausting two strict format repairs for the final response. This
failure remains in `live-gui-json/attempt-format-failure.json` and
`attempt-format-events.json`. After restoring final JSON envelopes in model-facing
history, the same end-to-end acceptance passed. This is evidence of a useful
correction, not proof that every future malformed model response is recoverable.
The passing JSON run also encountered a real failing test before the repair and
then succeeded on the corrected source.

The final repeat also passed after the readonly capability hint was narrowed.
Its screenshot was captured after renderer frame synchronization and visually
inspected: completed task/child, exit 0, current source snapshot and ready status.
The retained native inspection process was closed; the user's LM Studio was left
running. No installer was rebuilt or published. Start this built checkout with
`npm start` from the repository root to use these source changes; an older
installed executable does not receive them automatically.

The final native multi-file task used auto mode and the actual loaded context.
The parent renamed `total` to `calculateTotal` in the export and caller, then
corrected the tax coefficient after the first test exposed the remaining bug.
Both edited files have approved applied diffs; the unchanged independent test
confirmed the new API, removal of the old export and correct invoice behavior.
The visible completion panel shows two changed files, three operations, a
completed child and current command evidence. This closes real multi-file and
failed-test recovery coverage for this fixture; it does not erase the historical
small-window Python benchmark failure or establish arbitrary repository quality.

`git diff --check` passed after removing one existing whitespace-only defect.
Documentation checks passed with 101 Markdown files and 4,061 local links.

## Scenario outcome

A–I passed their deterministic expectations except host-unavailable symlink tests.
The real native desktop scenario confirmed model selection, project selection,
streaming continuation, parent/readonly child handback, inspectable diff approval,
actual test output, current verification evidence and completion. The independent
oracle confirmed 20% totals (100 → 120 and 0 → 0) and that the model did not rewrite
the test. Cancellation/restart was exercised with deterministic providers, not a
live-model process kill. The native screenshot visibly shows the completed child,
successful check with exit 0 and current source witness.

The live benchmark failures remain recorded. Build success and a successful small
GUI task are insufficient to certify general model quality or all configurations.
See [test procedures](AGENT_READINESS_TESTS.md) and
[known limitations/reproduction](AGENT_KNOWN_LIMITATIONS.md) for scope and next work.
