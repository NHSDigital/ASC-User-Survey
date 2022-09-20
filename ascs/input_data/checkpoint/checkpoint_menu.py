from pathlib import Path
from ascs import params
import inquirer
import os
import logging

from ascs.input_data.load_data_returns.data_return_config import LoadedDataReturns
from ascs.input_data.load_data_returns.load_excel import (
    load_all_data_returns_from_excel,
)
from .checkpoint_config import CHECKPOINTS_DIRECTORY
from .checkpoint_file_handler import (
    load_data_returns_from_checkpoint,
    get_current_year_checkpoint_files,
)


def load_data_from_data_return_with_menu() -> LoadedDataReturns:
    if check_current_year_checkpoint_directory_exists() and want_to_load_checkpoint():
        checkpoint_file_to_use = select_checkpoint_to_load()
        return load_data_returns_from_checkpoint(checkpoint_file_to_use)
    else:
        logging.info("Loading questionnaire data (takes a while)")
        return load_all_data_returns_from_excel()


def select_checkpoint_to_load() -> str:
    checkpoint_files = get_current_year_checkpoint_files()

    print(
        f"\nCheckpoint files available in checkpoints/{params.PUBLICATION_YEAR} folder:\n"
    )
    for i, file in enumerate(checkpoint_files):
        print(f"{i+1} - {file}")
    print()

    checkpoint_index_to_use = (
        int(inquirer.text(message="Enter the number of the checkpoint you wish to use"))
        - 1
    )

    return checkpoint_files[checkpoint_index_to_use]


def check_current_year_checkpoint_directory_exists():
    if os.path.exists(CHECKPOINTS_DIRECTORY + params.PUBLICATION_YEAR):
        return True
    else:
        logging.info("No checkpoint files available!")
        return False


def want_to_load_checkpoint() -> bool:
    return bool(
        inquirer.confirm("Do you want to load from a checkpoint?", default=False)
    )

