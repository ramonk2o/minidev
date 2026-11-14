# minidev

A Claude Code plugin with a fixed development cycle, the same in every project: ideas are interviewed until nothing is left open, features are built test-first, checked by an independent tester and reviewed by an independent reviewer, and three product documents keep track of what may come, what exists and what changed.

## Install

In Claude Code:

```
/plugin marketplace add ramonk2o/minidev
/plugin install minidev@minidev
```

To get new versions later: `/plugin marketplace update minidev`.

## First use

New to programming, git or GitHub? You don't need to know the cycle's vocabulary: start with `/minidev:guide`, and call it again whenever you're stuck or don't know what to do next. It looks at your project, says in plain words where it stands and what the next step is, and explains a term (pull request, branch, test-first, spec, backlog) when you ask. It never changes anything by itself.

Before you start, you need:

- **Claude Code**, installed and signed in.
- **git**, the tool that saves the history of your project. Check it with `git --version` in a terminal; if it isn't there, install it from [git-scm.com](https://git-scm.com).
- **A GitHub account and `gh`**, GitHub's command-line tool (see [cli.github.com](https://cli.github.com)), signed in with `gh auth login`. They're needed for the pull-request mode of the cycle; without them the cycle still works, with changes merged locally.

Then, in each project where you want the cycle, `/minidev:guide` will tell you to run `/minidev:setup` once (if you already know the cycle, run it yourself). If its questions (pull requests, where the backlog lives…) don't mean anything to you yet, answer "choose for me": it takes the safe default for each, explains it in a sentence, and tells you at the end how to change any of them.

## What's inside

| Piece | What it does |
|---|---|
| `brainstorm` skill | Starts a new project from an idea: interviews you about the product, decides the architecture and stack with you, picks the first feature, then scaffolds a project whose tests and build already run. |
| `guide` skill | Tells you where your project stands and what to do next, in plain words, and explains a term of the cycle when you ask. Reads only, writes nothing. Runs only when you call `/minidev:guide`; start there if you're new. |
| `setup` skill | Prepares a project for the cycle: git, CLAUDE.md, permissions, product documents. Runs only when you call `/minidev:setup`. |
| `interview` skill | Interviews you about an idea, a round of questions at a time, until nothing is left open. |
| `document` skill | The only writer of `BACKLOG.md`, `SPEC.md` and `CHANGELOG.md`. |
| `build` skill | Builds a backlog feature test-first, then has it checked by the `tester` agent and reviewed by the `reviewer` agent before committing. |
| `fix` skill | Fixes a bug on its own branch, test-first when it can be reproduced, and records it in the changelog when users could see it. |
| `chore` skill | Makes a change that keeps the behavior (refactoring, debt, dependency upgrades, migrations, tooling, typos) on its own branch, with the suite green before and after (a short path for prose-only changes). Also adds missing tests and, on request, prunes useless tests from the whole suite. |
| `swarm` skill | Runs a few backlog items in parallel, one worker per item in its own worktree (each through `build`, `fix` or `chore`), then brings them into the main branch one at a time. Every choice is made in one message at the start; then it runs to the end. Runs only when you call `/minidev:swarm`. |
| `checkup` skill | Checks the project's health as a whole, for what no single change's review sees: debt that piled up and architecture decisions that turned out wrong. Numbers from the change history, the suite and the dependencies, independent auditors, a refuter, a verdict per area and findings for the backlog. Changes no code. Runs only when you call `/minidev:checkup`. |
| `tester` agent | Independent tester: runs the suite, checks every rule is covered, tries to break the feature. Never fixes code. |
| `reviewer` agent | Independent code reviewer: reads the diff for what tests don't catch (risky logic, errors, security, design, leftovers) and checks the change's tests, the product's constraints and that SPEC/CHANGELOG match the code; reports blocking findings and suggestions. Told never to edit. |
| `auditor` agent | Independent auditor for one area of a check-up: reads the code, the documents and the history for what built up across changes, and reports only findings with evidence, a cost of waiting and what makes it come due. Told never to edit. |
| `refuter` agent | Independent refuter: gets only the auditors' findings and where the backlog is, opens the evidence each one cites and tries to knock it down; reports which stand, which are weakened and which are refuted. Told never to edit. |

You don't need to call `interview`, `document`, `build`, `fix` or `chore` by name. Just talk ("note this idea…", "let's build X", "X has a bug…", "release 1.2.0"): the CLAUDE.md written by `setup` tells Claude which skill each step uses. The steps themselves live in the skills, not in that CLAUDE.md, so updating the plugin updates every project.

## How the cycle works

```
 idea ──► interview (if behavior is open) ──► BACKLOG.md: Idea
                                                  │
                                                  ▼
                                   build: critical test list, open points
                                   and size in one message ──► your OK
                                                  │
                                                  ▼
                                   new branch feature/<name>
                                                  │
                                                  ▼
                                   tests first (shown failing) ──► code
                                                  │
                                                  ▼
                                   tester agent ◄──► fixes (a new tester for each round with failures)
                                                  │
                                                  ▼
  refactor ──► check the tests ──► SPEC + CHANGELOG, entry leaves BACKLOG ──► reviewer ──► fixes
                                                  │
                                                  ▼
                       verification commit: code, tests and documents
                                                  │
                                                  ▼
                                   you confirm the tester's assumptions and check by hand what tests can't
                                                  │
                                                  ▼
             pull request, squash-merged once the checks pass
     (off GitHub: main merged into the branch, test ──► squash into main, push)
```

The steps and their rules live in the skills; this is the map. Each step says which file to read for the detail.

### 0. Brainstorm (new projects only)

In an empty folder, describe the idea. `brainstorm` interviews you with the `interview` skill, in rounds, product first and stack second, each question with a recommended answer, then splits the first version into features in build order, scaffolds a project whose tests and build already run, and records the features in `BACKLOG.md` and the technical decisions in `SPEC.md`. No feature code is written. Then run `/minidev:setup`. Detail: `plugins/minidev/skills/brainstorm/SKILL.md`.

### 1. Setup (once per project)

`/minidev:setup` proposes, in one message: git, a `CLAUDE.md` with the project's real commands and conventions and the integration mode (pull requests when the project is on GitHub, merged by you or by the reviewer; local merge otherwise), a GitHub repository when the project has no remote (private unless you say otherwise; decline it and the project uses local merge and `BACKLOG.md`), `.claude/settings.json` permissions for the commands the cycle repeats (push, resets, installs and deletes keep asking, and so do the git commands run in the main branch's folder when it's checked out in another worktree), and what the cycle leaves orphaned. Answer "choose for me" (or pass it as the argument) if you don't know git or GitHub: it takes its own recommendations, skips the questions only someone who knows the project can answer, says plainly what's lost when `gh` isn't signed in, and lists what it chose for you (`plugins/minidev/skills/setup/references/choose-for-me.md`). Then it creates the missing product documents through `document`; for existing code, `SPEC.md` is written rule by rule from the code, and untested rules become `Missing tests` Debt entries. Detail: `plugins/minidev/skills/setup/SKILL.md`.

### 2. Idea

A clear idea goes straight into `BACKLOG.md` as an **Idea**; one that leaves behavior open gets an `interview` session, whose approved summary is the entry. "Just note it" skips the interview. With pull requests, `setup` recommends keeping the backlog in the repository's GitHub issues instead: each entry is an issue, a feature in progress is labeled and assigned as soon as it starts, and the change's final message closes it (`Closes #<number>`). Detail: `plugins/minidev/skills/document/references/backlog.md` and `issues.md` next to it.

### 3. Build

`build` works on one feature in a fixed order, on its own `feature/<name>` branch; several can be in progress at once. You're asked twice when it goes as planned:

- **At the start**, one message with everything the work needs decided: the open points with recommended answers, the **critical test list** in plain language (what the suite will check, and what you'll check by hand), the feature's **size**, modules with no tests, an overlap with another feature in progress. One OK covers it.
- **At the end**, the tester's assumptions Claude adopted, to confirm or change, and what to check by hand in the real app.

In between: tests written first and shown failing, then the code; the independent `tester` agent (skipped for a small feature), which sees only the entry and the diff and tries to break it; a refactor and a check of the tests' value; `SPEC.md` and `CHANGELOG.md` written from what was built; and the independent `reviewer` agent, which reads the code and the documents for what tests don't catch. Claude doesn't filter either report: removing a tester's test or disagreeing with a blocking finding goes to you. Checkpoints (`wip:` commits) let the work be paused and resumed in a new session ("continue X"). Detail: `plugins/minidev/skills/build/SKILL.md`, and the agents in `plugins/minidev/agents/`.

### 4. Finish

Code, tests and the three documents reach main as **one squashed commit** whose message records the verification: the test and build results, the tester's report, the check of the tests, the review, and the `Critical tests:`, `Regression tests:` and `To check by hand:` blocks (findable with `git log --grep`). In local merge mode, main is merged into the branch and tested there first, so main never holds untested code; in pull request mode, the branch is squash-merged once the checks pass. A change that breaks after it's pushed is fixed forward with `fix` or reverted as one commit. Detail: `plugins/minidev/skills/build/references/git-flow.md` (shared by `build`, `fix`, `chore` and releases) and `plugins/minidev/skills/build/references/review.md`.

### Bugs, chores and releases

- **Bug** (`fix`): its own `fix/<name>` branch, a test that reproduces it shown failing first, no tester; a trivial fix skips the review too. Detail: `plugins/minidev/skills/fix/SKILL.md`.
- **Chore** (`chore`): changes that keep the behavior (refactoring, debt, upgrades, migrations, tooling, typos), with the existing suite green before and after as the proof; prose and product text take short paths. It also adds missing tests and, on request, prunes useless tests. Detail: `plugins/minidev/skills/chore/SKILL.md`.
- **Later:** a bug or chore you don't want to do now goes to `BACKLOG.md` as a Bug or Debt entry.
- **Release:** "release 1.4.0" moves `[Unreleased]` into a version in `CHANGELOG.md`, after you confirm it, then pushes the commit and the tag. Detail: `plugins/minidev/skills/document/references/changelog.md`.

### Several at once

`/minidev:swarm` runs a few backlog items in parallel, each through its own skill (`build`, `fix` or `chore`) in its own worktree, then brings them into the main branch one at a time. It picks items whose files don't overlap, decides their open points and asks you once, with the options filled in and one that delegates everything to the end; after that OK it doesn't stop, and reports a line at each milestone. Defaults are sized for a small plan: two items, the cheapest model each needs, and an orchestrator that reads only the workers' short reports. Detail: `plugins/minidev/skills/swarm/SKILL.md`.

### Check-up

Every change is tested and reviewed on its own, but a review sees one diff; debt and a wrong architecture decision show only in the sum. `/minidev:checkup` looks there, every ten changes or so (`guide` says when one is due). First the numbers, which cost almost nothing: a script reads git for the files that change most, the folders where fixes concentrate and the files in different folders that change together, and the session times the suite, counts skipped tests and lists outdated or vulnerable dependencies. One message then shows them beside the last check-up's, what will run and what the last one cost, and you choose: the full check-up, only the numbers, or the full one on a cheaper model. The full check-up starts one `auditor` per area: the architecture as built against as decided, the decisions that get expensive to reverse and what breaks at ten times the data or use, the backlog against the structure, and a sample of the documents and tests against the code (two areas share an auditor in a small project). A finding needs evidence, what gets more expensive by waiting, and what makes that cost come due. A `refuter` then tries to knock each finding down, reading only the evidence it cites. You get a verdict per area (solid, with caveats, at risk) beside the last one's, the findings that stand and, apart, the refuted ones; the findings you approve become backlog entries through `document`, or are handed to the skill that owns the work (a spec audit, a test prune, a backlog clean-up), and `CHECKUP.md` keeps the verdicts, the numbers and where each finding went, so the next check-up compares itself with this one and doesn't raise the same things again. A finding recorded earlier and still open in the backlog keeps counting in its area's verdict: debt that's waiting hasn't gone away. It fixes nothing. Detail: `plugins/minidev/skills/checkup/SKILL.md`.

## The three documents

Each answers one question, so they never repeat each other:

| Document | Answers | Time |
|---|---|---|
| `BACKLOG.md` | What may come, and why you want it (features, plus bugs and debt left for later) | future |
| `SPEC.md` | How the product works **today**: rules, data, technical decisions, constraints | present |
| `CHANGELOG.md` | What changed in each version, for the people who use it | past |

`SPEC.md` describes only what exists: it's updated from what was built when a feature, fix or chore changes what it describes, never when something is only planned. Each fact lives in one place, and git history keeps the detail behind all three. When you suspect it drifted ("does SPEC.md match the code?"), `document` audits it: each rule against the code and its tests, and what the code exposes against the rules. The report lists contradictions, rules no code does, untested rules and behavior with no rule; you approve what changes, and the result is SPEC.md corrections plus Bug and Debt entries, without touching code. A large product is audited one area at a time.

## Developing the plugin

To work on the plugin from a local clone, add it as a marketplace by path instead of the GitHub name:

```
/plugin marketplace add /path/to/minidev
```

After changing the skills, bump `version` in `plugins/minidev/.claude-plugin/plugin.json` (and keep its `description` and the one in `.claude-plugin/marketplace.json` the same), record the change in `CHANGELOG.md`, and run `/plugin marketplace update minidev` so installed copies pick it up.

The evals need `bash`, `python3` and `node`, and were developed and run on macOS. Nothing in them is macOS-only: the fixture copies git from `xcrun --find git` when it's there (the eval sandbox blocks Xcode's shim) and from the `git` on the path otherwise; on other systems they haven't been run.

### Trigger evals

`plugins/minidev/evals/triggers/` holds one case per prompt that checks which skill fires: the right one for features (new or resumed), an update after a pull request was merged (`build`, in a project whose pull requests are merged by the reviewer), bugs (flaky tests and slowdowns included), chores, ideas (in BACKLOG.md and in a project whose backlog is in GitHub issues), bugs and debt left for later, finished features, releases, new projects and interviews, and none where a skill would be wrong (`brainstorm` in an existing project, `fix` for new behavior or a typo, `chore` when the user only wants to note it, `document` for only reading a document, the cycle in a project that doesn't use it, for a typo or a feature request, `build` for a plain pull of the main branch), and the close calls between skills (a typo in SPEC.md is `document`, a broken CI config, a speed-up nobody reported or "atualiza as dependências" is `chore`). Eval runs don't load a project's CLAUDE.md, so cases that need a project set up for the cycle pass it in `append_system_prompt`, a copy of the CLAUDE.md template in `skills/setup/SKILL.md`. When the template changes, update the copies too, and the fixture's CLAUDE.md in `evals/behavior/fixture.sh`; `python3 evals/check-copies.py` (from `plugins/minidev`) lists every copy that no longer matches, the behavior and outcome cases whose unattended-run prompt differs, the skills whose cycle check (the first step of `build`, `fix` and `chore`) no longer matches the others, graders that share a file name but not their content (a case that needs a different check gives it its own name), and the weight scale of a check-up's findings when `agents/auditor.md` and `agents/refuter.md` state it differently. Run the evals after changing a skill's description, from `plugins/minidev`:

```
claude plugin eval . --tag trigger --ablation none --no-publish -j 4
```

Each case runs 3 times by default (about $0.10 per run); add `--runs 1` for a quick check. Results go to `evals/results/`, which git ignores.

### Behavior evals

`plugins/minidev/evals/behavior/` runs the cycle for real on a small fixture project (`fixture.sh`: a Node library set up for the cycle, with one backlog Idea and one known bug) and checks what Claude did, not only which skill fired: `build-flow` (a small feature: an In progress commit, feature branch, a `wip:` checkpoint, the `reviewer` and no `tester`, a `Critical tests:` block, the squash into main), `build-tester-flow` (the same feature with the tester asked for), `fix-flow` (a trivial fix: fix branch, `Regression tests:`, no tester and no review), `chore-prose-flow` (a typo in the README fixed with one commit on main: no branch, suite or review) `chore-text-flow` (a typo in an error message: no branch or review, the suite once), `swarm-flow` (`/minidev:swarm` on the fixture with a second idea in its own module: both ideas set In progress in one commit, a worker per idea in a worktree, two squashes into main and no push; the known bug is left out, since it touches the same module as Note titles). Its first run (0.29.0, about $0.60) stopped before the workers because the eval harness refuses `isolation: worktree`; workers now make their own worktree, and `workers-in-worktrees` checks for two `git worktree add` calls. `checkup-flow` runs `/minidev:checkup` on the fixture: the history script runs, at least three `auditor` agents start (the fixture is small, so two areas share one), the `refuter` challenges their findings (the fixture's SPEC.md says notes are listed newest first and the code lists them oldest first, so there's at least one), `CHECKUP.md` is written, no file under `src/` or `test/` is edited and nothing is pushed. Its first run (before 0.33.0) passed every grader and cost $1.24 in about three minutes, with three auditors and the refuter; the second, after the fixes below, $1.13. Its transcript showed two things the graders don't check, both fixed since: three auditors reported the same contradiction and it put three areas at risk (a problem several auditors report now counts once, in the area whose brief asks for it), and the auditors couldn't read the two rule files the prompt pointed to outside the project (their sections are now copied into the prompt). The three `guide-*` cases run `/minidev:guide` and check that it only looks and recommends, with no file written and no git change, and that the reply names the right next step in plain words: `guide-empty-flow` (an empty folder: `brainstorm`), `guide-no-cycle-flow` (code with a CLAUDE.md that doesn't use the cycle: `/minidev:setup`) and `guide-ready-flow` (the fixture as it is: build the one Idea in the backlog); `guide-empty-flow` and `guide-ready-flow` ask in Portuguese. Those checks of the reply are graded by a model, so a run can fail on wording. The prompt tells Claude the user approved every list in advance. The scaffold runs bash on your machine, and the eval sandbox blocks the system git, so the fixture gets its own copy in `.tools/`:

```
claude plugin eval . --tag behavior --ablation none --no-publish --scaffold --allow-tools Bash Write Edit --runs 1 -j 3
```

They're slow and cost a few dollars per run (a whole feature with its tester and reviewer); run them after changing a skill's steps.

### Outcome evals

The behavior evals check what Claude did; `plugins/minidev/evals/outcome/` checks whether the result is right, and whether the plugin beats Claude without it. Each case runs with and without the plugin on the same fixture (`patch.sh` adapts the behavior fixture: the ordering bug fixed, a Search idea in the backlog, a SPEC rule no visible test checks, and a CLAUDE.md that doesn't tell the baseline to stop). `claude plugin eval` has no grader that runs code, so `run.sh` keeps each run's folder and `score.py` copies the `src/` it left next to the case's hidden acceptance tests (`<case>/hidden/`, which Claude never sees) and runs them with `node --test`. The hidden tests check the rules the entry or SPEC.md states, plus a few the fixture's code already follows (ids in order, `reset` starting them again, a note whose text isn't a string rejected). `search-feature` builds a feature whose rules are easy to miss (accents, combining marks, several words in any order); `list-refactor` speeds up `listNotes` without breaking the rule that its result can be changed safely.

```
plugins/minidev/evals/outcome/run.sh 3
```

It prints the hidden tests' pass rate and the mean cost per arm. A full run (2 cases, 2 arms, 3 runs) costs about $10. The first one, on 0.18.0: both arms passed every hidden test in every run; the feature cost $3.11 with the plugin and $0.37 without, the refactor $0.65 and $0.27. Most of the feature's cost was tester rounds started by questions, not failures; 0.19.0 stopped that, and the feature came down to $0.94, still passing every hidden test.

## Credits

`interview` is from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, see `plugins/minidev/skills/interview/LICENSE`). The patterns of useless tests in `test-value.md` are adapted from the `test-audit` skill in [mblode/agent-skills](https://github.com/mblode/agent-skills) (MIT), itself from OpenClaw's.

## License

MIT, see `LICENSE` (also shipped inside the plugin, as `plugins/minidev/LICENSE`). `interview` keeps its own MIT license from Matt Pocock.
