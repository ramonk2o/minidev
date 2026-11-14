# BACKLOG.md

`BACKLOG.md`, at the project root, is the single place for feature ideas, for the features being built, and for bugs and technical debt left for later. Each entry starts from **why** the user wants it, because a feature that loses its motivation gets built wrong or never gets prioritized. Implemented features leave the file.

Read `BACKLOG.md` before changing it.

When the project's CLAUDE.md says `Backlog: GitHub issues`, the entries live in the repository's issues: everything here holds except where they're stored and how each operation writes them, which `issues.md` says.

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

- Areas (`##`) group entries by the part of the product they change (e.g. "Editor", "Sync"), the same areas SPEC.md's Behavior uses when it has them. Put each entry in the area it changes most; if none fits, propose a new area and confirm before creating it.
- An area never says when. A phase, a priority or a "later" pile tells nobody what an entry touches: when an entry is planned for goes in its Version.
- Inside an area, entries are in the order to build them; a new one goes last unless the user says where.
- Remove an area as soon as it is left empty.
- "Discarded" is always the last section, so discarded ideas aren't proposed again. Omit it while empty.

### Legend

Translated to the file's language:

```markdown
Feature ideas, the features being built, and bugs and debt left for later, managed with the `document` skill. Implemented features leave this file: what changed goes to CHANGELOG.md and the rules to SPEC.md.

Status: **Idea** → **In progress** (each on its own branch) → done (leaves the file in the commit that implements it). Discarded ideas go to the last section.
```

## Statuses

| Status | Meaning | Extra fields |
|---|---|---|
| **Idea** | Recorded, not decided. | — |
| **In progress** | Being built, on the branch it names: `In progress (feature/<name>)`. Several can be in progress at once, each on its own branch. Set on the main branch when the work starts. | **To check by hand** (once the critical test list is approved) |
| done | Implemented and verified: the entry leaves the file. | — |

Only the user moves a feature to Discarded. A new entry is always an Idea. Only features go In progress: a Bug or Debt entry stays an Idea until `fix` or `chore` does it, and then leaves the file.

## Entry format

```markdown
### <Feature name>
- **Status:** Idea
- **Type:** <Bug | Debt> (only when it isn't a feature)
- **Version:** <the version it's planned for> (only when it's planned)
- **Needs:** <entry name>, <entry name> (only when it can't be built before them)
- **Motivation:** <the problem today, from the user's side>
  - When <situation>, I want <outcome>. (only when there's more than one distinct context)
- **Description:** <the solution, from the user's point of view>
- **Decisions:**
  - <a rule or choice already made>
  - <a tester's assumption adopted by `build`> (assumed: the tester's recommendation)
- **Constraints:**
  - <a limit the feature must respect, checkable: performance, security, accessibility, compatibility, privacy, volume>
- **Out of scope:** <what was explicitly left out>
- **Open questions:**
  - <what is still undecided>
- **Notes (<what they are>, <date>):**
  - <findings from research, trials or options discussed>
- **To check by hand:** (In progress only)
  - <a rule that only shows in the real app>
```

Omit any field with nothing to say; Status, Motivation and Description are always present.

**Type** marks an entry that isn't a feature:
- **Bug:** broken behavior left for later, fixed with the `fix` skill. Its Description is what's wrong and the steps to reproduce it.
- **Debt:** a change that keeps the behavior (refactoring, an upgrade, a migration, tooling), done with the `chore` skill. Its Description is what's owed and where.

For both, the Motivation says what it costs to leave it as it is.

**Version** names the version the entry is planned for: the number its release would take (`0.1.0` for a new project's first version), or a short name when the project doesn't number its versions. Only the user plans an entry for a version; an entry with none isn't planned yet, which is how most ideas stay. The **current version** is the lowest one that still has open entries (with names, the one planned first: the first in the file, or the milestone with the lowest number).

**Needs** names the entries that must be built before this one (Relations between entries).

How to fill it:
- **Motivation** comes first because it's what everything else is judged against. Don't copy the user literally: condense what they said into a short statement of the problem, quoting only key phrases or expressions when they help understanding. Add "When…, I want…" sub-items only when the feature serves distinct situations that would shape the solution differently; otherwise they just repeat the motivation. If the motivation was never stated, write "not recorded" rather than inventing one.
- **Description** describes the behavior the user will see, not the implementation.
- **Decisions** hold choices already made (rules, behaviors, technical options chosen). When the feature changes existing behavior, name the SPEC.md rule that changes and how. No file paths or code snippets: they go stale fast.
- **Constraints** hold what the feature must respect besides its behavior: speed, security, accessibility, compatibility, privacy, how much data it handles. Write each so it can be checked ("searching 10,000 notes answers in under 200 ms", "works without a network", "usable with the keyboard alone"), not as a wish ("fast", "secure"); a limit nobody can name yet is an open question. Constraints of the whole product live in SPEC.md, not repeated in each entry.
- **Open questions** keep undecided points visible instead of silently assuming an answer.
- **Notes** keep context that isn't a decision yet: research findings, a trial's results, options weighed. Date them and say what they are (e.g. "options discussed on 2026-10-12, nothing decided").
- Write only what the user said or decided. Don't invent requirements; an assumption is an open question. The one exception is a tester's assumption that `build` adopts while it builds the feature: it goes in Decisions marked "(assumed: the tester's recommendation)", until the user confirms or changes it at the end.

## Relations between entries

An entry that can't be built before another says so in **Needs**, so nobody starts it early and whoever picks the next work (`guide`, `swarm`) skips it until the other is done. Write it on the entry that waits, naming the one it needs, never on both: the other side is found by searching for the name. Only a real order counts: it uses what the other builds, or the other changes a rule it relies on. Two entries that merely touch the same area don't need each other.

Keep the relations true whenever you write an entry:
- **Adding or capturing one:** while checking for duplicates, look for open entries the new one needs and open entries that now need it, and write Needs on the one that waits. A relation the user didn't state is an interpretation: it's part of the draft when one is shown; otherwise say it after writing, so they can undo it.
- **Changing an entry's Description or Decisions:** see whether the change makes a relation or ends one.
- **Finishing one** (a feature, or a Bug or Debt entry done by `fix` or `chore`): remove its name from every Needs that names it, in the same commit.
- **Discarding one:** name the entries that needed it and ask, for each, whether the need is dropped or that entry is discarded too.
- **Renaming or merging one:** update the Needs that name it.
- **Starting a feature** whose Needs names an entry still open: name that entry and recommend building it first. The user decides.

Two entries that need each other are one entry, or one of the relations is wrong: show both and ask.

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
- **Leaves behavior open** (several connected decisions that would change what gets built): load the `minidev:interview` skill and interview the user with it. Write its final summary in this entry format, so approving the summary approves the text that will be recorded (see Capture).

"Just note it" (or the same in the user's language) always skips the questions and the interview: record what was said, with anything undecided as Open questions.

Only record it; don't implement it.

### Check for duplicates
Before adding or capturing, look for an identical or similar entry (including in Discarded). If one exists, show it and ask whether to merge into it or create a separate one. When merging, update the fields and keep the old notes that still hold.

### Present
Summarize by area: each entry's name and status, with its type, Version and Needs when it has them, and say which version is the current one. Apply the filter the user asks for (area, status, version). Give an entry's details only when asked.

### Plan a version
When the user says which version an entry is for, or takes it out of one ("these two go in 1.2.0", "leave sync for later"), write its Version and tell them. Don't plan entries on your own: propose, and write on their word. Entries still planned for a version when it's released are handled at the release (`changelog.md`, Releases).

### Start a feature
1. If other features are In progress, check whether one overlaps this one: the same modules (from its Description and Decisions, and `git diff --stat <main branch>...<its branch>` when the branch exists) or the same SPEC.md section. If one does, name it and recommend finishing it first: both would change the same rules, and the second merge would conflict in SPEC.md or the code. The user decides. With no overlap, say which features are in progress and go on. If the feature's Needs names an entry still open, say that too (Relations between entries).
2. Create the entry if it doesn't exist (a direct request).
3. Set it **In progress**, with its branch's name (`In progress (feature/<name>)`), on the main branch, before its branch is created, and commit that there: the main branch is where anyone looks to see what is being built. When the work reuses the session's worktree branch instead, it goes in that branch's first commit (`../../build/references/git-flow.md`, Worktrees).
4. Once the critical test list is approved, add **To check by hand**, on the feature's branch: the rules that only show in the real app, for the user to try once it's built. The automated checks live in the tests, not here.

### Finish a feature
Verifying the feature is the job of whoever built it (e.g. the `build` skill); this step only records it, in the same commit as the code.
1. Update SPEC.md with the rules of what was built (`references/spec.md`).
2. Add the change to CHANGELOG.md (`references/changelog.md`).
3. Remove the entry, its name from the Needs of the entries that waited for it and, if its area is left empty, the area.
4. The verification message, with the "To check by hand" list, is written by the skill that built the feature (`../../build/references/git-flow.md`, The verification commit), not here.

When the user says a feature is done that didn't go through `build` (built by hand or elsewhere), tell them it wasn't checked independently (no tester, no review) and offer to run it through `build` from its review step. If they just want it recorded, check that the code does what the entry says, write steps 1 to 3 from the code as it is, and commit them on their own, with a message that says it wasn't verified.

If the user later finds a problem in use, it's handled as a bug fix, not by reopening the entry. A revert is the exception: it restores the entry as it was, and this skill adds what went wrong to its Open questions (`../../build/references/git-flow.md`, When a merged change breaks).

### Change status
Update the field when the user asks, e.g. pause a feature (In progress → Idea). Write it directly and tell them. Pausing is written on the main branch; the feature's branch, if any, stays as it is, to be resumed later (`../../build/references/git-flow.md`, Resume).

### Discard
Move the entry to "Discarded", keeping only its **Description** and a **Why discarded** line with the reason and the date. If its area is left empty, remove the area. If the feature was In progress and has a branch, ask whether to delete it (`git branch -D`, the work is lost) or keep it. Before deleting it, look in `git log <main branch>..<branch> -- BACKLOG.md SPEC.md CHANGELOG.md` for document changes made on it that aren't part of the feature (an idea recorded meanwhile) and carry them to the main branch first, or they're lost with it.

### Clean up
Look for:
- duplicates and similar entries that could be merged
- entries already implemented in the code (check the code, SPEC.md and CHANGELOG.md)
- entries the user has dropped
- a Needs that names an entry no longer in the backlog, and a Version already released

Show what you intend to change and wait for the OK. Implemented ones leave the file (after checking they're in CHANGELOG.md); dropped ones go to Discarded.

### Reorganize
When areas stopped making sense (an area too big, entries in the wrong place, areas that are phases such as "Later" or "First version"), propose the new structure and apply it only after it's approved. Areas that are phases become parts of the product, taken from SPEC.md's Behavior or the code's modules, and the phase moves to each entry's Version when it names a version; a "later" pile gets none. The first time you write to a backlog whose areas are phases, propose this before going on, as SKILL.md says (Documents not in this format).
