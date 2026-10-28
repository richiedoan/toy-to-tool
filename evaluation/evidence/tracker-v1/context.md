# Tracker workflow context

This exercise uses disposable, non-sensitive local task data. It is a seeded test fixture, not a production service. Actual Chrome execution produced the browser evidence; observations are not simulated. The initial fixture author knows the intended defects, so evaluator-led browser work is manual workflow verification. An isolated agent attempt is recorded separately and is not an effectiveness comparison.

## Requirements and authority

The fixture README is the agreed contract: add a task, save a note/completion edit, refresh or reopen the same browser origin/profile and recover saved records. Titles are trimmed, 1-80 characters; notes allow up to 500. A pending repeated submission is one intention; a later intentional same-title submission is permitted. Failed writes must not claim success or destroy existing saved data. The tests inspect only the fixture's `task-tracker-v1` localStorage key.

Standard scope includes F01-F05. F06 is deferred: Advanced concurrency is not selected, and simultaneous tab editing is excluded by the fixture contract. All other criterion groups are outside this focused trial. Target-code corrections within the existing architecture and regression checks are authorized by the user request. No backend, accounts or synchronization are required.

## Evidence boundaries

Each browser scenario uses a fresh context; refresh/reopen uses the same context and origin within that scenario. Reopen means close/reopen the application tab, not an OS/browser restart or device change. Each result includes actual storage/UI values, timestamps, app source hashes, browser version and reproduction steps. Screenshots and Playwright traces accompany the raw results. Hidden browser assertions are evaluator tools, excluded from the agent packet.

No real users, field metrics, security or load tests were performed. Reports make claims only about the defined F protocols and exercised cases. A passing script assertion is not a global certification or effectiveness score.
