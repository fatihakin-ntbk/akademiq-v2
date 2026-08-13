import pandas as pd


REQUIRED_COLUMNS = [
    "OKUL NO",
    "ÖĞRENCİ ADI",
    "ÖĞRENCİ SOYADI",
    "ÖĞRENCİ TC KİMLİK NO",
    "SINIFI",
    "VELİ YAKINLIĞI",
    "VELİ ADI",
    "VELİ SOYADI",
    "VELİ TELEFON",
    "VELİ TC KİMLİK NO",
]


def read_student_excel(uploaded_file):

    df = pd.read_excel(
        uploaded_file,
        dtype=str,
    )

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    missing_columns = []

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:

        raise ValueError(

            "Eksik sütunlar:\n\n"

            + "\n".join(missing_columns)

        )

    df = df.fillna("")

    return df
