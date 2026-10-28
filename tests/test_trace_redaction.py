import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from evaluation.redact_trace import sanitize, EVALUATION_ROOT


class TraceRedactionTests(unittest.TestCase):
    def test_redaction_preserves_status_payload_and_binary_artifacts(self):
        with tempfile.TemporaryDirectory(dir=EVALUATION_ROOT / 'runs') as directory:
            trace = Path(directory) / 'fixture.trace.zip'
            record = {'status': 200, 'headers': [{'name': 'Set-Cookie', 'value': 'session=secret'}],
                      'cookies': [{'name': 'session', 'value': 'secret'}], 'body': 'fixture payload'}
            with zipfile.ZipFile(trace, 'w') as archive:
                archive.writestr('trace.trace', '{}\n')
                archive.writestr('trace.network', json.dumps(record) + '\n')
                archive.writestr('resources/image', b'pixels')
            self.assertEqual(sanitize(trace), 2)
            with zipfile.ZipFile(trace) as archive:
                actual = json.loads(archive.read('trace.network'))
                self.assertEqual(actual['headers'][0]['value'], '[REDACTED]')
                self.assertEqual(actual['cookies'][0]['value'], '[REDACTED]')
                self.assertEqual(actual['status'], 200)
                self.assertEqual(actual['body'], 'fixture payload')
                self.assertEqual(archive.read('resources/image'), b'pixels')
            self.assertEqual(sanitize(trace), 0)

    def test_refuses_unowned_or_unrecognized_archives(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                sanitize(Path(directory) / 'unowned.trace.zip')
