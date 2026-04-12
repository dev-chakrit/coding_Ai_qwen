# Local Coding Agent for Zed and VS Code

โปรเจ็กต์นี้เป็นจุดเริ่มต้นสำหรับทำ local coding agent ที่:

- ใช้โมเดลจาก Hugging Face ผ่าน OpenAI-compatible endpoint
- ต่อกับ `Zed` และ `VS Code` ผ่าน `MCP`
- รู้จักโครงสร้าง workspace และช่วย scaffold งานแบบ clean architecture
- รันบน `Pop!_OS` ได้โดยไม่ต้องพึ่ง cloud model

## แนวทางที่แนะนำกับเครื่องของคุณ

สเปก `Xeon E5-2686 + RAM 128GB + RTX 3060 12GB` เหมาะกับแนวนี้:

- editor หลัก: `Zed`
- editor เสริมสำหรับ strict workflow: `VS Code`
- local model runtime: `llama.cpp`
- model เริ่มต้น: `Qwen/Qwen3-Coder-Next-GGUF`
- vision model เริ่มต้น: `Qwen/Qwen3-VL-2B-Instruct`
- quantization เริ่มต้น: `Q4_K_M`

เหตุผลคือแยกบทบาทชัดเจน:

- `llama.cpp` ทำหน้าที่เสิร์ฟโมเดลแบบ OpenAI-compatible
- `Zed` ใช้ endpoint นี้เป็น agent model
- MCP server ใน repo นี้ทำหน้าที่เป็น repo-aware tool layer
- optional vision sidecar ใช้ `vLLM` สำหรับรับรูป UI และ screenshot error
- `VS Code` ใช้ repo เดียวกันนี้ในโหมด strict ได้ผ่าน custom agents และ hooks

## สถานะตอนนี้แบบตรงไปตรงมา

ยังไม่ใช่ระดับ “ไร้ที่ติ” แต่เป็นฐานที่ใช้งานจริงและต่อยอดได้ดี

ข้อที่พร้อมแล้ว:

- local MCP server ทำงานได้
- มีกฎ test-first, repair loop, clean architecture, frontend quality, และ quality gates
- มี config สำหรับ Zed และ VS Code
- มี script setup, run model server, และ run MCP server

ข้อที่ยังเป็นข้อจำกัดจริง:

- คุณภาพการแก้โค้ดขึ้นกับโมเดลที่เลือกและคุณภาพ tool calling
- ยังไม่มี semantic index หรือ code graph ขั้นสูงแบบ editor proprietary บางตัว
- การวน loop แก้จนผ่านยังขึ้นกับ editor/model ทำตาม instructions ได้ดีแค่ไหน
- ความเร็วและ context จริงถูกจำกัดด้วย `llama.cpp` config และ VRAM ไม่ใช่แค่ตัวเลขบน model card

## Context ตอนนี้ได้มากแค่ไหน

ตัวโมเดล `Qwen3-Coder-Next` รองรับ context `262,144` tokens ตาม model card แต่ในโปรเจ็กต์นี้ค่าดีฟอลต์ของ local server ถูกตั้งไว้ที่ `32,768` ผ่าน `LLAMA_CONTEXT_SIZE=32768` เพื่อให้เหมาะกับการเริ่มต้นบน `RTX 3060 12GB`

สรุปแบบใช้งานจริง:

- model capability สูงสุด: `262,144`
- default ในโปรเจ็กต์นี้: `32,768`
- ถ้าเครื่องไหวและยอมรับความช้าขึ้น สามารถเพิ่มเป็น `40960` หรือ `65536` ได้โดยปรับ `LLAMA_CONTEXT_SIZE`

ดังนั้นคำตอบคือ “รับ context ได้เยอะพอสมควรแล้ว” แต่ดีฟอลต์ยังไม่ได้เปิดสุด เพราะบนเครื่องคุณควรบาลานซ์ระหว่างความนิ่งกับความยาว context ก่อน

## คำสั่งติดตั้งแบบครบ

### 1. ติดตั้งแพ็กเกจระบบบน Pop!_OS

```bash
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
```

### 2. ติดตั้ง `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/.local/bin" sh
export PATH="$HOME/.local/bin:$PATH"
```

### 3. ติดตั้ง Hugging Face CLI

```bash
uv tool install hf
export PATH="$HOME/.local/bin:$PATH"
```

### 4. ติดตั้ง Zed บน Linux

```bash
curl -f https://zed.dev/install.sh | sh
```

### 5. ติดตั้ง dependencies ของ MCP server

```bash
uv --directory ./apps/agent-server sync --extra dev
```

### 6. ติดตั้ง VS Code เพิ่ม ถ้าต้องการโหมด strict workflow

```bash
sudo apt install -y code
```

### 7. ดาวน์โหลดโมเดลจาก Hugging Face

```bash
mkdir -p ./models
hf download Qwen/Qwen3-Coder-Next-GGUF \
  --include "Qwen3-Coder-Next-Q4_K_M/*" \
  --local-dir ./models/Qwen3-Coder-Next-Q4_K_M
```

### 8. เตรียม `llama.cpp`

```bash
git clone https://github.com/ggml-org/llama.cpp.git ./vendor/llama.cpp
cmake -S ./vendor/llama.cpp -B ./vendor/llama.cpp/build -G Ninja -DGGML_CUDA=ON
cmake --build ./vendor/llama.cpp/build --config Release -j
```

ถ้า `nvcc --version` ยังไม่มี ให้ติดตั้ง CUDA toolkit ที่เข้ากับ driver ของเครื่องก่อน มิฉะนั้น `llama.cpp` จะถูก build แบบ CPU อย่างเดียว

### 9. ติดตั้ง vision sidecar แบบ optional

```bash
bash ./scripts/setup_vision_stack.sh
```

ถ้าคุณต้องการให้โมเดลรับรูป UI หรือ screenshot error ได้ ให้ใช้ขั้นนี้เพิ่ม

## โครงสร้าง

```text
.
├── .vscode/mcp.json
├── .vscode/settings.json
├── .zed/settings.json
├── .rules
├── AGENTS.md
├── quality-gates.json
├── apps/
│   ├── agent-server/
│   │   ├── pyproject.toml
│   │   ├── src/local_coding_agent/
│   │   └── tests/
│   └── vscode-extension/
├── docs/
│   ├── agent-behavior.md
│   ├── clean-architecture.md
│   ├── editor-setup.md
│   ├── quality-gates.md
│   └── vision-workflow.md
└── scripts/
    ├── run_agent_server.sh
    ├── run_llamacpp_server.sh
    ├── run_quality_gates.sh
    ├── run_vision_server.sh
    ├── run_vision_smoke_test.sh
    ├── run_vscode_hook.sh
    ├── setup_popos.sh
    └── setup_vision_stack.sh
```

## Quick Start

1. เตรียมเครื่อง Pop!_OS

```bash
bash ./scripts/setup_popos.sh
```

2. โหลด dependencies ของ MCP server

```bash
uv --directory ./apps/agent-server sync --extra dev
```

ถ้าต้องการปรับค่า environment เพิ่ม เช่น command allowlist หรือ model path ให้คัดลอก `.env.example` เป็น `.env`

3. ดาวน์โหลดโมเดล GGUF จาก Hugging Face

```bash
mkdir -p ./models
hf download Qwen/Qwen3-Coder-Next-GGUF \
  --include "Qwen3-Coder-Next-Q4_K_M/*" \
  --local-dir ./models/Qwen3-Coder-Next-Q4_K_M
```

4. รัน local model server

```bash
MODEL_FILE=./models/Qwen3-Coder-Next-Q4_K_M/Qwen3-Coder-Next-Q4_K_M-00001-of-00004.gguf \
bash ./scripts/run_llamacpp_server.sh
```

5. รัน MCP server

```bash
bash ./scripts/run_agent_server.sh
```

6. ถ้าต้องการรับรูปภาพด้วย ให้รัน vision sidecar

```bash
bash ./scripts/run_vision_server.sh
```

จากนั้นลอง smoke test ด้วย:

```bash
bash ./scripts/run_vision_smoke_test.sh --image /path/to/reference-or-error.png
```

7. เปิด repo นี้ใน Zed หรือ VS Code

- Zed: ใช้ค่าจาก `.zed/settings.json` และเพิ่ม local model provider ตาม [docs/editor-setup.md](./docs/editor-setup.md)
- VS Code: ใช้ `.vscode/mcp.json` และ `.vscode/settings.json`

## MCP Server มีเครื่องมืออะไรบ้าง

- `workspace_summary` สรุป tree ของโปรเจ็กต์
- `find_files` หาไฟล์ตาม glob
- `search_code` ค้นโค้ดทั้ง repo
- `read_text_file` อ่านไฟล์แบบเจาะช่วงบรรทัด
- `write_text_file` สร้างหรือเขียนไฟล์ใหม่
- `replace_in_file` แก้โค้ดแบบตรงจุด
- `create_clean_architecture_feature` scaffold feature slice แบบ clean architecture
- `run_project_command` รันคำสั่งตรวจสอบที่อยู่ใน allowlist
- `get_quality_gates` อ่าน quality-gates ของ repo
- `suggest_quality_gate_commands` เลือก verification commands ตามไฟล์ที่แก้
- `run_quality_gates` รัน quality gates ตาม config กลาง

prompts/resources เพิ่มสำหรับ vision workflow:

- `workflow://vision-workflow-guide`
- `ui_reference_prompt`
- `screenshot_debug_prompt`

## Agent behavior ที่ฝังไว้ในโปรเจ็กต์

ผมเพิ่มกติกาสำหรับ agent แล้วเพื่อให้มีนิสัยแบบที่คุณต้องการ:

- `.rules` สำหรับ Zed
- `AGENTS.md` สำหรับ agent อื่น ๆ ที่อ่านไฟล์มาตรฐานนี้ได้
- `.github/copilot-instructions.md` สำหรับ VS Code
- `.github/instructions/testing.instructions.md` สำหรับ workflow แบบ test-first และ repair loop
- `.github/instructions/frontend.instructions.md` สำหรับงาน frontend
- `.github/prompts/*.prompt.md` สำหรับเรียกใช้งานเป็น prompt สำเร็จรูป

กติกาหลักคือ:

- ก่อนแก้ของที่มีผลกระทบ ต้องคิด verification step ก่อน
- ถ้า test fail ต้องย้อนกลับไปแก้ที่ root cause แล้ว rerun
- ห้ามแก้แบบลวก ๆ เช่นลด assertion, mute error, หรือซ่อนปัญหา
- งาน frontend ต้องนับ UX/UI เป็นส่วนหนึ่งของ definition of done
- ระหว่างงานหลายขั้น agent ควรรายงานความคืบหน้าสั้น ๆ ให้เห็นว่ากำลังทำอะไรอยู่

นอกจากนี้ยังมี `quality-gates.json` เป็น source of truth สำหรับ verification commands ทั้ง Zed, VS Code, และ shell

## Clean Architecture ที่ server ใช้เป็น baseline

แต่ละ feature จะถูกแยกเป็น 4 ชั้น:

- `domain`
- `application`
- `infrastructure`
- `presentation`

รายละเอียดอยู่ที่ [docs/clean-architecture.md](./docs/clean-architecture.md)

มาตรฐาน workflow และ frontend เพิ่มเติม:

- [docs/agent-behavior.md](./docs/agent-behavior.md)
- [docs/frontend-standards.md](./docs/frontend-standards.md)
- [docs/quality-gates.md](./docs/quality-gates.md)
- [docs/vision-workflow.md](./docs/vision-workflow.md)

## งานที่ใช้ vision sidecar ได้ดี

- แนบภาพ UI ที่อยากได้ แล้วให้มันสรุป visual direction ก่อนลงมือเขียนโค้ด
- แนบ screenshot error หรือ broken layout แล้วให้มันอ่านข้อความและ state บนภาพ
- แนบ mockup แล้วให้มันสรุปเป็น build brief ส่งต่อให้ coder model

workflow ที่แนะนำ:

1. ใช้ vision model วิเคราะห์ภาพ
2. สรุปผลลัพธ์ออกมาเป็น build/debug brief
3. สลับกลับไป coder model
4. ให้ coder model ใช้ MCP tools และ quality gates ทำงานใน repo จริง

## หมายเหตุสำคัญ

- repo นี้ยังไม่สามารถรับประกันระดับ “ไร้ที่ติ” ได้ เพราะคุณภาพสุดท้ายยังขึ้นกับโมเดล, context, และ editor runtime
- เป้าหมายของ repo นี้คือทำ “local stack ที่ใช้ได้จริง” และเพิ่ม quality rails ให้พลาดยากขึ้น
- ถ้าต้องการ workflow เบาและตรง ให้เริ่มจาก `Zed`
- ถ้าต้องการ workflow เข้มพร้อม custom agents และ stop hooks ให้ใช้ `VS Code` กับไฟล์ที่เพิ่มไว้ใน repo นี้
