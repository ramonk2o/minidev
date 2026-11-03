---
name: build
description: In projects set up for the minidev cycle (a CLAUDE.md that names it), implement a feature from the project's backlog test-first, then have it checked by an independent tester agent before it is committed. Use it whenever the user wants to implement, build, develop or start coding a feature, from BACKLOG.md or as a direct request, e.g. "let's build Tables", "implement the sync idea", "/minidev:build X", "start working on X", or when project instructions say to use the build skill.
---

# Build

Builds one feature in a fixed order: critical tests first, then the code, then an independent check by the `tester` agent. The order exists for two reasons. Tests written before the code pin down what the feature must do, instead of describing whatever the code happened to do. A tester with a clean context, which sees the code but not the reasoning behind it, catches the blind spots of whoever wrote both.

Statuses, backlog entries and every change to BACKLOG.md, SPEC.md and CHANGELOG.md go through the `document` skill. Project instructions (CLAUDE.md, AGENTS.md…) define the project's specifics: test and build commands, what to check by hand, steps required before writing code, commit rules. Follow them at the matching steps below; when they conflict with this skill, they win.

Talk to the user in the language of the conversation.

## 1. Start

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) names the `minidev` cycle or the `build` skill. If not, don't create a backlog, branches or documents in it: offer `/minidev:setup` and stop, or simply implement the request without this skill if the user prefers.

1. Find the feature's entry in `BACKLOG.md`. For a direct request with no entry, create one with the `document` skill.
2. If another feature is In progress, the `document` skill asks what to do; resolve it before going on.
3. Check that the entry has enough rules to derive tests from: what the user sees, plus the edge cases that matter. Guessing missing rules would make the tests, and then the code, encode assumptions nobody approved, so settle them first, with the smallest step that does it:
   - **Enough rules** (usually, when the idea was interviewed): go on. Don't re-ask what the entry already decides.
   - **One to three specific points open:** ask them directly, each with your recommended answer, and record the answers in the entry's Decisions.
   - **Key behavior undecided across several connected decisions** (e.g. the entry is still a bare idea): stop and offer a `grilling` interview, recording the answers in the entry.
4. Create the feature's branch `feature/<short-name>` as in `references/git-flow.md` (Start the branch). Read that file now: the staging, checkpoint and merge steps below follow it too. Commit a `wip:` checkpoint on the branch whenever a step below is done, and before stopping.
5. Do whatever the project instructions require before writing code.

## 2. Critical test list

A critical test checks a rule the user can see and that, if broken, means the feature fails. Take the rules from the entry's Description and Decisions, including the edge cases that were decided. Each one tests behavior from the outside, through the public function or module, never internal details. Internal details change during implementation; the user-visible rules don't.

Show the list to the user in plain language, without code, in two groups:
- **Automated tests:** the rules the test suite can check.
- **To check by hand:** the rules that only show in the real app (focus, dragging, browser shortcuts, visuals). They're checked by the user in the real app, not with fake tests.

Wait for the user's OK. This is their chance to check that the right rules are being tested without reading test code.

With the `document` skill, set the entry **In progress** with the approved **To check by hand** list. This status change isn't committed on its own: it goes in the branch's first checkpoint.

## 3. Tests first

Write the automated tests, following the project's test conventions (location, naming, helpers, fakes). If the module they call doesn't exist yet, first create its public interface as a stub: the functions or components the tests use, with their signatures, each failing with a "not implemented" error. Run the tests and show that they **fail**, and fail for the right reason: the feature is missing, not a typo or a broken import. A test that passes before the code exists isn't testing the feature.

## 4. Implement

Write the code until the critical tests, the whole test suite and the build pass. Don't change a critical test to make it pass. If a test turns out to be wrong, say why and ask before changing it, since the user approved that list.

## 5. Independent tester

If the approved list has no automated tests (the feature only shows in the real app), skip this step: the tester can't check anything there. Say so, and record "no tester: no automated tests" in the commit message.

Otherwise, launch the `tester` agent (agent type `minidev:tester`). Give it only:
- the feature's backlog entry, copied in full
- the base commit: where the feature's branch left the main branch (`git merge-base HEAD <main branch>`). First stage the work as in `references/git-flow.md` (Stage the work): `git diff` doesn't show files git doesn't track yet, and the new modules and tests are exactly what the tester needs to see. The tester reads the change itself with `git diff <base>`, instead of a copy pasted in its prompt
- the project's test and build commands

Don't pass your explanations, the conversation or your own view of what might be weak. Its value is not knowing what you meant.

When it returns, check that it only added new test files: the work was staged before it ran, so `git diff --name-only` (changes to files git already has) must be empty, and every untracked file in `git status --short` must have `tester` in its name. Undo any other change with `git restore <file>` and tell the user what it had touched.

Then act on its report:
- **Failures (bugs):** fix the code, keep the tester's test that caught it, and launch a **new** tester with the same inputs (stage the fixes first). A new one, so it doesn't carry the previous round's context.
- **Extra tests that pass** and check a rule from the entry: keep them.
- **Assumptions** (a test of a rule that was never decided): remove that test now, before anything is staged again (the report names its file and test). Ask the user, record the answer in the entry's Decisions, and test it if the answer makes it a rule.
- **Uncovered rules:** add the missing tests.

Repeat until a report comes back with no failures. After 3 rounds with failures still open, stop and show the user what's left instead of looping.

## 6. Finish

1. **Optional cleanup:** when the diff is large (many files, or new modules), run the `simplify` skill to make the code more direct and readable, then run the test suite and build again. Skip it for small changes.
2. With the `document` skill, finish the feature: it updates SPEC.md with what was built, adds the change to CHANGELOG.md and removes the entry from BACKLOG.md.
3. Stage the work and make the branch's verification commit, as in `references/git-flow.md`. It's the message the main branch gets, in the one squashed commit that brings it code, tests, `BACKLOG.md`, `SPEC.md` and `CHANGELOG.md`, unless project instructions say otherwise. It records the verification:
   - the test suite and build results
   - the tester's last report, summarized: rounds run, what it found and how it was resolved, extra tests kept (or why there was no tester)
   - what is left for the user to check by hand, as a block starting with a line that says exactly `To check by hand:`, one item per line, so it can be found later with `git log --grep`
4. Show the user the "To check by hand" list and wait for them to check it. If something fails, fix it on the same branch (test first when it can be reproduced in one) and commit it as a checkpoint.
5. **Merge and push** the feature's branch as in `references/git-flow.md` (Merge and push), in the project's integration mode: local merge, or a pull request. Either way, the combined code is tested before it reaches the main branch on the remote.

A feature with automated tests is only finished through step 5: without a tester report it hasn't been independently checked, and the commit message would claim more than was done.
