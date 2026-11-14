---
name: checkup
description: Check the health of a project set up for the minidev cycle, looking at what no single change's review can see, debt that piled up and architecture decisions that turned out wrong. It collects numbers from the change history, the test suite and the dependencies, starts independent auditors (the architecture as built against as decided, decisions that get expensive to reverse and what breaks as the product grows, the backlog against the structure, documents and tests against the code) and a refuter that tries to knock each finding down, then gives a verdict per area, compared with the last check-up, and records the findings the user approves in the backlog. It changes no code. One message at the start shows what will run and what the last check-up cost. Run only when the user invokes it, optionally with "numbers" to stop at the numbers (e.g. "/minidev:checkup", "/minidev:checkup numbers").
disable-model-invocation: true
argument-hint: "[numbers]"
---

# Check-up

Answers one question: is the software solid so far? Every change in the cycle is already tested and reviewed on its own (`build`, `fix`, `chore`), but a review sees one diff. Technical debt and a wrong architecture decision don't show in any diff. They show in the sum: files every change has to touch, fixes that keep landing in the same place, a backlog the structure can't take. The check-up looks only there, so they're noticed while they're still cheap to undo.

It reads and reports. It changes no code and fixes nothing: a finding the user approves goes to the backlog through `document`, and `chore`, `fix` or `build` do it later. Checking all of SPEC.md against the code is `document`'s spec audit, and pruning the test suite is `chore`'s; the check-up only says when one is due.

A check-up starts up to five agents, each reading the project in its own context, three of them on Opus. That's worth it every ten changes or so, not after each one, and the start message (step 3) shows what the last one cost before anything is spent.

Talk to the user in the language of the conversation.

## When to run

A check-up is due when about ten changes reached the main branch since the last one, or before a release that others will build on. A change is a commit that touches something other than a Markdown file, so the cycle's document commits (an idea noted, a feature set In progress, the check-up's own record) don't count: `git rev-list --count --first-parent <CHECKUP.md's Commit>..<main branch> -- . ':(exclude)*.md'` (with no CHECKUP.md, leave out the commit and `..`). CHECKUP.md's Commit is itself the last such change the check-up read, since a document commit may still be rewritten before it's pushed.

## 1. Check

1. The project uses the cycle, as `build` checks it (`../build/SKILL.md`, 1. Start). If not, offer `/minidev:setup` and stop.
2. The check-up reads the main branch, clean and up to date (`../build/references/git-flow.md`, The main branch). With uncommitted changes, or on a branch with commits of its own, say so and stop: a half-done change would be judged as if it were the product. A session branch with no commits beyond the main branch (a worktree the app made, with the main branch checked out in another folder) holds the same code. Bring the main branch up to date in its own folder (`git -C <its path>`; if that folder has uncommitted changes, stop and ask, since step 7 writes there), bring the session branch level with it (`git merge --ff-only <main branch>`) and go on.
3. From the project's CLAUDE.md, note the test command and where the backlog is: `BACKLOG.md`, or GitHub issues (`Backlog: GitHub issues`). With issues, `gh` must be signed in (`gh auth status`); if it isn't, the Backlog area can't run, and the start message says so.
4. If the project has a `CHECKUP.md`, read it as `references/checkup-file.md` says (Reading it): it's the last check-up. For each finding it has as Recorded, see whether its entry is still open (in BACKLOG.md, or `gh issue view <number> --json state`).
5. If the session can't start agents, only the numbers run: the start message says so.

## 2. The numbers

These need no judgment: run, copy the output and set it beside the last check-up's.

- **Change history:** from the project's root, `python3 "${CLAUDE_PLUGIN_ROOT}/skills/checkup/scripts/history.py" --since <CHECKUP.md's Commit>` (no `--since` on a first check-up). It only reads git, counts changes as When to run does, and prints the project's size, the files that change most, the folders where fixes concentrate and the files in different folders that change together. Without Python 3, skip it and say so: the auditors still run, with no history to start from.
- **Test suite:** run the test command once; note how long it took and the runner's counts, skipped tests included. If it fails, stop and show the user: a main branch that doesn't pass is `fix`'s work, and it comes before a check-up. A suite that can't start because nothing is installed (a fresh worktree) isn't that: offer to run the install command first.
- **Dependencies:** the stack's own commands that list outdated packages and known vulnerabilities (`npm outdated` and `npm audit`, `pip list --outdated`, `cargo outdated`…), only the ones that read. One that isn't installed or can't run is skipped and named; a non-zero exit that comes with a list is its answer, not a failure.
- **Code graph:** if the project already has one (a `graphify-out/` folder, for example), note its path for the auditors. Don't build one.

## 3. The start message

The one stop before anything is spent. With `numbers` as the argument, show the numbers (the table below and the script's tables), say whether a check-up is due (When to run) and end here; nothing is written.

Show, in one message:
- the numbers in a short table, each beside the last check-up's, and how many changes reached the main branch since;
- what will run: one auditor per area of `references/areas.md` and the refuter, each with its model:
  - Architecture, Decisions and growth, and Backlog: Opus, because they're judgment about structure;
  - Documents and tests, and the refuter: Sonnet;
  - with less than about 5,000 lines of code (the history script's Size), Architecture and Decisions and growth run as one auditor with both briefs: one reading of a small project serves both;
- an area that can't run, and why;
- the last check-up's Cost, as CHECKUP.md has it; on a first check-up, that it hasn't been measured for this project yet;
- that nothing is written until the report is approved (step 6).

Then ask, with the question tool when there is one, in the user's language (recommended option first):

**Run:** the full check-up / only the numbers, ending here / the full check-up with every agent on Sonnet (cheaper; the three judgment areas lose depth).

If the environment can't choose a model per agent, they run on the session's model: say that instead of the models.

## 4. The auditors

Note `git rev-parse HEAD` and `git status --short` (the suite's run may have left caches). Start every auditor at once, each as the `auditor` agent (agent type `minidev:auditor`) on its model, with this prompt, filled in and nothing added:

```
Area brief:
<the area's section of references/areas.md, copied in full; both sections when two areas run as one>

Numbers:
<the history script's output, the suite's time and counts, the dependency commands' output; "not collected: <why>" for a missing one>

Code graph: <its path, or "none">
Backlog: <"BACKLOG.md", or "GitHub issues: gh issue list --state open --limit 200 --json number,title,labels,createdAt,body">
Rules (Documents and tests only):
<the Each rule section of ../document/references/spec-audit.md, and the list of patterns in the Patterns of useless tests section of ../build/references/test-value.md, without its paragraph on skipped tests, which tells its reader to enable them>

Earlier check-ups, every area:
<from CHECKUP.md: the findings Recorded whose entry is still open, the ones Handed over and Declined, and the Refuted lines, each as written with its area; or "none">
```

The two rule sections are copied, not pointed to: an agent may not be allowed to read files outside the project. Every auditor gets the earlier findings of every area, since a problem filed under one area is often visible from another. Don't pass the conversation or your own view of what's wrong: an auditor told what to find finds it. Wait for the reports, which arrive on their own. When the environment shows each agent's tokens as it returns, note them for the Cost.

When they have all returned, check that they left nothing behind: `git rev-parse HEAD` and `git status --short` are as noted. They're told to change nothing, but they have a shell; if something changed, show the user what: put a tracked file back with `git restore`, and leave a new file for them to decide.

## 5. The refuter

Auditors asked to find problems tend to find some, so every finding is challenged before it reaches the user. With no finding at all, skip the refuter. Otherwise start one `refuter` agent (agent type `minidev:refuter`) on Sonnet, with every finding exactly as its auditor wrote it, the `Backlog:` line of the auditors' prompt (so it can open an entry a finding cites), and nothing else: not the numbers, not the Checked sections, not your opinion of any. When it returns, check the repository again, as after the auditors.

Don't filter either report. Every finding reaches the user as written, with the refuter's verdict on it; a refuted one is shown too, in its own list, so the user can bring it back.

## 6. The report

One message, in this order:

1. **The answer,** in one sentence: whether the software is solid so far, and what weighs most.
2. **A verdict per area,** beside the last check-up's. It counts the findings that stand (a weakened one with the weight the refuter left it) and the ones earlier check-ups recorded whose entry is still open: debt that's waiting hasn't gone away. An area that didn't run has no verdict.
   - **Solid:** none of those.
   - **With caveats:** some, none of high weight.
   - **At risk:** one of high weight.

   The weights are the auditor's (`agents/auditor.md`, What counts as a finding).
   A problem more than one auditor reported is one finding. It counts once, in the area whose brief asks for it, with the highest weight that stands, and the report says who else raised it; otherwise one bug puts three areas at risk. A Technical decision, Data model or Constraint of SPEC.md the code no longer follows is Architecture's; a Behavior rule the code contradicts is Documents and tests'. When two briefs still ask for it, it goes to the area of the auditor that weighed it highest.
3. **The findings that stand,** highest weight first: each one's evidence, cost of waiting, what makes it come due, and where it would go (the table below). Then, a line each, the earlier ones still open.
4. **Refuted,** a line each with the refuter's reason.
5. **The numbers that moved** since the last check-up.
6. **Cost:** each agent's tokens, when the environment showed them.

| Finding | Where it goes |
|---|---|
| Code to change while keeping the behavior: a structure to fix, two solutions to merge, a migration, a dependency to upgrade (one with a known vulnerability included) | A Debt entry, for `chore` |
| Behavior that's wrong: a bug an auditor ran into, a vulnerability in the product's own code | A Bug entry, for `fix` |
| A decision to take again, with more than one way out (where the product is going included) | A Debt entry with the options as its open questions, and the offer of an `interview` session to settle it |
| A rule or two with no test | A Debt entry `Missing tests: <area>`, as the spec audit writes it (`../document/references/spec-audit.md`, Each rule) |
| SPEC.md and the code disagree on a rule | Ask which is right, with your recommendation: the code wrong is a Bug entry; SPEC.md wrong is handed over to `document`, as a correction |
| Three or more sampled rules failing in an area | Handed over: the spec audit of that area, with `document` |
| Tests that prove nothing | Handed over: a test prune of those modules, with `chore` |
| Backlog entries to merge, close, correct or put first | Handed over: a backlog clean-up, with `document` |

A handed-over finding gets no entry: its owner does the work whole, and an entry would only repeat the request. Offer to start each right after step 7 (recommended) or leave it for later; CHECKUP.md keeps it as handed over, and the next check-up raises it again if it's still true.

Ask which findings to record: all of them (recommended), some, or none. The user may decline any one, handed-over ones included (its reason goes in CHECKUP.md; with none given, write that), and may bring a refuted one back, which is then recorded like one that stands. The verdicts stay as reported whatever the answer. Say that the answer also approves writing CHECKUP.md, and wait for it.

## 7. Record

When the main branch is checked out in another worktree, do this step from that folder (`../build/references/git-flow.md`, Worktrees); if it has uncommitted changes, stop and ask.

1. With the `document` skill, record each approved finding that gets an entry (its Record a bug or debt for later; as issues when the backlog lives there). The entry's Motivation holds the cost of waiting and what makes it come due; its Description holds what's owed, the evidence, and that it came from the check-up of this date.
2. Write `CHECKUP.md` as `references/checkup-file.md` says: the verdicts, the numbers, the cost, this check-up's findings with their Status and refuted ones, and what it carries over from the last file.
3. Commit CHECKUP.md alone on the main branch ("Check-up: <date>, <the verdicts in a few words>"). Like `document`'s commits, it isn't pushed on its own: it goes out with the next change (`../document/SKILL.md`, Commits).

End with one line: what was recorded and the step you'd take first (the highest-weight finding, with its skill). A hand-over or an interview the user accepted starts now, with its own skill.
