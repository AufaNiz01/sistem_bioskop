import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend import ManajemenBioskop

# ========== KONSTANTA UI ==========
DAFTAR_FILM = [
    "🎬 Avatar: The Way of Water",
    "🦸 Spider-Man: Across the Spider-Verse",
    "🚀 Oppenheimer",
    "💀 The Nun II",
    "🐉 John Wick: Chapter 4"
]

JADWAL = {
    "🎬 Avatar: The Way of Water": ["13:00", "16:00", "19:00", "21:30"],
    "🦸 Spider-Man: Across the Spider-Verse": ["14:30", "17:30", "20:00"],
    "🚀 Oppenheimer": ["12:00", "15:30", "19:00"],
    "💀 The Nun II": ["13:30", "16:30", "20:30"],
    "🐉 John Wick: Chapter 4": ["15:00", "18:00", "21:00"]
}

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(page_title="Sistem Antrean Bioskop", page_icon="🎬", layout="wide")

# ========== CSS ==========
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-family: 'Arial Black', sans-serif;
        font-weight: 800;
        color: #e50914;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    .cinema-screen {
        background: linear-gradient(180deg, #2c2c2c 0%, #1a1a1a 100%);
        color: #ffcc00;
        text-align: center;
        padding: 10px;
        margin: 10px auto 20px auto;
        border-radius: 8px;
        font-size: 0.9rem;
        letter-spacing: 6px;
        width: 85%;
    }
    .seat-kosong button {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        height: 45px !important;
        font-weight: bold !important;
    }
    .seat-terisi button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        color: #ddd !important;
        border-radius: 10px !important;
        height: 45px !important;
        opacity: 0.7 !important;
    }
    .label-baris {
        background: #16213e;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        color: #ffd700;
        padding: 12px 0;
    }
    .panggil-card {
        background: linear-gradient(135deg, #e50914 0%, #990000 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ========== INISIALISASI SESSION STATE ==========
if "manajemen" not in st.session_state:
    st.session_state.manajemen = ManajemenBioskop()
    st.session_state.manajemen.load_from_file()
    st.session_state.kursi_terpilih = None
    st.session_state.update_mode = False
    st.session_state.update_nomor = None
    st.session_state.tiket_terpanggil = None

def save_data():
    st.session_state.manajemen.save_to_file()

def reset_ui_state():
    st.session_state.kursi_terpilih = None
    st.session_state.update_mode = False
    st.session_state.update_nomor = None

# ========== HEADER ==========
st.markdown('<div class="main-title">🎬 SISTEM TIKET BIOSKOP 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ Pemesanan Tiket | Antrean | Denah Kursi Interaktif ✨</div>', unsafe_allow_html=True)
st.markdown("---")

# ========== TOMBOL PANGGIL ANTRIAN ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔔 PANGGIL ANTREAN BERIKUTNYA", type="primary", use_container_width=True):
        hasil = st.session_state.manajemen.panggil_antrian()
        if hasil:
            st.session_state.tiket_terpanggil = hasil
            st.success(f"📢 Memanggil {hasil['nomor_antrian']} - {hasil['nama']}")
            save_data()
            st.rerun()
        else:
            st.warning("⚠️ Antrean kosong!")

# ========== TAMPILAN TIKET TERPANGGIL ==========
if st.session_state.tiket_terpanggil:
    t = st.session_state.tiket_terpanggil
    st.markdown(f"""
    <div class="panggil-card">
        <h3>🎫 Tiket Dipanggil:</h3>
        <p style="font-size: 1.8rem; margin: 0;">
            <b style="color: #ffcc00;">{t['nomor_antrian']}</b>
        </p>
        <hr>
        <table style="width: 100%;">
            <tr><td style="width: 30%;"><b>Nama</b></td><td>: {t['nama']}</td>
            <tr><td><b>Film</b></td><td>: {t['film']}</td>
            <tr><td><b>Jam</b></td><td>: {t['jam_tayang']}</td>
            <tr><td><b>Kursi</b></td><td>: {t['kursi']}</td>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ========== DUA KOLOM UTAMA ==========
col_kiri, col_kanan = st.columns([1, 1.2], gap="large")

# ========== KOLOM KIRI: FORM PEMESANAN ==========
with col_kiri:
    st.subheader("🎬 Pemesanan Tiket")
    
    film_terpilih = st.selectbox("Pilih Film", options=DAFTAR_FILM, key="film_select")
    jam_tersedia = JADWAL.get(film_terpilih, ["19:00"])
    jam_tayang = st.selectbox("Pilih Jam Tayang", options=jam_tersedia, key="jam_select")
    
    statistik = st.session_state.manajemen.get_statistik_kursi(film_terpilih, jam_tayang)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("💺 Kursi Tersedia", f"{statistik['tersedia']}/{statistik['total_kursi']}")
    with col_b:
        st.metric("🎯 Kursi Terisi", f"{statistik['terisi']}")
    
    st.markdown("---")
    
    if st.session_state.update_mode:
        st.warning(f"✏️ MODE UPDATE: {st.session_state.update_nomor}")
        if st.button("❌ Batalkan Update"):
            st.session_state.update_mode = False
            st.session_state.update_nomor = None
            st.rerun()
    
    if st.session_state.update_mode:
        data = st.session_state.manajemen.lihat_satu(st.session_state.update_nomor)
        default_nama = data["nama"] if data else ""
        default_kursi = data["kursi"] if data else ""
    else:
        default_nama = ""
        default_kursi = ""
    
    # HANYA SATU INPUT KURSI DI SINI
    nama_input = st.text_input("👤 Nama Pembeli", value=default_nama, placeholder="Masukkan nama")
    kursi_input = st.text_input("💺 Kode Kursi (contoh: A1, B3)", value=default_kursi, placeholder="A1")
    
    if kursi_input:
        kursi_input = kursi_input.upper()
    
    tombol = "✏️ UPDATE" if st.session_state.update_mode else "🎫 PESAN"
    
    if st.button(tombol, type="primary", use_container_width=True):
        if not nama_input or nama_input.strip() == "":
            st.error("Nama harus diisi")
        elif not kursi_input:
            st.error("Kursi harus diisi")
        else:
            terisi = st.session_state.manajemen.get_kursi_terisi(film_terpilih, jam_tayang)
            if kursi_input in terisi:
                st.error(f"Kursi {kursi_input} sudah terisi")
            elif st.session_state.update_mode:
                hasil = st.session_state.manajemen.update_antrian(st.session_state.update_nomor, nama_input, kursi_input)
                if hasil["sukses"]:
                    st.success(hasil["pesan"])
                    st.session_state.update_mode = False
                    st.session_state.update_nomor = None
                    save_data()
                    st.rerun()
                else:
                    st.error(hasil["pesan"])
            else:
                hasil = st.session_state.manajemen.tambah_antrian(nama_input, film_terpilih, jam_tayang, kursi_input)
                if hasil["sukses"]:
                    st.success(hasil["pesan"])
                    save_data()
                    st.rerun()
                else:
                    st.error(hasil["pesan"])
# ========== KOLOM KANAN: DENAH KURSI (HANYA TAMPILAN) ==========
with col_kanan:
    st.subheader(f"💺 Denah Kursi - {film_terpilih}")
    st.caption(f"⏰ Jam Tayang: {jam_tayang}")
    
    st.markdown('<div class="cinema-screen">🎞️  L A Y A R  🎞️</div>', unsafe_allow_html=True)
    
    kursi_terisi = st.session_state.manajemen.get_kursi_terisi(film_terpilih, jam_tayang)
    
    # Tabel denah kursi (HANYA TAMPILAN, tidak bisa diklik)
    html_denah = '<table style="width:100%; text-align:center; margin:auto; border-collapse:collapse;">'
    
    # Header nomor kursi
    html_denah += '<tr><th style="width:50px"></th>'
    for i in range(1, 7):
        html_denah += f'<th style="width:60px">{i}</th>'
    html_denah += '<th style="width:40px"></th>'
    for i in range(7, 13):
        html_denah += f'<th style="width:60px">{i}</th>'
    html_denah += '<th style="width:50px"></th></tr>'
    
    # Baris A-G
    for row in ['A','B','C','D','E','F','G']:
        html_denah += '<tr>'
        # Label kiri
        html_denah += f'<td style="background:#16213e; color:#ffd700; font-weight:bold; border-radius:10px; padding:10px;">{row}</td>'
        
        # Kursi kiri 1-6
        for i in range(1, 7):
            seat = f"{row}{i}"
            if seat in kursi_terisi:
                html_denah += '<td style="background:#e74c3c; color:white; border-radius:10px; padding:10px; text-align:center;">❌</td>'
            else:
                html_denah += '<td style="background:#27ae60; color:white; border-radius:10px; padding:10px; text-align:center;">🎬</td>'
        
        # Lorong
        html_denah += '<td style="color:#ffd700; text-align:center;">⏺</td>'
        
        # Kursi kanan 7-12
        for i in range(7, 13):
            seat = f"{row}{i}"
            if seat in kursi_terisi:
                html_denah += '<td style="background:#e74c3c; color:white; border-radius:10px; padding:10px; text-align:center;">❌</td>'
            else:
                html_denah += '<td style="background:#27ae60; color:white; border-radius:10px; padding:10px; text-align:center;">🎬</td>'
        
        # Label kanan
        html_denah += f'<td style="background:#16213e; color:#ffd700; font-weight:bold; border-radius:10px; padding:10px;">{row}</td>'
        html_denah += '</tr>'
    
    html_denah += '</table>'
    
    st.markdown(html_denah, unsafe_allow_html=True)
    
    # Keterangan
    a, b, c = st.columns(3)
    a.markdown("🎬 **Kosong**")
    b.markdown("❌ **Terisi**")
    c.markdown(f"📊 **Terisi:** {statistik['terisi']}/{statistik['total_kursi']}")

# ========== DAFTAR ANTRIAN ==========
st.markdown("---")
st.subheader("📋 Daftar Antrean Saat Ini")

daftar_antrean = st.session_state.manajemen.lihat_antrian()

if daftar_antrean:
    st.dataframe(
        daftar_antrean,
        use_container_width=True,
        hide_index=True,
        column_config={
            "nomor_antrian": "No. Antrian",
            "nama": "Nama",
            "film": "Film",
            "jam_tayang": "Jam",
            "kursi": "Kursi",
            "waktu_pesan": "Waktu Pesan"
        }
    )
    
    # Tombol aksi CRUD
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    
    with col_act1:
        nomor_hapus = st.selectbox(
            "Pilih nomor untuk dihapus",
            options=[t["nomor_antrian"] for t in daftar_antrean],
            key="hapus_select"
        )
        if st.button("🗑️ HAPUS", use_container_width=True):
            hasil = st.session_state.manajemen.hapus_antrian(nomor_hapus)
            if hasil["sukses"]:
                st.success(hasil["pesan"])
                save_data()
                st.rerun()
            else:
                st.error(hasil["pesan"])
    
    with col_act2:
        nomor_update = st.selectbox(
            "Pilih nomor untuk diupdate",
            options=[t["nomor_antrian"] for t in daftar_antrean],
            key="update_select"
        )
        if st.button("✏️ UPDATE", use_container_width=True):
            st.session_state.update_mode = True
            st.session_state.update_nomor = nomor_update
            st.rerun()
    
    with col_act3:
        if st.button("🗑️ HAPUS SEMUA", use_container_width=True):
            hasil = st.session_state.manajemen.hapus_semua()
            st.success(hasil["pesan"])
            save_data()
            st.rerun()
    
    with col_act4:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
else:
    st.info("📭 Antrean kosong. Silakan tambah antrian baru.")