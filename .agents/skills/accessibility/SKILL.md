---
name: accessibility
description: Evaluate keyboard access, names and semantics, contrast, zoom/reflow, focus and pointer targets against the applicable WCAG 2.2 definitions. Use for scoped accessibility inspections and verification.
---

# Accessibility: Inspect → Improve → Recheck

Use when the requested audit includes group A; report only the agreed groups. Reuse the canonical [A01-A06 protocols](../../../criteria/v1.json), [method and decisions](../../../docs/method.md) and [English report template](../../../docs/report-template.md). Use `references/engine` as engine root when bundled; otherwise the repository root three directories above this skill directory. No sibling skill is required. Python and the engine requirements provide the shared validator; do not add another test framework by default.

## Conditions and scope

Inspect available requirements, three important tasks, users/data and runtime first. Ask only for facts changing expected behavior, applicability, impact, safe access or modification authority. Reuse existing permission; default to Essential inspection/recommendations if none is given. Announce a different level when a requested check requires it. Depth does not grant edit rights. Preflight actual tool/runtime access, not merely installed binary names. Use disposable data and authorized local/test environments.

## Inspect

- A01: complete important tasks with keyboard alone, recording focus order and entry/exit from widgets. Apply the path-dependent-function exception correctly; text entry is not exempt merely because one input technique is handwriting.
- A02: inspect actual accessible names, native labels, roles and exposed state changes using browser accessibility information. Prefer correct native controls; preserve them rather than adding redundant ARIA. If assistive-technology behavior is not exercised, record that limit.
- A03: measure actual text/background colors and compositing across relevant states. Use the canonical 4.5:1 normal / 3:1 large-text thresholds, source large-text definition and exact incidental/logo exceptions. Screenshots alone are not measurements.
- A04: test text resizing to 200%, then reflow at equivalent 320 CSS pixel width for vertical content or 256 CSS pixel height for horizontal content. Record zoom and actual dimensions; examine essential two-dimensional regions separately.
- A05: traverse sticky, dialog and overlay states. Capture visible focus and whether author content entirely hides the focused component; respect source notes and do not impose AAA appearance rules as AA minima.
- A06: measure actual hit regions, including spacing geometry for undersized targets. Apply 24 by 24 CSS pixels and all canonical exceptions individually; inline links are not categorically forced into square buttons.

Save immutable before observations and a criterion-linked report before editing. Include revision/file hashes, environment/tool versions, exact task/probe inputs, expected versus actual values, timestamps and raw artifacts. Record the source of the requirement. Use true/false/null app features with rationales; missing tools do not make an app feature absent. Run the shared engine's `select` and `template` with the agreed level and `--group A`. Keep `criterion_groups` in JSON. All selected IDs need a supported outcome; later-level IDs are deferred, not passed.

## Improve

Use the canonical fix/propose/preserve/investigate decision rule. Fix only demonstrated violations within existing, proportionate authority. Propose a measured benefit or a needed scope/product decision. Preserve satisfactory behavior and preferences without demonstrated benefit. Investigate missing contracts/evidence. Severity is independent; an essential outcome blocked without a valid workaround remains a blocker even when edits are not authorized.

Before editing, list the parts already meeting the contract and their positive-control checks. Record permitted changes and stable design/data/API boundaries. Make the smallest correction and retain a patch. Do not refactor, restyle, replace native controls or add infrastructure unrelated to the evidenced problem. If a patch affects a protected boundary, explain why and verify it; do not silently expand scope.

## Recheck and evidence

Repeat the affected keyboard/assistive-technology path and actual measurements at the same states. Recheck adjacent controls, supported zoom and unaffected native semantics. Preserve working labels, focus order, design tokens and inline content when no applicable violation is demonstrated. The six criteria and one automated scan cannot establish WCAG AA conformance. Missing browser, actual colors, geometry or required AT evidence leaves the relevant claim unknown.

Repeat the original reproduction and the positive controls, saving after evidence/report separately. Keep known failures/severity when their correction is unverified; never count unexecuted checks as pass. A previously failing outcome may become pass only on sufficient matching recheck evidence, with the earlier failure and fix retained as history. Unknown, not applicable and deferred outcomes stay visible. No total score may conceal a blocker.

Use the shared report schema and English template. Every factual conclusion, fix/proposal/preserve decision and limitation links criterion ID plus evidence IDs/locations. Validate with `scripts/audit.py validate --report <report.json>`; for an installation outside the app workspace pass `--evidence-root <absolute-target-workspace>` so local evidence resolves there rather than inside the installed skill. Use an available interpreter with the bundled `requirements.txt`; installed skill files do not need to be writable. Review evidence sufficiency and Markdown/JSON agreement even when validation passes.

## Limits

Follow [missing-access guidance](../../../docs/missing-access.md) for unavailable browser, runtime or credentials. Continue independent work, record the actual collection attempt and leave dependent conclusions unknown. A failed tool probe alone is not an application failure. Source review, handler tests, browser behavior, field measurements and real-user evidence have different scopes. Report the strongest conclusion actually supported. During evaluation do not seek hidden tests, expected findings or reference fixes. A manual walkthrough or isolated agent attempt is not a controlled skill-effectiveness study.
