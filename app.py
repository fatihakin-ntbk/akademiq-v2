import streamlit as st
import bcrypt
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="AkademIQ",
    page_icon="🎓",
    layout="centered",
)

engine = create_engine(st.secrets["DATABASE_URL"])


def login():

    st.title("🎓 AkademIQ")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):

        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT kullanici_adi,
                           sifre_hash,
                           rol
                    FROM kullanicilar
                    WHERE kullanici_adi=:u
                    AND aktif=TRUE
                """),
                {"u": username},
            ).mappings().first()

        if user is None:
            st.error("Kullanıcı bulunamadı.")
            return

        if bcrypt.checkpw(
            password.encode(),
            user["sifre_hash"].encode(),
        ):
            st.success(f"Hoş geldiniz {user['rol']}")
        else:
            st.error("Şifre yanlış.")


login()
