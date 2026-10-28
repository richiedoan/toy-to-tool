# Missing access and tools

Read when a capability needed by a selected criterion is unavailable. Use the following common rule: record the attempted check, missing capability and affected criterion IDs in a sanitized evidence artifact; link it from the report's unknown rows; complete independent checks. Do not mark an absent tool or account as an absent app feature. Do not repeatedly retry an unchanged access failure.

Ask for help only if it unlocks an important decision or a priority task and no already-authorized route exists. Explain exactly what remains unverified and offer the smallest useful route. Otherwise deliver the bounded audit with a clear next action. Stop only the dependent test/action, not the entire audit.

## Browser unavailable

First inspect available browser tools and the target's documented browser-test setup. Use an already-configured alternative that can establish the required behavior, such as the project's browser automation. Do not install a new system browser or add target dependencies just to complete a checklist without applicable authority.

Continue source inspection, applicable unit/integration/API tests and reproducible build checks. Preserve their actual scope. A genuine static violation can be reported as fail when the contract and source trace sufficiently demonstrate it; state that runtime reproduction is pending. Reading CSS or running unit tests does not establish visible layout, keyboard behavior or actual rendered contrast.

| Affected checks | What remains unknown without adequate browser evidence | Useful next route |
| --- | --- | --- |
| U01-U03, U05 | Actual screen hierarchy, relevant rendered states, layout and cross-screen behavior | Existing browser automation or a target-device session with reproducible recordings |
| A01-A06 | Unobserved keyboard/focus behavior, accessibility tree, real contrast, resize/reflow and hit geometry | Supported browser with the required inspection/measurement capabilities |
| F01-F03, U04, P01-P02 | UI portions of end-to-end operation, feedback, recovery and runtime behavior | Run browser workflow alongside independent authoritative state checks |
| U06 | Target-user task outcomes | Real participants and the agreed protocol; agent/browser automation is not user research |
| P03 | Field CWV, even if local browser measurements later become possible | Adequate relevant field measurements; lab results remain diagnostics |

Apply this table only to selected, relevant checks. Existing authentic evidence may support a narrower conclusion if its build, environment and scope match; explain its limits. Screenshots alone cannot establish keyboard completion or actual data persistence.

Suggested question when browser access blocks a priority task: “I can check code and APIs now. To verify the user-facing flow, can we use the existing browser test setup or an authorized test URL?” Do not claim success if neither route is available.

## Runtime, dependencies or environment unavailable

Inspect declared versions, setup instructions, configuration variable names and available local/test services. If the task authorizes ordinary local setup, use the declared setup process in an isolated environment with test data. Respect package/network restrictions. Do not guess production configuration, print secret values or silently replace the real backend with a mock.

If setup fails, save the command, sanitized error, tool versions and the point where execution stopped. Distinguish two cases:

- A documented build/startup step reproducibly fails under its declared supported conditions: this can be an O01 failure with evidence and contextual severity.
- The declared runtime/service cannot be obtained or accessed in the agent's environment: the blocked O01 execution is unknown, and dependent runtime checks stay unknown. This is not proof that the app is broken.

F01-F03 and P01-P02 often need actual operation; F02 and O02 need the specified persistence/deployment transitions. Inspecting files or starting a mock does not establish those results. Unavailable staging, backups or isolated recovery targets leave dependent O02/O05 checks unknown. Continue other valid checks; never run a destructive restore or load exercise against production as a fallback.

If only the audit engine's Python/dependencies are unavailable, record that schema/semantic validation was not run. Continue an English manual report using the actual catalogue fields and mark validation pending; do not describe the report as validated. The engine setup is documented in the repository README.

Suggested question when a missing environment blocks a priority task: “The declared service is unavailable, so I cannot verify saving and reopening data. Is there an authorized local or staging environment we can use?” Ask only after inspecting available setup information.

## Credentials or roles unavailable

Check for an already-authorized authenticated tool/session and documented test identities without extracting credential values. Use existing access only within its granted scope. Prefer a scoped test account or a user-established session; never request passwords, tokens or production secrets in chat or save them in reports.

Without the required access:

- S02 needs the relevant A/B and anonymous cases. One valid account does not prove cross-user authorization; record the covered cases and leave the overall criterion unknown if a relevant case is untested and no failure is demonstrated.
- S04 requires the actual applicable login, expiry and logout lifecycle. Public pages or a fake identity do not establish it.
- Protected F01/F02 workflows and O02/O03/O05 operational checks remain unknown where their needed resources cannot be reached. Continue public/anonymous and source checks where permitted.
- S01 may be evaluated on accessible surfaces only, with all uninspected authorized surfaces disclosed. Do not obtain broader secret/history access without need and authorization.

A missing credential never proves authentication or protected resources are not applicable. If a forbidden anonymous test request unexpectedly reveals a protected test resource, that observed failure can be reported with its real severity; missing other accounts does not erase it.

Suggested question: “To check whether users can access each other's records, I need two scoped test identities. Can you provide an authorized test-session route, or should I hand over those exact checks as unverified?” Do not repeat the question after the user chooses a bounded audit.

## Evidence for a limitation

Record a real observation of the limitation rather than inventing an app result. A suitable artifact includes:

```text
Evidence ID: E-access-01
Criterion IDs: F01, F02, S02
Environment/build: the actual inspected revision and available environment
Attempt: the real command/tool/access check, or why an unauthorized attempt was not made
Observed limitation: exact unavailable resource, with secrets redacted
Covered subcases: actual completed source/public checks, if any
Unexecuted subcases: protected create/read, relogin retention, cross-user request
Conclusion boundary: no pass claimed for these unexecuted checks
Next action: scoped test sessions and the named readback route
```

In JSON, register this as a non-synthetic observation/artifact with an actual capture time and existing file location. Link `E-access-01` from each affected unknown row, use null severity, `investigate`, and `evidence_sufficient: false`. The artifact establishes why a check is unverified, not that app behavior is correct. For a not-applicable conclusion, provide separate architecture/requirement evidence establishing genuine absence.
