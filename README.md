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
