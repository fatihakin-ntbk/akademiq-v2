import streamlit as st
import bcrypt
from sqlalchemy import create_engine, text

# --------------------------------------------------
# SAYFA AYARLARI
# --------------------------------------------------

st.set_page_config(
    page_title="AkademIQ",
    page_icon="🎓",
    layout="wide",
)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

engine = create_engine(st.secrets["DATABASE_URL"])

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# --------------------------------------------------
# LOGIN
# --------------------------------------------------


def login():

    st.title("🎓 AkademIQ")

    st.subheader("Kullanıcı Girişi")

    with st.form("login"):

        username = st.text_input("Kullanıcı Adı")

        password = st.text_input(
            "Şifre",
            type="password",
        )

        submit = st.form_submit_button(
            "Giriş Yap",
            use_container_width=True,
        )

    if not submit:
        return

    with engine.connect() as conn:

        user = conn.execute(
            text(
                """
                SELECT
                    kullanici_adi,
                    sifre_hash,
                    rol
                FROM kullanicilar
                WHERE kullanici_adi=:u
                AND aktif=TRUE
                LIMIT 1
                """
            ),
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


# --------------------------------------------------
# MENU
# --------------------------------------------------


def sidebar():

    st.sidebar.title("🎓 AkademIQ")

    st.sidebar.write("")

    st.sidebar.success(
        f"Giriş yapan : {st.session_state.username}"
    )

    st.sidebar.info(
        f"Rol : {st.session_state.role}"
    )

    st.sidebar.write("")

    page = st.sidebar.radio(

        "Menü",

        [

            "🏠 Ana Sayfa",

            "👨‍🎓 Öğrenci & Veli Yönetimi",

            "📝 Sınav Yönetimi",

            "📊 Analizler",

            "⚙️ Ayarlar",

        ],

    )

    st.sidebar.write("")

    if st.sidebar.button(
        "Çıkış Yap",
        use_container_width=True,
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    return page
    # --------------------------------------------------
# PAGES
# --------------------------------------------------


def page_home():

    st.title("🏠 Admin Paneli")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Öğrenci",
            "-"
        )

    with c2:
        st.metric(
            "Veli",
            "-"
        )

    with c3:
        st.metric(
            "Öğretmen",
            "-"
        )

    st.divider()

    st.info(
        "AkademIQ Yönetim Paneline hoş geldiniz."
    )


# --------------------------------------------------


def page_student_parent():

    st.title("👨‍🎓 Öğrenci & Veli Yönetimi")

    tab1, tab2, tab3, tab4 = st.tabs(
        [

            "📥 Öğrenci Aktar",

            "👨‍🎓 Öğrenciler",

            "👨‍👩‍👦 Veliler",

            "⚙️ Ayarlar",

        ]
    )

    with tab1:

        st.subheader("Excel'den Öğrenci Aktar")

        st.info(
            "Bu bölümde öğrenci ve veli Excel dosyası yüklenecek."
        )

    with tab2:

        st.subheader("Öğrenci Listesi")

        st.info(
            "Henüz veri yok."
        )

    with tab3:

        st.subheader("Veli Listesi")

        st.info(
            "Henüz veri yok."
        )

    with tab4:

        st.subheader("Modül Ayarları")

        st.info(
            "Henüz ayar bulunmuyor."
        )


# --------------------------------------------------


def page_exam():

    st.title("📝 Sınav Yönetimi")

    st.info(
        "Bu modül daha sonra geliştirilecek."
    )


# --------------------------------------------------


def page_analysis():

    st.title("📊 Analizler")

    st.info(
        "Bu modül daha sonra geliştirilecek."
    )


# --------------------------------------------------


def page_settings():

    st.title("⚙️ Ayarlar")

    st.info(
        "Bu modül daha sonra geliştirilecek."
    )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if not st.session_state.logged_in:

    login()

else:

    page = sidebar()

    if page == "🏠 Ana Sayfa":

        page_home()

    elif page == "👨‍🎓 Öğrenci & Veli Yönetimi":

        page_student_parent()

    elif page == "📝 Sınav Yönetimi":

        page_exam()

    elif page == "📊 Analizler":

        page_analysis()

    elif page == "⚙️ Ayarlar":

        page_settings()
