import os
import inquirer
from ascs.params_utils.json_to_params_dict import load_params_dict_from_json_file
from ascs import params


PARAMS_DIRECTORY = "./params_json/"


def choose_which_params_file_to_use() -> None:
    params_files = [
        PARAMS_DIRECTORY + file
        for file in os.listdir(PARAMS_DIRECTORY)
        if file.endswith(".json")
    ]

    print("\nParams files available in params_json folder:\n")
    for i, file in enumerate(params_files):
        print(f"{i+1} - {file}")
    print()

    params_index_to_use = (
        int(inquirer.text(message="Enter the number of the params you wish to use")) - 1
    )
    params_file_to_use = params_files[params_index_to_use]

    params.set_params_from_params_dict(
        load_params_dict_from_json_file(params_file_to_use)
    )


def select_tables_to_run(tables_ids: list[str]) -> list[str]:
    want_to_run_all = inquirer.confirm("Do you want to run all tables?", default=True)

    if want_to_run_all:
        return tables_ids
    else:
        return [
            table_id
            for table_id in tables_ids
            if inquirer.confirm(f"Do you want to run {table_id}?", default=True)
        ]
