import numpy as np
import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation

from ascs.methodology_figures.methodology_sample_split_by_column_table import (
    create_methodology_sample_split_by_column_table,
)


def test_create_methodology_sample_split_by_column_table():
    df_in = pd.DataFrame({"a": [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, np.nan]})

    df_expected = pd.DataFrame(
        {
            "population": [5, 10],
            "total_population": [10, 10],
            "percentage": [33.3, 66.7],
        },
        index=pd.Index([1.0, 2], name="a"),
    )

    df_actual = create_methodology_sample_split_by_column_table(
        DataNeededForTableCreation(df_questionnaire_by_person=df_in),
        column_to_split_by="a",
    )

    pd.testing.assert_frame_equal(df_actual, df_expected)
