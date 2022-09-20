import pandas as pd

from ascs.methodology_figures.utilities import apply_rounding, calc_percentage_column


def create_methodology_admin_proportions_table(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    """
    Works out how many people in the questionnaire data we have the gender, age and ethnicity info for
    Then outputs what % that is over the total number of people in the questionnaire data
    """
    return (
        df_questionnaire_by_person[["Gender", "Age", "ethnicity_methodology_grouping"]]
        .count()
        .rename("population")
        .to_frame()
        .assign(total_population=len(df_questionnaire_by_person))
        .pipe(calc_percentage_column)
        .pipe(apply_rounding)
    )
