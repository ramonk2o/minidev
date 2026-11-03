# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.10.0] - 2026-11-03

### Added
- **Reviewer agent**: a read-only, independent code review of every change, after the tester, looking for what tests don't catch (risky logic, error handling, security, design, leftovers, the project's conventions). Blocking findings are fixed or brought to the user; suggestions are applied when clearly better and cheap. `fix` and `chore` run it whenever they change code.

### Changed
- `build` gets a mandatory refactor step with the suite green before the review, replacing the optional cleanup; the verification message records the review.

## [0.9.0] - 2026-11-03

### Added
- **chore skill**: changes that keep the behavior (refactoring, debt, dependency upgrades, migrations, tooling, typos) get their own `chore/<name>` branch, with the suite green before and after and behavior tests left untouched. No critical list or tester; SPEC.md and CHANGELOG.md change only when a technical decision or something users notice did.
- **Bug and Debt entries** in BACKLOG.md, for bugs and chores left for later; they leave the file when `fix` or `chore` does them.
- **Trigger evals** (plugin development only, the skills don't change): 16 `claude plugin eval` cases checking that each skill fires on its own requests and that `brainstorm`, `fix`, `chore` and the cycle's skills stay quiet where they'd be wrong.

## [0.8.0] - 2026-11-03

### Added
- **Constraints**: backlog entries get a Constraints field for non-functional requirements (speed, security, accessibility, compatibility, privacy, volume), written so they can be checked. `build` asks about obvious unaddressed risks, turns measurable constraints into tests or checks and the rest into "To check by hand"; the tester covers them and pushes them to their limit. SPEC.md gets a Constraints section for the whole product, and `brainstorm` carries its constraints into each feature.

## [0.7.0] - 2026-11-03

### Added
- **Pull request mode**: `setup` asks how branches reach main and records it in CLAUDE.md. In pull request mode the branch is pushed, a pull request is opened with the verification message, and it's squash-merged once the checks pass; releases go through a `release/<version>` pull request.
- **Checkpoints**: `wip:` commits on the branch whenever a step is done, so work can be resumed in a new session or paused for a bug fix.

### Changed
- Branches reach main as one squashed commit carrying the verification message, in both modes. Document changes made on a branch get a line in that message.

## [0.6.0] - 2026-11-03

### Changed
- **Tester**: writes its tests in new files whose name contains `tester`, never changes git state, and declares `model: inherit`. After each round, `build` checks it only added test files and removes assumption tests before staging again.
- **Merge**: the test suite and build run again on the merged main branch before it's pushed. The main branch is the remote's default branch when there is one.
- **Staging**: `git status` is read before `git add -A`, so build output or secrets don't end up in the commit.
- **Tests first**: a new module gets a stub of its public interface, so the tests fail on missing behavior, not on the import.
- The branch, staging and merge steps live in one place, `skills/build/references/git-flow.md`, shared by `build` and `fix`.

## [0.5.0] - 2026-10-29

### Added
- **fix skill**: fixes bugs on their own branch, test-first when they can be reproduced.

### Changed
- The tester reads the full change, new files included, from the base commit.
- `build` and `document` only act in projects set up for the cycle.
- The CLAUDE.md written by `setup` only names which skill handles each step, so plugin updates reach every project.

## [0.4.0] - 2026-10-29

### Added
- **brainstorm skill**: takes a new project from an idea to a scaffold whose tests and build pass, with its plan in BACKLOG.md and SPEC.md.

## [0.3.0] - 2026-10-29

### Changed
- Plugin and marketplace renamed to `minidev`. Features and fixes are built on their own branches and merged into main once checked.
