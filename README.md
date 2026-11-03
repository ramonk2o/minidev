# minidev

A Claude Code plugin with a fixed development cycle, the same in every project: ideas are interviewed until nothing is left open, features are built test-first, checked by an independent tester and reviewed by an independent reviewer, and three product documents keep track of what may come, what exists and what changed.

## Install

In Claude Code:

```
/plugin marketplace add ramonk2o/minidev
/plugin install minidev@minidev
```

Then, in each project where you want the cycle, run:

```
/minidev:setup
```

To get new versions later: `/plugin marketplace update minidev`.

## What's inside

| Piece | What it does |
|---|---|
| `brainstorm` skill | Starts a new project from an idea: interviews you about the product, decides the architecture and stack with you, picks the first feature, then scaffolds a project whose tests and build already run. |
| `setup` skill | Prepares a project for the cycle: git, CLAUDE.md, permissions, product documents. Runs only when you call `/minidev:setup`. |
| `grilling` skill | Interviews you about an idea, a round of questions at a time, until nothing is left open. |
| `document` skill | The only writer of `BACKLOG.md`, `SPEC.md` and `CHANGELOG.md`. |
| `build` skill | Builds a backlog feature test-first, then has it checked by the `tester` agent before committing. |
| `fix` skill | Fixes a bug on its own branch, test-first when it can be reproduced, and records it in the changelog. |
| `chore` skill | Makes a change that keeps the behavior (refactoring, debt, dependency upgrades, migrations, tooling, typos) on its own branch, with the suite green before and after. |
| `tester` agent | Independent tester: runs the suite, checks every rule is covered, tries to break the feature. Never fixes code. |
| `reviewer` agent | Independent code reviewer: reads the diff for what tests don't catch (risky logic, errors, security, design, leftovers) and reports blocking findings and suggestions. Read-only. |

You don't need to call `grilling`, `document`, `build`, `fix` or `chore` by name. Just talk ("note this idea…", "let's build X", "X has a bug…", "release 1.2.0"): the CLAUDE.md written by `setup` tells Claude which skill each step uses. The steps themselves live in the skills, not in that CLAUDE.md, so updating the plugin updates every project.

## How the cycle works

```
 idea ──► grilling (if behavior is open) ──► BACKLOG.md: Idea
                                                  │
                                                  ▼
                                   build: critical test list ──► your OK
                                                  │
                                                  ▼
                                   new branch: feature/<name>
                                                  │
                                                  ▼
                                   tests first (shown failing) ──► code
                                                  │
                                                  ▼
                                   tester agent ◄──► fixes (new tester each round)
                                                  │
                                                  ▼
                                   refactor ──► reviewer agent ──► fixes
                                                  │
                                                  ▼
             verification commit: code + tests + SPEC + CHANGELOG, entry leaves BACKLOG
                                                  │
                                                  ▼
                                   you check by hand what tests can't
                                                  │
                                                  ▼
              squash into main (local merge or pull request), test, push
```

### 0. Brainstorm (new projects only)

Starting from nothing, describe the idea ("I want to build an app that…") in an empty folder. `brainstorm` interviews you in `grilling` rounds, product first and stack second, each question with a recommended answer:

- **Product:** the problem, who has it, the smallest first version that's already useful, what's out of scope, where users meet it, what it stores.
- **Architecture and stack:** language, framework, the few parts the product splits into, storage, how rules are tested. Mature tools and few dependencies, checked against current docs; options are compared only where the choice is really open.
- **Where to start:** the first version split into features in build order, starting with the thinnest path through the whole product, so the architecture is proven while it's still cheap to change.

After you approve the plan, it scaffolds the project (git, the framework's generator, folders, a passing smoke test, a README), shows install, tests and build passing, and records the features in `BACKLOG.md` and the technical decisions in `SPEC.md`. No feature code is written: the first feature goes through `build`. Then run `/minidev:setup`.

### 1. Setup (once per project)

`/minidev:setup` reads the repository and proposes, all in one message for a single approval:

- `git init` and a `.gitignore`, if the project isn't a repository yet;
- a `CLAUDE.md` with the project's real commands, test conventions, which skill handles each step of the cycle and the integration mode, local merge or pull requests (for repositories with CI, a protected main or several people); an existing CLAUDE.md is updated, not overwritten; a long cycle section written by older versions is slimmed down;
- `.claude/settings.json` permissions for the test, build and local git commands (including `switch` and `merge`) and, in pull request mode, the read-only `gh` commands, so the cycle doesn't stop on a prompt for each run (install, publish, push, resets, opening or merging pull requests, and deletes keep asking);
- what the cycle leaves orphaned: old `TODO.md`/`FEATURES.md`, local skills that overlap the plugin, broken references.

It then creates the missing product documents through `document`. The cycle needs automated tests; if the project has none, setup says so before going on.

### 2. Idea

A clear idea is recorded straight into `BACKLOG.md` as an **Idea**. If it leaves behavior open, Claude starts a `grilling` interview: rounds of numbered questions, each with a recommended answer, asking only what can be decided now and looking up facts itself instead of asking you. The final summary is the backlog entry, so approving it approves what gets recorded. Saying "just note it" skips the interview. This routing lives in the `document` skill.

### 3. Build

`build` works on one feature at a time, in a fixed order:

1. **Rules check.** The entry needs its rules and its **Constraints**: what it must respect besides behavior (speed, security, accessibility, compatibility, how much data), written so they can be checked. If a few are missing, or the feature has an obvious risk nobody addressed, Claude asks them directly; if it's still a bare idea, it offers a `grilling` interview first. Tests built on guessed rules would encode assumptions nobody approved.
2. **Critical test list.** In plain language, no code, split in two: what the test suite will check (measurable constraints included), and what you'll **check by hand** in the real app (visuals, focus, dragging…). You approve the list; the entry becomes **In progress**.

All the work happens on a `feature/<name>` branch created from an up-to-date main branch, so main only receives finished, verified features.
3. **Tests first.** The automated tests are written and run (against a stub of the public interface, if the module is new), and must fail for the right reason: the feature is missing. A test that passes before the code exists isn't testing the feature.
4. **Code.** Written until the critical tests, the whole suite and the build pass. A critical test is never changed to make it pass without asking you.

### 4. Independent tester

The `tester` agent gets only the backlog entry, the diff and the test/build commands: not the conversation or the author's reasoning. Not knowing what was meant is its value. It runs everything, checks that each rule has a test that would fail if the rule broke, and writes extra tests trying to break the feature, in new files whose name contains `tester`. It's told never to touch the feature's code or existing tests, nor git state, and after each round Claude checks that it only added test files. It reports:

- **Failures:** Claude fixes the code, keeps the test that caught it and launches a *new* tester, so nothing carries over from the last round.
- **Uncovered rules:** missing tests are added.
- **Assumptions:** tests of behavior nobody decided. They're dropped and the question comes to you.

This repeats until a round has no failures, or stops after 3 rounds to show you what's left.

### 5. Refactor and review

With the suite green, Claude cleans up its own code (leftover stubs, dead code, names, duplication) without changing behavior, using the `simplify` skill when the diff is large. Then the `reviewer` agent, again with only the entry and the diff, reads the code for what tests don't catch: risky logic, error handling, security, design that doesn't fit the codebase, leftovers, and the project's conventions. It can't edit anything. **Blocking** findings are fixed (one that changes behavior gets a test first and a new tester round) or, if Claude disagrees, brought to you; **suggestions** are applied when clearly better and cheap, and the rest are explained in a line. `fix` and `chore` run the same review whenever they change code.

### 6. Finish

`document` moves the feature out of the backlog: the rules that were actually built go to `SPEC.md` and the change goes to `CHANGELOG.md` under `[Unreleased]`. While working, Claude commits `wip:` checkpoints on the branch, so the work can be resumed in a new session or paused for a bug fix. Code, tests and the three documents reach main as **one squashed commit**, whose message records the test results, the tester's rounds, the review and a `To check by hand:` block (findable later with `git log --grep "To check by hand"`). You then check those items in the real app; anything that fails there is fixed on the same branch. Once you confirm everything works, the branch reaches main in the project's integration mode. **Local merge:** it's squashed into main, the test suite and build run again on the combined code, and only then is main pushed. **Pull requests:** the branch is pushed, a pull request is opened with the verification message as its description, and it's squash-merged once the checks pass (Claude stops if it needs a review). A merge conflict, or a failure after the merge, stops the cycle and is shown to you; a failure is then fixed as a bug. The branch steps live in one place, `skills/build/references/git-flow.md`, shared by `build` and `fix`.

### Bugs, chores and releases

- **Bug** (`fix` skill): no tester, and no backlog entry unless it was left for later (type Bug), on its own `fix/<name>` branch, brought into main like a feature once the fix is confirmed. If it can be reproduced in a test, the test is written and shown failing first, then the fix. The fix is recorded under Fixed in the changelog (and in SPEC.md if a rule changed). If the fix needs a decision about behavior, it's a feature and goes back to the idea step.
- **Chore** (`chore` skill): for changes that keep the behavior, such as refactoring, technical debt, dependency upgrades, migrations, tooling or a typo. On its own `chore/<name>` branch, with no critical test list and no tester: the existing suite is the proof, run before (a red suite stops it) and after, with the tests that check behavior left untouched. Upgrades are read against the dependency's changelog first. SPEC.md changes only if a technical decision did, CHANGELOG.md only if users will notice.
- **Later:** a bug or a chore you don't want to do now goes to `BACKLOG.md` with type Bug or Debt, and leaves it when `fix` or `chore` does it.
- **Release:** "release 1.4.0" moves the `[Unreleased]` changes into a version in `CHANGELOG.md`, after you confirm the version, date and entries, then pushes the commit and the tag (in pull request mode, through a `release/<version>` pull request, then the tag).

## The three documents

Each answers one question, so they never repeat each other:

| Document | Answers | Time |
|---|---|---|
| `BACKLOG.md` | What may come, and why you want it (features, plus bugs and debt left for later) | future |
| `SPEC.md` | How the product works **today**: rules, data, technical decisions, constraints | present |
| `CHANGELOG.md` | What changed in each version, for the people who use it | past |

`SPEC.md` describes only what exists: it's updated when a feature is finished, from what was built, not when it's planned. Each fact lives in one place, and git history keeps the detail behind all three.

## Developing the plugin

To work on the plugin from a local clone, add it as a marketplace by path instead of the GitHub name:

```
/plugin marketplace add /path/to/minidev
```

After changing the skills, bump `version` in `plugins/minidev/.claude-plugin/plugin.json`, record the change in `CHANGELOG.md`, and run `/plugin marketplace update minidev` so installed copies pick it up.

### Trigger evals

`plugins/minidev/evals/triggers/` holds one case per prompt that checks which skill fires: the right one for features, bugs, chores, ideas, debt left for later, releases, new projects and interviews, and none where a skill would be wrong (`brainstorm` in an existing project, `fix` for new behavior or a typo, `chore` when the user only wants to note it, the cycle in a project that doesn't use it). Eval runs don't load a project's CLAUDE.md, so cases that need a project set up for the cycle pass it in `append_system_prompt`. Run them after changing a skill's description, from `plugins/minidev`:

```
claude plugin eval . --tag trigger --ablation none --no-publish -j 4
```

Each case runs 3 times by default (about $0.10 per run); add `--runs 1` for a quick check. Results go to `evals/results/`, which git ignores.

## Credits

`grilling` is from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, see `plugins/minidev/skills/grilling/LICENSE`).

## License

MIT, see `LICENSE`. `grilling` keeps its own MIT license from Matt Pocock.
