import pytest
from ascs.params_utils.params import Params, get_params_from_file


@pytest.fixture()
def params() -> Params:
    return get_params_from_file("./params_json/2020-21.json")


def test_check_column_responses_by_question_is_in_order(params: Params):
    params.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION = {
        "q1": [4, 5, 6],
        "q99": ["a", "b", "c"],
    }
    params.check_column_responses_by_question_is_in_order()

    with pytest.raises(AssertionError) as err_container:
        params.STRATIFIED_PIVOTTED_TABLES_COLUMN_RESPONSES_BY_QUESTION = {
            "q9": [1, 2, 3],
            "q10": [1, 3, 2],
            "q11": [1, 9, 19],
        }
        params.check_column_responses_by_question_is_in_order()

    assert "q10" in str(err_container.value)
    assert "[1, 3, 2]" in str(err_container.value)


def test_expanded_multichoice_list(params: Params):
    params.MULTIPLE_CHOICE_QUESTIONS = {"q12": ("a", "b", "c"), "q13": ("a", "b")}

    expected_out = ["q12a", "q12b", "q12c", "q13a", "q13b"]

    assert params.get_expanded_multi_choice_list_without_excluded() == expected_out
