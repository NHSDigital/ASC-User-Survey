import numpy as np
import pandas as pd

from ascs.input_data.validators.whole_number_validator import WholeNumberValidator


def test_whole_number_validator():
    df_questionnaire = pd.DataFrame(
        {
            "LaCode": [101, 102, 103],
            "PrimaryKey": [1, 2, 3],
            "SerialNo": [11, 22, 33],
            "abc": [5, 5.5, np.nan],
        }
    )

    expected_questionnaire = pd.DataFrame(
        {
            "LaCode": [101, 102, 103],
            "PrimaryKey": [1, 2, 3],
            "SerialNo": [11, 22, 33],
            "abc": [5, np.nan, np.nan],
        }
    )

    expected_err = pd.DataFrame(
        {
            "LaCode": [102],
            "PrimaryKey": [2],
            "SerialNo": [22],
            "message": ["Column abc was 5.5 but should be a whole number"],
        },
        index=[1],
    )

    actual_questionnaire, (actual_error,) = WholeNumberValidator(
        column="abc"
    ).run_check(df_questionnaire,)

    pd.testing.assert_frame_equal(actual_error, expected_err)
    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
