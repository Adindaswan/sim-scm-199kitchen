if res.status_code == 200:
                    st.balloons()
                    st.success(f"✅ Transaksi {id_trx} Berhasil Tercatat!")
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
