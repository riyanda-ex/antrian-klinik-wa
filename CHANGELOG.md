# Changelog

## [2.0.0] - 2026-11-11
### Added
- Validasi nama, HP, poli (whitelist)
- Masking nomor HP di UI & API
- Kuota 100 antrean/hari, reset otomatis ganti hari
- Estimasi tunggu transparan (10 menit / pasien)
- Health check `GET /health`
- 10 test otomatis + CI GitHub Actions
- SECURITY, CONTRIBUTING, .gitignore

### Security
- Tanpa token / secret di kode
- API tidak mengembalikan nomor HP asli
- `debug=False`, tanpa `eval()` / `exec()`

## [1.0.0] - 2026-11-10
- Versi awal: ide antrean klinik via WA
