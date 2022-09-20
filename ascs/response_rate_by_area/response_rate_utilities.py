import pandas as pd

from ascs import params


def filter_out_people_who_didnt_respond_to_the_overall_questionnaire(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    return df_questionnaire_by_person[
        df_questionnaire_by_person["Response"] == params.RESPONSE_RESPONDED_TO_SURVEY
    ]
