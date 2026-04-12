#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VISION_RUNTIME_DIR="${VISION_RUNTIME_DIR:-$ROOT_DIR/.local-coding-agent-runtime/vision}"
VISION_VENV="${VISION_VENV:-$VISION_RUNTIME_DIR/.venv}"
VISION_VLLM_BIN="${VISION_VLLM_BIN:-$VISION_VENV/bin/vllm}"

MODEL_ID="${VISION_MODEL_ID:-Qwen/Qwen3-VL-2B-Instruct}"
MODEL_NAME="${VISION_MODEL_NAME:-Qwen3-VL-2B-Instruct}"
HOST="${VISION_MODEL_HOST:-127.0.0.1}"
PORT="${VISION_MODEL_PORT:-8081}"
API_KEY="${VISION_MODEL_API_KEY:-local-vision}"
MAX_MODEL_LEN="${VISION_MAX_MODEL_LEN:-8192}"
LIMIT_MM_PER_PROMPT="${VISION_LIMIT_MM_PER_PROMPT:-{\"image\":2}}"
GPU_MEMORY_UTILIZATION="${VISION_GPU_MEMORY_UTILIZATION:-0.85}"

if [[ ! -x "$VISION_VLLM_BIN" ]]; then
  echo "vLLM executable not found at: $VISION_VLLM_BIN"
  echo "Run ./scripts/setup_vision_stack.sh first or set VISION_VLLM_BIN explicitly."
  exit 1
fi

exec "$VISION_VLLM_BIN" serve "$MODEL_ID" \
  --host "$HOST" \
  --port "$PORT" \
  --api-key "$API_KEY" \
  --served-model-name "$MODEL_NAME" \
  --dtype auto \
  --max-model-len "$MAX_MODEL_LEN" \
  --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION" \
  --limit-mm-per-prompt "$LIMIT_MM_PER_PROMPT" \
  --trust-remote-code
