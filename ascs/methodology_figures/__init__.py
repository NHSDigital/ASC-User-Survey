from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs.methodology_figures.methodology_admin_proportions import (
    create_methodology_admin_proportions_table,
)
from ascs.methodology_figures.population_sample_table import (
    create_who_answered_population_sample_table,
)
from ascs.methodology_figures.methodology_sample_split_by_column_table import (
    create_methodology_sample_split_by_column_table,
)
from ascs.methodology_figures.utilities import add_ethnicity_methodology_grouping_column


def create_all_methodology_tables(data_for_table_creation: DataNeededForTableCreation):
    add_ethnicity_methodology_grouping_column(
        data_for_table_creation.df_questionnaire_by_person
    )
    return {
        "methodology_population_sample": create_who_answered_population_sample_table(
            data_for_table_creation
        ),
        "methodology_sample_by_response_type": create_methodology_sample_split_by_column_table(
            data_for_table_creation, column_to_split_by="Response"
        ),
        "methodology_sample_by_gender": create_methodology_sample_split_by_column_table(
            data_for_table_creation, column_to_split_by="Gender"
        ),
        "methodology_sample_by_age": create_methodology_sample_split_by_column_table(
            data_for_table_creation, column_to_split_by="age_1864"
        ),
        "methodology_sample_by_ethnicity": create_methodology_sample_split_by_column_table(
            data_for_table_creation, column_to_split_by="ethnicity_methodology_grouping"
        ),
        "methodology_admin_data": create_methodology_admin_proportions_table(
            data_for_table_creation.df_questionnaire_by_person
        ),
    }
