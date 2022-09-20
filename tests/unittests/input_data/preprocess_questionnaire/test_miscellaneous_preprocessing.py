import numpy as np
import pandas as pd

from ascs.input_data.preprocess_questionnaire.miscellaneous_preprocessing import (
    add_stratum_column,
)


def test_add_stratum_column():
    df_in = pd.DataFrame(
        [
            [7, 20, 1],
            [6, 65, 1],
            [6, 22, 1],
            [6, 68, 1],
            [6, 68, 3],
            [7, 60, 1],
            [np.nan, 30, 1],
            [5, np.nan, 1],
            [5, 89, np.nan],
        ],
        columns=["PrimarySupportReason", "Age", "SupportSetting",],
    )

    df_expected = pd.DataFrame(
        [
            [7, 20, 1, 1],
            [6, 65, 1, 4],
            [6, 22, 1, 2],
            [6, 68, 1, 4],
            [6, 68, 3, 3],
            [7, 60, 1, 1],
            [np.nan, 30, 1, np.nan],
            [5, np.nan, 1, np.nan],
            [5, 89, np.nan, np.nan],
        ],
        columns=["PrimarySupportReason", "Age", "SupportSetting", "Stratum"],
    )

    df_actual = add_stratum_column(df_in)

    pd.testing.assert_frame_equal(df_actual, df_expected)
