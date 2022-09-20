import numpy as np
import pandas as pd

from ascs.input_data.validators.numeric_column_validator import NumericColumnValidator


def test_numeric_column_validator() -> None:
    df_questionnaire = pd.DataFrame(
        {
            "LaCode": [101, 102, 103, 104],
            "PrimaryKey": [1, 2, 3, 4],
            "SerialNo": [11, 22, 33, 44],
            "abc": [5, 5.5, np.nan, "hello"],
        }
    )

    expected_questionnaire = pd.DataFrame(
        {
            "LaCode": [101, 102, 103, 104],
            "PrimaryKey": [1, 2, 3, 4],
            "SerialNo": [11, 22, 33, 44],
            "abc": [5, 5.5, np.nan, np.nan],
        }
    ).astype({"abc": object})

    expected_err = pd.DataFrame(
        {
            "LaCode": [104],
            "PrimaryKey": [4],
            "SerialNo": [44],
            "message": ["Column abc was 'hello' but should be a number"],
        },
        index=[3],
    )

    actual_questionnaire, (actual_error,) = NumericColumnValidator("abc").run_check(
        df_questionnaire,
    )

    pd.testing.assert_frame_equal(actual_error, expected_err)
    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
