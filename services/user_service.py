import secrets
import string
import bcrypt

from sqlalchemy import text


# --------------------------------------------------
# Şifre üret
# --------------------------------------------------

def generate_password(length=8):

    alphabet = (
        string.ascii_uppercase +
        string.digits
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


# --------------------------------------------------
# Hash
# --------------------------------------------------

def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


# --------------------------------------------------
# Kullanıcı var mı?
# --------------------------------------------------

def user_exists(conn, username):

    row = conn.execute(
        text("""
            SELECT id
            FROM kullanicilar
            WHERE kullanici_adi = :username
            LIMIT 1
        """),
        {
            "username": username
        },
    ).mappings().first()

    return row is not None


# --------------------------------------------------
# Kullanıcı Oluştur
# --------------------------------------------------

def create_user(
    conn,
    rol,
    referans_id,
    username,
):

    if user_exists(conn, username):
        return None

    password = generate_password()

    conn.execute(
        text("""
            INSERT INTO kullanicilar
            (
                id,
                rol,
                referans_id,
                kullanici_adi,
                sifre_hash,
                sifre_degistirilmeli,
                aktif
            )
            VALUES
            (
                gen_random_uuid(),
                :rol,
                :referans_id,
                :username,
                :password,
                TRUE,
                TRUE
            )
        """),
        {
            "rol": rol,
            "referans_id": referans_id,
            "username": username,
            "password": hash_password(password),
        },
    )

    return password
