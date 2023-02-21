# Data extractors

## What is a data extractor
A data extractor in *watermelon* is an object that stores all the data of the simulation in some desired format. In the code, these are classes that inherit from the `SimulationDataExtractor` trait, which must implement the `_initialize()`, `_append()` methods and the `extract_data()` static method. The purpose of these is:

- `_initialize()`: Initialize the `data` attribute to the necessary data type. This depends on the implementation.
- `_append()`: This is called on each iteration of the simulation, and its implementation depends on the type of the stored data.
- `extract_data()`: This static method is the one that extracts data from the `Simulator` object. It must return data in a format that `_initialize` and `_append` can understand.

Something important to note is that, similar to how agent actions are handled internally, while the methods that are implemented are `_initialize` and `_append`, when using *watermelon* you have to call `initialize` and `append` instead, respectively. These methods handle the data formatting and extraction internally.
