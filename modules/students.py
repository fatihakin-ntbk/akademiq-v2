import streamlit as st

from services.student_template import create_student_template


def show(engine):

    st.title("👨‍🎓 Öğrenci & Veli Yönetimi")

    tab1, tab2, tab3 = st.tabs(
        [
            "📥 Öğrenci Aktar",
            "👨‍🎓 Öğrenciler",
            "👨‍👩‍👦 Veliler",
        ]
    )

    # ===================================================
    # ÖĞRENCİ AKTAR
    # ===================================================

    with tab1:

        st.subheader("Öğrenci Excel Şablonu")

        st.write(
            "Lütfen önce sistemin oluşturduğu Excel şablonunu indiriniz."
        )

        st.download_button(
            label="📄 Öğrenci Excel Şablonunu İndir",
            data=create_student_template(),
            file_name="Ogrenci_Veli_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.divider()

        st.subheader("Excel Yükle")

        uploaded_file = st.file_uploader(
            "Excel dosyasını seçiniz",
            type=["xlsx"],
        )

        if uploaded_file is None:

            st.info(
                "Henüz herhangi bir Excel dosyası yüklenmedi."
            )

        else:

            st.success(
                f"{uploaded_file.name} başarıyla yüklendi."
            )

            st.info(
                "Bir sonraki adımda önizleme ekranı hazırlanacak."
            )

    # ===================================================
    # ÖĞRENCİLER
    # ===================================================

    with tab2:

        st.info(
            "Henüz öğrenci bulunmuyor."
        )

    # ===================================================
    # VELİLER
    # ===================================================

    with tab3:

        st.info(
            "Henüz veli bulunmuyor."
        )
