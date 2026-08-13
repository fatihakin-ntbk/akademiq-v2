import streamlit as st
from sqlalchemy import create_engine, text

st.write("DATABASE_URL bulundu mu?")

try:
    url = st.secrets["DATABASE_URL"]
    st.success("Secrets OK")
    st.code(url.replace("110856Le10..", "********"))
except Exception as e:
    st.error(e)
    st.stop()

try:
    engine = create_engine(url)

    with engine.connect() as conn:
        version = conn.execute(text("select version()")).scalar()

    st.success("Bağlantı başarılı")
    st.write(version)

except Exception as e:
    st.exception(e)
