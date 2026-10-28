"""Synthetic contract tests; these observations are never application assurance."""
import copy
import io
import itertools
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import audit


class ReportReviewTests(unittest.TestCase):
    def setUp(self):
        self.catalog = audit.load(audit.ROOT / 'criteria/v1.json')
        self.report = audit.template(self.catalog, audit.load(audit.ROOT / 'examples/profile.json'),
                                     'Essential', groups=['F'])
        self.report['report_kind'] = 'synthetic'
        self.report['evidence'] = [dict(id='E-load', location='examples/evidence/demo.txt',
            description='Synthetic HTTP 200 and title', environment='isolated synthetic test',
            captured_at='2026-10-28T00:00:00Z', kind='observation', synthetic=True,
            modes=['page_load'])]
        # Use an existing synthetic artifact, never a real audit observation.
        self.report['evidence'][0]['location'] = audit.load(audit.ROOT / 'examples/report.json')['evidence'][0]['location']
        self.report['tasks'] = [dict(id='T-save', actor='editor', starting_state='draft',
            expected_outcome='Saved value survives reopening', evidence_ids=['E-load'], steps=[
                self.step('load', [], ['page_load']),
                self.step('context', ['load'], ['interaction']),
                self.step('readback', ['context'], ['independent_confirmation'])])]
        self.row = self.report['findings'][0]
        self.row['step_ids'] = ['load', 'context', 'readback']

    def step(self, sid, dependencies, modes):
        return dict(id=sid, criterion_ids=['F01'], action=sid, expected_result='Expected ' + sid,
            actual_result='Not executed', execution='not_run', status='unknown',
            depends_on=dependencies, required_modes=modes, evidence_ids=[])

    def pass_row(self):
        self.row.update(status='pass', decision='preserve', evidence_ids=['E-load'])
        self.row['decision_inputs']['evidence_sufficient'] = True

    def test_interruption_does_not_verify_later_context_or_readback(self):
        steps = self.report['tasks'][0]['steps']
        steps[0].update(execution='interrupted', actual_result='Runner stopped', evidence_ids=['E-load'])
        audit.validate_report(self.report, self.catalog)
        self.assertEqual(steps[1]['execution'], 'not_run')
        self.assertEqual(steps[2]['status'], 'unknown')
        self.pass_row()
        with self.assertRaisesRegex(ValueError, 'completed|step'):
            audit.validate_report(self.report, self.catalog)

    def test_http_200_cannot_establish_task_completion(self):
        for step in self.report['tasks'][0]['steps']:
            step.update(execution='completed', status='pass', actual_result='HTTP 200', evidence_ids=['E-load'])
        self.pass_row()
        with self.assertRaisesRegex(ValueError, 'mode'):
            audit.validate_report(self.report, self.catalog)

    def test_source_contract_does_not_require_browser_evidence(self):
        self.report['evidence'][0]['modes'] = ['source_inspection']
        step = self.report['tasks'][0]['steps'][0]
        step.update(required_modes=['source_inspection'], execution='completed', status='pass',
                    actual_result='Source contract inspected', evidence_ids=['E-load'])
        self.report['tasks'][0]['steps'] = [step]
        self.row['step_ids'] = ['load']
        self.pass_row()
        audit.validate_report(self.report, self.catalog)

    def test_cannot_omit_unexecuted_tail_from_pass(self):
        step = self.report['tasks'][0]['steps'][0]
        step.update(execution='completed', status='pass', actual_result='Loaded', evidence_ids=['E-load'])
        self.row['step_ids'] = ['load']
        self.pass_row()
        with self.assertRaisesRegex(ValueError, 'every declared'):
            audit.validate_report(self.report, self.catalog)

    def test_completed_check_cannot_follow_unverified_prerequisite(self):
        self.report['tasks'][0]['steps'][1].update(execution='completed', status='unknown',
            actual_result='Incorrectly marked reached', evidence_ids=['E-load'])
        with self.assertRaisesRegex(ValueError, 'prerequisite'):
            audit.validate_report(self.report, self.catalog)

    def test_step_modes_are_not_a_substitute_for_linked_evidence(self):
        step = self.report['tasks'][0]['steps'][0]
        step.update(execution='completed', status='pass', actual_result='Loaded', evidence_ids=['E-load'])
        self.report['tasks'][0]['steps'] = [step]
        self.row['step_ids'] = ['load']
        self.pass_row()
        self.row['evidence_ids'] = []
        with self.assertRaisesRegex(ValueError, 'step evidence'):
            audit.validate_report(self.report, self.catalog)

    def test_synthetic_step_example_validates_without_new_assurance(self):
        example = audit.load(audit.ROOT / 'examples/report-steps.json')
        audit.validate_report(example, self.catalog)
        self.assertEqual(example['report_kind'], 'synthetic')
        self.assertEqual(example['findings'][0]['status'], 'unknown')

    def test_render_cli_preserves_observation_and_report_times(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            path.write_text(json.dumps(self.report))
            before = path.read_bytes()
            with patch('sys.argv', ['audit.py', 'render', '--report', str(path)]), \
                 patch('sys.stdout', new_callable=io.StringIO):
                self.assertEqual(audit.main(), 0)
            self.assertEqual(path.read_bytes(), before)
            md = path.with_suffix('.md')
            self.assertIn('2026-10-28T00:00:00Z', md.read_text())
            self.report['updated_at'] = '2026-10-29T00:00:00Z'
            path.write_text(json.dumps(self.report))
            with patch('sys.argv', ['audit.py', 'review', '--report', str(path)]), \
                 patch('sys.stderr', new_callable=io.StringIO):
                self.assertEqual(audit.main(), 1)

    def test_legacy_narrative_is_not_silently_overwritten(self):
        with self.assertRaisesRegex(ValueError, 'migrate'):
            audit.render_markdown(self.report, self.catalog, existing='# Old handover\n')

    def test_counts_combinations_and_distinct_urls(self):
        self.report['coverage_cases'] = [dict(url=f'https://example.test/{kind}/{language}',
            page_type=kind, language=language, viewport=viewport, step_ids=['load'])
            for kind, language, viewport in itertools.product(
                ['home', 'edit', 'list'], ['en', 'vi', 'fr'], ['320', '390', '768', '1440'])]
        counts = audit.report_counts(self.report, self.catalog)
        self.assertEqual(counts['test_combinations'], 36)
        self.assertEqual(counts['distinct_urls'], 9)
        self.assertEqual(counts['completed_combinations'], 0)
        self.report['coverage_cases'].append(copy.deepcopy(self.report['coverage_cases'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate.*combination'):
            audit.validate_report(self.report, self.catalog)

    def test_json_change_and_generated_edit_are_detected_and_narrative_preserved(self):
        md = audit.render_markdown(self.report, self.catalog) + '\nAgent narrative in Vietnamese.\n'
        audit.check_markdown(self.report, self.catalog, md)
        self.report['scope_and_limitations'] = 'Narrower scope'
        with self.assertRaisesRegex(ValueError, 'stale'):
            audit.check_markdown(self.report, self.catalog, md)
        updated = audit.render_markdown(self.report, self.catalog, existing=md)
        self.assertIn('Agent narrative in Vietnamese.', updated)
        audit.check_markdown(self.report, self.catalog, updated)
        with self.assertRaises(ValueError):
            audit.check_markdown(self.report, self.catalog, updated.replace('unknown', 'pass', 1))

    def test_disabled_feature_preserves_severity_and_groups_root_cause(self):
        self.row.update(status='fail', severity='blocker', decision='propose', root_cause_id='RC-save',
            remediation_priority='After enabling flag; before rollout',
            affected_users_and_conditions='Editors; flag SAVE_V2=true (default off); local Chrome',
            evidence_ids=['E-load'])
        self.row['decision_inputs'].update(evidence_sufficient=True, violates_requirement=True)
        step = self.report['tasks'][0]['steps'][0]
        step.update(criterion_ids=['F01', 'F02'], execution='completed', status='fail',
                    actual_result='Demonstrated load failure', evidence_ids=['E-load'])
        other = copy.deepcopy(self.row)
        other.update(id='same-root-F02', criterion_id='F02', step_ids=['load'])
        self.report['findings'].append(other)
        audit.validate_report(self.report, self.catalog)
        counts = audit.report_counts(self.report, self.catalog)
        self.assertEqual(counts['root_causes'], 1)
        self.assertEqual(counts['finding_rows']['fail'], 2)
        md = audit.render_markdown(self.report, self.catalog)
        self.assertIn('default off', md)
        self.assertIn('blocker', md)
        self.assertIn('After enabling flag', md)

    def test_review_only_reads_artifacts_and_never_calls_application_runner(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            import json
            path.write_text(json.dumps(self.report))
            md = path.with_suffix('.md')
            md.write_text(audit.render_markdown(self.report, self.catalog,
                          evidence_root=audit.ROOT, markdown_path=md))
            before = {p: p.read_bytes() for p in (path, md)}
            with patch('subprocess.run', side_effect=AssertionError('application runner called')), \
                 patch('subprocess.Popen', side_effect=AssertionError('application launched')), \
                 patch('sys.argv', ['audit.py', 'review', '--report', str(path)]), \
                 patch('sys.stdout', new_callable=io.StringIO) as output:
                self.assertEqual(audit.main(), 0)
            self.assertIn('Manual', output.getvalue())
            self.assertEqual(before, {p: p.read_bytes() for p in (path, md)})

    def test_legacy_validation_stays_supported_but_review_discloses_limit(self):
        legacy = audit.load(audit.ROOT / 'examples/report.json')
        audit.validate_report(legacy, self.catalog)
        self.assertIn('legacy', ' '.join(audit.review_report(legacy, self.catalog)).lower())


if __name__ == '__main__':
    unittest.main()
