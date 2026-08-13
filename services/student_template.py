from io import BytesIO

from openpyxl import Workbook


COLUMNS = [

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


def create_student_template():

    wb = Workbook()

    ws = wb.active

    ws.title = "Öğrenciler"

    for col, title in enumerate(COLUMNS, start=1):

        ws.cell(
            row=1,
            column=col,
            value=title,
        )

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return output
