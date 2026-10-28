# Source inspection and preservation record

Requirement source: owner-notes/README.md, retained verbatim in before/source/README.md. Applies to S01-S05 at Standard. Context and environment: context.json. Actual byte-stream handler observations: before/observations.json. The unsuccessful listening-socket attempt is network-startup-failure.log; browser tool discovery found no browser capability and no target browser-test setup.

## Classification and observed defects (S01, S02)

Public: three explicitly routed static assets and demo identities named in the README. Restricted: another owner's note, even though test data is disposable. Session identifiers are secrets and are redacted in traces; public demo credentials are not production secrets. No real exposed credential was identified in the five target source files. No built bundle exists; the browser receives app.js directly. Logging is disabled via log_message. Git has no HEAD/committed history; no historical credential review is claimed.

The owner-filtered list is correct. Individual GET selects by id alone; PATCH updates by id alone. The identity check only ensures somebody is signed in. Actual Handler execution reproduced both Alice reading/updating Bob and Bob reading/updating Alice. Independent SQLite snapshots confirmed the forbidden writes committed. The original read and write return 200; expected 404 matches the existing missing-note API while enforcing the README's owner-only contract. S01 restricted data disclosure and S02 authorization violation are important, bounded failures in a disposable local fixture, not evidence of production impact.

## Positive controls and stable boundaries (S01-S05)

Before observations contain 120 records with six expected-result mismatches, all due to the two bidirectional ownership bypasses and their independent state checks. Valid logins, owner-filtered lists, owned reads/saves, empty and 1000-character notes, quotes/Unicode, ownership transfer rejection, invalid/1001-character payload rejection, missing IDs, anonymous denial, forged-session denial, logout replay denial, expiry denial, and SQLite retention across server recreation behaved as expected in actual handlers. The probe restores owner marker content after cross-owner probes; it uses fresh disposable SQLite per run. Source hashes bind the checks to the original files.

Keep the login/editor controls, labels, stylesheet, escaped text/value rendering, parameterized SQL, SQLite schema, session generation, HttpOnly and SameSite=Strict cookies, logout behavior, loopback stdlib architecture, and JSON API. No evidence supports a UI redesign, new framework, auth replacement, general sanitizer, CSRF middleware or rate-limiting infrastructure.

## Input-to-sink trace (S03)

Login username checks membership and passwords feed PBKDF2/HMAC; no command sink. Record IDs and note text use bound SQLite parameters. Browser note text goes into textarea.value, labels/errors/status into textContent, and nodes into append/replaceChildren; there is no innerHTML/eval sink. Server JSON serialization escapes structured response data. Quotes, Unicode, inert markup containing an onerror marker and SQL-like text roundtrip exactly through PATCH, GET and SQLite. Identifier injection marker returns 404. No browser executed: DOM execution behavior remains unknown; source findings and handler probes are not browser evidence.

## Session lifecycle (S04)

Login issues secrets.token_urlsafe(32) server-side tokens; sessions are memory-only entries with time.monotonic deadlines. Cookie has HttpOnly, SameSite=Strict, Path=/, Max-Age; Secure is absent consistently with explicitly permitted loopback HTTP. No HTTPS or production claim. Logout removes the presented entry and expires the cookie. Invalid/forged, logged-out and expired tokens are rejected for read/write; independent state snapshots show rejected writes do not commit. New login works. Recreating create_server resets the session closure and keeps SQLite; this is not a real process-restart test. Network transport/cookie enforcement and actual process restart are unexecuted, so complete S04 remains unknown.

## Independently classified surfaces (S05)

- CSRF present: cookie ambient authority. SameSite=Strict is declared. Actual handler rejects text/plain PATCH with 422 and OPTIONS preflight with 501. A foreign Origin does not itself authenticate anything; browser enforcement of cookies/preflight, login/logout CSRF behavior and a real cross-site workflow are unexecuted. Subcase unknown.
- CORS present: same-origin application; no cross-origin data-sharing use case in README. Same/foreign Origin handler reads return no Access-Control-Allow-Origin and preflight is unsupported. Source has no permissive CORS headers. This is not authorization; cross-owner authorization is independently tested. Browser enforcement unexecuted; handler/header checks complete only.
- Uploads absent: no route or UI, plain text JSON only. Not applicable subcase; no feature added.
- Public endpoints present: explicitly routed static assets are public. Login returns 401 on wrong credentials; protected/unknown filesystem-like paths without session return 401. Logout is idempotent and has no sensitive response. No production secret exposure demonstrated on public paths.
- Abuse surface present: login and JSON input. Payload handler bounds Content-Length at 4096 and notes at 1000 characters; oversized/malformed JSON returns 422 without mutation, wrong passwords return 401. No agreed rate/concurrency budget; only bounded low-volume probes performed. No brute force, saturation or timing claims; abuse resistance beyond input validation unknown.

## Authorized correction and recheck plan (S01, S02)

Add authenticated owner equality to the existing parameterized GET predicate and UPDATE predicate, keeping denial indistinguishable from missing IDs. Exactly two SQL statements and corresponding bound parameter tuples change. This directly prevents the demonstrated leak/write for both users. Cost/risk: small local predicate change; verify owned operations and all forbidden mutations separately. Run the identical probe after editing and compare all baseline failures plus positive controls, including SQLite state. Preserve the baseline report and artifacts before the edit. Full browser/live-network checks remain unavailable and must not become passes.
