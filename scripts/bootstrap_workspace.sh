#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$ROOT_DIR/templates/other-workspace"

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
  shift
fi

TARGET_DIR="${1:-}"
if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: bash ./scripts/bootstrap_workspace.sh [--force] /absolute/path/to/workspace" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

copy_file() {
  local source_path="$1"
  local target_path="$2"

  mkdir -p "$(dirname "$target_path")"

  if [[ -e "$target_path" && "$FORCE" -ne 1 ]]; then
    echo "Skip existing: $target_path"
    return
  fi

  cp "$source_path" "$target_path"
  echo "Wrote: $target_path"
}

copy_file "$TEMPLATE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
copy_file "$TEMPLATE_DIR/.rules" "$TARGET_DIR/.rules"
copy_file "$TEMPLATE_DIR/.zed/settings.json" "$TARGET_DIR/.zed/settings.json"
copy_file "$TEMPLATE_DIR/.vscode/mcp.json" "$TARGET_DIR/.vscode/mcp.json"

echo
echo "Workspace bootstrap complete for: $TARGET_DIR"
echo "Next steps:"
echo "1. Install the global MCP command once with: bash $ROOT_DIR/scripts/install_global_agent.sh"
echo "2. Add your preferred Zed/VS Code model provider."
echo "3. Create a workspace-specific quality-gates.json if you want run_quality_gates to enforce tests."
