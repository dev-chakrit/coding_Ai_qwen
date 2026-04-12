# Frontend Standards

เอกสารนี้ใช้เป็น baseline สำหรับงาน UI/UX ใน repo นี้

## 1. Layout and spacing

- ใช้ spacing scale ที่สม่ำเสมอ เช่น `4, 8, 12, 16, 24, 32, 48, 64`
- ระยะห่างที่เหมือนหน้าที่กันควรเท่ากัน
- จัดกลุ่ม content ด้วย whitespace แทนเส้นคั่นพร่ำเพรื่อ
- ให้ขอบซ้าย ขวา และ baseline ของ element จัดแนวกัน

## 2. Typography

- ต้องมี hierarchy ชัดเจนระหว่าง heading, subheading, body, meta text
- ขนาดตัวอักษร, line-height, weight, และ letter spacing ต้องทำงานร่วมกัน ไม่ใช่ปรับทีละค่าแบบสุ่ม
- อย่าใช้ font หลายตระกูลโดยไม่มีเหตุผล
- text ยาวต้องอ่านสบาย ทั้งบนมือถือและ desktop

## 3. Visual hierarchy

- จุดสำคัญที่สุดของหน้าต้องเด่นสุดด้วยขนาด ตำแหน่ง น้ำหนัก หรือ contrast
- action หลักต้องมองออกภายในไม่กี่วินาที
- card, panel, section ต้องมีลำดับชั้นชัด ไม่แบนไปทั้งหน้า

## 4. Interaction states

- ปุ่มและ input ต้องมีอย่างน้อย default, hover, focus, disabled
- flow ที่ async ควรมี loading state
- flow ที่ fail ควรมี error state ที่อ่านแล้วรู้ว่าต้องทำอะไรต่อ
- ถ้ามี empty state ควรช่วยให้ผู้ใช้เริ่มต้นได้

## 5. Responsive behavior

- ออกแบบ mobile-first หรืออย่างน้อยต้องตรวจทั้งจอแคบและจอกว้าง
- หลีกเลี่ยง layout ที่พังเพราะ fixed width โดยไม่จำเป็น
- ระวัง text wrap, button overflow, card height mismatch, และ touch target ที่เล็กเกินไป

## 6. Accessibility

- contrast ต้องเพียงพอ
- keyboard focus ต้องมองเห็น
- อย่าใช้สีอย่างเดียวสื่อความหมาย
- label, helper text, error text ต้องสัมพันธ์กับ input

## 7. Design quality bar

งาน UI ที่ดีใน repo นี้ควร:

- ดูตั้งใจ ไม่เหมือน template สำเร็จรูปทั่ว ๆ ไป
- มี rhythm ของ spacing และ typography ที่สม่ำเสมอ
- อ่านง่าย ใช้ง่าย และ state ครบ
- มีรายละเอียดพอให้รู้สึก polished แม้จะเป็นหน้าธรรมดา
