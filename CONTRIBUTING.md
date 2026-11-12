# Contributing

## Aturan Utama
1. Jangan kirim data pasien asli & token WhatsApp
2. Semua perubahan wajib lolos: `python -m pytest test_main.py -v`
3. Nomor HP baru wajib dimasking, jangan tampilkan full

## Cara Kontribusi
1. Fork > buat branch `fix/nama-perbaikan`
2. Jalankan test sebelum commit
3. Buat Pull Request dengan deskripsi jelas

## Standar Kode
- Python 3.12, gaya kode ikuti `main.py`
- Poli baru wajib masuk whitelist `POLI_VALID`
- Jangan pakai `eval()` / `exec()` / `debug=True`
