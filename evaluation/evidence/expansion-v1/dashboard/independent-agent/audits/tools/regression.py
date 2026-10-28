from pathlib import Path
import datetime, difflib, hashlib, json

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / 'audits'
before = A / 'before/source'
patches = []
changed = []
for old in sorted(before.iterdir()):
    current = ROOT/'dashboard'/old.name
    if old.read_bytes() != current.read_bytes():
        changed.append(old.name)
        patches.extend(difflib.unified_diff(old.read_text().splitlines(True),current.read_text().splitlines(True),fromfile='a/dashboard/'+old.name,tofile='b/dashboard/'+old.name))
(A/'dashboard.patch').write_text(''.join(patches))
assert changed == ['app.js','style.css']
assert all((before/n).read_bytes() == (ROOT/'dashboard'/n).read_bytes() for n in ['README.md','index.html','server.py'])
original_css = (before/'style.css').read_text()
css = (ROOT/'dashboard/style.css').read_text()
normalized = css.replace(' max-width: 100%;','').replace(' flex-wrap: wrap;','').split('@media')[0]
assert normalized == original_css
b = json.loads((A/'before/handlers.json').read_text())
a = json.loads((A/'after/handlers.json').read_text())
assert a['initial'] == b['initial']
assert a['filters'] == b['filters']
assert a['filterRequests'] == b['filterRequests'] == 0
expected = a['initial']['rows']
for case in a['faults']:
    assert case['rows'] == expected and not case['disabled']
    assert ('Try Refresh data.' in case['status']) if case['fault'] != 'retry' else case['status'] == '4 metrics shown.'
assert a['loading']['status'] == 'Loading…' and a['loading']['disabled']
assert a['delayedSuccess'] == a['initial']
assert [c['nodes'] for c in a['cycles']] == [4,4,4]
assert all(c['listeners']['#filter']['input'] == c['listeners']['#refresh']['click'] == 1 for c in a['cycles'])
fresh = a['initialFailureComparison']
assert fresh[0]['failed']['status'] == ''
assert 'Try Refresh data.' in fresh[1]['failed']['status']
assert 'last successful' not in fresh[1]['failed']['status']
assert fresh[1]['failed']['rows'] == 0 and not fresh[1]['failed']['disabled']
assert all(f['retryRows'] == expected for f in fresh)
assert 'while (performance.now()' not in (ROOT/'dashboard/app.js').read_text()
hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'dashboard').iterdir()) if p.is_file()}
(A/'after/source-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
out = {'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed_checks':['Only app.js and style.css changed. README/index/server byte-identical.','CSS original declarations identical except added shell max-width and header wrapping; mobile grid media queries appended. At 1440px base shell remains 1100px and grid four columns; visual browser confirmation unavailable.','All four labels/values and initial success unchanged. Case-insensitive filter, no match, clear unchanged; zero filter requests.','503 and rejected fetch retain exact successful rows, explain failure, enable refresh; retry restores success.','Fresh initial 503 explains retry without claiming previous data; retry loads four exact metrics.','Delayed success shows Loading and disabled refresh, then re-enables and renders.','15 cycles preserve four nodes and exactly one input/click listener in adapter; browser teardown/resource profiling unexecuted.','Busy wait removed; Node diagnostics are not Chrome or field CWV.'],'limitations':['No browser render, screenshots, visual/keyboard/AT/contrast/zoom/hit-region verification.','No live network service: sandbox denied socket binding.','No hung request or bounded timeout verification; source has no timeout.','No Chrome input-to-frame measurement or p95; no field CWV.'],'patch':'audits/dashboard.patch','handler_observations':'audits/after/handlers.json','http_handler_observations':'audits/after/server-handlers.json','baseline':'audits/before/report.json'}
(A/'after/regression.json').write_text(json.dumps(out,indent=2)+'\n')
print('Source preservation and handler regression checks passed:',len(out['passed_checks']))
