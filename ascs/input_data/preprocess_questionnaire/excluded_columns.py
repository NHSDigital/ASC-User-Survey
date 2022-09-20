from typing import Any, Optional
import numpy as np
import pandas as pd

from ascs import params


def add_excluded_columns(
    df_questionnaire_by_person: pd.DataFrame,
    questions_and_values_to_exclude: Optional[dict[str, int]] = None,
) -> pd.DataFrame:
    """
    We want to know how people answered certain questions excluding those who answered a certain way
    E.g: "What type of help did you get completing the survey excluding those who got no help?"
    To do that we copy the original question columns but set the people who answered that way to np.nan
    Then we have new question columns that we are able to use through the rest of the analysis.
    """
    if questions_and_values_to_exclude is None:
        questions_and_values_to_exclude = params.QUESTIONS_AND_VALUES_TO_EXCLUDE

    for exclude_question, value_to_exclude in questions_and_values_to_exclude.items():
        create_exclude_column_non_multichoice_question(
            df_questionnaire_by_person, exclude_question, value_to_exclude
        )

    create_exclude_columns_for_q22_multichoice_question(df_questionnaire_by_person)

    return df_questionnaire_by_person


def create_exclude_column_non_multichoice_question(
    df_questionnaire_by_person: pd.DataFrame,
    exclude_question: str,
    value_to_exclude: Any,
) -> pd.DataFrame:
    df_questionnaire_by_person[exclude_question + "Excl"] = df_questionnaire_by_person[
        exclude_question
    ].replace(value_to_exclude, np.nan)

    return df_questionnaire_by_person


def create_exclude_columns_for_q22_multichoice_question(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    """
    Q22: what type of help did you recieve?
    Q22Excl: what type of help did you recieve excluding those who recieved no help
    """

    return df_questionnaire_by_person.pipe(
        copy_q22_subquestions_to_new_excluded_subquestion_columns
    ).pipe(set_q22_excluded_subquestion_cols_to_null_where_someone_recieved_help)


Q22_SUBQUESTIONS_IN_EXCLUDED_ORIGINAL_NAMES = ["q22b", "q22c", "q22d", "q22e", "q22f"]
Q22_SUBQUESTIONS_IN_EXCLUDED_NEW_NAMES = [
    "q22Exclb",
    "q22Exclc",
    "q22Excld",
    "q22Excle",
    "q22Exclf",
]


def copy_q22_subquestions_to_new_excluded_subquestion_columns(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    df_questionnaire_by_person[
        Q22_SUBQUESTIONS_IN_EXCLUDED_NEW_NAMES
    ] = df_questionnaire_by_person[Q22_SUBQUESTIONS_IN_EXCLUDED_ORIGINAL_NAMES]

    return df_questionnaire_by_person


def set_q22_excluded_subquestion_cols_to_null_where_someone_recieved_help(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    didnt_recieve_any_type_of_help_by_person = (
        df_questionnaire_by_person[Q22_SUBQUESTIONS_IN_EXCLUDED_ORIGINAL_NAMES]
        == params.ANSWERED_NO_TO_SUBQUESTION_RESPONSE
    ).all(axis=1)

    df_questionnaire_by_person.loc[
        didnt_recieve_any_type_of_help_by_person,
        Q22_SUBQUESTIONS_IN_EXCLUDED_NEW_NAMES,
    ] = np.nan

    return df_questionnaire_by_person
