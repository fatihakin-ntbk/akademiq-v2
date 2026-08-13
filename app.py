import streamlit as st
from sqlalchemy import create_engine, text
import bcrypt

st.set_page_config(
    page_title="AkademIQ",
    page_icon="🎓",
    layout="centered",
)

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

st.title("🎓 AkademIQ")

username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Giriş Yap"):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
                SELECT *
                FROM kullanicilar
                WHERE kullanici_adi=:u
                AND aktif=TRUE
                LIMIT 1
            """),
            {"u": username},
        ).mappings().first()

    if user is None:
        st.error("Kullanıcı bulunamadı.")

    elif bcrypt.checkpw(
        password.encode(),
        user["sifre_hash"].encode(),
    ):

        st.success(f"Hoş geldiniz {user['rol']}")

    else:
        st.error("Şifre yanlış.")
