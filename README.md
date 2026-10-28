# Toy to Tool evaluation criteria v1

A machine-readable evaluation protocol for deciding what to fix, propose, preserve or investigate in an application. There are exactly 36 criteria, six in each of six groups. Essential, Standard and Advanced are cumulative project audit scopes; they do not grant code-change authority or represent ASVS certification.

## Run

Requires Python 3.9 or later. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/audit.py validate
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/audit.py validate --report examples/report.json
.venv/bin/python scripts/audit.py select --profile examples/profile.json --level Standard
.venv/bin/python scripts/audit.py template --profile examples/profile.json --level Essential > /tmp/audit-report.json
```

Edit a copy of the example profile to describe the actual app before selecting criteria. `null` means a feature is not yet established; `false` requires a reason. A report template deliberately starts with unknown results, with reasoned exclusions for absent features. It is not a completed audit. Validation exits nonzero for invalid input.

## Audit orchestration skill

Use `$toy-to-tool-audit` from this checkout, or ask the agent to read [SKILL.md](.agents/skills/toy-to-tool-audit/SKILL.md). The repository-local skill follows six stages: understand the priority tasks/users/data/environment, set level and authority, select criteria, collect evidence, propose or make scoped fixes, then verify and hand over.

It defaults to Essential inspection and recommendations without target-code edits, reuses existing permissions, and asks only questions that change a decision. It includes an [English report template](.agents/skills/toy-to-tool-audit/assets/report.md) and [missing-browser/runtime/credentials guidance](.agents/skills/toy-to-tool-audit/references/missing-access.md). Keep this skill with its repository engine; copying the skill directory alone is insufficient. Audit artifacts go in ignored `audits/<run-id>/` directories and are not published automatically.

## Functionality & Data trial

Use `$functionality-data` for an F01-F06 focus through Inspect → Improve → Recheck. Scoped reports use `--group F`; other groups have no assessed outcome. The local tracker and its neutral behavior contract are in `fixtures/tracker/`.

Evaluator instructions, the immutable original, context-separated agent-packet export and recorded before/after browser evidence are described in [evaluation/README.md](evaluation/README.md). Evaluator material is excluded from the agent packet. The recorded exercise includes a restricted independent CLI attempt and evaluator-led Chrome verification; it is not evidence of a skill-effectiveness gain.

## Repository contract

| Path | Purpose |
| --- | --- |
| `criteria/v1.json` | All 36 protocols, applicability gates, evidence, pass/fail/unknown rules, contextual severity, decisions, verification and source registry |
| `schemas/` | JSON Schema 2020-12 contracts for catalogue, app profile and report |
| `scripts/audit.py` | Schema and semantic validation, cumulative selection, decision function and report template generation |
| `docs/method.md` | Skill-consumption instructions, aggregation, evidence and authority policy |
| `docs/review.md` | Explicit project choices, verified scope and remaining review decisions |
| `examples/` | Synthetic app profile/report and linked demonstration evidence for all four decisions |
| `tests/` | Rejection and behavior tests for contract violations and decision boundaries |

The detailed user brief was supplied locally as the untracked input `PROJECT_BRIFFF.md`, preserved unchanged. A file named `PROJECT_BRIEF.md` was not available. No application implementation was present.

## Sources and limits

The catalogue distinguishes [WCAG 2.2 normative requirements](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) from the project's evaluation policy and explanatory guidance. Security references [OWASP ASVS 5.0.0](https://asvs.owasp.org/) without claiming numbered control coverage; exact requirement mappings would need a separate scoped verification. [Google Web Vitals](https://web.dev/articles/vitals) informs the performance criterion's field thresholds. Full titles, versions, access dates, per-criterion links and exceptions are in the catalogue.

Passing this protocol is not a declaration of WCAG AA compliance or system security. The validator checks structure, enumerations, coverage, reference integrity and decision consistency. A reviewer or consuming skill must still inspect evidence authenticity, applicability, standards exceptions and sufficiency for the claimed scope. Synthetic examples are not assurance for a real app.
