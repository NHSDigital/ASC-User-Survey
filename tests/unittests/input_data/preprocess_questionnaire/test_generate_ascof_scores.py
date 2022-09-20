import pandas as pd
import numpy as np
import pytest
from ascs.input_data.preprocess_questionnaire import generate_ascof_scores
from ascs.input_data.preprocess_questionnaire.ascof_config import SimpleAscofConversion


def test_set_score_with_converion():
    df_in = pd.DataFrame({"q99": [1, 2, 3, 4, np.nan]})

    df_expected = df_in.copy()
    df_expected["GENERIC_SCORE"] = np.array([5, 5, 2, 2, np.nan])

    generic_score_conversion = SimpleAscofConversion(
        {
            "SCORE_NAME": "GENERIC_SCORE",
            "QUESTION_COLUMN": "q99",
            "CONVERSION": {1: 5, 2: 5, 3: 2, 4: 2},
        }
    )

    df_actual = generate_ascof_scores.apply_simple_conversion(
        df_in, generic_score_conversion
    )

    pd.testing.assert_frame_equal(df_expected, df_actual)


@pytest.mark.parametrize(
    "question_data,expected_score",
    [
        (
            {
                "q3a": [1, 2, 3, 4],
                "q4a": [1, 2, 3, 4],
                "q5a": [1, 2, 3, 4],
                "q6a": [1, 2, 3, 4],
                "q7a": [1, 2, 3, 4],
                "q8a": [1, 2, 3, 4],
                "q9a": [1, 2, 3, 4],
                "q11": [1, 2, 3, 4],
            },
            [24, 16, 8, 0],
        ),
        (
            {
                "q3a": [1, np.nan, 3, 4],
                "q4a": [1, 2, np.nan, 4],
                "q5a": [np.nan, 2, 3, 4],
                "q6a": [1, 2, 3, np.nan],
                "q7a": [1, 2, 3, 4],
                "q8a": [1, 2, 3, 4],
                "q9a": [1, 2, 3, 4],
                "q11": [1, 2, 3, 4],
            },
            [np.nan, np.nan, np.nan, np.nan],
        ),
    ],
)
def test_generate_1A(question_data, expected_score):
    df_in = pd.DataFrame(question_data)

    df_expected = df_in.copy()
    df_expected["ASCOF_1A"] = expected_score

    df_actual = generate_ascof_scores.generate_1A(df_in)

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_generate_simple_conversion_ascof_scores():
    df_in = pd.DataFrame({"q3a": [1, 2, 3, 4, np.nan], "q8a": [1, 2, 3, 4, np.nan]})

    simple_conversions = [
        SimpleAscofConversion(
            {
                "SCORE_NAME": "GENERIC_SCORE_1",
                "QUESTION_COLUMN": "q3a",
                "CONVERSION": {1: 0, 2: 5, 3: 99, 4: 64},
            }
        ),
        SimpleAscofConversion(
            {
                "SCORE_NAME": "GENERIC_SCORE_2",
                "QUESTION_COLUMN": "q8a",
                "CONVERSION": {1: 35, 2: 16, 3: 44, 4: 9},
            }
        ),
    ]

    df_expected = df_in.copy()
    df_expected["GENERIC_SCORE_1"] = np.array([0, 5, 99, 64, np.nan])
    df_expected["GENERIC_SCORE_2"] = np.array([35, 16, 44, 9, np.nan])
    df_actual = generate_ascof_scores.generate_simple_conversion_ascof_scores(
        df_in, simple_conversions
    )

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_generate_1J():
    df_in = pd.DataFrame(
        {
            "q3a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q4a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q5a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q6a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q7a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q8a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q9a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q11": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q13": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15b": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15c": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15d": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16b": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16c": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q17": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q18": [1.0, 2.0, 3.0, 4.0, 5.0],
            "age_1864": [True, True, False, False, False],
            "can_answer_2c": [True, True, True, True, False],
        }
    )

    df_expected = df_in.copy()
    df_expected["ASCOF_1J"] = np.array([0.418845, 0.410181, 0.075093, 0.111865, np.nan])

    df_actual = generate_ascof_scores.generate_1J(df_in)

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_recode_columns_for_1J():
    df_in = pd.DataFrame(
        {
            "q3a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q4a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q5a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q6a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q7a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q8a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q9a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q11": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q13": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15b": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15c": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q15d": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16b": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q16c": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q17": [1.0, 2.0, 3.0, 4.0, 5.0],
            "q18": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )

    df_expected = pd.DataFrame(
        {
            "q3a": [1, 0.919, 0.541, 0, 5],
            "q4a": [0.911, 0.789, 0.265, 0.195, 5],
            "q5a": [0.879, 0.775, 0.294, 0.184, 5],
            "q6a": [0.863, 0.78, 0.374, 0.288, 5],
            "q7a": [0.88, 0.452, 0.298, 0.114, 5],
            "q8a": [0.873, 0.748, 0.497, 0.241, 5],
            "q9a": [0.962, 0.927, 0.567, 0.17, 5],
            "q11": [0.847, 0.637, 0.295, 0.263, 5],
            "q13": [0.0, 0.0, -0.0148, -0.1090, -0.1090],
            "q15a": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q15b": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q15c": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q15d": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q16a": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q16b": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q16c": [0.0, 1.0, 2.0, 4.0, 5.0],
            "q17": [0.0, -0.0308, -0.1250, -0.1250, -0.1250],
            "q18": [0.0, -0.0603, -0.1100, -0.1100, 5.0],
        }
    )

    df_actual = generate_ascof_scores.recode_columns_for_1J(df_in)

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_calculate_weighted_quality_of_life_score():
    df_in = pd.DataFrame(
        {
            "q3a": [1, 2, 3, 4, 5],
            "q4a": [1, 2, 3, 4, 5],
            "q5a": [1, 2, 3, 4, 5],
            "q6a": [1, 2, 3, 4, 5],
            "q7a": [1, 2, 3, 4, 5],
            "q8a": [1, 2, 3, 4, 5],
            "q9a": [1, 2, 3, 4, 5],
            "q11": [1, 2, 3, 4, 5],
        }
    )

    df_expected = df_in.copy()
    df_expected["weighted_quality_of_life_score"] = np.array(
        [1.158, 2.782, 4.406, 6.03, 7.654]
    )

    df_actual = generate_ascof_scores.calculate_weighted_quality_of_life_score(df_in)

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_calculate_count_level_of_assistance_score():
    df_in = pd.DataFrame(
        {
            "q15a": [0, 1, 2, 3],
            "q15b": [0, 1, 2, 3],
            "q15c": [0, 1, 2, 3],
            "q15d": [0, 1, 2, 3],
            "q16a": [0, 1, 2, 3],
            "q16b": [0, 1, 2, 3],
            "q16c": [0, 1, 2, 3],
        }
    )

    df_expected = df_in.copy()
    df_expected["count_level_of_assistance_score"] = np.array([0, 7, 14, 21]).astype(
        "int64"
    )

    df_actual = generate_ascof_scores.calculate_count_level_of_assistance_score(df_in)

    pd.testing.assert_frame_equal(df_expected, df_actual)


def test_calculate_adjustment_factor():
    df_in = pd.DataFrame(
        {
            "q13": [0.0, 0.0, -0.0148, -0.1090, -0.1090],
            "q17": [0.0, -0.0308, -0.1250, -0.1250, -0.1250],
            "q18": [0.0, -0.0603, -0.1100, -0.1100, 5.0],
            "age_1864": [True, True, False, False, False],
            "count_level_of_assistance_score": [1, 1, 1, 1, 1],
        }
    )

    expected_adjustment_factor = pd.Series(
        [0.5596, 0.4685, 0.3571, 0.2629, 5.3729], name="adjustment_factor"
    )

    df_actual = generate_ascof_scores.calculate_adjustment_factor(df_in)

    pd.testing.assert_series_equal(
        expected_adjustment_factor, df_actual["adjustment_factor"]
    )


def test_calculate_1J():
    df_in = pd.DataFrame(
        {
            "weighted_quality_of_life_score": [1, 2, 3, 4, 5],
            "adjustment_factor": [5, 4, 3, 2, 1],
        }
    )

    expected_ASCOF_1J_by_person = pd.Series([-4, -2, 0, 2, 4])

    actual_ASCOF_1J_by_person = generate_ascof_scores.calculate_1J_from_recoded_questionnaire_df(
        df_in
    )

    pd.testing.assert_series_equal(
        expected_ASCOF_1J_by_person, actual_ASCOF_1J_by_person
    )


def test_set_1J_to_nan_for_invalid_responses():
    df_in = pd.DataFrame(
        {"q3a": [np.nan, 2], "can_answer_2c": [True, False,], "ASCOF_1J": [1, 2,],}
    )

    df_expected = df_in.copy()
    df_expected["ASCOF_1J"] = np.array([np.nan, np.nan,])

    df_actual = generate_ascof_scores.set_1J_to_nan_for_invalid_responses(
        df_in, ["q3a"]
    )

    pd.testing.assert_frame_equal(df_expected, df_actual)

