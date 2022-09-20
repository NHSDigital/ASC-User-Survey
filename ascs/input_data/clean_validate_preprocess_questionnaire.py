import pandas as pd

from typing import Callable

from ascs.input_data.validators.serial_number_duplicates_validator import (
    SerialNumberDuplicatesValidator,
)

from .df_with_errors import DFWithErrors

from .validators.whole_number_validator import run_all_whole_number_validations
from .validators.between_validator import run_all_between_validations
from .validators.easy_read_validator import run_all_easy_read_validations
from .validators.multichoice_questions_validator import run_all_multichoice_validations
from .validators.is_in_validator import (
    run_all_is_in_validations_for_demographic_columns,
)
from .validators.column_should_be_certain_value_for_non_respondents_validator import (
    run_all_column_should_be_certain_value_for_non_respondents_validations,
)
from .validators.column_should_be_null_for_non_respondents_validator import (
    run_all_column_should_be_null_for_non_respondents_validations,
)

from .preprocess_questionnaire.type_conversions import clean_all_types
from .preprocess_questionnaire.easy_read_columns import (
    add_easy_read_columns,
    add_is_easy_read_column,
)
from .preprocess_questionnaire.excluded_columns import add_excluded_columns
from .preprocess_questionnaire.q2c_preprocessing import do_q2c_preprocessing
from .preprocess_questionnaire.demographics_columns import (
    add_all_grouped_demographics_columns,
)
from .preprocess_questionnaire.miscellaneous_preprocessing import (
    replace_erroneous_input_value_with_null,
    add_stratum_column,
)
from .preprocess_questionnaire.generate_ascof_scores import generate_all_scores


PreprocessFunction = Callable[[pd.DataFrame], pd.DataFrame]
ValidateCleanerFunction = Callable[[pd.DataFrame], DFWithErrors]


def clean_validate_preprocess_questionnaire(
    df_questionnaire_by_person: pd.DataFrame,
) -> DFWithErrors:
    # Copying the data ensures the unclean DataFrame is not edited
    df_questionnaire_by_person = df_questionnaire_by_person.copy()

    # The validation, cleaning and preprocessing build on each other
    # The order that the steps are applied therefore matters

    df_questionnaire_w_errs = (
        DFWithErrors(df_questionnaire_by_person)
        .run_transformer_on_df(replace_erroneous_input_value_with_null)
        .pipe(clean_all_types)
        .pipe(validate_that_numbers_are_in_expected_range)
        .pipe(add_derived_columns_needed_for_later_validations)
        .pipe(run_more_complex_validations)
        .pipe(do_final_preprocessing)
    )

    return df_questionnaire_w_errs


def validate_that_numbers_are_in_expected_range(
    df_questionnaire_w_errs: DFWithErrors,
) -> DFWithErrors:
    return (
        df_questionnaire_w_errs.pipe(run_all_whole_number_validations)
        .pipe(run_all_between_validations)
        .pipe(run_all_is_in_validations_for_demographic_columns)
    )


def add_derived_columns_needed_for_later_validations(
    df_questionnaire_w_errs: DFWithErrors,
) -> DFWithErrors:
    return df_questionnaire_w_errs.run_transformer_on_df(
        add_stratum_column
    ).run_transformer_on_df(add_is_easy_read_column)


def run_more_complex_validations(
    df_questionnaire_w_errs: DFWithErrors,
) -> DFWithErrors:
    return (
        df_questionnaire_w_errs.pipe(
            run_all_column_should_be_null_for_non_respondents_validations
        )
        .pipe(run_all_column_should_be_certain_value_for_non_respondents_validations)
        .pipe(run_all_easy_read_validations)
        .pipe(run_all_multichoice_validations)
        .run_validator_on_df(SerialNumberDuplicatesValidator())
    )


def do_final_preprocessing(df_questionnaire_w_errs: DFWithErrors,) -> DFWithErrors:
    return (
        df_questionnaire_w_errs.run_transformer_on_df(add_easy_read_columns)
        .run_transformer_on_df(add_excluded_columns)
        .run_transformer_on_df(add_all_grouped_demographics_columns)
        .run_transformer_on_df(do_q2c_preprocessing)
        .run_transformer_on_df(generate_all_scores)
    )
