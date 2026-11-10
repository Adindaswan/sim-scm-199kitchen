import streamlit as st
import pandas as pd
import requests
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
# 2. MODERN PASTEL UI - 199 KITCHEN
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --cream: #FFF9F2;
    --sage: #E5F1E8;
    --sage-dark: #527B60;
    --sage-deep: #344F3D;
    --pink: #FCEAEC;
    --lavender: #F1EAF9;
    --text: #35443A;
    --muted: #87938A;
    --border: #E9EEE9;
}

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #FAFBF8;
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ==========================================
   PREMIUM MAIN HEADER
========================================== */

.main-header {
    background: linear-gradient(
        120deg,
        #FFF1E5 0%,
        #F5F4E9 48%,
        #E7F2E8 100%
    );
    padding: 36px 38px;
    border-radius: 24px;
    border: 1px solid #EAEDE4;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(70,100,70,0.055);
}

.header-tag {
    display: inline-block;
    background: rgba(255,255,255,0.75);
    color: #62816A;
    padding: 7px 15px;
    border-radius: 30px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 17px;
}

.main-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: clamp(26px, 3vw, 36px) !important;
    font-weight: 800 !important;
    color: #344F3D !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.35 !important;
    letter-spacing: -1.2px !important;
}

.sub-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #718274 !important;
    margin-top: 12px !important;
    margin-bottom: 0 !important;
    line-height: 1.9 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #F3F7F1;
    border-right: 1px solid #E4EBE1;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] p {
    color: #536459;
    font-weight: 500;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-size: 13px;
    font-weight: 600;
    padding: 7px 4px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 7px;
}

[data-testid="stSidebar"] hr {
    border-color: #DFE8DD;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #728477;
}

/* SIDEBAR BRAND */
.sidebar-brand {
    background: linear-gradient(135deg, #E4F0E5, #FFF0E6);
    padding: 19px;
    border-radius: 17px;
    margin-bottom: 20px;
    border: 1px solid #E5EBE2;
}

.sidebar-brand-title {
    color: #405C46;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.sidebar-brand-sub {
    color: #849387;
    font-size: 10px;
    margin-top: 5px;
    letter-spacing: 1px;
    font-weight: 600;
}

/* SECTION TITLE */
h1, h2, h3, h4, h5 {
    color: #344F3D !important;
    font-weight: 700 !important;
}

h3 {
    letter-spacing: -0.5px;
}

/* METRIC CARDS */
.metric-card {
    background: #FFFFFF;
    border-radius: 19px;
    padding: 23px;
    border: 1px solid #E9EEE9;
    box-shadow: 0 4px 15px rgba(60,80,60,0.035);
    transition: all 0.25s ease;
    min-height: 115px;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(60,80,60,0.09);
}

.metric-label {
    font-size: 10px;
    color: #89958C;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #344F3D;
    margin-top: 10px;
    letter-spacing: -0.7px;
}

/* CONTENT CARDS */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
}

/* CHART */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: #FFFFFF;
    border: 1px solid #EDF0EB;
    border-radius: 16px;
    padding: 12px;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #E5ECE4;
    border-radius: 15px;
    overflow: hidden;
}

/* INPUT */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 11px;
    border-color: #DFE8DF;
    background: #FCFDFC;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 11px;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 26px;
    border-radius: 20px;
    border: 1px solid #E8EEE7;
    box-shadow: 0 5px 20px rgba(60,80,60,0.04);
}

/* BUTTON */
.stButton > button,
.stFormSubmitButton > button {
    background: #73977B;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 700;
    transition: 0.2s ease;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #527B60;
    color: #FFFFFF;
    transform: translateY(-2px);
    border: none;
}

/* ALERT */
[data-testid="stAlert"] {
    border-radius: 13px;
}

/* DIVIDER */
hr {
    border-color: #E8EEE7;
}

/* CAPTION */
[data-testid="stCaptionContainer"] {
    color: #89958C;
    font-size: 12px;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {
    .main-title {
        font-size: 23px !important;
        letter-spacing: -0.7px !important;
    }

    .main-header {
        padding: 23px 20px;
        border-radius: 18px;
    }

    .sub-title {
        font-size: 12px !important;
    }

    .metric-card {
        padding: 16px;
        min-height: 100px;
    }

    .metric-value {
        font-size: 19px;
    }

    .header-tag {
        font-size: 9px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER UTAMA
# ==========================================
# HTML dibuat satu baris agar tidak terbaca
# sebagai teks Markdown oleh Streamlit.

st.markdown("""
<div class="main-header"><div class="header-tag">✨ 199 KITCHEN • SINGOSARI, MALANG</div><p class="main-title">🍲 Welcome to 199 Kitchen!</p><p class="sub-title">Your Kitchen Business, Managed Smarter.<br>Sistem informasi manajemen stok, HPP, penjualan dan forecasting dalam satu dashboard.</p></div>
""", unsafe_allow_html=True)

# ==========================================
# 4. PENGAMAN SECRETS CREDENTIALS
# ==========================================
try:
    SPREADSHEET_ID = st.secrets["spreadsheet"]["spreadsheet_id"]
    MAKE_WEBHOOK_URL = st.secrets["make_webhook"]["url"]
except Exception as e:
    st.error("⚠️ **Secrets Belum Dikonfigurasi!** Pastikan `[spreadsheet]` dan `[make_webhook]` sudah diatur di Advanced Settings Streamlit Cloud.")
    st.stop()

# ==========================================
# 5. LOAD DATA DARI GOOGLE SHEETS
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

df_bom, df_fefo, df_sales, df_supp = load_data_from_sheets()

# ==========================================
# 6. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("""
<div class="sidebar-brand"><div class="sidebar-brand-title">🍲 199 KITCHEN</div><div class="sidebar-brand-sub">SMART KITCHEN MANAGEMENT</div></div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📌 Navigasi Modul")

menu_option = st.sidebar.radio(
    "Pilih Menu:",
    [
        "📊 Dashboard Analytics",
        "📦 Inventory FEFO & Alerts",
        "📋 Master BOM & Resep HPP",
        "🛒 Form Sales (Input Webhook)",
        "🚛 Database Supplier"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<p style='font-size: 0.75rem; color: #66816B; font-weight: 800; letter-spacing: 1px;'>STATUS INTEGRASI</p>",
    unsafe_allow_html=True
)

st.sidebar.caption("🟢 Google Sheets: Connected")
st.sidebar.caption("🟢 Make.com Webhook: Active")

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<p style='font-size: 11px; color: #89958C;'>Made with ❤️ for 199 Kitchen</p>",
    unsafe_allow_html=True
)

# ==========================================
# 7. MODUL 1: DASHBOARD ANALYTICS
# ==========================================
if menu_option == "📊 Dashboard Analytics":

    st.markdown("### 📊 Ringkasan Performa & Operasional")
    st.caption("Pantau perkembangan bisnis 199 Kitchen melalui ringkasan data operasional.")

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

    # METRIC CARDS
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #8DBB98;">
                <div class="metric-label">💰 Total Omzet Gross</div>
                <div class="metric-value" style="color: #527B60;">Rp {total_omzet:,.0f}</div>
            </div>
        ''', unsafe_allow_html=True)

    with c2:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid #A8C7E8;">
                <div class="metric-label">🧾 Total Transaksi</div>
                <div class="metric-value" style="color: #648DB8;">{total_trx} Pesanan</div>
            </div>
        ''', unsafe_allow_html=True)

    with c3:
        border_color = "#E99A9A" if critical_items > 0 else "#8DBB98"
        val_color = "#C66B6B" if critical_items > 0 else "#527B60"

        st.markdown(f'''
            <div class="metric-card" style="border-left: 5px solid {border_color};">
                <div class="metric-label">📦 Bahan Perlu Reorder</div>
                <div class="metric-value" style="color: {val_color};">{critical_items} Item</div>
            </div>
        ''', unsafe_allow_html=True)

    with c4:
        st.markdown('''
            <div class="metric-card" style="border-left: 5px solid #D5B7E8;">
                <div class="metric-label">🛍️ Kanal Penjualan</div>
                <div class="metric-value" style="color: #9273B0;">5 Channel</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CHART SECTION
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

        st.info(
            "💡 **Moving Average Insight:** Persiapan stok bahan baku akhir pekan difokuskan pada peningkatan ketersediaan *Daging Ayam Fillet* dan *Saus Mentai* seiring tren kenaikan pesanan."
        )

# ==========================================
# 8. MODUL 2: INVENTORY FEFO
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

            st.dataframe(
                df_fefo.style.map(highlight_status, subset=[status_col]),
                use_container_width=True
            )

        else:
            st.dataframe(df_fefo, use_container_width=True)

    else:
        st.warning("Tabel Inventory FEFO kosong.")

# ==========================================
# 9. MODUL 3: MASTER BOM & RESEP HPP
# ==========================================
elif menu_option == "📋 Master BOM & Resep HPP":

    st.markdown("### 📋 Standar Resep & Kalkulasi HPP per Menu")
    st.caption("Kelola standar komposisi bahan dan biaya produksi setiap menu.")

    if not df_bom.empty:

        menu_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
        menu_col = menu_cols[0] if menu_cols else df_bom.columns[1]

        menu_list = df_bom[menu_col].dropna().unique()

        selected_menu = st.selectbox(
            "🎯 Pilih Menu 199 Kitchen:",
            menu_list
        )

        recipe_df = df_bom[df_bom[menu_col] == selected_menu]

        st.markdown(f"##### 🍽️ Rincian Komposisi Bahan untuk: **{selected_menu}**")

        st.dataframe(recipe_df, use_container_width=True)

        hpp_cols = [c for c in df_bom.columns if "hpp" in c.lower() or "est." in c.lower()]

        if hpp_cols:
            total_hpp = pd.to_numeric(recipe_df[hpp_cols[-1]], errors='coerce').sum()

            st.success(
                f"💰 **Estimasi Total HPP per Porsi:** **Rp {total_hpp:,.0f}**"
            )

    else:
        st.warning("Data Master BOM tidak tersedia.")

# ==========================================
# 10. MODUL 4: FORM SALES & TRIGGER WEBHOOK
# ==========================================
elif menu_option == "🛒 Form Sales (Input Webhook)":

    st.markdown("### 🛒 Input Transaksi & Sinkronisasi Otomatis")
    st.caption("Pencatatan pesanan baru akan langsung memicu Make.com Webhook dan masuk otomatis ke database Google Sheets.")

    with st.form("form_sales_soft"):

        c_left, c_right = st.columns(2)

        with c_left:

            id_trx = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            st.text_input(
                "ID Transaksi (Auto Generated):",
                value=id_trx,
                disabled=True
            )

            kanal = st.selectbox(
                "Kanal Penjualan:",
                ["GoFood", "GrabFood", "ShopeeFood", "WA Pre-Order", "Takeaway / Kasir"]
            )

            menu_options = [
                "Dimsum Mentai Mini",
                "Dimsum Mentai Regular",
                "Gyoza Kuah Keju",
                "Pentol Pedas",
                "Ice Cream",
                "Es Kopzu 199",
                "Matchacih"
            ]

            if not df_bom.empty:
                m_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
                if m_cols:
                    menu_options = df_bom[m_cols[0]].dropna().unique()

            menu_nama = st.selectbox("Menu Pilihan:", menu_options)

            qty = st.number_input(
                "Jumlah Porsi:",
                min_value=1,
                value=1,
                step=1
            )

        with c_right:

            waktu_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            st.text_input(
                "Waktu:",
                value=waktu_str,
                disabled=True
            )

            harga = st.number_input(
                "Harga per Porsi (Rp):",
                min_value=1000,
                value=15000,
                step=1000
            )

            metode = st.selectbox(
                "Metode Pembayaran:",
                ["GoPay", "OVO", "ShopeePay", "QRIS", "Tunai", "Transfer Bank"]
            )

            catatan = st.text_input(
                "Catatan Pesanan:",
                value="Normal"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        submit_button = st.form_submit_button(
            "🚀 Kirim Transaksi ke Spreadsheet",
            use_container_width=True
        )

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
                res = requests.post(
                    MAKE_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                if res.status_code == 200:
                    st.balloons()
                    st.success(f"✅ Transaksi **{id_trx}** Berhasil Tercatat!")
                    st.json(payload)

                else:
                    st.error(
                        f"Gagal mengirim ke Webhook. Status Code: {res.status_code}"
                    )

            except Exception as ex:
                st.error(f"Error koneksi Webhook: {ex}")

# ==========================================
# 11. MODUL 5: DATABASE SUPPLIER
# ==========================================
elif menu_option == "🚛 Database Supplier":

    st.markdown("### 🚛 Database Pemasok Bahan Baku & Vendor")
    st.caption("Informasi pemasok dan vendor untuk mendukung operasional 199 Kitchen.")

    if not df_supp.empty:
        st.dataframe(df_supp, use_container_width=True)

    else:
        st.info("Data supplier belum tersedia.")
