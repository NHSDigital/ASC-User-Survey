# Checkpoints

Loading excel files is an intensive task. This means that the process of loading data returns takes a long time.
For 2022, loading all excel data returns could take 45 minutes.
This is bad, because if you need to quickly rerun the code (to make a different output for instance, or because you needed to make changes to the params JSON, or because you're doing development work) you do not want to wait 45 minutes for the excel loading process to happen.

Due to this we created a checkpoint system.
When the code is run, and the excel data returns have been loaded, a checkpoint is created.
When the code is run again, the checkpoint can be used instead of loading the excel data returns again.

The checkpoint file stores the loaded data and is saved as a h5 file.
This is a way to save a pandas dataframe to a file whilst also saving the metadata (e.g column datatypes) of the dataframe.
Another reason we chose to use a h5 file is because it allows us to easily save multiple dataframes in one file.
Each dataframe is saved with a key that uniquely identifies it within the file.

If a checkpoint file exists then the user can decide whether to load the data returns from a checkpoint file or from the excel files.
