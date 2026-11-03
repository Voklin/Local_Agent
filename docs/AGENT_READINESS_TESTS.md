# Agent readiness tests

This suite exercises the existing engine, executor, journal, approvals, scheduler,
SQLite persistence and desktop bridge. A deterministic HTTP provider checks
orchestration; it does not establish model reasoning quality. Modification cases
use disposable repositories and isolated profiles. Never point them at user work.

## Repeatable commands

Use Python 3.12 with `requirements.txt` installed and the repository's npm lockfile.
The audit used `.venv-test/Scripts/python.exe`; `python` below must refer to that
environment or an equivalent supported environment.

```powershell
python tools/test_agent_readiness.py
python -m unittest discover -s tests -v
python -m unittest discover -s tests/migration -v
npm run build
npm run test:ui
python tools/generate_code_reference.py
python tools/check_docs.py
```

`npm run test:readiness` aliases the first command. The readiness runner creates a
fresh `.test-tmp/readiness-*` directory, changes TEMP/TMP/LOCALAPPDATA before Core
imports, and writes `artifacts/readiness/scenarios.json`. Its records contain the
expected behavior, status, elapsed seconds and failure traceback. Skips are
**UNVERIFIED**, not passes. The conventional unit/migration commands should also
run with disposable TEMP/TMP/LOCALAPPDATA. On the audited Windows host the managed
sandbox blocked localhost/temporary-directory access; the valid runs used an
approved execution environment. Those environmental failures are not app failures.

## Acceptance scenarios

| Scenario | Expected behavior and executable coverage |
| --- | --- |
| A: exploration | `test_a_exploration_returns_current_source_references`: real read result and source reference returned through HTTP continuation, no writes. ContextBuilder/index tests separately revalidate hashes, revocation, rename, deletion and backdated external edits. |
| B: single edit | `test_b_simple_edit_and_real_test`: approved patch followed by a real Python subprocess assertion; checkpoint records current command evidence. |
| C: multiple files | `test_c_multi_file_json_edit_and_test`: strict JSON renames a definition and import, changes behavior, runs the real assertion. |
| D: failure recovery | `test_d_failed_auto_check_returns_to_model_and_recovers`: first correction is deliberately wrong; exit 1/AssertionError reaches the next request, second correction yields exit 0. An additional case verifies checks run when no edit was necessary. |
| E: sustained work | `test_e_h_long_task_retains_goal_and_uses_full_canonical_history`: 24 distinct reads, original goal present in every request, completed checkpoint, no duplicated reads. Task graph integration tests cover receipt-backed steps and dependencies. |
| F: delegation | `test_child_execution`: real parent → child → parent HTTP requests; isolated readonly schema, source provenance, changed-source rejection, bounded transport failure, cancellation, draft profiles and disabled capability behavior. |
| G: approval | Readiness tests accept/reject file and command previews; a repeated denied command cannot re-prompt by changing purpose/check_id. OperationContext tests simulate nested human waits and cancellation. |
| H: context pressure | E sends roughly 144 KB of fixture source through a 12,000-character working projection; full canonical receipts survive. Smart-context tests additionally enforce serialized JSON size, protected user constraints and tool pairing. RequestBudget remains the final transport gate. |
| I: cancellation/recovery | Cancel at approval, recreate/resume checkpoint, verify unchanged files and no duplicate effects. `test_run_owner_restart` kills a disposable bridge owner and verifies invalidation of old consent, completed read recovery and released locks. |
| J: desktop | `studio-smoke.cjs` exercises renderer → IPC → Core with a deterministic provider. `readiness-live.cjs` uses a real local model, selects workspace/model through UI, delegates research, edits with preview, approves the test and independently checks the resulting fixture. |

## Real model desktop test (opt-in)

Start LM Studio's local server and load a model yourself. This test does not load,
unload or reconfigure models and does not alter the user's Neutral profile.

```powershell
$env:NEUTRAL_TEST_URL='http://127.0.0.1:1234/v1'
$env:NEUTRAL_TEST_MODEL='ornith-1.5-9b'
$env:NEUTRAL_TEST_PROTOCOL='native' # or json
npm run test:readiness:live
# A real multi-file rename plus behavior change with the same permissions:
$env:NEUTRAL_TEST_CASE='multifile'
npm run test:readiness:live
```

The fixture has `total.js`, `invoice.js`, `verify.js` and a README requiring 20%
tax. The prompt explicitly asks a readonly research child to inspect requirements,
then the parent to repair and verify. The harness approves only fixture source
patches and the exact built-in Node command with `verify.js`; it rejects other
actions. It independently executes an immutable oracle after the task and requires
an applied diff, a completed child and current `commands_passed` evidence.

Evidence is under `artifacts/readiness/live-gui/` (native) or `live-gui-json/`:
timestamped reports, current events, approval screenshots and completed/failed PNG.
The `multifile` variant adds `-multifile` to that directory, requires renaming the
public helper in `total.js` and its caller in `invoice.js`, asserts both applied
diffs, checks the new API and rejects changes to the immutable requirements/test.
Artifacts can contain model output and are gitignored. The 180-second watchdog is
only an experiment cutoff: it cancels the test task through the UI and preserves
its checkpoint. It is not a limit on local automatic agent execution.

Historical `tools/benchmark_agent.py` experiments use separate manual settings
(8,192 tokens and 10 model turns). Report those constraints when interpreting a
failure; do not treat their cutoffs as Neutral's automatic execution limits.

## Investigation and continuation

On failure, retain the report/trace before repeating. Compare the canonical tool
receipt, approval decision, workspace witness and next physical model request.
For a live quality failure, inspect the actual changed files with the independent
oracle; a model's final text or successful process exit alone is insufficient.
Run targeted regressions first, then the complete suites after changes converge.
