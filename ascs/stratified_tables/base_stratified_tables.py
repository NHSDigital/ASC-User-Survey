import logging
from typing import Any, Literal, NamedTuple, Type, Union
import numpy as np
import pandas as pd
from ascs import params
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs.stratification.stratification import perform_stratification
from ascs.utilities.combine_multiple_choice import (
    combine_multiple_choice,
    combine_multiple_choice_auxiliary_utility,
)

from ascs.stratification.get_est_population_for_demographic_subgroups import (
    get_est_population_for_demographic_subgroups,
)
from ascs.utilities.output_formatting import round_to_five


class EasyReadInfo(NamedTuple):
    base: str
    easy_read_type: Literal["Std", "ER", "Comb", None]


def get_question_easy_read_info(question) -> EasyReadInfo:
    for suffix in params.EASY_READ_COLUMN_ENDINGS:
        if question.endswith(suffix):
            return EasyReadInfo(base=question[: -len(suffix)], easy_read_type=suffix)
    return EasyReadInfo(base=question, easy_read_type=None)


class SectionSettings:
    column_question: str
    column_question_er_info: EasyReadInfo
    column_question_possible_responses: list[Any]

    def __init__(self, column_question: str) -> None:
        self.column_question = column_question
        self.column_question_er_info = get_question_easy_read_info(column_question)
        self.column_question_possible_responses = params.POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE[
            column_question
        ]

    def __str__(self) -> str:
        return f"SectionSettings(column_question={self.column_question})"

    def __repr__(self) -> str:
        return str(self)


class BaseStratifiedTables:
    subgroup_within_supergroup_columns: list[str]
    pivot_table_index_columns: list[str]
    pivot_table_index_order: list[Any]
    all_supergroup_combinations: list[list[Any]]
    respondents_zero_suppression_label: str
    section_settings_combinations: list[Type[SectionSettings]]

    def __init__(self, data_needed_for_table_creation: DataNeededForTableCreation):
        self.data_needed_for_table_creation = data_needed_for_table_creation
        self.set_standard_attributes()

    def set_standard_attributes(self):
        """
        Use this method to set all of the attributes listed at the top of the class.
        """
        raise NotImplementedError()

    def get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        df_table_for_pivot_by_supergroup_question_response: pd.DataFrame,
    ):
        raise NotImplementedError()

    def use_population_2c(self, section_settings: Type[SectionSettings]) -> bool:
        raise NotImplementedError()

    def get_supergroup_columns(
        self, section_settings: Type[SectionSettings]
    ) -> list[str]:
        raise NotImplementedError()

    def get_demographic_columns_to_split_est_population_by(
        self, section_settings: Type[SectionSettings]
    ) -> list[str]:
        raise NotImplementedError()

    def get_easy_read_weight_type_to_use(
        self, section_settings: Type[SectionSettings]
    ) -> Literal["Std", "ER", None]:
        raise NotImplementedError()

    def get_all_tables(self) -> dict[str, pd.DataFrame]:
        logging.info(f"Started generating {type(self).__name__}")

        df_table_by_supergroup_question_response = (
            self.get_table_by_supergroup_question_response()
        )
        df_table_for_pivot_by_supergroup_question_response = df_table_by_supergroup_question_response.pipe(
            self.pre_pivot_format_table_by_supergroup_question_response
        )
        all_tables = self.get_all_formatted_tables_from_auxilliary_table_by_supergroup_question_response(
            df_table_by_supergroup_question_response,
            df_table_for_pivot_by_supergroup_question_response,
        )

        logging.info(f"Finished generating {type(self).__name__}")

        return all_tables

    def get_table_by_supergroup_question_response(self) -> pd.DataFrame:
        table_sections = self.get_all_table_sections_from_setting_combinations()
        df_table_by_supergroup_question_response = (
            pd.concat(table_sections, axis=0)
            .pipe(self.add_missing_rows)
            .pipe(
                self.add_generic_respondents_column,
                new_column_name="supergroup_question_respondents",
                column_to_sum_name="respondents",
            )
            .pipe(
                self.add_generic_respondents_column,
                new_column_name="supergroup_population",
                column_to_sum_name="est_population",
            )
            .pipe(self.calc_suppress_column)
            .pipe(self.calc_suppress_margin_of_error_column)
            .pipe(self.format_auxiliary_table_output)
        )
        return df_table_by_supergroup_question_response

    def apply_rounding(self, df: pd.DataFrame):
        df["percentage"] = df["percentage"].round(1)
        df["est_population"] = df["est_population"].round(-1)
        df["margin_of_error"] = df["margin_of_error"].round(1)
        df["supergroup_population"] = df["supergroup_population"].round(-1)
        df["supergroup_question_respondents"] = df[
            "supergroup_question_respondents"
        ].pipe(round_to_five)
        return df

    def apply_suppression(
        self, df_by_supergroup_question_response: pd.DataFrame
    ) -> pd.DataFrame:
        df_by_supergroup_question_response.loc[
            df_by_supergroup_question_response["suppress"].astype(bool),
            params.COLUMNS_TO_SUPPRESS_IN_ANNEX_TABLE,
        ] = df_by_supergroup_question_response["suppress"]
        df_by_supergroup_question_response.loc[
            df_by_supergroup_question_response["suppress_margin_of_error"].astype(bool),
            "margin_of_error",
        ] = df_by_supergroup_question_response["suppress_margin_of_error"]
        return df_by_supergroup_question_response

    def add_missing_rows(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ) -> pd.DataFrame:
        """
        By "missing", we mean a missing combination of supergroup, question and response
        If nobody in supergroup 3 answered "2" to q3a,
        there will be no corresponding row in the dataframe
        but we need one, because we need to have a row there to say there were 0 respondents
        """
        return (
            df_table_by_supergroup_question_response.set_index(
                self.pivot_table_index_columns + ["column_question", "column_response"]
            )
            .pipe(self.check_no_rows_will_be_lost_on_reindex)
            .reindex(
                self.get_full_combination_of_supergroup_qustion_response_index(),
                fill_value=np.nan,
            )
            .pipe(self.fill_na_for_suppress_column_with_empty_string)
            .fillna(0)
            .reset_index()
        )

    def fill_na_for_suppress_column_with_empty_string(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ) -> pd.DataFrame:
        df_table_by_supergroup_question_response[
            "suppress"
        ] = df_table_by_supergroup_question_response["suppress"].fillna("")
        return df_table_by_supergroup_question_response

    def get_full_combination_of_supergroup_qustion_response_index(self):
        """
        With:

        self.all_supergroup_combinations = [
            ["Ethnicity", "White"],
            ["Ethnicity", "Black"],
        ]

        POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE = {
            "q3": [1,2],
            "q4": [5]
        }

        this function would output

        pd.MultiIndex([
            ["Ethnicity", "White", "q3", 1],
            ["Ethnicity", "White", "q3", 2],
            ["Ethnicity", "White", "q4", 5],
            ["Ethnicity", "Black", "q3", 1],
            ["Ethnicity", "Black", "q3", 2],
            ["Ethnicity", "Black", "q4", 5],
        ], ...)

        which is every combination of supergroup, question and question response
        """
        all_combs_of_supergroup_question_response = [
            [*supergroup, question, question_response]
            for supergroup in self.all_supergroup_combinations
            for question, question_responses in params.POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE.items()
            for question_response in question_responses
        ]
        return pd.MultiIndex.from_tuples(
            all_combs_of_supergroup_question_response,
            names=self.pivot_table_index_columns
            + ["column_question", "column_response"],
        )

    def check_no_rows_will_be_lost_on_reindex(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        index_before_reindex = df_table_by_supergroup_question_response.index
        index_after_reindex = (
            self.get_full_combination_of_supergroup_qustion_response_index()
        )
        overlapping_rows = index_before_reindex.intersection(index_after_reindex)
        elements_that_have_been_lost = index_before_reindex.difference(overlapping_rows)
        assert (
            len(elements_that_have_been_lost) == 0
        ), f"""
Reindexing in {type(self).__name__} to add missing rows would remove rows.
This likely indicates that params.py is wrong somehow.
The elements that have been lost are:
{elements_that_have_been_lost}
"""
        return df_table_by_supergroup_question_response

    def add_generic_respondents_column(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        new_column_name: str,
        column_to_sum_name: str,
    ) -> pd.DataFrame:
        df_table_by_supergroup_question_response[
            new_column_name
        ] = df_table_by_supergroup_question_response.groupby(
            self.pivot_table_index_columns + ["column_question"]
        )[
            column_to_sum_name
        ].transform(
            "sum"
        )
        return df_table_by_supergroup_question_response

    def calc_suppress_column(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ) -> pd.DataFrame:
        already_has_supression = df_table_by_supergroup_question_response[
            "suppress"
        ].astype(bool)

        zero_respondents = (
            df_table_by_supergroup_question_response["supergroup_question_respondents"]
            == 0
        )

        df_table_by_supergroup_question_response.loc[
            zero_respondents & ~already_has_supression, "suppress",
        ] = self.respondents_zero_suppression_label

        low_number_of_respondents = df_table_by_supergroup_question_response[
            "supergroup_question_respondents"
        ].isin(params.LOW_NUMBERS_OF_RESPONDENTS_TO_SUPRESS_FOR)

        df_table_by_supergroup_question_response.loc[
            low_number_of_respondents & ~already_has_supression, "suppress",
        ] = params.RESPONDENTS_LOW_SUPPRESSION_LABEL

        return df_table_by_supergroup_question_response

    def calc_suppress_margin_of_error_column(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ) -> pd.DataFrame:
        df_table_by_supergroup_question_response["suppress_margin_of_error"] = np.where(
            df_table_by_supergroup_question_response["respondents"].isin([0, 1]),
            "[w]",
            "",
        )

        df_table_by_supergroup_question_response["suppress_margin_of_error"] = np.where(
            df_table_by_supergroup_question_response["suppress"].astype(bool),
            df_table_by_supergroup_question_response["suppress"],
            df_table_by_supergroup_question_response["suppress_margin_of_error"],
        )

        return df_table_by_supergroup_question_response

    def get_section_from_section_settings(
        self, section_settings: Type[SectionSettings]
    ) -> pd.DataFrame:
        return perform_stratification(
            df_questionnaire_by_person=self.get_df_questionnaire_by_person_for_section(
                section_settings
            ),
            est_population_by_subgroup=self.get_est_population_by_subgroup_for_section(
                section_settings
            ),
            supergroup_columns=self.get_supergroup_columns(section_settings),
            subgroup_within_supergroup_columns=self.subgroup_within_supergroup_columns,
            discrete_column_name=section_settings.column_question,
        ).pipe(self.format_section, section_settings)

    def get_df_questionnaire_by_person_for_section(
        self, section_settings: Type[SectionSettings]
    ) -> pd.DataFrame:
        """This function is here in case a subclass needs to use a different df_questionnaire_by_person for each section"""
        return self.data_needed_for_table_creation.df_questionnaire_by_person

    def get_est_population_by_subgroup_for_section(
        self, section_settings: Type[SectionSettings],
    ):
        population_by_la_stratum_for_section = self.get_population_by_la_stratum_for_section(
            section_settings
        )

        easy_read_weight_type_to_use = self.get_easy_read_weight_type_to_use(
            section_settings
        )

        if easy_read_weight_type_to_use in ["Std", "ER"]:
            is_easy_read = easy_read_weight_type_to_use == "ER"
            return self.get_est_population_by_subgroup_with_calculated_arguments(
                population_by_la_stratum_for_section,
                section_settings,
                extra_demographics_to_get=["is_easy_read"],
            )[is_easy_read]
        else:
            return self.get_est_population_by_subgroup_with_calculated_arguments(
                population_by_la_stratum_for_section, section_settings
            )

    def get_all_table_sections_from_setting_combinations(self) -> list[pd.DataFrame]:
        return [
            self.get_section_from_section_settings(sections_setting)
            for sections_setting in self.section_settings_combinations
        ]

    def format_section(
        self, section: pd.DataFrame, section_settings: Type[SectionSettings]
    ):
        return section.rename(
            columns={"discrete": "column_question", "response": "column_response"}
        ).assign(suppress="")

    def get_population_by_la_stratum_for_section(
        self, section_settings: Type[SectionSettings]
    ) -> pd.Series:
        return (
            self.data_needed_for_table_creation.population_2c_by_la_stratum
            if self.use_population_2c(section_settings)
            else self.data_needed_for_table_creation.population_by_la_stratum
        )

    def get_est_population_by_subgroup_with_calculated_arguments(
        self,
        population_to_use_by_la_stratum: pd.Series,
        section_settings: Type[SectionSettings],
        extra_demographics_to_get: list[str] = [],
    ):
        full_demographics_to_get = (
            extra_demographics_to_get
            + self.get_demographic_columns_to_split_est_population_by(section_settings)
        )

        if len(full_demographics_to_get) == 0:
            return population_to_use_by_la_stratum

        return get_est_population_for_demographic_subgroups(
            full_demographics_to_get,
            section_settings.column_question_er_info.base,
            self.data_needed_for_table_creation.df_questionnaire_by_person,
            population_to_use_by_la_stratum,
        )

    def pivot(
        self, df_table_by_supergroup_question_response: pd.DataFrame, value_column: str
    ) -> pd.DataFrame:
        return df_table_by_supergroup_question_response.pivot(
            index=self.pivot_table_index_columns,
            columns=["column_question", "column_response"],
            values=value_column,
        )

    def get_respondents_df(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        column_to_select: str,
    ) -> pd.DataFrame:
        return (
            df_table_by_supergroup_question_response.groupby(
                self.pivot_table_index_columns + ["column_question"]
            )[column_to_select]
            .first()
            .unstack()
        )

    def add_respondents_columns_to_pivotted_df(
        self,
        df_table_by_supergroup: pd.DataFrame,
        df_table_by_supergroup_question_response: pd.DataFrame,
        column_to_select: Union[str, Literal[None]],
    ) -> pd.DataFrame:
        if not column_to_select:
            return df_table_by_supergroup

        df_respondents_by_supergroup = self.get_respondents_df(
            df_table_by_supergroup_question_response, column_to_select
        )
        respondents_index_that_defines_new_columns = pd.MultiIndex.from_product(
            [df_respondents_by_supergroup.columns, ["Respondents"]]
        )
        df_table_by_supergroup[
            respondents_index_that_defines_new_columns
        ] = df_respondents_by_supergroup
        return df_table_by_supergroup

    def round_percentage_table_by_supergroup(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        is_respondent_by_column = (
            df_table_by_supergroup.columns.get_level_values(1) == "Respondents"
        )
        df_table_by_supergroup.loc[
            :, ~is_respondent_by_column
        ] = df_table_by_supergroup.loc[:, ~is_respondent_by_column].round(1)
        if is_respondent_by_column.any():
            df_table_by_supergroup.loc[:, (slice(None), "Respondents")] = round_to_five(
                df_table_by_supergroup.loc[:, (slice(None), "Respondents")]
            )
        return df_table_by_supergroup

    def create_generic_pivotted_table(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        value_column: str,
        column_to_select_for_respondents: Union[str, Literal[None]],
    ) -> pd.DataFrame:
        return (
            df_table_by_supergroup_question_response.pipe(
                self.pivot, value_column=value_column
            )
            .pipe(
                self.add_respondents_columns_to_pivotted_df,
                df_table_by_supergroup_question_response,
                column_to_select=column_to_select_for_respondents,
            )
            .pipe(self.combine_rows_and_columns_in_pivotted)
            .pipe(self.order_rows_and_columns_in_pivotted)
        )

    def combine_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        return df_table_by_supergroup.pipe(
            combine_multiple_choice, params.get_multi_choice_questions_with_exclude()
        )

    def order_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        respondents_column_exists = (
            "Respondents" in df_table_by_supergroup.columns.get_level_values(1)
        )

        column_ordering_to_use = (
            params.get_stratified_pivot_tables_column_order_with_respondents()
            if respondents_column_exists
            else params.get_stratified_pivot_tables_column_order_without_respondents()
        )

        assert df_table_by_supergroup.shape == (
            len(self.pivot_table_index_order),
            len(column_ordering_to_use),
        ), f"""
The order_rows_and_columns_in_pivotted method would remove rows or columns!
This means that the rows and/or columns defined in params do not contain all the rows and columns in the true DataFrame

DataFrame shape = {df_table_by_supergroup.shape}
self.pivot_table_index_order length = {len(self.pivot_table_index_order)}
column_ordering_to_use = {len(column_ordering_to_use)}

Symm diff of columns = {pd.MultiIndex.from_tuples(column_ordering_to_use).symmetric_difference(df_table_by_supergroup.columns)}
Symm diff of rows = {(pd.MultiIndex.from_tuples if type(self.pivot_table_index_order[0]) == tuple else pd.Index)(self.pivot_table_index_order).symmetric_difference(df_table_by_supergroup.index)}
"""

        return df_table_by_supergroup.loc[
            self.pivot_table_index_order, column_ordering_to_use,
        ]

    def pre_pivot_format_table_by_supergroup_question_response(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return (
            df_table_by_supergroup_question_response.copy()
            .pipe(self.apply_rounding)
            .pipe(self.apply_suppression)
        )

    def create_percentage_table_by_supergroup(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return self.create_generic_pivotted_table(
            df_table_by_supergroup_question_response,
            value_column="percentage",
            column_to_select_for_respondents="supergroup_question_respondents",
        )

    def create_est_population_table_by_supergroup(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return self.create_generic_pivotted_table(
            df_table_by_supergroup_question_response,
            value_column="est_population",
            column_to_select_for_respondents="supergroup_population",
        )

    def create_margin_of_error_table_by_supergroup(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return self.create_generic_pivotted_table(
            df_table_by_supergroup_question_response,
            value_column="margin_of_error",
            column_to_select_for_respondents=None,
        )

    def are_columns_deleted_after_reordering(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        expected_column_order: list[str],
    ):
        is_columns_deleted_after_reordering = len(expected_column_order) != len(
            df_table_by_supergroup_question_response.columns
        )
        assert not (
            is_columns_deleted_after_reordering
        ), f"There were columns that were accidentally deleted when reordering the DataFrame. expected column order: {expected_column_order} | actual column order {list(df_table_by_supergroup_question_response.columns)} "

    def format_auxiliary_table_output(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        new_column_ordering = (
            self.pivot_table_index_columns + params.AUXILIARY_COLUMNS_TO_OUTPUT
        )

        self.are_columns_deleted_after_reordering(
            df_table_by_supergroup_question_response, new_column_ordering
        )

        df_table_by_supergroup_question_response_reordered = df_table_by_supergroup_question_response[
            new_column_ordering
        ]

        return df_table_by_supergroup_question_response_reordered

    def combine_multiple_choice_auxiliary(
        self, df_by_supergroup_question_response: pd.DataFrame
    ):
        return df_by_supergroup_question_response.pipe(
            combine_multiple_choice_auxiliary_utility,
            question_column="column_question",
            response_column="column_response",
            multichoice_questions=params.get_multi_choice_questions_with_exclude(),
        )

    def replace_single_digit_questions_with_double_digit(
        self, df_by_supergroup_question_response: pd.DataFrame
    ):
        df_by_supergroup_question_response[
            "column_question"
        ] = df_by_supergroup_question_response["column_question"].replace(
            params.QUESTION_DOUBLE_DIGIT_FORMAT
        )

        return df_by_supergroup_question_response

    def make_column_0_where_suppressed(
        self, df_by_supergroup_question_response: pd.DataFrame, column_name: str
    ) -> pd.DataFrame:
        df_by_supergroup_question_response[column_name] = pd.to_numeric(
            df_by_supergroup_question_response[column_name], errors="coerce"
        ).fillna(0)

        return df_by_supergroup_question_response

    def choose_power_bi_columns_to_output(
        self, df_by_supergroup_question_response: pd.DataFrame
    ):
        columns_to_output = self.pivot_table_index_columns + [
            "column_question",
            "column_response",
            "percentage",
            "margin_of_error",
            "supergroup_question_respondents",
        ]
        return df_by_supergroup_question_response[columns_to_output]

    def create_power_bi_table(
        self, df_table_by_supergroup_question_response: pd.DataFrame
    ):
        return (
            df_table_by_supergroup_question_response.pipe(
                self.combine_multiple_choice_auxiliary
            )
            .pipe(self.replace_single_digit_questions_with_double_digit)
            .pipe(self.make_column_0_where_suppressed, column_name="percentage")
            .pipe(self.make_column_0_where_suppressed, column_name="margin_of_error")
            .pipe(
                self.make_column_0_where_suppressed,
                column_name="supergroup_question_respondents",
            )
            .pipe(self.choose_power_bi_columns_to_output)
        )

