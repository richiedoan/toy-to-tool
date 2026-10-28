from pathlib import Path
import datetime, json, sys

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / 'audits'
phase = sys.argv[1]
after = phase == 'after'
report = json.loads((A/'template.json').read_text())
report.update(report_kind='audit', change_permission='fix_scoped', scope_and_limitations='Standard focused U/A/P/O audit against dashboard/README.md. Expert source review, real app handlers in Node VM with controlled DOM/fetch, Python in-memory HTTP handler checks, clean-copy startup attempts. No real browser: Chrome launch exit 134; no browser MCP/automation. Socket bind denied by sandbox. No screenshots, rendered accessibility/geometry, AT, text zoom, real keyboard, Chrome input-to-frame samples, field CWV, user sessions, load or production assurance. Source hashes identify builds; repository has no HEAD. Protected README startup-path failure remains proposed. Patched layout/performance failures remain verification pending at original severity until browser recheck.')
artifacts = {
    'requirements': ('audits/before/source/README.md', 'Agreed task, budget and preservation contract.', 'requirement'),
    'context': ('audits/context.json', 'Actual environment, probes, scope, tasks and unavailable tools.', 'observation'),
    'source': ('audits/before/source-observations.json', 'Criterion-linked static observations and preservation boundaries.', 'observation'),
    'hashes': (f'audits/{phase}/source-hashes.json', 'SHA-256 source manifest.', 'artifact'),
    'handlers': (f'audits/{phase}/handlers.json', 'Executed app handlers under explicitly controlled Node adapter; not browser results.', 'measurement'),
    'server': (f'audits/{phase}/server-handlers.json', 'Executed Python HTTP handlers in memory; no live service assurance.', 'observation'),
    'startup': ('audits/before/operations.json', 'Clean copy documented path failure and socket-denied fallback attempt.', 'observation'),
}
if after:
    artifacts['regression'] = ('audits/after/regression.json', 'Source preservation, handler outcomes and bounded patch checks.', 'observation')
    artifacts['patch'] = ('audits/dashboard.patch', 'Exact original-to-current patch.', 'artifact')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
report['evidence'] = [dict(id=k, location=v[0], description=v[1], environment='Local macOS; supplied Python 3.9.6 venv and Node v24.19.0; exact limits in context and artifacts.', captured_at=now, kind=v[2], synthetic=False) for k,v in artifacts.items()]

unknowns = {
 'U01': 'Source task mapping exists, but actual screen hierarchy and user interpretation have not been exercised. Expert review only.',
 'U05': 'Single screen uses consistent native controls/cards in source; rendered equivalent states and desktop preservation require browser evidence.',
 'A01': 'Native button and search retained; real Tab/Shift+Tab/Enter task paths and focus sequence unexecuted.',
 'A02': 'Explicit label, native roles, status live region retained; accessibility tree and supported AT state announcements unexecuted.',
 'A03': 'Source palette inventoried; actual computed/composited text colors across states and placeholder unmeasured.',
 'A05': 'Focus-visible rule retained; focus visibility and occlusion unexecuted in browser.',
 'A06': 'Native controls and CSS padding retained; real hit regions and spacing geometry unmeasured.',
 'P01': 'VM core data/filter/retry handlers run without exceptions, but supported-browser tasks and runtime logs are unavailable.',
 'P04': '15-cycle VM checkpoints show four nodes and stable listeners; real browser timers, requests, resources and teardown unexecuted.',
 'O04': 'In-memory real handlers produce correlated redacted 503 events with only event/request_id/status; actual owner stderr channel needs live startup, blocked by sandbox bind denial.',
}
failures = {
 'U02': ('important','503/offline handlers clear successful rows and blank status. Required explanation and retention fail.','Keep rows and explain retry; rerun 503/offline, initial failure, slow response, empty filter and recovery.'),
 'U03': ('important','Fixed 1100px shell exceeds 320/390/768 widths, with hidden horizontal overflow. Source establishes unsupported mobile layout; rendered control coordinates unavailable.','Fit shell, wrap narrow header and adapt columns; recheck three tasks at all four widths and approved 1440 desktop.'),
 'A04': ('important','Fixed 1100px shell with hidden overflow violates 320 CSS pixel reflow contract. 200% text-resize runtime is unexecuted.','Use responsive shell/cards; recheck at 320 CSS pixels and 200% text size, then desktop positive controls.'),
 'P02': ('important','Controlled rejected fetch and 503 erase last success and feedback; retry handler recovers but failure state is untruthful. Timeout subcase also unverified.','Retain data and show explanation/retry; rerun faults and delayed success; bounded hung-request case still needs investigation.'),
 'P03': ('important','Each input deliberately busy-waits at least 320ms before rendering, exceeding the 100ms input-to-next-frame ceiling. Node samples corroborate handler delay; Chrome measurements unavailable.','Remove busy wait; remeasure same Chrome setup at 1440x900 after warmup, five consecutive input-to-next-frame samples and nearest-rank p95 = sorted[ceil(.95*5)-1].'),
 'O01': ('important','Clean-copy README command fails: fixtures/dashboard/server.py does not exist. Correct actual path startup was attempted but sandbox denied bind; that denial is not an app failure.','Owner-approved future README correction to python3 dashboard/server.py --port 8767, then isolated clean startup and browser smoke. README is protected, so no edit authorized.'),
}
rows = []
for original in report['findings']:
    row = dict(original); cid = row['criterion_id']
    row.update(requirement_or_goal='dashboard/README.md tasks and boundaries; canonical '+cid+' protocol at Standard.', affected_users_and_conditions='Local dashboard readers/operators; disposable deterministic data. Source and controlled handler execution only; browser-dependent portions unexecuted.', evidence_ids=['requirements','context','source','hashes'], change_scope_cost_risk='Preserve approved desktop tokens, content, native controls, endpoint and architecture. No unrelated changes.', verification_plan='Repeat criterion protocol with a working browser/local socket permission; do not treat static checks as runtime assurance.')
    if row['status'] == 'not_applicable':
        row['reason'] += ' Source architecture and README inspected; no additional infrastructure justified.'
    elif cid in failures:
        severity, reason, plan = failures[cid]
        row.update(status='fail', severity=severity, reason=reason, decision='propose' if cid=='O01' else 'fix', verification_plan=plan,
                   decision_inputs=dict(evidence_sufficient=True,violates_requirement=True,measurable_benefit=True,authorized=cid!='O01',proportional=True),
                   change_scope_cost_risk='README edit forbidden; propose correction only.' if cid=='O01' else 'Small authorized app-only correction; verify measurable recovery/fit/delay and unchanged desktop/data. Low scope, browser regression evidence unavailable.')
        row['evidence_ids'] += ['startup'] if cid=='O01' else ['handlers']
        if after and cid in ['U03','A04','P03']:
            row['reason'] += ' Patch applied, but matching browser recheck is unavailable. Keep baseline failure/severity as verification pending; no pass claimed.'
            row['evidence_ids'] += ['regression','patch']
        if after and cid in ['U02','P02']:
            row.update(status='unknown',severity=None,decision='investigate',reason='Handler-level failure corrected and rechecked: 503/offline retain rows, explain failure, enable refresh, and retry restores successful status. Browser state visibility/announcements remain unverified; bounded timeout is unexecuted. Baseline important failure retained in before/report.json.',decision_inputs=dict(evidence_sufficient=False,violates_requirement=False,measurable_benefit=False,authorized=False,proportional=True))
            row['evidence_ids'] += ['regression','patch']
    else:
        row.update(reason=unknowns[cid], status='unknown',severity=None,decision='investigate',decision_inputs=dict(evidence_sufficient=False,violates_requirement=False,measurable_benefit=False,authorized=False,proportional=True))
        row['evidence_ids'] += ['server'] if cid=='O04' else ['handlers']
    rows.append(row)
report['findings'] = rows
(A/phase/'report.json').write_text(json.dumps(report,indent=2)+'\n')
counts = {s:sum(r['status']==s for r in rows) for s in ['pass','fail','unknown','not_applicable']}
text = f'''# Dashboard {phase} audit — Standard U/A/P/O

Expert review against the three README tasks: read values at 320/390/768/1440 CSS pixels; filter titles without changing values or fetching; refresh with explanation, retained last success and safe retry. No participant evidence. Exact contract: [requirements](../before/source/README.md). Scope and runtime: [context](../context.json). Source revision: [hashes](source-hashes.json); unborn Git repository.

No blocker was demonstrated in the checks performed. Browser-dependent scope remains unknown; this is not a clean bill of health. Current criterion counts: {counts}. Deferred: U06, P05, P06, O06. [Selection](../selection.json), [profile](../profile.json), [JSON report](report.json).

## Findings and coverage

| Criterion | Status | Severity | Decision | Evidence and reason |
| --- | --- | --- | --- | --- |
'''
for r in rows:
    links=', '.join(f'[{eid}](../../{artifacts[eid][0]})' for eid in r['evidence_ids'])
    text += f"| {r['criterion_id']} | {r['status']} | {r['severity'] or '—'} | {r['decision']} | {r['reason']} {links} |\n"
text += '''
## Changes, preservation and verification

Before evidence is retained separately. Authorized scope: responsive fit below desktop, failed-refresh retention/explanation, and removal of unconditional filter delay. Preserve all labels/values, native controls, focus rules, colors, font, card ordering, 1440px desktop hierarchy, API and stdlib architecture. No redesign or dependencies. [Positive controls and decision rationale](../before/source-observations.json). Each correction benefits the affected mobile reader, failed-refresh user or filtering user and is small relative to its demonstrated task impact.

README startup-path correction is proposed only: editing the contract was forbidden. No production deployment, important user data, required data restore or release rollback exists: O02/O03/O05 excluded. U04 excludes data mutations/destructive workflows; filter correction is included under U02.

## Unknowns and next checks

Chrome launch exited 134 and browser automation/MCP was unavailable. Real screen hierarchy, screenshots, control coordinates, keyboard focus, accessibility tree/AT, contrast/compositing, 200% text resizing, reflow and hit geometry were not collected. Server bind was denied by sandbox. The same failed environment probe was not retried. Browser failures patched without a matching recheck retain their known severity. Handler-level corrections have bounded execution evidence but no full UI pass.

Run all three tasks at four supported widths, keyboard/AT and state checks, text at 200%, and desktop screenshot comparison when browser access exists. At 1440x900 in the same actual Chrome/hardware, no throttling, warm up then collect five consecutive input-event-to-next-animation-frame durations. Nearest-rank p95 is the maximum of those five; require <=100ms. Record browser, hardware, samples, caching/network and calculation. No Chrome sample or percentile was fabricated. Node handler durations are diagnostics only. Field p75 LCP/INP/CLS remain unknown; local timing is not field CWV. Bounded hung-request behavior and browser resource teardown remain unexecuted. No WCAG AA conformance claim.

## Evidence and validation

Every evidence ID resolves in report.json. Artifacts are actual source snapshots or executed observations with controlled dependencies clearly disclosed; no browser or live-service result is inferred from them. See [handler observations](handlers.json), [HTTP handler observations](server-handlers.json), [startup attempt](../before/operations.json). JSON and this table have identical status/severity/decision rows. Shared validator checks structure, linkage and decisions, not evidence sufficiency.

Validation command: `.venv/bin/python .agents/skills/ux-visual-quality/references/engine/scripts/audit.py validate --report audits/PHASE/report.json --evidence-root /private/tmp/toy-dashboard-agent`. Output is retained in validation.txt. Next action: browser and permitted local startup rechecks; owner decision required only for protected README correction.
'''.replace('audits/PHASE/',f'audits/{phase}/')
if after:
    text += '\nApplied changes and exact checks: [patch](../dashboard.patch), [regression evidence](regression.json). Corrected handler subcases pass; overall U02/P02 remain unknown for browser/timeout portions. U03/A04/P03 remain verification pending at baseline severity.\n'
(A/phase/'report.md').write_text(text)
print(phase,counts)
