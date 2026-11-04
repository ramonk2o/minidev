---
name: fix
description: In projects set up for the minidev cycle (a CLAUDE.md that says it uses the `minidev` cycle), fix a bug on its own branch, test-first when it can be reproduced in a test, record it in the changelog and merge it once confirmed. Use it whenever the user reports something broken or wrong in existing behavior, e.g. "X has a bug", "saving fails when…", "isso quebrou", a flaky test or a CI run that fails on correct code, something that got slower than before or than a limit SPEC.md sets, "/minidev:fix X". Not for new behavior: that's a feature (document, then build). Not for typos, refactoring or upgrades that keep the behavior (chore).
---

# Fix

Fixes a bug: existing behavior that doesn't do what SPEC.md, the tests or the user expect. A bug has no independent tester, and a backlog entry only when it was left for later (type Bug); its weight is in the test that reproduces it, so it can't come back unnoticed.

Talk to the user in the language of the conversation. Project instructions (CLAUDE.md, AGENTS.md…) define the test and build commands and what only shows in the real app; when they conflict with this skill, they win.

## 1. Check it's a bug

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) says it uses the `minidev` cycle (the line `/minidev:setup` writes: "This project uses the `minidev` cycle"). A CLAUDE.md that only mentions a build command or a fix isn't that. If it doesn't, offer `/minidev:setup` or simply fix the bug without this skill.

If BACKLOG.md has an entry for it (type Bug), use it as the bug's description.

If the bug came with a change already on the main branch (a feature, fix or chore just merged), offer the choice in the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder), When a merged change breaks: fix forward here, or revert that change.

If fixing it means deciding how the product should behave (two reasonable answers, or a rule SPEC.md doesn't cover), it's a feature: say so and record it with the `document` skill instead.

## 2. Fix

1. Read the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder) and create the `fix/<short-name>` branch as it says (Start the branch), or resume it if this work was started before (Resume).
2. Run the test suite and the build first and note what already fails, so the reproducing test's failure is told apart from older ones (and those are shown to the user, not fixed here unless they're this bug).
3. If the bug can be reproduced in a test, write the test and show that it fails for the reason reported. Then fix the code until it, the whole suite and the build pass.
4. If it only shows in the real app, fix it and keep the steps to reproduce it for the commit message. If it can't be reproduced at all, in a test or in the app, stop: show the user what was tried and offer to record it as a Bug entry with those notes, instead of changing code on a guess.
5. If you added or changed tests beyond the one that reproduces the bug, check them as in the `build` skill's `references/test-value.md` (`../build/references/test-value.md` from this skill's folder), Check the change's tests. The reproducing test is protected.
6. With the `document` skill, record the fix in CHANGELOG.md under Fixed, and in SPEC.md if the fix corrects a rule written wrong there or makes explicit a rule it left implicit (deciding a new rule makes it a feature, as in section 1). If BACKLOG.md had a Bug entry for it, remove it. This comes before the review, so the reviewer reads the documents with the code.
7. If the fix changes code, have it reviewed by the `reviewer` agent as in the `build` skill's `references/review.md` (`../build/references/review.md` from this skill's folder), passing the bug as reported (or its Bug entry), and act on its report as that file says for `fix`.

## 3. Finish

1. If the review's fixes changed what the documents say, update them with the `document` skill.
2. Stage the work and make the branch's verification commit, in the format of `git-flow.md` (The verification commit): its message is what the main branch gets, in one squashed commit with code, tests and documents. A fix has no Tester or `Critical tests:` section; the reproducing test goes in `Regression tests:`, so a later prune knows it's protected; if the fix needs checking in the real app, `To check by hand:` holds the steps to reproduce the bug.
3. Show the user what to check, if anything, and wait for their confirmation.
4. Merge, test and push as in `git-flow.md` (Merge and push), in the project's integration mode.
