import numpy as np
import pandas as pd

from ascs import params


def replace_erroneous_input_value_with_null(
    df_questionnaire_by_person: pd.DataFrame,
) -> pd.DataFrame:
    return df_questionnaire_by_person.replace(
        params.ERRONEOUS_INPUT_VALUE, np.nan
    ).replace(str(params.ERRONEOUS_INPUT_VALUE), np.nan)


SUPPORT_SETTING_COMMUNITY = 1
SUPPORT_SETTING_RESIDENTIAL_CARE = 2
SUPPORT_SETTING_NURSING_CARE = 3


def add_stratum_column(df_questionnaire_by_person: pd.DataFrame) -> pd.DataFrame:
    is_stratum_1 = (
        df_questionnaire_by_person["PrimarySupportReason"]
        == params.PRIMARY_SUPPORT_REASON_LEARNING_DISABILITY
    )

    is_stratum_2 = ~is_stratum_1 & (df_questionnaire_by_person["Age"].between(18, 64))

    is_stratum_3 = (
        ~is_stratum_1
        & ~is_stratum_2
        & df_questionnaire_by_person["SupportSetting"].isin(
            [SUPPORT_SETTING_RESIDENTIAL_CARE, SUPPORT_SETTING_NURSING_CARE]
        )
    )

    is_stratum_4 = (
        ~is_stratum_1
        & ~is_stratum_2
        & (df_questionnaire_by_person["SupportSetting"] == SUPPORT_SETTING_COMMUNITY)
    )

    required_column_na_by_person = (
        df_questionnaire_by_person[["Age", "PrimarySupportReason", "SupportSetting"]]
        .isna()
        .any(axis=1)
    )

    df_questionnaire_by_person["Stratum"] = np.select(
        [
            required_column_na_by_person,
            is_stratum_1,
            is_stratum_2,
            is_stratum_3,
            is_stratum_4,
        ],
        [np.nan, 1, 2, 3, 4],
        default=np.nan,
    )

    return df_questionnaire_by_person
