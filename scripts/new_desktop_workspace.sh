#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

FORCE=0
OPEN_IN_ZED=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      shift
      ;;
    --no-open)
      OPEN_IN_ZED=0
      shift
      ;;
    *)
      break
      ;;
  esac
done

PROJECT_NAME="${1:-}"
if [[ -z "$PROJECT_NAME" ]]; then
  echo "Usage: bash ./scripts/new_desktop_workspace.sh [--force] [--no-open] project-name" >&2
  exit 1
fi

DESKTOP_DIR="${HOME}/Desktop"
TARGET_DIR="${DESKTOP_DIR}/${PROJECT_NAME}"

mkdir -p "$TARGET_DIR"

BOOTSTRAP_ARGS=()
if [[ "$FORCE" -eq 1 ]]; then
  BOOTSTRAP_ARGS+=(--force)
fi
BOOTSTRAP_ARGS+=("$TARGET_DIR")

bash "$ROOT_DIR/scripts/bootstrap_workspace.sh" "${BOOTSTRAP_ARGS[@]}"

echo
echo "Desktop workspace ready: $TARGET_DIR"

if [[ "$OPEN_IN_ZED" -eq 1 ]]; then
  if command -v zed >/dev/null 2>&1; then
    zed "$TARGET_DIR" >/dev/null 2>&1 &
    echo "Opened in Zed with zed CLI."
  elif [[ "$(uname -s)" == "Darwin" ]]; then
    if open -a Zed "$TARGET_DIR" >/dev/null 2>&1; then
      echo "Opened in Zed with macOS open."
    else
      echo "Could not open Zed automatically. Open this folder manually: $TARGET_DIR"
    fi
  else
    echo "Could not find zed CLI. Open this folder manually in Zed: $TARGET_DIR"
  fi
fi

echo
echo "Suggested first prompt in Zed:"
echo "สร้างโปรเจ็กต์ให้เลยใน workspace นี้ และรันให้ดูเมื่อพร้อม"
