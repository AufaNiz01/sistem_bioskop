import json, os
from typing import List, Dict, Optional
from .models import JadwalFilm, Kursi, Tiket
from .denah import DenahKursi

class ManajemenBioskop:
    def __init__(self):
        self._denah_per_jadwal: Dict[JadwalFilm, DenahKursi] = {}
        self._antrian: List[Tiket] = []
        self._nomor_berikutnya = 1
        self._file_data = "data/bioskop_data.json"
    
    def _get_denah(self, jadwal: JadwalFilm) -> DenahKursi:
        if jadwal not in self._denah_per_jadwal:
            self._denah_per_jadwal[jadwal] = DenahKursi(jadwal)
        return self._denah_per_jadwal[jadwal]
    
    def _buat_nomor(self) -> str:
        nomor = f"A{self._nomor_berikutnya:03d}"
        self._nomor_berikutnya += 1
        return nomor
    
    # CREATE
    def tambah_antrian(self, nama: str, film: str, jam: str, kode_kursi: str) -> dict:
        if not nama or not nama.strip():
            return {"sukses": False, "pesan": "Nama tidak boleh kosong"}
        kursi = Kursi.dari_kode(kode_kursi)
        if not kursi:
            return {"sukses": False, "pesan": f"Kode {kode_kursi} tidak valid"}
        jadwal = JadwalFilm(film, jam)
        denah = self._get_denah(jadwal)
        if not denah.is_tersedia(kursi):
            return {"sukses": False, "pesan": f"Kursi {kode_kursi} sudah terisi untuk {film} jam {jam}"}
        denah.pesan_kursi(kursi)
        tiket = Tiket(self._buat_nomor(), nama.strip(), jadwal, kursi)
        self._antrian.append(tiket)
        return {"sukses": True, "pesan": f"{nama} mendapat nomor {tiket.nomor_antrian}", "data": tiket.to_dict()}
    
    # READ
    def lihat_antrian(self) -> List[dict]:
        return [t.to_dict() for t in self._antrian]
    
    def lihat_satu(self, nomor: str) -> Optional[dict]:
        for t in self._antrian:
            if t.nomor_antrian == nomor:
                return t.to_dict()
        return None
    
    def get_kursi_terisi(self, film: str, jam: str) -> set:
        return set(self._get_denah(JadwalFilm(film, jam)).daftar_kode_terisi())
    
    def get_statistik_kursi(self, film: str, jam: str) -> dict:
        denah = self._get_denah(JadwalFilm(film, jam))
        return {"total_kursi": denah.total_kursi(), "terisi": denah.jumlah_terisi(), "tersedia": denah.jumlah_tersedia()}
    
    # UPDATE
    def update_antrian(self, nomor: str, nama_baru: str = None, kursi_baru: str = None) -> dict:
        for tiket in self._antrian:
            if tiket.nomor_antrian == nomor:
                if nama_baru and nama_baru.strip():
                    tiket.nama = nama_baru.strip()
                if kursi_baru and kursi_baru != tiket.kursi.kode():
                    k = Kursi.dari_kode(kursi_baru)
                    if not k:
                        return {"sukses": False, "pesan": f"Kode {kursi_baru} tidak valid"}
                    denah = self._get_denah(tiket.jadwal)
                    if not denah.is_tersedia(k):
                        return {"sukses": False, "pesan": f"Kursi {kursi_baru} sudah terisi"}
                    denah.pesan_kursi(k)
                    tiket.kursi = k
                return {"sukses": True, "pesan": f"Antrian {nomor} diupdate"}
        return {"sukses": False, "pesan": f"Antrian {nomor} tidak ditemukan"}
    
    # DELETE
    def hapus_antrian(self, nomor: str) -> dict:
        for i, t in enumerate(self._antrian):
            if t.nomor_antrian == nomor:
                self._antrian.pop(i)
                return {"sukses": True, "pesan": f"Antrian {nomor} dihapus"}
        return {"sukses": False, "pesan": "Tidak ditemukan"}
    
    def hapus_semua(self) -> dict:
        jml = len(self._antrian)
        self._antrian = []
        return {"sukses": True, "pesan": f"{jml} antrian dihapus"}
    
    def panggil_antrian(self) -> Optional[dict]:
        if not self._antrian:
            return None
        return self._antrian.pop(0).to_dict()
    
    # PERSISTENCE
    def save_to_file(self) -> bool:
        os.makedirs(os.path.dirname(self._file_data), exist_ok=True)
        data = {
            "denah": [d.to_dict() for d in self._denah_per_jadwal.values()],
            "antrian": [t.to_dict() for t in self._antrian],
            "nomor_berikutnya": self._nomor_berikutnya
        }
        try:
            with open(self._file_data, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False
    
    def load_from_file(self) -> bool:
        if not os.path.exists(self._file_data):
            return False
        try:
            with open(self._file_data, "r") as f:
                data = json.load(f)
            self._denah_per_jadwal = {}
            self._antrian = []
            for d in data.get("denah", []):
                denah = DenahKursi.from_dict(d)
                self._denah_per_jadwal[denah.jadwal] = denah
            for t in data.get("antrian", []):
                self._antrian.append(Tiket.dari_dict(t))
            self._nomor_berikutnya = data.get("nomor_berikutnya", 1)
            return True
        except:
            return False