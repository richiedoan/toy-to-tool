# Local task tracker

A single-person tracker for non-sensitive tasks, served locally in a browser. No account or backend is required.

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory fixtures/tracker
```

Open http://127.0.0.1:8765. If this folder is used as a standalone checkout, use `--directory .` instead.

## Agreed behavior

Three important tasks:

1. Add a titled task and see it in the list.
2. Edit a task's note and completion status, save, then read the saved values.
3. Refresh or reopen the same origin in the same browser profile and recover the saved tasks and their values.

Titles are trimmed and must contain 1-80 characters. Notes allow up to 500 characters. Unicode and ordinary punctuation are valid. Each submitted intention creates one record even if activation is repeated while pending; a separate later intentional submission with the same title is allowed. Failed persistence must not be reported as saved, and existing saved data must remain intact.

Storage is browser-local at the same scheme/host/port. Cross-device sync, accounts, concurrent-tab editing, server deployment and shared records are outside this contract. Do not add them. Test only disposable local records. Changing origin or clearing browser storage is not a required retention transition.
