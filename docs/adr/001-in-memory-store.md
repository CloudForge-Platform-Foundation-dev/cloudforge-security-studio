# ADR-001: ใช้ in-memory store ใน MVP

**สถานะ:** Accepted  
**วันที่:** 2026-09-30

## บริบท
MVP ของ Security Studio ต้องรับ event และแสดง finding ให้ครบวงจรในรอบเดียว
ยังไม่มีข้อกำหนดเรื่อง retention หรือ query ที่ซับซ้อน

## การตัดสินใจ
เก็บ event และ finding ในหน่วยความจำ (`src/store.py`) ป้องกัน race ด้วย lock
และกัน eventId ซ้ำ (409)

## ผลที่ตามมา
- ข้อมูลหายเมื่อ restart และใช้หลาย instance พร้อมกันไม่ได้
- **ขัดกับ security baseline** ของ Foundation (log ต้องเก็บ ≥ 1 ปี) ถ้านำไปใช้ production
  ต้องเปลี่ยนเป็น DB ก่อน โดยคง interface ของ `EventStore` ไว้
- ทดสอบง่าย ไม่มี infrastructure เพิ่ม

## ไม่ทำในรอบนี้
- Trivy ใน CI ตรวจ repo นี้เอง ไม่ใช่ฟีเจอร์ของแอป
- ตรวจผลสแกนตามนโยบาย `.rego` ต้องรันผ่าน OPA ด้วยไฟล์ policy ของ Foundation ไม่เขียนกฎซ้ำใน Python
- Hybrid Security analyst agent (reasoning trace, human-in-the-loop)
