import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Dampak MBG", page_icon="🍽️", layout="centered")

st.title("🍽️ Kalkulator Dampak Positif MBG")
st.write("Berbeda dengan narasi satir yang hanya melihat pengeluaran, mari kita hitung dampak ekonomi riil dari Program Makan Bergizi Gratis (MBG) menggunakan kacamata ekonomi makro.")

# --- BAGIAN INPUT PARAMETER ---
st.header("⚙️ Atur Parameter Simulasi")

anggaran_triliun = st.number_input("Total Anggaran MBG (Triliun Rupiah)", min_value=1.0, value=71.0, step=1.0)
mpc = st.slider("Kecenderungan Konsumsi Masyarakat Bawah (MPC)", min_value=0.50, max_value=0.99, value=0.75, step=0.01)
harga_porsi = st.number_input("Harga per Porsi (Rupiah)", min_value=5000, value=15000, step=1000)
hari_aktif = st.number_input("Jumlah Hari Efektif Sekolah (Setahun)", min_value=100, value=250, step=10)
jumlah_desa = st.number_input("Jumlah Desa di Indonesia", min_value=10000, value=75265, step=100)

# --- BAGIAN KALKULASI ---
# Konversi ke Rupiah penuh
anggaran_rp = anggaran_triliun * 1_000_000_000_000

# 1. Dampak Ekonomi Makro (Keynesian Multiplier)
multiplier = 1 / (1 - mpc)
dampak_pdb_rp = anggaran_rp * multiplier
dampak_pdb_triliun = dampak_pdb_rp / 1_000_000_000_000

# 2. Estimasi Penerima Manfaat
penerima_manfaat = anggaran_rp / (harga_porsi * hari_aktif)
penerima_juta = penerima_manfaat / 1_000_000

# 3. Potensi Perputaran Uang di Daerah (Asumsi 80% anggaran dibelanjakan ke UMKM lokal/Desa)
persentase_lokal = 0.80
uang_beredar_lokal = anggaran_rp * persentase_lokal
uang_per_desa = uang_beredar_lokal / jumlah_desa
uang_per_desa_miliar = uang_per_desa / 1_000_000_000

# --- BAGIAN HASIL (METRICS) ---
st.header("📊 Hasil Proyeksi Dampak")

col1, col2 = st.columns(2)
col1.metric("Angka Pengganda (Multiplier)", f"{multiplier:,.2f}x", "Roda Ekonomi Berputar")
col2.metric("Proyeksi Penambahan PDB", f"Rp {dampak_pdb_triliun:,.2f} Triliun", f"+ Rp {dampak_pdb_triliun - anggaran_triliun:,.2f} T dari Modal")

col3, col4 = st.columns(2)
col3.metric("Estimasi Penerima Manfaat", f"{penerima_juta:,.1f} Juta Anak", "Gizi Terpenuhi")
col4.metric("Uang Beredar per Desa/Tahun", f"Rp {uang_per_desa_miliar:,.2f} Miliar", "UMKM & Petani Untung")

# --- BAGIAN PENJELASAN & RUMUS ---
st.divider()
st.header("📖 Dari Mana Angka Ini Berasal?")

st.markdown("""
**1. Efek Pengganda Ekonomi (Keynesian Multiplier)** Injeksi dana pemerintah ke masyarakat bawah (untuk beli sayur, telur, beras dari petani lokal) akan terus dibelanjakan kembali. Jika masyarakat menghabiskan 75% pendapatannya untuk konsumsi (MPC = 0.75), maka uang tersebut akan berputar menghasilkan nilai ekonomi berkali-kali lipat.  
*Rumus: Multiplier = 1 / (1 - MPC)* *Dampak PDB = Multiplier * Anggaran Awal*

**2. Estimasi Penerima Manfaat** Angka ini dihitung murni dari kapasitas anggaran yang tersedia dibagi dengan biaya makan anak selama setahun (hari efektif sekolah).  
*Rumus: Total Anggaran / (Harga Porsi * Hari Efektif)*

**3. Uang Beredar di Tingkat Desa** Banyak narasi melupakan bahwa uang MBG tidak mengendap di elit, melainkan turun langsung ke dapur-dapur umum di daerah. Jika diasumsikan 80% anggaran dipakai membeli bahan baku dari petani dan UMKM desa, maka terjadi desentralisasi peredaran uang dari pusat ke daerah.  
*Rumus: (Total Anggaran * 80%) / Jumlah Desa di Indonesia*
""")

st.caption("Kalkulator ini dibuat untuk mengedukasi masyarakat tentang dampak ekonomi makro dari intervensi gizi pemerintah.")
