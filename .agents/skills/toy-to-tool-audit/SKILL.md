---
name: toy-to-tool-audit
description: Audit an existing application's important workflows using the Toy to Tool v1 criteria, collect linked evidence, and propose or verify scoped fixes. Use for application quality audits and turning audit findings into proportionate changes.
---

# Toy to Tool audit

Coordinate an evidence-based audit of an existing app through the six stages below. Use the user's language in conversation and English in saved artifacts. Preserve their product intent, existing work and authorization.

## Load the contract

For a group-specific audit, use its specialist if available, otherwise execute the selected canonical group protocols directly with explicit `--group` reporting. Retain the agreed level and authority; no other installed skill is required.

Use `references/engine` as engine root when bundled; otherwise use the repository root three directories above this skill directory. Resolve that root from this file, independently of the target app's working directory. Read [the evaluation method](../../../docs/method.md), validate [the catalogue](../../../criteria/v1.json), and load the full entries for selected criteria. The catalogue owns IDs, starting levels, exceptions, test protocols and decisions; do not copy or replace it with a new checklist. The skill requires the repository's `criteria/`, `schemas/`, `scripts/`, `docs/method.md` and Python dependencies. Copying this skill folder alone does not install the engine.

Run engine commands from that root with its documented Python environment. Run app commands from the app root. Store sanitized artifacts under a new `audits/<unique-run-id>/` in the target workspace; do not overwrite an earlier run. For separate installations validate local artifacts with `--evidence-root` set to that workspace; repository-local runs may use the engine root default. Reports may link authorized HTTPS artifacts instead. Local evidence locations in JSON are relative to the selected evidence root and must exist. Audit output is ignored by Git; do not publish evidence without the user's instruction.

If a required tool, runtime or account is absent, read [Missing access and tools](references/missing-access.md) and continue independent checks. Missing capability limits evidence; it does not make a criterion inapplicable.

## 1. Understand the important work

Inspect available briefs, README/setup instructions, app routes/data models, tests and deployment configuration before asking for facts. Do not read secret values. Record:

- The three most important user tasks: actor, starting state, action and actual successful outcome. Use fewer when the app genuinely has fewer tasks; do not invent a third feature.
- Intended users/roles and data types, sensitivity, ownership and required persistence transitions.
- Target runtime, supported devices, local/deployed differences and an authorized test environment.

Save a context artifact with the source of each fact: user requirement, file/line, observed configuration or explicit inference. Use it as requirement evidence for the relevant F/U/S/O criteria. Mark inferred tasks or undecided contracts as provisional; they cannot justify a pass against an invented goal.

Ask only when an unresolved answer changes applicability, expected behavior, impact, test access or change authority. Bundle related missing facts in a short plain-language question. For example: “Which three things must users be able to do, what data must survive reopening, and where do they use the app?” Ask only the parts not already established. Continue checks that do not depend on the answer. Unanswered business rules remain unknown.

## 2. Set the audit level and change authority

Reuse choices and permissions already established in the conversation. If unspecified, announce Essential and `read_only`: inspect, report and recommend changes without editing the target app. Creating audit artifacts is permitted by the audit request. Explain choices in ordinary language:

| Project level | Explain to the user |
| --- | --- |
| Essential | Check whether important tasks work and basic risks are controlled. |
| Standard | Also check everyday usability, accessibility and reliability. |
| Advanced | Also check defined concurrency, load and operational needs. |

`read_only` and `propose_only` do not authorize target-code changes. Use `fix_scoped` when the existing request authorizes concrete fixes, and record permitted files/behaviors, environment and excluded external actions. Do not ask again for permission already granted. Audit depth and modification authority are separate; these levels are not ASVS certification levels.

Do not ask a level question merely to obtain agreement with the default. Ask when the user needs a materially different scope or an important action lacks authorization. Explain what decision the answer changes. No response or elapsed time grants permission. Production changes, deployment, credential rotation and changes to business semantics require their own existing authorization; an audit request does not grant it.

## 3. Select applicable criteria

Create `profile.json` using [the profile schema](../../../schemas/profile.schema.json), not the hypothetical values in `examples/profile.json`. Set present features to true, demonstrated absence to false and unresolved features to null; include the supporting context/evidence IDs in each rationale. Inspect every feature once, without asking the user a separate question for each flag.

From the engine root, use the real run directory and selected level:

```sh
.venv/bin/python scripts/audit.py validate
.venv/bin/python scripts/audit.py select --profile audits/<run-id>/profile.json --level Essential
.venv/bin/python scripts/audit.py template --profile audits/<run-id>/profile.json --level Essential
```

Save selection output as `selection.json` and template output as `report.json` without overwriting existing files. Set the generated report's `change_permission` to the authority recorded in stage 2. Keep `report_kind: template` until observations are actually recorded; then use `audit`. Never use the synthetic example report as actual audit evidence.

All selected criteria need outcomes, including unknown and reasoned exclusions. Deferred higher-level criteria are unassessed, not passed or not applicable. Record an observed serious defect at any level, mark `observed_outside_level: true`, and correct contradictory profile facts before validating it. For composite criteria, evaluate each relevant surface separately as the method requires.

## 4. Collect evidence and assess

Prioritize the three important tasks and high-impact risks, then cover the remaining selected criteria. For each criterion, use its concrete test steps, data/environment, required evidence and pass/fail/unknown rules. Record reproducible steps, revision/build, environment/tool versions, expected/actual result and observation time. Link every conclusion to both its criterion ID and the evidence record/artifact. A claim spanning several criteria needs support for each.

Use the existing report schema: status is `pass`, `fail`, `unknown` or `not_applicable`; severity is `blocker`, `important` or `improvement` for a demonstrated failure and null otherwise; decision is independent. A test that did not run is never pass. A failed test attempt caused by missing infrastructure is not automatically an app failure. Record collection attempts and access gaps as evidence of limitations, not evidence of correct app behavior. Unknown rows still link the context or attempt artifact explaining the gap. Not-applicable rows link evidence supporting feature absence.

Source inspection and unit tests support only what they establish. Do not use them as substitutes for browser behavior, real users, field performance or restore execution. Redact secrets and personal data before saving evidence. Real audits cannot use synthetic observations as assurance.

## 5. Propose or perform proportionate fixes

Apply the decision procedure in the evaluation method and `scripts.audit.decide`:

- Missing sufficient evidence or an expected contract: investigate.
- Demonstrated requirement/risk violation with an authorized, proportionate correction: fix.
- Demonstrated violation needing a scope/authority/cost decision, or an optional measurable benefit: propose.
- Current behavior meets the need, or the suggestion is preference without demonstrated benefit: preserve.

For every fix/proposal record the requirement or goal, linked evidence, affected users/conditions, expected measurable benefit, scope/cost/risk and verification plan. Include preserve decisions when they prevent unnecessary redesign or infrastructure. Severity never decreases because the agent lacks permission: a blocker outside scope remains a blocker with a proposal.

When authorized, make the smallest supported correction and follow the target repository's applicable instructions. Stop dependent changes if a conflict rule, data-loss choice, new external service or other consequential product decision is missing; continue independent work. Do not redesign or add features just to raise audit coverage.

## 6. Verify and hand over

Save the observed baseline report/evidence before changing the app. Rerun the affected criterion's verification steps and relevant regression checks. Capture post-change results separately and link both revisions. If a demonstrated failure was patched but not rechecked, keep the current outcome fail with its original severity and explicitly say “change made; verification pending.” If the original behavior was never observed, retain unknown. Writing a patch is not a pass.

When rechecks actually pass, update the final report to the supported current outcome, link baseline and recheck evidence, and keep the earlier report as history. A now-passing row uses null severity and an appropriate current decision; the human report records the performed fix and original severity. Do not leave baseline failures mixed into current-outcome rows and then claim the aggregate passes.

Create `report.md` from [the English handover template](assets/report.md), alongside the schema-compatible `report.json`, context/profile, selection and evidence. Every factual result, recommendation, preserve decision and coverage limitation in the handover must cite criterion and evidence IDs with resolvable links. The Markdown is a human view of the JSON, not a second source of outcomes.

```sh
.venv/bin/python scripts/audit.py validate --report audits/<run-id>/report.json
```

Report validation failures honestly; do not lower the schema or delete unknown rows to get a clean result. If the engine cannot run, record that validation is unexecuted. Manually review evidence sufficiency, source exceptions and consistency between JSON and Markdown even when validation passes.

Lead the handover with unresolved blockers, followed by important failures, verified changes, proposals/preserve decisions, unknowns and exclusions/deferred work. Use separate status counts only when helpful; never an overall score or a completion percentage that conceals a blocker. State what was verified, what remains untested, the exact missing resource/decision and the next useful action. Do not claim general security, WCAG AA or ASVS certification from this audit.

For separate installations, save artifacts in the target workspace and validate with `--evidence-root` set to that absolute workspace. Install the engine requirements into the chosen Python environment; do not require write access to the installed skill.
