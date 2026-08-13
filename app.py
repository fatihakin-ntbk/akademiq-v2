import streamlit as st
import bcrypt

password = "AkademIQ2026!"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

st.code(hashed)
