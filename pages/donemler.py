import streamlit as st


def show(engine):

    st.title("📅 Dönem Seç")

    st.info(
        "Bu modül bir sonraki adımda veritabanına bağlanacak."
    )

    st.write("Aktif Dönem")

    st.success("2025-2026")

    st.divider()

    st.subheader("Kayıtlı Dönemler")

    st.radio(

        "",

        [

            "2025-2026",

        ],

    )

    st.button("➕ Yeni Dönem Ekle")
