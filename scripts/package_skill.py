"""Export a self-contained audit skill from canonical repository resources."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('toy-to-tool-audit', 'functionality-data', 'ux-visual-quality', 'accessibility',
          'security-privacy', 'performance-resilience', 'deployment-operations')
ENGINE_FILES = ('criteria/v1.json', 'schemas/catalog.schema.json', 'schemas/profile.schema.json',
                'schemas/report.schema.json', 'scripts/audit.py', 'requirements.txt',
                'docs/method.md', 'docs/missing-access.md', 'docs/report-template.md')


def package(name, destination):
    if name not in SKILLS:
        raise ValueError('Unknown skill')
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Destination must not exist; no installed work is overwritten')
    if ROOT == destination or ROOT in destination.parents:
        raise ValueError('Export outside the source repository to avoid recursive/self copies')
    source = ROOT / '.agents/skills' / name
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '.venv'))
    entry = destination / 'SKILL.md'
    entry.write_text(entry.read_text().replace('../../../', 'references/engine/'))
    for filename in ENGINE_FILES:
        target = destination / 'references/engine' / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / filename, target)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', choices=SKILLS)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(package(args.name, args.destination))
