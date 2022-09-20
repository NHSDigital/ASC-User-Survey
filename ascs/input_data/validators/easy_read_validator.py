import numpy as np
import pandas as pd

from typing import Optional
from ..df_with_errors import DFWithErrors

from .base_validator import BaseValidator

from ascs import params


def run_all_easy_read_validations(
    df_questionnaire_w_errs: DFWithErrors,
    easy_read_questions: Optional[list[str]] = None,
) -> DFWithErrors:
    if easy_read_questions is None:
        easy_read_questions = params.EASY_READ_QUESTIONS

    for column_name in params.EASY_READ_QUESTIONS:
        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            EasyReadValidator(column=column_name)
        )

    return df_questionnaire_w_errs


class EasyReadValidator(BaseValidator):
    column: str

    def __init__(self, column: str):
        self.column = column
        self.columns_to_set_null_for_invalid_rows = [column]

        self.accepted_values_std: list[int] = params.ACCEPTED_VALUES_STANDARD_QUESTIONS
        self.accepted_values_er: list[int] = params.ACCEPTED_VALUES_EASY_READ_QUESTIONS

    def get_where_incorrect(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        is_in_standard_accepted_values_by_person = df_questionnaire_by_person[
            self.column
        ].isin(self.accepted_values_std)
        is_in_er_accepted_values_by_person = df_questionnaire_by_person[
            self.column
        ].isin(self.accepted_values_er)

        is_er_by_person = df_questionnaire_by_person["is_easy_read"]

        return ~(
            (is_in_er_accepted_values_by_person & is_er_by_person)
            | (is_in_standard_accepted_values_by_person & ~is_er_by_person)
        )

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was "
            + df_questionnaire_by_person[self.column].astype(str)
            + " when accepted values are"
            + np.where(
                df_questionnaire_by_person["is_easy_read"],
                f" {self.accepted_values_er} for users who recieved the easy read questionnaire",
                f" {self.accepted_values_std} for users who recieved the standard questionnaire",
            )
        )
