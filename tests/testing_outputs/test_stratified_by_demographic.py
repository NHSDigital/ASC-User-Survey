import pytest
import numpy as np
from tests.testing_outputs.test_utilities import check_supression, get_actual
from ascs import params


def test_annex_table2_rows_columns_correct(annex_table2):
    assert (
        annex_table2["2a"].index.to_list()
        == params.STRATIFIED_BY_DEMOGRAPHIC_CORRECT_ROW_ORDER
    )
    assert (
        annex_table2["2a"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )
    assert (
        annex_table2["2b"].index.to_list()
        == params.STRATIFIED_BY_DEMOGRAPHIC_CORRECT_ROW_ORDER
    )
    assert (
        annex_table2["2b"].columns.to_list()
        == params.get_stratified_pivot_tables_column_order_with_respondents()
    )


@pytest.mark.parametrize(
    "table_str,row,question,supress_str",
    [
        ("2a", ("MethodCollection", "Face-to-face interview"), "q3b", "[w]"),
        ("2a", ("MethodCollection", "Face-to-face interview"), "q2c", "[w]"),
        ("2a", ("Gender", "Other"), "q1Std", "[c]"),
        ("2b", ("Gender", "Other"), "q1Std", "[c]"),
        ("2b", ("PrimarySupportReason", "Mental Health Support"), "q1ER", "[c]"),
        ("2b", ("Translated", "Yes"), "q19", "[w]"),
    ],
)
def test_annex_2_supression(table_str, row, question, supress_str, annex_table2):
    check_supression(table_str, row, question, supress_str, annex_table2)


@pytest.mark.parametrize(
    "table,row,question,expected",
    [
        # 2a normal
        ("2a", ("Gender", "Male"), "q3a", [36.9, 44.2, 15.1, 3.9, 2825]),
        ("2a", ("Gender", "Female"), "q3a", [35.5, 43.5, 16.2, 4.8, 3665]),
        ("2a", ("RHC", "Autism"), "q3a", [33.4, 50.0, 12.0, 4.6, 440]),
        ("2a", ("RHC", "Asperger"), "q3a", [40.8, 44.9, 10.7, 3.5, 70]),
        # 2a ER
        (
            "2a",
            ("Gender", "Male"),
            "q1Std",
            [29.4, 32.3, 26.6, 6.4, 2.2, 1.2, 1.9, 1715],
        ),
        ("2a", ("Gender", "Male"), "q1ER", [77.8, 16.7, 3.9, 1.4, 0.1, 1110]),
        ("2a", ("Gender", "Male"), "q1Comb", [66.9, 23.4, 5.6, 1.9, 2.1, 2830]),
        # 2a multi choice
        ("2a", ("Gender", "Male"), "q20", [26.0, 8.6, 67.0, 2640]),
        # 2a age
        ("2a", ("Age", "18-24"), "q1Std", [29.6, 22.4, 32.0, 7.4, 0, 8.0, 0.6, 60]),
        # 2a combined demo column
        ("2a", ("Ethnicity", "White"), "q3a", [36.4, 43.9, 15.5, 4.2, 5525]),
        # 2a 2c
        ("2a", ("Ethnicity", "White"), "q2c", [68.5, 24.1, 7.4, 2920]),
        # 2b normal
        ("2b", ("Gender", "Male"), "q3a", [9610, 11530, 3930, 1010, 26090]),
        ("2b", ("Gender", "Female"), "q3a", [12850, 15760, 5880, 1760, 36240]),
        # 2b ER
        (
            "2b",
            ("Gender", "Male"),
            "q1Std",
            [5230, 5750, 4720, 1140, 390, 210, 340, 17780],
        ),
        ("2b", ("Gender", "Male"), "q1ER", [6570, 1410, 330, 120, 10, 8450]),
        ("2b", ("Gender", "Male"), "q1Comb", [17550, 6140, 1480, 510, 560, 26230]),
        # 2b multi choice
        ("2b", ("FullCost", "No"), "q19", [1200, 1050, 630, 2580]),
        # 2b 2c
        ("2b", ("FullCost", "No"), "q2c", [500, 170, 40, 710]),
    ],
)
def test_annex_table_2(table, row, question, expected, annex_table2):
    # Tests for the table, row and question that all the values are close
    # Note, close is within 10**-8 so it means very very close
    actual = get_actual(annex_table2[table], row, question)
    assert np.isclose(actual, expected).all(), f"EXPECTED: {expected}, ACTUAL: {actual}"


def test_auxilliary_2(annex_table2):
    expected_columns = [
        "demographic",
        "demographic_value",
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
    actual_columns = list(annex_table2["2_auxilliary"])

    assert expected_columns == actual_columns

    assert len(annex_table2["2_auxilliary"]) == 10919
