import pandas as pd

from typing import Optional
from ..df_with_errors import DFWithErrors

from .base_validator import BaseValidator

from ascs import params


def run_all_between_validations(
    df_questionnaire_w_errs: DFWithErrors,
    acceptable_range_by_column: Optional[dict[str, list[int, int]]] = None,
) -> DFWithErrors:
    if acceptable_range_by_column is None:
        acceptable_range_by_column = params.DATA_RETURN.ACCEPTABLE_RANGE

    for (column_name, (lower_limit, upper_limit)) in acceptable_range_by_column.items():
        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            BetweenValidator(
                column=column_name, lower_limit=lower_limit, upper_limit=upper_limit
            )
        )

    return df_questionnaire_w_errs


class BetweenValidator(BaseValidator):
    """
    Validator allows any value between two other numbers, and also np.nan
    """

    def __init__(self, column: str, lower_limit: int, upper_limit: int):
        self.column: str = column
        self.lower_limit: int = lower_limit
        self.upper_limit: int = upper_limit
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(
        self, df_questionnaire_by_respondent: pd.DataFrame
    ) -> pd.Series:
        column_series = df_questionnaire_by_respondent[self.column]
        column_between_values_by_person = column_series.between(
            self.lower_limit, self.upper_limit
        )
        return ~(column_between_values_by_person | column_series.isna())

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was "
            + df_questionnaire_by_person[self.column].astype(str)
            + f" when accepted values must be between {self.lower_limit} and {self.upper_limit}"
        )
