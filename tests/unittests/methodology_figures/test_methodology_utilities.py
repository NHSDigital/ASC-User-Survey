import pandas as pd

from ascs.methodology_figures.utilities import calc_percentage_column


def test_calc_percentage_column():
    df_in = pd.DataFrame({"population": [5, 10], "total_population": [10, 10]})

    df_expected = pd.DataFrame(
        {"population": [5, 10], "total_population": [10, 10], "percentage": [50.0, 100]}
    )

    df_actual = calc_percentage_column(df_in)

    pd.testing.assert_frame_equal(df_actual, df_expected)
