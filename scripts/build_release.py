"""Generate or check the checked-in, skills-CLI-ready distribution."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.package_skill import package, SKILLS


def expected_files():
    result = {}
    with tempfile.TemporaryDirectory(prefix='toy-skills-build-') as directory:
        for name in SKILLS:
            skill = package(name, Path(directory) / name)
            for path in skill.rglob('*'):
                if path.is_file():
                    result[name + '/' + str(path.relative_to(skill))] = path.read_bytes()
    return result


def check_release(write=False):
    target = ROOT / '.agents/skills'
    expected = expected_files()
    extras = [str(path.relative_to(target)) for path in target.rglob('*')
              if path.is_file() and path.name != 'release-manifest.json'
              and '__pycache__' not in path.parts and str(path.relative_to(target)) not in expected]
    if extras:
        raise ValueError('Unexpected distribution files; review before removing: ' + ', '.join(extras))
    changed = [name for name, data in expected.items()
               if not (target / name).is_file() or (target / name).read_bytes() != data]
    if changed and not write:
        raise ValueError('Distribution drift; run python3 scripts/build_release.py --write: ' + ', '.join(changed))
    if write:
        for name, data in expected.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    manifest = {'version': '1.0.0', 'skills': list(SKILLS),
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(expected.items())}}
    manifest_path = target / 'release-manifest.json'
    encoded = json.dumps(manifest, indent=2) + '\n'
    if write:
        manifest_path.write_text(encoded)
    elif not manifest_path.is_file() or manifest_path.read_text() != encoded:
        raise ValueError('Distribution manifest is missing or stale')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Refresh known generated files without deleting unknown files.')
    args = parser.parse_args()
    manifest = check_release(args.write)
    print(f'Valid distribution: {len(manifest["skills"])} self-contained skills, version {manifest["version"]}.')
