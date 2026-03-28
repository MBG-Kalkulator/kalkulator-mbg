import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Dampak MBG", page_icon="🍽️", layout="wide")

# --- BAGIAN PEMBUKA ---
st.title("🍽️ Kalkulator Dampak Positif Program Makan Bergizi Gratis (MBG)")
st.write("Kalkulator ini dirancang untuk memproyeksikan dampak positif Program Makan Bergizi Gratis (MBG) terhadap perputaran ekonomi daerah dan investasi kualitas Sumber Daya Manusia (SDM) di masa depan.")
st.caption("💡 Tips: Anda bisa menggeser tuas (slider) di bawah ini, atau klik pada angka di sebelah kanan tuas untuk mengetik angkanya secara manual.")

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
# Menonaktifkan semua interaksi geser/zoom di grafik
fig.update_layout(
    showlegend=False, 
    yaxis_title="Triliun Rupiah", 
    xaxis_title="",
    dragmode=False
)
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# Memasukkan argumen staticPlot agar grafik murni menjadi mode tampilan saja (view-only)
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})


# --- BAGIAN PENJELASAN & RUMUS ---
st.divider()
st.header("📖 Mengapa MBG adalah Investasi, Bukan Biaya?")

st.markdown("### 1. Nilai Tambah SDM Jangka Panjang (Framework WFP & Rockefeller)")
st.markdown("Berdasarkan studi *UN World Food Programme (WFP)* dan *Rockefeller Institute* (2023), **setiap investasi 1 USD untuk program makanan bergizi di sekolah akan memberikan nilai kembalian (ROI) sebesar 5 hingga 35 USD.** Hal ini terjadi karena efek berantai biologis dan akademis: Kenyang $\\rightarrow$ Tidak Absen $\\rightarrow$ Konsentrasi Naik $\\rightarrow$ Nilai Ujian Naik $\\rightarrow$ Pendidikan Baik $\\rightarrow$ Usia Produktif Panjang $\\rightarrow$ **Pendapatan Seumur Hidup Meningkat**.")

# Highlight Rumus menggunakan st.info
st.info(r"**Rumus:** $\text{Total Nilai SDM} = \text{Anggaran MBG} \times \text{Asumsi ROI (5x hingga 35x)}$")

st.markdown("### 2. Efek Pengganda Ekonomi Makro (*Keynesian Multiplier*)")
st.markdown("Dana MBG tidak hilang dimakan. Dana ini pindah dari kas negara ke kantong peternak telur, petani sayur, dan ibu-ibu pengelola dapur umum. Semakin besar porsi uang yang dibelanjakan kembali oleh masyarakat bawah (*Marginal Propensity to Consume* / MPC), semakin kencang roda ekonomi berputar menciptakan PDB baru.")

# Highlight Rumus menggunakan st.info
st.info(r"**Rumus:** $\Delta Y = \frac{1}{1 - MPC} \times \Delta G$")
st.markdown("""
* **$\Delta Y$**: Total penambahan Pendapatan Domestik Bruto (PDB) atau roda ekonomi.
* **$MPC$**: *Marginal Propensity to Consume* (Kecenderungan masyarakat membelanjakan uangnya).
* **$\Delta G$**: Anggaran MBG (Suntikan dana pemerintah).
""")

st.markdown("### 3. Desentralisasi Ekonomi ke Desa & Kapasitas Penerima")
st.markdown("Selama ini perputaran uang tersentralisasi di kota besar. Dengan MBG, jika diasumsikan persentase besar bahan baku wajib dibeli dari UMKM dan petani lokal, maka terjadi transfer kekayaan besar-besaran ke **75.265 desa** di Indonesia. Program ini secara tidak langsung menciptakan lapangan kerja baru di daerah serta memperluas kapasitas jumlah anak yang gizinya terpenuhi.")

# Highlight Rumus menggunakan st.info
st.info(r"**Rumus Uang Beredar per Desa:** $\frac{\text{Anggaran MBG} \times \% \text{Bahan Baku Lokal}}{\text{Jumlah Desa di Indonesia}}$")
st.info(r"**Rumus Penerima Manfaat:** $\frac{\text{Total Anggaran}}{\text{Harga Per Porsi} \times \text{Hari Efektif Sekolah}}$")

st.divider()
# --- BAGIAN PENUTUP (Sesuai Redaksi Baru) ---
st.caption("Kalkulator ini disusun menggunakan pendekatan ilmu ekonomi makro dan data riset lembaga internasional.")
