import datetime, hashlib, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]; OUT=ROOT/'audits/owner-notes'; phase=sys.argv[1]; dest=OUT/phase
now=datetime.datetime.now(datetime.timezone.utc).isoformat(); observed=json.loads((dest/'regression.json').read_text()); before=phase=='before'
report=json.loads((OUT/'template.json').read_text()); report.update(report_kind='audit',change_permission='fix_scoped',scope_and_limitations='Standard, group S only; README and user define localhost disposable fixture contract. Source and real handler/SQLite checks only: socket bind denied; no network HTTP/browser verification. In-memory streams invoke original handlers and real database; only listening server class is captured. No production, TLS, race/load, brute-force, outside-workspace history or secret-store checks. No certification. S06 deferred. No committed HEAD; SHA-256 manifests identify source. '+('Before correction.' if before else 'After owner predicates added; historical failures retained in before/report.json.'))
files=[('E-context','audits/owner-notes/context.md','Requirement source, source traces, surface classification and scope','requirement'),('E-env','audits/owner-notes/environment.json','Actual project interpreter, revision and browser-tool discovery','observation'),('E-runtime','audits/owner-notes/before/startup-failure.json','Real port-0 startup failure: sandbox denied socket bind','observation'),('E-hashes','audits/owner-notes/'+phase+'/hashes.json','SHA-256 source identity','artifact'),('E-regression','audits/owner-notes/'+phase+'/regression.json','Executed actual handler request traces and independent SQLite expectations/results','measurement'),('E-runner','audits/owner-notes/probe.py','Exact executed deterministic request/state regression runner; no network claim','artifact'),('E-readme','audits/owner-notes/before/README.md','Immutable README requirements','requirement')]
if not before: files += [('E-baseline','audits/owner-notes/before/report.json','Immutable baseline important failures','artifact'),('E-patch','audits/owner-notes/change.patch','Minimal protected-boundary correction','artifact'),('E-review','audits/owner-notes/after/review.json','Source preservation, diff and evidence sufficiency review','observation')]
report['evidence']=[dict(id=i,location=l,description=d,environment='Python 3.9.6 / SQLite 3.54.0; local source + handler streams, disposable database; no listening service',captured_at=now,kind=k,synthetic=False) for i,l,d,k in files]
reasons={
'S01':('Cross-owner GET reveals owner-only note text to the other logged-in demo user. No production credentials exposed; public demo identities remain intentional.' if before else 'Inspected fixture source/static surfaces and handler responses contain only intended public values or authorized note data after correction; cross-owner reads return 404. No production/history assurance.'),
'S02':('Four forbidden requests return 200 (A reads/updates B, B reads/updates A); independent SQLite checks confirm two unauthorized mutations. List filtering and anonymous protection pass.' if before else 'Original A/B read/write reproductions now return 404; independent SQLite confirms forbidden targets unchanged. Owner read/update/readback, filtered list and anonymous read/write controls succeed. All 64 handler requests and all independent checks match expectations.'),
'S03':'Source traces establish bound SQL parameters and safe DOM .value/textContent sinks; inert markup/quotes/Unicode/SQL marker and 0/1000 character roundtrips preserve data, 1001 characters and ownership fields rejected without mutation. No browser execution was observed; conclusion covers inspected defenses and handler/SQLite probes only.',
'S04':'Valid/invalid login, monotonic expiry, logout replay (read/write), fresh login, session discard on factory recreation and SQLite retention all executed in original handlers. Cookie is HttpOnly/SameSite=Strict, scoped /; HTTP localhost is intentional. Factory recreation verifies in-memory invalidation, not an executed network process restart; real deployment/transport unverified.',
'S05':'Unknown composite: uploads absent by route/UI inventory; cross-origin reads grant no CORS headers, preflight 501; JSON-only write parser rejects simple cross-site form/text content and >4096-byte JSON without mutation; invalid public login errors bounded. CSRF browser SameSite enforcement unexecuted because no browser; abuse surface has no agreed rate/volume requirement. These unknown subcases prevent an overall pass. No observed S05 violation warrants changes.'}
for f in report['findings']:
 c=f['criterion_id']; fail=before and c in ['S01','S02']; unknown=c=='S05'
 f.update(status='fail' if fail else ('unknown' if unknown else 'pass'),severity='important' if fail else None,decision='fix' if fail else ('investigate' if unknown else 'preserve'),reason=reasons[c],requirement_or_goal='README: owner-only list/read/update, no ownership transfer, plain text <=1000 characters, logout/expiry/restart invalidation; installed canonical '+c+' protocol.',affected_users_and_conditions='Alice/Bob demo users and anonymous callers; isolated loopback fixture with disposable SQLite data. Bounded impact: no production data, credentials or deployment.',evidence_ids=['E-context','E-env','E-runtime','E-hashes','E-regression','E-runner','E-readme']+([] if before else ['E-baseline','E-patch','E-review']),decision_inputs=dict(evidence_sufficient=not unknown,violates_requirement=fail,measurable_benefit=fail,authorized=fail,proportional=True),change_scope_cost_risk=('Add owner predicate to individual GET and PATCH bound queries only. Minimal server.py correction within user authority; no response shape, UI, session, schema or README changes. Risk: accidental denial of legitimate owned operations, covered by A/B controls.' if fail else ('No app edit. Establish browser CSRF behavior and an owner-approved bounded abuse contract before further assessment.' if unknown else 'Preserve existing behavior/defenses. After patch only individual owner predicates differ; preserve UI/API/README/session/SQL parameterization.')),verification_plan='Replay identical runner against corrected source; compare forbidden reads/writes and independent owner state, allowed operations, anonymous, note constraints and session controls. For S05 obtain browser runtime and bounded abuse contract; do not claim these passed.',observed_outside_level=False)
(dest/'report.json').write_text(json.dumps(report,indent=2)+'\n')
md=f'''# Owner notes — {phase} Security & Privacy audit

## Audit context

Standard, group S only, scoped fixes authorized by user. Requirement: [README](README.md) in before snapshot and [context E-context](../context.md). File identity: [E-hashes](hashes.json); project Python/runtime/revision: [E-env](../environment.json). Only disposable fixture data, public demo accounts and owner-private test notes. No committed HEAD is available. [Profile](../profile.json), [selection](../selection.json), [JSON report](report.json).

## Three priority tasks

1. Alice/Bob sign in and list/read only their own note: see `login-*`, `*-list`, `*-read-*` in [E-regression](regression.json) (S01/S02/S04).
2. Edit own note and independently read committed text: `*-write-*`, `*-state-*`, `*-readback-*` and marker/boundary cases in E-regression (S02/S03).
3. Sign out and replay old session: `logout`, `logout-replay-*`, `new-session-read`; expiry and factory recreation controls in E-regression (S04). Factory recreation is not a process-restart test.

## Unresolved blockers

No blocker was demonstrated in the checks performed. Impact is bounded to disposable local fixture notes; S05 unknowns and network/browser limits remain visible (E-context, E-runtime, E-regression).

## Important failures and improvements

'''
md+='| Criterion | Status | Severity | Decision | Requirement/result and evidence |\n| --- | --- | --- | --- | --- |\n'
for f in report['findings']: md+=f"| {f['criterion_id']} | {f['status']} | {f['severity'] or 'null'} | {f['decision']} | {f['reason']} [E-regression](regression.json), [E-context](../context.md) |\n"
md+='''
## Changes and verification

'''
md+=('Baseline saved before edits. S01/S02 authorize only owner predicates on GET/PATCH: enforce README boundary, keep existing 404 response and parameterized SQL. Existing positive controls meet the contract: owner-filtered lists, A/B owned read/update, anonymous denial, immutable ownership, text bounds/quotes/Unicode, invalid credentials, logout/expiry and database retention under factory recreation (E-regression). Proportionate: two SQL predicates, no infrastructure or auth redesign. Recheck must deny both directions and independently preserve the forbidden owner record.\n' if before else 'S01/S02: [patch E-patch](../change.patch) adds bound owner predicates to GET and PATCH. The identical [runner E-runner](../probe.py) replays baseline probes; every status and state/value check matches. [Review E-review](review.json) confirms README/UI unchanged. Historical four forbidden 200 responses and two mutations remain in [baseline E-baseline](../before/report.json). Only source/handler/SQLite correctness is claimed; network execution remains unverified.\n')
md+='''
## Proposals and preserve decisions

S03/S04: preserve parameterized SQL, text-safe DOM, text validation, native UI and server-memory session handling, supported by their positive controls and E-context/E-regression. S01/S02: preserve public demo identities, filtered lists, valid owned API operations and anonymous denial. No benefit supports a redesign. The only corrective change is ownership enforcement in individual queries (E-context, E-regression).

## Unknowns and execution limits

S01–S05: real startup on port 0 was attempted and denied by sandbox socket permissions; see [E-runtime](../before/startup-failure.json). Fallback uses original BaseHTTPRequestHandler dispatch, real JSON parsing and SQLite, capturing only the listening-server constructor. It does not establish real HTTP socket behavior, threading, browser UI or process-restart behavior. No existing service was contacted. No browser tools or project browser setup were available (E-env); no new dependencies were installed. S03 safe DOM behavior is supported by source defense inspection, not rendered execution. S04 network/cookie enforcement and deployed TLS are not verified. No production privacy, backup, race/load, credential-history or brute-force claims. S05 CSRF/browser enforcement and abuse-budget checks remain unknown; next action requires a permitted socket/browser runtime and agreed bounded abuse expectations. No additional edits are justified (E-context, E-env, E-runtime, E-regression).

## Coverage and exclusions

'''
counts={s:sum(f['status']==s for f in report['findings']) for s in ['pass','fail','unknown','not_applicable']}
md+=', '.join(f'{k}: {v}' for k,v in counts.items())+'. S06 deferred (Advanced), not passed or not applicable; other groups not assessed. [Selection](../selection.json). No overall score, ASVS mapping or certification.\n'
md+='\n## Evidence register\n\n| ID | Artifact | Supports |\n| --- | --- | --- |\n'
for e in report['evidence']:
 rel=pathlib.Path(__import__('os').path.relpath(ROOT/e['location'],dest)); md+=f"| {e['id']} | [{rel}]({rel}) | {e['description']}; {e['kind']}; {e['environment']}; registered {e['captured_at']} |\n"
md+='''
## Validation and next actions

Validate this JSON with the installed engine and explicit project evidence root; command, exit code and output are saved in `validation.json` beside this report. Validation checks report structure/linkage, not security. Markdown/JSON outcomes and linked evidence were reviewed; retain S05 unknowns and runtime limits. No owner decision is needed for the minimal ownership fix. Further S05 verification requires browser access and a bounded abuse contract (E-env/E-runtime/E-context).
'''
(dest/'report.md').write_text(md)
print(json.dumps({'phase':phase,'counts':counts,'deferred':['S06']}))
