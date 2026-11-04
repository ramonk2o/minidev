---
name: chore
description: In projects set up for the minidev cycle (a CLAUDE.md that names it), make a change that keeps the product's behavior as it is, on its own branch, with the test suite green before and after: refactoring, technical debt, dependency upgrades, migrations, tooling, build or CI config, small fixes to text, comments or docs, adding missing tests and pruning useless ones. Use it whenever the user wants to clean up, refactor, reorganize or simplify code, add tests to code that has none, remove useless or duplicated tests, upgrade or replace a dependency, migrate a tool, or fix a typo, e.g. "refactor the storage module", "update React to 19", "atualiza as dependências", "fix the typo in the README", "limpa os testes inúteis", "/minidev:chore X". Not for broken behavior (fix) or new behavior (document, then build).
---

# Chore

Makes a change the user doesn't see in the product's behavior: the code, its dependencies or its tooling change, the rules don't. A chore has no critical test list and no independent tester (only a review of the code); its proof is the existing test suite, green before and after, with the tests that check behavior left as they were. Adding tests for rules that have none is a chore too; pruning tests is the one chore that removes existing tests, under its own rules (section 4).

Talk to the user in the language of the conversation. Project instructions (CLAUDE.md, AGENTS.md…) define the test and build commands; when they conflict with this skill, they win.

## 1. Check it's a chore

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) names the `minidev` cycle or the `chore` skill. If it doesn't, offer `/minidev:setup` or simply make the change without this skill.

If the change alters what the user sees or a rule in SPEC.md, it isn't a chore: broken behavior is a bug (`fix`), new or different behavior is a feature (`document`, then `build`). Say so and switch. A dependency upgrade that forces a visible change (a removed option, a new minimum version) is still a chore, but tell the user what will change before starting.

If BACKLOG.md has an entry for it (type Debt), use it as the description of the work.

## 2. Work

1. Read the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder) and create the `chore/<short-name>` branch as it says (Start the branch), or resume it if this work was started before (Resume).
2. Run the test suite and the build **before** changing anything, and record the result. If they already fail, stop and show the user: a chore on a red suite can't prove it changed nothing. They decide whether to fix that first (with `fix`) or go on knowing which failures were there before.
3. Make the change. Commit `wip:` checkpoints as in `git-flow.md`.
   - **Refactoring, debt, migrations:** don't change the tests that check behavior; if one fails, the change broke something, not the test. A test that checks an internal detail the refactoring removes may be changed: say which and why, and ask before changing it.
   - **Dependency upgrades:** read the dependency's changelog or migration guide between the two versions for breaking changes before upgrading, and upgrade one dependency (or one group that must move together) at a time.
   - **Text, comments, docs:** no tests to add; the suite and build still run, since docs can be part of the build.
   - **Missing tests:** test the rules of SPEC.md (or of the Debt entry) from the outside, and show each new test fails when its rule is sabotaged, as in the `build` skill's `references/test-value.md` (`../build/references/test-value.md` from this skill's folder): a test written after the code can't be shown failing first.
   - **Pruning tests:** follow section 4 instead of this step.
4. Run the test suite and the build again: everything that passed before must pass now.
5. If the change added or edited tests (outside a prune), check them as in `test-value.md` (Check the change's tests).
6. Update the documents, with the `document` skill, only where the chore touched what they describe:
   - **SPEC.md** when a technical decision changed (a dependency added, replaced or removed, storage, structure the spec names), with its reason.
   - **CHANGELOG.md** only when the people who use the product will notice: a new minimum version, faster loading, a security upgrade (under Security). Otherwise nothing: an internal refactoring isn't news (a notable change to project docs or tooling may still get a line, as the changelog reference allows).
   - **BACKLOG.md**: remove the Debt entry, if there was one.

   This comes before the review, so the reviewer reads the documents with the code.
7. If the change touches code (not only text, docs or a version number), have it reviewed by the `reviewer` agent as in the `build` skill's `references/review.md` (`../build/references/review.md` from this skill's folder), passing the chore's description (or its Debt entry), and act on its report as that file says for `chore`. For a refactoring it's the only independent look at the new structure.

## 3. Finish

1. If the review's fixes changed what the documents say, update them with the `document` skill.
2. Stage the work and make the branch's verification commit, as in `git-flow.md`: its message is what the main branch gets. It records what changed and why, the suite and build results before and after, for an upgrade the versions and any breaking change handled, the check of the tests and the review, if there were any. If something should be checked in the real app (an upgraded UI library, a build tool), end the message with a block starting with a line that says exactly `To check by hand:`, one item per line.
3. Show the user what to check, if anything, and wait for their confirmation.
4. Merge, test and push as in `git-flow.md` (Merge and push), in the project's integration mode.

## 4. Pruning tests

Removes the tests that don't earn their place, across the whole project unless the user names a part of it. Read `../build/references/test-value.md` first: it holds the rules, the patterns, the protected tests and the sabotage this section uses. Sections 2 and 3 still apply: steps 1 to 4 below replace step 3 of section 2, step 5 adds to its review (step 7) and step 6 to the verification message (section 3, step 2).

1. **Map.** Handle skipped tests as that file says. Tie each test to what it keeps: a rule of SPEC.md (or its Constraints), a regression, an outside contract. Find the protected tests (`Critical tests:` and `Regression tests:` blocks, or the fallback for older projects) and the `Redundant older tests:` blocks earlier changes left (`git log --grep "Redundant older tests:"`). There's no target number unless the user gives one, and even then a test that stays by the rules stays.
2. **List.** Show the user, in plain language and grouped by module, each candidate: the test, the pattern it fits, and the test that keeps its rule (or why it keeps nothing). Protected and "maybe protected" ones go in a separate group, named one by one. Also list the moves (misplaced tests) and, apart, the rules of SPEC.md no test checks. Wait for the user's OK; remove only what they approved.
3. **Remove** in batches, one module at a time, together with the production code only those tests kept alive (an unused export, wrapper or reset hook). After each batch, sabotage each rule that lost a test as that file says (it starts with a checkpoint), and run the module's tests.
4. **Record** each rule with no test as a Debt entry in BACKLOG.md, with the `document` skill. Don't write tests here: a prune only removes.
5. **Review:** give the `reviewer` the approved list along with the chore's description.
6. **Verification message:** tests before and after (count), test lines and production lines removed, counted apart, each sabotage, coverage per file before and after if the project measures it, the tests kept that looked useless and why, and what kept producing the useless tests; suggest the user a line for the project's CLAUDE.md, or, if the cycle itself produced them, a report to the plugin.

