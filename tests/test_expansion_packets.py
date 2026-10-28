import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from evaluation.prepare_expansion import prepare, ROOT, FIXTURES


class ExpansionPacketTests(unittest.TestCase):
    def test_each_packet_contains_restorable_original_and_only_needed_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            for fixture, skills in FIXTURES.items():
                packet = prepare(fixture, Path(directory) / fixture)
                version = 2 if fixture == 'owner-notes' else 1
                manifest = json.loads((ROOT / f'evaluation/baselines/{fixture}-v{version}.manifest.json').read_text())
                for name, digest in manifest['files'].items():
                    self.assertEqual(hashlib.sha256((packet / 'fixtures' / fixture / name).read_bytes()).hexdigest(), digest)
                self.assertEqual({p.name for p in (packet / '.agents/skills').iterdir()}, set(skills))
                self.assertFalse((packet / 'evaluation').exists())
                self.assertFalse((packet / 'tests').exists())
                self.assertFalse((packet / 'docs/review.md').exists())
                with self.assertRaises(ValueError):
                    prepare(fixture, packet)

    def test_packet_must_be_outside_evaluator_repository(self):
        with self.assertRaises(ValueError):
            prepare('dashboard', ROOT / 'evaluation/runs/forbidden')
