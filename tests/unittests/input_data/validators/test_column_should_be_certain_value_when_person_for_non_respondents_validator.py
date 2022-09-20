import numpy as np
from ascs.input_data.validators.column_should_be_certain_value_for_non_respondents_validator import (
    ColumnShouldBeCertainValueForNonRespondentsValidator,
)
import pandas as pd


def test_check_column_is_1_when_person_did_not_respond_to_survey():
    test_check_column_is_1_when_person_did_not_respond_to_survey_dataframe = pd.DataFrame(
        [
            [211, 1, 1, 1, 2],
            [211, 2, 2, 1, 1],
            [211, 3, 3, 1, 2],
            [211, 4, 4, 2, 1],
            [211, 5, 5, 2, 2],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "Response", "abc"],
    )
    expected_questionnaire = pd.DataFrame(
        [
            [211, 1, 1, 1, 2],
            [211, 2, 2, 1, 1],
            [211, 3, 3, 1, 2],
            [211, 4, 4, 2, np.nan],
            [211, 5, 5, 2, 2],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo", "Response", "abc"],
    )

    expected_error = pd.DataFrame(
        [
            [
                211,
                4,
                4,
                "Column abc must be 2 when the person did not respond to the questionnaire",
            ]
        ],
        index=[3],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )

    (
        actual_questionnaire,
        (actual_error,),
    ) = ColumnShouldBeCertainValueForNonRespondentsValidator(
        "abc", the_value_the_column_should_be_when_person_didnt_respond=2
    ).run_check(
        test_check_column_is_1_when_person_did_not_respond_to_survey_dataframe,
    )

    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
    pd.testing.assert_frame_equal(actual_error, expected_error)

