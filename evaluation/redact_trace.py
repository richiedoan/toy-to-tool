"""Redact session/authentication headers from evaluator-owned Playwright traces."""
import argparse
import json
import os
from pathlib import Path
import tempfile
import zipfile

EVALUATION_ROOT = Path(__file__).resolve().parent
SENSITIVE = {'cookie', 'set-cookie', 'authorization', 'proxy-authorization'}


def redact(value, cookie_context=False):
    count = 0
    if isinstance(value, dict):
        if 'value' in value and (str(value.get('name', '')).lower() in SENSITIVE or cookie_context):
            if value['value'] != '[REDACTED]':
                value['value'] = '[REDACTED]'
                count += 1
        for key, child in value.items():
            if key.lower() in SENSITIVE and isinstance(child, str):
                if child != '[REDACTED]':
                    value[key] = '[REDACTED]'
                    count += 1
            else:
                count += redact(child, cookie_context=key.lower() == 'cookies')
    elif isinstance(value, list):
        for child in value:
            count += redact(child, cookie_context=cookie_context)
    return count


def sanitize(path):
    path = Path(path)
    if path.is_symlink() or EVALUATION_ROOT not in path.resolve().parents or not path.name.endswith('.trace.zip'):
        raise ValueError('Use an evaluator-owned .trace.zip under the evaluation directory')
    entries = []
    count = 0
    with zipfile.ZipFile(path) as archive:
        if not any(info.filename.endswith('.trace') for info in archive.infolist()):
            raise ValueError('Not a Playwright trace')
        for info in archive.infolist():
            data = archive.read(info)
            if info.filename.endswith(('.trace', '.network')):
                lines = []
                for line in data.decode().splitlines():
                    record = json.loads(line)
                    count += redact(record)
                    lines.append(json.dumps(record, separators=(',', ':')))
                data = ('\n'.join(lines) + '\n').encode()
            entries.append((info, data))
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.zip', delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary, 'w') as archive:
            for info, data in entries:
                archive.writestr(info, data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    print(json.dumps({'redacted_fields': sanitize(parser.parse_args().path)}))
