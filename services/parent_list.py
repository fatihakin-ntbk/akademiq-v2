import pandas as pd
from sqlalchemy import text


def get_parents(engine, search=""):

    with engine.connect() as conn:

        if search.strip() == "":

            query = text("""
                SELECT
                    v.id,
                    v.ad,
                    v.soyad,
                    v.telefon,
                    COUNT(ov.ogrenci_id) AS ogrenci_sayisi
                FROM veliler v
                LEFT JOIN ogrenci_velileri ov
                    ON ov.veli_id = v.id
                GROUP BY
                    v.id,
                    v.ad,
                    v.soyad,
                    v.telefon
                ORDER BY
                    v.ad,
                    v.soyad
            """)

            return pd.read_sql(query, conn)

        query = text("""
            SELECT
                v.id,
                v.ad,
                v.soyad,
                v.telefon,
                COUNT(ov.ogrenci_id) AS ogrenci_sayisi
            FROM veliler v
            LEFT JOIN ogrenci_velileri ov
                ON ov.veli_id = v.id
            WHERE
                LOWER(v.ad) LIKE LOWER(:q)
                OR LOWER(v.soyad) LIKE LOWER(:q)
                OR LOWER(COALESCE(v.telefon,'')) LIKE LOWER(:q)
            GROUP BY
                v.id,
                v.ad,
                v.soyad,
                v.telefon
            ORDER BY
                v.ad,
                v.soyad
        """)

        return pd.read_sql(
            query,
            conn,
            params={
                "q": f"%{search}%"
            },
        )
