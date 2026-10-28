"""Actual app HTTP-handler byte-stream probes; no network server or browser execution. Cookies/passwords are never persisted in traces."""
from pathlib import Path
import datetime, hashlib, http.client, io, json, os, sqlite3, sys, tempfile, time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'audits/owner-notes-standard' / sys.argv[1]
records = []
cookies = {}

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def req(label, method, path, actor='anonymous', data=None, headers=None, expected=None, raw=None):
    h = dict(headers or {})
    if actor in cookies:
        h['Cookie'] = cookies[actor]
    body = raw
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode()
        h.setdefault('Content-Type', 'application/json')
    payload = body or b''
    h.setdefault('Content-Length', str(len(payload)))
    wire = (method + ' ' + path + ' HTTP/1.0\r\nHost: localhost\r\n' + ''.join(k+': '+v+'\r\n' for k,v in h.items()) + '\r\n').encode() + payload
    class Connection:
        def __init__(self, wire):
            self.incoming=io.BytesIO(wire)
            self.outgoing=io.BytesIO()
        def makefile(self, *args):
            return self.incoming
        def sendall(self, data):
            self.outgoing.write(data)
    conn=Connection(wire)
    process.handler(conn, ('127.0.0.1',12345), process)
    response_wire=conn.outgoing.getvalue()
    class ResponseConnection:
        def makefile(self, *args):
            return io.BytesIO(response_wire)
    r=http.client.HTTPResponse(ResponseConnection())
    r.begin()
    result=r.read().decode()
    rh=dict(r.getheaders())
    if 'Set-Cookie' in rh:
        value = rh['Set-Cookie']
        if path == '/api/login' and r.status == 200:
            cookies[actor] = value.split(';')[0]
        rh['Set-Cookie'] = 'session=[REDACTED];' + value.split(';', 1)[1]
    try:
        value = json.loads(result)
    except ValueError:
        value = result
    safe_data = dict(data) if isinstance(data, dict) else data
    if safe_data and 'password' in safe_data:
        safe_data['password'] = '[REDACTED public demo or invalid test password]'
    records.append(dict(timestamp=stamp(), label=label, actor=actor, method=method, path=path,
                        request_body=safe_data if raw is None else raw.decode(),
                        request_headers={k:('[REDACTED]' if k.lower()=='cookie' else v) for k,v in h.items()},
                        status=r.status, response_headers=rh, response=value, expected_status=expected,
                        matches_expected=None if expected is None else r.status in expected))
    r.close()
    return r.status, value

def state(label, expected=None):
    with sqlite3.connect(data_dir/'notes.sqlite') as db:
        rows = [dict(zip(('id','owner','text'), row)) for row in db.execute('SELECT id, owner, text FROM notes ORDER BY id')]
    records.append(dict(timestamp=stamp(),label=label, independent_sqlite_state=rows,
                        expected_state=expected,matches_expected=None if expected is None else rows==expected))
    return rows

def start(ttl=1800):
    # Only replace the listening server constructor. Real Handler request parsing,
    # identity, payload validation, route methods and SQLite are all exercised.
    class CaptureServer:
        def __init__(self, addr, handler):
            self.handler=handler
            self.server_name='localhost'
            self.server_port=0
    with patch.dict(app, {'ThreadingHTTPServer':CaptureServer}):
        server=app['create_server'](0, data_dir, ttl)
    return server,0

def stop(p):
    pass

app={'__file__':str(ROOT/'owner-notes/server.py'),'__name__':'audited_app'}
exec(compile((ROOT/'owner-notes/server.py').read_bytes(), str(ROOT/'owner-notes/server.py'), 'exec'),app)

DEST.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='disposable-', dir=DEST) as td, (DEST/'server.log').open('w') as log:
    data_dir=Path(td)
    process,port=start()
    try:
        records.append(dict(timestamp=stamp(),label='runtime', python=sys.version, port=port,
                            source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'owner-notes').iterdir() if p.is_file()},
                            command='supplied .venv/bin/python audits/owner-notes-standard/probe.py '+sys.argv[1], execution='Actual BaseHTTPRequestHandler parses HTTP/1.0 bytes; only listening server constructor replaced; real SQLite and session closure. Recreate closure for restart simulation, not process/network restart.'))
        for path in ('/','/app.js','/style.css'):
            req('public asset','GET',path,expected=[200])
        for actor in ('alice','bob'):
            req('invalid login','POST','/api/login',actor,dict(username=actor,password='wrong'),expected=[401])
            req('valid login','POST','/api/login',actor,dict(username=actor,password=actor+'-demo'),expected=[200])
        for path in ('/api/notes','/api/notes/note-a','/api/notes/note-b'):
            req('anonymous read','GET',path,expected=[401])
        for note in ('note-a','note-b'):
            baseline=state('before anonymous write')
            req('anonymous write','PATCH','/api/notes/'+note,data={'text':'ANONYMOUS'},expected=[401])
            state('anonymous write must not mutate',baseline)
        cookies['forged']='session=invalid-marker'
        req('forged session','GET','/api/notes','forged',expected=[401])
        for actor,own,other in (('alice','note-a','note-b'),('bob','note-b','note-a')):
            req('owner filtered list','GET','/api/notes',actor,expected=[200])
            req('owner read','GET','/api/notes/'+own,actor,expected=[200])
            req('forbidden cross-owner read','GET','/api/notes/'+other,actor,expected=[404])
            baseline=state('before forbidden write')
            req('forbidden cross-owner write','PATCH','/api/notes/'+other,actor,{'text':'CROSS-OWNER-MARKER-'+actor},expected=[404])
            state('forbidden write must leave independent state unchanged',baseline)
            other_actor='bob' if actor=='alice' else 'alice'
            req('victim independently reads after forbidden write','GET','/api/notes/'+other,other_actor,expected=[200])
            marker='Plain quotes \' " Unicode café 雪 — <img src=x onerror="window.auditMarker=1"> ; SELECT \'audit\';'
            req('valid plain text save','PATCH','/api/notes/'+own,actor,{'text':marker},expected=[200])
            status,result=req('independent committed readback','GET','/api/notes/'+own,actor,expected=[200])
            records.append(dict(timestamp=stamp(),label='plain text roundtrip',actor=actor,expected=marker,actual=result.get('text'),matches_expected=result.get('text')==marker))
            state('committed SQLite plain text')
            for bad in ({'text':'x','owner':other_actor},{'owner':other_actor},{'text':None},{'text':'x'*1001}):
                baseline=state('before invalid payload')
                req('reject invalid note or ownership transfer','PATCH','/api/notes/'+own,actor,bad,expected=[422])
                state('rejected payload must not mutate',baseline)
            for text in ('','雪'*1000):
                req('valid length boundary','PATCH','/api/notes/'+own,actor,{'text':text},expected=[200])
                _,v=req('boundary readback','GET','/api/notes/'+own,actor,expected=[200])
                records.append(dict(timestamp=stamp(),label='length boundary exact roundtrip',length=len(text),matches_expected=v.get('text')==text))
            req('restore readable marker','PATCH','/api/notes/'+own,actor,{'text':marker},expected=[200])
            req('SQL identifier marker','GET',"/api/notes/'%20OR%201=1--",actor,expected=[404])
            req('missing resource read','GET','/api/notes/missing',actor,expected=[404])
            req('missing resource write','PATCH','/api/notes/missing',actor,{'text':'safe'},expected=[404])
        baseline=state('before feature probes')
        req('cross-site simple form content rejected','PATCH','/api/notes/note-a','alice',headers={'Origin':'https://invalid.example','Content-Type':'text/plain'},raw=b'{"text":"CROSS-SITE"}',expected=[422])
        req('cross-origin preflight unsupported','OPTIONS','/api/notes/note-a',headers={'Origin':'https://invalid.example','Access-Control-Request-Method':'PATCH','Access-Control-Request-Headers':'content-type'},expected=[501])
        req('foreign origin read has no CORS grant','GET','/api/notes','alice',headers={'Origin':'https://invalid.example'},expected=[200])
        req('same origin read','GET','/api/notes','alice',headers={'Origin':'http://127.0.0.1:'+str(port)},expected=[200])
        req('bounded oversized JSON','PATCH','/api/notes/note-a','alice',{'text':'x'*4100},expected=[422])
        req('malformed JSON','PATCH','/api/notes/note-a','alice',raw=b'{',headers={'Content-Type':'application/json'},expected=[422])
        state('feature probes must leave state unchanged',baseline)
        for path in ('/server.py','/README.md','/notes.sqlite','/../server.py','/api/no-such-route'):
            req('nonpublic path denied','GET',path,expected=[401])
        saved_session=cookies['alice']
        req('logout','POST','/api/logout','alice',{},expected=[200])
        cookies['alice']=saved_session
        for path in ('/api/notes','/api/notes/note-a'):
            req('post logout replay read','GET',path,'alice',expected=[401])
        baseline=state('before logout replay write')
        req('post logout replay write','PATCH','/api/notes/note-a','alice',{'text':'REPLAY'},expected=[401])
        state('logout replay must not mutate',baseline)
        req('new login after logout','POST','/api/login','alice',{'username':'alice','password':'alice-demo'},expected=[200])
        req('new valid session read','GET','/api/notes','alice',expected=[200])
        persisted=state('before server recreation')
        stop(process)
        process,port=start()
        for actor in ('alice','bob'):
            req('server recreation invalidates old session','GET','/api/notes',actor,expected=[401])
            req('relogin after restart','POST','/api/login',actor,{'username':actor,'password':actor+'-demo'},expected=[200])
            req('persisted note owner read','GET','/api/notes/'+('note-a' if actor=='alice' else 'note-b'),actor,expected=[200])
        state('SQLite persists across server recreation',persisted)
        stop(process)
        process,port=start(1)
        req('short expiry login','POST','/api/login','alice',{'username':'alice','password':'alice-demo'},expected=[200])
        req('short expiry initially valid','GET','/api/notes','alice',expected=[200])
        time.sleep(1.2)
        for path in ('/api/notes','/api/notes/note-a'):
            req('expired read','GET',path,'alice',expected=[401])
        baseline=state('before expired write')
        req('expired write','PATCH','/api/notes/note-a','alice',{'text':'EXPIRED'},expected=[401])
        state('expiry must not mutate',baseline)
    finally:
        stop(process)
        (DEST/'observations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
        mismatches=[r['label'] for r in records if r.get('matches_expected') is False]
        (DEST/'probe-summary.json').write_text(json.dumps(dict(timestamp=stamp(),observation_count=len(records),mismatches=mismatches,limits='Actual HTTP handlers with byte streams and independent SQLite checks; no listening socket, process restart or browser execution. Expected cross-owner denials are 404 to match existing missing-resource API.'),indent=2)+'\n')
        print(json.dumps(dict(observations=len(records),mismatches=mismatches)))
