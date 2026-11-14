#!/bin/bash
# The behavior fixture as it is: one Idea in the backlog (Note titles) and
# notes listed oldest first where SPEC.md says newest first. The prompt's
# three complaints land on each: the order (a bug), the 40-character cut (a
# change to the open entry) and no way to find a note (a new idea), so the
# plan writes more than one entry and the auditor runs.
set -euo pipefail
bash "$(dirname "$0")/../fixture.sh"
