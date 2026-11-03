---
name: document
description: In projects set up for the minidev cycle, or that already have these files, own a project's product documents and keep their roles apart, BACKLOG.md (ideas, the feature being built, and bugs or debt left for later), SPEC.md (how the product works today) and CHANGELOG.md (what changed in each version), creating any of them that's missing, adapted to the project. Use it for ANY change to these files, even a one-word fix, and whenever the user wants to record, list, start, finish, discard or clean up features or ideas ("note this idea", "what's in the backlog?", "X is done"), update or create the spec, write changelog entries, or cut a release ("release 1.4.0", "prepare the new version"). Also use it when another skill (like build) needs a feature's status changed or these documents updated.
---

# Product

Three documents describe the product, each answering one question in time:

| Document | Answers | Time |
|---|---|---|
| `BACKLOG.md` | What may come, and why the user wants it | future |
| `SPEC.md` | How the product works **today**: rules, data, technical decisions | present |
| `CHANGELOG.md` | What changed in each version, for the people who use it | past |

The git history keeps the detail behind all three. This skill is the only one that writes them, so their roles stay apart and their formats stay consistent. Reading them for context needs no skill.

Project instructions (CLAUDE.md, AGENTS.md…) may add project-specific details, such as how to verify a feature or the release steps outside these files. Follow them on top of this skill; when they conflict, they win.

## Where to look

Read the reference for the document you're about to change, before changing it:
- `references/backlog.md`: statuses, the entry format and every backlog operation (add, capture, start, finish, done, discard, clean up, reorganize).
- `references/spec.md`: the spec's role, how to create one adapted to the project, and when and how to update it.
- `references/changelog.md`: entry format, creating the file, and releases.

## Rules across the documents

- **Each fact lives in one place.** A rule of behavior lives in SPEC.md. The changelog says, in a sentence or two, what changed for the user; a backlog entry says what is wanted and why. Don't copy SPEC rules into other documents (the README included): point to SPEC.md. Copies drift, and then two documents disagree.
- **SPEC.md describes only what exists.** It's updated when a feature is finished, from what was actually built, not when it's planned. A planned rule lives in the feature's Decisions until then.
- **A finished feature leaves the backlog** and lives on in the changelog (what changed), the spec (the rules) and git history (the detail).
- **When a feature changes existing behavior**, its Decisions say which SPEC.md rule changes and how, so the update at the end is a known edit, not a rediscovery.

## The feature lifecycle at a glance

1. **Recorded** in BACKLOG.md as an Idea.
2. **Started:** In progress, with what to check by hand.
3. **Finished:** verified; the entry leaves BACKLOG.md, the change goes to CHANGELOG.md and the rules to SPEC.md, all in the same commit as the code. The verification results go in that commit's message. If it fails later in use, it's a bug, not a reopened entry.
4. **Released:** the version's changes leave `[Unreleased]` in CHANGELOG.md.

## Documents not in this format

A project may already have these documents (or older ones like `FEATURES.md`, `TODO.md`, `HISTORY.md`) with another structure. Don't rewrite them on your own. The first time you work on one, show how it differs from this skill's format, propose how to align it, and wait for the OK. Until then, follow the structure that's there.

## Language

- Write the documents in the language of the project's existing docs. If there are none, ask once.
- Talk to the user in the language of the conversation.

## Legends

Each document starts with a short legend, so it's readable without this skill. The full rules live here; the legend only orients. The exact texts are in each reference.

## Confirmation

| Operation | Before writing |
|---|---|
| Capture a feature from the conversation | Show the draft, wait for OK (an interview summary the user already approved counts as that OK) |
| Clear idea, status change asked by the user | Write directly, then tell them |
| Clean up, reorganize, new area, aligning a document's format | Show the plan, wait for OK |
| Create SPEC.md | Show the proposed outline, wait for OK |
| Update SPEC.md when a feature is finished, changelog entry | Write directly as part of finishing, then tell them |
| Bug fix: changelog entry under Fixed, SPEC.md if a rule changed | Write directly as part of the fix, then tell them |
| Release | Show the version, date and entries, wait for OK |

## Commits

In a git repository, commit after writing, with a short message saying what changed (e.g. "Tables: recorded in BACKLOG (Idea)", "Sync discarded", "Release 1.4.0"). Commit only these documents, never other pending changes. When the change is part of a larger piece of work being committed, such as finishing a feature, it goes in that commit instead. Don't push these commits on their own: they go out with the next merge into the main branch or release (in pull request mode, inside the next pull request). On a feature or fix branch they're squashed into that branch's commit, whose message gets a line for each.
