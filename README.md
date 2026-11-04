# Toy to Tool Agent Skills

**Help your coding agent check whether people can rely on your app.**

Toy to Tool gives Codex, Claude Code, Gemini CLI, and other compatible coding agents a structured way to test real workflows, document what breaks, and verify fixes. Use it to check the details people depend on every day: saving their work, keeping data private, recovering from failed requests, and restoring important data.

**7 skills · 6 quality areas · 36 criteria**

[Explore the criteria](#the-36-criteria) · [See the recorded checks](#evidence-and-limitations) · [Install the skills](#quick-start)

## The questions behind a working screen

These examples illustrate the kinds of checks the skills guide. They are not findings from a particular app.

| What appears to work | What the audit checks |
| --- | --- |
| The app says “Saved.” | Can the saved value be read independently, and does it survive reopening when required? |
| A protected button is hidden. | Can a user without permission still perform the action through a direct request? |
| A failed request offers “Retry.” | Does retrying recover safely, or create a duplicate? |
| The page looks good on a laptop. | Can someone complete the same task on a supported phone screen or with a keyboard? |
| The app starts on your machine. | Can a clean checkout start by following the documented setup? |
| A recovery procedure exists. | Has someone exercised it and checked the recovered data? |

## Example: saving on an unstable connection

Suppose a tracker should save each new task once and keep it after reopening. A request reaches the server, but the connection drops before the browser gets the response. The user clicks Retry.

The audit follows the whole task:

1. Create a task with a unique test value and interrupt the response.
2. Check what the interface tells the user and whether their input is retained.
3. Inspect the stored data to find out whether the first save completed.
4. Retry, then count the resulting records and compare their values.
5. Reopen the app and check that the expected task is still there.

This connects real operation results (**F01**), required persistence (**F02**), accurate feedback (**F03**), repeated actions (**F05**), and network recovery (**P02**). The agent records which steps ran and what each one showed. If it cannot inspect the stored result, that part stays **unknown**.

This is an illustrative scenario. The exact checks depend on what your app promises to do.

## What the skills cover

Start with `toy-to-tool-audit` for a coordinated review. It establishes what the app needs to do, chooses the checks that apply, and brings the results together. Choose a specialist when you want to focus on one area; each can run independently.

| Specialist | Criteria | What it evaluates |
| --- | --- | --- |
| `functionality-data` | F01–F06 | Real workflow outcomes, required persistence, truthful feedback, input rules, repeated actions, concurrent updates |
| `ux-visual-quality` | U01–U06 | Screen purpose, interface states, responsive task access, mistake recovery, consistent patterns, evaluation with target users |
| `accessibility` | A01–A06 | Keyboard operation, names and semantics, contrast, zoom and reflow, visible focus, pointer targets |
| `security-privacy` | S01–S06 | Sensitive data exposure, authorization, unsafe execution, sessions, feature-specific attack surfaces, trust boundaries |
| `performance-resilience` | P01–P06 | Runtime failures, network recovery, performance targets, resource accumulation, expected load, interrupted-state recovery |
| `deployment-operations` | O01–O06 | Reproducible startup, runtime configuration, data preservation, failure diagnosis, verified recovery and rollback, operational objectives |

## The 36 criteria

**36 criteria, each with a test protocol and evidence requirements.** Every criterion explains when it applies, what to test, what evidence to keep, how to judge the result, and how to verify a fix.

Essential covers core outcomes and basic risks. Standard adds everyday usability and quality checks. Advanced goes further into concurrency, load, user evaluation, and operational needs where they apply. The scope follows your app's requirements and features.

Expand a group to see the checks. The [canonical catalogue](criteria/v1.json) contains the full protocols and starting level for each criterion.

<details>
<summary><strong>Functionality &amp; Data — Do tasks produce the promised results?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| F01 | Core workflows perform real operations | Complete the main tasks, then inspect the saved result or output independently. Record where the app deliberately uses demo or mock behavior. |
| F02 | Data persists according to the agreed requirements | Check the data before and after the refresh, reopen, login, device, or deployment changes the app promises to support. |
| F03 | UI feedback reflects actual operation outcomes | Compare loading, success, and error messages with what actually happened. If the UI updates early, check that it corrects itself when the operation fails. |
| F04 | Inputs follow the application's data rules | Try valid, invalid, and boundary values. Check the stored result and whether rules also hold at the server when there is one. |
| F05 | Repeated actions do not create unintended side effects | Repeat a submission or retry a request. Check that record counts and other effects match the rules for that operation. |
| F06 | Concurrent updates follow an explicit consistency rule | Update the same data from separate sessions. Check how conflicts are handled, what each user sees, and which values are finally saved. |

</details>

<details>
<summary><strong>UX &amp; Visual Quality — Can people understand and complete the task?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| U01 | Users can identify the screen purpose and primary action | Check whether the purpose, labels, and main action fit the intended task. Identify which conclusions come from expert review and which come from users. |
| U02 | Relevant interface states are complete and actionable | Trigger loading, empty, success, error, and disabled states. Check that people can understand what happened and what to do next. |
| U03 | Layout does not obstruct essential tasks | Try supported screen sizes. Check that clipping, overlaps, or overlays do not block the content and controls needed to finish a task. |
| U04 | Users can prevent, correct, and recover from mistakes | Try input mistakes, cancellation, back navigation, and destructive actions. Check that prevention and recovery match the consequences. |
| U05 | Visual and interaction patterns are consistent | Compare text styles, spacing, colors, controls, labels, and behavior across screens. Check differences against the agreed design and any intentional exceptions. |
| U06 | Important workflows are evaluated with target users | Have real target users try representative tasks against goals set in advance. Keep deidentified observations and explain the limits of the sample. |

</details>

<details>
<summary><strong>Accessibility — Can people operate the essential workflows?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| A01 | Essential workflows are keyboard accessible | Complete essential tasks with a keyboard. Check focus order and places where focus gets trapped, accounting for applicable standard exceptions. |
| A02 | Controls have appropriate names and semantics | Inspect control names, roles, labels, and states in the accessibility tree and with assistive technology. Check that they describe each control accurately. |
| A03 | Text contrast meets applicable minimum requirements | Measure text against its actual background: at least 4.5:1 for normal text and 3:1 for large text, with applicable standard exceptions documented. |
| A04 | Zoom and reflow preserve content and functionality | Resize text to 200% and test reflow at the dimensions required by the standard. Check that content and tasks remain usable; document exceptions. |
| A05 | Keyboard focus is visible and not entirely obscured | Move through the interface with a keyboard. Check that focus is visible and that page content does not entirely hide the focused control. |
| A06 | Pointer targets have sufficient size or spacing | Measure clickable areas and spacing against the 24 × 24 CSS pixel requirement, or document the applicable standard exception. |

These six criteria reference WCAG 2.2 requirements; they do not establish full WCAG AA conformance.

</details>

<details>
<summary><strong>Security &amp; Privacy — Do data and actions stay within authorized boundaries?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| S01 | Secrets and sensitive data are not unintentionally exposed | Check what reaches public files, responses, and other exposed surfaces. Compare it with the intended audience and keep secrets out of the evidence. |
| S02 | Authorization is enforced at the trusted boundary | Use authorized test accounts to request protected actions and records directly. Check that forbidden requests are denied and leave protected data unchanged. |
| S03 | Untrusted data cannot cross execution boundaries unsafely | Follow untrusted input to places where it could become executable content or commands. Use safe probes to check the relevant encoding, sanitization, or parameterization. |
| S04 | Authentication and session lifecycle match the architecture | Check login, expiry, logout, reuse of old sessions, transport, and storage against the session behavior required by the architecture. |
| S05 | Feature-specific attack surfaces have appropriate controls | Check relevant CSRF, CORS, file upload, public endpoint, and abuse risks separately. Record which surfaces apply, the results, and what remains untested. |
| S06 | Threats and trust boundaries are explicitly assessed | Map important data, users, data flows, and trust boundaries. Connect threats to tested protections and identify who owns the remaining risks. |

Security probes require authorized environments and test identities. These scoped checks do not establish comprehensive security or ASVS conformance.

</details>

<details>
<summary><strong>Performance &amp; Resilience — Does the app stay usable under delay, repetition, and failure?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| P01 | Core tasks are not blocked by runtime failures | Run essential tasks and investigate crashes or exceptions that block completion. Keep the steps, logs, and requests needed to reproduce them. |
| P02 | Network failures resolve into truthful, recoverable states | Simulate offline, timeout, and server errors. Check the message, retained input, saved result, and whether retrying is safe. |
| P03 | Loading and interaction meet agreed performance targets | Compare loading and interaction measurements with applicable field Core Web Vitals and agreed task targets. Keep field results separate from local measurements. |
| P04 | Repeated usage does not accumulate unintended resources | Repeat tasks and track resources over time. Look for listeners, timers, requests, or retained objects that accumulate beyond their intended lifetime. |
| P05 | Expected load and data volume meet agreed budgets | Test agreed user loads and data volumes in an authorized environment. Compare response times, errors, and resource use with targets set before the test. |
| P06 | State recovers consistently after interruption | Disconnect and reconnect. Where the protocol allows, test duplicate, missing, or reordered events and compare client and server data with the expected recovery behavior. |

Local timings do not establish field performance, and load budgets must be agreed for the app.

</details>

<details>
<summary><strong>Deployment &amp; Operations — Can the app be started, diagnosed, and recovered?</strong></summary>

| ID | Criterion | What the audit checks |
| --- | --- | --- |
| O01 | Build and startup are reproducible | Start from a clean checkout and follow the setup instructions. Record tool versions, commands, and whether the app starts and completes a basic task. |
| O02 | Deployment configuration matches the runtime environment | Check environment variables, URLs, public and private settings, connectivity, and storage behavior in the intended runtime. |
| O03 | Important data has an appropriate preservation strategy | Identify data that matters, how much loss is acceptable, and who is responsible for preserving it. Distinguish exports from scheduled backups and record a test copy. |
| O04 | Failures can be detected and investigated | Trigger a controlled failure. Check whether it reaches a responsible person with enough diagnostic information to investigate. |
| O05 | Recovery and rollback procedures are verified | Try applicable data restore and release rollback procedures in isolation. Check recovered values, schema compatibility, elapsed time, and basic app behavior. |
| O06 | Operational objectives are defined and measured | Check that service targets, recovery time, and acceptable data loss have defined measurement periods, owners, and response rules. Review measurements against those targets. |

</details>

## What you get back

A report ties each finding to the relevant criterion, the steps that ran, the observed result, and supporting evidence. It explains who is affected, how serious the problem is, and what would prove a fix worked. Checks that could not run remain visible as unknown; exclusions and deferred checks are listed separately.

For example, a finding from the scenario above might look like this. **This is an illustrative report excerpt, not a recorded result.**

| Field | Example |
| --- | --- |
| Finding | Retrying after a lost response creates a second task. |
| Criterion | F05 — Repeated actions do not create unintended side effects. |
| Conditions | The first save commits, its response is interrupted, and the user retries. |
| Expected / actual | One saved task / two records with the same submitted value. |
| Reproduction | Save a unique task, interrupt the response, retry, then inspect stored records. |
| Evidence to attach | Request sequence, UI observations, and an independent record count with environment and capture time. |
| Severity | Important in this example: duplicated ordinary tasks need manual cleanup. More consequential duplicate effects could warrant a blocker. |
| Verification after a fix | Repeat the interruption and retry; verify one record, reopen the app, and check a normal save still works. |

### Inspect → Improve → Recheck

1. **Inspect:** agree on the important tasks and audit scope, run applicable checks, and keep evidence of results and gaps.
2. **Improve:** make the smallest authorized fix for a demonstrated problem. Propose changes that need a product or scope decision; preserve behavior that already meets the requirements.
3. **Recheck:** repeat the original check and relevant neighboring tasks. Keep before/after evidence so the result can be reviewed.

You can request an audit without code changes, or allow fixes within a stated scope. Missing requirements or evidence lead to further investigation.

## Evidence and limitations

The repository includes recorded fixture checks and installation verification you can inspect:

| Record | What it contains |
| --- | --- |
| [Tracker workflow](evaluation/evidence/tracker-v1/workflow.md) | A Functionality & Data trial, with before/after reports and browser checks recorded separately from the agent's restricted-runtime attempt. |
| [Owner-notes and dashboard trials](evaluation/evidence/expansion-v1/workflow.md) | Security, UX, accessibility, performance, and operations observations, with HTTP/browser rechecks, preservation evidence, and unexecuted checks identified. |
| [Installation verification](evaluation/evidence/release-v1/verification.md) | Skill discovery, copied installation, explicit Codex invocation on macOS, bundled resource integrity, and a bounded fixture recheck. |

These records show the workflows exercised in those environments. They do not establish a general improvement in coding-agent performance; the [controlled comparison](docs/comparison.md) has not been run. Other agents and platforms remain unverified.

The 36 criteria define a scoped audit, not comprehensive certification. Browser, assistive-technology, load, and recovery conclusions need the corresponding real checks. The report validator checks structure and evidence links; a reviewer still needs to judge whether the evidence supports the conclusion.

See the [specialist guide](docs/skills.md) and [limitations](docs/limitations.md) for the full scope.

## Quick start

Run the command for your agent from your project's directory, then choose which skills to install. Each skill includes its supporting resources.

### Codex

```sh
npx skills add richiedoan/toy-to-tool --agent codex
```

### Claude Code

```sh
npx skills add richiedoan/toy-to-tool --agent claude-code
```

### Gemini CLI

```sh
npx skills add richiedoan/toy-to-tool --agent gemini-cli
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
npx skills add richiedoan/toy-to-tool --agent codex --skill toy-to-tool-audit
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

## Documentation and contributing

- [Installation](docs/installation.md): detailed setup and verified environments.
- [Audit method](docs/method.md): criteria, evidence, and report rules.
- [Contributing](CONTRIBUTING.md): source layout, bundle generation, and validation commands.
- [Evaluation](evaluation/README.md): fixture workflows and retained evidence.
- [Verification record](evaluation/evidence/release-v1/verification.md): installation and invocation evidence.
- [Comparison protocol](docs/comparison.md): controlled evaluation design.

## License

[MIT](LICENSE). External standards retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).
