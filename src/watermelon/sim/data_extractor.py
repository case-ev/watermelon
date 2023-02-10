"""
watermelon.sim.data_extractor
-----------------------------
Code that defines the class that extracts data from the simulation
and transforms it into the correct format.
"""

import abc

import pandas as pd


class SimulationDataExtractor(abc.ABC):
    """Abstract class for an object that extracts data from a simulation"""

    @abc.abstractmethod
    def initialize(self, data):
        """Initialize the extractor"""

    @abc.abstractmethod
    def append(self, simulation_state):
        """Add new data"""


class DataFrameExtractor(SimulationDataExtractor):
    """Object that extracts data into a pandas.DataFrame object.

    In the dataframe that is created, there are columns which indicate
    each agent involved in the graph. Each row has a timestamp and
    indicates the state of each agent at every instant.
    """

    def __init__(self, state):
        self.data = None
        self.initialize(
            self.parse_data(state.agents, [a.actions[0] for a in state.agents], 0)
        )

    def initialize(self, data):
        self.data = pd.DataFrame(data)

    def append(self, simulation_state):
        """Get the data from the simulator and append it"""
        data = self.parse_data(
            simulation_state.agents, simulation_state.state, simulation_state.time
        )
        self.data = pd.concat([self.data, pd.DataFrame(data)], ignore_index=True)

    @staticmethod
    def parse_data(agents, state, time=0):
        """Parse some input data according to the required format"""
        return {
            **{"time": [time]},
            **dict(zip(agents, state)),
        }
