import pandas as pd
import numpy as np

from ascs.response_rate_by_area.response_rate_by_la import (
    calc_question_response_rate_by_la,
    calc_total_response_rate_column,
)


def test_calc_total_response_rate():
    df_in = pd.DataFrame(
        [[211, 1], [211, 1], [211, 2], [211, 3], [311, 1]],
        columns=["LaCode", "Response"],
    )
    empty_annex_table4 = pd.DataFrame()
    actual = calc_total_response_rate_column(empty_annex_table4, df_in)

    expected_series_input = pd.Series(
        [0.5, 1], index=pd.Index([211, 311], name="LaCode")
    )

    expected = pd.DataFrame(expected_series_input, columns=["total_response_rate"])

    pd.testing.assert_frame_equal(actual, expected)


def test_calc_question_response_rate():
    df_in = pd.DataFrame(
        [
            [211, 1, 1, 3],
            [211, 1, 1, np.nan],
            [211, 1, 2, np.nan],
            [211, 2, np.nan, np.nan],
            [311, 1, 5, 5],
        ],
        columns=["LaCode", "Response", "q3a", "q4a"],
    )

    actual = calc_question_response_rate_by_la(df_in, ["q3a", "q4a"])

    expected = pd.DataFrame(
        [[1.0, 1 / 3], [1.0, 1.0]],
        columns=["q3a", "q4a"],
        index=pd.Index([211, 311], name="LaCode"),
    )

    pd.testing.assert_frame_equal(actual, expected)
