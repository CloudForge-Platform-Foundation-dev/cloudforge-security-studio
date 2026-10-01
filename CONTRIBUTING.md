# Contributing

## หลักการทั่วไป

- ห้าม push ตรงเข้า `main` เสมอ แม้จะมีสิทธิ์ admin ก็ตาม — เปิดเป็น PR แยก branch ทุกครั้ง
- ทุก PR ต้องผ่าน reusable CI gate (`foundation-validation`) ก่อน merge
- ตาม auth pattern มาตรฐานของแพลตฟอร์ม (`src/auth/`) ห้ามเบี่ยงเบน

## ขั้นตอนการ contribute

1. Fork หรือสร้าง branch ใหม่จาก `main`
2. เขียนโค้ด + test ให้ครอบคลุม
3. รัน test ในเครื่องให้ผ่านก่อน push: `pytest tests/`
4. เปิด PR พร้อมคำอธิบายว่าทำอะไร ทำไม
5. รอ CI ผ่าน + review ก่อน merge

## Coding standards

- Python: ตาม `engineering-standards` ใน Foundation repo
- ตั้งชื่อไฟล์/โฟลเดอร์ตาม naming convention ของแพลตฟอร์ม
- เขียนไฟล์ผ่าน editor ที่ระบุ encoding เป็น UTF-8 (ไม่มี BOM) เสมอ — ปัญหานี้เจอมาแล้วหลายรอบใน repo อื่นของแพลตฟอร์ม
