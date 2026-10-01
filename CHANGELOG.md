# Changelog

รูปแบบอ้างอิง [Keep a Changelog](https://keepachangelog.com/) และ [Semantic Versioning](https://semver.org/)

## [0.1.0] - 2026-09-30

### Added
- Scaffold ตาม Foundation Studio Contract (README, LICENSE, CHANGELOG, VERSION, `docs/adr/`)
- Auth ผ่าน `cloudforge-auth-core@v1.1.4` (scope `security:read`, `security:write`)
- `POST /events` (canonical event), `GET /findings`, `GET /health`
- CI: governance-gate + pytest, และ Trivy (`security-scan.yml`)
