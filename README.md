# Toy to Tool Agent Skills v1

Seven installable Agent Skills for evidence-led application audits and narrowly verified fixes. The package contains one coordinator, six specialists, a 36-criterion catalogue, JSON schemas, a validator and three deliberately faulty local fixtures.

The project keeps four concepts separate: status (`pass`, `fail`, `unknown`, `not_applicable`), severity (`blocker`, `important`, `improvement`), decision (`fix`, `propose`, `preserve`, `investigate`) and audit level (`Essential`, `Standard`, `Advanced`). The project levels are cumulative scopes, not ASVS certification levels. An unrun check is never a pass and no aggregate score can hide a blocker.

## Install with the skills CLI

Requirements: Node.js 22.20 or later for `skills` CLI 1.7.4, and Python 3.9 or later for the bundled validator. Clone or extract this repository, then run from the target project:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add /path/to/toy-to-tool --list
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add /path/to/toy-to-tool \
  --agent codex --skill '*' --copy --yes
npx --yes skills@1.7.4 list --agent codex
```

Install one skill by replacing `'*'` with, for example, `security-privacy`. `--copy` makes a project-local copy in `.agents/skills`; every copied skill contains its own criteria, schemas, validator, documentation and license. No plugin configuration is required or supplied.

The exact local-path installation above was verified on macOS arm64 with Node 24.19.0, `skills` CLI 1.7.4 and Codex CLI 0.164.0. See the [installation guide](docs/installation.md) for the verified procedure, official format references, dependency setup and platform limits.

## Use

Ask explicitly for the relevant skill:

```text
$toy-to-tool-audit inspect this app at Essential level. Do not edit code.
```

```text
$security-privacy inspect the owner-notes fixture, fix only demonstrated ownership
boundary failures, recheck them, and preserve the current UI and API.
```

Reports must link each conclusion to a criterion and evidence. A typical workflow is Understand → set level/authority → select → collect evidence → propose or fix → verify and hand over. See [usage examples](docs/usage.md), [specialist scopes](docs/skills.md) and [limitations](docs/limitations.md).

## Skills

| Skill | Scope |
| --- | --- |
| `toy-to-tool-audit` | Coordinates a scoped multi-group audit |
| `functionality-data` | F01–F06: operations, persistence, feedback, validation, repeats and concurrency |
| `ux-visual-quality` | U01–U06: purpose, states, responsiveness, recovery and consistency |
| `accessibility` | A01–A06: keyboard, semantics, contrast, reflow, focus and targets |
| `security-privacy` | S01–S06: authorization, exposure, execution boundaries and sessions |
| `performance-resilience` | P01–P06: task performance, recovery, budgets, lifecycle and load behavior |
| `deployment-operations` | O01–O06: setup, configuration, persistence, diagnosis and recovery |

`.agents/skills/` is the generated, install-ready distribution. `authoring/` is the source for skill instructions; `scripts/build_release.py --write` regenerates the distribution deterministically. `criteria/v1.json`, `schemas/` and `scripts/audit.py` are canonical.

## Validate the release

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/audit.py validate
.venv/bin/python scripts/build_release.py
.venv/bin/python -m unittest discover -s tests -v
```

The validator checks structure and internal consistency, not the truth of audit evidence. Fixture workflows and retained evidence are documented in [evaluation/README.md](evaluation/README.md).

## Controlled comparison

The repository includes a fail-closed paired protocol for the same Codex version/model, prompt, base tools, fixture and budget, with the only intended treatment difference being installed project skills. Every arm is restored from a checksummed baseline in a new git workspace. External adjudication records true defects, false alerts, successful fixes, regressions, report accuracy, intervention counts and observed cost without combining them into one score.

The comparison is currently **not evaluated**: this machine has ambient user skills and no reviewed clean-environment receipt, so the runner correctly refuses to execute. No efficacy numbers are claimed. Read [comparison protocol](docs/comparison.md) and [machine-readable status](evaluation/comparison/STATUS.json) to reproduce it in a clean environment.

## Project status and license

Release-installation and installed-skill integration evidence is in [evaluation/evidence/release-v1](evaluation/evidence/release-v1/verification.md). Only the platforms listed there are verified; installation on one agent is not evidence of support for every agent.

Contributions are welcome under [CONTRIBUTING.md](CONTRIBUTING.md). Original project code and documentation are licensed under the [MIT License](LICENSE); external standards remain under their own terms as described in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
