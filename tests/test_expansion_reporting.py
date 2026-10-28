import unittest
from evaluation.expansion_reports import assess


class ExpansionReportingTests(unittest.TestCase):
    def test_local_task_success_does_not_pass_field_cwv(self):
        self.assertEqual(assess('P03', [{'status': 'pass'}]), 'unknown')
        self.assertEqual(assess('P03', [{'status': 'fail', 'error': 'AssertionError: local budget exceeded'}]), 'fail')

    def test_coverage_gaps_and_infrastructure_do_not_disappear(self):
        self.assertEqual(assess('A02', [{'status': 'pass'}]), 'unknown')
        self.assertEqual(assess('U03', [{'status': 'pass'}]), 'pass')
        self.assertEqual(assess('U03', [{'status': 'unknown', 'error': 'Browser unavailable'}]), 'unknown')
