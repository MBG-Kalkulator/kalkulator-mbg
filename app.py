import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman (Wide Mode untuk Desktop, responsif di Mobile)
st.set_page_config(page_title="Kalkulator Dampak MBG", page_icon="🍽️", layout="wide")

# --- CUSTOM CSS UNTUK SEDIKIT POLESAN (Opsional) ---
st.markdown("""
    <style>
    /* Mengurangi jarak kosong di atas halaman */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- BAGIAN PEMBUKA ---
st.title("🍽️ Kalkulator Dampak MBG")
st.write("Kalkulator ini dirancang untuk memproyeksikan dampak positif Program Makan Bergizi Gratis (MBG) terhadap perputaran ekonomi daerah dan investasi kualitas Sumber Daya Manusia (SDM) di masa depan.")
st.caption("💡 Geser tuas di dalam kotak untuk mengubah simulasi.")

st.divider()

# --- BAGIAN INPUT PARAMETER ---
st.header("⚙️ Atur Parameter Simulasi")

col_input1, col_input2 = st.columns(2)

with col_input1:
    # Membungkus dengan container agar menjadi "Kartu"
    with st.container(border=True):
        st.subheader("Anggaran & Ekonomi")
        anggaran_triliun = st.slider(
            "Total Anggaran (Triliun Rupiah)", 
            min_value=1.0, max_value=1000.0, value=335.0, step=1.0,
            help="Total alokasi dana pemerintah pusat untuk program MBG dalam satu tahun anggaran."
        )
        mpc = st.slider(
            "Kecenderungan Konsumsi (MPC)", 
            min_value=0.50, max_value=0.99, value=0.88, step=0.01,
            help="Marginal Propensity to Consume (MPC). Angka 0.88 berarti 88% dari tambahan pendapatan masyarakat langsung dibelanjakan kembali."
        )
        persentase_lokal = st.slider(
            "Porsi Bahan Baku Lokal (%)", 
            min_value=10, max_value=100, value=80, step=5,
            help="Persentase anggaran yang wajib dibelanjakan untuk UMKM/petani lokal setempat."
        )

with col_input2:
    with st.container(border=True):
        st.subheader("Program & Kapasitas SDM")
        harga_porsi = st.slider(
            "Harga per Porsi (Rupiah)", 
            min_value=5000, max_value=30000, value=15000, step=500,
            help="Estimasi harga rata-rata satu porsi makanan bergizi yang diberikan kepada anak."
        )
        hari_aktif = st.slider(
            "Hari Efektif Sekolah", 
            min_value=100, max_value=300, value=250, step=5,
            help="Jumlah perkiraan hari anak masuk sekolah dalam setahun."
        )
        roi_sdm = st.slider(
            "ROI SDM Jangka Panjang (WFP)", 
            min_value=5, max_value=35, value=15, step=1, 
            help="Return on Investment. Studi PBB (WFP, 2023) mencatat tiap 1 USD investasi MBG kembali 5-35 USD sebagai nilai tambah kualitas SDM seumur hidup."
        )

jumlah_desa = 75265 

# --- BAGIAN KALKULASI ---
anggaran_rp = anggaran_triliun * 1_000_000_000_000
multiplier = 1 / (1 - mpc)
dampak_pdb_rp = anggaran_rp * multiplier
dampak_pdb_triliun = dampak_pdb_rp / 1_000_000_000_000

penerima_manfaat = anggaran_rp / (harga_porsi * hari_aktif)
penerima_juta = penerima_manfaat / 1_000_000

uang_beredar_lokal = anggaran_rp * (persentase_lokal / 100)
uang_per_desa = uang_beredar_lokal / jumlah_desa
uang_per_desa_miliar = uang_per_desa / 1_000_000_000

roi_sdm_rp = anggaran_rp * roi_sdm
roi_sdm_triliun = roi_sdm_rp / 1_000_000_000_000

# --- BAGIAN HASIL (METRICS) ---
st.header("📊 Hasil Proyeksi Dampak")

# Dibungkus dalam container agar terlihat lebih solid
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Penerima Manfaat", f"{penerima_juta:,.1f} Juta", "Anak Sekolah")
    col2.metric("Uang per Desa/Tahun", f"Rp {uang_per_desa_miliar:,.2f} M", f"{persentase_lokal}% Bahan Lokal")
    col3.metric("Roda Ekonomi (PDB)", f"Rp {dampak_pdb_triliun:,.0f} T", f"Multiplier {multiplier:,.2f}x")
    col4.metric("Nilai SDM (Masa Depan)", f"Rp {roi_sdm_triliun:,.0f} T", f"ROI {roi_sdm}x Lipat")

# --- BAGIAN GRAFIK (VISUALISASI CLEAN UI) ---
st.divider()
st.subheader("📈 Perbandingan Nilai (Triliun Rupiah)")

data_grafik = pd.DataFrame({
    "Kategori": ["Anggaran Awal", "Perputaran Ekonomi (PDB)", "Proyeksi Nilai SDM"],
    "Nilai (Triliun Rupiah)": [anggaran_triliun, dampak_pdb_triliun, roi_sdm_triliun]
})

fig = px.bar(
    data_grafik, 
    x="Kategori", 
    y="Nilai (Triliun Rupiah)",
    text="Nilai (Triliun Rupiah)",
    color="Kategori",
    # Menggunakan palet warna yang lebih "Tech Dashboard"
    color_discrete_sequence=["#FF7A59", "#00B4B6", "#425B76"] 
)

# Mempercantik tampilan teks pada batang
fig.update_traces(
    texttemplate='<b>Rp %{text:,.0f} T</b>', 
    textposition='outside',
    cliponaxis=False, # Mencegah teks terpotong di atas
    marker_line_width=0 # Menghilangkan border pada batang
)

# Membersihkan layout grafik
fig.update_layout(
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="",
    yaxis_title="",
    margin=dict(t=40, b=0, l=0, r=0), # Memangkas margin berlebih
    dragmode=False,
    font=dict(size=14)
)

# Menyembunyikan grid dan angka di sumbu Y (karena sudah ada di batang)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, fixedrange=True)
fig.update_xaxes(showgrid=False, zeroline=False, fixedrange=True)

st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})


# --- BAGIAN PENJELASAN & RUMUS ---
st.divider()
st.header("📖 Mengapa MBG adalah Investasi, Bukan Biaya?")

with st.expander("1. Nilai Tambah SDM Jangka Panjang (Framework WFP & Rockefeller)", expanded=True):
    st.markdown("Berdasarkan studi *UN World Food Programme (WFP)* dan *Rockefeller Institute* (2023), **setiap investasi 1 USD untuk program makanan bergizi di sekolah akan memberikan nilai kembalian (ROI) sebesar 5 hingga 35 USD.** Hal ini terjadi karena efek berantai biologis dan akademis: Kenyang $\\rightarrow$ Tidak Absen $\\rightarrow$ Konsentrasi Naik $\\rightarrow$ Nilai Ujian Naik $\\rightarrow$ Pendidikan Baik $\\rightarrow$ Usia Produktif Panjang $\\rightarrow$ **Pendapatan Seumur Hidup Meningkat**.")
    st.info(r"**Rumus:** $\text{Total Nilai SDM} = \text{Anggaran MBG} \times \text{Asumsi ROI (5x hingga 35x)}$")

with st.expander("2. Efek Pengganda Ekonomi Makro (Keynesian Multiplier)", expanded=False):
    st.markdown("Dana MBG tidak hilang dimakan. Dana ini pindah dari kas negara ke kantong peternak telur, petani sayur, dan ibu-ibu pengelola dapur umum. Semakin besar porsi uang yang dibelanjakan kembali oleh masyarakat bawah (*Marginal Propensity to Consume* / MPC), semakin kencang roda ekonomi berputar menciptakan PDB baru.")
    st.info(r"**Rumus:** $\Delta Y = \frac{1}{1 - MPC} \times \Delta G$")
    st.markdown("""
    * **$\Delta Y$**: Total penambahan Pendapatan Domestik Bruto (PDB) atau roda ekonomi.
    * **$MPC$**: *Marginal Propensity to Consume* (Kecenderungan masyarakat membelanjakan uangnya).
    * **$\Delta G$**: Anggaran MBG (Suntikan dana pemerintah).
    """)

with st.expander("3. Desentralisasi Ekonomi & Kapasitas Penerima", expanded=False):
    st.markdown("Selama ini perputaran uang tersentralisasi di kota besar. Dengan MBG, jika diasumsikan persentase besar bahan baku wajib dibeli dari UMKM dan petani lokal, maka terjadi transfer kekayaan besar-besaran ke **75.265 desa** di Indonesia. Program ini secara tidak langsung menciptakan lapangan kerja baru di daerah serta memperluas kapasitas jumlah anak yang gizinya terpenuhi.")
    st.info(r"**Rumus Uang Beredar per Desa:** $\frac{\text{Anggaran MBG} \times \% \text{Bahan Baku Lokal}}{\text{Jumlah Desa di Indonesia}}$")
    st.info(r"**Rumus Penerima Manfaat:** $\frac{\text{Total Anggaran}}{\text{Harga Per Porsi} \times \text{Hari Efektif Sekolah}}$")

st.divider()
st.caption("Kalkulator ini disusun menggunakan pendekatan ilmu ekonomi makro dan data riset lembaga internasional.")
