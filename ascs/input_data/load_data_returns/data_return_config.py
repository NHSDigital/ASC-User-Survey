from typing import NamedTuple, Union
import typed_params
import pandas as pd


class DataReturnParams(typed_params.BaseModel):
    NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING: dict[str, str]
    STRING_COLUMNS: list[str]
    ACCEPTABLE_RANGE: dict[str, list[int, int]]


class LoadedDataReturns(NamedTuple):
    df_questionnaire_unclean_by_person: pd.DataFrame
    df_loading_error_by_file: pd.DataFrame
