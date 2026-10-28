# Implementation decisions and review record

## Implemented choices

- JSON is the only structured data format. JSON Schema 2020-12 validates shape; Python checks the exact ID set, group/starting-level assignments, source references, selected-criterion coverage, evidence links/local artifact existence, synthetic-evidence boundaries and decision rules.
- All 36 requested criteria and their starting levels are retained. Every criterion includes purpose/user impact, applicability/exclusion, expected behavior, concrete tests, test data/environment, evidence, pass/fail/unknown conditions, contextual severity, all four decisions, verification, prohibited overreach and source attribution.
- Status, severity and decision are independent fields. Severity is null when no failure has been assessed; a demonstrated failure must use blocker, important or improvement. This avoids assigning invented severity to a pass or an unknown.
- Feature gates use true/false/null and written rationales. Partial composite applicability requires per-surface evaluation, not wholesale exclusion. Deferred is selection metadata, not a fifth outcome status.
- Optional measured benefits are proposals; preference alone preserves behavior. Even a demonstrated violation becomes a proposal if scope/authority or proportionality needs a decision. Severity is unaffected.
- No individual ASVS requirement codes are invented. WCAG mappings use checked 2.2 IDs. Living guidance carries an access date rather than an invented version.
- The supplied `PROJECT_BRIFFF.md` is kept unchanged. It contains the detailed brief; there is no separate `PROJECT_BRIEF.md`.

## Review decisions before an application audit

These are app-specific inputs, not reasons to change or omit a requested criterion:

1. Confirm the actual app profile, audience, essential workflows, allowed test environments and inspection/change scope. The checked-in profile is deliberately hypothetical.
2. Agree persistence transitions, repeat-action rules, concurrency conflict semantics and interruption recovery contracts where applicable. Do not let an evaluator choose business semantics silently.
3. Agree supported devices, real-user task goals, representative participants, field-data adequacy, task/load budgets and operational objectives. No universal concurrency, participant count, uptime or data-loss target is imposed.
4. Confirm data classification, ownership of preservation copies and who may authorize secret rotation, hosting changes or new dependencies in an audited application.
5. Review the v1 conventions of nullable failure severity, any-feature selection and proposal-first treatment of optional measured benefits. They are project policy choices, not external standard requirements.

No requested criterion was replaced or removed. No redesign, database requirement, certification claim or production probing was introduced.

## Verification scope

Official WCAG 2.2 text and linked Understanding guidance were consulted for the used IDs, contrast thresholds/definitions, keyboard exception, focus minimum and notes, resize/reflow dimensions, and target-size exceptions. Google Web Vitals was checked for LCP/INP/CLS thresholds, p75 and field segmentation. OWASP's official site identifies ASVS 5.0.0; linked Authorization, Session Management, XSS Prevention and Threat Modeling Cheat Sheets were consulted as guidance. Exact ASVS control-by-control coverage is not claimed.

Automated validation checks structure and cross-references, not the authenticity of a screenshot, a participant, an external artifact or a reviewer-entered boolean. Unknown facts remain unknown. No real application, user research, production security, field CWV, capacity or restore procedure has been audited by creating this repository. The synthetic example is only an executable demonstration of report and decision contracts.

## Recorded checks (2026-10-28)

The implementation at `b2615dc` was exported with `git archive HEAD` into a temporary directory, installed into a new virtual environment from the pinned `requirements.txt`, and checked using Python 3.9.6. All 14 unit tests passed. Catalogue validation, the synthetic example report, template generation/validation at all three levels, criterion selection, and the nonzero CLI exit for an invalid report passed.

For the hypothetical profile, the cumulative planned scopes contain 19 Essential, 30 Standard and 36 Advanced criteria before feature exclusions. At Advanced, three criteria are not applicable and four have unresolved applicability. These counts describe the example profile only, not application results.

A deliberate inversion of the evidence-sufficiency branch in the decision function caused the test suite to fail. The original implementation was restored and verified in the clean archived checkout. This demonstrates that the tests detect that decision regression; it is not a claim of comprehensive mutation coverage.
