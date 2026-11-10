import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM SOFT STYLING (CSS)
# ==========================================
st.set_page_config(
    page_title="SIM SCM 199 Kitchen",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Soft CSS Styling untuk Tampilan Web Modern & Estetik
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Terapkan Font Modern ke Seluruh Elemen */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Styling Header Utama dengan Gradasi Soft */
    .main-header {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #FDE68A;
        margin-bottom: 24px;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #92400E;
        margin: 0;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #78350F;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Styling Metric Cards yang Soft & Clean */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1F2937;
        margin-top: 4px;
    }
    
    /* Styling Sidebar Agar Lebih Soft */
    [data-testid="stSidebar"] {
        background-color: #F9FAFB;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Tombol Interaktif */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama dengan Desain Kotak Soft
st.markdown("""
    <div class="main-header">
        <p class="main-title">🍲 System Information Management SCM</p>
        <p class="sub-title"><b>199 Kitchen Singosari, Malang</b> &bull; Dashboard Real-time Monitoring Stok, HPP, Penjualan & Forecast</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. PENGAMAN SECRETS CREDENTIALS
# ==========================================
try:
    SPREADSHEET_ID = st.secrets["spreadsheet"]["spreadsheet_id"]
    MAKE_WEBHOOK_URL = st.secrets["make_webhook"]["url"]
except Exception as e:
    st.error("⚠️ **Secrets Belum Dikonfigurasi!** Pastikan `[spreadsheet]` dan `[make_webhook]` sudah diatur di Advanced Settings Streamlit Cloud.")
    st.stop()

# ==========================================
# 3. LOAD DATA DARI GOOGLE SHEETS
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
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/restaurant-menu.png", width=70)
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
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #6B7280; font-weight: 600;'>STATUS INTEGRASI</p>", unsafe_allow_html=True)
st.sidebar.caption("🟢 Google Sheets: Connected")
st.sidebar.caption("🟢 Make.com Webhook: Active")

# ==========================================
# 5. MODUL 1: DASHBOARD ANALYTICS
# ==========================================
if menu_option == "📊 Dashboard Analytics":
    st.markdown("### 📊 Ringkasan Performa & Operasional")
    
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

    # Kartu Metrik Soft Design
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid #10B981;">
                <div class="metric-label">Total Omzet Gross</div>
                <div class="metric-value" style="color: #047857;">Rp {total_omzet:,.0f}</div>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid #3B82F6;">
                <div class="metric-label">Total Transaksi</div>
                <div class="metric-value" style="color: #1D4ED8;">{total_trx} Pesanan</div>
            </div>
        ''', unsafe_allow_html=True)
    with c3:
        border_color = "#EF4444" if critical_items > 0 else "#10B981"
        val_color = "#B91C1C" if critical_items > 0 else "#047857"
        st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid {border_color};">
                <div class="metric-label">Bahan Perlu Reorder</div>
                <div class="metric-value" style="color: {val_color};">{critical_items} Item</div>
            </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid #F59E0B;">
                <div class="metric-label">Kanal Penjualan</div>
                <div class="metric-value" style="color: #B45309;">5 Channel</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 📈 Performa Penjualan Berdasarkan Kanal")
        if not df_sales.empty:
            kanal_cols = [c for c in df_sales.columns if "kanal" in c.lower()]
            omzet_cols = [c for c in df_sales.columns if "omzet" in c.lower() or "total" in c.lower()]
            if kanal_cols and omzet_cols:
                chart_data = df_sales.groupby(kanal_cols[0])[omzet_cols[0]].sum().reset_index()
                st.bar_chart(chart_data.set_index(kanal_cols[0]), color="#F59E0B")
            else:
                st.dataframe(df_sales, use_container_width=True)
        else:
            st.info("Belum ada data transaksi tercatat.")

    with col_g2:
        st.markdown("##### 🔮 Forecast & Rekomendasi Belanja")
        st.info("💡 **Moving Average Insight:** Persiapan stok bahan baku akhir pekan difokuskan pada peningkatan ketersediaan *Daging Ayam Fillet* dan *Saus Mentai* seiring tren kenaikan pesanan.")

# ==========================================
# 6. MODUL 2: INVENTORY FEFO
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
                    return 'background-color: #FEE2E2; color: #991B1B; font-weight: 600;'
                elif 'WARNING' in str(val).upper():
                    return 'background-color: #FEF3C7; color: #92400E; font-weight: 600;'
                elif 'SAFE' in str(val).upper():
                    return 'background-color: #D1FAE5; color: #065F46; font-weight: 600;'
                return ''

            st.dataframe(df_fefo.style.map(highlight_status, subset=[status_col]), use_container_width=True)
        else:
            st.dataframe(df_fefo, use_container_width=True)
    else:
        st.warning("Tabel Inventory FEFO kosong.")

# ==========================================
# 7. MODUL 3: MASTER BOM & RESEP HPP
# ==========================================
elif menu_option == "📋 Master BOM & Resep HPP":
    st.markdown("### 📋 Standar Resep & Kalkulasi HPP per Menu")
    
    if not df_bom.empty:
        menu_cols = [c for c in df_bom.columns if "menu" in c.lower() and "nama" in c.lower()]
        menu_col = menu_cols[0] if menu_cols else df_bom.columns[1]
        
        menu_list = df_bom[menu_col].dropna().unique()
        selected_menu = st.selectbox("🎯 Pilih Menu 199 Kitchen:", menu_list)
        
        recipe_df = df_bom[df_bom[menu_col] == selected_menu]
        st.markdown(f"##### Rincian Komposisi Bahan untuk: **{selected_menu}**")
        st.dataframe(recipe_df, use_container_width=True)
        
        hpp_cols = [c for c in df_bom.columns if "hpp" in c.lower() or "est." in c.lower()]
        if hpp_cols:
            total_hpp = pd.to_numeric(recipe_df[hpp_cols[-1]], errors='coerce').sum()
            st.success(f"💰 **Estimasi Total HPP per Porsi:** **Rp {total_hpp:,.0f}**")
    else:
        st.warning("Data Master BOM tidak tersedia.")

# ==========================================
# 8. MODUL 4: FORM SALES & TRIGGER WEBHOOK
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
        submit_button = st.form_submit_button("🚀 Kirim Transaksi ke Spreadsheet")
        
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

# ==========================================
# 9. MODUL 5: DATABASE SUPPLIER
# ==========================================
elif menu_option == "🚛 Database Supplier":
    st.markdown("### 🚛 Database Pemasok Bahan Baku & Vendor")
    if not df_supp.empty:
        st.dataframe(df_supp, use_container_width=True)
    else:
        st.info("Data supplier belum tersedia.")
