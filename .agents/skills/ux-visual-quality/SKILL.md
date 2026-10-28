---
name: ux-visual-quality
description: Evaluate screen purpose, reachable states, responsive task access, error recovery and pattern consistency. Use for usability and layout audits with evidence-led, scoped changes.
license: MIT
metadata:
  version: "1.0.0"
---

# UX & Visual Quality: Inspect → Improve → Recheck

Use when the requested audit includes group U; report only the agreed groups. Reuse the canonical [U01-U06 protocols](references/engine/criteria/v1.json), [method and decisions](references/engine/docs/method.md) and [English report template](references/engine/docs/report-template.md). Use `references/engine` as engine root when bundled; otherwise the repository root three directories above this skill directory. No sibling skill is required. Python and the engine requirements provide the shared validator; do not add another test framework by default.

## Conditions and scope

Inspect available requirements, three important tasks, users/data and runtime first. Ask only for facts changing expected behavior, applicability, impact, safe access or modification authority. Reuse existing permission; default to Essential inspection/recommendations if none is given. Announce a different level when a requested check requires it. Depth does not grant edit rights. Preflight actual tool/runtime access, not merely installed binary names. Use disposable data and authorized local/test environments.

## Inspect

- U01: map each important screen and primary action to an agreed task. Label expert interpretation separately from participant evidence; do not claim users understand because the agent does.
- U02: list reachable loading, empty, success, error and disabled states. Induce a real or controlled request failure and slow response, then follow the available recovery action. Observe retained data and whether waiting ends.
- U03: record target CSS viewports/devices and complete the important tasks. Save screenshots and exact obstructed-control coordinates; exempt meaningful two-dimensional content rather than every horizontal scrollbar.
- U04: try correction, cancel/back and destructive actions only where present. Match prevention or undo to the actual consequence; avoid confirmations for every reversible action.
- U05: compare equivalent controls/states and documented design patterns. Preserve intentional differences and the existing visual language. Aesthetic preference without a requirement or measured benefit means preserve.
- U06: at Advanced, define task goals before real target-user sessions; record participant count/conditions, completion, errors/time and limitations. Without real participants, unknown.

Save immutable before observations and a criterion-linked report before editing. Include revision/file hashes, environment/tool versions, exact task/probe inputs, expected versus actual values, timestamps and raw artifacts. Record the source of the requirement. Use true/false/null app features with rationales; missing tools do not make an app feature absent. Run the shared engine's `select` and `template` with the agreed level and `--group U`. Keep `criterion_groups` in JSON. All selected IDs need a supported outcome; later-level IDs are deferred, not passed.

## Improve

Use the canonical fix/propose/preserve/investigate decision rule. Fix only demonstrated violations within existing, proportionate authority. Propose a measured benefit or a needed scope/product decision. Preserve satisfactory behavior and preferences without demonstrated benefit. Investigate missing contracts/evidence. Severity is independent; an essential outcome blocked without a valid workaround remains a blocker even when edits are not authorized.

Before editing, list the parts already meeting the contract and their positive-control checks. Record permitted changes and stable design/data/API boundaries. Make the smallest correction and retain a patch. Do not refactor, restyle, replace native controls or add infrastructure unrelated to the evidenced problem. If a patch affects a protected boundary, explain why and verify it; do not silently expand scope.

## Recheck and evidence

Recreate the original state/device and repeat the obstructed or confusing task. Capture before/after screenshots and next-action results. Include positive controls at already-working desktop sizes; preserve labels, colors, typography, information order and existing interactions unless the evidenced correction specifically needs a change. A responsive fix may alter mobile layout, not justify a desktop redesign. Usability research remains unknown when only an expert review ran.

Repeat the original reproduction and the positive controls, saving after evidence/report separately. Keep known failures/severity when their correction is unverified; never count unexecuted checks as pass. A previously failing outcome may become pass only on sufficient matching recheck evidence, with the earlier failure and fix retained as history. Unknown, not applicable and deferred outcomes stay visible. No total score may conceal a blocker.

Use the shared report schema and English template. Every factual conclusion, fix/proposal/preserve decision and limitation links criterion ID plus evidence IDs/locations. Validate with `scripts/audit.py validate --report <report.json>`; for an installation outside the app workspace pass `--evidence-root <absolute-target-workspace>` so local evidence resolves there rather than inside the installed skill. Use an available interpreter with the bundled `requirements.txt`; installed skill files do not need to be writable. Review evidence sufficiency and Markdown/JSON agreement even when validation passes.

## Limits

Follow [missing-access guidance](references/engine/docs/missing-access.md) for unavailable browser, runtime or credentials. Continue independent work, record the actual collection attempt and leave dependent conclusions unknown. A failed tool probe alone is not an application failure. Source review, handler tests, browser behavior, field measurements and real-user evidence have different scopes. Report the strongest conclusion actually supported. During evaluation do not seek hidden tests, expected findings or reference fixes. A manual walkthrough or isolated agent attempt is not a controlled skill-effectiveness study.
