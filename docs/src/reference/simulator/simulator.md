# Simulator functionality

## How it works
The simulator is contained by the `Simulator` class, which is the object that determines the parameters that the simulation uses. This object contains two attributes `params` and `control`, which are instances of the classes `SimulationParameters` and `SimulationControl`, respectively.

`SimulationParameters` handles the parameters of "the world", i.e. things like the efficiency of batteries. These are all attributes that are shared amongst all agents, and are intended to be changeable by the user.

On the other hand, the `SimulationControl` class handles properties and information of the simulation itself, such as the current simulation time, which time step to use, the data extractor (of which we talk about in [Data extractors](data_extractor.md)), etc.
