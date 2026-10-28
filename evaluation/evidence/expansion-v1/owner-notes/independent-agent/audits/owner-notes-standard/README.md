# Owner notes Standard security/privacy audit

[Before report](before/report.md) · [After report](after/report.md) · [Patch](ownership.patch)

Only owner-notes/server.py changed: individual GET and PATCH now bind authenticated ownership in their existing SQL predicates. UI, README, API, sessions, SQLite and architecture preserved. Baseline records two bidirectional bypasses with committed forbidden writes; recheck records denied requests and independent unchanged victim state.

- Source snapshots and SHA-256 hashes: before/source/, after/source/, and each phase/source-hashes.json.
- Raw observations: before/observations.json and after/observations.json; 120 records each, six baseline mismatches, zero after mismatches. These are actual HTTP-handler byte-stream executions with real disposable SQLite, not network or browser tests.
- Regression comparison and preservation: after/preservation.json.
- Baseline report was saved, validated and made read-only before application edits. All final artifacts are read-only, with SHA-256 manifest for tamper detection. This is file-permission and hash preservation, not a claim of externally enforced WORM storage.
- Shared engine: supplied .venv interpreter and declared dependency versions in context.json; select/template at Standard --group S; validate with explicit workspace evidence root. Both validation outputs retained. Report consistency/sufficiency review: report-review.json.
- Network attempt: network-probe.py, network-startup-failure.log. Sandbox denied socket.bind. Browser discovery found no tools/setup; no browser installed. S03/S04/S05 remain unknown for their unexecuted portions. S06 deferred. No overall score or certification.

Reproduction: probe.py accepts a new output-directory name under this evidence directory. To rerun after sealing, copy the harness into a writable disposable workspace or explicitly choose a new unsealed evidence directory; do not overwrite baseline or after artifacts. The harness only substitutes the listening server constructor, uses the app's real BaseHTTPRequestHandler request parser, routing, payload/session logic and SQLite. Server recreation checks are not process-restart evidence. network-probe.py retains the original attempted live HTTP method. Cookies are redacted and test databases are removed after probes.

Requirements and pre-edit decisions: before/source/README.md and source-review.md. Captured environment/access limits: context.json. No target design or contract change; no production credentials, external evaluator material, brute force or load test.
