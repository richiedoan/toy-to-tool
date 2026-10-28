# Audit specialists and independent bundles

All specialists reuse `criteria/v1.json`, the existing JSON report schema and fix/propose/preserve/investigate rules. Source skills live under `.agents/skills/`; criteria are not reauthored in each skill.

| Skill | Group | Primary evidence | Key limits |
| --- | --- | --- | --- |
| functionality-data | F01-F06 | Actual operation/readback, retention transitions, values/identities/counts | Do not impose database/sync or conflict semantics |
| ux-visual-quality | U01-U06 | Task/state observations, target-device screenshots, recovery, pattern comparisons | Expert review is not a real-user study; preserve approved design |
| accessibility | A01-A06 | Keyboard/AT behavior, accessible names, actual color/geometry/focus/resize measurements | Source exceptions apply; six criteria do not certify WCAG AA |
| security-privacy | S01-S06 | Scoped actor/resource/action requests, state readback, safe sink/session probes | Authorized test environments only; no blanket ASVS/security claim |
| performance-resilience | P01-P06 | Raw timing distributions, task results, fault recovery and bounded resource series | Local task timing is not adequate field CWV or a load study |
| deployment-operations | O01-O06 | Clean setup transcript/smoke, config boundaries, copy/restore and diagnosis evidence | No invented hosting, backups, SLO or telemetry stack |

Each SKILL.md defines when to use it, Inspect → Improve → Recheck, evidence, limits and preservation controls. The coordinator can use an installed specialist or the canonical protocols directly; no installed sibling is mandatory.

## Export a separately usable skill

```sh
python3 scripts/package_skill.py security-privacy /tmp/exported-skills/security-privacy
python3 scripts/package_skill.py accessibility /tmp/exported-skills/accessibility
```

Use a new destination outside the source repository. The output folder is the self-contained skill bundle to use/install separately. Do not copy only the unbundled source SKILL.md. The exporter includes source instructions/assets, the full canonical catalogue/source registry, schemas, validator, requirements, method, English report template and missing-access guidance under `references/engine/`. Links are rewritten to bundled resources. It copies no fixture, evaluator oracle, hidden test, historical report, virtual environment or credentials. Existing destinations are never overwritten.

The environment still needs a compatible Python interpreter and the declared packages, plus browser/AT/runtime/credentials for the checks that require them. Install the included requirements into an available environment; no write access to the installed skill is required. Create app profiles and evidence in the target workspace. Explicitly pass its root when validating local artifact links:

```sh
/path/to/python /tmp/exported-skills/security-privacy/references/engine/scripts/audit.py validate \
  --report /path/to/target/audits/run/after-report.json --evidence-root /path/to/target
```

Use `select`/`template` with the actual profile and chosen `--group`/level. Do not use an example profile as real facts. Without sufficient evidence, retain unknown. Local artifact traversal and symlink escape outside the selected evidence root are rejected. Remote HTTPS artifact availability/authenticity remains a reviewer responsibility.

## Why these scripts exist

There are no per-specialist scanners that invent a pass from an opinion. The canonical validator/selector handles repeated structural decisions. The bundle exporter prevents missing dependency/reference files and silent drift from the canonical criteria. Fixture packet exporters prevent answer contamination and preserve checksummed originals. The evaluator HTTP/browser harness adds value where source inspection cannot establish ownership enforcement, rendered mobile geometry, real recovery, local timing or visual preservation. A small evaluator-only trace redactor removes session/authentication headers while retaining observation payloads and screenshots; it is integrated into the HTTP/browser harness. Report helpers retain unknowns for unexecuted/insufficient protocols, including field CWV after a local budget correction.

## Recorded trials

Read [the expansion handover](../evaluation/evidence/expansion-v1/workflow.md) for source/visual preservation, actual request/browser results and limitations. The original tracker workflow remains separate. The new fixtures are not evidence of general skill effectiveness or comprehensive conformance; both independent CLI attempts had runtime restrictions, followed by separately labeled evaluator rechecks.
