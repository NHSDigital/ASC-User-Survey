import pandas as pd

from .q2c_population import calculate_q2c_strata
from .melt_stratum_population import get_melted_stratum_population_series
from ..preprocess_utilities import filter_local_authorities_to_only_those_in_whitelist

from ascs import params


def preprocess_eligible_population_data(
    df_population_by_la: pd.DataFrame,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    df_population_by_la = filter_local_authorities_to_only_those_in_whitelist(
        df_population_by_la
    )

    population_by_la_stratum = get_melted_stratum_population_series(df_population_by_la)

    sample_by_la_stratum = get_melted_stratum_population_series(
        df_population_by_la, params.STRATUM_COLUMN_NAMES_SAMPLES
    )

    population_2c_by_la_stratum = get_melted_stratum_population_series(
        calculate_q2c_strata(df_population_by_la)
    )

    return population_by_la_stratum, sample_by_la_stratum, population_2c_by_la_stratum

