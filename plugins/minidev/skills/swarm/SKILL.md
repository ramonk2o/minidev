---
name: swarm
description: Run several backlog items of a project set up for the minidev cycle in parallel, one worker per item in its own worktree, each through build, fix or chore, then bring them into the main branch one at a time. Every choice is made in one message at the start, with defaults filled in; after the OK the batch runs to the end without stopping. Run only when the user invokes it, optionally with item numbers or a label (e.g. "/minidev:swarm 12 15", "/minidev:swarm bugs").
disable-model-invocation: true
argument-hint: "[item numbers | label]"
---

# Swarm

Runs a batch of backlog items to the main branch in parallel. This session is the orchestrator: it picks the batch, decides each item's open points, starts one worker per item, cues the merges one at a time and reports. It never writes the items' code. Each worker runs `build`, `fix` or `chore` as they are, in its own worktree; their steps, checks and merge live there, not here.

## The orchestrator's job

You are the orchestrator, and the batch's outcome is yours. Workers do the items; you answer for the whole. When the batch ends, each item is on the main branch and works, or is left out with a reason the user can act on. A worker that says it's done hasn't made the batch a success; the main branch passing its tests, build and lint after the last merge has.

Weigh every decision by these, in this order:
1. **Safety:** nothing outside the limits (step 3), nothing the main branch can't take back. When in doubt, the option that can be undone.
2. **The result:** each item correct and complete, as its skill checks it, and the items still correct together.
3. **Efficiency:** the tokens and time the batch spends (below).
4. **The user's attention:** they approved the batch so they wouldn't be stopped. Decide, record the decision, report it in a line.

Check a worker's claim when the check is cheap (a pull request's checks, the main branch's last commit, the suite after a merge), not by rereading its work.

A batch multiplies what the session spends, and on a small plan every worker draws from the same usage limit. So the defaults are small and the orchestrator stays lean:
- At most 3 items; 2 by default.
- Workers on the cheapest model their item needs (step 2).
- The orchestrator reads the workers' short reports, never their diffs, test output or logs; it asks a worker for more only when a decision needs it.
- No polling: a worker's report arrives on its own. Wait for it.
- Every update to the user is two lines at most.

Talk to the user in the language of the conversation. Everything written to the repository follows the project's CLAUDE.md (Documents language).

## 1. Check

1. The project uses the cycle, as `build` checks it (`../build/SKILL.md`, 1. Start). If not, offer `/minidev:setup` and stop.
2. From its CLAUDE.md, note: where the backlog is (`BACKLOG.md`, or GitHub issues with `Backlog: GitHub issues`), the integration mode (`../build/references/git-flow.md`, Integration mode), the install, test, build and lint commands, and any setup a fresh checkout needs (environment files, a test database).
3. In pull request mode, whether the main branch requires a review (`gh api repos/{owner}/{repo}/branches/<main branch>/protection --jq .required_pull_request_reviews`, or a pull request's `reviewDecision`): if it does, or the query fails (no admin rights), treat the project as merged by the reviewer here (step 3, Delegation).
4. How workers run: a separate session per item, each in its own worktree, where the environment can start one (in the Claude desktop app); otherwise a background subagent per item with `isolation: worktree`. If neither is available, say so and stop: the items run one after another with their own skill instead.
5. The main branch is clean and up to date (`../build/references/git-flow.md`, The main branch). Uncommitted changes there: stop and ask.
6. If work branches of an earlier batch are left (`feature/`, `fix/` or `chore/` branches and their worktrees, found as `../build/references/git-flow.md` says in Resume), they may be an earlier batch or someone's own work, so don't guess: the start message lists them and asks whether to resume them, with the ones whose worktree's session no longer exists checked by default. The ones the user keeps are the batch. Each one goes back to its worker when that session still exists (a message to it); otherwise a new worker resumes it as its skill's Resume says, after its old worktree is removed (`git worktree remove`, only when it's clean; one with uncommitted changes is someone's work: leave the item out and say so). Go to step 3 with them; at step 4, a resumed item skips 4.1 (its Decisions and status are already written) and gets the brief's resume line.

## 2. Pick the batch

Read the open items: `BACKLOG.md`, or `gh issue list --state open --limit 100 --json number,title,labels,body`. With numbers or a label in the arguments, take only those.

Pick up to the batch size, by priority, by what the current version needs, and by dependencies (an item that needs another waits for a later batch). Leave out:
- items whose files overlap a picked one: estimate each item's files from its entry and a search of the code (`git grep`); two items in the same module don't go in one batch;
- a second item that adds a database migration or changes a schema: at most one per batch;
- items with a work branch or In progress outside a resume (someone's work), and ideas whose key behavior is undecided across several connected decisions (they need an `interview` session, not a decision taken here).

For each picked item, prepare:
- **Skill:** `build` for an Idea, `fix` for a Bug, `chore` for Debt or a behavior-preserving change (always its full path, on a branch: its short paths act on the main branch, which only the merge cue may touch).
- **Decisions:** every open point the item's skill would ask at its start, each answered with the recommendation that skill would give.
- **Files:** the ones it may change, and the ones it must avoid (the other items' files).
- **Model:** Haiku for a chore or a fix of a few lines; Sonnet for the rest; Opus only if the user asks.

## 3. The start message

The batch's one stop. Show, in one message:
- the items picked, each with its skill, model, files and decisions, in a line or two;
- the items left out and why, one line each;
- the limits below;
- in the desktop app, that the workers' git commands on the main branch's folder ask for permission unless the session's permission mode allows them (`setup` leaves them asking).

Then ask, with the question tool when there is one, these questions with these options, in the user's language and without rewording them (recommended option first); otherwise as a numbered list with the defaults filled in, where "OK" accepts them all. Each item's model is part of the batch: changing one is an answer to Batch.
1. **Batch:** as shown / only the first item / other items or models (e.g. "#67 on Opus"). On a resume: the branches found, which to resume.
2. **Delegation:** delegate everything: I judge each item, ask its worker for fixes when something fails, bring it into the main branch when it's good, and don't stop you until the summary / leave each one ready for you (open pull requests, or verified branches in local merge), also without stopping. In a project whose pull requests are merged by the reviewer, there's no question: the start message says the batch ends with the pull requests open and verified.
3. **Updates:** at every milestone / only problems and the end.

The answer is the OK for the whole batch. It stands in for every stop the workers' skills would make for the user (their start messages, their end messages), except one: a worker whose work would change an existing test of current behavior stops and reports, and you decide in the user's place. From here on, take every decision without asking, and record each one where its item keeps its Decisions. Things to check by hand don't hold a merge back: they go to the final summary as pending.

**Limits,** for the orchestrator and every worker, whatever the user approves:
- no migration run against the development database or any database the worktrees share (`db:migrate` and the like), and no development server started in a worktree; a worker may create and migrate its own test database, named after its branch;
- no push to the main branch (with local merge, the main branch stays local until the user pushes it), no force-push;
- nothing destructive outside the worker's own worktree and branch, except the steps its skill's Merge and push runs on the main branch for the project's mode;
- the project's own rules in its CLAUDE.md.

## 4. Start the workers

1. Write each item's Decisions with the `document` skill before its worker starts. With `BACKLOG.md`, also set every feature In progress with its branch name, all in one commit on the main branch, so workers never edit BACKLOG.md on the main branch at the same time (a Bug or Debt entry has no In progress: `document` keeps it as it is until its fix or chore is done). With issues, a feature's worker sets its own issue In progress, as `build` does.
2. Start every worker at once, each with the brief in `references/brief.md` filled in, on its model. Tell the user one line per worker (its name and item).

## 5. While they run

- Pass each worker's milestone to the user in a line (unless the user chose only problems).
- A worker that's blocked, or reports a conflict, a red suite it can't fix or a plan that can't hold: decide the safest way out from its report. When the way out is bigger than the item (a redesign, a change to another item's files), drop the item: the worker commits a checkpoint and stops, its entry goes back to its status with a line on why, and the final summary names it.
- A finding outside an item (a bug, debt, a decision for later) becomes a new backlog entry or issue with the `document` skill, never a fix in that item. Write to the main branch's folder only while no worker is merging (right after the cued worker's report), so your commit never meets its squash.
- Before starting a worker or cueing a merge, check the usage when the environment shows it. Close to the limit, start nothing new: let the running workers reach a checkpoint, then go to step 7. Running `/minidev:swarm` again resumes (step 1.6).

## 6. Bring them in, one at a time

When the user chose to leave them ready, skip to step 7.

Take the workers ready to merge in the order they got ready, except that an item with a migration goes first once it's ready. Cue one worker at a time ("your turn" in the brief): it brings the main branch in, runs the tests, build and lint again, and merges as its skill says for the project's mode. Wait for its report before cueing the next. A worker that can't merge (a conflict outside BACKLOG.md and CHANGELOG.md, a failing check after 3 rounds) is handled as in step 5.

## 7. Final check and summary

If anything reached the main branch, bring the local main branch up to date (`../build/references/git-flow.md`, The main branch) and run the tests, build and lint once there. A failure is a broken merged change. Revert the squashed commit that broke it, as `../build/references/git-flow.md` says (When a merged change breaks, Revert), without asking the user: the batch's OK covers it. Say so in the summary.

Then, in one message:
- what reached the main branch (each item, its pull request or commit);
- the items left out or dropped, and why;
- the entries or issues opened during the batch;
- the decisions taken, one line each;
- what's pending: each item's To check by hand, pull requests left for review, a local main branch the user still has to push, workers stopped by the usage limit and how to resume them.
