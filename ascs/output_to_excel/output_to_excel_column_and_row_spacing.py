from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from ascs.output_to_excel.excel_config import ExcelConfig
from ascs.output_to_excel.write_one_section_to_excel import write_one_section_to_excel
from ascs import params
import pandas as pd


def output_all_tables_with_column_and_row_spacing(
    all_tables: dict[str, pd.DataFrame], template_wb: Workbook
) -> None:
    for (
        table_name,
        table_config,
    ) in params.EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME.items():
        table = all_tables[table_name]
        table_sheet = template_wb[table_config.SHEET_NAME]
        output_table_with_column_and_row_spacing(
            table_sheet, table_config, table,
        )


def output_table_with_column_and_row_spacing(
    table_sheet: Worksheet,
    excel_table_config: ExcelConfig,
    table_to_output: pd.DataFrame,
) -> None:
    current_row = excel_table_config.START_ROW

    for rows_section_label in table_to_output.index.unique(0):

        current_column = excel_table_config.START_COLUMN

        for columns_section_label in table_to_output.columns.unique(0):
            df_one_section = table_to_output.loc[
                rows_section_label, columns_section_label
            ]

            write_one_section_to_excel(
                df_one_section, table_sheet, current_row, current_column,
            )

            current_column += (
                len(df_one_section.columns) + excel_table_config.HORIZONTAL_GAP_SIZE
            )

        current_row += (
            len(table_to_output.loc[rows_section_label].index)
            + excel_table_config.VERTICAL_GAP_SIZE
        )
