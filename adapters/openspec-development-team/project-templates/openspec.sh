#!/usr/bin/env bash
# Example only: integrate with the existing pinned wrapper after review.
set -euo pipefail
team_project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$team_project_root"
export OPENSPEC_TELEMETRY=0
export XDG_CONFIG_HOME="$team_project_root/.tools/openspec-config"
exec "$team_project_root/node_modules/.bin/openspec" "$@"
