# Toy to Tool Agent Skills

Seven skills that help your coding agent inspect an app, find problems, and verify fixes. Start with a general audit or choose a specialist for functionality, usability, accessibility, security, performance, or deployment.

Findings link to evidence. Checks that could not be run stay marked as unknown.

## Quick start

Run this from your project's directory, then choose the skills and agent to install to:

```sh
npx skills add richiedoan/toy-to-tool
```

Requires Node.js 22.20 or later. No manual clone is needed.

Browse before installing:

```sh
npx skills add richiedoan/toy-to-tool --list
```

Or install just the audit coordinator:

```sh
npx skills add richiedoan/toy-to-tool --skill toy-to-tool-audit
```

Each skill includes its supporting resources and can be installed separately. See the [installation guide](docs/installation.md) for local installation, validator setup, and troubleshooting. Python is needed to run the bundled validator.

## Use it

In Codex, ask for an audit:

```text
$toy-to-tool-audit inspect this app at Essential level. Do not edit code.
```

Essential is the smallest audit scope; Standard and Advanced add more checks.

Or ask a specialist to inspect and fix a specific area:

```text
$accessibility inspect this app's keyboard navigation, fix demonstrated
problems, and verify the fixes. Preserve the current visual design.
```

See [usage examples](docs/usage.md) for more workflows.

## Available skills

| Skill | What it checks |
| --- | --- |
| `toy-to-tool-audit` | Coordinates an audit across the areas below |
| `functionality-data` | Core actions, saved data, input validation, and repeated or concurrent actions |
| `ux-visual-quality` | Clear screens, responsive layouts, consistent patterns, and error recovery |
| `accessibility` | Keyboard access, accessible names, contrast, zoom, and focus |
| `security-privacy` | Access controls, data exposure, unsafe execution, and sessions |
| `performance-resilience` | Task speed, resource use, and recovery from network failures |
| `deployment-operations` | Setup, configuration, data preservation, and recovery |

Read the [specialist guide](docs/skills.md) for detailed scopes and the [limitations](docs/limitations.md) for what these audits can establish.

## Documentation and contributing

- [Installation](docs/installation.md): detailed setup and verified environments.
- [Audit method](docs/method.md): criteria, evidence, and report rules.
- [Contributing](CONTRIBUTING.md): source layout, bundle generation, and validation commands.
- [Evaluation](evaluation/README.md): fixture workflows and retained evidence.

Installation and invocation have been tested with Codex on macOS; see the [verification record](evaluation/evidence/release-v1/verification.md) for details. The controlled comparison of runs with and without these skills is [not yet evaluated](docs/comparison.md); no measured effectiveness claims are made.

## License

[MIT](LICENSE). External standards retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).
