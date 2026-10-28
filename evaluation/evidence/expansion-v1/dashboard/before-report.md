# dashboard: before report

Evaluator-led real HTTP/Chrome checks on an isolated seeded fixture. Scope is limited to recorded cases; source/handler-only independent agent findings are archived separately. No skill-effectiveness, full WCAG, field CWV or ASVS certification claim. See E-context and E-preservation.

[Schema-validated JSON](before-report.json) | [Context](context.md) | [Preservation evidence](preservation.json)

| Criterion | Status | Severity | Decision | Evidence and reason |
| --- | --- | --- | --- | --- |
| A04 | fail | blocker | fix | Demonstrated assertion failure in: layout-320 [Evidence](before/results.json), [scope](context.md) |
| U03 | fail | blocker | fix | Demonstrated assertion failure in: layout-320, layout-390, layout-768 [Evidence](before/results.json), [scope](context.md) |
| P02 | fail | important | fix | Demonstrated assertion failure in: error-recovery [Evidence](before/results.json), [scope](context.md) |
| P03 | fail | important | fix | Demonstrated assertion failure in: local-filter-budget [Evidence](before/results.json), [scope](context.md) |
| U02 | fail | important | fix | Demonstrated assertion failure in: error-recovery [Evidence](before/results.json), [scope](context.md) |
| A01 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| A02 | unknown | null | investigate | Native name/label positive controls passed, but actual assistive-technology behavior was not exercised. [Evidence](before/results.json), [scope](context.md) |
| A03 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| A05 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| A06 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| O01 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| O02 | not_applicable | null | preserve | All relevant features are absent: deployed: E-context: absent from the explicitly local, replaceable-data architecture/contract. [Evidence](before/results.json), [scope](context.md) |
| O03 | not_applicable | null | preserve | All relevant features are absent: important_data: E-context: absent from the explicitly local, replaceable-data architecture/contract. [Evidence](before/results.json), [scope](context.md) |
| O04 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| O05 | not_applicable | null | preserve | All relevant features are absent: persistent_data: E-context: absent from the explicitly local, replaceable-data architecture/contract.; deployed: E-context: absent from the explicitly local, replaceable-data architecture/contract. [Evidence](before/results.json), [scope](context.md) |
| P01 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| P04 | unknown | null | investigate | Bounded repeated-request controls ran; full timer/subscription/teardown resource lifecycle evidence is missing. [Evidence](before/results.json), [scope](context.md) |
| U01 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. This is expert task-alignment review, not real-user understanding evidence. [Evidence](before/results.json), [scope](context.md) |
| U04 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |
| U05 | pass | null | preserve | All listed applicable cases passed; conclusion limited to these tasks/states. [Evidence](before/results.json), [scope](context.md) |

Deferred higher-level IDs are listed in the selection JSON; other groups have no assessed outcome. Unknown is never pass. No overall quality score.

Original failing reproductions that now succeed are retained in the before evidence. Some broader criteria remain unknown despite verified corrections because their remaining protocols were not executed.
