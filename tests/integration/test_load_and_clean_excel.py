from pathlib import Path
import pandas as pd
import pytest
from ascs.input_data.clean_validate_preprocess_questionnaire import (
    clean_validate_preprocess_questionnaire,
)
from ascs.input_data.df_with_errors import DFWithErrors
from ascs.input_data.load_data_returns.load_excel import (
    LoadedDataReturns,
    load_all_data_returns_from_excel,
)


this_directory = Path(__file__).parent


@pytest.fixture(scope="session")
def loaded_data_returns() -> LoadedDataReturns:
    all_data_returns = load_all_data_returns_from_excel(
        (this_directory / "fake_data_return_directory").resolve()
    )
    return all_data_returns


@pytest.fixture(scope="session")
def cleaned_and_preprocessed_data_returns(
    loaded_data_returns: LoadedDataReturns,
) -> DFWithErrors:
    clean_validate_preprocessed = clean_validate_preprocess_questionnaire(
        loaded_data_returns.df_questionnaire_unclean_by_person
    )

    return clean_validate_preprocessed


def test_cleaned_questionnaire(
    cleaned_and_preprocessed_data_returns: DFWithErrors,
) -> None:
    expected_cleaned_questionnaire = (
        pd.read_csv(
            this_directory
            / "fake_data_return_expected"
            / "cleaned_data_expected_test.csv"
        )
        .astype(cleaned_and_preprocessed_data_returns.df.dtypes.to_dict())
        .astype({"LaCode": str})
    )

    pd.testing.assert_frame_equal(
        cleaned_and_preprocessed_data_returns.df, expected_cleaned_questionnaire,
    )


def test_dq_validations_expected(
    cleaned_and_preprocessed_data_returns: DFWithErrors,
) -> None:
    expected_dq_validation_errors = pd.read_csv(
        this_directory
        / "fake_data_return_expected"
        / "dq_validation_errors_expected_test.csv"
    ).astype({"LaCode": str})

    pd.testing.assert_frame_equal(
        cleaned_and_preprocessed_data_returns.concatenate_errors_into_one_df(),
        expected_dq_validation_errors,
    )


def test_errors_loading_files(loaded_data_returns: LoadedDataReturns,) -> None:
    df_errors = loaded_data_returns.df_loading_error_by_file

    assert len(df_errors) == 3
    assert df_errors.columns.to_list() == ["file_path", "error_message"]

    assert "unacceptable_column_deleted" in df_errors.iloc[0]["file_path"]
    assert "expected a column like" in df_errors.iloc[0]["error_message"]

    assert "unacceptable_no_la_code" in df_errors.iloc[1]["file_path"]
    assert (
        df_errors.iloc[1]["error_message"]
        == "LA not selected (cell E3, Sign Off Sheet)"
    )

    assert "unacceptable_sheet_renamed" in df_errors.iloc[2]["file_path"]
    assert (
        df_errors.iloc[2]["error_message"]
        == "Expected worksheet called 'Service User Data' but couldn't find it - did you change a sheet name?"
    )
