import pandas as pd
import numpy as np

from ascs.simple_outputs.admin_data_table import (
    calculate_proportion_missing_in_columns_by_la,
)


def test_calculate_proportion_missing_in_columns_by_la():
    df_input = pd.DataFrame(
        [[211, np.nan, 1], [211, 1, 1], [311, 1, 1], [311, 1, 1], [311, 1, np.nan]],
        columns=["LaCode", "abc", "def"],
    )
    df_actual = calculate_proportion_missing_in_columns_by_la(df_input)

    df_expected = pd.DataFrame(
        [[0.5, 0.0], [0.0, 1 / 3]],
        columns=["abc", "def"],
        index=pd.Index([211, 311], name="LaCode"),
    )

    pd.testing.assert_frame_equal(df_actual, df_expected)
