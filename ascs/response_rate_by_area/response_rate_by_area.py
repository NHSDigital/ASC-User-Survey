import pandas as pd

from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation

from .response_rate_by_la import create_response_rate_by_la_table
from .response_rate_by_average_group import add_response_rate_by_average_group
from .response_rate_formatting import format_annex_table4_for_output


def create_response_rate_by_area_table(
    data_needed_for_table_creation: DataNeededForTableCreation,
) -> dict[str, pd.DataFrame]:

    df_response_rate_by_area = (
        create_response_rate_by_la_table(
            data_needed_for_table_creation.df_questionnaire_by_person
        )
        .pipe(
            add_response_rate_by_average_group,
            data_needed_for_table_creation.df_questionnaire_by_person,
        )
        .pipe(format_annex_table4_for_output)
    )

    return {"4": df_response_rate_by_area}
