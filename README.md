# Toy to Tool Agent Skills

**Seven agent skills. Six quality areas. 36 evidence-driven criteria.**

For Codex, Claude Code, Gemini CLI, and other compatible coding agents: inspect whether core workflows produce real results, saved data survives required transitions, access controls hold across users, and recovery procedures actually work.

Start with a coordinated audit or choose a specialist. Findings link to evidence, authorized fixes are rechecked, and untested behavior stays unknown.

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

`toy-to-tool-audit` coordinates the audit: establish the app's requirements and architecture, select applicable criteria at the chosen level, and consolidate findings and verification results. Each specialist below can also run independently.

| Specialist | Criteria | What it evaluates |
| --- | --- | --- |
| `functionality-data` | F01–F06 | Real workflow outcomes, required persistence, truthful feedback, input rules, repeated actions, concurrent updates |
| `ux-visual-quality` | U01–U06 | Screen purpose, interface states, responsive task access, mistake recovery, consistent patterns, evaluation with target users |
| `accessibility` | A01–A06 | Keyboard operation, names and semantics, contrast, zoom and reflow, visible focus, pointer targets |
| `security-privacy` | S01–S06 | Sensitive data exposure, authorization, unsafe execution, sessions, feature-specific attack surfaces, trust boundaries |
| `performance-resilience` | P01–P06 | Runtime failures, network recovery, performance targets, resource accumulation, expected load, interrupted-state recovery |
| `deployment-operations` | O01–O06 | Reproducible startup, runtime configuration, data preservation, failure diagnosis, verified recovery and rollback, operational objectives |

## The 36 criteria

Each criterion defines expected behavior, applicability, test steps, required evidence, pass/fail conditions, severity guidance, and verification after a fix. Essential, Standard, and Advanced set inspection depth; criteria are selected for the app's actual features and agreed requirements.

Expand a group to see what the audit asks the agent to establish. The [canonical catalogue](criteria/v1.json) contains the full protocols and starting level for each criterion.

<details>
<summary><strong>Functionality &amp; Data — Do tasks produce the promised results?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| F01 | Core workflows perform real operations | Execute essential tasks and independently read the resulting state or artifact; identify disclosed demo or mock behavior. |
| F02 | Data persists according to the agreed requirements | Compare values before and after required refresh, reopen, relogin, device, or deployment transitions. |
| F03 | UI feedback reflects actual operation outcomes | Match pending, success, and failure states to actual results; verify optimistic updates reconcile or roll back. |
| F04 | Inputs follow the application's data rules | Exercise valid, invalid, and boundary values at relevant boundaries, including the server when present; inspect stored results. |
| F05 | Repeated actions do not create unintended side effects | Repeat submissions and retries; compare resulting records and effects with the operation's repetition rules. |
| F06 | Concurrent updates follow an explicit consistency rule | Trace competing writes from separate sessions and verify conflict handling, visibility, and final authoritative state. |

</details>

<details>
<summary><strong>UX &amp; Visual Quality — Can people understand and complete the task?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| U01 | Users can identify the screen purpose and primary action | Compare screen purpose, labels, and primary actions with target tasks; distinguish expert review from participant observations. |
| U02 | Relevant interface states are complete and actionable | Trigger loading, empty, success, error, and disabled states; check that explanations and next actions match the situation. |
| U03 | Layout does not obstruct essential tasks | Inspect supported viewports for clipping, overlap, and occlusion; verify essential content and controls remain reachable. |
| U04 | Users can prevent, correct, and recover from mistakes | Exercise invalid input, cancel/back behavior, and destructive actions; verify proportionate prevention or recovery. |
| U05 | Visual and interaction patterns are consistent | Compare typography, spacing, color, controls, labels, and behavior against agreed patterns and intentional differences. |
| U06 | Important workflows are evaluated with target users | Observe real target users performing representative tasks against predefined goals; retain deidentified results and sample limits. |

</details>

<details>
<summary><strong>Accessibility — Can people operate the essential workflows?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| A01 | Essential workflows are keyboard accessible | Complete tasks by keyboard with meaningful focus order and no keyboard traps, applying documented source exceptions. |
| A02 | Controls have appropriate names and semantics | Inspect names, roles, labels, and states using the DOM/accessibility tree and assistive-technology observations. |
| A03 | Text contrast meets applicable minimum requirements | Measure actual foreground/background combinations: at least 4.5:1 for normal text and 3:1 for large text, subject to source exceptions. |
| A04 | Zoom and reflow preserve content and functionality | Test text resizing to 200% and reflow at the source-defined dimensions; record task outcomes and applicable exceptions. |
| A05 | Keyboard focus is visible and not entirely obscured | Follow keyboard focus through tested states; capture the indicator and any content that obscures the focused control. |
| A06 | Pointer targets have sufficient size or spacing | Measure hit boxes and spacing against the 24 × 24 CSS pixel requirement or document the applicable source exception. |

These six criteria reference WCAG 2.2 requirements; they do not establish full WCAG AA conformance.

</details>

<details>
<summary><strong>Security &amp; Privacy — Do data and actions stay within authorized boundaries?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| S01 | Secrets and sensitive data are not unintentionally exposed | Inspect public surfaces and exposure paths against intended audiences; retain redacted evidence without copying raw secrets. |
| S02 | Authorization is enforced at the trusted boundary | Send authorized test requests across actors, actions, and resources; verify denied operations leave protected state unchanged. |
| S03 | Untrusted data cannot cross execution boundaries unsafely | Trace inputs to relevant execution sinks; use safe probes to assess context-correct encoding, sanitization, or parameterization. |
| S04 | Authentication and session lifecycle match the architecture | Check login, expiry, logout, replay, transport, and storage against the documented session lifecycle. |
| S05 | Feature-specific attack surfaces have appropriate controls | Assess applicable CSRF, CORS, upload, public-endpoint, and abuse risks separately, with evidence and limits for each surface. |
| S06 | Threats and trust boundaries are explicitly assessed | Connect assets, actors, data flows, and trust boundaries to ranked threats, verified mitigations, and residual risk ownership. |

Security probes require authorized environments and test identities. These scoped checks do not establish comprehensive security or ASVS conformance.

</details>

<details>
<summary><strong>Performance &amp; Resilience — Does the app stay usable under delay, repetition, and failure?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| P01 | Core tasks are not blocked by runtime failures | Execute essential tasks and correlate blocking crashes or exceptions with logs, requests, and reproducible steps. |
| P02 | Network failures resolve into truthful, recoverable states | Inject offline, timeout, and server-error conditions; inspect retained input, committed state, and safe retry behavior. |
| P03 | Loading and interaction meet agreed performance targets | Evaluate applicable field Core Web Vitals and agreed task budgets; retain distributions and distinguish field evidence from local diagnostics. |
| P04 | Repeated usage does not accumulate unintended resources | Measure resources across repeated task cycles; identify unintended listeners, timers, requests, or retained objects against expected lifecycles. |
| P05 | Expected load and data volume meet agreed budgets | Run authorized scenarios against predeclared latency, error-rate, and resource budgets; record environment differences. |
| P06 | State recovers consistently after interruption | Exercise disconnect/reconnect and protocol-permitted duplicate, missing, or reordered events; compare client/server state with the recovery contract. |

Local timings do not establish field performance, and load budgets must be agreed for the app.

</details>

<details>
<summary><strong>Deployment &amp; Operations — Can the app be started, diagnosed, and recovered?</strong></summary>

| ID | Criterion | What to establish |
| --- | --- | --- |
| O01 | Build and startup are reproducible | Follow documented dependency and configuration steps from a clean checkout; retain versions, command output, and a startup/smoke result. |
| O02 | Deployment configuration matches the runtime environment | Verify environment variables, URLs, public/private configuration, connectivity, and storage assumptions in the target runtime. |
| O03 | Important data has an appropriate preservation strategy | Match preservation to acceptable loss and ownership requirements; distinguish exports from automated backups and retain a test-copy manifest. |
| O04 | Failures can be detected and investigated | Trigger a scoped failure and trace its detection, diagnostic information, and delivery to a responsible owner. |
| O05 | Recovery and rollback procedures are verified | Exercise applicable restore and release rollback procedures in isolation; verify data, schema compatibility, elapsed time, and smoke results. |
| O06 | Operational objectives are defined and measured | Check agreed service objectives, recovery time, and acceptable data loss against measurement windows, owners, and response rules. |

</details>

## What evidence looks like

**A “Saved” message is the starting point.** In an illustrative save workflow, the audit checks whether the operation completed and reads the value independently (F01/F03), verifies retention across the required reload or reopen (F02), and repeats the submission to check for unintended duplicates (F05). If a required observation cannot be made, that check stays unknown.

The same principle applies across groups: a hidden button does not establish authorization enforcement, and a written restore procedure needs an actual recovery check before it can pass.

## What an audit delivers

- **Traceable findings:** criterion IDs, expected and observed behavior, reproduction steps, and linked evidence with environment and observation time.
- **Explicit coverage:** pass, fail, unknown, and justified not-applicable outcomes; exclusions and deferred checks remain visible.
- **Actionable priorities:** demonstrated failures classified as blocker, important, or improvement, with affected users and conditions.
- **Scoped decisions:** fix, propose, preserve, or investigate, based on evidence, authority, measurable benefit, and proportionality.
- **Verified corrections:** before/after evidence, a repeat of the original check, and relevant neighboring checks after an authorized fix.

Missing access, tools, requirements, or representative participants limits the conclusion. A validated report checks structure and evidence links; reviewers still need to assess whether the evidence supports each claim.

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
