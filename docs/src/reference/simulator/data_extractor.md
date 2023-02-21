# Data extractors

## What is a data extractor
A data extractor in *watermelon* is an object that stores all the data of the simulation in some desired format. In the code, these are classes that inherit from the `SimulationDataExtractor` trait, which must implement the `_initialize()`, `_append()` methods and the `extract_data()` static method. The purpose of these is:

- `_initialize()`: Initialize the `data` attribute to the necessary data type. This depends on the implementation.
- `_append()`: This is called on each iteration of the simulation, and its implementation depends on the type of the stored data.
- `extract_data()`: This static method is the one that extracts data from the `SimulatorData` object. It must return data in a format that `_initialize` and `_append` can understand.

Something important to note is that, similar to how agent actions are handled internally, while the methods that are implemented are `_initialize` and `_append`, when using *watermelon* you have to call `initialize` and `append` instead, respectively. These methods handle the data formatting and extraction internally.

Another thing to note is that, while `extract_data()` takes an instance of the `SimulatorData` object, because of duck typing and the way the data is laid out you can directly pass it an instance of `Simulator` instead, and the data will be extracted from the current state without any issue.

## Default implementations
### Pandas `DataFrameExtractor`
Currently, the only implemented data extractor (and thus the one that `Simulator` uses by default) is `DataFrameExtractor`, which stores the data as a `pandas.DataFrame` object. In this DataFrame, each column represents an agent and each row a time step, and every cell contains a `DataElement` object that handles the storing of the current and past decision, as well as the state of each agent. It also handles how the data is displayed to the users.
