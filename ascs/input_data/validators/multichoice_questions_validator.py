import pandas as pd

from typing import Optional
from ..df_with_errors import DFWithErrors

from ascs.params_utils.params_transformations import get_questions_with_all_suffixes

from .base_validator import BaseValidator

from ascs import params


def run_all_multichoice_validations(
    df_questionnaire_w_errs: DFWithErrors,
    multichoice_questions: Optional[dict[str, list[str]]] = None,
) -> DFWithErrors:
    if multichoice_questions is None:
        multichoice_questions = params.MULTIPLE_CHOICE_QUESTIONS

    for (
        multichoice_question,
        multichoice_subquestions_unexpanded,
    ) in multichoice_questions.items():
        multichoice_subquestions_expanded = get_questions_with_all_suffixes(
            [multichoice_question], multichoice_subquestions_unexpanded
        )

        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            MultichoiceQuestionsValidator(
                sub_questions=multichoice_subquestions_expanded
            )
        )

    return df_questionnaire_w_errs


class MultichoiceQuestionsValidator(BaseValidator):
    """
    Multichoice questions (like q12) are made up of multiple subquestions (q12a, q12b, q12c)
    A multichoice question is invalid if:
    - In the subquestions there is a mix of nulls and not nulls
    - All the subquestions have answer "no"
    """

    def __init__(self, sub_questions: list[str]):
        self.sub_questions: list[str] = sub_questions
        self.columns_to_set_null_for_invalid_rows = sub_questions

    def get_where_incorrect(self, df_questionnaire_by_person: pd.DataFrame):
        df_subquestions_only = df_questionnaire_by_person[self.sub_questions]

        df_subquestions_nan = df_subquestions_only.isna()

        subquestions_are_mix_of_nulls_and_not_nulls = df_subquestions_nan.any(
            axis=1
        ) & ~df_subquestions_nan.all(axis=1)

        all_subquestions_are_no_by_respondent = (
            df_subquestions_only == params.ANSWERED_NO_TO_SUBQUESTION_RESPONSE
        ).all(axis="columns")

        is_invalid_by_respondent = (
            subquestions_are_mix_of_nulls_and_not_nulls
            | all_subquestions_are_no_by_respondent
        )

        return is_invalid_by_respondent

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> str:
        return f"The list of subquestions {self.sub_questions} has one of these problems: there is a mix of nulls and not nulls; all the subquestions were answered 2 (no)"
