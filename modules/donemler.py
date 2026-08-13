import streamlit as st
import pandas as pd
from sqlalchemy import text


def show(engine):

    st.title("📅 Dönem Yönetimi")

    st.write("")

    # -------------------------------
    # Yeni dönem ekleme
    # -------------------------------

    with st.expander("➕ Yeni Dönem Ekle", expanded=False):

        c1, c2 = st.columns(2)

        with c1:
            baslangic = st.number_input(
                "Başlangıç Yılı",
                min_value=2020,
                max_value=2100,
                value=2026,
                step=1,
            )

        with c2:
            bitis = st.number_input(
                "Bitiş Yılı",
                min_value=2021,
                max_value=2101,
                value=2027,
                step=1,
            )

        if st.button("Kaydet", use_container_width=True):

            ad = f"{int(baslangic)}-{int(bitis)}"

            try:

                with engine.begin() as conn:

                    conn.execute(
                        text("""
                            INSERT INTO donemler(ad)
                            VALUES(:ad)
                        """),
                        {"ad": ad},
                    )

                st.success("Dönem eklendi.")

                st.rerun()

            except Exception:

                st.error("Bu dönem zaten kayıtlı.")

    st.divider()

    # -------------------------------
    # Liste
    # -------------------------------

    with engine.connect() as conn:

        donemler = pd.read_sql(

            text("""

                SELECT
                    id,
                    ad,
                    aktif
                FROM donemler
                ORDER BY ad DESC

            """),

            conn,

        )

    if donemler.empty:

        st.warning("Henüz dönem bulunmuyor.")

        return

    st.subheader("Kayıtlı Dönemler")

    for _, row in donemler.iterrows():

        c1, c2, c3 = st.columns([5, 2, 2])

        with c1:

            if row["aktif"]:

                st.success(row["ad"])

            else:

                st.write(row["ad"])

        with c2:

            if row["aktif"]:

                st.write("✅ Aktif")

            else:

                if st.button(
                    "Aktif Yap",
                    key=f"a{row['id']}",
                ):

                    with engine.begin() as conn:

                        conn.execute(
                            text(
                                "UPDATE donemler SET aktif=FALSE"
                            )
                        )

                        conn.execute(
                            text("""
                                UPDATE donemler
                                SET aktif=TRUE
                                WHERE id=:id
                            """),
                            {"id": int(row["id"])},
                        )

                    st.rerun()

        with c3:

            if not row["aktif"]:

                if st.button(
                    "Sil",
                    key=f"s{row['id']}",
                ):

                    with engine.begin() as conn:

                        conn.execute(
                            text("""
                                DELETE
                                FROM donemler
                                WHERE id=:id
                            """),
                            {"id": int(row["id"])},
                        )

                    st.rerun()
