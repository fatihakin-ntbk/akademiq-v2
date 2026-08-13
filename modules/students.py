import streamlit as st
import pandas as pd

from services.student_template import create_student_template
from services.student_import import read_student_excel


def show(engine):

    st.title("👨‍🎓 Öğrenci & Veli Yönetimi")

    tab1, tab2, tab3 = st.tabs(
        [
            "📥 Öğrenci Aktar",
            "👨‍🎓 Öğrenciler",
            "👨‍👩‍👦 Veliler",
        ]
    )

    # ==================================================
    # ÖĞRENCİ AKTAR
    # ==================================================

    with tab1:

        st.subheader("1️⃣ Excel Şablonunu İndir")

        st.download_button(
            label="📄 Öğrenci Excel Şablonunu İndir",
            data=create_student_template(),
            file_name="Ogrenci_Veli_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.divider()

        st.subheader("2️⃣ Excel Dosyasını Yükle")

        uploaded_file = st.file_uploader(
            "Excel dosyası",
            type=["xlsx"],
        )

        if uploaded_file is None:

            st.info("Henüz Excel yüklenmedi.")

            return

        try:

            df = read_student_excel(uploaded_file)

        except Exception as e:

            st.error(str(e))

            return

        st.success("Excel başarıyla okundu.")

        st.write("")

        st.subheader("Önizleme")

        preview = pd.DataFrame()

        preview["OKUL NO"] = df["OKUL NO"]

        preview["ADI"] = df["ÖĞRENCİ ADI"]

        preview["SOYADI"] = df["ÖĞRENCİ SOYADI"]

        preview["SINIF"] = df["SINIFI"]

        preview["VELİ"] = (
            df["VELİ ADI"]
            + " "
            + df["VELİ SOYADI"]
        )

        st.dataframe(

            preview.head(10),

            use_container_width=True,

            hide_index=True,

        )

        st.info(

            f"Toplam **{len(df)}** öğrenci bulundu."

        )

    # ==================================================
    # ÖĞRENCİLER
    # ==================================================

    with tab2:

        st.info("Henüz öğrenci bulunmuyor.")

    # ==================================================
    # VELİLER
    # ==================================================

    with tab3:

        st.info("Henüz veli bulunmuyor.")
