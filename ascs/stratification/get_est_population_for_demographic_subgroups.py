from ascs.utilities.get_respondents_by_columns import get_respondents_by_columns
import pandas as pd


def get_est_population_for_demographic_subgroups(
    demographics: list[str],
    question: str,
    df_questionnaire_by_person: pd.DataFrame,
    population_by_la_stratum: pd.Series,
) -> pd.Series:
    """
    Gets the estimated population size for a group like Males in LA 211 Stratum 1
    See docs/maths.md for an explanation
    """
    respondents_by_demographic_la_stratum = get_respondents_by_columns(
        df_questionnaire_by_person,
        question,
        groupby_columns=[*demographics, "LaCode", "Stratum"],
    ).to_frame(name=f"{question}_n_dem_la_stratum")

    respondents_by_la_stratum = get_respondents_by_columns(
        df_questionnaire_by_person, question, groupby_columns=["LaCode", "Stratum"]
    ).rename(f"{question}_n_la_stratum")

    df_by_demographic_la_stratum = (
        # For each demorgraphic la stratum combo we need
        # The respondents in the dem la stratum
        respondents_by_demographic_la_stratum
        # The respondents in the la stratum
        .join(respondents_by_la_stratum, on=["LaCode", "Stratum"])
        # The total LA stratum population
        .join(population_by_la_stratum, on=["LaCode", "Stratum"],)
    )

    est_population_by_subgroup = (
        df_by_demographic_la_stratum["la_stratum_pop"]
        * df_by_demographic_la_stratum[f"{question}_n_dem_la_stratum"]
        / df_by_demographic_la_stratum[f"{question}_n_la_stratum"]
    )

    return est_population_by_subgroup
