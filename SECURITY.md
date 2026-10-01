# Security Policy

## รายงานช่องโหว่

หากพบช่องโหว่ใน CloudForge Security Studio กรุณาอย่าเปิด public issue
ให้ติดต่อเจ้าของ repo (ดู `CODEOWNERS`) แบบส่วนตัว พร้อมรายละเอียด:

- ขั้นตอนการ reproduce
- ผลกระทบที่คาดว่าจะเกิด
- เวอร์ชัน/commit ที่พบปัญหา

## เวอร์ชันที่ยังซัพพอร์ตอยู่

| เวอร์ชัน | ซัพพอร์ต |
|---|---|
| 0.1.x | ✅ |

## ขอบเขต

Studio นี้เป็น resource server — ตรวจ token จาก Identity Service ผ่าน `cloudforge-auth-core`
ห้าม commit credential ใด ๆ ลง repo ใช้ environment variable เท่านั้น (ดู `.env.example`)
