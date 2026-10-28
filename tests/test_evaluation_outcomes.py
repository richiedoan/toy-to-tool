import unittest
from evaluation.make_report import outcome


class OutcomeTests(unittest.TestCase):
    def test_only_completed_assertions_can_pass(self):
        self.assertEqual(outcome([{'status': 'pass'}]), 'pass')
        self.assertEqual(outcome([]), 'unknown')
        self.assertEqual(outcome([{'status': 'skipped'}]), 'unknown')

    def test_infrastructure_error_is_unknown(self):
        self.assertEqual(outcome([{'status': 'fail', 'error': 'TimeoutError: browser unavailable'}]), 'unknown')

    def test_demonstrated_failure_is_not_hidden_by_another_unexecuted_case(self):
        self.assertEqual(outcome([{'status': 'fail', 'error': 'AssertionError: stored value differs'},
                                  {'status': 'fail', 'error': 'TimeoutError: browser unavailable'}]), 'fail')
