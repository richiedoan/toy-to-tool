import json
from pathlib import Path
import tempfile
import unittest

from scripts.package_skill import ROOT, SKILLS, package
from scripts.build_release import check_release


class ReleaseTests(unittest.TestCase):
    def test_repository_skills_are_already_installable_without_export_step(self):
        check_release()
        for name in SKILLS:
            root = ROOT / '.agents/skills' / name
            self.assertTrue((root / 'references/engine/scripts/audit.py').is_file())
            self.assertEqual(json.loads((root / 'references/engine/criteria/v1.json').read_text()),
                             json.loads((ROOT / 'criteria/v1.json').read_text()))
            self.assertTrue((root / 'LICENSE').is_file())

    def test_export_is_generated_from_authoring_not_a_stale_bundled_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            target = package('security-privacy', Path(directory) / 'security-privacy')
            self.assertEqual((target / 'SKILL.md').read_bytes(),
                             (ROOT / '.agents/skills/security-privacy/SKILL.md').read_bytes())
