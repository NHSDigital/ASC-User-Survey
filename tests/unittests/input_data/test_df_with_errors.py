import pandas as pd
from ascs.input_data.df_with_errors import DFWithErrors


def test_run_transformer_on_df():
    df_errs_in = DFWithErrors(df="pretend DataFrame", error_dfs=["error 1"])

    def transformer(fake_df, some_arg, *, some_kwarg):
        assert fake_df == "pretend DataFrame"
        assert some_arg == "some arg"
        assert some_kwarg == "some kwarg"

        return "pretend return df"

    expected_df_errs = DFWithErrors(df="pretend return df", error_dfs=["error 1"])

    actual_df_errs = df_errs_in.run_transformer_on_df(
        transformer, "some arg", some_kwarg="some kwarg"
    )

    assert expected_df_errs == actual_df_errs


def test_run_validator_on_df():
    df_errs_in = DFWithErrors(df="pretend DataFrame", error_dfs=["error 1"])

    class FakeValidator:
        def run_check(self, fake_df, some_arg, *, some_kwarg):
            assert fake_df == "pretend DataFrame"
            assert some_arg == "some arg"
            assert some_kwarg == "some kwarg"

            return DFWithErrors(df="pretend return df", error_dfs=["error 2"])

    expected_df_errs = DFWithErrors(
        df="pretend return df", error_dfs=["error 1", "error 2"]
    )

    actual_df_errs = df_errs_in.run_validator_on_df(
        FakeValidator(), "some arg", some_kwarg="some kwarg"
    )

    assert expected_df_errs == actual_df_errs


def test_pipe():
    df_errs_in = DFWithErrors(df="pretend DataFrame", error_dfs=["error 1"])

    def pipe_function(df_errs_passed_to_function, some_arg, *, some_kwarg) -> str:
        assert df_errs_passed_to_function == df_errs_in
        assert some_arg == "some arg"
        assert some_kwarg == "some kwarg"

        return "some return"

    expected_return = "some return"

    actual_return = df_errs_in.pipe(pipe_function, "some arg", some_kwarg="some kwarg")

    assert expected_return == actual_return


def test_concatenate_errors_into_one_df__doesnt_error_with_no_errors():
    df_errs_in = DFWithErrors(df=None, error_dfs=[])

    expected_concatenated_errs = pd.DataFrame(
        [], columns=["LaCode", "PrimaryKey", "SerialNo", "message"]
    )

    actual_concatenated_errs = df_errs_in.concatenate_errors_into_one_df()

    pd.testing.assert_frame_equal(actual_concatenated_errs, expected_concatenated_errs)
