# Scoped correction record

Only tracker/app.js was changed. The original source, README, HTML, raw observations, before report and hashes were saved before edits. No git HEAD exists; source SHA-256 identifies builds. The original harness is copied to before/regression.cjs; tools/regression.cjs remains the same original reproduction. The supplemental baseline run was executed later against the preserved original source; it does not replace the initial observations.

- **F01 / F03:** Save now snapshots note/completion, writes the next complete task list to localStorage and updates memory only after write success. Failure retains committed state and draft values; retries are allowed. Baseline edit / edit-failure-retry checks fail; current checks pass.
- **F02:** Startup reads existing localStorage records. A parse/type/read failure reports load failure and blocks adding, preserving original saved bytes. Existing valid records keep IDs/values. Startup adapter and existing-data checks now pass; real browser refresh/reopen remains pending.
- **F04:** Save handler rejects notes above the existing 500 UTF-16 code-unit limit. Title trim/1-80 checks and Unicode/punctuation behavior are preserved. Boundary checks now pass in the handler harness. Browser maxlength/required enforcement is unexecuted.
- **F05:** A synchronous pending guard prevents overlapping add submissions even when disabled controls are bypassed by direct event dispatch. Each task save also has a pending guard. Finally blocks release pending state after success/failure. Later same-title submissions and subsequent edits remain allowed.
- **F01 / F03 neighboring correction:** Adding appends newly committed records without replacing existing task editors. This retains a failed-save draft and keeps pending-save values visible if another add completes. The supplemental baseline fails these cases, while the current extended suite passes.

All fixes address explicit README outcomes with bounded app.js changes. Audience: single users operating disposable/non-sensitive browser-local tasks. Cost/risk: small handler/startup changes; no new dependencies, backend, schema migration, account or sync feature. Startup rejection intentionally preserves unrecognized saved bytes rather than silently overwriting them. There is no repair/export feature in scope. No optional expansion proposed.

## Executed verification

Original suite: baseline 8 pass / 11 fail; current 19 pass / 0 fail. Extended suite: preserved baseline 8 pass / 19 fail; current 27 pass / 0 fail. Extended results include the original 19 tests and are not 27 additional independent tests. Raw assertions and exact fixtures are in before/regression.json, before/supplemental.json, after/regression.json and after/neighboring.json. Syntax check executed successfully; see after/syntax.json.

These are real executions of application source in a Node VM with explicitly controlled test adapters. They are not browser observations and do not establish actual browser-local retention. Current F01-F04 remain unknown at full browser scope; F05 passes for directly exercised operation-handler repetition. Null severity on current rows is not a claim that the application is fully verified. Historical blocker (F01) and important failures (F02-F05) remain in the immutable before report. Browser verification and audit-engine validation are outstanding.
