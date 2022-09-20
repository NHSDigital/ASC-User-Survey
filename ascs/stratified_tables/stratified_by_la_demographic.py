from ascs.stratified_tables.stratified_by_demographic_tables import (
    StratifiedByDemographicTables,
    DemographicSectionSettings,
)
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)
from ascs import params
from typing import Any
import pandas as pd


def create_tables_stratified_by_la_demographic(
    data_needed_for_table_creation: DataNeededForTableCreation,
):
    return StratifiedByLAAndDemographic(data_needed_for_table_creation).get_all_tables()


class StratifiedByLAAndDemographic(StratifiedByDemographicTables):
    def set_standard_attributes(self):
        super().set_standard_attributes()

        self.subgroup_within_supergroup_columns: list[str] = ["Stratum"]
        self.pivot_table_index_columns: list[str] = [
            "LaCode",
            "demographic",
            "demographic_value",
        ]

        self.all_supergroup_combinations: list[list[Any]] = [
            [LaCode, demographic, demographic_value]
            for LaCode in params.ALL_LA_CODES
            for demographic, demographic_values in params.DEMOGRAPHIC_VALUES_BY_DEMOGRAPHIC.items()
            for demographic_value in demographic_values
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {
            "LA_and_Demographic_power_bi": self.create_power_bi_table(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "LA_and_Demographic_auxiliary": df_table_by_supergroup_question_response,
        }

    def get_supergroup_columns(self, section_settings: DemographicSectionSettings):
        return ["LaCode", section_settings.demographic_column]

    def attach_average_rows(self, df_by_supergroup_question_response):
        # Don't attach average rows
        return df_by_supergroup_question_response
