---
name: build
description: In projects set up for the minidev cycle (a CLAUDE.md that says it uses the `minidev` cycle), implement a feature from the project's backlog test-first, then have it checked by an independent tester agent and reviewed by an independent reviewer agent before it is committed. Use it whenever the user wants to implement, build, develop or start coding a feature, from BACKLOG.md or as a direct request, e.g. "let's build Tables", "implement the sync idea", "/minidev:build X", "start working on X", "continue X where we left off", or when project instructions say to use the build skill. Not for broken behavior (fix) or changes that keep the behavior, like refactoring or upgrades (chore).
---

# Build

Builds one feature in a fixed order: critical tests first, then the code, then an independent check by the `tester` agent and a review by the `reviewer` agent. The order exists for two reasons. Tests written before the code pin down what the feature must do, instead of describing whatever the code happened to do. A tester with a clean context, which sees the code but not the reasoning behind it, catches the blind spots of whoever wrote both.

Statuses, backlog entries and every change to BACKLOG.md, SPEC.md and CHANGELOG.md go through the `document` skill. Project instructions (CLAUDE.md, AGENTS.md…) define the project's specifics: test and build commands, what to check by hand, steps required before writing code, commit rules. Follow them at the matching steps below; when they conflict with this skill, they win.

Talk to the user in the language of the conversation.

## 1. Start

First check that the project uses the cycle: its CLAUDE.md (or AGENTS.md) says it uses the `minidev` cycle (the line `/minidev:setup` writes: "This project uses the `minidev` cycle"). A CLAUDE.md that only mentions a build command or a fix isn't that. If not, don't create a backlog, branches or documents in it: offer `/minidev:setup` and stop, or simply implement the request without this skill if the user prefers.

Read `references/git-flow.md` now: the resume, branch, staging, checkpoint and merge steps below follow it.

1. Find the feature's entry in `BACKLOG.md`. If it's already **In progress**, or a `feature/` branch matches it, the work was started: resume it as in `references/git-flow.md` (Resume) instead of starting again. For a direct request with no entry, create one with the `document` skill.
2. If another feature is In progress, the `document` skill asks what to do; resolve it before going on.
3. Check that the entry has enough rules to derive tests from: what the user sees, plus the edge cases that matter, plus the Constraints the feature must respect: its own, and those in SPEC.md's Constraints (whole-product limits, like "works offline") that apply to what it touches. When the feature has an obvious risk the entry doesn't address (data that can grow without limit, user input reaching a query or the page, a public surface), count it as an open point, with a recommended limit. Guessing missing rules would make the tests, and then the code, encode assumptions nobody approved, so settle them first, with the smallest step that does it:
   - **Enough rules** (usually, when the idea was interviewed): go on. Don't re-ask what the entry already decides.
   - **One to three specific points open:** ask them directly, each with your recommended answer, and record the answers in the entry's Decisions.
   - **Key behavior undecided across several connected decisions** (e.g. the entry is still a bare idea): stop and offer a `minidev:grilling` interview, recording the answers in the entry.
4. With the `document` skill, set the entry **In progress** on the main branch. It's committed there, so the main branch's BACKLOG.md shows what is being built, from any branch or session; it reaches the remote with the next merge into the main branch.
5. If the modules the feature will change have no tests of their current behavior, say so and offer to add them first as a chore (`chore`, Missing tests): without them, the refactor step and the rest of the suite can't show that what existed still works. The user may go on without them; note it in the verification message.
6. Create the feature's branch `feature/<short-name>` as in `references/git-flow.md` (Start the branch). Commit a `wip:` checkpoint on the branch whenever a step below is done, and before stopping.
7. Do whatever the project instructions require before writing code.

## 2. Critical test list

A critical test checks a rule the user can see and that, if broken, means the feature fails. Take the rules from the entry's Description and Decisions, including the edge cases that were decided, its Constraints, and the SPEC.md Constraints that apply to it. A measurable constraint becomes an automated test (e.g. a search over 10,000 generated notes, with a time limit loose enough not to fail on a slow machine) or a check the project already runs (an accessibility or security linter); one that only shows in the real app goes to **To check by hand**. Each one tests behavior from the outside, through the public function or module, never internal details. Internal details change during implementation; the user-visible rules don't.

Show the list to the user in plain language, without code, in two groups:
- **Automated tests:** the rules the test suite can check.
- **To check by hand:** the rules that only show in the real app (focus, dragging, browser shortcuts, visuals). They're checked by the user in the real app, not with fake tests.

Wait for the user's OK. This is their chance to check that the right rules are being tested without reading test code.

With the `document` skill, add the approved **To check by hand** list to the entry. This change isn't committed on its own: it goes in the branch's next checkpoint.

## 3. Tests first

Write the automated tests, following the project's test conventions (location, naming, helpers, fakes). If the module they call doesn't exist yet, first create its public interface as a stub: the functions or components the tests use, with their signatures, each failing with a "not implemented" error. Run the tests and show that they **fail**, and fail for the right reason: the feature is missing, not a typo or a broken import. A test that passes before the code exists isn't testing the feature.

## 4. Implement

Write the code until the critical tests, the whole test suite and the build pass. Don't change a critical test to make it pass. If a test turns out to be wrong, say why and ask before changing it, since the user approved that list.

## 5. Independent tester

If the approved list has no automated tests (the feature only shows in the real app), skip this step: the tester can't check anything there. Say so, and record "no tester: no automated tests" in the commit message.

Otherwise, stage the work as in `references/git-flow.md` (Stage the work): `git diff` doesn't show files git doesn't track yet, and the new modules and tests are exactly what the tester needs to see. Then launch the `tester` agent (agent type `minidev:tester`) with this prompt, filled in and nothing added:

```
Feature entry (BACKLOG.md):
<the entry, copied in full>

Product constraints (SPEC.md, Constraints):
<the section, copied in full, or "none">

Base commit: <git merge-base HEAD <main branch>>
Test command: <command>
Build command: <command, or "none">
```

Don't pass your explanations, the conversation or your own view of what might be weak. Its value is not knowing what you meant.

Before launching it and when it returns, check the repository as in `references/git-flow.md` (Check after an agent): it may only have added new test files with `tester` in their name.

Then act on its report:
- **Failures (bugs):** fix the code, keep the tester's test that caught it, and launch a **new** tester with the same inputs (stage the fixes first). A new one, so it doesn't carry the previous round's context.
- **Extra tests that pass** and check a rule from the entry: keep them.
- **Assumptions** (a test of a rule that was never decided): remove that test now, before anything is staged again (the report names its file and test). Ask the user, record the answer in the entry's Decisions, and test it if the answer makes it a rule.
- **Uncovered rules:** add the missing tests.
- **A tester's test you believe is wrong** (it contradicts the entry, or checks something the entry doesn't say): don't change the code to fit it, and don't remove it. Tell the user which test and why, and let them decide, as with a critical test.

The tester's report is the check of your work, so you don't get to filter it: removing one of its tests, or calling a failure an assumption, always goes to the user first, with the test's name and a line on why. Only the tester's own Assumptions section can be acted on as above.

Repeat until a report comes back with no failures. After 3 rounds with failures still open, stop and show the user what's left instead of looping.

## 6. Refactor, check the tests, documents and review

Green tests say the feature works, not that the code, its tests and its documents are ready to live with. Four steps take care of that, in this order.

**Refactor.** With the whole suite green, clean up the code you wrote: remove stubs that are left, dead code and debug output; give things names that say what they do; remove duplication, using what the codebase already has. Don't change behavior or the tests that check it. When the diff is large (many files, or new modules), run the `simplify` skill for this, if it's available. Run the test suite and the build again.

**Check the tests.** Read `references/test-value.md`. First move the tester's kept tests out of their `tester` files into the tests of the module they exercise, following the project's conventions (the `tester` name only served the check after each round). Note which tests came from the tester; they stay protected, so merging or removing one still goes to the user. Then check the tests this feature added as that file says (Check the change's tests). If a later tester round adds tests (after a blocking review fix), move and check those too.

**Documents.** With the `document` skill, finish the feature: it updates SPEC.md with what was built, adds the change to CHANGELOG.md and removes the entry from BACKLOG.md. This comes before the review, so the rules written in SPEC.md from what was built are read against the code by someone who didn't write them.

**Review.** Even when there was no tester, have the change reviewed by the `reviewer` agent as in `references/review.md`, giving it the feature's backlog entry (as it was before the documents step removed it), and act on its report as that file says.

## 7. Finish

1. If anything after the review changed behavior, update SPEC.md and CHANGELOG.md to match, with the `document` skill.
2. Stage the work and make the branch's verification commit, in the format of `references/git-flow.md` (The verification commit). It's the message the main branch gets, in the one squashed commit that brings it code, tests, `BACKLOG.md`, `SPEC.md` and `CHANGELOG.md`, unless project instructions say otherwise. A feature uses every section but `Regression tests:`: the tester's last report goes in verbatim, so the record is its words and not your summary, and each tester test kept is listed as moved, since the report names the old files.
3. Show the user the "To check by hand" list and wait for them to check it. If something fails, fix it on the same branch (test first when it can be reproduced in one), update SPEC.md if the fix changes a rule it states, and commit it as a checkpoint.
4. **Merge and push** the feature's branch as in `references/git-flow.md` (Merge and push), in the project's integration mode: local merge, or a pull request. Either way, the combined code is tested on the branch before it reaches the main branch. If it breaks after it's on the remote, follow `references/git-flow.md` (When a merged change breaks).

A feature is only finished through step 4, after the review (and, with automated tests, the tester): without their reports it hasn't been independently checked, and the commit message would claim more than was done.
