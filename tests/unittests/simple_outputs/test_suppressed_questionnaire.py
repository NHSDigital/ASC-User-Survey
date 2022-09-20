import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation

from ascs.simple_outputs.suppressed_questionnaire import create_suppressed_questionnaire


def test_create_suprressed_questionnaire():
    df_in = pd.DataFrame(
        [[211, 1, 1], [211, 1, 1], [211, 1, 1], [211, 2, 2], [211, 3, 3], [311, 1, 1]],
        columns=["a", "b", "Age_Grouped"],
    )
    input_data = DataNeededForTableCreation(df_in, None, None, None, None)

    actual = create_suppressed_questionnaire(
        input_data, ["a", "b"], ["a", "b", "Age_Grouped"], ["a", "b"], {}
    )

    expected = pd.DataFrame(
        [[211, 1, 1], [211, 1, 1], [211, 1, 1], [99, 99, 2], [99, 99, 3], [99, 99, 1]],
        columns=["a", "b", "Age_Grouped"],
    )

    pd.testing.assert_frame_equal(actual["suppressed_questionnaire"], expected)
