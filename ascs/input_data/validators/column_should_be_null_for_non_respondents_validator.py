import pandas as pd

from typing import Optional
from ..df_with_errors import DFWithErrors

from .base_validator import BaseValidator

from ascs import params


def run_all_column_should_be_null_for_non_respondents_validations(
    df_questionnaire_w_errs: DFWithErrors,
    columns_that_should_be_null: Optional[list[str]] = None,
) -> DFWithErrors:
    if columns_that_should_be_null is None:
        columns_that_should_be_null = (
            params.get_input_columns_that_should_be_null_for_non_respondents_for_validations()
        )

    for column_name in columns_that_should_be_null:
        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            ColumnShouldBeNullForNonRespondentsValidator(column=column_name)
        )

    return df_questionnaire_w_errs


class ColumnShouldBeNullForNonRespondentsValidator(BaseValidator):
    def __init__(self, column: str):
        self.column: str = column
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(self, questionnaire_data: pd.DataFrame,) -> pd.Series:
        person_didnt_respond_to_survey = (
            questionnaire_data["Response"] != params.RESPONSE_RESPONDED_TO_SURVEY
        )
        return person_didnt_respond_to_survey & ~questionnaire_data[self.column].isna()

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was "
            + df_questionnaire_by_person[self.column].astype(str)
            + " but should be blank when the person did not respond to the questionnaire"
        )
