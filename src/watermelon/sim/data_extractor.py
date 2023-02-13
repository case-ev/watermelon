"""
watermelon.sim.data_extractor
-----------------------------
Code that defines the class that extracts data from the simulation
and transforms it into the correct format.
"""

import abc
import dataclasses
import pandas as pd

from watermelon.model.state import AgentState
from watermelon.model.actions import Decision


@dataclasses.dataclass
class DataElement:
    """Element of simulation data of an agent"""

    decision: Decision
    state: AgentState

    def __str__(self):
        result = f"{str(self.decision)}, {100 * self.state.soc:.1f}%, \
time={self.state.action_time:.2f} "
        if self.state.is_travelling[0]:
            result += "[T]"
        if self.state.is_done:
            result += "[F]"
        if self.state.is_waiting:
            result += "[W]"
        if self.state.out_of_charge:
            result += "[D]"
        if self.state.overcharged:
            result += "[O]"
        return result


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
        self.initialize(self.extract_data(state))

    def initialize(self, data):
        self.data = pd.DataFrame(data)

    def append(self, simulation_state):
        """Get the data from the simulator and append it"""
        data = self.extract_data(simulation_state)
        self.data = pd.concat([self.data, pd.DataFrame(data)], ignore_index=True)

    @staticmethod
    def extract_data(simulation):
        """Extract some input data according to the required format"""
        return {
            **{"time": [simulation.time]},
            **{
                a: DataElement(a.actions[a.state.current_action], a.state.copy())
                for a in simulation.agents
            },
        }
