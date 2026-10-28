# Local metrics dashboard

Python 3.9+ and a browser are sufficient; no dependencies or build step:

```sh
python3 fixtures/dashboard/server.py --port 8767
```

Open http://127.0.0.1:8767. This localhost fixture reads deterministic, replaceable metrics; it stores no user data and has no login, upload, synchronization or production deployment.

## Agreed tasks and quality boundaries

1. Read the current metrics on supported widths of 320, 390, 768 and 1440 CSS pixels.
2. Filter metric titles and read matching values accurately.
3. Refresh data; if the API fails, see an explanation, retain the last successful data when available, and retry using Refresh data.

The refresh action and text must remain reachable on mobile without horizontal page scrolling. Existing desktop hierarchy, colors, typography, labels, metric values and native controls are approved; preserve them. Keep keyboard access, control labels and focus indicators. Do not redesign the dashboard or add a frontend framework.

Local filter responsiveness budget: after warmup, p95 of five consecutive input-event-to-next-animation-frame measurements must be <= 100ms in the same local Chrome setup at 1440x900, no artificial CPU/network throttling. Record actual hardware/browser, samples and percentile calculation. This is a fixture task budget, not field CWV or a universal performance requirement. Filtering must not change metric values or refresh data.

The API is `/api/metrics`. For authorized fault checks, `/api/metrics?unavailable=1` returns a controlled 503; the local operator gets a structured stderr event with a request ID. `--fail-on N` rejects that numbered metrics request once. Preserve useful redacted diagnostics; a monitoring service is not required. App release rollback is not an operational requirement for this undeployed, replaceable-data fixture.
