import pandas as pd


def get_respondents_by_columns(
    df_questionnaire_by_person: pd.DataFrame, question: str, groupby_columns: list[str],
) -> pd.Series:
    """
    Args:
        questionnaire_data
            A dataframe of the form (with question="q3a")
            +---------+-----+
            | LaCode  | q3a |
            +---------+-----+
            | 211     | 1   | <- One respondent from LA 211 answered "1" for question 3a
            | ...     | ... |
            | str/int | int |
            +---------+-----+

        question
            A string representing the question
            e.g: "q3a"

        groupby_columns
            The columns to groupby on before doing the count
            e.g: ["LaCode"]

    Returns:
        A pandas series of the form
            +---------+-----+
            | LaCode  |  -  |
            +---------+-----+
            | 211     | 123 | <- 123 people in LA 211 answered without error question q3a
            | ...     | ... |
            | str/int | int |
            +---------+-----+
    """
    return df_questionnaire_by_person.groupby(groupby_columns)[question].count()
