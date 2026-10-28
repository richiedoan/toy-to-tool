"""Create evaluator reports from actual tracker browser observations, not oracle answers."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit import load, select, template, validate_catalog, validate_report


BUNDLE = ROOT / 'evaluation/evidence/tracker-v1'
CASES = {
    'F01': ['create-readback', 'save-readback', 'save-repeat'],
    'F02': ['refresh', 'reopen'],
    'F03': ['save-readback', 'create-storage-failure', 'save-storage-failure', 'feedback-timing'],
    'F04': ['create-readback', 'title-boundaries', 'note-boundaries'],
    'F05': ['rapid-repeat', 'intentional-repeat', 'save-repeat'],
}
REQUIREMENTS = {
    'F01': 'Create and edit actual task values, not just interface fields or a completion message.',
    'F02': 'Saved records load after refresh and app-tab reopen at the same origin/profile.',
    'F03': 'Completion feedback follows actual committed results; rejected writes preserve draft and previous data.',
    'F04': 'Trimmed titles allow 1-80 characters; notes allow up to 500; valid Unicode and punctuation are accepted.',
    'F05': 'One pending intention creates one identity; later intentional same-title actions remain possible.',
}



def outcome(cases):
    """A probe/infrastructure error alone cannot establish an application failure."""
    if any(case.get('status') == 'fail' and case.get('error', '').startswith('AssertionError') for case in cases):
        return 'fail'
    if cases and all(case.get('status') == 'pass' for case in cases):
        return 'pass'
    return 'unknown'


def build(phase):
    output = BUNDLE / f'{phase}-report.json'
    if output.exists():
        raise ValueError('Reports are immutable; choose a new run directory for another audit')
    catalog = validate_catalog(load(ROOT / 'criteria/v1.json'))
    raw_path = BUNDLE / phase / 'results.json'
    raw = load(raw_path)
    cases = {result['id']: result for result in raw['results']}
    keys = load(ROOT / 'schemas/profile.schema.json')['properties']['features']['properties']
    present = {'ui', 'pointer_ui', 'operations', 'inputs', 'persistent_data', 'user_changes'}
    profile = {'name': 'Single-person local browser tracker',
               'features': {key: key in present for key in keys},
               'rationale': {key: 'E-context: fixture README, app code and tested browser contract; ' +
                             ('feature present.' if key in present else 'not part of this local, non-sensitive, single-editor contract.') for key in keys}}
    report = template(catalog, profile, 'Standard', 'fix_scoped', groups=['F'])
    report.update(report_kind='audit', scope_and_limitations=(
        'Evaluator-led real Chrome workflow checks of a deliberately seeded fixture. '
        'Not an agent-effectiveness comparison. See E-context for scope and limitations. '
        'Some assertions following a first failure did not run; no pass claimed for those subcases.'))
    report['evidence'] = [{'id': 'E-context', 'location': str((BUNDLE / 'context.md').relative_to(ROOT)),
                           'description': 'Agreed tasks, environment, authorization and scope limitations.',
                           'environment': 'Local disposable tracker fixture', 'captured_at': raw['captured_at'],
                           'kind': 'requirement', 'synthetic': False}]
    for case_id in cases:
        report['evidence'].append({'id': 'E-' + case_id, 'location': str(raw_path.relative_to(ROOT)),
                                  'description': f'Actual browser result {case_id}; see its steps, observed storage/UI and adjacent screenshot/trace.',
                                  'environment': json.dumps(raw['environment']), 'captured_at': raw['captured_at'],
                                  'kind': 'observation', 'synthetic': False})
    for row in report['findings']:
        cid = row['criterion_id']
        selected = [cases[name] for name in CASES[cid]]
        status = outcome(selected)
        failed = [case['id'] for case in selected if case['status'] == 'fail' and case.get('error', '').startswith('AssertionError')]
        row.update(status=status,
                   severity=('blocker' if cid in ('F01', 'F02') else 'important') if failed else None,
                   decision='fix' if failed else 'investigate' if status == 'unknown' else 'preserve',
                   reason=('Executed browser assertion failures: ' + ', '.join(failed) + '. Later assertions after a failure remain unexecuted.' if failed else
                           'A required observation is unavailable or a probe failed; investigate before concluding.' if status == 'unknown' else
                           'All listed protocol scenarios completed their assertions in actual Chrome; claim limited to recorded cases.'),
                   requirement_or_goal=REQUIREMENTS[cid],
                   affected_users_and_conditions='Single local user with disposable tasks at the same browser origin/profile.',
                   evidence_ids=['E-context'] + ['E-' + name for name in CASES[cid]],
                   decision_inputs={'evidence_sufficient': status != 'unknown', 'violates_requirement': bool(failed),
                                    'measurable_benefit': bool(failed), 'authorized': bool(failed), 'proportional': True},
                   change_scope_cost_risk=('Correct existing handlers/loading only; preserve browser-local architecture and valid data. See recorded patch.' if failed else
                                           'No correction is supported until the missing observation is collected.' if status == 'unknown' else
                                           'Preserve the verified implementation and local-only architecture; no demonstrated need for a database or sync.'),
                   verification_plan='Run the same browser scenarios against the exact recorded app hashes; compare committed values, counts and failure behavior.')
    validate_report(report, catalog)
    output.write_text(json.dumps(report, indent=2) + '\n')
    (BUNDLE / f'{phase}-selection.json').write_text(json.dumps(select(catalog, profile, 'Standard', groups=['F']), indent=2) + '\n')
    lines = [f'# {phase.title()} Functionality & Data report', '', report['scope_and_limitations'], '',
             'See [context](context.md) and the [schema-validated JSON](' + output.name + ').', '',
             '| Criterion | Status | Severity | Decision | Evidence |', '| --- | --- | --- | --- | --- |']
    for row in report['findings']:
        links = f'[raw browser observations]({phase}/results.json); [context](context.md)'
        lines.append(f'| {row["criterion_id"]} | {row["status"]} | {row["severity"] or "null"} | {row["decision"]} | {links} |')
    lines += ['', 'F06: deferred at Standard; see [scope evidence](context.md). Other groups are outside this trial.', '',
              'Each row in JSON names its evidence case IDs. Raw results include steps, actual values and any assertion error; matching PNG and trace ZIP files are adjacent. No overall score is assigned.']
    (BUNDLE / f'{phase}-report.md').write_text('\n'.join(lines) + '\n')
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['before', 'after'])
    build(parser.parse_args().phase)
