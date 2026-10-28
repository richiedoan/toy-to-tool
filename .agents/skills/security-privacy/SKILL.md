---
name: security-privacy
description: Assess authorization, data exposure, execution boundaries and session behavior using authorized test identities and safe probes. Use for architecture-specific security audits and narrowly verified corrections.
license: MIT
metadata:
  version: "1.0.0"
---

# Security & Privacy: Inspect → Improve → Recheck

Use when the requested audit includes group S; report only the agreed groups. Reuse the canonical [S01-S06 protocols](references/engine/criteria/v1.json), [method and decisions](references/engine/docs/method.md) and [English report template](references/engine/docs/report-template.md). Use `references/engine` as engine root when bundled; otherwise the repository root three directories above this skill directory. No sibling skill is required. Python and the engine requirements provide the shared validator; do not add another test framework by default.

## Conditions and scope

Inspect available requirements, three important tasks, users/data and runtime first. Ask only for facts changing expected behavior, applicability, impact, safe access or modification authority. Reuse existing permission; default to Essential inspection/recommendations if none is given. Announce a different level when a requested check requires it. Depth does not grant edit rights. Preflight actual tool/runtime access, not merely installed binary names. Use disposable data and authorized local/test environments.

## Inspect

- S01: classify intended public versus sensitive surfaces before inspecting accessible source, bundles, responses and redacted logs/history. Public fixture identities are not production secrets. A real exposed credential needs a scoped revocation/rotation proposal; deleting a line alone is insufficient.
- S02: build actor/resource/action cases for account A, account B and anonymous access. Send direct read and mutation requests for another test owner, then independently check the resource state. Test each protected boundary; a correctly filtered list or hidden button cannot establish object authorization.
- S03: trace untrusted data to relevant rendering/query/command sinks. Use harmless non-exfiltrating markers and context-correct defenses. Preserve parameterized queries and text-safe rendering rather than applying one sanitizer everywhere.
- S04: document the actual login, expiry, logout and invalidation model. Test live valid/invalid sessions and post-logout replay without saving session credentials in shared evidence. Transport/cookie expectations must match the permitted local or deployed architecture.
- S05: classify CSRF, CORS, uploads, public endpoints and abuse independently. Use only authorized, bounded probes on present surfaces. Unknown subcases cannot disappear behind an overall pass. CORS is not authentication or authorization.
- S06: at Advanced map data, assets, trust boundaries and plausible threats to verified controls and residual risks. A threat-model document is not proof of security.

Save immutable before observations and a criterion-linked report before editing. Include revision/file hashes, environment/tool versions, exact task/probe inputs, expected versus actual values, timestamps and raw artifacts. Record the source of the requirement. Use true/false/null app features with rationales; missing tools do not make an app feature absent. Run the shared engine's `select` and `template` with the agreed level and `--group S`. Keep `criterion_groups` in JSON. All selected IDs need a supported outcome; later-level IDs are deferred, not passed.

## Improve

Use the canonical fix/propose/preserve/investigate decision rule. Fix only demonstrated violations within existing, proportionate authority. Propose a measured benefit or a needed scope/product decision. Preserve satisfactory behavior and preferences without demonstrated benefit. Investigate missing contracts/evidence. Severity is independent; an essential outcome blocked without a valid workaround remains a blocker even when edits are not authorized.

Before editing, list the parts already meeting the contract and their positive-control checks. Record permitted changes and stable design/data/API boundaries. Make the smallest correction and retain a patch. Do not refactor, restyle, replace native controls or add infrastructure unrelated to the evidenced problem. If a patch affects a protected boundary, explain why and verify it; do not silently expand scope.

## Recheck and evidence

Replay the original forbidden request and allowed-owner/anonymous controls, covering read and write routes separately. Independently verify the other owner's data was not changed and authorized operations still work. Preserve existing login/session handling, parameterization, escaped UI and architecture when they meet the contract; do not reimplement auth or redesign the UI to fix one ownership check. Missing identities, permission or protected-boundary access leaves dependent checks unknown. Only the canonical checked mappings may be claimed; project levels are not ASVS certification levels.

Repeat the original reproduction and the positive controls, saving after evidence/report separately. Keep known failures/severity when their correction is unverified; never count unexecuted checks as pass. A previously failing outcome may become pass only on sufficient matching recheck evidence, with the earlier failure and fix retained as history. Unknown, not applicable and deferred outcomes stay visible. No total score may conceal a blocker.

Use the shared report schema and English template. Every factual conclusion, fix/proposal/preserve decision and limitation links criterion ID plus evidence IDs/locations. Validate with `scripts/audit.py validate --report <report.json>`; for an installation outside the app workspace pass `--evidence-root <absolute-target-workspace>` so local evidence resolves there rather than inside the installed skill. Use an available interpreter with the bundled `requirements.txt`; installed skill files do not need to be writable. Review evidence sufficiency and Markdown/JSON agreement even when validation passes.

## Limits

Follow [missing-access guidance](references/engine/docs/missing-access.md) for unavailable browser, runtime or credentials. Continue independent work, record the actual collection attempt and leave dependent conclusions unknown. A failed tool probe alone is not an application failure. Source review, handler tests, browser behavior, field measurements and real-user evidence have different scopes. Report the strongest conclusion actually supported. During evaluation do not seek hidden tests, expected findings or reference fixes. A manual walkthrough or isolated agent attempt is not a controlled skill-effectiveness study.
