# Adult Social Care Survey (ASCS)

The adult social care survey asks people who are over 18 and who use adult social care about their experiences. This questionnaire is run every year. The questionnaire looks at how these services are helping people to live safely and independently in their own homes. Survey data is collected by local authorities and then NHS Digital collates the data and releases the publication.

This repository contains the python code used to generate all of the outputs from the publication from the input data. Many of these outputs are published publically at the links below. The input data is generally an excel sheet data return from the councils with information about their populations, and the survey responses they collected.

Information on how the survey is collected (including questionnaire material):
https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/social-care-user-surveys

Survey publication (including the output annex tables that this script generates):
https://digital.nhs.uk/data-and-information/publications/statistical/personal-social-services-adult-social-care-survey

**_For any queries please email enquiries@nhsdigital.nhs.uk_**

## New to the repository?

You should [take a look at our documentation folder](docs). It contains a ton of information about how the data flows, the design decisions we've made, and what the data looks like.

## Initial package set up

Run the following command to set up your environment correctly from the root directory (the top level `ascs` folder).

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\git-hooks\setup-hooks.py
```

For Visual Studio Code it is necessary that you change your default interpreter to the virtual environment you just created `.venv`. To do this use the shortcut `Ctrl-Shift-P`, search for `Python: Select interpreter` and select `.venv` from the list.

**Please do not use the VS Code Git Tab to commit as this will no longer work.**

_However, you can use it for adding files to be committed._

if the packages have updated and you need to install the new ones after pulling the new changes, please run

```
python -m pip install -r requirements.txt
```

You can read about the virtual environments we've created, and the git hooks we've implemented in `docs/design_decisions.md`

## Running the code

The code will run with the settings in the params JSON file you select, read more below.

You can create the publication (from the base directory) using

```
python -m ascs.create_publication
```

and answering all of the question prompts that it gives you.

## Testing the code

You can run the tests on the repository using (from the base directory)

```
pytest
```

Please read more about this topic in `docs/design_decisions.md`.

## Working on the code

### Changing the params JSON

Running the publication has lots of specific settings. For instance, it has to know what order to output the columns in for table 1a.

We save these settings in JSON files, which you can find in the `params_json` folder.

Each file contains one configuration, and you will be able to pick which configuration to use in the menu that you see when you run the code.

When there is a new year of the survey and if the new survey year has different settings, then we recommend that you create a new JSON file with the settings for that year.

To make that new JSON file, we recommend copying an old one and then changing those settings that need to be changed.

A comprehensive list of the properties and their types can be found in `ascs/params_utils/params.py`.

You can read more about the design of the params system in `docs/design_decisions.md`

### Changing the installed packages

If, while developing this package, you change the installed packages, please update the environment file using

```
pip freeze > requirements.txt
```

You can read more about virtual environments and dependency management in `docs/design_decisions.md`

## Package structure

The main steps of the code are documented in `ascs/create_publication.py`

We recommend reading the code from there and then following all of the functions that it calls to get an idea of the flow of the program.

### Chi squared tests for independence - R code

Within `archives/` there is some R code that runs significance testing using chi squared tests. This code is run separately to the main script.

## Other documentation

Please see [the documentation folder](docs). It is recommended to read the entire folder when you are new to the repository.
