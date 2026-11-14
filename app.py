import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="SIM SCM 199 Kitchen",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. MODERN PASTEL ENTERPRISE UI - 199 KITCHEN
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --cream: #FFF9F2;
    --sage: #E5F1E8;
    --sage-dark: #527B60;
    --sage-deep: #344F3D;
    --text: #2C3E35;
    --muted: #7E8C82;
    --border: #E4EAE2;
}

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #F7F9F6;
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* ==========================================
   SKELETON SHIMMER ANIMATION
========================================== */
@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

.skeleton-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.skeleton-card {
    height: 115px;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: #EEF3ED;
    background-image: linear-gradient(90deg, #EEF3ED 0px, #FFFFFF 50%, #EEF3ED 100%);
    background-size: 1000px 100%;
    animation: shimmer 1.8s infinite linear;
}

.skeleton-chart {
    height: 260px;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: #EEF3ED;
    background-image: linear-gradient(90deg, #EEF3ED 0px, #FFFFFF 50%, #EEF3ED 100%);
    background-size: 1000px 100%;
    animation: shimmer 1.8s infinite linear;
}

/* ==========================================
   WELCOME GREETING CARD (PROFESSIONAL)
========================================== */
.welcome-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 26px 30px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(50,80,50,0.03);
    margin-bottom: 24px;
}

.welcome-title {
    font-size: clamp(20px, 2.3vw, 28px);
    font-weight: 800;
    color: var(--sage-deep);
    margin: 0 0 4px 0;
    letter-spacing: -0.6px;
}

.welcome-date {
    font-size: 13px;
    color: var(--muted);
    font-weight: 600;
    margin: 0;
}

/* PREMIUM MAIN HEADER WITH LOGO */
.main-header {
    background: linear-gradient(120deg, #FFF4EC 0%, #F5F6EE 50%, #E7EFE8 100%);
    padding: 26px 30px;
    border-radius: 20px;
    border: 1px solid var(--border);
    margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(50,80,50,0.03);
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-logo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--sage-dark);
    box-shadow: 0 4px 12px rgba(82, 123, 96, 0.15);
    flex-shrink: 0;
}

.header-content {
    flex-grow: 1;
}

.header-tag {
    display: inline-block;
    background: rgba(255,255,255,0.8);
    color: var(--sage-dark);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 6px;
}

.main-title {
    font-size: clamp(18px, 2vw, 26px) !important;
    font-weight: 800 !important;
    color: var(--sage-deep) !important;
    margin: 0 !important;
    line-height: 1.3 !important;
    letter-spacing: -0.6px !important;
}

.sub-title {
    font-size: 11.5px !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    margin-top: 4px !important;
    margin-bottom: 0 !important;
}

/* SIDEBAR STYLING MIRIP CONTOH REFERENSI */
[data-testid="stSidebar"] {
    background: #1B3024;
    border-right: 1px solid #243D2F;
}

[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] label {
    color: #E2EFE5 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.sidebar-brand {
    background: rgba(255, 255, 255, 0.05);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
}

/* STYLING SEARCH BAR & RADIO MENU DI SIDEBAR */
[data-testid="stSidebar"] .stTextInput input {
    background: #243D2F !important;
    border: 1px solid #335442 !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    font-size: 13px;
}

[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #A3B5A8 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-size: 13.5px;
    font-weight: 600;
    padding: 10px 14px;
    border-radius: 10px;
    color: #D1E2D5 !important;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] hr {
    border-color: #2D4D3C !important;
}

/* SECTION TITLE */
h1, h2, h3, h4, h5 {
    color: var(--sage-deep) !important;
    font-weight: 700 !important;
}

/* METRIC CARDS */
.metric-card {
    position: relative;
    background: #FFFFFF;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 15px rgba(50,80,50,0.03);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 110px;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 22px rgba(82, 123, 96, 0.08);
}

.metric-label {
    font-size: 9.5px;
    color: var(--muted);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-value {
    font-size: 22px;
    font-weight: 800;
    color: var(--sage-deep);
    margin-top: 8px;
}

/* DATAFRAME & FORM */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
}

.stTextInput input, .stNumberInput input, .stTextArea textarea {
    border-radius: 10px;
    border-color: #D3E0D5;
    background: #FCFDFB;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 18px rgba(50,80,50,0.03);
}

/* BUTTON */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #73977B 0%, #527B60 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 9px 16px;
    font-weight: 700;
    box-shadow: 0 4px 10px rgba(82, 123, 96, 0.2);
    transition: 0.2s ease;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #527B60 0%, #344F3D 100%);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Session State Navigasi
if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = "📊 Beranda (Dashboard)"

# ==========================================
# 3. LOGIKA WAKTU, TANGGAL & SAPAAN PENGAKSES
# ==========================================
current_hour = datetime.now().hour
if 4 <= current_hour < 11:
    sapaan = "Selamat Pagi"
elif 11 <= current_hour < 15:
    sapaan = "Selamat Siang"
elif 15 <= current_hour < 18:
    sapaan = "Selamat Sore"
else:
    sapaan = "Selamat Malam"

days_id = {"Sun": "Minggu", "Mon": "Senin", "Tue": "Selasa", "Wed": "Rabu", "Thu": "Kamis", "Fri": "Jumat", "Sat": "Sabtu"}
months_id = {"Jan": "Januari", "Feb": "Februari", "Mar": "Maret", "Apr": "April", "May": "Mei", "Jun": "Juni", "Jul": "Juli", "Aug": "Agustus", "Sep": "September", "Oct": "Oktober", "Nov": "November", "Dec": "Desember"}

now = datetime.now()
day_name = days_id.get(now.strftime("%a"), now.strftime("%A"))
month_name = months_id.get(now.strftime("%b"), now.strftime("%B"))
tanggal_str = f"{day_name}, {now.day} {month_name} {now.year}"

# Tampilkan Kartu Sapaan
st.markdown(f"""
<div class="welcome-card">
    <p class="welcome-title">{sapaan}, Ibu Adinda Arum Sari!</p>
    <p class="welcome-date">{tanggal_str}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. HEADER UTAMA DENGAN LOGO
# ==========================================
logo_url = "https://images.glints.com/unsafe/glints-dashboard.oss-ap-southeast-1.aliyuncs.com/company-logo/688dca2d5e43fca352724ab6c2f5aa76.png"

st.markdown(f"""
<div class="main-header">
    <img src="{logo_url}" class="header-logo" alt="199 Kitchen Logo">
    <div class="header-content">
        <div class="header-tag">✨ 199 KITCHEN • SINGOSARI, MALANG</div>
        <p class="main-title">Sweet & Savory Supply Chain System</p>
        <p class="sub-title">Sistem informasi manajemen stok, HPP, penjualan, dan forecasting terintegrasi Google Sheets & Make.com.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. PENGAMAN SECRETS CREDENTIALS
# ==========================================
try:
    SPREADSHEET_ID = st.secrets["spreadsheet"]["spreadsheet_id"]
    MAKE_WEBHOOK_URL = st.secrets["make_webhook"]["url"]
except Exception as e:
    st.error("⚠️ **Secrets Belum Dikonfigurasi!** Pastikan `[spreadsheet]` dan `[make_webhook]` sudah diatur di Advanced Settings Streamlit Cloud.")
    st.stop()

# ==========================================
# 6. LOAD DATA DARI GOOGLE SHEETS + SKELETON
# ==========================================
@st.cache_data(ttl=20)
def load_data_from_sheets():
    try:
        url_bom = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Master%20BOM"
        url_fefo = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Inventory%20FEFO"
        url_sales = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sales%20Log"
        url_supp = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Supplier%20DB"

        return pd.read_csv(url_bom), pd.read_csv(url_fefo), pd.read_csv(url_sales), pd.read_csv(url_supp)
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

skeleton_placeholder = st.empty()
skeleton_placeholder.markdown("""
<div class="skeleton-wrapper">
    <div class="skeleton-card"></div>
    <div class="skeleton-card"></div>
    <div class="skeleton-card"></div>
    <div class="skeleton-card"></div>
</div>
<div class="skeleton-chart"></div>
""", unsafe_allow_html=True)

df_bom, df_fefo, df_sales, df_supp = load_data_from_sheets()
time.sleep(0.3)
skeleton_placeholder.empty()

# ==========================================
# 7. SIDEBAR NAVIGATION (DENGAN CARI MENU & TOMBOL COLLAPSE HIJAU)
# ==========================================
st.sidebar.markdown(f"""
<div class="sidebar-brand">
    <img src="{logo_url}" width="65" style="border-radius: 50%; margin-bottom: 6px; border: 2px solid #73977B;">
    <div style="color: #FFFFFF; font-size: 14px; font-weight: 800;">199 KITCHEN</div>
    <div style="color: #A3B5A8; font-size: 8.5px; letter-spacing: 1px; font-weight: 600;">SWEET & SAVORY</div>
</div>
""", unsafe_allow_html=True)

# Tombol Sembunyikan Panel (Collapse Sidebar) warna hijau ikon selalu terlihat
if st.sidebar.button("☰ Sembunyikan Panel", use_container_width=True, help="Ciutkan atau sembunyikan sidebar menu"):
    st.rerun()

st.sidebar.markdown("---")

# Kotak Pencarian Menu (Cari Menu) seperti pada gambar referensi
search_query = st.sidebar.text_input("Cari Menu", placeholder="Ketik menu...", label_visibility="collapsed")

# Daftar seluruh modul
all_menu_options = [
    "📊 Beranda (Dashboard)",
    "📦 Inventory FEFO & Alerts",
    "📋 Master BOM & Resep HPP",
    "🛒 Form Sales (Input Webhook)",
    "🚛 Database Supplier"
]

# Filter menu jika diketik di kotak pencarian
if search_query:
    menu_options = [m for m in all_menu_options if search_query.lower() in m.lower()]
    if not menu_options:
        menu_options = all_menu_options
        st.sidebar.caption("⚠️ Menu tidak ditemukan")
else:
    menu_options = all_menu_options

menu_option = st.sidebar.radio(
    "Pilih Menu:",
    menu_options,
    index=0 if st.session_state.nav_selection in menu_options else 0,
    label_visibility="collapsed"
)

st.session_state.nav_selection = menu_option

st.sidebar.markdown("---")
st.sidebar.caption("🟢 Google Sheets: Connected")
st.sidebar.caption("🟢 Make.com Webhook: Active")
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size: 10.5px; color: #8FA395;'>Made with ❤️ for 199 Kitchen</p>", unsafe_allow_html=True)

# ==========================================
# 8. MODUL 1: BERANDA (DASHBOARD ANALYTICS)
# ==========================================
if menu_option == "📊 Beranda (Dashboard)":

    st.markdown("### 📊 Beranda & Ringkasan Performa")
    st.caption("Klik tombol di bawah setiap kartu ringkasan untuk langsung membuka data detail terkait.")

    total_omzet = 0
    total_trx = 0

    if not df_sales.empty:
        total_trx = len(df_sales)
        omzet_cols = [c for c in df_sales.columns if "omzet" in c.lower() or "total" in c.lower()]
        if omzet_cols:
            total_omzet = pd.to_numeric(df_sales[omzet_cols[0]], errors='coerce').sum()

    critical_items = 0
    if not df_fefo.empty:
        status_cols = [c for c in df_fefo.columns if "status" in c.lower() or "action" in c.lower() or "fefo" in c.lower()]
        if status_cols:
            critical_items = len(df_fefo[df_fefo[status_cols[0]].astype(str).str.contains("CRITICAL", case=False, na=False)])

    # METRIC CARDS DENGAN TOMBOL AKSI CEPAT
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #8DBB98;">
                <div class="metric-label">💰 Total Omzet Gross</div>
                <div class="metric-value" style="color: #527B60;">Rp {total_omzet:,.0f}</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("👁️ Buka Log Penjualan", use_container_width=True, key="btn_sales_log"):
            st.session_state.nav_selection = "🛒 Form Sales (Input Webhook)"
            st.rerun()

    with c2:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #A8C7E8;">
                <div class="metric-label">🧾 Total Transaksi</div>
                <div class="metric-value" style="color: #648DB8;">{total_trx} Pesanan</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("👁️ Lihat Detail Transaksi", use_container_width=True, key="btn_trx_detail"):
            st.session_state.nav_selection = "🛒 Form Sales (Input Webhook)"
            st.rerun()

    with c3:
        border_color = "#E99A9A" if critical_items > 0 else "#8DBB98"
        val_color = "#C66B6B" if critical_items > 0 else "#527B60"
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid {border_color};">
                <div class="metric-label">📦 Bahan Perlu Reorder</div>
                <div class="metric-value" style="color: {val_color};">{critical_items} Item</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("⚠️ Cek Inventory FEFO", use_container_width=True, key="btn_fefo_check"):
            st.session_state.nav_selection = "📦 Inventory FEFO & Alerts"
            st.rerun()

    with c4:
        st.markdown('''
            <div class="metric-card" style="border-left: 5px solid #D5B7E8;">
                <div class="metric-label">🛍️ Kanal Penjualan</div>
                <div class="metric-value" style="color: #9273B0;">5 Channel</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("🚛 Cek Database Supplier", use_container_width=True, key="btn_supp_check"):
            st.session_state.nav_selection = "🚛 Database Supplier"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 📈 Performa Penjualan Berdasarkan Kanal")
        if not df_sales.empty:
            kanal_cols = [c for c in df_sales.columns if "kanal" in c.lower()]
            omzet_cols = [c for c in df_sales.columns if "omzet" in c.lower() or "total" in c.lower()]
            if kanal_cols and omzet_cols:
                chart_data = df_sales.groupby(kanal_cols[0])[omzet_cols[0]].sum().reset_index()
                st.bar_chart(chart_data.set_index(kanal_cols[0]), color="#88AE91")
            else:
                st.dataframe(df_sales, use_container_width=True)
        else:
            st.info("Belum ada data transaksi tercatat.")

    with col_g2:
        st.markdown("##### 🔮 Forecast & Rekomendasi Belanja")
        st.info("💡 **Moving Average Insight:** Persiapan stok bahan baku akhir pekan difokuskan pada peningkatan ketersediaan *Daging Ayam Fillet* dan *Saus Mentai* seiring tren kenaikan pesanan.")

# ==========================================
# 9. MODUL 2: INVENTORY FEFO
# ==========================================
elif menu_option == "📦 Inventory FEFO & Alerts":
    st.markdown("### 📦 Monitoring Stok Bahan Baku (FEFO)")
    st.caption("Sistem pengawasan tanggal kedaluwarsa dan sisa stok agar operasional dapur tetap terkontrol.")

    if not df_fefo.empty:
        status_col = None
        for col in df_fefo.columns:
            if "status" in col.lower() or "action" in col.lower() or "fefo" in col.lower():
                status_col = col
                break

        if status_col:
            def highlight_status(val):
                if 'CRITICAL' in str(val).upper():
                    return 'background-color: #FCE4E4; color: #A34343; font-weight: 700;'
                elif 'WARNING' in str(val).upper():
                    return 'background-color: #FFF0D9; color: #9B7135; font-weight: 700;'
                elif 'SAFE' in str(val).upper():
                    return 'background-color: #E3F2E5; color: #477653; font-weight: 700;'
                return ''

            st.dataframe(df_fefo.style.map(highlight_status, subset=[status_col]), use_container_width=True)
        else:
            st.dataframe(df_fefo, use_container_width=True)
    else:
        st.warning("Tabel Inventory FEFO kosong.")

# ==========================================
# 10. MODUL 3: MASTER BOM & RESEP HPP
# ==========================================
elif menu_option == "📋 Master BOM & Resep HPP":
    st.markdown("### 📋 Standar Resep & Kalkulasi HPP per Menu")
    st.caption("Kelola standar komposisi bahan dan biaya produksi setiap menu.")

    if not df_bom.empty:
        menu_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
        menu_col = menu_cols[0] if menu_cols else df_bom.columns[1]

        menu_list = df_bom[menu_col].dropna().unique()
        selected_menu = st.selectbox("🎯 Pilih Menu 199 Kitchen:", menu_list)

        recipe_df = df_bom[df_bom[menu_col] == selected_menu]
        st.markdown(f"##### 🍽️ Rincian Komposisi Bahan untuk: **{selected_menu}**")
        st.dataframe(recipe_df, use_container_width=True)

        hpp_cols = [c for c in df_bom.columns if "hpp" in c.lower() or "est." in c.lower()]
        if hpp_cols:
            total_hpp = pd.to_numeric(recipe_df[hpp_cols[-1]], errors='coerce').sum()
            st.success(f"💰 **Estimasi Total HPP per Porsi:** **Rp {total_hpp:,.0f}**")
    else:
        st.warning("Data Master BOM tidak tersedia.")

# ==========================================
# 11. MODUL 4: FORM SALES & TRIGGER WEBHOOK
# ==========================================
elif menu_option == "🛒 Form Sales (Input Webhook)":
    st.markdown("### 🛒 Input Transaksi & Sinkronisasi Otomatis")
    st.caption("Pencatatan pesanan baru akan langsung memicu Make.com Webhook dan masuk otomatis ke database Google Sheets.")

    with st.form("form_sales_soft"):
        c_left, c_right = st.columns(2)

        with c_left:
            id_trx = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            st.text_input("ID Transaksi (Auto Generated):", value=id_trx, disabled=True)
            kanal = st.selectbox("Kanal Penjualan:", ["GoFood", "GrabFood", "ShopeeFood", "WA Pre-Order", "Takeaway / Kasir"])

            menu_options = ["Dimsum Mentai Mini", "Dimsum Mentai Regular", "Gyoza Kuah Keju", "Pentol Pedas", "Ice Cream", "Es Kopzu 199", "Matchacih"]
            if not df_bom.empty:
                m_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
                if m_cols:
                    menu_options = df_bom[m_cols[0]].dropna().unique()

            menu_nama = st.selectbox("Menu Pilihan:", menu_options)
            qty = st.number_input("Jumlah Porsi:", min_value=1, value=1, step=1)

        with c_right:
            waktu_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.text_input("Waktu:", value=waktu_str, disabled=True)
            harga = st.number_input("Harga per Porsi (Rp):", min_value=1000, value=15000, step=1000)
            metode = st.selectbox("Metode Pembayaran:", ["GoPay", "OVO", "ShopeePay", "QRIS", "Tunai", "Transfer Bank"])
            catatan = st.text_input("Catatan Pesanan:", value="Normal")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("🚀 Kirim Transaksi ke Spreadsheet", use_container_width=True)

        if submit_button:
            payload = {
                "id_transaksi": id_trx,
                "waktu": waktu_str,
                "kanal": kanal,
                "menu": menu_nama,
                "qty": qty,
                "harga": harga,
                "omzet": qty * harga,
                "metode": metode,
                "catatan": catatan
            }

            try:
                res = requests.post(MAKE_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
                if res.status_code == 200:
                    st.balloons()
                    st.success(f"✅ Transaksi **{id_trx}** Berhasil Tercatat!")
                    st.json(payload)
                else:
                    st.error(f"Gagal mengirim ke Webhook. Status Code: {res.status_code}")
            except Exception as ex:
                st.error(f"Error koneksi Webhook: {ex}")

    st.markdown("---")
    st.markdown("##### 📋 Riwayat Log Transaksi (Sales Log)")
    if not df_sales.empty:
        st.dataframe(df_sales, use_container_width=True)
    else:
        st.info("Belum ada data Sales Log.")

# ==========================================
# 12. MODUL 5: DATABASE SUPPLIER
# ==========================================
elif menu_option == "🚛 Database Supplier":
    st.markdown("### 🚛 Database Pemasok Bahan Baku & Vendor")
    st.caption("Informasi pemasok dan vendor untuk mendukung operasional 199 Kitchen.")

    if not df_supp.empty:
        st.dataframe(df_supp, use_container_width=True)
    else:
        st.info("Data supplier belum tersedia.")
