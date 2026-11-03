# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
