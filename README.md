Bioskop Queue Management System

Sistem ini merupakan aplikasi manajemen antrean dan pemesanan tiket bioskop yang dikembangkan menggunakan konsep Object-Oriented Programming (OOP). Pengguna dapat melakukan pemesanan tiket, memilih kursi melalui denah bioskop interaktif, serta melihat ketersediaan kursi secara real-time. Selain itu, sistem menyediakan fitur CRUD (Create, Read, Update, Delete) yang memungkinkan pengelolaan data pemesanan secara lengkap. Antarmuka aplikasi dibangun menggunakan Streamlit, sementara seluruh logika bisnis dan pengolahan data dikembangkan dengan Python.

✨ Fitur Unggulan

- 🎫 **Manajemen Antrean FIFO** — Sistem antrean yang adil (First In, First Out)
- 💺 **Denah Kursi Real-time** — Visualisasi kursi kosong/terisi dengan kode warna
- 📊 **CRUD Lengkap** — Create, Read, Update, Delete data antrean
- 💾 **Persistent Storage** — Data tersimpan otomatis ke file JSON
- 🎨 **UI/UX Modern** — Tampilan bioskop yang imersif dengan CSS custom
- 🔍 **Validasi Kursi Ganda** — Mencegah pemesanan kursi yang sama untuk jadwal yang sama

## 🏗️ Arsitektur Proyek

```
bioskop/
├── backend/                 # Logika bisnis (OOP murni)
│   ├── models.py           # User-Defined Data Structure
│   ├── denah.py            # Manajemen denah kursi
│   ├── manajemen.py        # CRUD & queue operations
│   └── __init__.py         # Package initializer
├── frontend/
│   └── app.py              # Streamlit UI (tanpa logika bisnis)
└── data/
    └── bioskop_data.json   # Penyimpanan data otomatis
```

## 🚀 Cara Menjalankan

```bash
# Clone repository
git clone https://github.com/AufaNiz01/sistem_bioskop.git

# Masuk ke folder proyek
cd sistem_bioskop/bioskoppp     <-- p nya 3 janlup!

# Install dependencies
pip install streamlit

# Jalankan aplikasi
streamlit run frontend/app.py
```

## 🧠 Konsep yang Diterapkan

| Konsep | Implementasi |
|--------|--------------|
| **OOP** | Class `Kursi`, `JadwalFilm`, `Tiket`, `DenahKursi`, `ManajemenBioskop` |
| **User-Defined Data Structure** | Semua struktur data dibuat dari class sendiri, bukan bawaan Python |
| **Encapsulation** | Atribut protected dengan underscore `_` |
| **Queue (FIFO)** | Antrean tiket dengan `pop(0)` dan `append()` |
| **Serialization** | Method `to_dict()` dan `from_dict()` untuk penyimpanan JSON |

📸 Screenshot
<img width="1343" height="611" alt="image" src="https://github.com/user-attachments/assets/98d9909c-c949-4b67-a179-505f284a6f16" />


👥 Tim Pengembang
- Fairuz Idzihar Iftiran — [@fayydzi]
- Musyfiq Fakhruzzaman — [@musyfiq-mfiq]
- Aufa Nu'aim I. Z — [@AufaNiz01]

⚙️ Teknologi

| Lapisan        | Teknologi    |
|--------------- |-----------   |
| Frontend       | Streamlit    |
| Backend        | Python (OOP) |
| Data Structure | User-Defined |
| Storage        | JSON         |

