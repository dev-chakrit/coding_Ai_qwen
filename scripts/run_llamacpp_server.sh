#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LLAMA_CPP_DIR="${LLAMA_CPP_DIR:-$ROOT_DIR/vendor/llama.cpp}"
LLAMA_SERVER_BIN="${LLAMA_SERVER_BIN:-$LLAMA_CPP_DIR/build/bin/llama-server}"
MODEL_FILE="${MODEL_FILE:-${1:-}}"
PORT="${LLAMA_SERVER_PORT:-8080}"
CONTEXT_SIZE="${LLAMA_CONTEXT_SIZE:-32768}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"
MODEL_ALIAS="${LOCAL_MODEL_NAME:-Qwen3-Coder-Next}"

if [[ -z "$MODEL_FILE" ]]; then
  echo "MODEL_FILE is required. Point it to the first GGUF shard, for example:"
  echo "  /path/to/Qwen3-Coder-Next-00001-of-00004.gguf"
  exit 1
fi

if [[ ! -x "$LLAMA_SERVER_BIN" ]]; then
  echo "llama-server not found at: $LLAMA_SERVER_BIN"
  echo "Run ./scripts/setup_popos.sh first or set LLAMA_SERVER_BIN explicitly."
  exit 1
fi

exec "$LLAMA_SERVER_BIN" \
  -m "$MODEL_FILE" \
  --host 127.0.0.1 \
  --port "$PORT" \
  --alias "$MODEL_ALIAS" \
  --jinja \
  -c "$CONTEXT_SIZE" \
  -ngl "$GPU_LAYERS" \
  -fa on \
  -sm row \
  --temp 0.2 \
  --top-p 0.95 \
  --min-p 0.0
