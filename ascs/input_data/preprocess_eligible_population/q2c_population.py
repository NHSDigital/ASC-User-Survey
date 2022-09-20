import pandas as pd


def calculate_q2c_strata(df_population_by_la: pd.DataFrame) -> pd.DataFrame:
    """
    Question 2c asks whether a person has choice
    It was considered too complicated to ask to those with learning difficulties (Stratum 1)
    It was considered unethical to ask those in residential (Stratum 3 and some in Stratum 2)
    Therefore the population sizes of the strata are different for Q2C than others
    This function works out those stratum sizes
    """
    df_population_2c_by_la = df_population_by_la.copy()

    df_population_2c_by_la["stratum1Pop"] = 0
    df_population_2c_by_la["stratum3Pop"] = 0
    remove_groups_that_cant_answer_2c_from_stratum_2_population_count(
        df_population_2c_by_la
    )
    # Stratum 4's population is the same for q2c as not

    return df_population_2c_by_la


def remove_groups_that_cant_answer_2c_from_stratum_2_population_count(
    df_population_2c_by_la: pd.DataFrame,
) -> pd.DataFrame:
    for column_name in df_population_2c_by_la.columns:
        is_stratum_1 = "LearnDis" in column_name
        is_stratum_2 = "1864" in column_name and not is_stratum_1
        is_in_residential = "Residential" in column_name or "Nursing" in column_name

        if is_stratum_2 and is_in_residential:
            df_population_2c_by_la["stratum2Pop"] -= df_population_2c_by_la[column_name]

    return df_population_2c_by_la
