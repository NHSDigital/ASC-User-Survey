import pandas as pd

from ascs.simple_outputs.eligible_population_questionnaire_data_disparity_dq_table import (
    create_eligible_population_questionnaire_data_disparity_dq_table,
)

from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)


def test_eligible_population_questionaire_data_disparity_dq_table():
    index_input_series = pd.MultiIndex.from_tuples(
        [(213, 1), (219, 1), (728, 1), (916, 4)], names=["LaCode", "Stratum"]
    )
    series = pd.Series([1, 1, 1, 2], index=index_input_series)
    dataframe = pd.DataFrame(
        [[213, 1], [219, 1], [728, 1], [916, 4]], columns=["LaCode", "Stratum"]
    )
    data_needed_for_table_creation = DataNeededForTableCreation(
        dataframe, None, series, None, None
    )
    index_expected = pd.MultiIndex.from_tuples([(916, 4)], names=["LaCode", "Stratum"])
    actual = create_eligible_population_questionnaire_data_disparity_dq_table(
        data_needed_for_table_creation
    )
    expected = pd.DataFrame(
        [[2, 1]],
        index=index_expected,
        columns=["expected_sample_population", "actual_sample_population",],
    )
    pd.testing.assert_frame_equal(actual["population_disparity_dq_table"], expected)
