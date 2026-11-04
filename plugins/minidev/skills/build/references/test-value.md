# Test value

What makes a test worth keeping, and how to check it. Used by the `build`, `fix` and `chore` skills to check the tests a change adds (Check the change's tests) and by `chore` to prune a whole suite; the `tester` and `reviewer` agents judge tests by the same rules.

A test earns its place by being the one that fails when a rule breaks. A test that would still pass with the code broken, or that only repeats another test, costs maintenance and suite time and proves nothing.

## A test stays when

- it's the only test that would fail if a rule broke: a rule of SPEC.md or of the change's entry, including its Constraints, defaults, errors and edge cases;
- it guards a regression a bug fix found;
- it checks an outside contract the product promises: a public API, a file or storage format, a migration, security, a supported platform;
- the order of calls is observable behavior, or it reads a file, key or text users depend on, so it fails when that changes and survives a rename.

Slow, static or close to the implementation isn't a reason to remove it: a test that looks like the code may still be the only proof of a rule. Show which test keeps the rule before removing one.

## Patterns of useless tests

- **Passes with the code broken:** no assertion, or only "does not throw" on a path that can't throw; a mock that implements the behavior under test; an expected value produced by the code under test; a fixture that supplies the result the code should produce; a negative test that passes for an unrelated reason (a different guard rejects it).
- **Repeats another test:** the same rule through the same entry point, with inputs that don't change the outcome; the same shared helper replayed once per caller; a check of an internal call (`toHaveBeenCalledWith` on a private function) already covered at the public boundary.
- **Checks the wrong thing:** an internal detail, so it fails on a rename and survives a real change of behavior; a copy of data the test also defines (a list, a snapshot of its own fixture); flags or config restated instead of exercising what they promise.
- **Keeps dead code alive:** the only caller of an export, wrapper or reset hook that production doesn't use.
- **Misplaced:** lives in one module's tests but only exercises another's. Move it to its owner's tests; moving isn't removing.
- **Promises more than it checks:** judge a test by its assertions, not by its name.

A skipped test (`skip`, `xit`, `@pytest.mark.skip`, `t.Skip()`) isn't a candidate on sight: enable it temporarily and run it. If it passes, leave it enabled and judge it like any other. If it fails, restore the skip and show the user: it may be a bug, and it isn't removed. A skip with a real platform or environment reason stays.

## Protected tests

Removing or merging one of these always goes to the user first, named one by one, with the test that keeps its rule:

- **Critical tests:** the ones the user approved in a feature's critical test list, listed in its verification commit under `Critical tests:` (`git log --grep "Critical tests:"`).
- **Regression tests:** the ones that reproduce a fixed bug, listed under `Regression tests:` (`git log --grep "Regression tests:"`).
- **Tester tests:** during `build`, a test the `tester` wrote; the author doesn't filter the tester's work.

A protected test that was renamed or moved is found through the history of its file (`git log --follow`). In projects whose commits have no such blocks (built before them), count as "maybe protected" every test added by a commit that also added a line under Fixed in CHANGELOG.md, and let the user decide.

## Sabotage

The proof that removing tests didn't remove a check. First commit a `wip:` checkpoint, so there's a clean point to return to. Then, for each rule that loses a test: break that rule in the code on purpose (invert a condition, return a wrong value, skip the step), run the test that stays and show it fails, then undo the sabotage and check that `git status --short` is clean again. One sabotage per rule, not per removed test. If the test that stays still passes, it isn't keeping the rule: the removal is wrong, keep the test. Record each sabotage (rule, what was broken, the test that failed) in the verification message.

Coverage, when the project already measures it, is an extra signal: compare it per file, before and after. Line coverage alone doesn't prove a rule is checked, since another test may run those lines without asserting anything.

## Check the change's tests

Run with the suite green, before the review, on the tests the change added or edited since the branch's base (`git diff $(git merge-base HEAD <main branch>)`), not on the rest of the suite:

1. Tie each new test to a rule of the change's entry or bug, a rule of SPEC.md, or a risk the entry names. A test tied to nothing is a candidate.
2. Compare the new tests with each other and with the existing tests of the same modules, looking for the patterns above.
3. Act on each candidate:
   - **Extra tests this change added** (not critical, not the regression test, not the tester's): merge or remove them yourself.
   - **Protected tests:** ask the user, as above.
   - **Older tests**, including ones this change edited, and ones the new tests make redundant: don't remove them in this change; list them for a later prune.
   - **Misplaced tests:** move them to their owner's tests.
4. Sabotage each rule that lost a test, and run the suite and the build again.

The verification message records the extras merged or removed, each sabotage and, when there are any, the older tests as a block starting with a line that says exactly `Redundant older tests:`, one per line as `<file> — <test name> — <the test that covers it>`, so a prune finds them with `git log --grep "Redundant older tests:"`.
