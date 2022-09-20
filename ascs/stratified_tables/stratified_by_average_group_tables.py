from typing import Any, Union
import pandas as pd
from ascs import params
from ascs.stratified_tables.base_stratified_not_by_response_tables import (
    BaseStratifiedNotByResponseTables,
)
from ascs.stratified_tables.base_stratified_tables import SectionSettings


class AverageGroupSectionSettings(SectionSettings):
    average_name: str
    la_codes_to_average: list[Union[str, int]]

    def __init__(
        self,
        column_question,
        average_name: str,
        la_codes_to_average: list[Union[str, int]],
    ):
        super().__init__(column_question)
        self.average_name = average_name
        self.la_codes_to_average = la_codes_to_average

    def __str__(self) -> str:
        return f"AverageGroupSectionSettings(column_question={self.column_question}, average_name={self.average_name})"


class StratifiedByAverageGroupTables(BaseStratifiedNotByResponseTables):
    def set_standard_attributes(self):
        self.subgroup_within_supergroup_columns: list[str] = ["LaCode", "Stratum"]
        self.pivot_table_index_columns: list[str] = ["average_name"]

        self.all_supergroup_combinations: list[list[Any]] = [
            [average_group_name]
            for average_group_name in params.LA_CODE_LIST_BY_AVERAGE_GROUP_NAME.keys()
        ]
        self.respondents_zero_suppression_label: str = params.RESPONDENTS_ZERO_SUPRESSION_LABEL_BY_LA

        self.section_settings_combinations: list[AverageGroupSectionSettings] = [
            AverageGroupSectionSettings(question, average_name, la_codes_to_average)
            for question in params.get_all_question_columns_pre_multichoice_merge()
            for average_name, la_codes_to_average in params.LA_CODE_LIST_BY_AVERAGE_GROUP_NAME.items()
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {"average_rows": df_table_by_supergroup_question_response}

    def format_section(
        self, section: pd.DataFrame, section_settings: AverageGroupSectionSettings
    ):
        return (
            super()
            .format_section(section, section_settings)
            .assign(average_name=section_settings.average_name)
        )

    def get_supergroup_columns(
        self, section_settings: AverageGroupSectionSettings
    ) -> list[str]:
        return []

    def get_demographic_columns_to_split_est_population_by(
        self, section_settings: SectionSettings
    ):
        return []

    def get_df_questionnaire_by_person_for_section(
        self, section_settings: AverageGroupSectionSettings
    ) -> pd.DataFrame:
        return self.data_needed_for_table_creation.df_questionnaire_by_person[
            self.data_needed_for_table_creation.df_questionnaire_by_person[
                "LaCode"
            ].isin(section_settings.la_codes_to_average)
        ]
