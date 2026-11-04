---
name: fix
description: In projects set up for the minidev cycle (a CLAUDE.md that names it), fix a bug on its own branch, test-first when it can be reproduced in a test, record it in the changelog and merge it once confirmed. Use it whenever the user reports something broken or wrong in existing behavior, e.g. "X has a bug", "saving fails when…", "isso quebrou", "/minidev:fix X". Not for new behavior: that's a feature (document, then build). Not for typos, refactoring or upgrades that keep the behavior (chore).
---

# Fix

Fixes a bug: existing behavior that doesn't do what SPEC.md, the tests or the user expect. A bug has no independent tester, and a backlog entry only when it was left for later (type Bug); its weight is in the test that reproduces it, so it can't come back unnoticed.

Talk to the user in the language of the conversation. Project instructions (CLAUDE.md, AGENTS.md…) define the test and build commands and what only shows in the real app; when they conflict with this skill, they win.

## 1. Check it's a bug

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) names the `minidev` cycle or the `fix` skill. If it doesn't, offer `/minidev:setup` or simply fix the bug without this skill.

If BACKLOG.md has an entry for it (type Bug), use it as the bug's description.

If fixing it means deciding how the product should behave (two reasonable answers, or a rule SPEC.md doesn't cover), it's a feature: say so and record it with the `document` skill instead.

## 2. Fix

1. Read the `build` skill's `references/git-flow.md` (`../build/references/git-flow.md` from this skill's folder) and create the `fix/<short-name>` branch as it says (Start the branch).
2. If the bug can be reproduced in a test, write the test and show that it fails for the reason reported. Then fix the code until it, the whole suite and the build pass.
3. If it only shows in the real app, fix it and keep the steps to reproduce it for the commit message.
4. If the fix changes code, launch the `reviewer` agent (agent type `minidev:reviewer`) as in the `build` skill's Refactor and review section, Review (`../build/SKILL.md` from this skill's folder; read only that part), passing the bug as reported (or its Bug entry) instead of a backlog entry. A fix has no tester, so a blocking finding that changes behavior is fixed test first, with no tester round after it.

## 3. Finish

1. With the `document` skill, record the fix in CHANGELOG.md under Fixed, and in SPEC.md if a rule changed. If BACKLOG.md had a Bug entry for it, remove it.
2. Stage the work and make the branch's verification commit, as in `git-flow.md`: its message is what the main branch gets, in one squashed commit with code, tests and documents. It records the suite and build results and the review, if there was one. If the fix needs checking in the real app, end the message with a block starting with a line that says exactly `To check by hand:`, with the steps to reproduce the bug, one per line.
3. Show the user what to check, if anything, and wait for their confirmation.
4. Merge, test and push as in `git-flow.md` (Merge and push), in the project's integration mode.
