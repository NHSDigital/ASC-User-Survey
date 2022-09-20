import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs.methodology_figures.utilities import (
    apply_rounding,
    calc_percentage_column,
)


def create_who_answered_population_sample_table(
    data_for_table_creation: DataNeededForTableCreation,
) -> pd.DataFrame:
    """
    Creates a table with the eligible pop and the sample pop
    and calcs % sample pop / eligible pop
    """
    total_eligible_pop = data_for_table_creation.population_by_la_stratum.sum()

    total_sample_pop = data_for_table_creation.population_sample_by_la_stratum.sum()

    return (
        place_total_populations_in_dataframe(total_eligible_pop, total_sample_pop)
        .pipe(calc_percentage_column)
        .pipe(apply_rounding)
    )


def place_total_populations_in_dataframe(
    total_eligible_pop: int, total_sample_pop: int
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Total Eligible", total_eligible_pop, total_eligible_pop],
            ["Sample", total_sample_pop, total_eligible_pop],
        ],
        columns=["group", "population", "total_population"],
    ).set_index("group")
