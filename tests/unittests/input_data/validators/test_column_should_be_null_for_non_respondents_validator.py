import numpy as np
from ascs.input_data.validators.column_should_be_null_for_non_respondents_validator import (
    ColumnShouldBeNullForNonRespondentsValidator,
)
import pandas as pd


def test_check_column_is_1_when_person_did_not_respond_to_survey():
    test_check_column_is_1_when_person_did_not_respond_to_survey_dataframe = pd.DataFrame(
        [
            [211, 1, 1, 1, 2],
            [211, 2, 2, 1, np.nan],
            [211, 4, 4, 2, np.nan],
            [211, 5, 5, 2, 2],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "Response", "abc"],
    )
    expected_questionnaire = pd.DataFrame(
        [
            [211, 1, 1, 1, 2],
            [211, 2, 2, 1, np.nan],
            [211, 4, 4, 2, np.nan],
            [211, 5, 5, 2, np.nan],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "Response", "abc"],
    )

    expected_error = pd.DataFrame(
        [
            [
                211,
                5,
                5,
                "Column abc was 2.0 but should be blank when the person did not respond to the questionnaire",
            ]
        ],
        index=[3],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )

    (
        actual_questionnaire,
        (actual_error,),
    ) = ColumnShouldBeNullForNonRespondentsValidator("abc").run_check(
        test_check_column_is_1_when_person_did_not_respond_to_survey_dataframe,
    )

    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
    pd.testing.assert_frame_equal(actual_error, expected_error)

