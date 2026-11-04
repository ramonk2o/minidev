---
name: chore
description: In projects set up for the minidev cycle (a CLAUDE.md that says it uses the `minidev` cycle), make a change that keeps the product's behavior as it is, on its own branch, with the test suite green before and after (prose and wording fixes to product text take short paths): refactoring, technical debt, dependency upgrades, migrations, tooling, build or CI config, small fixes to text, comments or docs, adding missing tests and pruning useless ones. Use it whenever the user wants to clean up, refactor, reorganize or simplify code, add tests to code that has none, remove useless or duplicated tests, upgrade or replace a dependency, migrate a tool, or fix a typo, e.g. "refactor the storage module", "update React to 19", "atualiza as dependências", "fix the typo in the README", "limpa os testes inúteis", "/minidev:chore X". Not for broken behavior, flaky tests or something that got slower (fix), or new behavior (document, then build). Making something faster that nobody reported as slow is a chore.
---

# Chore

Makes a change the user doesn't see in the product's behavior: the code, its dependencies or its tooling change, the rules don't. A chore has no critical test list and no independent tester (only a review of the code); its proof is the existing test suite, green before and after, with the tests that check behavior left as they were. Adding tests for rules that have none is a chore too; pruning tests is the one chore that removes existing tests, under its own procedure (`references/prune.md`).

Talk to the user in the language of the conversation. Project instructions (CLAUDE.md, AGENTS.md…) define the test and build commands; when they conflict with this skill, they win.

## 1. Check it's a chore

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) says it uses the `minidev` cycle (the line `/minidev:setup` writes: "This project uses the `minidev` cycle"). A CLAUDE.md that only mentions a build command or a fix isn't that. If not, don't create a backlog, branches or documents in it: offer `/minidev:setup` and stop, or simply make the change without this skill if the user prefers.

If the change alters what the user sees or a rule in SPEC.md, it isn't a chore: broken behavior is a bug (`fix`), new or different behavior is a feature (`document`, then `build`). Say so and switch. A dependency upgrade that forces a visible change (a removed option, a new minimum version) is still a chore, but tell the user what will change before starting.

If BACKLOG.md has an entry for it (type Debt), use it as the description of the work.

If the change only touches prose (Markdown or other docs files, and comments in code), follow the prose short path below instead of sections 2 and 3. If it only fixes the wording of text the product shows (a typo, punctuation, the same message said better, in code strings or translation files), follow the product text short path. Anything else takes the full path, including comments that tools read: doctests, lint or compiler directives (`eslint-disable`, `noqa`, `//go:build`, `@ts-expect-error`), type annotations in comments (JSDoc in a type-checked project). A new text, or one that changes what a message means, isn't a wording fix: it's a feature (or a bug, if the text was wrong).

### Short path: prose only

Prose can't break the code, so a branch, a suite run before and a review would only add cost. What can still break is the build, when it builds the docs, and links.

1. In **local merge** mode, work on the main branch: bring it up to date and handle uncommitted or in-progress work as in the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder), The main branch and Start the branch. In **pull request** mode, create a `chore/<short-name>` branch as that file says: the main branch only takes pull requests.
2. Make the change. Check that any link or anchor you touched still points somewhere.
3. If the build processes these files (a docs site, a README bundled in a package), run it.
4. Show the diff, then commit with a one-line message (e.g. `docs: fix typo in the README title`), with a line for the build result if it ran; no verification blocks. Product documents (BACKLOG.md, SPEC.md, CHANGELOG.md) are still changed only through the `document` skill.
5. Local merge: push the main branch if it has a remote. Pull requests: bring it in as in `git-flow.md` (Merge and push).

If, while working, the change turns out to touch anything but prose, stop and switch to the full path from section 2 (in local merge mode, move the work to a branch first: `git switch -c chore/<short-name>`).

### Short path: product text

A wording fix can't change behavior, but a test may check that string, so the suite runs once, after the change; there's still no branch in local merge mode, no suite run before and no review.

1. Start as in the prose short path, step 1.
2. Search the tests for the old text (e.g. `grep -rn "<old text>" <test folders>`). A test that checks it checks a text users may depend on: changing that test goes to the user first, and with their OK it changes in the same commit.
3. Make the change, only in the strings.
4. Run the test suite and the build once. If something fails that the step 2 search didn't predict, the change did more than wording: undo it and take the full path.
5. Show the diff, then commit with a one-line message (e.g. `chore: fix typo in the empty-note error`) and a line with the test and build results; no verification blocks. CHANGELOG.md gets a line only if users will notice (rarely, for a wording fix), through the `document` skill.
6. Finish as in the prose short path, step 5.

If the change turns out to touch anything but the wording, switch to the full path as above.

## 2. Work

1. Read the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder) and create the `chore/<short-name>` branch as it says (Start the branch), or resume it if this work was started before (Resume).
2. Run the test suite and the build **before** changing anything, and record the result. If they already fail, stop and show the user: a chore on a red suite can't prove it changed nothing. They decide whether to fix that first (with `fix`) or go on knowing which failures were there before.
3. Make the change. Commit `wip:` checkpoints as in `git-flow.md`.
   - **Refactoring, debt, migrations:** don't change the tests that check behavior; if one fails, the change broke something, not the test. A test that checks an internal detail the refactoring removes may be changed: say which and why, and ask before changing it.
   - **Dependency upgrades:** read the dependency's changelog or migration guide between the two versions for breaking changes before upgrading, and upgrade one dependency (or one group that must move together) at a time.
   - **Text mixed with other changes** (prose only takes the short path in section 1): no tests to add for the text; the suite and build still run.
   - **Missing tests:** test the rules of SPEC.md (or of the Debt entry) from the outside, and show each new test fails when its rule is sabotaged, as in the `build` skill's `references/test-value.md` (`../build/references/test-value.md` from this skill's folder): a test written after the code can't be shown failing first. If a test of a SPEC.md rule fails on the code as it is, the code has a bug: don't write the test to match it, and don't fix the code in the chore. Stop and tell the user, and offer `fix` (or recording it as a Bug entry); if it's unclear whether the code or SPEC.md is right, ask.
4. Run the test suite and the build again: everything that passed before must pass now.
5. If the change added or edited tests, check them as in `test-value.md` (Check the change's tests).
6. Update the documents, with the `document` skill, only where the chore touched what they describe:
   - **SPEC.md** when a technical decision changed (a dependency added, replaced or removed, storage, structure the spec names), with its reason.
   - **CHANGELOG.md** only when the people who use the product will notice: a new minimum version, faster loading, a security upgrade (under Security). Otherwise nothing: an internal refactoring isn't news (a notable change to project docs or tooling may still get a line, as the changelog reference allows).
   - **BACKLOG.md**: remove the Debt entry, if there was one.

   This comes before the review, so the reviewer reads the documents with the code.
7. If the change touches code (not only text, docs or a version number), have it reviewed by the `reviewer` agent as in the `build` skill's `references/review.md` (`../build/references/review.md` from this skill's folder), passing the chore's description (or its Debt entry), and act on its report as that file says for `chore`. For a refactoring it's the only independent look at the new structure.

## 3. Finish

1. If the review's fixes changed what the documents say, update them with the `document` skill.
2. Stage the work and make the branch's verification commit, in the format of `git-flow.md` (The verification commit): its message is what the main branch gets. A chore has no Tester, `Critical tests:` or `Regression tests:` section; its Tests line gives the results before and after, and for an upgrade the versions and any breaking change handled. If something should be checked in the real app (an upgraded UI library, a build tool), list it under `To check by hand:`.
3. Show the user what to check, if anything, and wait for their confirmation.
4. Merge, test and push as in `git-flow.md` (Merge and push), in the project's integration mode.

## 4. Pruning tests

A request to remove useless or duplicated tests follows `references/prune.md` from start to finish, instead of sections 2 and 3.
