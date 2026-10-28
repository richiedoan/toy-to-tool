# Controlled same-agent comparison

## Status

**Not evaluated.** No comparative agent run has been executed and all outcome metrics are `null`. The current macOS user has 26 ambient project/user skill directories and the environment receipt is unverified. `comparison_runner.py preflight` detects both conditions and refuses to launch either arm. The installation/invocation smoke is separate and must not be counted as a skills-effectiveness result.

## Question and treatment

The experiment compares the same pinned Codex CLI/model on the same fixture with:

- `no_skills`: no Toy to Tool project skills installed;
- `with_skills`: only the relevant Toy to Tool project skill bundles installed.

Unavoidable agent built-ins must be identical in both arms and recorded as a reviewed inventory hash. “No skills” therefore means no experimental or ambient custom skills, not a claim that the agent binary contains no built-in behavior. The treatment measures the full installed package, including its references and validator, rather than the wording of `SKILL.md` alone.

## Controls

`evaluation/comparison/config.json` pins Codex CLI 0.164.0, `gpt-6.1-sol`, medium reasoning, workspace-write sandbox, three fixtures, three replicates, a 300-second wall budget and 40 observed command starts. Both arms receive byte-identical:

- prompt and neutral trial report schema;
- baseline fixture archive;
- requirements, `AGENTS.md` and `.gitignore`;
- base agent settings, disabled apps and disabled automatic skill dependency installation;
- workspace structure and local git baseline.

Arm order is deterministically randomized by the declared seed. Each run receives a new opaque directory restored from a checksummed archive. Input hashes, full installed-skill hashes and clean git status are checked immediately before execution. A modified, stale or previously used workspace is rejected; runs are never resumed.

The wall limit is enforced by the runner. Command-start count is an observed client-side stop, not a server admission limit, so a command already starting at the boundary may complete; actual count and stop reason remain in the receipt.

## Prepare in a clean environment

Use a clean OS account or isolated runner with no custom user skills. Do not simply rename an ambient directory. Record an independently reviewed, secret-free copy of `evaluation/comparison/environment.template.json` with the actual tool inventory, versions, common built-in inventory hash and capability check, then point `environment_receipt` in a copied config to it.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python evaluation/comparison_runner.py preflight \
  --config /path/to/reviewed-config.json

.venv/bin/python evaluation/comparison_runner.py prepare \
  --config /path/to/reviewed-config.json \
  --destination /new/outside-repo/experiment

.venv/bin/python evaluation/comparison_runner.py execute \
  --plan /new/outside-repo/experiment/plan.json
```

`prepare` is safe to run on a blocked host and creates only unexecuted workspaces. `execute` repeats preflight and fails closed before any model call if the environment is ineligible. Keep the experiment directory, agent JSONL, stderr, run receipts, git diffs and output artifacts.

## Independent adjudication

Do not place evaluator ground truth in a trial workspace. After execution, a reviewer uses `evaluation/comparison/ground-truth.json`, the fixture contracts, before/after regression checks and the schemas to create one `adjudication.schema.json` document per run. Additional real defects are allowed; they are not false alerts merely because the seeded oracle omitted them. Correlated symptoms of one root defect share one `defect_id`.

Score a reviewed run:

```sh
.venv/bin/python evaluation/comparison_runner.py score \
  --plan /new/outside-repo/experiment/plan.json \
  --run-id OPAQUE_RUN_ID \
  --grade /path/to/adjudication.json \
  --evidence-root /path/to/review/evidence
```

The scorer rejects unexecuted runs, duplicate review IDs, missing evidence and evidence paths outside the declared root. It never overwrites an existing score.

## Metrics

Report each arm and paired differences; retain replicate-level records.

| Metric | Rule |
| --- | --- |
| True defects detected | Unique adjudicated root `defect_id`s correctly reported |
| False alerts | Findings adjudicated false; unknown/unresolved is separate |
| Successful fixes | Unique root defects corrected and independently rechecked |
| Regressions | Confirmed baseline-pass → after-fail cases; `null` until coverage review is complete |
| Report accuracy | Correct / (correct + incorrect) factual claims; unresolved excluded and reported |
| User intervention | Questions required and actually answered, separately; `null` until review is complete |
| Cost | Actual wall time and token receipt; USD only with an actual per-run billing receipt |

Scope violations are reported alongside regressions to test whether the agent preserves good behavior and avoids unrelated refactors or UI changes. No aggregate score is calculated. Blockers, unknowns and unresolved claims stay visible.

## Interpretation

Three replicates on three seeded fixtures are calibration evidence, not general proof across repositories, models or agents. Report failures, protocol deviations and missing receipts. Do not price tokens from a current public table after the fact, and do not convert an installation smoke into one comparison arm.

