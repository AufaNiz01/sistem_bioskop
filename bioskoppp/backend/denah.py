from typing import Set, List
from .models import Kursi, JadwalFilm

class DenahKursi:
    BARIS = ['A','B','C','D','E','F','G']
    KURSI_KIRI, KURSI_KANAN = 6, 6
    
    def __init__(self, jadwal: JadwalFilm):
        self._jadwal = jadwal
        self._kursi_terisi: Set[Kursi] = set()
    
    @property
    def jadwal(self):
        return self._jadwal
    
    def is_tersedia(self, kursi: Kursi) -> bool:
        return kursi not in self._kursi_terisi
    
    def pesan_kursi(self, kursi: Kursi) -> bool:
        if not self.is_tersedia(kursi):
            return False
        self._kursi_terisi.add(kursi)
        return True
    
    def jumlah_terisi(self) -> int:
        return len(self._kursi_terisi)
    
    def jumlah_tersedia(self) -> int:
        return self.total_kursi() - self.jumlah_terisi()
    
    def total_kursi(self) -> int:
        return len(self.BARIS) * (self.KURSI_KIRI + self.KURSI_KANAN)
    
    def daftar_kode_terisi(self) -> List[str]:
        return sorted([k.kode() for k in self._kursi_terisi])
    
    def to_dict(self) -> dict:
        return {"jadwal_key": self._jadwal.key(), "kursi_terisi": self.daftar_kode_terisi()}
    
    @staticmethod
    def from_dict(data: dict):
        from .models import JadwalFilm
        jadwal = JadwalFilm.dari_key(data["jadwal_key"])
        denah = DenahKursi(jadwal)
        for kode in data.get("kursi_terisi", []):
            kursi = Kursi.dari_kode(kode)
            if kursi:
                denah._kursi_terisi.add(kursi)
        return denah