# Security Policy

## Dilarang
Jangan kirim di repo / issue / PR:
- Nama lengkap pasien, NIK, No. BPJS, No. RM
- Token WhatsApp / API key / password
- Rekam medis asli

## Yang Sudah Diamankan
- Tidak ada token / secret di kode
- Nomor HP dimasking di UI & API (`08xx****xxxx`)
- API antrean tidak mengembalikan nomor HP asli
- Validasi nama (huruf saja), HP (format Indonesia), poli (whitelist)
- Input dibatasi & di-escape, tanpa `eval()` / `exec()`
- `debug=False` di produksi

## Melaporkan Celah
Jangan buat Issue publik. Hubungi pemilik repo via GitHub DM / email di profil.

## Disclaimer
Ini SIMULASI edukasi, bukan integrasi WhatsApp resmi & bukan pendaftaran resmi klinik.
