import numpy as np
import pandas as pd

from ascs.input_data.validators.easy_read_validator import EasyReadValidator


def test_easy_read_validator():
    df_in = pd.DataFrame(
        [
            [211, 1, 1, False, 4],
            [211, 2, 2, False, 8],
            [211, 3, 3, True, 4],
            [211, 4, 4, True, 7],
            [211, 5, 5, True, 8],
            [211, 6, 6, True, np.nan],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "is_easy_read", "abc"],
    )

    expected_questionnaire = pd.DataFrame(
        [
            [211, 1, 1, False, 4],
            [211, 2, 2, False, np.nan],
            [211, 3, 3, True, 4],
            [211, 4, 4, True, np.nan],
            [211, 5, 5, True, np.nan],
            [211, 6, 6, True, np.nan],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "is_easy_read", "abc"],
    )

    expected_error = pd.DataFrame(
        [
            [
                211,
                2,
                2,
                "Column abc was 8.0 when accepted values are [1, 2, 3, 4, 5, 6, 7, nan] for users who recieved the standard questionnaire",
            ],
            [
                211,
                4,
                4,
                "Column abc was 7.0 when accepted values are [1, 2, 3, 4, 5, nan] for users who recieved the easy read questionnaire",
            ],
            [
                211,
                5,
                5,
                "Column abc was 8.0 when accepted values are [1, 2, 3, 4, 5, nan] for users who recieved the easy read questionnaire",
            ],
        ],
        index=[1, 3, 4],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )

    actual_questionnaire, (actual_error,) = EasyReadValidator("abc").run_check(df_in)

    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
    pd.testing.assert_frame_equal(actual_error, expected_error)
