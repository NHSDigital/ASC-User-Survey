import pandas as pd

from .base_validator import BaseValidator


class NumericColumnValidator(BaseValidator):
    """
    Looks through a column and finds any values that aren't ints or floats.
    """

    def __init__(self, column: str) -> None:
        self.column: str = column
        self.columns_to_set_null_for_invalid_rows = [column]

    def get_where_incorrect(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        return ~df_questionnaire_by_person[self.column].apply(type).isin([int, float])

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"Column {self.column} was '"
            + df_questionnaire_by_person[self.column].astype(str)
            + "' but should be a number"
        )
