import pandas as pd


def validate_student_dataframe(df: pd.DataFrame):

    errors = []

    # OKUL NO
    for row, value in enumerate(df["OKUL NO"], start=2):
        if str(value).strip() == "":
            errors.append({
                "Satır": row,
                "Alan": "OKUL NO",
                "Hata": "Boş"
            })

    # Tekrar eden OKUL NO
    duplicated = df[df["OKUL NO"].duplicated(keep=False)]

    for row, value in duplicated["OKUL NO"].items():
        errors.append({
            "Satır": row + 2,
            "Alan": "OKUL NO",
            "Hata": f"Tekrar ediyor ({value})"
        })

    # AD
    for row, value in enumerate(df["ÖĞRENCİ ADI"], start=2):
        if str(value).strip() == "":
            errors.append({
                "Satır": row,
                "Alan": "ÖĞRENCİ ADI",
                "Hata": "Boş"
            })

    # SOYAD
    for row, value in enumerate(df["ÖĞRENCİ SOYADI"], start=2):
        if str(value).strip() == "":
            errors.append({
                "Satır": row,
                "Alan": "ÖĞRENCİ SOYADI",
                "Hata": "Boş"
            })

    # SINIF
    for row, value in enumerate(df["SINIFI"], start=2):
        if str(value).strip() == "":
            errors.append({
                "Satır": row,
                "Alan": "SINIFI",
                "Hata": "Boş"
            })

    return pd.DataFrame(errors)
