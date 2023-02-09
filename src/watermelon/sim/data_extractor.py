"""
watermelon.sim.data_extractor
-----------------------------
Code that defines the class that extracts data from the simulation
and transforms it into the correct format.
"""

import pandas as pd


class DataFrameExtractor:
    """Object that extracts data into a pandas.DataFrame object.

    In the dataframe that is created, there are columns which indicate
    each agent involved in the graph. Each row has a timestamp and
    indicates the state of each agent at every instant.
    """

    def __init__(self, agents, initial_state):
        self.data = pd.DataFrame(self.parse_data(agents, initial_state, 0))

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
