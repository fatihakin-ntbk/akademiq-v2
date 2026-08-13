import streamlit as st


def show():

    st.title("🏠 Admin Paneli")

    c1, c2, c3 = st.columns(3)

    c1.metric("Öğrenci", "-")
    c2.metric("Veli", "-")
    c3.metric("Öğretmen", "-")

    st.divider()

    st.info("AkademIQ Yönetim Paneline hoş geldiniz.")
