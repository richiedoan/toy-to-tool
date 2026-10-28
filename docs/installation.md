# Installation

## Verified project-local installation

This procedure was executed on 2026-10-28 from a local repository checkout into a new target project. It uses a copy rather than a symlink, so the installed skill remains self-contained.

Prerequisites:

- Node.js 22.20 or later (`skills` CLI 1.7.4 declares that engine requirement).
- Python 3.9 or later for the catalogue/report validator.
- A target agent supported by the selected `skills` CLI version. Only Codex was exercised here.

From a new or existing target project:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add /absolute/path/to/toy-to-tool --list
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add /absolute/path/to/toy-to-tool \
  --agent codex --skill '*' --copy --yes
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 list --agent codex
```

Use `--skill security-privacy` (or another listed name) instead of `'*'` to install one skill. Inspect `.agents/skills/<name>/SKILL.md`; `references/engine/` must contain the catalogue, schemas, validator, requirements and shared guidance.

Create a project environment for validator commands:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r .agents/skills/security-privacy/references/engine/requirements.txt
.venv/bin/python .agents/skills/security-privacy/references/engine/scripts/audit.py validate
```

Restart or open a new agent session if the agent cached skill discovery before installation. Invoke a skill explicitly, for example `$security-privacy`, for a simple recognition test. Do not infer that every agent supports this package because one agent recognized it.

## What was verified

| Item | Result |
| --- | --- |
| Host | macOS arm64 |
| Node/npm | 24.19.0 / 11.17.0 |
| `skills` CLI | 1.7.4, local-path discovery and copied project install |
| Agent | Codex CLI 0.164.0, `gpt-6.1-sol`, medium reasoning |
| Python | 3.9.6 |
| Browser recheck | Chrome 156.0.8078.49 |
| Target isolation | New project directory and virtual environment; same OS user profile |

Linux, Windows, fresh OS-user isolation, global installs, symlink mode, remote GitHub installation, and Claude/Cursor/Gemini or other agents were not verified. The clean target retained the host's ambient user profile; therefore it proves project-local packaging and invocation, not a clean comparative experiment.

## Format sources checked

The generated distribution follows the [Agent Skills specification](https://agentskills.io/specification): `SKILL.md` has a YAML `name` matching its directory and a `description`; names use lowercase letters and hyphens. It also uses the optional `license` and `metadata` fields. Local source discovery and `--list`, `--agent`, `--skill`, `--copy` and `--yes` follow the [`skills` CLI command reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md). Telemetry opt-out follows the [`skills` CLI documentation](https://www.skills.sh/docs/cli). Codex's repository skill location and explicit invocation were checked against [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills).

Those pages were checked on 2026-10-28. The CLI is pinned in examples because its behavior and requirements can change.

## Alternative export

For a single portable folder without invoking the CLI against the whole repository:

```sh
python3 scripts/package_skill.py security-privacy /tmp/security-privacy
```

The destination must not exist and must be outside the source repository. This exporter is also used by release consistency tests. It is an export step, not an agent installer.

## Troubleshooting

- If discovery returns no skills, confirm the source has `.agents/skills/<name>/SKILL.md` and rerun the pinned `--list` command.
- If the agent sees the skill but validation fails, install the bundled Python requirements and use that environment's interpreter.
- If browser, runtime or credentials are absent, retain `unknown`, record the failed capability check and use only the documented fallback evidence. Never convert source inspection into an executed pass.
- Do not copy only an authoring template. Install from `.agents/skills/` or use the exporter so references and scripts remain available.

