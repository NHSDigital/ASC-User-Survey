import numpy as np
import pandas as pd
from ascs.input_data.validators.is_in_validator import IsInValidator


def test_get_error_df():
    df_in = pd.DataFrame(
        [[211, 3, 4, 133], [211, 5, 6, 1]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "abc"],
    )
    series_in = pd.Series([True, False])
    actual = IsInValidator("abc", [1, 2, 3]).get_error_df(df_in, series_in)
    expected = pd.DataFrame(
        [[211, 3, 4, "Column abc was 133 when accepted values are [1, 2, 3]"]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_get_where_incorrect():
    df_in = pd.DataFrame([[133], [1]], columns=["abc"],)
    actual = IsInValidator("abc", [1, 2, 3]).get_where_incorrect(df_in)
    expected = pd.Series([True, False], name="abc")
    pd.testing.assert_series_equal(actual, expected)


def test_run_check():
    df_in = pd.DataFrame(
        [[311, 1, 2, 2], [211, 3, 4, 133], [211, 5, 6, 1]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "abc"],
    )
    expected_error = pd.DataFrame(
        [[211, 3, 4, "Column abc was 133 when accepted values are [1, 2, 3]"]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
        index=[1],
    )
    expected_questionnaire = pd.DataFrame(
        [[311, 1, 2, 2], [211, 3, 4, np.nan], [211, 5, 6, 1]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "abc"],
    )

    actual_questionnaire, (actual_error,) = IsInValidator("abc", [1, 2, 3]).run_check(
        df_in
    )

    pd.testing.assert_frame_equal(actual_error, expected_error)
    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)

