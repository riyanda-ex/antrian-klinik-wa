# Sistem Antrean Klinik via WhatsApp - Tanpa Aplikasi

from datetime import datetime, timedelta

class AntreanKlinik:
    def __init__(self):
        self.antrean = []
        self.nomor_terakhir = 0
        self.rata_rata_per_pasien = 7 # menit

    def ambil_nomor(self, nama, no_wa, keluhan):
        self.nomor_terakhir += 1
        pasien = {
            "nomor": self.nomor_terakhir,
            "nama": nama,
            "no_wa": no_wa,
            "keluhan": keluhan,
            "jam_daftar": datetime.now(),
            "status": "menunggu"
        }
        self.antrean.append(pasien)
        
        # Hitung estimasi tunggu
        posisi = len([p for p in self.antrean if p["status"] == "menunggu"])
        estimasi_menit = posisi * self.rata_rata_per_pasien
        jam_perkiraan = datetime.now() + timedelta(minutes=estimasi_menit)

        pesan = f"""
Halo {nama}, nomor antrean kamu: A-{pasien['nomor']:03d}
Keluhan: {keluhan}
Posisi antrean: ke-{posisi}
Perkiraan dipanggil: {jam_perkiraan.strftime('%H:%M')} WIB
Silakan tunggu di rumah, kami WA lagi kalau sudah dekat giliran.
"""
        print(pesan)
        return pasien

    def panggil_berikutnya(self):
        for p in self.antrean:
            if p["status"] == "menunggu":
                p["status"] = "dipanggil"
                print(f"MEMANGGIL: A-{p['nomor']:03d} - {p['nama']} - Kirim WA ke {p['no_wa']}: Giliran Anda, silakan ke ruang periksa!")
                return p
        print("Antrean kosong.")
        return None

    def kirim_reminder(self):
        # Kirim WA ke 3 orang berikutnya biar siap-siap
        menunggu = [p for p in self.antrean if p["status"] == "menunggu"][:3]
        for p in menunggu:
            print(f"REMINDER WA ke {p['no_wa']}: Halo {p['nama']}, giliran Anda sebentar lagi (A-{p['nomor']:03d}), mohon bersiap.")

# CONTOH PAKAI
if __name__ == "__main__":
    klinik = AntreanKlinik()
    klinik.ambil_nomor("Bu Siti", "08123456789", "Demam")
    klinik.ambil_nomor("Pak Budi", "08129876543", "Batuk")
    klinik.ambil_nomor("Mbak Ani", "08125554444", "Sakit gigi")
    klinik.kirim_reminder()
    klinik.panggil_berikutnya()
