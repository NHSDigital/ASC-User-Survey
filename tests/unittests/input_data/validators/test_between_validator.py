import numpy as np
import pandas as pd
from ascs.input_data.validators.between_validator import BetweenValidator


def test_run_check():
    df_in = pd.DataFrame(
        [[311, 1, 2, np.nan], [211, 3, 4, 133], [211, 5, 6, 1]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "abc"],
    )
    expected_error = pd.DataFrame(
        [
            [
                211,
                3,
                4,
                "Column abc was 133.0 when accepted values must be between 1 and 3",
            ]
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
        index=[1],
    )
    expected_questionnaire = pd.DataFrame(
        [[311, 1, 2, np.nan], [211, 3, 4, np.nan], [211, 5, 6, 1]],
        columns=["LaCode", "PrimaryKey", "SerialNo", "abc"],
    )

    actual_questionnaire, (actual_error,) = BetweenValidator("abc", 1, 3).run_check(
        df_in
    )

    pd.testing.assert_frame_equal(actual_error, expected_error)
    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)

