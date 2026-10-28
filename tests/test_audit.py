import copy
import unittest
from scripts.audit import validate_catalog, validate_report, select, decide, load, ROOT


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load(ROOT / 'criteria/v1.json')
        cls.profile = load(ROOT / 'examples/profile.json')

    def test_catalog_is_complete(self):
        validate_catalog(self.catalog)
        self.assertEqual(len(self.catalog['criteria']), 36)

    def test_rejects_duplicate_and_missing_ids(self):
        bad = copy.deepcopy(self.catalog)
        bad['criteria'][0] = bad['criteria'][1]
        with self.assertRaises(ValueError):
            validate_catalog(bad)

    def test_rejects_missing_detail_and_dangling_source(self):
        for field in ('verification', 'test_steps', 'sources'):
            bad = copy.deepcopy(self.catalog)
            del bad['criteria'][0][field]
            with self.assertRaises(ValueError):
                validate_catalog(bad)
        bad = copy.deepcopy(self.catalog)
        bad['criteria'][0]['sources'][0]['source_id'] = 'missing'
        with self.assertRaises(ValueError):
            validate_catalog(bad)

    def test_levels_are_cumulative_but_features_are_conditional(self):
        essential = select(self.catalog, self.profile, 'Essential')
        advanced = select(self.catalog, self.profile, 'Advanced')
        self.assertEqual(essential['F06']['selection'], 'deferred')
        self.assertEqual(advanced['F06']['selection'], 'not_applicable')
        self.assertEqual(essential['S02']['selection'], 'unknown')
        self.assertEqual(advanced['F01']['selection'], 'applicable')
        self.assertEqual(advanced['A06']['selection'], 'applicable')

    def test_decisions_do_not_depend_on_severity(self):
        self.assertEqual(decide(True, True, True, True), 'fix')
        self.assertEqual(decide(True, True, False, True), 'propose')
        self.assertEqual(decide(True, False, True, False), 'preserve')
        self.assertEqual(decide(False, True, True, True), 'investigate')
        self.assertEqual(decide(True, False, False, True), 'propose')
        self.assertEqual(decide(True, True, True, True, proportional=False), 'propose')

    def test_example_report_is_consistent(self):
        validate_report(load(ROOT / 'examples/report.json'), self.catalog)

    def test_report_rejects_invalid_enums_and_dangling_evidence(self):
        for field, value in [('status', 'ok'), ('severity', 'critical'),
                             ('decision', 'ignore'), ('evidence_ids', ['missing'])]:
            report = load(ROOT / 'examples/report.json')
            report['findings'][0][field] = value
            with self.assertRaises(ValueError):
                validate_report(report, self.catalog)

    def test_report_rejects_unsupported_pass_and_unjustified_na(self):
        report = load(ROOT / 'examples/report.json')
        row = next(f for f in report['findings'] if f['status'] == 'unknown')
        row['status'] = 'pass'
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)
        report = load(ROOT / 'examples/report.json')
        row = next(f for f in report['findings'] if f['status'] == 'not_applicable')
        row['reason'] = ''
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)

    def test_report_requires_coverage_and_consistent_decision(self):
        report = load(ROOT / 'examples/report.json')
        report['findings'].pop()
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)
        report = load(ROOT / 'examples/report.json')
        report['findings'][0]['decision'] = 'preserve'
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)

    def test_profile_rejects_unknown_keys_and_boolean_strings(self):
        for key, value in [('shared_writes', 'false'), ('typo', True)]:
            profile = copy.deepcopy(self.profile)
            profile['features'][key] = value
            with self.assertRaises(ValueError):
                select(self.catalog, profile, 'Advanced')

    def test_real_report_cannot_use_synthetic_evidence(self):
        report = load(ROOT / 'examples/report.json')
        report['report_kind'] = 'audit'
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)

    def test_local_evidence_artifact_must_exist(self):
        report = load(ROOT / 'examples/report.json')
        report['evidence'][0]['location'] = 'examples/missing-trace.txt'
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)

    def test_blocker_remains_blocker_without_fix_authority(self):
        report = load(ROOT / 'examples/report.json')
        report['change_permission'] = 'read_only'
        row = report['findings'][0]
        row['decision_inputs']['authorized'] = False
        row['decision'] = 'propose'
        validate_report(report, self.catalog)
        self.assertEqual(row['severity'], 'blocker')

    def test_out_of_level_failure_requires_explicit_observation(self):
        report = load(ROOT / 'examples/report.json')
        report['audit_level'] = 'Essential'
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)
        # Trim unobserved higher-level rows; keep the O03 in-level failure.
        selected = select(self.catalog, report['profile'], 'Essential')
        report['findings'] = [r for r in report['findings']
                              if selected[r['criterion_id']]['selection'] != 'deferred']
        observed = copy.deepcopy(report['findings'][0])
        observed.update(id='outside-P05', criterion_id='P05', observed_outside_level=True)
        report['findings'].append(observed)
        # The hypothetical profile says there is no load requirement.
        with self.assertRaises(ValueError):
            validate_report(report, self.catalog)
        report['profile']['features']['load_requirements'] = True
        report['profile']['rationale']['load_requirements'] = 'Observed contract requires this load.'
        validate_report(report, self.catalog)


if __name__ == '__main__':
    unittest.main()
