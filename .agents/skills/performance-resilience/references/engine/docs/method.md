# Evaluation method v1

This project defines 36 evaluation criteria across Functionality & Data (F), UX & Visual Quality (U), Accessibility (A), Security & Privacy (S), Performance & Resilience (P), and Deployment & Operations (O). Each group has six stable IDs. The catalogue is `criteria/v1.json`; its source registry supplies titles, versions and URLs. All method, selection, evidence, severity and decision rules below are project-defined unless explicitly attributed to a source.

The supplied detailed brief was present in the working workspace as `PROJECT_BRIFFF.md` (a user-provided, untracked input). `PROJECT_BRIEF.md` was not present. The user-provided file is preserved as received; no application code or previous project conventions were available at implementation time.

## Scope and levels

Essential checks essential outcomes and basic risks, favoring minimal changes. Standard includes Essential and everyday usability/quality. Advanced includes Standard and additional evaluation based on defined load, complexity and operational needs. Levels determine the planned inspection depth, not permission to modify code. They are independent of ASVS assurance levels and convey no ASVS certification.

1. Record the agreed audience, essential tasks, requirements, supported devices, environment and allowed inspection/modification scope. Use only authorized environments and test data for security and load probes.
2. Create a profile using `schemas/profile.schema.json`. Every feature is true (present), false (demonstrably absent) or null (not established), with a rationale. Feature names are facts about architecture, not desired additions. For example, `persistent_data` is true when retention across some transition is required; `important_data` is true when difficult-to-replace user/business data exists.
3. Select criteria at the chosen level. An empty feature list means an unconditional core assessment. Otherwise any true feature selects the criterion; all false means not applicable with reasons; no true and at least one null requires investigation. Higher-level criteria are deferred, which is not an assessment status and never means not applicable. Report serious observed defects at any level, explicitly marking out-of-level observations.
4. For each selected criterion, establish its expected contract, then execute its specific steps with the listed data/environment. Retain the required evidence and record the limits of the sample. Missing requirements, access, tooling, observations or representative users mean unknown rather than pass.
5. Assign status and, for a demonstrated failure, contextual severity. Evaluate modification authority separately using the decision procedure below. Complete the affected-users, benefit verification and scope/cost/risk fields before proposing a change.
6. After an authorized change, execute the criterion's verification steps under the original conditions and check relevant neighboring behavior. Keep before/after evidence; do not mark pass merely because a patch was written.

Composite criteria need subcase records within evidence: S05 classifies CSRF, CORS, uploads, public endpoints and abuse independently. O05 distinguishes restore from release rollback. An applicable failed subcase makes the criterion fail; absent subcases need reasons. If no subcase fails but a relevant subcase is untested, the result is unknown. A partly applicable criterion cannot be marked not applicable as a whole. The profile gates planning; it does not replace architecture review or subcase evidence.

## Focused group audits

For an agreed group-only audit, use `--group F` (or repeat `--group` for several groups) with `select` and `template`. The report records `criterion_groups`; omitted means all six groups for backwards compatibility. Coverage validation still requires every selected in-scope criterion, including unknowns and exclusions. Other groups have no assessed result. Do not narrow scope after observing a failure merely to make a report pass. A focused Functionality & Data report is not an overall application audit.

## Status, severity and decision

Status is `pass`, `fail`, `unknown` or `not_applicable`. Pass needs sufficient evidence for the declared scope. Fail needs evidence of an agreed requirement/goal violation or a demonstrated risk under the criterion contract. Unknown is missing evidence/expectation; it is never counted as pass. Not applicable requires demonstrated feature absence and a written reason. Do not use a numeric total to hide failures or merge unknown with success. Summarize failures by severity and list unknown, excluded and deferred criteria separately.

Severity is `blocker`, `important` or `improvement` for a failure. The JSON report uses null when no failure severity has been assessed. A blocker prevents an essential outcome or creates serious security, loss or operational impact; important means a material violation with bounded impact/workaround; improvement is a minor evidenced violation. Assess affected users, reachability, data sensitivity, reversibility, frequency and workarounds using the criterion guidance. A blocker remains a blocker when permission to fix is absent. An optional improvement without a failure may be proposed with null failure severity.

The executable decision procedure takes five independent booleans. `evidence_sufficient` means sufficient for this particular conclusion, not evidence of a problem by default. `violates_requirement` includes demonstrated unacceptable risk under an agreed criterion contract. `measurable_benefit` needs an identified outcome and measurement plan. `authorized` is true only for a concrete correction within the audit's `fix_scoped` permission and agreed scope. `proportional` considers change size, cost and regression risk relative to the benefit.

| Priority | Condition | Decision |
| --- | --- | --- |
| 1 | Evidence or expected behavior is insufficient | investigate |
| 2 | Demonstrated violation, authorized correction and proportionate scope | fix |
| 3 | Demonstrated violation but authority or proportionality needs a decision | propose |
| 4 | Measurable benefit without a demonstrated violation | propose |
| 5 | Current behavior satisfies needs, or suggestion is preference without demonstrated benefit | preserve |

Every proposed/fix change must answer: what agreed requirement or goal is affected; what evidence establishes the problem; who is affected and when; what post-change measurement proves benefit; and whether scope, cost and risk are proportionate. A proposal for a failure is still an unresolved failure. Insufficient information about proportionality/authority must never be assumed to grant permission. Record a proposal or investigate the missing facts.

## Evidence and report contract

Use `scripts/audit.py template` to create an unexecuted JSON report. Every selected ID needs at least one outcome; several findings may reference the same criterion. For a criterion summary, any fail wins; otherwise any unknown wins; otherwise pass requires every applicable subcase to pass. Not applicable is allowed only when every relevant feature is established absent. Preserve the underlying rows. The catalogue is a test protocol, not evidence that a particular app passed.

Evidence records contain an ID, durable artifact location, description, environment, timestamp, type and synthetic flag. Capture exact steps, build/revision, tool versions, test values, expected/actual results and limitations in artifacts. Keep credentials and personal data out of shared evidence. Reference stable files, sanitized traces, measurements or participant notes, not merely an assertion that an agent checked something. Evidence IDs must resolve within the report. Artifact locations can be files relative to the explicitly selected evidence root or authorized HTTPS URLs. The default evidence root is the engine repository; separately installed skills pass `--evidence-root <absolute-target-workspace>` to validate artifacts outside the installed skill. The validator checks local file existence and linkage; it does not fetch remote artifacts or establish authenticity.

A template has unknown rows and justified profile exclusions; replace instructional field text before an actual audit. `examples/report.json` and its evidence are entirely synthetic and demonstrate format and decisions only. Reports declare `report_kind` as `template`, `synthetic` or `audit`. Validation rejects pass/fail claims in an unexecuted template and synthetic evidence in an audit. A downstream skill must also inspect artifact contents and reject synthetic evidence as real assurance. Human/skill review must assess evidence sufficiency, exceptions, feature rationale and the stated cost/risk; schema validation cannot establish those facts.

## Execution and evidence depth (report format 1.1)

`template` now emits `report_format: "1.1"`. Keep the catalogue and its stable IDs as the protocol. `tasks` records actual important tasks and criterion-specific subcases, not a competing checklist. Each task records actor, starting state, expected outcome and context/requirement `evidence_ids`. Its ordered steps record action, expected/actual result, `criterion_ids`, `depends_on`, `execution`, `status`, `required_modes` and result/attempt `evidence_ids`. Step IDs are unique across tasks; dependencies refer to earlier steps. Add all necessary subcases before claiming their criterion passes. Use separate steps for checks that can stop independently.

Execution is `completed`, `interrupted` or `not_run`; result is `pass`, `fail` or `unknown`. An app assertion that ran and demonstrated a violation is a completed failing step. Infrastructure failure is an interrupted attempt with unknown result. Steps after the interruption or an unmet prerequisite remain not_run/unknown, without result evidence. Separate independent checks may still execute. Partial artifacts support only assertions actually reached. Never infer later checks from the runner's overall status.

Findings link `step_ids`. In 1.1, a pass requires every declared step for that criterion to be linked, completed and passed, with all step evidence included in finding evidence. This deliberately prevents omitting an unfinished subcase from a pass row. Use criterion rows that summarize all its subcases; retain subcase detail in tasks. Fail requires at least one completed failing step; unexecuted neighboring checks do not hide a demonstrated failure. A human must still assess whether the declared steps cover the whole claimed scope and whether artifacts prove their asserted results. A validated ledger does not prove its own completeness or authenticity.

Evidence retains its existing `kind`, `description`, `environment`, `captured_at` and location. Add `modes` describing what it actually establishes: `source_inspection`, `page_load`, `interaction`, `independent_confirmation`. A step's `required_modes` is an explicit criterion-specific requirement, not an evidence score. The engine checks that linked modes cover this requirement, not whether the requirement was chosen correctly. There is no ranking: source review can prove a source contract, while browser interaction does not automatically prove persistence, authorization or field performance. Independent confirmation checks the promised outcome separately, such as committed values after reopen. HTTP 200/title proves loading only, never completion of a task requiring interaction/readback. Record limitations in evidence descriptions, actual results and finding reasons.

`coverage_cases` lists unique `(url, page_type, language, viewport)` combinations linked to the actual steps for each case. Counts distinguish declared combinations, completed combinations (all linked steps executed to completion), verified combinations (all passed), and distinct URL strings; no URL normalization is inferred. A completed failing case is not a verified case. Do not reuse steps across cases unless the same observation genuinely covers them. Three page types × three languages × four viewports gives 36 combinations, corresponding to nine distinct URLs when each type/language has one URL. Do not describe these as 36 distinct pages. Evidence is still needed for the claimed sample and each environment/state.

Keep triggering configuration, environment and affected roles together in existing `affected_users_and_conditions`, beside each finding. A default-off feature does not automatically lower the severity of a demonstrated violation; record exposure/rollout and fix ordering separately in `remediation_priority` (plain language, no score). Failure rows sharing a demonstrated cause use the same `root_cause_id` even across criteria. Count criterion outcomes, finding rows and distinct root causes separately; a shared cause does not erase criterion-specific evidence requirements. Root-cause counts are unknown (`null`) if any failure lacks a cause ID in a legacy report.

## Generated handover and review

`report.json` owns all results. `created_at` and `updated_at` are report metadata, separate from evidence observation time `captured_at`. Set report times when creating/changing results; rendering and translation preserve them. Never replace an observation time with the rendering time.

```sh
.venv/bin/python scripts/audit.py render --report audits/<run-id>/report.json
.venv/bin/python scripts/audit.py review --report audits/<run-id>/report.json
```

Use `--evidence-root <absolute-workspace>` for external artifacts and optional `--markdown <path>` for another view (including a translated narrative). Local artifact links are resolved relative to that Markdown file. Render validates JSON first, then updates only the delimited generated region; it preserves narrative outside it. All structured fields, outcomes, severities, decisions, counts, IDs, paths and timestamps come from JSON. The region includes a SHA-256 of canonical JSON; review also compares its exact rendered content, detecting both stale JSON and manual changes to generated facts. It does not trust a copied hash alone. An existing unmarked Markdown is rejected: choose a new view path for migration, retaining the old report. The narrative template is guidance, not a second result store.

Translations keep the canonical generated region and translate narrative outside it. Do not edit statuses, IDs, paths or observation/report times or create a new audit run merely for translation. Human review must catch narrative contradicting generated facts; the engine cannot determine semantic equivalence across languages.

Before handover, run engine review on existing artifacts and manually inspect evidence for passes missing required support, stopped tests, omitted subcases, overbroad claims, wrong counting units, and inconsistent narrative/translations. Engine checks schemas, dependencies, links, declared mode coverage, result rules, units/count derivation and Markdown equality; it does not establish evidence sufficiency. For a read/review-only request, do not start the app, invoke an application/system-test runner, or fetch remote evidence. Engine review is local/read-only and never does those actions. Missing evidence means unknown with the precise remaining check in `verification_plan`; do not rerun a whole system to complete a report. A previously demonstrated failure retains its severity until a verified correction, as above.

## Compatibility and migration

Report format is independent of `catalog_version`, which remains 1.0.0. An omitted `report_format` or explicit `"1.0"` uses the original validation contract; no historical report is rewritten. `review` identifies legacy coverage as unenforced and still requires manual evidence review. Legacy validation passing is not new assurance. Existing Python callers may explicitly request `template(..., report_format='1.0')` while retaining their existing collection semantics; the historical fixture evaluation builders do so and are not rerun by this change. New audits use 1.1. Never switch a new audit back to legacy to bypass missing evidence.

To migrate an active report, retain its baseline, set format 1.1 in a new report, add report timestamps and reconstruct tasks/steps only from actual recorded artifacts. Add step links, case records, and cause/priority fields where supported. Unestablished subcases stay unknown; do not invent observations or downgrade demonstrated failures. An empty tasks/cases array conveys no coverage and cannot support a pass. Do not migrate historical evidence bundles just to satisfy the new schema. `examples/report-steps.json` is explicitly synthetic format documentation, not application assurance.

## Source interpretation

WCAG references use the pinned 2.2 Recommendation dated 2024-12-12. Requirement IDs in A01-A06 were cross-checked against that document. Linked Understanding pages provide explanatory guidance, not additional normative obligations. The six sampled criteria do not establish WCAG AA conformance; neither does an automated scan. Source exceptions and definitions must be applied to the actual content.

OWASP ASVS is referenced at 5.0.0 as security verification context. No numbered ASVS control mapping is claimed; that would require checking each exact requirement against implementation scope. OWASP Cheat Sheets are living guidance, identified by access date rather than an invented release. F, U, O and the non-CWV P rules are project-defined practical evaluation contracts. External guidance does not require adding a database, authentication, telemetry stack or an unrelated feature.

P03 distinguishes field CWV evidence from local diagnostics. Task-specific budgets, field sample adequacy and operating targets must be agreed for the app before judging them; this project does not invent a universal load, uptime or sample-count threshold.
