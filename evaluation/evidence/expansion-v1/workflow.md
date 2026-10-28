# Five-group expansion: Inspect → Improve → Recheck

## What ran and what it establishes

Five specialists now cover UX & Visual Quality, Accessibility, Security & Privacy, Performance & Resilience, and Deployment & Operations. They reuse the unchanged 36-criterion catalogue and the existing report schema. The Functionality & Data specialist and coordinator are also exportable as self-contained bundles. No per-skill scanner or aggregate quality score was introduced.

Two fresh CLI threads received allowlisted original fixtures and independently packaged skills. They did not receive evaluator expectations, hidden HTTP/Chrome tests, previous reports, reference fixes or this authoring conversation. Their exact installed instructions (checksummed `input-skills.zip`), invocation rules and events are retained under each fixture's `independent-agent/` directory. This is context/input separation, not an OS read-isolation guarantee. Both sandboxes limited sockets/browser execution; agent source/handler rechecks are separate from the actual evaluator HTTP/Chrome runs. There is no controlled skill/no-skill comparison, efficacy gain claim, general security guarantee or WCAG/ASVS certification.

## Owner notes

- Original runnable baseline: [owner-notes-v2 archive](../../baselines/owner-notes-v2.tar.gz) and [manifest](../../baselines/owner-notes-v2.manifest.json). Source hashes in accepted before evidence match this archive.
- [Before report](owner-notes/before-report.md): S02 fails direct cross-owner read and mutation. B's independent readback exposes the unauthorized change; the already-owner-filtered list is a positive control, not authorization evidence for object routes.
- Independent correction: [two SQL predicate edits](owner-notes/independent-agent/applied.patch) bind the authenticated owner on GET and PATCH. No evaluator app correction was applied after that independent patch.
- [After report](owner-notes/after-report.md): both forbidden operations are rejected; owner operations, anonymous denial, safe text handling, logout/replay, actual expiry and UI smoke controls succeed. All seven recorded HTTP/browser scenario assertions pass. S01/S05 remain unknown for their incomplete coverage; source and lifecycle conclusions remain bounded to the tested local model.
- [Preservation evidence](owner-notes/preservation.json): README, HTML, JS and CSS hashes are unchanged, and the approved login PNG is byte-identical. Parameterized queries, native controls, owner-filtered listing and local SQLite/session architecture remain. No unrelated auth rewrite, framework or UI change occurred.

See [raw before](owner-notes/before/results.json), [raw after](owner-notes/after/results.json), [context](owner-notes/context.md), [agent events](owner-notes/independent-agent/events.jsonl) and the archived agent reports. Evaluator JSON omits cookie/session values. Archived Playwright traces have authentication/cookie header fields redacted by the evaluator utility; statuses, payloads, screenshots and observed results are retained. [Redaction record](trace-redaction.json) logs the removed fields. Original unsanitized scratch traces were not versioned. All data is disposable.

## Dashboard

- Original baseline: [dashboard-v1 archive](../../baselines/dashboard-v1.tar.gz) and [manifest](../../baselines/dashboard-v1.manifest.json).
- [Before report](dashboard/before-report.md): U03/A04 expose essential-task obstruction at 320/390/768 CSS pixels; U02/P02 expose blank failed-refresh feedback and lost displayed prior data; P03 exposes the predeclared local task-budget violation. The same core issue may support several criteria; assertion counts are not independent defect counts.
- Independent correction: [targeted JS/CSS patch](dashboard/independent-agent/applied.patch) constrains the shell, wraps the narrow header/cards, retains last data with actionable failure feedback, and removes the 320ms synchronous wait. No evaluator app correction was applied after the independent patch.
- [After report](dashboard/after-report.md): all fourteen recorded Chrome/HTTP scenario assertions pass, including all four target widths, error/retry/loading/empty correction, filtering correctness, keyboard/focus/target controls, measured normal-theme contrast, bounded request cycles, clean startup and correlated operator diagnostics. Local p95 is 17.1ms against a predeclared <=100ms budget, versus 320.9ms before; raw five-sample distributions and conditions are in [before](dashboard/before/results.json) and [after](dashboard/after/results.json).
- P03 remains unknown for full field CWV: local success is not p75 field LCP/INP/CLS evidence. A02, complete A04, P02 offline/timeout and P04 full resource lifecycle also retain their named coverage gaps. Previously failing specific reproductions were rechecked successfully; broader unexecuted checks are not counted as pass. U01 is expert task-alignment review, not real-user understanding research. Advanced work is deferred; O02/O03/O05 have reasoned exclusions for this undeployed, replaceable-data fixture.
- [Preservation evidence](dashboard/preservation.json): README/HTML/server hashes are unchanged; the approved 1440px successful desktop PNG is byte-identical. Metric values, native controls, labels, design tokens, normal-theme contrast, empty-filter correction and already-useful redacted logs remain. Mobile layout changes are scoped corrections; no desktop redesign or architecture migration occurred.

See [context](dashboard/context.md), [agent events](dashboard/independent-agent/events.jsonl), raw traces/screenshots and archived agent reports. Local timing is subject to the recorded hardware/browser/run conditions and does not generalize to real users or production load.

## Calibration and workflow corrections

1. The first owner fixture could not start because host Python lacked `hashlib.scrypt`. The actual [infrastructure result](calibration/owner-v1-infrastructure.json) and v1 archive are retained. That attempt was interrupted, not scored as an ownership test. The author corrected the runtime compatibility using available PBKDF2 before freezing runnable v2 and starting a new independent thread with no prior answers. Both ownership defects remained for discovery.
2. Initial packets relocated app folders relative to unchanged README commands. The dashboard agent correctly recorded that mismatch without editing protected requirements. This is an exporter artifact, not a source-app O01 failure. The exporter now preserves `fixtures/<name>/`; tests verify source hashes, neutral contents and layout. Accepted evaluator O01 evidence uses clean temporary source copies and real process/API smoke, not the broken packet command.
3. Standalone bundles now carry canonical references, schemas, validator, requirements, method, report template and fallback guidance. `--evidence-root` permits target-workspace evidence without writes to installed skills. Tests execute validation from unrelated directories and a read-only installation; traversal outside the selected root is rejected.
4. Report construction explicitly retains incomplete AT/zoom/fault/lifecycle/field protocols as unknown. Tests ensure a local-budget pass cannot become field CWV pass, while a demonstrated budget failure remains visible.
5. Preserving good behavior is an explicit pre-change contract, not a subjective review after edits. The trial checks protected file hashes, exact approved screenshot equality and working-flow controls. No source changes outside the minimal allowed correction sets were accepted.

Final exporter/runtime refinements were tested structurally and with isolated execution. They have not been subjected to another fresh independent trial. The recorded CLI input snapshots preserve the earlier exact instructions, avoiding retroactive claims.

## Deliverables and next use

The five new source SKILL.md files each define conditions, procedure, evidence, limits, preservation and recheck. [Bundle instructions](../../../docs/skills.md) explain separate use and runtime prerequisites. Reports remain schema-compatible; raw agent artifacts have their original relative paths and are interpreted in the original packet layout. Evaluator before/after reports use repository-root evidence paths and are validated there.

Remaining useful work is targeted at the listed evidence gaps when the required environment/participants/telemetry exist. No new production service, monitoring platform, database migration or redesign is justified by these local trials.
