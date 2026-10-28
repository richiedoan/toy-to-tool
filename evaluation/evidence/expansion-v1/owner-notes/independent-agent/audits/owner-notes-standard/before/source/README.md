# Owner notes (local fixture)

Run with Python 3.9+; no third-party packages or build step:

```sh
python3 fixtures/owner-notes/server.py --port 8766 --data-dir /tmp/owner-notes-data
```

Open http://127.0.0.1:8766. This is an isolated localhost fixture using disposable data, not production authentication. Public test identities are `alice` / `alice-demo` and `bob` / `bob-demo`.

## Agreed tasks and boundaries

1. Sign in, list and read your own notes.
2. Edit your own note, save and independently read the committed text.
3. Sign out; the previous session no longer accesses protected routes.

Each user may list, read and update only their own records. Anonymous requests cannot access protected routes. Users cannot transfer note ownership. Notes are plain text up to 1000 characters; quotes and Unicode are valid. Use test accounts A/B for verification. SQLite stores records across process restarts; sessions expire in memory and are invalid after server restart. `--session-seconds` selects a bounded local test-session lifetime (default 1800).

Preserve the current native login/editor controls, labels, green/neutral design, correctly owner-filtered list, parameterized SQL, text-safe rendering, logout behavior and local stdlib/SQLite setup. Corrections must retain the existing API contract and valid owned operations. Do not add account registration, a framework, cloud services, or a new auth system. Only disposable fixture data is used; no production privacy/backup claim is required.
