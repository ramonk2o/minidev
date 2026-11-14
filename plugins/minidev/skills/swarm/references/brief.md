# Worker brief

The message that starts each worker (`../SKILL.md`, 4. Start the workers). Fill in the brackets; drop a line that doesn't apply. Write it in English, short: everything the worker needs is in its skill and the project's CLAUDE.md, so the brief carries only what this batch decided.

```
You are one worker of a minidev swarm; another session (the orchestrator) coordinates it.
Work on <item: #number or the BACKLOG.md entry's title> with the minidev `<build | fix | chore>` skill, in this worktree only, on the branch that skill names.

Approved in advance: the user approved your start message with these decisions, already recorded in the item: <decisions, one line each>. They accept every assumption you adopt that follows them. Wherever your skill says to wait for the user, go on; list what you would have asked in your next report. Things to check by hand go in your final message (the pull request's body), not in a stop.

Files you may change: <paths>. Avoid: <paths: the other items' files>. If the work needs a file you must avoid, stop and report.

Setup before the first test run: <install command>; <environment file: copy from where>; <test database: its own, named after the branch, created how>.

Never: run database migrations (<the project's migrate command>) or start the development server; push the main branch or force-push; delete or rewrite anything outside this worktree and branch. <The item's own limits, if any.>

Report to the orchestrator in at most three lines when: the tests are written, the implementation is done, the review is done, and the work is ready to merge (with the pull request's link, or the branch in local merge). Report at once when you're blocked. A bug, debt or question outside this item: one line in your next report; don't fix it.

Stop when the work is ready to merge: <pull request mode: the pull request open, checks green, not merged | local merge: the verification commit on the branch, not merged>. When the orchestrator says "your turn": bring the main branch into your branch, run the tests, build and lint again, and merge as your skill's Merge and push says for this project's mode<, without pushing the main branch>. Then report, and stop.
```

How the reports travel: a session sends them to the orchestrator as messages; a subagent can only report when it ends, so in that case each milestone report is its final message and the orchestrator continues it for the next stage (the merge cue included).
