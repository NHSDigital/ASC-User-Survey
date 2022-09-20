import pandas as pd
from ascs.stratification.stratification import Stratification


def test_perform_stratification():
    df_questionnaire_by_person = pd.DataFrame(
        [
            [211, 1, 1],  # 0.2, n=10
            [211, 1, 1],
            [211, 1, 2],  # 0.2
            [211, 1, 2],
            [211, 1, 3],  # 0.6
            [211, 1, 3],
            [211, 1, 3],
            [211, 1, 3],
            [211, 1, 3],
            [211, 1, 3],
            [211, 2, 1],  # 0.6, n=5
            [211, 2, 1],
            [211, 2, 1],
            [211, 2, 2],  # 0.2
            [211, 2, 3],  # 0.2
            [311, 1, 2],  # 1, n=3
            [311, 1, 2],
            [311, 1, 2],
            [311, 2, 1],  # 0.5, n=4
            [311, 2, 1],
            [311, 2, 2],  # 0.5
            [311, 2, 2],
        ],
        columns=["LaCode", "Stratum", "q3a"],
    )

    population_by_la_stratum = pd.DataFrame(
        [[211, 1, 100], [211, 2, 100], [311, 1, 1000], [311, 2, 3000]],
        columns=["LaCode", "Stratum", "weight"],
    ).set_index(["LaCode", "Stratum"])["weight"]

    df_actual = Stratification(
        supergroup_columns=["LaCode"],
        subgroup_within_supergroup_columns=["Stratum"],
        discrete_column_name="q3a",
    ).do_stratification(df_questionnaire_by_person, population_by_la_stratum)

    df_expected_out = pd.DataFrame(
        [
            [211, "q3a", 1, 80.0, 40.0, 26.47814192876834, 5, 200],
            [211, "q3a", 2, 40, 20.0, 22.77314207569961, 3, 200],
            [211, "q3a", 3, 80, 40.0, 24.401803212057917, 7, 200],
            [311, "q3a", 1, 1500, 37.5, 42.40694518590086, 2, 4000],
            [311, "q3a", 2, 1000 + 1500, 62.5, 42.40694518590086, 5, 4000.0],
        ],
        columns=[
            "LaCode",
            "discrete",
            "response",
            "est_population",
            "percentage",
            "margin_of_error",
            "respondents",
            "supergroup_population",
        ],
    )

    pd.testing.assert_frame_equal(df_actual, df_expected_out)


def test_perform_stratification_handles_empty_columns_that_define_supergroup_list():
    df_questionnaire_by_person = pd.DataFrame(
        [
            [211, 1, 1],
            [211, 1, 2],
            [211, 1, 2],
            [211, 1, 2],
            [211, 1, 2],
            [211, 2, 2],
            [211, 2, 2],
            [211, 2, 2],
        ],
        columns=["LaCode", "Stratum", "q3a"],
    )

    population_by_la_stratum = pd.DataFrame(
        [[211, 1, 100], [211, 2, 100]], columns=["LaCode", "Stratum", "weight"],
    ).set_index(["LaCode", "Stratum"])["weight"]

    df_actual = Stratification(
        supergroup_columns=[],
        subgroup_within_supergroup_columns=["LaCode", "Stratum"],
        discrete_column_name="q3a",
    ).do_stratification(df_questionnaire_by_person, population_by_la_stratum)

    df_expected_out = pd.DataFrame(
        [
            ["q3a", 1, 20.0, 10.0, 19.10371691582557, 1, 200],
            ["q3a", 2, 180, 90.0, 19.10371691582557, 7, 200.0],
        ],
        columns=[
            "discrete",
            "response",
            "est_population",
            "percentage",
            "margin_of_error",
            "respondents",
            "supergroup_population",
        ],
    )

    pd.testing.assert_frame_equal(df_actual, df_expected_out)
