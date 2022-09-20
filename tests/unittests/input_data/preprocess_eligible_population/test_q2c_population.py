import pandas as pd

from ascs.input_data.preprocess_eligible_population.q2c_population import (
    remove_groups_that_cant_answer_2c_from_stratum_2_population_count,
)


def test_remove_groups_that_cant_answer_2c_from_stratum_2_population_count():
    df_input = pd.DataFrame(
        [[1, 1], [1, 2]], columns=["1864Residential", "stratum2Pop"]
    )

    actual = remove_groups_that_cant_answer_2c_from_stratum_2_population_count(df_input)
    
    expected = pd.DataFrame(
        [[1, 0], [1, 1]], columns=["1864Residential", "stratum2Pop"]
    )

    pd.testing.assert_frame_equal(actual, expected)

    df_input = pd.DataFrame([[1, 1], [1, 2]], columns=["1864", "stratum2Pop"])
    
    actual = remove_groups_that_cant_answer_2c_from_stratum_2_population_count(df_input)
    
    expected = pd.DataFrame([[1, 1], [1, 2]], columns=["1864", "stratum2Pop"])

    pd.testing.assert_frame_equal(actual, expected)
