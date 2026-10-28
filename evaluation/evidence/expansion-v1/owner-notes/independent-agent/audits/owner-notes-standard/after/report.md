# Owner notes — After Standard security/privacy audit

Captured 2026-10-28T09:02:14.824149+00:00. Focused group S; no overall security certification. Requirements: [E-contract](../before/source/README.md). Profile/selection: [profile](../profile.json), [selection](../selection.json). Machine report: [report.json](report.json).

## Audit context

Authorized: demonstrated, proportionate target corrections only. Disposable Alice/Bob records; plain text and SQLite persistence. Original UI, API and stdlib architecture preserved. Source revision: file hashes (no HEAD). Environment and tool limits: [E-context](../context.json), [E-hashes](source-hashes.json), [E-network](../network-startup-failure.log).

## Three priority tasks

| Task | Observed outcome and limits | Evidence |
| --- | --- | --- |
| Login, list/read own notes | Valid and invalid credentials, owner list/read exercised in actual handlers; visible browser flow unexecuted. | S01/S02/S04, E-probes |
| Edit/save and independently read committed text | Own saves/readbacks and SQLite snapshots exercised, including quotes/Unicode and length boundaries. | S02/S03, E-probes |
| Sign out and replay | Previous session denied for GET and PATCH; independent state unchanged. Browser controls unexecuted. | S04, E-probes |

## Unresolved blockers

No blocker was demonstrated in the checks performed. S03/S04/S05 contain unknown portions; this does not establish absence of blockers there (E-network, E-context, E-source).

## Findings and decisions

| Criterion | Status | Severity | Decision | Evidence-linked result |
| --- | --- | --- | --- | --- |
| S01 | pass | — | preserve | Cross-owner response disclosure fixed by owner predicate; inspected source/assets and tested anonymous/owner/cross-owner handler responses match intended audiences. No history available or production surfaces in scope. E-contract/E-source/E-probes/E-summary. |
| S02 | pass | — | preserve | Original forbidden read and write now return 404 in both directions; independent SQLite state unchanged. Owned operations, anonymous denials and all neighboring handler controls pass. E-contract/E-source/E-probes/E-summary. |
| S03 | unknown | — | investigate | SQL parameterization and safe DOM sinks inspected; inert markup/quotes/Unicode/SQL-like text roundtrip exactly. Actual browser execution unverified. E-contract/E-source/E-probes/E-summary. |
| S04 | unknown | — | investigate | Valid/invalid login, server-side expiry, logout replay for reads/writes, relogin and server recreation tested via actual handlers. Cookie/transport behavior in browser, live network and real process restart unexecuted. E-contract/E-source/E-probes/E-summary. |
| S05 | unknown | — | investigate | Source and low-volume handler probes cover JSON bounds, CORS headers, static/login routes; uploads absent. Browser cross-site workflow and cookie enforcement unexecuted; no agreed rate/concurrency budget. Composite remains unknown. E-contract/E-source/E-probes/E-summary. |

## Changes and verification

Baseline: S01/S02 important failures retained in [before/report.json](../before/report.json). Applied [ownership.patch](../ownership.patch): only owner predicates and bound tuples in GET/PATCH. Original bypasses now denied; independent state unchanged, owned operations preserved (E-probes/E-summary). [E-integrity](preservation.json) confirms all other target files unchanged.

Probe command: `.venv/bin/python audits/owner-notes-standard/probe.py after`. 120 observation records; 0 mismatches against expected values. Raw requests/responses, inputs and SQLite snapshots: [E-probes](observations.json); [E-summary](probe-summary.json).

## Proposals and preserve decisions

Preserve filtered list, parameterized SQL, text-safe UI sinks, native controls/labels/styles, logout/session model and stdlib/SQLite architecture. Positive controls and proportionality: S01-S05 / [E-source](../source-review.md), E-probes. No redesign/infrastructure proposal has a demonstrated scoped benefit.

## Unknowns and execution limits

S03: browser markup execution unexecuted. S04: browser cookie behavior, network transport and actual process restart unexecuted; server closure recreation is only a narrower retention/invalidation test. S05: CSRF browser state-change workflow/login/logout and enforcement unexecuted; CORS header checks do not establish browser enforcement or auth. Abuse beyond low-volume input bounds unknown because no rate/concurrency budget exists. Uploads demonstrably absent. See per-surface rationale and next steps in [E-source](../source-review.md), actual startup failure E-network, capability discovery E-context. No failed tool probe is classified as an application defect. Next verification requires an environment allowing loopback serving and a browser; no user approval needed for the completed two-predicate correction.

## Coverage and exclusions

Pass: S01, S02 (2, inspected source/actual handler scope); fail: 0; unknown: S03, S04, S05 (3); not applicable whole criteria: 0.
S06 is deferred at Advanced, never counted as passed. Groups F/U/A/P/O are outside the agreed focused audit. No score.

## Evidence register

| ID | Artifact | Description |
| --- | --- | --- |
| E-contract | [README.md](../before/source/README.md) | Unchanged product contract, three priority tasks and preservation boundaries. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-context | [context.json](../context.json) | Environment, versions, source classification and capability discovery. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-source | [source-review.md](../source-review.md) | Criterion-linked sink/lifecycle/surface inspection, positive controls and pre-edit decision. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-network | [network-startup-failure.log](../network-startup-failure.log) | Actual startup failed at socket.bind with PermissionError; network checks unexecuted. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-hashes | [source-hashes.json](../after/source-hashes.json) | SHA-256 target source identity. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-probes | [observations.json](../after/observations.json) | Actual handler requests/responses, expected values, independent SQLite state. Sessions redacted. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-summary | [probe-summary.json](../after/probe-summary.json) | Observation count and mismatches against expected contract. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-patch | [ownership.patch](../ownership.patch) | Minimal parameterized owner predicates. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-baseline | [report.json](../before/report.json) | Immutable baseline failures and limitations. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |
| E-integrity | [preservation.json](../after/preservation.json) | All other target files unchanged; exact two-statement correction checked. Captured 2026-10-28T09:02:14.824149+00:00; non-synthetic. |

## Validation and next actions

Shared validator: `.venv/bin/python .agents/skills/security-privacy/references/engine/scripts/audit.py validate --report audits/owner-notes-standard/after/report.json --evidence-root /private/tmp/toy-owner-notes-v2-agent`. Result retained separately in validation.txt. JSON/Markdown use identical finding rows and coverage; links and evidence sufficiency reviewed. Schema validation checks the report contract, not application security. Reports will be sealed read-only with SHA-256 manifest after validation. No new scope decision requested.
