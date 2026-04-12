#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LLAMA_CPP_DIR="$ROOT_DIR/vendor/llama.cpp"

install_system_packages() {
  sudo apt update
  sudo apt install -y \
    build-essential \
    ccache \
    cmake \
    curl \
    git \
    git-lfs \
    ninja-build \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-venv
}

install_uv() {
  export PATH="$HOME/.local/bin:$PATH"

  if command -v uv >/dev/null 2>&1; then
    return
  fi

  curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/.local/bin" sh
}

prepare_agent_server() {
  uv --directory "$ROOT_DIR/apps/agent-server" sync --extra dev
}

install_hf_cli() {
  export PATH="$HOME/.local/bin:$PATH"

  if command -v hf >/dev/null 2>&1; then
    return
  fi

  uv tool install hf
}

prepare_llamacpp() {
  mkdir -p "$ROOT_DIR/vendor"

  if [[ ! -d "$LLAMA_CPP_DIR/.git" ]]; then
    git clone https://github.com/ggml-org/llama.cpp.git "$LLAMA_CPP_DIR"
  fi

  if command -v nvcc >/dev/null 2>&1; then
    cmake -S "$LLAMA_CPP_DIR" -B "$LLAMA_CPP_DIR/build" -G Ninja -DGGML_CUDA=ON
  else
    cmake -S "$LLAMA_CPP_DIR" -B "$LLAMA_CPP_DIR/build" -G Ninja
  fi

  cmake --build "$LLAMA_CPP_DIR/build" --config Release -j
}

install_system_packages
install_uv
install_hf_cli
prepare_agent_server
prepare_llamacpp

echo
echo "Setup complete."
echo "Next:"
echo "  1. Download a GGUF model from Hugging Face"
echo "  2. Run ./scripts/run_llamacpp_server.sh"
echo "  3. Open the repo in Zed or VS Code"
