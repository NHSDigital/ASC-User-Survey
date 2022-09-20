import pandas as pd

from ascs.input_data.preprocess_questionnaire.demographics_columns import (
    add_grouped_columns_from_demographics_conversions,
    add_age_grouped_columns_to_questionnaire_data,
)


TEST_DEMOGRAPHICS_CONVERSIONS = {
    "Gender": {1: "Male", 2: "Female", 3: "Other"},
    "Ethnicity": {
        (1, 2, 3, 4): "White",
        (5, 6, 7, 8): "Mixed",
        (9, 10, 11, 12, 13): "Asian or Asian British",
        (14, 15, 16): "Black or Black British",
        (17, 18): "Other",
        (98, 99): "Not Stated",
    },
    "Religion": {
        1: "None",
        2: "Christian",
        3: "Buddhist",
        4: "Hindu",
        5: "Jewish",
        6: "Muslim",
        7: "Sikh",
        8: "Other",
        99: "Refused to say",
    },
    "PrimarySupportReason": {
        (1, 2): "Physical Support",
        (3, 4, 5): "Sensory Support",
        6: "Support with Memory and Cognition",
        7: "Learning Disability Support",
        8: "Mental Health Support",
        (9, 10, 11, 12): "Social Support",
    },
}


def test_add_grouped_columns_from_demographics_conversions():
    df_input = pd.DataFrame(
        [[1, 1, 7, 12], [2, 8, 3, 8], [3, 15, 6, 6], [1, 98, 99, 2]],
        columns=["Gender", "Ethnicity", "Religion", "PrimarySupportReason"],
    )

    df_expected = pd.DataFrame(
        [
            [1, 1, 7, 12, "Male", "White", "Sikh", "Social Support"],
            [2, 8, 3, 8, "Female", "Mixed", "Buddhist", "Mental Health Support"],
            [
                3,
                15,
                6,
                6,
                "Other",
                "Black or Black British",
                "Muslim",
                "Support with Memory and Cognition",
            ],
            [1, 98, 99, 2, "Male", "Not Stated", "Refused to say", "Physical Support"],
        ],
        columns=[
            "Gender",
            "Ethnicity",
            "Religion",
            "PrimarySupportReason",
            "Gender_Grouped",
            "Ethnicity_Grouped",
            "Religion_Grouped",
            "PrimarySupportReason_Grouped",
        ],
    )
    add_grouped_columns_from_demographics_conversions(
        df_input, demographic_conversions=TEST_DEMOGRAPHICS_CONVERSIONS
    )
    pd.testing.assert_frame_equal(df_input, df_expected)


def test_add_age_grouped_columns_to_questionnaire_data():
    df_input = pd.DataFrame({"Age": [18, 24, 25, 34, 35, 43, 44, 45, 64, 99]})

    df_expected = pd.DataFrame(
        [
            [18, "18-24"],
            [24, "18-24"],
            [25, "25-34"],
            [34, "25-34"],
            [35, "35-44"],
            [43, "35-44"],
            [44, "35-44"],
            [45, "45-54"],
            [64, "55-64"],
            [99, "85-inf"],
        ],
        columns=["Age", "Age_Grouped"],
    )
    add_age_grouped_columns_to_questionnaire_data(df_input)
    pd.testing.assert_frame_equal(df_input.astype({"Age_Grouped": object}), df_expected)
