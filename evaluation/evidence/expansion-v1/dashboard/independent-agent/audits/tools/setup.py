from pathlib import Path
import datetime, hashlib, importlib.metadata as metadata, json, platform, subprocess

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'audits'
ENGINE = ROOT / '.agents/skills/ux-visual-quality/references/engine'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / 'dashboard').glob('*')) if p.is_file()}

if __name__ == '__main__':
    write(AUDIT / 'context.json', {
        'captured_at': NOW, 'root': str(ROOT), 'revision': 'Unborn Git repository; use retained SHA-256 source manifests.',
        'runtime': {'python': platform.python_version(), 'platform': platform.platform(), 'machine': platform.machine(),
                    'node': subprocess.check_output(['node', '--version'], text=True).strip()},
        'dependencies': {n: metadata.version(n) for n in ['attrs', 'jsonschema', 'jsonschema-specifications', 'referencing', 'rpds-py', 'typing_extensions']},
        'browser_probe': {'command': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --remote-debugging-port=9222 --user-data-dir=<workspace>/audits/browser-profile --no-first-run --no-default-browser-check about:blank', 'exit_code': 134, 'output': 'No output; exited before a debugging endpoint became available.'},
        'tool_probe': 'No browser MCP tool. Workspace Node playwright, puppeteer and @playwright/test unavailable. Python playwright, websocket, websockets and selenium unavailable. No browser or dependencies installed.',
        'limits': ['No screenshots, rendered geometry, accessibility tree, assistive technology, real keyboard, text zoom or Chrome filter timings collected.', 'No field CWV, participant research, load or production checks. Node handler timing is not the README Chrome budget.'],
        'tasks': ['Read four metrics at 320, 390, 768 and 1440 CSS pixels.', 'Filter titles without changing values or requesting data.', 'Refresh, explain failure, retain last success, retry.'],
        'scope': 'Standard U/A/P/O; scoped edits to dashboard only. Preserve README, desktop design, labels, metrics, native controls, existing behavior and simple architecture.'})
    write(AUDIT / 'before/source-hashes.json', hashes())
    names = json.loads((ENGINE / 'schemas/profile.schema.json').read_text())['properties']['features']['required']
    present = {'ui': 'Native dashboard screen.', 'pointer_ui': 'Search and refresh native controls.', 'operations': 'Read and refresh metrics.', 'inputs': 'Disposable title filter.', 'network': 'GET /api/metrics.', 'resource_lifecycle': 'Document listeners, replaced nodes and transient fetches.', 'operated_service': 'Local operator starts service and receives stderr events.'}
    profile = {'name': 'Local metrics dashboard', 'features': {n: n in present for n in names}, 'rationale': {n: present.get(n, 'README and source establish absence: deterministic read-only stateless localhost fixture; no ' + n.replace('_', ' ') + '.') for n in names}}
    profile['rationale']['persistent_data'] = 'No durable retention or restore. Last success is document memory, checked in U02/P02.'
    profile['rationale']['user_changes'] = 'No data mutation, destructive, cancel or back workflow. Disposable filter correction is checked in U02.'
    write(AUDIT / 'profile.json', profile)
    for command, name in [('select', 'selection.json'), ('template', 'template.json')]:
        result = subprocess.run([str(ROOT / '.venv/bin/python'), str(ENGINE / 'scripts/audit.py'), command, '--profile', str(AUDIT / 'profile.json'), '--level', 'Standard', '--group', 'U', '--group', 'A', '--group', 'P', '--group', 'O', '--evidence-root', str(ROOT)], capture_output=True, text=True)
        (AUDIT / name).write_text(result.stdout)
        print(command, result.returncode, result.stderr)
