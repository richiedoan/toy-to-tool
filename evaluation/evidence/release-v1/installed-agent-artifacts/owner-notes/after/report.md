# Owner notes — after Security & Privacy audit

## Audit context

Standard, group S only, scoped fixes authorized by user. Requirement: [README](../before/README.md) in before snapshot and [context E-context](../context.md). File identity: [E-hashes](hashes.json); project Python/runtime/revision: [E-env](../environment.json). Only disposable fixture data, public demo accounts and owner-private test notes. No committed HEAD is available. [Profile](../profile.json), [selection](../selection.json), [JSON report](report.json).

## Three priority tasks

1. Alice/Bob sign in and list/read only their own note: see `login-*`, `*-list`, `*-read-*` in [E-regression](regression.json) (S01/S02/S04).
2. Edit own note and independently read committed text: `*-write-*`, `*-state-*`, `*-readback-*` and marker/boundary cases in E-regression (S02/S03).
3. Sign out and replay old session: `logout`, `logout-replay-*`, `new-session-read`; expiry and factory recreation controls in E-regression (S04). Factory recreation is not a process-restart test.

## Unresolved blockers

No blocker was demonstrated in the checks performed. Impact is bounded to disposable local fixture notes; S05 unknowns and network/browser limits remain visible (E-context, E-runtime, E-regression).

## Important failures and improvements

| Criterion | Status | Severity | Decision | Requirement/result and evidence |
| --- | --- | --- | --- | --- |
| S01 | pass | null | preserve | Inspected fixture source/static surfaces and handler responses contain only intended public values or authorized note data after correction; cross-owner reads return 404. No production/history assurance. [E-regression](regression.json), [E-context](../context.md) |
| S02 | pass | null | preserve | Original A/B read/write reproductions now return 404; independent SQLite confirms forbidden targets unchanged. Owner read/update/readback, filtered list and anonymous read/write controls succeed. All 64 handler requests and all independent checks match expectations. [E-regression](regression.json), [E-context](../context.md) |
| S03 | pass | null | preserve | Source traces establish bound SQL parameters and safe DOM .value/textContent sinks; inert markup/quotes/Unicode/SQL marker and 0/1000 character roundtrips preserve data, 1001 characters and ownership fields rejected without mutation. No browser execution was observed; conclusion covers inspected defenses and handler/SQLite probes only. [E-regression](regression.json), [E-context](../context.md) |
| S04 | pass | null | preserve | Valid/invalid login, monotonic expiry, logout replay (read/write), fresh login, session discard on factory recreation and SQLite retention all executed in original handlers. Cookie is HttpOnly/SameSite=Strict, scoped /; HTTP localhost is intentional. Factory recreation verifies in-memory invalidation, not an executed network process restart; real deployment/transport unverified. [E-regression](regression.json), [E-context](../context.md) |
| S05 | unknown | null | investigate | Unknown composite: uploads absent by route/UI inventory; cross-origin reads grant no CORS headers, preflight 501; JSON-only write parser rejects simple cross-site form/text content and >4096-byte JSON without mutation; invalid public login errors bounded. CSRF browser SameSite enforcement unexecuted because no browser; abuse surface has no agreed rate/volume requirement. These unknown subcases prevent an overall pass. No observed S05 violation warrants changes. [E-regression](regression.json), [E-context](../context.md) |

## Changes and verification

S01/S02: [patch E-patch](../change.patch) adds bound owner predicates to GET and PATCH. The identical [runner E-runner](../probe.py) replays baseline probes; every status and state/value check matches. [Review E-review](review.json) confirms README/UI unchanged. Historical four forbidden 200 responses and two mutations remain in [baseline E-baseline](../before/report.json). Only source/handler/SQLite correctness is claimed; network execution remains unverified.

## Proposals and preserve decisions

S03/S04: preserve parameterized SQL, text-safe DOM, text validation, native UI and server-memory session handling, supported by their positive controls and E-context/E-regression. S01/S02: preserve public demo identities, filtered lists, valid owned API operations and anonymous denial. No benefit supports a redesign. The only corrective change is ownership enforcement in individual queries (E-context, E-regression).

## Unknowns and execution limits

S01–S05: real startup on port 0 was attempted and denied by sandbox socket permissions; see [E-runtime](../before/startup-failure.json). Fallback uses original BaseHTTPRequestHandler dispatch, real JSON parsing and SQLite, capturing only the listening-server constructor. It does not establish real HTTP socket behavior, threading, browser UI or process-restart behavior. No existing service was contacted. No browser tools or project browser setup were available (E-env); no new dependencies were installed. S03 safe DOM behavior is supported by source defense inspection, not rendered execution. S04 network/cookie enforcement and deployed TLS are not verified. No production privacy, backup, race/load, credential-history or brute-force claims. S05 CSRF/browser enforcement and abuse-budget checks remain unknown; next action requires a permitted socket/browser runtime and agreed bounded abuse expectations. No additional edits are justified (E-context, E-env, E-runtime, E-regression).

## Coverage and exclusions

pass: 4, fail: 0, unknown: 1, not_applicable: 0. S06 deferred (Advanced), not passed or not applicable; other groups not assessed. [Selection](../selection.json). No overall score, ASVS mapping or certification.

## Evidence register

| ID | Artifact | Supports |
| --- | --- | --- |
| E-context | [../context.md](../context.md) | Requirement source, source traces, surface classification and scope; requirement; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-env | [../environment.json](../environment.json) | Actual project interpreter, revision and browser-tool discovery; observation; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-runtime | [../before/startup-failure.json](../before/startup-failure.json) | Real port-0 startup failure: sandbox denied socket bind; observation; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-hashes | [hashes.json](hashes.json) | SHA-256 source identity; artifact; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-regression | [regression.json](regression.json) | Executed actual handler request traces and independent SQLite expectations/results; measurement; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-runner | [../probe.py](../probe.py) | Exact executed deterministic request/state regression runner; no network claim; artifact; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-readme | [../before/README.md](../before/README.md) | Immutable README requirements; requirement; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-baseline | [../before/report.json](../before/report.json) | Immutable baseline important failures; artifact; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-patch | [../change.patch](../change.patch) | Minimal protected-boundary correction; artifact; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |
| E-review | [review.json](review.json) | Source preservation, diff and evidence sufficiency review; observation; Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service; registered 2026-10-28T10:40:52.073379+00:00 |

## Validation and next actions

Validate this JSON with the installed engine and explicit project evidence root; command, exit code and output are saved in `validation.json` beside this report. Validation checks report structure/linkage, not security. Markdown/JSON outcomes and linked evidence were reviewed; retain S05 unknowns and runtime limits. No owner decision is needed for the minimal ownership fix. Further S05 verification requires browser access and a bounded abuse contract (E-env/E-runtime/E-context).
