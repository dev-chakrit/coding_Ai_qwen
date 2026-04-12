# Quality Gates

repo นี้มีไฟล์ [quality-gates.json](../quality-gates.json) เป็น source of truth สำหรับ verification commands

## แนวคิด

- ระบุ command verification กลางไว้ที่เดียว
- ให้ทั้ง `Zed`, `VS Code`, และ shell script ใช้ชุดเดียวกัน
- ถ้างานแตะไฟล์กลุ่มไหน ให้เลือก command ตาม pattern ที่ match

## ใช้ใน Zed

ให้ agent เรียก MCP tools ต่อไปนี้:

- `get_quality_gates`
- `suggest_quality_gate_commands`
- `run_quality_gates`

workflow ที่แนะนำ:

1. อ่าน code และระบุไฟล์ที่จะกระทบ
2. เรียก `suggest_quality_gate_commands`
3. แก้โค้ด
4. เรียก `run_quality_gates`
5. ถ้า fail ให้ย้อนกลับไป repair loop

## ใช้ใน VS Code

VS Code custom agents และ hooks ใน repo นี้ใช้ `quality-gates.json` ไฟล์เดียวกัน

- `Senior Implementer`
- `Frontend Polisher`

ทั้งสองตัวมี stop hook ที่พยายามรัน quality gates ก่อนจบงาน

## ใช้จาก shell

```bash
bash ./scripts/run_quality_gates.sh
```

หรือเจาะไฟล์ที่เพิ่งแก้:

```bash
bash ./scripts/run_quality_gates.sh --files apps/agent-server/src/local_coding_agent/server.py
```
