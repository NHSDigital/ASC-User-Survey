import pandas as pd
from ascs.utilities.output_formatting import round_to_five


def test_round_to_five():
    actual = round_to_five(pd.DataFrame([[4.99, 5.01, 142.49, 142.51, 189,]]))

    expected = pd.DataFrame([[5, 5, 140, 145, 190,]])

    pd.testing.assert_frame_equal(actual, expected)
