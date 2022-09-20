import pandas as pd
import pytest
from ascs import params

from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs.input_data.load_data_returns.data_return_config import LoadedDataReturns

from ascs.methodology_figures import create_all_methodology_tables
from ascs.output_to_excel.output_to_excel import output_annex_table_excel_file
from ascs.stratified_tables.stratified_by_demographic_tables import (
    create_tables_stratified_by_demographic,
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
from ascs.stratified_tables.stratified_by_la_response import (
    create_tables_stratified_by_la_response,
)
from ascs.response_rate_by_area.response_rate_by_area import (
    create_response_rate_by_area_table,
)
from ascs.simple_outputs.demographics_table import create_demographics_table
from ascs.simple_outputs.admin_data_table import create_admin_data_table

from ascs.create_publication import (
    get_data_needed_for_table_creation_from_loaded_data_returns,
)
from ascs.input_data.load_data_returns.load_excel import (
    load_all_data_returns_from_excel,
)


@pytest.fixture(scope="session")
def loaded_data_returns() -> LoadedDataReturns:
    return load_all_data_returns_from_excel()


@pytest.fixture(scope="session")
def data_needed_for_table_creation(loaded_data_returns) -> DataNeededForTableCreation:
    return get_data_needed_for_table_creation_from_loaded_data_returns(
        loaded_data_returns
    )


@pytest.fixture(scope="session")
def annex_table1_and_5(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_tables_stratified_by_la(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def annex_table2(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_tables_stratified_by_demographic(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def annex_table3(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_tables_stratified_by_response(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def annex_table4(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_response_rate_by_area_table(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def annex_table6(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_demographics_table(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def consolidated_tables_for_annex_table(
    annex_table1_and_5: dict[str, pd.DataFrame],
    annex_table2: dict[str, pd.DataFrame],
    annex_table3: dict[str, pd.DataFrame],
    annex_table4: dict[str, pd.DataFrame],
    annex_table6: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    return {
        **annex_table1_and_5,
        **annex_table2,
        **annex_table3,
        **annex_table4,
        **annex_table6,
    }


@pytest.fixture(scope="session")
def annex_dq_table1_and_2(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_admin_data_table(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def average_rows(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return data_needed_for_table_creation.average_rows


@pytest.fixture(scope="session")
def stratified_by_la_demographic(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_tables_stratified_by_la_demographic(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def stratified_by_la_response(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_tables_stratified_by_la_response(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def methodology_tables(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:
    return create_all_methodology_tables(data_needed_for_table_creation)


@pytest.fixture(scope="session")
def my_temp_path(tmp_path_factory) -> str:
    return tmp_path_factory.mktemp("temp")


@pytest.fixture(scope="session")
def save_to_excel(
    my_temp_path: str, consolidated_tables_for_annex_table: dict[str, pd.DataFrame]
) -> str:
    output_path = f"{my_temp_path}/{params.OUTPUT_ANNEX_TABLE_FILE_NAME}"

    output_annex_table_excel_file(
        consolidated_tables_for_annex_table,
        template_path=params.TEMPLATE_ANNEX_TABLE_FILE_PATH,
        output_path=output_path,
    )

    return output_path
