import pandas as pd

from typing import Any, Optional
from ..df_with_errors import DFWithErrors

from .base_validator import BaseValidator

from ascs import params


def run_all_column_should_be_certain_value_for_non_respondents_validations(
    df_questionnaire_w_errs: DFWithErrors,
    columns_that_should_be_no_for_non_respondents: Optional[list[str]] = None,
) -> DFWithErrors:
    if columns_that_should_be_no_for_non_respondents is None:
        columns_that_should_be_no_for_non_respondents = (
            params.VALIDATION_COLUMNS_THAT_SHOULD_BE_NO_FOR_NON_RESPONDENTS
        )

    for column_name in columns_that_should_be_no_for_non_respondents:
        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            ColumnShouldBeCertainValueForNonRespondentsValidator(
                column=column_name,
                the_value_the_column_should_be_when_person_didnt_respond=params.ANSWERED_NO_TO_SUBQUESTION_RESPONSE,
            )
        )

    return df_questionnaire_w_errs


class ColumnShouldBeCertainValueForNonRespondentsValidator(BaseValidator):
    def __init__(
        self, column: str, the_value_the_column_should_be_when_person_didnt_respond: Any
    ):
        self.column: str = column
        assert not pd.isna(
            the_value_the_column_should_be_when_person_didnt_respond
        ), "The value cannot be NA, for that use ColumnShouldBeNullForNonRespondentsValidator"
        self.the_value_the_column_should_be_when_person_didnt_respond: Any = the_value_the_column_should_be_when_person_didnt_respond
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(self, questionnaire_data: pd.DataFrame,) -> pd.Series:
        person_didnt_respond_to_survey = (
            questionnaire_data["Response"] != params.RESPONSE_RESPONDED_TO_SURVEY
        )
        column_is_the_value_column_should_be_for_non_respondents = (
            questionnaire_data[self.column]
            == self.the_value_the_column_should_be_when_person_didnt_respond
        )
        return (
            person_didnt_respond_to_survey
            & ~column_is_the_value_column_should_be_for_non_respondents
        )

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> str:
        return f"Column {self.column} must be {self.the_value_the_column_should_be_when_person_didnt_respond} when the person did not respond to the questionnaire"
