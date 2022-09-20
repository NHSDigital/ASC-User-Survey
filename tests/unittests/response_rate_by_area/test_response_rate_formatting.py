import pandas as pd

from ascs.response_rate_by_area.response_rate_formatting import add_missing_las


def test_add_missing_las():
    df_input = pd.DataFrame(
        {"LaCode": [211, 311], "q2": [34.5, 68.1], "q3": [56.9, 11]}
    ).set_index("LaCode")

    actual = add_missing_las(df_input, [1, 211, 916])

    expected = pd.DataFrame(
        {
            "LaCode": [211, 311, 1, 916],
            "q2": [34.5, 68.1, "[x]", "[x]"],
            "q3": [56.9, 11, "[x]", "[x]"],
        }
    ).set_index("LaCode")

    pd.testing.assert_frame_equal(actual, expected)
