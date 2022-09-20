import numpy as np
from ascs.utilities.get_respondents_by_columns import get_respondents_by_columns
import pandas as pd


def test_get_respondents_by_columns():
    df_input = pd.DataFrame(
        [[211, 1], [916, 1], [916, np.nan], [916, None], [916, 2]],
        columns=["LaCode", "q20"],
    )

    actual = get_respondents_by_columns(df_input, "q20", groupby_columns="LaCode")

    expected = pd.Series([1, 2], name="q20", index=pd.Index([211, 916], name="LaCode"))

    pd.testing.assert_series_equal(actual, expected)
