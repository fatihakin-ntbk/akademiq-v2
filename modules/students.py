import streamlit as st


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

        st.info(
            "Excel şablonu bu bölüme eklenecek."
        )

    with tab2:

        st.info(
            "Öğrenci listesi burada olacak."
        )

    with tab3:

        st.info(
            "Veli listesi burada olacak."
        )
