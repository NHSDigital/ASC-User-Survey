import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation


def get_average_rows(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return {"average_rows": data_needed_for_table_creation.average_rows}


def get_dq_errors_loading_validating(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return {
        "dq_validation_errors": data_needed_for_table_creation.df_by_validation_error,
        "errors_loading_files": data_needed_for_table_creation.df_loading_error_by_file,
    }


def get_cleaned_questionnaire(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return {
        "cleaned_questionnaire": data_needed_for_table_creation.df_questionnaire_by_person
    }


def get_unclean_questionnaire(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return {
        "uncleaned_questionnaire": data_needed_for_table_creation.df_questionnaire_unclean_by_person
    }
