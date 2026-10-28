# Inspect → Improve → Recheck: recorded tracker trial

## Scope and interpretation

This is a Functionality & Data workflow exercise on a deliberately seeded, local tracker. The fixture author/evaluator knew the defects. Evaluator-led Chrome checks are manual workflow verification assisted by browser automation, not a blind agent-efficiency experiment. A separate fresh CLI thread was attempted with an allowlisted neutral packet; it had limited runtime access. Neither this single attempt nor the manual work establishes that skills improve agent effectiveness. There is no no-skill control, randomized repeated trial, controlled model configuration or time/cost comparison.

The contract and authorized scope are recorded in [E-context](context.md). The [before JSON](before-report.json) and [after JSON](after-report.json) declare Standard and `criterion_groups: ["F"]`. F06 is deferred; other groups are not assessed. No application-wide quality score is assigned.

## Inspect

The restorable original is [the archived baseline](../../baselines/tracker-v1.tar.gz), with [SHA256 manifest](../../baselines/tracker-v1.manifest.json). Browser evidence source hashes match its file hashes. It was never overwritten by the fix. `prepare_packet.py` restores it into a new destination and refuses to overwrite an existing one.

Evaluator Chrome observations reproduced:

| Observed issue | Criterion and impact | Evidence |
| --- | --- | --- |
| The save UI confirms completion while stored note/completion stay unchanged | F01 blocker; F03 important | E-save-readback: [raw values](before/results.json), [screen](before/save-readback.png), [trace](before/save-readback.trace.zip) |
| Refresh/reopening the app presents no saved task despite a stored record | F02 blocker under the three-task contract | E-refresh/E-reopen: [raw values](before/results.json), [refresh screen](before/refresh.png) |
| Two pending submissions produce two record identities | F05 important | E-rapid-repeat: [count/identities](before/results.json), [screen](before/rapid-repeat.png) |
| A valid 500-character note is not committed, so later oversized-note assertions are not reached | F04 important, correlated with the broken save path | E-note-boundaries: [assertion and values](before/results.json) |

Positive controls also ran: actual creation/readback with Unicode/punctuation, title boundaries, later intentional same-title creation and failed-create input/data retention. See the corresponding case IDs in [the raw baseline results](before/results.json). Eight of twelve browser scenarios failed; four passed. These are assertion counts, not a quality score or independent defect count.

## Independent coding attempt

A new `codex exec --ephemeral --sandbox workspace-write` thread used `/tmp/toy-functionality-agent-run`, created by the allowlist exporter with a new empty Git history. The input contained the original app, product contract, F skill and engine resources. No evaluator oracle, hidden browser harness, previous reports or reference fix was copied. The neutral instruction is preserved in the evaluator run procedure. [Recorded events](independent-agent/events.jsonl) show the actual work; no evaluator-only source read appears in that transcript. This is input/context separation, not proof of OS-level read isolation.

The CLI was installed and authenticated, but its sandbox denied loopback/browser execution and dependency installation. [Tooling evidence](independent-agent/audits/standard-20261028/tooling.json) and [setup limitations](independent-agent/audits/standard-20261028/setup-limitations.md) record those failures. A CLI existing did not establish a complete coding-agent browser environment.

The agent preserved its own [before report](independent-agent/audits/standard-20261028/before/report.md), corrected the app and saved an [after report](independent-agent/audits/standard-20261028/after/report.md). It executed application source through Node DOM/storage/timer adapters: [27 regression checks](independent-agent/audits/standard-20261028/after/neighboring.json) passed. Its report kept F01-F04 unknown for full browser behavior and limited the F05 pass to executed handlers. Those adapters do not establish real browser persistence. Original handler failures were rerun and corrected; broader browser coverage remained explicitly unverified by that agent.

Its original engine validation was unavailable. The evaluator later validated both original JSON reports using the available interpreter against their original packet-relative artifacts; both passed. This later evaluator check does not retroactively turn the agent's unexecuted validation into an executed agent check. Copies of raw agent reports retain original relative evidence paths and belong to their packet layout; the main before/after reports use repository-root evidence paths.

## Improve

The applied [patch](change.patch) is the independent agent's app.js change, with no evaluator code correction afterward. It loads existing data, writes edits before confirming success, rejects oversized notes, guards pending operations and preserves drafts when adding a different task. Its [change history](independent-agent/audits/standard-20261028/changes.md) links the original failures and checks.

Preserve decision: keep browser-local storage and the existing one-person architecture; the contract does not justify a database, accounts or synchronization. F02/F05 evidence: [context](context.md), [intentional-repeat](after/results.json). The patch preserves separately intentional same-title records while preventing rapid duplicate activation.

## Recheck and regression

The evaluator ran the same twelve browser scenario assertions against the exact applied app hashes; all passed. The [after results](after/results.json) include actual UI/storage state, environment and source hashes; each case has an adjacent PNG and trace ZIP. F01-F05 current outcomes and evidence IDs are in [the after report](after-report.json).

Verified cases include create/readback, edited note/completion readback, same-origin refresh and tab reopening, rapid repeats, separately intentional repeats, title/note boundaries, storage rejection without false confirmation or loss of previous data/drafts, truthful delayed-save feedback, and repeat save. Scope remains the listed scenarios. Browser/OS restart, cross-device retention and F06 concurrency were not tested or claimed.

## Workflow weaknesses addressed before expansion

| Weakness observed | Correction and verification |
| --- | --- |
| The engine required coverage of all groups for a focused skill | Added optional `criterion_groups` and `--group F`; coverage/rejection tests verify omitted F rows still fail and unscoped group claims are rejected. Existing full-catalogue reports remain compatible. |
| HTML maxlength silently changed the evaluator's intended oversized input | Programmatically inject and assert actual length before submission. Rerunning the original app made the title-boundary test pass; this false positive was not reported as an app bug. The earlier calibration run remains in ignored evaluator scratch output, separate from accepted evidence. |
| Agent source-only F02 severity differed from the evaluator's browser-confirmed blocked core task | Clarified severity assessment against the three priority outcomes and required contract-valid workarounds; browser-confirmed F02 stays blocker in the evaluator baseline. This refinement is not yet independently retested. |
| Installed CLI/Chrome did not imply usable agent execution capabilities | Added an early capability preflight to the F skill, `--bootstrap` to the neutral exporter, and explicit separate handler/browser evidence. The actual restricted trial is disclosed, not relabeled as a complete agent browser audit. |
| A packet nested inside the evaluator checkout could inherit evaluator context | Exporter now rejects destinations inside this repository; allowlist/overwrite/corruption/isolation tests cover the boundary. |
| Broad `audits/` ignore could hide archived agent evidence | Anchor the ignore rule to `/audits/`; evaluator archives nested under evidence remain versioned. |
| Probe/infrastructure errors could be mistaken for app failures during automatic report generation | The report builder now distinguishes demonstrated assertion failures from probe errors; unexecuted/infra-only cases remain unknown. Tests cover empty/skipped probes and preserving a demonstrated failure alongside an unknown. |
| An evaluator could accidentally replace prior screenshots/results | The browser harness now requires a new output directory; report creation and packet export also refuse overwrite. |

The final skill includes these refinements after the trial; the packet used by the recorded agent contains the pre-refinement skill, preserved in the event record. These refinements have structural/integration verification, not a second independent agent trial. No expansion to other criterion groups was performed.

## Remaining limits

A complete independent browser-capable coding-agent trial still needs an environment permitting the documented runtime, declared engine dependencies, loopback server and browser process. The current artifacts support workflow correctness for this fixture and the stated checks. They do not support claims about skill efficacy, real users, real production systems or all application behavior.
