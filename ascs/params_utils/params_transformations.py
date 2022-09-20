from typing import Any, Union


def get_questions_with_all_suffixes(questions: list[str], suffixes: list[str]):
    """
    Input:
        Something like
            questions ["q1", "q2"]
            suffixes ["a", "b"]

    Outputs:
        Something like
            ["q1a", "q1b", "q2a", "q2b"]
    """
    return [question + suffix for question in questions for suffix in suffixes]


def get_expanded_multichoice_list(
    multiple_choice_questions: dict[str, list[str]]
) -> list[str]:
    """
    Input:
        Dict like
        {
            "q12": ("a", "b", "c"),
            "q13": ("a", "b")
        }

    Outputs:
        List like
        ["q12a", "q12b", "q12c", "q13a", "q13b"]
    """
    return [
        question + subquestion
        for question, subquestions in multiple_choice_questions.items()
        for subquestion in subquestions
    ]


def add_exclude_to_multichoice_questions(
    multiple_choice_questions: dict[str, list[str]],
    multiple_choice_questions_to_exclude: dict[str, dict[str, Union[str, int]]],
) -> dict[str, list[str]]:
    return {
        **multiple_choice_questions,
        **{
            multiple_choice_question
            + "Excl": [
                subquestion
                for subquestion in multiple_choice_questions[multiple_choice_question]
                if subquestion != to_exclude["subquestion"]
            ]
            for multiple_choice_question, to_exclude in multiple_choice_questions_to_exclude.items()
        },
    }


def get_question_responses_and_respondents_list_of_tuples(
    stratified_pivotted_tables_column_responses_by_question: dict[str, list[int]],
):
    return [
        (question, response)
        for question, possible_responses in stratified_pivotted_tables_column_responses_by_question.items()
        for response in possible_responses + ["Respondents"]
    ]


def get_question_responses_no_respondents_list_of_tuples(
    stratified_pivotted_tables_column_responses_by_question: dict[str, list[int]],
):
    return [
        (question, response)
        for question, possible_responses in stratified_pivotted_tables_column_responses_by_question.items()
        for response in possible_responses
    ]


def get_excluded_question_columns_pre_multichoice_merge(
    questions_and_values_to_exclude: dict[str, Any],
    multiple_choice_questions_to_exclude: dict[str, int],
    multiple_choice_questions: dict[str, list[str]],
) -> list[str]:
    return [
        question + "Excl" for question in questions_and_values_to_exclude.keys()
    ] + [
        question + "Excl" + subquestion
        for question, to_exclude in multiple_choice_questions_to_exclude.items()
        for subquestion in multiple_choice_questions[question]
        if subquestion != to_exclude["subquestion"]
    ]


def get_grouped_demographic_column_by_readable_name(
    demographics_conversions: dict[str, Any]
) -> dict[str, str]:
    demographic_readable_names = list(demographics_conversions.keys()) + ["Age"]
    demographic_columns = [
        dem_key + "_Grouped" for dem_key in demographic_readable_names
    ]
    return {
        readable_name: column
        for readable_name, column in zip(
            demographic_readable_names, demographic_columns
        )
    }


def get_grouped_demographic_column_by_readable_name_table_6(
    demographics_conversions: dict[str, Any]
) -> dict[str, str]:
    """
    Table 6 uses different columns to just the grouped demog cols list
    """
    demog_col_by_name = get_grouped_demographic_column_by_readable_name(
        demographics_conversions
    )

    demog_names_to_use_original_and_not_grouped_column = [
        "Sexuality",
        "Advocate",
        "Interpreter",
    ]
    for demog_name in demog_names_to_use_original_and_not_grouped_column:
        demog_col_by_name[demog_name] = demog_name

    demog_names_to_not_use = [
        "Stratum",
        "MethodCollection",
        "Questionnaire",
        "FullCost",
    ]
    for demog_name in demog_names_to_not_use:
        del demog_col_by_name[demog_name]

    return demog_col_by_name


def column_name_is_a_question_column(column_name: str) -> bool:
    return column_name.startswith("q") and column_name[1].isdigit()
