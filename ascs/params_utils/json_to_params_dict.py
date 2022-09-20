import json
from pathlib import Path
from typing import Any, Union


def load_params_dict_from_json_file(file_path: Union[str, Path]):
    uncleaned_params_dict = load_uncleaned_params_dict_from_file(file_path)
    return clean_params_dict(uncleaned_params_dict)


def load_uncleaned_params_dict_from_file(file_path: Union[str, Path]):
    with open(file_path) as params_file:
        return json.load(params_file)


def clean_params_dict(params_dict: dict) -> dict:
    do_all_list_of_tuples_conversions(params_dict)
    do_all_dictionary_keys_to_integer_conversions(params_dict)
    return params_dict


def do_all_list_of_tuples_conversions(params_dict: dict) -> None:
    for param_name in [
        "STRATIFIED_BY_DEMOGRAPHIC_CORRECT_ROW_ORDER",
        "STRATIFIED_BY_RESPONSE_CORRECT_ROW_ORDER",
    ]:
        params_dict[param_name] = convert_list_of_lists_to_list_of_tuples(
            params_dict[param_name]
        )


def do_all_dictionary_keys_to_integer_conversions(params_dict: dict) -> dict:
    params_dict["DEMOGRAPHICS_CONVERSIONS"] = convert_demographic_conversion_dict(
        params_dict["DEMOGRAPHICS_CONVERSIONS"]
    )
    params_dict["ASCOF_CONVERSIONS"] = [
        {
            **simple_conversion_dict,
            "CONVERSION": convert_dictionary_keys_to_integers(
                simple_conversion_dict["CONVERSION"]
            ),
        }
        for simple_conversion_dict in params_dict["ASCOF_CONVERSIONS"]
    ]
    return params_dict


def convert_demographic_conversion_dict(
    conversion_dict: dict[str, dict[str, str]]
) -> dict[str, dict[int, str]]:
    for conversion_name, conversion in conversion_dict.items():
        conversion_dict[conversion_name] = convert_dictionary_keys_to_integers(
            conversion
        )
    return conversion_dict


def convert_dictionary_keys_to_integers(json_dict: dict[str, Any]) -> dict[int, Any]:
    return {int(key): value for key, value in json_dict.items()}


def convert_list_of_lists_to_list_of_tuples(list_of_lists: list[list]) -> list[tuple]:
    return [tuple(element) for element in list_of_lists]
