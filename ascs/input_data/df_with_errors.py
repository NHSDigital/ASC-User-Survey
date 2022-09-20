from __future__ import annotations

# This import is needed to allow a type definition for a method that refers to the type it is in
# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class

import pandas as pd

from typing import TYPE_CHECKING, Callable, NamedTuple, TypeVar


if TYPE_CHECKING:
    from .validators.base_validator import BaseValidator


# The types down here don't reflect the fact that the functions can take other arguments
# But those types are confusing to write so I left them out
DFTransformerFunction = Callable[[pd.DataFrame], pd.DataFrame]
ValidatorFunction = Callable[[pd.DataFrame], "DFWithErrors"]

ReturnType = TypeVar("ReturnType")


class DFWithErrors(NamedTuple):
    """
    While doing preprocessing and validating, you slowly create a new DataFrame, and you accumulate errors.
    This class stores both the errors and the DataFrame together for convenience.
    It also makes it easy to append new errors to this list of errors as you go doing multiple validations in a row.
    """

    df: pd.DataFrame
    error_dfs: list[pd.DataFrame] = []

    def run_transformer_on_df(
        self, df_transformer_function: DFTransformerFunction, *args, **kwargs
    ) -> DFWithErrors:
        """
        Runs the transformer function on this object's DataFrame
        Return a new DFWithErrors with:
            df = The new transformed DF;
            error_dfs = The old error dfs that were here before
        """
        processed_df = df_transformer_function(self.df, *args, **kwargs)

        return DFWithErrors(df=processed_df, error_dfs=self.error_dfs)

    def run_validator_on_df(
        self, validator: BaseValidator, *args, **kwargs
    ) -> DFWithErrors:
        """
        Runs the validator on this object's DataFrame
        Return a new DFWithErrors with:
            df = The new transformed DF;
            error_dfs = The old error dfs that were here before PLUS the new errors from the validator
        """
        return self.run_validator_function_on_df(validator.run_check, *args, **kwargs)

    def run_validator_function_on_df(
        self, validator_function: ValidatorFunction, *args, **kwargs
    ) -> DFWithErrors:
        """
        Runs the validator function on this object's DataFrame
        Return a new DFWithErrors with:
            df = The new transformed DF;
            error_dfs = The old error dfs that were here before PLUS the new errors from the validator
        """
        (processed_df, new_error_dfs) = validator_function(self.df, *args, **kwargs)

        list_containing_old_and_new_error_dfs = self.error_dfs + new_error_dfs

        return DFWithErrors(
            df=processed_df, error_dfs=list_containing_old_and_new_error_dfs
        )

    def pipe(
        self,
        function_that_takes_df_with_errors: Callable[..., ReturnType],
        *args,
        **kwargs
    ) -> ReturnType:
        """
        Runs the function with this DFWithErrors object
        Returns whatever that function returns.
        """
        return function_that_takes_df_with_errors(self, *args, **kwargs)

    def concatenate_errors_into_one_df(self):
        if len(self.error_dfs) == 0:
            return pd.DataFrame(
                [], columns=["LaCode", "PrimaryKey", "SerialNo", "message"]
            )

        return pd.concat(self.error_dfs, axis=0, ignore_index=True)
