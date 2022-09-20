import pandas as pd

from ascs.input_data.preprocess_questionnaire.q2c_preprocessing import (
    add_can_answer_2c_column,
)


def test_add_can_answer_2c_column():
    df_input = pd.DataFrame(
        [
            ["Learning Disability Support", "a"],
            ["b", "Residential Care"],
            ["c", "Nursing Care"],
            ["d", "d"],
        ],
        columns=["PrimarySupportReason_Grouped", "SupportSetting_Grouped"],
    )
    actual = add_can_answer_2c_column(df_input)
    expected = pd.Series([False, False, False, True], name="can_answer_2c")
    pd.testing.assert_series_equal(actual["can_answer_2c"], expected)
