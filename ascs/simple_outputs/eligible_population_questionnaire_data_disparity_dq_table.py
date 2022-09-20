import pandas as pd
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)


def create_eligible_population_questionnaire_data_disparity_dq_table(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    actual_sample_population = (
        data_needed_for_table_creation.df_questionnaire_by_person.groupby(
            ["LaCode", "Stratum"]
        )
        .size()
        .rename("actual_sample_population")
    )
    expected_sample_population = (
        data_needed_for_table_creation.population_sample_by_la_stratum.sort_index()
        .rename("expected_sample_population")
        .to_frame()
    )
    merged_dataframe = expected_sample_population.merge(
        actual_sample_population, left_index=True, right_index=True, how="outer"
    )
    filtered_dataframe_by_differing_actual_and_expected_size = merged_dataframe[
        merged_dataframe["actual_sample_population"]
        != merged_dataframe["expected_sample_population"]
    ]
    return {
        "population_disparity_dq_table": filtered_dataframe_by_differing_actual_and_expected_size
    }
