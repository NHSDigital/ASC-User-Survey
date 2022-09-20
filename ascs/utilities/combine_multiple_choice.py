import pandas as pd

from ascs import params
from ascs.params_utils.params_transformations import get_expanded_multichoice_list


def combine_multiple_choice(
    annex_table: pd.DataFrame, multiple_choice_questions: dict[str, list[str]],
) -> pd.DataFrame:
    question_table_block_list = [annex_table]
    do_respondents_column = "Respondents" in annex_table.columns.unique(level=1)

    for question, subquestions in multiple_choice_questions.items():
        complete_questions = [question + subquestion for subquestion in subquestions]

        new_cols = annex_table.loc[
            :, (complete_questions, params.ANSWERED_YES_TO_SUBQUESTION_RESPONSE)
        ].copy()
        new_cols.columns = pd.MultiIndex.from_product(
            [[question], subquestions], names=annex_table.columns.names
        )

        if do_respondents_column:
            new_cols[(question, "Respondents")] = annex_table[
                (question + subquestions[0], "Respondents")
            ]

        question_table_block_list.append(new_cols)

    return pd.concat(question_table_block_list, axis=1).drop(
        get_expanded_multichoice_list(multiple_choice_questions),
        axis="columns",
        level=0,
    )


def combine_multiple_choice_auxiliary_utility(
    df_by_supergroup_question_response: pd.DataFrame,
    question_column: str,
    response_column: str,
    multichoice_questions: dict[str, list[str]],
) -> pd.DataFrame:
    """
    Instead of having

    question | response
    -------------------
    q11a     | yes
    q11a     | no
    q11b     | yes
    q11b     | no

    we just want

    question | response
    -------------------
    q11      | a
    q11      | b
    """

    return (
        df_by_supergroup_question_response.copy()
        .pipe(
            add_question_is_multichoice_column, question_column, multichoice_questions
        )
        .pipe(
            filter_out_rows_that_are_subquestions_and_the_response_is_no,
            response_column,
        )
        .pipe(
            set_response_column_to_the_subquestion_letter,
            question_column,
            response_column,
        )
        .pipe(remove_subquestion_letter_from_the_question_column, question_column)
        .drop("question_is_multichoice", axis=1)
    )


def add_question_is_multichoice_column(
    df_by_supergroup_question_response: pd.DataFrame,
    question_column: str,
    multichoice_questions: dict[str, list[str]],
) -> pd.DataFrame:
    expanded_multichoice_list = get_expanded_multichoice_list(multichoice_questions)

    df_by_supergroup_question_response[
        "question_is_multichoice"
    ] = df_by_supergroup_question_response[question_column].isin(
        expanded_multichoice_list
    )

    return df_by_supergroup_question_response


def filter_out_rows_that_are_subquestions_and_the_response_is_no(
    df_by_supergroup_question_response: pd.DataFrame, response_column: str,
) -> pd.DataFrame:
    question_is_multichoice_subquestion_no = df_by_supergroup_question_response[
        "question_is_multichoice"
    ] & (
        df_by_supergroup_question_response[response_column]
        == params.ANSWERED_NO_TO_SUBQUESTION_RESPONSE
    )

    return df_by_supergroup_question_response[
        ~question_is_multichoice_subquestion_no
    ].copy()


def set_response_column_to_the_subquestion_letter(
    df_by_supergroup_question_response: pd.DataFrame,
    question_column: str,
    response_column: str,
) -> pd.DataFrame:
    """The subquestion letter is like "a" "b" "c"."""
    df_by_supergroup_question_response.loc[
        df_by_supergroup_question_response["question_is_multichoice"], response_column
    ] = df_by_supergroup_question_response[question_column].str.slice(start=-1)

    return df_by_supergroup_question_response


def remove_subquestion_letter_from_the_question_column(
    df_by_supergroup_question_response: pd.DataFrame, question_column: str,
):
    df_by_supergroup_question_response.loc[
        df_by_supergroup_question_response["question_is_multichoice"], question_column
    ] = df_by_supergroup_question_response[question_column].str.slice(stop=-1)

    return df_by_supergroup_question_response
