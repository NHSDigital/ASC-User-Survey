from pathlib import Path
from datetime import datetime
from .checkpoint_config import (
    LOADING_BY_ERROR_KEY,
    QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY,
    CHECKPOINTS_DIRECTORY,
)
from ..load_data_returns.data_return_config import LoadedDataReturns
from ascs import params
import pandas as pd
import os


def save_data_return_checkpoint(
    checkpoint_data: LoadedDataReturns, path_to_save_to: Path
):
    if not Path.exists(path_to_save_to):
        os.mkdir(path_to_save_to)

    checkpoint_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h5"
    checkpoint_data.df_questionnaire_unclean_by_person.to_hdf(
        path_to_save_to / checkpoint_filename, key=QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY
    )
    checkpoint_data.df_loading_error_by_file.to_hdf(
        path_to_save_to / checkpoint_filename, key=LOADING_BY_ERROR_KEY,
    )


def load_data_returns_from_checkpoint(checkpoint_file_to_use: str) -> LoadedDataReturns:
    df_questionnaire_unclean_by_person = pd.read_hdf(
        checkpoint_file_to_use, key=QUESTIONNAIRE_UNCLEAN_BY_PERSON_KEY
    )
    df_loading_error_by_file = pd.read_hdf(
        checkpoint_file_to_use, key=LOADING_BY_ERROR_KEY
    )

    return LoadedDataReturns(
        df_questionnaire_unclean_by_person, df_loading_error_by_file
    )


def get_current_year_checkpoint_files() -> list[str]:
    current_year_checkpoints_directory = Path(
        CHECKPOINTS_DIRECTORY + params.PUBLICATION_YEAR
    )
    return [
        str(current_year_checkpoints_directory / file)
        for file in os.listdir(CHECKPOINTS_DIRECTORY + params.PUBLICATION_YEAR)
        if file.endswith(".h5")
    ]
