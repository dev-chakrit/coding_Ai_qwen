#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LLAMA_CPP_DIR="${LLAMA_CPP_DIR:-$ROOT_DIR/vendor/llama.cpp}"
DEFAULT_LLAMA_SERVER_BIN="$LLAMA_CPP_DIR/build/bin/llama-server"
PATH_LLAMA_SERVER_BIN="$(command -v llama-server 2>/dev/null || true)"
LLAMA_SERVER_BIN="${LLAMA_SERVER_BIN:-}"
MODEL_FILE="${MODEL_FILE:-${1:-}}"
MODEL_HF_REPO="${MODEL_HF_REPO:-}"
MODEL_HF_FILE="${MODEL_HF_FILE:-}"
PORT="${LLAMA_SERVER_PORT:-8080}"
CONTEXT_SIZE="${LLAMA_CONTEXT_SIZE:-16384}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"
MODEL_ALIAS="${LOCAL_MODEL_NAME:-Gemma4-E4B-it-GGUF}"
TEMPERATURE="${LLAMA_TEMPERATURE:-0.1}"
TOP_P="${LLAMA_TOP_P:-0.9}"
MIN_P="${LLAMA_MIN_P:-0.0}"
REASONING_MODE="${LLAMA_REASONING:-on}"
CHAT_TEMPLATE_KWARGS="${LLAMA_CHAT_TEMPLATE_KWARGS:-}"

if [[ -z "$LLAMA_SERVER_BIN" ]]; then
  if [[ -x "$DEFAULT_LLAMA_SERVER_BIN" ]]; then
    LLAMA_SERVER_BIN="$DEFAULT_LLAMA_SERVER_BIN"
  elif [[ -n "$PATH_LLAMA_SERVER_BIN" ]]; then
    LLAMA_SERVER_BIN="$PATH_LLAMA_SERVER_BIN"
  fi
fi

if [[ -z "$MODEL_FILE" && -z "$MODEL_HF_REPO" ]]; then
  echo "Set MODEL_FILE to a local GGUF path, or set MODEL_HF_REPO/MODEL_HF_FILE to let llama.cpp download it."
  echo "Example local file:"
  echo "  /path/to/gemma-4-E4B-it-Q4_K_M.gguf"
  echo "Example Hugging Face repo:"
  echo "  MODEL_HF_REPO=ggml-org/gemma-4-E4B-it-GGUF"
  echo "  MODEL_HF_FILE=gemma-4-E4B-it-Q4_K_M.gguf"
  exit 1
fi

if [[ ! -x "$LLAMA_SERVER_BIN" ]]; then
  echo "llama-server not found at: $LLAMA_SERVER_BIN"
  echo "Install llama.cpp first, for example with Homebrew on macOS:"
  echo "  brew install llama.cpp"
  echo "Or set LLAMA_SERVER_BIN explicitly."
  exit 1
fi

LLAMA_ARGS=(
  --host 127.0.0.1
  --port "$PORT"
  --alias "$MODEL_ALIAS"
  --jinja
  -c "$CONTEXT_SIZE"
  -ngl "$GPU_LAYERS"
  -fa on
  -sm row
  --temp "$TEMPERATURE"
  --top-p "$TOP_P"
  --min-p "$MIN_P"
  --reasoning "$REASONING_MODE"
)

if [[ -n "$CHAT_TEMPLATE_KWARGS" ]]; then
  LLAMA_ARGS+=(--chat-template-kwargs "$CHAT_TEMPLATE_KWARGS")
fi

if [[ -n "$MODEL_FILE" ]]; then
  LLAMA_ARGS=(-m "$MODEL_FILE" "${LLAMA_ARGS[@]}")
else
  LLAMA_ARGS=(--hf-repo "$MODEL_HF_REPO" "${LLAMA_ARGS[@]}")
  if [[ -n "$MODEL_HF_FILE" ]]; then
    LLAMA_ARGS=(--hf-file "$MODEL_HF_FILE" "${LLAMA_ARGS[@]}")
  fi
fi

exec "$LLAMA_SERVER_BIN" "${LLAMA_ARGS[@]}"
