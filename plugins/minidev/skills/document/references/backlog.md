# BACKLOG.md

`BACKLOG.md`, at the project root, is the single place for feature ideas, for the feature being built, and for bugs and technical debt left for later. Each entry starts from **why** the user wants it, because a feature that loses its motivation gets built wrong or never gets prioritized. Implemented features leave the file.

Read `BACKLOG.md` before changing it.

## File structure

```markdown
# Backlog

<legend>

## <Area>

### <Feature name>
<entry fields>

## Discarded

### <Feature name>
- **Description:** …
- **Why discarded:** … (date)
```

- Areas (`##`) group features by part of the product (e.g. "Editor", "Sync"). Put each feature in the area it belongs to; if none fits, propose a new area and confirm before creating it.
- Remove an area as soon as it is left empty.
- "Discarded" is always the last section, so discarded ideas aren't proposed again. Omit it while empty.

### Legend

Translated to the file's language:

```markdown
Feature ideas, the feature being built, and bugs and debt left for later, managed with the `document` skill. Implemented features leave this file: what changed goes to CHANGELOG.md and the rules to SPEC.md.

Status: **Idea** → **In progress** (one at a time) → done (leaves the file in the commit that implements it). Discarded ideas go to the last section.
```

## Statuses

| Status | Meaning | Extra fields |
|---|---|---|
| **Idea** | Recorded, not decided. | — |
| **In progress** | Being built. Only one at a time. | **To check by hand** |
| done | Implemented and verified: the entry leaves the file. | — |

Only the user moves a feature to Discarded. A new entry is always an Idea. Only features go In progress: a Bug or Debt entry stays an Idea until `fix` or `chore` does it, and then leaves the file.

## Entry format

```markdown
### <Feature name>
- **Status:** Idea
- **Type:** <Bug | Debt> (only when it isn't a feature)
- **Motivation:** <the problem today, from the user's side>
  - When <situation>, I want <outcome>. (only when there's more than one distinct context)
- **Description:** <the solution, from the user's point of view>
- **Decisions:**
  - <a rule or choice already made>
- **Constraints:**
  - <a limit the feature must respect, checkable: performance, security, accessibility, compatibility, privacy, volume>
- **Out of scope:** <what was explicitly left out>
- **Open questions:**
  - <what is still undecided>
- **Notes (<what they are>, <date>):**
  - <findings from research, trials or options discussed>
```

Omit any field with nothing to say; Status, Motivation and Description are always present.

**Type** marks an entry that isn't a feature:
- **Bug:** broken behavior left for later, fixed with the `fix` skill. Its Description is what's wrong and the steps to reproduce it.
- **Debt:** a change that keeps the behavior (refactoring, an upgrade, a migration, tooling), done with the `chore` skill. Its Description is what's owed and where.

For both, the Motivation says what it costs to leave it as it is.

How to fill it:
- **Motivation** comes first because it's what everything else is judged against. Don't copy the user literally: condense what they said into a short statement of the problem, quoting only key phrases or expressions when they help understanding. Add "When…, I want…" sub-items only when the feature serves distinct situations that would shape the solution differently; otherwise they just repeat the motivation. If the motivation was never stated, write "not recorded" rather than inventing one.
- **Description** describes the behavior the user will see, not the implementation.
- **Decisions** hold choices already made (rules, behaviors, technical options chosen). When the feature changes existing behavior, name the SPEC.md rule that changes and how. No file paths or code snippets: they go stale fast.
- **Constraints** hold what the feature must respect besides its behavior: speed, security, accessibility, compatibility, privacy, how much data it handles. Write each so it can be checked ("searching 10,000 notes answers in under 200 ms", "works without a network", "usable with the keyboard alone"), not as a wish ("fast", "secure"); a limit nobody can name yet is an open question. Constraints of the whole product live in SPEC.md, not repeated in each entry.
- **Open questions** keep undecided points visible instead of silently assuming an answer.
- **Notes** keep context that isn't a decision yet: research findings, a trial's results, options weighed. Date them and say what they are (e.g. "options discussed on 2026-10-12, nothing decided").
- Write only what the user said or decided. Don't invent requirements; an assumption is an open question.

## Operations

### Create the file
When the project has no `BACKLOG.md`, create it with the title and the legend. If an older backlog file exists (e.g. `FEATURES.md`, `TODO.md`, `IDEAS.md`), propose migrating it: rename it with `git mv` to keep its history, and convert its entries to this format.

### Capture from the conversation
Turn what was discussed into an entry. Don't interview the user; synthesize what you already know from the conversation and the codebase. The only exception is the motivation: if it never came up, ask at most 2 or 3 short questions about it (what problem does it solve? in what situation is it missing?). Anything else unresolved becomes an open question.

Show the draft (and the area it will go in) and wait for the user's OK before writing, since a synthesis involves interpretation. When the capture follows an interview whose final summary the user approved, present that summary as the entry and its approval as the OK: don't ask twice.

### Record a bug or debt for later
When the user wants to leave a bug or a chore for later ("note this bug, I'll fix it later", "we owe a refactor of X"), record it right away with its Type, in the area of the part it affects. No interview: what's unknown is an open question. When `fix` or `chore` does it, the entry leaves the file in that work's commit.

### Add an idea
When the user states an idea:
- **Clear:** record it right away and tell them what was written.
- **Vague:** ask 2 or 3 short questions first (what problem does it solve? how do they picture it working?).
- **Leaves behavior open** (several connected decisions that would change what gets built): load the `grilling` skill and interview the user with it. Write its final summary in this entry format, so approving the summary approves the text that will be recorded (see Capture).

"Just note it" (or the same in the user's language) always skips the questions and the interview: record what was said, with anything undecided as Open questions.

Only record it; don't implement it.

### Check for duplicates
Before adding or capturing, look for an identical or similar entry (including in Discarded). If one exists, show it and ask whether to merge into it or create a separate one. When merging, update the fields and keep the old notes that still hold.

### Present
Summarize by area: each feature's name and status. Apply the filter the user asks for (area, status). Give a feature's details only when asked.

### Start a feature
1. If another feature is In progress, say so and ask what to do: finish it, pause it back to Idea, or stop.
2. Create the entry if it doesn't exist (a direct request).
3. Set it **In progress** and add **To check by hand**: the rules that only show in the real app, for the user to try once it's built. The automated checks live in the tests, not here.

### Finish a feature
Verifying the feature is the job of whoever built it (e.g. the `build` skill); this step only records it, in the same commit as the code.
1. Update SPEC.md with the rules of what was built (`references/spec.md`).
2. Add the change to CHANGELOG.md (`references/changelog.md`).
3. Remove the entry and, if its area is left empty, the area.
4. Give the commit message the verification results: what passed, and the "To check by hand" list as a block starting with a line that says exactly `To check by hand:`.

If the user later finds a problem in use, it's handled as a bug fix, not by reopening the entry.

### Change status
Update the field when the user asks, e.g. pause a feature (In progress → Idea). Write it directly and tell them.

### Discard
Move the entry to "Discarded", keeping only its **Description** and a **Why discarded** line with the reason and the date. If its area is left empty, remove the area.

### Clean up
Look for:
- duplicates and similar entries that could be merged
- entries already implemented in the code (check the code, SPEC.md and CHANGELOG.md)
- entries the user has dropped

Show what you intend to change and wait for the OK. Implemented ones leave the file (after checking they're in CHANGELOG.md); dropped ones go to Discarded.

### Reorganize
When areas stopped making sense (an area too big, features in the wrong place), propose the new structure and apply it only after it's approved.
