import pandas as pd

from typing import Optional
from ..df_with_errors import DFWithErrors

from ..preprocess_utilities import get_numeric_columns_from_df_questionnaire_by_person

from .base_validator import BaseValidator


def run_all_whole_number_validations(
    df_questionnaire_w_errs: DFWithErrors, numeric_columns: Optional[list[str]] = None,
) -> DFWithErrors:
    if numeric_columns is None:
        numeric_columns = get_numeric_columns_from_df_questionnaire_by_person(
            df_questionnaire_w_errs.df
        )

    for column_name in numeric_columns:
        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            WholeNumberValidator(column=column_name)
        )

    return df_questionnaire_w_errs


class WholeNumberValidator(BaseValidator):
    def __init__(self, column: str) -> None:
        self.column: str = column
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        column_series = df_questionnaire_by_person[self.column]
        column_as_whole_nums = column_series.round(0)
        column_is_whole_num_by_person = (column_series == column_as_whole_nums) | (
            column_series.isna() & column_as_whole_nums.isna()
        )
        return ~column_is_whole_num_by_person

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was "
            + df_questionnaire_by_person[self.column].astype(str)
            + " but should be a whole number"
        )
