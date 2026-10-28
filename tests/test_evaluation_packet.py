import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from evaluation.prepare_packet import prepare, ROOT


class PacketTests(unittest.TestCase):
    def test_packet_contains_baseline_and_skill_without_evaluator_answers_or_history(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'agent'
            prepare(destination)
            self.assertFalse((destination / 'evaluation').exists())
            self.assertFalse((destination / 'tests').exists())
            self.assertFalse((destination / 'fixtures').exists())
            self.assertFalse((destination / 'docs/review.md').exists())
            self.assertFalse((destination / 'examples').exists())
            manifest = json.loads((ROOT / 'evaluation/baselines/tracker-v1.manifest.json').read_text())
            for name, digest in manifest['files'].items():
                self.assertEqual(hashlib.sha256((destination / 'tracker' / name).read_bytes()).hexdigest(), digest)
            self.assertTrue((destination / '.agents/skills/functionality-data/SKILL.md').is_file())
            self.assertFalse((destination / '.git/refs/heads/main').exists())

    def test_agent_packet_cannot_be_nested_in_evaluator_repository(self):
        destination = ROOT / 'evaluation/runs/forbidden-agent-packet'
        with self.assertRaisesRegex(ValueError, 'outside'):
            prepare(destination)
        self.assertFalse(destination.exists())

    def test_existing_destination_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'keep.txt'
            marker.write_text('existing work')
            with self.assertRaises(ValueError):
                prepare(directory)
            self.assertEqual(marker.read_text(), 'existing work')

    def test_corrupt_archive_is_rejected_before_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'evaluator'
            baseline = source / 'evaluation/baselines'
            baseline.mkdir(parents=True)
            for name in ('tracker-v1.tar.gz', 'tracker-v1.manifest.json'):
                (baseline / name).write_bytes((ROOT / 'evaluation/baselines' / name).read_bytes())
            with (baseline / 'tracker-v1.tar.gz').open('ab') as stream:
                stream.write(b'tampered')
            with patch('evaluation.prepare_packet.ROOT', source):
                with self.assertRaises(ValueError):
                    prepare(root / 'agent')
            self.assertFalse((root / 'agent').exists())
