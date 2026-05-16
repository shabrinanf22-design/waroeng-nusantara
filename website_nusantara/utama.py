import streamlit as st 
import pandas as pd
import os
import urllib.parse

# =========================
# 🛒 INIT KERANJANG
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

# Konfigurasi halaman
st.set_page_config(page_title="Waroeng Nusantara", layout="wide")

# Banner (opsional)
if os.path.exists("banner.png"):
    st.image("banner.png", use_container_width=True)

st.title("🍽️ Waroeng Nusantara")
st.write("")
st.divider()

try:
    if os.path.exists("data_menu1.csv"):
        df = pd.read_csv("data_menu1.csv")

        df = df.dropna(subset=['foto'])

        daftar_kategori = df['kategori'].unique()

        for kat in daftar_kategori:
            st.write("")
            st.subheader(f"📦 {kat}")
            st.divider()

            data_per_kat = df[df['kategori'] == kat]
            cols = st.columns(4)

            for index, row in data_per_kat.reset_index(drop=True).iterrows():
                nama_foto = str(row['foto']).strip()

                with cols[index % 4]:
                    with st.container(border=True):

                        if os.path.exists(nama_foto):
                            st.image(nama_foto, use_container_width=True)
                        else:
                            st.warning("Foto tidak ditemukan")

                        st.write("")
                        st.subheader(row['nama'])
                        st.metric("Harga", f"Rp {row['harga']:,}")

                        status = str(row['status'])

                        if status.lower() == "tersedia":
                            st.success("🟢 Tersedia")
                        else:
                            st.error("🔴 Habis")

                        st.write("")

                        # =========================
                        # 📲 PESAN PER ITEM
                        # =========================
                        no_hp = "6289652975903"
                        pesan = f"Halo kak, saya mau pesan {row['nama']}"
                        link_wa = f"https://wa.me/{no_hp}?text={urllib.parse.quote(pesan)}"

                       

                        # =========================
                        # 🛒 TAMBAH KERANJANG
                        # =========================
                        if st.button(f"➕ Keranjang", key=f"add_{index}_{row['nama']}"):
                            st.session_state.cart.append({
                                "nama": row["nama"],
                                "harga": row["harga"]
                            })
                            st.success("✔ Ditambahkan ke keranjang")

            st.divider()

    else:
        st.error("File data_menu1.csv tidak ditemukan!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

# =========================
# 🛒 SIDEBAR KERANJANG
# =========================
st.sidebar.title("🛒 Keranjang")

if st.session_state.cart:
    total = 0

    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"{item['nama']} - Rp {item['harga']:,}")
        total += item['harga']

        if st.sidebar.button(f"❌ Hapus {item['nama']}", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

    st.sidebar.divider()
    st.sidebar.markdown(f"### 💰 Total: Rp {total:,}")

    # Checkout WhatsApp
    if st.sidebar.button("📲 Checkout WhatsApp"):
        no_hp = "6289652975903"

        isi = "Halo kak, saya mau pesan:\n"
        for item in st.session_state.cart:
            isi += f"- {item['nama']} (Rp {item['harga']:,})\n"

        link = f"https://wa.me/{no_hp}?text={urllib.parse.quote(isi)}"

        st.sidebar.link_button("Kirim Pesanan", link)

    if st.sidebar.button("🗑️ Kosongkan Keranjang"):
        st.session_state.cart = []
        st.rerun()

else:
    st.sidebar.info("Keranjang masih kosong")

# =========================
# 📞 FOOTER
# =========================
st.write("")
st.divider()
st.subheader("📞 Hubungi Kami")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Alamat:**
    Jl. Nusantara No. 123  
    Indonesia
    """)

with col2:
    no_hp = "6289652975903"
    pesan = "Halo kak, saya mau pesan dari Warung Nusantara"
    link_wa = f"https://wa.me/{no_hp}?text={pesan.replace(' ', '%20')}"

    st.link_button("📲 Pesan via WhatsApp", link_wa)

st.caption("© 2026 Warung Nusantara")       