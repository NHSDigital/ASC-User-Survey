import numpy as np
import pandas as pd

from ascs.utilities.output_formatting import round_to_five


def calc_percentage_column(table: pd.DataFrame) -> pd.DataFrame:
    table["percentage"] = 100 * table["population"] / table["total_population"]

    return table


def apply_rounding(table: pd.DataFrame) -> pd.DataFrame:
    table["population"] = table["population"].pipe(round_to_five)
    table["total_population"] = table["total_population"].pipe(round_to_five)
    table["percentage"] = table["percentage"].round(1)

    return table


def add_ethnicity_methodology_grouping_column(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    df_questionnaire_by_person[
        "ethnicity_methodology_grouping"
    ] = df_questionnaire_by_person["Ethnicity_Grouped"].replace(
        {
            "Mixed": "Non-White",
            "Asian or Asian British": "Non-White",
            "Black or Black British": "Non-White",
            "Other": "Non-White",
            "Not Stated": np.nan,
        }
    )

    return df_questionnaire_by_person
