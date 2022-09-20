import pandas as pd
import logging
from ascs.output_to_excel.output_to_excel import output_annex_table_excel_file


def save_all_tables_to_csv(all_tables: dict[str, pd.DataFrame]) -> None:
    logging.info("Saving files to csv...")
    for table_name, table in all_tables.items():
        table.to_csv(f"./outputs/{table_name}.csv")


def save_all_tables_to_excel(all_tables: dict[str, pd.DataFrame]) -> None:
    all_tables_has_tables_needed_for_excel = all(
        table_id in all_tables
        for table_id in ["1a", "1b", "2a", "2b", "3a", "3b", "4", "5", "6"]
    )
    if all_tables_has_tables_needed_for_excel:
        logging.info("Saving files to excel...")
        output_annex_table_excel_file(all_tables)
    else:
        logging.info(
            "Not all the tables needed for excel were generated, so we are not saving to excel."
        )
