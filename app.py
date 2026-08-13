import streamlit as st

st.set_page_config(
    page_title="AkademIQ",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AkademIQ")

username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Giriş Yap"):
    st.info("Bir sonraki adımda veritabanından doğrulama yapılacak.")
