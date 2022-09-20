import pandas as pd
import pytest


def test_powerbi_output_puts_subquestion_letter_in_response_column(
    annex_table1_and_5: dict[str, pd.DataFrame]
) -> None:
    powerbi_table = annex_table1_and_5["1_power_bi"]

    assert "18 CASSR Average" in powerbi_table["LaCode"].values

    assert (
        "a"
        in powerbi_table.loc[
            powerbi_table["column_question"] == "q19", "column_response"
        ].values
    )


@pytest.mark.parametrize(
    "question,is_expected",
    [("q01Std", True), ("q03a", True), ("q3a", False), ("q19a", False),],
)
def test_powerbi_outputs(
    annex_table1_and_5: dict[str, pd.DataFrame], question: str, is_expected: bool
):
    powerbi_table = annex_table1_and_5["1_power_bi"]

    assert (question in powerbi_table["column_question"].values) == is_expected


@pytest.mark.parametrize("column", ["column_response", "row_response"])
def test_powerbi_output_puts_subquestion_letter_in_response_column_3(
    annex_table3: dict[str, pd.DataFrame], column: str
):
    powerbi_table = annex_table3["3_power_bi"]

    assert (
        "a"
        in powerbi_table.loc[powerbi_table["column_question"] == "q19", column].values
    )


@pytest.mark.parametrize(
    "value,column,is_expected",
    [
        ("q01Std", "column_question", True),
        ("q03a", "column_question", True),
        ("q3a", "column_question", False),
        ("q19a", "column_question", False),
        ("q01Std", "row_question", True),
        ("q03a", "row_question", True),
        ("q3a", "row_question", False),
        ("q19a", "row_question", False),
        ("18 CASSR Average", "row_response", True),
    ],
)
def test_powerbi_outputs_3(annex_table3, value, column, is_expected):
    powerbi_table = annex_table3["3_power_bi"]

    assert (value in powerbi_table[column].values) == is_expected
