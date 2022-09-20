import logging
import pandas as pd
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)
from ascs.stratification.stratification import perform_stratification
from ascs import params


def create_demographics_table(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    logging.info("Started creating annex table 6")

    annex_table6 = create_proportion_and_estimated_population_in_demographic_rows(
        data_needed_for_table_creation
    ).pipe(format_table_output)

    logging.info("Finished creating annex table 6")

    return {"6": annex_table6}


def create_proportion_and_estimated_population_in_demographic_rows(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> pd.DataFrame:
    list_of_df_dem_data = []

    for (
        demographic_readable_name,
        demographic_column,
    ) in params.get_grouped_demographic_column_by_readable_name_table_6().items():
        df_prop_and_est_pop_in_dem = (
            perform_stratification(
                data_needed_for_table_creation.df_questionnaire_by_person,
                data_needed_for_table_creation.population_by_la_stratum,
                subgroup_within_supergroup_columns=["LaCode", "Stratum"],
                supergroup_columns=[],
                discrete_column_name=demographic_column,
            )
            .rename(
                columns={
                    "discrete": "Demographic",
                    "response": "Demographic Value",
                    "percentage": "Percentage in Demographic",
                    "est_population": "Estimated Population of Demographic",
                }
            )
            .assign(Demographic=demographic_readable_name)
            .set_index(["Demographic", "Demographic Value"])
        )

        list_of_df_dem_data.append(df_prop_and_est_pop_in_dem)

    return pd.concat(list_of_df_dem_data)


def format_table_output(annex_table6: pd.DataFrame) -> pd.DataFrame:
    return (
        annex_table6.pipe(round_table6).pipe(select_output_columns).pipe(reindex_table6)
    )


def round_table6(annex_table6: pd.DataFrame) -> pd.DataFrame:
    annex_table6["Estimated Population of Demographic"] = annex_table6[
        "Estimated Population of Demographic"
    ].round(-1)
    annex_table6["Percentage in Demographic"] = (
        annex_table6["Percentage in Demographic"]
    ).round(1)
    annex_table6["margin_of_error"] = annex_table6["margin_of_error"].round(1)

    return annex_table6


def select_output_columns(annex_table6: pd.DataFrame) -> pd.DataFrame:
    return annex_table6[
        ["Estimated Population of Demographic", "Percentage in Demographic"]
    ]


def reindex_table6(annex_table6: pd.DataFrame) -> pd.DataFrame:
    new_index = pd.MultiIndex.from_tuples(
        params.TABLE6_CORRECT_ROW_ORDER, names=["Demographic", "Demographic Value"]
    )
    rows_that_would_be_deleted = annex_table6.index.difference(
        params.TABLE6_CORRECT_ROW_ORDER
    )
    assert (
        len(rows_that_would_be_deleted) == 0
    ), f"""
Reindex in table 6 would delete rows
Rows that would be deleted:
{rows_that_would_be_deleted}

This is a sign that there is some group in the data that is not accounted for in TABLE6_CORRECT_ROW_ORDER in params
"""
    return annex_table6.reindex(new_index, fill_value="[w]")
