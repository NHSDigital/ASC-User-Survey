from datetime import datetime
import pathlib
import pandas as pd
import numpy as np
import os
from ascs.input_data.load_data_returns.data_return_config import LoadedDataReturns
from ascs.input_data.checkpoint import checkpoint_file_handler
from ascs.input_data.checkpoint.checkpoint_config import (
    LOADING_BY_ERROR_KEY,
    QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY,
)
from freezegun import freeze_time


@freeze_time("2022-08-09 12:00:00")
def test_save_data_return_checkpoint(tmp_path: pathlib.Path):
    df_questionnaire_unclean_by_person_to_save = pd.DataFrame(
        {"col_1": [1, 2, 3, 4], "col_2": [5, 6, 7, 8]}
    )
    df_loading_error_by_file_to_save = pd.DataFrame(
        {"col_3": [9, 10, 11, 12], "col_4": [13, 14, 15, 16]}
    )
    checkpoint_data_to_save = LoadedDataReturns(
        df_questionnaire_unclean_by_person_to_save, df_loading_error_by_file_to_save
    )

    checkpoint_file_handler.save_data_return_checkpoint(
        checkpoint_data_to_save, tmp_path
    )

    checkpoint_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h5"
    df_questionnaire_unclean_by_person_loaded = pd.read_hdf(
        tmp_path / checkpoint_filename, key=QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY,
    )
    df_loading_error_by_file_loaded = pd.read_hdf(
        tmp_path / checkpoint_filename, key=LOADING_BY_ERROR_KEY
    )

    assert len(os.listdir(tmp_path)) == 1
    pd.testing.assert_frame_equal(
        df_questionnaire_unclean_by_person_loaded,
        df_questionnaire_unclean_by_person_to_save,
    )
    pd.testing.assert_frame_equal(
        df_loading_error_by_file_loaded, df_loading_error_by_file_to_save
    )


def test_load_data_returns_from_checkpoint(tmp_path: pathlib.Path):
    df_questionnaire_unclean_by_person_to_save = pd.DataFrame(
        {"string_column": ["a", "b", "c", "d"], "number_column": [1, 2, 3, 4]}
    )
    df_loading_error_by_file_to_save = pd.DataFrame(
        {
            "boolean_column": [True, True, False, False],
            "float_column": [1.1, 2.2, 3.3, np.nan],
        }
    )

    filename = "test.h5"
    df_questionnaire_unclean_by_person_to_save.to_hdf(
        tmp_path / filename, key=QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY
    )
    df_loading_error_by_file_to_save.to_hdf(
        tmp_path / filename, key=LOADING_BY_ERROR_KEY
    )

    loaded_data_returns = checkpoint_file_handler.load_data_returns_from_checkpoint(
        str(tmp_path / filename)
    )

    pd.testing.assert_frame_equal(
        loaded_data_returns.df_questionnaire_unclean_by_person,
        df_questionnaire_unclean_by_person_to_save,
    )
    pd.testing.assert_frame_equal(
        loaded_data_returns.df_loading_error_by_file, df_loading_error_by_file_to_save
    )
