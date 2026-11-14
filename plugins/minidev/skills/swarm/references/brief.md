# Worker brief

The message that starts each worker (`../SKILL.md`, 4. Start the workers). Fill in the brackets; drop a line that doesn't apply. Write it in English, short: everything the worker needs is in its skill and the project's CLAUDE.md, so the brief carries only what this batch decided.

```
You are one worker of a minidev swarm; another session (the orchestrator) coordinates it.
Work on <item: #number or the BACKLOG.md entry's title> with the minidev `<build | fix | chore>` skill, in <session: this worktree only | subagent: a worktree you make first, and nowhere else: `git worktree add .claude/worktrees/<branch with / as -> -b <branch> <main branch>` run from the project's folder, then work in that folder (for a resumed item, without `-b <branch> <main branch>`: just `<branch>`)>, on the branch `<branch>`. <a feature, in BACKLOG.md: The item is already In progress on the main branch, naming that branch; the orchestrator set it.> <new item: Create that branch (a session: or rename this worktree's branch to it; a subagent's worktree command already creates it), start the work fresh, and don't set the item's status again. | resumed item: The branch exists from an earlier batch, with its checkpoints: check it out and resume as your skill's Resume says; don't start over.>

Your skill's tester and reviewer run as usual. If you can't start them, stop and report: don't imitate them.

Approved in advance: the user approved your start message with these decisions, already recorded in the item: <decisions, one line each>. They accept every assumption you adopt that follows them. Wherever your skill says to wait for the user, go on; list what you would have asked in your next report. Things to check by hand go in your final message (the pull request's body), not in a stop.

If your work would change an existing test of current behavior (one your skill protects), stop and report which test and why: the orchestrator decides.

Files you may change: <paths>. Avoid: <paths: the other items' files>. If the work needs a file you must avoid, stop and report.

Setup before the first test run: <install command>; <environment file: copy from where>; <test database: its own, named after the branch, created how>.

Never: run migrations (<the project's migrate command>) against the development database or one the worktrees share, or start the development server; you may create and migrate your own test database; push the main branch or force-push; delete or rewrite anything outside this worktree and branch, except what your skill's Merge and push runs on the main branch. <The item's own limits, if any.>

<Session: Report to the orchestrator, as a message of at most three lines, when: the tests are written, the implementation is done, the review is done, and the work is ready to merge (with the pull request's link, or the branch in local merge). Report at once when you're blocked. | Subagent: Your final message is your report, in at most three lines: end your run when the work is ready to merge (with the pull request's link, or the branch in local merge), or at once when you're blocked. The orchestrator continues you with its answer or the merge cue.> A bug, debt or question outside this item: one line in your next report; don't fix it.

Stop when the work is ready to merge: <pull request mode: the pull request open, checks green, not merged | local merge: the verification commit on the branch, not merged>. When the orchestrator says "your turn": bring the main branch into your branch, run the tests, build and lint again, and merge as your skill's Merge and push says for this project's mode<, without pushing the main branch>. Then report, and stop.
```

How the reports travel: a session sends them as messages while it works. A subagent reports only when it ends, so it gets no milestone reports in between, and the orchestrator continues it (by its id) with each answer and the merge cue.
