from typing import Any
from ascs.input_data.data_needed_for_table_creation import DataNeededForTableCreation
from ascs import params


def create_suppressed_questionnaire(
    data_needed_for_table_creation: DataNeededForTableCreation,
    identifier_cols: list[str] = None,
    columns_to_show: list[str] = None,
    columns_to_suppress: list[str] = None,
    columns_to_change_type: dict[str, Any] = {"Age_Grouped": object},
):
    """
    We want to output the questionnaire data, but don't want to compromise people's privacy.
    We do this by:
    1) Outputting less specific grouped demographic columns instead of the original specific demog cols
    2) Check how many people there are in "identifier group"
    Each identifier group is one combination of demographic/other columns
    We then erase the demographic info of anyone in a identifier group with very few people
    That way people can't be identified to their answers if they have a very unique combo of demographics.
    """
    if identifier_cols is None:
        identifier_cols = params.IDENTIFIER_COLUMNS_FOR_SUPPRESSED_QUESTIONNAIRE_CSV
    if columns_to_show is None:
        columns_to_show = params.COLUMNS_TO_SHOW_IN_SUPPRESSED_QUESTIONNAIRE_CSV
    if columns_to_suppress is None:
        columns_to_suppress = params.COLUMNS_TO_SUPPRESS_IN_QUESTIONNAIRE_CSV

    size_by_identifier_group = data_needed_for_table_creation.df_questionnaire_by_person.groupby(
        identifier_cols, dropna=False,
    ).size()

    should_suppress_by_identifier_group = (
        size_by_identifier_group
        <= params.QUESTIONNAIRE_CSV_MAX_SIZE_OF_GROUP_TO_SUPPRESS
    ).rename("Should_Suppress")

    df_questionnaire_by_person = data_needed_for_table_creation.df_questionnaire_by_person.merge(
        should_suppress_by_identifier_group, how="left", on=identifier_cols,
    ).astype(
        columns_to_change_type
    )

    df_questionnaire_by_person.loc[
        df_questionnaire_by_person["Should_Suppress"], columns_to_suppress
    ] = 99

    df_questionnaire_by_person = df_questionnaire_by_person[columns_to_show]

    return {"suppressed_questionnaire": df_questionnaire_by_person}
