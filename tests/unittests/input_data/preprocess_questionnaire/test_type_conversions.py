import numpy as np
import pandas as pd
import pytest

from ascs.input_data.preprocess_questionnaire.type_conversions import (
    make_string_columns_either_string_or_none,
    clean_types_in_numeric_columns,
)

from ascs import params


def test_clean_string_columns():
    df_in = pd.DataFrame({"abc": [1, "hi", None, np.nan, ""]})

    df_expected = pd.DataFrame({"abc": ["1", "hi", None, None, None]})

    df_actual = make_string_columns_either_string_or_none(df_in, ["abc"])

    pd.testing.assert_frame_equal(df_actual, df_expected)


def test_convert_numbers_in_numeric_columns():
    df_in = pd.DataFrame(
        {
            "abc": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
            "xyz": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
        }
    ).assign(LaCode=211, PrimaryKey=range(7), SerialNo=range(7))

    df_cleaned_expected = pd.DataFrame(
        {
            "abc": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
            "xyz": [1, 1, 1.5, np.nan, np.nan, np.nan, np.nan],
        }
    ).assign(LaCode=211, PrimaryKey=range(7), SerialNo=range(7))

    df_expected_by_error = pd.DataFrame(
        {
            "LaCode": [211],
            "PrimaryKey": [5],
            "SerialNo": [5],
            "message": ["Column xyz was 'hi' but should be a number"],
        },
        index=[5],
    )

    df_cleaned_actual, error_dfs = clean_types_in_numeric_columns(df_in, ["xyz"])

    pd.testing.assert_frame_equal(df_cleaned_actual, df_cleaned_expected)

    assert len(error_dfs) == 1
    df_actual_by_error = error_dfs[0]
    pd.testing.assert_frame_equal(df_actual_by_error, df_expected_by_error)


def test_convert_numbers_in_numeric_columns__gets_numeric_columns_correctly_from_params(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(params.DATA_RETURN, "STRING_COLUMNS", ["abc"])

    df_in = pd.DataFrame(
        {
            "abc": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
            "xyz": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
        }
    ).assign(LaCode=211, PrimaryKey=range(7), SerialNo=range(7))

    df_cleaned_expected = pd.DataFrame(
        {
            "abc": [1, "1", "1.5", np.nan, None, "hi", pd.NA],
            "xyz": [1, 1, 1.5, np.nan, np.nan, np.nan, np.nan],
        }
    ).assign(LaCode=211, PrimaryKey=range(7), SerialNo=range(7))

    df_cleaned_actual, error_dfs = clean_types_in_numeric_columns(df_in)

    pd.testing.assert_frame_equal(df_cleaned_actual, df_cleaned_expected)
