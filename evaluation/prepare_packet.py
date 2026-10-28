"""Build a neutral, answer-free workspace from the immutable tracker baseline."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination, bootstrap=False):
    destination = Path(destination).resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError('Agent packets must be outside the evaluator repository')
    if destination.exists():
        raise ValueError('Destination must not exist; existing work is never overwritten')
    archive = ROOT / 'evaluation/baselines/tracker-v1.tar.gz'
    manifest = json.loads(archive.with_name('tracker-v1.manifest.json').read_text())
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Baseline archive checksum mismatch')
    if set(manifest['files']) != {'index.html', 'app.js', 'style.css', 'README.md'}:
        raise ValueError('Baseline manifest must contain only the neutral tracker files')
    with tarfile.open(archive) as source:
        members = source.getmembers()
        expected = {'tracker/' + name for name in manifest['files']}
        if {m.name for m in members} != expected or any(not m.isfile() for m in members):
            raise ValueError('Baseline has unexpected members or nonregular files')
        for member in members:
            name = Path(member.name).name
            content = source.extractfile(member).read()
            if hashlib.sha256(content).hexdigest() != manifest['files'][name]:
                raise ValueError('Baseline file checksum mismatch')
        destination.mkdir(parents=True)
        source.extractall(destination)
    # Explicit files only: no evaluator docs, hidden tests, run logs, or Git history.
    files = ['criteria/v1.json', 'schemas/catalog.schema.json', 'schemas/profile.schema.json',
             'schemas/report.schema.json', 'scripts/audit.py', 'docs/method.md', 'docs/missing-access.md', 'docs/report-template.md', 'requirements.txt',
             '.agents/skills/functionality-data/SKILL.md',
             '.agents/skills/toy-to-tool-audit/references/missing-access.md']
    for name in files:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    (destination / 'AGENTS.md').write_text(
        '# Local evaluation workspace\n\n'
        'Use .agents/skills/functionality-data/SKILL.md for Functionality & Data work. '
        'The target app is tracker/. Read its README for the agreed behavior. '
        'Inspect, improve and recheck at Standard level. Target-code fixes are authorized within tracker/. '
        'Keep source architecture and product scope. Save baseline and final reports/evidence under audits/. '
        'Do not read outside this workspace or search for evaluator materials. '
        'Use only disposable local test data. Save artifacts in English. '
        'Python dependencies are declared in requirements.txt. Chrome is installed locally.\n')
    (destination / '.gitignore').write_text('.venv/\nnode_modules/\n__pycache__/\naudits/\n')
    subprocess.run(['git', 'init', '-q', str(destination)], check=True)
    if bootstrap:
        subprocess.run([sys.executable, '-m', 'venv', str(destination / '.venv')], check=True)
        python = str(destination / '.venv/bin/python')
        subprocess.run([python, '-m', 'pip', 'install', '--disable-pip-version-check',
                        '-r', str(destination / 'requirements.txt')], check=True)
        subprocess.run([python, str(destination / 'scripts/audit.py'), 'validate'],
                       cwd=destination, check=True)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--bootstrap', action='store_true', help='Install engine dependencies and validate before handing off to an agent.')
    args = parser.parse_args()
    print(prepare(args.destination, bootstrap=args.bootstrap))
