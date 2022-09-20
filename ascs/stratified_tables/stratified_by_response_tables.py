from typing import Any, Literal
import pandas as pd
from ascs import params
from ascs.input_data.get_data_needed_for_table_creation import (
    DataNeededForTableCreation,
)
from ascs.utilities.combine_multiple_choice import (
    combine_multiple_choice,
    combine_multiple_choice_auxiliary_utility,
)
from .base_stratified_tables import (
    BaseStratifiedTables,
    EasyReadInfo,
    SectionSettings,
    get_question_easy_read_info,
)


def create_tables_stratified_by_response(
    data_needed_for_table_creation: DataNeededForTableCreation,
):
    return StratifiedByResponseTables(data_needed_for_table_creation).get_all_tables()


class ByResponseSectionSettings(SectionSettings):
    row_question: str
    row_question_er_info: EasyReadInfo
    row_question_possible_responses: list[Any]

    def __init__(self, column_question: str, row_question: str) -> None:
        super().__init__(column_question)
        self.row_question = row_question
        self.row_question_er_info = get_question_easy_read_info(row_question)
        self.row_question_possible_responses = params.POSSIBLE_RESPONSES_BY_QUESTION_ANNEX_3_ROWS[
            row_question
        ]

    def __str__(self) -> str:
        return f"ByResponseSectionSettings(column_question={self.column_question}, row_question={self.row_question})"


def section_is_a_combination_of_questions_that_doesnt_make_sense(
    section_settings: ByResponseSectionSettings,
) -> bool:
    (
        column_question_base,
        column_question_easy_read_type,
    ) = section_settings.column_question_er_info
    (
        row_question_base,
        row_question_easy_read_type,
    ) = section_settings.row_question_er_info

    if any(
        row_question_base.startswith(multichoice_question_base)
        for multichoice_question_base in params.MULTIPLE_CHOICE_QUESTIONS
    ):
        row_question_base = row_question_base[:-1]

    if any(
        column_question_base.startswith(multichoice_question_base)
        for multichoice_question_base in params.MULTIPLE_CHOICE_QUESTIONS
    ):
        column_question_base = column_question_base[:-1]

    if row_question_base == column_question_base:
        return True

    if row_question_base.replace("Excl", "") == column_question_base.replace(
        "Excl", ""
    ):
        return True

    questions_both_easy_read_type = (
        row_question_easy_read_type and column_question_easy_read_type
    )
    easy_read_type_different = (
        row_question_easy_read_type != column_question_easy_read_type
    )

    if questions_both_easy_read_type and easy_read_type_different:
        return True

    one_question_easy_read = "ER" in [
        row_question_easy_read_type,
        column_question_easy_read_type,
    ]

    one_question_2c = "q2c" in [row_question_base, column_question_base]

    if one_question_easy_read and one_question_2c:
        return True

    return False


class StratifiedByResponseTables(BaseStratifiedTables):
    def set_standard_attributes(self):
        self.subgroup_within_supergroup_columns: list[str] = ["LaCode", "Stratum"]

        self.pivot_table_index_columns: list[str] = [
            "row_question",
            "row_response",
        ]
        self.pivot_table_index_order: list[
            Any
        ] = params.STRATIFIED_BY_RESPONSE_CORRECT_ROW_ORDER

        self.all_supergroup_combinations: list[list[Any]] = [
            [row_question, row_response]
            for row_question, row_responses in params.POSSIBLE_RESPONSES_BY_QUESTION_ANNEX_3_ROWS.items()
            for row_response in row_responses
        ]
        self.respondents_zero_suppression_label: str = params.RESPONDENTS_ZERO_SUPRESSION_LABEL_STANDARD

        self.section_settings_combinations: list[SectionSettings] = [
            ByResponseSectionSettings(
                column_question=column_question, row_question=row_question
            )
            for column_question in params.get_all_question_columns_pre_multichoice_merge()
            for row_question in params.get_questions_without_excluded_questions()
        ]

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        return {
            "3a": self.create_percentage_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "3b": self.create_est_population_table_by_supergroup(
                df_table_for_pivot_by_supergroup_question_response
            ),
            "3_auxilliary": df_table_by_supergroup_question_response,
            "3_power_bi": self.create_power_bi_table(
                df_table_for_pivot_by_supergroup_question_response
            ),
        }

    def get_section_that_is_all_z(
        self, section_settings: ByResponseSectionSettings
    ) -> pd.DataFrame:
        return (
            pd.DataFrame(
                [],
                columns=[
                    "est_population",
                    "percentage",
                    "margin_of_error",
                    "respondents",
                    "supergroup_population",
                ],
                # If you don't set a dtype it becomes dtype object
                # Later on, dtype object makes rounding not work
                dtype=float,
            )
            .reindex(
                self.get_section_that_is_all_z_index(section_settings), fill_value=0,
            )
            .assign(suppress="[z]")
            .reset_index()
        )

    def get_section_that_is_all_z_index(
        self, section_settings: ByResponseSectionSettings
    ):
        return pd.MultiIndex.from_product(
            [
                [section_settings.row_question],
                section_settings.row_question_possible_responses,
                [section_settings.column_question],
                section_settings.column_question_possible_responses,
            ],
            names=[
                "row_question",
                "row_response",
                "column_question",
                "column_response",
            ],
        )

    def get_section_from_section_settings(
        self, section_settings: ByResponseSectionSettings
    ) -> pd.DataFrame:
        if section_is_a_combination_of_questions_that_doesnt_make_sense(
            section_settings
        ):
            return self.get_section_that_is_all_z(section_settings)
        else:
            return super().get_section_from_section_settings(section_settings)

    def get_supergroup_columns(self, section_settings: ByResponseSectionSettings):
        return [section_settings.row_question]

    def format_section(
        self, section: pd.DataFrame, section_settings: ByResponseSectionSettings
    ):
        return (
            super()
            .format_section(section, section_settings)
            .rename(columns={section_settings.row_question: "row_response"})
            .assign(row_question=section_settings.row_question)
        )

    def get_demographic_columns_to_split_est_population_by(
        self, section_settings: ByResponseSectionSettings
    ):
        return [section_settings.row_question]

    def use_population_2c(self, section_settings: ByResponseSectionSettings) -> bool:
        return (
            section_settings.column_question == "q2c"
            or section_settings.row_question == "q2c"
        )

    def get_easy_read_weight_type_to_use(
        self, section_settings: ByResponseSectionSettings
    ) -> Literal["Std", "ER", None]:
        if "Std" in [
            section_settings.column_question_er_info.easy_read_type,
            section_settings.row_question_er_info.easy_read_type,
        ]:
            return "Std"
        if "ER" in [
            section_settings.column_question_er_info.easy_read_type,
            section_settings.row_question_er_info.easy_read_type,
        ]:
            return "ER"
        return None

    def combine_multiple_choice_rows(
        self, generic_pivot_table: pd.DataFrame
    ) -> pd.DataFrame:
        return generic_pivot_table.T.pipe(
            combine_multiple_choice, params.MULTIPLE_CHOICE_QUESTIONS
        ).T

    def combine_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        return (
            super()
            .combine_rows_and_columns_in_pivotted(df_table_by_supergroup)
            .pipe(self.combine_multiple_choice_rows)
        )

    def pre_pivot_format_table_by_supergroup_question_response(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return super().pre_pivot_format_table_by_supergroup_question_response(
            df_table_by_supergroup_question_response.pipe(self.attach_average_rows)
        )

    def attach_average_rows(self, df_by_supergroup_question_response):
        average_rows_formatted = self.data_needed_for_table_creation.average_rows.rename(
            columns={"average_name": "row_response"}
        )
        average_rows_formatted["row_question"] = "Average"
        return pd.concat(
            [average_rows_formatted, df_by_supergroup_question_response],
            ignore_index=True,
        )[df_by_supergroup_question_response.columns]

    def combine_multiple_choice_auxiliary(
        self, df_by_supergroup_question_response: pd.DataFrame
    ):
        return (
            super()
            .combine_multiple_choice_auxiliary(df_by_supergroup_question_response)
            .pipe(
                combine_multiple_choice_auxiliary_utility,
                question_column="row_question",
                response_column="row_response",
                multichoice_questions=params.MULTIPLE_CHOICE_QUESTIONS,
            )
        )

    def replace_single_digit_questions_with_double_digit(
        self, df_by_supergroup_question_response: pd.DataFrame
    ):
        df_by_supergroup_question_response[
            "row_question"
        ] = df_by_supergroup_question_response["row_question"].replace(
            params.QUESTION_DOUBLE_DIGIT_FORMAT
        )

        return super().replace_single_digit_questions_with_double_digit(
            df_by_supergroup_question_response
        )
