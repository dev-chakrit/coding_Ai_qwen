#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VISION_RUNTIME_DIR="${VISION_RUNTIME_DIR:-$ROOT_DIR/.local-coding-agent-runtime/vision}"
VISION_VENV="${VISION_VENV:-$VISION_RUNTIME_DIR/.venv}"

mkdir -p "$VISION_RUNTIME_DIR"

if [[ ! -d "$VISION_VENV" ]]; then
  uv venv "$VISION_VENV"
fi

"$VISION_VENV/bin/python" -m pip install --upgrade pip
"$VISION_VENV/bin/pip" install "vllm>=0.8.5" "openai>=1.75.0"

echo
echo "Vision stack setup complete."
echo "Next:"
echo "  1. Run ./scripts/run_vision_server.sh"
echo "  2. Add the vision provider snippet from docs/editor-setup.md to Zed"
echo "  3. Test with ./scripts/run_vision_smoke_test.sh --image /path/to/image.png"
