from ascs.utilities.combine_multiple_choice import (
    combine_multiple_choice,
    combine_multiple_choice_auxiliary_utility,
)
import pandas as pd


def test_combine_multiple_choice(monkeypatch):
    df_annex = pd.DataFrame(
        [
            [0.6, 0.4, 200, 0.8, 0.2, 200, 0.1, 0.9, 200, 0.01, 0.99, 150],
            [0.5, 0.5, 350, 0.8, 0.2, 350, 0.1, 0.9, 350, 0.02, 0.98, 130],
        ],
        columns=pd.MultiIndex.from_product(
            [["q12a", "q12b", "q12c", "q13"], [1, 2, "Respondents"]],
            names=["question", "column_response"],
        ),
        index=[211, 311],
    )

    multiple_choice_questions = {"q12": ("a", "b", "c")}

    actual = combine_multiple_choice(df_annex, multiple_choice_questions)

    expected = pd.DataFrame(
        [[0.01, 0.99, 150, 0.6, 0.8, 0.1, 200], [0.02, 0.98, 130, 0.5, 0.8, 0.1, 350]],
        index=[211, 311],
        columns=pd.MultiIndex.from_arrays(
            [
                ["q13", "q13", "q13", "q12", "q12", "q12", "q12"],
                [1, 2, "Respondents", "a", "b", "c", "Respondents"],
            ],
            names=["question", "column_response"],
        ),
    )

    pd.testing.assert_frame_equal(actual, expected)


def test_combine_multiple_choice_auxiliary():
    df_in = pd.DataFrame(
        [
            ["q9a", 1, 1],
            ["q9a", 2, 2],
            ["q9b", 1, 3],
            ["q9b", 2, 4],
            ["q9c", 1, 5],
            ["q9c", 2, 6],
            ["q11", 99, 7],
        ],
        columns=["q", "r", "est_pop"],
    )

    df_expected = pd.DataFrame(
        [["q9", "a", 1], ["q9", "b", 3], ["q9", "c", 5], ["q11", 99, 7],],
        columns=["q", "r", "est_pop"],
        index=[0, 2, 4, 6],
    )

    df_actual = combine_multiple_choice_auxiliary_utility(
        df_in,
        question_column="q",
        response_column="r",
        multichoice_questions={"q9": ["a", "b", "c"]},
    )

    pd.testing.assert_frame_equal(df_actual, df_expected)
