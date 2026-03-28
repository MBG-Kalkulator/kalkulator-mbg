import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Dampak MBG", page_icon="🍽️", layout="wide")

st.title("🍽️ Kalkulator Dampak Positif MBG")
st.write("Berbeda dengan narasi satir yang hanya melihat pengeluaran, mari kita hitung dampak ekonomi riil dan investasi SDM dari Program Makan Bergizi Gratis (MBG).")
st.caption("💡 Tips: Anda bisa menggeser tuas (slider) di bawah ini, atau klik pada angka di sebelah kanan tuas untuk mengetik angkanya secara manual.")

st.divider()

# --- BAGIAN INPUT PARAMETER ---
st.header("⚙️ Atur Parameter Simulasi")

col_input1, col_input2 = st.columns(2)

with col_input1:
    st.subheader("Parameter Anggaran & Ekonomi")
    anggaran_triliun = st.slider("Total Anggaran MBG (Triliun Rupiah)", min_value=1.0, max_value=400.0, value=71.0, step=1.0)
    mpc = st.slider("Kecenderungan Konsumsi Masyarakat (MPC)", min_value=0.50, max_value=0.99, value=0.75, step=0.01)
    persentase_lokal = st.slider("Persentase Anggaran untuk UMKM/Petani Lokal (%)", min_value=10, max_value=100, value=80, step=5)

with col_input2:
    st.subheader("Parameter Program & SDM")
    harga_porsi = st.slider("Harga per Porsi (Rupiah)", min_value=5000, max_value=30000, value=15000, step=500)
    hari_aktif = st.slider("Hari Efektif Sekolah (Setahun)", min_value=100, max_value=300, value=250, step=5)
    roi_sdm = st.slider("Asumsi ROI SDM Jangka Panjang (WFP & Rockefeller)", min_value=5, max_value=35, value=15, step=1, 
                        help="Studi WFP (2023) menyebut 1 USD investasi MBG kembali menjadi 5 - 35 USD dalam bentuk nilai tambah SDM seumur hidup.")

# Jumlah desa di Indonesia (konstanta, tapi bisa diubah jadi slider jika mau)
jumlah_desa = 75265 

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

# 3. Potensi Perputaran Uang di Daerah
uang_beredar_lokal = anggaran_rp * (persentase_lokal / 100)
uang_per_desa = uang_beredar_lokal / jumlah_desa
uang_per_desa_miliar = uang_per_desa / 1_000_000_000

# 4. Return on Investment (ROI) SDM Jangka Panjang (Berdasarkan WFP)
roi_sdm_rp = anggaran_rp * roi_sdm
roi_sdm_triliun = roi_sdm_rp / 1_000_000_000_000

# --- BAGIAN HASIL (METRICS) ---
st.header("📊 Hasil Proyeksi Dampak")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Penerima Manfaat", f"{penerima_juta:,.1f} Juta", "Anak Sekolah")
col2.metric("Uang Beredar per Desa", f"Rp {uang_per_desa_miliar:,.2f} M", f"{persentase_lokal}% Bahan Lokal")
col3.metric("Roda Ekonomi (PDB)", f"Rp {dampak_pdb_triliun:,.0f} T", f"Multiplier {multiplier:,.1f}x")
col4.metric("Nilai Tambah SDM (Masa Depan)", f"Rp {roi_sdm_triliun:,.0f} T", f"ROI {roi_sdm}x Lipat")

# --- BAGIAN PENJELASAN & RUMUS ---
st.divider()
st.header("📖 Penjelasan: Mengapa MBG adalah Investasi, Bukan Biaya?")

st.markdown("""
### 1. Nilai Tambah SDM Jangka Panjang (Framework WFP & Rockefeller)
Berdasarkan studi *UN World Food Programme (WFP)* dan *Rockefeller Institute* (2023), **setiap investasi 1 USD untuk program makanan bergizi di sekolah akan memberikan nilai kembalian (ROI) sebesar 5 hingga 35 USD.**
Hal ini terjadi karena efek berantai biologis dan akademis:
* **Fisik & Waktu di Sekolah:** Nutrisi menekan angka absen dan putus sekolah.
* **Kognitif:** Menurunnya defisiensi mikronutrien membuat anak lebih konsentrasi dan nilai ujian naik.
* **Hasil Akhir:** Pendidikan yang baik menghasilkan pekerjaan yang lebih baik. SDM yang sehat hidup produktif lebih lama, yang pada akhirnya **meningkatkan upah dan pendapatan seumur hidup**.

### 2. Efek Pengganda Ekonomi Makro (*Keynesian Multiplier*)
Dana MBG tidak "hangus" dimakan. Dana ini pindah dari kas negara ke kantong peternak telur, petani sayur, dan ibu-ibu pengelola dapur umum. 
* **Rumus:** `Multiplier = 1 / (1 - MPC)`
* Semakin besar porsi uang yang dibelanjakan kembali oleh masyarakat bawah (*Marginal Propensity to Consume* / MPC), semakin kencang roda ekonomi berputar menciptakan PDB baru.

### 3. Desentralisasi Ekonomi ke Desa
Selama ini uang berputar di Jakarta. Dengan MBG, jika kita asumsikan persentase besar bahan baku wajib dibeli dari UMKM dan petani lokal, maka terjadi transfer kekayaan besar-besaran ke puluhan ribu desa di Indonesia. Program ini secara tidak langsung menciptakan **lapangan kerja baru, terutama untuk wanita/ibu-ibu** di daerah, serta membiasakan anak pada **pangan lokal sehat**.
""")

st.caption("Kalkulator tandingan ini dibuat berdasarkan ilmu ekonomi makro dan riset lembaga internasional (WFP PBB) untuk mengedukasi masyarakat.")
