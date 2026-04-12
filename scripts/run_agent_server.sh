#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export LOCAL_CODING_AGENT_WORKSPACE_ROOT="${LOCAL_CODING_AGENT_WORKSPACE_ROOT:-$ROOT_DIR}"

exec uv --directory "$ROOT_DIR/apps/agent-server" run local-coding-agent
