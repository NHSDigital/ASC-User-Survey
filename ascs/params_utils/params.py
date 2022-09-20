from pathlib import Path
from typing import Union
from typed_params import BaseModel
from ascs.input_data.load_data_returns.data_return_config import DataReturnParams
from ascs.input_data.preprocess_questionnaire.ascof_config import SimpleAscofConversion
from ascs.output_to_excel.excel_config import ExcelConfig
from ascs.params_utils.json_to_params_dict import load_params_dict_from_json_file
from ascs.params_utils.params_transformations import (
    add_exclude_to_multichoice_questions,
    column_name_is_a_question_column,
    get_excluded_question_columns_pre_multichoice_merge,
    get_grouped_demographic_column_by_readable_name,
    get_grouped_demographic_column_by_readable_name_table_6,
    get_question_responses_and_respondents_list_of_tuples,
    get_question_responses_no_respondents_list_of_tuples,
    get_questions_with_all_suffixes,
    get_expanded_multichoice_list,
)


def get_params_from_file(file_path: Union[str, Path]):
    params_dict = load_params_dict_from_json_file(file_path)
    return Params(params_dict)


class Params(BaseModel):
    PUBLICATION_YEAR: str
    TEST_ANNEX_TABLES_FILE_PATH: str
    OUTPUT_ANNEX_TABLE_FILE_NAME: str
    TEMPLATE_ANNEX_TABLE_FILE_PATH: str
    DATA_RETURNS_DIRECTORY: str

    EXCEL_HORIZONTAL_GAP_SIZE_CONFIG_BY_NAME: dict[str, ExcelConfig]
    EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME: dict[str, ExcelConfig]
    EXCEL_NO_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME: dict[str, ExcelConfig]

    LA_CODE_WHITELIST: list[Union[str, int]]

    RESPONSE_RESPONDED_TO_SURVEY: int
    PRIMARY_SUPPORT_REASON_LEARNING_DISABILITY: int
    SUBQUESTION_A_INDEX: int
    ERRONEOUS_INPUT_VALUE: int
    ANSWERED_YES_TO_SUBQUESTION_RESPONSE: int
    ANSWERED_NO_TO_SUBQUESTION_RESPONSE: int

    QUESTIONAIRE_DATA_PATH: str
    ELIGIBLE_POPULATION_DATA_PATH: str

    STRATUM_COLUMN_NAMES: list[str]
    STRATUM_COLUMN_NAMES_SAMPLES: list[str]
    IDENTIFIER_COLUMNS_FOR_SUPPRESSED_QUESTIONNAIRE_CSV: list[str]
    COLUMNS_TO_SUPPRESS_IN_QUESTIONNAIRE_CSV: list[str]
    QUESTIONNAIRE_CSV_MAX_SIZE_OF_GROUP_TO_SUPPRESS: int
    COLUMNS_TO_SUPPRESS_IN_ANNEX_TABLE: list[str]

    ANNEX_TABLE_4_COLUMN_ORDER: list[str]
    ANNEX_TABLE_4_QUESTIONS_TO_COUNT: list[str]

    TYPICAL_QUESTIONS_LIST: list[str]
    COLUMNS_TO_SHOW_IN_SUPPRESSED_QUESTIONNAIRE_CSV: list[str]
    AUXILIARY_COLUMNS_TO_OUTPUT: list[str]

    QUESTIONS_AND_VALUES_TO_EXCLUDE: dict[str, int]
    MULTIPLE_CHOICE_QUESTIONS: dict[str, list[str]]
    MULTIPLE_CHOICE_QUESTIONS_TO_EXCLUDE: dict[str, dict[str, Union[str, int]]]

    EASY_READ_QUESTIONS: list[str]
    EASY_READ_QUESTIONNAIRE_TYPES: list[int]
    DEMOGRAPHICS_CONVERSIONS: dict[str, dict[str, str]]
    AGE_GROUP_BINS_START_AGES: list[int]
    EASY_READ_COLUMN_ENDINGS: list[str]

    LA_CODE_LIST_BY_AVERAGE_GROUP_NAME: dict[str, list[Union[int, str]]]
    TABLE6_CORRECT_ROW_ORDER: list[list[str, str]]
    STRATIFIED_BY_LA_CORRECT_ROW_ORDER: list[int]
    STRATIFIED_BY_DEMOGRAPHIC_CORRECT_ROW_ORDER: list[list[str, str]]
    STRATIFIED_BY_RESPONSE_CORRECT_ROW_ORDER: list[list[str, Union[str, int]]]
    STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION: dict[str, list[int]]
    ALL_LA_CODES: list[int]
    POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE: dict[str, list[int]]
    POSSIBLE_RESPONSES_BY_QUESTION_ANNEX_3_ROWS: dict[str, list[int]]
    DEMOGRAPHIC_VALUES_BY_DEMOGRAPHIC: dict[str, list[str]]

    LOW_NUMBERS_OF_RESPONDENTS_TO_SUPRESS_FOR: list[int]
    RESPONDENTS_LOW_SUPPRESSION_LABEL: str
    RESPONDENTS_ZERO_SUPRESSION_LABEL_STANDARD: str
    RESPONDENTS_ZERO_SUPRESSION_LABEL_BY_LA: str

    ACCEPTED_VALUES_STANDARD_QUESTIONS: list[int]
    ACCEPTED_VALUES_EASY_READ_QUESTIONS: list[int]
    MULTICHOICE_SUBQUESTIONS_ALLOWED_VALUES: list[int]

    QUESTION_DOUBLE_DIGIT_FORMAT: dict[str, str]

    VALIDATION_COLUMNS_THAT_SHOULD_BE_NO_FOR_NON_RESPONDENTS: list[str]
    DATA_RETURN: DataReturnParams
    ASCOF_CONVERSIONS: list[SimpleAscofConversion]

    def run_validations(self):
        self.check_column_responses_by_question_is_in_order()
        self.check_la_codes_are_consistent()
        self.check_ascof_conversion_question_responses_are_consistent()

    def check_column_responses_by_question_is_in_order(self):
        for (
            question,
            possible_responses,
        ) in self.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION.items():
            previous = -float("inf")
            for response in possible_responses:
                if type(response) == str:
                    response = ord(response)
                assert (
                    response >= previous
                ), f"""
    In params.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION
    for question {question}
    The list of responses is out of order
    {possible_responses}
    """
                previous = response

    def check_la_codes_are_consistent(self):
        """
        Every LA code in ALL_LA_CODES should be in STRATIFIED_BY_LA_CORRECT_ROW_ORDER
        If it is not then it is a sign that someone has missed something in the params.
        """
        all_la_codes_set = set(self.ALL_LA_CODES)
        stratified_by_la_correct_row_order_set = set(
            self.STRATIFIED_BY_LA_CORRECT_ROW_ORDER
        )
        difference = all_la_codes_set.difference(stratified_by_la_correct_row_order_set)
        assert (
            len(difference) == 0
        ), f"""
        params.ALL_LA_CODES and params.STRATIFIED_BY_LA_CORRECT_ROW_ORDER does not match!
        Elements in ALL_LA_CODES that are not in STRATIFIED_BY_LA_CORRECT_ROW_ORDER
        {difference}
        """

    def check_ascof_conversion_question_responses_are_consistent(self):
        for simple_ascof_conversion in self.ASCOF_CONVERSIONS:
            ascof_conversions_questions_responses = list(
                simple_ascof_conversion.CONVERSION.keys()
            )
            expected_question_responses = self.POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE[
                simple_ascof_conversion.QUESTION_COLUMN
            ]
            assert (
                expected_question_responses == ascof_conversions_questions_responses
            ), f"""
            params.ASCOF_CONVERSIONS and params.POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE do not match!
            The order must also match!
            For ASCOF_CONVERSIONS - score {simple_ascof_conversion.SCORE_NAME} - column - {simple_ascof_conversion.QUESTION_COLUMN}
            ASCOF_CONVERSIONS value: {ascof_conversions_questions_responses}
            POSSIBLE_RESPONSES_BY_QUESTION_AUX_TABLE value: {expected_question_responses}
            """

    def get_easy_read_expanded_questions(self) -> list[str]:
        return get_questions_with_all_suffixes(
            self.EASY_READ_QUESTIONS, self.EASY_READ_COLUMN_ENDINGS
        )

    def get_expanded_multi_choice_list_without_excluded(self) -> list[str]:
        """
        Gets a list of all the columns of the multichoice subquetions
        """
        return get_expanded_multichoice_list(self.MULTIPLE_CHOICE_QUESTIONS)

    def get_questions_without_excluded_questions(self) -> list[str]:
        return [
            *self.get_easy_read_expanded_questions(),
            *self.TYPICAL_QUESTIONS_LIST,
            *self.get_expanded_multi_choice_list_without_excluded(),
        ]

    def get_all_question_columns_pre_multichoice_merge(self) -> list[str]:
        return (
            self.get_questions_without_excluded_questions()
            + self.get_excluded_question_columns_pre_multichoice_merge()
        )

    def get_multi_choice_questions_with_exclude(self):
        return add_exclude_to_multichoice_questions(
            self.MULTIPLE_CHOICE_QUESTIONS, self.MULTIPLE_CHOICE_QUESTIONS_TO_EXCLUDE
        )

    def get_stratified_pivot_tables_column_order_with_respondents(self):
        return get_question_responses_and_respondents_list_of_tuples(
            self.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION
        )

    def get_stratified_pivot_tables_column_order_without_respondents(self):
        return get_question_responses_no_respondents_list_of_tuples(
            self.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION
        )

    def get_excluded_question_columns_pre_multichoice_merge(self) -> list[str]:
        return get_excluded_question_columns_pre_multichoice_merge(
            self.QUESTIONS_AND_VALUES_TO_EXCLUDE,
            self.MULTIPLE_CHOICE_QUESTIONS_TO_EXCLUDE,
            self.MULTIPLE_CHOICE_QUESTIONS,
        )

    def get_grouped_demographic_column_by_readable_name(self) -> dict[str, str]:
        return get_grouped_demographic_column_by_readable_name(
            self.DEMOGRAPHICS_CONVERSIONS
        )

    def get_grouped_demographic_column_by_readable_name_table_6(self) -> dict[str, str]:
        return get_grouped_demographic_column_by_readable_name_table_6(
            self.DEMOGRAPHICS_CONVERSIONS
        )

    def get_input_columns_that_should_be_null_for_non_respondents_for_validations(self):
        question_columns = [
            column_name
            for column_name in self.DATA_RETURN.NEW_COLUMN_NAMES_BY_EXPECTED_COLUMN_SUBSTRING.values()
            if column_name_is_a_question_column(column_name)
        ]
        return question_columns
