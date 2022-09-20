# Design Decisions

This document contains a list of the design decisions we have made, and why we made them.

## Params

You can find the params JSON files in the `params_json` directory.

You can find the params object in the `ascs/params_utils/params.py` file.

The params object is created in `ascs/__init__.py`.

We chose this structure because:

1. To be able to use parameters in tests without difficulty, even if the params used are different than the ones for the main publication
2. To have type definitions and autocomplete for our parameters
3. To be able to access the params easily (you shouldn't have to type loads to get access to the params)
4. To be able to select which year of params you want to have from a menu.
5. To have a neat way of doing derived params (params that can be worked out from other params)
6. To be able to run sense checks easily on our params

Any derived params are found as methods on the Params object.

Whenever params is accessed, it must be in a function. That way, it always uses the current version of params, which is vital for testing.

### typed_params

We have created a Python package `typed_params`. This handles the processing of the params JSON files. It will check the type hint in the `params` class and convert the JSON object into the relevant class. This means that these subobjects in params can be accessed in the same way as params.

### Examples

<details>
<summary>How to access a param</summary>

```python
# params_json/2020-21.json
{
    ...
    "SOME_PROPERTY": [1, 2, 3],
    ...
}

# ascs/params_utils/params.py
class Params(BaseModel):
    ...
    SOME_PROPERTY: list[int]
    ...

# ascs/utilities/accessing_a_param.py
from ascs import params

print(params.SOME_PROPERTY)
print("Because of the class, the propery has type definitions")
```

</details>

<details>
<summary>How to access a derived param</summary>

The scenario, you have a param "PARAM_1" and another "PARAM_2" and you want to be able to get the sum of them.

```python
# params_json/2020-21.json
{
    ...
    "PARAM_1": 8,
    "PARAM_2": 2,
    ...
}

# ascs/params_utils/params.py
class Params(BaseModel):
    ...
    PARAM_1: int
    PARAM_2: int
    ...

    def get_added_params(self) -> int:
        return self.PARAM_1 + self.PARAM_2

# ascs/utilities/accessing_a_derived_param.py
from ascs import params

print(params.get_added_params())  # 10
```

</details>

<details>
<summary>How typed_params converts JSON objects</summary>

In this scenario you have a subobject `SOME_CONFIG` in the params JSON file which should be converted to an object.

```python
# params_json/2020-21.json
{
    ...
    "SOME_CONFIG": {
        "PROPERTY_A": 1,
        "PROPERTY_B": 2
    }
    ...
}

# ascs/param_utils/params.py
class SomeConfig(BaseModel):
    ...
    PROPERTY_A: int
    PROPERTY_B: int
    ...

class Params(BaseModel):
    SOME_CONFIG: SomeConfig

# ascs/utilities/accessing_a_subobject.py
from ascs import params

print(params.SOME_CONFIG.PROPERTY_A) # 1

```

</details>

### Resources

Read more about JSON here: https://www.w3schools.com/whatis/whatis_json.asp

Read more about classes and objects here: https://www.w3schools.com/python/python_classes.asp

## Packages

The code is in packages, this is because packages allow easier importing when you have a multi-folder structure. We need multiple folders to keep the code well organised.

This means following three rules:

1. Every folder that has a python file in it must contain an `__init__.py` file
2. When you call the code, you must do `python -m ascs.create_publication` and _not_ `python .\ascs\create_publication.py`
3. When you run code, you must be in the base directory of the repository (the `/ascs` folder, not the `/ascs/ascs` folder or the `/ascs/docs` folder)

If you follow these rules, then if you have code in `/ascs (the base directory) /ascs/abc/something.py` then anywhere in your code you can do

```python
from ascs.abc.something import the_thing_you_want_to_import
```

What happens to the code in `__init__.py`? You can import it!

```python
# /ascs (the base directory) /ascs/abc/__init__.py
some_var = 5

# another_file.py
from ascs.abc import some_var
```

Read more about modules here: https://www.programiz.com/python-programming/modules

Read more about packages here: https://www.programiz.com/python-programming/package

## Pipe

Where appropriate we use the pandas `.pipe` function.

Before you might have seen code like this

```python
filtered_df = filter(df)
merged_1_df = merge_1(filtered_df, "some_argument")
merged_2_df = merge_2(merged_1_df)
df_dropped_na = merged_2_df.dropna()
stratified_df = stratify(merged_2_df, kwarg=8)
return stratified_df
```

This is bad because:

1. It is a lot of visual clutter
2. It is very easy to have a bug where you accidentally pass the wrong DataFrame in the middle step.
3. When writing code like this, the variable names get very long, and it is really tiring to have to think of variable names for every small step that you do.

You could instead do

```python
df = filter(df)
df = merge_1(df, "some_argument")
df = merge_2(df)
df = df.dropna()
df = stratify(df, kwarg=8)
return df
```

This is bad because:

1. It still contains a lot of visual clutter
2. It isn't best practice to assign a new and different object to an old object's variable

We have decided instead to write it as

```python
return (
    df.pipe(filter)
    .pipe(merge_1, "some_argument")
    .pipe(merge_2)
    .dropna()
    .pipe(stratify, kwarg=8)
)
```

Warning: If your function forgets to return a DataFrame/Series (or returns something that isn't a DataFrame or Series) then you cannot use pipe after.

<details>
<summary>What happens when you forget to put a return statement at the end of a function</summary>

```python
def add_abc_column(df: pd.DataFrame) -> pd.DataFrame:
    df["abc"] = 99

    # oh no! this function forgot to return the DataFrame

def higher_level_function(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.pipe(subfunction_1)
        .pipe(add_abc_column)
        .pipe(subfunction_2)
    )
```

You will see the error

```
AttributeError: 'NoneType' object has no attribute 'pipe'
```

because functions that return nothing return None.

</details>

Read more about pipe here: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pipe.html?highlight=pipe#pandas.DataFrame.pipe

## Use of classes

This codebase makes use of classes quite a lot, and for different reasons in each case.

### Params

See above.

### Stratification

We had a function that called a lot of other functions, and it was always having to pass through a lot of arguments. Classes avoid that.

<details>
<summary>See an example of how this works</summary>

```python
# The situation before

def perform_stratification(df: pd.DataFrame, argument_a, argument_b, argument_c, argument_d) -> pd.DataFrame:
    return (
        df.pipe(
            subfunction_1,
            argument_a,
            argument_c
        )
        .pipe(
            subfunction_2,
            argument_b,
        )
        .pipe(
            subfunction_3,
            argument_d
        )
    )

def subfunction_1(df: pd.DataFrame, argument_a, argument_b) -> pd.DataFrame:
    print(argument_a)
```

When you put something in a class, you can avoid passing through arguments, because they are in `self`.

```python
# The situation after
class Stratification:
    def __init__(self, argument_a, argument_b, argument_c, argument_d):
        self.argument_a = argument_a
        self.argument_b = argument_b
        self.argument_c = argument_c
        self.argument_d = argument_d

    def perform_stratification(self, df: pd.DataFrame) -> pd.DataFrame:
        print(self.argument_a)
```

</details>

### Stratified Tables

We had a lot of repeated code between tables 1, 2 and 3. A class allows us to get them sharing code and then override the bits that change.

<details>
<summary>See an example of how this works</summary>

The context of this example is that when we create the pivotted tables, we need to combine together multichoice questions (q21a, q21b, q21c -> q21).

For most of the tables we need to only combine together the columns.

For the table split by response we need to combine together the multichoice questions in the rows as well.

Here's how we adjust the base class "recipe" to do this in the subclass.

```python
class BaseStratifiedTables:
    ...

    def create_generic_pivotted_table(
        self,
        df_table_by_supergroup_question_response: pd.DataFrame,
        value_column: str,
        column_to_select_for_respondents: Union[str, Literal[None]],
    ) -> pd.DataFrame:
        return (
            df_table_by_supergroup_question_response.pipe(
                self.pivot, value_column=value_column
            )
            .pipe(self.combine_rows_and_columns_in_pivotted)
        )

    def combine_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        return df_table_by_supergroup.pipe(
            combine_multiple_choice, params.get_multi_choice_questions_with_exclude()
        )

    ...

class StratifiedByResponseTables(BaseStratifiedTables):
    ...

    # We override the method on the base class
    def combine_rows_and_columns_in_pivotted(
        self, df_table_by_supergroup: pd.DataFrame
    ) -> pd.DataFrame:
        return (
            # Calling super calls the method on the base class
            # Which combines the multi choice columns
            super()
            .combine_rows_and_columns_in_pivotted(df_table_by_supergroup)
            # After which we can combine the rows
            .pipe(self.combine_multiple_choice_rows)
        )

    def combine_multiple_choice_rows(
        self, generic_pivot_table: pd.DataFrame
    ) -> pd.DataFrame:
        return generic_pivot_table.T.pipe(
            combine_multiple_choice, params.MULTIPLE_CHOICE_QUESTIONS
        ).T
    ...
```

In this

</details>

Read the basics of inheritance in Python: https://www.w3schools.com/python/python_inheritance.asp

Read more about inheritance, overriding and `super()`: https://www.thedigitalcatonline.com/blog/2014/05/19/method-overriding-in-python/

## Type Hints

Type hints allow for VSCode to do autocomplete. They also serve as a form of documentation.

Read more about them here: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

## MultiIndexing

MultiIndexes are good and we should use more of them!

Avoid resetting a MultiIndex unless you have a reason.

Read an introduction to MultiIndexing here: https://towardsdatascience.com/how-to-use-multiindex-in-pandas-to-level-up-your-analysis-aeac7f451fce

Read more about MultiIndexing here: https://pandas.pydata.org/docs/user_guide/advanced.html

## Styling

We use the code formatter `black` to give the code a consistent, neat style.

Read more about black here: https://black.readthedocs.io/en/stable/

VSCode can help with formatting by automatically applying formatters, read more about using formatters in VSCode here: https://code.visualstudio.com/docs/editor/codebasics#_formatting

Read about VSCode settings for Python formatters here: https://code.visualstudio.com/docs/python/editing#_formatting

## Variable naming

The first principle we follow is to always follow the python style guide conventions on variable names.

[Python's official style guide](https://peps.python.org/pep-0008/#naming-conventions):

1. Normal variables and function names should use `underscore_names`
2. Constant variables should use `ALL_CAPS_UNDERSCORES`
3. Classes should use `CapitalisedWords`

Other principles we've tried to follow:

1. Use full words where possible. `demographic` instead of `demog`.

To get further than this we need some wider principles.

Variable naming rules from [Clean Code by Uncle Bob](https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29):

1. Choose descriptive and unambiguous names
2. Make meaningful distinction
3. Use pronouncable names
4. Use searchable names
5. Replace magic numbers with named constants
6. Avoid encodings. Don't append prefixes or type information.

Data presents a unique challenge to these rules, because in data you often have a process like this:

1. Start with a data frame from a survey
2. Add a demographic column with grouped demographic characteristics
3. Merge in some data about the local authority like the local authority name
4. Add another column derived from their answers to the questions

This DataFrame contains a lot of different forms of information, which defies easy naming. It has information about the people's survey responses, but also their demographics, and information about their local authority.

We had names of very large length. It was getting hard to type, and made the code cluttered.

We decided it would be better to base ourselves in the principle of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html).

In tidy data

1. Every column is a variable (like "q3a" or "percentage")
2. Every row is an observation (like one person, or one local authority)
3. Every cell is a single value (no cells containing values like "LA_211_Stratum_1")

The DataFrame object is a container that organises many different variables into rows. We decided:

1. The main thing the DataFrame does is organise the data in rows, therefore the main thing a DataFrame name should state is what the rows are.  
   If we are following Tidy Data Principles, each row is an observation, so this should be easy.

2. To name the rows, start the variable name `df_by` and then list all the things it is by.  
   In the DataFrame `df_by_la_question` I would expect one row to be a single combination of Local Authority and Question.  
   This does break the rule "no types in names" but the name `by_la_question` would look strange.

3. If the data comes from some obvious single source, it is acceptable to include that in the variable name, before the word `by`.  
   E.g: `df_questionnaire_by_person`.

4. The variable name of the overall DataFrame is not the place to describe what is in the columns. The column names are the place to describe what is in the columns.  
   This means no names like `df_questionnaire_with_population_and_la`.

5. Sometimes, it doesn't matter what the rows are. For example, in the output to excel function handles lots of DataFrames with various different types of rows. In this case, you can omit the `by_something` part of the variable name. You can just use `df`.

Some examples:

- `df_questionnaire_by_person`
- `df_by_supergroup_question_response` (one row is one combination of supergroup, question and response)
- `df_by_la`

If you see `df_questionnaire_by_person["q3a"]` then you can probably guess that the resulting series is people's answers to question 3a.

Column naming:

1. Follow the same variable naming conventions as for a normal Python variable.
2. Either the variable in the column has the same observation level as the DataFrame or you should state it.  
   `df_by_person["name"]` means the name of the person.  
   `df_by_person["la_name"]` means the name of the local authority (of the person).  
   `df_by_la_stratum["la_population"]` means the population of the local authority, not the population of the local authority stratum combination.
3. Avoid changing the column names from the original names in the input data for consistency. This is why our code uses "LaCode" as a column name everywhere.

Note: These ideas are easier to implement if you do use `.pipe` - see the pipe section in this document.

Series naming:

In a DataFrame, when you select a column, you know what the rows are and you know what the column is. When you read `df_by_teacher["weekly_contracted_hours"]` you can tell that it is going to be a series with the weekly contracted hours for every teacher. The variable name for a series should convey both the information in the column name, and in the DataFrame name. In this case, we would choose the variable name `weekly_contracted_hours_by_teacher`.

## Testing

If testing is completely new to you, [read more about it here](https://realpython.com/python-testing/).

We use [pytest](https://docs.pytest.org/en/7.1.x/). It is worth [reading about fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) because we make a lot of use of those.

We also use parameterizing a lot, read about it here: https://docs.pytest.org/en/6.2.x/parametrize.html

<details>
<summary>See why we use fixtures with scope="session"</summary>

We have a lot of tests that test the outputted data.

This would be slow:

```python
def test_1():
    table = create_table()  # This function takes 30 seconds to run

    assert table.loc[1, 1] == something

def test_2():
    table = create_table()  # This function takes 30 seconds to run

    assert table.loc[2, 2] == something_else

def test_3():
    table = create_table()  # This function takes 30 seconds to run

    assert table.loc[3, 3] == something_more
```

We run `create_table` 3 times to test the output in 3 different ways. It would be better to generate the table once and then to run the three different tests. Fixtures let us do this.

```python
@pytest.fixture(scope="session")
def table():
    return create_table()

def test_1(table):
    assert table.loc[1, 1] == something

def test_2(table):
    assert table.loc[2, 2] == something_else

def test_3(table):
    assert table.loc[3, 3] == something_more
```

Also, if we only want to run `test_1` we can, and it will generate the table without running `test_2` and `test_3`.

</details>

<details>
<summary>See how fixtures are intelligent when you want to run one specific test</summary>

Imagine we want to test only the DQ table. We have a setup like this:

```python
@pytest.fixture(scope="session")
def input_data():
    return get_input_data()  # Takes 5 seconds to run

@pytest.fixture(scope="session")
def table_dq(input_data):
    return calc_dq_table(input_data)  # Takes 10 seconds to run

@pytest.fixture(scope="session")
def table_annex(input_data):
    return create_annex_table(input_data)  # Takes 1 minute to run

def test_annex(table_annex):
    assert table_annex.loc[1, 1] == something

def test_dq(table_dq):
    assert table_annex.loc[1, 1] == something
```

If we tell pytest to only run `test_dq`, then pytest will look and see that `test_dq` needs `table_dq`. It will see that `table_dq` needs `input_data`. Therefore it will run

```
input_data -> table_dq -> test_dq
```

and will skip creating the annex table completely, which saves us 1 minute when running the tests.

If this example does not make sense to you, please read the pytest fixture docs again: https://docs.pytest.org/en/6.2.x/fixture.html

Note: Using VSCode you can select the specific tests you want to run easily. See how here: https://code.visualstudio.com/docs/python/testing

</details>

Using VSCode, we can very easily run only certain tests.

Read about how to do testing well in VSCode: https://code.visualstudio.com/docs/python/testing

Note: Tests are a good way to understand how code is meant to work. If you don't understand a function, read the test for it. Tests contain examples of how the code should work.

### Tests structure

**testing_outputs** - These are our end to end tests. They check that after the whole process is done, the numbers come out correct.

**integrationtests** - These test specific processes of the code. e.g loading data returns

**unittests** - These are the tests of the functions and little components of our system.

You will find that the structure of the unittests directory mirrors that of the real code. This is to make it easy to find where the tests for certain code are.

If you have a function `f` in `ascs/table3/random.py`, you can find the tests for `f` in `tests/unittests/table3/test_random.py`.

## Virtual Environments

Virtual environments and `requirements.txt` ensure that when you are working on code, everyone is using the same version of all the different packages. They also allow a project to easily get set up on a new computer.

Read more about virtual environments and `requirements.txt`: https://towardsdatascience.com/virtual-environments-104c62d48c54

Read a more comprehensive description of virtual environments and `requirements.txt`: https://realpython.com/python-virtual-environments-a-primer/

Virtual environments work very well with VSCode, ensure you have your virtual environment set up in VSCode.

Read more about virtual environments in VSCode here: https://code.visualstudio.com/docs/python/environments

## Git hooks

Git hooks allow you to run a script every time you commit code. We use ours to prepend the ticket number to the commit message.

If your branch name contains the ticket number (e.g. with the branch name `ASCS-145-docs`) you will see

```
(.venv) PS C:\Users\USERNAME\ascs> git commit -m "Updated terminology"
No JIRA ID referenced by commit message.
Use ASCS-145 from branch name? (y/n) y
Prepended ASCS-145 to commit message.
[ASCS-145-docs 384fa93] ASCS-145 Updated terminology
```

You can find the code for the git hooks in the `git-hooks` directory.

Warning: This git hook will mean that you cannot use VSCode's big "Commit" button. You will have to use git on the command line for committing.

Read more about git hooks: https://www.atlassian.com/git/tutorials/git-hooks

## Data Flow

The most accurate way to see how the data flows through the program is to read the code, and most of what is discussed here can be seen in `create_publication.py`.

Essentially the flow has the following steps:

1. Get the data needed for table creation

- Load it from the files
- Verify it
- Perform transformations to it that multiple tables will need (for example, adding columns for easy read questions)
- Also average rows are generated, because the average rows are needed in multiple outputs

2. Generate tables/outputs

- Table generation is done in multiple separate functions. Each function is in charge of creating one set of tables. One function may both generate table 2a and 2b for example.
- All tables take a [NamedTuple](https://realpython.com/python-namedtuple/) with all the data they need for table creation - like the questionnaire data.
- All tables return a dictionary of string keys to DataFrames. This is the tables they have generated labelled by name.
- You can choose in the menu which of those functions to run.

3. All the generated tables get combined into one dictionary
4. The generated tables are saved (to csv and excel)

This structure has worked well.

It has made it easy to put code into modules with high cohestion but low coupling.

Read more about cohesion here (warning - advanced comp sci concepts): https://en.wikipedia.org/wiki/Cohesion_(computer_science)

Read more about coupling here (warning - advanced comp sci concepts): https://en.wikipedia.org/wiki/Coupling_(computer_programming)

A short summary of why this is good, is that when we change the code for one output, we only have to change the code in one little coherent module, rather than having to change a million things throught various files in the codebase.

Also, when we are developing a new output, we have the ability to run only the code needed to generate that specific output. We don't have to wait for other slow outputs to run. We are then able to run the code more and hence develop faster.

Plus, this structure of data flow makes it really really easy to create good test fixtures in pytest. To see how this works, it is easiest to read the code. It has allowed us to create tests for particular outputs that can run really quickly, creating a fast feedback loop.
