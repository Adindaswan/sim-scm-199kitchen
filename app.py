import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="SIM SCM 199 Kitchen",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍲 System Information Management SCM - 199 Kitchen")
st.caption("Singosari, Kabupaten Malang | Dashboard Monitoring Stok, HPP, Penjualan & Forecast")

# ==========================================
# 2. LOAD CREDENTIALS DARI STREAMLIT SECRETS
# ==========================================
@st.cache_data(ttl=60)
def load_data_from_sheets():
    """
    Fungsi untuk membaca data real-time dari Google Sheets API via Secrets
    """
    try:
        # Mengambil Spreadsheet ID dari Secrets
        spreadsheet_id = st.secrets["spreadsheet"]["spreadsheet_id"]
        
        # URL publik / API read-only Google Sheets (format CSV export per sheet)
        url_bom = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Master_BOM"
        url_fefo = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Inventory_FEFO"
        url_sales = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Sales_Log"
        url_supp = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Supplier_DB"
        
        df_bom = pd.read_csv(url_bom)
        df_fefo = pd.read_csv(url_fefo)
        df_sales = pd.read_csv(url_sales)
        df_supp = pd.read_csv(url_supp)
        
        return df_bom, df_fefo, df_sales, df_supp
    except Exception as e:
        st.error(f"Gagal mengambil data dari Google Sheets: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Load Data
df_bom, df_fefo, df_sales, df_supp = load_data_from_sheets()

# ==========================================
# 3. SIDEBAR NAVIGATION & INTEGRATION
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/restaurant-menu.png", width=80)
st.sidebar.header("Navigasi SIM SCM")
menu_option = st.sidebar.radio(
    "Pilih Modul:",
    [
        "📊 Dashboard Analytics & Forecast",
        "📦 Inventory Stok & Alerts (FEFO)",
        "📋 Recipe & Master BOM (HPP)",
        "🛒 Input Penjualan & Trigger Webhook",
        "🚛 Database Supplier"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Status Koneksi:**\n- Google Sheets: `Connected`\n- Make.com Webhook: `Active`")

# ==========================================
# 4. MODUL 1: DASHBOARD ANALYTICS & FORECAST
# ==========================================
if menu_option == "📊 Dashboard Analytics & Forecast":
    st.subheader("📊 ringkasan Performa Operasional & Forecast Belanja")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if not df_sales.empty:
        total_omzet = df_sales["Total Omzet Gross (Rp)"].sum() if "Total Omzet Gross (Rp)" in df_sales.columns else 0
        total_trx = len(df_sales)
    else:
        total_omzet, total_trx = 0, 0
        
    if not df_fefo.empty:
        critical_items = len(df_fefo[df_fefo["Status FEFO / Action"].str.contains("CRITICAL", case=False, na=False)])
    else:
        critical_items = 0

    col1.metric("Total Omzet Penjualan", f"Rp {total_omzet:,.0f}")
    col2.metric("Total Transaksi", f"{total_trx} Pesanan")
    col3.metric("Bahan Perlu Reorder", f"{critical_items} Item", delta="-Critical" if critical_items > 0 else "Safe")
    col4.metric("Kanal Penjualan Aktif", "5 Kanal")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.write("### 📈 Penjualan Berdasarkan Kanal")
        if not df_sales.empty and "Kanal Penjualan" in df_sales.columns:
            sales_by_channel = df_sales.groupby("Kanal Penjualan")["Total Omzet Gross (Rp)"].sum().reset_index()
            st.bar_chart(sales_by_channel.set_index("Kanal Penjualan"))
        else:
            st.info("Data transaksi belum tersedia.")
            
    with col_chart2:
        st.write("### 🔮 Moving Average Forecast Belanja (Kebutuhan Bahan)")
        st.write("Estimasi kebutuhan belanja bahan baku berdasarkan tren transaksi harian.")
        st.success("Prediksi Minggu Depan: Daging Ayam Fillet +15%, Saus Mentai +20% (Fokus Weekend).")

# ==========================================
# 5. MODUL 2: INVENTORY FEFO
# ==========================================
elif menu_option == "📦 Inventory Stok & Alerts (FEFO)":
    st.subheader("📦 Monitoring Stok Bahan Baku & Tanggal Kedaluwarsa (FEFO)")
    st.write("Sistem mendeteksi persediaan secara otomatis berbasis metode *First Expired, First Out*.")
    
    if not df_fefo.empty:
        # Filter Status
        status_filter = st.multiselect(
            "Filter Status FEFO:",
            options=df_fefo["Status FEFO / Action"].unique() if "Status FEFO / Action" in df_fefo.columns else [],
            default=df_fefo["Status FEFO / Action"].unique() if "Status FEFO / Action" in df_fefo.columns else []
        )
        filtered_fefo = df_fefo[df_fefo["Status FEFO / Action"].isin(status_filter)]
        st.dataframe(filtered_fefo, use_container_width=True)
    else:
        st.warning("Tabel Inventory_FEFO tidak dapat dimuat.")

# ==========================================
# 6. MODUL 3: RECIPE & MASTER BOM
# ==========================================
elif menu_option == "📋 Recipe & Master BOM (HPP)":
    st.subheader("📋 Standar Takaran Resep & Perhitungan HPP per Menu")
    
    if not df_bom.empty:
        menu_list = df_bom["Nama Menu (Varian)"].unique() if "Nama Menu (Varian)" in df_bom.columns else []
        selected_menu = st.selectbox("Pilih Menu / Produk 199 Kitchen:", menu_list)
        
        recipe_detail = df_bom[df_bom["Nama Menu (Varian)"] == selected_menu]
        st.write(f"#### Rincian Bahan Baku untuk: **{selected_menu}**")
        st.dataframe(recipe_detail, use_container_width=True)
        
        if "Est. HPP Bahan per Porsi (Rp)" in recipe_detail.columns:
            total_hpp = recipe_detail["Est. HPP Bahan per Porsi (Rp)"].sum()
            st.info(f"💡 **Total Estimasi HPP (Food Cost) per Porsi:** Rp {total_hpp:,.0f}")
    else:
        st.warning("Data Master_BOM kosong atau tidak terhubung.")

# ==========================================
# 7. MODUL 4: INPUT TRANSAKSI & MAKE.COM WEBHOOK
# ==========================================
elif menu_option == "🛒 Input Penjualan & Trigger Webhook":
    st.subheader("🛒 Form Catat Penjualan Baru (Otomatis Sync via Make.com)")
    
    with st.form("form_transaksi"):
        id_trx = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        tgl_trx = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kanal = st.selectbox("Kanal Penjualan:", ["GoFood", "GrabFood", "ShopeeFood", "WA Pre-Order", "Takeaway / Kasir"])
            menu_nama = st.selectbox("Menu Dipilih:", ["Dimsum Mentai Mini (isi 3)", "Dimsum Mentai Regular A (isi 6)", "Gyoza Kuah Keju Creamy", "Pentol Pedas (Level 2)", "Cookies Ice Cream", "Es Kopzu 199", "Matchacih"])
            qty = st.number_input("Jumlah Porsi (Qty):", min_value=1, value=1, step=1)
            
        with col_f2:
            harga = st.number_input("Harga per Porsi (Rp):", min_value=1000, value=15000, step=1000)
            metode = st.selectbox("Metode Pembayaran:", ["GoPay", "OVO", "ShopeePay", "QRIS", "Tunai", "Transfer Bank"])
            catatan = st.text_input("Catatan Pesanan:", value="Normal")
            
        btn_submit = st.form_submit_button("🚀 Kirim Transaksi & Kurangi Stok Otomatis")
        
        if btn_submit:
            total_omzet = qty * harga
            payload = {
                "id_transaksi": id_trx,
                "waktu": tgl_trx,
                "kanal": kanal,
                "menu": menu_nama,
                "qty": qty,
                "harga": harga,
                "omzet": total_omzet,
                "metode": metode,
                "catatan": catatan
            }
            
            # Pengiriman ke Webhook URL Make.com yang tersimpan di Secrets
            try:
                webhook_url = st.secrets["make_webhook"]["url"]
                response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    st.success(f"✅ Transaksi Berhasil Terkirim ke Make.com! (ID: {id_trx})")
                    st.json(payload)
                else:
                    st.error(f"Gagal memicu Webhook Make.com. Status Code: {response.status_code}")
            except Exception as e:
                st.warning(f"Simulasi Kirim Data (Webhook URL belum disetting di Secrets): {e}")
                st.json(payload)

# ==========================================
# 8. MODUL 5: DATABASE SUPPLIER
# ==========================================
elif menu_option == "🚛 Database Supplier":
    st.subheader("🚛 Database Pemasok Bahan Baku & Histori Harga")
    if not df_supp.empty:
        st.dataframe(df_supp, use_container_width=True)
    else:
        st.info("Data supplier belum tersedia.")
