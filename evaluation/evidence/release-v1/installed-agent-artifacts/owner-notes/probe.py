"""Stdlib HTTP regression: launches only this fixture on port 0 with disposable SQLite."""
import datetime, hashlib, http.client, json, pathlib, select, sqlite3, subprocess, sys, tempfile, time, io, importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[2]; OUT=ROOT/'audits/owner-notes'/sys.argv[1]; APP=ROOT/'fixtures/owner-notes'; rows=[]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
class MemorySocket:
 def __init__(self, data): self.input=io.BytesIO(data); self.output=bytearray()
 def makefile(self, *args, **kwargs): return self.input
 def sendall(self, data): self.output.extend(data)
class ResponseSocket:
 def __init__(self, data): self.data=data
 def makefile(self, *args, **kwargs): return io.BytesIO(self.data)
def launch(data, seconds=60):
 # Invoke original factory with only socket-creating class replaced by capture.
 # Real Handler, SQLite, session dictionary, payload parser and dispatch remain intact.
 spec=importlib.util.spec_from_file_location('owner_notes_under_audit', APP/'server.py')
 module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
 module.ThreadingHTTPServer=lambda address, handler: handler
 handler=module.create_server(0,data,seconds)
 launches.append({'mode':'real BaseHTTPRequestHandler over in-memory request/response streams; no listening socket','factory':'create_server(0, <disposable-data-dir>, '+str(seconds)+')','timestamp':now()})
 return handler,0
def stop(p):
 logs.append({'stderr':'No network server or log_message output; handler requests complete synchronously.','timestamp':now()})
def req(label,actor,method,path,expected,body=None,cookie=None,headers=None,raw=None):
 h=dict(headers or {});
 if cookie: h['Cookie']=cookie
 if raw is None and body is not None: raw=json.dumps(body); h.setdefault('Content-Type','application/json')
 if raw is None: wire_body=b''
 else: wire_body=raw.encode() if isinstance(raw,str) else raw
 if raw is not None: h['Content-Length']=str(len(wire_body))
 h['Host']='127.0.0.1'
 wire=(method+' '+path+' HTTP/1.1\r\n'+''.join(k+': '+v+'\r\n' for k,v in h.items())+'\r\n').encode()+wire_body
 sock=MemorySocket(wire)
 p(sock,('127.0.0.1',1),object())
 response=http.client.HTTPResponse(ResponseSocket(bytes(sock.output))); response.begin()
 data=response.read(); rh=dict(response.getheaders())
 try: val=json.loads(data)
 except (ValueError,UnicodeDecodeError): val=data.decode(errors='replace')
 safe={k: ('session=<redacted>; '+v.split('; ',1)[1] if k.lower()=='set-cookie' and '; ' in v else v) for k,v in rh.items()}
 logged_body=body
 if path=='/api/login' and isinstance(body,dict): logged_body={**body,'password':'<public demo value omitted>'}
 rows.append({'id':label,'timestamp':now(),'actor':actor,'method':method,'path':path,'input':logged_body if raw is None else (logged_body if body is not None else raw),'headers':{k:v for k,v in h.items() if k.lower()!='cookie'},'session': 'present (redacted)' if cookie else 'absent','expected_status':expected,'actual_status':response.status,'status_matches':response.status in expected,'response':val,'response_headers':safe})
 return response.status,val,rh
checks=[]
def check(label,expected,actual): checks.append({'id':label,'expected':expected,'actual':actual,'matches':expected==actual,'timestamp':now()})
def state():
 with sqlite3.connect(data/'notes.sqlite') as db: return [list(r) for r in db.execute('SELECT id,owner,text FROM notes ORDER BY id')]
def login(name,label=None):
 _,_,h=req(label or 'login-'+name,name,'POST','/api/login',[200],{'username':name,'password':name+'-demo'})
 return h.get('Set-Cookie','').split(';',1)[0]
launches=[]; logs=[]
with tempfile.TemporaryDirectory(prefix='owner-notes-audit-') as tmp:
 data=pathlib.Path(tmp); p,port=launch(data)
 try:
  for path in ['/','/app.js','/style.css']:
   _,v,_=req('public-'+path,'anonymous','GET',path,[200]); check('static-matches-'+path,(APP/({'/':'index.html','/app.js':'app.js','/style.css':'style.css'}[path])).read_text(),v)
  req('invalid-login','anonymous','POST','/api/login',[401],{'username':'alice','password':'invalid'})
  req('unknown-login','anonymous','POST','/api/login',[401],{'username':'nobody','password':'invalid'})
  cookies={n:login(n) for n in ['alice','bob']}
  for actor,cookie in [*cookies.items(),('anonymous',None)]:
   _,v,_=req(actor+'-list',actor,'GET','/api/notes',[401] if cookie is None else [200],cookie=cookie)
   if cookie: check(actor+'-list-owners',[actor],[r['owner'] for r in v])
   for owner,note in [('alice','note-a'),('bob','note-b')]:
    allowed=actor==owner; expect=[401] if cookie is None else ([200] if allowed else [404])
    req(actor+'-read-'+note,actor,'GET','/api/notes/'+note,expect,cookie=cookie)
    before=state(); marker='owned:'+actor if allowed else 'forbidden:'+actor
    req(actor+'-write-'+note,actor,'PATCH','/api/notes/'+note,expect,{'text':marker},cookie)
    after=state(); target=0 if owner=='alice' else 1
    check(actor+'-state-'+note,[[r[0],r[1], marker if i==target and allowed else r[2]] for i,r in enumerate(before)],after)
    if allowed:
     _,v,_=req(actor+'-readback-'+note,actor,'GET','/api/notes/'+note,[200],cookie=cookie); check(actor+'-readback-text',marker,v.get('text'))
  marker="<audit-tag> & ' \" ; SELECT * FROM notes; -- Unicode café 🐍"
  for text,label in [(marker,'inert-marker'),('x'*1000,'limit-1000'),('','empty-text')]:
   req(label,'alice','PATCH','/api/notes/note-a',[200],{'text':text},cookies['alice']); check(label+'-db',text,state()[0][2])
   _,v,_=req(label+'-read','alice','GET','/api/notes/note-a',[200],cookie=cookies['alice']); check(label+'-roundtrip',text,v.get('text'))
  for body,label in [({'text':'x'*1001},'over-limit'),({'text':None},'null'),({'text':3},'number'),({'text':'safe','owner':'bob'},'owner-transfer'),({},'missing-text')]:
   before=state(); req(label,'alice','PATCH','/api/notes/note-a',[422],body,cookies['alice']); check(label+'-unchanged',before,state())
  for note in ['missing',"note-a' OR '1'='1"]:
   req('id-query-read-'+note,'alice','GET','/api/notes/'+note.replace(' ','%20'),[404],cookie=cookies['alice'])
   before=state(); req('id-query-write-'+note,'alice','PATCH','/api/notes/'+note.replace(' ','%20'),[404],{'text':'inert'},cookies['alice']); check('id-query-unchanged-'+note,before,state())
  for raw,ct,label in [('text=csrf','application/x-www-form-urlencoded','csrf-form'),('{"text":"cross-site-marker"}','text/plain','csrf-text'),('{','application/json','malformed-json'),('x'*4097,'application/json','oversized-json')]:
   before=state(); req(label,'alice (explicit cookie; not browser)','PATCH','/api/notes/note-a',[422],cookie=cookies['alice'],headers={'Content-Type':ct,'Origin':'https://untrusted.invalid'},raw=raw); check(label+'-unchanged',before,state())
  for origin in ['http://127.0.0.1:'+str(port),'https://untrusted.invalid']:
   _,_,h=req('origin-read-'+origin,'anonymous','GET','/api/notes',[401],headers={'Origin':origin}); check('no-cors-grant-'+origin,None,h.get('Access-Control-Allow-Origin'))
   _,_,h=req('preflight-'+origin,'anonymous','OPTIONS','/api/notes/note-a',[501],headers={'Origin':origin,'Access-Control-Request-Method':'PATCH'}); check('no-preflight-grant-'+origin,None,h.get('Access-Control-Allow-Origin'))
  for path in ['/server.py','/README.md','/../server.py','/.git/config','/notes.sqlite']:
   req('private-path-'+path,'anonymous','GET',path,[401])
  req('logout','alice','POST','/api/logout',[200],{},cookies['alice'])
  for path in ['/api/notes','/api/notes/note-a']: req('logout-replay-read-'+path,'alice revoked','GET',path,[401],cookie=cookies['alice'])
  before=state(); req('logout-replay-write','alice revoked','PATCH','/api/notes/note-a',[401],{'text':'revoked'},cookies['alice']); check('logout-unchanged',before,state())
  cookies['alice']=login('alice','new-login-after-logout'); req('new-session-read','alice','GET','/api/notes/note-a',[200],cookie=cookies['alice'])
  saved=state()
 finally: stop(p)
 p,port=launch(data,1)
 try:
  for actor,cookie in cookies.items(): req('restart-replay-'+actor,actor+' prior process','GET','/api/notes',[401],cookie=cookie)
  check('restart-database-preserved',saved,state())
  expiry=login('alice','short-session-login'); req('pre-expiry','alice','GET','/api/notes',[200],cookie=expiry)
  time.sleep(1.2)
  req('post-expiry-read','alice expired','GET','/api/notes/note-a',[401],cookie=expiry)
  before=state(); req('post-expiry-write','alice expired','PATCH','/api/notes/note-a',[401],{'text':'expired'},expiry); check('expiry-unchanged',before,state())
 finally: stop(p)
result={'phase':sys.argv[1],'captured_at':now(),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in APP.iterdir() if p.is_file()},'launches':launches,'requests':rows,'independent_checks':checks,'server_logs':logs,'summary':{'requests':len(rows),'unexpected_statuses':[r['id'] for r in rows if not r['status_matches']],'state_or_value_failures':[r['id'] for r in checks if not r['matches']]},'limits':'Socket bind denied (before/startup-failure.json). Real request handlers with in-memory HTTP wire streams and actual SQLite, not network HTTP/browser execution. No browser, TLS/deployed behavior, brute force, race/load or production privacy testing. Cookies redacted. Temp data removed. No service started.'}
(OUT/'regression.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps(result['summary']))
if sys.argv[1]=='after' and (result['summary']['unexpected_statuses'] or result['summary']['state_or_value_failures']): sys.exit(1)
