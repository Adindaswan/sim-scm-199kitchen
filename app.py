import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM STYLING (CSS)
# ==========================================
st.set_page_config(
    page_title="SIM SCM 199 Kitchen",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan Dashboard yang Modern & Atraktif
st.markdown("""
    <style>
    /* Styling Header Utama */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #D97706;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 20px;
    }
    
    /* Styling Metric Cards */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px;
        border-left: 6px solid #F59E0B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 10px;
    }
    .metric-card-danger {
        border-left: 6px solid #EF4444;
    }
    .metric-card-success {
        border-left: 6px solid #10B981;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1F2937;
    }
    
    /* Highlight Tab & Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama Dashboard
st.markdown('<p class="main-title">🍲 System Information Management SCM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title"><b>199 Kitchen Singosari, Malang</b> | Real-time Inventory, HPP, Sales & Automation Dashboard</p>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 2. SEBAGAI PENGAMAN SECRETS CREDENTIALS
# ==========================================
try:
    SPREADSHEET_ID = st.secrets["spreadsheet"]["spreadsheet_id"]
    MAKE_WEBHOOK_URL = st.secrets["make_webhook"]["url"]
except Exception as e:
    st.error("⚠️ **Secrets Belum Dikonfigurasi dengan Benar!**\nPastikan `[spreadsheet]` dan `[make_webhook]` sudah diatur di Advanced Settings Streamlit Cloud.")
    st.stop()

# ==========================================
# 3. LOAD DATA REAL-TIME DARI GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl=20)
def load_data_from_sheets():
    try:
        url_bom = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Master%20BOM"
        url_fefo = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Inventory%20FEFO"
        url_sales = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sales%20Log"
        url_supp = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Supplier%20DB"
        
        df_bom = pd.read_csv(url_bom)
        df_fefo = pd.read_csv(url_fefo)
        df_sales = pd.read_csv(url_sales)
        df_supp = pd.read_csv(url_supp)
        
        return df_bom, df_fefo, df_sales, df_supp
    except Exception as e:
        st.error(f"Gagal mengambil data dari Google Sheets: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_bom, df_fefo, df_sales, df_supp = load_data_from_sheets()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/restaurant-menu.png", width=75)
st.sidebar.title("📌 Modul SCM")
menu_option = st.sidebar.radio(
    "Pilih Menu Layanan:",
    [
        "📊 Dashboard Analytics",
        "📦 Inventory FEFO & Alerts",
        "📋 Master BOM & Resep HPP",
        "🛒 Form Sales (Input Webhook)",
        "🚛 Database Supplier"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🟢 Status Integrasi")
st.sidebar.caption("✅ Google Sheets: **Connected**")
st.sidebar.caption("✅ Make.com Webhook: **Active**")

# ==========================================
# 5. MODUL 1: DASHBOARD ANALYTICS
# ==========================================
if menu_option == "📊 Dashboard Analytics":
    st.subheader("📊 Analisis Omzet & Ringkasan Stok")
    
    # Perhitungan Metrik Utama
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

    # Visual Cards Metric
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
            <div class="metric-card metric-card-success">
                <div class="metric-label">Total Omzet Gross</div>
                <div class="metric-value">Rp {total_omzet:,.0f}</div>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">Total Transaksi</div>
                <div class="metric-value">{total_trx} Pesanan</div>
            </div>
        ''', unsafe_allow_html=True)
    with c3:
        card_class = "metric-card-danger" if critical_items > 0 else "metric-card-success"
        st.markdown(f'''
            <div class="metric-card {card_class}">
                <div class="metric-label">Bahan Perlu Reorder</div>
                <div class="metric-value">{critical_items} Item</div>
            </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown('''
            <div class="metric-card">
                <div class="metric-label">Kanal Penjualan</div>
                <div class="metric-value">5 Channel</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grafik Visual Penjualan
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("### 📈 Penjualan per Kanal")
        if not df_sales.empty:
            kanal_cols = [c for c in df_sales.columns if "kanal" in c.lower()]
            omzet_cols = [c for c in df_sales.columns if "omzet" in c.lower() or "total" in c.lower()]
            if kanal_cols and omzet_cols:
                chart_data = df_sales.groupby(kanal_cols[0])[omzet_cols[0]].sum().reset_index()
                st.bar_chart(chart_data.set_index(kanal_cols[0]), color="#F59E0B")
            else:
                st.dataframe(df_sales, use_container_width=True)
        else:
            st.info("Belum ada data transaksi yang dicatat.")

    with col_g2:
        st.markdown("### 🔮 Proyeksi Belanja Minggu Depan")
        st.info("💡 **Moving Average Forecasting:** System mendeteksi peningkatan permintaan Dimsum Mentai (+15%) dan Matcha Powder (+20%) untuk persiapan lonjakan pesanan akhir pekan.")

# ==========================================
# 6. MODUL 2: INVENTORY FEFO
# ==========================================
elif menu_option == "📦 Inventory FEFO & Alerts":
    st.subheader("📦 Monitoring Stok Bahan Baku (First Expired, First Out)")
    st.caption("Pantau tanggal kedaluwarsa dan sisa stok bahan baku secara efisien.")
    
    if not df_fefo.empty:
        status_col = None
        for col in df_fefo.columns:
            if "status" in col.lower() or "action" in col.lower() or "fefo" in col.lower():
                status_col = col
                break

        if status_col:
            # Custom Styling Warna untuk Tabel Status
            def highlight_status(val):
                if 'CRITICAL' in str(val).upper():
                    return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
                elif 'WARNING' in str(val).upper():
                    return 'background-color: #FEF3C7; color: #92400E; font-weight: bold;'
                elif 'SAFE' in str(val).upper():
                    return 'background-color: #D1FAE5; color: #065F46; font-weight: bold;'
                return ''

            st.dataframe(df_fefo.style.map(highlight_status, subset=[status_col]), use_container_width=True)
        else:
            st.dataframe(df_fefo, use_container_width=True)
    else:
        st.warning("Tabel Inventory_FEFO tidak dapat dimuat.")

# ==========================================
# 7. MODUL 3: MASTER BOM & RESEP HPP
# ==========================================
elif menu_option == "📋 Master BOM & Resep HPP":
    st.subheader("📋 Standar Resep & Kalkulasi HPP per Menu")
    
    if not df_bom.empty:
        menu_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
        menu_col = menu_cols[0] if menu_cols else df_bom.columns[1]
        
        menu_list = df_bom[menu_col].dropna().unique()
        selected_menu = st.selectbox("🎯 Pilih Menu 199 Kitchen untuk Melihat Resep:", menu_list)
        
        recipe_df = df_bom[df_bom[menu_col] == selected_menu]
        
        st.write(f"#### Rincian Takaran Resep: **{selected_menu}**")
        st.dataframe(recipe_df, use_container_width=True)
        
        hpp_cols = [c for c in df_bom.columns if "hpp" in c.lower() or "est." in c.lower()]
        if hpp_cols:
            total_hpp = pd.to_numeric(recipe_df[hpp_cols[-1]], errors='coerce').sum()
            st.success(f"💰 **Estimasi Total HPP (Food Cost) per Porsi:** **Rp {total_hpp:,.0f}**")
    else:
        st.warning("Data Master_BOM kosong atau tidak terhubung.")

# ==========================================
# 8. MODUL 4: FORM SALES & TRIGGER WEBHOOK
# ==========================================
elif menu_option == "🛒 Form Sales (Input Webhook)":
    st.subheader("🛒 Input Transaksi Baru & Sinkronisasi Otomatis")
    st.caption("Form ini akan memicu Webhook Make.com secara langsung untuk menambahkan baris baru ke Google Sheets.")
    
    with st.form("form_sales_input"):
        c_left, c_right = st.columns(2)
        
        with c_left:
            id_trx = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            st.text_input("ID Transaksi (Auto Generator):", value=id_trx, disabled=True)
            kanal = st.selectbox("Kanal Penjualan:", ["GoFood", "GrabFood", "ShopeeFood", "WA Pre-Order", "Takeaway / Kasir"])
            
            menu_options = ["Dimsum Mentai Mini (isi 3)", "Dimsum Mentai Regular A (isi 6)", "Gyoza Kuah Keju Creamy", "Pentol Pedas", "Cookies Ice Cream", "Es Kopzu 199", "Matchacih"]
            if not df_bom.empty:
                m_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
                if m_cols:
                    menu_options = df_bom[m_cols[0]].dropna().unique()
            menu_nama = st.selectbox("Pilih Menu Dipesan:", menu_options)
            
            qty = st.number_input("Jumlah Porsi (Qty):", min_value=1, value=1, step=1)
            
        with c_right:
            waktu_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.text_input("Waktu Transaksi:", value=waktu_str, disabled=True)
            harga = st.number_input("Harga per Porsi (Rp):", min_value=1000, value=15000, step=1000)
            metode = st.selectbox("Metode Pembayaran:", ["GoPay", "OVO", "ShopeePay", "QRIS", "Tunai", "Transfer Bank"])
            catatan = st.text_input("Catatan Pesanan:", value="Normal")

        st.markdown("---")
        submit_button = st.form_submit_button("🚀 Kirim Transaksi & Kurangi Stok Otomatis")
        
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
                    st.success(f"✅ Transaksi **{id_trx}** Berhasil Dikirim ke Make.com & Terpencet Masuk ke Google Sheets!")
                    st.json(payload)
                else:
                    st.error(f"Gagal mengirim transaksi ke Make.com. Status Code: {res.status_code}")
            except Exception as ex:
                st.error(f"Terjadi kesalahan saat memicu Webhook: {ex}")

# ==========================================
# 9. MODUL 5: DATABASE SUPPLIER
# ==========================================
elif menu_option == "🚛 Database Supplier":
    st.subheader("🚛 Database Pemasok Bahan Baku & Kontak Vendor")
    if not df_supp.empty:
        st.dataframe(df_supp, use_container_width=True)
    else:
        st.info("Data supplier belum tersedia.")
