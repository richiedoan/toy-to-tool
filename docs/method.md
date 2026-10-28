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

Evidence records contain an ID, durable artifact location, description, environment, timestamp, type and synthetic flag. Capture exact steps, build/revision, tool versions, test values, expected/actual results and limitations in artifacts. Keep credentials and personal data out of shared evidence. Reference stable files, sanitized traces, measurements or participant notes, not merely an assertion that an agent checked something. Evidence IDs must resolve within the report. Artifact locations can be repository-relative files or authorized HTTPS URLs. The validator checks local file existence and linkage; it does not fetch remote artifacts or establish authenticity.

A template has unknown rows and justified profile exclusions; replace instructional field text before an actual audit. `examples/report.json` and its evidence are entirely synthetic and demonstrate format and decisions only. Reports declare `report_kind` as `template`, `synthetic` or `audit`. Validation rejects pass/fail claims in an unexecuted template and synthetic evidence in an audit. A downstream skill must also inspect artifact contents and reject synthetic evidence as real assurance. Human/skill review must assess evidence sufficiency, exceptions, feature rationale and the stated cost/risk; schema validation cannot establish those facts.

## Source interpretation

WCAG references use the pinned 2.2 Recommendation dated 2024-12-12. Requirement IDs in A01-A06 were cross-checked against that document. Linked Understanding pages provide explanatory guidance, not additional normative obligations. The six sampled criteria do not establish WCAG AA conformance; neither does an automated scan. Source exceptions and definitions must be applied to the actual content.

OWASP ASVS is referenced at 5.0.0 as security verification context. No numbered ASVS control mapping is claimed; that would require checking each exact requirement against implementation scope. OWASP Cheat Sheets are living guidance, identified by access date rather than an invented release. F, U, O and the non-CWV P rules are project-defined practical evaluation contracts. External guidance does not require adding a database, authentication, telemetry stack or an unrelated feature.

P03 distinguishes field CWV evidence from local diagnostics. Task-specific budgets, field sample adequacy and operating targets must be agreed for the app before judging them; this project does not invent a universal load, uptime or sample-count threshold.
