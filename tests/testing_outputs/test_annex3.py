import pytest

import numpy as np

from .utilities import get_actual, check_supression

from ascs import params


def test_annex_table3_rows_columns_correct(annex_table3):
    assert (
        annex_table3["3a"].index.to_list()
        == params.STRATIFIED_BY_RESPONSE_CORRECT_ROW_ORDER
    )
    assert (
        annex_table3["3a"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )
    assert (
        annex_table3["3b"].index.to_list()
        == params.STRATIFIED_BY_RESPONSE_CORRECT_ROW_ORDER
    )
    assert (
        annex_table3["3b"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )


@pytest.mark.parametrize(
    "table_str,row,question,supress_str",
    [
        ("3a", ("q4a", 1), "q4a", "[z]"),
        ("3b", ("q1Std", 7), "q1Std", "[z]"),
        ("3a", ("q2aER", 3), "q2aComb", "[z]"),
        ("3b", ("q2aStd", 3), "q2aER", "[z]"),
        ("3b", ("q2c", 2), "q1ER", "[z]"),
        ("3a", ("q2aER", 5), "q2c", "[z]"),
        ("3a", ("q1ER", 5), "q22Excl", "[c]"),
        ("3b", ("q1ER", 5), "q22Excl", "[c]"),
    ],
)
def test_annex_3_supression(table_str, row, question, supress_str, annex_table3):
    check_supression(table_str, row, question, supress_str, annex_table3)


@pytest.mark.parametrize(
    "table,row,question,expected",
    [
        # 3a Normal
        ("3a", ("q2b", 1), "q3a", [37.4, 45.2, 13.9, 3.5, 5815]),
        ("3a", ("q2b", 1), "q3b", [93.3, 6.7, 5745]),
        # 3a ER
        ("3a", ("q1Std", 3), "q2aStd", [1.6, 9.5, 33.7, 42.4, 9.1, 2.7, 1.0, 1160]),
        ("3a", ("q1Std", 5), "q4a", [22.3, 51.8, 21.2, 4.8, 100]),
        ("3a", ("q2aER", 1), "q1ER", [92.2, 5.3, 1.5, 0.7, 0.3, 750]),
        ("3a", ("q2aER", 5), "q7a", [26.9, 52.8, 7.5, 12.9, 10]),
        ("3a", ("q2aComb", 4), "q1Comb", [39.5, 33.0, 12.5, 10.1, 4.9, 335]),
        ("3a", ("q2aComb", 2), "q5a", [68.2, 28.9, 2.1, 0.7, 2045]),
        ("3a", ("q6a", 1), "q1Std", [37.1, 36.3, 20.8, 3.2, 1.0, 0.5, 1.0, 2770]),
        ("3a", ("q6a", 3), "q1ER", [29.7, 28.3, 12.8, 29.2, 0.0, 20]),
        ("3a", ("q6a", 3), "q1Comb", [31.2, 30.8, 16.4, 12.0, 9.6, 255]),
        # 3a multi choice
        ("3a", ("q14a", 1), "q19", [45.2, 34.4, 27.4, 2545]),
        ("3a", ("q22", "c"), "q19", [53.8, 36.0, 19.8, 1435]),
        # 3a 2c
        ("3a", ("q22", "c"), "q2c", [72.0, 23.3, 4.6, 255]),
        ("3a", ("q2aStd", 2), "q2c", [81.8, 9.7, 8.5, 665]),
        # 3b Normal
        ("3b", ("q2b", 1), "q3a", [20750, 25090, 7740, 1960, 55540]),
        ("3b", ("q2b", 1), "q3b", [52650, 3770, 56420]),
        # 3b multi choice
        ("3b", ("q22", "d"), "q1Std", [4000, 4860, 3790, 730, 330, 180, 190, 14080]),
        ("3b", ("q2aER", 2), "q20", [1260, 630, 3890, 5670]),
        # 3b 2c
        ("3b", ("q22", "d"), "q2c", [6760, 2730, 690, 10180]),
    ],
)
def test_annex_table_3(table, row, question, expected, annex_table3):
    # Tests for the table, row and question that all the values are close
    # Note, close is within 10**-8 so it means very very close
    actual = get_actual(annex_table3[table], row, question)
    assert np.isclose(actual, expected).all(), f"EXPECTED: {expected}, ACTUAL: {actual}"


def test_auxilliary_3(annex_table3):
    expected_columns = [
        "row_question",
        "row_response",
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
    actual_columns = list(annex_table3["3_auxilliary"])

    assert expected_columns == actual_columns

    assert len(annex_table3["3_auxilliary"]) == 29535
