from numbers import Number
import numpy as np
import pandas as pd

from ascs import params


def add_all_grouped_demographics_columns(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    """
    Certain columns contain very general information (like people's exact age in years)
    but we mainly need the grouped information (for example ageBand = 18-24)
    This function adds these.
    """
    return (
        df_questionnaire_by_person.pipe(
            add_grouped_columns_from_demographics_conversions
        )
        .pipe(add_age_1864_column_to_questionnaire_data)
        .pipe(add_age_grouped_columns_to_questionnaire_data)
    )


def add_grouped_columns_from_demographics_conversions(
    df_questionnaire_by_person: pd.DataFrame,
    demographic_conversions: dict[str, dict[str, str]] = None,
) -> pd.DataFrame:
    """
    Takes the specific columns of data
        e.g: col Ethnicity = [1, 2, 7, ...]
    and a dictionary with conversions
        e.g: {"Ethnicity": {1: "White", 2: "White", 7: "Asian" ...} ...}
    and adds new converted, grouped columns
        e.g: col Ethnicity_Grouped = ["White", "White", "Asian" ...]
    """
    if demographic_conversions is None:
        demographic_conversions = params.DEMOGRAPHICS_CONVERSIONS

    for column, conversion in demographic_conversions.items():
        df_questionnaire_by_person[f"{column}_Grouped"] = df_questionnaire_by_person[
            column
        ].replace(conversion)

    return df_questionnaire_by_person


def add_age_1864_column_to_questionnaire_data(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    df_questionnaire_by_person["age_1864"] = df_questionnaire_by_person["Age"].between(
        18, 64
    )

    # Make sure that nulls stay as nulls
    df_questionnaire_by_person.loc[
        df_questionnaire_by_person["Age"].isna(), "age_1864"
    ] = np.nan

    return df_questionnaire_by_person


def add_age_grouped_columns_to_questionnaire_data(
    df_questionnaire_by_person: pd.DataFrame, age_group_bins: list[int] = None,
) -> pd.DataFrame:
    """
    From col Age = [18, 89, 36 ...]
    To col Age_Grouped = ["18-24", "85-inf", "35-44", ...]
    """
    if age_group_bins is None:
        age_group_bins = params.AGE_GROUP_BINS_START_AGES

    bins = pd.IntervalIndex.from_breaks(age_group_bins, closed="left")

    labels = get_list_of_labels_for_each_age_group_bin(age_group_bins)

    label_by_bin: dict[str, str] = dict(zip(bins, labels))

    df_questionnaire_by_person["Age_Grouped"] = pd.cut(
        df_questionnaire_by_person["Age"], bins=bins
    ).replace(label_by_bin)

    return df_questionnaire_by_person


def get_list_of_labels_for_each_age_group_bin(
    age_group_bins: list[Number],
) -> list[str]:
    return [
        f"{age_group_bins[pos]}-{age_group_bins[pos+1] -1}"
        for pos in range(len(age_group_bins) - 1)
    ]
