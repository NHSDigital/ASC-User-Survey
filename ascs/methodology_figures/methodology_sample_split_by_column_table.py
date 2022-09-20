import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs.methodology_figures.utilities import (
    apply_rounding,
    calc_percentage_column,
)


def create_methodology_sample_split_by_column_table(
    data_for_table_creation: DataNeededForTableCreation, column_to_split_by: str
) -> dict[str, int]:
    """
    Works out how the people in the sample population break down into demographic categories
    For example how the population breaks down into white and non-white
    Gets direct number of people, and also the percentage (over those who we know their demographic)
    """
    return (
        get_sample_population_by_how_responded(
            data_for_table_creation.df_questionnaire_by_person,
            column_to_split_by=column_to_split_by,
        )
        .to_frame()
        .pipe(add_total_population_column)
        .pipe(calc_percentage_column)
        .pipe(apply_rounding)
    )


def get_sample_population_by_how_responded(
    df_questionnaire_by_person: pd.DataFrame, column_to_split_by: str
) -> pd.Series:
    return (
        df_questionnaire_by_person.groupby(column_to_split_by)
        .size()
        .rename("population")
    )


def add_total_population_column(table: pd.DataFrame,):
    table["total_population"] = table["population"].sum()
    return table
