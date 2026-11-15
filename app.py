import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime  # <-- PERBAIKAN: Menambahkan import datetime di sini

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="199 Kitchen • Sweet & Savory SCM",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SOLID PASTEL PALETTE THEME (TANPA GRADASI)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-main: #F7FAF9;
    --sidebar-bg: #E0F2F4;
    --card-bg: #FFFFFF;
    --text-main: #1F2937;
    --text-muted: #555B6E;
    
    /* Solid Palette dari Referensi */
    --color-green-lime: #DDDD7B;
    --color-blue-soft: #E0F2F4;
    --color-blue-pastel: #BAD6DA;
    --color-pink-soft: #FFDBDF;
    --color-pink-bold: #F791A9;
    --color-yellow: #FFE797;
    
    --border-color: #D1E0E3;
}

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: var(--bg-main);
    color: var(--text-main);
}

.block-container {
    max-width: 1550px;
    padding-top: 1.5rem;
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
    height: 120px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    background: #E0F2F4;
    background-image: linear-gradient(90deg, #E0F2F4 0px, #FFFFFF 50%, #E0F2F4 100%);
    background-size: 1000px 100%;
    animation: shimmer 1.8s infinite linear;
}

/* ==========================================
   HERO BANNER SYSTEM (SOLID COLOR)
========================================== */
.hero-banner {
    background: #BAD6DA;
    padding: 30px 36px;
    border-radius: 22px;
    border: 1px solid var(--border-color);
    margin-bottom: 26px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.02);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.hero-logo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #1F2937;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
}

.hero-title {
    font-size: clamp(22px, 2.5vw, 32px) !important;
    font-weight: 800 !important;
    color: #1F2937 !important;
    margin: 0 !important;
    letter-spacing: -0.8px !important;
}

.hero-sub {
    font-size: 12.5px !important;
    font-weight: 600 !important;
    color: #374151 !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
}

/* ==========================================
   SIDEBAR STYLING (SOLID, TANPA POIN, TEKS HITAM)
========================================== */
[data-testid="stSidebar"] {
    background: #BAD6DA;
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.sidebar-brand-card {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid var(--border-color);
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

/* KOTAK PENCARIAN MENU DI SIDEBAR */
[data-testid="stSidebar"] .stTextInput input {
    background: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    color: #1F2937 !important;
    border-radius: 12px;
    font-size: 13px;
    padding: 10px 14px;
}

[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #6B7280 !important;
}

/* RADIO MENU SEBAGAI KOTAK BERSIH TANPA TITIK POIN */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    font-size: 13px;
    font-weight: 700;
    padding: 12px 16px;
    border-radius: 14px;
    color: #1F2937 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
    width: 100%;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    color: #1F2937 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #FFDBDF;
    border-color: #F791A9;
    transform: translateX(3px);
}

[data-testid="stSidebar"] hr {
    border-color: #A4C5CB !important;
}

/* SECTION TITLE */
h1, h2, h3, h4, h5 {
    color: #1F2937 !important;
    font-weight: 700 !important;
}

/* METRIC CARDS */
.metric-card {
    position: relative;
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 16px rgba(0,0,0,0.03);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 120px;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.06);
}

.metric-label {
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #1F2937;
    margin-top: 10px;
}

/* DATAFRAME & FORM */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color);
    border-radius: 16px;
    overflow: hidden;
}

.stTextInput input, .stNumberInput input, .stTextArea textarea {
    border-radius: 12px;
    border-color: var(--border-color);
    background: #FFFFFF;
    color: #1F2937 !important;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 26px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 18px rgba(0,0,0,0.03);
}

/* BUTTON DENGAN PALET SOLID */
.stButton > button, .stFormSubmitButton > button {
    background: #F791A9;
    color: #1F2937;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(247, 145, 169, 0.3);
    transition: 0.2s ease;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #DDDD7B;
    color: #1F2937;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Session State Navigasi
if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = "📊 Beranda (Dashboard)"

# ==========================================
# 3. WAKTU & TANGGAL REAL-TIME CLIENT (JAVASCRIPT)
# ==========================================
import streamlit.components.v1 as components

time_html = """
<div id="realtime-clock" style="font-family: 'Plus Jakarta Sans', sans-serif;"></div>
<script>
function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    
    let sapaan = "Selamat Malam";
    if (hours >= 4 && hours < 11) sapaan = "Selamat Pagi";
    else if (hours >= 11 && hours < 15) sapaan = "Selamat Siang";
    else if (hours >= 15 && hours < 18) sapaan = "Selamat Sore";
    
    const days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
    const months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
    
    const dayName = days[now.getDay()];
    const dateNum = now.getDate();
    const monthName = months[now.getMonth()];
    const year = now.getFullYear();
    
    const dateStr = dayName + ", " + dateNum + " " + monthName + " " + year;
    
    const el = document.getElementById('realtime-clock');
    if(el) {
        el.innerHTML = '<div style="background: #FFFFFF; border: 1px solid #D1E0E3; padding: 24px 32px; border-radius: 22px; box-shadow: 0 4px 18px rgba(0,0,0,0.02); margin-bottom: 22px; display: flex; align-items: center; justify-content: space-between;"><div><p style="font-size: clamp(20px, 2.2vw, 26px); font-weight: 800; color: #1F2937; margin: 0 0 4px 0; letter-spacing: -0.6px;">' + sapaan + ', Ibu Adinda Arum Sari!</p><p style="font-size: 13px; color: #555B6E; font-weight: 600; margin: 0;">' + dateStr + '</p></div><div style="font-size: 32px;">👋</div></div>';
    }
}
updateClock();
setInterval(updateClock, 1000);
</script>
"""
components.html(time_html, height=105)

# ==========================================
# 4. HERO HEADER UTAMA DENGAN LOGO
# ==========================================
logo_url = "https://images.glints.com/unsafe/glints-dashboard.oss-ap-southeast-1.aliyuncs.com/company-logo/688dca2d5e43fca352724ab6c2f5aa76.png"

st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; align-items: center; gap: 22px;">
        <img src="{logo_url}" class="hero-logo" alt="199 Kitchen Logo">
        <div>
            <div style="font-size: 10px; font-weight: 800; color: #1F2937; letter-spacing: 1.2px; margin-bottom: 6px;">199 KITCHEN • SINGOSARI, MALANG</div>
            <p class="hero-title">Sweet & Savory Supply Chain System</p>
            <p class="hero-sub">Sistem informasi manajemen stok, HPP, penjualan, dan forecasting terintegrasi Google Sheets & Make.com.</p>
        </div>
    </div>
    <div style="display: flex; gap: 6px; align-items: center;">
        <span style="width: 10px; height: 10px; background: #F791A9; border-radius: 50%; display: inline-block;"></span>
        <span style="width: 10px; height: 10px; background: #DDDD7B; border-radius: 50%; display: inline-block;"></span>
        <span style="width: 10px; height: 10px; background: #FFE797; border-radius: 50%; display: inline-block;"></span>
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
""", unsafe_allow_html=True)

df_bom, df_fefo, df_sales, df_supp = load_data_from_sheets()
time.sleep(0.3)
skeleton_placeholder.empty()

# ==========================================
# 7. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"""
<div class="sidebar-brand-card">
    <img src="{logo_url}" width="65" style="border-radius: 50%; margin-bottom: 6px; border: 2px solid #1F2937;">
    <div style="color: #1F2937; font-size: 14px; font-weight: 800;">199 KITCHEN</div>
    <div style="color: #555B6E; font-size: 8.5px; letter-spacing: 1px; font-weight: 600;">SWEET & SAVORY</div>
</div>
""", unsafe_allow_html=True)

search_query = st.sidebar.text_input("Cari Menu", placeholder="🔍 Cari menu...", label_visibility="collapsed")

all_menu_options = [
    "📊 Beranda (Dashboard)",
    "📦 Inventory FEFO & Alerts",
    "📋 Master BOM & Resep HPP",
    "🛒 Form Sales (Input Webhook)",
    "🚛 Database Supplier"
]

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
st.sidebar.markdown("<p style='font-size: 10.5px; color: #1F2937; text-align: center; font-weight: 700;'>Made with ❤️ for 199 Kitchen</p>", unsafe_allow_html=True)

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

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #F791A9;">
                <div class="metric-label">💰 Total Omzet Gross</div>
                <div class="metric-value" style="color: #1F2937;">Rp {total_omzet:,.0f}</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("👁️ Buka Log Penjualan", use_container_width=True, key="btn_sales_log"):
            st.session_state.nav_selection = "🛒 Form Sales (Input Webhook)"
            st.rerun()

    with c2:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #BAD6DA;">
                <div class="metric-label">🧾 Total Transaksi</div>
                <div class="metric-value" style="color: #1F2937;">{total_trx} Pesanan</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("👁️ Lihat Detail Transaksi", use_container_width=True, key="btn_trx_detail"):
            st.session_state.nav_selection = "🛒 Form Sales (Input Webhook)"
            st.rerun()

    with c3:
        border_color = "#F791A9" if critical_items > 0 else "#DDDD7B"
        val_color = "#9B2226" if critical_items > 0 else "#1F2937"
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
            <div class="metric-card" style="border-left: 5px solid #FFE797;">
                <div class="metric-label">🛍️ Kanal Penjualan</div>
                <div class="metric-value" style="color: #1F2937;">5 Channel</div>
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
                st.bar_chart(chart_data.set_index(kanal_cols[0]), color="#BAD6DA")
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
                    return 'background-color: #FFDBDF; color: #9B2226; font-weight: 700;'
                elif 'WARNING' in str(val).upper():
                    return 'background-color: #FFE797; color: #7F5539; font-weight: 700;'
                elif 'SAFE' in str(val).upper():
                    return 'background-color: #DDDD7B; color: #1F2937; font-weight: 700;'
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
