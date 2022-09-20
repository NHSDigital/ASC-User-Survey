import pandas as pd
from openpyxl import Workbook
from ascs import params
from ascs.output_to_excel.write_one_section_to_excel import write_one_section_to_excel


def output_all_tables_with_no_spacing(
    all_tables: dict[str, pd.DataFrame], template_wb: Workbook
):
    for (
        table_name,
        table_config,
    ) in params.EXCEL_NO_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME.items():
        table = all_tables[table_name]
        write_one_section_to_excel(
            table,
            template_wb[table_config.SHEET_NAME],
            table_config.START_ROW,
            table_config.START_COLUMN,
        )
