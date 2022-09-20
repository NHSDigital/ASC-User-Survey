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


class DemographicSectionSettings(SectionSettings):
    def __init__(
        self,
        column_question: str,
        demographic_readable_name: str,
        demographic_column: str,
    ) -> None:
        super().__init__(column_question)
        self.demographic_readable_name: str = demographic_readable_name
        self.demographic_column: str = demographic_column

    def __str__(self) -> str:
        return f"DemographicSectionSettings(column_question={self.column_question}, demographic_readable_name={self.demographic_readable_name})"


def create_tables_stratified_by_demographic(
    data_needed_for_table_creation: DataNeededForTableCreation,
):
    return StratifiedByDemographicTables(
        data_needed_for_table_creation
    ).get_all_tables()


class StratifiedByDemographicTables(BaseStratifiedNotByResponseTables):
    def set_standard_attributes(self):
        self.subgroup_within_supergroup_columns: list[str] = ["LaCode", "Stratum"]

        self.pivot_table_index_columns: list[str] = ["demographic", "demographic_value"]
        self.pivot_table_index_order: list[
            Any
        ] = params.STRATIFIED_BY_DEMOGRAPHIC_CORRECT_ROW_ORDER

        self.all_supergroup_combinations: list[list[Any]] = [
            [demographic, demographic_value]
            for demographic, demographic_values in params.DEMOGRAPHIC_VALUES_BY_DEMOGRAPHIC.items()
            for demographic_value in demographic_values
        ]
        self.respondents_zero_suppression_label: str = params.RESPONDENTS_ZERO_SUPRESSION_LABEL_STANDARD

        self.section_settings_combinations: list[DemographicSectionSettings] = [
            DemographicSectionSettings(
                column_question=question,
                demographic_readable_name=demographic_readable_name,
                demographic_column=demographic_column,
            )
            for question in params.get_all_question_columns_pre_multichoice_merge()
            for demographic_readable_name, demographic_column in params.get_grouped_demographic_column_by_readable_name().items()
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {
            "2a": self.create_percentage_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "2b": self.create_est_population_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "2_auxilliary": df_table_by_supergroup_question_response,
            "2_power_bi": self.create_power_bi_table(
                df_table_for_pivot_by_supergroup_question_response
            ),
        }

    def get_supergroup_columns(self, section_settings: DemographicSectionSettings):
        return [section_settings.demographic_column]

    def format_section(
        self, section: pd.DataFrame, section_settings: DemographicSectionSettings
    ):
        return (
            super()
            .format_section(section, section_settings)
            .rename(columns={section_settings.demographic_column: "demographic_value"})
            .assign(demographic=section_settings.demographic_readable_name)
        )

    def get_demographic_columns_to_split_est_population_by(
        self, section_settings: DemographicSectionSettings
    ):
        return [section_settings.demographic_column]

    def combine_RHC_rows(self, df_table_by_supergroup):
        df_table_by_supergroup.loc[("RHC", "Autism"), :] = df_table_by_supergroup.loc[
            ("RHC_autism", "Yes")
        ]
        df_table_by_supergroup.loc[("RHC", "Asperger"), :] = df_table_by_supergroup.loc[
            ("RHC_asperger", "Yes")
        ]
        df_table_by_supergroup = df_table_by_supergroup.drop(
            ["RHC_autism", "RHC_asperger"]
        )
        return df_table_by_supergroup

    def combine_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        return (
            super()
            .combine_rows_and_columns_in_pivotted(df_table_by_supergroup)
            .pipe(self.combine_RHC_rows)
        )

    def pre_pivot_format_table_by_supergroup_question_response(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return super().pre_pivot_format_table_by_supergroup_question_response(
            df_table_by_supergroup_question_response.pipe(self.attach_average_rows)
        )

    def attach_average_rows(self, df_by_supergroup_question_response):
        average_rows_formatted = self.data_needed_for_table_creation.average_rows.rename(
            columns={"average_name": "demographic_value"}
        )
        average_rows_formatted["demographic"] = "Average"
        return pd.concat(
            [average_rows_formatted, df_by_supergroup_question_response],
            ignore_index=True,
        )[df_by_supergroup_question_response.columns]
