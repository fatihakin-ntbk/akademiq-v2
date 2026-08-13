import streamlit as st
import bcrypt
from sqlalchemy import create_engine, text

from pages import home
from pages import donemler
from pages import students
from pages import exams
from pages import analysis

# ------------------------------------------------
# Sayfa
# ------------------------------------------------

st.set_page_config(
    page_title="AkademIQ",
    page_icon="🎓",
    layout="wide",
)

# ------------------------------------------------
# Database
# ------------------------------------------------

engine = create_engine(st.secrets["DATABASE_URL"])

# ------------------------------------------------
# Session
# ------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ------------------------------------------------
# Login
# ------------------------------------------------

def login():

    st.title("🎓 AkademIQ")

    with st.form("login"):

        username = st.text_input("Kullanıcı Adı")

        password = st.text_input(
            "Şifre",
            type="password",
        )

        submit = st.form_submit_button("Giriş Yap")

    if not submit:
        return

    with engine.connect() as conn:

        user = conn.execute(
            text("""
                SELECT
                    kullanici_adi,
                    sifre_hash,
                    rol
                FROM kullanicilar
                WHERE kullanici_adi=:u
                AND aktif=TRUE
                LIMIT 1
            """),
            {"u": username},
        ).mappings().first()

    if user is None:
        st.error("Kullanıcı bulunamadı.")
        return

    if not bcrypt.checkpw(
        password.encode(),
        user["sifre_hash"].encode(),
    ):
        st.error("Şifre yanlış.")
        return

    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.role = user["rol"]

    st.rerun()

# ------------------------------------------------
# Menü
# ------------------------------------------------

def menu():

    st.sidebar.title("🎓 AkademIQ")

    st.sidebar.success(
        st.session_state.username
    )

    page = st.sidebar.radio(

        "Menü",

        [

            "🏠 Ana Sayfa",

            "📅 Dönem Seç",

            "👨‍🎓 Öğrenci & Veli Yönetimi",

            "📝 Sınav Yönetimi",

            "📊 Analizler",

        ]

    )

    st.sidebar.divider()

    if st.sidebar.button("Çıkış Yap"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    return page

# ------------------------------------------------
# Main
# ------------------------------------------------

if not st.session_state.logged_in:

    login()

else:

    page = menu()

    if page == "🏠 Ana Sayfa":
        home.show()

    elif page == "📅 Dönem Seç":
        donemler.show(engine)

    elif page == "👨‍🎓 Öğrenci & Veli Yönetimi":
        students.show(engine)

    elif page == "📝 Sınav Yönetimi":
        exams.show()

    elif page == "📊 Analizler":
        analysis.show()
