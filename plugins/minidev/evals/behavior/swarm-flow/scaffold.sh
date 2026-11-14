#!/bin/bash
# The behavior fixture plus a second idea in a module of its own, so a swarm
# can take two items whose files don't overlap.
set -euo pipefail
bash "$(dirname "$0")/../fixture.sh"
cat >> BACKLOG.md <<'ENTRY'

## Stats

### Word count
- **Status:** Idea
- **Motivation:** Scripts want to show how long a note is.
- **Description:** A new module `src/stats.js` exports `countWords(text)`, the number of words in a text.
- **Decisions:**
  - A word is a run of characters other than whitespace.
  - An empty text, or one with only whitespace, has 0 words.
- **Constraints:**
  - No new dependencies.
ENTRY
git add BACKLOG.md
git commit -qm "Backlog: Word count"
