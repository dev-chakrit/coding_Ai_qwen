#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VISION_RUNTIME_DIR="${VISION_RUNTIME_DIR:-$ROOT_DIR/.local-coding-agent-runtime/vision}"
VISION_VENV="${VISION_VENV:-$VISION_RUNTIME_DIR/.venv}"

if [[ ! -x "$VISION_VENV/bin/python" ]]; then
  echo "Vision venv not found at: $VISION_VENV"
  echo "Run ./scripts/setup_vision_stack.sh first."
  exit 1
fi

exec "$VISION_VENV/bin/python" "$ROOT_DIR/scripts/vision_smoke_test.py" "$@"
