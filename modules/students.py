import streamlit as st
import pandas as pd

from services.student_template import create_student_template
from services.student_import import read_student_excel
from services.student_validation import validate_student_dataframe
from services.student_database import import_students
from services.student_list import get_students


def show(engine):

    st.title("👨‍🎓 Öğrenci & Veli Yönetimi")

    tab1, tab2, tab3 = st.tabs(
        [
            "📥 Öğrenci Aktar",
            "👨‍🎓 Öğrenciler",
            "👨‍👩‍👦 Veliler",
        ]
    )

    # =====================================================
    # TAB 1
    # =====================================================

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

        else:

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
                df["VELİ ADI"] + " " + df["VELİ SOYADI"]
            )

            st.subheader("Önizleme")

            st.dataframe(
                preview.head(10),
                hide_index=True,
                use_container_width=True,
            )

            st.info(
                f"Toplam {len(df)} öğrenci bulundu."
            )

            st.divider()

            st.subheader("3️⃣ Doğrulama")

            errors = validate_student_dataframe(df)

            if errors.empty:

                st.success("Doğrulama başarılı.")

                if st.button(
                    "📥 Veritabanına Aktar",
                    type="primary",
                    use_container_width=True,
                ):

                    try:

                        count = import_students(
                            engine,
                            df,
                        )

                        st.success(
                            f"{count} öğrenci başarıyla aktarıldı."
                        )

                    except Exception as e:

                        st.error(str(e))

            else:

                st.error(
                    f"{len(errors)} hata bulundu."
                )

                st.dataframe(
                    errors,
                    hide_index=True,
                    use_container_width=True,
                )
        # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.subheader("👨‍🎓 Öğrenciler")

        search = st.text_input(
            "Ara (Okul No, Ad veya Soyad)"
        )

        students = get_students(
            engine,
            search,
        )

        st.info(
            f"Toplam {len(students)} öğrenci bulundu."
        )

        if students.empty:

            st.warning(
                "Aktif dönemde öğrenci bulunamadı."
            )

        else:

            students["Ad Soyad"] = (
                students["ad"]
                + " "
                + students["soyad"]
            )

            table = students[
                [
                    "ogrenci_no",
                    "Ad Soyad",
                    "sinif",
                ]
            ].rename(
                columns={
                    "ogrenci_no": "Okul No",
                    "sinif": "Sınıf",
                }
            )

            st.dataframe(
                table,
                hide_index=True,
                use_container_width=True,
            )
      # =====================================================
    # TAB 3
    # =====================================================

    with tab3:

        from services.parent_list import get_parents

        st.subheader("👨‍👩‍👦 Veliler")

        search = st.text_input(
            "Ara (Ad, Soyad veya Telefon)",
            key="parent_search",
        )

        parents = get_parents(
            engine,
            search,
        )

        st.info(
            f"Toplam {len(parents)} veli bulundu."
        )

        if parents.empty:

            st.warning(
                "Kayıtlı veli bulunamadı."
            )

        else:

            parents["Veli"] = (
                parents["ad"]
                + " "
                + parents["soyad"]
            )

            table = parents[
                [
                    "Veli",
                    "telefon",
                    "ogrenci_sayisi",
                ]
            ].rename(
                columns={
                    "telefon": "Telefon",
                    "ogrenci_sayisi": "Öğrenci Sayısı",
                }
            )

            st.dataframe(
                table,
                hide_index=True,
                use_container_width=True,
            )
        st.info(
            "Bu modül bir sonraki adımda geliştirilecek."
        )
