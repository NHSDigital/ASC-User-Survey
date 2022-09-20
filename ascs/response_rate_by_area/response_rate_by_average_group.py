import pandas as pd

from typing import Optional

from .response_rate_utilities import (
    filter_out_people_who_didnt_respond_to_the_overall_questionnaire,
)

from ascs import params


def add_response_rate_by_average_group(
    df_response_rate_by_area: pd.DataFrame,
    df_questionnaire_by_person: pd.DataFrame,
    la_codes_by_average_group_name: Optional[dict[str, list[str]]] = None,
) -> pd.DataFrame:
    if la_codes_by_average_group_name is None:
        la_codes_by_average_group_name = params.LA_CODE_LIST_BY_AVERAGE_GROUP_NAME

    for (
        average_group_name,
        la_codes_in_average_group,
    ) in la_codes_by_average_group_name.items():
        df_response_rate_by_area = add_response_rate_row_for_one_average_group(
            df_response_rate_by_area,
            df_questionnaire_by_person,
            average_group_name,
            la_codes_in_average_group,
        )

    return df_response_rate_by_area


def add_response_rate_row_for_one_average_group(
    annex_table4: pd.DataFrame,
    df_questionnaire_by_person: pd.DataFrame,
    average_group_name: str,
    la_codes_in_average_group: list[str],
) -> pd.DataFrame:
    df_questionnaire_by_respondent_in_average_group = df_questionnaire_by_person.pipe(
        filter_out_people_who_didnt_respond_to_the_overall_questionnaire
    ).pipe(filter_to_only_people_in_average_group, la_codes_in_average_group)

    return (
        annex_table4.pipe(
            add_average_row_for_normal_questions,
            df_questionnaire_by_respondent_in_average_group,
            average_group_name,
        )
        .pipe(
            calc_proportion_of_people_in_average_group_who_responded_to_overall_questionnaire,
            df_questionnaire_by_respondent_in_average_group,
            df_questionnaire_by_person,
            average_group_name,
        )
        .pipe(
            calc_2c_response_rate_in_average_group,
            df_questionnaire_by_respondent_in_average_group,
            average_group_name,
        )
    )


def add_average_row_for_normal_questions(
    annex_table4: pd.DataFrame,
    df_questionnaire_by_respondent_in_average_group: pd.DataFrame,
    average_row_name: str,
) -> pd.DataFrame:
    annex_table4.loc[average_row_name] = calc_response_rate_in_whole_df(
        df_questionnaire_by_respondent_in_average_group,
        params.ANNEX_TABLE_4_QUESTIONS_TO_COUNT,
    )

    return annex_table4


def calc_response_rate_in_whole_df(
    df_questionnaire_by_person: pd.DataFrame, questions_to_count: list[str],
) -> pd.DataFrame:
    return df_questionnaire_by_person[questions_to_count].count(axis=0) / len(
        df_questionnaire_by_person
    )


def filter_to_only_people_in_average_group(
    df_questionnaire_by_person: pd.DataFrame, la_codes_in_average_group: list[str]
) -> pd.DataFrame:
    return df_questionnaire_by_person.loc[
        df_questionnaire_by_person["LaCode"].isin(la_codes_in_average_group)
    ]


def calc_proportion_of_people_in_average_group_who_responded_to_overall_questionnaire(
    annex_table4: pd.DataFrame,
    df_questionnaire_by_respondent_in_average_group: pd.Series,
    df_questionnaire_by_person: pd.DataFrame,
    average_row_name: str,
):
    total_response_rate = len(df_questionnaire_by_respondent_in_average_group) / len(
        df_questionnaire_by_person
    )

    annex_table4.loc[average_row_name, "total_response_rate"] = total_response_rate

    return annex_table4


def calc_2c_response_rate_in_average_group(
    annex_table4: pd.DataFrame,
    df_questionnaire_by_respondent_in_average_group: pd.Series,
    average_row_name: str,
) -> pd.DataFrame:
    df_questionnaire_by_2c_respondent_in_average_group = df_questionnaire_by_respondent_in_average_group[
        df_questionnaire_by_respondent_in_average_group["can_answer_2c"]
    ]

    response_rate_2c = df_questionnaire_by_2c_respondent_in_average_group[
        "q2c"
    ].count() / len(df_questionnaire_by_2c_respondent_in_average_group)

    annex_table4.loc[average_row_name, "q2c"] = response_rate_2c

    return annex_table4
