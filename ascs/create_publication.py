from typing import Callable
import pandas as pd

import logging
import timeit
from ascs.input_data.checkpoint.checkpoint_menu import (
    load_data_from_data_return_with_menu,
)

from ascs.menu import choose_which_params_file_to_use, select_tables_to_run
from ascs.simple_outputs.admin_data_table import create_admin_data_table
from ascs.simple_outputs.demographics_table import create_demographics_table
from ascs.simple_outputs.outputs_already_in_the_data_needed_for_table_creation import (
    get_average_rows,
    get_cleaned_questionnaire,
    get_dq_errors_loading_validating,
    get_unclean_questionnaire,
)
from ascs.simple_outputs.suppressed_questionnaire import create_suppressed_questionnaire
from ascs.utilities.setup_logging import setup_logging

from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
    get_data_needed_for_table_creation_from_loaded_data_returns,
)

from ascs.methodology_figures import create_all_methodology_tables
from ascs.stratified_tables.stratified_by_demographic_tables import (
    create_tables_stratified_by_demographic,
)
from ascs.stratified_tables.stratified_by_la_response import (
    create_tables_stratified_by_la_response,
)
from ascs.stratified_tables.stratified_by_la_tables import (
    create_tables_stratified_by_la,
)
from ascs.stratified_tables.stratified_by_response_tables import (
    create_tables_stratified_by_response,
)
from ascs.stratified_tables.stratified_by_la_demographic import (
    create_tables_stratified_by_la_demographic,
)
from ascs.response_rate_by_area.response_rate_by_area import (
    create_response_rate_by_area_table,
)
from ascs.utilities.save_to_file import save_all_tables_to_csv, save_all_tables_to_excel

from ascs.simple_outputs.eligible_population_questionnaire_data_disparity_dq_table import (
    create_eligible_population_questionnaire_data_disparity_dq_table,
)

FunctionForTableCreation = Callable[
    [DataNeededForTableCreation], dict[str, pd.DataFrame]
]

TABLES_OPTIONS: dict[str, FunctionForTableCreation] = {
    "Response by LA (1a, 1b, 5, 1aux)": create_tables_stratified_by_la,
    "Response by Demographic (2a, 2b, 2aux)": create_tables_stratified_by_demographic,
    "Response by Response (3a, 3b, 3aux)": create_tables_stratified_by_response,
    "Response Rates (4)": create_response_rate_by_area_table,
    "Demographics (6)": create_demographics_table,
    "Missing admin (DQ1, DQ2)": create_admin_data_table,
    "Suppressed Questionnaire": create_suppressed_questionnaire,
    "Stratified_by_LA_Demographic": create_tables_stratified_by_la_demographic,
    "Stratified_by_LA_Response": create_tables_stratified_by_la_response,
    "Methodology Figures": create_all_methodology_tables,
    "Eligible Population/Questionnaire Data Disparity DQ Table": create_eligible_population_questionnaire_data_disparity_dq_table,
    "Average Rows": get_average_rows,
    "DQ Errors Loading and Validating Data": get_dq_errors_loading_validating,
    "Cleaned questionnaire": get_cleaned_questionnaire,
    "Consolidated but uncleaned questionnaire": get_unclean_questionnaire,
}

ALL_TABLES_IDS = list(TABLES_OPTIONS.keys())


def main() -> None:
    setup_logging()

    choose_which_params_file_to_use()

    selected_table_ids: list[str] = select_tables_to_run(ALL_TABLES_IDS)

    start_time = timeit.default_timer()

    loaded_data_returns = load_data_from_data_return_with_menu()

    data_needed_for_table_creation = get_data_needed_for_table_creation_from_loaded_data_returns(
        loaded_data_returns
    )

    output_tables = create_selected_tables(
        data_needed_for_table_creation, selected_table_ids
    )

    save_all_tables_to_csv(output_tables)
    save_all_tables_to_excel(output_tables)

    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_publication: {int(total_time / 60)} minutes and {round(total_time%60)} seconds."
    )


def create_selected_tables(
    data_needed_for_table_creation: DataNeededForTableCreation,
    tables_to_run=ALL_TABLES_IDS,
) -> dict[str, pd.DataFrame]:

    output_tables_by_table_name = {}

    for table_id in tables_to_run:
        function_to_create_table: FunctionForTableCreation = TABLES_OPTIONS[table_id]

        logging.info(f"Started creating table {table_id}")

        generated_tables: dict[str, pd.DataFrame] = function_to_create_table(
            data_needed_for_table_creation
        )

        logging.info(f"Finished creating table {table_id}")

        output_tables_by_table_name.update(generated_tables)

    return output_tables_by_table_name


if __name__ == "__main__":
    main()
