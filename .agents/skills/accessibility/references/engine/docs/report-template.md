# Application audit handover narrative

Generate the structured results from `report.json` first with engine `render`.
This template guides only agent-written text outside the generated region; it is
not a second set of status/severity/decision tables. Keep the generated facts
unchanged, including in translations. Never copy these prompts as audit evidence.

## Context and important tasks

Explain the agreed users, successful outcomes, persistence boundaries, revision,
environment and authority, citing criterion and evidence IDs from JSON. Distinguish
requirements from inferences. Refer to the generated task/step records for what
actually ran, stopped or remains unexecuted.

## Impact and next actions

Lead with unresolved blockers, then other demonstrated failures. For each, refer
to its finding/criterion IDs and linked evidence; explain triggers, environment,
affected users, workarounds and exposure. Keep severity distinct from fix order.
A default-off flag affects exposure, not automatically severity. Several criterion
rows sharing one root cause are not independent defects.

Explain verified changes, proposals and preserve decisions with supporting links.
Keep baseline history separate from current results. A patch without verification
retains its demonstrated failure/severity and says verification pending.

## Evidence limits and review

State the precise missing checks/resources and next useful actions from JSON.
HTTP 200/title proves loading only. Do not extrapolate source review, one viewport,
or an interrupted test to a whole workflow. Report combinations and distinct URLs
as separate units. Manual review assesses artifact contents, omitted subcases,
scope and translation consistency; engine `review` checks declared structure and
JSON/Markdown freshness without starting the app or rerunning system tests.

Link validation/review output if retained. Say when validation was unexecuted.
This audit gives no overall score, WCAG AA/ASVS certification or general security
assurance. Translations preserve evidence IDs, paths, results and times and are
not a new audit observation.
