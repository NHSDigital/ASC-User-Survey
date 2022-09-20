from typing import Union
import pandas as pd
import numpy as np

from ..df_with_errors import DFWithErrors


class BaseValidator:
    """
    A class that:
    Finds an issue (like a number being outside of an accepted range in a column).
    Creates a DataFrame highlighting the rows with that error, with a good error message.
    Sets the invalid cells to null.
    """

    columns_to_set_null_for_invalid_rows: list[str]

    def run_check(self, df_questionnaire_by_person: pd.DataFrame) -> DFWithErrors:
        incorrect_by_person_series = self.get_where_incorrect(
            df_questionnaire_by_person
        )

        there_were_no_errors = not incorrect_by_person_series.any()

        if there_were_no_errors:
            return DFWithErrors(df=df_questionnaire_by_person, error_dfs=[])

        df_by_error = self.get_error_df(
            df_questionnaire_by_person, incorrect_by_person_series
        )
        df_questionnaire_by_person_validated = self.set_incorrect_to_nan(
            df_questionnaire_by_person, incorrect_by_person_series
        )
        return DFWithErrors(
            df=df_questionnaire_by_person_validated, error_dfs=[df_by_error],
        )

    def set_incorrect_to_nan(
        self, df_questionnaire_by_person: pd.DataFrame, incorrect_by_person: pd.Series,
    ) -> pd.DataFrame:
        df_questionnaire_by_person.loc[
            incorrect_by_person, self.columns_to_set_null_for_invalid_rows
        ] = np.nan
        return df_questionnaire_by_person

    def get_where_incorrect(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        """
        Return a pandas boolean series with True for invalid rows
        """
        raise NotImplementedError()

    def get_error_df(
        self, df_questionnaire_by_person: pd.DataFrame, incorrect_by_person: pd.Series
    ) -> pd.DataFrame:
        df_by_error = self.get_rows_and_columns_of_questionnaire_needed_in_error_df(
            df_questionnaire_by_person, incorrect_by_person
        )
        df_by_error["message"] = self.get_error_message(
            df_questionnaire_by_person.loc[incorrect_by_person]
        )
        return df_by_error

    def get_rows_and_columns_of_questionnaire_needed_in_error_df(
        self, df_questionnaire_by_person: pd.DataFrame, incorrect_by_person: pd.Series
    ) -> pd.DataFrame:
        return df_questionnaire_by_person.loc[
            incorrect_by_person, ["LaCode", "PrimaryKey", "SerialNo"]
        ]

    def get_error_message(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> Union[str, pd.Series]:
        """
        Return a human readable error message describing the problem (for the rows with a problem)
        """
        raise NotImplementedError()

