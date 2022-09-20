from ascs.stratified_tables.stratified_by_response_tables import (
    get_question_easy_read_info,
    section_is_a_combination_of_questions_that_doesnt_make_sense,
    ByResponseSectionSettings,
)


def test_extract_question_easy_read_type():
    assert get_question_easy_read_info("q3a") == ("q3a", None)
    assert get_question_easy_read_info("q1Std") == ("q1", "Std")
    assert get_question_easy_read_info("q2Comb") == ("q2", "Comb")
    assert get_question_easy_read_info("q3ER") == ("q3", "ER")


def test_combination_needs_to_be_skipped():
    assert section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q3a", "q3a")
    )
    assert section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q1Std", "q1ER")
    )
    assert section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q1ER", "q2aStd")
    )
    assert not section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q3b", "q6b")
    )
    assert not section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q1ER", "q6b")
    )
    assert not section_is_a_combination_of_questions_that_doesnt_make_sense(
        ByResponseSectionSettings("q2aComb", "q1Comb")
    )
