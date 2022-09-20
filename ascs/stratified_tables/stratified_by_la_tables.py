from typing import Any
import pandas as pd
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)
from ascs import params
from ascs.stratified_tables.base_stratified_not_by_response_tables import (
    BaseStratifiedNotByResponseTables,
)
from .base_stratified_tables import SectionSettings


def create_tables_stratified_by_la(
    data_needed_for_table_creation: DataNeededForTableCreation,
):
    return StratifiedByLATables(data_needed_for_table_creation).get_all_tables()


class StratifiedByLATables(BaseStratifiedNotByResponseTables):
    def set_standard_attributes(self):
        self.subgroup_within_supergroup_columns: list[str] = ["Stratum"]

        self.pivot_table_index_columns: list[str] = ["LaCode"]
        self.pivot_table_index_order: list[
            Any
        ] = params.STRATIFIED_BY_LA_CORRECT_ROW_ORDER

        self.all_supergroup_combinations: list[list[Any]] = [
            [la_code] for la_code in params.ALL_LA_CODES
        ]
        self.respondents_zero_suppression_label: str = params.RESPONDENTS_ZERO_SUPRESSION_LABEL_BY_LA

        self.section_settings_combinations: list[SectionSettings] = [
            SectionSettings(column_question=question)
            for question in params.get_all_question_columns_pre_multichoice_merge()
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {
            "1a": self.create_percentage_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "1b": self.create_est_population_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "5": self.create_margin_of_error_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "1_auxilliary": df_table_by_supergroup_question_response,
            "1_power_bi": self.create_power_bi_table(
                df_table_for_pivot_by_supergroup_question_response
            ),
        }

    def get_supergroup_columns(self, section_settings: SectionSettings):
        return ["LaCode"]

    def get_demographic_columns_to_split_est_population_by(
        self, section_settings: SectionSettings
    ):
        return []

    def pre_pivot_format_table_by_supergroup_question_response(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return super().pre_pivot_format_table_by_supergroup_question_response(
            df_table_by_supergroup_question_response.pipe(self.attach_average_rows)
        )

    def attach_average_rows(self, df_by_supergroup_question_response):
        average_rows_formatted = self.data_needed_for_table_creation.average_rows.rename(
            columns={"average_name": "LaCode"}
        )
        return pd.concat(
            [df_by_supergroup_question_response, average_rows_formatted],
            axis=0,
            ignore_index=True,
        )
