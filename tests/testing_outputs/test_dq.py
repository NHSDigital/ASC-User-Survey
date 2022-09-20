import pandas as pd
import numpy as np


def test_dq_annex1(annex_dq_table1_and_2: dict[str, pd.DataFrame]) -> None:
    assert np.isclose(
        annex_dq_table1_and_2["dq1"]["Sexuality"],
        [
            100.0,
            100.0,
            100.0,
            98.5,
            97.7,
            97.5,
            100.0,
            100.0,
            100.0,
            71.7,
            59.0,
            95.8,
            72.4,
            64.3,
            81.3,
            90.3,
            100.0,
            92.7,
        ],
    ).all()


def test_dq_annex2(annex_dq_table1_and_2: dict[str, pd.DataFrame]) -> None:
    expected = np.array(
        [
            100.0,
            100.0,
            100.0,
            97.5,
            96.7,
            97.2,
            100.0,
            100.0,
            100.0,
            73.1,
            57.1,
            95.2,
            75.5,
            58.7,
            84.0,
            87.6,
            100.0,
            90.2,
        ]
    )
    actual = annex_dq_table1_and_2["dq2"]["Sexuality"]
    assert np.isclose(
        actual, expected,
    ).all(), f"""
expected: {expected}
actual: {actual}
"""
