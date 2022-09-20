import pytest

import pandas as pd


@pytest.mark.parametrize(
    "table,columns,index",
    [
        (
            "methodology_population_sample",
            {
                "population": [62340, 24700],
                "total_population": [62340, 62340],
                "percentage": [100, 39.6],
            },
            pd.Index(["Total Eligible", "Sample"], name="group"),
        ),
        (
            "methodology_admin_data",
            {
                "population": [24700, 24700, 23765],
                "total_population": [24700, 24700, 24700],
                "percentage": [100, 100, 96.2],
            },
            ["Gender", "Age", "ethnicity_methodology_grouping"],
        ),
        (
            "methodology_sample_by_ethnicity",
            {
                "population": [3340, 20425],
                "total_population": [23765, 23765],
                "percentage": [14.1, 85.9],
            },
            pd.Index(["Non-White", "White"], name="ethnicity_methodology_grouping"),
        ),
    ],
)
def test_methodology_tables(methodology_tables, table, columns, index):
    actual = methodology_tables[table]
    expected = pd.DataFrame(columns, index=index)
    pd.testing.assert_frame_equal(actual, expected)


def test_methodology_response_type_table(methodology_tables):
    actual = methodology_tables["methodology_sample_by_response_type"]
    expected = pd.DataFrame(
        {
            "population": [6695, 665, 17340],
            "total_population": [24700, 24700, 24700],
            "percentage": [27.1, 2.7, 70.2],
        },
        index=pd.Index([1, 2, 3], name="Response"),
    )
    pd.testing.assert_frame_equal(actual, expected)


def test_methodology_admin_proportions(methodology_tables):
    actual = methodology_tables["methodology_admin_data"]
    expected = pd.DataFrame(
        [[24700, 24700, 100.0], [24700, 24700, 100.0], [23765, 24700, 96.2],],
        columns=["population", "total_population", "percentage"],
        index=["Gender", "Age", "ethnicity_methodology_grouping",],
    )
    pd.testing.assert_frame_equal(actual, expected)
