import numpy as np
import pandas as pd

from typing import Any, Optional
from ..df_with_errors import DFWithErrors

from .base_validator import BaseValidator

from ascs import params


def run_all_is_in_validations_for_demographic_columns(
    df_questionnaire_w_errs: DFWithErrors,
    demographics_coversions: Optional[dict[str, dict[int, Any]]] = None,
) -> DFWithErrors:
    """
    Checks the demographic columns have the values listed in params.DEMOGRAPHICS_CONVERSIONS
    """
    if demographics_coversions is None:
        demographics_coversions = params.DEMOGRAPHICS_CONVERSIONS

    for demog_column_name, demog_conversions in demographics_coversions.items():
        if demog_column_name == "Stratum":
            continue  # Stratum is a derived column, no need to check it

        df_questionnaire_w_errs = df_questionnaire_w_errs.run_validator_on_df(
            IsInValidator(
                column=demog_column_name,
                accepted_values=list(demog_conversions.keys()) + [np.nan],
            )
        )

    return df_questionnaire_w_errs


class IsInValidator(BaseValidator):
    """
    Validator allows any value in a list, and also np.nan
    """

    def __init__(self, column: str, accepted_values: list[Any]):
        self.column: str = column
        self.accepted_values: list[Any] = accepted_values
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(
        self, df_questionnaire_by_respondent: pd.DataFrame
    ) -> pd.Series:
        return ~df_questionnaire_by_respondent[self.column].isin(self.accepted_values)

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was "
            + df_questionnaire_by_person[self.column].astype(str)
            + f" when accepted values are {self.accepted_values}"
        )
