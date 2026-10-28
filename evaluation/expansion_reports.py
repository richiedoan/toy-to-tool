"""Reuse the canonical report contract for bounded evaluator observations and gaps."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit import load, template, select, validate_catalog, validate_report
from evaluation.make_report import outcome

BUNDLE = ROOT / 'evaluation/evidence/expansion-v1'
CASES = {
    'owner-notes': {'S02': ['owner-positive-controls', 'cross-owner-read', 'cross-owner-write', 'owned-edit-and-validation'],
                    'S03': ['owned-edit-and-validation', 'login-desktop-preserve'],
                    'S04': ['session-lifecycle', 'session-expiry', 'login-desktop-preserve']},
    'dashboard': {'U01': ['desktop-approved'], 'U02': ['error-recovery', 'loading-empty-correction'],
                  'U03': ['layout-320', 'layout-390', 'layout-768', 'layout-1440'],
                  'U04': ['loading-empty-correction'], 'U05': ['desktop-approved'],
                  'A01': ['keyboard-focus-targets'], 'A02': ['desktop-approved', 'keyboard-focus-targets'],
                  'A03': ['text-contrast'], 'A04': ['layout-320', 'resize-text'],
                  'A05': ['keyboard-focus-targets'], 'A06': ['keyboard-focus-targets'],
                  'P01': ['repeat-refresh-resources'], 'P02': ['error-recovery'],
                  'P03': ['local-filter-budget'], 'P04': ['repeat-refresh-resources'],
                  'O01': ['clean-startup-smoke'], 'O04': ['operator-diagnostics']},
}
GAPS = {'S01': 'No complete secret/sensitive-surface inventory and authorized history review was executed.',
        'S05': 'Architecture-relevant CSRF/public-endpoint/abuse subcases were not all exercised; no blanket security pass.',
        'A02': 'Native name/label positive controls passed, but actual assistive-technology behavior was not exercised.',
        'A04': 'Original narrow-layout geometry was rechecked; text-scale probe is supplemental, not complete zoom/state conformance coverage.',
        'P02': 'The observed 503 recovery was rechecked; offline and timeout paths remain unexecuted.',
        'P03': 'The agreed local task budget was measured; adequate field p75 LCP/INP/CLS data does not exist.',
        'P04': 'Bounded repeated-request controls ran; full timer/subscription/teardown resource lifecycle evidence is missing.'}



def assess(criterion_id, cases):
    observed = outcome(cases)
    return 'unknown' if observed != 'fail' and criterion_id in GAPS else observed


def profile(name):
    keys = load(ROOT / 'schemas/profile.schema.json')['properties']['features']['properties']
    true = {'ui', 'pointer_ui', 'operations', 'inputs', 'user_changes', 'network', 'resource_lifecycle', 'public_endpoints', 'operated_service'}
    false = {'uploads', 'deployed', 'important_data', 'load_requirements', 'realtime', 'offline_sync', 'background_sync', 'cors_surface'}
    if name == 'owner-notes':
        true |= {'persistent_data', 'authentication', 'protected_resources', 'untrusted_execution', 'csrf_surface'}
    else:
        false |= {'persistent_data', 'authentication', 'protected_resources', 'csrf_surface', 'untrusted_execution', 'shared_writes'}
    return {'name': name + ' disposable local fixture', 'features': {k: True if k in true else False if k in false else None for k in keys},
            'rationale': {k: 'E-context: ' + ('present in documented tasks/source and exercised runtime.' if k in true else
                            'absent from the explicitly local, replaceable-data architecture/contract.' if k in false else
                            'not established; do not infer absence from this focused trial.') for k in keys}}


def build(name, phase):
    folder = BUNDLE / name
    output = folder / f'{phase}-report.json'
    if output.exists():
        raise ValueError('Immutable report already exists')
    raw_path = folder / phase / 'results.json'; raw = load(raw_path)
    by_id = {case['id']: case for case in raw['results']}
    catalog = validate_catalog(load(ROOT / 'criteria/v1.json'))
    protocols = {c['id']: c for c in catalog['criteria']}
    groups = ['S'] if name == 'owner-notes' else list('UAPO')
    report = template(catalog, profile(name), 'Standard', 'fix_scoped', groups=groups, report_format='1.0')
    report.update(report_kind='audit', scope_and_limitations=(
        'Evaluator-led real HTTP/Chrome checks on an isolated seeded fixture. Scope is limited to recorded cases; '
        'source/handler-only independent agent findings are archived separately. No skill-effectiveness, full WCAG, '
        'field CWV or ASVS certification claim. See E-context and E-preservation.'))
    report['evidence'] = []
    def evidence(eid, path, description, kind='observation'):
        report['evidence'].append({'id': eid, 'location': str(path.relative_to(ROOT)), 'description': description,
            'environment': json.dumps(raw['environment']), 'captured_at': raw['captured_at'], 'kind': kind, 'synthetic': False})
    evidence('E-context', folder / 'context.md', 'Agreed tasks, safe scope, source inspection, capability and evidence limits.', 'requirement')
    evidence('E-preservation', folder / 'preservation.json', 'Protected source hashes and identical approved screenshot comparison.', 'artifact')
    for case_id in by_id:
        evidence('E-' + case_id, raw_path, 'Executed case ' + case_id + ': raw HTTP/UI/measurement observations and reproduction steps.')
    for row in report['findings']:
        cid = row['criterion_id']; case_ids = CASES[name].get(cid, [])
        cases = [by_id[case_id] for case_id in case_ids]
        status = assess(cid, cases)
        if row['status'] == 'not_applicable':
            row['evidence_ids'] = ['E-context']
            row['requirement_or_goal'] = protocols[cid]['expected_behavior']
            row['affected_users_and_conditions'] = 'No qualifying deployment, important data or persistent user storage exists in this documented fixture.'
            row['change_scope_cost_risk'] = 'Preserve the local replaceable-data setup; no infrastructure addition is justified.'
            row['verification_plan'] = 'Revisit applicability if the deployment, data importance or persistence contract changes.'
            continue
        failed = status == 'fail'; sufficient = status in ('pass', 'fail')
        reason = ('Demonstrated assertion failure in: ' + ', '.join(c['id'] for c in cases if c['status'] == 'fail') if failed else
                  GAPS[cid] if cid in GAPS else 'All listed applicable cases passed; conclusion limited to these tasks/states.')
        if cid == 'U01': reason += ' This is expert task-alignment review, not real-user understanding evidence.'
        row.update(status=status, severity=('blocker' if cid in ('U03', 'A04') else 'important') if failed else None,
            decision='fix' if failed else 'preserve' if status == 'pass' else 'investigate', reason=reason,
            requirement_or_goal=protocols[cid]['expected_behavior'],
            affected_users_and_conditions='Disposable local fixture users in the documented tasks and recorded browser/API environment.',
            evidence_ids=['E-context'] + ['E-' + case_id for case_id in case_ids] + (['E-preservation'] if cid in ('U05', 'S02', 'S03', 'S04') else []),
            decision_inputs={'evidence_sufficient': sufficient, 'violates_requirement': failed, 'measurable_benefit': failed,
                             'authorized': failed, 'proportional': True},
            change_scope_cost_risk='Only the demonstrated target-app correction is authorized; preserve approved controls, design and architecture. Unknown subcases require evidence, not speculative refactoring.',
            verification_plan='Repeat the original cases with matching source/environment, compare protected-file hashes and approved screenshots, then collect the named missing evidence before any broader pass.')
    validate_report(report, catalog)
    output.write_text(json.dumps(report, indent=2) + '\n')
    (folder / f'{phase}-selection.json').write_text(json.dumps(select(catalog, report['profile'], 'Standard', groups=groups), indent=2) + '\n')
    lines = [f'# {name}: {phase} report', '', report['scope_and_limitations'], '',
        f'[Schema-validated JSON]({phase}-report.json) | [Context](context.md) | [Preservation evidence](preservation.json)', '',
        '| Criterion | Status | Severity | Decision | Evidence and reason |', '| --- | --- | --- | --- | --- |']
    for row in sorted(report['findings'], key=lambda r: (0 if r['severity'] == 'blocker' else 1 if r['status'] == 'fail' else 2, r['criterion_id'])):
        lines.append(f'| {row["criterion_id"]} | {row["status"]} | {row["severity"] or "null"} | {row["decision"]} | {row["reason"]} [Evidence]({phase}/results.json), [scope](context.md) |')
    lines += ['', 'Deferred higher-level IDs are listed in the selection JSON; other groups have no assessed outcome. Unknown is never pass. No overall quality score.', '',
              'Original failing reproductions that now succeed are retained in the before evidence. Some broader criteria remain unknown despite verified corrections because their remaining protocols were not executed.']
    (folder / f'{phase}-report.md').write_text('\n'.join(lines) + '\n')
    print(output)


if __name__ == '__main__':
    for name in CASES:
        for phase in ('before', 'after'):
            build(name, phase)
