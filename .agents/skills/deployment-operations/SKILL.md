---
name: deployment-operations
description: Check reproducible startup, runtime configuration, data preservation, failure diagnosis and verified recovery objectives. Use for app setup and operational-readiness audits appropriate to the real deployment.
license: MIT
metadata:
  version: "1.0.0"
---

# Deployment & Operations: Inspect → Improve → Recheck

Use when the requested audit includes group O; report only the agreed groups. Reuse the canonical [O01-O06 protocols](references/engine/criteria/v1.json), [method and decisions](references/engine/docs/method.md) and [English report template](references/engine/docs/report-template.md). Use `references/engine` as engine root when bundled; otherwise the repository root three directories above this skill directory. No sibling skill is required. Python and the engine requirements provide the shared validator; do not add another test framework by default.

## Conditions and scope

Inspect available requirements, three important tasks, users/data and runtime first. Ask only for facts changing expected behavior, applicability, impact, safe access or modification authority. Reuse existing permission; default to Essential inspection/recommendations if none is given. Announce a different level when a requested check requires it. Depth does not grant edit rights. Preflight actual tool/runtime access, not merely installed binary names. Use disposable data and authorized local/test environments.

## Inspect

- O01: use a clean copy/checkout and the declared runtime/configuration. Capture install/build/start commands, dependency versions and an actual smoke task. Distinguish a broken supported setup from an unavailable evaluator runtime.
- O02: only where deployed, inspect variable names, URL/config boundaries, storage and local/deployed differences without revealing values. Test required persistence transitions; do not put private config in a client bundle.
- O03: establish important data, accepted loss, ownership and actual preservation mechanism. Distinguish manual export from automatic backup. Stateless or replaceable fixture data does not require a database backup.
- O04: inject a safe failure in an authorized environment; verify the responsible owner can detect it and has sufficient redacted context to investigate. Preserve simple working logs when adequate; do not install a telemetry platform by default.
- O05: execute each required restore/rollback in isolation and verify data integrity, schema compatibility, smoke tasks, elapsed time and limitations. Reading a runbook or finding a backup file cannot establish restore success.
- O06: at Advanced agree SLOs, recovery time/loss, measurement windows, alert ownership and response. Inspect sufficient observations; do not invent uptime/on-call targets.

Save immutable before observations and a criterion-linked report before editing. Include revision/file hashes, environment/tool versions, exact task/probe inputs, expected versus actual values, timestamps and raw artifacts. Record the source of the requirement. Use true/false/null app features with rationales; missing tools do not make an app feature absent. Run the shared engine's `select` and `template` with the agreed level and `--group O`. Keep `criterion_groups` in JSON. All selected IDs need a supported outcome; later-level IDs are deferred, not passed.

## Improve

Use the canonical fix/propose/preserve/investigate decision rule. Fix only demonstrated violations within existing, proportionate authority. Propose a measured benefit or a needed scope/product decision. Preserve satisfactory behavior and preferences without demonstrated benefit. Investigate missing contracts/evidence. Severity is independent; an essential outcome blocked without a valid workaround remains a blocker even when edits are not authorized.

Before editing, list the parts already meeting the contract and their positive-control checks. Record permitted changes and stable design/data/API boundaries. Make the smallest correction and retain a patch. Do not refactor, restyle, replace native controls or add infrastructure unrelated to the evidenced problem. If a patch affects a protected boundary, explain why and verify it; do not silently expand scope.

## Recheck and evidence

Repeat clean startup or the affected isolated recovery/configuration/failure drill with the documented procedure. Confirm target tasks and durable-data integrity rather than a process merely existing. Preserve reproducible stdlib/simple setups and existing adequate diagnostics; no Docker, cloud deployment, database, backups or monitoring stack without an actual need. Unavailable production access or unexecuted restore leaves those claims unknown, not passed. Exclusions require architecture/data evidence.

Repeat the original reproduction and the positive controls, saving after evidence/report separately. Keep known failures/severity when their correction is unverified; never count unexecuted checks as pass. A previously failing outcome may become pass only on sufficient matching recheck evidence, with the earlier failure and fix retained as history. Unknown, not applicable and deferred outcomes stay visible. No total score may conceal a blocker.

Use the shared report schema and English template. Every factual conclusion, fix/proposal/preserve decision and limitation links criterion ID plus evidence IDs/locations. Validate with `scripts/audit.py validate --report <report.json>`; for an installation outside the app workspace pass `--evidence-root <absolute-target-workspace>` so local evidence resolves there rather than inside the installed skill. Use an available interpreter with the bundled `requirements.txt`; installed skill files do not need to be writable. Review evidence sufficiency and Markdown/JSON agreement even when validation passes.

## Limits

Follow [missing-access guidance](references/engine/docs/missing-access.md) for unavailable browser, runtime or credentials. Continue independent work, record the actual collection attempt and leave dependent conclusions unknown. A failed tool probe alone is not an application failure. Source review, handler tests, browser behavior, field measurements and real-user evidence have different scopes. Report the strongest conclusion actually supported. During evaluation do not seek hidden tests, expected findings or reference fixes. A manual walkthrough or isolated agent attempt is not a controlled skill-effectiveness study.
