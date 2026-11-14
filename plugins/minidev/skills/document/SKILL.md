---
name: document
description: In projects set up for the minidev cycle, or elsewhere when the user explicitly asks to change one of these files, own a project's product documents and keep their roles apart, BACKLOG.md (ideas, the features being built, and bugs or debt left for later; or the GitHub issues a project keeps them in), SPEC.md (how the product works today) and CHANGELOG.md (what changed in each version), creating any of them that's missing, adapted to the project. Use it for ANY change to these files, even a one-word fix, and whenever the user wants to record, list, start, finish, discard, plan, relabel or clean up features or ideas ("note this idea", "what's in the backlog?", "X is done", "fix the issues' labels"), update, create or audit the spec ("does SPEC.md match the code?"), write changelog entries, or cut a release ("release 1.4.0", "prepare the new version"). Also use it when another skill (like build) needs a feature's status changed or these documents updated.
---

# Document

Three documents describe the product, each answering one question in time:

| Document | Answers | Time |
|---|---|---|
| `BACKLOG.md` | What may come, and why the user wants it (features, plus bugs and debt left for later) | future |
| `SPEC.md` | How the product works **today**: rules, data, technical decisions, constraints | present |
| `CHANGELOG.md` | What changed in each version, for the people who use it | past |

A project whose CLAUDE.md says `Backlog: GitHub issues` keeps the backlog in the repository's issues instead of BACKLOG.md, so the team sees it as it changes; this skill writes those issues too, and each step below that names BACKLOG.md is written on the issue (`references/issues.md`).

The git history keeps the detail behind all three. This skill is the only one that writes them, so their roles stay apart and their formats stay consistent. Reading them for context needs no skill; presenting the backlog when the user asks what's in it ("what's in the backlog?") does, since it's an operation of `references/backlog.md` (Present).

Project instructions (CLAUDE.md, AGENTS.md…) may add project-specific details, such as how to verify a feature or the release steps outside these files. Follow them on top of this skill; when they conflict, they win.

## Where to look

Read the reference for the document you're about to change, before changing it:
- `references/backlog.md`: statuses, the entry format, the relations between entries and every backlog operation (create, capture, record a bug or debt, add, check for duplicates, present, plan a version, start, finish, change status, discard, clean up, reorganize).
- `references/issues.md`: the backlog in GitHub issues: how entries, statuses, versions, relations and each operation map to issues, labels and milestones, and migrating from BACKLOG.md.
- `references/spec.md`: the spec's role, how to create one adapted to the project, and when and how to update it.
- `references/spec-audit.md`: checking SPEC.md against the code, rule by rule, when it's created for existing code, when `setup` adopts a project, or when the user asks.
- `references/changelog.md`: entry format, creating the file, and releases.

## Rules across the documents

- **Each fact lives in one place.** A rule of behavior lives in SPEC.md. The changelog says, in a sentence or two, what changed for the user; a backlog entry says what is wanted and why. Don't copy SPEC rules into other documents (the README included): point to SPEC.md. Copies drift, and then two documents disagree.
- **SPEC.md describes only what exists.** It's updated from what was actually built (a feature finished, a fix that corrects a rule, a chore that changes a technical decision, a revert), never when something is planned. A planned rule lives in the feature's Decisions until then.
- **A finished feature leaves the backlog** and lives on in the changelog (what changed), the spec (the rules) and git history (the detail).
- **When a feature changes existing behavior**, its Decisions say which SPEC.md rule changes and how, so the update at the end is a known edit, not a rediscovery.

## The feature lifecycle at a glance

1. **Recorded** in BACKLOG.md as an Idea.
2. **Started:** In progress, with its branch's name; what to check by hand is added on the feature's branch. Where and when it's written: `references/backlog.md`, Start a feature.
3. **Finished:** verified; the entry leaves BACKLOG.md, the change goes to CHANGELOG.md and the rules to SPEC.md, all in the same commit as the code. The verification results go in that commit's message. If it fails later in use, it's a bug, not a reopened entry, unless its change is reverted, which restores the entry (`../build/references/git-flow.md`, When a merged change breaks).
4. **Released:** the version's changes leave `[Unreleased]` in CHANGELOG.md.

Bug and Debt entries skip In progress: they stay in BACKLOG.md until `fix` or `chore` does them, and leave it in that work's commit.

## Documents not in this format

A project may already have these documents (or older ones like `FEATURES.md`, `TODO.md`, `HISTORY.md`) with another structure. Don't rewrite them on your own. The first time you work on one, show how it differs from this skill's format, propose how to align it, and wait for the OK. Until then, follow the structure that's there.

## Language

- Write the documents in the language the project's CLAUDE.md names (`Documents: <language>`), or the one the calling skill passes (`brainstorm` settles it in its plan), or else in that of its existing docs. If none says, ask once; if CLAUDE.md has a Development cycle section, add that line there so it isn't asked again. Don't create a CLAUDE.md or that section for it.
- Talk to the user in the language of the conversation.

## Legends

Each document starts with a short legend, so it's readable without this skill. The full rules live here; the legend only orients. The exact texts are in each reference.

## Confirmation

| Operation | Before writing |
|---|---|
| Capture a feature from the conversation | Show the draft, wait for OK (an interview summary the user already approved counts as that OK, and so does `build`'s start message, which shows the draft with the critical test list) |
| Clear idea, bug or debt left for later, status change or version asked by the user | Write directly, then tell them |
| Entries created, changed and discarded from a `rethink` plan | The plan the user approved is the OK: write, then tell them |
| Clean up, reorganize (relabeling issues included), new area, aligning a document's format | Show the plan, wait for OK |
| Create SPEC.md | Show the proposed outline, wait for OK (an outline the user approved in a `brainstorm` plan counts as that OK) |
| Update SPEC.md when a feature is finished, changelog entry | Write directly as part of finishing, then tell them |
| Bug fix: changelog entry under Fixed if users could see the bug, SPEC.md if a rule changed, Bug entry removed | Write directly as part of the fix, then tell them |
| Chore: SPEC.md if a technical decision changed, changelog if users will notice (or a notable docs/tooling change, `references/changelog.md`), Debt entry removed | Write directly as part of the chore, then tell them |
| Revert: restored entry back to Idea with what went wrong in its Open questions, document changes that rode along reapplied, changelog line if the change was released | Write directly as part of the revert, then tell them |
| Release | Show the version, date and entries, wait for OK |
| Spec audit | Show the report, wait for OK (the user may approve parts) |

## Commits

In a git repository, commit after writing (backlog changes kept in issues aren't committed), on the branch you're on (a feature set In progress is the exception: `references/backlog.md`, Start a feature), with a short message saying what changed (e.g. "Tables: recorded in BACKLOG (Idea)", "Sync discarded", "Release 1.4.0"). Commit only these documents, never other pending changes. When the change is part of a larger piece of work being committed, it goes in that commit instead: finishing a feature, a fix or a chore, or the documents `brainstorm` or `setup` create, which go in the commit those skills offer (don't commit them here). Don't push these commits on their own: they go out with the next merge into the main branch or release (in pull request mode, inside the next pull request). On a work branch (feature, fix, chore, release) they're squashed into that branch's commit, whose message gets a line for each change that isn't part of the work.
