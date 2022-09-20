import numpy as np
import pandas as pd


def do_q2c_preprocessing(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    return df_questionnaire_by_person.pipe(add_can_answer_2c_column).pipe(
        set_q2c_null_for_people_who_shouldnt_answer_2c
    )


def set_q2c_null_for_people_who_shouldnt_answer_2c(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    df_questionnaire_by_person.loc[
        ~df_questionnaire_by_person["can_answer_2c"], "q2c"
    ] = np.nan

    return df_questionnaire_by_person


def add_can_answer_2c_column(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    primary_support_reason_learning_disability = (
        df_questionnaire_by_person["PrimarySupportReason_Grouped"]
        == "Learning Disability Support"
    )
    support_setting_residential_nursing = df_questionnaire_by_person[
        "SupportSetting_Grouped"
    ].isin(["Residential Care", "Nursing Care"])

    people_who_shouldnt_answer_2c = (
        primary_support_reason_learning_disability | support_setting_residential_nursing
    )

    df_questionnaire_by_person["can_answer_2c"] = ~people_who_shouldnt_answer_2c

    return df_questionnaire_by_person
