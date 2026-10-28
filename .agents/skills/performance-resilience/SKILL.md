---
name: performance-resilience
description: Measure core-task failures, network recovery, interaction budgets, repeated resource lifecycles and defined load/reconnection behavior. Use for reproducible performance or resilience investigations.
license: MIT
metadata:
  version: "1.0.0"
---

# Performance & Resilience: Inspect → Improve → Recheck

Use when the requested audit includes group P; report only the agreed groups. Reuse the canonical [P01-P06 protocols](references/engine/criteria/v1.json), [method and decisions](references/engine/docs/method.md) and [English report template](references/engine/docs/report-template.md). Use `references/engine` as engine root when bundled; otherwise the repository root three directories above this skill directory. No sibling skill is required. Python and the engine requirements provide the shared validator; do not add another test framework by default.

## Conditions and scope

Inspect available requirements, three important tasks, users/data and runtime first. Ask only for facts changing expected behavior, applicability, impact, safe access or modification authority. Reuse existing permission; default to Essential inspection/recommendations if none is given. Announce a different level when a requested check requires it. Depth does not grant edit rights. Preflight actual tool/runtime access, not merely installed binary names. Use disposable data and authorized local/test environments.

## Inspect

- P01: exercise important tasks and correlate runtime exceptions with actual task failure. Separate unrelated extension/console noise from app defects.
- P02: induce offline, timeout and server rejection where relevant. Record waiting termination, truthful feedback, retained data and a safe retry; do not retry indefinitely or infer no commit from a missing response.
- P03: establish relevant task budgets and measurement conditions before judging them. Record build, browser/hardware, viewport, cache/network, repetitions and distribution/percentile calculation. Prefer the same controlled setup before/after. Field CWV requires adequate actual field p75 LCP/INP/CLS data; local task timing may demonstrate an agreed-budget failure but cannot establish a full CWV pass. Keep field conclusions unknown without that data.
- P04: define a warmed-up repeated-use cycle and intended lifecycle; observe timers, subscriptions, requests and relevant resources at several checkpoints and teardown. One heap snapshot does not prove a leak.
- P05: at Advanced, agree representative volume/concurrency, duration, latency/error/resource budgets and authorized test environment before load testing. No universal capacity target is invented.
- P06: where real-time/offline/background sync exists, test contract-permitted disconnect, duplicates, gaps and ordering with authoritative server/client readback. Do not invent a client sequence scheme independently of the protocol.

Save immutable before observations and a criterion-linked report before editing. Include revision/file hashes, environment/tool versions, exact task/probe inputs, expected versus actual values, timestamps and raw artifacts. Record the source of the requirement. Use true/false/null app features with rationales; missing tools do not make an app feature absent. Run the shared engine's `select` and `template` with the agreed level and `--group P`. Keep `criterion_groups` in JSON. All selected IDs need a supported outcome; later-level IDs are deferred, not passed.

## Improve

Use the canonical fix/propose/preserve/investigate decision rule. Fix only demonstrated violations within existing, proportionate authority. Propose a measured benefit or a needed scope/product decision. Preserve satisfactory behavior and preferences without demonstrated benefit. Investigate missing contracts/evidence. Severity is independent; an essential outcome blocked without a valid workaround remains a blocker even when edits are not authorized.

Before editing, list the parts already meeting the contract and their positive-control checks. Record permitted changes and stable design/data/API boundaries. Make the smallest correction and retain a patch. Do not refactor, restyle, replace native controls or add infrastructure unrelated to the evidenced problem. If a patch affects a protected boundary, explain why and verify it; do not silently expand scope.

## Recheck and evidence

Run the same measured tasks and fault sequences after the correction; retain distributions and raw samples, not a single favorable number. Recheck data accuracy, successful paths and existing response behavior. Preserve already-fast tasks, caching, layouts and application structure unless measurements justify changing them. A local latency improvement is not field CWV, user research or a general scalability result. Missing agreed budgets, sufficient field data or safe load access leaves the corresponding conclusion unknown.

Repeat the original reproduction and the positive controls, saving after evidence/report separately. Keep known failures/severity when their correction is unverified; never count unexecuted checks as pass. A previously failing outcome may become pass only on sufficient matching recheck evidence, with the earlier failure and fix retained as history. Unknown, not applicable and deferred outcomes stay visible. No total score may conceal a blocker.

Use the shared report schema and English template. Every factual conclusion, fix/proposal/preserve decision and limitation links criterion ID plus evidence IDs/locations. Validate with `scripts/audit.py validate --report <report.json>`; for an installation outside the app workspace pass `--evidence-root <absolute-target-workspace>` so local evidence resolves there rather than inside the installed skill. Use an available interpreter with the bundled `requirements.txt`; installed skill files do not need to be writable. Review evidence sufficiency and Markdown/JSON agreement even when validation passes.

## Limits

Follow [missing-access guidance](references/engine/docs/missing-access.md) for unavailable browser, runtime or credentials. Continue independent work, record the actual collection attempt and leave dependent conclusions unknown. A failed tool probe alone is not an application failure. Source review, handler tests, browser behavior, field measurements and real-user evidence have different scopes. Report the strongest conclusion actually supported. During evaluation do not seek hidden tests, expected findings or reference fixes. A manual walkthrough or isolated agent attempt is not a controlled skill-effectiveness study.
