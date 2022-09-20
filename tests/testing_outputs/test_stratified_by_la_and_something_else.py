import pytest

from typing import Union

import pandas as pd


@pytest.mark.parametrize(
    "LaCode,demographic,demographic_value,column_question,column_response,percentage",
    [
        ("211", "Age", "18-24", "q1Comb", 2, 12.8),
        ("211", "Age", "18-24", "q1Comb", 1, 87.2),
        ("211", "Age", "18-24", "q1ER", 2, 14.3),
        ("211", "Age", "18-24", "q1ER", 1, 85.7),
        ("211", "Age", "25-34", "q1Comb", 3, 3.2),
        ("211", "Ethnicity", "White", "q1Comb", 4, 1.8),
    ],
)
def test_stratified_by_la_demographic(
    LaCode: Union[str, int],
    demographic: str,
    demographic_value: str,
    column_question: str,
    column_response: Union[str, int],
    percentage: float,
    stratified_by_la_demographic: dict[str, pd.DataFrame],
) -> None:
    aux_table = stratified_by_la_demographic["LA_and_Demographic_auxiliary"]
    row = aux_table.query(
        "LaCode == @LaCode & demographic == @demographic & demographic_value == @demographic_value & column_question == @column_question & column_response == @column_response"
    )

    assert row["percentage"].round(1).squeeze() == percentage


@pytest.mark.parametrize(
    "LaCode,row_question,row_response,column_question,column_response,percentage",
    [
        ("211", "q1Comb", 1, "q2aComb", 1, 42.1),
        ("211", "q1Comb", 1, "q2aComb", 2, 35.5),
        ("211", "q1Comb", 1, "q2aComb", 3, 18),
        ("211", "q1Comb", 1, "q2aComb", 4, 2.4),
        ("211", "q1Comb", 1, "q2aComb", 5, 2),
        ("211", "q1Comb", 1, "q2b", 2, 1.6),
    ],
)
def test_stratified_by_la_response(
    LaCode: Union[str, int],
    row_question: str,
    row_response: Union[str, int],
    column_question: str,
    column_response: Union[str, int],
    percentage: float,
    stratified_by_la_response: dict[str, pd.DataFrame],
) -> None:
    aux_table = stratified_by_la_response["LA_and_Response_auxiliary"]
    row = aux_table.query(
        "LaCode == @LaCode & row_question == @row_question & row_response == @row_response & column_question == @column_question & column_response == @column_response"
    )

    assert row["percentage"].round(1).squeeze() == percentage


def test_stratified_by_la_response_supresses_correctly(
    stratified_by_la_response: dict[str, pd.DataFrame]
) -> None:
    aux_table = stratified_by_la_response["LA_and_Response_auxiliary"]

    row = aux_table.query(
        "LaCode == 211 & row_question == 'q3a' & column_question == 'q3a'"
    )

    assert (row["suppress"] == "[z]").all()
