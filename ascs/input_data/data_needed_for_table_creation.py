from typing import NamedTuple
import pandas as pd


class DataNeededForTableCreation(NamedTuple):
    df_questionnaire_by_person: pd.DataFrame = None
    population_by_la_stratum: pd.Series = None
    population_sample_by_la_stratum: pd.Series = None
    population_2c_by_la_stratum: pd.Series = None
    average_rows: pd.DataFrame = None
    df_by_validation_error: pd.DataFrame = None
    df_loading_error_by_file: pd.DataFrame = None
    df_questionnaire_unclean_by_person: pd.DataFrame = None
