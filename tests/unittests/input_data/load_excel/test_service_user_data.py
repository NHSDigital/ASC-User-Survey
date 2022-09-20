from typing import Any
import numpy as np
from openpyxl import Workbook, load_workbook

from pathlib import Path
import pandas as pd

import pytest

from ascs.input_data.load_data_returns.service_user_data import (
    SERVICE_USER_DATA_SHEET_NAME,
    check_service_user_data_column_names,
    get_service_user_data_from_workbook,
    get_worksheet_as_np_array_from_workbook,
    ignore_rows_where_there_isnt_a_person,
    select_only_initial_expected_columns,
)

from ascs import params

this_directory = Path(__file__).parent


@pytest.fixture(scope="session")
def service_data_example_wb():
    return load_workbook(
        filename=(
            this_directory / "service_data_example_test_data_return.xlsx"
        ).resolve(),
        data_only=True,
    )


@pytest.fixture(scope="session")
def service_data_example(service_data_example_wb) -> np.ndarray:
    service_data_example = get_worksheet_as_np_array_from_workbook(
        service_data_example_wb, SERVICE_USER_DATA_SHEET_NAME
    )
    return service_data_example


TEST_NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING = {
    "la code": "LaCode",
    "serial number": "SerialNo",
    "primary key": "PrimaryKey",
    "stratum": "Stratum",
    "population in stratum": "PopInStratum",
    "method of collection": "MethodCollection",
    "response": "Response",
}


def test_get_service_user_data_from_workbook(
    service_data_example_wb: Workbook, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        params.DATA_RETURN,
        "NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING",
        TEST_NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING,
    )

    df_service_user_data_actual = get_service_user_data_from_workbook(
        service_data_example_wb, la_code=555
    )

    df_service_user_data_expected = pd.DataFrame(
        [[555, 1, "555_0", 1, 1], [555, 5, "555_1", 1, 2]],
        columns=["LaCode", "SerialNo", "PrimaryKey", "MethodCollection", "Response"],
    )

    pd.testing.assert_frame_equal(
        df_service_user_data_actual, df_service_user_data_expected
    )


def test_select_only_initial_expected_columns(
    service_data_example: np.ndarray, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        params.DATA_RETURN,
        "NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING",
        {"col 1": "blah"},
    )
    service_data_example_columns_cut = select_only_initial_expected_columns(
        service_data_example
    )
    assert service_data_example_columns_cut.shape[1] == 1


def test_check_columns__doesnt_error_when_columns_correct(
    service_data_example: np.ndarray,
) -> None:
    check_service_user_data_column_names(
        service_data_example,
        [
            "LACode",
            "serial number",
            "primary_key",
            "stratum",
            "populationIn stratum",
            "method of collection",
            "r[[esp]]onse",
        ],
    )


def test_check_columns__does_error_when_columns_incorrect(
    service_data_example: np.ndarray,
) -> None:
    with pytest.raises(AssertionError) as err:
        check_service_user_data_column_names(
            service_data_example,
            [
                "LB Code",
                "serial number",
                "secondary key",
                "stratum",
                "population in stratum",
                # the below two are out of order
                "response",
                "method of collection",
            ],
        )

    error_message = str(err.value)

    assert "LB Code" in error_message
    assert "la code" in error_message.lower()
    assert "secondary key" in error_message
    assert "serial number" not in error_message
    assert "stratum" not in error_message.lower()
    assert "response" in error_message
    assert "method of collection" in error_message


@pytest.mark.parametrize(
    "method_collection_values,response_values,row_with_issue",
    [(["aligned", None], [1, 2], 1), (["unaligned", "aligned"], [np.nan, 2], 0)],
)
def test_ignore_rows_where_there_isnt_a_person__throws_error_for_misaligned(
    method_collection_values: list[Any], response_values: list[Any], row_with_issue: int
) -> None:
    df_in = pd.DataFrame(
        {"MethodCollection": method_collection_values, "Response": response_values}
    )

    with pytest.raises(AssertionError) as err:
        ignore_rows_where_there_isnt_a_person(df_in)

    err_message = str(err.value)
    assert "misalign" in err_message
    assert str(row_with_issue) in err_message


def test_ignore_rows_where_there_isnt_a_person__correctly_ignores_rows():
    df_in = pd.DataFrame(
        {
            "MethodCollection": [1.0, 1, 1, None, None, None],
            "Response": [2.0, 2, 2, None, None, None],
        }
    )

    df_expected = pd.DataFrame(
        {"MethodCollection": [1.0, 1, 1], "Response": [2.0, 2, 2],}
    )

    df_actual = ignore_rows_where_there_isnt_a_person(df_in)

    pd.testing.assert_frame_equal(df_actual, df_expected)
