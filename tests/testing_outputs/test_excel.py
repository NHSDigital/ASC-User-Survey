import pytest

import numpy as np
import pandas as pd

from ascs import params


@pytest.mark.parametrize(
    "excel_sheet_name,header_row",
    [
        (params.EXCEL_HORIZONTAL_GAP_SIZE_CONFIG_BY_NAME["1a"].SHEET_NAME, 4),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_CONFIG_BY_NAME["1b"].SHEET_NAME, 4),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_CONFIG_BY_NAME["5"].SHEET_NAME, 5),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["2a"].SHEET_NAME, 4,),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["2b"].SHEET_NAME, 4,),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["3a"].SHEET_NAME, 4,),
        (params.EXCEL_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["3b"].SHEET_NAME, 4,),
        (params.EXCEL_NO_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["4"].SHEET_NAME, 3,),
        (params.EXCEL_NO_HORIZONTAL_GAP_SIZE_AND_SECTIONS_BY_NAME["6"].SHEET_NAME, 5,),
    ],
)
def test_excel_tables(save_to_excel, excel_sheet_name, header_row):
    df_actual = pd.read_excel(
        save_to_excel, excel_sheet_name, header=header_row, index_col=0,
    )
    df_actual_numeric = df_actual.apply(pd.to_numeric, errors="coerce")

    df_expected = pd.read_excel(
        params.TEST_ANNEX_TABLES_FILE_PATH,
        excel_sheet_name,
        header=header_row,
        index_col=0,
    )
    df_expected_numeric = df_expected.apply(pd.to_numeric, errors="coerce")

    is_same_by_cell = (
        np.isclose(df_actual_numeric, df_expected_numeric)
        | (df_actual == df_expected)
        | (df_actual.isna() & df_expected.isna())
    )

    assert is_same_by_cell.all().all()
