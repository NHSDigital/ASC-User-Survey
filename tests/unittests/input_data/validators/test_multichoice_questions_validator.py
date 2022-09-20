import numpy as np
import pandas as pd

from ascs.input_data.validators.multichoice_questions_validator import (
    MultichoiceQuestionsValidator,
)


def test_checks_multichoice_questions():
    sub_questions = ["q19a", "q19b", "19c"]
    message_error = f"The list of subquestions {sub_questions} has one of these problems: there is a mix of nulls and not nulls; all the subquestions were answered 2 (no)"
    df_input = pd.DataFrame(
        [
            [211, 1, 1, 1, 2, 2],
            [211, 2, 2, 2, 1, 1],
            [211, 3, 3, 2, 1, 2],
            [211, 4, 4, 1, 2, 1],
            [211, 6, 6, np.nan, np.nan, np.nan],
            [211, 7, 7, 2, 2, 2],
            [211, 8, 8, np.nan, 1, 1],
            [211, 9, 9, 1, np.nan, 1],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo"] + sub_questions,
    )
    expected_questionnaire = pd.DataFrame(
        [
            [211, 1, 1, 1, 2, 2],
            [211, 2, 2, 2, 1, 1],
            [211, 3, 3, 2, 1, 2],
            [211, 4, 4, 1, 2, 1],
            [211, 6, 6, np.nan, np.nan, np.nan],
            [211, 7, 7, np.nan, np.nan, np.nan],
            [211, 8, 8, np.nan, np.nan, np.nan],
            [211, 9, 9, np.nan, np.nan, np.nan],
        ],
        columns=["LaCode", "PrimaryKey", "SerialNo"] + sub_questions,
    )
    expected_error = pd.DataFrame(
        [
            [211, 7, 7, message_error],
            [211, 8, 8, message_error],
            [211, 9, 9, message_error],
        ],
        index=[5, 6, 7],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )
    actual_questionnaire, (actual_error,) = MultichoiceQuestionsValidator(
        sub_questions
    ).run_check(df_input)

    pd.testing.assert_frame_equal(actual_questionnaire, expected_questionnaire)
    pd.testing.assert_frame_equal(actual_error, expected_error)

