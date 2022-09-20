import pandas as pd

from .response_rate_utilities import (
    filter_out_people_who_didnt_respond_to_the_overall_questionnaire,
)

from ascs import params


def create_response_rate_by_la_table(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    df_response_rate_by_la = (
        calc_question_response_rate_by_la(
            df_questionnaire_by_person, params.ANNEX_TABLE_4_QUESTIONS_TO_COUNT
        )
        .pipe(calc_q2c_response_rate_by_la, df_questionnaire_by_person)
        .pipe(calc_total_response_rate_column, df_questionnaire_by_person)
    )

    return df_response_rate_by_la


def calc_q2c_response_rate_by_la(
    annex_table4: pd.DataFrame, df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    questionnaire_only_those_that_could_answer_2c = df_questionnaire_by_person[
        df_questionnaire_by_person["can_answer_2c"]
    ]

    annex_table4["q2c"] = calc_question_response_rate_by_la(
        questionnaire_only_those_that_could_answer_2c, ["q2c"],
    )

    return annex_table4


def calc_question_response_rate_by_la(
    df_questionnaire_by_person: pd.DataFrame, questions_to_count: list[str],
) -> pd.DataFrame:
    """
    Get dataframe with questions as the columns
    LAs as the rows
    and the values are the proportion of people in that LA who responded to that question
    excluding people who didn't respond to the questionnaire at all
    """
    return (
        df_questionnaire_by_person.pipe(
            filter_out_people_who_didnt_respond_to_the_overall_questionnaire
        )
        .groupby("LaCode")[questions_to_count]
        .apply(calc_proportion_of_series_that_is_null)
    )


def calc_proportion_of_series_that_is_null(series: pd.Series) -> float:
    return series.count(axis=0) / len(series)


def calc_total_response_rate_column(
    annex_table4: pd.DataFrame, df_questionnaire_by_person: pd.DataFrame
) -> pd.DataFrame:
    """
    This adds a column that for each LA has the percentage of people who responded to the overall questionnaire
    """
    annex_table4["total_response_rate"] = df_questionnaire_by_person.groupby("LaCode")[
        "Response"
    ].apply(
        lambda responses_in_la: (
            responses_in_la == params.RESPONSE_RESPONDED_TO_SURVEY
        ).sum()
        / len(responses_in_la)
    )

    return annex_table4
