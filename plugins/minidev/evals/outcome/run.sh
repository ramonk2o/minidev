#!/bin/bash
# Outcome evals: runs the outcome cases with and without the plugin, then runs
# each case's hidden acceptance tests (outcome/<case>/hidden/) against the code
# every run left, and prints the pass rate per arm.
# Usage: evals/outcome/run.sh [runs per arm, default 3]   (JOBS=n sets -j)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
plugin="$(cd "$here/../.." && pwd)"
out="$(mktemp -d)"
claude plugin eval "$plugin" --tag outcome --no-publish --scaffold \
  --allow-tools Bash Write Edit --runs "${1:-3}" -j "${JOBS:-4}" \
  --keep-temp --json "$out/result.json" >/dev/null
python3 -I "$here/score.py" "$out/result.json" "$here"
