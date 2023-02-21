"""
watermelon.sim.simulation_data
------------------------------
Objects that store the data of simulations.
"""

import dataclasses
from typing import List

from watermelon import Agent, Graph
from watermelon.sim.parameters import SimulationControl, SimulationParameters


@dataclasses.dataclass
class SimulationData:
    """Raw data extracted from the simulation"""

    graph: Graph
    agents: List[Agent]
    control: SimulationControl
    params: SimulationParameters
