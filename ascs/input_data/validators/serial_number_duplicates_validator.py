import pandas as pd
from ascs.input_data.validators.base_validator import BaseValidator


class SerialNumberDuplicatesValidator(BaseValidator):
    def __init__(self) -> None:
        self.columns_to_set_null_for_invalid_rows = []

    def get_where_incorrect(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        return df_questionnaire_by_person.duplicated(
            subset=["LaCode", "SerialNo"], keep=False
        )

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            "serial number "
            + df_questionnaire_by_person["SerialNo"].astype(str)
            + " not unique in LA "
            + df_questionnaire_by_person["LaCode"].astype(str)
        )

