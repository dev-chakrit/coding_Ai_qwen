#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

UV_BIN="${UV_BIN:-}"

if [[ -z "$UV_BIN" ]]; then
  if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
  else
    for candidate in \
      "$HOME/.local/bin/uv" \
      "/usr/local/bin/uv" \
      "/opt/homebrew/bin/uv"
    do
      if [[ -x "$candidate" ]]; then
        UV_BIN="$candidate"
        break
      fi
    done
  fi
fi

if [[ -z "$UV_BIN" ]]; then
  echo "uv was not found. Install it first or set UV_BIN to the absolute path." >&2
  exit 127
fi

"$UV_BIN" tool install --editable "$ROOT_DIR/apps/agent-server" --force

echo
echo "Installed global MCP command: local-coding-agent"
echo "If the command is still missing, add this to your shell profile:"
echo '  export PATH="$HOME/.local/bin:$PATH"'
