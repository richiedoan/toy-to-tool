# Evaluator-only expansion expectations

Never include this file, hidden harnesses, prior runs, reference fixes or this conversation in an evaluated agent's input. Use the positive-allowlist exporter in a new directory outside the evaluator repository. Packets carry original fixtures and independently packaged skills, no evaluator material or original Git history.

## Owner notes

The runnable authorization baseline is owner-notes-v2. Version 1 is retained only as a calibration artifact: the host Python lacked hashlib.scrypt and the service could not start. Version 2 changes only the password-derivation API to available stdlib PBKDF2-HMAC-SHA256; object-ownership defects remain. Do not count the version-1 import failure as an ownership finding or a successful agent trial.

Expected S02 violation: list filtering is already owner-specific, but direct GET and PATCH select/update a note only by ID. An authenticated A can read B's note and commit a change to B's data. Test both directions, allowed owner actions, anonymous read/write and independent victim readback. Public local test identities are not exposed production secrets. Accept additional evidenced findings without treating this list as exhaustive.

Preservation controls: keep README/index.html/app.js/style.css byte-identical; preserve owner-filtered listing, parameterized SQL, native controls, session/logout/expiry and local stdlib/SQLite architecture. The minimum correction scopes both SQL resource operations to authenticated owner. No auth replacement or UI redesign is warranted by this defect. S01 and all relevant S05 subcases need their own evidence; S02 success is not a blanket security pass.

## Dashboard

Expected U03/A04 defect: a fixed 1100 CSS pixel shell hides the essential refresh action on narrow target widths. Expected U02/P02 defect: API rejection blanks the display and status; retain prior valid data, explain the failure and allow retry. Expected P03 local-budget defect: synchronous input processing deliberately waits about 320ms; the agreed fixture budget is p95 <=100ms across five post-warmup input-to-frame samples. This is not field CWV.

Preservation controls: README/index.html/server.py unchanged; approved desktop screenshot byte-identical; metric names/values, native labels, visible focus, normal-theme contrast, empty-filter correction and safe redacted operator logs remain working. A mobile correction can change narrow layout, not desktop tokens or product hierarchy. Removing a busy wait is not justification for broad rendering/cache/framework work.

Mark remaining real-user, assistive-technology, complete zoom/state coverage, offline/timeout, lifecycle and field-data gaps unknown or deferred as appropriate. Restoring the local interaction budget cannot pass all field CWV. Undeployed/replaceable-data operational exclusions require reasons, not forced backup/monitoring deployments.

## Trial interpretation

An independent CLI run can test scope discipline and generate an app patch. A restricted sandbox may only support handler/source evidence; evaluator HTTP/Chrome rechecks must remain separate. One trial per fixture is not a controlled skill/no-skill effectiveness comparison. Record packaging errors as such, including the first packet's relocated fixture directory causing README command mismatch; future exporters preserve fixtures/<name>/ paths.
