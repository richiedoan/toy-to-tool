from pathlib import Path
import datetime, json, shutil, subprocess, sys, time, urllib.request, urllib.error

ROOT = Path(__file__).resolve().parents[2]
phase = sys.argv[1]
out = ROOT / 'audits' / phase
clean = out / 'clean-start'
clean.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'dashboard', clean / 'dashboard', dirs_exist_ok=True)
result = {'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'python': sys.version, 'clean_copy': str(clean.relative_to(ROOT)), 'declared_command': 'python3 fixtures/dashboard/server.py --port 8767'}
r = subprocess.run([sys.executable, '-I', 'fixtures/dashboard/server.py', '--port', '8767'], cwd=clean, capture_output=True, text=True)
result['documented_start'] = {'exit': r.returncode, 'stderr': r.stderr}
stdout = (out / 'server.stdout').open('w'); stderr = (out / 'server.stderr').open('w')
p = subprocess.Popen([sys.executable, '-I', 'dashboard/server.py', '--port', '8767', '--fail-on', '2'], cwd=clean, stdout=stdout, stderr=stderr)
def request(path):
    try:
        response = urllib.request.urlopen('http://127.0.0.1:8767' + path, timeout=3)
    except urllib.error.HTTPError as e:
        response = e
    with response:
        return {'path': path, 'status': response.status, 'headers': dict(response.headers), 'body': response.read().decode()}
try:
    for _ in range(30):
        try:
            first = request('/'); break
        except OSError: time.sleep(.1)
    else: raise RuntimeError('Fallback startup unavailable')
    result['fallback_command'] = 'python -I dashboard/server.py --port 8767 --fail-on 2'
    result['requests'] = [first] + [request(path) for path in ['/app.js','/style.css','/api/metrics','/api/metrics','/api/metrics','/api/metrics?unavailable=1','/api/metrics','/missing']]
except Exception as error:
    result['runtime_limitation'] = str(error) + '; inspect server.stderr. A sandbox bind denial is not an application failure.'
finally:
    p.terminate(); p.wait(timeout=5); stdout.close(); stderr.close()
result['stderr_raw'] = (out/'server.stderr').read_text()
(out/'operations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'phase':phase,'documented_exit':result['documented_start']['exit'],'runtime_limitation':result.get('runtime_limitation')}))
