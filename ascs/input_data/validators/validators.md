# Validators

The validator class was added because the process of

- Spotting some issue (e.g: age can't be lower than 18)
- Creating a DataFrame showing the issue with a nice error message
- Setting the cells that are wrong

was very repetitive when many different types of issue needed to be checked - issues including that serial numbers weren't duplicates and that the easy read questions were answered correctly.

The BaseValidator class contains all of the repeated code, and uses inheritance/overrides to "switch out" the parts that change with each different type of validation.

It is recommended you have a basic understanding of object oriented programming before delving into this module:

- http://inventwithpython.com/beyond/chapter15.html
- http://inventwithpython.com/beyond/chapter16.html
- https://pynative.com/python-object-oriented-programming-oop-exercise/ - Excercises you can use to check your understanding

Another important concept is the idea of a boolean series.

Read about boolean series in this section here: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#boolean-indexing

Read an example that we made to check understanding here: https://nhsd-git.digital.nhs.uk/data-services/analytics-service/social-care/teaching-examples/-/blob/d3e24df83d4df41cf3f4a8a1273efe11b0d2ef7e/boolean_series.py

## Example

Let's imagine that in our data, we wanted to run a validation.

We need to check that the column "contrived_example" is not 123 or 321, if the column is 123 or 321 it is an error.

How do we write this?

We create a new class extended from the base class, and then we need to overwrite three methods

- override `__init__` to tell the base class which columns to set to null (when the row is wrong)
- `get_where_incorrect` to tell the validator which rows are wrong
- `get_error_message` to help output a human readable error

The base class does the repetitive stuff needed to create a nice error DataFrame, and to set the incorrect cells to none. All of the repetitive code is in the base class.

```python
class ContrivedExampleValidator(BaseValidator):
    def __init__(self):
        # In the __init__ you must set the columns_to_set_null_for_invalid_rows attribute
        self.columns_to_set_null_for_invalid_rows = ["contrived_example"]

    def get_where_incorrect(
        self, df_questionnaire_by_respondent: pd.DataFrame
    ) -> pd.Series:
        # This method must return a boolean series with True for each row that is incorrect
        return (
            (df_questionnaire_by_respondent["contrived_example"] == 123)
            | (df_questionnaire_by_respondent["contrived_example"] == 321)
        )

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        # This method returns the error message for the rows that are wrong
        return (
            "The contrived_example column was "
            + df_questionnaire_by_person["contrived_example"].astype(str)
            + " and this value is not allowed."
        )
```

How do we make the validator do the validating?

Imagine that the questionnaire data looks like this

| LaCode | PrimaryKey | SerialNo | contrived_example | other_columns |
|--------|------------|----------|-------------------|---------------|
| 211    | 211_5      | XIQ      | 36                | ...           |
| 211    | 211_6      | QOI      | 123               | ...           |
| 213    | 213_9      | 923      | 51                | ...           |
| 213    | 213_10     | 412      | 321               | ...           |

If we run

```python
cleaned_df_with_errors = ContrivedExampleValidator().run_check(df_questionnaire_by_person)
```

we will see the following.

The table `cleaned_df_with_errors.df` is

| LaCode | PrimaryKey | SerialNo | contrived_example | other_columns |
|--------|------------|----------|-------------------|---------------|
| 211    | 211_5      | XIQ      | 36                | ...           |
| 211    | 211_6      | QOI      | NaN               | ...           |
| 213    | 213_9      | 923      | 51                | ...           |
| 213    | 213_10     | 412      | NaN               | ...           |

and the table in `cleaned_df_with_errors.error_dfs[0]` is

| LaCode | PrimaryKey | SerialNo | message                                                             |
|--------|------------|----------|---------------------------------------------------------------------|
| 211    | 211_6      | QOI      | The contrived_example column was 123 and this value is not allowed. |
| 213    | 213_10     | 412      | The contrived_example column was 321 and this value is not allowed. |

## Example Extension - Making the validator work on a different column

What if we wanted to change the code so that the validator could be run on a column that wasn't the `"contrived_example"` column?

You can save the column as an attribute in the object to be able to do this

```python
class GenericContrivedExampleValidator(BaseValidator):
    def __init__(self, column: str):
        self.columns_to_set_null_for_invalid_rows = [column]
        self.column: str = column  # We save the column we want to run it on to the class

    def get_where_incorrect(
        self, df_questionnaire_by_respondent: pd.DataFrame
    ) -> pd.Series:
        return (
            (df_questionnaire_by_respondent[self.column] == 123)  # And we use self.column instead of "contrived_example"
            | (df_questionnaire_by_respondent[self.column] == 321)
        )

    def get_error_message(self, df_questionnaire_by_person: pd.DataFrame) -> pd.Series:
        return (
            f"The {self.column} column was "  # We can also include it in the error message using f-strings
            + df_questionnaire_by_person[self.column].astype(str)
            + " and this value is not allowed."
        )
```
