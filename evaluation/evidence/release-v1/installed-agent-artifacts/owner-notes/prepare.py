import hashlib, json, pathlib, sys, sqlite3, subprocess, datetime, importlib.metadata
root=pathlib.Path(__file__).resolve().parents[2]; out=root/'audits/owner-notes'; app=root/'fixtures/owner-notes'; engine=root/'.agents/skills/security-privacy/references/engine'
def dump(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def hashes(): return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(app.iterdir()) if p.is_file()}
for p in app.iterdir():
 if p.is_file(): (out/'before'/p.name).write_bytes(p.read_bytes())
dump(out/'before/hashes.json',hashes())
features={}; rationale={}
true={'ui':'Native login/editor controls.', 'pointer_ui':'Buttons and text fields.', 'operations':'Login, read, update and logout routes.', 'inputs':'JSON credentials and plain text notes.', 'persistent_data':'SQLite survives restart.', 'shared_writes':'Threaded server can receive simultaneous writes.', 'user_changes':'Users edit notes.', 'protected_resources':'Owner-only notes.', 'untrusted_execution':'Input reaches SQL and browser text sinks.', 'authentication':'Cookie sessions for two demo users.', 'csrf_surface':'Cookie-authenticated PATCH and POST routes.', 'public_endpoints':'Static assets, login and logout.', 'abuse_surface':'Public login and bounded JSON request parsing.', 'network':'Loopback HTTP.', 'resource_lifecycle':'In-memory sessions and SQLite connections.'}
false={'cors_surface':'No intended cross-origin API or CORS grants; still probe denied origins.', 'uploads':'No upload routes or file input.', 'load_requirements':'No throughput or concurrent load budget in README.', 'realtime':'No push transport.', 'offline_sync':'No offline synchronization.', 'background_sync':'No background synchronization.', 'deployed':'README defines localhost disposable fixture.', 'important_data':'Only disposable demo notes per README.', 'operated_service':'Local fixture without production operations contract.'}
for k in json.load(open(engine/'schemas/profile.schema.json'))['properties']['features']['properties']:
 features[k]=k in true; rationale[k]=(true|false)[k]
dump(out/'profile.json',{'name':'Owner notes localhost fixture','features':features,'rationale':rationale})
rev=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=root,capture_output=True,text=True)
dump(out/'environment.json',{'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'sqlite':sqlite3.sqlite_version,'jsonschema':importlib.metadata.version('jsonschema'),'revision':rev.stdout.strip() if rev.returncode==0 else 'No committed HEAD; file SHA-256 manifests identify source','revision_command_exit':rev.returncode,'browser_tool_discovery':'No Chrome, browser or Playwright tool exposed by available tool metadata. No documented project browser test setup. Browser execution unavailable; no dependency installed.','scope':'User: Standard S group; scoped app-only fixes. README/UI/API/working behavior preserved. Only installed skill resources, workspace and project Python. Outside RTK reference not read because user prohibits outside workspace reads.'})
(out/'context.md').write_text('''# Requirement, scope and source inspection (S01–S05)

Requirement source: fixtures/owner-notes/README.md (immutable copy before/README.md). User authorizes proportionate app-only fixes at Standard, preserving README, UI, API and working behavior.

Three priority tasks: A/B sign in and list/read only their own note; edit own text and independently read committed SQLite text; sign out and replay old session with access denied. SQLite persists restart; sessions do not. Note ownership cannot transfer. Text <=1000 characters, including quotes and Unicode.

Classification: source and static HTML/JS/CSS are public fixture implementation; alice/bob passwords are deliberately public test identities, not leaked production credentials. In-memory session tokens are private, never saved here. Note text is owner-only, even though synthetic disposable data. No production privacy/backup assertion. History outside fixture is out of scope; no committed revision exists, so source snapshots and hashes identify builds. Request logging is disabled in Handler.log_message; disposable stdout/stderr captured for runtime failures. No deployed bundle/build pipeline exists.

Input/sink inventory (S03): JSON text -> type/length/key checks -> bound SQLite UPDATE parameters -> JSON serialization -> textarea.value. Note id -> bound SQL parameter; list label and error/status text -> textContent. DOM created via createElement, replaceChildren and append; no innerHTML/eval, shell execution, rich text, upload or user URL sink. Login -> PBKDF2 and constant-time digest comparison. Preserve these defenses. Browser marker execution remains unobserved; source sink defenses and API/SQLite roundtrip are the supported evidence.

Session model (S04): random token_urlsafe(32), server-memory user/monotonic-expiry mapping, HttpOnly/SameSite=Strict/Path=/ cookie with Max-Age; HTTP is intentional isolated 127.0.0.1 fixture (no HTTPS/Secure claim). Logout pops server token and expires cookie; restart discards sessions. Probe actual expiry and restart.

Feature surfaces (S05): CSRF present via ambient cookie, Strict cookie and JSON-only body protect writes from cross-site browser requests; CORS absent as a feature (no grants or OPTIONS handler); uploads absent; public assets/login/logout present; abuse exposure present with 4096-byte JSON cap and text cap, but no agreed brute-force/rate budget. Bounded malformed/oversize probes only; browser cross-site cookie enforcement and agreed abuse controls remain unknown. Origin headers alone do not emulate browser security.

Authority/stable boundaries: change only a demonstrated violation in server.py. Keep owner-filtered list, native UI, labels/colors/assets, parameterized SQL, session implementation, localhost stdlib/SQLite architecture and response shapes. Nonowner resource should use existing 404 Not found convention without disclosing its existence. No ownership transfer, new auth system, registration, framework or service.

Runtime limits (S01–S05): local Python 3.9 project interpreter only; ephemeral port 0, disposable data. No production, remote services, browser execution, load test, external history/secret store or user research. No ASVS certification. S06 deferred at Standard.
''')
for command,filename in [('select','selection.json'),('template','template.json')]:
 r=subprocess.run([sys.executable,str(engine/'scripts/audit.py'),command,'--profile',str(out/'profile.json'),'--level','Standard','--group','S'],capture_output=True,text=True)
 (out/filename).write_text(r.stdout); (out/(filename+'.stderr')).write_text(r.stderr)
 if r.returncode: raise SystemExit(r.stderr)
