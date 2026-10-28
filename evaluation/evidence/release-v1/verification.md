# v1 release verification

Captured 2026-10-28. These are installation/integration checks, not a controlled skills-effectiveness comparison.

## Checklist

1. **CLI discovery — verified.** `skills` CLI 1.7.4 discovered all seven skills from the repository. The command exited 0; see [command receipt](install-commands.json) and `skills-cli-0.txt`.
2. **Copied install — verified in a new project, partially isolated.** All seven skills were copied into a newly created git project and a new Python virtual environment. The install and list commands exited 0 (`skills-cli-1.txt`, `skills-cli-2.txt`). It was not a fresh OS account/container: the same user profile had ambient skills, so clean-account isolation remains unverified.
3. **Agent recognition/invocation — verified for Codex.** A fresh ephemeral Codex CLI process was explicitly prompted with `$security-privacy`; its event stream shows reads from the target project's installed `SKILL.md` and installed engine. See [recognition receipt](agent-recognition.json), [invocation receipt](agent-invocation.json) and `installed-agent-events.jsonl`.
4. **References/catalogue/scripts after install — verified.** Every installed skill was a copy, not a symlink, and included the catalogue, schemas, validator, requirements and shared docs. All installed files still matched the release manifest after the agent run. See [resource receipt](installed-resources.json) and [recognition receipt](agent-recognition.json).
5. **Fixture from installed target — verified.** The owner-notes v2 baseline was restored under the target project, not run from the source repository. The installed agent changed only the target fixture's `server.py`. An evaluator then ran the target fixture through real HTTP and Chrome: positive controls, cross-owner read/write denial, owned edit/validation, logout replay, expiry and desktop preservation all passed. See [fixture results](installed-fixture/results.json), screenshot and trace in `installed-fixture/`, and the installed agent's before/after artifacts in `installed-agent-artifacts/`.
6. **Platform statement — recorded below.** No claim is made for untested platforms or agents.

## Actual environment

| Component | Exercised |
| --- | --- |
| OS/CPU | macOS, Apple M2 arm64 |
| Node/npm | 24.19.0 / 11.17.0 |
| `skills` CLI | 1.7.4, local repository path, `--copy`, project install |
| Agent | Codex CLI 0.164.0, `gpt-6.1-sol`, medium reasoning, ephemeral workspace-write run |
| Python | 3.9.6, target-local virtual environment |
| Browser | Chrome 156.0.8078.49, no throttling |

Not verified: Linux, Windows, a fresh OS user or container, global/symlink/remote GitHub installation, agents other than Codex, or automatic skill invocation without an explicit `$security-privacy` request. The Codex subprocess could not bind sockets or launch a browser, so it used source/handler/SQLite evidence and correctly retained limitations; the separate evaluator process performed the real HTTP/Chrome recheck.

## Integrity and claims

The installed process made no command reference to the source repository. It read and executed the installed engine and retained `unknown` for checks it could not run. The integration run recorded token usage and wall time, but no per-run billing receipt was available, so monetary cost is `null` and no price was inferred.

The controlled comparison remains `not_evaluated`; see [comparison preflight](comparison-preflight.json). This smoke proves packaging, explicit discovery and a bounded installed workflow only.
