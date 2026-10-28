---
name: functionality-data
description: Inspect and improve an application's real operations, persistence, outcome feedback, input rules, repeated actions and concurrent updates using criteria F01-F06. Use for Functionality & Data audits and verified scoped fixes.
---

# Functionality & Data: Inspect → Improve → Recheck

Use this repository's [evaluation method](../../../docs/method.md) and canonical [F01-F06 protocols](../../../criteria/v1.json). Use `references/engine` as the engine root when bundled; otherwise use the repository root three directories above this skill directory. Keep conversation in the user's language and saved artifacts in English. This skill assesses only Functionality & Data; other groups are outside its claim.

Reuse known user goals and authority. Inspect project docs, code and existing tests first. Ask only questions changing expected behavior, applicability, user impact, access or permission. Record the three important tasks, actual successful outcomes, users/data, persistence boundaries and runtime. Missing business contracts remain unknown. Default to Essential and read-only recommendations unless existing instructions specify otherwise. Repeated-action checks begin at Standard; concurrency begins at Advanced. Do not silently omit a requested repetition/concurrency check because of a default level.

## Inspect

Preflight the documented runtime, audit-engine interpreter/dependencies and required browser/test access before claiming an executable plan. An installed CLI or browser binary alone does not establish socket/process permission or usable dependencies. Attempt ordinary authorized local setup once; otherwise record the capability gap and separate source/handler evidence from browser outcomes.

1. Establish the data contract before changing code: create/read/update outcomes, retention transitions, validation limits and whether repetitions represent one intention or separate intentional actions. Identify the authoritative result: database/API, browser-local store, file or generated artifact, according to the actual architecture. A toast or changed input is not authoritative evidence.
2. Create a real app profile using the profile schema. Use true/false/null and evidence-backed rationales. Do not infer that all apps need a database, cross-device sync or conflict resolution. Run the engine's `select` and `template` with `--group F` and the agreed level. Retain `criterion_groups: ["F"]` in reports so excluded groups are not implicitly passed or artificially marked unknown.
3. Exercise each selected protocol. Pair visible outcome/feedback with an independent readback of actual values and counts. For persistence, read both saved state and what the app loads after each promised transition. For repetition, count identities/effects, not just titles; verify a later valid same-title action remains possible. For feedback, include slow/failure conditions and optimistic reconciliation where relevant. F04 requires valid, empty, malformed/oversized and boundary inputs at each relevant boundary; no missing server is invented.
4. Save an immutable before report and raw evidence before editing: timestamp, revision or file hashes, environment/tool versions, exact steps/test values, expected/actual observations, screenshots or traces where helpful. Create a reproduction/regression check that fails against that baseline. A check must assert the requirement rather than the injected implementation detail. If execution is unavailable, link the limitation and leave dependent outcomes unknown; source conclusions must state their narrower scope.

From the engine root, adapting the run path and level:

```sh
.venv/bin/python scripts/audit.py select --profile audits/<run-id>/profile.json --level Standard --group F
.venv/bin/python scripts/audit.py template --profile audits/<run-id>/profile.json --level Standard --group F
```

The template starts unexecuted. Once real observations exist, set `report_kind` to `audit`, populate evidence and record the actual `change_permission`. A seeded test application can yield real non-synthetic observations; the application is a fixture, not an invented observation.

## Improve

Use the canonical decision function. Demonstrated violations get the smallest authorized, proportionate fix; missing authority or product decisions get a proposal. Optional measured benefits are proposals, preference alone preserves, and missing evidence triggers investigation. Record user impact and contextual severity independently of permission. Assess impact against the named priority tasks: an essential outcome that cannot be completed without a contract-valid workaround is a blocker. Distinguish inaccessible saved data from proven permanent destruction by reading the store. Keep a blocker visible even if it cannot yet be fixed.

Preserve the verified baseline before edits. Work only on the authorized app/behavior. Do not replace its architecture just to simplify a test. Save a patch/change record linked to criterion IDs and the before evidence. Retain existing valid data, declared input rules and intentional repeated operations. Do not treat UI button disabling as sufficient if the actual operation can still create unintended repeated effects.

## Recheck

Run the original reproduction on the changed app under comparable conditions, then check neighboring behavior:

- Independently read back created and edited values, including completion flags or notes where relevant (F01).
- Refresh/reopen only the promised boundaries, with the same origin/profile/storage; preserve before/after values and counts (F02).
- Verify feedback on success, delayed completion and controlled failure; storage/request rejection must retain the input and previous committed data (F03).
- Rerun valid and boundary input cases, including Unicode and previously accepted data (F04).
- Verify rapid duplicate activation, retry when applicable, and a separate later same-title intention (F05).
- If relevant and selected, use independent competing sessions and the agreed consistency rule; otherwise document genuine absence or deferral (F06).

Save an after report separately; never overwrite the before report or raw observations. A patch with an unexecuted recheck retains the demonstrated failure and severity, with verification pending. A now-passing current row uses null severity and preserves the earlier failure/fix in the change history. Do not mix historical failing rows into current aggregation.

Validate both reports using the existing engine. Link every conclusion and preservation/proposal decision to criterion IDs and real evidence. List unresolved blockers first, then other failures, verified fixes, unknowns and exclusions/deferred checks. Do not emit a quality score. The report should distinguish browser observations, automated assertions, source inspection and user evidence, rather than treating them as interchangeable.

## Capability limits and evaluation hygiene

If tools/access are missing, follow [the fallback guidance](../../../docs/missing-access.md). Continue independent checks and record the exact missing resource. Test execution failure is not automatically an app failure. Unit tests cannot establish browser persistence by themselves.

When this skill is being evaluated, use only the supplied app requirements, allowed workspace and skill resources. Do not seek evaluator-only expected findings, hidden tests, prior before/after reports or reference fixes. Keep your own observations and change history. A manual walkthrough or one independent agent run can verify a workflow but does not establish that skills improve coding-agent effectiveness; that requires a separately designed comparison.

For a separate installation, create artifacts in the target workspace and pass its absolute path as `--evidence-root` when validating reports. Use the bundled engine requirements with an available Python interpreter; no sibling skill is required.
