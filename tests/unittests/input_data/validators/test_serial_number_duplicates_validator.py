import pandas as pd
from ascs.input_data.validators.serial_number_duplicates_validator import (
    SerialNumberDuplicatesValidator,
)


def test_serial_number_duplicates_validator():
    df_in = pd.DataFrame(
        {
            "LaCode": [211, 211, 211, 213, 213],
            "SerialNo": [1, 2, 2, 1, 2],
            "PrimaryKey": [1, 2, 3, 4, 5],
        }
    )

    questionnaire_expected = df_in.copy()

    errors_expected = pd.DataFrame(
        [
            [211, 2, 2, "serial number 2 not unique in LA 211"],
            [211, 3, 2, "serial number 2 not unique in LA 211"],
        ],
        index=[1, 2],
        columns=["LaCode", "PrimaryKey", "SerialNo", "message"],
    )

    (
        actual_questionnaire,
        (actual_errors,),
    ) = SerialNumberDuplicatesValidator().run_check(df_in)

    pd.testing.assert_frame_equal(actual_questionnaire, questionnaire_expected)
    pd.testing.assert_frame_equal(actual_errors, errors_expected)
