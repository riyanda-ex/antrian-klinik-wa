# simulasi.py - Simulasi Antrean Klinik WA (Aman, tanpa bot WA asli)
# Cara jalanin: python simulasi.py

antrian = []
nomor = 0

def mask_hp(no_hp):
    no_hp = ''.join(c for c in no_hp if c.isdigit())
    if len(no_hp) < 8:
        return "****"
    return f"{no_hp[:4]}****{no_hp[-4:]}"

def daftar():
    global nomor
    print("\n=== DAFTAR ANTREAN BARU ===")
    nama = input("Nama samaran: ").strip()
    hp = input("No HP (contoh 081234567890): ").strip()
    poli = input("Poli (UMUM/GIGI/ANAK/LANSIA/KIA): ").strip().upper()

    if not nama or len(nama) > 50:
        print("❌ Nama tidak valid")
        return
    if poli not in ["UMUM", "GIGI", "ANAK", "LANSIA", "KIA"]:
        print("❌ Poli tidak valid")
        return

    nomor += 1
    estimasi = len(antrian) * 10
    antrian.append({"nomor": nomor, "nama": nama.title(), "poli": poli, "hp_mask": mask_hp(hp), "estimasi": estimasi})
    print(f"\n✅ Berhasil! Balasan WA:")
    print(f"Halo {nama.title()}, pendaftaran berhasil!")
    print(f"Nomor antrean: {nomor} - Poli {poli}")
    print(f"Estimasi tunggu: ~{estimasi} menit")
    print(f"Jangan kirim NIK / No. BPJS via chat.")

def lihat():
    print("\n=== ANTREAN HARI INI ===")
    if not antrian:
        print("Belum ada antrean.")
        return
    for a in antrian:
        print(f"#{a['nomor']} {a['nama']} - {a['poli']} - ~{a['estimasi']} mnt - {a['hp_mask']}")

while True:
    print("\n--- SIMULASI ANTREAN KLINIK WA ---")
    print("1. Daftar antrean")
    print("2. Lihat antrean")
    print("3. Keluar")
    pilih = input("Pilih (1/2/3): ").strip()
    if pilih == "1":
        daftar()
    elif pilih == "2":
        lihat()
    elif pilih == "3":
        print("Sampai jumpa! Ini simulasi edukasi.")
        break
    else:
        print("Pilih 1, 2, atau 3")
