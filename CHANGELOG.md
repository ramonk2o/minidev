# Changelog

All notable changes to this plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
applied to how the skills behave.

## [Unreleased]

### Added

- **`checkup`: a health check-up of the whole project, for what no single change's review sees** (debt that piled up, architecture decisions that turned out wrong): `/minidev:checkup` collects numbers that need no model (a script reads git for the files that change most, where fixes concentrate and which files in different folders change together; the suite's time and skipped tests; outdated and vulnerable dependencies), shows them with what will run and what the last check-up cost, and on your OK starts independent `auditor` agents (architecture, decisions and growth, the backlog, documents and tests) and a `refuter` that tries to knock each finding down. You get a verdict per area beside the last check-up's (a problem several auditors report counts once) and the refuted findings apart; the ones you approve become backlog entries, and `CHECKUP.md` keeps the result for the next one. It changes no code. `guide` says when a check-up is due.

- **`rethink`: everything that bothers you about a product in use becomes backlog changes you approve**: `/minidev:rethink` takes loose points with no solution yet, reads the backlog and SPEC.md, plays them back with the earlier decisions they collide with, questions them in rounds and ends in one plan of entries to create, change and discard. An `auditor` that wasn't in the conversation checks a plan with more than one change before `document` writes it, and what can't be settled stays as open questions. It changes no code and runs only when you call it; `guide` points to it, and `document` offers it when one message brings several loose complaints.

### Changed

- **`document`, `swarm`, `brainstorm` and `guide`: a backlog entry says what it touches, when it's planned and what it waits for**: an area is the part of the product an entry changes, never a phase like "Later"; the version it's planned for is its own field (`Version`, the milestone in GitHub issues) and the entries that must be built first are its `Needs` (GitHub's "blocked by" relation), which `document` keeps true as entries are added, finished, discarded or renamed. `brainstorm` writes the first version and its dependencies that way and shows them in its plan, `build` names an entry the feature still waits for in its start message, `guide` proposes the current version's first entry that isn't waiting, and `swarm` reads the backlog without the bodies, shortlists from the current version and opens only the shortlist.
- **`document`: relabeling the issues is a reorganization, shown as a plan first**: features get GitHub's `enhancement` label, area labels are created with a description, a request to relabel or classify the issues lists what each open issue gains and loses before anything is written, and `in progress` comes off an issue once its change reaches the main branch. A release asks where the entries still planned for it go, and closes its milestone.

### Fixed

- **`guide`: a command you're told to type comes with a sentence on what it changes**: sending you to `/minidev:setup` (or `swarm`, `checkup`, `rethink`), it says what the command will change in your project, e.g. that setup prepares it and shows everything it will change first, not only the command. Closes #17.
- **`document`: a note asked in a session's worktree reaches the main branch**: when the session's branch has no commits of its own and the main branch is open in another folder, the change is written and committed there and the session's branch catches up, instead of staying on a branch nothing merges. Closes #12.

## [0.32.0] - 2026-11-14

A `setup` path for people who don't know git or GitHub, and `swarm` workers that make their own worktree when the environment can't.

### Added

- **`setup`: a "choose for me" path for people who don't know git or GitHub**: answering "choose for me" (or passing it as the argument of `/minidev:setup`) takes every recommendation of the questions round without asking, says each choice in one plain sentence with what it changes day to day, and skips the question only someone who knows the project can answer (the rules a newcomer would break; Conventions is left out). Questions that protect the user's work (uncommitted changes) are still asked, in plain words. When `gh` is missing or signed out it says what is lost (no review step, no backlog in issues) and how to get it, then continues with local merge. At the end it lists what it chose and how to change it by running `/minidev:setup` again. Closes #3.

### Changed

- **swarm: workers make their own worktree when the environment can't**: a subagent worker creates its worktree under `.claude/worktrees/` (which the swarm adds to `.gitignore` when missing) instead of relying on `isolation: worktree`, so a batch runs wherever a subagent and git exist. The orchestrator removes the clean worktrees of merged items at the end and lists the others as pending. `setup` allows `git worktree add` so those workers don't stall on a permission prompt (projects set up earlier get it by running `/minidev:setup` again).

## [0.31.0] - 2026-11-14

A new `guide` skill tells newcomers where their project stands and what to do next, `swarm` offers to delegate everything in one click, and it no longer mistakes an unprotected main branch for one that requires a review.

### Added
- **`guide`: where the project stands and what to do next, in plain words**: `/minidev:guide` (run only by the user, so it never competes with the other skills) reads the folder, git, the CLAUDE.md, the backlog, the branch, uncommitted changes and open pull requests, and says in a few sentences where the project is, the one next step and the words or command that take it: `brainstorm` for an empty folder, `/minidev:setup` for a project that doesn't use the cycle yet, "continue X" or the first backlog entry for one that does. It explains a term of the cycle (pull request, branch, test-first, spec, backlog) in one sentence when asked. It writes nothing. The README's new "First use" section tells newcomers to start with it and to come back whenever they're stuck, and lists what to have installed (Claude Code, git, `gh` and a GitHub login). `brainstorm` and `setup` end by pointing to it.

### Changed
- **`swarm` offers to delegate everything in one click**: the start message asks three questions with fixed wording instead of four that each run phrased its own way. Its recommended Delegation option says what delegating means (the orchestrator judges each item, asks its worker for fixes, brings it into the main branch when it's good and doesn't stop you until the summary), so it no longer takes a typed answer. The models question is gone: each item's model is shown in the batch, and changing one is an answer to Batch.

### Fixed
- **`swarm` no longer takes an unprotected main branch for one that requires a review**: a 404 from the branch protection query (no protection, or a plan that offers none) means no review is required, as `setup` already reads it; only a 403 (no admin rights) leaves it unknown. Before, any failure ended the batch with the pull requests open and dropped the Delegation question.

## [0.30.0] - 2026-11-14

The `grilling` skill is now `interview` (a breaking change before 1.0: `/minidev:grilling` no longer exists), and a trigger eval stops failing on correct behavior.

### Changed
- **`grilling` is now `interview`**: the skill has the name the rest of the plugin already uses for what it does, and a description that says what it does (rounds of numbered questions with a recommended answer, until nothing is left open) and what it isn't for (a new project is `brainstorm`, just noting an idea is `document`). "Grill me" and "me sabatina" still trigger it. `/minidev:grilling` no longer exists: use `/minidev:interview`. Projects set up with `setup` don't name the skill in their CLAUDE.md, so they keep working.

### Fixed
- **Trigger evals: the case for new behavior checks only that `fix` doesn't fire**: it also required `document` or `interview` to fire, but its prompt states a wish without asking for any action, so the model sometimes answers in text and the case failed on correct behavior.

## [0.29.0] - 2026-11-13

Swarm runs a few backlog items in parallel, from one start message to the main branch.

### Added
- **swarm: a few backlog items in parallel, to the main branch**: `/minidev:swarm` picks a batch (2 items by default, 3 at most) whose files don't overlap and with at most one database migration, settles every open point and asks once, with the options filled in (the batch, the models, who merges, how often it reports). Then it runs without stopping: one worker per item in its own worktree (a separate session in the desktop app, a background subagent elsewhere), each through `build`, `fix` or `chore` on the cheapest model its item needs, brought into the main branch one at a time, and a final check of the main branch. It works with BACKLOG.md or GitHub issues, and with local merge (the main branch isn't pushed) or pull requests. Findings outside an item become new entries; running it again resumes a batch stopped by the usage limit.

## [0.28.0] - 2026-11-13

Setup recommends pull requests and issues on GitHub, and its commit carries only its own changes.

### Changed
- **setup: pull requests and issues are the recommendation on GitHub**: a project on GitHub with `gh` signed in is recommended pull requests and, with issues on, the backlog in GitHub issues, without needing CI, a protected main branch or more than one author. A project with no remote is offered a GitHub repository (private unless the user says otherwise), created on the user's OK and pushed on another; declining it keeps local merge and BACKLOG.md, as does a remote on another host or a missing `gh`. Projects already set up don't change unless `setup` runs again.

### Fixed
- **setup: its commit carries only its own changes**: it checks where the session stands first, asks the user to commit uncommitted work on a branch of their own or stash it before writing (or stops), and when it can't commit straight on an up-to-date main branch (pull requests, or a session on another branch or in a worktree) it writes on a `chore/minidev-setup` branch started from the main branch, instead of whatever branch the session was on. Brought in by local merge, that branch doesn't push the main branch.
- **setup: Debt entries from a new SPEC.md** reach the backlog where it lives after the move to issues, approved with the SPEC.md draft, instead of landing in a BACKLOG.md about to be removed or in issues nobody approved. Declining the move to issues at the review redoes the CLAUDE.md and the permissions for BACKLOG.md. The migration also runs when the project already has all three documents.

## [0.27.0] - 2026-11-09

The backlog can live in GitHub issues, and setup in pull request mode commits through a pull request.

### Added
- **Backlog in GitHub issues**: a project whose CLAUDE.md says `Backlog: GitHub issues` keeps its ideas, bugs and debt in the repository's issues instead of BACKLOG.md, so the team sees what's being built as it starts, without waiting for a merge. Each entry is an issue in the same format, with areas and types as labels; starting a feature labels and assigns its issue (no commit on the main branch) and names the branch after its number; the change's final message closes it with `Closes #<number>`; a discarded idea is closed as not planned, and a revert reopens it. Changing the body of an issue someone else opened asks first, and an issue is read again, comments included, before it's used. `setup` asks where the backlog lives when pull requests are recommended or chosen, allows the read-only `gh issue` commands, and migrates an existing BACKLOG.md to issues after an OK to the list. SPEC.md and CHANGELOG.md stay files.

### Fixed
- **Setup in pull request mode** commits on a `chore/minidev-setup` branch and brings it in through a pull request when the main branch exists on the remote, instead of a commit on the local main branch that a protected main branch wouldn't take; after a move to issues, the pull request names them.

## [0.26.0] - 2026-11-09

A new integration mode where the reviewer, not the author, merges pull requests; Resume reads pull requests before picking a branch.

### Added
- **Pull requests, merged by the reviewer**: a new integration mode for teams where the author never merges their own pull request. The cycle pushes the branch, opens the pull request, waits for the checks and handles review comments as in pull request mode, keeping the pull request's body equal to the final message and requesting a new review after each round of fixes, but never runs `gh pr merge`: it tells the author the merge is the reviewer's and stops. When the author asks to continue, or says the pull request was merged and asks to update (`build` handles it, whatever the branch: feature, fix or chore), a merged pull request updates the local main branch, deletes the branches and checks that the squashed commit kept the verification message (otherwise it says the repository should squash with "Title and description"); an open one gets its comments, failing checks or conflicts handled, or its state reported. In both pull request modes, a pull request no one was asked to review gets a reviewer the user names, review comments include those on lines of code, and Resume reads the pull request's state before switching to its branch. `setup` recommends it when the main branch requires an approving review and warns about the squash setting; releases are tagged after the reviewer merges.

### Changed
- **Resume** with several matching branches (a bare "continue" weighs them all), in pull request mode, reads each pull request first: it updates from a merged one, reports the ones only waiting, and proposes the branch left with work (in Pull requests mode, an approved one to merge counts) instead of asking which.

### Fixed
- In pull request mode, the final message also lists the commits the branch carries from the main branch that aren't part of the work (an idea recorded there meanwhile), written once and kept on later body updates, so a revert of the squash doesn't drop them unrecorded.

## [0.25.3] - 2026-11-06

Setup explains why some git prompts in worktrees keep asking.

### Changed
- **Setup permissions** add no `git -C` rule and say why: the steps run in the main branch's folder when it's checked out in another worktree keep asking, since no rule allows them without letting a push or reset through.

## [0.25.2] - 2026-11-06

The eval copy check also catches graders that share a name but not their content.

### Changed
- `evals/check-copies.py` also requires graders with the same file name to be identical in every case that has one; a case that needs a different check gives it its own name.

## [0.25.1] - 2026-11-06

The In progress rule lives in one place, and the eval copy check covers the cycle check.

### Changed
- The In progress rule (where and when the status is written) lives only in `document`'s Start a feature; `build` and `document`'s lifecycle summary point to it instead of repeating it.
- `evals/check-copies.py` also checks that `build`, `fix` and `chore` start with the same cycle check.

## [0.25.0] - 2026-11-05

Review and prune rules are aligned across skills, the README becomes a map, and an eval copy check arrives.

### Added
- `evals/check-copies.py` lists the eval copies of the CLAUDE.md template and of the unattended-run prompt that no longer match their source. The unattended-run prompt now names the start message and the adopted tester assumptions, `outcome/patch.sh` no longer needs BSD `sed`, and the README says what the evals need to run.

### Changed
- **Chore review:** an upgrade is reviewed even when only a version number and the lockfile change, as `review.md` already said; only text or docs skip it.
- **Prune** records the rules left with no test the way the spec audit does: one Debt entry per area, `Missing tests: <area>`.
- **Setup permissions** also allow `git rebase --abort`, `git read-tree`, `git restore`, `git branch -m`, `git remote set-head` and `git tag`, which the cycle runs locally.
- **README:** the cycle is now a map that points to each skill's file, instead of a second copy of the rules.

### Fixed
- `document` said reading the documents needs no skill, while presenting the backlog ("what's in the backlog?") is one of its operations; that's now the stated exception.

## [0.24.1] - 2026-11-05

Leftovers from 0.22–0.24 are fixed: constraints, adopted assumptions and checkpoints now agree everywhere.

### Fixed
- **Constraints on how the code is made** (no new dependency, a platform version) are left to the reviewer everywhere, not only in the tester: `build` no longer puts them in the critical test list, and the reviewer no longer blocks them for having no test.
- **Adopted tester assumptions:** `document` now allows them in an entry's Decisions, marked "(assumed: the tester's recommendation)"; before, it said an assumption is always an open question. The entry format shows that marker and the **To check by hand** field.
- **Checkpoint contents:** the list in `git-flow.md` now includes the size, the adopted assumptions and which tester tests caught a failure, so a resumed feature doesn't lose them.
- **Setup** offers the spec audit only for a SPEC.md that already has behavior rules, not for one `brainstorm` just wrote.
- **`fix` description:** a broken CI config goes to `chore`, and the changelog line is written only when users could see the bug, as in the skill's steps (also in `document` and the README).
- Smaller leftovers: broken `git-flow.md` links in `document`'s backlog reference, the branch exception in `git-flow.md` now covering both chore short paths, "step N" references in `build` that meant sections, README passages left over from 0.22–0.24, and the trigger evals' copy of the CLAUDE.md template ("the features in progress").

## [0.24.0] - 2026-11-05

The tester leaves how-the-code-is-made constraints to the reviewer, and its useful tests are kept as regression tests.

### Changed
- **Tester:** Constraints on how the code is made (no new dependency, a platform version, no network access in a module) are left to the reviewer, who already reads the diff for them; the tester no longer writes tests that only read config or source text for them, or reports them as uncovered.
- **Tester tests after the merge:** the ones that caught a failure are listed under `Regression tests:` in the feature's verification commit, so a later prune keeps asking before removing them; the other tester tests become ordinary tests at the merge.

## [0.23.0] - 2026-11-05

`document` can audit SPEC.md against the code.

### Added
- **Spec audit** (`document`, `references/spec-audit.md`): SPEC.md checked against the code rule by rule, and the code's visible behavior checked against the rules. Contradictions, rules no code does and behavior that looks accidental come as questions with a recommendation; untested rules become `Missing tests` Debt entries; a large product goes one area at a time. It runs when asked ("does SPEC.md match the code?"), when `setup` adopts a project that already has SPEC.md (offered), and as part of writing a new SPEC.md for existing code.
- Trigger evals: auditing the spec fires `document` (not `chore`), in Portuguese and English.

## [0.22.0] - 2026-11-05

A feature that goes as planned stops only twice: once at the start and once at the end.

### Changed
- **Two stops in a feature that goes as planned.** At the start, one message holds everything the work needs decided: the entry's draft for a direct request, the open points with recommended answers, modules with no tests, an overlap with another feature in progress, the critical test list and the size; one OK covers it, before the entry is set In progress or the branch exists. The tester's assumptions no longer stop the work: their recommended answers are adopted, tested and marked in the entry's Decisions, and shown at the end with what to check by hand, to confirm or change. Unexpected stops (a red suite, a disputed test, a review disagreement, a conflict) and the `grilling` interview stay.

## [0.21.0] - 2026-11-05

The verification commit's test and build lines are copied from a real run.

### Changed
- The verification commit's Tests and Build lines are copied from a run, not written: the runner's summary verbatim and the build's result, each with its command, from a run made after the last change to the code being committed.
- The squash grader of the behavior evals accepts flags before `--squash` (`git merge -q --squash`).

## [0.20.0] - 2026-11-05

Several features can be in progress at once, each on its own branch.

### Changed
- **Several features in progress at once**, each on its own branch (and worktree, if wanted). An In progress entry names its branch (`In progress (feature/<name>)`), so Resume finds it. Starting a feature no longer asks what to do with the one in progress: it checks whether another in progress touches the same modules or SPEC.md section, and if so recommends finishing that one first, leaving the choice to the user.

## [0.19.0] - 2026-11-05

A leaner tester cuts a feature's cost by about two thirds, and outcome evals compare the plugin with plain Claude.

### Added
- Outcome evals (`evals/outcome/`): a feature and a refactor run with and without the plugin, scored by hidden acceptance tests that `run.sh` runs against the code each run left.

### Changed
- **Leaner tester.** Only failures start a new tester round; assumptions, uncovered rules and extra tests no longer do, and a blocking review fix gets a test but no new round. The tester reports at most 3 assumptions, each with a recommended answer and no test. The feature size no longer counts rules, only lines and risk. On the Search outcome eval this cut the cost from $3.11 to $0.94 per run, with every hidden test still passing.

## [0.18.0] - 2026-11-04

Small features skip the tester and trivial fixes skip the review.

### Added
- **Size tiers.** A small feature (about 50 production lines, no new module or dependency, no security, data, volume or input constraint, at most 5 automated rules) skips the tester; the size is approved with the critical test list, recounted once built, and the reviewer checks coverage instead. A trivial fix (about 10 lines, with a regression test shown failing first) skips the review.
- `chore` has a product text short path for wording fixes to strings users see: the tests that check the old text are found first, and the suite runs once, after the change.
- Behavior evals `build-tester-flow` and `chore-text-flow`; `build-flow` and `fix-flow` now expect the small and trivial paths.

### Changed
- `build` runs only the affected tests after the refactor; the whole suite runs once, after the check of the tests.

## [0.17.0] - 2026-11-04

Setup reads more of the repository, checkpoints carry everything a resumed session needs, and many git edge cases get a defined path.

### Added
- **Setup reads more of the repository**: commit hooks and message conventions, a changelog generator and a main branch other than the remote's default become optional Development cycle lines (`Commit messages:`, `Changelog:`, `Main branch:`) that the other skills follow. Branch protection is read from rulesets too, and a 403 counts as unknown.
- **Features that change an existing rule** list the existing tests they change, for approval with the critical tests; the tester is told SPEC.md predates the feature.
- Trigger evals: a feature request outside the cycle fires nothing, a typo in SPEC.md fires `document` (not `chore`), a broken CI config and an unreported speed-up fire `chore` (not `fix`), discarding an idea fires `document`, `grilling` fires in Portuguese; reading CHANGELOG.md now runs in a project set up for the cycle.

### Changed
- `build` runs the suite and the build on its new branch before writing anything, stops on a red suite, and tells the tester what already failed.
- **Checkpoints carry what a resumed session needs**: the approved critical test list, each tester report verbatim, which tests came from the tester and where they moved, the entry before the documents step. A resumed branch missing one redoes that step.
- `fix`: a flaky test is reproduced by repeated runs, before and after; a CI failure caused by its config goes to `chore`; only bugs users could see get a Fixed line.
- `chore`: comments that tools read (doctests, lint or compiler directives, typed JSDoc) leave the prose short path; a missing-tests chore that finds a bug stops and offers `fix`.
- Releases start from the up-to-date main branch, and a tool-generated changelog isn't edited by hand.
- The reviewer counts a repeated test as a suggestion, not blocking; blocking stays for tests that pass with the code broken.
- `setup` allows the read-only commands every round runs (`git write-tree`, branch and worktree listing, `git remote`, `git ls-remote`, `git pull --rebase`, `gh pr list`).
- Behavior eval graders look for the blocks inside a `git commit`, and the fixture's CLAUDE.md tells agents where git is.

### Fixed
- **Git cases the flow left to improvisation**: a push rejected by branch protection stops and offers pull request mode instead of looping; commit-msg hooks get an adapted first line; a worktree branch is detached before it's deleted, and both worktree cases can hold at once; conflicts only in BACKLOG.md or CHANGELOG.md keep both sides, others say how to continue; a failed `pull --rebase` is aborted; Resume finds branches only on the remote; review comments on a pull request are handled as post-verification fixes; the verification commit uses `--allow-empty`; a revert reapplies document changes that rode along and puts the restored entry back to Idea.
- Contradictions: In progress on a reused worktree branch, the SPEC outline approved in `brainstorm`, the documents' language before CLAUDE.md exists, the setup's test setup in its review and apply steps, the cycle check in `fix` and `chore`, `build` citing git-flow before reading it, and a feature declared done without `build`.
- Leftovers: `git push origin` in releases, partial copies of the test patterns in the agents, and the README on the entry, the diagram and the reviewer's inputs.

## [0.16.0] - 2026-11-04

Behavior evals run the cycle for real, projects without tests are supported, and shared rules move to one place each.

### Added
- **Behavior evals** in `evals/behavior/`: the cycle runs for real on a small fixture project and the graders check what Claude did: `build-flow` (In progress on main, feature branch, `wip:` checkpoints, tester and reviewer, `Critical tests:`, squash), `fix-flow` (fix branch, `Regression tests:`, review, no tester) and `chore-prose-flow` (one commit on main, no branch, suite or review).
- **Projects without tests**: `setup` proposes a minimal test setup (the stack's standard framework, a command, a passing smoke test) in the same approval, instead of stopping; `build` offers tests of the current behavior, as a chore, before changing modules that have none.
- Trigger evals: a bug left for later fires `document` (not `fix`), a flaky test and a slowdown fire `fix` (not `chore`), "X is done" fires `document` (not `build`), reading CHANGELOG.md fires no skill, and new behavior asked as a wish fires `document` or `grilling`.

### Changed
- `fix` and `chore` say where flaky tests, failing CI and slowdowns go: a regression or a broken limit is a bug; making something faster that nobody reported as slow is a chore.
- **The cycle check is literal**: `build`, `fix` and `chore` run only where CLAUDE.md says the project uses the `minidev` cycle, not where it merely mentions a build or a fix; `document` works outside the cycle only when the user explicitly asks to change one of its files.
- **The documents' language is recorded** in CLAUDE.md (`Documents: <language>`): `setup` writes it, `brainstorm` asks it in the plan, and `document` asks once and records it when nothing says.
- `brainstorm`'s plan approval covers the SPEC.md outline, so `document` doesn't ask for it again.
- `setup` leaves Build out for projects without one and lists commands per package in a monorepo.
- Skills load `minidev:grilling` by its full name, so another installed `grilling` isn't picked.
- **Test pruning has its own reference**, `chore/references/prune.md`: one linear procedure from branch to merge, instead of a section of `chore` that replaced and extended numbered steps elsewhere. It's loaded only for a prune.
- **One verification message format**, in `git-flow.md` (The verification commit), with every section and the exact block names `git log --grep` searches; `build`, `fix`, `chore` and the review and test-value references say only which sections they use, instead of describing the blocks in four places.
- **Fixed prompts for the tester and the reviewer**: `build` and `review.md` give the exact prompt to fill in (entry, SPEC constraints, base commit, commands, whether a tester ran), so nothing else reaches the agents.

### Fixed
- `fix` runs the suite before writing the reproducing test, so older failures aren't mistaken for the bug, and stops with an offer to record a Bug entry when the bug can't be reproduced at all.
- Discarding an In progress feature carries document changes made on its branch (an idea recorded meanwhile) to the main branch before the branch is deleted.
- Changelog compare links are left out when there's no remote to link to.
- **Checking the repository after the tester and the reviewer** is one procedure in `git-flow.md` (Check after an agent): it compares `HEAD` and the staged tree (`git write-tree`) too, restores tracked files from the staged version, sends tool output (coverage, caches) to `.gitignore` instead of flagging it, and asks before deleting any other new file, which `git restore` can't remove.
- **Git flow is sturdier**: the main branch is found even when `<remote>/HEAD` isn't set (`git ls-remote --symref`), with any remote name; worktrees are handled (an app-made session branch can become the work's branch, and the main branch checked out elsewhere is worked on with `git -C`); a rejected push in local merge undoes the local squash and starts over instead of forcing; a pre-commit hook that rejects a `wip:` checkpoint leads to one question about `--no-verify`, recorded in CLAUDE.md; fixing a merge with the main branch stops after 3 failing rounds.

## [0.15.0] - 2026-11-04

Prose-only chores take a short path, and local merge runs the suite once less.

### Added
- **Short path for prose**: a `chore` that only touches docs files or code comments skips the branch (in local merge mode), the suite run before and the review; the build runs if it processes those files, links are checked, and the change is one plain commit. A text the product shows, or anything else, still takes the full path.

### Changed
- **Local merge runs the suite once less**: after the squash, `git diff --quiet <branch> HEAD` confirms the main branch holds exactly the tree tested on the branch, and the suite and build run again only if it doesn't. The run after merging the main branch into the branch is skipped when that merge brought nothing and they already passed on the branch's last commit.

## [0.14.0] - 2026-11-04

Product constraints reach the tester and reviewer, and the documents are reviewed with the code.

### Changed
- **Product constraints reach the checks**: SPEC.md's Constraints (whole-product limits like "works offline", which entries don't repeat) count in `build`'s rules check and critical test list, and are passed, copied in full, to the `tester` and the `reviewer`. The tester lists them among the rules to cover; the reviewer blocks a change that breaks one.
- **Documents before the review**: `build`, `fix` and `chore` update SPEC.md, CHANGELOG.md and BACKLOG.md before the `reviewer` runs, so the rules written from what was built are read against the code by someone who didn't write them. The reviewer blocks a SPEC rule the code doesn't follow, new behavior SPEC.md doesn't state, a rule left false, or a changelog line that claims more than was done. Fixes after the review update the documents again.

## [0.13.0] - 2026-11-04

Work can be resumed in a new session, and In progress is visible from the main branch.

### Added
- **Resume**: `git-flow.md` says how to continue work from an earlier session: find its branch (and worktree or pull request), read its `wip:` checkpoints, which now name the step done, run the suite and go on from the next step. `build`, `fix` and `chore` resume instead of starting again when the work already has a branch; `build` also when its entry is In progress. Trigger eval: "continue feature X" fires `build`.

### Changed
- **In progress is set on the main branch**, committed there right before the feature's branch is created, so the main branch's BACKLOG.md shows what is being built and "another feature is In progress" is seen from any branch or session. The **To check by hand** list is added on the branch once the critical test list is approved. Pausing is written on the main branch and keeps the branch; discarding an In progress feature asks whether to delete its branch.
- Bringing the main branch up to date falls back to `git pull --rebase` when it holds local document commits not yet pushed.

## [0.12.1] - 2026-11-04

The revert flow, the spec's lifecycle and the reviewer's inputs no longer contradict each other.

### Fixed
- **Revert** no longer contradicts the documents: `git revert` already undoes the change's SPEC rules, changelog line and backlog removal, so `document` only puts back a line from a released version (recording the revert under `[Unreleased]`) and adds what went wrong to the restored entry. `document` and the backlog reference name the revert as the one exception to "a failure in use is a bug".
- SPEC.md's legend, the spec reference and `document` say the spec changes with fixes, chores and reverts too, not only when a feature is finished; `fix` says when it may change a rule without becoming a feature.
- The `reviewer` is told whether a tester ran, instead of assuming one did for every feature; its description and the README mention its check of the tests.
- The test-value sabotage covers tests written after the code (missing tests), as `chore` already used it, and names the agents' copies of its patterns that must change with it.
- `brainstorm`'s description sends existing projects to `setup` first, as its body does.
- The verification message is written by the skill that built the feature, not by `document`.
- README: full paths to the build references, the local-merge flow in the diagram, the reviewer gets the base commit (not the diff), the chore changelog exception; the marketplace description matches `plugin.json`; the three-document table in `document`, the setup template and the trigger evals mention bugs, debt and constraints.

## [0.12.0] - 2026-11-04

Tests are judged by their value: a shared reference, a check in every change, missing-test chores and test pruning.

### Added
- **Test value**: `test-value.md`, next to `review.md`, holds what makes a test worth keeping, the patterns of useless tests, which tests are protected and the **sabotage** check (break a rule on purpose to show the test that stays fails). `build`, `fix` and `chore` read it; the `tester` and `reviewer` judge tests by the same rules.
- **Check the tests** in every change that adds them: after the refactor, the change's new tests are tied to rules and compared with each other and with the existing tests; the author merges or removes only their own extras, protected tests go to the user, and redundant older tests are noted for a later prune.
- **Missing tests** are a chore: new tests for rules that have none, each shown failing by sabotage.
- **Test pruning** in `chore`, on request ("clean up the useless tests"): the whole suite mapped to SPEC.md rules, regressions and outside contracts, a list of candidates for the user's approval with the test that keeps each rule, removal by module with the production code only those tests kept alive, a sabotage per rule, and rules with no test recorded as Debt. No target number unless the user gives one.
- Verification commits list critical and regression tests in `Critical tests:` (`build`) and `Regression tests:` (`fix`) blocks, and older tests a change made redundant in `Redundant older tests:`, so a prune can find them with `git log --grep`.
- Trigger evals: a prune request and a request for missing tests fire `chore`.

### Changed
- The tester's kept tests move out of their `tester` files into the module's tests before the review, instead of staying in separate files on main.
- The `tester` writes an extra test only when no existing test would already fail in that case, and reports the failure only it catches.
- The `reviewer` blocks tests that would pass with the code broken, repeats inside the same diff and removed tests whose rule nothing checks; other test issues are suggestions. A blocking fix that touches a protected test goes to the user first.

## [0.11.0] - 2026-11-04

Pushed changes can be reverted, and local merge tests the combined code before main gets it.

### Added
- **Revert**: when a change already pushed breaks, the user chooses between fixing forward with `fix` and reverting its one squashed commit on a `fix/revert-<name>` branch; a reverted feature goes back to BACKLOG.md as an Idea. The main branch's pushed history is never rewritten.
- `review.md`, next to `git-flow.md`: the reviewer protocol (launch, state check, acting on the report, what changes for `build`, `fix` and `chore`) in one file the three skills read, instead of `fix` and `chore` reading a section of `build`.
- The plugin ships its own `LICENSE`, so installed copies carry it.

### Changed
- **Local merge** tests the combined code on the branch first: main is merged into the branch, the suite and build run there, and failures are fixed there. Main gets the squash only after that, and a failed confirmation run undoes the local commit instead of leaving main broken.
- **The tester's report isn't filtered by the author**: removing a tester's test or calling a failure an assumption goes to the user first, a test the author thinks is wrong is the user's call, and the last report goes into the verification message verbatim.

## [0.10.1] - 2026-11-04

Fixes to the reviewer's assumptions, the skills' boundaries and setup's permissions.

### Fixed
- The `reviewer` no longer assumes a tester ran: in `fix` and `chore` it also checks that the change keeps the behavior it should. `build` checks that `HEAD` didn't move while it ran, instead of claiming it can't edit files.
- `fix` and `chore` name the file and section they take from `build` (cycle check inline, Review in `../build/SKILL.md`), and say how a blocking finding that changes behavior is handled without a tester.
- `brainstorm` puts whole-product constraints in SPEC.md's Constraints instead of copying them into each backlog entry, as the backlog format says.
- `document` doesn't commit the documents `brainstorm` and `setup` create (those skills offer the commit); its operation index, lifecycle and confirmation table cover Bug and Debt entries and chores.
- Skill descriptions mark the boundaries between `build`, `fix` and `chore` (typos and refactors are chores).
- `setup` discovers a type-check command, allows the read-only git commands the cycle runs (and `git pull --ff-only`), and lists the `reviewer` and `brainstorm` among old global copies.
- Changelog version headings use a hyphen, as in Keep a Changelog.
- README: branch order in the cycle, the reviewer in the `build` row, `git-flow.md` shared by `chore` and releases too, and a numbered list that rendered broken.
- Trigger evals (plugin development only): the simulated CLAUDE.md now includes the `chore` line from the setup template.

## [0.10.0] - 2026-11-03

An independent reviewer agent checks every change for what tests don't catch.

### Added
- **Reviewer agent**: a read-only, independent code review of every change, after the tester, looking for what tests don't catch (risky logic, error handling, security, design, leftovers, the project's conventions). Blocking findings are fixed or brought to the user; suggestions are applied when clearly better and cheap. `fix` and `chore` run it whenever they change code.

### Changed
- `build` gets a mandatory refactor step with the suite green before the review, replacing the optional cleanup; the verification message records the review.

## [0.9.0] - 2026-11-03

The `chore` skill handles changes that keep behavior, and the backlog takes bugs and debt.

### Added
- **chore skill**: changes that keep the behavior (refactoring, debt, dependency upgrades, migrations, tooling, typos) get their own `chore/<name>` branch, with the suite green before and after and behavior tests left untouched. No critical list or tester; SPEC.md and CHANGELOG.md change only when a technical decision or something users notice did.
- **Bug and Debt entries** in BACKLOG.md, for bugs and chores left for later; they leave the file when `fix` or `chore` does them.
- **Trigger evals** (plugin development only, the skills don't change): 16 `claude plugin eval` cases checking that each skill fires on its own requests and that `brainstorm`, `fix`, `chore` and the cycle's skills stay quiet where they'd be wrong.

## [0.8.0] - 2026-11-03

Non-functional constraints are recorded, tested and checked by hand.

### Added
- **Constraints**: backlog entries get a Constraints field for non-functional requirements (speed, security, accessibility, compatibility, privacy, volume), written so they can be checked. `build` asks about obvious unaddressed risks, turns measurable constraints into tests or checks and the rest into "To check by hand"; the tester covers them and pushes them to their limit. SPEC.md gets a Constraints section for the whole product, and `brainstorm` carries its constraints into each feature.

## [0.7.0] - 2026-11-03

Pull request mode and resumable checkpoints arrive.

### Added
- **Pull request mode**: `setup` asks how branches reach main and records it in CLAUDE.md. In pull request mode the branch is pushed, a pull request is opened with the verification message, and it's squash-merged once the checks pass; releases go through a `release/<version>` pull request.
- **Checkpoints**: `wip:` commits on the branch whenever a step is done, so work can be resumed in a new session or paused for a bug fix.

### Changed
- Branches reach main as one squashed commit carrying the verification message, in both modes. Document changes made on a branch get a line in that message.

## [0.6.0] - 2026-11-03

The git flow lives in one shared reference, and merges are tested before they're pushed.

### Changed
- **Tester**: writes its tests in new files whose name contains `tester`, never changes git state, and declares `model: inherit`. After each round, `build` checks it only added test files and removes assumption tests before staging again.
- **Merge**: the test suite and build run again on the merged main branch before it's pushed. The main branch is the remote's default branch when there is one.
- **Staging**: `git status` is read before `git add -A`, so build output or secrets don't end up in the commit.
- **Tests first**: a new module gets a stub of its public interface, so the tests fail on missing behavior, not on the import.
- The branch, staging and merge steps live in one place, `skills/build/references/git-flow.md`, shared by `build` and `fix`.

## [0.5.0] - 2026-10-29

The `fix` skill fixes bugs test-first on their own branch.

### Added
- **fix skill**: fixes bugs on their own branch, test-first when they can be reproduced.

### Changed
- The tester reads the full change, new files included, from the base commit.
- `build` and `document` only act in projects set up for the cycle.
- The CLAUDE.md written by `setup` only names which skill handles each step, so plugin updates reach every project.

## [0.4.0] - 2026-10-29

The `brainstorm` skill starts a new project from an idea.

### Added
- **brainstorm skill**: takes a new project from an idea to a scaffold whose tests and build pass, with its plan in BACKLOG.md and SPEC.md.

## [0.3.0] - 2026-10-29

The plugin is renamed to minidev, and work happens on branches.

### Changed
- Plugin and marketplace renamed to `minidev`. Features and fixes are built on their own branches and merged into main once checked.

[Unreleased]: https://github.com/ramonk2o/minidev/compare/v0.31.0...HEAD
[0.31.0]: https://github.com/ramonk2o/minidev/compare/v0.30.0...v0.31.0
[0.30.0]: https://github.com/ramonk2o/minidev/compare/v0.29.0...v0.30.0
[0.29.0]: https://github.com/ramonk2o/minidev/compare/v0.28.0...v0.29.0
[0.28.0]: https://github.com/ramonk2o/minidev/compare/v0.27.0...v0.28.0
[0.27.0]: https://github.com/ramonk2o/minidev/compare/v0.26.0...v0.27.0
[0.26.0]: https://github.com/ramonk2o/minidev/compare/v0.25.3...v0.26.0
[0.25.3]: https://github.com/ramonk2o/minidev/compare/v0.25.2...v0.25.3
[0.25.2]: https://github.com/ramonk2o/minidev/compare/v0.25.1...v0.25.2
[0.25.1]: https://github.com/ramonk2o/minidev/compare/v0.25.0...v0.25.1
[0.25.0]: https://github.com/ramonk2o/minidev/compare/v0.24.1...v0.25.0
[0.24.1]: https://github.com/ramonk2o/minidev/compare/v0.24.0...v0.24.1
[0.24.0]: https://github.com/ramonk2o/minidev/compare/v0.23.0...v0.24.0
[0.23.0]: https://github.com/ramonk2o/minidev/compare/v0.22.0...v0.23.0
[0.22.0]: https://github.com/ramonk2o/minidev/compare/v0.21.0...v0.22.0
[0.21.0]: https://github.com/ramonk2o/minidev/compare/v0.20.0...v0.21.0
[0.20.0]: https://github.com/ramonk2o/minidev/compare/v0.19.0...v0.20.0
[0.19.0]: https://github.com/ramonk2o/minidev/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/ramonk2o/minidev/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/ramonk2o/minidev/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/ramonk2o/minidev/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/ramonk2o/minidev/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/ramonk2o/minidev/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/ramonk2o/minidev/compare/v0.12.1...v0.13.0
[0.12.1]: https://github.com/ramonk2o/minidev/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/ramonk2o/minidev/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/ramonk2o/minidev/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/ramonk2o/minidev/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/ramonk2o/minidev/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/ramonk2o/minidev/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/ramonk2o/minidev/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/ramonk2o/minidev/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/ramonk2o/minidev/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/ramonk2o/minidev/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/ramonk2o/minidev/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/ramonk2o/minidev/tree/v0.3.0
