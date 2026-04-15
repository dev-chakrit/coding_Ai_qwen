# Editor Setup

## แนะนำให้เริ่มด้วย Zed

stack นี้เหมาะกับ `Zed + llama.cpp + MCP` มากที่สุด เพราะ Zed ต่อ OpenAI-compatible local endpoint ได้ตรง และใช้ MCP tools ได้ใน agent panel เลย

ถ้าคุณต้องการ workflow ที่เข้มแบบมี custom agents และ stop hooks เพิ่มเติม ให้ใช้ repo เดียวกันนี้เปิดใน `VS Code` ได้ด้วย แต่โหมดหลักของโปรเจ็กต์นี้ยังเป็น `Zed`

## 1. Zed: เพิ่ม model provider

ไปที่ user settings ของ Zed แล้วเพิ่มประมาณนี้ ถ้าคุณจะใช้ทั้ง backend ที่นิ่งกว่าและ `Gemma4 E4B` ใน workspace เดียว:

```json
{
  "language_models": {
    "openai_compatible": {
      "OpenAI Stable MCP": {
        "api_url": "https://api.openai.com/v1",
        "available_models": [
          {
            "name": "gpt-5.4-mini",
            "display_name": "GPT-5.4 mini Stable MCP",
            "max_tokens": 128000,
            "max_output_tokens": 8192,
            "capabilities": {
              "tools": true,
              "images": false,
              "parallel_tool_calls": true,
              "prompt_cache_key": true,
              "chat_completions": true
            }
          }
        ]
      },
      "Local llama.cpp MCP": {
        "api_url": "http://127.0.0.1:8080/v1",
        "available_models": [
          {
            "name": "Gemma4-E4B-it-GGUF",
            "display_name": "Gemma4 E4B MCP Lite",
            "max_tokens": 12288,
            "max_output_tokens": 2048,
            "capabilities": {
              "tools": true,
              "images": false,
              "parallel_tool_calls": false,
              "prompt_cache_key": false,
              "chat_completions": true
            }
          }
        ]
      },
      "Local llama.cpp Fast": {
        "api_url": "http://127.0.0.1:8080/v1",
        "available_models": [
          {
            "name": "Gemma4-E4B-it-GGUF",
            "display_name": "Gemma4 E4B Fast",
            "max_tokens": 16384,
            "max_output_tokens": 2048,
            "capabilities": {
              "tools": false,
              "images": false,
              "parallel_tool_calls": false,
              "prompt_cache_key": false,
              "chat_completions": true
            }
          }
        ]
      }
    }
  }
}
```

จากนั้นเปิด Agent Panel แล้วเลือกตามงาน:

- `GPT-5.4 mini Stable MCP`
  ใช้เป็น backend หลักสำหรับ MCP/tool use จริง ถ้าคุณต้องการ capability ครบทุกอันยกเว้นรูปแบบรองรับจริง
- `Gemma4 E4B Fast`
  ใช้คุย, สรุป, วางแผน, หรือร่างคำตอบแบบไม่ต้องพึ่ง tools
- `Gemma4 E4B MCP Lite`
  ใช้กับ MCP/tool use แบบเบาและสั้น เช่นอ่าน tree, ค้นโค้ด, อ่านไฟล์ทีละช่วง, รัน command เดียว

ถ้าจะใช้ `Gemma4 E4B` ให้เสถียรที่สุดใน Zed:

- ใช้ profile `Ask` ก่อน `Write`
- สั่งงานสั้นและทำทีละอย่าง
- ให้มันใช้ tool ทีละตัว
- ถ้ามันเริ่มพ่น JSON tool call ดิบ ให้หยุด thread นั้นแล้วสลับไป stack ที่นิ่งกว่า

ถ้าใช้ Apple Silicon 16 GB แบบ M2/M3 ให้เริ่มด้วย `Q4_K_M` และ `LLAMA_CONTEXT_SIZE=16384` ก่อน ถ้าต้องการความเร็วขึ้นค่อยลดเป็น `8192` และถ้าต้องการ context เพิ่มค่อยขยับเป็น `24576` หรือ `32768`

สำคัญ:

- ค่า `max_tokens` ใน Zed ควรเท่ากับหรือต่ำกว่า `LLAMA_CONTEXT_SIZE` ของ server ที่รันอยู่
- สำหรับ `Gemma4 E4B MCP Lite` ผมแนะนำให้ Zed อยู่ที่ `12288` แม้ server จะรัน `16384` เพื่อเหลือ headroom สำหรับ system prompt, tool schema, และผลลัพธ์
- `Gemma4 E4B` ยังไม่ใช่โมเดลที่นิ่งพอสำหรับ heavy tool orchestration แบบยาวหลายขั้น
- ในสแตก `llama.cpp + local Gemma4` นี้ ให้เปิดจริงแค่ `tools` กับ `chat_completions` และปิด `images`
- อย่าเปิด `parallel_tool_calls` หรือ `prompt_cache_key` เพื่อหลอก Zed ว่ารองรับ ถ้าสแตกปลายทางยังไม่รองรับ parameter นั้นจริง
- ถ้าคุณต้องการ `tools + parallel_tool_calls + prompt_cache_key + /chat/completions` แบบรองรับจริง ให้ใช้ `OpenAI Stable MCP`
- provider ชื่อนี้จะอ่าน API key จาก env var `OPENAI_STABLE_MCP_API_KEY`

ถ้าต้องการใช้งานรูปภาพด้วย ให้เพิ่ม vision provider อีกตัว:

```json
{
  "language_models": {
    "openai_compatible": {
      "Local vLLM Vision": {
        "api_url": "http://127.0.0.1:8081/v1",
        "available_models": [
          {
            "name": "Qwen3-VL-2B-Instruct",
            "display_name": "Qwen3-VL-2B Vision Local",
            "max_tokens": 8192,
            "max_output_tokens": 1024,
            "capabilities": {
              "tools": false,
              "images": true,
              "parallel_tool_calls": false,
              "prompt_cache_key": false
            }
          }
        ]
      }
    }
  }
}
```

ใช้ตัวนี้เฉพาะตอนที่ต้องแนบภาพหรือ screenshot แล้วค่อยสลับกลับไป coder model ตอนจะลงมือแก้ repo

## 2. Zed: เพิ่ม MCP server

repo นี้มี `.zed/settings.json` ให้แล้ว ถ้า Zed ยังไม่เห็น server:

1. เปิด `agent: open settings`
2. กด `Add Custom Server`
3. ใช้ค่าเดียวกับใน `.zed/settings.json`

ถ้าจะใช้ `./scripts/run_agent_server.sh` แบบ relative path ให้ใส่ไว้ใน workspace file ของโปรเจ็กต์นี้คือ `.zed/settings.json` จะชัวร์ที่สุด เพราะ path จะอิง repo root โดยตรง

ถ้า Zed เห็นชื่อ server แล้วแต่เปิดไม่ขึ้น:

- ตรวจว่า `uv --directory ./apps/agent-server sync --extra dev` รันจบแล้ว
- ลองปิดแล้วเปิด Zed ใหม่หนึ่งรอบ เพื่อให้มันโหลด script ล่าสุด
- ถ้าเครื่องติดตั้ง `uv` ไว้นอก path ปกติ ให้เพิ่ม `env` ตอน add server เช่น:

```json
{
  "localCodingAgent": {
    "command": "bash",
    "args": ["./scripts/run_agent_server.sh"],
    "env": {
      "UV_BIN": "/home/<user>/.local/bin/uv"
    }
  }
}
```

path จริงของ `uv` ดูได้จาก `command -v uv` ใน terminal

## 2.1 Zed: stack ที่นิ่งกว่าสำหรับ MCP/tool use จริง

ถ้าคุณต้องการ workflow ที่นิ่งกว่า `4B` สำหรับแก้โค้ดจริง, รัน tests, และใช้ MCP หนัก ๆ ให้แยก role แบบนี้:

- `Gemma4 E4B Fast` ใช้คุย, สรุป, และร่างทางเลือก
- `GPT-5.4 mini Stable MCP` ใช้เป็นตัวหลักสำหรับ MCP/tool use จริง

สรุปตรง ๆ:

- `4B` เหมาะกับ lightweight assistance
- งาน MCP/tool use จริงให้ใช้ `GPT-5.4 mini Stable MCP`
- MCP server ไม่ต้องเปลี่ยน แค่เปลี่ยน agent/model ที่เรียกมัน

ถ้าคุณมี `Codex CLI` อยู่แล้วใน Zed นั่นก็ยังเป็น stack ที่นิ่งมากเช่นกัน แต่ถ้าคุณต้องการให้ capability ของ native provider ครบจริงใน Zed ให้ใช้ `OpenAI Stable MCP`

## 2.2 Zed: ตั้งค่า API key สำหรับ OpenAI Stable MCP

ตั้ง env var นี้ใน shell config ของคุณ:

```bash
export OPENAI_STABLE_MCP_API_KEY="YOUR_OPENAI_API_KEY"
```

ถ้าใช้หลาย workspace ให้ใส่ไว้ใน `~/.zshrc` หรือ `~/.bashrc` หนึ่งครั้ง แล้วทุก workspace ที่ใช้ template นี้จะเห็น provider เดียวกัน

## 2.3 เริ่มโปรเจ็กต์ใหม่บน Desktop แบบนิ่งกว่าเปิด Zed เปล่า ๆ

ถ้าคุณอยากสั่งให้ agent สร้างโปรเจ็กต์ใหม่บน `Desktop` ให้ใช้ workflow นี้แทนการเปิด Zed แบบไม่มี workspace:

```bash
bash ./scripts/new_desktop_workspace.sh my-new-app
```

สิ่งที่สคริปต์นี้ทำ:

- สร้างโฟลเดอร์ `~/Desktop/my-new-app`
- bootstrap กฎและ editor config ลงไปทันที
- พยายามเปิดโฟลเดอร์นั้นใน Zed ให้เลย

หลังจาก Zed เปิดโฟลเดอร์ใหม่แล้ว ค่อยสั่ง:

```text
สร้างเว็บหรือแอปให้เลยใน workspace นี้ แล้วรันให้ดูเมื่อพร้อม
```

ถ้าใช้วิธีนี้ agent จะเห็น workspace, rules, MCP server, และ provider config ตั้งแต่ต้น จึงนิ่งกว่าการเริ่มจากหน้าว่างแล้วค่อยบอก path ปลายทาง

## 3. Zed: project rules

repo นี้มีไฟล์ `.rules` ที่ตั้งใจให้เป็น always-on behavior ของ agent เช่น:

- คิด verification step ก่อนแก้
- rerun test เมื่อมีการแก้โค้ด
- ถ้า fail ให้ย้อนกลับไปแก้ที่ root cause
- งาน frontend ต้องนับ UX/UI เป็นส่วนหนึ่งของ definition of done
- ระหว่างงานหลายขั้นต้องรายงานสั้น ๆ ว่ากำลังทำอะไรอยู่

ถ้าต้องการ strict workflow ใน Zed ให้กำชับ agent ให้ใช้ MCP tools เหล่านี้เป็นชุดมาตรฐาน:

- `workspace_summary`
- `search_code`
- `read_text_file`
- `suggest_quality_gate_commands`
- `run_quality_gates`

ถ้าต้องการปรับนิสัย agent ใน Zed ให้แก้ที่ `.rules` เป็นหลัก

## 4. Zed: MCP prompts และ resources ที่เพิ่มไว้

repo นี้มี MCP prompts/resources สำหรับช่วยคุมมาตรฐานงานเพิ่มแล้ว:

- `workflow://senior-delivery-guide`
- `workflow://quality-gates`
- `workflow://delivery-quality`
- `design://frontend-quality-guide`
- `workflow://vision-workflow-guide`
- `senior_delivery_prompt`
- `quality_gate_prompt`
- `repair_loop_prompt`
- `frontend_polish_prompt`
- `ui_reference_prompt`
- `screenshot_debug_prompt`

ใช้สิ่งเหล่านี้เมื่ออยากบังคับแนวคิด senior-style ให้ชัดขึ้นระหว่างงานใน Zed

## 5. VS Code: ใช้ MCP config จาก workspace

เปิด Command Palette แล้วใช้:

- `MCP: Open Workspace Folder MCP Configuration`
- ตรวจว่าโหลด `.vscode/mcp.json` แล้ว

ถ้า server ยังไม่ start:

- `MCP: List Servers`
- start `localCodingAgent`

## 6. VS Code: always-on instructions, custom agents, และ hooks

repo นี้เพิ่มไฟล์ให้ VS Code ใช้แล้ว:

- `.github/copilot-instructions.md`
- `.github/instructions/testing.instructions.md`
- `.github/instructions/frontend.instructions.md`
- `.github/prompts/test-repair-loop.prompt.md`
- `.github/prompts/frontend-polish.prompt.md`
- `.github/agents/*.agent.md`
- `.github/hooks/session-context.json`
- `.vscode/settings.json`

ตัวแรกเป็น always-on instructions ทั้ง workspace ส่วน `.instructions.md` จะช่วยเสริมตามชนิดไฟล์ และ `.prompt.md` จะเรียกใช้ผ่าน `/test-repair-loop` หรือ `/frontend-polish`

custom agents ที่เพิ่มมา:

- `Senior Delivery`
- `Senior Planner`
- `Senior Implementer`
- `Senior Reviewer`
- `Frontend Polisher`

ถ้าต้องการ workflow ที่เข้มที่สุดใน VS Code ให้เริ่มจาก `Senior Delivery`

## 7. ถ้าต้องการให้ VS Code ใช้ local model ด้วย

แนวทางที่เรียบที่สุดคือใช้ extension หรือ agent client ที่รับ OpenAI-compatible endpoint ได้ แล้วชี้ไปที่:

```text
http://127.0.0.1:8080/v1
```

โมเดลที่ใช้:

```text
Gemma4-E4B-it-GGUF
```

repo นี้ตั้งใจแยกส่วน model serving ออกจาก MCP เพื่อให้ใช้ editor ได้หลายตัวโดยไม่ล็อกกับ vendor เดียว

## 8. ใช้ข้ามหลาย workspace

ถ้าจะใช้ `localCodingAgent` กับ workspace อื่นด้วย ไม่จำเป็นต้องผูกกับ script ใน repo นี้ทุกครั้ง

แนวที่แนะนำคือ:

1. ติดตั้ง MCP command แบบ global หนึ่งครั้ง
```bash
bash ./scripts/install_global_agent.sh
```
2. ใน Zed หรือ VS Code ของ workspace อื่น ให้เรียก command ชื่อ `local-coding-agent`
3. ถ้าจะ bootstrap workspace ใหม่แบบเร็ว ให้ใช้
```bash
bash ./scripts/bootstrap_workspace.sh /absolute/path/to/other-workspace
```

คำสั่งนี้จะคัดลอกไฟล์ตั้งต้นไปให้:

- `AGENTS.md`
- `.rules`
- `.zed/settings.json`
- `.vscode/mcp.json`

MCP command แบบ global จะใช้ workspace ปัจจุบันเป็นฐาน และถ้า editor เปิดจาก subdirectory มันจะพยายามหา root ของโปรเจ็กต์จาก marker เช่น `.git`, `pyproject.toml`, `package.json`, `.zed`, `.vscode`

## 9. Local vision sidecar

ถ้าต้องการให้ editor รับรูปภาพด้วย:

1. รัน `bash ./scripts/setup_vision_stack.sh`
2. รัน `bash ./scripts/run_vision_server.sh`
3. เพิ่ม vision provider snippet ด้านบน
4. ใช้โมเดล vision ตอนแนบรูป และกลับมาใช้ coder model ตอนจะลงมือแก้โค้ด
