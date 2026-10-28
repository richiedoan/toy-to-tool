# Synthetic evidence fixture

All entries are fictional examples, recorded on 2026-10-28 for validator and decision demonstrations. No real app, users, backup, database or performance was tested.

| Criterion | Fictional expected/actual observation | Decision rationale |
| --- | --- | --- |
| F01 | Create DEMO-1 should commit one record. UI says saved; independent read returns zero records. | Failure blocks the core outcome. Existing save-handler correction is explicitly within the hypothetical scoped permission, so fix. |
| F02 | DEMO-2 remains byte-for-byte equal after refresh and full reopen on the same device. Retention contract excludes cross-device sync. | Pass for the fictional retention scope. A database/cloud migration has no demonstrated benefit, so preserve. |
| U05 | Both example screens use the same save label, component and state behavior. No observed task error is attributed to color. | A different color is aesthetic preference, so preserve. |
| O03 | The hypothetical owner requires daily backups. Only an unscheduled manual export exists. | Important failure; a new storage service needs cost/access decisions, so propose. This does not resolve the failure. |
| U04 | Fictional correction takes 8 seconds against a predeclared 15-second task goal. An undo prototype takes 4 seconds in the same fictional task. | Existing flow passes. A measurable optional benefit warrants a proposal; adding undo requires a product decision. |

All other selected outcomes remain unknown or are excluded using the explicitly hypothetical profile. A real audit must replace these rows with reproducible task steps, build/environment, test records, authentic traces, measured distributions or real-participant observations as required by each criterion. These entries establish no real-world pass/fail claim.
