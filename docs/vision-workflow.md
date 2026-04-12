# Vision Workflow

repo นี้เพิ่มเส้นทาง local vision sidecar สำหรับงานที่ต้องดูภาพ เช่น:

- ดู reference UI แล้วสรุป visual system
- ดู screenshot error แล้วช่วย debug
- ดู mockup แล้วแปลงเป็น component/layout plan
- อ่าน text จาก screenshot หรือ panel UI ที่ copy ออกมาตรง ๆ ลำบาก

## แนะนำโมเดล

ค่าเริ่มต้นใน repo นี้ใช้:

- `Qwen/Qwen3-VL-2B-Instruct`

เหตุผล:

- เป็น official Qwen vision-language model ที่เบากว่า 3B
- model card ระบุชัดว่าเด่นเรื่อง visual agent, UI, OCR, และ GUI interaction
- เหมาะกว่าการเอา coder model ไปแบกงานรูปภาพ

ถ้าอยากใช้รุ่นที่มี docs ฝั่ง Qwen2.5-VL ชัดกว่า:

- `Qwen/Qwen2.5-VL-3B-Instruct`

## แนะนำ workflow ใน Zed

### กรณี 1: คุณมีรูป UI reference

1. เลือกโมเดล vision
2. แนบรูป
3. ให้มันสรุป:
   - layout
   - spacing rhythm
   - typography hierarchy
   - color system
   - interaction cues
4. สลับกลับไป coder model
5. ให้ coder model ลงมือแก้ repo โดยใช้ MCP tools และ quality gates

### กรณี 2: คุณมี screenshot error

1. เลือกโมเดล vision
2. แนบ screenshot
3. ให้มันสกัด:
   - error message
   - file path
   - line number
   - likely root cause
4. สลับกลับไป coder model
5. ให้ coder model อ่านไฟล์จริงใน repo และ repair loop ต่อ

## Prompt ที่แนะนำ

### UI reference

```text
Analyze this interface as a senior product designer and frontend engineer.
Describe the layout structure, spacing scale, typography hierarchy, component system, visual hierarchy, and interaction cues.
Then produce a concise build brief that a coding model can use to recreate the same direction in code.
```

### Screenshot error

```text
Read this screenshot carefully.
Extract the exact error text, file paths, line numbers, and the likely root cause.
Then suggest a minimal debugging plan for a coding model that has access to the repository.
```

## Local serving path

repo นี้ใช้ `vLLM` สำหรับ vision sidecar เพราะ:

- Qwen แนะนำ `vLLM` สำหรับ deployment
- `vLLM` เสิร์ฟ OpenAI-compatible API ได้
- docs ของ `vLLM` รองรับ image inputs ผ่าน Chat Completions API

## ข้อจำกัดที่ควรรู้

- งาน “ลอกหน้าตาให้เหมือนเป๊ะทุก pixel” ยังไม่ควรคาดหวังจาก local 2B vision model
- ภาพ UI ที่รกมากควร crop เป็นส่วน ๆ เพื่อให้ผลดีกว่า
- ถ้าจะให้วิเคราะห์ error จาก screenshot ควรแนบภาพชัดและไม่ย่อมากเกินไป
- vision model ควรใช้เพื่อ “วิเคราะห์ภาพ” แล้วส่งงานต่อให้ coder model แก้ repo จริง
