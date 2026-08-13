import pandas as pd
from sqlalchemy import text


def get_students(engine, search=""):

    with engine.connect() as conn:

        if search.strip() == "":

            query = text("""
                SELECT
                    o.id,
                    o.ogrenci_no,
                    o.ad,
                    o.soyad,
                    od.sinif
                FROM ogrenciler o
                JOIN ogrenci_donemleri od
                    ON od.ogrenci_id = o.id
                JOIN donemler d
                    ON d.id = od.donem_id
                WHERE d.aktif = TRUE
                ORDER BY
                    od.sinif,
                    o.ogrenci_no
            """)

            return pd.read_sql(query, conn)

        query = text("""
            SELECT
                o.id,
                o.ogrenci_no,
                o.ad,
                o.soyad,
                od.sinif
            FROM ogrenciler o
            JOIN ogrenci_donemleri od
                ON od.ogrenci_id = o.id
            JOIN donemler d
                ON d.id = od.donem_id
            WHERE d.aktif = TRUE
              AND (
                    LOWER(o.ad) LIKE LOWER(:q)
                 OR LOWER(o.soyad) LIKE LOWER(:q)
                 OR LOWER(o.ogrenci_no) LIKE LOWER(:q)
              )
            ORDER BY
                od.sinif,
                o.ogrenci_no
        """)

        return pd.read_sql(
            query,
            conn,
            params={
                "q": f"%{search}%"
            },
        )
