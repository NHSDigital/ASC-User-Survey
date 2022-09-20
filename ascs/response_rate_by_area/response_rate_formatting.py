import pandas as pd

from typing import Any

from ascs import params


def format_annex_table4_for_output(annex_table4: pd.DataFrame) -> pd.DataFrame:
    annex_table4 = (
        (annex_table4 * 100)
        .round(1)
        .rename(columns={"q19a": "q19", "q20a": "q20", "q22a": "q22"})
        .pipe(add_missing_las)
    )[params.ANNEX_TABLE_4_COLUMN_ORDER]

    return annex_table4


def add_missing_las(
    annex_table4: pd.DataFrame, all_la_list: list[Any] = None
) -> pd.DataFrame:
    if all_la_list is None:
        all_la_list = params.ALL_LA_CODES

    full_index = annex_table4.index.union(all_la_list, sort=False)
    return annex_table4.reindex(full_index, fill_value="[x]")
