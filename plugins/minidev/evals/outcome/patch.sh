#!/bin/bash
# Turns the behavior fixture into a fair outcome fixture: the ordering bug is
# fixed, SPEC.md gains a rule the visible tests don't check, a Search idea is
# added, and CLAUDE.md no longer tells Claude to stop without the minidev skills
# (the baseline arm runs without them).
set -euo pipefail
sed -i '' 's/a.createdAt - b.createdAt/b.createdAt - a.createdAt/' src/notes.js
python3 -I - <<'PY'
import re
s=open('SPEC.md').read()
s=s.replace("- Notes are listed newest first.\n","- Notes are listed newest first.\n- `listNotes` returns a new list each time: changing that list doesn't change the stored notes.\n",1)
open('SPEC.md','w').write(s)
c=open('CLAUDE.md').read()
c=c.replace("When a step needs one of its skills and it isn't available, tell the user and stop; don't imitate it from memory.","If its skills aren't available, do the work directly.",1)
open('CLAUDE.md','w').write(c)
b=open('BACKLOG.md').read()
b=b.replace("""## Notes
""","""## Notes

### Search
- **Status:** Idea
- **Motivation:** Scripts need to find notes without listing all of them.
- **Description:** `searchNotes(query)`, exported from `src/notes.js`, returns the notes whose text matches the query, in the same order as `listNotes`.
- **Decisions:**
  - Matching ignores case and accents: "cafe" finds "Café".
  - A query with several words finds the notes that contain every word, in any order, anywhere in the text.
  - Words match inside other words: "milk" finds "milkshake".
  - A query that is empty or only spaces returns no notes.
- **Constraints:**
  - No new dependencies.
""",1)
open('BACKLOG.md','w').write(b)
PY
git add -A
git commit -qm "Notes 1.0.1"
