# Editor Setup

## แนะนำให้เริ่มด้วย Zed

stack นี้เหมาะกับ `Zed + llama.cpp + MCP` มากที่สุด เพราะ Zed ต่อ OpenAI-compatible local endpoint ได้ตรง และใช้ MCP tools ได้ใน agent panel เลย

ถ้าคุณต้องการ workflow ที่เข้มแบบมี custom agents และ stop hooks เพิ่มเติม ให้ใช้ repo เดียวกันนี้เปิดใน `VS Code` ได้ด้วย แต่โหมดหลักของโปรเจ็กต์นี้ยังเป็น `Zed`

## 1. Zed: เพิ่ม local model provider

ไปที่ user settings ของ Zed แล้วเพิ่มประมาณนี้:

```json
{
  "language_models": {
    "openai_compatible": {
      "Local llama.cpp": {
        "api_url": "http://127.0.0.1:8080/v1",
        "available_models": [
          {
            "name": "Qwen3-Coder-Next",
            "display_name": "Qwen3-Coder-Next Local",
            "max_tokens": 262144,
            "max_output_tokens": 8192,
            "capabilities": {
              "tools": true,
              "images": false,
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

จากนั้นเปิด Agent Panel แล้วเลือกโมเดล `Qwen3-Coder-Next Local`

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
Qwen3-Coder-Next
```

repo นี้ตั้งใจแยกส่วน model serving ออกจาก MCP เพื่อให้ใช้ editor ได้หลายตัวโดยไม่ล็อกกับ vendor เดียว

## 8. Local vision sidecar

ถ้าต้องการให้ editor รับรูปภาพด้วย:

1. รัน `bash ./scripts/setup_vision_stack.sh`
2. รัน `bash ./scripts/run_vision_server.sh`
3. เพิ่ม vision provider snippet ด้านบน
4. ใช้โมเดล vision ตอนแนบรูป และกลับมาใช้ coder model ตอนจะลงมือแก้โค้ด
