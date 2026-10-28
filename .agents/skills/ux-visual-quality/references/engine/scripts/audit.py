"""Validate audit contracts, select criteria, and render/review evidence-linked reports."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import sys
from urllib.parse import quote, urlparse

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ('Essential', 'Standard', 'Advanced')
EXPECTED_IDS = {f'{group}{number:02}' for group in 'FUASPO' for number in range(1, 7)}
EXPECTED_LEVELS = {
    **{f'F{i:02}': level for i, level in enumerate([*['Essential']*4, 'Standard', 'Advanced'], 1)},
    **{f'U{i:02}': level for i, level in enumerate([*['Essential']*3, *['Standard']*2, 'Advanced'], 1)},
    **{f'A{i:02}': level for i, level in enumerate([*['Essential']*3, *['Standard']*3], 1)},
    **{f'S{i:02}': level for i, level in enumerate([*['Essential']*4, 'Standard', 'Advanced'], 1)},
    **{f'P{i:02}': level for i, level in enumerate([*['Essential']*2, *['Standard']*2, *['Advanced']*2], 1)},
    **{f'O{i:02}': level for i, level in enumerate([*['Essential']*3, *['Standard']*2, 'Advanced'], 1)},
}
# Only identifiers cross-checked against the pinned WCAG Recommendation are permitted.
WCAG_IDS = {
    'A01': ['2.1.1', '2.1.2', '2.4.3'],
    'A02': ['1.3.1', '3.3.2', '4.1.2'],
    'A03': ['1.4.3'], 'A04': ['1.4.4', '1.4.10'],
    'A05': ['2.4.7', '2.4.11'], 'A06': ['2.5.8'],
}


def load(path):
    return json.loads(Path(path).read_text())


def check_schema(value, name):
    definition = load(ROOT / f'schemas/{name}.schema.json')
    Draft202012Validator.check_schema(definition)
    errors = list(Draft202012Validator(definition, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        error = errors[0]
        raise ValueError(f'{name}: {list(error.absolute_path)}: {error.message}')


def unique(items, label):
    ids = [item['id'] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError(f'Duplicate {label} IDs')
    return set(ids)


def validate_catalog(catalog):
    check_schema(catalog, 'catalog')
    if unique(catalog['criteria'], 'criterion') != EXPECTED_IDS:
        raise ValueError('Catalog must contain exactly F/U/A/S/P/O01-06')
    sources = {source['id']: source for source in catalog['sources']}
    unique(catalog['sources'], 'source')
    for source in sources.values():
        url = urlparse(source['url'])
        if url.scheme:
            if url.scheme != 'https' or not url.netloc:
                raise ValueError(f'Invalid source URL: {source["id"]}')
        else:
            target = (ROOT / source['url']).resolve()
            if ROOT not in target.parents or not target.is_file():
                raise ValueError(f'Missing/unsafe local source: {source["id"]}')
    for criterion in catalog['criteria']:
        cid = criterion['id']
        if criterion['group'] != cid[0] or criterion['starts_at'] != EXPECTED_LEVELS[cid]:
            raise ValueError(f'Incorrect group or starting level: {cid}')
        for ref in criterion['sources']:
            if ref['source_id'] not in sources:
                raise ValueError(f'Dangling source: {cid}')
            if ref['requirement_ids']:
                if ref['source_id'] != 'wcag' or ref['requirement_ids'] != WCAG_IDS.get(cid):
                    raise ValueError(f'Unverified requirement mapping: {cid}')
        if cid in WCAG_IDS and not any(
            r['source_id'] == 'wcag' and r['requirement_ids'] == WCAG_IDS[cid]
            for r in criterion['sources']
        ):
            raise ValueError(f'Missing verified WCAG mapping: {cid}')
    return catalog


def select(catalog, profile, level, groups=None):
    check_schema(profile, 'profile')
    if level not in LEVELS:
        raise ValueError(f'Invalid audit level: {level}')
    if groups is None:
        groups = list('FUASPO')
    if not groups or len(groups) != len(set(groups)) or not set(groups) <= set('FUASPO'):
        raise ValueError('Criterion groups must be a nonempty unique subset of F/U/A/S/P/O')
    selections = {}
    for criterion in catalog['criteria']:
        if criterion['group'] not in groups:
            continue
        features = criterion['applicability']['any_features']
        values = [profile['features'][feature] for feature in features]
        if LEVELS.index(criterion['starts_at']) > LEVELS.index(level):
            state, reason = 'deferred', f'Starts at {criterion["starts_at"]}; report observed risks anyway.'
        elif not features or True in values:
            state, reason = 'applicable', 'Core criterion or at least one relevant feature is present.'
        elif None in values:
            state, reason = 'unknown', 'Feature applicability needs investigation.'
        else:
            state = 'not_applicable'
            reason = 'All relevant features are absent: ' + '; '.join(
                f'{feature}: {profile["rationale"][feature]}' for feature in features
            )
        selections[criterion['id']] = {'selection': state, 'reason': reason}
    return selections


def decide(evidence_sufficient, violates_requirement, authorized, measurable_benefit, proportional=True):
    """Severity deliberately does not enter the change-authority decision."""
    if not evidence_sufficient:
        return 'investigate'
    if violates_requirement:
        return 'fix' if authorized and proportional else 'propose'
    if measurable_benefit:
        return 'propose'
    return 'preserve'


def execution_steps(report):
    return {step['id']: step for task in report.get('tasks', []) for step in task['steps']}


def validate_execution(report, selections, evidence_ids):
    """Check declared execution/linkage, not the truth or sufficiency of artifacts."""
    unique(report.get('tasks', []), 'task')
    flat = [step for task in report.get('tasks', []) for step in task['steps']]
    unique(flat, 'step')
    steps = execution_steps(report)
    evidence = {item['id']: item for item in report['evidence']}
    seen = set()
    for task in report.get('tasks', []):
        if not set(task['evidence_ids']) <= evidence_ids:
            raise ValueError(f'Dangling task evidence: {task["id"]}')
        for step in task['steps']:
            sid = step['id']
            # Dependencies precede their consumers: this also rules out cycles.
            if not set(step['depends_on']) <= seen:
                raise ValueError(f'Missing or unordered step dependency: {sid}')
            if not set(step['criterion_ids']) <= selections.keys():
                raise ValueError(f'Step outside declared criterion groups: {sid}')
            if not set(step['evidence_ids']) <= evidence_ids:
                raise ValueError(f'Dangling step evidence: {sid}')
            if step['execution'] != 'completed' and step['status'] != 'unknown':
                raise ValueError(f'Uncompleted step cannot pass or fail: {sid}')
            if step['execution'] == 'not_run' and step['evidence_ids']:
                raise ValueError(f'Unexecuted step cannot claim result evidence: {sid}')
            if step['execution'] != 'not_run' and not step['evidence_ids']:
                raise ValueError(f'Executed step needs attempt/result evidence: {sid}')
            if step['execution'] == 'completed':
                if any(steps[dep]['status'] != 'pass' or steps[dep]['execution'] != 'completed'
                       for dep in step['depends_on']):
                    raise ValueError(f'Completed step has unverified prerequisite: {sid}')
                if step['status'] in ('pass', 'fail'):
                    modes = {mode for eid in step['evidence_ids'] for mode in evidence[eid].get('modes', [])}
                    if not set(step['required_modes']) <= modes:
                        raise ValueError(f'Step evidence modes do not meet declared requirement: {sid}')
            seen.add(sid)
    for finding in report['findings']:
        linked = finding.get('step_ids', [])
        if not set(linked) <= steps.keys():
            raise ValueError(f'Dangling finding step: {finding["id"]}')
        if any(finding['criterion_id'] not in steps[sid]['criterion_ids'] for sid in linked):
            raise ValueError(f'Finding/step criterion mismatch: {finding["id"]}')
        if report.get('report_format') != '1.1':
            continue
        if finding['status'] == 'pass':
            required = {sid for sid, step in steps.items() if finding['criterion_id'] in step['criterion_ids']}
            if not required or not required <= set(linked) or any(
                steps[sid]['execution'] != 'completed' or steps[sid]['status'] != 'pass' for sid in linked
            ):
                raise ValueError(f'Pass requires every declared criterion step completed and passed: {finding["id"]}')
        if finding['status'] == 'fail' and not any(
            steps[sid]['execution'] == 'completed' and steps[sid]['status'] == 'fail' for sid in linked
        ):
            raise ValueError(f'Failure requires a completed failing step: {finding["id"]}')
        if finding['status'] in ('pass', 'fail') and not {
            eid for sid in linked for eid in steps[sid]['evidence_ids']
        } <= set(finding['evidence_ids']):
            raise ValueError(f'Finding must link its step evidence: {finding["id"]}')
    combinations = set()
    for case in report.get('coverage_cases', []):
        key = tuple(case[field] for field in ('url', 'page_type', 'language', 'viewport'))
        if key in combinations:
            raise ValueError('Duplicate coverage combination')
        combinations.add(key)
        if not set(case['step_ids']) <= steps.keys():
            raise ValueError('Dangling coverage step')


def report_counts(report, catalog):
    rows = report['findings']
    selections = select(catalog, report['profile'], report['audit_level'], report.get('criterion_groups'))
    outcomes = {}
    for cid in selections:
        statuses = {row['status'] for row in rows if row['criterion_id'] == cid}
        outcomes[cid] = next((s for s in ('fail', 'unknown', 'pass', 'not_applicable') if s in statuses), 'deferred')
    failures = [row for row in rows if row['status'] == 'fail']
    steps = execution_steps(report)
    cases = report.get('coverage_cases', [])
    return {'finding_rows': dict(Counter(row['status'] for row in rows)),
            'criterion_outcomes': outcomes, 'criteria': dict(Counter(outcomes.values())),
            'failure_severity_rows': dict(Counter(row['severity'] for row in failures)),
            'root_causes': len({row['root_cause_id'] for row in failures})
                if all('root_cause_id' in row for row in failures) else None,
            'test_combinations': len(cases), 'distinct_urls': len({case['url'] for case in cases}),
            'completed_combinations': sum(all(steps[sid]['execution'] == 'completed'
                for sid in case['step_ids']) for case in cases),
            'verified_combinations': sum(all(steps[sid]['execution'] == 'completed' and steps[sid]['status'] == 'pass'
                for sid in case['step_ids']) for case in cases)}


BEGIN = '<!-- toy-to-tool:generated -->'
END = '<!-- /toy-to-tool:generated -->'


def markdown_region(markdown):
    if markdown.count(BEGIN) != 1 or markdown.count(END) != 1:
        raise ValueError('Missing/duplicate generated Markdown region; render explicitly to migrate')
    start, stop = markdown.index(BEGIN), markdown.index(END) + len(END)
    if stop <= start:
        raise ValueError('Invalid generated Markdown region')
    return start, stop


def render_markdown(report, catalog, existing='', evidence_root=None, markdown_path=None):
    """Deterministic generated facts; preserve agent narrative outside the region."""
    digest = hashlib.sha256(json.dumps(report, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
    lines = [BEGIN, f'<!-- report.json sha256: {digest} -->', '## Recorded audit results', '',
             'Generated facts; narrative/translations outside this region must preserve these results.', '',
             '### Counts (units are separate)', '',
             '```json', json.dumps(report_counts(report, catalog), indent=2, ensure_ascii=True), '```', '']
    # Render every field, so new schema fields cannot silently disappear from the handover.
    def fields(record):
        for key, value in record.items():
            encoded = json.dumps(value, ensure_ascii=True)
            # HTML code avoids Markdown delimiters/pipes in untrusted artifact text.
            lines.append(f'- {key}: <code>{html.escape(encoded)}</code>')
        lines.append('')

    lines += ['### Report context and report timestamps', '']
    fields({key: value for key, value in report.items() if key not in ('findings', 'evidence', 'tasks', 'coverage_cases')})
    lines += ['### Findings (severity and remediation priority are separate)', '']
    order = {'blocker': 0, 'important': 1, 'improvement': 2, None: 3}
    for row in sorted(report['findings'], key=lambda row: (order[row['severity']], row['id'])):
        fields(row)
    lines += ['### Tasks and executed steps', '']
    for task in report.get('tasks', []):
        fields({key: value for key, value in task.items() if key != 'steps'})
        for step in task['steps']:
            fields(step)
    lines += ['### Coverage combinations (URL, page type, language, viewport)', '']
    for case in report.get('coverage_cases', []):
        fields(case)
    lines += ['### Evidence (captured_at is observation time)', '']
    for item in report['evidence']:
        fields(item)
        location = item['location']
        if not urlparse(location).scheme and markdown_path is not None:
            root = Path(evidence_root).resolve() if evidence_root is not None else ROOT
            location = Path(os.path.relpath(root / location, Path(markdown_path).resolve().parent)).as_posix()
        lines += [f'[Evidence artifact](<{quote(location, safe="/:#?=&%")}>).', '']
    lines.append(END)
    generated = '\n'.join(lines)
    if existing:
        start, stop = markdown_region(existing)
        return existing[:start] + generated + existing[stop:]
    return '# Application audit handover\n\n' + generated + '\n\n## Agent narrative\n\n'


def check_markdown(report, catalog, markdown, **kwargs):
    start, stop = markdown_region(markdown)
    expected = render_markdown(report, catalog, **kwargs)
    a, b = markdown_region(expected)
    if markdown[start:stop] != expected[a:b]:
        raise ValueError('Markdown is stale or generated facts were edited; render from report.json')


def review_report(report, catalog, evidence_root=None):
    """Read-only review of existing artifacts; deliberately has no runner or network API."""
    validate_report(report, catalog, evidence_root)
    notes = []
    if report.get('report_format') != '1.1':
        notes.append('Legacy report: step coverage is not enforced; no new assurance from validation.')
    for step in execution_steps(report).values():
        if step['execution'] != 'completed' or step['status'] == 'unknown':
            notes.append(f'Unverified step {step["id"]}: {step["execution"]}; missing check: {step["action"]}')
    for finding in report['findings']:
        if finding['status'] == 'unknown':
            notes.append(f'Unknown {finding["id"]}: {finding["verification_plan"]}')
    notes.append('Manual review required: inspect linked artifact contents, criterion-specific evidence sufficiency, '
                 'unrecorded subcases, interruption boundaries, claim scope, counting units and narrative/translation consistency. '
                 'HTTP 200/title proves loading only. Record unknown and the exact missing check; do not rerun the system.')
    return notes


def validate_report(report, catalog, evidence_root=None):
    evidence_root = Path(evidence_root).resolve() if evidence_root is not None else ROOT
    check_schema(report, 'report')
    selections = select(catalog, report['profile'], report['audit_level'], report.get('criterion_groups'))
    evidence_ids = unique(report['evidence'], 'evidence')
    validate_execution(report, selections, evidence_ids)
    for evidence in report['evidence']:
        if report['report_kind'] == 'audit' and evidence['synthetic']:
            raise ValueError('Synthetic evidence cannot support a real audit')
        location = urlparse(evidence['location'])
        if location.scheme:
            if location.scheme != 'https' or not location.netloc:
                raise ValueError('Evidence remote locations must use HTTPS')
        else:
            target = (evidence_root / evidence['location']).resolve()
            if evidence_root not in target.parents or not target.is_file():
                raise ValueError(f'Missing/unsafe local evidence: {evidence["id"]}')
    unique(report['findings'], 'finding')
    covered = set()
    for finding in report['findings']:
        cid, status = finding['criterion_id'], finding['status']
        if cid not in selections:
            raise ValueError(f'Unknown criterion: {cid}')
        covered.add(cid)
        selection = selections[cid]['selection']
        if not set(finding['evidence_ids']) <= evidence_ids:
            raise ValueError(f'Dangling evidence: {finding["id"]}')
        inputs = finding['decision_inputs']
        if finding['decision'] != decide(**inputs):
            raise ValueError(f'Inconsistent decision: {finding["id"]}')
        if inputs['authorized'] and report['change_permission'] != 'fix_scoped':
            raise ValueError('Finding claims change authority not granted by audit scope')
        if status in ('pass', 'fail'):
            if not finding['evidence_ids'] or not inputs['evidence_sufficient']:
                raise ValueError(f'{status} requires linked, sufficient evidence')
        if status == 'fail':
            if finding['severity'] is None or not inputs['violates_requirement']:
                raise ValueError('Failure requires contextual severity and a demonstrated violation')
        elif finding['severity'] is not None:
            raise ValueError('Severity is assigned to failures only; use null for other statuses')
        if status == 'pass' and inputs['violates_requirement']:
            raise ValueError('Passing result cannot claim a demonstrated violation')
        if status == 'unknown' and (inputs['evidence_sufficient'] or finding['decision'] != 'investigate'):
            raise ValueError('Unknown requires investigation; never count it as pass')
        if status == 'not_applicable':
            if selection != 'not_applicable' or finding['decision'] != 'preserve':
                raise ValueError('Not applicable requires supported feature absence and preserve')
            if inputs['violates_requirement'] or inputs['measurable_benefit']:
                raise ValueError('Not applicable cannot assert a violation or change benefit')
        if selection == 'not_applicable' and status != 'not_applicable':
            raise ValueError('Profile contradicts criterion applicability; correct the profile first')
        if selection == 'unknown' and status != 'unknown':
            raise ValueError('Resolve feature applicability before assigning an outcome')
        if report['report_kind'] == 'template' and status in ('pass', 'fail'):
            raise ValueError('Unexecuted templates cannot claim tested outcomes')
        if selection == 'deferred':
            actual = select(catalog, report['profile'], 'Advanced')[cid]['selection']
            if status != 'unknown' and actual != 'applicable':
                raise ValueError('Out-of-level result contradicts profile; resolve applicability first')
            if status != 'unknown' and not finding['observed_outside_level']:
                raise ValueError('Out-of-level observation must be explicitly identified')
        elif finding['observed_outside_level']:
            raise ValueError('In-level finding cannot be labeled outside level')
    required = {cid for cid, item in selections.items() if item['selection'] != 'deferred'}
    if not required <= covered:
        raise ValueError(f'Missing selected criterion outcomes: {sorted(required - covered)}')
    return report


def template(catalog, profile, level, permission='read_only', groups=None, report_format='1.1'):
    if report_format not in ('1.0', '1.1'):
        raise ValueError('Unsupported report format')
    selections = select(catalog, profile, level, groups)
    findings = []
    for cid, item in selections.items():
        if item['selection'] == 'deferred':
            continue
        na = item['selection'] == 'not_applicable'
        findings.append({
            'id': f'finding-{cid}', 'criterion_id': cid,
            'status': 'not_applicable' if na else 'unknown', 'severity': None,
            'decision': 'preserve' if na else 'investigate',
            'reason': item['reason'] if na else item['reason'] + ' No test observations recorded yet.',
            'requirement_or_goal': 'Collect or link the agreed criterion-specific requirement.',
            'affected_users_and_conditions': 'Identify the audience and tested conditions.',
            'evidence_ids': [],
            'decision_inputs': {'evidence_sufficient': na, 'violates_requirement': False,
                                'authorized': False, 'measurable_benefit': False, 'proportional': True},
            'change_scope_cost_risk': 'No change authorized or evaluated for this row yet.',
            'verification_plan': 'Follow criterion test_steps and verification; link observations before concluding.',
            'observed_outside_level': False,
            **({'step_ids': []} if report_format == '1.1' else {}),
        })
    now = datetime.now(timezone.utc).isoformat()
    return {**({'report_format': '1.1', 'created_at': now, 'updated_at': now,
                'tasks': [], 'coverage_cases': []} if report_format == '1.1' else {}),
            **({'criterion_groups': groups} if groups is not None else {}),
            'report_kind': 'template', 'catalog_version': catalog['version'], 'audit_level': level,
            'change_permission': permission, 'profile': profile,
            'scope_and_limitations': 'Unexecuted template; profile facts require confirmation. No application assurance claimed.',
            'evidence': [], 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'select', 'template', 'render', 'review'])
    parser.add_argument('--catalog', type=Path, default=ROOT / 'criteria/v1.json')
    parser.add_argument('--profile', type=Path, default=ROOT / 'examples/profile.json')
    parser.add_argument('--level', choices=LEVELS, default='Essential')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--markdown', type=Path, help='Markdown view; defaults to the report path with .md suffix.')
    parser.add_argument('--evidence-root', type=Path, default=ROOT, help='Explicit allowed root for local report artifacts; defaults to the engine root.')
    parser.add_argument('--group', dest='groups', action='append', choices=list('FUASPO'),
                        help='Limit selection/template to this group; repeat for several groups.')
    args = parser.parse_args()
    try:
        catalog = validate_catalog(load(args.catalog))
        if args.command in ('render', 'review'):
            if args.report is None:
                raise ValueError('--report is required for render/review')
            report = load(args.report)
            notes = review_report(report, catalog, args.evidence_root)
            markdown = args.markdown or args.report.with_suffix('.md')
            options = {'evidence_root': args.evidence_root, 'markdown_path': markdown}
            if args.command == 'render':
                existing = markdown.read_text() if markdown.exists() else ''
                markdown.write_text(render_markdown(report, catalog, existing=existing, **options))
                print(f'Rendered: {markdown}; observation/report timestamps unchanged.')
            else:
                check_markdown(report, catalog, markdown.read_text(), **options)
                print('\n'.join(notes))
        elif args.command == 'validate':
            if args.report:
                validate_report(load(args.report), catalog, evidence_root=args.evidence_root)
                if args.markdown:
                    check_markdown(load(args.report), catalog, args.markdown.read_text(),
                                   evidence_root=args.evidence_root, markdown_path=args.markdown)
            print('Valid: 36 unique criteria; structure, levels and references checked.' +
                  (' Report structure, coverage and decisions checked.' if args.report else ''))
        else:
            profile = load(args.profile)
            value = select(catalog, profile, args.level, args.groups) if args.command == 'select' else template(catalog, profile, args.level, groups=args.groups)
            print(json.dumps(value, indent=2))
    except (ValueError, OSError) as error:
        print(f'Invalid: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
