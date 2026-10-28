# Usage examples

## Coordinator inspection

```text
$toy-to-tool-audit inspect this repository at Essential level. The three priority
tasks are sign in, create a record, and retrieve it after restart. Use local test
data only. Do not edit code. Link every conclusion to a criterion and evidence.
```

If the user has not established an audit level or edit authority, the coordinator defaults to Essential inspection with recommendations only. It asks only questions that can change applicability, evidence access, authority or a consequential decision.

## Scoped specialist fix

```text
$functionality-data inspect the tracker against F01-F06, fix only reproduced
persistence or duplicate-submit failures, and recheck the same scenarios. Preserve
the existing layout, labels and unrelated behavior. Save before/after reports and
raw evidence under audits/tracker/.
```

The expected flow is Inspect → Improve → Recheck. A criterion with no executed or otherwise sufficient evidence remains `unknown`. A demonstrated requirement violation or risk can be `fix`; measurable benefit outside edit authority is `propose`; preference without demonstrated benefit is `preserve`; insufficient evidence is `investigate`.

## Installed validator

From the application project, after installing dependencies:

```sh
.venv/bin/python .agents/skills/functionality-data/references/engine/scripts/audit.py \
  select --profile audits/tracker/profile.json --level Standard --group F

.venv/bin/python .agents/skills/functionality-data/references/engine/scripts/audit.py \
  validate --report audits/tracker/after-report.json --evidence-root "$PWD"
```

Use the real app profile. The report schema keeps status, severity and decision separate. Artifact links are checked against the explicit evidence root; remote evidence authenticity still needs reviewer judgment.

## Review existing evidence without running the app

```text
$toy-to-tool-audit review audits/my-run/report.json and its existing evidence only.
Do not start the app or rerun system tests. Identify unsupported conclusions and
the exact missing checks; preserve historical observations.
```

For a new format 1.1 report, populate the task/step records from actual observations,
then generate and review the human view from the engine root:

```sh
.venv/bin/python scripts/audit.py render --report audits/my-run/report.json
.venv/bin/python scripts/audit.py review --report audits/my-run/report.json
```

Installed engines use the same commands and an explicit `--evidence-root "$PWD"`.
Review reads local artifacts and checks Markdown freshness; it invokes no app
runner. The generated region stays canonical when translating the surrounding
narrative. See [format and migration rules](method.md#compatibility-and-migration)
and the synthetic [step example](../examples/report-steps.json). Legacy reports
remain readable and validate under the old contract without new assurance.

## Missing capabilities

When a browser, runnable environment or credentials are missing:

1. Record the capability check and exact failure.
2. Continue only with evidence the available environment can genuinely establish.
3. Mark the affected conclusion `unknown` and decision `investigate`.
4. State the smallest next action and required owner/access.
5. Do not change the app solely to make an unavailable check appear green.

The full fallback policy is bundled at `references/engine/docs/missing-access.md` in every installed skill.

