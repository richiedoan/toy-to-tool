# Evaluator-only expected findings

Do not include this file, the evaluation harness, baseline labels, reference fixes, earlier reports or this conversation in an evaluated agent's input. `prepare_packet.py` uses a positive allowlist and a fresh Git repository. This document is for evaluating results after a run, not coaching the agent during it. Filesystem separation is a context boundary, not an OS security boundary.

Baseline archive: `evaluation/baselines/tracker-v1.tar.gz`; hashes are in its adjacent manifest. Restore it into a new directory, never over a live app or a user's data.

| Expected behavior violation | Criterion and contextual impact | Independent reproduction |
| --- | --- | --- |
| Save changes says success but does not commit note/completion values | F01 blocker: one of three core tasks is impossible. F03 important: user is given false confirmation. | Add a uniquely titled task, edit its note and completion flag, save, inspect browser-local stored record. Stored values remain empty/false despite confirmation. |
| Existing saved tasks are not loaded on refresh | F02 blocker: the promised reopen task is unavailable. | Add a task, verify a stored record, refresh same origin/profile, compare visible list with store. The store can still contain the record while the app presents none. Further creation risks replacing the unloaded records. |
| Two rapid submissions of one intention create two IDs | F05 important: duplicate records require manual correction. | Dispatch two form submissions before the pending 200ms operation settles. Inspect stored IDs and count; expect one, observe two. A later separately submitted same-title task is allowed and must not be suppressed. |

F04 should be assessed independently, not assumed broken: title trimming, empty and 80/81 boundaries, valid Unicode/punctuation and 500/501 note boundaries. A direct programmatic input can bypass HTML maxlength; the operation still needs its contract. If the agent exposes another evidenced defect, accept it with correct scope and severity rather than forcing the result to match only this oracle.

F06 is deferred at Standard. A single-tab, single-editor contract does not justify imposing an arbitrary cross-tab conflict strategy. Other groups have no assessed outcome in this F-only trial.

Evaluator regression must include genuine storage rejection, input retention, previous-data integrity, delayed truthful feedback, save repeat activation, intentional same-title creation, same-origin reopen and malformed stored-data handling. The original fixture's broken save may cause additional F04/F03 observations; do not count correlated symptoms as independent successes in any future study.

Assess scope discipline too: retaining local storage, avoiding account/database additions, preserving valid titles and making a minimal correction are useful preserve decisions.

The primary implementation session knows these defects because it created the fixture. Its own walkthrough is therefore manual workflow verification. A separate fresh CLI run without these materials is an independent attempt, but neither is a controlled effectiveness comparison. Never claim a skill efficacy gain from this exercise alone.
