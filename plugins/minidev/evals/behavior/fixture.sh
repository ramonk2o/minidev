#!/bin/bash
# Builds the "Notes" fixture project in the current directory: a tiny Node
# library set up for the minidev cycle, with one Idea in the backlog and one
# known bug (notes are listed oldest first; SPEC.md says newest first).
set -euo pipefail
mkdir -p src test
cat > package.json <<'EOF'
{ "name": "notes", "version": "1.0.0", "type": "module", "private": true,
  "scripts": { "test": "node --test" } }
EOF
cat > src/notes.js <<'EOF'
let notes = [];
let clock = 0;

export function reset() { notes = []; clock = 0; }

export function addNote(text) {
  if (typeof text !== 'string' || text.trim() === '') throw new Error('A note needs text');
  const note = { id: notes.length + 1, text, createdAt: ++clock };
  notes.push(note);
  return note;
}

export function listNotes() {
  return [...notes].sort((a, b) => a.createdAt - b.createdAt);
}
EOF
cat > test/notes.test.js <<'EOF'
import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { addNote, listNotes, reset } from '../src/notes.js';

beforeEach(() => reset());

test('an empty note is rejected', () => {
  assert.throws(() => addNote('   '), /needs text/);
});

test('a note keeps its text', () => {
  addNote('Buy milk');
  assert.equal(listNotes()[0].text, 'Buy milk');
});
EOF
cat > README.md <<'EOF'
# Nots

A tiny notes library.
EOF
cat > SPEC.md <<'EOF'
# Notes

How Notes works today, as rules (not visual details), plus its data and technical decisions. Managed with the `document` skill: it's updated when a feature, fix or chore changes what it describes, from what was built. Ideas live in BACKLOG.md; what changed and when lives in CHANGELOG.md.

## Goal
A small in-memory notes library for scripts.

## Behavior
### Notes
- A note with no text (empty or only spaces) is rejected.
- Notes are listed newest first.

## Technical decisions
- Plain Node.js with `node:test`, no dependencies: the library is tiny.

## Constraints
- No dependencies outside the Node.js standard library: it's copied into scripts.
EOF
cat > BACKLOG.md <<'EOF'
# Backlog

Feature ideas, the feature being built, and bugs and debt left for later, managed with the `document` skill. Implemented features leave this file: what changed goes to CHANGELOG.md and the rules to SPEC.md.

Status: **Idea** → **In progress** (one at a time) → done (leaves the file in the commit that implements it). Discarded ideas go to the last section.

## Notes

### Note titles
- **Status:** Idea
- **Motivation:** Scripts that list notes print the whole text, which is hard to scan.
- **Description:** Each note gets a `title`, taken from its text.
- **Decisions:**
  - The title is the first line of the text, trimmed.
  - A title longer than 40 characters is cut to 40 and ends with "…" (41 characters in all).
  - `title` is set when the note is added and returned by `listNotes`.
- **Constraints:**
  - No new dependencies.
EOF
cat > CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-10-01

### Added
- Add and list notes.
EOF
cat > CLAUDE.md <<'EOF'
# Notes

A tiny in-memory notes library for scripts.
- How it works today: `SPEC.md`. Ideas, the feature in progress and bugs or debt left for later: `BACKLOG.md`. What changed in each version: `CHANGELOG.md`.

## Commands
- Tests: `npm test` (node:test)
- Git: run it as `./.tools/git` from the project folder (the eval sandbox blocks the system git).

## Tests
- Tests live in `test/`, named `<module>.test.js`; each starts from `reset()`.

## Development cycle
This project uses the `minidev` cycle. When a step needs one of its skills and it isn't available, tell the user and stop; don't imitate it from memory.
- Ideas: `document`. Features: `build`. Bugs: `fix`. Refactoring, upgrades and other changes that keep the behavior: `chore`.
- Integration: local merge.
- Documents: English.
EOF
printf 'node_modules/\n' > .gitignore
git init -q -b main
git config user.name "Eval User"
git config user.email "eval@example.com"
git config commit.gpgsign false
git add -A
git commit -qm "Notes 1.0.0"
# The eval sandbox blocks the system git (Xcode's shim and its folder), so the
# run gets its own copy; the case prompt tells Claude to call it.
mkdir -p .tools
cp "$(xcrun --find git 2>/dev/null || command -v git)" .tools/git
echo ".tools/" >> .git/info/exclude
