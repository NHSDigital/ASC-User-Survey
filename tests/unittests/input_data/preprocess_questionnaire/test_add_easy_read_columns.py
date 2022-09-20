import pandas as pd
import numpy as np
from ascs.input_data.preprocess_questionnaire.easy_read_columns import (
    add_columns_for_one_easy_read_question,
    clamp_std_answer_to_make_it_between_1_and_5,
)


def test_add_columns_for_one_easy_read_question():
    df_input = pd.DataFrame(
        [[False, 3], [True, 5], [False, 7], [False, 1], [True, 1], [False, 6]],
        columns=["is_easy_read", "q99"],
    )

    df_expected = pd.DataFrame(
        [
            [False, 3, np.nan, 3, 2],
            [True, 5, 5, np.nan, 5],
            [False, 7, np.nan, 7, 5],
            [False, 1, np.nan, 1, 1],
            [True, 1, 1, np.nan, 1],
            [False, 6, np.nan, 6, 5.0],
        ],
        columns=["is_easy_read", "q99", "q99ER", "q99Std", "q99Comb"],
    )

    add_columns_for_one_easy_read_question(df_input, "q99")

    pd.testing.assert_frame_equal(df_input, df_expected)


def test_clamp_std_answer_to_make_it_between_1_and_5():
    series_input = pd.Series([1, 2, 3, 4, 5, 6, 7])

    series_expected = pd.Series([1, 1, 2, 3, 4, 5, 5])

    series_actual = clamp_std_answer_to_make_it_between_1_and_5(series_input)

    pd.testing.assert_series_equal(series_actual, series_expected)
