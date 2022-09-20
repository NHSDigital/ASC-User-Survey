import pytest
import pandas as pd
from ascs.input_data.preprocess_eligible_population.melt_stratum_population import (
    melt_stratum_population,
)


def test_melt_stratum_population():
    example_ep_dataframe = pd.DataFrame(
        {
            "LaCode": [100, 200, 300],
            "stratum1Pop": [10, 11, 12],
            "stratum2Pop": [20, 21, 22],
            "stratum3Pop": [30, 31, 32],
            "stratum4Pop": [40, 41, 42],
        }
    )

    actual = melt_stratum_population(example_ep_dataframe)
    expected = pd.DataFrame(
        {
            "LaCode": [100, 200, 300, 100, 200, 300, 100, 200, 300, 100, 200, 300],
            "Stratum": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
            "la_stratum_pop": [10, 11, 12, 20, 21, 22, 30, 31, 32, 40, 41, 42],
        }
    )

    pd.testing.assert_frame_equal(actual, expected)
