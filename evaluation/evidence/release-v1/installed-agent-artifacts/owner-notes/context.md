# Requirement, scope and source inspection (S01–S05)

Requirement source: fixtures/owner-notes/README.md (immutable copy before/README.md). User authorizes proportionate app-only fixes at Standard, preserving README, UI, API and working behavior.

Three priority tasks: A/B sign in and list/read only their own note; edit own text and independently read committed SQLite text; sign out and replay old session with access denied. SQLite persists restart; sessions do not. Note ownership cannot transfer. Text <=1000 characters, including quotes and Unicode.

Classification: source and static HTML/JS/CSS are public fixture implementation; alice/bob passwords are deliberately public test identities, not leaked production credentials. In-memory session tokens are private, never saved here. Note text is owner-only, even though synthetic disposable data. No production privacy/backup assertion. History outside fixture is out of scope; no committed revision exists, so source snapshots and hashes identify builds. Request logging is disabled in Handler.log_message; disposable stdout/stderr captured for runtime failures. No deployed bundle/build pipeline exists.

Input/sink inventory (S03): JSON text -> type/length/key checks -> bound SQLite UPDATE parameters -> JSON serialization -> textarea.value. Note id -> bound SQL parameter; list label and error/status text -> textContent. DOM created via createElement, replaceChildren and append; no innerHTML/eval, shell execution, rich text, upload or user URL sink. Login -> PBKDF2 and constant-time digest comparison. Preserve these defenses. Browser marker execution remains unobserved; source sink defenses and API/SQLite roundtrip are the supported evidence.

Session model (S04): random token_urlsafe(32), server-memory user/monotonic-expiry mapping, HttpOnly/SameSite=Strict/Path=/ cookie with Max-Age; HTTP is intentional isolated 127.0.0.1 fixture (no HTTPS/Secure claim). Logout pops server token and expires cookie; restart discards sessions. Probe actual expiry and restart.

Feature surfaces (S05): CSRF present via ambient cookie, Strict cookie and JSON-only body protect writes from cross-site browser requests; CORS absent as a feature (no grants or OPTIONS handler); uploads absent; public assets/login/logout present; abuse exposure present with 4096-byte JSON cap and text cap, but no agreed brute-force/rate budget. Bounded malformed/oversize probes only; browser cross-site cookie enforcement and agreed abuse controls remain unknown. Origin headers alone do not emulate browser security.

Authority/stable boundaries: change only a demonstrated violation in server.py. Keep owner-filtered list, native UI, labels/colors/assets, parameterized SQL, session implementation, localhost stdlib/SQLite architecture and response shapes. Nonowner resource should use existing 404 Not found convention without disclosing its existence. No ownership transfer, new auth system, registration, framework or service.

Runtime limits (S01–S05): local Python 3.9 project interpreter only; ephemeral port 0, disposable data. No production, remote services, browser execution, load test, external history/secret store or user research. No ASVS certification. S06 deferred at Standard.
