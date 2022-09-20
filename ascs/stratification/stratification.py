import numpy as np
import pandas as pd

from ascs.utilities.get_respondents_by_columns import get_respondents_by_columns


MARGIN_OF_ERROR_CRITICAL_VALUE = 1.96


def perform_stratification(
    df_questionnaire_by_person: pd.DataFrame,
    est_population_by_subgroup: pd.Series,
    supergroup_columns: list[str],
    subgroup_within_supergroup_columns: list[str],
    discrete_column_name: str,
) -> pd.DataFrame:
    return Stratification(
        discrete_column_name=discrete_column_name,
        supergroup_columns=supergroup_columns,
        subgroup_within_supergroup_columns=subgroup_within_supergroup_columns,
    ).do_stratification(df_questionnaire_by_person, est_population_by_subgroup)


class Stratification:
    """
    Class to combine people's answers across subgroups.
    The answers are combined so that one subgroup's contribution to the answer is proportional to its population size
    and not to the number of people in that subgroup who responded.

    See docs/maths.md
    """
    discrete_column_name: str
    supergroup_columns: list[str]
    subgroup_within_supergroup_columns: list[str]

    def __init__(
        self,
        discrete_column_name: str,
        supergroup_columns: list[str],
        subgroup_within_supergroup_columns: list[str],
    ):
        self.discrete_column_name = discrete_column_name
        self.supergroup_columns = supergroup_columns
        self.subgroup_within_supergroup_columns = subgroup_within_supergroup_columns

    def get_subgroup_columns(self) -> list[str]:
        return self.supergroup_columns + self.subgroup_within_supergroup_columns

    def do_stratification(
        self,
        df_questionnaire_by_person: pd.DataFrame,
        est_population_by_subgroup: pd.Series,
    ) -> pd.DataFrame:
        df_questionnaire_by_person = self.reformat_questionnaire_data_for_stratification(
            df_questionnaire_by_person
        )

        df_by_subgroup_response = (
            df_questionnaire_by_person.pipe(
                self.get_number_of_respondents_that_responded_each_way_in_subgroup
            )
            .pipe(self.get_proportion_that_responded_each_way_in_subgroup)
            .pipe(
                self.attach_other_needed_subgroup_information,
                df_questionnaire_by_person,
                est_population_by_subgroup,
            )
            .pipe(self.calc_est_population_in_subgroup_response)
            .pipe(self.calc_variance_in_subgroup_response)
        )
        df_by_supergroup_response = (
            df_by_subgroup_response.pipe(self.sum_to_supergroup)
            .pipe(self.calc_population_in_supergroup)
            .pipe(self.calc_proportion_in_supergroup_response)
            .pipe(self.calc_margin_of_error_in_supergroup_response)
            .pipe(self.calc_percentage_in_supergroup_response)
            .pipe(self.format_output)
        )
        return df_by_supergroup_response

    def reformat_questionnaire_data_for_stratification(
        self, df_questionnaire_by_person: pd.DataFrame,
    ) -> pd.DataFrame:
        return (
            df_questionnaire_by_person.pipe(self.select_only_relevent_columns,)
            .copy()
            .rename(columns={self.discrete_column_name: "response"})
        )

    def select_only_relevent_columns(
        self, df_questionnaire_by_person: pd.DataFrame,
    ) -> pd.DataFrame:
        return df_questionnaire_by_person[
            self.get_subgroup_columns() + [self.discrete_column_name]
        ]

    def get_number_of_respondents_that_responded_each_way_in_subgroup(
        self, df_questionnaire_by_person: pd.DataFrame
    ) -> pd.Series:
        prop_by_subgroup_series = df_questionnaire_by_person.groupby(
            self.get_subgroup_columns()
        )["response"].value_counts(normalize=False, sort=False)

        prop_by_subgroup_series.index.set_names("response", level=-1, inplace=True)

        return prop_by_subgroup_series.reset_index(name="respondents")

    def get_proportion_that_responded_each_way_in_subgroup(
        self, df_by_subgroup_response: pd.DataFrame
    ) -> pd.Series:
        df_by_subgroup_response["proportion"] = df_by_subgroup_response[
            "respondents"
        ] / df_by_subgroup_response.groupby(self.get_subgroup_columns())[
            "respondents"
        ].transform(
            "sum"
        )
        return df_by_subgroup_response

    def attach_other_needed_subgroup_information(
        self,
        df_by_subgroup_response: pd.DataFrame,
        df_questionnaire_by_person: pd.DataFrame,
        est_population_by_subgroup: pd.Series,
    ) -> pd.DataFrame:
        n_answered_question_by_subgroup = self.calc_how_many_in_each_subgroup_answered_the_question(
            df_questionnaire_by_person
        )
        return df_by_subgroup_response.merge(
            n_answered_question_by_subgroup.rename(
                "subgroup_number_who_answered_question"
            ),
            how="left",
            left_on=self.get_subgroup_columns(),
            right_index=True,
        ).merge(
            est_population_by_subgroup.rename("subgroup_est_population"),
            how="left",
            on=self.get_subgroup_columns(),
        )

    def calc_how_many_in_each_subgroup_answered_the_question(
        self, df_questionnaire_by_person: pd.DataFrame,
    ) -> pd.Series:
        return get_respondents_by_columns(
            df_questionnaire_by_person,
            "response",
            groupby_columns=self.get_subgroup_columns(),
        )

    def calc_est_population_in_subgroup_response(
        self, df_by_subgroup_response: pd.DataFrame,
    ) -> pd.DataFrame:
        df_by_subgroup_response["est_population"] = (
            df_by_subgroup_response["proportion"]
            * df_by_subgroup_response["subgroup_est_population"]
        )
        return df_by_subgroup_response

    def calc_variance_in_subgroup_response(
        self, df_by_subgroup_response: pd.DataFrame
    ) -> pd.DataFrame:
        """
        See https://files.digital.nhs.uk/BD/6D7209/pss-ascs-eng-1819-Methodology_report.pdf
        """
        df_by_subgroup_response["variance"] = (
            df_by_subgroup_response["proportion"]
            * (1 - df_by_subgroup_response["proportion"])
            * df_by_subgroup_response["subgroup_est_population"] ** 2
            * (
                1
                - (
                    df_by_subgroup_response["subgroup_number_who_answered_question"]
                    / df_by_subgroup_response["subgroup_est_population"]
                )
            )
            / (df_by_subgroup_response["subgroup_number_who_answered_question"] - 1)
        )
        return df_by_subgroup_response

    def sum_to_supergroup(self, df_by_subgroup_response: pd.DataFrame) -> pd.DataFrame:
        """
        Sum up over the subgroups
        Adding the subgroups (like males in LA 211 strat 1, males in LA 213 strat 3)
        in each bigger supergroup (males)
        """
        return df_by_subgroup_response.groupby(self.supergroup_columns + ["response"])[
            ["est_population", "variance", "respondents"]
        ].sum()

    def calc_population_in_supergroup(
        self, df_by_supergroup_response: pd.DataFrame
    ) -> pd.DataFrame:
        more_than_one_supergroup = len(self.supergroup_columns) > 0
        if more_than_one_supergroup:
            df_by_supergroup_response[
                "supergroup_population"
            ] = df_by_supergroup_response.groupby(self.supergroup_columns)[
                "est_population"
            ].transform(
                "sum"
            )
        else:
            df_by_supergroup_response["supergroup_population"] = (
                df_by_supergroup_response["est_population"]
            ).sum()
        return df_by_supergroup_response

    def calc_margin_of_error_in_supergroup_response(
        self, df_by_supergroup_response: pd.DataFrame
    ) -> pd.DataFrame:
        df_by_supergroup_response["variance"] *= (
            100 ** 2 / df_by_supergroup_response["supergroup_population"] ** 2
        )
        df_by_supergroup_response["margin_of_error"] = (
            MARGIN_OF_ERROR_CRITICAL_VALUE
            * np.sqrt(df_by_supergroup_response["variance"])
        )
        return df_by_supergroup_response

    def calc_proportion_in_supergroup_response(
        self, df_by_supergroup_response: pd.DataFrame
    ) -> pd.DataFrame:
        df_by_supergroup_response["proportion"] = (
            df_by_supergroup_response["est_population"]
            / df_by_supergroup_response["supergroup_population"]
        )
        return df_by_supergroup_response

    def format_output(self, df_by_supergroup_response: pd.DataFrame) -> pd.DataFrame:
        df_by_supergroup_response["discrete"] = self.discrete_column_name
        return df_by_supergroup_response.reset_index()[
            [
                *self.supergroup_columns,
                "discrete",
                "response",
                "est_population",
                "percentage",
                "margin_of_error",
                "respondents",
                "supergroup_population",
            ]
        ]

    def calc_percentage_in_supergroup_response(
        self, df_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        df_by_supergroup["percentage"] = 100 * df_by_supergroup["proportion"]
        return df_by_supergroup
