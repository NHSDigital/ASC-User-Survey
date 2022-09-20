import numpy as np
import pandas as pd

from openpyxl import Workbook

from typing import Optional, Union

from ascs import params
from ascs.input_data.load_data_returns.worksheets import SERVICE_USER_DATA_SHEET_NAME


COLUMNS_TO_DROP_BECAUSE_WE_RECALCULATE_THEM_LATER = [
    "Stratum",
    "PopInStratum",
]


def get_service_user_data_from_workbook(
    wb: Workbook, la_code: Union[str, int]
) -> pd.DataFrame:
    service_user_data_np = get_worksheet_as_np_array_from_workbook(
        wb, SERVICE_USER_DATA_SHEET_NAME
    )
    service_user_data_np = select_only_initial_expected_columns(service_user_data_np)

    check_service_user_data_column_names(service_user_data_np)

    df_service_user_data = (
        place_service_user_data_in_dataframe(service_user_data_np)
        .pipe(ignore_rows_where_there_isnt_a_person)
        .infer_objects()
        .assign(LaCode=la_code)
        .pipe(set_primary_key)
        .drop(columns=COLUMNS_TO_DROP_BECAUSE_WE_RECALCULATE_THEM_LATER)
    )

    return df_service_user_data


def set_primary_key(df_service_user_data: pd.DataFrame) -> pd.DataFrame:
    df_service_user_data["PrimaryKey"] = (
        df_service_user_data["LaCode"].astype(str)
        + "_"
        + df_service_user_data.index.to_series().astype(str)
    )

    return df_service_user_data


def ignore_rows_where_there_isnt_a_person(
    df_service_user_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    When we open the excel data, we recieve many more rows than people, there are empty rows at the end.
    Discard the empty rows.
    If the row has a person, the MethodCollection and Response column won't be null, we use this to choose the rows to discard.
    """
    method_collection_null_by_row = df_service_user_data["MethodCollection"].isna()
    response_null_by_row = df_service_user_data["Response"].isna()

    nulls_align_by_row = method_collection_null_by_row == response_null_by_row

    assert nulls_align_by_row.all(), f"""
There are rows where method collection is empty but the response is not or visa versa.
Both are required properties, this misalignment could result in a person being lost from the analysis.
Rows with misalignment (where the first person is at row zero): {df_service_user_data.index[~nulls_align_by_row].to_list()}
"""

    return df_service_user_data[~method_collection_null_by_row]


def place_service_user_data_in_dataframe(
    service_user_data_np: np.ndarray,
) -> pd.DataFrame:
    return pd.DataFrame(
        service_user_data_np[1:, :],
        columns=list(
            params.DATA_RETURN.NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING.values()
        ),
    )


def select_only_initial_expected_columns(
    service_user_data_np: np.ndarray,
) -> np.ndarray:
    """
    select the number of columns that we expect from params
    discard columns in the excel that we dont need
    """
    number_of_columns_to_keep = len(
        params.DATA_RETURN.NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING
    )
    return service_user_data_np[:, :number_of_columns_to_keep]


def get_worksheet_as_np_array_from_workbook(wb: Workbook, sheet_name: str) -> np.array:
    return np.array(list(wb[sheet_name].values))


def check_service_user_data_column_names(
    service_user_data_np: np.ndarray,
    expected_column_substrings: Optional[list[str]] = None,
) -> None:
    if expected_column_substrings is None:
        expected_column_substrings = (
            params.DATA_RETURN.NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING.keys()
        )

    actual_columns = service_user_data_np[0]

    assert len(actual_columns) == len(
        expected_column_substrings
    ), "Actual length of columns != Expected length of columns somehow. This is a bug."

    incorrect_column_messages = [
        f"At column {i+1} expected a column like '{expected_column_substring}' but saw '{actual_column_name}'"
        for i, (actual_column_name, expected_column_substring) in enumerate(
            zip(actual_columns, expected_column_substrings)
        )
        if standardize_column_name(expected_column_substring)
        not in standardize_column_name(actual_column_name)
    ]

    incorrect_column_messages_joined = "\n".join(incorrect_column_messages)

    assert (
        len(incorrect_column_messages) == 0
    ), f"""
In the sheet {SERVICE_USER_DATA_SHEET_NAME} we expect certain columns in a certain order.
The following columns below are missing, misspelled or in the wrong order.

Note: The columns don't have to exactly match, just be similar.

Incorrect columns:
{incorrect_column_messages_joined}
"""


def standardize_column_name(column_name):
    if column_name is None:
        column_name = "< BLANK >"
    for character_to_remove in [" ", "_", "[", "]", "(", ")"]:
        column_name = column_name.replace(character_to_remove, "")
    return column_name.lower()
