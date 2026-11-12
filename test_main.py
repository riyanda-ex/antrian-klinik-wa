"""Test otomatis Antrian Klinik WA - 10 test."""
from main import app, mask_hp, validasi_nama, validasi_hp, validasi_poli
import main

client = app.test_client()

def setup_function():
    main._antrian.clear()
    main._counter["nomor"] = 0

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_home_ok():
    assert client.get("/").status_code == 200

def test_daftar_berhasil():
    r = client.post("/api/daftar", json={"nama": "Budi", "no_hp": "081234567890", "poli": "UMUM"})
    assert r.status_code == 201
    assert r.get_json()["nomor"] == 1
    assert "Nomor antrean" in r.get_json()["balasan_wa"]

def test_daftar_nomor_urut():
    client.post("/api/daftar", json={"nama": "Budi", "no_hp": "081234567890", "poli": "UMUM"})
    r = client.post("/api/daftar", json={"nama": "Siti", "no_hp": "081234567891", "poli": "GIGI"})
    assert r.get_json()["nomor"] == 2

def test_daftar_nama_angka_ditolak():
    r = client.post("/api/daftar", json={"nama": "Budi123", "no_hp": "081234567890", "poli": "UMUM"})
    assert r.status_code == 400

def test_daftar_hp_salah_ditolak():
    r = client.post("/api/daftar", json={"nama": "Budi", "no_hp": "123", "poli": "UMUM"})
    assert r.status_code == 400

def test_daftar_poli_salah_ditolak():
    r = client.post("/api/daftar", json={"nama": "Budi", "no_hp": "081234567890", "poli": "BEDAH"})
    assert r.status_code == 400

def test_antrian_tidak_bocorkan_hp():
    client.post("/api/daftar", json={"nama": "Budi", "no_hp": "081234567890", "poli": "UMUM"})
    r = client.get("/api/antrian")
    data = r.get_json()
    assert "081234567890" not in str(data)
    assert "****" in str(data)

def test_mask_hp():
    assert mask_hp("081234567890") == "0812****7890"

def test_validasi_helper():
    assert validasi_nama("Budi Santoso") is True
    assert validasi_hp("081234567890") is True
    assert validasi_poli("UMUM") is True
    assert validasi_poli("BEDAH") is False
