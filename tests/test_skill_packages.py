from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.audit import ROOT, load, template, validate_catalog, validate_report
from scripts.package_skill import package, SKILLS


class SkillPackageTests(unittest.TestCase):
    def test_isolated_package_has_canonical_engine_and_no_evaluator_material(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'security-privacy'
            package('security-privacy', destination)
            engine = destination / 'references/engine'
            self.assertEqual(load(engine / 'criteria/v1.json'), load(ROOT / 'criteria/v1.json'))
            self.assertFalse((destination / 'evaluation').exists())
            result = subprocess.run([str(ROOT / '.venv/bin/python'), str(engine / 'scripts/audit.py'), 'validate'],
                                    cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('../../../', (destination / 'SKILL.md').read_text())
            with self.assertRaises(ValueError):
                package('security-privacy', destination)

    def test_every_skill_copies_without_external_markdown_dependencies(self):
        import re
        with tempfile.TemporaryDirectory() as directory:
            for name in SKILLS:
                destination = package(name, Path(directory) / name)
                for document in [destination / 'SKILL.md']:
                    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
                        if '://' not in link and not link.startswith('#'):
                            self.assertTrue((document.parent / link).exists(), (name, link))

    def test_read_only_installation_can_validate_target_workspace_artifacts(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            installed = package('security-privacy', base / 'installed')
            engine = installed / 'references/engine'
            target = base / 'app'
            target.mkdir()
            (target / 'attempt.md').write_text('Unexecuted credentials-dependent check.')
            catalog = load(engine / 'criteria/v1.json')
            report = template(catalog, load(ROOT / 'examples/profile.json'), 'Essential', groups=['S'])
            report['evidence'] = [{'id': 'E-gap', 'location': 'attempt.md', 'description': 'Missing test identity',
                'environment': 'isolated app workspace', 'captured_at': '2026-10-28T00:00:00Z',
                'kind': 'observation', 'synthetic': False}]
            report['findings'][0]['evidence_ids'] = ['E-gap']
            (target / 'report.json').write_text(json.dumps(report))
            entries = list(installed.rglob('*'))
            try:
                for item in entries:
                    item.chmod(0o555 if item.is_dir() else 0o444)
                installed.chmod(0o555)
                result = subprocess.run([str(ROOT / '.venv/bin/python'), str(engine / 'scripts/audit.py'),
                    'validate', '--report', str(target / 'report.json'), '--evidence-root', str(target)],
                    cwd=target, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            finally:
                installed.chmod(0o755)
                for item in entries:
                    item.chmod(0o755 if item.is_dir() else 0o644)

    def test_evidence_root_supports_target_workspace_without_path_escape(self):
        catalog = validate_catalog(load(ROOT / 'criteria/v1.json'))
        report = template(catalog, load(ROOT / 'examples/profile.json'), 'Essential', groups=['F'])
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / 'workspace'
            workspace.mkdir()
            (Path(directory) / 'outside.md').write_text('Existing artifact outside authorized evidence root.')
            (workspace / 'attempt.md').write_text('No runtime available; no pass claimed.')
            report['evidence'] = [{'id': 'E-gap', 'location': 'attempt.md', 'description': 'Runtime gap',
                'environment': 'test workspace', 'captured_at': '2026-10-28T00:00:00Z',
                'kind': 'observation', 'synthetic': False}]
            report['findings'][0]['evidence_ids'] = ['E-gap']
            validate_report(report, catalog, evidence_root=workspace)
            with self.assertRaises(ValueError):
                validate_report(report, catalog)
            report['evidence'][0]['location'] = '../outside.md'
            with self.assertRaises(ValueError):
                validate_report(report, catalog, evidence_root=workspace)
            (workspace / 'escape.md').symlink_to(Path(directory) / 'outside.md')
            report['evidence'][0]['location'] = 'escape.md'
            with self.assertRaises(ValueError):
                validate_report(report, catalog, evidence_root=workspace)
