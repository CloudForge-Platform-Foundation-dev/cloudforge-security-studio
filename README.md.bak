# CloudForge Security Studio

> Studio สำหรับ security analysis และ compliance ของ CloudForge Platform — **MVP v0.1.0**

รับ canonical event จาก Studio อื่น, เก็บ security finding และให้ดูสรุป
ยืนยันตัวตนผ่าน `cloudforge-auth-core@v1.1.4` (Identity Contract v1) ห้าม implement JWT เองใน repo นี้

## Endpoints

| Method | Path | Scope | ผลลัพธ์ |
|--------|------|-------|---------|
| GET | `/health` | — | `200` |
| POST | `/events` | `security:write` | `202` รับแล้ว / `409` eventId ซ้ำ / `422` schema ไม่ตรง |
| GET | `/findings?severity=&limit=` | `security:read` | `200` รายการ + `countsBySeverity` |

ทุก endpoint ที่ต้อง auth: `401` token ไม่ถูกต้อง, `403` scope ไม่พอ, `503` JWKS ไม่พร้อม

`POST /events` รับ event ตาม `schemas/canonical/event.schema.json` ของ Foundation
ฟิลด์ `source` คือ Studio **ที่ส่ง** event (เช่น `ingest-studio`) ถ้า `eventType` เป็น `Finding.Created`
payload ต้องมี `severity` (`CRITICAL|HIGH|MEDIUM|LOW|INFO`) และ `title` ระบบจะสร้าง finding ให้

ตัวอย่าง:

```json
{
  "eventId": "3f0c2a4e-6d0a-4f6e-9a55-0c1f5d9e7b10",
  "eventType": "Finding.Created",
  "source": "ingest-studio",
  "timestamp": "2026-09-30T10:00:00Z",
  "payload": {"severity": "HIGH", "title": "Hardcoded password", "resource": "src/app.py"}
}
```

## รันในเครื่อง

```bash
cp .env.example .env
pip install -r requirements-dev.txt
pytest tests/ -v
uvicorn src.main:app --port 8003
```

หรือ `docker compose up --build` (พอร์ต 8003)

## ข้อจำกัดของ MVP

- ข้อมูลเก็บใน memory หายเมื่อ restart (ADR-001)
- ยังไม่มีการตรวจตาม policy `.rego` และ AI agent
- ชื่อ scope `security:read` / `security:write` ตั้งตามรูปแบบ `nova:query` — ตรวจให้ตรงกับ Identity Contract v1 ก่อนใช้จริง

## การตั้งค่า CI

- ตั้ง secret `FOUNDATION_PAT` ใน repo (governance-gate ต้องใช้)
- แก้ `CODEOWNERS`, อีเมลใน `openapi.yaml` และ `x-governance-id` (`CFG-SECURITY-001` เป็นค่าที่ตั้งเอง) ให้ตรงกับของจริง
