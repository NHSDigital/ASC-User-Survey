import pandas as pd


def round_to_five(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes any DataFrame and rounds all values within to the nearest 5
    e.g: 134.2 -> 135
         522   -> 520

    Args:
        df
            The DataFrame to round

    Returns:
        A new DataFrame with the rounded values
    """
    return ((df / 5).round(0) * 5).fillna(0).astype("int64")
