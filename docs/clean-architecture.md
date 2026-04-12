# Clean Architecture Baseline

repo นี้ใช้กติกาง่าย ๆ เพื่อให้ agent พัฒนาโค้ดต่อได้โดยไม่มั่ว layer:

## 1. Dependency Direction

dependency ต้องไหลเข้าด้านในเสมอ:

- `presentation -> application -> domain`
- `infrastructure -> application -> domain`
- `domain` ห้ามรู้จัก framework, database, HTTP, editor API

## 2. ความรับผิดชอบของแต่ละ layer

### `domain`

- entity
- value object
- domain rule
- repository contract

### `application`

- use case
- orchestration logic
- input/output model
- transaction boundary

### `infrastructure`

- database implementation
- file system adapter
- LLM adapter
- external API adapter

### `presentation`

- CLI contract
- HTTP DTO
- editor-facing payload
- serialization layer

## 3. กติกาการเพิ่ม feature ใหม่

ทุก feature ใหม่ควรเป็น slice ของตัวเอง เช่น:

```text
src/billing/
  domain/
  application/
  infrastructure/
  presentation/
```

## 4. กติกาการเขียน agent-friendly code

- ชื่อไฟล์และชื่อคลาสต้องสื่อหน้าที่ตรง ๆ
- use case หนึ่งไฟล์ควรมี responsibility ชัดเจน
- หลีกเลี่ยง utility กลางแบบกว้างเกินไป
- ถ้าต้องพึ่ง framework ให้เก็บไว้ใน infrastructure หรือ presentation
- ถ้าไฟล์เริ่มทำหลายอย่างเกินไป ให้แยกก่อนเพิ่ม feature ใหม่
