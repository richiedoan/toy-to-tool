# Application audit handover

Replace the fields below with observed facts and remove instructional rows. Keep this report in English. Use criterion and linked evidence IDs for every finding, recommendation, preserve decision and limitation. Maintain the same current outcomes as `report.json`. This file is a template and establishes no application result.

## Audit context

| Item | Recorded value | Criterion and evidence |
| --- | --- | --- |
| Application, revision and audit date | {{app_revision_date}} | F01 / [{{context_evidence_id}}]({{context_artifact}}) |
| Users, roles and data/persistence needs | {{users_roles_data}} | {{relevant_criterion_ids}} / [{{context_evidence_id}}]({{context_artifact}}) |
| Runtime, test environment and supported devices | {{environment_and_devices}} | U03, O01, O02 where applicable / [{{environment_evidence_id}}]({{environment_artifact}}) |
| Level and granted modification scope | {{level_permission_scope_and_source}} | {{affected_criterion_ids}} / [{{scope_evidence_id}}]({{scope_artifact}}) |
| Report/selection/profile | [report.json](report.json), [selection.json](selection.json), [profile.json](profile.json) | {{context_evidence_links}} |

## Three priority tasks

Record actual successful outcomes, not just changed screens. If fewer than three tasks exist, explain the supported scope. Mark any inferred task or undecided outcome as provisional.

| Task and actor | Successful result and retention boundaries | Criterion IDs | Requirement/context evidence | Executed result evidence or gap |
| --- | --- | --- | --- | --- |
| {{task_1}} | {{expected_actual_outcome}} | {{criterion_ids}} | [{{requirement_id}}]({{requirement_artifact}}) | [{{result_or_gap_id}}]({{result_or_gap_artifact}}) |

## Unresolved blockers

List every unresolved blocker before other findings. If none was demonstrated, say “No blocker was demonstrated in the checks performed” and link the relevant assessed scope and unknowns. Do not imply unknown checks are free of blockers.

| Finding | Criterion | User impact and conditions | Current status | Decision and authority limitation | Evidence |
| --- | --- | --- | --- | --- | --- |
| {{finding_id}} | {{criterion_id}} | {{affected_users_conditions}} | {{status}} | {{decision_and_scope}} | [{{evidence_id}}]({{artifact}}) |

## Important failures and improvements

Keep status, severity and decision separate. Include failures outside the planned level and identify them as observed outside scope. A proposal leaves the failure unresolved.

| Finding | Criterion | Status | Severity | Decision | Requirement, actual result and impact | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {{finding_id}} | {{criterion_id}} | {{status}} | {{severity_or_null}} | {{decision}} | {{expected_actual_impact}} | [{{evidence_id}}]({{artifact}}) |

## Changes and verification

Keep baseline results as history, separate from the current outcome. A change without a recheck remains “verification pending”; retain the original demonstrated failure and severity. A current pass requires sufficient post-change evidence.

| Change/finding | Criterion | Baseline status/severity and evidence | Scope and change made | Recheck command/task and conditions | Post-change evidence | Current outcome |
| --- | --- | --- | --- | --- | --- | --- |
| {{change_id}} | {{criterion_id}} | {{baseline_status_severity}} / [{{before_id}}]({{before_artifact}}) | {{authorized_scope_and_change}} | {{recheck_steps_environment}} | [{{after_or_gap_id}}]({{after_or_gap_artifact}}) | {{current_status_or_verification_pending}} |

## Proposals and preserve decisions

For a proposal, explain the measurable benefit and why the decision is needed. For preserve, explain the fulfilled requirement or why a preference lacks demonstrated benefit. Never treat an unrelated redesign as a required fix.

| Finding | Criterion | Decision | Requirement/goal, users and conditions | Evidence | Benefit verification | Scope, cost and risk; decision needed |
| --- | --- | --- | --- | --- | --- | --- |
| {{finding_id}} | {{criterion_id}} | {{propose_or_preserve}} | {{requirement_and_impact}} | [{{evidence_id}}]({{artifact}}) | {{measurement_or_no_supported_benefit}} | {{scope_cost_risk_and_owner_question}} |

## Unknowns and execution limits

A selected check that did not run is unknown. Link the real collection attempt/context evidence, which supports the limitation rather than correct app behavior. Distinguish missing tools/access from an observed app defect.

| Criterion/finding | Completed subcases | Unexecuted check and reason | Limitation evidence | Exact missing resource/decision | Next useful action |
| --- | --- | --- | --- | --- | --- |
| {{criterion_id_and_finding_id}} | {{covered_scope}} | {{unknown_check_and_reason}} | [{{attempt_or_context_id}}]({{artifact}}) | {{missing_browser_runtime_account_or_contract}} | {{next_action}} |

## Coverage and exclusions

Use separate lists/counts for pass, fail, unknown, not applicable and deferred criteria. Count distinct criteria using the evaluation method's aggregation rule; do not count multiple findings as additional criteria. Link the detailed current rows and evidence for every result. There is no overall quality score or weighted average.

| Criterion | Current status or deferred selection | Reason, scope and exceptions | Evidence |
| --- | --- | --- | --- |
| {{criterion_id}} | {{status_or_deferred}} | {{scope_or_reason_for_exclusion_or_deferral}} | [{{context_or_result_id}}]({{artifact}}) |

## Evidence register

Match the JSON evidence IDs. Use sanitized durable artifacts and real observation times. Disclose historical build/environment mismatches. Synthetic demonstrations do not support a real audit.

| Evidence ID | Criterion IDs | Artifact | Type, build/environment and capture time | Supports; limitations |
| --- | --- | --- | --- | --- |
| {{evidence_id}} | {{criterion_ids}} | [{{artifact_label}}]({{artifact}}) | {{type_environment_time}} | {{supported_claim_and_limits}} |

## Validation and next actions

- Validation command, exit result and captured output: {{command_result}} / [{{validation_evidence_id}}]({{validation_artifact}}).
- JSON/Markdown consistency and evidence/exception review: {{review_scope}} / {{criterion_ids}} / [{{review_evidence_id}}]({{review_artifact}}).
- Remaining user decisions and owners: {{only_decision_affecting_questions}} / {{criterion_ids}} / {{evidence_links}}.
- Next verification or action: {{concrete_next_action}} / {{criterion_ids}} / {{evidence_links}}.

State exactly what was verified and what remains untested. Validation passing checks the report contract; it does not prove the app meets the criteria. This audit makes no general WCAG AA, ASVS certification or system-security claim.
