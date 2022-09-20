import pandas as pd
import numpy as np

from typing import Optional

from ascs import params


def get_melted_stratum_population_series(
    df_population_by_la: pd.DataFrame, stratum_columns: Optional[list[str]] = None
):
    """
    Data is in tabular form (type DataFrame)

    LaCode  |  stratum_1_pop  |   stratum_2_pop  |  stratum_3_pop

    211        100                115               300
    ...

    We want it in the form (type Series)

    Series index        | Series values
    LaCode  |  Stratum  | population
    211        1          100
               2          115
               3          300
                          ...
    """
    return df_population_by_la.pipe(melt_stratum_population, stratum_columns).pipe(
        convert_to_est_population_series
    )


def convert_to_est_population_series(
    df_population_by_la_stratum: pd.DataFrame,
) -> pd.DataFrame:
    return df_population_by_la_stratum.set_index(["LaCode", "Stratum"])[
        "la_stratum_pop"
    ]


def melt_stratum_population(
    df_population_by_la: pd.DataFrame, stratum_cols: list[str] = None
) -> pd.DataFrame:
    if stratum_cols is None:
        stratum_cols = params.STRATUM_COLUMN_NAMES

    df_wide = df_population_by_la[["LaCode", *stratum_cols]]

    df_long = pd.melt(
        df_wide, id_vars="LaCode", var_name="Stratum", value_name="la_stratum_pop"
    )

    df_long["Stratum"] = df_long["Stratum"].str.extract(r"(\d+)").astype(np.int64)

    return df_long
