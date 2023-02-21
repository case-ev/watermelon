"""
watermelon.sim.data_extractor
-----------------------------
Code that defines the class that extracts data from the simulation
and transforms it into the correct format.
"""

import abc
import dataclasses
import pandas as pd

from watermelon.model.agent import AgentState, Decision


@dataclasses.dataclass
class DataElement:
    """Element of simulation data of an agent"""

    decision: Decision
    state: AgentState
    prev_decision: Decision = None

    def __str__(self):
        soc_str = f"{100 * self.state.soc:.1f}"
        if self.state.is_travelling[0]:
            vertex_str = (
                f"({str(self.prev_decision.vertex)}->{str(self.decision.vertex)})"
            )
        else:
            vertex_str = f"{str(self.decision)}"
        time_str = f"{self.state.action_time:.2f}"

        result = f"{soc_str}% @ {vertex_str}, {time_str}min"
        if self.state.is_done:
            result = f"FINISHED, {time_str}min"
        if self.state.is_waiting:
            result = f"WAITING, {soc_str}% @ {vertex_str}, {time_str}min"
        if self.state.out_of_charge:
            result = f"OOC @ {vertex_str}, {time_str}min"

        if self.state.overcharged:
            result += "[O]"
        return result


class SimulationDataExtractor(abc.ABC):
    """Abstract class for an object that extracts data from a simulation"""
    def __init__(self, simulation_state) -> None:
        self._data = None
        self.initialize(simulation_state)

    @property
    def data(self):
        """Contained data of the simulation"""
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @abc.abstractmethod
    def _initialize(self, data):
        """Initialize the extractor"""

    @abc.abstractmethod
    def _append(self, data):
        """Add new data"""

    @staticmethod
    @abc.abstractmethod
    def extract_data(simulation_state):
        """Extract the required data from the simulation"""

    def initialize(self, simulation_state):
        """Initialize the data extractor.

        This method handles the extraction of the data internally.

        Parameters
        ----------
        simulation_state : Simulator
            Object that handles the simulation and contains the data associated
            to the current time step.
        """
        return self._initialize(self.extract_data(simulation_state))

    def append(self, simulation_state):
        """Append some new data.

        This method handles the extraction of the data internally.

        Parameters
        ----------
        simulation_state : Simulator
            Object that handles the simulation and contains the data associated
            to the current time step.
        """
        return self._append(self.extract_data(simulation_state))


class DataFrameExtractor(SimulationDataExtractor):
    """Object that extracts data into a pandas.DataFrame object.

    In the dataframe that is created, there are columns which indicate
    each agent involved in the graph. Each row has a timestamp and
    indicates the state of each agent at every instant.
    """

    def _initialize(self, data):
        self.data = pd.DataFrame(data)

    def _append(self, data):
        self.data = pd.concat([self.data, pd.DataFrame(data)], ignore_index=True)

    @staticmethod
    def extract_data(simulation_state):
        states = {}
        for a in simulation_state.agents:
            i = a.state.current_action
            if i != 0:
                states[a] = DataElement(a.actions[i], a.state.copy(), a.actions[i - 1])
            else:
                states[a] = DataElement(a.actions[i], a.state.copy(), None)
        return {"time": [simulation_state.time], **states}
