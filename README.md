# Antrian Klinik WA

[![Tests](https://github.com/riyanda-ex/antrian-klinik-wa/actions/workflows/tests.yml/badge.svg)](https://github.com/riyanda-ex/antrian-klinik-wa/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/riyanda-ex/antrian-klinik-wa/blob/main/LICENSE)

Pasien tidak perlu lagi menunggu 4 jam di klinik. Ambil nomor antrean dari HP, lihat estimasi tunggu, datang saat giliran hampir tiba.

> ⚠️ **Simulasi edukasi.** Bukan integrasi WhatsApp resmi & bukan pendaftaran resmi klinik. Jangan kirim NIK / No. BPJS.

## Fitur

- Ambil nomor antrean otomatis & urut
- Estimasi tunggu transparan (10 menit / pasien)
- Validasi nama, HP Indonesia, poli (whitelist)
- Nomor HP dimasking, API tidak bocorkan nomor asli
- Kuota 100 / hari, reset otomatis ganti hari
- 10 test otomatis + CI GitHub Actions

## Cara Jalanin

```bash
pip install -r requirements.txt
python main.py
# Buka: http://127.0.0.1:5000
