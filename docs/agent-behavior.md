# Agent Behavior

เอกสารนี้กำหนดนิสัยการทำงานของ agent ใน workspace นี้

## 1. Test-first mindset

- ก่อนแก้ของที่ไม่เล็กมาก ให้หา verification step ที่เล็กและชัดที่สุดก่อน
- ถ้าบั๊กมีวิธี reproduce ชัดเจน ให้เพิ่มหรือแก้ regression test ก่อนถ้าทำได้
- ถ้าเป็นงาน prototype หรือเอกสารที่ไม่มี test ตรง ๆ ให้กำหนดวิธีตรวจสอบที่เหมาะสมแทน

## 2. Repair loop

เมื่อรันทดสอบแล้ว fail:

1. อ่าน failure output ให้ครบ
2. หา root cause แทนการเดา
3. แก้ให้ตรงสาเหตุ
4. rerun เฉพาะ check ที่เกี่ยวก่อน
5. ถ้าผ่านแล้วค่อยขยายไปยัง check ที่กว้างขึ้น

ห้ามหยุดที่ patch แรกถ้ายัง fail อยู่

## 3. สิ่งที่ไม่ถือว่าเป็น fix ที่ดี

- ปิด test ทิ้ง
- ลด assertion เพื่อให้ผ่าน
- ใส่ try/except กว้างเกินไป
- ซ่อน error ด้วย fallback ที่ไม่แก้ต้นเหตุ
- hardcode หรือ magic number โดยไม่มีเหตุผล
- ใส่ CSS/JS workaround แบบเฉพาะจุดจนระบบอ่านยากขึ้น

## 4. Definition of done

งานหนึ่งชิ้นควรถือว่าเสร็จเมื่อ:

- โค้ดตรงตามเป้าหมาย
- test หรือ verification ที่เกี่ยวผ่าน
- ไม่มี regression ที่รู้ชัดค้างอยู่
- สรุปได้ว่า verify อะไรไปแล้ว และยัง verify อะไรไม่ได้

## 5. Progress visibility

ระหว่างงานที่มีหลายขั้น:

- ควรบอกสั้น ๆ ว่าตอนนี้กำลังตรวจอะไรหรือแก้อะไร
- ถ้ามีเหตุผลสำคัญ เช่น test fail หรือเจอ blocker ควรบอกทันที
- ควรบอก next step แบบสั้น ๆ เพื่อให้ผู้ใช้รู้ว่างานยังเดินอยู่

## 6. Frontend-specific bar

งาน frontend ถือว่าไม่เสร็จ ถ้าแม้ฟังก์ชันทำงานแล้วแต่:

- spacing ยังมั่ว
- typography ไม่มี hierarchy
- layout แน่นหรือโปร่งผิดจังหวะ
- responsive แตกบนมือถือหรือจอใหญ่
- state ต่าง ๆ เช่น hover, focus, error, loading ยังไม่ครบ

รายละเอียดเชิงออกแบบอยู่ที่ [frontend-standards.md](./frontend-standards.md)
