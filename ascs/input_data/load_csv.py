from pathlib import Path
from typing import Union
import pandas as pd
from ascs import params


def load_df_population_by_la(
    eligible_population_data_filename: Union[str, Path] = None,
) -> pd.DataFrame:
    if eligible_population_data_filename is None:
        eligible_population_data_filename = params.ELIGIBLE_POPULATION_DATA_PATH

    return pd.read_csv(eligible_population_data_filename, index_col=False)
