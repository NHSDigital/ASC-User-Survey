import pandas as pd
import pytest
from ascs.stratified_tables.base_stratified_tables import BaseStratifiedTables


class MockStratifiedTables(BaseStratifiedTables):
    def set_standard_attributes(self):
        pass

    def get_full_combination_of_supergroup_qustion_response_index(
        self, *args, **kwargs
    ):
        return pd.MultiIndex.from_product(
            [[211, 311], ["q1", "q2"]], names=["LaCode", "question"]
        )


def test_check_no_rows_will_be_lost_on_reindex__shows_error_when_rows_lost():

    mst = MockStratifiedTables(None)
    index_before_reindex = pd.MultiIndex.from_tuples(
        [(211, "q1"), (211, "q2"), (411, "q1")]
    )
    df_by_supergroup_question_response = pd.DataFrame([], index=index_before_reindex)

    with pytest.raises(AssertionError) as err:
        mst.check_no_rows_will_be_lost_on_reindex(df_by_supergroup_question_response)

    assert "411" in str(
        err.value
    ), "411 is the LaCode that is going to be lost, it should show in the error"
    assert "q1" in str(
        err.value
    ), "The row to be lost involves q1, this should also show in the error"
    assert "211" not in str(
        err.value
    ), "LaCode 211 is irrelevant to the error, this index would not be lost"


def test_check_no_rows_will_be_lost_on_reindex__doesnt_show_error_when_correct():
    mst = MockStratifiedTables(None)
    mst.get_full_combination_of_supergroup_qustion_response_index = lambda *args: pd.MultiIndex.from_product(
        [[211, 311], ["q1", "q2"]], names=["LaCode", "question"]
    )
    index_before_reindex = pd.MultiIndex.from_tuples([(311, "q2"), (211, "q1")])
    df_by_supergroup_question_response = pd.DataFrame([], index=index_before_reindex)

    mst.check_no_rows_will_be_lost_on_reindex(df_by_supergroup_question_response)


def test_calc_suppress_margin_of_error_column():
    df_in = pd.DataFrame(
        [[34, ""], [48, "[x]"], [1, ""], [0, "[a]"]],
        columns=["respondents", "suppress"],
    )

    df_expected = pd.DataFrame(
        [[34, "", ""], [48, "[x]", "[x]"], [1, "", "[w]"], [0, "[a]", "[a]"]],
        columns=["respondents", "suppress", "suppress_margin_of_error"],
    )

    df_actual = MockStratifiedTables(None).calc_suppress_margin_of_error_column(df_in)

    pd.testing.assert_frame_equal(df_actual, df_expected)


def test_check_no_rows_will_be_lost_on_column_reordering__shows_error_when_rows_lost():
    bst = MockStratifiedTables(None)
    df_by_supergroup_question_response = pd.DataFrame(
        [[1, 2, 3, 4]], columns=["a", "b", "c", "d"]
    )

    with pytest.raises(AssertionError):
        bst.are_columns_deleted_after_reordering(
            df_by_supergroup_question_response, ["a", "b"]
        )


def test_check_no_rows_will_be_lost_on_column_reordering__does_not_show_error_when_no_rows_lost():
    bst = MockStratifiedTables(None)
    df_by_supergroup_question_response = pd.DataFrame(
        [[1, 2, 3, 4]], columns=["a", "b", "c", "d"]
    )

    bst.are_columns_deleted_after_reordering(
        df_by_supergroup_question_response, ["a", "b", "d", "c"]
    )
