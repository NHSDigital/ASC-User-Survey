import pytest

import pandas as pd
import numpy as np

from .utilities import get_actual, check_supression

from ascs import params


def test_annex_table1_5_rows_columns_correct(annex_table1_and_5):
    assert (
        annex_table1_and_5["1a"].index.to_list()
        == params.STRATIFIED_BY_LA_CORRECT_ROW_ORDER
    )
    assert (
        annex_table1_and_5["1a"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )
    assert (
        annex_table1_and_5["1b"].index.to_list()
        == params.STRATIFIED_BY_LA_CORRECT_ROW_ORDER
    )
    assert (
        annex_table1_and_5["1b"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )
    assert (
        annex_table1_and_5["5"].index.to_list()
        == params.STRATIFIED_BY_LA_CORRECT_ROW_ORDER
    )
    assert (
        annex_table1_and_5["5"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_without_respondents()
    )


@pytest.mark.parametrize(
    "table,row,question,expected",
    [
        # 1a normal
        ("1a", "211", "q3a", [38.7, 46.4, 11.0, 3.9, 495]),
        ("1a", "616", "q6a", [63.6, 26.9, 9.1, 0.4, 260]),
        # 1a ER
        ("1a", "211", "q1Std", [31.9, 31.7, 28.0, 4.8, 2.1, 0.6, 0.8, 295]),
        ("1a", "211", "q1ER", [74.5, 21.4, 4.1, 0, 0, 195]),
        ("1a", "211", "q1Comb", [66.7, 26.1, 4.6, 1.5, 1.0, 490]),
        ("1a", "916", "q1Std", [30.0, 34.0, 26.4, 5.8, 2.9, 0.7, 0.2, 415]),
        ("1a", "916", "q1ER", [80.1, 18.1, 1.2, 0.6, 0.0, 165]),
        ("1a", "916", "q1Comb", [67.6, 24.5, 4.8, 2.4, 0.7, 580]),
        # 1a multi choice
        ("1a", "727", "q19", [47.6, 41.6, 19.3, 375]),
        # 1a q2c
        ("1a", "219", "q2c", [70.6, 23.3, 6.1, 145]),
        # 1b normal
        ("1b", "211", "q3a", [1640, 1960, 470, 160, 4240]),
        ("1b", "616", "q6a", [1050, 440, 150, 10, 1640]),
        # 1b ER
        ("1b", "211", "q1Std", [970, 960, 850, 150, 60, 20, 20, 3030]),
        ("1b", "211", "q1ER", [900, 260, 50, 0, 0, 1200]),
        ("1b", "211", "q1Comb", [2830, 1110, 200, 60, 40, 4240]),
        ("1b", "916", "q1Std", [1120, 1270, 980, 220, 110, 20, 10, 3730]),
        ("1b", "916", "q1ER", [860, 190, 10, 10, 0, 1070]),
        ("1b", "916", "q1Comb", [3250, 1180, 230, 120, 30, 4800]),
        # 1b q2c
        ("1b", "211", "q2c", [1560, 450, 50, 2060]),
        # 1b multi choice
        ("1b", "219", "q22", [600, 850, 290, 680, 560, 260, 2030]),
        # 5
        # Note that we calculate the numbers with a different critical value
        # So these are not the same as the SAS numbers
        ("5", "219", "q1Std", [7.1, 6.8, 5.9, 2.6, 1.4, 1.4, 1.2]),
        ("5", "211", "q3a", [4.2, 4.3, 2.6, 1.5]),
        ("5", "211", "q2c", [5.3, 5.2, 1.8]),
        # Average Rows
        (
            "1a",
            "18 CASSR Average",
            "q1Std",
            [29.8, 34.7, 24.8, 6.0, 2.1, 1.5, 1.2, 4565],
        ),
        ("1a", "18 CASSR Average", "q5a", [67.0, 27.5, 4.2, 1.3, 6380]),
        ("1a", "18 CASSR Average", "q20", [25.9, 8.8, 67.0, 6080]),
        ("1a", "18 CASSR Average", "q2c", [68.2, 24.6, 7.2, 3520]),
        ("1b", "18 CASSR Average", "q2aER", [5660, 5780, 2880, 160, 60, 14540]),
        ("1b", "18 CASSR Average", "q13", [11530, 18410, 22980, 6850, 2570, 62340]),
        ("5", "18 CASSR Average", "q3a", [1.4, 1.5, 1.1, 0.7]),
    ],
)
def test_annex_table_1_and_5(table, row, question, expected, annex_table1_and_5):
    actual = get_actual(annex_table1_and_5[table], row, question)
    assert np.isclose(
        actual, expected
    ).all(), f"""
table: {table}
row: {row}
question: {question}
EXPECTED: {expected}
ACTUAL: {actual}
"""


@pytest.mark.parametrize(
    "table_str,row,question,supress_str",
    [
        ("1a", "316", "q5b", "[x]"),
        ("1a", "102", "q6a", "[x]"),
        ("1b", "111", "q1Std", "[x]"),
        ("1b", "803", "q5b", "[x]"),
    ],
)
def test_annex_1_supression(table_str, row, question, supress_str, annex_table1_and_5):
    check_supression(table_str, row, question, supress_str, annex_table1_and_5)


@pytest.mark.parametrize(
    "average_name,question,value_column,rounding,expected",
    [
        (
            "18 CASSR Average",
            "q1Std",
            "percentage",
            1,
            [29.8, 34.7, 24.8, 6.0, 2.1, 1.5, 1.2],
        ),
        ("18 CASSR Average", "q5a", "percentage", 1, [67.0, 27.5, 4.2, 1.3],),
        ("18 CASSR Average", "q2c", "percentage", 1, [68.2, 24.6, 7.2]),
        ("18 CASSR Average", "q3a", "margin_of_error", 1, [1.4, 1.5, 1.1, 0.7]),
        (
            "18 CASSR Average",
            "q2aER",
            "est_population",
            -1,
            [5660, 5780, 2880, 160, 60],
        ),
        (
            "18 CASSR Average",
            "q13",
            "est_population",
            -1,
            [11530, 18410, 22980, 6850, 2570],
        ),
    ],
)
def test_average_rows(
    average_name, question, value_column, rounding, expected, average_rows
):
    actual = average_rows.loc[
        (average_rows["average_name"] == average_name)
        & (average_rows["column_question"] == question),
        value_column,
    ].round(rounding)
    assert np.isclose(
        actual, expected
    ).all(), f"""
Average name: {average_name}
Question: {question}
Value column: {value_column}
Rounding: {rounding}
Actual: {actual}
Expected: {expected}
"""


@pytest.mark.parametrize(
    "row_name,question,expected",
    [
        (
            "211",
            ["q1Comb", "q2b", "q2c", "q3a", "q3b", "q4a", "q5a", "q22"],
            [97.2, 96.4, 95.3, 98, 96.6, 97.8, 96, 97.0],
        ),
        (
            "18 CASSR Average",
            ["total_response_rate", "q2b", "q2c", "q3a", "q3b", "q4a", "q5a", "q19",],
            [27.1, 95.5, 93.7, 97.0, 94.4, 97.5, 95.3, 93.5],
        ),
    ],
)
def test_annex4(row_name, question, expected, annex_table4):
    actual = annex_table4["4"].loc[row_name, question].astype(float)
    assert np.isclose(
        actual, expected,
    ).all(), f"EXPECTED: {expected}, ACTUAL: {actual}"


def test_annex6(annex_table6):
    actual = (
        annex_table6["6"]
        .loc[
            ("Gender", ["Male", "Female", "Other"]),
            ["Estimated Population of Demographic", "Percentage in Demographic"],
        ]
        .astype(float)
    )
    expected = [[26640, 42.7], [35700, 57.3], [10, 0]]
    assert np.isclose(
        actual, expected,
    ).all(), f"""
expected: {expected}
actual: {actual}
"""


def test_auxilliary_1(annex_table1_and_5):
    expected_columns = [
        "LaCode",
        "column_question",
        "column_response",
        "est_population",
        "percentage",
        "margin_of_error",
        "respondents",
        "supergroup_population",
        "supergroup_question_respondents",
        "suppress",
        "suppress_margin_of_error",
    ]
    actual_columns = list(annex_table1_and_5["1_auxilliary"])

    assert expected_columns == actual_columns

    assert len(annex_table1_and_5["1_auxilliary"]) == 27029


@pytest.mark.parametrize(
    "row,question,expected",
    [
        ("316", "q1Std", [None, None, None, None, None, "[w]", None]),
        ("718", "q1Std", [None, None, None, None, None, "[w]", "[w]"]),
        ("102", "q3a", ["[x]", "[x]", "[x]", "[x]"]),
        ("608", "q5b", ["[x]", "[x]"]),
    ],
)
def test_table5_suppression(row, question, expected, annex_table1_and_5):
    table5 = annex_table1_and_5["5"]
    expected = np.array(expected)
    actual = table5.loc[row, (question, slice(None))]
    actual_is_number = actual.apply(pd.api.types.is_number)
    expected_is_none = pd.isnull(expected)
    is_equal = expected == actual
    is_valid = is_equal | (actual_is_number & expected_is_none)
    assert is_valid.all(), f"""
    ACTUAL = {actual}
    Expected = {expected}
    is_valid = {is_valid}
    """
