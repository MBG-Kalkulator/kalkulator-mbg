import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Dampak MBG", page_icon="🍽️", layout="wide")

st.title("🍽️ Kalkulator Dampak Positif Program Makan Bergizi Gratis (MBG)")
st.caption("Gunakan tuas (slider) di bawah ini untuk mensimulasikan dampak ekonomi dan investasi SDM dari program MBG. Anda juga bisa mengklik angka di sebelah kanan tuas untuk mengetiknya secara manual.")

st.divider()

# --- BAGIAN INPUT PARAMETER ---
st.header("⚙️ Atur Parameter Simulasi")

col_input1, col_input2 = st.columns(2)

with col_input1:
    st.subheader("Parameter Anggaran & Ekonomi")
    anggaran_triliun = st.slider(
        "Total Anggaran MBG (Triliun Rupiah)", 
        min_value=1.0, max_value=1000.0, value=335.0, step=1.0,
        help="Total alokasi dana pemerintah pusat untuk program MBG dalam satu tahun anggaran."
    )
    mpc = st.slider(
        "Kecenderungan Konsumsi Masyarakat (MPC)", 
        min_value=0.50, max_value=0.99, value=0.88, step=0.01,
        help="Marginal Propensity to Consume (MPC). Angka 0.88 berarti 88% dari setiap tambahan pendapatan masyarakat (petani/UMKM pemasok MBG) akan langsung dibelanjakan kembali, memutar roda ekonomi."
    )
    persentase_lokal = st.slider(
        "Persentase Anggaran untuk UMKM/Petani Lokal (%)", 
        min_value=10, max_value=100, value=80, step=5,
        help="Asumsi besaran porsi anggaran yang wajib dibelanjakan untuk bahan baku dari petani, peternak, dan UMKM di daerah/desa setempat."
    )

with col_input2:
    st.subheader("Parameter Program & SDM")
    harga_porsi = st.slider(
        "Harga per Porsi (Rupiah)", 
        min_value=5000, max_value=30000, value=15000, step=500,
        help="Estimasi harga rata-rata satu porsi makanan bergizi yang diberikan kepada anak."
    )
    hari_aktif = st.slider(
        "Hari Efektif Sekolah (Setahun)", 
        min_value=100, max_value=300, value=250, step=5,
        help="Jumlah perkiraan hari anak masuk sekolah dan menerima makanan dalam satu tahun akademik."
    )
    roi_sdm = st.slider(
        "Asumsi ROI SDM Jangka Panjang", 
        min_value=5, max_value=35, value=15, step=1, 
        help="Return on Investment. Studi PBB (WFP) & Rockefeller Institute (2023) mencatat bahwa setiap 1 USD investasi MBG akan menghasilkan kembalian 5-35 USD dalam bentuk nilai tambah kualitas SDM seumur hidup."
    )

jumlah_desa = 75265 

# --- BAGIAN KALKULASI ---
anggaran_rp = anggaran_triliun * 1_000_000_000_000

# 1. Dampak Ekonomi Makro (Keynesian Multiplier)
multiplier = 1 / (1 - mpc)
dampak_pdb_rp = anggaran_rp * multiplier
dampak_pdb_triliun = dampak_pdb_rp / 1_000_000_000_000

# 2. Estimasi Penerima Manfaat
penerima_manfaat = anggaran_rp / (harga_porsi * hari_aktif)
penerima_juta = penerima_manfaat / 1_000_000

# 3. Potensi Perputaran Uang di Daerah
uang_beredar_lokal = anggaran_rp * (persentase_lokal / 100)
uang_per_desa = uang_beredar_lokal / jumlah_desa
uang_per_desa_miliar = uang_per_desa / 1_000_000_000

# 4. Return on Investment (ROI) SDM Jangka Panjang
roi_sdm_rp = anggaran_rp * roi_sdm
roi_sdm_triliun = roi_sdm_rp / 1_000_000_000_000

# --- BAGIAN HASIL (METRICS) ---
st.header("📊 Hasil Proyeksi Dampak")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Penerima Manfaat", f"{penerima_juta:,.1f} Juta", "Anak Sekolah")
col2.metric("Uang Beredar per Desa", f"Rp {uang_per_desa_miliar:,.2f} M", f"{persentase_lokal}% Bahan Lokal")
col3.metric("Roda Ekonomi (PDB)", f"Rp {dampak_pdb_triliun:,.0f} T", f"Multiplier {multiplier:,.2f}x")
col4.metric("Nilai Tambah SDM (Masa Depan)", f"Rp {roi_sdm_triliun:,.0f} T", f"ROI {roi_sdm}x Lipat")

# --- BAGIAN GRAFIK (VISUALISASI) ---
st.divider()
st.subheader("📈 Visualisasi Perbandingan Nilai (Triliun Rupiah)")

# Data untuk Bar Chart
data_grafik = pd.DataFrame({
    "Kategori": ["Anggaran Awal", "Dampak Perputaran Ekonomi (PDB)", "Proyeksi Nilai Tambah SDM"],
    "Nilai (Triliun Rupiah)": [anggaran_triliun, dampak_pdb_triliun, roi_sdm_triliun]
})

fig = px.bar(
    data_grafik, 
    x="Kategori", 
    y="Nilai (Triliun Rupiah)",
    text="Nilai (Triliun Rupiah)",
    color="Kategori",
    color_discrete_sequence=["#EF553B", "#00CC96", "#636EFA"]
)
fig.update_traces(texttemplate='Rp %{text:,.0f} T', textposition='outside')
fig.update_layout(showlegend=False, yaxis_title="Triliun Rupiah", xaxis_title="")
st.plotly_chart(fig, use_container_width=True)

# --- BAGIAN PENJELASAN & RUMUS ---
st.divider()
st.header("📖 Dari Mana Angka-Angka Ini Berasal?")

st.markdown("""
### 1. Efek Pengganda Ekonomi (*Keynesian Multiplier*)
Dana MBG tidak hilang. Dana tersebut dibelanjakan ke peternak telur, petani sayur, dan dapur umum. Mereka kemudian membelanjakan pendapatannya lagi. Perputaran uang ini dihitung menggunakan rumus Multiplier:
""")
st.latex(r"\Delta Y = \frac{1}{1 - MPC} \times \Delta G")
st.markdown("""
* **$\Delta Y$**: Total penambahan Pendapatan Domestik Bruto (PDB) atau roda ekonomi.
* **$MPC$**: *Marginal Propensity to Consume* (kecenderungan konsumsi).
* **$\Delta G$**: Anggaran MBG (Suntikan dana pemerintah).

### 2. Estimasi Penerima Manfaat (Kapasitas Program)
Jumlah anak yang gizinya terpenuhi dihitung dari total anggaran dibagi biaya operasional harian selama setahun penuh.
""")
st.latex(r"\text{Penerima Manfaat} = \frac{\text{Total Anggaran}}{\text{Harga Per Porsi} \times \text{Hari Efektif Sekolah}}")

### 3. Nilai Tambah SDM Jangka Panjang (Framework PBB & Rockefeller)
st.markdown("""
Berdasarkan studi *UN World Food Programme (WFP)* dan *Rockefeller Institute* (2023), program makanan bergizi di sekolah memiliki efek biologis dan akademis yang berantai:
Kenyang $\\rightarrow$ Tidak Absen $\\rightarrow$ Konsentrasi Naik $\\rightarrow$ Nilai Ujian Naik $\\rightarrow$ Pendidikan Baik $\\rightarrow$ Usia Produktif Panjang $\\rightarrow$ **Pendapatan Seumur Hidup Meningkat**.
""")
st.latex(r"\text{Total Nilai SDM} = \text{Anggaran MBG} \times \text{Asumsi ROI (5x hingga 35x)}")

### 4. Desentralisasi Uang ke Tingkat Desa
st.markdown("""
Untuk memastikan uang dari pusat turun ke bawah dan menciptakan lapangan kerja baru bagi warga lokal (khususnya perempuan/ibu-ibu):
""")
st.latex(r"\text{Uang Beredar per Desa} = \frac{\text{Anggaran MBG} \times \% \text{Bahan Baku Lokal}}{\text{Jumlah Desa di Indonesia (75.265)}}")

st.caption("Kalkulator tandingan ini disusun menggunakan pendekatan ilmu ekonomi makro dan data riset lembaga internasional.")
