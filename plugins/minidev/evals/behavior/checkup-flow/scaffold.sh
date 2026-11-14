#!/bin/bash
# The behavior fixture as it is: its SPEC.md says notes are listed newest
# first and the code lists them oldest first, so a check-up has at least one
# finding. The history script calls git itself, so the CLAUDE.md also says
# how to give it the sandbox's copy.
set -euo pipefail
bash "$(dirname "$0")/../fixture.sh"
sed -i.bak 's#(the eval sandbox blocks the system git)\.#(the eval sandbox blocks the system git); a script that runs git itself takes it as `--git ./.tools/git`.#' CLAUDE.md
rm CLAUDE.md.bak
grep -q -- '--git ./.tools/git' CLAUDE.md
git add CLAUDE.md
git commit -qm "CLAUDE.md: git for scripts"
