import uuid

from sqlalchemy import text

from services.user_service import create_user


# --------------------------------------------------
# Aktif Dönem
# --------------------------------------------------

def get_active_term(conn):

    row = conn.execute(
        text("""
            SELECT id
            FROM donemler
            WHERE aktif = TRUE
            LIMIT 1
        """)
    ).mappings().first()

    if row is None:
        raise Exception("Aktif dönem bulunamadı.")

    return row["id"]


# --------------------------------------------------
# Öğrenci Bul
# --------------------------------------------------

def find_student(conn, ogrenci_no):

    return conn.execute(
        text("""
            SELECT *
            FROM ogrenciler
            WHERE ogrenci_no = :ogrenci_no
            LIMIT 1
        """),
        {
            "ogrenci_no": str(ogrenci_no).strip()
        },
    ).mappings().first()


# --------------------------------------------------
# Öğrenci Oluştur
# --------------------------------------------------

def create_student(conn, row):

    student_id = str(uuid.uuid4())

    conn.execute(
        text("""
            INSERT INTO ogrenciler
            (
                id,
                ogrenci_no,
                tc_kimlik_no,
                ad,
                soyad,
                telefon,
                aktif
            )
            VALUES
            (
                :id,
                :ogrenci_no,
                :tc,
                :ad,
                :soyad,
                '',
                TRUE
            )
        """),
        {
            "id": student_id,
            "ogrenci_no": str(row["OKUL NO"]).strip(),
            "tc": str(row["ÖĞRENCİ TC KİMLİK NO"]).strip(),
            "ad": str(row["ÖĞRENCİ ADI"]).strip(),
            "soyad": str(row["ÖĞRENCİ SOYADI"]).strip(),
        },
    )

    create_user(
        conn=conn,
        rol="ogrenci",
        referans_id=student_id,
        username=str(row["OKUL NO"]).strip(),
    )

    return student_id


# --------------------------------------------------
# Öğrenci Güncelle
# --------------------------------------------------

def update_student(conn, student_id, row):

    conn.execute(
        text("""
            UPDATE ogrenciler
            SET
                tc_kimlik_no = :tc,
                ad = :ad,
                soyad = :soyad,
                aktif = TRUE
            WHERE id = :id
        """),
        {
            "id": student_id,
            "tc": str(row["ÖĞRENCİ TC KİMLİK NO"]).strip(),
            "ad": str(row["ÖĞRENCİ ADI"]).strip(),
            "soyad": str(row["ÖĞRENCİ SOYADI"]).strip(),
        },
    )
# --------------------------------------------------
# Veli Bul
# --------------------------------------------------

def find_parent(conn, row):

    tc = str(row["VELİ TC KİMLİK NO"]).strip()
    telefon = str(row["VELİ TELEFON"]).strip()
    ad = str(row["VELİ ADI"]).strip()
    soyad = str(row["VELİ SOYADI"]).strip()

    if tc:

        veli = conn.execute(
            text("""
                SELECT *
                FROM veliler
                WHERE tc_kimlik_no=:tc
                LIMIT 1
            """),
            {"tc": tc},
        ).mappings().first()

        if veli:
            return veli

    if telefon:

        veli = conn.execute(
            text("""
                SELECT *
                FROM veliler
                WHERE telefon=:telefon
                LIMIT 1
            """),
            {"telefon": telefon},
        ).mappings().first()

        if veli:
            return veli

    return conn.execute(
        text("""
            SELECT *
            FROM veliler
            WHERE ad=:ad
              AND soyad=:soyad
            LIMIT 1
        """),
        {
            "ad": ad,
            "soyad": soyad,
        },
    ).mappings().first()


# --------------------------------------------------
# Veli Oluştur
# --------------------------------------------------

def create_parent(conn, row):

    parent_id = str(uuid.uuid4())

    conn.execute(
        text("""
            INSERT INTO veliler
            (
                id,
                tc_kimlik_no,
                ad,
                soyad,
                telefon
            )
            VALUES
            (
                :id,
                :tc,
                :ad,
                :soyad,
                :telefon
            )
        """),
        {
            "id": parent_id,
            "tc": str(row["VELİ TC KİMLİK NO"]).strip(),
            "ad": str(row["VELİ ADI"]).strip(),
            "soyad": str(row["VELİ SOYADI"]).strip(),
            "telefon": str(row["VELİ TELEFON"]).strip(),
        },
    )

    username = str(row["VELİ TELEFON"]).strip()

    if username == "":
        username = str(row["VELİ TC KİMLİK NO"]).strip()

    if username:

        create_user(
            conn=conn,
            rol="veli",
            referans_id=parent_id,
            username=username,
        )

    return parent_id


# --------------------------------------------------
# Öğrenci - Veli İlişkisi
# --------------------------------------------------

def create_student_parent_relation(
    conn,
    student_id,
    parent_id,
    yakinlik,
):

    row = conn.execute(
        text("""
            SELECT id
            FROM ogrenci_velileri
            WHERE ogrenci_id=:ogrenci
              AND veli_id=:veli
            LIMIT 1
        """),
        {
            "ogrenci": student_id,
            "veli": parent_id,
        },
    ).mappings().first()

    if row:
        return

    conn.execute(
        text("""
            INSERT INTO ogrenci_velileri
            (
                id,
                ogrenci_id,
                veli_id,
                yakinlik,
                birincil
            )
            VALUES
            (
                :id,
                :ogrenci,
                :veli,
                :yakinlik,
                TRUE
            )
        """),
        {
            "id": str(uuid.uuid4()),
            "ogrenci": student_id,
            "veli": parent_id,
            "yakinlik": str(yakinlik).strip(),
        },
    )
# --------------------------------------------------
# Dönem Kaydı
# --------------------------------------------------

def create_student_term(
    conn,
    student_id,
    term_id,
    sinif,
):

    row = conn.execute(
        text("""
            SELECT id
            FROM ogrenci_donemleri
            WHERE ogrenci_id=:ogrenci_id
              AND donem_id=:donem_id
            LIMIT 1
        """),
        {
            "ogrenci_id": student_id,
            "donem_id": term_id,
        },
    ).mappings().first()

    if row:
        return

    conn.execute(
        text("""
            INSERT INTO ogrenci_donemleri
            (
                id,
                ogrenci_id,
                donem_id,
                sinif
            )
            VALUES
            (
                :id,
                :ogrenci_id,
                :donem_id,
                :sinif
            )
        """),
        {
            "id": str(uuid.uuid4()),
            "ogrenci_id": student_id,
            "donem_id": term_id,
            "sinif": str(sinif).strip(),
        },
    )


# --------------------------------------------------
# Öğrenci Aktar
# --------------------------------------------------

def import_students(engine, df):

    imported = 0

    with engine.begin() as conn:

        term_id = get_active_term(conn)

        for _, row in df.iterrows():

            student = find_student(
                conn,
                row["OKUL NO"],
            )

            if student:

                student_id = student["id"]

                update_student(
                    conn,
                    student_id,
                    row,
                )

            else:

                student_id = create_student(
                    conn,
                    row,
                )

            parent = find_parent(
                conn,
                row,
            )

            if parent:

                parent_id = parent["id"]

            else:

                parent_id = create_parent(
                    conn,
                    row,
                )

            create_student_parent_relation(
                conn,
                student_id,
                parent_id,
                row["VELİ YAKINLIĞI"],
            )

            create_student_term(
                conn,
                student_id,
                term_id,
                row["SINIFI"],
            )

            imported += 1

    return imported
