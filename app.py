import streamlit as st
import bcrypt

st.code(
    bcrypt.hashpw(
        "AkademIQ2026!".encode(),
        bcrypt.gensalt()
    ).decode()
)
