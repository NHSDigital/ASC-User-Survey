import logging
from pathlib import Path
import warnings
import pandas as pd

from openpyxl import load_workbook
import os

from typing import Optional

from .data_return_config import LoadedDataReturns
from .service_user_data import get_service_user_data_from_workbook
from .worksheets import SIGN_OFF_SHEET_NAME, check_workbook_has_needed_worksheets
from ..checkpoint.checkpoint_config import CHECKPOINTS_DIRECTORY
from ..checkpoint.checkpoint_file_handler import save_data_return_checkpoint
from ascs import params


LA_CODE_CELL_REF = "E2"


def load_all_data_returns_from_excel(
    directory: Optional[str] = None,
) -> LoadedDataReturns:
    if directory is None:
        directory = params.DATA_RETURNS_DIRECTORY

    data_return_file_paths = get_all_data_return_file_paths(directory)

    data_return_dfs: list[pd.DataFrame] = []
    load_file_errors: list[dict] = []

    for file_path in data_return_file_paths:
        try:
            df_questionnaire_in_la_by_person = load_one_data_return(file_path)
            data_return_dfs.append(df_questionnaire_in_la_by_person)
        except Exception as err:
            logging.error(f"Error loading {file_path}")
            logging.error(err)
            load_file_errors.append({"file_path": file_path, "error_message": str(err)})

    df_questionnaire_by_person = pd.concat(data_return_dfs, axis=0, ignore_index=True)
    df_by_loading_error = (
        pd.DataFrame(load_file_errors)
        if load_file_errors
        else pd.DataFrame([["No errors while loading files!"]])
    )

    loaded_data_returns = LoadedDataReturns(
        df_questionnaire_unclean_by_person=df_questionnaire_by_person,
        df_loading_error_by_file=df_by_loading_error,
    )

    save_data_return_checkpoint(
        loaded_data_returns, Path(CHECKPOINTS_DIRECTORY + params.PUBLICATION_YEAR),
    )
    logging.info("Checkpoint saved!")

    return loaded_data_returns


def get_all_data_return_file_paths(directory: str):
    directory: Path = Path(directory)

    data_return_file_paths = [
        str((directory / file_path).resolve())
        for file_path in os.listdir(directory)
        if file_path.endswith(".xlsx") and not file_path.startswith("~$")
    ]

    return data_return_file_paths


def load_one_data_return(file_path: str) -> pd.DataFrame:
    logging.info(file_path)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = load_workbook(file_path, data_only=True, read_only=True)

    check_workbook_has_needed_worksheets(wb)

    la_code = wb[SIGN_OFF_SHEET_NAME][LA_CODE_CELL_REF].value
    assert (
        la_code is not None and la_code != ""
    ), "LA Code (cell E2, sheet Sign Off Sheet) - likely the excel file has been damaged"
    assert (
        "select la name" not in str(la_code).lower()
    ), "LA not selected (cell E3, Sign Off Sheet)"

    la_code = str(la_code)

    df_questionnaire_in_la_by_person = get_service_user_data_from_workbook(wb, la_code)

    wb.close()

    return df_questionnaire_in_la_by_person
