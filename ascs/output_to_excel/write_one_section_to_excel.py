import pandas as pd
from openpyxl.worksheet.worksheet import Worksheet


def write_one_section_to_excel(
    df_section_by_response: pd.DataFrame,
    table_sheet: Worksheet,
    section_start_row: int,
    section_start_column: int,
) -> None:
    question_by_response_rows = df_section_by_response.values.tolist()
    for row_index, row_of_table in enumerate(
        question_by_response_rows, section_start_row
    ):
        for column_index, cell_value in enumerate(row_of_table, section_start_column):
            table_sheet.cell(row=row_index, column=column_index, value=cell_value)

