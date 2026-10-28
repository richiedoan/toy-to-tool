# Toy to Tool Agent Skills

Seven Agent Skills for Codex, Claude Code, Gemini CLI, and other compatible coding agents to inspect an app, find problems, and verify fixes. Start with a general audit or choose a specialist for functionality, usability, accessibility, security, performance, or deployment.

Findings link to evidence. Checks that could not be run stay marked as unknown.

## Quick start

Run the command for your agent from your project's directory. Each command installs all seven skills, including their supporting resources.

### Codex

```sh
npx skills add richiedoan/toy-to-tool --agent codex --skill '*' --copy --yes
```

### Claude Code

```sh
npx skills add richiedoan/toy-to-tool --agent claude-code --skill '*' --copy --yes
```

### Gemini CLI

```sh
npx skills add richiedoan/toy-to-tool --agent gemini-cli --skill '*' --copy --yes
```

### Other agents

For Cursor, GitHub Copilot, OpenCode, and other [supported agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md), use the interactive installer and choose your agent and skills:

```sh
npx skills add richiedoan/toy-to-tool
```

### Installation options

Requires Node.js 22.20 or later. No manual clone is needed. Add `--global` to an install command to make the skills available across projects.

Browse before installing:

```sh
npx skills add richiedoan/toy-to-tool --list
```

Or install just the audit coordinator for your agent (Codex shown):

```sh
npx skills add richiedoan/toy-to-tool --agent codex --skill toy-to-tool-audit --copy --yes
```

Each skill includes its supporting resources and can be installed separately. See the [installation guide](docs/installation.md) for local installation, validator setup, and troubleshooting. Python is needed to run the bundled validator.

## Use it

Open a new agent session after installation. In any supported agent, ask for an audit:

```text
Use toy-to-tool-audit to inspect this app at Essential level. Do not edit code.
```

In Codex, you can also invoke the skill explicitly:

```text
$toy-to-tool-audit inspect this app at Essential level. Do not edit code.
```

Essential is the smallest audit scope; Standard and Advanced add more checks.

Or ask a specialist to inspect and fix a specific area:

```text
Use accessibility to inspect this app's keyboard navigation, fix demonstrated
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

- [Verification record](evaluation/evidence/release-v1/verification.md): installation and invocation evidence.
- [Comparison protocol](docs/comparison.md): controlled evaluation design.

## License

[MIT](LICENSE). External standards retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).
