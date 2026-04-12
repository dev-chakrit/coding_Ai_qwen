#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

exec uv --directory "$ROOT_DIR/apps/agent-server" run python "$ROOT_DIR/scripts/quality_gate_runner.py" "$@"
