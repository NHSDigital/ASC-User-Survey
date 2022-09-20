import pandas as pd

from ascs.methodology_figures.population_sample_table import (
    place_total_populations_in_dataframe,
)


def test_place_total_populations_in_dataframe():
    tot_elig_pop = 1234
    tot_sample_pop = 456

    df_expected = pd.DataFrame(
        [["Total Eligible", 1234, 1234], ["Sample", 456, 1234],],
        columns=["group", "population", "total_population"],
    ).set_index("group")

    df_actual = place_total_populations_in_dataframe(tot_elig_pop, tot_sample_pop)

    pd.testing.assert_frame_equal(df_actual, df_expected)
