import pandas as pd


def get_actual(table_df, row, question):
    return table_df.loc[row, (question, slice(None))].pipe(
        pd.to_numeric, errors="coerce"
    )


def check_supression(table_str, row, question, suppress_str, annex_table):
    actual = annex_table[table_str].loc[row, (question, slice(None))]
    assert (
        actual == suppress_str
    ).all(), f"""
table = {table_str}
row = {row}
question = {question}
should have all been supress_str "{suppress_str}"
actual = {actual}
"""
