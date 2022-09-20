from ascs.params_utils.json_to_params_dict import (
    convert_demographic_conversion_dict,
    convert_list_of_lists_to_list_of_tuples,
    convert_dictionary_keys_to_integers,
    do_all_dictionary_keys_to_integer_conversions,
)


def test_do_all_dictionary_keys_to_integer_conversions():
    input_dict = {
        "DEMOGRAPHICS_CONVERSIONS": {
            "Gender": {"1": "Male", "2": "Female", "3": "Other"}
        },
        "ASCOF_CONVERSIONS": [
            {
                "SCORE_NAME": "1B",
                "QUESTION_COLUMN": "q3a",
                "CONVERSION": {"1": 1, "2": 1, "3": 2, "4": 2},
            }
        ],
    }

    expected_dict = {
        "DEMOGRAPHICS_CONVERSIONS": {"Gender": {1: "Male", 2: "Female", 3: "Other"}},
        "ASCOF_CONVERSIONS": [
            {
                "SCORE_NAME": "1B",
                "QUESTION_COLUMN": "q3a",
                "CONVERSION": {1: 1, 2: 1, 3: 2, 4: 2},
            }
        ],
    }

    actual_dict = do_all_dictionary_keys_to_integer_conversions(input_dict)

    assert actual_dict == expected_dict


def test_convert_conversion_dict():
    input_dict = {"Gender": {"1": "Male", "2": "Female", "3": "Other"}}

    expected_dict = {"Gender": {1: "Male", 2: "Female", 3: "Other"}}

    actual_dict = convert_demographic_conversion_dict(input_dict)

    assert actual_dict == expected_dict


def test_convert_dictionary_keys_to_integers():
    input_dict = {"1": "one", "2": "two", "3": "three"}

    expected_dict = {1: "one", 2: "two", 3: "three"}

    actual_dict = convert_dictionary_keys_to_integers(input_dict)

    assert actual_dict == expected_dict


def test_convert_list_of_lists_to_list_of_tuples():
    input_list = [["Apple", "Orange"], ["Salt", "Pepper"], ["Cat", "Dog"]]
    expected_list = [("Apple", "Orange"), ("Salt", "Pepper"), ("Cat", "Dog")]

    actual_list = convert_list_of_lists_to_list_of_tuples(input_list)

    assert expected_list == actual_list

