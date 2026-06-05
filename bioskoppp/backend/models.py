from datetime import datetime
from typing import Optional, List, Dict

class Kursi:
    BARIS_VALID = ['A','B','C','D','E','F','G']
    def __init__(self, baris: str, nomor: int):
        if baris.upper() not in self.BARIS_VALID or not 1 <= nomor <= 12:
            raise ValueError("Baris A-G, nomor 1-12")
        self.baris = baris.upper()
        self.nomor = nomor
    def kode(self) -> str:
        return f"{self.baris}{self.nomor}"
    def __eq__(self, other):
        return isinstance(other, Kursi) and self.kode() == other.kode()
    def __hash__(self):
        return hash(self.kode())
    def __str__(self):
        return self.kode()
    def to_dict(self) -> dict:
        return {"baris": self.baris, "nomor": self.nomor, "kode": self.kode()}
    @staticmethod
    def dari_kode(kode: str):
        return Kursi(kode[0], int(kode[1:])) if kode and len(kode)>=2 else None
    @staticmethod
    def semua_kode():
        return [f"{b}{n}" for b in Kursi.BARIS_VALID for n in range(1,13)]

class JadwalFilm:
    def __init__(self, film: str, jam: str):
        self.film = film
        self.jam_tayang = jam
    def key(self) -> str:
        return f"{self.film}|{self.jam_tayang}"
    def __eq__(self, other):
        return isinstance(other, JadwalFilm) and self.key() == other.key()
    def __hash__(self):
        return hash(self.key())
    def to_dict(self):
        return {"film": self.film, "jam_tayang": self.jam_tayang}
    @staticmethod
    def dari_key(key: str):
        film, jam = key.split("|", 1)
        return JadwalFilm(film, jam)

class Tiket:
    def __init__(self, nomor: str, nama: str, jadwal: JadwalFilm, kursi: Kursi):
        self.nomor_antrian = nomor
        self.nama = nama
        self.jadwal = jadwal
        self.kursi = kursi
        self.waktu_pesan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def to_dict(self):
        return {"nomor_antrian": self.nomor_antrian, "nama": self.nama,
                "film": self.jadwal.film, "jam_tayang": self.jadwal.jam_tayang,
                "kursi": self.kursi.kode(), "waktu_pesan": self.waktu_pesan}
    @staticmethod
    def dari_dict(data):
        jadwal = JadwalFilm(data["film"], data["jam_tayang"])
        kursi = Kursi.dari_kode(data["kursi"])
        t = Tiket(data["nomor_antrian"], data["nama"], jadwal, kursi)
        t.waktu_pesan = data.get("waktu_pesan", t.waktu_pesan)
        return t