import numpy as np
import pandas as pd

from typing import Optional

from ascs import params


def add_is_easy_read_column(
    df_questionnaire_by_person: pd.DataFrame,
    easy_read_questionnaire_types: Optional[list[int]] = None,
) -> pd.DataFrame:
    if easy_read_questionnaire_types is None:
        easy_read_questionnaire_types = params.EASY_READ_QUESTIONNAIRE_TYPES

    df_questionnaire_by_person["is_easy_read"] = (
        df_questionnaire_by_person["Questionnaire"]
        .isin(easy_read_questionnaire_types)
        .astype(bool)
    )

    return df_questionnaire_by_person


def add_easy_read_columns(
    df_questionnaire_by_person: pd.DataFrame,
    easy_read_questions: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    For each easy read question (like q1) creates easy read columns (like q1ER, q1Std, q1Comb)
    """
    if easy_read_questions is None:
        easy_read_questions = params.EASY_READ_QUESTIONS

    for easy_read_question in easy_read_questions:
        add_columns_for_one_easy_read_question(
            df_questionnaire_by_person, easy_read_question
        )

    return df_questionnaire_by_person


def add_columns_for_one_easy_read_question(
    df_questionnaire_by_person: pd.DataFrame, question: str
) -> None:
    r"""
    The question column contains all people's raw untransformed answers

    This function creates three columns

    Column 1: question + ER = Only the raw ER answers

    Column 2: question + Std = Only the raw Std answers

    Column 3: question + Comb:
    - Answered the ER survey: their raw answer (which is a number from 1-5)
    - Answered the Std survey:
        The Std raw answer is a number from 1-7
        We transform it to be in range 1-5 to make it comparable to Std
    """

    initialise_easy_read_columns_to_null(df_questionnaire_by_person, question)

    easy_read = df_questionnaire_by_person["is_easy_read"]
    standard = ~df_questionnaire_by_person["is_easy_read"]

    df_questionnaire_by_person.loc[
        easy_read, f"{question}ER"
    ] = df_questionnaire_by_person.loc[easy_read, question]

    df_questionnaire_by_person.loc[
        standard, f"{question}Std"
    ] = df_questionnaire_by_person.loc[standard, question]

    df_questionnaire_by_person.loc[
        easy_read, f"{question}Comb"
    ] = df_questionnaire_by_person.loc[easy_read, question]

    df_questionnaire_by_person.loc[
        standard, f"{question}Comb"
    ] = clamp_std_answer_to_make_it_between_1_and_5(
        df_questionnaire_by_person[question]
    )


def initialise_easy_read_columns_to_null(
    df_questionnaire_by_person: pd.DataFrame, question: str
) -> pd.DataFrame:
    df_questionnaire_by_person[
        [f"{question}ER", f"{question}Std", f"{question}Comb"]
    ] = np.nan

    return df_questionnaire_by_person


def clamp_std_answer_to_make_it_between_1_and_5(
    question_response_by_person: pd.Series,
) -> pd.Series:
    """
    Standard answers are 1-7
    Make them comparable to easy read answers by putting them in range 1-5
    Transformation is as follows:
    Standard answer: 1 2 3 4 5 6 7
                      ⧹| | | | |/
    Combined answer:   1 2 3 4 5
    """
    return np.minimum(np.maximum(question_response_by_person - 1, 1), 5)
