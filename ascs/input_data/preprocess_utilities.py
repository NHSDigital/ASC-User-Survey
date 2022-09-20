import pandas as pd

from typing import Any, Optional

from ascs import params


def filter_local_authorities_to_only_those_in_whitelist(
    df: pd.DataFrame, la_code_whitelist: Optional[list[Any]] = None,
):
    if la_code_whitelist is None:
        la_code_whitelist = params.LA_CODE_WHITELIST

    return df[df.LaCode.isin(la_code_whitelist)]


def get_numeric_columns_from_df_questionnaire_by_person(
    df_questionnaire_by_person: pd.DataFrame, string_columns: Optional[list[str]] = None
) -> list[str]:
    """
    Either the column is string, or the column is numeric.
    Hence, get all the columns then take out those that are string
    """
    if string_columns is None:
        string_columns = params.DATA_RETURN.STRING_COLUMNS

    return df_questionnaire_by_person.columns.difference(
        params.DATA_RETURN.STRING_COLUMNS
    ).to_list()
