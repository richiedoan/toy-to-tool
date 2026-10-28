import contextlib, datetime, importlib.util, io, json, sys
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[2]
phase = sys.argv[1]
spec = importlib.util.spec_from_file_location('dashboard_server', root/'dashboard/server.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with patch.object(module, 'ThreadingHTTPServer', side_effect=lambda addr, handler: (addr, handler)):
    address, handler = module.create_server(8767, fail_on=2)
events = io.StringIO()
rows = []
with contextlib.redirect_stderr(events):
    for path in ['/', '/app.js', '/style.css', '/api/metrics', '/api/metrics', '/api/metrics', '/api/metrics?unavailable=1', '/api/metrics', '/missing']:
        h = handler.__new__(handler)
        h.requestline = 'GET '+path+' HTTP/1.1'
        h.request_version = 'HTTP/1.1'
        h.command = 'GET'; h.path = path
        h.wfile = io.BytesIO()
        h.do_GET()
        raw = h.wfile.getvalue().decode()
        headers, body = raw.split('\r\n\r\n', 1)
        rows.append({'path':path, 'response_headers':headers,'body':body})
diagnostics = [json.loads(line) for line in events.getvalue().splitlines()]
assert len(diagnostics) == 2
assert all(set(e) == {'event','request_id','status'} and e['status'] == 503 and any(e['request_id'] in r['response_headers'] for r in rows) for e in diagnostics)
assert json.loads(rows[3]['body']) == json.loads(rows[5]['body']) == json.loads(rows[7]['body']) == module.METRICS
output = {'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope':'Actual server do_GET handlers with in-memory output and intercepted server construction. No socket, actual startup, network or operator detection path verified.', 'bind_address': address, 'requests':rows,'diagnostics':diagnostics,'checks':'Two correlated redacted 503 events; fail-on-2 once; controlled unavailable; success before/after; assets and 404; deterministic metric equality.'}
(root/'audits'/phase/'server-handlers.json').write_text(json.dumps(output,indent=2)+'\n')
print(phase, 'server handler checks passed')
