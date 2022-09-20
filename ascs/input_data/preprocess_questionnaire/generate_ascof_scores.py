from typing import NamedTuple, Optional, Union
from ascs import params
import numpy as np
import pandas as pd

from ascs.input_data.preprocess_questionnaire.ascof_config import SimpleAscofConversion


class ScoreCondition(NamedTuple):
    condition: pd.Series
    value_to_set: Union[int, float]


def generate_all_scores(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    df_questionnaire_by_person = (
        generate_1A(df_questionnaire_by_person)
        .pipe(generate_simple_conversion_ascof_scores)
        .pipe(generate_1J)
    )
    
    return df_questionnaire_by_person


def apply_simple_conversion(
    df_questionnaire_by_person: pd.DataFrame, ascof_conversion: SimpleAscofConversion
):
    score_name = ascof_conversion.SCORE_NAME

    df_questionnaire_by_person[score_name] = df_questionnaire_by_person[
        ascof_conversion.QUESTION_COLUMN
    ].replace(ascof_conversion.CONVERSION)

    return df_questionnaire_by_person


def generate_1A(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    COLUMNS_FOR_1A = ["q3a", "q4a", "q5a", "q6a", "q7a", "q8a", "q9a", "q11"]
    df_questionnaire_by_person["ASCOF_1A"] = 32 - df_questionnaire_by_person[
        COLUMNS_FOR_1A
    ].sum(axis=1, skipna=False)

    return df_questionnaire_by_person


def generate_simple_conversion_ascof_scores(
    df_questionnaire_by_person: pd.DataFrame,
    simple_ascof_conversions: Optional[list[SimpleAscofConversion]] = None,
) -> pd.DataFrame:
    """
    This function creates simple ascof scores by applying a conversion dict on a question column
    e.g simple_conversions = {
        "ASCOF_1B": {
            "q3a": {
                1: 1,
                2: 1,
                3: 2,
                4: 2
    }}}
    So a person with a q3a response of 2 would have an ASCOF_1B score of 1
    """
    if simple_ascof_conversions is None:
        simple_ascof_conversions = params.ASCOF_CONVERSIONS

    for ascof_conversion in simple_ascof_conversions:
        df_questionnaire_by_person = apply_simple_conversion(
            df_questionnaire_by_person, ascof_conversion
        )

    return df_questionnaire_by_person


def generate_1J(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    df_questionnaire_by_person["ASCOF_1J"] = (
        df_questionnaire_by_person.copy()
        .pipe(recode_columns_for_1J)
        .pipe(calculate_weighted_quality_of_life_score)
        .pipe(calculate_count_level_of_assistance_score)
        .pipe(calculate_adjustment_factor)
        .pipe(calculate_1J_from_recoded_questionnaire_df)
    )

    df_questionnaire_by_person = set_1J_to_nan_for_invalid_responses(
        df_questionnaire_by_person
    )

    return df_questionnaire_by_person


def recode_columns_for_1J(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    MINUS_ONE_CONVERSION = {1: 0.0, 2: 1.0, 3: 2.0}
    CONVERSIONS_BY_QUESTION = {
        "q3a": {1: 1, 2: 0.919, 3: 0.541, 4: 0},
        "q4a": {1: 0.911, 2: 0.789, 3: 0.265, 4: 0.195},
        "q5a": {1: 0.879, 2: 0.775, 3: 0.294, 4: 0.184},
        "q6a": {1: 0.863, 2: 0.78, 3: 0.374, 4: 0.288},
        "q7a": {1: 0.88, 2: 0.452, 3: 0.298, 4: 0.114},
        "q8a": {1: 0.873, 2: 0.748, 3: 0.497, 4: 0.241},
        "q9a": {1: 0.962, 2: 0.927, 3: 0.567, 4: 0.17},
        "q11": {1: 0.847, 2: 0.637, 3: 0.295, 4: 0.263},
        "q13": {1: 0.0, 2: 0.0, 3: -0.0148, 4: -0.1090, 5: -0.1090},
        "q15a": MINUS_ONE_CONVERSION,
        "q15b": MINUS_ONE_CONVERSION,
        "q15c": MINUS_ONE_CONVERSION,
        "q15d": MINUS_ONE_CONVERSION,
        "q16a": MINUS_ONE_CONVERSION,
        "q16b": MINUS_ONE_CONVERSION,
        "q16c": MINUS_ONE_CONVERSION,
        "q17": {1: 0.0, 2: -0.0308, 3: -0.1250, 4: -0.1250, 5: -0.1250},
        "q18": {1: 0.0, 2: -0.0603, 3: -0.1100, 4: -0.1100},
    }
    df_questionnaire_by_person = df_questionnaire_by_person.replace(
        CONVERSIONS_BY_QUESTION
    )

    return df_questionnaire_by_person


def calculate_weighted_quality_of_life_score(
    df_questionnaire_by_person_recoded: pd.DataFrame,
) -> pd.DataFrame:
    COLUMNS_FOR_WEIGHTED_QUALITY_OF_LIFE_SCORE = [
        "q3a",
        "q4a",
        "q5a",
        "q6a",
        "q7a",
        "q8a",
        "q9a",
        "q11",
    ]
    df_questionnaire_by_person_recoded["weighted_quality_of_life_score"] = (
        df_questionnaire_by_person_recoded[
            COLUMNS_FOR_WEIGHTED_QUALITY_OF_LIFE_SCORE
        ].sum(axis=1)
        * 0.203
        - 0.466
    )

    return df_questionnaire_by_person_recoded


def calculate_count_level_of_assistance_score(
    df_questionnaire_by_person_recoded: pd.DataFrame,
) -> pd.DataFrame:
    COLUMNS_FOR_COUNT_LEVEL_OF_ASSISTANCE_SCORE = [
        "q15a",
        "q15b",
        "q15c",
        "q15d",
        "q16a",
        "q16b",
        "q16c",
    ]
    df_questionnaire_by_person_recoded[
        "count_level_of_assistance_score"
    ] = df_questionnaire_by_person_recoded[
        COLUMNS_FOR_COUNT_LEVEL_OF_ASSISTANCE_SCORE
    ].sum(
        axis=1
    )

    return df_questionnaire_by_person_recoded


def calculate_adjustment_factor(
    df_questionnaire_by_person_recoded: pd.DataFrame,
) -> pd.DataFrame:
    COLUMNS_FOR_ADJUSTMENT_FACTOR = [
        "q13",
        "q17",
        "q18",
        "age_1864",
        "count_level_of_assistance_score",
    ]
    ADJUSTMENT_FACTOR_CONVERSION = {"age_1864": {True: 0, False: 0.0473}}
    df_questionnaire_by_person_recoded = df_questionnaire_by_person_recoded.replace(
        ADJUSTMENT_FACTOR_CONVERSION
    )

    df_questionnaire_by_person_recoded["count_level_of_assistance_score"] = 0.5798 - (
        df_questionnaire_by_person_recoded["count_level_of_assistance_score"] * 0.0202
    )

    df_questionnaire_by_person_recoded[
        "adjustment_factor"
    ] = df_questionnaire_by_person_recoded[COLUMNS_FOR_ADJUSTMENT_FACTOR].sum(axis=1)

    return df_questionnaire_by_person_recoded


def calculate_1J_from_recoded_questionnaire_df(
    df_questionnaire_by_person_recoded: pd.DataFrame,
) -> pd.Series:
    return (
        df_questionnaire_by_person_recoded["weighted_quality_of_life_score"]
        - df_questionnaire_by_person_recoded["adjustment_factor"]
    )


def set_1J_to_nan_for_invalid_responses(
    df_questionnaire_by_person: pd.DataFrame,
    columns_that_must_not_contain_null: Optional[list[str]] = None,
):
    if columns_that_must_not_contain_null is None:
        columns_that_must_not_contain_null = [
            "q3a",
            "q4a",
            "q5a",
            "q6a",
            "q7a",
            "q8a",
            "q9a",
            "q11",
            "q13",
            "q15a",
            "q15b",
            "q15c",
            "q15d",
            "q16a",
            "q16b",
            "q16c",
            "q17",
            "q18",
            "age_1864",
            "can_answer_2c",
        ]

    can_answer_2c = df_questionnaire_by_person["can_answer_2c"]
    df_questionnaire_by_person.loc[~can_answer_2c, "ASCOF_1J"] = np.nan

    rows_containing_null = (
        df_questionnaire_by_person[columns_that_must_not_contain_null]
        .isnull()
        .any(axis=1)
    )
    df_questionnaire_by_person.loc[rows_containing_null, "ASCOF_1J"] = np.nan

    return df_questionnaire_by_person

