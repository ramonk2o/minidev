#!/bin/bash
# The behavior fixture with a CLAUDE.md that never mentions the cycle: the
# project has code and git but isn't set up for it.
set -euo pipefail
bash "$(dirname "$0")/../fixture.sh"
printf '# Notes\n\nA tiny in-memory notes library for scripts.\n\nTests: `npm test`.\n' > CLAUDE.md
./.tools/git add CLAUDE.md
./.tools/git commit -qm "CLAUDE.md without the cycle"
