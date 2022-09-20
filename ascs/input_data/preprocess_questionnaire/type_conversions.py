import numpy as np
import pandas as pd

from typing import Optional

from ..preprocess_utilities import get_numeric_columns_from_df_questionnaire_by_person
from ..df_with_errors import DFWithErrors

from ..validators.numeric_column_validator import NumericColumnValidator

from ascs import params


def clean_all_types(df_questionnaire_w_errs: DFWithErrors,) -> DFWithErrors:
    """
    Makes string column string
    Number columns number
    And also makes sure that nulls are a consistent data type (None for string cols, np.nan for number cols)
    """
    return df_questionnaire_w_errs.run_transformer_on_df(
        make_string_columns_either_string_or_none
    ).run_validator_function_on_df(clean_types_in_numeric_columns)


def clean_types_in_numeric_columns(
    df_questionnaire_by_person: pd.DataFrame,
    numeric_column_names: Optional[list[str]] = None,
) -> DFWithErrors:
    """
    Numeric columns could contain a string like "5"
    Convert that string to a number, 5
    If there are strings like "a" in the column, they will be set to np.nan
    and there will be a warning in the error df
    """
    if numeric_column_names is None:
        numeric_column_names = get_numeric_columns_from_df_questionnaire_by_person(
            df_questionnaire_by_person
        )

    error_dfs: list[pd.DataFrame] = []

    for column_name in numeric_column_names:
        df_questionnaire_by_person[column_name] = (
            df_questionnaire_by_person[column_name]
            .copy()
            .pipe(make_all_null_values_consistent, output_null_value=np.nan)
            .pipe(convert_strings_that_are_numbers_into_numbers)
        )

        (
            df_questionnaire_by_person,
            error_dfs_from_one_validator,
        ) = NumericColumnValidator(column=column_name).run_check(
            df_questionnaire_by_person
        )

        error_dfs.extend(error_dfs_from_one_validator)

        df_questionnaire_by_person[column_name] = df_questionnaire_by_person[
            column_name
        ].infer_objects()

        assert np.issubdtype(
            df_questionnaire_by_person[column_name].dtype, np.number  # type: ignore
        ), f"Column {column_name} was still not a numeric dtype even after conversion. This is a bug that could cause later issues."

    return DFWithErrors(df=df_questionnaire_by_person, error_dfs=error_dfs)


def convert_strings_that_are_numbers_into_numbers(series: pd.Series) -> pd.Series:
    series_converted_to_number = pd.to_numeric(series, errors="coerce")
    series[~series_converted_to_number.isna()] = series_converted_to_number

    return series


def make_string_columns_either_string_or_none(
    df_questionnaire_by_person: pd.DataFrame,
    string_column_names: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Ensures string columns have consistent format
    Either the value is a string
    Or the value is a None, standing for null
    Empty strings -> None
    """
    if string_column_names is None:
        string_column_names = params.DATA_RETURN.STRING_COLUMNS

    for column_name in string_column_names:
        df_questionnaire_by_person[column_name] = (
            df_questionnaire_by_person[column_name]
            .copy()
            .pipe(make_all_null_values_consistent, output_null_value=None)
            .pipe(convert_to_string_where_series_isnt_null)
        )

    return df_questionnaire_by_person


def make_all_null_values_consistent(
    series: pd.Series, output_null_value=None
) -> pd.Series:
    """
    Counts an empty string as a null value
    """
    series[series.isna()] = output_null_value

    return series.replace({"": output_null_value})


def convert_to_string_where_series_isnt_null(series: pd.Series) -> pd.Series:
    series[~series.isna()] = series.astype(str)

    return series
