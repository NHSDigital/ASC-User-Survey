import logging

from .data_needed_for_table_creation import DataNeededForTableCreation
from .load_data_returns.data_return_config import LoadedDataReturns
from .load_csv import load_df_population_by_la

from ascs.stratified_tables.stratified_by_average_group_tables import (
    StratifiedByAverageGroupTables,
)
from .checkpoint.checkpoint_menu import load_data_from_data_return_with_menu
from .clean_validate_preprocess_questionnaire import (
    clean_validate_preprocess_questionnaire,
)
from .preprocess_eligible_population.preprocessing_eligible_population import (
    preprocess_eligible_population_data,
)


def get_data_needed_for_table_creation_from_loaded_data_returns(
    loaded_data_returns: LoadedDataReturns,
) -> DataNeededForTableCreation:
    df_questionnaire_unclean_by_person = (
        loaded_data_returns.df_questionnaire_unclean_by_person
    )
    df_loading_error_by_file = loaded_data_returns.df_loading_error_by_file
    logging.info("Loading population data")
    df_population_by_la = load_df_population_by_la().astype({"LaCode": str})
    (
        population_by_la_stratum,
        population_sample_by_la_stratum,
        population_2c_by_la_stratum,
    ) = preprocess_eligible_population_data(df_population_by_la)

    logging.info("Starting clean, validate and preprocess questionnaire")
    df_questionnaire_w_errs = clean_validate_preprocess_questionnaire(
        df_questionnaire_unclean_by_person
    )

    df_questionnaire_by_person = df_questionnaire_w_errs.df
    df_by_validation_error = df_questionnaire_w_errs.concatenate_errors_into_one_df()

    average_rows = StratifiedByAverageGroupTables(
        DataNeededForTableCreation(
            df_questionnaire_by_person=df_questionnaire_by_person,
            population_by_la_stratum=population_by_la_stratum,
            population_sample_by_la_stratum=population_sample_by_la_stratum,
            population_2c_by_la_stratum=population_2c_by_la_stratum,
        )
    ).get_table_by_supergroup_question_response()

    return DataNeededForTableCreation(
        df_questionnaire_by_person=df_questionnaire_by_person,
        population_by_la_stratum=population_by_la_stratum,
        population_sample_by_la_stratum=population_sample_by_la_stratum,
        population_2c_by_la_stratum=population_2c_by_la_stratum,
        average_rows=average_rows,
        df_by_validation_error=df_by_validation_error,
        df_loading_error_by_file=df_loading_error_by_file,
        df_questionnaire_unclean_by_person=df_questionnaire_unclean_by_person,
    )
