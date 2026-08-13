import streamlit as st
import pandas as pd

from services.student_template import create_student_template
from services.student_import import read_student_excel
from services.student_validation import validate_student_dataframe


def show(engine):

    st.title("👨‍🎓 Öğrenci & Veli Yönetimi")

    tab1, tab2, tab3 = st.tabs(
        [
            "📥 Öğrenci Aktar",
            "👨‍🎓 Öğrenciler",
            "👨‍👩‍👦 Veliler",
        ]
    )

    with tab1:

        st.subheader("1️⃣ Excel Şablonunu İndir")

        st.download_button(
            "📄 Öğrenci Excel Şablonunu İndir",
            data=create_student_template(),
            file_name="Ogrenci_Veli_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.divider()

        st.subheader("2️⃣ Excel Yükle")

        uploaded_file = st.file_uploader(
            "Excel Dosyası",
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

        st.subheader("Önizleme")

        st.dataframe(
            preview.head(10),
            hide_index=True,
            use_container_width=True,
        )

        st.info(f"Toplam **{len(df)}** öğrenci bulundu.")

        st.divider()

        st.subheader("3️⃣ Doğrulama")

        errors = validate_student_dataframe(df)

        if errors.empty:

            st.success("Doğrulama başarılı.")

            st.button(
                "📥 Veritabanına Aktar",
                type="primary",
                use_container_width=True,
            )

        else:

            st.error(
                f"{len(errors)} hata bulundu."
            )

            st.dataframe(
                errors,
                hide_index=True,
                use_container_width=True,
            )

    with tab2:

        st.info("Henüz öğrenci bulunmuyor.")

    with tab3:

        st.info("Henüz veli bulunmuyor.")
