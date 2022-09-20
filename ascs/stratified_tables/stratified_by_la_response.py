from typing import Any

import pandas as pd
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs import params
from ascs.stratified_tables.stratified_by_response_tables import (
    ByResponseSectionSettings,
    StratifiedByResponseTables,
)


def create_tables_stratified_by_la_response(
    data_needed_for_table_creation: DataNeededForTableCreation,
):
    return StratifiedByLAAndResponse(data_needed_for_table_creation).get_all_tables()


class StratifiedByLAAndResponse(StratifiedByResponseTables):
    def set_standard_attributes(self):
        super().set_standard_attributes()

        self.subgroup_within_supergroup_columns: list[str] = ["Stratum"]
        self.pivot_table_index_columns: list[str] = [
            "LaCode",
            "row_question",
            "row_response",
        ]

        self.all_supergroup_combinations: list[list[Any]] = [
            [LaCode, row_question, row_question_response]
            for LaCode in params.ALL_LA_CODES
            for row_question, row_question_responses in params.POSSIBLE_RESPONSES_BY_QUESTION_ANNEX_3_ROWS.items()
            for row_question_response in row_question_responses
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {
            "LA_and_Response_power_bi": self.create_power_bi_table(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "LA_and_Response_auxiliary": df_table_by_supergroup_question_response,
        }

    def get_supergroup_columns(self, section_settings: ByResponseSectionSettings):
        return ["LaCode", section_settings.row_question]

    def get_section_that_is_all_z_index(
        self, section_settings: ByResponseSectionSettings
    ):
        return pd.MultiIndex.from_product(
            [
                params.ALL_LA_CODES,
                [section_settings.row_question],
                section_settings.row_question_possible_responses,
                [section_settings.column_question],
                section_settings.column_question_possible_responses,
            ],
            names=[
                "LaCode",
                "row_question",
                "row_response",
                "column_question",
                "column_response",
            ],
        )

    def attach_average_rows(self, df_by_supergroup_question_response):
        # Don't attach average rows
        return df_by_supergroup_question_response
