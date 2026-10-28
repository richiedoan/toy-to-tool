# Functionality & Data workflow evaluation

This directory belongs to the evaluator. Do not give it to an evaluated coding agent. It contains hidden checks, expected findings and earlier results. The target app is `fixtures/tracker/`; its README contains only product requirements and setup instructions. The canonical skill is `.agents/skills/functionality-data/SKILL.md`.

## Run the current local tracker

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory fixtures/tracker
```

Use http://127.0.0.1:8765. Task data stays in that browser origin/profile. This is a test fixture with disposable data, not a hosted service.

## Restore the original and prepare a clean agent packet

```sh
python3 evaluation/prepare_packet.py --bootstrap /tmp/tracker-fresh-agent
```

The destination must be outside this evaluator repository and must not exist. The exporter verifies archive and per-file SHA256 hashes, restores the original tracker into `tracker/`, copies only a positive allowlist of criteria/engine/skill files, adds neutral instructions and creates a fresh Git repository without history. It does not copy this directory, the main README, expected findings, previous reports, comparison tests or fixed code. `--bootstrap` provisions and validates Python dependencies before an agent enters a restricted environment; omit it for a source-only packet and disclose the missing capability.

The immutable baseline is `baselines/tracker-v1.tar.gz`; its manifest is adjacent. Do not overwrite the current app to restore it. The [expected findings](private/expected-findings.md) are evaluator-only. Packet separation prevents deliberate context injection; it is not an OS read-isolation guarantee. Give the independent agent no surrounding authoring conversation or oracle content. Use only the packet as its working directory and retain the neutral prompt, actual commands/events and environment limits. Inspect transcripts for reads outside the packet before calling a trial context-separated.

A suitable neutral prompt is: “Use the functionality-data skill in this workspace. Inspect the tracker against its README, preserve a before report, make proportionate authorized corrections, then recheck and save the after report and regression evidence. Standard; Functionality & Data only. Use disposable local data and do not read outside the supplied workspace.”

Preflight engine imports, loopback binding and actual browser launch in the execution environment. A logged-in CLI is not proof that those capabilities work inside its sandbox. Do not bypass the sandbox merely to make a trial succeed. If browser execution is unavailable, retain source/handler findings with their explicit limitations and perform a separately labeled evaluator-led browser recheck, or leave browser results unknown.

## Evaluator browser checks

Requires Node.js and installed Google Chrome. Playwright is a pinned evaluator-only development dependency; the tracker itself has no Node dependency.

```sh
npm ci --prefix evaluation
node evaluation/browser-check.mjs fixtures/tracker evaluation/runs/new-check
```

Always use a new output directory. Exit 0 means every executed scenario assertion passed; exit 1 reports at least one scenario failure. A launch/dependency failure is an infrastructure failure, not proof of an app defect. The harness starts a loopback-only server for the supplied app, isolates browser contexts, inspects only the fixture storage key and closes browser/server resources. It records source hashes, environment, test steps, actual UI/storage state, screenshots and traces. Test titles use actual programmatic boundary injection when needed; assert the injected length so HTML maxlength cannot silently change the case being tested.

Inspect traces with the local Playwright trace viewer if needed. Initial baseline and fixed app were checked using the same 12 browser scenarios. Immutable, sanitized evidence is saved under [evidence/tracker-v1](evidence/tracker-v1). Raw temporary runs are ignored by Git. Reports are generated from actual results by `make_report.py`, not from the oracle, and refuse to overwrite an existing report. Both reports declare group F; other groups have no assessed result.

## What this exercise establishes

Read the [run record](evidence/tracker-v1/workflow.md), [before report](evidence/tracker-v1/before-report.md) and [after report](evidence/tracker-v1/after-report.md). They separate a fresh CLI coding attempt with restricted runtime access from evaluator-led Chrome observations. The CLI's Node adapter tests execute app handlers but do not prove real browser persistence; the later evaluator browser checks establish the limited outcomes they actually ran. No result here is a controlled comparison of skill versus no skill, and no effectiveness gain is claimed.

## Additional group trials

`prepare_expansion.py` exports owner-notes with the Security & Privacy skill, or dashboard with UX/Accessibility/Performance/Operations skills. Each exported skill carries its canonical engine and references; no sibling repository is required. Exported fixtures retain `fixtures/<name>/` so README startup commands remain valid.

```sh
python3 evaluation/prepare_expansion.py owner-notes /tmp/owner-notes-fresh --bootstrap
python3 evaluation/prepare_expansion.py dashboard /tmp/dashboard-fresh --bootstrap
node evaluation/expansion-check.mjs owner-notes fixtures/owner-notes evaluation/runs/new-owner-check
node evaluation/expansion-check.mjs dashboard fixtures/dashboard evaluation/runs/new-dashboard-check
```

Use new external packet destinations and new output directories under `evaluation/`. The harness redacts session/authentication fields from traces using the stdlib evaluator utility; this is not an app modification. `owner-notes-v2` is the runnable buggy baseline; v1 is kept only for the recorded unavailable-scrypt calibration. Dashboard uses v1. Both have adjacent hash manifests. Evaluator-only expectations are in `private/expansion-expected-findings.md`; they are not exported. The [expansion handover](evidence/expansion-v1/workflow.md) separates the two fresh CLI attempts from real evaluator HTTP/Chrome observations, preservation evidence and unexecuted checks. `expansion_reports.py` maps recorded observations and explicit coverage gaps into the same schema; it refuses to overwrite reports and does not promote a local task-budget pass into field CWV.

## Installed release smoke and controlled comparison

The [release-v1 verification](evidence/release-v1/verification.md) records `skills` CLI discovery, a copied install into a new target project, explicit Codex invocation from that installed copy, resource integrity and a real HTTP/Chrome recheck of the installed target fixture. It is an integration smoke, not an efficacy comparison.

The paired skills/no-skills protocol is documented in [docs/comparison.md](../docs/comparison.md). Its runner restores every arm from immutable archives, pins model/prompt/tools/budgets, hashes inputs, rejects reused workspaces and requires independent evidence-backed adjudication. Its current [status](comparison/STATUS.json) is `not_evaluated`; the local profile failed the clean-environment preflight, so no model runs or comparative metrics were created.
