import logging

import pandas as pd
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)

from ascs import params


def create_admin_data_table(
    data_needed_for_table_creation: DataNeededForTableCreation,
    columns_to_include: list[str] = list(params.DEMOGRAPHICS_CONVERSIONS),
) -> dict[str, pd.DataFrame]:
    logging.info("Started creating Data Quality Annex Table 1 and 2")

    df_questionnaire_by_person = filter_questionnaire_columns_to_only_admin_data(
        data_needed_for_table_creation.df_questionnaire_by_person, columns_to_include
    )
    df_questionnaire_excluding_non_respondents_by_respondent = filter_questionnaire_to_those_that_responded(
        df_questionnaire_by_person
    )

    annex_table1 = df_questionnaire_excluding_non_respondents_by_respondent.pipe(
        calculate_proportion_missing_in_columns_by_la
    ).pipe(format_output)

    annex_table2 = df_questionnaire_by_person.pipe(
        calculate_proportion_missing_in_columns_by_la
    ).pipe(format_output)

    logging.info("Finished creating Data Quality Annex Table 1 and 2")

    return {
        "dq1": annex_table1,
        "dq2": annex_table2,
    }


def calculate_proportion_missing_in_columns_by_la(
    df_specific_annex_table: pd.DataFrame,
) -> pd.DataFrame:
    df_grouped_by_la = df_specific_annex_table.groupby("LaCode")
    proportions = 1 - (df_grouped_by_la.count().divide(df_grouped_by_la.size(), axis=0))
    return proportions


def format_output(df_input) -> pd.DataFrame:
    return (100 * df_input).round(1).drop(columns=["Response"])


def filter_questionnaire_columns_to_only_admin_data(
    df_questionnaire_by_response: pd.DateOffset, columns_to_include: list[str]
) -> pd.DataFrame:
    return df_questionnaire_by_response[
        columns_to_include + ["LaCode", "Age", "Response"]
    ]


def filter_questionnaire_to_those_that_responded(
    df_questionnaire_by_response: pd.DateOffset,
) -> pd.DataFrame:
    responded_to_survey = (
        df_questionnaire_by_response["Response"] == params.RESPONSE_RESPONDED_TO_SURVEY
    )

    return df_questionnaire_by_response[responded_to_survey]
