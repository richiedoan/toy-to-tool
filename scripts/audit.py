"""Validate the v1 contract and emit deterministic criterion selections/report templates."""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

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


def validate_report(report, catalog):
    check_schema(report, 'report')
    selections = select(catalog, report['profile'], report['audit_level'], report.get('criterion_groups'))
    evidence_ids = unique(report['evidence'], 'evidence')
    for evidence in report['evidence']:
        if report['report_kind'] == 'audit' and evidence['synthetic']:
            raise ValueError('Synthetic evidence cannot support a real audit')
        location = urlparse(evidence['location'])
        if location.scheme:
            if location.scheme != 'https' or not location.netloc:
                raise ValueError('Evidence remote locations must use HTTPS')
        else:
            target = (ROOT / evidence['location']).resolve()
            if ROOT not in target.parents or not target.is_file():
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


def template(catalog, profile, level, permission='read_only', groups=None):
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
        })
    return {**({'criterion_groups': groups} if groups is not None else {}),
            'report_kind': 'template', 'catalog_version': catalog['version'], 'audit_level': level,
            'change_permission': permission, 'profile': profile,
            'scope_and_limitations': 'Unexecuted template; profile facts require confirmation. No application assurance claimed.',
            'evidence': [], 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'select', 'template'])
    parser.add_argument('--catalog', type=Path, default=ROOT / 'criteria/v1.json')
    parser.add_argument('--profile', type=Path, default=ROOT / 'examples/profile.json')
    parser.add_argument('--level', choices=LEVELS, default='Essential')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--group', dest='groups', action='append', choices=list('FUASPO'),
                        help='Limit selection/template to this group; repeat for several groups.')
    args = parser.parse_args()
    try:
        catalog = validate_catalog(load(args.catalog))
        if args.command == 'validate':
            if args.report:
                validate_report(load(args.report), catalog)
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
