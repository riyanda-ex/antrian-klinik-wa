"""
Antrian Klinik WA - Versi 2.0.0 Production Safe

Sistem antrean klinik via WhatsApp (SIMULASI).
Bukan integrasi WhatsApp asli - untuk demo edukasi.

Keamanan:
- TIDAK ada token / API key di kode
- TIDAK menyimpan NIK / nama lengkap / rekam medis
- Nomor HP dimasking (08xx****1234) di log
- Input dibatasi & divalidasi
- TIDAK ada eval() / exec()

Cara jalanin:
  pip install -r requirements.txt
  python main.py
  Buka: http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime, date
import re
import html
import threading

app = Flask(__name__)

# ================= KONFIGURASI =================
MAX_NAMA_PANJANG = 50
MAX_PESAN_PANJANG = 500
MAX_ANTRIAN_PER_HARI = 100
LOKET_BUKA_JAM = 8
LOKET_TUTUP_JAM = 16

# Data in-memory. Reset tiap restart. Untuk produksi, ganti ke database.
_lock = threading.Lock()
_antrian = []  # list dict: {nomor, nama_samaran, poli, waktu_daftar, status, estimasi_menit}
_counter = {"nomor": 0}

POLI_VALID = ["UMUM", "GIGI", "ANAK", "LANSIA", "KIA"]

def mask_hp(no_hp: str) -> str:
    """08xxxxxxxxxx -> 08xx****xxxx. Jangan tampilkan nomor full di log/UI."""
    no_hp = re.sub(r"\D", "", no_hp or "")
    if len(no_hp) < 8:
        return "****"
    return f"{no_hp[:4]}****{no_hp[-4:]}"

def bersihkan(teks) -> str:
    if not isinstance(teks, str):
        return ""
    return html.escape(teks.strip()[:MAX_PESAN_PANJANG])

def validasi_nama(nama: str) -> bool:
    nama = (nama or "").strip()
    if not nama or len(nama) > MAX_NAMA_PANJANG:
        return False
    # Hanya huruf, spasi, titik, strip. Tolak angka & simbol aneh.
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ .'-]+", nama))

def validasi_hp(no_hp: str) -> bool:
    no_hp = re.sub(r"\D", "", no_hp or "")
    # Format Indonesia: 08... (10-13 digit) atau 62... (11-14 digit)
    return bool(re.fullmatch(r"(08\d{8,11}|62\d{9,12})", no_hp))

def validasi_poli(poli: str) -> bool:
    return (poli or "").strip().upper() in POLI_VALID

def reset_harian_jika_beda_hari():
    """Antrian reset otomatis kalau sudah ganti hari."""
    today = date.today().isoformat()
    if _antrian and _antrian[0].get("tanggal") != today:
        _antrian.clear()
        _counter["nomor"] = 0

def estimasi_menit(posisi: int) -> int:
    # Asumsi 1 pasien = 10 menit. Transparan & mudah dijelaskan.
    return posisi * 10

def daftar_antrian(nama: str, no_hp: str, poli: str):
    """Daftarkan antrean. Return (sukses, data/error)."""
    with _lock:
        reset_harian_jika_beda_hari()
        if len(_antrian) >= MAX_ANTRIAN_PER_HARI:
            return False, "Kuota antrean hari ini penuh (100). Silakan datang besok."
        _counter["nomor"] += 1
        nomor = _counter["nomor"]
        item = {
            "nomor": nomor,
            "nama_samaran": nama.strip().title(),
            "poli": poli.strip().upper(),
            "tanggal": date.today().isoformat(),
            "waktu_daftar": datetime.now().strftime("%H:%M:%S"),
            "status": "MENUNGGU",
            "estimasi_menit": estimasi_menit(len(_antrian)),
            "hp_mask": mask_hp(no_hp),
        }
        _antrian.append(item)
        return True, item

def format_balasan_wa(item: dict) -> str:
    return (
        f"Halo {item['nama_samaran']}, pendaftaran berhasil!\n"
        f"Nomor antrean: {item['nomor']} - Poli {item['poli']}\n"
        f"Waktu daftar: {item['waktu_daftar']} WIB\n"
        f"Estimasi tunggu: ~{item['estimasi_menit']} menit\n"
        f"Jangan kirim NIK / No. BPJS via chat. Bawa KTP saat datang.\n"
        f"Ini demo edukasi, bukan pengganti pendaftaran resmi."
    )

# ================= UI =================
HTML = """
<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Antrian Klinik WA</title>
<style>body{font-family:system-ui;max-width:640px;margin:32px auto;padding:0 16px}
input,select{width:100%;padding:10px;margin:6px 0}button{padding:10px 16px}
.card{border:1px solid #ddd;border-radius:12px;padding:16px;margin:12px 0}
small{color:#666}</style></head><body>
<h2>Antrian Klinik WA (Simulasi)</h2>
<p><small>Demo edukasi. Jangan kirim NIK / No. BPJS. Nomor HP ditampilkan termasking.</small></p>
<div class="card"><h3>Ambil Nomor Antrean</h3>
<input id="nama" placeholder="Nama samaran (huruf saja)" maxlength="50">
<input id="hp" placeholder="No. HP, contoh 081234567890" maxlength="14">
<select id="poli"><option>UMUM</option><option>GIGI</option><option>ANAK</option><option>LANSIA</option><option>KIA</option></select>
<button onclick="daftar()">Daftar</button><p id="hasil"></p></div>
<div class="card"><h3>Antrean Hari Ini</h3><button onclick="muat()">Refresh</button><div id="list"></div></div>
<script>
async function daftar(){
  const body={nama:document.getElementById('nama').value, no_hp:document.getElementById('hp').value, poli:document.getElementById('poli').value};
  const r=await fetch('/api/daftar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const d=await r.json();
  document.getElementById('hasil').innerText = d.balasan_wa || d.error || 'Gagal';
  muat();
}
async function muat(){
  const r=await fetch('/api/antrian'); const d=await r.json();
  document.getElementById('list').innerHTML = d.antrian.map(a=>`<p><b>#${a.nomor}</b> ${a.nama_samaran} - ${a.poli} - ${a.status} - ~${a.estimasi_menit} mnt - ${a.hp_mask}</p>`).join('') || '<p>Belum ada antrean.</p>';
}
muat();
</script></body></html>
"""

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "antrian-klinik-wa", "version": "2.0.0"}), 200

@app.route("/api/daftar", methods=["POST"])
def api_daftar():
    if not request.is_json:
        return jsonify({"error": "Content-Type harus application/json"}), 400
    data = request.get_json(silent=True) or {}
    nama = bersihkan(data.get("nama", ""))
    no_hp = bersihkan(data.get("no_hp", ""))
    poli = bersihkan(data.get("poli", ""))

    if not validasi_nama(nama):
        return jsonify({"error": "Nama tidak valid. Hanya huruf, maks 50 karakter."}), 400
    if not validasi_hp(no_hp):
        return jsonify({"error": "No. HP tidak valid. Contoh: 081234567890"}), 400
    if not validasi_poli(poli):
        return jsonify({"error": f"Poli tidak valid. Pilihan: {', '.join(POLI_VALID)}"}), 400

    sukses, hasil = daftar_antrian(nama, no_hp, poli)
    if not sukses:
        return jsonify({"error": hasil}), 409
    return jsonify({"nomor": hasil["nomor"], "estimasi_menit": hasil["estimasi_menit"], "balasan_wa": format_balasan_wa(hasil)}), 201

@app.route("/api/antrian", methods=["GET"])
def api_antrian():
    with _lock:
        reset_harian_jika_beda_hari()
        # Jangan kirim nomor HP asli ke frontend, hanya yang termasking
        data = [{"nomor": a["nomor"], "nama_samaran": a["nama_samaran"], "poli": a["poli"], "status": a["status"], "estimasi_menit": a["estimasi_menit"], "hp_mask": a["hp_mask"]} for a in _antrian]
    return jsonify({"tanggal": date.today().isoformat(), "total": len(data), "antrian": data}), 200

@app.errorhandler(404)
def nf(e):
    return jsonify({"error": "Endpoint tidak ditemukan"}), 404

@app.errorhandler(500)
def se(e):
    return jsonify({"error": "Terjadi gangguan server"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
