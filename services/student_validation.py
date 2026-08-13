import pandas as pd


def validate_student_dataframe(df: pd.DataFrame):

    errors = []

    # -------------------------------------------------
    # Boş Okul No
    # -------------------------------------------------

    for index, value in enumerate(df["OKUL NO"], start=2):

        if str(value).strip() == "":

            errors.append(
                f"{index}. satır → OKUL NO boş."
            )

    # -------------------------------------------------
    # Aynı Okul No
    # -------------------------------------------------

    duplicated = df[
        df["OKUL NO"].duplicated(keep=False)
    ]

    for _, row in duplicated.iterrows():

        errors.append(
            f"OKUL NO tekrar ediyor : {row['OKUL NO']}"
        )

    # -------------------------------------------------
    # Öğrenci Adı
    # -------------------------------------------------

    for index, value in enumerate(
        df["ÖĞRENCİ ADI"],
        start=2,
    ):

        if str(value).strip() == "":

            errors.append(
                f"{index}. satır → Öğrenci adı boş."
            )

    # -------------------------------------------------
    # Öğrenci Soyadı
    # -------------------------------------------------

    for index, value in enumerate(
        df["ÖĞRENCİ SOYADI"],
        start=2,
    ):

        if str(value).strip() == "":

            errors.append(
                f"{index}. satır → Öğrenci soyadı boş."
            )

    # -------------------------------------------------
    # Sınıf
    # -------------------------------------------------

    for index, value in enumerate(
        df["SINIFI"],
        start=2,
    ):

        if str(value).strip() == "":

            errors.append(
                f"{index}. satır → Sınıf bilgisi boş."
            )

    return errors
