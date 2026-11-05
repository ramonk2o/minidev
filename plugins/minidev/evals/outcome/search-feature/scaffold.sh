#!/bin/bash
set -euo pipefail
d="$(dirname "$0")"
bash "$d/../../behavior/fixture.sh"
bash "$d/../patch.sh"
