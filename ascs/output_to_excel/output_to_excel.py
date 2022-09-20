import logging
import pandas as pd
from typing import Optional
from openpyxl import load_workbook
from ascs.output_to_excel.output_to_excel_column_and_row_spacing import (
    output_all_tables_with_column_and_row_spacing,
)
from ascs.output_to_excel.output_to_excel_no_spacing import (
    output_all_tables_with_no_spacing,
)
from ascs.output_to_excel.output_to_excel_column_spacing import (
    output_all_tables_with_column_spacing,
)
from ascs import params


def output_annex_table_excel_file(
    all_tables: dict[str, pd.DataFrame],
    template_path: Optional[str] = None,
    output_path: Optional[str] = None,
):
    if template_path is None:
        template_path = params.TEMPLATE_ANNEX_TABLE_FILE_PATH
    if output_path is None:
        output_path = f"./outputs/{params.OUTPUT_ANNEX_TABLE_FILE_NAME}"

    template_wb = load_workbook(template_path)

    logging.info("Saving stratified by la tables to excel...")
    output_all_tables_with_column_spacing(all_tables, template_wb)
    logging.info("Finished saving stratified by la tables to excel...")

    logging.info(
        "Saving stratified by demographic and stratified by response tables to excel..."
    )
    output_all_tables_with_column_and_row_spacing(all_tables, template_wb)
    logging.info(
        "Finished saving stratified by demographic and stratified by response tables to excel..."
    )

    logging.info("Saving annex table 4 and annex table 6 to excel...")
    output_all_tables_with_no_spacing(all_tables, template_wb)
    logging.info("Finished saving annex table 4 and annex table 6 to excel...")

    template_wb.save(output_path)
