---
name: chore
description: In projects set up for the minidev cycle (a CLAUDE.md that names it), make a change that keeps the product's behavior as it is, on its own branch, with the test suite green before and after: refactoring, technical debt, dependency upgrades, migrations, tooling, build or CI config, and small fixes to text, comments or docs. Use it whenever the user wants to clean up, refactor, reorganize or simplify code, upgrade or replace a dependency, migrate a tool, or fix a typo, e.g. "refactor the storage module", "update React to 19", "atualiza as dependências", "fix the typo in the README", "/minidev:chore X". Not for broken behavior (fix) or new behavior (document, then build).
---

# Chore

Makes a change the user doesn't see in the product's behavior: the code, its dependencies or its tooling change, the rules don't. A chore has no critical test list and no independent tester (only a review of the code); its proof is the existing test suite, green before and after, with the tests that check behavior left as they were.

Talk to the user in the language of the conversation. Project instructions (CLAUDE.md, AGENTS.md…) define the test and build commands; when they conflict with this skill, they win.

## 1. Check it's a chore

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) names the `minidev` cycle or the `chore` skill. If it doesn't, offer `/minidev:setup` or simply make the change without this skill.

If the change alters what the user sees or a rule in SPEC.md, it isn't a chore: broken behavior is a bug (`fix`), new or different behavior is a feature (`document`, then `build`). Say so and switch. A dependency upgrade that forces a visible change (a removed option, a new minimum version) is still a chore, but tell the user what will change before starting.

If BACKLOG.md has an entry for it (type Debt), use it as the description of the work.

## 2. Work

1. Read the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder) and create the `chore/<short-name>` branch as it says (Start the branch).
2. Run the test suite and the build **before** changing anything, and record the result. If they already fail, stop and show the user: a chore on a red suite can't prove it changed nothing. They decide whether to fix that first (with `fix`) or go on knowing which failures were there before.
3. Make the change. Commit `wip:` checkpoints as in `git-flow.md`.
   - **Refactoring, debt, migrations:** don't change the tests that check behavior; if one fails, the change broke something, not the test. A test that checks an internal detail the refactoring removes may be changed: say which and why, and ask before changing it.
   - **Dependency upgrades:** read the dependency's changelog or migration guide between the two versions for breaking changes before upgrading, and upgrade one dependency (or one group that must move together) at a time.
   - **Text, comments, docs:** no tests to add; the suite and build still run, since docs can be part of the build.
4. Run the test suite and the build again: everything that passed before must pass now.
5. If the change touches code (not only text, docs or a version number), launch the `reviewer` agent (agent type `minidev:reviewer`) as in the `build` skill's Refactor and review section, Review (`../build/SKILL.md` from this skill's folder; read only that part), passing the chore's description (or its Debt entry) instead of a feature entry. For a refactoring it's the only independent look at the new structure. A blocking finding whose fix would change behavior means the work is no longer only a chore: stop and tell the user, and handle that part as a bug (`fix`) or a feature.

## 3. Finish

1. Update the documents, with the `document` skill, only where the chore touched what they describe:
   - **SPEC.md** when a technical decision changed (a dependency added, replaced or removed, storage, structure the spec names), with its reason.
   - **CHANGELOG.md** only when the people who use the product will notice: a new minimum version, faster loading, a security upgrade (under Security). Otherwise nothing: an internal refactoring isn't news (a notable change to project docs or tooling may still get a line, as the changelog reference allows).
   - **BACKLOG.md**: remove the Debt entry, if there was one.
2. Stage the work and make the branch's verification commit, as in `git-flow.md`: its message is what the main branch gets. It records what changed and why, the suite and build results before and after, for an upgrade the versions and any breaking change handled, and the review, if there was one. If something should be checked in the real app (an upgraded UI library, a build tool), end the message with a block starting with a line that says exactly `To check by hand:`, one item per line.
3. Show the user what to check, if anything, and wait for their confirmation.
4. Merge, test and push as in `git-flow.md` (Merge and push), in the project's integration mode.
