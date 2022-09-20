from ascs.stratification.get_est_population_for_demographic_subgroups import (
    get_est_population_for_demographic_subgroups,
)
import pandas as pd


def test_create_weights():

    demographic = "Gender"
    question = "q3a"
    questionnaire_data = pd.DataFrame(
        [
            ["211", 1, 1, 1],
            ["211", 1, 1, 1],
            ["211", 1, 2, 1],
            ["211", 2, 1, 2],
            ["211", 2, 2, 2],
            ["211", 2, 2, 2],
            ["321", 1, 1, 1],
            ["321", 1, 2, 2],
            ["321", 1, 3, 2],
        ],
        columns=["LaCode", "Stratum", "q3a", "Gender"],
    )
    population_by_la_stratum = pd.DataFrame(
        {
            "LaCode": ["211", "321", "211", "321", "211", "321"],
            "Stratum": [1, 1, 2, 2, 3, 3],
            "la_stratum_pop": [10, 11, 20, 21, 30, 31],
        }
    ).set_index(["LaCode", "Stratum"])["la_stratum_pop"]

    actual = get_est_population_for_demographic_subgroups(
        [demographic], question, questionnaire_data, population_by_la_stratum,
    )

    expected = (
        pd.DataFrame(
            {
                "Gender": [1, 1, 2, 2],
                "LaCode": ["211", "321", "211", "321"],
                "Stratum": [1, 1, 2, 1],
                "weight": [10, 11 / 3, 20, 22 / 3],
            }
        )
        .set_index(["Gender", "LaCode", "Stratum"])["weight"]
        .rename(None)
    )

    pd.testing.assert_series_equal(actual, expected)
