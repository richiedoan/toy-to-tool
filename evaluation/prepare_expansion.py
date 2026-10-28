"""Export one neutral fixture plus independently installable audit skills."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.package_skill import package

FIXTURES = {'owner-notes': ('security-privacy',),
            'dashboard': ('ux-visual-quality', 'accessibility', 'performance-resilience', 'deployment-operations')}


def prepare(name, destination, bootstrap=False):
    if name not in FIXTURES:
        raise ValueError('Unknown fixture')
    destination = Path(destination).resolve()
    if destination == ROOT or ROOT in destination.parents or destination.exists():
        raise ValueError('Use a new destination outside the evaluator repository')
    archive = ROOT / 'evaluation/baselines' / (name + ('-v2.tar.gz' if name == 'owner-notes' else '-v1.tar.gz'))
    manifest = json.loads(archive.with_suffix('').with_suffix('.manifest.json').read_text())
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Archive checksum mismatch')
    allowed = {'README.md', 'index.html', 'app.js', 'style.css', 'server.py'}
    if set(manifest['files']) != allowed:
        raise ValueError('Unexpected baseline files')
    with tarfile.open(archive) as source:
        members = source.getmembers()
        if {m.name for m in members} != {name + '/' + f for f in allowed} or any(not m.isfile() for m in members):
            raise ValueError('Unexpected archive members')
        for member in members:
            if hashlib.sha256(source.extractfile(member).read()).hexdigest() != manifest['files'][Path(member.name).name]:
                raise ValueError('File checksum mismatch')
        destination.mkdir(parents=True)
        (destination / "fixtures").mkdir()
        source.extractall(destination / "fixtures")
    for skill in FIXTURES[name]:
        package(skill, destination / '.agents/skills' / skill)
    (destination / 'AGENTS.md').write_text(
        '# Fixture review workspace\n\n'
        f'Target: fixtures/{name}/. Use the supplied skills: {", ".join(FIXTURES[name])}. '
        'Read the target README for product requirements and preservation boundaries. '
        'Run Inspect -> Improve -> Recheck at Standard. Fix scoped, demonstrated defects within the target app only; '
        'do not change the README, product contract, unrelated code or approved desktop design. '
        'Retain before/after reports, raw observations and patches under audits/. '
        'Use an available Python interpreter with the declared engine dependencies, and an explicit target evidence root. '
        'Do not read outside this workspace or seek evaluator answers. Use disposable data; save artifacts in English.\n')
    (destination / '.gitignore').write_text('.venv/\n__pycache__/\n/audits/\n/data/\n')
    subprocess.run(['git', 'init', '-q', str(destination)], check=True)
    if bootstrap:
        subprocess.run([sys.executable, '-m', 'venv', str(destination / '.venv')], check=True)
        requirements = destination / '.agents/skills' / FIXTURES[name][0] / 'references/engine/requirements.txt'
        subprocess.run([str(destination / '.venv/bin/python'), '-m', 'pip', 'install', '--disable-pip-version-check', '-q', '-r', str(requirements)], check=True)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', choices=FIXTURES)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()
    print(prepare(args.name, args.destination, args.bootstrap))
