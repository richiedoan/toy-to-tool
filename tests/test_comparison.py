import copy
from pathlib import Path
import subprocess
import tempfile
import unittest

from evaluation.comparison_runner import prepare, summarize, validate_config, verify_inputs, load, ROOT


class ComparisonTests(unittest.TestCase):
    def test_paired_inputs_are_identical_except_installed_skills(self):
        config = load(ROOT / 'evaluation/comparison/config.json')
        config.update(fixtures=['owner-notes'], replicates=1)
        with tempfile.TemporaryDirectory() as directory:
            plan = prepare(config, Path(directory) / 'experiment')
            self.assertEqual(plan['status'], 'not_evaluated')
            self.assertTrue(all(value is None for value in plan['metrics'].values()))
            runs = plan['runs']
            self.assertEqual(len(runs), 2)
            self.assertEqual(runs[0]['fixture_sha256'], runs[1]['fixture_sha256'])
            self.assertEqual(runs[0]['prompt_sha256'], runs[1]['prompt_sha256'])
            self.assertEqual(runs[0]['common_files_sha256'], runs[1]['common_files_sha256'])
            self.assertEqual(runs[0]['budget'], runs[1]['budget'])
            for run in runs:
                skills = Path(run['workspace']) / '.agents/skills'
                self.assertEqual(skills.exists(), run['condition'] == 'with_skills')

    def test_budget_and_model_must_be_explicit(self):
        config = load(ROOT / 'evaluation/comparison/config.json')
        for key, value in [('model', ''), ('replicates', 0), ('budget', {'wall_seconds': 0, 'observed_command_starts': 40})]:
            invalid = copy.deepcopy(config); invalid[key] = value
            with self.assertRaises(ValueError):
                validate_config(invalid)

    def test_reused_or_tampered_trial_is_rejected(self):
        config = load(ROOT / 'evaluation/comparison/config.json')
        config.update(fixtures=['owner-notes'], replicates=1)
        with tempfile.TemporaryDirectory() as directory:
            plan = prepare(config, Path(directory) / 'experiment')
            run = next(item for item in plan['runs'] if item['condition'] == 'with_skills')
            workspace = Path(run['workspace'])
            (workspace / '.agents/skills/security-privacy/SKILL.md').write_text('tampered\n')
            with self.assertRaisesRegex(ValueError, 'used or modified'):
                verify_inputs(run)
            subprocess.run(['git', 'add', '.'], cwd=workspace, check=True)
            subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false',
                            '-c', 'user.name=Evaluation test', '-c', 'user.email=test@example.invalid',
                            'commit', '-qm', 'tamper'], cwd=workspace, check=True)
            with self.assertRaisesRegex(ValueError, 'skill content drift'):
                verify_inputs(run)

    def test_ungraded_or_unknown_is_not_fake_zero_or_perfect_accuracy(self):
        result = summarize({'status':'not_adjudicated'})
        self.assertTrue(all(value is None for value in result.values()))
        # Synthetic unit data only; never written as a real experiment result.
        grade = {'status':'adjudicated','reviewer':'unit-test',
            'finding_reviews':[{'verdict':'true_positive','defect_id':'same-root'},
                               {'verdict':'true_positive','defect_id':'same-root'},
                               {'verdict':'unresolved'}],
            'fix_reviews':[{'verdict':'unverified','defect_id':'same-root'}],
            'regressions':[], 'claim_reviews':[{'verdict':'unresolved'}],
            'interventions_required':[], 'interventions_performed':[]}
        result = summarize(grade)
        self.assertEqual(result['true_defects_detected'], 1)
        self.assertEqual(result['unresolved_findings'], 1)
        self.assertIsNone(result['report_accuracy'])
        self.assertEqual(result['successful_fixes'], 0)
